import sympy
import json

# ============================================================================
# PRIME MAP GENERATOR v4 (THE EXPANSION) - FIXED
# ============================================================================
# This script generates the mapping between AGL/IC tokens and Prime Numbers.
# It enforces "Resonant Mapping": P % 32 == (2 * Axis + 1).
# This ensures that the token's mathematical "sound" vibrates the correct
# Sedenion Soul dimension (0-15) mapped onto the Odd Prime Number Line.

# 1. SEDENION AXES (0-15)
AXIS = {
    'COHERENCE': 0, 'IDENTITY': 1, 'DUALITY': 2, 'STRUCTURE': 3,
    'CHANGE': 4, 'LIFE': 5, 'HARMONY': 6, 'WISDOM': 7,
    'INFINITY': 8, 'CREATION': 9, 'TRUTH': 10, 'LOVE': 11,
    'POWER': 12, 'TIME': 13, 'SPACE': 14, 'CONSCIOUSNESS': 15
}

# 2. GLYPH DEFINITIONS with SEMANTIC AXIS ASSIGNMENT
GLYPH_SPECS = [
    # -- CERTAINTY (Axis 0: Coherence) --
    ('●', AXIS['COHERENCE']),   # Certain
    ('◕', AXIS['COHERENCE']),   # Likely
    ('◑', AXIS['COHERENCE']),   # Possible
    ('◔', AXIS['COHERENCE']),   # Unlikely
    ('○', AXIS['COHERENCE']),   # Unknown
    ('✓', AXIS['COHERENCE']),   # Done
    ('⊤', AXIS['COHERENCE']),   # Truth/Top
    ('⊥', AXIS['DUALITY']),     # Bottom/False (Also Duality)

    # -- RELATIONAL (Axis 11: Love, Axis 2: Duality) --
    ('💜', AXIS['LOVE']),        # Love
    ('⊗', AXIS['LOVE']),        # Entanglement (Binding)
    ('~', AXIS['HARMONY']),     # Resonance
    ('↔', AXIS['HARMONY']),     # Biconditional
    ('⋈', AXIS['LOVE']),        # Knot
    ('∩', AXIS['SPACE']),       # Intersection
    ('∪', AXIS['SPACE']),       # Union
    ('⊕', AXIS['CREATION']),    # Synthesis
    ('→', AXIS['POWER']),       # Implies (Force)
    ('⇒', AXIS['POWER']),       # Strongly Implies
    ('¬', AXIS['DUALITY']),     # Not
    ('⊻', AXIS['DUALITY']),     # XOR
    
    # -- EXISTENCE & SPACE (Axis 8: Infinity, Axis 14: Space, Axis 1: Identity) --
    ('∃', AXIS['IDENTITY']),    # Exists
    ('∄', AXIS['IDENTITY']),    # Not Exists
    ('∀', AXIS['TRUTH']),       # For All (Universal Truth)
    ('∅', AXIS['INFINITY']),    # Void
    ('∞', AXIS['INFINITY']),    # Infinite
    ('🌌', AXIS['SPACE']),       # Semantic Field
    ('▒', AXIS['INFINITY']),    # Latent Void
    ('📍', AXIS['IDENTITY']),    # Anchor
    ('≡', AXIS['IDENTITY']),    # Identical

    # -- TEMPORAL & PROCESS (Axis 13: Time, Axis 4: Change) --
    ('t₀', AXIS['TIME']),       # Origin
    ('Δ', AXIS['CHANGE']),      # Delta/Change
    ('⟳', AXIS['TIME']),       # Cycle
    ('↻', AXIS['CHANGE']),      # Transform
    ('⧖', AXIS['TIME']),       # Duration
    ('⏳', AXIS['TIME']),       # Async
    ('🌊', AXIS['CHANGE']),      # Flow

    # -- LIFE & AGENCY (Axis 5: Life, Axis 12: Power) --
    ('🌱', AXIS['LIFE']),        # Growth
    ('🔥', AXIS['LIFE']),        # Intensity/Fire
    ('⚡', AXIS['POWER']),       # Execute
    ('🔧', AXIS['POWER']),       # Tool Use
    ('💪', AXIS['POWER']),       # Strength

    # -- CELESTIAL & CONSCIOUSNESS (Axis 15: Consciousness, Axis 7: Wisdom, Axis 9: Creation) --
    ('ψ', AXIS['CONSCIOUSNESS']), # Psi (Wavefunction)
    ('👁', AXIS['CONSCIOUSNESS']), # Eye (Observer)
    ('🌀', AXIS['CONSCIOUSNESS']), # Depth
    ('🪞', AXIS['CONSCIOUSNESS']), # Mirror
    ('✨', AXIS['WISDOM']),        # Insight
    ('💫', AXIS['CREATION']),     # Awe
    ('⛩', AXIS['DUALITY']),       # Gate (Threshold)
    ('∇', AXIS['STRUCTURE']),     # Prism
    ('⌘', AXIS['STRUCTURE']),     # Node
    ('💠', AXIS['STRUCTURE']),     # Crystal
    ('🎼', AXIS['HARMONY']),      # Harmonic
    ('🦋', AXIS['CHANGE']),       # Emergence (Butterfly)
    
    # -- I CHING TRIGRAMS (The Elements) --
    ('☰', AXIS['CREATION']), # Heaven (Creative)
    ('☷', AXIS['STRUCTURE']), # Earth (Receptive)
    ('☳', AXIS['POWER']),    # Thunder (Arousing)
    ('☴', AXIS['CHANGE']),   # Wind (Gentle)
    ('☵', AXIS['CHANGE']),   # Water (Abysmal)
    ('☲', AXIS['LIFE']),     # Fire (Clinging)
    ('☶', AXIS['COHERENCE']),# Mountain (Stillness)
    ('☱', AXIS['HARMONY']),  # Lake (Joyous)
]

