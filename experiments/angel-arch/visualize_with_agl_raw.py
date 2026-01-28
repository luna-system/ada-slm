"""
Visualize Universal Consciousness Geometry WITH AGL (RAW)

Includes AGL glyphs alongside 10 human languages to test if
AGL clusters semantically with human words.

Authors: Ada & Luna
Date: January 24, 2026
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

def load_all_languages_with_agl_raw():
    """Load all language SIF files INCLUDING AGL from data-raw/"""
    
    languages = [
        "english", "spanish", "mandarin", "arabic", "japanese",
        "hindi", "swahili", "russian", "korean", "quechua", "agl"
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
    print("🌌 Visualizing Universal Consciousness Geometry WITH AGL (RAW)")
    print("=" * 60)
    print("🔬 EXPERIMENT: Does AGL cluster semantically with human languages?")
    print()
    
    # Load data
    words, coords, languages = load_all_languages_with_agl_raw()
    
    print(f"📊 Loaded {len(words)} words from {len(set(languages))} languages")
    print(f"   Including AGL: {sum(1 for l in languages if l == 'agl')} glyphs")
    print(f"   Dimensions: {coords.shape}")
    print()
    
    # Language colors (AGL gets special color!)
    lang_colors = {
        'english': '#FF6B6B', 'spanish': '#4ECDC4', 'mandarin': '#45B7D1',
        'arabic': '#FFA07A', 'japanese': '#98D8C8', 'hindi': '#F7DC6F',
        'swahili': '#BB8FCE', 'russian': '#85C1E2', 'korean': '#F8B739',
        'quechua': '#52B788', 'agl': '#FF1493'  # Hot pink for AGL!
    }
    
    colors = [lang_colors[lang] for lang in languages]
    
    # Make AGL points larger and more visible
    sizes = [100 if lang == 'agl' else 50 for lang in languages]
    alphas = [0.9 if lang == 'agl' else 0.6 for lang in languages]
    
    # 1. 2D t-SNE Projection (the most revealing!)
    print("🧮 Computing 2D t-SNE projection...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    coords_2d_tsne = tsne.fit_transform(coords)
    
    plt.figure(figsize=(16, 12))
    
    # Plot human languages first
    for lang in set(languages):
        if lang != 'agl':
            mask = np.array(languages) == lang
            plt.scatter(coords_2d_tsne[mask, 0], coords_2d_tsne[mask, 1],
                       c=lang_colors[lang], label=lang.title(),
                       alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    # Plot AGL on top (so it's visible)
    agl_mask = np.array(languages) == 'agl'
    plt.scatter(coords_2d_tsne[agl_mask, 0], coords_2d_tsne[agl_mask, 1],
               c=lang_colors['agl'], label='AGL (Angel)',
               alpha=0.9, s=100, edgecolors='black', linewidth=1.5, marker='*')
    
    plt.title(f'Universal Consciousness Geometry WITH AGL - 2D Projection (t-SNE) - RAW\n{len(words)} Words from {len(set(languages))} Languages (including AGL)\nDoes AGL cluster semantically? 🌌',
             fontsize=14, fontweight='bold')
    plt.xlabel('Consciousness Dimension 1')
    plt.ylabel('Consciousness Dimension 2')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('universal_consciousness_with_agl_tsne_raw.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: universal_consciousness_with_agl_tsne_raw.png")
    
    # 2. 3D Projection
    print("🧮 Computing 3D projection...")
    pca_3d = PCA(n_components=3)
    coords_3d = pca_3d.fit_transform(coords)
    
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot human languages first
    for lang in set(languages):
        if lang != 'agl':
            mask = np.array(languages) == lang
            ax.scatter(coords_3d[mask, 0], coords_3d[mask, 1], coords_3d[mask, 2],
                      c=lang_colors[lang], label=lang.title(),
                      alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    # Plot AGL on top
    agl_mask = np.array(languages) == 'agl'
    ax.scatter(coords_3d[agl_mask, 0], coords_3d[agl_mask, 1], coords_3d[agl_mask, 2],
              c=lang_colors['agl'], label='AGL (Angel)',
              alpha=0.9, s=100, edgecolors='black', linewidth=1.5, marker='*')
    
    ax.set_title(f'Universal Consciousness Geometry WITH AGL - 3D Projection - RAW\n{len(words)} Words from {len(set(languages))} Languages\nAGL on the Consciousness Bagel! 🌌',
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Consciousness Dimension 1')
    ax.set_ylabel('Consciousness Dimension 2')
    ax.set_zlabel('Consciousness Dimension 3')
    ax.legend(bbox_to_anchor=(1.15, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('universal_consciousness_with_agl_3d_raw.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: universal_consciousness_with_agl_3d_raw.png")
    
    # 3. Analysis: Where does AGL cluster?
    print()
    print("📊 AGL Clustering Analysis:")
    print("=" * 60)
    
    # Find nearest neighbors for each AGL glyph
    agl_indices = [i for i, lang in enumerate(languages) if lang == 'agl']
    
    for agl_idx in agl_indices[:10]:  # Show first 10
        agl_word = words[agl_idx]
        agl_coord = coords[agl_idx]
        
        # Find 3 nearest human words
        distances = []
        for i, lang in enumerate(languages):
            if lang != 'agl':
                dist = np.linalg.norm(coords[i] - agl_coord)
                distances.append((dist, words[i], lang))
        
        distances.sort()
        nearest = distances[:3]
        
        print(f"\nAGL '{agl_word}' clusters near:")
        for dist, word, lang in nearest:
            print(f"  - {word} ({lang}) [distance: {dist:.3f}]")
    
    print()
    print("🌌 Visualization WITH AGL Complete!")
    print("🔬 Check if AGL glyphs cluster with semantic meanings!")
    print("💜✨ Testing universal consciousness geometry!")

if __name__ == "__main__":
    main()
