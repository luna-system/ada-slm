#!/usr/bin/env python3
"""
Expand v9f_polyglot dataset by sampling from v9g_stage1.

Goal: 200 → 500 examples while maintaining:
- All original v9f examples (the magic ones!)
- Balanced language distribution
- No duplicates
"""

import json
import random
from pathlib import Path
from collections import defaultdict

random.seed(42)  # Reproducibility

DATA_DIR = Path(__file__).parent.parent / "data"

def load_jsonl(path: Path) -> list[dict]:
    """Load JSONL file."""
    with open(path) as f:
        return [json.loads(line) for line in f]

def save_jsonl(data: list[dict], path: Path):
    """Save to JSONL file."""
    with open(path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def get_content_key(item: dict) -> str:
    """Get unique key for deduplication."""
    return item['messages'][0]['content'].strip().lower()

def main():
    # Load datasets
    v9f = load_jsonl(DATA_DIR / "v9f_polyglot.jsonl")
    v9g = load_jsonl(DATA_DIR / "v9g_stage1_polyglot.jsonl")
    
    print(f"v9f: {len(v9f)} examples")
    print(f"v9g_stage1: {len(v9g)} examples")
    
    # Get existing v9f content keys for dedup
    v9f_keys = {get_content_key(item) for item in v9f}
    
    # Filter v9g to only new examples
    v9g_new = [item for item in v9g if get_content_key(item) not in v9f_keys]
    print(f"v9g unique (not in v9f): {len(v9g_new)} examples")
    
    # Group by phase
    v9g_by_phase = defaultdict(list)
    for item in v9g_new:
        v9g_by_phase[item['phase']].append(item)
    
    for phase, items in v9g_by_phase.items():
        print(f"  {phase}: {len(items)} available")
    
    # Target: 500 total, balanced across languages
    # v9f has: 60 english, 70 toki pona, 70 lojban = 200
    # Want: ~167 each = 500 total
    # Need to add: ~107 english, ~97 toki pona, ~97 lojban = 300 more
    
    target_per_phase = {
        'polyglot_english': 107,
        'polyglot_tokipona': 97,
        'polyglot_lojban': 97,
    }
    
    # Sample from each phase
    additions = []
    for phase, target in target_per_phase.items():
        available = v9g_by_phase[phase]
        n_sample = min(target, len(available))
        sampled = random.sample(available, n_sample)
        additions.extend(sampled)
        print(f"Sampled {n_sample} from {phase}")
    
    # Combine
    expanded = v9f + additions
    random.shuffle(expanded)  # Shuffle for training
    
    print(f"\nFinal dataset: {len(expanded)} examples")
    
    # Count by phase
    phase_counts = defaultdict(int)
    for item in expanded:
        phase_counts[item['phase']] += 1
    for phase, count in sorted(phase_counts.items()):
        print(f"  {phase}: {count}")
    
    # Save
    output_path = DATA_DIR / "v9f_expanded_500.jsonl"
    save_jsonl(expanded, output_path)
    print(f"\nSaved to: {output_path}")

if __name__ == "__main__":
    main()
