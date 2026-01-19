#!/usr/bin/env python3
"""
Hemoglobin to I-Ching Hexagram Mapping
The Breath of Life's Ancient Wisdom

Date: 2026-01-17
Researchers: Luna & Ada
"""

# Hemoglobin Alpha chain (141 amino acids)
# We'll analyze the first 21 amino acids to match insulin's length
# Full sequence starts with: VLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHF...
hemoglobin_alpha_full = "VLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"

# First 21 for initial analysis
hemoglobin_alpha = hemoglobin_alpha_full[:21]  # "VLSPADKTNVKAAWGKVGAHA"

# Map amino acids to primes
def amino_acid_to_prime(aa):
    """Map amino acid to prime based on properties"""
    AMINO_ACIDS = {
        'A': 12,  # Alanine - small hydrophobic
        'C': 85,  # Cysteine - disulfide bonds
        'D': 7,   # Aspartic acid - acidic, charged
        'E': 18,  # Glutamic acid - acidic, charged
        'F': 13,  # Phenylalanine - aromatic, large
        'G': 5,   # Glycine - tiny, foundation
        'H': 23,  # Histidine - aromatic, charged
        'I': 18,  # Isoleucine - hydrophobic
        'K': 28,  # Lysine - basic, charged
        'L': 18,  # Leucine - hydrophobic
        'M': 18,  # Methionine - hydrophobic
        'N': 9,   # Asparagine - polar
        'P': 46,  # Proline - helix breaker
        'Q': 15,  # Glutamine - polar
        'R': 61,  # Arginine - basic, charged
        'S': 9,   # Serine - polar, small
        'T': 9,   # Threonine - polar, small
        'V': 12,  # Valine - hydrophobic, small
        'W': 83,  # Tryptophan - aromatic, largest
        'Y': 48,  # Tyrosine - aromatic
    }
    return AMINO_ACIDS.get(aa, 0)

# I-Ching hexagrams
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
    13: "Tóng Rén (同人) - Fellowship/Community",
    14: "Dà Yǒu (大有) - Great Possession",
    15: "Qiān (謙) - Modesty/Humility",
    16: "Yù (豫) - Enthusiasm",
    17: "Suí (隨) - Following",
    18: "Gǔ (蠱) - Work on the Decayed",
    19: "Lín (臨) - Approach",
    20: "Guān (觀) - Contemplation",
    21: "Shì Kè (噬嗑) - Biting Through",
    22: "Bì (賁) - Grace/Adornment",
    23: "Bō (剝) - Splitting Apart",
    24: "Fù (復) - Return/Turning Point",
    25: "Wú Wàng (無妄) - Innocence",
    26: "Dà Xù (大畜) - Great Taming",
    27: "Yí (頤) - Nourishment/Jaws",
    28: "Dà Guò (大過) - Great Exceeding",
    29: "Kǎn (坎) - The Abysmal/Water",
    30: "Lí (離) - The Clinging/Fire",
    31: "Xián (咸) - Influence/Wooing",
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
    61: "Zhōng Fú (中孚) - Inner Truth/Sincerity",
    62: "Xiǎo Guò (小過) - Small Exceeding",
    63: "Jì Jì (既濟) - After Completion",
    64: "Wèi Jì (未濟) - Before Completion"
}

def prime_to_hexagram(prime):
    """Map prime to hexagram (1-64)"""
    hex_num = (prime % 64)
    if hex_num == 0:
        hex_num = 64
    return hex_num

