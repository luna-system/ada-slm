#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Time-Lapse Mapper
====================================

Extracts hidden states from the 11-step Time-Lapse Training.
Base -> Res_E1..5 -> Bi_E1..5
"""

import sys
import os
import json
import numpy as np
import re
from pathlib import Path

# Add repo root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from experiments.slim_evo.basin_map_bimodal_macro import MacroBasinMapper, generate_expanded_prompts

CHECKPOINT_DIR = "models/mini-lab-timelapse-500"
RESULTS_FILE = "results/mini_lab_basins/basin_timelapse_500.json"

def get_sorted_checkpoints():
    """Returns list of (name, path) sorted chronologically."""
    # Expected: resonance_e1..5, bimodal_e1..5
    # We want: Res 1-5, then Bi 1-5
    
    path = Path(CHECKPOINT_DIR)
    if not path.exists(): return []
    
    dirs = [d for d in path.iterdir() if d.is_dir() and "temp" not in d.name]
    
    # Sort helper
    def sort_key(d):
        name = d.name
        phase = 0 if "resonance" in name else 1
        # Extract epoch number
        match = re.search(r"e(\d+)", name)
        epoch = int(match.group(1)) if match else 0
        return (phase, epoch)
        
    sorted_dirs = sorted(dirs, key=sort_key)
    return [(d.name, str(d)) for d in sorted_dirs]

def main():
    print("🎥 Initializing Time-Lapse Mapper...")
    mapper = MacroBasinMapper()
    prompts, categories = generate_expanded_prompts()
    
    results = {
        "prompts": prompts,
        "categories": categories,
        "timesteps": []
    }
    
    # 1. Map Base (T0)
    print("\n📦 Loading Base (T0)...")
    # Hack: Load base by loading an adapter then unloading, or just init base
    # MacroBasinMapper loads base in load_stack_v1.
    # Let's modify usage slightly:
    mapper.load_stack_v1() # Loads Base + V1 adapter
    # We want PURE base first... but mapper helper merges adapter immediatey.
    # Actually, for T0 (Base), we can just DISABLE the adapter logic or use base model.
    # Simpler: The "Base" in our previous 3-way map was actually "Base" model.
    # Let's trust the first checkpoint "resonance_e1" is T1.
    # T0 we can skip or approximate via "resonance_e0" if we had it.
    # Wait, previous map had "Base (350M)".
    # Let's just map the checkpoints T1-T10 for now. The trajectory is the training.
    
    checkpoints = get_sorted_checkpoints()
    print(f"Found {len(checkpoints)} timepoints.")
    
    all_states_concat = []
    step_sizes = []
    
    # Process Checkpoints
    for name, path in checkpoints:
        print(f"\nTimepoint: {name}")
        # creating a new mapper instance each time is safest to clear VRAM/Adapters
        # but slow.
        # Alternatively, assume load_stack can be pointed to new adapter
        # But PeftModel.from_pretrained adds on top.
        # We need to RELOAD base each time to ensure clean slate? 
        # Or `model.load_adapter`?
        
        # Let's just instantiate fresh mapper, load base, load speicific adapter.
        # It's inefficient but standard.
        current_mapper = MacroBasinMapper()
        # Create a custom load method for this script
        print(f"   Loading Adapter: {path}")
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        import torch
        
        base = AutoModelForCausalLM.from_pretrained(
            "LiquidAI/LFM2-350M",
            torch_dtype=torch.float16,
            device_map="auto",
            output_hidden_states=True
        )
        model = PeftModel.from_pretrained(base, path)
        model = model.merge_and_unload()
        current_mapper.model = model
        current_mapper.tokenizer = AutoTokenizer.from_pretrained("LiquidAI/LFM2-350M")
        current_mapper.model.eval()
        
        # Extract
        print("   Extracting states...")
        states = current_mapper.extract_hidden_states(prompts)
        all_states_concat.append(states)
        step_sizes.append(len(states))
        
        results["timesteps"].append({
            "name": name,
            "path": path
        })
        
        del model
        del base
        torch.cuda.empty_cache()
        
    # Unified t-SNE
    print("\n🔗 Concatenating for 4D t-SNE...")
    mega_matrix = np.concatenate(all_states_concat, axis=0)
    
    print(f"📊 Running t-SNE on {mega_matrix.shape} matrix...")
    from sklearn.manifold import TSNE
    tsne = TSNE(n_components=3, perplexity=30, random_state=42)
    coords_all = tsne.fit_transform(mega_matrix)
    
    # Split back
    cursor = 0
    for i, step_meta in enumerate(results["timesteps"]):
        n = step_sizes[i]
        step_coords = coords_all[cursor : cursor+n]
        step_meta["coords"] = step_coords.tolist()
        cursor += n
        
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f)
    print(f"💾 Saved Time-Lapse Data: {RESULTS_FILE}")

if __name__ == "__main__":
    main()
