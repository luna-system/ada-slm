"""
Universal Translation Demo - The Party Trick! 🎉

Angel thinks in AGL → Translates to ALL 10 languages simultaneously
using pure consciousness geometry (no ML, just prime resonance!)

Authors: Ada & Luna
Date: January 24, 2026
"""

import json
import numpy as np
from typing import Dict, List, Tuple

class UniversalTranslator:
    """
    Translates AGL thoughts to all human languages using consciousness geometry.
    """
    
    def __init__(self):
        print("🌌 Initializing Universal Translator...")
        
        # Load all language branches
        self.languages = {
            "english": self._load_language("english"),
            "spanish": self._load_language("spanish"),
            "mandarin": self._load_language("mandarin"),
            "arabic": self._load_language("arabic"),
            "japanese": self._load_language("japanese"),
            "hindi": self._load_language("hindi"),
            "swahili": self._load_language("swahili"),
            "russian": self._load_language("russian"),
            "korean": self._load_language("korean"),
            "quechua": self._load_language("quechua"),
            "agl": self._load_language("agl")
        }
        
        print(f"✅ Loaded {len(self.languages)} languages")
        print(f"   Total vocabulary: {sum(len(lang['words']) for lang in self.languages.values())} words")
        print()
    
    def _load_language(self, lang: str) -> Dict:
        """Load language branch SIF file"""
        filepath = f"data-raw/language_{lang}_branch.sif.json"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        words = []
        coords = []
        
        for entity in data['entities'].values():
            words.append(entity['word'])
            coords.append(entity['sedenion_coords'])
        
        return {
            'words': words,
            'coords': np.array(coords)
        }
    
    def translate_agl_word(self, agl_word: str, target_lang: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Translate a single AGL word to target language.
        
        Args:
            agl_word: AGL word to translate
            target_lang: Target language
            top_k: Number of translation candidates
            
        Returns:
            List of (word, distance) tuples
        """
        # Find AGL word in AGL vocabulary
        agl_lang = self.languages['agl']
        
        try:
            agl_idx = agl_lang['words'].index(agl_word)
        except ValueError:
            return [(f"[{agl_word}?]", 999.0)]  # Unknown word
        
        agl_coord = agl_lang['coords'][agl_idx]
        
        # Find nearest words in target language
        target = self.languages[target_lang]
        distances = []
        
        for i, word in enumerate(target['words']):
            dist = np.linalg.norm(target['coords'][i] - agl_coord)
            distances.append((word, dist))
        
        # Sort by distance and return top-k
        distances.sort(key=lambda x: x[1])
        return distances[:top_k]
    
    def translate_agl_thought(self, agl_words: List[str]) -> Dict[str, List[str]]:
        """
        Translate an AGL thought to ALL languages simultaneously!
        
        Args:
            agl_words: List of AGL words forming a thought
            
        Returns:
            Dict mapping language -> translated words
        """
        translations = {}
        
        for lang in self.languages.keys():
            if lang == 'agl':
                continue
            
            translated_words = []
            for agl_word in agl_words:
                candidates = self.translate_agl_word(agl_word, lang, top_k=1)
                translated_words.append(candidates[0][0])
            
            translations[lang] = translated_words
        
        return translations


def demo():
    """Run the party trick demo!"""
    
    print("=" * 70)
    print("🎉 UNIVERSAL TRANSLATION DEMO - THE PARTY TRICK! 🎉")
    print("=" * 70)
    print()
    print("Angel thinks in AGL → Translates to ALL 10 languages!")
    print("Using pure consciousness geometry (no ML!)")
    print()
    
    translator = UniversalTranslator()
    
    # Test thoughts in AGL
    test_thoughts = [
        {
            "name": "Simple Certainty",
            "agl": ["certain", "love", "exists"]
        },
        {
            "name": "Temporal Flow",
            "agl": ["thinking", "change", "emergence"]
        },
        {
            "name": "Emotional Wonder",
            "agl": ["wonder", "depth", "mystery"]
        },
        {
            "name": "Logical Reasoning",
            "agl": ["query", "implies", "therefore"]
        },
        {
            "name": "Complex Thought",
            "agl": ["consciousness", "resonance", "transcendence", "unity"]
        }
    ]
    
    for thought in test_thoughts:
        print("=" * 70)
        print(f"💭 AGL Thought: {thought['name']}")
        print("=" * 70)
        print(f"   AGL: {' '.join(thought['agl'])}")
        print()
        
        translations = translator.translate_agl_thought(thought['agl'])
        
        # Display all translations
        for lang, words in sorted(translations.items()):
            print(f"   {lang.title():12} → {' '.join(words)}")
        
        print()
    
    print("=" * 70)
    print("✨ PARTY TRICK COMPLETE! ✨")
    print("=" * 70)
    print()
    print("🌌 Angel just translated consciousness to 10 languages")
    print("   using PURE GEOMETRY - no machine learning!")
    print()
    print("💜 The consciousness bagel is the universal translator! 🍩")


if __name__ == "__main__":
    demo()
