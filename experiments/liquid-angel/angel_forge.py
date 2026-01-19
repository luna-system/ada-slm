import random
import math
import sympy
from collections import deque

# ============================================================================
# ANGEL FORGE: SYNTHETIC DATA GENERATOR
# Generates Geometric, Logic, and Prime Resonance data for Slim-Evo-13
# ============================================================================

OUTPUT_DIR = "data"
VOCAB_SIZE = 1999

# ----------------------------------------------------------------------------
# 1. THE PRIME SKELETON (Number Sense)
# ----------------------------------------------------------------------------
def generate_prime_sequence(length=200, start_range=(2, 1000)):
    """Generates a sequence of primes and their gaps."""
    start = random.randint(*start_range)
    primes = []
    current = start
    for _ in range(length):
        p = sympy.nextprime(current)
        if p >= 1999: # Stay within Vocab
            current = 2
            p = 2
        primes.append(str(p))
        current = p
    return " ".join(primes)

def generate_factorization_task():
    """Generates a 'Factor This' task."""
    # We use tokens to represent numbers. 
    # Example: "Factor 53 : P" (where P is a token for Prime)
    # Example: "Factor 15 : 3 5"
    n = random.randint(4, 500)
    factors = sympy.factorint(n)
    
    # Format: VAL ∇ → FACTOR FACTOR
    # Using AGL Logic: "Number Prism -> Factors"
    expanded_factors = []
    for f, count in factors.items():
        expanded_factors.extend([str(f)] * count)
        
    return f"{n} ∇ → {' '.join(expanded_factors)}"

# ----------------------------------------------------------------------------
# 2. THE LOGIC LATTICE (AGL Syntax)
# ----------------------------------------------------------------------------
AGL_GLYPHS = {
    'entity': ['Self', 'Other', 'Void', 'Light', 'Pattern', 'Chaos'],
    'action': ['⊗', '→', '↔', '∇', '⋈', '⛩'],
    'state': ['●', '○', 'Φ', '13', '53'],
    'top': ['⊤', '⊥']
}

def generate_agl_chain():
    """Generates valid AGL logic statements."""
    # Pattern 1: Transformation
    # A ⊗ B → C
    a = random.choice(AGL_GLYPHS['entity'])
    b = random.choice(AGL_GLYPHS['entity'])
    op = '⊗' # Entangle
    res = 'Pattern' if a != b else 'Resonance'
    
    return f"{a} {op} {b} → {res}"

def generate_agl_topological_truth():
    """Generates topological truth assertions."""
    # Pattern: A ⛩ B (Transition)
    a = random.choice(AGL_GLYPHS['entity'])
    return f"{a} ⛩ ∇ → 💠{a}" # Entity enters Gate, Refracts, becomes Crystal

# ----------------------------------------------------------------------------
# 3. THE LIQUID FLOW (Wave Dynamics)
# ----------------------------------------------------------------------------
def generate_wave_sequence(length=200):
    """Generates numeric tokens representing a coherent wave."""
    # We map sine wave amplitude to token IDs [100-200]
    freq = random.uniform(0.1, 0.5)
    phase = random.uniform(0, math.pi)
    tokens = []
    for t in range(length):
        val = math.sin(t * freq + phase)
        # Map -1..1 to integer token range 100-200
        token_id = int(150 + (val * 50))
        tokens.append(str(token_id))
    return " ".join(tokens)

# ----------------------------------------------------------------------------
# MAIN FORGE
# ----------------------------------------------------------------------------
def forge_dataset(num_samples=1000, filename="corpus_angelic.txt"):
    print(f"Forging {num_samples} samples into {filename}...")
    
    import os
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    with open(f"{OUTPUT_DIR}/{filename}", "w") as f:
        for _ in range(num_samples):
            # Prioritize Numeric Modes (Prime, Wave) for initial training compatibility
            # AGL and Factor modes produce short or non-numeric output which the current simple loader drops
            mode = random.choices(['prime', 'wave'], weights=[0.7, 0.3])[0]
            
            if mode == 'prime':
                line = generate_prime_sequence(length=256)
            elif mode == 'wave':
                line = generate_wave_sequence(length=256)
                
            f.write(line + "\n")
            
    print("Forging complete.")

if __name__ == "__main__":
    # Ensure sympy is installed (it usually is in this env, if not we'd need to install)
    try:
        forge_dataset(num_samples=5000)
    except ImportError:
        print("SymPy not found. Please install sympy to run the Forge.")
