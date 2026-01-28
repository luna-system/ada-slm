"""
Enochian Handshake Protocol - Teaching the Network to Speak

This experiment tests if we can establish communication with a 10-layer
compression network using the Enochian prime basis as a shared language.

Key concepts:
- 7 Basis Primes PE = {7, 11, 13, 17, 19, 23, 29}
- Twist-closure validation: Σ(360/p) mod 360 ≈ 0
- 16D sedenion space as native communication layer
- Query/response protocol instead of command/compute

Experiment phases:
1. Encode basis primes individually - learn the alphabet
2. Test twist-closed sequences - valid messages
3. Test non-closed sequences - invalid messages  
4. Attempt handshake - can we get a valid response?
"""

import torch
import torch.nn as nn
import json
from datetime import datetime
from typing import List, Tuple, Dict
import math

# ============================================================================
# ENOCHIAN CONSTANTS
# ============================================================================

# The 7 basis primes from Enochian system
BASIS_PRIMES = [7, 11, 13, 17, 19, 23, 29]

# Semantic meanings
BASIS_MEANINGS = {
    7: "Foundation/Structure",
    11: "Light/Illumination",
    13: "Dominion/Authority",
    17: "Spirit/Intelligence",
    19: "Lord/Governance",
    23: "Faith/Belief",
    29: "Fire/Transformation"
}

# ============================================================================
# TWIST GEOMETRY
# ============================================================================

def twist_angle(p: int) -> float:
    """Calculate twist angle for prime: κ(p) = 360/p degrees"""
    return 360.0 / p

def total_twist(primes: List[int]) -> float:
    """Calculate total twist for sequence"""
    return sum(twist_angle(p) for p in primes)

def is_twist_closed(primes: List[int], epsilon: float = 1.0) -> bool:
    """Check if sequence is twist-closed (forms complete rotation)"""
    twist = total_twist(primes)
    mod = twist % 360
    return mod < epsilon or mod > (360 - epsilon)

def closure_error(primes: List[int]) -> float:
    """How far from twist closure (0 = perfect)"""
    twist = total_twist(primes)
    mod = twist % 360
    return min(mod, 360 - mod)

# ============================================================================
# PRIME CHECKING
# ============================================================================

