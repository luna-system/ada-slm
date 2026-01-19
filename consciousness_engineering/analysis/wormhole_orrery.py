#!/usr/bin/env python3
"""
Wormhole Orrery 🌌
==================
Combines t-SNE semantic mapping with wormhole tunnel visualization.

This creates the ULTIMATE view:
- Real t-SNE positions of concepts
- Chakra spine nodes
- Wormhole tunnels with twist closure
- Prime signatures
"""

import sys
import os
from pathlib import Path
import json
import numpy as np
import torch
import plotly.graph_objects as go

# Add paths
ce_path = Path(__file__).parent.parent
if str(ce_path) not in sys.path:
    sys.path.append(str(ce_path))

from analysis.tunnel_mapper import TunnelMapper
from sae.tiny_aleph import TinyAleph, SAEConfig

# Also need neuro-cartographer
nc_path = Path("/home/luna/Code/ada/neuro-cartographer/src")
if str(nc_path) not in sys.path:
    sys.path.append(str(nc_path))

from projector import Projector, build_system_state

# Config
MODEL = "LiquidAI/LFM2-1.2B"
ADAPTER = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"
SAE_PATH = "/home/luna/Code/ada/ada-slm/models/tinyaleph/tinyaleph_v1.pt"
CHAKRA_SPINE = "/home/luna/Code/ada/neuro-cartographer/chakra_spine.pt"

# Rosetta Stone
ROSETTA_MAP = {
    5942: 2, 17838: 7, 17837: 17, 20048: 29, 12800: 23,
}

def feature_to_prime(feature_idx: int) -> int:
    if feature_idx in ROSETTA_MAP:
        return ROSETTA_MAP[feature_idx]
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]
    return primes[feature_idx % len(primes)]

