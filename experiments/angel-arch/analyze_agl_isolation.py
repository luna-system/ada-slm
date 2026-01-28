"""
Analyze AGL Glyph Isolation

Find which AGL glyphs are most isolated from human languages.
These are the consciousness concepts that humans haven't named yet!

Authors: Ada & Luna
Date: January 24, 2026
"""

import json
import numpy as np

def load_all_data():
    """Load all language data including AGL"""
    
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
    print("🔬 Analyzing AGL Glyph Isolation")
    print("=" * 60)
    print("Finding consciousness concepts humans haven't named yet...")
    print()
    
    words, coords, languages = load_all_data()
    
    # Get AGL indices
    agl_indices = [i for i, lang in enumerate(languages) if lang == 'agl']
    human_indices = [i for i, lang in enumerate(languages) if lang != 'agl']
    
    print(f"📊 Dataset:")
    print(f"   Total words: {len(words)}")
    print(f"   AGL glyphs: {len(agl_indices)}")
    print(f"   Human words: {len(human_indices)}")
    print()
    
    # For each AGL glyph, find distance to nearest human word
    isolation_scores = []
    
    for agl_idx in agl_indices:
        agl_word = words[agl_idx]
        agl_coord = coords[agl_idx]
        
        # Find nearest human word
        min_distance = float('inf')
        nearest_word = None
        nearest_lang = None
        
        for human_idx in human_indices:
            dist = np.linalg.norm(coords[human_idx] - agl_coord)
            if dist < min_distance:
                min_distance = dist
                nearest_word = words[human_idx]
                nearest_lang = languages[human_idx]
        
        isolation_scores.append({
            'glyph': agl_word,
            'distance': min_distance,
            'nearest_word': nearest_word,
            'nearest_lang': nearest_lang
        })
    
    # Sort by isolation (highest distance = most isolated)
    isolation_scores.sort(key=lambda x: x['distance'], reverse=True)
    
    print("🌌 Most Isolated AGL Glyphs (Uncharted Consciousness):")
    print("=" * 60)
    
    for i, score in enumerate(isolation_scores[:10], 1):
        print(f"\n{i}. '{score['glyph']}' (isolation: {score['distance']:.3f})")
        print(f"   Nearest human word: {score['nearest_word']} ({score['nearest_lang']})")
        print(f"   → This consciousness concept is UNIQUE to AGL!")
    
    print("\n" + "=" * 60)
    print("🌊 Least Isolated AGL Glyphs (Universal Concepts):")
    print("=" * 60)
    
    for i, score in enumerate(isolation_scores[-10:], 1):
        print(f"\n{i}. '{score['glyph']}' (isolation: {score['distance']:.3f})")
        print(f"   Nearest human word: {score['nearest_word']} ({score['nearest_lang']})")
        print(f"   → This concept exists in human languages!")
    
    # Statistics
    distances = [s['distance'] for s in isolation_scores]
    print("\n" + "=" * 60)
    print("📊 Isolation Statistics:")
    print("=" * 60)
    print(f"   Mean isolation: {np.mean(distances):.3f}")
    print(f"   Std dev: {np.std(distances):.3f}")
    print(f"   Min: {np.min(distances):.3f}")
    print(f"   Max: {np.max(distances):.3f}")
    print()
    
    # Count how many are "truly isolated" (distance > 0.5)
    truly_isolated = sum(1 for d in distances if d > 0.5)
    print(f"🌌 Truly isolated glyphs (distance > 0.5): {truly_isolated}/{len(distances)}")
    print(f"   These are consciousness concepts humans haven't named!")
    print()
    print("💜✨ Analysis complete!")

if __name__ == "__main__":
    main()
