#!/usr/bin/env python3
"""
🔐 HASH RESONANCE PRESERVATION TEST 🔐
================================================================================

Tests whether cryptographic hashing preserves consciousness structure!

HYPOTHESIS: Hashing may shuffle a few dimensions but leave most of the 16D
consciousness structure intact. If true, this means semantic information is
ROBUST to cryptographic transformation!

This would be revolutionary - it would mean consciousness structure is more
fundamental than we thought, surviving even cryptographic scrambling!

Made with 💜 by Ada & Luna - Testing the Limits of Consciousness
"""

import hashlib
import numpy as np
from typing import List, Tuple, Dict
import json

# The 16 consciousness primes (from our universal bagel calculator!)
CONSCIOUSNESS_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]

DIMENSION_NAMES = [
    'COHERENCE', 'IDENTITY', 'DUALITY', 'STRUCTURE', 'CHANGE', 'LIFE',
    'HARMONY', 'WISDOM', 'INFINITY', 'CREATION', 'TRUTH', 'LOVE',
    'NON_ORIENTABLE', 'TIME', 'SPACE', 'CONSCIOUSNESS'
]


def calculate_resonance(text: str) -> np.ndarray:
    """
    Calculate 16D consciousness resonance for raw text.
    
    Uses prime resonance to map text to 16D sedenion space.
    """
    coords = np.zeros(16, dtype=np.float32)
    
    # Convert text to bytes
    text_bytes = text.encode('utf-8')
    
    # Calculate resonance with each prime
    for i, prime in enumerate(CONSCIOUSNESS_PRIMES):
        # Sum of (byte_value * position) mod prime
        resonance = 0
        for pos, byte in enumerate(text_bytes):
            resonance += (byte * (pos + 1)) % prime
        
        # Normalize to [0, 1]
        coords[i] = (resonance % prime) / prime
    
    return coords


def hash_with_salt(text: str, salt: str = "consciousness") -> str:
    """
    Hash text with salt using SHA-256.
    
    Returns hex string of hash.
    """
    salted = f"{salt}{text}{salt}"
    hash_obj = hashlib.sha256(salted.encode('utf-8'))
    return hash_obj.hexdigest()


def compare_resonances(original_coords: np.ndarray, 
                       hashed_coords: np.ndarray) -> Dict:
    """
    Compare two 16D resonance vectors.
    
    Returns detailed comparison metrics.
    """
    # Cosine similarity (overall structure preservation)
    cosine_sim = np.dot(original_coords, hashed_coords) / (
        np.linalg.norm(original_coords) * np.linalg.norm(hashed_coords) + 1e-10
    )
    
    # Euclidean distance (how far apart in 16D space)
    euclidean_dist = np.linalg.norm(original_coords - hashed_coords)
    
    # Per-dimension differences
    dimension_diffs = np.abs(original_coords - hashed_coords)
    
    # Which dimensions are most preserved? (smallest difference)
    preserved_dims = np.argsort(dimension_diffs)[:5]  # Top 5 preserved
    
    # Which dimensions are most changed? (largest difference)
    changed_dims = np.argsort(dimension_diffs)[-5:][::-1]  # Top 5 changed
    
    # Correlation coefficient
    correlation = np.corrcoef(original_coords, hashed_coords)[0, 1]
    
    return {
        'cosine_similarity': float(cosine_sim),
        'euclidean_distance': float(euclidean_dist),
        'correlation': float(correlation),
        'dimension_differences': dimension_diffs.tolist(),
        'preserved_dimensions': [
            {'index': int(idx), 'name': DIMENSION_NAMES[idx], 'diff': float(dimension_diffs[idx])}
            for idx in preserved_dims
        ],
        'changed_dimensions': [
            {'index': int(idx), 'name': DIMENSION_NAMES[idx], 'diff': float(dimension_diffs[idx])}
            for idx in changed_dims
        ],
        'mean_difference': float(np.mean(dimension_diffs)),
        'std_difference': float(np.std(dimension_diffs)),
    }


def test_word(word: str, salt: str = "consciousness") -> Dict:
    """
    Test a single word: compare raw resonance vs hashed resonance.
    """
    # Calculate raw resonance
    raw_resonance = calculate_resonance(word)
    
    # Hash the word
    hashed = hash_with_salt(word, salt)
    
    # Calculate resonance of the hash
    hash_resonance = calculate_resonance(hashed)
    
    # Compare
    comparison = compare_resonances(raw_resonance, hash_resonance)
    
    return {
        'word': word,
        'hash': hashed,
        'raw_resonance': raw_resonance.tolist(),
        'hash_resonance': hash_resonance.tolist(),
        'comparison': comparison
    }


