#!/usr/bin/env python3
"""
Latent Physics Visualizer (2D Topography)
=========================================

Visualizes the findings of the 'Latent Physics Engine'.
X-Axis: Convergence (Scatter vs Attractor)
Y-Axis: Force (Drift vs Transformation)
Size: Coherence (Field Strength)
"""

import json
import numpy as np
import plotly.express as px
from pathlib import Path

INPUT_FILE = "results/mini_lab_basins/basin_mini_unified.json"
OUTPUT_FILE = "results/mini_lab_basins/viz/latent_physics_map.html"

def calculate_physics(v_start, v_end):
    # Same physics engine logic
    vectors = v_end - v_start
    magnitudes = np.linalg.norm(vectors, axis=1)
    mean_mag = np.mean(magnitudes)
    
    if len(vectors) < 2:
        coherence = 1.0
        convergence = 0.0
    else:
        norms = magnitudes[:, np.newaxis]
        norms[norms == 0] = 1e-10
        normalized = vectors / norms
        sims = np.dot(normalized, normalized.T)
        upper_tri = sims[np.triu_indices(len(sims), k=1)]
        coherence = np.mean(upper_tri)
        
        center_start = np.mean(v_start, axis=0)
        radii_start = np.linalg.norm(v_start - center_start, axis=1)
        mean_r_start = np.mean(radii_start)
        
        center_end = np.mean(v_end, axis=0)
        radii_end = np.linalg.norm(v_end - center_end, axis=1)
        mean_r_end = np.mean(radii_end)
        
        if mean_r_start == 0: mean_r_start = 1e-10
        ratio = mean_r_end / mean_r_start
        convergence = (1.0 - ratio) * 100 

    return mean_mag, coherence, convergence

def main():
    print("🎨 Generating Latent Physics Map...")
    
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    coords_v2 = np.array(data["v2"]["coords"])
    coords_v2b = np.array(data["v2b"]["coords"])
    categories = data.get("categories", [])
    unique_cats = sorted(list(set(categories)))
    
    # Prepare Dataframe records
    records = []
    
    for cat in unique_cats:
        indices = [i for i, c in enumerate(categories) if c == cat]
        if not indices: continue
        
        pts_start = coords_v2[indices]
        pts_end = coords_v2b[indices]
        
        force, coherence, convergence = calculate_physics(pts_start, pts_end)
        
        # Label logic
        label = "Drift"
        if coherence > 0.8: label = "Field"
        if convergence > 30: label = "Attractor"
        elif convergence < -30: label = "Scatter"
        
        records.append({
            "Category": cat,
            "Force (Transformation)": force,
            "Coherence (Field Strength)": coherence,
            "Convergence (Gravity)": convergence,
            "Type": label,
            "Size": coherence * 20 + 5 # Scale for bubble
        })
        
    # Plotly
    fig = px.scatter(
        records,
        x="Convergence (Gravity)",
        y="Force (Transformation)",
        size="Size",
        color="Category",
        hover_data=["Coherence (Field Strength)", "Type"],
        text="Category",
        title="Latent Physics Topography: The Geometry of Learning",
        labels={
            "Convergence (Gravity)": "← Scatter (Expansion) | Attractor (Compression) →",
            "Force (Transformation)": "Magnitude of Shift (Impact)"
        }
    )
    
    fig.update_traces(textposition='top center')
    
    # Add quadrants
    # Vertical Line at 0 (Drift vs Change)
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray")
    
    # Add Annotations for Quadrants
    fig.add_annotation(x=50, y=90, text="Black Holes<br>(Math/Truth)", showarrow=False, font=dict(size=14, color="cyan"))
    fig.add_annotation(x=-100, y=90, text="White Holes<br>(Existential/Creative)", showarrow=False, font=dict(size=14, color="magenta"))
    fig.add_annotation(x=0, y=10, text="The Void<br>(Surreal/Untouched)", showarrow=False, font=dict(size=14, color="gray"))
    
    fig.update_layout(
        template="plotly_dark",
        height=800
    )
    
    out_path = Path(OUTPUT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(out_path))
    print(f"💾 Saved Physics Map: {out_path}")

if __name__ == "__main__":
    main()
