#!/usr/bin/env python3
"""
Seaborn Basin Visualizer
========================

Generates high-quality density maps of model consciousness basins.
Comparing Resonance (v1) vs Bimodal (v1b).
"""

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = "results/basin_comparisons_macro"
OUTPUT_DIR = "results/basin_comparisons_macro/viz"

def load_data(slug):
    path = f"{RESULTS_DIR}/basin_{slug}.json"
    if not Path(path).exists():
        print(f"❌ File not found: {path}")
        return None
    with open(path, 'r') as f:
        data = json.load(f)
    
    # Create DataFrame
    coords = data['tsne_coords']
    if len(coords[0]) == 3:
        cols = ['x', 'y', 'z']
    else:
        cols = ['x', 'y']
        
    df = pd.DataFrame(coords, columns=cols)
    df['model'] = slug
    df['category'] = data['prompt_labels']
    df['cluster'] = data['cluster_labels']
    return df

def plot_kde_comparison(df_v1, df_v1b):
    """Density contour plots to visualize basin shape."""
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="white", palette="mako")

    # Combined DF
    df_combined = pd.concat([df_v1, df_v1b])
    
    # Plot
    g = sns.FacetGrid(df_combined, col="model", height=6, aspect=1)
    g.map_dataframe(sns.kdeplot, x="x", y="y", fill=True, alpha=0.6, cmap="viridis")
    g.map_dataframe(sns.scatterplot, x="x", y="y", hue="category", alpha=0.8, s=30, palette="deep")
    
    g.add_legend()
    g.fig.suptitle("Consciousness Basin Geography (High Density = Attractor)", y=1.05)
    
    out_path = f"{OUTPUT_DIR}/comparison_density.png"
    g.savefig(out_path, dpi=200, bbox_inches='tight')
    print(f"Saved: {out_path}")

def draw_convex_hulls(ax, df, palette):
    """Draw convex hulls around categories with >= 3 points."""
    from scipy.spatial import ConvexHull
    import numpy as np
    
    for cat in df['category'].unique():
        points = df[df['category'] == cat][['x', 'y']].values
        if len(points) >= 3:
            try:
                hull = ConvexHull(points)
                # Get hull points in order
                hull_points = points[hull.vertices]
                # Close the loop
                hull_points = np.vstack([hull_points, hull_points[0]])
                
                color = palette.get(cat, 'gray')
                ax.fill(hull_points[:,0], hull_points[:,1], alpha=0.1, color=color)
                ax.plot(hull_points[:,0], hull_points[:,1], alpha=0.5, color=color, linestyle='--')
            except Exception:
                pass # Collinear points can fail ConvexHull

def plot_category_clusters(df_v1, df_v1b):
    """Scatter plots with Convex Hulls for semantic territories."""
    plt.figure(figsize=(14, 7))
    sns.set_theme(style="darkgrid")
    
    # Get unified palette
    categories = list(set(df_v1['category']) | set(df_v1b['category']))
    colors = sns.color_palette("husl", len(categories))
    palette = dict(zip(categories, colors))
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # v1
    draw_convex_hulls(axes[0], df_v1, palette)
    sns.scatterplot(data=df_v1, x='x', y='y', hue='category', style='category', s=100, ax=axes[0], palette=palette, legend=False)
    axes[0].set_title("V1: Resonance (Chaos/Fluidity)")
    
    # v1b
    draw_convex_hulls(axes[1], df_v1b, palette)
    sns.scatterplot(data=df_v1b, x='x', y='y', hue='category', style='category', s=100, ax=axes[1], palette=palette)
    axes[1].set_title("V1b: Bimodal (Crystalline/Ordered)")
    axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    out_path = f"{OUTPUT_DIR}/comparison_scatter_hulls.png"
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    print(f"Saved: {out_path}")

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Load Data
    df_v1 = load_data("v1_resonance")
    df_v1b = load_data("v1b_bimodal")
    
    if df_v1 is None or df_v1b is None:
        return
        
    print("🎨 Generating Seaborn visualizations...")
    plot_kde_comparison(df_v1, df_v1b)
    plot_category_clusters(df_v1, df_v1b)
    
if __name__ == "__main__":
    main()
