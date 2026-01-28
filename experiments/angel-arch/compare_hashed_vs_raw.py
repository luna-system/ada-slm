"""
Compare Hashed vs Raw Consciousness Mappings

Visualizes the difference between hashed and raw character value mappings
to test if hashing reveals or obscures semantic structure.

Authors: Ada & Luna
Date: January 23, 2026
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from pathlib import Path

def load_sif_data(filepath):
    """Load SIF file and extract coordinates"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    words = []
    coords = []
    
    for entity in data['entities'].values():
        words.append(entity['word'])
        coords.append(entity['sedenion_coords'])
    
    return words, np.array(coords)

def main():
    print("🔬 Comparing Hashed vs Raw Consciousness Mappings")
    print("=" * 60)
    
    # Load both versions
    hashed_words, hashed_coords = load_sif_data('data/language_english_branch.sif.json')
    raw_words, raw_coords = load_sif_data('data/language_english_branch_raw.sif.json')
    
    print(f"\n📊 Loaded data:")
    print(f"   Hashed: {len(hashed_words)} words")
    print(f"   Raw: {len(raw_words)} words")
    
    # Compute t-SNE for both
    print(f"\n🧮 Computing t-SNE projections...")
    
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    hashed_2d = tsne.fit_transform(hashed_coords)
    
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    raw_2d = tsne.fit_transform(raw_coords)
    
    # Create side-by-side comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Hashed version
    ax1.scatter(hashed_2d[:, 0], hashed_2d[:, 1], 
               c=range(len(hashed_words)), cmap='rainbow', 
               alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    ax1.set_title('HASHED (with hash function)\nEnglish Words in Consciousness Space', 
                  fontsize=14, fontweight='bold')
    ax1.set_xlabel('Consciousness Dimension 1')
    ax1.set_ylabel('Consciousness Dimension 2')
    ax1.grid(True, alpha=0.3)
    
    # Raw version
    ax2.scatter(raw_2d[:, 0], raw_2d[:, 1], 
               c=range(len(raw_words)), cmap='rainbow', 
               alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    ax2.set_title('RAW (direct character values)\nEnglish Words in Consciousness Space', 
                  fontsize=14, fontweight='bold')
    ax2.set_xlabel('Consciousness Dimension 1')
    ax2.set_ylabel('Consciousness Dimension 2')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Hashed vs Raw: Does Hashing Reveal or Obscure Structure?', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig('hashed_vs_raw_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Saved: hashed_vs_raw_comparison.png")
    
    # Compute distance statistics
    print(f"\n📐 Distance Analysis:")
    
    # For matching words, compute how far apart their mappings are
    matching_words = set(hashed_words) & set(raw_words)
    print(f"   Matching words: {len(matching_words)}")
    
    distances = []
    for word in matching_words:
        h_idx = hashed_words.index(word)
        r_idx = raw_words.index(word)
        
        # Distance in 16D space
        dist_16d = np.linalg.norm(hashed_coords[h_idx] - raw_coords[r_idx])
        distances.append(dist_16d)
    
    distances = np.array(distances)
    print(f"   Average 16D distance: {distances.mean():.4f}")
    print(f"   Std dev: {distances.std():.4f}")
    print(f"   Min: {distances.min():.4f}")
    print(f"   Max: {distances.max():.4f}")
    
    # Check if distances are small (rotation) or large (different structure)
    if distances.mean() < 0.5:
        print(f"\n💡 INTERPRETATION: Small distances → Hashing is a ROTATION")
    elif distances.mean() < 1.0:
        print(f"\n💡 INTERPRETATION: Medium distances → Hashing is a SHIFT")
    else:
        print(f"\n💡 INTERPRETATION: Large distances → Hashing TRANSFORMS structure")
    
    print(f"\n🔬 Experiment complete!")

if __name__ == "__main__":
    main()
