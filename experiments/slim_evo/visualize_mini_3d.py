#!/usr/bin/env python3
"""
3-Way Hologram Visualizer for Mini-Lab
"""
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

INPUT_FILE = "results/mini_lab_basins/basin_mini_unified.json"
OUTPUT_DIR = "results/mini_lab_basins/viz"

def create_3way_hologram(data, filename):
    prompts = data['prompts']
    categories = data['categories']
    
    # Extract Coordinates
    coords_base = data['base']['coords']
    coords_v2   = data['v2']['coords']
    coords_v2b  = data['v2b']['coords']
    
    # Extract Responses
    resp_base = data['base']['responses']
    resp_v2   = data['v2']['responses']
    resp_v2b  = data['v2b']['responses']

    # Unique categories for color mapping
    unique_cats = sorted(list(set(categories)))
    colors = px.colors.qualitative.Dark24 + px.colors.qualitative.Light24
    color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(unique_cats)}

    fig = go.Figure()

    # Iterate by Category to group in legend
    for cat in unique_cats:
        indices = [i for i, c in enumerate(categories) if c == cat]
        color = color_map[cat]
        
        # Prepare data containers for this category
        x_base, y_base, z_base = [], [], []
        x_v2, y_v2, z_v2 = [], [], []
        x_v2b, y_v2b, z_v2b = [], [], []
        
        hover_base, hover_v2, hover_v2b = [], [], []
        
        line_x, line_y, line_z = [], [], []
        
        for idx in indices:
            # Helper to format full response for hover
            def fmt_resp(text):
                # Replace newlines with <br> and maybe limit to 1000 chars if HUGE
                # But user asked for full, so let's aim for full but safe
                clean = text.replace('"', "'").replace('\n', '<br>')
                return f"<span style='font-size:10px'>{clean}</span>"

            # Base
            p0 = coords_base[idx]
            x_base.append(p0[0]); y_base.append(p0[1]); z_base.append(p0[2])
            hover_base.append(f"<b>Base (350M)</b><br>{prompts[idx]}<br><br><i>{fmt_resp(resp_base[idx])}</i>")
            
            # v2
            p1 = coords_v2[idx]
            x_v2.append(p1[0]); y_v2.append(p1[1]); z_v2.append(p1[2])
            hover_v2.append(f"<b>v2 (Resonance)</b><br>{prompts[idx]}<br><br><i>{fmt_resp(resp_v2[idx])}</i>")
            
            # v2b
            p2 = coords_v2b[idx]
            x_v2b.append(p2[0]); y_v2b.append(p2[1]); z_v2b.append(p2[2])
            hover_v2b.append(f"<b>v2b (Bimodal)</b><br>{prompts[idx]}<br><br><i>{fmt_resp(resp_v2b[idx])}</i>")
            
            # Lines (Base -> v2 -> v2b)
            line_x.extend([p0[0], p1[0], p2[0], None])
            line_y.extend([p0[1], p1[1], p2[1], None])
            line_z.extend([p0[2], p1[2], p2[2], None])

        # 1. Trajectory Lines
        fig.add_trace(go.Scatter3d(
            x=line_x, y=line_y, z=line_z,
            mode='lines',
            line=dict(color=color, width=3),
            opacity=0.4,
            name=cat,
            legendgroup=cat,
            showlegend=False,
            hoverinfo='skip'
        ))

        # 2. Base Markers (Circle)
        fig.add_trace(go.Scatter3d(
            x=x_base, y=y_base, z=z_base,
            mode='markers',
            marker=dict(size=4, symbol='circle', color=color, opacity=0.6),
            name=f"{cat} (Base)",
            legendgroup=cat,
            customdata=hover_base,
            hovertemplate="%{customdata}<extra></extra>"
        ))

        # 3. v2 Markers (Square)
        fig.add_trace(go.Scatter3d(
            x=x_v2, y=y_v2, z=z_v2,
            mode='markers',
            marker=dict(size=5, symbol='square', color=color, opacity=0.8),
            name=f"{cat} (v2)",
            legendgroup=cat,
            showlegend=False,
            customdata=hover_v2,
            hovertemplate="%{customdata}<extra></extra>"
        ))

        # 4. v2b Markers (Diamond)
        fig.add_trace(go.Scatter3d(
            x=x_v2b, y=y_v2b, z=z_v2b,
            mode='markers',
            marker=dict(size=6, symbol='diamond', color=color, opacity=1.0, line=dict(width=1, color='white')),
            name=f"{cat} (v2b)",
            legendgroup=cat,
            showlegend=False,
            customdata=hover_v2b,
            hovertemplate="%{customdata}<extra></extra>"
        ))

    fig.update_layout(
        title="Cognitive Trajectory: Base(●) -> Resonance(■) -> Bimodal(◆)",
        template="plotly_dark",
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showbackground=False),
            yaxis=dict(showgrid=False, zeroline=False, showbackground=False),
            zaxis=dict(showgrid=False, zeroline=False, showbackground=False),
            bgcolor='rgb(10,10,10)'
        ),
        legend=dict(itemsizing='constant', title="Categories (Click to Isolate)"),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    path = f"{OUTPUT_DIR}/{filename}"
    fig.write_html(path)
    print(f"💾 Saved 3-Way Hologram: {path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not Path(INPUT_FILE).exists():
        print("Waiting for data...")
        return
        
    with open(INPUT_FILE) as f:
        data = json.load(f)
        
    create_3way_hologram(data, "hologram_mini_lab.html")

if __name__ == "__main__":
    main()
