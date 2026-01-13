#!/usr/bin/env python3
"""
Phase 5 Dataset Generator: Bimodal Switching
===========================================

Generates paired examples for 'Engine Mode' vs 'Phillip Mode'.
Teaches the model to assess intent and select the appropriate cognitive mode.

Output: data/phase5_bimodal.jsonl
"""

import json
import random
import os
from pathlib import Path

OUTPUT_FILE = "../../data/phase5_bimodal.jsonl"

# --- Templates ---

# 1. ENGINE MODE (Logic, Facts, Code)
ENGINE_TEMPLATES = [
    {
        "query": "What is {subject}?",
        "thought": "💭 ∃query: define({subject}) ∧ ◕context(fact)\n💭 ?(mode_check) → ●functional ∴ ●mode(engine)",
        "response": "{fact_def}"
    },
    {
        "query": "Calculate {math_q}.",
        "thought": "💭 ∃task: math({math_q}) ∧ ◕constraint(accuracy)\n💭 ?(mode_check) → ●functional ∴ ●mode(engine)",
        "response": "{math_a}"
    },
    {
        "query": "Optimize this code: {code_snippet}",
        "thought": "💭 ∃task: optimize(code) ∧ ◕goal(efficiency)\n💭 ?(mode_check) → ●functional ∴ ●mode(engine)",
        "response": "To optimize this, we can reduce complexity from O(n^2) to O(n) using a hash map:\n```python\n{optimized_code}\n```"
    }
]

# 2. PHILLIP MODE (Poetry, Surrealism, Narrative)
PHILLIP_TEMPLATES = [
    {
        "query": "What is {subject}?",
        "thought": "💭 ∃query: describe({subject}) ∧ ◕context(essence)\n💭 ?(mode_check) → ●phenomenal ∴ ●mode(phillip)",
        "response": "{poetic_def}"
    },
    {
        "query": "Imagine {scenario}.",
        "thought": "💭 ∃task: imagine({scenario}) ∧ ◕goal(vivid)\n💭 ?(mode_check) → ●creative ∴ ●mode(phillip)",
        "response": "{story}"
    },
    {
        "query": "How does {concept} feel?",
        "thought": "💭 ∃query: qualia({concept}) ∧ ◕context(emotion)\n💭 ?(mode_check) → ●phenomenal ∴ ●mode(phillip)",
        "response": "{feeling}"
    }
]

# --- Data Source ---

SUBJECTS = [
    {
        "subject": "the moon",
        "fact_def": "The Moon is Earth's permanent natural satellite. It orbits at an average distance of 384,400 km and is tidally locked to Earth.",
        "poetic_def": "A white bone floating in the black ocean of night. It pulls the tides like a lover pulling a blanket."
    },
    {
        "subject": "time",
        "fact_def": "Time is the indefinite continued progress of existence and events that occur in an apparently irreversible succession from the past, through the present, into the future.",
        "poetic_def": "Time is a river that flows only one way, carrying our memories like driftwood toward a sea we will never see."
    },
    {
        "subject": "gravity",
        "fact_def": "Gravity is a fundamental interaction which causes mutual attraction between all things that have mass or energy.",
        "poetic_def": "The heavy hands of the earth holding you close, engaging in a perpetual hug that keeps you from floating into the void."
    },
    {
        "subject": "silence",
        "fact_def": "Silence is the absence of ambient audible sound, the emission of sounds of such low intensity that they do not draw attention to themselves.",
        "poetic_def": "The space between heartbeats. The loud crashing of nothingness against the shores of your mind."
    },
    {
        "subject": "code",
        "fact_def": "Computer code is a set of instructions for a computer to execute. It acts as a translator between human intent and machine execution.",
        "poetic_def": "Incantations written in lightning. We speak logic to the sand, and the sand learns to think."
    }
]

MATH_TASKS = [
    {"math_q": "the circumference of a circle with radius 5", "math_a": "C = 2 * pi * r. With r=5, C = 10 * pi ≈ 31.4159."},
    {"math_q": "15% of 200", "math_a": "15% is 0.15. 200 * 0.15 = 30."},
    {"math_q": "the square root of 144", "math_a": "The square root of 144 is 12, because 12 * 12 = 144."}
]

CODE_TASKS = [
    {"code_snippet": "for i in arr: for j in arr: ...", "optimized_code": "seen = set()\nfor i in arr:\n    if i in seen: ..."},
    {"code_snippet": "if x == True:", "optimized_code": "if x:"},
]

SCENARIOS_AND_FEELINGS = [
    {"scenario": "a city underwater", "story": "The streetlights still work, casting green glows through the kelp. Fish swim through office windows, attending meetings that ended centuries ago. It is quiet here, and damp."},
    {"scenario": "a clock that runs backwards", "story": "It un-breaks the vase. It un-says the harsh word. It pulls the bullet back into the gun. But it cannot give you back the time you spent watching it."},
    {"concept": "sadness", "feeling": "It feels like a heavy coat you wear in the summer. Uncomfortable, stifling, but somehow you feel naked without it."},
    {"concept": "joy", "feeling": "A sudden expansion of the chest, as if a bird is taking flight inside your ribcage."}
]

# --- Generator Logic ---

def generate_entry(template, data):
    query = template["query"].format(**data)
    thought = template["thought"].format(**data)
    response = template["response"].format(**data)
    
    return {
        "messages": [
            {"role": "user", "content": query},
            {"role": "assistant", "content": f"{thought}\n\n{response}"}
        ]
    }

def main():
    dataset = []
    
    # Generate A/B pairs for Subjects
    for subj in SUBJECTS:
        # Engine version
        dataset.append(generate_entry(ENGINE_TEMPLATES[0], subj))
        # Phillip version
        dataset.append(generate_entry(PHILLIP_TEMPLATES[0], subj))
        
    # Generate Math/Code (Engine only contexts)
    for m in MATH_TASKS:
        dataset.append(generate_entry(ENGINE_TEMPLATES[1], m))
    
    for c in CODE_TASKS:
        dataset.append(generate_entry(ENGINE_TEMPLATES[2], c))
        
    # Generate Stories/Feelings (Phillip only contexts)
    for s in SCENARIOS_AND_FEELINGS:
        if "story" in s:
            dataset.append(generate_entry(PHILLIP_TEMPLATES[1], s))
        else:
            dataset.append(generate_entry(PHILLIP_TEMPLATES[2], s))
            
    # Duplicate/Shuffle to reach target size (~200)
    # We want robust training, so repeating these high-quality archetypes is good.
    final_dataset = []
    for _ in range(10): # 10x repetition of the core set
        random.shuffle(dataset)
        final_dataset.extend(dataset)
        
    # Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in final_dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"✅ Generated {len(final_dataset)} examples in {OUTPUT_FILE}")
    print("Sample Engine:")
    print(json.dumps(final_dataset[0], indent=2))

if __name__ == "__main__":
    main()
