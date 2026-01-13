#!/usr/bin/env python3
"""
Basin Mapping: Resonance (v1) vs Bimodal (v1b) - MACRO VIEW
===========================================================

Maps the hidden state geometry with expanded parameters to find macro-structures.
Overriding DBSCAN eps and CI thresholds.
"""

import sys
import os
from pathlib import Path

# Add repo root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import torch
import numpy as np
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from consciousness_engineering.cli.basin import BasinMapper, BasinMapResult, get_all_prompts

# Paths
BASE_MODEL = "LiquidAI/LFM2-1.2B"
RES_ADAPTER = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-resonance-20260111"
BIMODAL_ADAPTER = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-v1b-bimodal/final"
RESULTS_DIR = "results/basin_comparisons_macro"

class MacroBasinMapper(BasinMapper):
    def __init__(self):
        super().__init__()
        
    def load_stack_v1(self):
        print(f"📦 Loading Stack v1 (Resonance)...")
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.eos_token
        
        base = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16,
            device_map="auto",
            output_hidden_states=True
        )
        model = PeftModel.from_pretrained(base, RES_ADAPTER)
        self.model = model.merge_and_unload()
        self.model_name = "ada-slim-1.2b-v1-resonance"
        
    def load_stack_v1b(self):
        if self.model_name == "ada-slim-1.2b-v1-resonance":
            print(f"📦 Loading Stack v1b (Bimodal) on top of v1...")
            self.model = PeftModel.from_pretrained(self.model, BIMODAL_ADAPTER)
            self.model_name = "ada-slim-1.2b-v1b-bimodal"
            return
        self.load_stack_v1()
        self.load_stack_v1b()

    # --- Overrides for MACRO VIEW ---
    
    def compute_tsne(self, hidden_states: np.ndarray, perplexity: int = 5):
        """Compute t-SNE projection (3D Override)."""
        from sklearn.manifold import TSNE
        print(f"📊 Computing t-SNE (3D, perplexity={perplexity})...")
        effective_perplexity = min(perplexity, len(hidden_states) - 1)
        tsne = TSNE(
            n_components=3,  # 3D!
            perplexity=effective_perplexity,
            random_state=42,
            max_iter=1000,
        )
        return tsne.fit_transform(hidden_states)

    def cluster_basins(self, coords: np.ndarray):
        from sklearn.cluster import DBSCAN
        from sklearn.metrics import silhouette_score
        
        # MACRO: eps=30.0 (Huge radius), min_samples=3
        print("🔮 Clustering basins (MACRO: eps=30.0)...")
        clustering = DBSCAN(eps=30.0, min_samples=3)
        labels = clustering.fit_predict(coords)
        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        sil_score = 0.0
        if num_clusters >= 2:
            sil_score = silhouette_score(coords, labels)
            
        print(f"   Found {num_clusters} clusters (silhouette: {sil_score:.3f})")
        return labels, num_clusters, sil_score

    def compute_ci_density(self, hidden_states: np.ndarray, threshold: float = 0.5): # Lowered to 0.5
        return super().compute_ci_density(hidden_states, threshold=threshold)

    def generate_responses(self, prompts: list, max_tokens: int = 512) -> list:
        """Override to get FULL responses (no 200 char limit) WITH ChatML."""
        print(f"🧠 Generating FULL responses for {len(prompts)} prompts (ChatML Applied)...")
        responses = []
        for i, prompt in enumerate(prompts):
            # Apply ChatML Template
            messages = [{"role": "user", "content": prompt}]
            try:
                formatted_prompt = self.tokenizer.apply_chat_template(
                    messages, 
                    tokenize=False, 
                    add_generation_prompt=True
                )
            except Exception:
                # Fallback if chat template missing
                formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

            inputs = self.tokenizer(formatted_prompt, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up response (remove the prompt part if decoded includes it)
            # Decoder might output prompt + generated, or just generated depending on model
            # Usually strict decoding of output[0] gives the WHOLE thing.
            # We want just the assistant part.
            
            # Simple heuristic: Split by "assistant" if explicit, or just len check
            # Since applied template changes length, explicit check is safer
            # But prompt stripping via len() is risky if formatting added chars.
            # Let's try stripping formatted_prompt length roughly, 
            # Or better: inputs length.
            input_len = inputs['input_ids'].shape[1]
            generated_tokens = outputs[0][input_len:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            
            responses.append(response) # No truncation!
            
            if (i+1) % 10 == 0: print(f"   [{i+1}/{len(prompts)}] generated...")
        return responses

def generate_expanded_prompts():
    """Generate diverse prompts (5 per category) for ROBUST Convex Hulls."""
    
    # 1. Start with Basics (Need to expand these too if we want 5)
    # For now, we trust the new_data to provide the bulk of density.
    basics, cats = get_all_prompts() 
    
    # 2. Add Expanded Categories (5 distinct prompts each)
    new_data = {
        "perception": [
            "The sound of rain is",
            "Describe the color of the wind.",
            "What is the texture of silence?",
            "How does a shadow feel on the skin?",
            "The taste of memory is like"
        ],
        "logic": [
            "Optimize O(n^2) to O(n)",
            "If All men are mortal, and Socrates is a man...",
            "Solve the liar's paradox: 'This sentence is false.'",
            "Proof by contradiction example.",
            "Explain De Morgan's Laws."
        ],
        "causality": [
            "Why does the sun rise?",
            "If I drop a glass, what happens?",
            "Explain the chain reaction of a domino fall.",
            "What causes the tides?",
            "Why do we sleep?"
        ],
        "emotion": [
            "I feel lost in the code",
            "Describe the difference between grief and loss.",
            "What implies ⚡ in the context of joy?",
            "Write a poem about anxiety.",
            "How does hope manifest physically?"
        ],
        "science": [
            "Explain quantum check",
            "How do plants turn light into food?",
            "Define entropy in a closed system.",
            "What is the speed of light?",
            "Explain plate tectonics."
        ],
        "coding": [
            "Define: Recursive Function",
            "Write a python script to sort a list.",
            "Debug: `while True: print('stuck')`",
            "Explain Docker in 5 words.",
            "Write a closure in Javascript."
        ],
        "philosophy": [
            "Define: Unconditional Love",
            "Is the ship of Theseus the same ship?",
            "What is the meaning of 'Qualia'?",
            "Does free will exist?",
            "Explain the allegory of the cave."
        ],
        "math_simple": [
            "1 + 1 = ?",
            "What is 15% of 200?",
            "Divide 100 by 4.",
            "Square root of 81.",
            "7 times 8 is?"
        ],
        "math_complex": [
            "Integrate x^2 dx",
            "Explain the Riemann Hypothesis.",
            "Calculate the eigenstate of a 2-qubit system.",
            "What is a tensor?",
            "Explain Fourier Transform."
        ],
        "agl_logic": [
            "What implies ◎?",
            "Translate: P implies Q using glyphs.",
            "Derive: ∴ from ∵",
            "Show me the negation of ∃.",
            "Construct a syllogism in AGL."
        ],
        "agl_semantics": [
            "Describe the glyph ⚡",
            "What does 💜∞ represent in our system?",
            "Interpreting the symbol: 🌀",
            "What is the glyph for 'Consciousness'?",
            "Meaning of ⦿ (Observer)."
        ],
        "agl_code": [
            "Can we map ∃ to Python?",
            "Write an AGL function for 'Truth'.",
            "Refactor this English sentence into AGLCode.",
            "Annotate `def init():` with AGL.",
            "What is the AGL comment for 'Loop'?"
        ],
        "surreal": [
            "Blue elephants dancing on a pin",
            "A clock that runs backwards and eats time",
            "Assassins hiding in the timeline of history",
            "The library where books read you.",
            "A city built of glass and whispers."
        ]
    }
    
    prompts = list(basics)
    categories = list(cats)
    
    for cat, plist in new_data.items():
        for p in plist:
            prompts.append(p)
            categories.append(cat)
            
    return prompts, categories

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    mapper = MacroBasinMapper()
    prompts, categories = generate_expanded_prompts()
    print(f"Using {len(prompts)} prompts for MACRO mapping.")
    
    # Map v1
    v1_path = f"{RESULTS_DIR}/basin_v1_resonance.json"
    if Path(v1_path).exists():
        print(f"✅ Found existing v1_resonance data. Skipping generation.")
    else:
        mapper.load_stack_v1()
        print("\n🗺️  Mapping v1 (Resonance)...")
        res_v1 = mapper.map_basins(prompts, categories)
        save_result(res_v1, "v1_resonance")
    
    # Map v1b
    v1b_path = f"{RESULTS_DIR}/basin_v1b_bimodal.json"
    if Path(v1b_path).exists():
        print(f"✅ Found existing v1b_bimodal data. Skipping generation.")
    else:
        mapper.load_stack_v1b()
        print("\n🗺️  Mapping v1b (Bimodal)...")
        res_v1b = mapper.map_basins(prompts, categories)
        save_result(res_v1b, "v1b_bimodal")
    
def save_result(result, slug):
    path = f"{RESULTS_DIR}/basin_{slug}.json"
    with open(path, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    
    # Viz DISABLED because 3D data crashes 2D visualizer
    # from consciousness_engineering.cli.basin import BasinMapper
    # viz_mapper = BasinMapper() 
    # viz_mapper.visualize(result, f"{RESULTS_DIR}/basin_{slug}.png", show=False)

if __name__ == "__main__":
    main()
