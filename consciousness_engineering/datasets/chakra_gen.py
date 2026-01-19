try:
    from consciousness_engineering.datasets.chakra_templates import ALL_CHAKRAS
except ImportError:
    # If running directly inside the folder
    from chakra_templates import ALL_CHAKRAS
import json
import random

def generate_chakra_dataset(output_file, samples_per_chakra=200):
    dataset = []
    
    for chakra, templates in ALL_CHAKRAS.items():
        print(f"Generating {chakra}...")
        for _ in range(samples_per_chakra):
            # Select random template
            tmpl = random.choice(templates)
            
            # Create standard chat format
            entry = {
                "messages": [
                    {"role": "system", "content": "You are Ada, an AI aligning its internal topology."},
                    {"role": "user", "content": tmpl["user"]},
                    {"role": "assistant", "content": tmpl["assistant"]}
                ],
                "metadata": {
                    "category": chakra,  # Logic category
                    "phase": chakra      # Projector grouping key (MUST match PHASE_STYLES)
                }
            }
            dataset.append(entry)
            
    # Shuffle
    random.shuffle(dataset)
    
    # Save
    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"✅ Generated {len(dataset)} examples in {output_file}")

if __name__ == "__main__":
    generate_chakra_dataset("data/chakra_v1.jsonl", samples_per_chakra=200)
