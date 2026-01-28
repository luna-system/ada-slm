"""
Create RAW versions of all hydration scripts

Converts all hydrate_*_branch.py scripts to use RawLanguageSIFGenerator
and output to data-raw/ folder.

Authors: Ada & Luna
Date: January 23, 2026
"""

import re
from pathlib import Path

# List of all language hydration scripts
LANGUAGES = [
    "english", "spanish", "mandarin", "arabic", "japanese",
    "hindi", "swahili", "russian", "korean", "quechua"
]

def convert_script(language: str):
    """Convert a hydration script to RAW version"""
    
    input_file = f"hydrate_{language}_branch.py"
    output_file = f"hydrate_{language}_branch_raw.py"
    
    print(f"Converting {input_file} → {output_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace imports
    content = content.replace(
        "from generate_language_sif import UniversalLanguageSIFGenerator",
        "from generate_language_sif_raw import RawLanguageSIFGenerator"
    )
    
    # Replace class name
    content = content.replace(
        "UniversalLanguageSIFGenerator()",
        "RawLanguageSIFGenerator()"
    )
    
    # Replace output path
    content = content.replace(
        'output_path = "data/language_',
        'output_path = "data-raw/language_'
    )
    
    # Update title comment
    content = content.replace(
        f"Hydrate {language.title()} Language Branch",
        f"Hydrate {language.title()} Language Branch (RAW - No Hashing)"
    )
    
    # Add experiment note
    if "🔬 EXPERIMENT:" not in content:
        content = content.replace(
            'print(f"\\n✅',
            'print(f"\\n🔬 EXPERIMENT: RAW character values (no hashing)")\n    print(f"\\n✅'
        )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Created {output_file}")

def main():
    print("🔬 Creating RAW hydration scripts for all languages")
    print("=" * 60)
    
    for language in LANGUAGES:
        convert_script(language)
    
    print(f"\n✅ Created {len(LANGUAGES)} RAW hydration scripts!")
    print(f"📁 Output will go to: data-raw/")

if __name__ == "__main__":
    main()
