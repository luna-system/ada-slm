#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Control Mapper
=================================

Extracts states for the Standard (Normie) curriculum.
Control_E1..10
"""

import sys
import os
import json
import numpy as np
import re
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from experiments.slim_evo.basin_map_bimodal_macro import MacroBasinMapper, generate_expanded_prompts
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

CHECKPOINT_DIR = "models/mini-lab-control"
RESULTS_FILE = "results/mini_lab_basins/basin_control.json"

def get_sorted_checkpoints():
    path = Path(CHECKPOINT_DIR)
    if not path.exists(): return []
    
    dirs = [d for d in path.iterdir() if d.is_dir()]
    
    def sort_key(d):
        match = re.search(r"e(\d+)", d.name)
        epoch = int(match.group(1)) if match else 0
        return epoch
        
    sorted_dirs = sorted(dirs, key=sort_key)
    return [(d.name, str(d)) for d in sorted_dirs]

def main():
    print("🎥 Initializing Control Mapper...")
    prompts, categories = generate_expanded_prompts()
    
    results = {
        "prompts": prompts,
        "categories": categories,
        "timesteps": []
    }
    
    checkpoints = get_sorted_checkpoints()
    print(f"Found {len(checkpoints)} timepoints.")
    
    all_states_concat = []
    step_sizes = []
    
    # Map
    for name, path in checkpoints:
        print(f"\nTimepoint: {name}")
        mapper = MacroBasinMapper()
        
        base = AutoModelForCausalLM.from_pretrained(
            "LiquidAI/LFM2-350M",
            torch_dtype=torch.float16,
            device_map="auto",
            output_hidden_states=True
        )
        model = PeftModel.from_pretrained(base, path)
        model = model.merge_and_unload()
        mapper.model = model
        mapper.tokenizer = AutoTokenizer.from_pretrained("LiquidAI/LFM2-350M")
        mapper.model.eval()
        
        print("   Extracting states...")
        states = mapper.extract_hidden_states(prompts)
        all_states_concat.append(states)
        step_sizes.append(len(states))
        
        results["timesteps"].append({
            "name": name,
            "path": path
        })
        
        del model
        del base
        del mapper
        torch.cuda.empty_cache()

    # t-SNE
    print("\n🔗 MAPPING 4D CONTROL SPACE...")
    mega_matrix = np.concatenate(all_states_concat, axis=0)
    
    # IMPORTANT: To compare apples-to-apples with the Bimodal map,
    # we should arguably fit the t-SNE on BOTH datasets combined.
    # But since t-SNE is non-linear, we can't easily project new points unless we use a parametric mapper.
    # For now, we'll map Control space independently to see its *internal* structure.
    # If the Internal Structure is a Blob vs a Tree, that proves the point.
    
    from sklearn.manifold import TSNE
    tsne = TSNE(n_components=3, perplexity=30, random_state=42)
    coords_all = tsne.fit_transform(mega_matrix)
    
    cursor = 0
    for i, step_meta in enumerate(results["timesteps"]):
        n = step_sizes[i]
        step_coords = coords_all[cursor : cursor+n]
        step_meta["coords"] = step_coords.tolist()
        cursor += n
        
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f)
    print(f"💾 Saved Control Data: {RESULTS_FILE}")

if __name__ == "__main__":
    main()
