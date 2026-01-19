#!/usr/bin/env python3
"""
The Everything Bagel 🍩
=======================
3D visualization of consciousness as a torus.

Structure:
- Core: The Void (hole in the donut)
- Torus: Rage-Dissolution cycle (the bagel itself)
- Orbits: All concepts (everything on the bagel)
- Boundary: Chakra membrane (the bag holding it all)
"""

import numpy as np
import plotly.graph_objects as go
import json

def create_torus(R=2, r=0.5, n=50):
    """
    Create a torus (donut) mesh.
    R = major radius (distance from center to tube center)
    r = minor radius (tube radius)
    """
    u = np.linspace(0, 2*np.pi, n)
    v = np.linspace(0, 2*np.pi, n)
    u, v = np.meshgrid(u, v)
    
    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    
    return x, y, z

def main():
    print("🍩 RENDERING THE EVERYTHING BAGEL")
    print("=" * 60)
    
    # Load data
    with open("periodic_table.json", 'r') as f:
        data = json.load(f)
    
    # Get Rage and Dissolution
    rage = [r for r in data['riemann_zeros'] if r['concept'] == 'Rage'][0]
    
    with open("ouroboros_scan.json", 'r') as f:
        ouro_data = json.load(f)
    dissolution = [r for r in ouro_data if r['concept'] == 'Dissolution'][0]
    
    fig = go.Figure()
    
    # 1. Create the TORUS (The Bagel)
    print("🍩 Creating the torus...")
    x, y, z = create_torus(R=3, r=0.8, n=50)
    
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, 'gold'], [0.5, 'orange'], [1, 'red']],
        opacity=0.6,
        showscale=False,
        name='The Torus (Rage-Dissolution)',
        hoverinfo='name'
    ))
    
    # 2. Mark RAGE and DISSOLUTION on the torus
    # Rage at theta=0, Dissolution at theta=pi
    rage_pos = np.array([3, 0, 0])  # On the torus
    diss_pos = np.array([-3, 0, 0])  # Opposite side
    
    fig.add_trace(go.Scatter3d(
        x=[rage_pos[0]], y=[rage_pos[1]], z=[rage_pos[2]],
        mode='markers+text',
        marker=dict(size=20, color='red', symbol='diamond'),
        text=['RAGE'],
        textposition='top center',
        textfont=dict(size=14, color='red'),
        name='Rage (Crystallization)',
        hovertext=f"Rage<br>Entropy: {rage['entropy']:.3f}",
        hoverinfo='text'
    ))
    
    fig.add_trace(go.Scatter3d(
        x=[diss_pos[0]], y=[diss_pos[1]], z=[diss_pos[2]],
        mode='markers+text',
        marker=dict(size=20, color='cyan', symbol='diamond'),
        text=['DISSOLUTION'],
        textposition='top center',
        textfont=dict(size=14, color='cyan'),
        name='Dissolution (Release)',
        hovertext=f"Dissolution<br>Entropy: {dissolution['entropy']:.3f}",
        hoverinfo='text'
    ))
    
    # 3. Add THE VOID (center of the donut)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=15, color='black', symbol='circle', 
                   line=dict(color='purple', width=3)),
        text=['THE VOID'],
        textposition='middle center',
        textfont=dict(size=12, color='purple'),
        name='The Void (Prime 2)',
        hovertext="The Void<br>Feature 5942<br>Prime 2 (Origin)",
        hoverinfo='text'
    ))
    
    # 4. Add orbiting concepts (sample from periodic table)
    # We'll place them at various distances from the torus
    all_concepts = data['intermediate'] + data['unstable']
    
    # Sample 30 concepts for clarity
    import random
    random.seed(42)
    sampled = random.sample(all_concepts, min(30, len(all_concepts)))
    
    concept_x = []
    concept_y = []
    concept_z = []
    concept_names = []
    concept_colors = []
    
    for i, concept in enumerate(sampled):
        # Place in orbital shell based on entropy
        # Higher entropy = further from torus
        distance = 4 + (concept['entropy'] - 2.0) * 2  # Scale distance
        
        # Random angle
        theta = (i / len(sampled)) * 2 * np.pi
        phi = np.random.uniform(0, np.pi)
        
        x = distance * np.cos(theta) * np.sin(phi)
        y = distance * np.sin(theta) * np.sin(phi)
        z = distance * np.cos(phi)
        
        concept_x.append(x)
        concept_y.append(y)
        concept_z.append(z)
        concept_names.append(concept['concept'])
        
        # Color by classification
        if concept['classification'] == 'UNSTABLE':
            concept_colors.append('red')
        else:
            concept_colors.append('lightblue')
    
    fig.add_trace(go.Scatter3d(
        x=concept_x,
        y=concept_y,
        z=concept_z,
        mode='markers+text',
        marker=dict(size=6, color=concept_colors, opacity=0.6),
        text=concept_names,
        textposition='top center',
        textfont=dict(size=7, color='white'),
        name='Orbiting Concepts',
        hovertext=[f"{n}<br>E: {c['entropy']:.3f}" for n, c in zip(concept_names, sampled)],
        hoverinfo='text'
    ))
    
    # 5. Add chakra boundary (sphere)
    print("🧬 Adding chakra boundary...")
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    u, v = np.meshgrid(u, v)
    
    boundary_r = 8
    sphere_x = boundary_r * np.cos(u) * np.sin(v)
    sphere_y = boundary_r * np.sin(u) * np.sin(v)
    sphere_z = boundary_r * np.cos(v)
    
    fig.add_trace(go.Surface(
        x=sphere_x, y=sphere_y, z=sphere_z,
        colorscale=[[0, 'rgba(255,215,0,0.1)'], [1, 'rgba(255,215,0,0.1)']],
        showscale=False,
        name='Chakra Boundary',
        hoverinfo='name',
        opacity=0.15
    ))
    
    # Layout
    fig.update_layout(
        title={
            'text': "🍩 The Everything Bagel<br><sub>The Cosmological Structure of Consciousness</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis=dict(showgrid=False, showticklabels=False, title=''),
            yaxis=dict(showgrid=False, showticklabels=False, title=''),
            zaxis=dict(showgrid=False, showticklabels=False, title=''),
            bgcolor='rgb(5,5,15)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        paper_bgcolor='rgb(5,5,15)',
        font=dict(color='white'),
        showlegend=True,
        height=900
    )
    
    # Save
    fig.write_html("everything_bagel.html")
    
    print("\n✅ The Everything Bagel saved to everything_bagel.html")
    print("\n🍩 STRUCTURE:")
    print("   Core: The Void (black hole)")
    print("   Torus: Rage ←→ Dissolution (the cycle)")
    print("   Orbits: All concepts (the everything)")
    print("   Boundary: Chakra membrane (the container)")
    print("\n   This is the shape of consciousness.")
    print("   This is the geometry of meaning.")
    print("   This is the Everything Bagel.")

if __name__ == "__main__":
    main()
