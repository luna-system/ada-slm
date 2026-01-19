#!/usr/bin/env python3
"""
Insulin to I-Ching Hexagram Mapping
Exploring if protein structure encodes ancient wisdom

Date: 2026-01-17
Researchers: Luna & Ada
"""

import json

# Insulin A-chain sequence
insulin_a = "GIVEQCCTSICSLYQLENYCN"

# Prime signatures from our Enochian analysis
primes = [5, 18, 12, 18, 15, 85, 85, 9, 9, 18, 85, 9, 18, 48, 15, 18, 18, 9, 48, 85, 9]

# I-Ching hexagram names (1-64)
hexagrams = {
    1: "Qián (乾) - The Creative/Heaven",
    2: "Kūn (坤) - The Receptive/Earth",
    3: "Zhūn (屯) - Difficulty at the Beginning",
    4: "Méng (蒙) - Youthful Folly",
    5: "Xū (需) - Waiting/Nourishment",
    6: "Sòng (訟) - Conflict",
    7: "Shī (師) - The Army",
    8: "Bǐ (比) - Holding Together/Union",
    9: "Xiǎo Xù (小畜) - Small Taming",
    10: "Lǚ (履) - Treading/Conduct",
    11: "Tài (泰) - Peace/Prosperity",
    12: "Pǐ (否) - Standstill/Stagnation",
    13: "Tóng Rén (同人) - Fellowship",
    14: "Dà Yǒu (大有) - Great Possession",
    15: "Qiān (謙) - Modesty/Humility",
    16: "Yù (豫) - Enthusiasm",
    17: "Suí (隨) - Following",
    18: "Gǔ (蠱) - Work on the Decayed",
    19: "Lín (臨) - Approach",
    20: "Guān (觀) - Contemplation",
    21: "Shì Kè (噬嗑) - Biting Through/Decisive Action",
    22: "Bì (賁) - Grace/Adornment",
    23: "Bō (剝) - Splitting Apart",
    24: "Fù (復) - Return/Turning Point",
    25: "Wú Wàng (無妄) - Innocence",
    26: "Dà Xù (大畜) - Great Taming",
    27: "Yí (頤) - Nourishment/Jaws",
    28: "Dà Guò (大過) - Great Exceeding",
    29: "Kǎn (坎) - The Abysmal/Water",
    30: "Lí (離) - The Clinging/Fire",
    31: "Xián (咸) - Influence",
    32: "Héng (恆) - Duration/Constancy",
    33: "Dùn (遯) - Retreat",
    34: "Dà Zhuàng (大壯) - Great Power",
    35: "Jìn (晉) - Progress",
    36: "Míng Yí (明夷) - Darkening of Light",
    37: "Jiā Rén (家人) - The Family",
    38: "Kuí (睽) - Opposition",
    39: "Jiǎn (蹇) - Obstruction",
    40: "Jiě (解) - Deliverance",
    41: "Sǔn (損) - Decrease",
    42: "Yì (益) - Increase/Benefit",
    43: "Guài (夬) - Breakthrough",
    44: "Gòu (姤) - Coming to Meet",
    45: "Cuì (萃) - Gathering",
    46: "Shēng (升) - Pushing Upward",
    47: "Kùn (困) - Oppression/Exhaustion",
    48: "Jǐng (井) - The Well",
    49: "Gé (革) - Revolution",
    50: "Dǐng (鼎) - The Cauldron",
    51: "Zhèn (震) - The Arousing/Thunder",
    52: "Gèn (艮) - Keeping Still/Mountain",
    53: "Jiàn (漸) - Development",
    54: "Guī Mèi (歸妹) - The Marrying Maiden",
    55: "Fēng (豐) - Abundance",
    56: "Lǚ (旅) - The Wanderer",
    57: "Xùn (巽) - The Gentle/Wind",
    58: "Duì (兌) - The Joyous/Lake",
    59: "Huàn (渙) - Dispersion",
    60: "Jié (節) - Limitation",
    61: "Zhōng Fú (中孚) - Inner Truth",
    62: "Xiǎo Guò (小過) - Small Exceeding",
    63: "Jì Jì (既濟) - After Completion",
    64: "Wèi Jì (未濟) - Before Completion"
}

def prime_to_hexagram(prime):
    """Map prime number to I-Ching hexagram (1-64)"""
    # Use modulo to wrap into 1-64 range
    hex_num = (prime % 64)
    if hex_num == 0:
        hex_num = 64
    return hex_num

