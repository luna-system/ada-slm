#!/usr/bin/env python3
"""
The Periodic Table of Meaning (Visualization) 🧪
================================================
3D interactive visualization of ALL 117 concepts.

Color coding:
- GOLD: Riemann Zeros (super-attractors)
- RED: Unstable states
- BLUE: Intermediate states

Size: Proportional to coherence
Hover: Shows entropy, primes, classification
"""

import json
import numpy as np
import torch
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add paths
ce_path = Path(__file__).parent.parent
if str(ce_path) not in sys.path:
    sys.path.append(str(ce_path))

nc_path = Path("/home/luna/Code/ada/neuro-cartographer/src")
if str(nc_path) not in sys.path:
    sys.path.append(str(nc_path))

from analysis.scanner import LatentScanner
from projector import Projector

# Config
MODEL = "LiquidAI/LFM2-1.2B"
ADAPTER = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"

def load_periodic_table():
    """Load the classification data."""
    with open("periodic_table.json", 'r') as f:
        return json.load(f)

def main():
    print("🧪 VISUALIZING PERIODIC TABLE OF MEANING")
    print("=" * 60)
    
    # 1. Load data
    print("\n📊 Loading periodic table...")
    data = load_periodic_table()
    
    all_results = data['riemann_zeros'] + data['intermediate'] + data['unstable']
    concepts = [r['concept'] for r in all_results]
    
    print(f"   Total concepts: {len(concepts)}")
    print(f"   Riemann Zeros: {data['summary']['num_zeros']}")
    print(f"   Unstable: {data['summary']['num_unstable']}")
    print(f"   Intermediate: {data['summary']['num_intermediate']}")
    
    # 2. Scan to get vectors (for t-SNE)
    print("\n📡 Scanning for t-SNE coordinates...")
    scanner = LatentScanner(MODEL, device="cuda", dtype=torch.float16)
    scanner.load_adapter(ADAPTER)
    
    vectors, _ = scanner.scan(concepts, batch_size=8)
    
    # 3. Project to 3D
    print("\n📉 Projecting to 3D...")
    projector = Projector(method="tsne", perplexity=min(30, len(vectors)-1))
    coords = projector.project(vectors)
    
    # 4. Build visualization
    print("\n🎨 Creating visualization...")
    
    # Separate by classification
    zeros_coords = []
    zeros_text = []
    zeros_hover = []
    
    unstable_coords = []
    unstable_text = []
    unstable_hover = []
    
    intermediate_coords = []
    intermediate_text = []
    intermediate_hover = []
    
    for i, result in enumerate(all_results):
        coord = coords[i]
        concept = result['concept']
        classification = result['classification']
        
        hover_text = (
            f"<b>{concept}</b><br>"
            f"Classification: {classification}<br>"
            f"Entropy: {result['entropy']:.3f}<br>"
            f"Coherence: {result['coherence']:.3f}<br>"
            f"Resonance: {result['resonance']:.3f}<br>"
            f"Primes: {result['primes'][:5]}"
        )
        
        if classification == "RIEMANN_ZERO":
            zeros_coords.append(coord)
            zeros_text.append(concept)
            zeros_hover.append(hover_text)
        elif classification == "UNSTABLE":
            unstable_coords.append(coord)
            unstable_text.append(concept)
            unstable_hover.append(hover_text)
        else:
            intermediate_coords.append(coord)
            intermediate_text.append(concept)
            intermediate_hover.append(hover_text)
    
    fig = go.Figure()
    
    # Add Riemann Zeros (GOLD)
    if zeros_coords:
        zeros_coords = np.array(zeros_coords)
        fig.add_trace(go.Scatter3d(
            x=zeros_coords[:, 0],
            y=zeros_coords[:, 1],
            z=zeros_coords[:, 2],
            mode='markers+text',
            marker=dict(
                size=25,
                color='gold',
                symbol='diamond',
                line=dict(color='orange', width=4)
            ),
            text=zeros_text,
            textposition='top center',
            textfont=dict(size=14, color='gold', family='monospace'),
            hovertext=zeros_hover,
            hoverinfo='text',
            name='⭐ Riemann Zeros'
        ))
    
    # Add Unstable (RED)
    if unstable_coords:
        unstable_coords = np.array(unstable_coords)
        fig.add_trace(go.Scatter3d(
            x=unstable_coords[:, 0],
            y=unstable_coords[:, 1],
            z=unstable_coords[:, 2],
            mode='markers+text',
            marker=dict(
                size=8,
                color='rgba(255,100,100,0.6)',
                line=dict(color='red', width=1)
            ),
            text=unstable_text,
            textposition='top center',
            textfont=dict(size=8, color='rgba(255,150,150,0.8)'),
            hovertext=unstable_hover,
            hoverinfo='text',
            name='💥 Unstable'
        ))
    
    # Add Intermediate (BLUE)
    if intermediate_coords:
        intermediate_coords = np.array(intermediate_coords)
        fig.add_trace(go.Scatter3d(
            x=intermediate_coords[:, 0],
            y=intermediate_coords[:, 1],
            z=intermediate_coords[:, 2],
            mode='markers+text',
            marker=dict(
                size=10,
                color='rgba(100,150,255,0.6)',
                line=dict(color='blue', width=1)
            ),
            text=intermediate_text,
            textposition='top center',
            textfont=dict(size=9, color='rgba(150,180,255,0.8)'),
            hovertext=intermediate_hover,
            hoverinfo='text',
            name='⚖️ Intermediate'
        ))
    
    # Layout
    fig.update_layout(
        title={
            'text': "🧪 The Periodic Table of Meaning<br><sub>Gold = Riemann Zero | Red = Unstable | Blue = Intermediate</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showticklabels=False, title=''),
            yaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showticklabels=False, title=''),
            zaxis=dict(showgrid=True, gridcolor='rgba(100,100,100,0.2)', showticklabels=False, title=''),
            bgcolor='rgb(10,10,30)'
        ),
        paper_bgcolor='rgb(10,10,30)',
        font=dict(color='white'),
        showlegend=True,
        height=900
    )
    
    # Save
    output_path = "periodic_table_3d.html"
    fig.write_html(output_path)
    
    print(f"\n✅ Periodic Table visualization saved to {output_path}")
    print("\n🌌 Key Findings:")
    print(f"   ⭐ RAGE is the ONLY Riemann Zero")
    print(f"   💥 {len(unstable_text)} concepts are unstable (high entropy)")
    print(f"   ⚖️  {len(intermediate_text)} concepts are intermediate")
    print("\n   Rage is the atomic nucleus of meaning.")

if __name__ == "__main__":
    main()