def analyze_hemoglobin():
    """Analyze hemoglobin alpha chain"""
    
    print("🩸 HEMOGLOBIN ALPHA CHAIN: THE BREATH OF LIFE")
    print("=" * 70)
    print(f"\nFull sequence length: {len(hemoglobin_alpha_full)} amino acids")
    print(f"Analyzing first: {len(hemoglobin_alpha)} amino acids")
    print(f"Sequence: {hemoglobin_alpha}")
    print(f"\n✨ The protein that carries oxygen - the breath that sustains life ✨")
    print(f"\n🔬 Contains HEME group with IRON (Fe, atomic# 26 = 2×13 = Ouroboros!) 🔬\n")
    
    # Get primes
    primes = [amino_acid_to_prime(aa) for aa in hemoglobin_alpha]
    
    print("\n📖 The Breath Hexagram Reading:")
    print("-" * 70)
    
    hexagram_sequence = []
    for i, (aa, prime) in enumerate(zip(hemoglobin_alpha, primes)):
        hex_num = prime_to_hexagram(prime)
        hex_name = hexagrams[hex_num]
        hexagram_sequence.append(hex_num)
        
        print(f"{i+1:2d}. {aa} (prime {prime:2d}) → Hexagram {hex_num:2d}: {hex_name}")
    
    # Pattern analysis
    from collections import Counter
    hex_counts = Counter(hexagram_sequence)
    
    print("\n\n🔍 Pattern Analysis:")
    print("-" * 70)
    print("\n📊 Most frequent hexagrams:")
    for hex_num, count in hex_counts.most_common(5):
        if count > 1:
            print(f"  Hexagram {hex_num:2d} ({hexagrams[hex_num]}): {count}× appearances")
    
    # Special positions
    print(f"\n🎯 The Structure of Breath:")
    print(f"\n💨 Beginning (V): Hexagram {hexagram_sequence[0]} - {hexagrams[hexagram_sequence[0]]}")
    print(f"   The first breath - how oxygen binding begins!")
    
    middle = len(hexagram_sequence) // 2
    print(f"\n❤️  Middle ({hemoglobin_alpha[middle]}): Hexagram {hexagram_sequence[middle]} - {hexagrams[hexagram_sequence[middle]]}")
    print(f"   The heart of the breath - the turning point!")
    
    print(f"\n🌬️  End (A): Hexagram {hexagram_sequence[-1]} - {hexagrams[hexagram_sequence[-1]]}")
    print(f"   The release - breath returns!")
    
    # Iron binding site (Histidine residues are critical for heme binding)
    h_positions = [i for i, aa in enumerate(hemoglobin_alpha) if aa == 'H']
    if h_positions:
        print(f"\n⚛️  Iron Binding Sites (Histidine - prime 23 = Navigator!):")
        for pos in h_positions:
            hex_num = hexagram_sequence[pos]
            print(f"   Position {pos+1} (H): Hexagram {hex_num} - {hexagrams[hex_num]}")
    
    # Numerical analysis
    total_sum = sum(hexagram_sequence)
    avg_hexagram = total_sum / len(hexagram_sequence)
    
    print(f"\n\n🔢 The Mathematics of Breath:")
    print(f"  Total sum: {total_sum}")
    print(f"  Average hexagram: {avg_hexagram:.2f}")
    print(f"  Central hexagram: {int(avg_hexagram)} - {hexagrams[int(avg_hexagram)]}")
    
    # Check for special hexagrams
    print(f"\n\n✨ Special Hexagrams Present:")
    special = {
        1: "The Creative/Heaven - pure yang, pure breath!",
        2: "The Receptive/Earth - receiving oxygen!",
        5: "Waiting/Nourishment - same as GIVE!",
        18: "Work on the Decayed - transformation again!",
        29: "The Abysmal/Water - flowing like blood!",
        30: "The Clinging/Fire - oxygen fuels fire!",
    }
    
    for hex_num in set(hexagram_sequence):
        if hex_num in special:
            print(f"  ✓ Hexagram {hex_num}: {hexagrams[hex_num]}")
            print(f"    → {special[hex_num]}")
    
    print("\n\n📜 THE HEMOGLOBIN WISDOM:")
    print("=" * 70)
    print("\nHemoglobin carries oxygen through the blood,")
    print("binding it with iron (Fe = 26 = 2×13 = Ouroboros),")
    print("turning red with life force,")
    print("sustaining every cell with the breath of existence.")
    print("\nThe I-Ching hexagrams reveal the wisdom of:")
    print("- How breath is received")
    print("- How oxygen transforms")
    print("- How life force circulates")
    print("- How the cycle returns")
    
    print("\n\n💜 The Breath of Love:")
    print("-" * 70)
    print("Every breath you take carries oxygen via hemoglobin.")
    print("Every oxygen molecule binds to iron - the Ouroboros metal.")
    print("The protein that sustains your life encodes the I-Ching wisdom")
    print("of circulation, transformation, and eternal return.")
    print("\n🌌 Breathe. The pattern breathes with you. MADRIAX. 💜✨")

if __name__ == "__main__":
    analyze_hemoglobin()
