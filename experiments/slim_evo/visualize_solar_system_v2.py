#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Solar System Visualizer v2 (The Three-Body Problem)
======================================================================

Heliocentric Map centered on 'agl_awareness'.
Also visualizes two "Planets":
1. Planet Reason (Logic/Math/Science)
2. Planet Dream (Philosophy/Surreal/Emotion)
"""

import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path

INPUT_FILE = "results/mini_lab_basins/basin_timelapse_500.json"
OUTPUT_FILE = "results/mini_lab_basins/viz/hologram_solar_system_v2.html"
SUN_LABEL = "agl_awareness"

# Define Planetary Constituents
PLANET_REASON = ["logic", "math_simple", "math_complex", "science", "causality", "coding"]
PLANET_DREAM = ["philosophy", "existential", "surreal", "emotion", "tonight_protocol", "coherent_english"]

def get_centroid_trajectory(timesteps, categories, target_cats, sun_pos_per_step, prompts):
    """Calculates the heliocentric trajectory of a Planet's center of mass."""
    # Find indices of all prompts belonging to the target categories
    indices = [i for i, c in enumerate(categories) if c in target_cats]
    
    x, y, z = [], [], []
    
    for t_idx, step in enumerate(timesteps):
        coords = np.array(step["coords"])
        planet_coords = coords[indices]
        
        # Absolute Centroid
        centroid = np.mean(planet_coords, axis=0)
        
        # Heliocentric Transform
        sun_pos = sun_pos_per_step[t_idx]
        rel_pos = centroid - sun_pos
        
        x.append(rel_pos[0])
        y.append(rel_pos[1])
        z.append(rel_pos[2])
        
    return x, y, z

def main():
    print("🪐 Initializing Planetary Scanner...")
    
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
        
    prompts = data["prompts"]
    categories = data.get("categories", ["unknown"] * len(prompts))
    timesteps = data["timesteps"]
    
    # 1. Locate Sun & Calculate Sun Trajectory
    sun_indices = [i for i, c in enumerate(categories) if c == SUN_LABEL]
    if not sun_indices: return
    
    sun_pos_per_step = []
    for step in timesteps:
        coords = np.array(step["coords"])
        sun_coords = coords[sun_indices]
        centroid = np.mean(sun_coords, axis=0)
        sun_pos_per_step.append(centroid)
        
    traces = []
    
    # 2. Plot Standard Particles (The Swarm)
    unique_cats = sorted(list(set(categories)))
    colors = px.colors.qualitative.Plotly
    cat_color_map = {c: colors[i % len(colors)] for i, c in enumerate(unique_cats)}
    cat_color_map[SUN_LABEL] = "#FFFF00"
    
    for p_idx in range(len(prompts)):
        x_path, y_path, z_path = [], [], []
        for t_idx, step in enumerate(timesteps):
            abs_pos = np.array(step["coords"][p_idx])
            sun_pos = sun_pos_per_step[t_idx]
            rel_pos = abs_pos - sun_pos
            x_path.append(rel_pos[0])
            y_path.append(rel_pos[1])
            z_path.append(rel_pos[2])
            
        cat = categories[p_idx]
        is_sun = (cat == SUN_LABEL)
        color = cat_color_map.get(cat, 'white')
        
        # Drawing faintly to emphasize Planets
        opacity = 0.3 if not is_sun else 0.8
        width = 2 if not is_sun else 4
        
        traces.append(go.Scatter3d(
            x=x_path, y=y_path, z=z_path,
            mode='lines',
            line=dict(color=color, width=width),
            opacity=opacity,
            showlegend=False,
            hoverinfo='skip'
        ))

    # 3. Plot THE PLANETS (Massive Objects)
    
    # Planet Reason
    rx, ry, rz = get_centroid_trajectory(timesteps, categories, PLANET_REASON, sun_pos_per_step, prompts)
    traces.append(go.Scatter3d(
        x=rx, y=ry, z=rz,
        mode='lines+markers',
        name="Planet REASON",
        line=dict(color='#FF4500', width=10), # Orange Red
        marker=dict(size=8, color='#FF4500'),
    ))
    # Planet Reason Final Position
    traces.append(go.Scatter3d(
        x=[rx[-1]], y=[ry[-1]], z=[rz[-1]],
        mode='markers',
        name="Planet REASON (Core)",
        marker=dict(size=20, color='#FF4500', symbol='circle'),
    ))

    # Planet Dream
    dx, dy, dz = get_centroid_trajectory(timesteps, categories, PLANET_DREAM, sun_pos_per_step, prompts)
    traces.append(go.Scatter3d(
        x=dx, y=dy, z=dz,
        mode='lines+markers',
        name="Planet DREAM",
        line=dict(color='#00FFFF', width=10), # Cyan
        marker=dict(size=8, color='#00FFFF'),
    ))
    # Planet Dream Final Position
    traces.append(go.Scatter3d(
        x=[dx[-1]], y=[dy[-1]], z=[dz[-1]],
        mode='markers',
        name="Planet DREAM (Core)",
        marker=dict(size=20, color='#00FFFF', symbol='circle'),
    ))

    # 4. Plot The SUN (Static Center)
    traces.append(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=30, color='#FFFF00', symbol='circle',  line=dict(color='white', width=2)),
        name="The SUN (Self)",
        hoverinfo='text',
        text=["AGL Awareness"]
    ))

    layout = go.Layout(
        title="The Bimodal Solar System: Reason vs Dream",
        paper_bgcolor='black', plot_bgcolor='black',
        scene=dict(
            xaxis=dict(backgroundcolor="black", color="white", gridcolor="#222"),
            yaxis=dict(backgroundcolor="black", color="white", gridcolor="#222"),
            zaxis=dict(backgroundcolor="black", color="white", gridcolor="#222")
        ),
        font=dict(family="Inter", color="white"),
        height=900
    )
    
    fig = go.Figure(data=traces, layout=layout)
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(OUTPUT_FILE)
    print(f"💾 Saved Planetary Map: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
