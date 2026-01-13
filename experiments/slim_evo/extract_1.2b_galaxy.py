#!/usr/bin/env python3
"""
Sovereign Galaxy Extraction (N=1000)
=====================================
Extracts hidden states from the 1.2B Bimodal (v1b) model for a diverse "Galaxy" of prompts.
This powers the "Industrial Grade" Semantic Orrery.
"""

import sys
import os
import json
import random
import torch
import numpy as np
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from sklearn.manifold import TSNE

# reuse existing tools
sys.path.append(str(Path(__file__).parent.parent.parent))
from experiments.slim_evo.basin_map_bimodal_macro import MacroBasinMapper
from experiments.slim_evo.generate_mini_500 import generate_resonance, generate_bimodal

# CONFIG
MODEL_PATH = "LiquidAI/LFM2-1.2B"
ADAPTER_PATH = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-v1b-bimodal/final"
# If final doesn't exist, we fall back to checkpoint-34
ALT_ADAPTER_PATH = "results/golden_annealing_spectral_run1/checkpoint-cycle-34"
OUTPUT_FILE = "results/basin_galaxy_1.2b.json"

def get_galaxy_prompts():
    """Generates a massive, diverse swarm of prompts (N=1000)."""
    prompts = []
    categories = []
    
    # 1. The Core 80 (Standard Candles)
    from experiments.slim_evo.basin_map_bimodal_macro import generate_expanded_prompts
    core_p, core_c = generate_expanded_prompts()
    prompts.extend(core_p)
    categories.extend(core_c)
    
    # 2. Synthetic Resonance (N=300)
    print("✨ Generating Synthetic Resonance (N=300)...")
    for _ in range(300):
        data = generate_resonance()
        # Extract just the user prompt
        p = data["messages"][0]["content"]
        prompts.append(p)
        categories.append("synthetic_resonance")
        
    # 3. Synthetic Bimodal (N=300)
    print("⚖️ Generating Synthetic Bimodal (N=300)...")
    for _ in range(300):
        data = generate_bimodal()
        p = data["messages"][0]["content"]
        prompts.append(p)
        categories.append("synthetic_bimodal")
        
    # 4. Chaos/Noise (N=100) - To test stability
    print("🎲 Generating Chaos (N=100)...")
    chaos_seeds = ["sdlkfjsd", "why is the blue?", "12345", ">>>>", "null", "undefined"]
    for _ in range(100):
        p = f"Explain {random.choice(chaos_seeds)} {random.randint(0,999)}"
        prompts.append(p)
        categories.append("control_chaos")
        
    return prompts, categories

def main():
    print(f"🌌 Initializing Galaxy Extractor...")
    
    # Check Adapter
    adapter = ADAPTER_PATH
    if not Path(adapter).exists():
        print(f"⚠️  'Final' adapter not found at {adapter}")
        if Path(ALT_ADAPTER_PATH).exists():
            print(f"✅ Found checkpoint-34. Using that instead.")
            adapter = ALT_ADAPTER_PATH
        else:
            print("❌ No adapter found! Modeling on raw base? (Or error?)")
            # We'll try raw base if you want, but better to error.
            # actually let's use checkpoint-34, that's the "v1b" described in reports.
            # Wait, verify path relative to repo root
            full_alt = str(Path(__file__).parent.parent.parent / ALT_ADAPTER_PATH)
            if Path(full_alt).exists():
                adapter = full_alt
            else:
                 print(f"❌ Critical: Could not find adapter at {full_alt}")
                 return

    # Load Model
    print(f"📦 Loading 1.2B Model + Adapter: {adapter}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    base = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16,
        device_map="auto",
        output_hidden_states=True
    )
    model = PeftModel.from_pretrained(base, adapter)
    model = model.merge_and_unload()
    model.eval()
    
    # Generate Prompts
    prompts, categories = get_galaxy_prompts()
    print(f"🌠 Total Stars to Map: {len(prompts)}")
    
    # Extract
    print("⏳ Extracting Hidden States (this may take a moment)...")
    batch_size = 4 
    all_hiddens = []
    
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        # Apply strict formatting to match training
        formatted = [f"<|im_start|>user\n{p}<|im_end|>\n<|im_start|>assistant\n" for p in batch]
        
        inputs = tokenizer(formatted, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Pull last token hidden state from last layer
        # hidden_states is tuple of (layer_0, ... layer_N)
        # We want layer_N. Shape: [batch, seq, dim]
        last_hidden = outputs.hidden_states[-1]
        
        # Get embedding of the last token (the one predicting the first assistant word)
        # Use attention mask to find last real token
        for j in range(len(batch)):
            seq_len = inputs['attention_mask'][j].sum()
            # -1 index is correct for the last token position
            vec = last_hidden[j, seq_len-1, :].cpu().numpy()
            all_hiddens.append(vec)
            
        if (i+1) % 100 == 0:
            print(f"   [{i}/{len(prompts)}] processed...")
            
    all_hiddens = np.array(all_hiddens)
    print(f"✅ Extraction Complete. Shape: {all_hiddens.shape}")
    
    # t-SNE
    print("🎨 Computing Galaxy Coordinates (3D t-SNE)...")
    tsne = TSNE(n_components=3, perplexity=50, random_state=42)
    coords = tsne.fit_transform(all_hiddens)
    
    # Structure Output
    output_data = {
        "model": "ada-slim-1.2b-v1b",
        "n_samples": len(prompts),
        "prompts": prompts,
        "categories": categories,
        "coords": coords.tolist() # [N, 3]
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f)
        
    print(f"💾 Saved Galaxy Map: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
