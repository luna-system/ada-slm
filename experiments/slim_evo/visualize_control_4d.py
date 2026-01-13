#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Control Hologram (4D)
========================================

Visualizes the 10-step evolutionary path of the CONTROL (Normie) run.
"""

import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

INPUT_FILE = "results/mini_lab_basins/basin_control.json"
OUTPUT_FILE = "results/mini_lab_basins/viz/hologram_control.html"

def main():
    print("🛸 Generating Control Hologram...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    prompts = data["prompts"]
    categories = data.get("categories", ["unknown"] * len(prompts))
    timesteps = data["timesteps"]
    
    num_prompts = len(prompts)
    
    traces = []
    unique_cats = sorted(list(set(categories)))
    colors = px.colors.qualitative.Plotly
    cat_color_map = {c: colors[i % len(colors)] for i, c in enumerate(unique_cats)}
    
    for p_idx in range(num_prompts):
        x_path, y_path, z_path = [], [], []
        hover_text = []
        
        for t, step in enumerate(timesteps):
            coords = step["coords"][p_idx]
            x_path.append(coords[0])
            y_path.append(coords[1])
            z_path.append(coords[2])
            hover_text.append(f"<b>{step['name']}</b><br>{prompts[p_idx]}")
            
        cat = categories[p_idx]
        color = cat_color_map.get(cat, 'white')
        
        traces.append(go.Scatter3d(
            x=x_path, y=y_path, z=z_path,
            mode='lines+markers',
            name=cat,
            legendgroup=cat,
            showlegend=(p_idx == categories.index(cat)),
            line=dict(color=color, width=4),
            marker=dict(size=3, color=color),
            text=hover_text,
            hoverinfo='text'
        ))
        
        # Start/End markers
        traces.append(go.Scatter3d(
            x=[x_path[0]], y=[y_path[0]], z=[z_path[0]],
            mode='markers', marker=dict(size=5, symbol='circle', color=color),
            showlegend=False, hoverinfo='skip'
        ))
        traces.append(go.Scatter3d(
            x=[x_path[-1]], y=[y_path[-1]], z=[z_path[-1]],
            mode='markers', marker=dict(size=6, symbol='diamond', color=color),
            showlegend=False, hoverinfo='skip'
        ))

    layout = go.Layout(
        title="Evolutionary Trajectories (Standard Control Run)",
        paper_bgcolor='black', plot_bgcolor='black',
        scene=dict(
            xaxis=dict(backgroundcolor="black", color="white", gridcolor="#333"),
            yaxis=dict(backgroundcolor="black", color="white", gridcolor="#333"),
            zaxis=dict(backgroundcolor="black", color="white", gridcolor="#333")
        ),
        font=dict(family="Inter", color="white"),
        height=900
    )
    
    fig = go.Figure(data=traces, layout=layout)
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(OUTPUT_FILE)
    print(f"💾 Saved Control Hologram: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
