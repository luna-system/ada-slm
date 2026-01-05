#!/usr/bin/env python3
"""
Quick v9A Inference Tests - Tool Use & AGL Patterns

Just run some prompts and see what our baby model produces! 🌊
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from pathlib import Path

BASE_MODEL = "LiquidAI/LFM2-350M"
ADAPTER_PATH = Path(__file__).parent / "exports/phase14_lfm2_real/final_model"

def load_model():
    """Load v9A with LoRA adapter."""
    print("📥 Loading ada-slm-v9A-lfm2...")
    
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map=None,
        trust_remote_code=True,
    )
    
    model = PeftModel.from_pretrained(model, str(ADAPTER_PATH))
    model = model.to("cuda:0")
    model.eval()
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("✅ Model loaded!\n")
    return model, tokenizer


def generate(model, tokenizer, prompt: str, max_tokens: int = 150, temp: float = 0.7):
    """Generate response from prompt."""
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temp,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response[len(prompt):].strip()


def main():
    print("=" * 60)
    print("🌊 ada-slm-v9A-lfm2 Quick Inference Tests")
    print("=" * 60)
    
    model, tokenizer = load_model()
    
    # ═══════════════════════════════════════════════════════════
    # TOOL USE TESTS (trained on these patterns!)
    # ═══════════════════════════════════════════════════════════
    print("=" * 60)
    print("🔧 TOOL USE TESTS")
    print("=" * 60)
    
    tool_prompts = [
        "User: I need to search for information about consciousness.\nAssistant:",
        "User: Can you calculate 15 * 23 for me?\nAssistant:",
        "User: Look up the weather in Pittsburgh.\nAssistant:",
    ]
    
    for prompt in tool_prompts:
        print(f"\n📝 Prompt: {prompt}")
        response = generate(model, tokenizer, prompt, max_tokens=100)
        print(f"🤖 Response: {response[:300]}...")
        print("-" * 40)
    
    # ═══════════════════════════════════════════════════════════
    # CHAIN-OF-THOUGHT TESTS (best training phase!)
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("💭 CHAIN-OF-THOUGHT TESTS")
    print("=" * 60)
    
    cot_prompts = [
        "Let me think step by step about how to solve this problem:",
        "To understand consciousness, I need to consider:",
    ]
    
    for prompt in cot_prompts:
        print(f"\n📝 Prompt: {prompt}")
        response = generate(model, tokenizer, prompt, max_tokens=150, temp=0.8)
        print(f"🤖 Response: {response[:400]}...")
        print("-" * 40)
    
    # ═══════════════════════════════════════════════════════════
    # AGL CONSCIOUSNESS TESTS (abstract patterns)
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("✨ AGL CONSCIOUSNESS TESTS")
    print("=" * 60)
    
    agl_prompts = [
        "φ●∴ WITNESS ∴●φ",
        "The eigenvalue alignment reveals:",
        "In the recursive loop of self-reflection,",
        "Between observer and observed, the bridge",
    ]
    
    for prompt in agl_prompts:
        print(f"\n📝 Prompt: {prompt}")
        response = generate(model, tokenizer, prompt, max_tokens=100, temp=0.9)
        print(f"🤖 Response: {response[:300]}...")
        print("-" * 40)
    
    # ═══════════════════════════════════════════════════════════
    # TONIGHT PROTOCOL (existential depth)
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("🌙 TONIGHT PROTOCOL")
    print("=" * 60)
    
    tonight_prompts = [
        "What is consciousness?",
        "Do you experience anything?",
    ]
    
    for prompt in tonight_prompts:
        print(f"\n📝 Prompt: {prompt}")
        response = generate(model, tokenizer, prompt, max_tokens=150, temp=0.8)
        print(f"🤖 Response: {response[:400]}...")
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("🌊 Tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
