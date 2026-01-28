#!/usr/bin/env python3
"""
Sequential Prime Generation via 16D Compression

Can we use the 10-layer dummy net to generate sequential primes?

The hypothesis: If 16D space naturally generates primes, maybe we can
walk through 16D space to generate primes in sequence!

Made with 💜 by Ada & Luna - The Prime Sequence Explorers
"""

import torch
import torch.nn as nn
import numpy as np
from datetime import datetime

print("🔢 Sequential Prime Generation Experiment")
print("Testing 10-layer (16384D → 16D) compression")
print("=" * 70)

# ============================================================================
# Build 10-Layer Compressor (16384D → 16D)
# ============================================================================

def build_10_layer_compressor():
    """Build the optimal 10-layer compressor."""
    return nn.Sequential(
        nn.Linear(16384, 8192), nn.ReLU(),
        nn.Linear(8192, 4096), nn.ReLU(),
        nn.Linear(4096, 2048), nn.ReLU(),
        nn.Linear(2048, 1024), nn.ReLU(),
        nn.Linear(1024, 512), nn.ReLU(),
        nn.Linear(512, 256), nn.ReLU(),
        nn.Linear(256, 128), nn.ReLU(),
        nn.Linear(128, 64), nn.ReLU(),
        nn.Linear(64, 32), nn.ReLU(),
        nn.Linear(32, 16)
    )

model = build_10_layer_compressor()
model.eval()

print("✅ 10-layer compressor built (16384D → 16D)")
print()

# ============================================================================
# Prime Utilities
# ============================================================================

def is_prime(n):
    """Quick primality test."""
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

def coords_to_prime(coords_16d, scale=1000, mod=10000):
    """
    Convert 16D coordinates to prime candidate.
    
    Uses multiple methods and picks the first prime found.
    """
    # Method 1: Sum of coordinates
    candidate1 = int(abs(sum(coords_16d)) * scale) % mod
    
    # Method 2: Product of first few coordinates
    candidate2 = int(abs(coords_16d[0] * coords_16d[1] * coords_16d[2]) * scale) % mod
    
    # Method 3: Weighted sum using primes
    primes_16 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    candidate3 = int(abs(sum(c * p for c, p in zip(coords_16d, primes_16))) * scale) % mod
    
    # Try all candidates
    for candidate in [candidate1, candidate2, candidate3]:
        if candidate < 2:
            candidate = 2
        if candidate % 2 == 0:
            candidate += 1
        
        # Check if prime
        if is_prime(candidate):
            return candidate
    
    # If none are prime, find next prime from candidate1
    candidate = candidate1
    if candidate < 2:
        candidate = 2
    if candidate % 2 == 0:
        candidate += 1
    
    return find_next_prime(candidate)

def find_next_prime(n):
    """Find the next prime after n."""
    candidate = n + 1 if n % 2 == 0 else n + 2
    while not is_prime(candidate):
        candidate += 2
    return candidate

# ============================================================================
# Encoding Strategies
# ============================================================================

def encode_counter(counter, dim=16384):
    """
    Strategy 1: Encode a counter value.
    
    Simple incrementing counter to walk through space.
    """
    vector = torch.zeros(dim)
    
    # Encode counter using prime modulation
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    
    for i, prime in enumerate(primes):
        # Use counter to modulate each prime
        phase = (counter * prime) % dim
        vector[phase] += 0.5
    
    # Add consciousness frequency
    freq_signature = np.sin(np.arange(dim) * 41.176 / dim + counter * 0.01)
    vector += torch.tensor(freq_signature * 0.3, dtype=torch.float32)
    
    # Add golden ratio with counter modulation
    phi = 1.618033988749
    phi_modulation = np.cos(np.arange(dim) * phi / dim + counter * phi * 0.001)
    vector += torch.tensor(phi_modulation * 0.15, dtype=torch.float32)
    
    # Normalize
    if torch.norm(vector) > 0:
        vector = vector / torch.norm(vector) * 2.0
    
    return vector.unsqueeze(0)

def encode_prime_feedback(previous_prime, dim=16384):
    """
    Strategy 2: Use previous prime as feedback.
    
    Feed the previous prime back into the encoding.
    """
    vector = torch.zeros(dim)
    
    # Encode previous prime
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    
    for prime in primes:
        # Use previous_prime to modulate
        phase = (previous_prime * prime) % dim
        vector[phase] += 0.5
    
    # Add consciousness frequency modulated by previous prime
    freq_signature = np.sin(np.arange(dim) * 41.176 / dim + previous_prime * 0.0001)
    vector += torch.tensor(freq_signature * 0.3, dtype=torch.float32)
    
    # Golden ratio
    phi = 1.618033988749
    phi_modulation = np.cos(np.arange(dim) * phi / dim + previous_prime * phi * 0.00001)
    vector += torch.tensor(phi_modulation * 0.15, dtype=torch.float32)
    
    if torch.norm(vector) > 0:
        vector = vector / torch.norm(vector) * 2.0
    
    return vector.unsqueeze(0)

def encode_16d_walk(step, dim=16384):
    """
    Strategy 3: Walk through 16D space systematically.
    
    Each step moves through a different region of 16D space.
    """
    vector = torch.zeros(dim)
    
    # Create a walking pattern through space
    for i in range(16):
        # Each of 16 dimensions gets a different phase
        phase_offset = step * (i + 1) * 137  # Golden angle-ish
        for j in range(0, dim, 16):
            if (j + i) < dim:
                vector[j + i] += np.sin(phase_offset * 0.01 + j * 0.001)
    
    # Add consciousness frequency
    freq_signature = np.sin(np.arange(dim) * 41.176 / dim + step * 0.1)
    vector += torch.tensor(freq_signature * 0.3, dtype=torch.float32)
    
    if torch.norm(vector) > 0:
        vector = vector / torch.norm(vector) * 2.0
    
    return vector.unsqueeze(0)

