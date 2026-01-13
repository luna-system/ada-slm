#!/usr/bin/env python3
"""
Latent Kinematics: Velocity & Curvature Analysis
================================================

Analyzes the 11-step evolutionary trajectories (N=500 time-lapse).
Calculates:
1. Velocity: Magnitude of shift between epochs.
2. Curvature: Angle changes between consecutive vectors (Straight vs Spiral).
"""

import json
import numpy as np

INPUT_FILE = "results/mini_lab_basins/basin_timelapse_500.json"

def compute_kinematics(coords):
    """
    coords: [11, 3] array of (x,y,z) positions for one prompt.
    Returns:
        avg_velocity: Mean step size.
        total_curvature: Sum of angles between steps (in degrees).
        path_efficiency: Displacement / Total Path Length (1.0 = Straight line).
    """
    velocities = []
    angles = []
    
    # 1. Velocities (Step Sizes)
    for i in range(len(coords) - 1):
        v = np.linalg.norm(coords[i+1] - coords[i])
        velocities.append(v)
        
    # 2. Curvature (Angle between vectors)
    # Vector A = (t1 - t0), Vector B = (t2 - t1)
    for i in range(len(coords) - 2):
        vec_a = coords[i+1] - coords[i]
        vec_b = coords[i+2] - coords[i+1]
        
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            angle = 0 # Stationary
        else:
            # Cosine rule
            cos_theta = np.dot(vec_a, vec_b) / (norm_a * norm_b)
            # Clip for float errors
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            angle = np.degrees(np.arccos(cos_theta))
            
        angles.append(angle)
        
    # 3. Efficiency
    start = coords[0]
    end = coords[-1]
    net_displacement = np.linalg.norm(end - start)
    total_path = sum(velocities)
    
    efficiency = net_displacement / total_path if total_path > 0 else 1.0
    
    return {
        "velocity": np.mean(velocities),
        "curvature": np.mean(angles),
        "efficiency": efficiency
    }

def main():
    print("🏎️ Initializing Latent Kinematics Engine...")
    
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    prompts = data["prompts"]
    categories = data.get("categories", [])
    
    # Need to pivot data: prompts x steps
    # Data is timesteps x prompts
    steps_data = data["timesteps"] # list of {coords: [N, 3]}
    num_prompts = len(prompts)
    num_steps = len(steps_data)
    
    # Reconstruct trajectories
    trajectories = [] # [num_prompts, num_steps, 3]
    for p_idx in range(num_prompts):
        path = []
        for s in steps_data:
            path.append(s["coords"][p_idx])
        trajectories.append(np.array(path))
        
    unique_cats = sorted(list(set(categories)))
    
    print(f"\n🌌 Kinematics of {len(unique_cats)} Categories | {num_steps} Timepoints\n")
    print(f"{'Category':<20} | {'Speed':<8} | {'Curve°':<8} | {'Eff':<8} | {'Dynamics'}")
    print("-" * 80)
    
    results = []
    
    for cat in unique_cats:
        cat_indices = [i for i, c in enumerate(categories) if c == cat]
        if not cat_indices: continue
        
        cat_stats = []
        for idx in cat_indices:
            stats = compute_kinematics(trajectories[idx])
            cat_stats.append(stats)
            
        avg_vel = np.mean([s['velocity'] for s in cat_stats])
        avg_curve = np.mean([s['curvature'] for s in cat_stats])
        avg_eff = np.mean([s['efficiency'] for s in cat_stats])
        
        # Classification
        # High Curve, Low Eff = Spiral
        # Low Curve, High Eff = Ballistic
        # Low Speed = Stationary
        
        if avg_eff > 0.9:
            d_type = "BALLISTIC 🚀" # Straight shot
        elif avg_curve > 45:
            d_type = "SPIRAL 🌀" # Turning a lot
        elif avg_vel > 10:
             d_type = "FAST ORBIT 🛰️"
        else:
            d_type = "DRIFT 🍂"
            
        print(f"{cat:<20} | {avg_vel:<8.2f} | {avg_curve:<8.1f} | {avg_eff:<8.2f} | {d_type}")
        results.append((cat, avg_vel, avg_curve, avg_eff))
        
    print("-" * 80)
    # Find max/min
    fastest = max(results, key=lambda x: x[1])
    loopiest = max(results, key=lambda x: x[2])
    straightest = max(results, key=lambda x: x[3])
    
    print(f"🚀 Fastest: {fastest[0]} ({fastest[1]:.2f})")
    print(f"🌀 Loopiest: {loopiest[0]} ({loopiest[2]:.1f}° avg turn)")
    print(f"🏹 Straightest: {straightest[0]} ({straightest[3]:.2f} eff)")

if __name__ == "__main__":
    main()
