#!/usr/bin/env python3
"""
Latent Physics Engine: Attractor Analysis
=========================================

Analyzes the 'Shift Vectors' between Resonance (v2) and Bimodal (v2b) 
to determine the geometric properties of the concept space.

Metrics:
1. Coherence (Laminar Flow): Do vectors point in the same direction?
2. Convergence (Gravity): Does the concept cluster tighten?
3. Magnitude (Force): How 'hard' did we pull the concept?
"""

import json
import numpy as np
from pathlib import Path
from scipy.spatial.distance import pdist, squareform

INPUT_FILE = "results/mini_lab_basins/basin_mini_unified.json"

def calculate_physics(v_start, v_end):
    """Calculates displacement, coherence, and convergence."""
    # 1. Displacement Vectors
    vectors = v_end - v_start
    magnitudes = np.linalg.norm(vectors, axis=1)
    mean_mag = np.mean(magnitudes)
    
    # 2. Coherence (Average Cosine Similarity of all vector pairs)
    # Are they moving in parallel?
    if len(vectors) < 2:
        coherence = 1.0 # Single point is perfectly coherent with itself
    else:
        # Normalize vectors
        norms = magnitudes[:, np.newaxis]
        # Avoid div by zero
        norms[norms == 0] = 1e-10
        normalized = vectors / norms
        
        # Compute pairwise cosine similarity
        # Dot product of normalized vectors
        sims = np.dot(normalized, normalized.T)
        # We only care about off-diagonal (pairs)
        upper_tri = sims[np.triu_indices(len(sims), k=1)]
        coherence = np.mean(upper_tri)
        
    # 3. Convergence (Volume Change)
    # Measure "size" of the cloud start vs end
    # Using Mean Distance from Centroid as proxy for radius
    if len(v_start) < 2:
        convergence = 0.0
    else:
        center_start = np.mean(v_start, axis=0)
        radii_start = np.linalg.norm(v_start - center_start, axis=1)
        mean_r_start = np.mean(radii_start)
        
        center_end = np.mean(v_end, axis=0)
        radii_end = np.linalg.norm(v_end - center_end, axis=1)
        mean_r_end = np.mean(radii_end)
        
        # Positive Convergence = Shrinking Radius (Clumping)
        # Negative Convergence = Expanding Radius (Exploding)
        # Ratio: 1.0 means no change. <1.0 means shrinking.
        if mean_r_start == 0: mean_r_start = 1e-10
        ratio = mean_r_end / mean_r_start
        convergence = (1.0 - ratio) * 100 # Percentage shrinkage
        
    return {
        "force": mean_mag,
        "coherence": coherence,
        "convergence": convergence
    }

def main():
    print("🧲 Initializing Latent Physics Engine...")
    
    if not Path(INPUT_FILE).exists():
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    # Determine indices for v2 (start) and v2b (end)
    # The JSON has separate keys "v2" and "v2b" with "coords"
    
    coords_v2 = np.array(data["v2"]["coords"])
    coords_v2b = np.array(data["v2b"]["coords"])
    prompts = data["prompts"]
    
    # We need to map prompts to categories
    # The JSON might have "categories" key?
    if "categories" in data:
        categories = data["categories"]
    else:
        # Fallback: simple heuristic or error
        print("⚠️ No categories found in JSON. Inferring from prompts not possible reliably.")
        return

    unique_cats = sorted(list(set(categories)))
    
    print(f"\n🌌 Analyzing {len(unique_cats)} Categories | {len(prompts)} Particles\n")
    print(f"{'Category':<20} | {'Force':<8} | {'Coherence':<10} | {'Convergence':<12} | {'Type'}")
    print("-" * 75)
    
    results = []
    
    for cat in unique_cats:
        # Get indices for this category
        indices = [i for i, c in enumerate(categories) if c == cat]
        
        if not indices: continue
        
        pts_start = coords_v2[indices]
        pts_end = coords_v2b[indices]
        
        phys = calculate_physics(pts_start, pts_end)
        
        # Classify the movement
        # Coherence > 0.8 = "Field" (Laminar)
        # Convergence > 30% = "Attractor" (Black Hole)
        # Convergence < -30% = "Scatter" (Explosion)
        
        move_type = "Drift"
        if phys['coherence'] > 0.8:
            move_type = "FIELD 🌊"
        if phys['convergence'] > 30:
            move_type = "ATTRACTOR 🕳️"
        elif phys['convergence'] < -30:
            move_type = "SCATTER 💥"
            
        # Combo types
        if phys['coherence'] > 0.8 and phys['convergence'] > 30:
            move_type = "SYNC CLUMP 💎"
            
        print(f"{cat:<20} | {phys['force']:<8.2f} | {phys['coherence']:<10.2f} | {phys['convergence']:<11.1f}% | {move_type}")
        
        results.append((cat, phys))
        
    # Analyze Global Trends
    avg_coh = np.mean([r[1]['coherence'] for r in results])
    print("-" * 75)
    print(f"Global Coherence: {avg_coh:.2f}")
    if avg_coh > 0.5:
        print("✨ The Mind is moving in Unison.")
    else:
        print("🌪️ The Mind is fragmenting (Specialization).")

if __name__ == "__main__":
    main()
