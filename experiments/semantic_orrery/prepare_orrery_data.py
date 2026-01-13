import json
import numpy as np
import os

INPUT_FILE = "results/basin_galaxy_1.2b.json"
OUTPUT_FILE = "experiments/semantic_orrery/data/system_state.json"

SUN_LABEL = "agl_awareness"
PLANET_REASON = ["logic", "math_simple", "math_complex", "science", "causality", "coding"]
PLANET_DREAM = ["philosophy", "existential", "surreal", "emotion", "tonight_protocol", "coherent_english"]

# Color Mapping (Hex)
COLORS = {
    "agl_awareness": "#FFFF00", # Yellow Sun
    "reason_core": "#FF4500",   # Orange/Red
    "dream_core": "#00FFFF",    # Cyan
    "l4": "#00FF00",            # Green (Stable)
    "l5": "#FF00FF",            # Magenta (Exotic)
    "default": "#AAAAAA"
}

def get_centroid_and_mass(coords, indices):
    if not indices: return np.array([0,0,0]), 0
    points = coords[indices]
    centroid = np.mean(points, axis=0)
    dists = np.linalg.norm(points - centroid, axis=1)
    avg_dist = np.mean(dists) if len(dists) > 0 else 1.0
    mass = 10.0 / (avg_dist + 1e-6) # Arbitrary scaling for visual gravity
    return centroid, mass

def main():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    prompts = data["prompts"]
    categories = data.get("categories", ["unknown"] * len(prompts))
    
    raw_coords = np.array(data["coords"])
    
    # Identify Indices
    sun_indices = [i for i, c in enumerate(categories) if c == SUN_LABEL]
    reason_indices = [i for i, c in enumerate(categories) if c in PLANET_REASON]
    dream_indices = [i for i, c in enumerate(categories) if c in PLANET_DREAM]
    
    # Calculate Centroids
    sun_pos, sun_mass = get_centroid_and_mass(raw_coords, sun_indices)
    reason_pos, reason_mass = get_centroid_and_mass(raw_coords, reason_indices)
    dream_pos, dream_mass = get_centroid_and_mass(raw_coords, dream_indices)
    
    # RELATIVITY SHIFT: Everything must be relative to SUN (0,0,0)
    # We subtract sun_pos from everything.
    
    nodes = []
    for i, (p, c) in enumerate(zip(prompts, categories)):
        pos = raw_coords[i] - sun_pos
        nodes.append({
            "id": i,
            "label": p,
            "category": c,
            "pos": pos.tolist()
        })
        
    # Recalculate attractors relative to Sun
    # Sun is now 0,0,0
    sun_pos_rel = np.array([0.0, 0.0, 0.0])
    reason_pos_rel = reason_pos - sun_pos
    dream_pos_rel = dream_pos - sun_pos
    
    # Calculate Lagrange Points (same math as before)
    vec_r = reason_pos_rel # Sun is origin
    dist_r = np.linalg.norm(vec_r)
    
    # Plane normal defined by Dream
    vec_d = dream_pos_rel
    plane_normal = np.cross(vec_r, vec_d)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    
    theta = np.deg2rad(60)
    cross_k_r = np.cross(plane_normal, vec_r)
    
    # L4
    vec_l4 = vec_r * np.cos(theta) + cross_k_r * np.sin(theta)
    
    # L5
    vec_l5 = vec_r * np.cos(-theta) + cross_k_r * np.sin(-theta)
    
    output_data = {
        "attractors": [
            {
                "name": "The Sun (Awareness)",
                "type": "sun",
                "pos": sun_pos_rel.tolist(),
                "mass": float(sun_mass),
                "color": COLORS["agl_awareness"],
                "radius": 4.0
            },
            {
                "name": "Planet Reason",
                "type": "planet",
                "pos": reason_pos_rel.tolist(),
                "mass": float(reason_mass),
                "color": COLORS["reason_core"],
                "radius": 2.5
            },
            {
                "name": "Planet Dream",
                "type": "planet",
                "description": "Stabilizing L4 Attractor",
                "pos": dream_pos_rel.tolist(),
                "mass": float(dream_mass),
                "color": COLORS["dream_core"],
                "radius": 2.5
            }
        ],
        "lagrange": {
            "l4": {
                "pos": vec_l4.tolist(),
                "label": "L4 (Joy/Dream)",
                "color": COLORS["l4"]
            },
            "l5": {
                "pos": vec_l5.tolist(),
                "label": "L5 (The Void)",
                "color": COLORS["l5"]
            }
        },
        "nodes": nodes
    }
    
    print(f"Writing {len(nodes)} nodes to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=2)
    print("Done.")

if __name__ == "__main__":
    main()
