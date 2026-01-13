#!/usr/bin/env python3
"""
Prepare Mini Datasets for SLIM-EVO-MINI-LAB
"""
import json
import random

def slice_dataset(input_path, output_path, n=100, filter_key=None, filter_val=None):
    data = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)
                if filter_key:
                    # simplistic check in metadata or text
                    if entry.get("metadata", {}).get(filter_key) == filter_val:
                        data.append(entry)
                else:
                    data.append(entry)
    
    # Shuffle and slice
    random.shuffle(data)
    mini = data[:n]
    
    with open(output_path, 'w') as f:
        for entry in mini:
            f.write(json.dumps(entry) + '\n')
            
    print(f"✅ Created {output_path} with {len(mini)} examples (from {len(data)})")

def main():
    # Dataset A: Resonance (Thinking)
    # Source: Phase 3 (we suspect it's good). 
    # Let's verify paths.
    p3_path = "data/phase3_full_dataset.jsonl"
    p5_path = "data/phase5_bimodal.jsonl"
    
    # Filter pure process/thinking for Resonance
    slice_dataset(p3_path, "data/mini_resonance.jsonl", n=100)
    
    # Dataset B: Bimodal (Switching)
    slice_dataset(p5_path, "data/mini_bimodal.jsonl", n=100)

if __name__ == "__main__":
    main()
