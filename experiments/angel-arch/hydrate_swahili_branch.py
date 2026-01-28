"""
Hydrate Swahili Language Branch SIF

Takes the top 100 Swahili words and maps them to 16D consciousness coordinates.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
from generate_language_sif import UniversalLanguageSIFGenerator


def main():
    """Hydrate Swahili branch with top 100 words"""
    
    # Top 100 Swahili words from 1000mostcommonwords.com
    top_100_swahili = [
        "kama", "mimi", "yake", "kwamba", "yeye", "mara", "kwa", "juu ya", "wako", "kwa",
        "wao", "kuwa", "katika", "moja", "na", "hii", "kutoka", "na", "moto", "neno",
        "lakini", "nini", "baadhi", "ni", "yake", "ninyi", "au", "alikuwa", "akaonekana", "ya",
        "kwa", "na", "a", "katika", "sisi", "unaweza", "nje", "nyingine", "walikuwa", "ambayo",
        "kufanya", "yao", "wakati", "kama", "mapenzi", "jinsi", "alisema", "an", "kila", "kuwaambia",
        "gani", "kuweka", "tatu", "wanataka", "hewa", "vizuri", "pia", "kucheza", "ndogo", "mwisho",
        "kuweka", "nyumbani", "kusoma", "mkono", "bandari", "kubwa", "Spell", "kuongeza", "hata", "ardhi",
        "hapa", "lazima", "kubwa", "high", "kama", "kufuata", "tendo", "kwa nini", "kuuliza", "wanaume",
        "mabadiliko ya", "akaenda", "mwanga", "aina", "mbali", "haja", "nyumba", "picha", "kujaribu", "sisi",
        "tena", "mnyama", "uhakika", "mama", "dunia", "karibu", "kujenga", "binafsi", "dunia", "baba"
    ]
    
    print(f"🌌 Hydrating Swahili branch with {len(top_100_swahili)} words...")
    
    # Initialize generator
    generator = UniversalLanguageSIFGenerator()
    
    # Language metadata
    language_metadata = {
        "name": "Swahili",
        "family": "Bantu (Niger-Congo)",
        "writing_system": "Latin"
    }
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        top_100_swahili,
        "swahili",
        language_metadata
    )
    
    # Save to file
    output_path = "ada-slm/experiments/angel-arch/data/language_swahili_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ Swahili Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ Swahili branch hydration complete! 🍩✨")


if __name__ == "__main__":
    main()
