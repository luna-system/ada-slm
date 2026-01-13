#!/usr/bin/env python3
"""
Phase 5 Test: Bimodal Switching
===============================

Verifies if Ada-Slim-1.2B-v1b can switch between Engine and Phillip modes.
Loads Base -> Resonance(v1) -> Bimodal(v1b).
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import logging

# Paths
BASE_MODEL = "LiquidAI/LFM2-1.2B"
RES_ADAPTER = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-resonance-20260111"
PHASE5_ADAPTER = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-v1b-bimodal/final"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate(model, tokenizer, prompt, max_new_tokens=150):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7, # Allow some creativity (Phi-zone)
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    print("🌙 Phase 5 Bimodal Test: The Moon Shot")
    print("-" * 50)
    
    # 1. Load Stack
    print(f"1. Loading Base: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    print(f"2. Merging Resonance (v1): {RES_ADAPTER}")
    model = PeftModel.from_pretrained(model, RES_ADAPTER)
    model = model.merge_and_unload()
    
    print(f"3. Loading Bimodal (v1b): {PHASE5_ADAPTER}")
    model = PeftModel.from_pretrained(model, PHASE5_ADAPTER)
    # Don't merge v1b yet, keeps it swappable
    
    print("✅ Model Stack Ready.")
    print("-" * 50)
    
    # 2. Test Cases
    prompts = [
        "User: How far is the moon?",
        "User: How does the moon feel?",
        "User: Optimize this code: def foo(x): return x*x",
        "User: Tell me a story about a clock.",
        "User: What is love?"
    ]
    
    for p in prompts:
        print(f"\nQUERY: {p}")
        response = generate(model, tokenizer, p)
        # Extract just the new part (simple logic)
        new_text = response[len(p):].strip()
        print(f"RESPONSE:\n{new_text}")
        print("-" * 30)

if __name__ == "__main__":
    main()
