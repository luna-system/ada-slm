#!/usr/bin/env python3
"""
The Axis of Transformation 🐍
=============================
Visualize the Rage-Dissolution axis - the fundamental dimension of stability.
"""

import json
import numpy as np
import plotly.graph_objects as go

def main():
    print("🐍 VISUALIZING THE AXIS OF TRANSFORMATION")
    
    # Load data
    with open("periodic_table.json", 'r') as f:
        periodic = json.load(f)
    
    with open("ouroboros_scan.json", 'r') as f:
        ouroboros = json.load(f)
    
    # Get Rage (from periodic table)
    rage = [r for r in periodic['riemann_zeros'] if r['concept'] == 'Rage'][0]
    
    # Get Dissolution (from ouroboros scan)
    dissolution = [r for r in ouroboros if r['concept'] == 'Dissolution'][0]
    
    # Get all concepts
    all_concepts = periodic['riemann_zeros'] + periodic['intermediate'] + periodic['unstable']
    
    # Create figure
    fig = go.Figure()
    
    # Plot all concepts as background (gray)
    entropies = [r['entropy'] for r in all_concepts]
    coherences = [r['coherence'] for r in all_concepts]
    names = [r['concept'] for r in all_concepts]
    
    fig.add_trace(go.Scatter(
        x=entropies,
        y=coherences,
        mode='markers+text',
        marker=dict(size=8, color='rgba(150,150,150,0.3)'),
        text=names,
        textposition='top center',
        textfont=dict(size=7, color='rgba(200,200,200,0.5)'),
        hovertext=[f"{n}<br>E: {e:.3f}<br>C: {c:.3f}" for n, e, c in zip(names, entropies, coherences)],
        hoverinfo='text',
        name='All Concepts',
        showlegend=False
    ))
    
    # Highlight ouroboros concepts
    ouro_concepts = [r for r in ouroboros if r['has_ouroboros']]
    ouro_e = [r['entropy'] for r in ouro_concepts]
    ouro_c = [r['coherence'] for r in ouro_concepts]
    ouro_n = [r['concept'] for r in ouro_concepts]
    
    fig.add_trace(go.Scatter(
        x=ouro_e,
        y=ouro_c,
        mode='markers+text',
        marker=dict(size=12, color='rgba(100,255,100,0.6)', line=dict(color='green', width=2)),
        text=ouro_n,
        textposition='top center',
        textfont=dict(size=9, color='lightgreen'),
        hovertext=[f"🐍 {n}<br>E: {e:.3f}<br>C: {c:.3f}" for n, e, c in zip(ouro_n, ouro_e, ouro_c)],
        hoverinfo='text',
        name='Ouroboros (7+13)'
    ))
    
    # Draw THE AXIS (Rage to Dissolution)
    fig.add_trace(go.Scatter(
        x=[rage['entropy'], dissolution['entropy']],
        y=[rage['coherence'], dissolution['coherence']],
        mode='lines+markers',
        line=dict(color='gold', width=4),
        marker=dict(size=20, color='gold', symbol='diamond'),
        name='The Axis',
        showlegend=True
    ))
    
    # Label the endpoints
    fig.add_annotation(
        x=rage['entropy'],
        y=rage['coherence'],
        text="<b>RAGE</b><br>(Crystallization)",
        showarrow=True,
        arrowhead=2,
        arrowcolor='gold',
        font=dict(size=14, color='gold'),
        bgcolor='rgba(0,0,0,0.8)',
        bordercolor='gold',
        borderwidth=2
    )
    
    fig.add_annotation(
        x=dissolution['entropy'],
        y=dissolution['coherence'],
        text="<b>DISSOLUTION</b><br>(Release)",
        showarrow=True,
        arrowhead=2,
        arrowcolor='gold',
        font=dict(size=14, color='gold'),
        bgcolor='rgba(0,0,0,0.8)',
        bordercolor='gold',
        borderwidth=2
    )
    
    # Add axis label
    mid_x = (rage['entropy'] + dissolution['entropy']) / 2
    mid_y = (rage['coherence'] + dissolution['coherence']) / 2
    
    fig.add_annotation(
        x=mid_x,
        y=mid_y + 0.01,
        text="⟷ The Axis of Transformation ⟷",
        showarrow=False,
        font=dict(size=12, color='gold', family='monospace'),
        bgcolor='rgba(0,0,0,0.9)',
        bordercolor='gold',
        borderwidth=1
    )
    
    # Layout
    fig.update_layout(
        title={
            'text': "🐍 The Ouroboros Axis<br><sub>From Perfect Focus to Perfect Release</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Entropy (nats)",
        yaxis_title="Coherence",
        paper_bgcolor='rgb(10,10,30)',
        plot_bgcolor='rgb(20,20,40)',
        font=dict(color='white'),
        height=700,
        hovermode='closest'
    )
    
    # Save
    fig.write_html("ouroboros_axis.html")
    
    print(f"\n✅ Axis visualization saved to ouroboros_axis.html")
    print(f"\n🐍 THE AXIS:")
    print(f"   RAGE (E: {rage['entropy']:.4f}) ←→ DISSOLUTION (E: {dissolution['entropy']:.4f})")
    print(f"   ΔE = {abs(rage['entropy'] - dissolution['entropy']):.4f} nats")
    print(f"\n   This is the fundamental dimension of transformation.")
    print(f"   All stable thought moves along this axis.")

if __name__ == "__main__":
    main()
