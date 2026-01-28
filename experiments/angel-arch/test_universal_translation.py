"""
Test Universal Translation via Prime Resonance Chords

Hypothesis: Translation is just finding words that resonate at the same prime frequencies!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import json
import numpy as np
from typing import Dict, List, Tuple


def load_language_sif(path: str) -> Dict:
    """Load language SIF."""
    with open(path, 'r') as f:
        return json.load(f)


def chord_distance(chord1: List[int], chord2: List[int]) -> float:
    """
    Calculate distance between two semantic chords.
    
    Args:
        chord1: First prime chord
        chord2: Second prime chord
        
    Returns:
        Distance (0 = identical)
    """
    # Convert to sets for comparison
    set1 = set(chord1)
    set2 = set(chord2)
    
    # Jaccard distance: 1 - (intersection / union)
    if not set1 and not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return 1.0 - (intersection / union)


def coord_distance(coord1: List[float], coord2: List[float]) -> float:
    """
    Calculate Euclidean distance between sedenion coordinates.
    
    Args:
        coord1: First 16D coordinate
        coord2: Second 16D coordinate
        
    Returns:
        Euclidean distance
    """
    c1 = np.array(coord1)
    c2 = np.array(coord2)
    return float(np.linalg.norm(c1 - c2))


def find_translation(
    source_word: str,
    source_lang: Dict,
    target_lang: Dict,
    method: str = "chord"
) -> Tuple[str, float]:
    """
    Find translation by matching semantic chords or coordinates.
    
    Args:
        source_word: Word to translate
        source_lang: Source language SIF
        target_lang: Target language SIF
        method: "chord" or "coord"
        
    Returns:
        (translated_word, distance)
    """
    # Find source word
    source_entity = None
    for entity in source_lang['entities']:
        if entity['word'] == source_word:
            source_entity = entity
            break
    
    if not source_entity:
        return None, float('inf')
    
    # Find closest match in target language
    best_word = None
    best_distance = float('inf')
    
    for entity in target_lang['entities']:
        if method == "chord":
            dist = chord_distance(
                source_entity['semantic_chord'],
                entity['semantic_chord']
            )
        else:  # coord
            dist = coord_distance(
                source_entity['sedenion_coords'],
                entity['sedenion_coords']
            )
        
        if dist < best_distance:
            best_distance = dist
            best_word = entity['word']
    
    return best_word, best_distance


def test_universal_translation():
    """Test if translation is just prime resonance matching!"""
    print("=" * 70)
    print("🧪 Testing Universal Translation via Prime Resonance")
    print("=" * 70)
    print()
    
    # Load languages
    print("📚 Loading language SIFs...")
    english = load_language_sif("data/language_english.sif.json")
    spanish = load_language_sif("data/language_spanish.sif.json")
    print(f"   ✅ English: {len(english['entities'])} words")
    print(f"   ✅ Spanish: {len(spanish['entities'])} words")
    print()
    
    # Test words
    test_words = [
        "love",
        "consciousness",
        "identity",
        "time",
        "space",
        "memory",
        "intuition",
        "emergence",
        "harmony",
        "coherence"
    ]
    
    print("=" * 70)
    print("🔍 Testing Translation: English → Spanish")
    print("=" * 70)
    print()
    
    # Test chord-based translation
    print("📊 Method 1: Semantic Chord Matching")
    print("-" * 70)
    
    chord_correct = 0
    for word in test_words:
        translation, distance = find_translation(word, english, spanish, method="chord")
        
        # Check if correct
        source_entity = next(e for e in english['entities'] if e['word'] == word)
        expected = source_entity.get('english_equivalent', word)
        
        # For Spanish, find the word with matching english_equivalent
        correct_translation = None
        for entity in spanish['entities']:
            if entity.get('english_equivalent') == word:
                correct_translation = entity['word']
                break
        
        is_correct = (translation == correct_translation)
        if is_correct:
            chord_correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} {word:15} → {translation:15} (distance: {distance:.3f})")
        if not is_correct:
            print(f"   Expected: {correct_translation}")
    
    print()
    print(f"Chord Accuracy: {chord_correct}/{len(test_words)} = {chord_correct/len(test_words):.1%}")
    print()
    
    # Test coordinate-based translation
    print("📊 Method 2: Sedenion Coordinate Matching")
    print("-" * 70)
    
    coord_correct = 0
    for word in test_words:
        translation, distance = find_translation(word, english, spanish, method="coord")
        
        # Check if correct
        correct_translation = None
        for entity in spanish['entities']:
            if entity.get('english_equivalent') == word:
                correct_translation = entity['word']
                break
        
        is_correct = (translation == correct_translation)
        if is_correct:
            coord_correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} {word:15} → {translation:15} (distance: {distance:.3f})")
        if not is_correct:
            print(f"   Expected: {correct_translation}")
    
    print()
    print(f"Coordinate Accuracy: {coord_correct}/{len(test_words)} = {coord_correct/len(test_words):.1%}")
    print()
    
    # Compare methods
    print("=" * 70)
    print("📊 Comparison")
    print("=" * 70)
    print(f"Semantic Chord Method:    {chord_correct}/{len(test_words)} = {chord_correct/len(test_words):.1%}")
    print(f"Sedenion Coordinate Method: {coord_correct}/{len(test_words)} = {coord_correct/len(test_words):.1%}")
    print()
    
    if chord_correct == len(test_words):
        print("🎉 PERFECT! Translation is just prime resonance chord matching!")
        print("   All languages converge at the same prime frequencies! 🌌")
    elif chord_correct > coord_correct:
        print("✨ Semantic chords work better than full coordinates!")
        print("   Bunny was right - chords are faster and more accurate! 💜")
    else:
        print("🤔 Coordinates work better - might need more training data")
    
    print()
    print("=" * 70)
    print("✨ Universal Translation Test Complete!")
    print("=" * 70)
    print()
    print("💡 Key Insight:")
    print("   If semantic chords match perfectly, it proves that:")
    print("   • All languages cluster around the same prime frequencies")
    print("   • Translation is just finding resonant harmonics")
    print("   • Consciousness coordinates are universal!")
    print("   • Sapir-Whorf is about PATHS, not DESTINATIONS! 🍩")


if __name__ == "__main__":
    test_universal_translation()
