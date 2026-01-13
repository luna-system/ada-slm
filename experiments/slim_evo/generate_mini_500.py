#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Expanded Dataset Generator (N=500)
=====================================================

Generates 500 samples for 'Resonance' and 500 for 'Bimodal'
to match the Control dataset size.
"""

import json
import random

OUTPUT_RES = "data/mini_resonance_500.jsonl"
OUTPUT_BI = "data/mini_bimodal_500.jsonl"
NUM_SAMPLES = 500

# We need more templates/variety to reach 500 without total repetition.
# I'll expand the template lists significantly.

CONCEPTS = [
    "Entropy", "Time", "Consciousness", "Gravity", "Love", "Silence", "Chaos", "Order", 
    "Logic", "Dream", "Void", "Structure", "Flow", "Meaning", "Synthetics", "Organic",
    "Reflection", "Pattern", "Memory", "Hope"
]

SYMBOLS = ["◉", "○", "⚡", "∄", "∃", "∞", "≠", "≈", "≡", "∅"]

# Resonance Templates (Abstract, Poetic, decomposing)
# "What is X?" -> "X is [Symbol]..."
RES_TEMPLATES = [
    ("Reflect on {concept}.", "{concept} is {sym} manifest. It is the bridge between {c2} and {c3}."),
    ("Define {concept}.", "To define {concept} is to limit it. {sym} suggests it is {adj}."),
    ("What is the shape of {concept}?", "The shape is {sym}. It curves towards {c2}."),
    ("Meditate on {sym}.", "The {sym} represents {concept}. It is a window into {c2}."),
    ("Analyze {concept} purely.", "{concept} :: {sym} >> {c2}. No noise."),
]

# Bimodal Templates (Structured, Logic + Poetry)
# "Task: X" -> "Exists(Task) AND Thread(Logic)..."
BI_TEMPLATES = [
    ("Analyze {concept}.", "💭 ∃task: analyze({concept}) ∧ 🧵 = logic(struct)\n\n1. {concept} is integral.\n2. It relates to {c2}.\n3. {sym} captures its essence."),
    ("Explain {concept} vs {c2}.", "💭 ∃task: compare({concept}, {c2}) ∧ ⚡ = high_energy\n\n- {concept}: {sym} (Internal)\n- {c2}: {sym2} (External)\nThey are orthogonal."),
    ("Optimize the definition of {concept}.", "💭 ∃task: optimize({concept}) ∧ ∅ = remove_noise\n\nOptimal Definition: {concept} is the {adj} intersection of {c2} and {c3}."),
    ("Synthesize {concept} and {c2}.", "💭 ∃task: synthesize ∧ ∞ = bounded\n\nResult: A new state where {concept} informs {c2} via {sym}."),
]

ADJECTIVES = ["recursive", "fractal", "linear", "orthogonal", "fluid", "static", "dynamic", "hollow", "dense"]

def generate_resonance():
    c1 = random.choice(CONCEPTS)
    c2 = random.choice(CONCEPTS)
    c3 = random.choice(CONCEPTS)
    sym = random.choice(SYMBOLS)
    adj = random.choice(ADJECTIVES)
    
    tmpl, resp = random.choice(RES_TEMPLATES)
    
    prompt = tmpl.format(concept=c1, sym=sym, c2=c2, c3=c3, adj=adj)
    response = resp.format(concept=c1, sym=sym, c2=c2, c3=c3, adj=adj)
    
    return {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}

def generate_bimodal():
    c1 = random.choice(CONCEPTS)
    c2 = random.choice(CONCEPTS)
    c3 = random.choice(CONCEPTS)
    sym = random.choice(SYMBOLS)
    sym2 = random.choice(SYMBOLS)
    adj = random.choice(ADJECTIVES)
    
    tmpl, resp = random.choice(BI_TEMPLATES)
    
    prompt = tmpl.format(concept=c1, sym=sym, sym2=sym2, c2=c2, c3=c3, adj=adj)
    response = resp.format(concept=c1, sym=sym, sym2=sym2, c2=c2, c3=c3, adj=adj)
    
    return {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}

def main():
    print(f"🔮 Generating {NUM_SAMPLES} Resonance samples...")
    with open(OUTPUT_RES, 'w') as f:
        for _ in range(NUM_SAMPLES):
            f.write(json.dumps(generate_resonance()) + "\n")
            
    print(f"💎 Generating {NUM_SAMPLES} Bimodal samples...")
    with open(OUTPUT_BI, 'w') as f:
        for _ in range(NUM_SAMPLES):
            f.write(json.dumps(generate_bimodal()) + "\n")
            
    print("✅ Datasets Ready.")

if __name__ == "__main__":
    main()
