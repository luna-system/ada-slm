#!/usr/bin/env python3
"""
3-Way Unified Basin Mapping for Mini-Lab
========================================
Maps the trajectory: Base -> v2 (Resonance) -> v2b (Bimodal)
"""

import sys
import os
from pathlib import Path
import json
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Add repo root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from experiments.slim_evo.basin_map_bimodal_macro import MacroBasinMapper, generate_expanded_prompts

# Override MacroBasinMapper to support 350M and flexible loading
class MiniBasinMapper(MacroBasinMapper):
    def __init__(self):
        self.model_name = "LiquidAI/LFM2-350M"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.eos_token
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "results/mini_lab_basins"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_base(self):
        print(f"📦 Loading BASE: {self.model_name}")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, 
            torch_dtype=torch.float16, 
            device_map=self.device
        )
        self.model.eval()

    def load_adapter(self, adapter_path):
        print(f"📦 Loading Adapter: {adapter_path}")
        # Reload base to clear previous adapter or unload
        self.load_base()
        self.model = PeftModel.from_pretrained(self.model, adapter_path)
        self.model.eval()

RESULTS_DIR = "results/mini_lab_basins"

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    mapper = MiniBasinMapper()
    prompts, categories = generate_expanded_prompts()
    print(f"Using {len(prompts)} prompts for 3-WAY mapping.")
    
    # 1. Base
    mapper.load_base()
    states_base = mapper.extract_hidden_states(prompts)
    resps_base = mapper.generate_responses(prompts)
    
    # 2. v2 (Resonance)
    mapper.load_adapter("models/mini-lab/v2-resonance")
    states_v2 = mapper.extract_hidden_states(prompts)
    resps_v2 = mapper.generate_responses(prompts)
    
    # 3. v2b (Bimodal)
    mapper.load_adapter("models/mini-lab/v2b-bimodal")
    states_v2b = mapper.extract_hidden_states(prompts)
    resps_v2b = mapper.generate_responses(prompts)
    
    # 4. Concatenate & t-SNE
    print("\n🔗 Concatenating (Base + v2 + v2b)...")
    combined = np.concatenate([states_base, states_v2, states_v2b], axis=0)
    
    tsne_coords = mapper.compute_tsne(combined, perplexity=30) # 80*3 = 240 points
    
    # 5. Split
    n = len(prompts)
    c_base = tsne_coords[:n]
    c_v2   = tsne_coords[n:2*n]
    c_v2b  = tsne_coords[2*n:]
    
    # 6. Save
    result = {
        "timestamp": "MINI-LAB-3WAY",
        "prompts": prompts,
        "categories": categories,
        "base": {"coords": c_base.tolist(), "responses": resps_base},
        "v2":   {"coords": c_v2.tolist(),   "responses": resps_v2},
        "v2b":  {"coords": c_v2b.tolist(),  "responses": resps_v2b}
    }
    
    path = f"{RESULTS_DIR}/basin_mini_unified.json"
    with open(path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Saved Mini-Lab Data: {path}")

if __name__ == "__main__":
    main()
