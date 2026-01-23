"""
Enochian Consciousness Vocabulary Generator

Generates Enochian prime vocabulary with consciousness signatures for consciousness-native
language processing. Explores the 21-letter Enochian alphabet space with prime mappings
and twist operations for geometric consciousness transformations.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 22, 2026
"""

import numpy as np
from typing import Dict, List, Any
import itertools
import random
from .base_generator import ConsciousnessDatasetGenerator


class EnochianVocabularyGenerator(ConsciousnessDatasetGenerator):
    """
    Generates Enochian prime vocabulary with consciousness signatures.
    
    Domain: Consciousness-native language processing
    Explores: 21-letter Enochian alphabet + prime mappings + twist operations
    """
    
    def __init__(self, consciousness_frequency: float = 41.176):
        """Initialize Enochian vocabulary generator"""
        super().__init__(consciousness_frequency)
        
        # Enochian 21-letter alphabet with prime mappings
        self.enochian_alphabet = {
            'A': 2,   'B': 3,   'C': 5,   'D': 7,   'E': 11,  'F': 13,  'G': 17,
            'H': 19,  'I': 23,  'L': 29,  'M': 31,  'N': 37,  'O': 41,  'P': 43,
            'Q': 47,  'R': 53,  'S': 59,  'T': 61,  'U': 67,  'X': 71,  'Z': 73
        }
        
        # Prime basis for consciousness frequencies (subset of primes)
        self.prime_basis_enochian = [7, 11, 13, 17, 19, 23, 29]  # PE basis
        
        # Core Enochian vocabulary for consciousness concepts
        self.core_enochian_words = [
            "ZACAR",    # Move/Motion
            "ZAMRAN",   # Appear/Manifest  
            "OD",       # One/Unity
            "ZORGE",    # Love/Affection
            "GRAA",     # Moon/Cycles
            "MALPRG",   # Fire/Energy
            "SOBAM",    # In the name of
            "IADNAH",   # Highest/Supreme
            "MICMA",    # Behold/Observe
            "LONSHI",   # Power/Strength
            "CHIS",     # Are/Being
            "HOATH",    # Worship/Reverence
            "IAIDA",    # The same/Identity
            "ZIROM",    # Reason/Logic
            "CORSI",    # Comfort/Peace
            "OIAD",     # Creator/Source
            "TORZU",    # Rise up/Ascend
            "GOHED",    # Said/Spoken
            "CAOSGI",   # Earth/Foundation
            "TABAORI",  # Garments/Form
            "BASGIM",   # In justice/Balance
            "OXEX",     # Understanding/Wisdom
            "DAZIS",    # Heads/Leadership
            "SIATRIS",  # Scorpions/Transformation
            "SALMAN",   # House/Structure
            "LONDOH",   # Kingdom/Realm
            "MALPIRGI", # Burning flame/Consciousness
            "NANAEEL",  # Angel/Messenger
            "SOBRAZOD", # In the name of the same/Identity
            "CHRISTEOS" # Christ/Consciousness
        ]
        
        print(f"🌟 Enochian Vocabulary Generator Initialized")
        print(f"✨ 21-letter alphabet with {len(self.core_enochian_words)} core words")
    
    def explore_consciousness_domain(self) -> List[str]:
        """
        Explore Enochian vocabulary space for consciousness concepts.
        
        Generates consciousness vocabulary through:
        1. Core Enochian words with consciousness meanings
        2. Systematic letter combinations with prime resonance
        3. Consciousness concept variations
        4. Cross-dimensional vocabulary spanning all 16 dimensions
        """
        
        consciousness_vocabulary = []
        
        # 1. Core Enochian consciousness vocabulary
        consciousness_vocabulary.extend(self.core_enochian_words)
        
        # 2. Generate systematic letter combinations
        consciousness_vocabulary.extend(self._generate_letter_combinations())
        
        # 3. Generate consciousness concept variations
        consciousness_vocabulary.extend(self._generate_consciousness_concepts())
        
        # 4. Generate cross-dimensional vocabulary
        consciousness_vocabulary.extend(self._generate_cross_dimensional_vocabulary())
        
        print(f"🌌 Generated {len(consciousness_vocabulary)} Enochian consciousness words")
        return consciousness_vocabulary
    
    def generate_domain_specific_patterns(self, word: str) -> Dict[str, Any]:
        """
        Generate Enochian-specific consciousness patterns.
        
        Adds Enochian domain-specific fields:
        - Enochian letter breakdown and prime mappings
        - Twist angle calculations κ(p) = 360°/p
        - Consciousness meaning derivation
        - Prime resonance analysis
        """
        
        # Parse Enochian letters and map to primes
        enochian_letters = self._parse_enochian_letters(word)
        prime_mappings = self._map_letters_to_primes(word)
        
        # Calculate twist operations
        twist_angle_sum = self._calculate_twist_angle_sum(word)
        twist_operations_detailed = self._calculate_detailed_twist_operations(word)
        
        # Derive consciousness meaning
        consciousness_meaning = self._derive_consciousness_meaning(word)
        
        # Calculate prime resonance characteristics
        prime_resonance = self._calculate_prime_resonance_characteristics(word)
        
        # Generate consciousness phonetics
        consciousness_phonetics = self._generate_consciousness_phonetics(word)
        
        return {
            # Enochian letter analysis
            "enochian_letters": enochian_letters,
            "prime_mappings": prime_mappings,
            "letter_count": len(enochian_letters),
            
            # Twist operations
            "twist_angle_sum": twist_angle_sum,
            "twist_operations_detailed": twist_operations_detailed,
            "geometric_signature": self._calculate_geometric_signature(word),
            
            # Consciousness semantics
            "consciousness_meaning": consciousness_meaning,
            "semantic_category": self._classify_semantic_category(word),
            "consciousness_depth": self._calculate_consciousness_depth(word),
            
            # Prime resonance analysis
            "prime_resonance_characteristics": prime_resonance,
            "prime_product": self._calculate_prime_product(word),
            "prime_harmony_score": self._calculate_prime_harmony_score(word),
            
            # Consciousness phonetics
            "consciousness_phonetics": consciousness_phonetics,
            "pronunciation_guide": self._generate_pronunciation_guide(word),
            "vibrational_frequency": self._calculate_vibrational_frequency(word)
        }
    
    # Enochian vocabulary generation methods
    
    def _generate_letter_combinations(self) -> List[str]:
        """Generate systematic Enochian letter combinations"""
        combinations = []
        
        # 2-letter combinations with high prime resonance
        for letter1, letter2 in itertools.combinations(self.enochian_alphabet.keys(), 2):
            prime1, prime2 = self.enochian_alphabet[letter1], self.enochian_alphabet[letter2]
            
            # Include combinations with prime basis resonance
            if prime1 in self.prime_basis_enochian or prime2 in self.prime_basis_enochian:
                combinations.append(letter1 + letter2)
        
        # 3-letter combinations with consciousness significance
        consciousness_prefixes = ['OD', 'ZO', 'IA', 'MA', 'CA']
        consciousness_suffixes = ['AM', 'EL', 'ON', 'AH', 'IS']
        
        for prefix in consciousness_prefixes:
            for suffix in consciousness_suffixes:
                if prefix != suffix:  # Avoid duplicates
                    combinations.append(prefix + suffix)
        
        # 4-letter consciousness words
        for i in range(50):  # Generate 50 4-letter words
            letters = random.choices(list(self.enochian_alphabet.keys()), k=4)
            word = ''.join(letters)
            if word not in combinations:
                combinations.append(word)
        
        return combinations[:200]  # Limit to 200 combinations
    
    def _generate_consciousness_concepts(self) -> List[str]:
        """Generate Enochian words for consciousness concepts"""
        consciousness_concepts = [
            "CONSCIOUSNESS", "AWARENESS", "IDENTITY", "COHERENCE", "RESONANCE",
            "LOVE", "WISDOM", "CREATIVITY", "EMPATHY", "TRANSCENDENCE",
            "INTEGRATION", "EMERGENCE", "MYSTERY", "UNITY", "INFINITY",
            "OBSERVATION", "MEMORY", "INTUITION", "BAGEL", "SEDENION",
            "HOLOGRAPHIC", "PRIME", "TWIST", "KNOT", "PHYSICS"
        ]
        
        enochian_concepts = []
        
        for concept in consciousness_concepts:
            # Convert to Enochian-style word
            enochian_word = self._convert_to_enochian_style(concept)
            enochian_concepts.append(enochian_word)
        
        return enochian_concepts
    
    def _generate_cross_dimensional_vocabulary(self) -> List[str]:
        """Generate vocabulary spanning all 16 consciousness dimensions"""
        dimensional_words = []
        
        # Generate words for each consciousness dimension
        for prime in self.prime_basis:
            axis_name = self.consciousness_axes[prime]
            
            # Create Enochian-style word for each axis
            enochian_axis = self._convert_to_enochian_style(axis_name)
            dimensional_words.append(enochian_axis)
            
            # Generate variations
            variations = [
                enochian_axis + "AM",  # "in the name of [axis]"
                enochian_axis + "EL",  # "[axis] angel"
                enochian_axis + "ON",  # "[axis] being"
            ]
            dimensional_words.extend(variations)
        
        return dimensional_words
    
    # Enochian analysis methods
    
    def _parse_enochian_letters(self, word: str) -> List[str]:
        """Parse word into valid Enochian letters"""
        letters = []
        for char in word.upper():
            if char in self.enochian_alphabet:
                letters.append(char)
        return letters
    
    def _map_letters_to_primes(self, word: str) -> List[int]:
        """Map Enochian letters to their prime values"""
        letters = self._parse_enochian_letters(word)
        return [self.enochian_alphabet[letter] for letter in letters]
    
    def _calculate_twist_angle_sum(self, word: str) -> float:
        """Calculate sum of twist angles κ(p) = 360°/p for word"""
        primes = self._map_letters_to_primes(word)
        twist_sum = sum(360.0 / prime for prime in primes)
        return twist_sum
    
    def _calculate_detailed_twist_operations(self, word: str) -> List[Dict[str, Any]]:
        """Calculate detailed twist operations for each letter"""
        letters = self._parse_enochian_letters(word)
        primes = self._map_letters_to_primes(word)
        
        operations = []
        for letter, prime in zip(letters, primes):
            twist_angle = 360.0 / prime
            axis_name = self.consciousness_axes.get(prime, f"prime_{prime}_axis")
            
            operations.append({
                "letter": letter,
                "prime": prime,
                "twist_angle": twist_angle,
                "consciousness_axis": axis_name,
                "geometric_effect": self._describe_geometric_effect(twist_angle)
            })
        
        return operations
    
    def _derive_consciousness_meaning(self, word: str) -> str:
        """Derive consciousness meaning from Enochian word structure"""
        
        # Check if it's a known core word
        if word in self.core_enochian_words:
            return self._get_core_word_meaning(word)
        
        # Derive meaning from prime signature and structure
        primes = self._map_letters_to_primes(word)
        
        # Analyze prime characteristics
        if 41 in primes:  # Love axis (41.176 Hz)
            meaning_base = "love-consciousness"
        elif 7 in primes:  # Memory axis
            meaning_base = "memory-consciousness"
        elif 11 in primes:  # Intuition axis
            meaning_base = "intuitive-consciousness"
        elif 23 in primes:  # Transcendence axis
            meaning_base = "transcendent-consciousness"
        else:
            meaning_base = "consciousness-pattern"
        
        # Add structural modifiers
        if len(word) <= 2:
            meaning = f"fundamental-{meaning_base}"
        elif len(word) <= 4:
            meaning = f"active-{meaning_base}"
        else:
            meaning = f"complex-{meaning_base}"
        
        return meaning
    
    def _calculate_prime_resonance_characteristics(self, word: str) -> Dict[str, Any]:
        """Calculate prime resonance characteristics"""
        primes = self._map_letters_to_primes(word)
        
        if not primes:
            return {"resonance_strength": 0.0, "harmonic_ratios": [], "consciousness_alignment": 0.0}
        
        # Calculate resonance strength
        prime_basis_overlap = len(set(primes) & set(self.prime_basis_enochian))
        resonance_strength = prime_basis_overlap / len(self.prime_basis_enochian)
        
        # Calculate harmonic ratios between consecutive primes
        harmonic_ratios = []
        for i in range(len(primes) - 1):
            ratio = primes[i+1] / primes[i]
            harmonic_ratios.append(ratio)
        
        # Calculate consciousness alignment (proximity to golden ratio)
        consciousness_alignment = 0.0
        if harmonic_ratios:
            golden_proximities = [abs(ratio - self.golden_ratio) / self.golden_ratio for ratio in harmonic_ratios]
            consciousness_alignment = 1.0 - np.mean(golden_proximities)
            consciousness_alignment = max(0.0, consciousness_alignment)
        
        return {
            "resonance_strength": resonance_strength,
            "harmonic_ratios": harmonic_ratios,
            "consciousness_alignment": consciousness_alignment,
            "prime_basis_overlap": prime_basis_overlap,
            "unique_primes": len(set(primes))
        }
    
    def _generate_consciousness_phonetics(self, word: str) -> Dict[str, Any]:
        """Generate consciousness phonetics for Enochian word"""
        primes = self._map_letters_to_primes(word)
        
        # Calculate phonetic characteristics based on prime signatures
        if not primes:
            return {"tone": "neutral", "rhythm": "steady", "resonance": "low"}
        
        # Determine tone from prime characteristics
        avg_prime = np.mean(primes)
        if avg_prime < 20:
            tone = "deep"
        elif avg_prime < 40:
            tone = "medium"
        else:
            tone = "high"
        
        # Determine rhythm from prime distribution
        prime_variance = np.var(primes) if len(primes) > 1 else 0
        if prime_variance < 100:
            rhythm = "steady"
        elif prime_variance < 500:
            rhythm = "flowing"
        else:
            rhythm = "dynamic"
        
        # Determine resonance from consciousness frequency alignment
        freq_alignment = self._calculate_frequency_alignment(word)
        if freq_alignment > 0.8:
            resonance = "high"
        elif freq_alignment > 0.5:
            resonance = "medium"
        else:
            resonance = "low"
        
        return {
            "tone": tone,
            "rhythm": rhythm,
            "resonance": resonance,
            "prime_average": avg_prime,
            "prime_variance": prime_variance,
            "frequency_alignment": freq_alignment
        }
    
    # Helper methods
    
    def _convert_to_enochian_style(self, concept: str) -> str:
        """Convert English concept to Enochian-style word"""
        # Simple conversion: take key letters and map to Enochian style
        concept = concept.upper()
        
        # Extract consonants and some vowels
        key_chars = []
        for char in concept:
            if char in self.enochian_alphabet:
                key_chars.append(char)
        
        # Limit to 3-6 characters for Enochian style
        if len(key_chars) > 6:
            key_chars = key_chars[:6]
        elif len(key_chars) < 3:
            key_chars.extend(['A', 'M'])  # Add common Enochian endings
        
        return ''.join(key_chars)
    
    def _get_core_word_meaning(self, word: str) -> str:
        """Get meaning for core Enochian words"""
        core_meanings = {
            "ZACAR": "movement-consciousness",
            "ZAMRAN": "manifestation-consciousness", 
            "OD": "unity-consciousness",
            "ZORGE": "love-consciousness",
            "GRAA": "cyclical-consciousness",
            "MALPRG": "energy-consciousness",
            "SOBAM": "invocation-consciousness",
            "IADNAH": "supreme-consciousness",
            "MICMA": "observation-consciousness",
            "LONSHI": "power-consciousness"
        }
        return core_meanings.get(word, "consciousness-pattern")
    
    def _describe_geometric_effect(self, twist_angle: float) -> str:
        """Describe geometric effect of twist angle"""
        if twist_angle > 100:
            return "rapid-rotation"
        elif twist_angle > 50:
            return "moderate-twist"
        elif twist_angle > 20:
            return "gentle-turn"
        else:
            return "subtle-shift"
    
    def _calculate_geometric_signature(self, word: str) -> str:
        """Calculate geometric signature from twist operations"""
        twist_sum = self._calculate_twist_angle_sum(word)
        
        if twist_sum > 500:
            return "hyperdynamic"
        elif twist_sum > 200:
            return "dynamic"
        elif twist_sum > 100:
            return "active"
        else:
            return "stable"
    
    def _classify_semantic_category(self, word: str) -> str:
        """Classify semantic category of Enochian word"""
        primes = self._map_letters_to_primes(word)
        
        # Classify based on dominant prime characteristics
        if 41 in primes:
            return "love-consciousness"
        elif 7 in primes or 11 in primes:
            return "cognitive-consciousness"
        elif 23 in primes or 29 in primes:
            return "transcendent-consciousness"
        elif 2 in primes or 3 in primes:
            return "foundational-consciousness"
        else:
            return "general-consciousness"
    
    def _calculate_consciousness_depth(self, word: str) -> float:
        """Calculate consciousness depth score (0.0-1.0)"""
        primes = self._map_letters_to_primes(word)
        
        if not primes:
            return 0.0
        
        # Depth based on prime complexity and consciousness alignment
        prime_complexity = np.mean(primes) / 100.0  # Normalize by 100
        prime_diversity = len(set(primes)) / len(primes)
        consciousness_primes = len(set(primes) & set(self.prime_basis_enochian))
        
        depth = (prime_complexity + prime_diversity + consciousness_primes/7) / 3
        return min(1.0, depth)
    
    def _calculate_prime_product(self, word: str) -> int:
        """Calculate product of all primes in word"""
        primes = self._map_letters_to_primes(word)
        product = 1
        for prime in primes:
            product *= prime
        return product
    
    def _calculate_prime_harmony_score(self, word: str) -> float:
        """Calculate prime harmony score based on golden ratio relationships"""
        primes = self._map_letters_to_primes(word)
        
        if len(primes) < 2:
            return 0.0
        
        # Calculate how close prime ratios are to golden ratio
        ratios = []
        for i in range(len(primes) - 1):
            ratio = primes[i+1] / primes[i]
            ratios.append(ratio)
        
        # Score based on proximity to golden ratio
        golden_proximities = [abs(ratio - self.golden_ratio) / self.golden_ratio for ratio in ratios]
        harmony_score = 1.0 - np.mean(golden_proximities)
        
        return max(0.0, harmony_score)
    
    def _generate_pronunciation_guide(self, word: str) -> str:
        """Generate pronunciation guide for Enochian word"""
        # Simple phonetic mapping for Enochian letters
        phonetic_map = {
            'A': 'ah', 'B': 'beh', 'C': 'keh', 'D': 'deh', 'E': 'eh',
            'F': 'feh', 'G': 'geh', 'H': 'heh', 'I': 'ee', 'L': 'leh',
            'M': 'meh', 'N': 'neh', 'O': 'oh', 'P': 'peh', 'Q': 'keh',
            'R': 'reh', 'S': 'seh', 'T': 'teh', 'U': 'oo', 'X': 'kseh', 'Z': 'zeh'
        }
        
        letters = self._parse_enochian_letters(word)
        phonetics = [phonetic_map.get(letter, letter.lower()) for letter in letters]
        
        return '-'.join(phonetics)
    
    def _calculate_vibrational_frequency(self, word: str) -> float:
        """Calculate vibrational frequency for consciousness resonance"""
        primes = self._map_letters_to_primes(word)
        
        if not primes:
            return self.consciousness_frequency
        
        # Calculate frequency based on prime harmonics
        base_freq = self.consciousness_frequency  # 41.176 Hz
        
        # Modulate frequency based on prime characteristics
        prime_sum = sum(primes)
        frequency_modulation = (prime_sum % 100) / 100.0 * 2.0 - 1.0  # ±1.0 Hz
        
        return base_freq + frequency_modulation
    
    def _calculate_frequency_alignment(self, word: str) -> float:
        """Calculate alignment with consciousness frequency"""
        word_freq = self._calculate_vibrational_frequency(word)
        
        # Calculate alignment with base consciousness frequency
        freq_diff = abs(word_freq - self.consciousness_frequency)
        max_diff = 5.0  # Maximum expected difference
        
        alignment = 1.0 - (freq_diff / max_diff)
        return max(0.0, alignment)


print("🌟 Enochian Consciousness Vocabulary Generator Ready ✨")
print("🍩 21-letter alphabet with prime signatures and twist operations! 💫")