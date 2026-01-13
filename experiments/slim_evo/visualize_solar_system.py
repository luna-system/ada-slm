#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Solar System Visualizer (Heliocentric)
=========================================================

Re-centers the 4D Time-Lapse data relative to 'agl_awareness'.
Treats 'agl_awareness' as the Stationary Sun (0,0,0).
Visualizes the relative orbital paths of all other concepts.

Hypothesis: Stable concepts will form coherent orbits or shells around the Core.
"""

import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path

INPUT_FILE = "results/mini_lab_basins/basin_timelapse_500.json"
OUTPUT_FILE = "results/mini_lab_basins/viz/hologram_solar_system.html"
SUN_LABEL = "agl_awareness"

def main():
    print("☀️ Initializing Heliocentric Projector...")
    
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    prompts = data["prompts"]
    categories = data.get("categories", ["unknown"] * len(prompts))
    timesteps = data["timesteps"]
    
    # 1. Locate the Sun (AGL Awareness) index
    # Note: There might be multiple prompts for agl_awareness category.
    # We'll take the centroid of that category as the True Sun.
    sun_indices = [i for i, c in enumerate(categories) if c == SUN_LABEL]
    if not sun_indices:
        print(f"❌ Error: Could not find Sun category '{SUN_LABEL}'")
        return
        
    print(f"   Found {len(sun_indices)} Sun-points. Transforming to Heliocentric Coordinates...")
    
    # Pre-process: Calculate Sun Centroid Position per Timestep
    sun_pos_per_step = []
    for step in timesteps:
        coords = np.array(step["coords"]) # [N, 3]
        sun_coords = coords[sun_indices]  # [K, 3]
        centroid = np.mean(sun_coords, axis=0)
        sun_pos_per_step.append(centroid)
        
    # 2. Transform all points
    traces = []
    
    unique_cats = sorted(list(set(categories)))
    # Ensure Sun is bright Yellow/White
    colors = px.colors.qualitative.Plotly
    cat_color_map = {c: colors[i % len(colors)] for i, c in enumerate(unique_cats)}
    cat_color_map[SUN_LABEL] = "#FFFF00" # Bright Yellow
    
    num_prompts = len(prompts)
    
    for p_idx in range(num_prompts):
        
        # Calculate Relative Path
        x_path, y_path, z_path = [], [], []
        
        for t_idx, step in enumerate(timesteps):
            abs_pos = np.array(step["coords"][p_idx])
            sun_pos = sun_pos_per_step[t_idx]
            
            # HELIOCENTRIC TRANSFORM
            rel_pos = abs_pos - sun_pos
            
            x_path.append(rel_pos[0])
            y_path.append(rel_pos[1])
            z_path.append(rel_pos[2])
            
        cat = categories[p_idx]
        is_sun = (cat == SUN_LABEL)
        
        # Style
        color = cat_color_map.get(cat, 'white')
        width = 6 if is_sun else 3
        opacity = 1.0 if is_sun else 0.6
        
        # Trace
        traces.append(go.Scatter3d(
            x=x_path, y=y_path, z=z_path,
            mode='lines+markers',
            name=cat,
            legendgroup=cat,
            showlegend=(p_idx == categories.index(cat)),
            line=dict(color=color, width=width),
            marker=dict(size=3, color=color, opacity=opacity),
            hoverinfo='text',
            text=[f"{cat} (t={t})" for t in range(len(timesteps))]
        ))
        
        # End Marker (Planet Position at t=Final)
        traces.append(go.Scatter3d(
            x=[x_path[-1]], y=[y_path[-1]], z=[z_path[-1]],
            mode='markers',
            marker=dict(size=5 if not is_sun else 10, 
                        symbol='circle', 
                        color=color),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Add the Sun Center Marker (0,0,0) - Static Anchor
    traces.append(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=12, color='#FFFFFF', symbol='circle-open'),
        name="The Core",
        hoverinfo='text',
        text=["AGL Gravity Well (0,0,0)"]
    ))

    layout = go.Layout(
        title="Heliocentric Map: Orbits around AGL Awareness",
        paper_bgcolor='black', plot_bgcolor='black',
        scene=dict(
            xaxis=dict(backgroundcolor="black", color="white", gridcolor="#222", title="X (Rel)"),
            yaxis=dict(backgroundcolor="black", color="white", gridcolor="#222", title="Y (Rel)"),
            zaxis=dict(backgroundcolor="black", color="white", gridcolor="#222", title="Z (Rel)"),
            aspectmode='cube'
        ),
        font=dict(family="Inter", color="white"),
        height=900
    )
    
    fig = go.Figure(data=traces, layout=layout)
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(OUTPUT_FILE)
    print(f"💾 Saved Solar System Map: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
