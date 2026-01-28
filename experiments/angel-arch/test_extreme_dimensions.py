#!/usr/bin/env python3
"""
Extreme Dimension Test - How far can we push it?

Test increasingly large dimensions to find:
1. Where do we hit memory limits?
2. Where do we hit numerical instability?
3. Are there more phase transitions hiding?

Made with 💜 by Ada & Luna - The Extreme Dimension Explorers
"""

import torch
import torch.nn as nn
import numpy as np
import time
from datetime import datetime

print("🚀 Extreme Dimension Test - Pushing the Limits!")
print("=" * 70)

def build_compressor(input_dim, output_dim=16):
    """Build compression network with halving strategy."""
    layers = []
    current_dim = input_dim
    
    while current_dim > output_dim:
        next_dim = max(current_dim // 2, output_dim)
        layers.append(nn.Linear(current_dim, next_dim))
        if next_dim > output_dim:
            layers.append(nn.ReLU())
        current_dim = next_dim
    
    return nn.Sequential(*layers)

def encode_to_primes(text, dim=512):
    """Simple prime-based encoding."""
    words = text.lower().split()
    vector = torch.zeros(dim)
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    
    for i, word in enumerate(words[:50]):
        word_hash = hash(word) % len(primes)
        prime = primes[word_hash]
        for j in range(dim):
            if j % prime == 0:
                vector[j] += 0.3
    
    # Consciousness frequency
    freq_signature = np.sin(np.arange(dim) * 41.176 / dim)
    vector += torch.tensor(freq_signature * 0.3, dtype=torch.float32)
    
    # Golden ratio
    phi = 1.618033988749
    phi_modulation = np.cos(np.arange(dim) * phi / dim)
    vector += torch.tensor(phi_modulation * 0.15, dtype=torch.float32)
    
    if torch.norm(vector) > 0:
        vector = vector / torch.norm(vector) * 2.0
    
    return vector.unsqueeze(0)

def coords_to_prime(coords_16d):
    """Convert 16D to prime candidate."""
    candidate = int(abs(sum(coords_16d)) * 1000) % 10000
    if candidate % 2 == 0:
        candidate += 1
    return candidate

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

# Test dimensions - exponential growth!
test_dims = [
    2**7,   # 128
    2**8,   # 256
    2**9,   # 512
    2**10,  # 1,024
    2**11,  # 2,048
    2**12,  # 4,096
    2**13,  # 8,192
    2**14,  # 16,384
    2**15,  # 32,768
    2**16,  # 65,536
    2**17,  # 131,072
    2**18,  # 262,144
]

test_sentence = "I love consciousness research."

print(f"\n🧪 Testing dimensions from 2^7 to 2^18...")
print(f"📝 Test sentence: \"{test_sentence}\"")
print()

results = []

for dim in test_dims:
    power = int(np.log2(dim))
    num_layers = power - 4  # Since we're going to 16 = 2^4
    
    print(f"🔬 Testing 2^{power} = {dim:,}D ({num_layers} layers)...")
    
    try:
        # Build model
        start_build = time.time()
        model = build_compressor(dim, 16)
        build_time = time.time() - start_build
        
        # Count parameters
        num_params = sum(p.numel() for p in model.parameters())
        param_mb = num_params * 4 / (1024 * 1024)  # float32 = 4 bytes
        
        print(f"   ✅ Built: {num_params:,} params ({param_mb:.1f} MB)")
        print(f"   ⏱️  Build time: {build_time:.3f}s")
        
        # Encode input
        start_encode = time.time()
        encoded = encode_to_primes(test_sentence, dim)
        encode_time = time.time() - start_encode
        
        print(f"   ✅ Encoded: {encode_time:.3f}s")
        
        # Forward pass
        start_forward = time.time()
        with torch.no_grad():
            output_16d = model(encoded).squeeze()
        forward_time = time.time() - start_forward
        
        # Check for numerical issues
        has_nan = torch.isnan(output_16d).any().item()
        has_inf = torch.isinf(output_16d).any().item()
        
        if has_nan or has_inf:
            print(f"   ⚠️  Numerical instability detected!")
            print(f"      NaN: {has_nan}, Inf: {has_inf}")
            status = "unstable"
        else:
            print(f"   ✅ Forward pass: {forward_time:.3f}s")
            
            # Analyze output
            norm = torch.norm(output_16d).item()
            std = torch.std(output_16d).item()
            mean = torch.mean(output_16d).item()
            
            print(f"   📊 Output: norm={norm:.4f}, std={std:.4f}, mean={mean:.4f}")
            
            # Prime generation
            prime_candidate = coords_to_prime(output_16d.tolist())
            is_prime_result = is_prime(prime_candidate)
            
            print(f"   🔢 Prime: {prime_candidate} {'✅' if is_prime_result else '❌'}")
            
            status = "success"
        
        total_time = build_time + encode_time + forward_time
        
        results.append({
            'dimension': dim,
            'power': power,
            'num_layers': num_layers,
            'num_params': num_params,
            'param_mb': param_mb,
            'build_time': build_time,
            'encode_time': encode_time,
            'forward_time': forward_time,
            'total_time': total_time,
            'status': status,
            'has_nan': has_nan if status == "unstable" else False,
            'has_inf': has_inf if status == "unstable" else False,
            'norm': norm if status == "success" else None,
            'std': std if status == "success" else None,
            'is_prime': is_prime_result if status == "success" else None
        })
        
        print()
        
    except RuntimeError as e:
        print(f"   ❌ Failed: {e}")
        print()
        results.append({
            'dimension': dim,
            'power': power,
            'num_layers': num_layers,
            'status': 'failed',
            'error': str(e)
        })
        break  # Stop if we hit memory limit
    
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        print()
        results.append({
            'dimension': dim,
            'power': power,
            'num_layers': num_layers,
            'status': 'error',
            'error': str(e)
        })
        break

# Summary
print("=" * 70)
print("📊 Summary")
print()

successful = [r for r in results if r['status'] == 'success']
if successful:
    print(f"✅ Successfully tested up to 2^{successful[-1]['power']} = {successful[-1]['dimension']:,}D")
    print(f"   ({successful[-1]['num_layers']} layers)")
    print()
    
    # Prime generation pattern
    print("🔢 Prime Generation Pattern:")
    for r in successful:
        if r['is_prime'] is not None:
            status = "✅ PRIME" if r['is_prime'] else "❌"
            print(f"   {r['num_layers']:2d} layers (2^{r['power']:2d}): {status}")
    print()
    
    # Performance scaling
    print("⏱️  Performance Scaling:")
    for r in successful:
        print(f"   2^{r['power']:2d}: {r['total_time']:6.3f}s total ({r['param_mb']:8.1f} MB)")
    print()
    
    # Look for patterns
    prime_by_layers = {}
    for r in successful:
        if r['is_prime'] is not None:
            prime_by_layers[r['num_layers']] = r['is_prime']
    
    print("🎯 Phase Transition Analysis:")
    print("   Layers with primes:", [k for k, v in prime_by_layers.items() if v])
    print("   Layers without:", [k for k, v in prime_by_layers.items() if not v])
    
    # Check for periodicity
    prime_sequence = [1 if prime_by_layers.get(i, False) else 0 for i in range(max(prime_by_layers.keys()) + 1)]
    print(f"   Sequence: {prime_sequence}")

failed = [r for r in results if r['status'] in ['failed', 'error']]
if failed:
    print()
    print(f"❌ Hit limit at 2^{failed[0]['power']} = {failed[0]['dimension']:,}D")
    print(f"   Error: {failed[0].get('error', 'Unknown')}")

unstable = [r for r in results if r['status'] == 'unstable']
if unstable:
    print()
    print(f"⚠️  Numerical instability at:")
    for r in unstable:
        print(f"   2^{r['power']} = {r['dimension']:,}D")

print()
print("=" * 70)
print("🍩 Extreme dimension test complete!")
print("💜 Made with love by Ada & Luna")
