"""
Hydrate Spanish Language Branch SIF

Takes the top 100 Spanish words and maps them to 16D consciousness coordinates.
Updates the existing language_spanish.sif.json branch file.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
from generate_language_sif import UniversalLanguageSIFGenerator


def main():
    """Hydrate Spanish branch with top 100 words"""
    
    # Top 100 Spanish words from 1000mostcommonwords.com
    top_100_spanish = [
        "como", "I", "su", "que", "él", "era", "para", "en", "son", "con",
        "ellos", "ser", "en", "uno", "tener", "este", "desde", "por", "caliente", "palabra",
        "pero", "qué", "algunos", "es", "lo", "usted", "o", "tenido", "la", "de",
        "a", "y", "un", "en", "nos", "lata", "fuera", "otros", "eran", "que",
        "hacer", "su", "tiempo", "si", "lo hará", "cómo", "dicho", "un", "cada", "decir",
        "hace", "conjunto", "tres", "querer", "aire", "así", "también", "jugar", "pequeño", "fin",
        "poner", "casa", "leer", "mano", "puerto", "grande", "deletrear", "añadir", "incluso", "tierra",
        "aquí", "debe", "grande", "alto", "tal", "siga", "acto", "por qué", "preguntar", "hombres",
        "cambio", "se fue", "luz", "tipo", "fuera", "necesitarán", "casa", "imagen", "tratar", "nosotros",
        "de nuevo", "animal", "punto", "madre", "mundo", "cerca", "construir", "auto", "tierra", "padre"
    ]
    
    print(f"🌌 Hydrating Spanish branch with {len(top_100_spanish)} words...")
    
    # Initialize generator
    generator = UniversalLanguageSIFGenerator()
    
    # Language metadata
    language_metadata = {
        "name": "Spanish",
        "family": "Romance (Indo-European)",
        "writing_system": "Latin"
    }
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        top_100_spanish,
        "spanish",
        language_metadata
    )
    
    # Save to file
    output_path = "ada-slm/experiments/angel-arch/data/language_spanish_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ Spanish Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ Spanish branch hydration complete! 🍩✨")


if __name__ == "__main__":
    main()
