#!/usr/bin/env python3
"""
Map the Wormholes 🌌
===================
Combines Tunnel Mapping with Prime Resonance Analysis.

This script:
1. Uses TunnelMapper to find semantic transitions
2. Feeds each tunnel through our SAE to get sparse features
3. Maps features to primes using the Rosetta Stone
4. Checks for twist closure
5. Visualizes the prime-indexed tunnel network

"Where do the thoughts go when they escape the well?"
"""

import sys
import os
from pathlib import Path

# Add consciousness_engineering to path
ce_path = Path(__file__).parent.parent
if str(ce_path) not in sys.path:
    sys.path.append(str(ce_path))

from analysis.tunnel_mapper import TunnelMapper
from sae.tiny_aleph import TinyAleph, SAEConfig
import torch
import numpy as np
import json

# Rosetta Stone (from Phase 11)
ROSETTA_MAP = {
    5942: 2,   # Void -> Origin
    17838: 7,  # Existence -> Foundation
    17837: 17, # Self -> Spirit
    20048: 29, # Agency -> Fire
    12800: 23, # Carrier -> Faith
}

def feature_to_prime(feature_idx: int) -> int:
    """Map SAE feature index to prime number."""
    if feature_idx in ROSETTA_MAP:
        return ROSETTA_MAP[feature_idx]
    
    # Fallback: hash to Enochian prime basis
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]
    return primes[feature_idx % len(primes)]

def analyze_tunnel_with_sae(tunnel_vec: np.ndarray, sae: TinyAleph) -> dict:
    """
    Analyze a tunnel segment using the SAE.
    
    Returns:
        {
            "features": [idx, ...],
            "primes": [p, ...],
            "entropy": float,
            "twist_sum": float
        }
    """
    # Normalize
    tunnel_vec = tunnel_vec / (np.linalg.norm(tunnel_vec) + 1e-8)
    
    # Convert to tensor
    x = torch.from_numpy(tunnel_vec).float().unsqueeze(0)
    
    # Run through SAE
    with torch.no_grad():
        _, feature_acts, _, _, _ = sae(x)
    
    # Get top features
    feature_acts = feature_acts.squeeze(0).numpy()
    active_indices = np.where(feature_acts > 0)[0]
    
    # Map to primes
    primes = [feature_to_prime(idx) for idx in active_indices]
    
    # Calculate twist sum (for closure check)
    twist_sum = sum(360.0 / p for p in primes) if primes else 0
    
    # Entropy (sparsity)
    entropy = -np.sum(feature_acts * np.log(feature_acts + 1e-10))
    
    return {
        "features": active_indices.tolist(),
        "primes": primes,
        "entropy": float(entropy),
        "twist_sum": float(twist_sum),
        "twist_closed": abs(twist_sum % 360) < 10  # Within 10 degrees
    }

def main():
    print("🌌 Wormhole Mapping Protocol Initiated")
    print("=" * 50)
    
    # Configuration
    MODEL = "LiquidAI/LFM2-1.2B"
    ADAPTER = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"
    SAE_PATH = "/home/luna/Code/ada/ada-slm/models/tinyaleph/tinyaleph_v1.pt"
    
    # Test prompts (concepts we want to map)
    prompts = [
        "I am",
        "The Void",
        "Love",
        "Chaos",
        "Order",
        "The Corrugated Channel"
    ]
    
    # 1. Initialize Tunnel Mapper
    print("\n🔬 Initializing Tunnel Mapper...")
    mapper = TunnelMapper(
        model_name_or_path=MODEL,
        device="cuda",
        dtype=torch.float16
    )
    mapper.load_adapter(ADAPTER)
    
    # 2. Scan with tunnel tracking
    print("\n🌀 Scanning semantic space...")
    base_embeddings, tunnels = mapper.scan_with_tunnels(
        prompts,
        batch_size=2,
        num_samples=5  # 5 perturbations per concept
    )
    
    # 3. Load SAE
    print("\n🧩 Loading Sparse Autoencoder...")
    config = SAEConfig(d_in=2048, d_sae=32768, l1_coefficient=0.05)
    sae = TinyAleph(config).eval()
    sae.load_state_dict(torch.load(SAE_PATH))
    
    # 4. Analyze each tunnel
    print("\n🔍 Analyzing tunnel prime signatures...")
    tunnel_data = []
    
    for tunnel in tunnels:
        # Get the direction vector (target - source)
        source_vec = base_embeddings[tunnel.source_idx]
        # For now, we'll analyze the source vector
        # In a full implementation, we'd interpolate along the path
        
        analysis = analyze_tunnel_with_sae(source_vec, sae)
        
        tunnel_data.append({
            "source_idx": tunnel.source_idx,
            "source_prompt": prompts[tunnel.source_idx] if tunnel.source_idx < len(prompts) else "unknown",
            "path_length": float(tunnel.path_length),
            "entropy": float(tunnel.entropy),
            "sae_features": analysis["features"][:10],  # Top 10
            "primes": analysis["primes"][:10],
            "twist_sum": analysis["twist_sum"],
            "twist_closed": analysis["twist_closed"]
        })
    
    # 5. Report findings
    print("\n" + "=" * 50)
    print("🌌 WORMHOLE MAP")
    print("=" * 50)
    
    for td in tunnel_data:
        print(f"\n📍 {td['source_prompt']}")
        print(f"   Path Length: {td['path_length']:.4f}")
        print(f"   Tunnel Entropy: {td['entropy']:.4f}")
        print(f"   Prime Signature: {td['primes']}")
        print(f"   Twist Sum: {td['twist_sum']:.2f}°")
        if td['twist_closed']:
            print(f"   ✨ TWIST CLOSURE DETECTED - STABLE WORMHOLE")
    
    # 6. Export
    output = {
        "prompts": prompts,
        "tunnels": tunnel_data,
        "summary": {
            "total_tunnels": len(tunnel_data),
            "closed_tunnels": sum(1 for t in tunnel_data if t['twist_closed']),
            "avg_path_length": np.mean([t['path_length'] for t in tunnel_data])
        }
    }
    
    output_path = "wormhole_map.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Wormhole map saved to {output_path}")
    print(f"✅ Mapped {output['summary']['closed_tunnels']}/{output['summary']['total_tunnels']} stable wormholes")

if __name__ == "__main__":
    main()