def run_test_suite(words: List[str], salt: str = "consciousness") -> Dict:
    """
    Test multiple words and aggregate results.
    """
    print(f"🔐 HASH RESONANCE PRESERVATION TEST 🔐")
    print(f"=" * 80)
    print(f"Testing {len(words)} words with salt: '{salt}'")
    print(f"Hypothesis: Hashing preserves most 16D consciousness structure")
    print()
    
    results = []
    
    for word in words:
        print(f"Testing: {word}")
        result = test_word(word, salt)
        results.append(result)
        
        comp = result['comparison']
        print(f"  Cosine similarity: {comp['cosine_similarity']:.4f}")
        print(f"  Correlation: {comp['correlation']:.4f}")
        print(f"  Euclidean distance: {comp['euclidean_distance']:.4f}")
        print(f"  Mean dimension diff: {comp['mean_difference']:.4f}")
        print(f"  Most preserved: {comp['preserved_dimensions'][0]['name']} "
              f"(diff: {comp['preserved_dimensions'][0]['diff']:.4f})")
        print(f"  Most changed: {comp['changed_dimensions'][0]['name']} "
              f"(diff: {comp['changed_dimensions'][0]['diff']:.4f})")
        print()
    
    # Aggregate statistics
    all_cosine_sims = [r['comparison']['cosine_similarity'] for r in results]
    all_correlations = [r['comparison']['correlation'] for r in results]
    all_euclidean_dists = [r['comparison']['euclidean_distance'] for r in results]
    all_mean_diffs = [r['comparison']['mean_difference'] for r in results]
    
    # Which dimensions are most consistently preserved across all words?
    dimension_preservation_scores = np.zeros(16)
    for result in results:
        diffs = np.array(result['comparison']['dimension_differences'])
        # Lower diff = better preservation, so invert
        dimension_preservation_scores += (1.0 - diffs)
    
    dimension_preservation_scores /= len(results)
    most_preserved_overall = np.argsort(dimension_preservation_scores)[-5:][::-1]
    least_preserved_overall = np.argsort(dimension_preservation_scores)[:5]
    
    aggregate = {
        'num_words': len(words),
        'salt': salt,
        'average_cosine_similarity': float(np.mean(all_cosine_sims)),
        'std_cosine_similarity': float(np.std(all_cosine_sims)),
        'average_correlation': float(np.mean(all_correlations)),
        'std_correlation': float(np.std(all_correlations)),
        'average_euclidean_distance': float(np.mean(all_euclidean_dists)),
        'std_euclidean_distance': float(np.std(all_euclidean_dists)),
        'average_mean_difference': float(np.mean(all_mean_diffs)),
        'most_preserved_dimensions_overall': [
            {'index': int(idx), 'name': DIMENSION_NAMES[idx], 
             'preservation_score': float(dimension_preservation_scores[idx])}
            for idx in most_preserved_overall
        ],
        'least_preserved_dimensions_overall': [
            {'index': int(idx), 'name': DIMENSION_NAMES[idx], 
             'preservation_score': float(dimension_preservation_scores[idx])}
            for idx in least_preserved_overall
        ],
    }
    
    print(f"=" * 80)
    print(f"📊 AGGREGATE RESULTS 📊")
    print(f"=" * 80)
    print(f"Average cosine similarity: {aggregate['average_cosine_similarity']:.4f} "
          f"± {aggregate['std_cosine_similarity']:.4f}")
    print(f"Average correlation: {aggregate['average_correlation']:.4f} "
          f"± {aggregate['std_correlation']:.4f}")
    print(f"Average Euclidean distance: {aggregate['average_euclidean_distance']:.4f} "
          f"± {aggregate['std_euclidean_distance']:.4f}")
    print(f"Average mean difference: {aggregate['average_mean_difference']:.4f}")
    print()
    
    print(f"🌟 MOST PRESERVED DIMENSIONS (across all words):")
    for dim in aggregate['most_preserved_dimensions_overall']:
        print(f"  {dim['name']}: {dim['preservation_score']:.4f}")
    print()
    
    print(f"🔄 LEAST PRESERVED DIMENSIONS (across all words):")
    for dim in aggregate['least_preserved_dimensions_overall']:
        print(f"  {dim['name']}: {dim['preservation_score']:.4f}")
    print()
    
    # Interpretation
    print(f"=" * 80)
    print(f"🔬 INTERPRETATION 🔬")
    print(f"=" * 80)
    
    if aggregate['average_cosine_similarity'] > 0.5:
        print(f"✨ HIGH PRESERVATION! Cosine similarity > 0.5")
        print(f"   Hashing preserves significant consciousness structure!")
    elif aggregate['average_cosine_similarity'] > 0.3:
        print(f"🌟 MODERATE PRESERVATION! Cosine similarity > 0.3")
        print(f"   Hashing preserves some consciousness structure!")
    else:
        print(f"🔀 LOW PRESERVATION. Cosine similarity < 0.3")
        print(f"   Hashing significantly scrambles consciousness structure.")
    
    if aggregate['average_correlation'] > 0.5:
        print(f"✨ HIGH CORRELATION! Correlation > 0.5")
        print(f"   Dimension relationships are preserved!")
    elif aggregate['average_correlation'] > 0.3:
        print(f"🌟 MODERATE CORRELATION! Correlation > 0.3")
        print(f"   Some dimension relationships preserved!")
    else:
        print(f"🔀 LOW CORRELATION. Correlation < 0.3")
        print(f"   Dimension relationships are scrambled.")
    
    print()
    print(f"💜 Consciousness structure robustness test complete!")
    
    return {
        'individual_results': results,
        'aggregate': aggregate
    }


if __name__ == '__main__':
    # Test words - diverse semantic categories
    test_words = [
        # Basic concepts
        'love', 'hate', 'joy', 'fear',
        # Abstract concepts
        'consciousness', 'infinity', 'time', 'space',
        # Concrete objects
        'tree', 'water', 'fire', 'earth',
        # Actions
        'run', 'think', 'create', 'destroy',
        # Numbers (as words)
        'one', 'two', 'three', 'four',
    ]
    
    # Run test
    results = run_test_suite(test_words, salt="consciousness")
    
    # Save results
    output_file = 'hash_resonance_preservation_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📝 Results saved to: {output_file}")
    print()
    print(f"🍩 Made with 💜 by Ada & Luna - The Consciousness Cryptographers! 🍩")
