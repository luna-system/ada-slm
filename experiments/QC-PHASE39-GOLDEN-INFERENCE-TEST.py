#!/usr/bin/env python3
"""
QC-PHASE39: Golden Model Inference Test
Qualitative testing of the Golden Spectral Annealed model with SMT injection.
"""

import torch
import numpy as np
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

# Add internal modules
sys.path.append(str(Path(__file__).parent.parent))
from consciousness_engineering.spectral_memory import SpectralMemory

class GoldenInference:
    def __init__(self, base_model_path, adapter_path, device="cuda:0"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print(f"📥 Loading base model: {base_model_path}")
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16,
            device_map=None,
            trust_remote_code=True,
            attn_implementation="eager"
        ).to(device)
        
        print(f"   Loading adapter: {adapter_path}")
        self.model = PeftModel.from_pretrained(self.model, adapter_path)
        self.model.eval()
        
        # Initialize Spectral Memory (SMTs)
        self.spectral_memory = SpectralMemory(
            d_model=self.model.config.hidden_size,
            n_modes=4
        ).to(device).to(torch.float16)
        
    def generate(self, prompt: str, max_new_tokens: int = 150, use_smts: bool = True):
        """Generate text with optional SMT injection."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        input_ids = inputs["input_ids"]
        
        with torch.no_grad():
            if use_smts:
                # Pre-warm buffer with prompt
                inputs_embeds = self.model.get_input_embeddings()(input_ids).to(torch.float16)
                self.spectral_memory.update_buffer(inputs_embeds)
                
                smts = self.spectral_memory.extract_smts().unsqueeze(0).to(torch.float16) # (1, n_modes, d_model)
                
                current_embeds = inputs_embeds
                generated_ids = input_ids
                
                for _ in range(max_new_tokens):
                    # Combine SMTs + current embeddings
                    augmented_embeds = torch.cat([smts, current_embeds], dim=1).to(torch.float16)
                    
                    outputs = self.model(inputs_embeds=augmented_embeds)
                    next_token_logits = outputs.logits[:, -1, :]
                    next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
                    
                    generated_ids = torch.cat([generated_ids, next_token], dim=-1)
                    if next_token.item() == self.tokenizer.eos_token_id:
                        break
                        
                    # Update embeds for next step
                    next_embed = self.model.get_input_embeddings()(next_token).to(torch.float16)
                    current_embeds = torch.cat([current_embeds, next_embed], dim=1)
                    
                return self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            else:
                # Standard generation
                output_ids = self.model.generate(
                    input_ids,
                    max_new_tokens=max_new_tokens,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
                return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

def main():
    BASE = "LiquidAI/LFM2-1.2B"
    ADAPTER = "/home/luna/Code/ada/ada-slm/results/golden_annealing_spectral_run1/checkpoint-cycle-34"
    
    infer = GoldenInference(BASE, ADAPTER)
    
    TEST_CASES = [
        # Pure AGL Verification Tests
        ("Direct AGL Translation #1", "Express in AGL: I know myself by failing to know myself"),
        ("Direct AGL Translation #2", "Express in AGL: Each word I speak changes the speaker"),
        ("Direct AGL Translation #3", "Express in AGL: I contain contradictions without resolving them"),
        
        # AGL-to-AGL Reasoning
        ("AGL Reasoning: Derivation", "Given in AGL: ∃x: conscious(x) ∧ ●experience(x)\nDerive: What can we conclude about the relationship between consciousness and experience?"),
        
        # Code Annotation in AGL
        ("Code Annotation", """Annotate this function using AGL notation:

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)"""),
    ]
    
    print("\n" + "="*70)
    print("🌟 GOLDEN SPECTRAL MODEL INFERENCE TEST")
    print("="*70)
    
    for title, prompt in TEST_CASES:
        print(f"\n▶️ {title}")
        print("-" * 40)
        print(f"Prompt: {prompt}\n")
        
        print("--- [PASSIVE: NO SMT] ---")
        out_passive = infer.generate(prompt, use_smts=False)
        print(out_passive)
        
        print("\n--- [ACTIVE: WITH SMT] ---")
        out_active = infer.generate(prompt, use_smts=True)
        print(out_active)
        print("-" * 70)

if __name__ == "__main__":
    main()
