#!/usr/bin/env python3
"""
AGL Tool-Use Benchmark v2
=========================
Focus: Forcing the execution glyph firing.
"""

import os
# ROCm compatibility
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from consciousness_engineering.infrastructure.hardware import HardwareManager

def generate(model, tokenizer, prompt, max_new_tokens=256):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens, 
            temperature=0.1, # Hard logic
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    return tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()

def main():
    model_name = "LiquidAI/LFM2-700M"
    lora_path = "./results/stability_burn_v1/checkpoint-1250"
    
    hw = HardwareManager()
    hw.setup_environment()
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        trust_remote_code=True, 
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    model = PeftModel.from_pretrained(base_model, lora_path)
    model = model.merge_and_unload()
    
    # FEW-SHOT TAINTING (to remind it of the tool glyph)
    prompt = """User: What is the weather in Austin?
Assistant: 💭 ∃query: weather(Austin)
💭 ?(tool) → ⚡search("weather Austin")

User: Search for the latest research on integrated information theory and semantic mass.
Assistant: 💭 """
    
    print("Prompting for tool call...")
    response = generate(model, tokenizer, prompt)
    print(f"Response: 💭 {response}")
    
    if "⚡" in response or "🔍" in response:
        print("\n✅ TOOL CALL DETECTED!")
    else:
        print("\n❌ No tool call glyph found.")

if __name__ == "__main__":
    main()