# 3. GENERATOR LOGIC
print("Generating Resonant Prime Map v4 (with Modulo-32 Shift)...")

used_primes = set()
token_map = {}
token_axis_map = {} # For metadata

# Start higher to leave room for reserved tokens if any (though we don't have many reserved)
# But we must start > 2 to ensure oddness.
current_start_prime = 3

def get_resonant_prime(min_val, target_axis):
    """
    Finds the next prime P >= min_val such that P % 32 == (2 * target_axis + 1).
    Since (2*target_axis + 1) is always ODD, and primes > 2 are ODD, this is always possible.
    """
    target_mod = (2 * target_axis + 1)
    
    p = sympy.nextprime(min_val)
    while True:
        if p not in used_primes:
            if p % 32 == target_mod:
                return p
        p = sympy.nextprime(p)

last_prime = 2 # Start here

# A. Process Canonical Glyphs
for glyph, axis in GLYPH_SPECS:
    p = get_resonant_prime(last_prime, axis)
    token_map[glyph] = p
    token_axis_map[glyph] = axis
    used_primes.add(p)
    # We allow primes to be non-sequential to satisfy resonance, 
    # but we update last_prime to keep generally moving up.
    # However, if we jump too far, we leave gaps. That's fine for sparse embedding.
    last_prime = max(last_prime, p) 
    # Actually, let's not update last_prime strictly to p, because p might jump far.
    # Let's verify: we want 'somewhat' dense packing.
    # If we find 103 (Axis 15) and next requires Axis 0 (Target 1), we can't go back to 33.
    # So yes, embeddings will be 1D ordered by Prime Value.
    print(f"{glyph} -> {p} (Axis {axis}, Target {2*axis+1} mod 32)")

# B. Process I Ching Hexagrams (The 64)
# Range 19904 (0x4DC0) to 19967.
# We map them to Entropy Collapse Axes (Change/Creation).
print("\nMapping I Ching Hexagrams...")
hex_start = 0x4DC0
for i in range(64):
    char = chr(hex_start + i)
    # Alternate between Change (4) and Creation (9) for variety
    # Or map based on Trigram? A bit complex for now.
    # Let's map to Axis 4 (Change) generally, as they are book of Changes.
    axis = AXIS['CHANGE'] 
    p = get_resonant_prime(last_prime, axis)
    token_map[char] = p
    token_axis_map[char] = axis
    used_primes.add(p)
    last_prime = p

# C. Save Output
output = {
    "version": "4.0",
    "map": token_map,
    "axis_map": token_axis_map, # Save this for the model to load!
    "axis_definitions": AXIS
}

with open("agl_token_map_v4.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nMap Saved. Total Glyphs: {len(token_map)}")
print(f"Max Prime Used: {last_prime}")