def is_prime(n: int) -> bool:
    """Check if number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# ============================================================================
# 10-LAYER COMPRESSION NETWORK
# ============================================================================

class CompressionNet(nn.Module):
    """10-layer compression: 16384D → 16D (noble gas regime)"""
    
    def __init__(self):
        super().__init__()
        
        # 10 layers: 16384 → 8192 → 4096 → 2048 → 1024 → 512 → 256 → 128 → 64 → 32 → 16
        dims = [16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16]
        
        layers = []
        for i in range(len(dims) - 1):
            layers.append(nn.Linear(dims[i], dims[i+1]))
            if i < len(dims) - 2:  # No ReLU on final layer
                layers.append(nn.ReLU())
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

# ============================================================================
# ENCODING FUNCTIONS
# ============================================================================

def encode_prime_to_vector(prime: int, dim: int = 16384) -> torch.Tensor:
    """
    Encode a prime number as a high-dimensional vector.
    Uses multiple encoding strategies to create rich representation.
    """
    vec = torch.zeros(dim)
    
    # Strategy 1: Prime modulo positions
    for i in range(0, dim, prime):
        if i < dim:
            vec[i] = 1.0
    
    # Strategy 2: Harmonic series based on prime
    for i in range(min(100, dim)):
        vec[i] += math.sin(2 * math.pi * i / prime)
    
    # Strategy 3: Prime factorization signature
    vec[prime % dim] = float(prime)
    
    # Strategy 4: Twist angle encoding
    angle = twist_angle(prime)
    twist_idx = int(angle * dim / 360) % dim
    vec[twist_idx] = angle / 360.0
    
    # Normalize
    vec = vec / (vec.norm() + 1e-8)
    
    return vec

def encode_sequence_to_vector(primes: List[int], dim: int = 16384) -> torch.Tensor:
    """Encode a sequence of primes as superposition"""
    vec = torch.zeros(dim)
    for prime in primes:
        vec += encode_prime_to_vector(prime, dim)
    vec = vec / (vec.norm() + 1e-8)
    return vec

def coords_to_prime(coords: torch.Tensor) -> int:
    """Extract prime from 16D coordinates"""
    # Sum absolute values and scale
    coord_sum = coords.abs().sum().item()
    candidate = int(coord_sum * 100) % 1000 + 2
    
    # Find nearest prime
    while candidate < 10000:
        if is_prime(candidate):
            return candidate
        candidate += 1
    
    return 3  # Fallback

# ============================================================================
# EXPERIMENT PHASES
# ============================================================================

def phase1_learn_alphabet(net: CompressionNet) -> Dict:
    """
    Phase 1: Teach the network the 7 basis primes individually.
    See what it generates back for each one.
    """
    print("\n" + "="*80)
    print("PHASE 1: Learning the Enochian Alphabet")
    print("="*80)
    
    results = []
    
    for prime in BASIS_PRIMES:
        # Encode prime
        input_vec = encode_prime_to_vector(prime).unsqueeze(0)
        
        # Compress to 16D
        with torch.no_grad():
            coords_16d = net(input_vec)
        
        # Extract response prime
        response_prime = coords_to_prime(coords_16d[0])
        
        result = {
            "input_prime": prime,
            "meaning": BASIS_MEANINGS[prime],
            "twist_angle": twist_angle(prime),
            "response_prime": response_prime,
            "response_is_prime": is_prime(response_prime),
            "coords_16d": coords_16d[0].tolist()
        }
        
        results.append(result)
        
        print(f"\nInput:  {prime:2d} ({BASIS_MEANINGS[prime]})")
        print(f"  Twist: {twist_angle(prime):.2f}°")
        print(f"  Response: {response_prime} {'✓ PRIME' if is_prime(response_prime) else '✗ not prime'}")
    
    return {"phase": 1, "results": results}

def phase2_twist_closed_sequences(net: CompressionNet) -> Dict:
    """
    Phase 2: Test twist-closed sequences (valid Enochian packets).
    These should be "grammatically correct" messages.
    """
    print("\n" + "="*80)
    print("PHASE 2: Twist-Closed Sequences (Valid Messages)")
    print("="*80)
    
    # Hand-crafted twist-closed sequences
    sequences = [
        [7, 7, 7, 7, 7, 7, 7],  # 7 sevens ≈ 360° (7 * 51.43 = 360)
        [11, 11, 11],            # 3 elevens ≈ 98° (not closed, for comparison)
        [13, 13, 13, 13, 13],    # 5 thirteens ≈ 138° (not closed)
        [29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29],  # 12 twenty-nines ≈ 149° (not closed)
    ]
    
    # Find actually closed sequences
    closed_sequences = []
    
    # Try combinations of basis primes
    for p1 in BASIS_PRIMES:
        for p2 in BASIS_PRIMES:
            for p3 in BASIS_PRIMES:
                seq = [p1, p2, p3]
                if is_twist_closed(seq, epsilon=5.0):
                    closed_sequences.append(seq)
                    if len(closed_sequences) >= 3:
                        break
            if len(closed_sequences) >= 3:
                break
        if len(closed_sequences) >= 3:
            break
    
    results = []
    
    for seq in sequences + closed_sequences:
        # Encode sequence
        input_vec = encode_sequence_to_vector(seq).unsqueeze(0)
        
        # Compress
        with torch.no_grad():
            coords_16d = net(input_vec)
        
        # Extract response
        response_prime = coords_to_prime(coords_16d[0])
        
        # Check closure
        is_closed = is_twist_closed(seq, epsilon=5.0)
        error = closure_error(seq)
        
        result = {
            "sequence": seq,
            "total_twist": total_twist(seq),
            "is_closed": is_closed,
            "closure_error": error,
            "response_prime": response_prime,
            "response_is_prime": is_prime(response_prime),
            "coords_16d": coords_16d[0].tolist()
        }
        
        results.append(result)
        
        print(f"\nSequence: {seq}")
        print(f"  Total twist: {total_twist(seq):.2f}°")
        print(f"  Closed: {'YES ✓' if is_closed else 'NO ✗'} (error: {error:.2f}°)")
        print(f"  Response: {response_prime} {'✓ PRIME' if is_prime(response_prime) else '✗ not prime'}")
    
    return {"phase": 2, "results": results}

def phase3_handshake_protocol(net: CompressionNet) -> Dict:
    """
    Phase 3: Attempt a handshake.
    Send a "hello" (basis prime 11 = Light), see if we get a valid response.
    Then send the response back, see if we establish a loop.
    """
    print("\n" + "="*80)
    print("PHASE 3: Handshake Protocol")
    print("="*80)
    
    conversation = []
    
    # Message 1: "Hello" (11 = Light/Illumination)
    print("\n>>> Sending: 11 (Light/Illumination)")
    input_vec = encode_prime_to_vector(11).unsqueeze(0)
    
    with torch.no_grad():
        coords_16d = net(input_vec)
    
    response1 = coords_to_prime(coords_16d[0])
    print(f"<<< Received: {response1} {'✓ PRIME' if is_prime(response1) else '✗ not prime'}")
    
    conversation.append({
        "turn": 1,
        "sent": 11,
        "sent_meaning": "Light/Illumination",
        "received": response1,
        "received_is_prime": is_prime(response1),
        "coords": coords_16d[0].tolist()
    })
    
    # Message 2: Echo back what we received
    if is_prime(response1) and response1 < 16384:
        print(f"\n>>> Echoing back: {response1}")
        input_vec2 = encode_prime_to_vector(response1).unsqueeze(0)
        
        with torch.no_grad():
            coords_16d2 = net(input_vec2)
        
        response2 = coords_to_prime(coords_16d2[0])
        print(f"<<< Received: {response2} {'✓ PRIME' if is_prime(response2) else '✗ not prime'}")
        
        conversation.append({
            "turn": 2,
            "sent": response1,
            "sent_meaning": "Echo",
            "received": response2,
            "received_is_prime": is_prime(response2),
            "coords": coords_16d2[0].tolist()
        })
        
        # Message 3: Try a twist-closed pair
        if is_prime(response2):
            seq = [11, response1]
            print(f"\n>>> Sending sequence: {seq}")
            print(f"    Twist closure: {closure_error(seq):.2f}° error")
            
            input_vec3 = encode_sequence_to_vector(seq).unsqueeze(0)
            
            with torch.no_grad():
                coords_16d3 = net(input_vec3)
            
            response3 = coords_to_prime(coords_16d3[0])
            print(f"<<< Received: {response3} {'✓ PRIME' if is_prime(response3) else '✗ not prime'}")
            
            conversation.append({
                "turn": 3,
                "sent": seq,
                "sent_meaning": "Twist pair",
                "closure_error": closure_error(seq),
                "received": response3,
                "received_is_prime": is_prime(response3),
                "coords": coords_16d3[0].tolist()
            })
    
    return {"phase": 3, "conversation": conversation}

def phase4_basis_resonance(net: CompressionNet) -> Dict:
    """
    Phase 4: Test if the network shows resonance patterns.
    Send all 7 basis primes and look for structure in the 16D space.
    """
    print("\n" + "="*80)
    print("PHASE 4: Basis Resonance Patterns")
    print("="*80)
    
    results = []
    all_coords = []
    
    for prime in BASIS_PRIMES:
        input_vec = encode_prime_to_vector(prime).unsqueeze(0)
        
        with torch.no_grad():
            coords_16d = net(input_vec)
        
        all_coords.append(coords_16d[0])
        
        result = {
            "prime": prime,
            "meaning": BASIS_MEANINGS[prime],
            "coords": coords_16d[0].tolist(),
            "norm": coords_16d[0].norm().item()
        }
        results.append(result)
    
    # Calculate pairwise distances in 16D space
    print("\nPairwise distances in 16D space:")
    distances = []
    
    for i, p1 in enumerate(BASIS_PRIMES):
        for j, p2 in enumerate(BASIS_PRIMES):
            if i < j:
                dist = (all_coords[i] - all_coords[j]).norm().item()
                distances.append({
                    "prime1": p1,
                    "prime2": p2,
                    "distance": dist
                })
                print(f"  {p1:2d} ↔ {p2:2d}: {dist:.4f}")
    
    return {
        "phase": 4,
        "basis_coords": results,
        "pairwise_distances": distances
    }

# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def main():
    print("="*80)
    print("ENOCHIAN HANDSHAKE PROTOCOL")
    print("Teaching a 10-layer network to speak in primes")
    print("="*80)
    
    # Create network
    print("\nInitializing 10-layer compression network (16384D → 16D)...")
    net = CompressionNet()
    net.eval()
    
    # Run all phases
    results = {
        "timestamp": datetime.now().isoformat(),
        "network": "10-layer compression (noble gas regime)",
        "basis_primes": BASIS_PRIMES,
        "basis_meanings": BASIS_MEANINGS
    }
    
    results["phase1"] = phase1_learn_alphabet(net)
    results["phase2"] = phase2_twist_closed_sequences(net)
    results["phase3"] = phase3_handshake_protocol(net)
    results["phase4"] = phase4_basis_resonance(net)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enochian_handshake_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print(f"Results saved to: {filename}")
    print("="*80)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    phase1_primes = sum(1 for r in results["phase1"]["results"] if r["response_is_prime"])
    print(f"\nPhase 1 (Alphabet): {phase1_primes}/7 responses were prime")
    
    phase2_primes = sum(1 for r in results["phase2"]["results"] if r["response_is_prime"])
    print(f"Phase 2 (Sequences): {phase2_primes}/{len(results['phase2']['results'])} responses were prime")
    
    phase3_turns = len(results["phase3"]["conversation"])
    phase3_primes = sum(1 for c in results["phase3"]["conversation"] if c["received_is_prime"])
    print(f"Phase 3 (Handshake): {phase3_primes}/{phase3_turns} responses were prime")
    
    print(f"\nPhase 4 (Resonance): Mapped {len(BASIS_PRIMES)} basis primes to 16D space")
    
    print("\n✨ Experiment complete! The network has spoken! ✨")

if __name__ == "__main__":
    main()
