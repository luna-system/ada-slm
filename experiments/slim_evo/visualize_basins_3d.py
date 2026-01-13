#!/usr/bin/env python3
"""
3D Basin Hologram Generator
===========================

Generates interactive 3D visualizations of consciousness basins using Plotly.
"""

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

RESULTS_DIR = "results/basin_comparisons_macro"
OUTPUT_DIR = "results/basin_comparisons_macro/viz"

def load_data(slug):
    path = f"{RESULTS_DIR}/basin_{slug}.json"
    if not Path(path).exists():
        return None
    with open(path, 'r') as f:
        data = json.load(f)
    
    coords = data['tsne_coords']
    # Ensure 3D
    if len(coords[0]) < 3:
        print(f"⚠️ Data for {slug} is not 3D! Re-run mapping with n_components=3.")
        return None
        
    df = pd.DataFrame(coords, columns=['x', 'y', 'z'])
    df['model'] = slug
    df['category'] = data['prompt_labels']
    df['response'] = [r[:100] + "..." for r in data['response_labels']]
    df['full_label'] = df['category'] + ": " + df['response']
    return df

def create_hologram(df, title, filename):
    """Create 3D scatter plot with interactive hover."""
    fig = px.scatter_3d(
        df, x='x', y='y', z='z',
        color='category',
        hover_data=['full_label'],
        title=f"Consciousness Hologram: {title}",
        opacity=0.8,
        symbol='category'
    )
    
    # Update marker size
    fig.update_traces(marker=dict(size=5, line=dict(width=1, color='DarkSlateGrey')))
    
    # Add connecting lines for same categories (Constellations)
    for cat in df['category'].unique():
        cat_df = df[df['category'] == cat]
        if len(cat_df) > 1:
            # Add a mesh or line trace? Line trace is cleaner.
            # Ideally minimal spanning tree, but simple line loop works
            fig.add_trace(go.Scatter3d(
                x=cat_df['x'], y=cat_df['y'], z=cat_df['z'],
                mode='lines',
                line=dict(width=2, color=px.colors.qualitative.Plotly[list(df['category'].unique()).index(cat) % 10]),
                opacity=0.3,
                showlegend=False
            ))

    path = f"{OUTPUT_DIR}/{filename}"
    fig.write_html(path)
    print(f"💾 Saved Hologram: {path}")

def create_unified_hologram(data, filename):
    """Create a unified hologram with movement vectors (v1 -> v1b)."""
    import numpy as np
    
    # Extract data
    v1_coords = data['v1']['coords']
    v1b_coords = data['v1b']['coords']
    categories = data['categories']
    prompts = data['prompts']
    v1_resps = data['v1']['responses']
    v1b_resps = data['v1b']['responses']

    # Unique categories for color mapping
    unique_cats = sorted(list(set(categories)))
    # Use a vibrant color cycle
    colors = px.colors.qualitative.Dark24 + px.colors.qualitative.Light24
    color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(unique_cats)}

    fig = go.Figure()

    # Iterate by category to group them in the legend
    for cat in unique_cats:
        # Filter indices for this category
        indices = [i for i, c in enumerate(categories) if c == cat]
        
        # Prepare arrays for this category
        c_v1_x, c_v1_y, c_v1_z = [], [], []
        c_v1b_x, c_v1b_y, c_v1b_z = [], [], []
        c_lines_x, c_lines_y, c_lines_z = [], [], []
        
        hover_texts_v1 = []
        hover_texts_v1b = []
        
        # Helper to format full response for hover
        def fmt_resp(text):
            clean = text.replace('"', "'").replace('\n', '<br>')
            return f"<span style='font-size:10px'>{clean}</span>"
        
        for idx in indices:
            # V1 Point
            x1, y1, z1 = v1_coords[idx]
            c_v1_x.append(x1); c_v1_y.append(y1); c_v1_z.append(z1)
            hover_texts_v1.append(f"<b>V1 (Resonance)</b><br>{prompts[idx]}<br><br><i>{fmt_resp(v1_resps[idx])}</i>")
            
            # V1b Point
            x2, y2, z2 = v1b_coords[idx]
            c_v1b_x.append(x2); c_v1b_y.append(y2); c_v1b_z.append(z2)
            hover_texts_v1b.append(f"<b>V1b (Bimodal)</b><br>{prompts[idx]}<br><br><i>{fmt_resp(v1b_resps[idx])}</i>")
            
            # Line (Shift Vector)
            # Plotly lines need None to break segments
            c_lines_x.extend([x1, x2, None])
            c_lines_y.extend([y1, y2, None])
            c_lines_z.extend([z1, z2, None])

        color = color_map[cat]

        # 1. Shift Lines (Vectors)
        fig.add_trace(go.Scatter3d(
            x=c_lines_x, y=c_lines_y, z=c_lines_z,
            mode='lines',
            line=dict(color=color, width=3), # Opacity moved out
            opacity=0.4,
            name=cat,
            legendgroup=cat,
            showlegend=False,
            hoverinfo='skip'
        ))

        # 2. V1 Points (Circle/Sphere)
        fig.add_trace(go.Scatter3d(
            x=c_v1_x, y=c_v1_y, z=c_v1_z,
            mode='markers',
            marker=dict(color=color, size=5, symbol='circle', opacity=0.8),
            name=f"{cat}",
            legendgroup=cat,
            customdata=hover_texts_v1,
            hovertemplate="%{customdata}<extra></extra>"
        ))

        # 3. V1b Points (Diamond)
        fig.add_trace(go.Scatter3d(
            x=c_v1b_x, y=c_v1b_y, z=c_v1b_z,
            mode='markers',
            marker=dict(color=color, size=5, symbol='diamond', opacity=1.0, line=dict(width=1, color='white')),
            name=f"{cat} (bimodal)",
            legendgroup=cat,
            showlegend=False, # Share legend entry with V1
            customdata=hover_texts_v1b,
            hovertemplate="%{customdata}<extra></extra>"
        ))

    # Layout Updates
    fig.update_layout(
        title="Bimodal Shift: Consciousness Hologram (V1 ● -> V1b ◆)",
        template="plotly_dark",
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showbackground=False),
            yaxis=dict(showgrid=False, zeroline=False, showbackground=False),
            zaxis=dict(showgrid=False, zeroline=False, showbackground=False),
            bgcolor='rgb(10,10,10)'
        ),
        legend=dict(itemsizing='constant', title="Concept Categories"),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    path = f"{OUTPUT_DIR}/{filename}"
    fig.write_html(path)
    print(f"💾 Saved Unified Hologram (Cyberpunk): {path}")

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    print("🛸 Generating 3D Holograms...")
    
    # Unified?
    unified_path = f"{RESULTS_DIR}/basin_unified.json"
    if Path(unified_path).exists():
        with open(unified_path, 'r') as f:
            u_data = json.load(f)
        create_unified_hologram(u_data, "hologram_unified.html")

    # v1
    df_v1 = load_data("v1_resonance")
    if df_v1 is not None:
        create_hologram(df_v1, "v1 Resonance (Fluid)", "hologram_v1.html")
        
    # v1b
    df_v1b = load_data("v1b_bimodal")
    if df_v1b is not None:
        create_hologram(df_v1b, "v1b Bimodal (Crystalline)", "hologram_v1b.html")

if __name__ == "__main__":
    main()