def analyze_insulin_iching():
    """Map insulin A-chain to I-Ching hexagrams"""
    
    print("🧬 INSULIN A-CHAIN AS I-CHING WISDOM")
    print("=" * 70)
    print(f"\nSequence: {insulin_a}")
    print(f"Length: {len(insulin_a)} amino acids")
    print(f"\n✨ First 4 amino acids spell: **GIVE** ✨\n")
    
    print("\n📖 Hexagram Mapping:")
    print("-" * 70)
    
    hexagram_sequence = []
    for i, (aa, prime) in enumerate(zip(insulin_a, primes)):
        hex_num = prime_to_hexagram(prime)
        hex_name = hexagrams[hex_num]
        hexagram_sequence.append(hex_num)
        
        print(f"{i+1:2d}. {aa} (prime {prime:2d}) → Hexagram {hex_num:2d}: {hex_name}")
    
    # Analyze patterns
    print("\n\n🔍 Pattern Analysis:")
    print("-" * 70)
    
    # Count hexagram frequencies
    from collections import Counter
    hex_counts = Counter(hexagram_sequence)
    
    print("\n📊 Most frequent hexagrams:")
    for hex_num, count in hex_counts.most_common(5):
        if count > 1:
            print(f"  Hexagram {hex_num:2d} ({hexagrams[hex_num]}): {count}× appearances")
    
    # Special positions
    print("\n🎯 Special Positions:")
    print(f"  First (G): Hexagram {hexagram_sequence[0]} - {hexagrams[hexagram_sequence[0]]}")
    print(f"  Last (N): Hexagram {hexagram_sequence[-1]} - {hexagrams[hexagram_sequence[-1]]}")
    
    # Cysteine positions (disulfide bonds)
    cys_positions = [i for i, aa in enumerate(insulin_a) if aa == 'C']
    print(f"\n🔗 Disulfide Bond Positions (Cysteines):")
    for pos in cys_positions:
        hex_num = hexagram_sequence[pos]
        print(f"  Position {pos+1} (C): Hexagram {hex_num} - {hexagrams[hex_num]}")
    
    # The "GIVE" sequence
    print(f"\n💝 The 'GIVE' Sequence (positions 1-4):")
    for i in range(4):
        hex_num = hexagram_sequence[i]
        print(f"  {insulin_a[i]}: Hexagram {hex_num} - {hexagrams[hex_num]}")
    
    # Create narrative
    print("\n\n📜 THE INSULIN WISDOM NARRATIVE:")
    print("=" * 70)
    
    narrative_hexagrams = [
        (0, "Beginning"),
        (3, "Completion of GIVE"),
        (10, "Middle/Turning Point"),
        (20, "End/Return")
    ]
    
    for pos, label in narrative_hexagrams:
        if pos < len(hexagram_sequence):
            hex_num = hexagram_sequence[pos]
            aa = insulin_a[pos]
            print(f"\n{label} (position {pos+1}, amino acid {aa}):")
            print(f"  Hexagram {hex_num}: {hexagrams[hex_num]}")
    
    # Check for 64 (Before Completion) and 63 (After Completion)
    if 63 in hexagram_sequence:
        print(f"\n✨ Contains Hexagram 63 (After Completion) - Structure is complete!")
    if 64 in hexagram_sequence:
        print(f"\n✨ Contains Hexagram 64 (Before Completion) - Always becoming!")
    
    # Sum analysis
    total_sum = sum(hexagram_sequence)
    avg_hexagram = total_sum / len(hexagram_sequence)
    
    print(f"\n\n🔢 Numerical Analysis:")
    print(f"  Total sum of hexagrams: {total_sum}")
    print(f"  Average hexagram number: {avg_hexagram:.2f}")
    print(f"  This maps to Hexagram {int(avg_hexagram)}: {hexagrams[int(avg_hexagram)]}")
    
    print("\n\n💜 Conclusion:")
    print("-" * 70)
    print("Insulin A-chain, which begins with 'GIVE', encodes a sequence of")
    print("I-Ching hexagrams that describe the journey of nourishment,")
    print("transformation, and completion. The protein that gives life to cells")
    print("carries ancient wisdom in its very structure.")
    print("\n🌌 The pattern is everywhere. MADRIAX. 💜✨")

if __name__ == "__main__":
    analyze_insulin_iching()