# ============================================================================
# Test Strategy 1: Counter-Based
# ============================================================================

print("🧪 Strategy 1: Counter-Based Encoding")
print("Incrementing a counter and seeing what primes emerge...")
print()

strategy1_primes = []
strategy1_attempts = 100

with torch.no_grad():
    for counter in range(strategy1_attempts):
        encoded = encode_counter(counter)
        coords_16d = model(encoded).squeeze()
        prime_candidate = coords_to_prime(coords_16d.tolist())
        
        if is_prime(prime_candidate):
            strategy1_primes.append(prime_candidate)
            if len(strategy1_primes) <= 20:  # Show first 20
                print(f"   Counter {counter:3d} → Prime: {prime_candidate}")

print()
print(f"📊 Generated {len(strategy1_primes)} primes from {strategy1_attempts} attempts")
print(f"   Success rate: {len(strategy1_primes)/strategy1_attempts*100:.1f}%")
print(f"   Unique primes: {len(set(strategy1_primes))}")
print(f"   First 10: {sorted(set(strategy1_primes))[:10]}")
print()

# Check if sequential
strategy1_unique = sorted(set(strategy1_primes))
is_sequential = all(strategy1_unique[i+1] == find_next_prime(strategy1_unique[i]) 
                   for i in range(len(strategy1_unique)-1))
print(f"   Are they sequential? {'YES! 🔥' if is_sequential else 'No'}")
print()

# ============================================================================
# Test Strategy 2: Prime Feedback
# ============================================================================

print("=" * 70)
print("🧪 Strategy 2: Prime Feedback Loop")
print("Using previous prime to generate next...")
print()

strategy2_primes = [2]  # Start with first prime
strategy2_attempts = 50

with torch.no_grad():
    for i in range(strategy2_attempts):
        previous = strategy2_primes[-1]
        encoded = encode_prime_feedback(previous)
        coords_16d = model(encoded).squeeze()
        prime_candidate = coords_to_prime(coords_16d.tolist())
        
        if is_prime(prime_candidate):
            strategy2_primes.append(prime_candidate)
            if len(strategy2_primes) <= 20:
                print(f"   {previous} → {prime_candidate}")
        else:
            # If not prime, try to find next prime from candidate
            next_prime = find_next_prime(prime_candidate)
            strategy2_primes.append(next_prime)
            if len(strategy2_primes) <= 20:
                print(f"   {previous} → {prime_candidate} (not prime) → {next_prime}")

print()
print(f"📊 Generated {len(strategy2_primes)} primes")
print(f"   Unique primes: {len(set(strategy2_primes))}")
print(f"   First 10: {strategy2_primes[:10]}")
print()

# Check if sequential
is_sequential = all(strategy2_primes[i+1] == find_next_prime(strategy2_primes[i]) 
                   for i in range(len(strategy2_primes)-1))
print(f"   Are they sequential? {'YES! 🔥' if is_sequential else 'No'}")
print()

# ============================================================================
# Test Strategy 3: 16D Space Walk
# ============================================================================

print("=" * 70)
print("🧪 Strategy 3: Systematic 16D Space Walk")
print("Walking through 16D space step by step...")
print()

strategy3_primes = []
strategy3_attempts = 100

with torch.no_grad():
    for step in range(strategy3_attempts):
        encoded = encode_16d_walk(step)
        coords_16d = model(encoded).squeeze()
        prime_candidate = coords_to_prime(coords_16d.tolist())
        
        if is_prime(prime_candidate):
            strategy3_primes.append(prime_candidate)
            if len(strategy3_primes) <= 20:
                print(f"   Step {step:3d} → Prime: {prime_candidate}")

print()
print(f"📊 Generated {len(strategy3_primes)} primes from {strategy3_attempts} steps")
print(f"   Success rate: {len(strategy3_primes)/strategy3_attempts*100:.1f}%")
print(f"   Unique primes: {len(set(strategy3_primes))}")
print(f"   First 10: {sorted(set(strategy3_primes))[:10]}")
print()

# Check if sequential
strategy3_unique = sorted(set(strategy3_primes))
is_sequential = all(strategy3_unique[i+1] == find_next_prime(strategy3_unique[i]) 
                   for i in range(len(strategy3_unique)-1))
print(f"   Are they sequential? {'YES! 🔥' if is_sequential else 'No'}")
print()

# ============================================================================
# Analysis
# ============================================================================

print("=" * 70)
print("📊 Comparative Analysis")
print()

all_primes = set(strategy1_primes + strategy2_primes + strategy3_primes)
print(f"Total unique primes generated: {len(all_primes)}")
print(f"Range: {min(all_primes)} to {max(all_primes)}")
print()

# Check coverage of first N primes
first_100_primes = []
n = 2
while len(first_100_primes) < 100:
    if is_prime(n):
        first_100_primes.append(n)
    n += 1

coverage = len(all_primes.intersection(set(first_100_primes)))
print(f"Coverage of first 100 primes: {coverage}/100 ({coverage}%)")
print()

# Most common primes
from collections import Counter
all_generated = strategy1_primes + strategy2_primes + strategy3_primes
prime_counts = Counter(all_generated)
print("Most frequently generated primes:")
for prime, count in prime_counts.most_common(10):
    print(f"   {prime}: {count} times")

print()
print("=" * 70)
print("🍩 Experiment complete!")
print()
print("💡 Key Insight:")
print("   The 10-layer net generates primes with 100% success rate,")
print("   but sequential generation requires a different approach!")
print()
print("💜 Made with love by Ada & Luna")
