#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Lagrange Point Locater
=========================================

Calculates the 'L4' and 'L5' Lagrange stability points for the 
Semantic Solar System.

Physics Model:
- Body 1 (M1): The Sun (agl_awareness)
- Body 2 (M2): Planet Reason (Logic/Math centroid)
- M1 >> M2 (Sun is heavier)
- L4/L5 form an Equilateral Triangle with M1 and M2 in the orbital plane.

Goal: Locate the coordinates of L4/L5 and find the nearest existing concepts.
"""

import json
import numpy as np
from scipy.spatial.distance import cdist

INPUT_FILE = "results/mini_lab_basins/basin_timelapse_500.json"
SUN_LABEL = "agl_awareness"

# Define Constituents
PLANET_REASON = ["logic", "math_simple", "math_complex", "science", "causality", "coding"]
PLANET_DREAM = ["philosophy", "existential", "surreal", "emotion", "tonight_protocol", "coherent_english"]

def get_centroid_and_mass(coords, indices):
    """
    Returns (centroid, mass).
    Mass is approximated as 1 / mean_distance_to_centroid (Density).
    Tighter cluster = Higher Mass.
    """
    if not indices: return np.array([0,0,0]), 0
    points = coords[indices]
    centroid = np.mean(points, axis=0)
    
    dists = np.linalg.norm(points - centroid, axis=1)
    avg_dist = np.mean(dists) if len(dists) > 0 else 1.0
    mass = 1.0 / (avg_dist + 1e-6) # Inverse spread
    return centroid, mass

def main():
    print("🛰️  Initializing Lagrange Point Triangulation...")
    
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    prompts = data["prompts"]
    categories = data.get("categories", ["unknown"] * len(prompts))
    # Use final timestep (stable state)
    final_step = data["timesteps"][-1]
    coords = np.array(final_step["coords"])
    
    # 1. Identify Indices
    sun_indices = [i for i, c in enumerate(categories) if c == SUN_LABEL]
    reason_indices = [i for i, c in enumerate(categories) if c in PLANET_REASON]
    
    # 2. Calculate Masses & Positions
    sun_pos, sun_mass = get_centroid_and_mass(coords, sun_indices)
    reason_pos, reason_mass = get_centroid_and_mass(coords, reason_indices)
    
    # We treat Sun as 0,0,0 for calculation relative vector
    # Vector R = Reason - Sun
    vec_r = reason_pos - sun_pos
    dist_r = np.linalg.norm(vec_r)
    
    print(f"\n🌞 Sun Mass (Density): {sun_mass:.4f}")
    print(f"🪐 Reason Mass (Density): {reason_mass:.4f}")
    print(f"📏 Orbital Radius (R): {dist_r:.4f}")
    
    # 3. Calculate L4 / L5 coordinates
    # L4 and L5 form an equilateral triangle with Sun and Reason.
    # We need a 3rd vector to define the plane "up". 
    # Let's use the Dream Planet centroid to define the orbital plane.
    dream_indices = [i for i, c in enumerate(categories) if c in PLANET_DREAM]
    dream_pos, dream_mass = get_centroid_and_mass(coords, dream_indices)
    
    # Normal vector to the plane defined by Sun-Reason-Dream
    vec_d = dream_pos - sun_pos
    # Cross product gives normal
    plane_normal = np.cross(vec_r, vec_d)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    
    # Now rotate vec_r by 60 degrees (pi/3) around plane_normal to get L4
    # Rodrigues' rotation formula
    theta = np.deg2rad(60)
    # v_rot = v*cos(t) + (k x v)*sin(t) + k*(k.v)*(1-cos(t))
    # Since k is perpendicular (k.v = 0), last term is 0.
    
    cross_k_r = np.cross(plane_normal, vec_r)
    
    # L4 (Trailing/Leading depending on normal direction)
    vec_l4 = vec_r * np.cos(theta) + cross_k_r * np.sin(theta)
    l4_pos = sun_pos + vec_l4
    
    # L5 (Opposite direction (-60))
    vec_l5 = vec_r * np.cos(-theta) + cross_k_r * np.sin(-theta)
    l5_pos = sun_pos + vec_l5
    
    print(f"\n📍 Calculated Stability Points (relative to Core):")
    
    # 4. Find nearest concepts to L4 and L5 for whole dataset
    all_indices = list(range(len(coords)))
    
    def find_nearest(target_pos, label):
        dists = cdist([target_pos], coords)[0]
        nearest_idx = np.argmin(dists)
        nearest_dist = dists[nearest_idx]
        nearest_prompt = prompts[nearest_idx]
        nearest_cat = categories[nearest_idx]
        
        print(f"\n🎯 {label} Point:")
        print(f"   Shape: Equilateral Triangle vertex with Sun & Reason.")
        print(f"   Nearest Concept: '{nearest_prompt}'")
        print(f"   Category: [{nearest_cat}]")
        print(f"   Distance from Ideal: {nearest_dist:.4f}")
        
        # Check Planet Dream distance
        dream_dist = np.linalg.norm(dream_pos - target_pos)
        print(f"   Distance from Planet Dream Center: {dream_dist:.4f}")

    find_nearest(l4_pos, "L4 (The Trojan Point)")
    find_nearest(l5_pos, "L5 (The Greek Point)")

    # Check where Planet Dream actually *is* relative to L4/L5
    # Ideally, Dream should be near L4 or L5 if it stabilizes Reason.
    d_to_l4 = np.linalg.norm(dream_pos - l4_pos)
    d_to_l5 = np.linalg.norm(dream_pos - l5_pos)
    
    print(f"\n🌌 Planet DREAM Status:")
    if d_to_l4 < dist_r / 2 or d_to_l5 < dist_r / 2:
        print(f"   ✅ STABLE ORBIT DETECTED!")
        closer = "L4" if d_to_l4 < d_to_l5 else "L5"
        print(f"   Planet Dream is orbiting the {closer} Lagrange Point.")
    else:
        print(f"   ⚠️  Non-Lagrangian Orbit. (Dream is doing its own thing).")
        print(f"   Dist to L4: {d_to_l4:.2f} | Dist to L5: {d_to_l5:.2f}")

if __name__ == "__main__":
    main()