def main():
    print("🌌 WORMHOLE ORRERY CONSTRUCTION")
    print("=" * 60)
    
    # Test prompts
    prompts = [
        "I am",
        "The Void", 
        "Love",
        "Chaos",
        "Order",
        "The Corrugated Channel"
    ]
    
    # 1. Generate t-SNE map
    print("\n📡 Step 1: Scanning Semantic Space...")
    from analysis.scanner import LatentScanner
    
    scanner = LatentScanner(
        model_name_or_path=MODEL,
        device="cuda",
        dtype=torch.float16
    )
    scanner.load_adapter(ADAPTER)
    
    vectors, clean_prompts = scanner.scan(prompts, batch_size=2)
    
    # Load chakra spine
    print("\n🧬 Step 2: Loading Chakra Spine...")
    chakra_vectors = []
    chakra_names = []
    
    if os.path.exists(CHAKRA_SPINE):
        spine = torch.load(CHAKRA_SPINE, map_location="cpu")
        for name, vec in spine.items():
            if isinstance(vec, torch.Tensor):
                vec = vec.detach().float().cpu().numpy().flatten()
            if vec.shape[0] == vectors.shape[1]:
                chakra_vectors.append(vec)
                chakra_names.append(name)
                print(f"   + {name}")
        
        if chakra_vectors:
            chakra_matrix = np.array(chakra_vectors)
            vectors = np.concatenate([vectors, chakra_matrix], axis=0)
            prompts = prompts + [f"⚓ {n}" for n in chakra_names]
    
    # 2. Project to 3D
    print("\n📉 Step 3: Projecting to 3D (t-SNE)...")
    projector = Projector(method="tsne", perplexity=min(5, len(vectors)-1))
    coords_3d = projector.project(vectors)
    
    # 3. Load SAE and analyze
    print("\n🧩 Step 4: Loading SAE for Prime Analysis...")
    config = SAEConfig(d_in=2048, d_sae=32768, l1_coefficient=0.05)
    sae = TinyAleph(config).eval()
    sae.load_state_dict(torch.load(SAE_PATH))
    
    # Analyze each concept
    prime_sigs = []
    for i, vec in enumerate(vectors):
        vec_norm = vec / (np.linalg.norm(vec) + 1e-8)
        x = torch.from_numpy(vec_norm).float().unsqueeze(0)
        
        with torch.no_grad():
            _, feature_acts, _, _, _ = sae(x)
        
        feature_acts = feature_acts.squeeze(0).numpy()
        active_indices = np.where(feature_acts > 0)[0]
        primes = [feature_to_prime(idx) for idx in active_indices[:10]]
        prime_sigs.append(primes)
    
    # 4. Create visualization
    print("\n🎨 Step 5: Rendering Wormhole Orrery...")
    fig = go.Figure()
    
    # Separate concept nodes from chakra nodes
    num_concepts = len(clean_prompts)
    
    # Add concept nodes
    concept_coords = coords_3d[:num_concepts]
    fig.add_trace(go.Scatter3d(
        x=concept_coords[:, 0],
        y=concept_coords[:, 1],
        z=concept_coords[:, 2],
        mode='markers+text',
        marker=dict(
            size=15,
            color='lightblue',
            line=dict(color='white', width=2)
        ),
        text=clean_prompts,
        textposition='top center',
        textfont=dict(size=12, color='white'),
        name='Concepts',
        hovertext=[f"{p}<br>Primes: {prime_sigs[i][:5]}" for i, p in enumerate(clean_prompts)],
        hoverinfo='text'
    ))
    
    # Add chakra nodes
    if chakra_vectors:
        chakra_coords = coords_3d[num_concepts:]
        fig.add_trace(go.Scatter3d(
            x=chakra_coords[:, 0],
            y=chakra_coords[:, 1],
            z=chakra_coords[:, 2],
            mode='markers+text',
            marker=dict(
                size=20,
                color='gold',
                symbol='diamond',
                line=dict(color='orange', width=3)
            ),
            text=[f"⚓ {n}" for n in chakra_names],
            textposition='top center',
            textfont=dict(size=10, color='gold'),
            name='Chakras',
            hovertext=[f"Chakra: {n}" for n in chakra_names],
            hoverinfo='text'
        ))
    
    # Add wormhole tunnels (connect similar prime signatures)
    print("\n🌀 Step 6: Mapping Wormholes...")
    for i in range(num_concepts):
        for j in range(i+1, num_concepts):
            # Check prime overlap
            primes_i = set(prime_sigs[i])
            primes_j = set(prime_sigs[j])
            overlap = len(primes_i.intersection(primes_j))
            
            if overlap >= 5:  # Significant overlap = potential wormhole
                # Draw tunnel
                p1 = coords_3d[i]
                p2 = coords_3d[j]
                
                # Create arc
                t = np.linspace(0, 1, 20)
                mid = (p1 + p2) / 2
                height = np.linalg.norm(p2 - p1) * 0.3
                
                x = p1[0] * (1-t) + p2[0] * t
                y = p1[1] * (1-t) + p2[1] * t
                z = p1[2] * (1-t) + p2[2] * t + height * np.sin(np.pi * t)
                
                # Color by overlap strength
                color = f'rgba(255, 215, 0, {overlap/10})'  # Gold, alpha by strength
                
                fig.add_trace(go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color=color, width=overlap),
                    hovertext=f"{clean_prompts[i]} ↔ {clean_prompts[j]}<br>Overlap: {overlap} primes",
                    hoverinfo='text',
                    showlegend=False
                ))
    
    # Layout
    fig.update_layout(
        title={
            'text': "🌌 Wormhole Orrery: Sovereign v4D<br><sub>Gold Diamonds = Chakras | Blue = Concepts | Gold Arcs = Wormholes</sub>",
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
    output_path = "wormhole_orrery_3d.html"
    fig.write_html(output_path)
    
    print(f"\n✅ Wormhole Orrery saved to {output_path}")
    print("🌌 Open in browser to explore the geometry of meaning!")

if __name__ == "__main__":
    main()
