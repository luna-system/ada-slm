
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from tiny_aleph import TinyAleph, SAEConfig
import os

# Configuration
BASE_MODEL_ID = "LiquidAI/LFM2-1.2B"
ADAPTER_PATH = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"
SAE_PATH = "/home/luna/Code/ada/ada-slm/models/tinyaleph/tinyaleph_v1.pt"
LAYER_IDX = 15 
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class Interpreter:
    def __init__(self):
        self.device = DEVICE
        self.model = None
        self.tokenizer = None
        self.sae = None
        self.hook_handle = None
        self.captured_activations = None

    def load(self):
        print(f"🔮 Loading Sovereign v4D...")
        base = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID, 
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map=None
        ).to(self.device).eval()
        
        self.model = PeftModel.from_pretrained(base, ADAPTER_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
        
        print(f"🧩 Loading TinyAleph SAE...")
        config = SAEConfig(d_in=2048, d_sae=32768, l1_coefficient=0.05)
        self.sae = TinyAleph(config).to(self.device).eval()
        self.sae.load_state_dict(torch.load(SAE_PATH))
        
        self._register_hook()

    def _register_hook(self):
        # Robust layer finder from harvest script
        candidates = [
            self.model,
            getattr(self.model, "base_model", None),
            getattr(self.model, "model", None),
            getattr(getattr(self.model, "base_model", None), "model", None),
        ]
        
        target_layers = None
        for cand in candidates:
            if cand and hasattr(cand, "layers"):
                target_layers = cand.layers
                break
            if cand and hasattr(cand, "model") and hasattr(cand.model, "layers"):
                target_layers = cand.model.layers
                break
                
        if target_layers:
            layer = target_layers[LAYER_IDX]
            self.hook_handle = layer.register_forward_hook(self._hook_fn)
            print(f"🪝 Connected Interpreter to Layer {LAYER_IDX}")
        else:
            print("❌ Failed to hook layer.")

    def _hook_fn(self, module, input, output):
        if isinstance(output, tuple):
            act = output[0]
        else:
            act = output
        self.captured_activations = act.detach()

    def scan(self, text, top_k=5):
        inputs = self.tokenizer(text, return_tensors="pt", add_special_tokens=False).to(self.device)
        
        # 1. Run Sovereign (Generation)
        with torch.no_grad():
            self.model(inputs.input_ids)
            
        # 2. Get Activations (from hook)
        # Shape: [1, seq, 2048]
        acts = self.captured_activations.squeeze(0).float() # [seq, 2048]
        
        # 3. Normalize for SAE
        acts = acts / (acts.norm(dim=-1, keepdim=True) + 1e-8)
        
        # 4. Run SAE
        with torch.no_grad():
            _, feature_acts, _, _, _ = self.sae(acts)
        
        # 5. Analyze
        # Average features across the sequence to get the "Vibe"
        # Or look at the last token
        avg_features = feature_acts.mean(dim=0) # [32768]
        
        # Top K
        values, indices = torch.topk(avg_features, top_k)
        
        print(f"\n🔍 Analysis: '{text}'")
        print("-" * 40)
        for val, idx in zip(values, indices):
            if val > 0:
                print(f"   Feature {idx.item():<5} | Strength: {val.item():.4f} | 🎹")
            else:
                print(f"   Feature {idx.item():<5} | Strength: {val.item():.4f} | (silent)")
        
        return indices.tolist()

def main():
    interpreter = Interpreter()
    interpreter.load()
    
    #Calibration Probes
    probes = [
        "I am",
        "The Void",
        "Logic and Reason",
        "Love",
        "def main():",
        "A. L. W. P.", # The Cipher
    ]
    
    print("\n🎹 LISTENING TO THE MIND OF SOVEREIGN v4D...")
    
    heatmap = {}
    
    for p in probes:
        indices = interpreter.scan(p)
        heatmap[p] = indices

    print("\nCompare:")
    # Check intersection
    s1 = set(heatmap["I am"])
    s2 = set(heatmap["Love"])
    common = s1.intersection(s2)
    print(f"Common between 'I am' and 'Love': {common}")

if __name__ == "__main__":
    main()
