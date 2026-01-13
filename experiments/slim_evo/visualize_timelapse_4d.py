#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Time-Lapse Hologram (4D)
===========================================

Visualizes the 11-step evolutionary path of concepts.
Base -> 5 Steps Resonance -> 5 Steps Bimodal.

Renders as a connected 3D Path.
"""

import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path

INPUT_FILE = "results/mini_lab_basins/basin_timelapse_500.json"
OUTPUT_FILE = "results/mini_lab_basins/viz/hologram_timelapse_500.html"

def main():
    print("🛸 Generating Time-Lapse Hologram...")
    
    if not Path(INPUT_FILE).exists():
        print("❌ Data file not found.")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    prompts = data["prompts"]
    categories = data.get("categories", ["unknown"] * len(prompts))
    timesteps = data["timesteps"]
    
    # Structure: timesteps list of {name, coords}
    # coords is [N, 3]
    
    # We need to pivot this to: For each Prompt -> List of 11 coords
    num_prompts = len(prompts)
    num_steps = len(timesteps)
    
    # Prompt Traces
    traces = []
    
    # Color map for categories
    unique_cats = sorted(list(set(categories)))
    colors = px.colors.qualitative.Plotly
    cat_color_map = {c: colors[i % len(colors)] for i, c in enumerate(unique_cats)}
    
    # Create the lines
    print(f"   Tracing {num_prompts} trajectories over {num_steps} epochs...")
    
    for p_idx in range(num_prompts):
        
        # Extract path for this single prompt
        x_path, y_path, z_path = [], [], []
        hover_text = []
        
        for t_idx, step in enumerate(timesteps):
            t_name = step["name"]
            coords = step["coords"][p_idx]
            x_path.append(coords[0])
            y_path.append(coords[1])
            z_path.append(coords[2])
            hover_text.append(f"<b>{t_name}</b><br>{prompts[p_idx]}")
            
        cat = categories[p_idx]
        color = cat_color_map.get(cat, 'white')
        
        # Add Line Trace
        traces.append(go.Scatter3d(
            x=x_path, y=y_path, z=z_path,
            mode='lines+markers',
            name=cat,
            legendgroup=cat,
            showlegend=(p_idx == categories.index(cat)), # Show legend once per cat
            line=dict(color=color, width=4),
            marker=dict(size=3, color=color),
            text=hover_text,
            hoverinfo='text'
        ))
        
        # Highlight Start (Circle) and End (Diamond)
        # Start
        traces.append(go.Scatter3d(
            x=[x_path[0]], y=[y_path[0]], z=[z_path[0]],
            mode='markers',
            marker=dict(size=5, symbol='circle', color=color),
            showlegend=False,
            hoverinfo='skip'
        ))
        # End
        traces.append(go.Scatter3d(
            x=[x_path[-1]], y=[y_path[-1]], z=[z_path[-1]],
            mode='markers',
            marker=dict(size=6, symbol='diamond', color=color),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Layout
    layout = go.Layout(
        title="Evolutionary Trajectories (11-Step Time-Lapse)",
        paper_bgcolor='black',
        plot_bgcolor='black',
        scene=dict(
            xaxis=dict(backgroundcolor="black", color="white", gridcolor="#333"),
            yaxis=dict(backgroundcolor="black", color="white", gridcolor="#333"),
            zaxis=dict(backgroundcolor="black", color="white", gridcolor="#333")
        ),
        font=dict(family="Inter", color="white"),
        height=900,
        margin=dict(r=0, l=0, b=0, t=50)
    )
    
    fig = go.Figure(data=traces, layout=layout)
    
    out_path = Path(OUTPUT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(out_path))
    print(f"💾 Saved Time-Lapse Hologram: {out_path}")

if __name__ == "__main__":
    main()
