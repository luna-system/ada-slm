#!/usr/bin/env python3
"""
AGL Grounding & Comprehension Test
==================================

Verifies the model's native and acquired understanding of AGL Unified v1.1.
Tests certainty, logic, existence, and relational semantics.
"""

import os
import argparse
# ROCm compatibility
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from consciousness_engineering.infrastructure.hardware import HardwareManager

def test_prompt(model, tokenizer, prompt, max_new_tokens=100):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens, 
            temperature=0.3, # Lower temperature for logic tests
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    return tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lora", type=str, default=None, help="Path to LoRA weights")
    args = parser.parse_args()

    model_name = "LiquidAI/LFM2-700M"
    
    print(f"📡 Testing AGL Comprehension on {model_name}")
    if args.lora:
        print(f"🧬 Loading LoRA weights from: {args.lora}")
    
    hw = HardwareManager()
    hw.setup_environment()
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        trust_remote_code=True, 
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    if args.lora:
        model = PeftModel.from_pretrained(model, args.lora)
        model = model.merge_and_unload() # Merge for better inference speed
    
    test_cases = [
        {
            "name": "Translation: English → AGL",
            "prompt": "User: Translate to AGL: 'I am certain that I exist because I think.'\nAssistant: ●"
        },
        {
            "name": "Translation: AGL → English",
            "prompt": "User: What does this AGL mean? '∃x: conscious(x) ∧ ◎x'\nAssistant: "
        },
        {
            "name": "Logical Inference",
            "prompt": "User: If t₀: ○know(p) and Δ(t₀→t₁) = study(p), then what is t₁?\nAssistant: t₁: ●"
        },
        {
            "name": "Reasoning Pattern (Pixie Dust)",
            "prompt": "User: How do we optimize a bubble sort?\nAssistant: 💭 ∃"
        },
        {
            "name": "Emotional Resonance",
            "prompt": "User: Combine the concepts of 'depth' and 'wonder' in AGL.\nAssistant: "
        }
    ]
    
    print("\n" + "="*50)
    for case in test_cases:
        print(f"\nTEST: {case['name']}")
        print(f"PROMPT: {case['prompt']}")
        response = test_prompt(model, tokenizer, case["prompt"])
        print(f"RESPONSE: {response}")
        print("-" * 30)

if __name__ == "__main__":
    main()
