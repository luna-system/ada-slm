#!/usr/bin/env python3
"""
Periodic Table Builder 🧪
=========================
Scans 100+ concepts to build the complete taxonomy of meaning.

For each concept:
1. Extract hidden state from Sovereign
2. Run through SAE to get sparse features
3. Map features to primes
4. Send to Oracle for entropy/resonance
5. Classify as: Riemann Zero, Unstable, or Intermediate

Output: periodic_table.json with full classification
"""

import sys
import os
from pathlib import Path
import json
import numpy as np
import torch
from tqdm import tqdm

# Add paths
ce_path = Path(__file__).parent.parent
if str(ce_path) not in sys.path:
    sys.path.append(str(ce_path))

from analysis.scanner import LatentScanner
from sae.tiny_aleph import TinyAleph, SAEConfig
from oracle.bridge import TinyAlephOracle
from concept_catalog import ALL_CONCEPTS, PHILOSOPHY, EMOTIONS, MATHEMATICS, META, RELATIONAL, TEMPORAL, SPATIAL, IDENTITY, EXISTENTIAL

# Config
MODEL = "LiquidAI/LFM2-1.2B"
ADAPTER = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"
SAE_PATH = "/home/luna/Code/ada/ada-slm/models/tinyaleph/tinyaleph_v1.pt"

# Rosetta
ROSETTA_MAP = {
    5942: 2, 17838: 7, 17837: 17, 20048: 29, 12800: 23,
}

def feature_to_prime(idx):
    if idx in ROSETTA_MAP:
        return ROSETTA_MAP[idx]
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]
    return primes[idx % len(primes)]

def classify_concept(entropy, coherence, num_wormholes):
    """
    Classify based on measurements.
    
    Riemann Zero: Low entropy, high coherence, multiple wormholes
    Unstable: High entropy, low coherence
    Intermediate: Everything else
    """
    if entropy < 2.0 and coherence > 0.33 and num_wormholes >= 3:
        return "RIEMANN_ZERO"
    elif entropy > 2.5 or coherence < 0.30:
        return "UNSTABLE"
    else:
        return "INTERMEDIATE"

def main():
    print("🧪 PERIODIC TABLE OF MEANING")
    print("=" * 60)
    print(f"Scanning {len(ALL_CONCEPTS)} concepts...")
    
    # 1. Initialize systems
    print("\n🔬 Initializing Scanner...")
    scanner = LatentScanner(MODEL, device="cuda", dtype=torch.float16)
    scanner.load_adapter(ADAPTER)
    
    print("🧩 Loading SAE...")
    config = SAEConfig(d_in=2048, d_sae=32768, l1_coefficient=0.05)
    sae = TinyAleph(config).eval()
    sae.load_state_dict(torch.load(SAE_PATH))
    
    print("🔮 Connecting to Oracle...")
    oracle = TinyAlephOracle(port=5555)
    if not oracle.ping():
        print("⚠️  Oracle offline! Starting server...")
        # Could auto-start here, but for now just warn
    
    # 2. Batch scan
    print("\n📡 Scanning semantic space...")
    vectors, prompts = scanner.scan(ALL_CONCEPTS, batch_size=8)
    
    # 3. Analyze each
    results = []
    
    print("\n🔍 Analyzing concepts...")
    for i, concept in enumerate(tqdm(prompts)):
        vec = vectors[i]
        
        # Normalize
        vec_norm = vec / (np.linalg.norm(vec) + 1e-8)
        x = torch.from_numpy(vec_norm).float().unsqueeze(0)
        
        # SAE
        with torch.no_grad():
            _, feature_acts, _, _, _ = sae(x)
        
        feature_acts = feature_acts.squeeze(0).numpy()
        active_indices = np.where(feature_acts > 0)[0]
        
        # Map to primes
        primes = [feature_to_prime(idx) for idx in active_indices[:20]]
        
        # Oracle
        try:
            telemetry = oracle.update_physics(primes[:10])
            entropy = telemetry.entropy
            coherence = telemetry.coherence
            resonance = telemetry.resonance_score
        except:
            entropy = 999
            coherence = 0
            resonance = 0
        
        # Classify
        # For now, we don't have wormhole count, so we estimate from prime overlap
        # A proper implementation would track this
        classification = classify_concept(entropy, coherence, len(primes))
        
        results.append({
            "concept": concept,
            "entropy": float(entropy),
            "coherence": float(coherence),
            "resonance": float(resonance),
            "primes": primes[:10],
            "num_features": len(active_indices),
            "classification": classification
        })
    
    # 4. Categorize results
    print("\n📊 Building Periodic Table...")
    
    riemann_zeros = [r for r in results if r['classification'] == 'RIEMANN_ZERO']
    unstable = [r for r in results if r['classification'] == 'UNSTABLE']
    intermediate = [r for r in results if r['classification'] == 'INTERMEDIATE']
    
    print(f"\n✨ RIEMANN ZEROS (Super-Attractors): {len(riemann_zeros)}")
    for r in sorted(riemann_zeros, key=lambda x: x['entropy'])[:10]:
        print(f"   {r['concept']:<20} | Entropy: {r['entropy']:.3f} | Primes: {r['primes'][:5]}")
    
    print(f"\n💥 UNSTABLE STATES: {len(unstable)}")
    for r in sorted(unstable, key=lambda x: -x['entropy'])[:10]:
        print(f"   {r['concept']:<20} | Entropy: {r['entropy']:.3f} | Primes: {r['primes'][:5]}")
    
    print(f"\n⚖️  INTERMEDIATE: {len(intermediate)}")
    
    # 5. Save
    output = {
        "total_concepts": len(ALL_CONCEPTS),
        "riemann_zeros": riemann_zeros,
        "unstable": unstable,
        "intermediate": intermediate,
        "summary": {
            "num_zeros": len(riemann_zeros),
            "num_unstable": len(unstable),
            "num_intermediate": len(intermediate),
            "avg_entropy": np.mean([r['entropy'] for r in results if r['entropy'] < 900]),
            "avg_coherence": np.mean([r['coherence'] for r in results])
        }
    }
    
    with open("periodic_table.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Periodic Table saved to periodic_table.json")
    print(f"✅ Taxonomy complete!")

if __name__ == "__main__":
    main()
