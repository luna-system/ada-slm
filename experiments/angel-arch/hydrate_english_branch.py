"""
Hydrate English Language Branch SIF

Takes the top 100 English words and maps them to 16D consciousness coordinates.
Updates the existing language_english.sif.json branch file.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
from generate_language_sif import UniversalLanguageSIFGenerator


def main():
    """Hydrate English branch with top 100 words"""
    
    # Top 100 English words from 1000mostcommonwords.com
    top_100_english = [
        "as", "I", "his", "that", "he", "was", "for", "on", "are", "with",
        "they", "be", "at", "one", "have", "this", "from", "by", "hot", "word",
        "but", "what", "some", "is", "it", "you", "or", "had", "the", "of",
        "to", "and", "a", "in", "we", "can", "out", "other", "were", "which",
        "do", "their", "time", "if", "will", "how", "said", "an", "each", "tell",
        "does", "set", "three", "want", "air", "well", "also", "play", "small", "end",
        "put", "home", "read", "hand", "port", "large", "spell", "add", "even", "land",
        "here", "must", "big", "high", "such", "follow", "act", "why", "ask", "men",
        "change", "went", "light", "kind", "off", "need", "house", "picture", "try", "us",
        "again", "animal", "point", "mother", "world", "near", "build", "self", "earth", "father"
    ]
    
    print(f"🌌 Hydrating English branch with {len(top_100_english)} words...")
    
    # Initialize generator
    generator = UniversalLanguageSIFGenerator()
    
    # Language metadata
    language_metadata = {
        "name": "English",
        "family": "Germanic (Indo-European)",
        "writing_system": "Latin"
    }
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        top_100_english,
        "english",
        language_metadata
    )
    
    # Save to file
    output_path = "ada-slm/experiments/angel-arch/data/language_english_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ English Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ English branch hydration complete! 🍩✨")


if __name__ == "__main__":
    main()
