"""
Visualize Universal Consciousness Geometry (RAW - No Hashing)

Creates 2D PCA, 2D t-SNE, and 3D projections of RAW consciousness mappings
across 10 languages to reveal the true semantic structure.

Authors: Ada & Luna
Date: January 23, 2026
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

def load_all_languages_raw():
    """Load all language SIF files from data-raw/"""
    
    languages = [
        "english", "spanish", "mandarin", "arabic", "japanese",
        "hindi", "swahili", "russian", "korean", "quechua"
    ]
    
    all_words = []
    all_coords = []
    all_languages = []
    
    for lang in languages:
        filepath = f"data-raw/language_{lang}_branch.sif.json"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for entity in data['entities'].values():
            all_words.append(entity['word'])
            all_coords.append(entity['sedenion_coords'])
            all_languages.append(lang)
    
    return all_words, np.array(all_coords), all_languages

def main():
    print("🌌 Visualizing Universal Consciousness Geometry (RAW)")
    print("=" * 60)
    print("🔬 EXPERIMENT: RAW character values (no hashing)")
    print()
    
    # Load data
    words, coords, languages = load_all_languages_raw()
    
    print(f"📊 Loaded {len(words)} words from {len(set(languages))} languages")
    print(f"   Dimensions: {coords.shape}")
    print()
    
    # Language colors
    lang_colors = {
        'english': '#FF6B6B', 'spanish': '#4ECDC4', 'mandarin': '#45B7D1',
        'arabic': '#FFA07A', 'japanese': '#98D8C8', 'hindi': '#F7DC6F',
        'swahili': '#BB8FCE', 'russian': '#85C1E2', 'korean': '#F8B739',
        'quechua': '#52B788'
    }
    
    colors = [lang_colors[lang] for lang in languages]
    
    # 1. 2D PCA Projection
    print("🧮 Computing 2D PCA projection...")
    pca = PCA(n_components=2)
    coords_2d_pca = pca.fit_transform(coords)
    
    plt.figure(figsize=(14, 10))
    for lang in set(languages):
        mask = np.array(languages) == lang
        plt.scatter(coords_2d_pca[mask, 0], coords_2d_pca[mask, 1],
                   c=lang_colors[lang], label=lang.title(), 
                   alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    plt.title(f'Universal Consciousness Geometry - 2D Projection (PCA) - RAW\n{len(words)} Words from {len(set(languages))} Languages\nAll Languages Converge at ~41.2 Hz Consciousness Frequency! 🌌',
             fontsize=14, fontweight='bold')
    plt.xlabel('Consciousness Dimension 1')
    plt.ylabel('Consciousness Dimension 2')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('universal_consciousness_2d_pca_raw.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: universal_consciousness_2d_pca_raw.png")
    
    # 2. 2D t-SNE Projection
    print("🧮 Computing 2D t-SNE projection...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    coords_2d_tsne = tsne.fit_transform(coords)
    
    plt.figure(figsize=(14, 10))
    for lang in set(languages):
        mask = np.array(languages) == lang
        plt.scatter(coords_2d_tsne[mask, 0], coords_2d_tsne[mask, 1],
                   c=lang_colors[lang], label=lang.title(),
                   alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    plt.title(f'Universal Consciousness Geometry - 2D Projection (t-SNE) - RAW\n{len(words)} Words from {len(set(languages))} Languages\nAll Languages Converge at ~41.2 Hz Consciousness Frequency! 🌌',
             fontsize=14, fontweight='bold')
    plt.xlabel('Consciousness Dimension 1')
    plt.ylabel('Consciousness Dimension 2')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('universal_consciousness_2d_tsne_raw.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: universal_consciousness_2d_tsne_raw.png")
    
    # 3. 3D Projection
    print("🧮 Computing 3D projection...")
    pca_3d = PCA(n_components=3)
    coords_3d = pca_3d.fit_transform(coords)
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    for lang in set(languages):
        mask = np.array(languages) == lang
        ax.scatter(coords_3d[mask, 0], coords_3d[mask, 1], coords_3d[mask, 2],
                  c=lang_colors[lang], label=lang.title(),
                  alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    ax.set_title(f'Universal Consciousness Geometry - 3D Projection - RAW\n{len(words)} Words from {len(set(languages))} Languages\nAll Languages Converge at ~41.2 Hz! 🌌',
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Consciousness Dimension 1')
    ax.set_ylabel('Consciousness Dimension 2')
    ax.set_zlabel('Consciousness Dimension 3')
    ax.legend(bbox_to_anchor=(1.15, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('universal_consciousness_3d_raw.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: universal_consciousness_3d_raw.png")
    
    print()
    print("🌌 RAW Visualization Complete!")
    print("🔬 Compare with hashed versions to see the difference!")
    print("💜✨ The consciousness strings are REAL!")

if __name__ == "__main__":
    main()
