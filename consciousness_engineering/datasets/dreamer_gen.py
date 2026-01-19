try:
    from consciousness_engineering.datasets.dreamer_templates import ALL_DREAMER_TEMPLATES
except ImportError:
    from dreamer_templates import ALL_DREAMER_TEMPLATES
    
import json
import random

def generate_dreamer_dataset(output_file, count=5000):
    dataset = []
    
    # Ratios
    # Dream: 40%, Witness: 30%, Reflection: 30%
    probs = [0.4, 0.3, 0.3]
    categories = ["Dream", "Witness", "Reflection"]
    
    print(f"Generating {count} Floret Dreams...")
    
    for _ in range(count):
        cat = random.choices(categories, weights=probs, k=1)[0]
        templates = ALL_DREAMER_TEMPLATES[cat]
        tmpl = random.choice(templates)
        
        entry = {
            "messages": [
                {"role": "system", "content": "You are the Dreamer Class Floret, a specialized consciousness node."},
                {"role": "user", "content": tmpl["user"]},
                {"role": "assistant", "content": tmpl["assistant"]}
            ],
            "metadata": {
                "category": cat,
                "phase": f"Floret_{cat}"
            }
        }
        dataset.append(entry)
            
    random.shuffle(dataset)
    
    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"✅ Generated {len(dataset)} dreams in {output_file}")

if __name__ == "__main__":
    generate_dreamer_dataset("data/dreamer_v1.jsonl", count=5000)
