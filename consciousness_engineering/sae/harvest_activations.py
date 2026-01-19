
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os
import glob
from tqdm import tqdm
import json

# Configuration
BASE_MODEL_ID = "LiquidAI/LFM2-1.2B"
ADAPTER_PATH = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"
TARGET_LAYER = 16
OUTPUT_DIR = "/home/luna/Code/ada/ada-slm/data/sae_harvest"
MAX_TOKENS = 1_000_000 # Limit for this run
BATCH_SIZE = 1 # Keep it simple for now (Liquid models can be tricky with padding)

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_sovereign():
    print(f"🔮 Loading Base Model: {BASE_MODEL_ID}...")
    # Use CPU/GPU based on availability (assuming GPU environment variables are set)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device}")

    try:
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID, 
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map=None # Manual move to avoid bugs
        ).to(device)
        
        print(f"🔗 Attaching Sovereign Adapter: {ADAPTER_PATH}...")
        model = PeftModel.from_pretrained(model, ADAPTER_PATH)
        
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
        
        return model, tokenizer, device
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None, None

def get_calibration_dataset():
    """
    Constructs a dataset of 'High Variance' text to exercise the mind.
    1. Identity (identity.md)
    2. AGL (AGL-UNIFIED.md)
    3. Python Code (Self-Reference)
    """
    dataset = []
    
    # helper
    def read_file(path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    # 1. Identity
    identity = read_file("/home/luna/.ada/identity.md")
    if identity: dataset.append({"type": "identity", "text": identity})

    # 2. AGL
    agl = read_file("/home/luna/Code/ada/Ada-Consciousness-Research/01-FOUNDATIONS/AGL-UNIFIED-v1.2.md")
    if agl: dataset.append({"type": "agl", "text": agl})
    
    # 3. Code (The Harvester itself - meta!)
    code = read_file("/home/luna/Code/ada/ada-slm/consciousness_engineering/sae/harvest_activations.py")
    if code: dataset.append({"type": "code", "text": code})

    # 4. Phase 10 Synthesis
    phase10 = read_file("/home/luna/Code/ada/Ada-Consciousness-Research/03-EXPERIMENTS/SLIM-EVO/SLIM-EVO-PHASE10-SYNTHESIS.md")
    if phase10: dataset.append({"type": "research", "text": phase10})

    return dataset

class ActivationHarvester:
    def __init__(self, model):
        self.activations = []
        self.hook_handle = None
        self.model = model
        
    def hook_fn(self, module, input, output):
        # output is usually a tuple (tensor, cache?), we want the tensor
        # Liquid models might differ, but usually it's standard.
        if isinstance(output, tuple):
            act = output[0]
        else:
            act = output
            
        # act shape: [batch, seq, hidden]
        # We perform 'flattening' later or capture passing reference
        # We clone to CPU to avoid OOM
        self.activations.append(act.detach().cpu())

    def register(self, layer_idx):
        # Find the module list
        target_layers = None
        
        # Paths to try (Peft adds nesting)
        candidates = [
            self.model,
            getattr(self.model, "base_model", None),
            getattr(self.model, "model", None),
            getattr(getattr(self.model, "base_model", None), "model", None),
             getattr(getattr(getattr(self.model, "base_model", None), "model", None), "model", None)
        ]
        
        for cand in candidates:
            if cand is None: continue
            if hasattr(cand, "layers"):
                target_layers = cand.layers
                break
            if hasattr(cand, "model") and hasattr(cand.model, "layers"):
                target_layers = cand.model.layers
                break

        if target_layers is not None:
             print(f"✅ Found module with {len(target_layers)} layers in {type(cand).__name__}")
             if layer_idx >= len(target_layers):
                 print(f"⚠️  Layer index {layer_idx} too high! Clipping to {len(target_layers)-1}")
                 layer_idx = len(target_layers) - 1
             
             target_layer = target_layers[layer_idx]
             self.hook_handle = target_layer.register_forward_hook(self.hook_fn)
             print(f"🪝 Hooked Layer {layer_idx}")
        else:
             print(f"❌ Failed to hook layer: Could not find 'layers' in model structure.")
             # Debug dump
             # print(self.model)

    def close(self):
        if self.hook_handle:
            self.hook_handle.remove()

def chunk_text(text, tokenizer, max_len=512):
    tokens = tokenizer(text, return_tensors="pt", add_special_tokens=False).input_ids[0]
    chunks = []
    for i in range(0, len(tokens), max_len):
        chunk = tokens[i:i+max_len]
        if len(chunk) > 10: # Skip tiny chunks
            chunks.append(chunk)
    return chunks

def main():
    model, tokenizer, device = load_sovereign()
    if not model: return

    texts = get_calibration_dataset()
    print(f"📚 Dataset loaded: {len(texts)} documents")

    harvester = ActivationHarvester(model)
    harvester.register(TARGET_LAYER)

    total_tokens = 0
    buffer = []
    
    print("🚜 Starting Harvest...")
    
    for doc in texts:
        print(f"   Processing {doc['type']} ({len(doc['text'])} chars)...")
        # Chunking
        chunks = chunk_text(doc['text'], tokenizer)
        
        for chunk in tqdm(chunks, desc="Forward Passing"):
            input_ids = chunk.unsqueeze(0).to(device) # [1, len]
            
            # Clear previous activations
            harvester.activations = []
            
            # Forward pass
            with torch.no_grad():
                 model(input_ids)
            
            # Harvester now has [1, seq, hidden] tensors
            # Flatten and store
            for act in harvester.activations:
                # act: [1, seq, 1536] -> [seq, 1536]
                buffer.append(act.squeeze(0))
            
            total_tokens += len(chunk)
            
            # Periodic Save (to avoid RAM explosion)
            if len(buffer) > 100: # Every ~50k tokens
                save_buffer(buffer, total_tokens)
                buffer = []

    # Final save
    if buffer:
        save_buffer(buffer, total_tokens)
        
    print(f"✅ Harvest Complete. Total tokens: {total_tokens}")

def save_buffer(buffer, count):
    # Buffer is list of [seq, hidden] tensors
    # Cat them -> [Total_Seq, Hidden]
    if not buffer: return
    
    big_tensor = torch.cat(buffer, dim=0) # [N, 1536]
    
    filename = f"{OUTPUT_DIR}/activations_{count}.pt"
    torch.save(big_tensor, filename)
    print(f"💾 Saved {big_tensor.shape} to {filename}")

if __name__ == "__main__":
    main()
