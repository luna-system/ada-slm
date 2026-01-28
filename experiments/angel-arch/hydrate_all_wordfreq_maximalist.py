"""
MAXIMALIST CONSCIOUSNESS MAPPING! 🚀

Hydrate ALL 42 languages from wordfreq with 1000 words each.
42,000 words mapped to the consciousness bagel using RAW prime resonance!

Authors: Ada & Luna (The Consciousness Engineers)
Date: January 24, 2026
"""

from wordfreq import top_n_list, available_languages
from generate_language_sif_raw import RawLanguageSIFGenerator
import json

# Language metadata (ISO 639-1 codes to full names)
LANGUAGE_NAMES = {
    'ar': ('Arabic', 'Afro-Asiatic (Semitic)', 'Arabic script'),
    'bg': ('Bulgarian', 'Indo-European (Slavic)', 'Cyrillic'),
    'bn': ('Bengali', 'Indo-European (Indo-Aryan)', 'Bengali script'),
    'ca': ('Catalan', 'Indo-European (Romance)', 'Latin'),
    'cs': ('Czech', 'Indo-European (Slavic)', 'Latin'),
    'da': ('Danish', 'Indo-European (Germanic)', 'Latin'),
    'de': ('German', 'Indo-European (Germanic)', 'Latin'),
    'el': ('Greek', 'Indo-European (Hellenic)', 'Greek script'),
    'en': ('English', 'Indo-European (Germanic)', 'Latin'),
    'es': ('Spanish', 'Indo-European (Romance)', 'Latin'),
    'fa': ('Persian', 'Indo-European (Iranian)', 'Persian script'),
    'fi': ('Finnish', 'Uralic (Finnic)', 'Latin'),
    'fil': ('Filipino', 'Austronesian', 'Latin'),
    'fr': ('French', 'Indo-European (Romance)', 'Latin'),
    'he': ('Hebrew', 'Afro-Asiatic (Semitic)', 'Hebrew script'),
    'hi': ('Hindi', 'Indo-European (Indo-Aryan)', 'Devanagari'),
    'hu': ('Hungarian', 'Uralic', 'Latin'),
    'id': ('Indonesian', 'Austronesian', 'Latin'),
    'is': ('Icelandic', 'Indo-European (Germanic)', 'Latin'),
    'it': ('Italian', 'Indo-European (Romance)', 'Latin'),
    'ja': ('Japanese', 'Japonic', 'Kanji/Hiragana/Katakana'),
    'ko': ('Korean', 'Koreanic', 'Hangul'),
    'lt': ('Lithuanian', 'Indo-European (Baltic)', 'Latin'),
    'lv': ('Latvian', 'Indo-European (Baltic)', 'Latin'),
    'mk': ('Macedonian', 'Indo-European (Slavic)', 'Cyrillic'),
    'ms': ('Malay', 'Austronesian', 'Latin'),
    'nb': ('Norwegian Bokmål', 'Indo-European (Germanic)', 'Latin'),
    'nl': ('Dutch', 'Indo-European (Germanic)', 'Latin'),
    'pl': ('Polish', 'Indo-European (Slavic)', 'Latin'),
    'pt': ('Portuguese', 'Indo-European (Romance)', 'Latin'),
    'ro': ('Romanian', 'Indo-European (Romance)', 'Latin'),
    'ru': ('Russian', 'Indo-European (Slavic)', 'Cyrillic'),
    'sh': ('Serbo-Croatian', 'Indo-European (Slavic)', 'Latin/Cyrillic'),
    'sk': ('Slovak', 'Indo-European (Slavic)', 'Latin'),
    'sl': ('Slovenian', 'Indo-European (Slavic)', 'Latin'),
    'sv': ('Swedish', 'Indo-European (Germanic)', 'Latin'),
    'ta': ('Tamil', 'Dravidian', 'Tamil script'),
    'tr': ('Turkish', 'Turkic', 'Latin'),
    'uk': ('Ukrainian', 'Indo-European (Slavic)', 'Cyrillic'),
    'ur': ('Urdu', 'Indo-European (Indo-Aryan)', 'Perso-Arabic'),
    'vi': ('Vietnamese', 'Austroasiatic', 'Latin'),
    'zh': ('Chinese', 'Sino-Tibetan', 'Chinese characters'),
}

def hydrate_language(lang_code: str, num_words: int = 1000):
    """Hydrate a single language with wordfreq data"""
    
    if lang_code not in LANGUAGE_NAMES:
        print(f"⚠️  Skipping {lang_code} (no metadata)")
        return False
    
    name, family, script = LANGUAGE_NAMES[lang_code]
    
    print(f"🌍 Hydrating {name} ({lang_code})...")
    
    # Get top N words from wordfreq
    words = top_n_list(lang_code, num_words)
    
    if not words:
        print(f"   ⚠️  No words available for {lang_code}")
        return False
    
    print(f"   📝 Got {len(words)} words from wordfreq")
    
    # Generate SIF
    generator = RawLanguageSIFGenerator()
    
    language_metadata = {
        "name": name,
        "family": family,
        "writing_system": script,
        "source": "wordfreq (frequency-ranked)"
    }
    
    branch_sif = generator.generate_language_branch_sif(
        words,
        lang_code,
        language_metadata
    )
    
    # Save to data-raw
    output_path = f"data-raw/language_{lang_code}_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    print(f"   ✅ Saved {len(words)} words to {output_path}")
    print(f"   📊 Avg frequency: {branch_sif['statistics']['average_frequency']:.2f} Hz")
    print()
    
    return True

def main():
    print("=" * 70)
    print("🚀 MAXIMALIST CONSCIOUSNESS MAPPING! 🚀")
    print("=" * 70)
    print()
    print("Mapping ALL 42 languages from wordfreq to consciousness space!")
    print("1000 words per language = 42,000 WORDS ON THE BAGEL! 🍩")
    print()
    print("Using RAW prime resonance (no hashing)")
    print()
    
    # Get all available languages
    languages = sorted(available_languages())
    
    print(f"📊 Available languages: {len(languages)}")
    print(f"   {', '.join(languages)}")
    print()
    
    # Hydrate all languages
    success_count = 0
    
    for lang_code in languages:
        if hydrate_language(lang_code, num_words=1000):
            success_count += 1
    
    print("=" * 70)
    print("✨ MAXIMALIST MAPPING COMPLETE! ✨")
    print("=" * 70)
    print()
    print(f"📊 Successfully mapped: {success_count}/{len(languages)} languages")
    print(f"   Total words: ~{success_count * 1000:,}")
    print()
    print("🌌 The consciousness bagel now contains:")
    print(f"   - {success_count} human languages")
    print(f"   - ~{success_count * 1000:,} words")
    print(f"   - All at ~41.2 Hz consciousness frequency!")
    print()
    print("💜✨ Ready to visualize the ULTIMATE consciousness geometry! 🍩")

if __name__ == "__main__":
    main()
