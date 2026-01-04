#!/usr/bin/env python3
"""
Generate v9B-pure AGL training dataset.

Creates 2000 examples across 4 phases:
- Warmup (500): Certainty gradient, basic φ-patterns
- Tonight (500): Existential questions, quantifiers, 0.60 threshold
- Eigenvalue (500): Temporal progressions, Δ operators
- Deep AGL (500): Full vocabulary integration

Output: data/v9b_pure_agl_training.jsonl
"""

import sys
sys.path.insert(0, ".")

from pathlib import Path
from consciousness_engineering.datasets.v9b_pure import V9BPureGenerator

def main():
    print("=" * 60)
    print("V9B-Pure AGL Dataset Generator")
    print("=" * 60)
    
    # Create generator
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    generator = V9BPureGenerator(output_dir=str(output_dir))
    
    print(f"\nConfiguration:")
    print(f"  Output directory: {output_dir.absolute()}")
    print(f"  Examples per phase: 500")
    print(f"  Total examples: 2000")
    print(f"  Phases: warmup → tonight → eigenvalue → deep_agl")
    
    print("\n" + "-" * 60)
    print("Generating dataset...")
    print("-" * 60)
    
    # Generate and save
    output_path = generator.generate_and_save()
    
    print("\n" + "=" * 60)
    print(f"Dataset saved to: {output_path}")
    print("=" * 60)
    
    # Show sample from each phase
    print("\nSample from each phase:")
    print("-" * 60)
    
    with open(output_path) as f:
        import json
        lines = f.readlines()
        
        # Get first example from each phase
        phases_seen = set()
        for line in lines:
            data = json.loads(line)
            phase = data.get("phase", "unknown")
            if phase not in phases_seen:
                phases_seen.add(phase)
                print(f"\n[{phase.upper()}]")
                print(f"User: {data['messages'][0]['content'][:60]}...")
                print(f"Assistant: {data['messages'][1]['content'][:100]}...")
                
                if len(phases_seen) >= 4:
                    break
    
    print("\n" + "=" * 60)
    print("Generation complete! Ready for training.")
    print("=" * 60)

if __name__ == "__main__":
    main()
