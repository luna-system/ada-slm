#!/usr/bin/env python3
"""
Hunt for the Second Zero 🐍
===========================
Scan ouroboros candidates to find the second Riemann zero.
"""

import sys
import os
from pathlib import Path
import json
import numpy as np
import torch
from tqdm import tqdm

ce_path = Path(__file__).parent.parent
if str(ce_path) not in sys.path:
    sys.path.append(str(ce_path))

from analysis.scanner import LatentScanner
from sae.tiny_aleph import TinyAleph, SAEConfig
from oracle.bridge import TinyAlephOracle
from ouroboros_candidates import OUROBOROS_CANDIDATES

MODEL = "LiquidAI/LFM2-1.2B"
ADAPTER = "/home/luna/Code/ada/ada-slm/results/phase10_sovereign"
SAE_PATH = "/home/luna/Code/ada/ada-slm/models/tinyaleph/tinyaleph_v1.pt"

ROSETTA_MAP = {5942: 2, 17838: 7, 17837: 17, 20048: 29, 12800: 23}

def feature_to_prime(idx):
    if idx in ROSETTA_MAP:
        return ROSETTA_MAP[idx]
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]
    return primes[idx % len(primes)]

def main():
    print("🐍 HUNTING FOR THE SECOND ZERO")
    print("=" * 60)
    
    scanner = LatentScanner(MODEL, device="cuda", dtype=torch.float16)
    scanner.load_adapter(ADAPTER)
    
    config = SAEConfig(d_in=2048, d_sae=32768, l1_coefficient=0.05)
    sae = TinyAleph(config).eval()
    sae.load_state_dict(torch.load(SAE_PATH))
    
    oracle = TinyAlephOracle(port=5555)
    
    print(f"\n📡 Scanning {len(OUROBOROS_CANDIDATES)} candidates...")
    vectors, prompts = scanner.scan(OUROBOROS_CANDIDATES, batch_size=8)
    
    results = []
    
    for i, concept in enumerate(tqdm(prompts)):
        vec = vectors[i]
        vec_norm = vec / (np.linalg.norm(vec) + 1e-8)
        x = torch.from_numpy(vec_norm).float().unsqueeze(0)
        
        with torch.no_grad():
            _, feature_acts, _, _, _ = sae(x)
        
        feature_acts = feature_acts.squeeze(0).numpy()
        active_indices = np.where(feature_acts > 0)[0]
        primes = [feature_to_prime(idx) for idx in active_indices[:20]]
        
        try:
            telemetry = oracle.update_physics(primes[:10])
            entropy = telemetry.entropy
            coherence = telemetry.coherence
        except:
            entropy = 999
            coherence = 0
        
        # Check for ouroboros signature (7 and 13 in primes)
        has_ouroboros = (7 in primes and 13 in primes)
        
        results.append({
            "concept": concept,
            "entropy": float(entropy),
            "coherence": float(coherence),
            "primes": primes[:10],
            "has_ouroboros": has_ouroboros
        })
    
    # Sort by entropy
    results.sort(key=lambda x: x['entropy'])
    
    print("\n" + "=" * 60)
    print("🔥 TOP CANDIDATES (Lowest Entropy)")
    print("=" * 60)
    
    for r in results[:15]:
        ouro = "🐍" if r['has_ouroboros'] else "  "
        print(f"{ouro} {r['concept']:<25} | E: {r['entropy']:.3f} | C: {r['coherence']:.3f} | P: {r['primes'][:5]}")
    
    # Find potential zeros
    zeros = [r for r in results if r['entropy'] < 2.0 and r['coherence'] > 0.33]
    
    if zeros:
        print(f"\n✨ POTENTIAL RIEMANN ZEROS FOUND: {len(zeros)}")
        for z in zeros:
            print(f"   🌟 {z['concept']} | Entropy: {z['entropy']:.4f}")
    else:
        print(f"\n⚠️  No new zeros found, but closest candidates:")
        for r in results[:5]:
            print(f"   → {r['concept']} (E: {r['entropy']:.3f})")
    
    with open("ouroboros_scan.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to ouroboros_scan.json")

if __name__ == "__main__":
    main()
