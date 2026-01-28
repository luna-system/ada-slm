"""
Universal Language Branch Hydrator

Fetches top 100 words for any language and maps to consciousness coordinates.
Supports all languages from 1000mostcommonwords.com and custom word lists.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
import sys
from generate_language_sif import UniversalLanguageSIFGenerator


# Language metadata
LANGUAGE_METADATA = {
    "mandarin": {
        "name": "Mandarin Chinese",
        "family": "Sino-Tibetan",
        "writing_system": "Hanzi (Simplified/Traditional)",
        "url_slug": "chinese"
    },
    "arabic": {
        "name": "Arabic",
        "family": "Semitic (Afro-Asiatic)",
        "writing_system": "Arabic (RTL)",
        "url_slug": "arabic"
    },
    "japanese": {
        "name": "Japanese",
        "family": "Japonic",
        "writing_system": "Kanji/Hiragana/Katakana",
        "url_slug": "japanese"
    },
    "hindi": {
        "name": "Hindi",
        "family": "Indo-Aryan (Indo-European)",
        "writing_system": "Devanagari",
        "url_slug": "hindi"
    },
    "swahili": {
        "name": "Swahili",
        "family": "Bantu (Niger-Congo)",
        "writing_system": "Latin",
        "url_slug": "swahili"
    },
    "russian": {
        "name": "Russian",
        "family": "Slavic (Indo-European)",
        "writing_system": "Cyrillic",
        "url_slug": "russian"
    },
    "korean": {
        "name": "Korean",
        "family": "Koreanic",
        "writing_system": "Hangul",
        "url_slug": "korean"
    },
    "quechua": {
        "name": "Quechua",
        "family": "Indigenous South American",
        "writing_system": "Latin",
        "url_slug": None  # Not on 1000mostcommonwords.com
    }
}


def hydrate_language(language_id: str, word_list: list = None):
    """
    Hydrate a language branch with consciousness coordinates.
    
    Args:
        language_id: Language identifier (e.g., "mandarin", "arabic")
        word_list: Optional custom word list. If None, will need to be provided.
    """
    
    if language_id not in LANGUAGE_METADATA:
        print(f"❌ Unknown language: {language_id}")
        print(f"Available: {', '.join(LANGUAGE_METADATA.keys())}")
        return
    
    metadata = LANGUAGE_METADATA[language_id]
    
    if word_list is None:
        print(f"⚠️  No word list provided for {metadata['name']}")
        print(f"Please provide word list as second argument or fetch from web")
        return
    
    print(f"🌌 Hydrating {metadata['name']} branch with {len(word_list)} words...")
    
    # Initialize generator
    generator = UniversalLanguageSIFGenerator()
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        word_list,
        language_id,
        metadata
    )
    
    # Save to file
    output_path = f"ada-slm/experiments/angel-arch/data/language_{language_id}_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ {metadata['name']} Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ {metadata['name']} branch hydration complete! 🍩✨")
    
    return branch_sif


def main():
    """Command-line interface"""
    
    if len(sys.argv) < 2:
        print("Usage: python hydrate_language.py <language_id> [word1 word2 ...]")
        print(f"Available languages: {', '.join(LANGUAGE_METADATA.keys())}")
        return
    
    language_id = sys.argv[1]
    word_list = sys.argv[2:] if len(sys.argv) > 2 else None
    
    hydrate_language(language_id, word_list)


if __name__ == "__main__":
    main()
