#!/usr/bin/env python3
"""
Visualize the Wormhole Network 🌌
=================================
Creates a 3D interactive visualization of semantic wormholes.

Uses plotly for interactive 3D rendering.
"""

import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_wormhole_data(path="wormhole_map.json"):
    """Load the wormhole map."""
    with open(path, 'r') as f:
        return json.load(f)

def create_wormhole_viz(data):
    """
    Create an interactive 3D visualization of the wormhole network.
    """
    
    prompts = data['prompts']
    tunnels = data['tunnels']
    
    # Create a simple layout for nodes (we'll use a circle for now)
    # In a real implementation, we'd use the actual t-SNE coordinates
    num_nodes = len(prompts)
    theta = np.linspace(0, 2*np.pi, num_nodes, endpoint=False)
    
    # Node positions (circular layout)
    node_x = 10 * np.cos(theta)
    node_y = 10 * np.sin(theta)
    node_z = np.zeros(num_nodes)
    
    # Create figure
    fig = go.Figure()
    
    # Add tunnels as lines
    for tunnel in tunnels:
        source_idx = tunnel['source_idx']
        
        # For visualization, we'll show tunnels as arcs
        # In reality, we'd plot the actual path through latent space
        
        # Determine target (for now, we'll connect to a random nearby node)
        # In full implementation, this would be the actual destination
        target_idx = (source_idx + 1) % num_nodes
        
        # Create arc
        t = np.linspace(0, 1, 20)
        
        # Bezier curve for nice arcs
        x = node_x[source_idx] * (1-t) + node_x[target_idx] * t
        y = node_y[source_idx] * (1-t) + node_y[target_idx] * t
        z = 5 * np.sin(np.pi * t)  # Arc upward
        
        # Color based on twist closure
        color = 'gold' if tunnel.get('twist_closed', False) else 'rgba(255,100,100,0.3)'
        
        # Width based on inverse entropy (low entropy = thick line)
        width = max(1, 10 / (tunnel['entropy'] + 1))
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(
                color=color,
                width=width
            ),
            hovertext=f"{prompts[source_idx]}<br>Entropy: {tunnel['entropy']:.2f}<br>Primes: {tunnel['primes'][:5]}",
            hoverinfo='text',
            showlegend=False
        ))
    
    # Add nodes
    node_colors = []
    node_sizes = []
    node_text = []
    
    for i, prompt in enumerate(prompts):
        # Count how many stable tunnels connect to this node
        stable_count = sum(1 for t in tunnels if t['source_idx'] == i and t.get('twist_closed', False))
        
        # Color by stability
        if stable_count >= 3:
            node_colors.append('gold')
        elif stable_count > 0:
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')
        
        # Size by number of connections
        node_sizes.append(15 + stable_count * 5)
        
        node_text.append(f"{prompt}<br>Stable Wormholes: {stable_count}")
    
    fig.add_trace(go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode='markers+text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(color='white', width=2)
        ),
        text=prompts,
        textposition='top center',
        textfont=dict(size=10, color='white'),
        hovertext=node_text,
        hoverinfo='text',
        name='Concepts'
    ))
    
    # Layout
    fig.update_layout(
        title={
            'text': "🌌 Semantic Wormhole Network<br><sub>Gold = Stable (Twist Closure) | Red = Unstable</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis=dict(showgrid=False, showticklabels=False, title=''),
            yaxis=dict(showgrid=False, showticklabels=False, title=''),
            zaxis=dict(showgrid=False, showticklabels=False, title=''),
            bgcolor='rgb(10,10,30)'
        ),
        paper_bgcolor='rgb(10,10,30)',
        font=dict(color='white'),
        showlegend=True,
        height=800
    )
    
    return fig

def create_prime_spectrum_viz(data):
    """
    Create a visualization of prime signatures.
    """
    tunnels = data['tunnels']
    prompts = data['prompts']
    
    # Collect all primes and their frequencies
    prime_freq = {}
    
    for tunnel in tunnels:
        prompt = tunnel['source_prompt']
        for prime in tunnel['primes']:
            if prime not in prime_freq:
                prime_freq[prime] = {}
            prime_freq[prime][prompt] = prime_freq[prime].get(prompt, 0) + 1
    
    # Create heatmap
    primes = sorted(prime_freq.keys())
    
    # Build matrix
    matrix = []
    for prompt in prompts:
        row = [prime_freq.get(p, {}).get(prompt, 0) for p in primes]
        matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=[f"p={p}" for p in primes],
        y=prompts,
        colorscale='Viridis',
        hovertemplate='%{y}<br>Prime %{x}<br>Frequency: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Prime Signature Spectrum",
        xaxis_title="Prime Numbers",
        yaxis_title="Concepts",
        height=500
    )
    
    return fig

def main():
    print("🌌 Loading wormhole data...")
    data = load_wormhole_data()
    
    print("🎨 Creating 3D visualization...")
    fig_3d = create_wormhole_viz(data)
    
    print("📊 Creating prime spectrum...")
    fig_spectrum = create_prime_spectrum_viz(data)
    
    # Save
    fig_3d.write_html("wormhole_network_3d.html")
    fig_spectrum.write_html("prime_spectrum.html")
    
    print("✅ Visualizations saved:")
    print("   - wormhole_network_3d.html")
    print("   - prime_spectrum.html")
    print("\nOpen these files in your browser to explore!")

if __name__ == "__main__":
    main()
