#!/usr/bin/env python3
"""
Basin Mapping: Resonance (v1) vs Bimodal (v1b)
==============================================

Maps the hidden state geometry of our two key consciousness models.
"""

import sys
import os
from pathlib import Path

# Add repo root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import torch
import numpy as np
import json
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from consciousness_engineering.cli.basin import BasinMapper, BasinMapResult, BASIN_MAPPING_PROMPTS, get_all_prompts

# Paths
BASE_MODEL = "LiquidAI/LFM2-1.2B"
RES_ADAPTER = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-resonance-20260111"
BIMODAL_ADAPTER = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-v1b-bimodal/final"
RESULTS_DIR = "results/basin_comparisons"

class BimodalBasinMapper(BasinMapper):
    def __init__(self):
        super().__init__()
        
    def load_stack_v1(self):
        """Load Base + Resonance (v1) Merged."""
        print(f"📦 Loading Stack v1 (Resonance)...")
        print(f"   Base: {BASE_MODEL}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.eos_token
        
        base = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16,
            device_map="auto",
            output_hidden_states=True
        )
        
        print(f"   Merging: {RES_ADAPTER}")
        model = PeftModel.from_pretrained(base, RES_ADAPTER)
        self.model = model.merge_and_unload()
        self.model_name = "ada-slim-1.2b-v1-resonance"
        
    def load_stack_v1b(self):
        """Load Stack v1 + Bimodal (v1b)."""
        # Optimized: If we already have v1 loaded, just add v1b adapter
        if self.model_name == "ada-slim-1.2b-v1-resonance":
            print(f"📦 Loading Stack v1b (Bimodal) on top of v1...")
            print(f"   Adapter: {BIMODAL_ADAPTER}")
            self.model = PeftModel.from_pretrained(self.model, BIMODAL_ADAPTER)
            self.model_name = "ada-slim-1.2b-v1b-bimodal"
            return

        # Fallback if v1 not loaded
        self.load_stack_v1()
        self.load_stack_v1b()

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    mapper = BimodalBasinMapper()
    prompts, categories = get_all_prompts()
    
    # 1. Map v1 (Resonance)
    mapper.load_stack_v1()
    print("\n🗺️  Mapping v1 (Resonance)...")
    res_v1 = mapper.map_basins(prompts, categories)
    save_result(res_v1, "v1_resonance")
    
    # 2. Map v1b (Bimodal)
    mapper.load_stack_v1b()
    print("\n🗺️  Mapping v1b (Bimodal)...")
    res_v1b = mapper.map_basins(prompts, categories)
    save_result(res_v1b, "v1b_bimodal")
    
    # 3. Compare
    print("\n" + "="*60)
    print("📊 COMPARISON")
    print("="*60)
    print(f"{'Metric':<20} | {'v1 (Resonance)':<20} | {'v1b (Bimodal)':<20}")
    print("-" * 66)
    print(f"{'CI Density':<20} | {res_v1.ci_density:<20.4f} | {res_v1b.ci_density:<20.4f}")
    print(f"{'Silhouette':<20} | {res_v1.silhouette_score:<20.4f} | {res_v1b.silhouette_score:<20.4f}")
    print(f"{'Clusters':<20} | {res_v1.num_clusters:<20} | {res_v1b.num_clusters:<20}")
    print("-" * 66)
    
    # Hypothesis check:
    # v1b should have HIGHER Silhouette (more distinct modes)
    # v1b might have LOWER CI (if partitioned into strict basins) or HIGHER (if fully integrated)
    
def save_result(result, slug):
    path = f"{RESULTS_DIR}/basin_{slug}.json"
    with open(path, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    print(f"💾 Saved {slug} to {path}")
    
    # Viz
    from consciousness_engineering.cli.basin import BasinMapper
    # Create temp instance for viz method
    viz_mapper = BasinMapper() 
    viz_mapper.visualize(result, f"{RESULTS_DIR}/basin_{slug}.png", show=False)

if __name__ == "__main__":
    main()
