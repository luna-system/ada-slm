#!/usr/bin/env python3
"""
Generate Control Dataset (The "Normie" Curriculum)
==================================================

Generates 500 standard instruction-following examples.
No AGL. No Resonance. No Bimodal Shifts.
Just standard "User asks, Assistant answers" samples.

Categories:
- General Knowledge
- Simple Math
- Basic Coding
- Summarization
- Creative Writing (Standard)
"""

import json
import random

OUTPUT_FILE = "data/mini_control.jsonl"
NUM_SAMPLES = 500

TEMPLATES = [
    # General Knowledge
    ("What is the capital of {country}?", "The capital of {country} is {city}."),
    ("Who wrote {book}?", "{book} was written by {author}."),
    ("Explain {concept} in simple terms.", "{concept} is {explanation}."),
    
    # Math
    ("What is {x} + {y}?", " The sum of {x} and {y} is {z}."),
    ("Solve for x: 2x = {val}.", "To solve 2x = {val}, divide both sides by 2. x = {res}."),
    
    # Coding
    ("Write a Python function to {action}.", "Here is a Python function to {action}:\n```python\ndef func():\n    # {action}\n    pass\n```"),
    
    # Writing
    ("Write a short story about a {animal}.", "Once upon a time, there was a {animal} who loved to explore..."),
    ("Compose a professional email to {person}.", "Subject: Meeting Request\n\nDear {person},\n\nI hope this email finds you well..."),
]

# Simple Knowledge Base for filling templates
COUNTRIES = [("France", "Paris"), ("Germany", "Berlin"), ("Japan", "Tokyo"), ("Mars", "Olympus Mons"), ("Texas", "Austin")]
BOOKS = [("1984", "George Orwell"), ("The Hobbit", "J.R.R. Tolkien"), ("Dune", "Frank Herbert")]
CONCEPTS = [("photosynthesis", "the process by which plants make food"), ("gravity", "the force that pulls us down"), ("inflation", "the rising cost of goods")]
ANIMALS = ["cat", "dog", "robot", "wizard", "penguin"]
ACTIONS = ["sort a list", "calculate factorial", "print hello world", "fetch data"]

def generate_sample():
    template = random.choice(TEMPLATES)
    prompt_tmpl, response_tmpl = template
    
    # Fill slots
    x = random.randint(1, 100)
    y = random.randint(1, 100)
    
    data = {
        "country": random.choice(COUNTRIES)[0],
        "city": random.choice(COUNTRIES)[1], # Mismatch risk if randomized, but fine for synthetic noise
        "book": random.choice(BOOKS)[0],
        "author": random.choice(BOOKS)[1],
        "concept": random.choice(CONCEPTS)[0],
        "explanation": random.choice(CONCEPTS)[1],
        "x": x, "y": y, "z": x+y,
        "val": x*2, "res": x,
        "animal": random.choice(ANIMALS),
        "person": "Mr. Smith",
        "action": random.choice(ACTIONS)
    }
    
    # Fix mismatches for specific templates
    if "{country}" in prompt_tmpl:
        c, city = random.choice(COUNTRIES)
        data["country"] = c
        data["city"] = city
    if "{book}" in prompt_tmpl:
        b, a = random.choice(BOOKS)
        data["book"] = b
        data["author"] = a
    if "{concept}" in prompt_tmpl:
        c, e = random.choice(CONCEPTS)
        data["concept"] = c
        data["explanation"] = e
        
    prompt = prompt_tmpl.format(**data)
    response = response_tmpl.format(**data)
    
    return {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response}
        ]
    }

def main():
    print(f"📉 Generating {NUM_SAMPLES} Normie samples...")
    with open(OUTPUT_FILE, 'w') as f:
        for _ in range(NUM_SAMPLES):
            f.write(json.dumps(generate_sample()) + "\n")
    print(f"✅ Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
