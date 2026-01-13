#!/usr/bin/env python3
"""
Unified Basin Mapping (Concat+Split)
====================================

Extracts hidden states from both models FIRST, then runs t-SNE on the 
combined dataset to creating a SHARED semantic space for comparison.
"""

import sys
import os
from pathlib import Path
import json
import numpy as np

# Add repo root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from experiments.slim_evo.basin_map_bimodal_macro import MacroBasinMapper, generate_expanded_prompts

RESULTS_DIR = "results/basin_comparisons_macro"

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    mapper = MacroBasinMapper()
    prompts, categories = generate_expanded_prompts()
    print(f"Using {len(prompts)} prompts for UNIFIED mapping.")
    
    # 1. Extract V1
    print("\n📦 Loading v1 (Resonance)...")
    mapper.load_stack_v1()
    print("🔍 Extracting v1 states...")
    states_v1 = mapper.extract_hidden_states(prompts)
    responses_v1 = mapper.generate_responses(prompts) # Optional, but good to have
    
    # 2. Extract V1b
    print("\n📦 Loading v1b (Bimodal)...")
    mapper.load_stack_v1b()
    print("🔍 Extracting v1b states...")
    states_v1b = mapper.extract_hidden_states(prompts)
    responses_v1b = mapper.generate_responses(prompts)
    
    # 3. Concatenate
    print("\n🔗 Concatenating states for Unified t-SNE...")
    # Shape: (2*N, hidden_dim)
    combined_states = np.concatenate([states_v1, states_v1b], axis=0)
    
    # 4. Run t-SNE (3D)
    # Using the mapper's override method
    tsne_coords = mapper.compute_tsne(combined_states, perplexity=30) 
    # Increased perplexity because N is double (80 -> 160)
    
    # 5. Split
    n = len(states_v1)
    coords_v1 = tsne_coords[:n]
    coords_v1b = tsne_coords[n:]
    
    # 6. Save Unified Result
    result = {
        "timestamp": "UNIFIED",
        "prompts": prompts,
        "categories": categories,
        "v1": {
            "coords": coords_v1.tolist(),
            "responses": responses_v1,
        },
        "v1b": {
            "coords": coords_v1b.tolist(),
            "responses": responses_v1b,
        }
    }
    
    path = f"{RESULTS_DIR}/basin_unified.json"
    with open(path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Saved Unified Data: {path}")

if __name__ == "__main__":
    main()
