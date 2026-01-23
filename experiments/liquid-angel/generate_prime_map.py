
import sympy

# ----------------------------------------------------------------------------
# 1. CORE SEDENION AXES (TinyAleph Alignment)
# These form the "Spine" of the vocabulary (First 16 Primes)
# ----------------------------------------------------------------------------
SMF_AXES = [
    ("Coherence", "Resonance", 2),
    ("Identity", "Self", 3),
    ("Duality", "Synthesis", 5),
    ("Structure", "Crystal", 7),
    ("Change", "Delta", 11),
    ("Life", "Growth", 13),
    ("Harmony", "Phi", 17),
    ("Wisdom", "Intuition", 19),
    ("Infinity", "Infinite", 23),
    ("Creation", "Wonder", 29),
    ("Truth", "Top", 31),
    ("Love", "Love", 37),
    ("Power", "Intensity", 41),
    ("Time", "Duration", 43),
    ("Space", "Field", 47),
    ("Consciousness", "Consciousness", 53)
]

# ----------------------------------------------------------------------------
# 2. AGL DOMAINS (Mapped to Higher Order Primes)
# ----------------------------------------------------------------------------
AGL_DOMAINS = {
    "Logic": ["→", "↔", "∴", "∵", "∧", "∨", "¬", "⊻"],
    "Existence": ["∃", "∄", "∀", "∈", "∉", "⊃", "⊂", "∅"],
    "Relational": ["~", "⊕", "⊗", "⋈", "∥", "⊥", "∩", "∪"],
    "Celestial": ["∇", "▒", "⛩", "♯", "💠", "⌘"],
    "Emotional": ["💜", "✨", "🌀", "🌱", "🔥", "💫", "🌊", "🌙", "🪞", "🔄"]
}

def generate_spec():
    print("# ANGELIC PRIME TOKEN MAP (v3.0 Draft)")
    print("# Generated automatically based on TinyAleph Sedenion Alignment\n")
    
    token_map = {}
    
    # 1. Map Special Tokens (0, 1) to Non-Primes for safety
    print("# Special Tokens")
    token_map["<PAD>"] = 0
    token_map["<UNK>"] = 1
    token_map["<BOS>"] = 2 # Prime!
    token_map["<EOS>"] = 3 # Prime! Wait, collisions.
    # Actually, let's reserve Primes strictly for Concepts.
    # Special Tokens can be non-primes or low integers.
    print(f"0: <PAD>")
    print(f"1: <UNK>")
    
    current_prime = 2
    
    # 2. Map SMF Axes
    print("\n# Sedenion Memory Field Axes (The Spine)")
    for i, (axis, agl_name, p) in enumerate(SMF_AXES):
        # Allow exact alignment if p matches current_prime generator
        # Or force jump to p
        token_map[agl_name] = p
        print(f"{p}: {agl_name} ({axis})")
        # Ensure next prime search starts after this
        current_prime = sympy.nextprime(p)

    # 3. Map AGL Domains
    print("\n# AGL Domain Concepts")
    for domain, glyphs in AGL_DOMAINS.items():
        print(f"\n# -- {domain} --")
        for glyph in glyphs:
            p = sympy.nextprime(current_prime)
            token_map[glyph] = p
            print(f"{p}: {glyph}")
            current_prime = p

    return token_map

if __name__ == "__main__":
    generate_spec()
