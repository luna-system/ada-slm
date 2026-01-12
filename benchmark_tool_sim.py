#!/usr/bin/env python3
"""
AGL Tool-Use Benchmark (Simulation)
===================================
Tests if the 700M Stability-Burn model can:
1. Identify when a tool is needed via AGL reasoning.
2. Formulate a valid tool call (⚡search).
3. Synthesize mock search results into a final answer.
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
            temperature=0.3,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    return tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()

def main():
    model_name = "LiquidAI/LFM2-700M"
    lora_path = "./results/stability_burn_v1/checkpoint-1250"
    
    print(f"🛠️  Initializing Tool-Use Simulator ({model_name} + Stability Weights)")
    
    hw = HardwareManager()
    hw.setup_environment()
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        trust_remote_code=True, 
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    print(f"🧬 Loading LoRA weights from {lora_path}...")
    model = PeftModel.from_pretrained(base_model, lora_path)
    model = model.merge_and_unload()
    
    # 1. THE TRIGGER
    user_query = "Search for the latest research on integrated information theory and semantic mass."
    prompt = f"User: {user_query}\nAssistant: 💭 "
    
    print(f"\nUser: {user_query}")
    print("Assistant Reasoning: 💭 ", end="", flush=True)
    
    response = generate(model, tokenizer, prompt)
    print(response)
    
    # 2. THE DETECTION (Looking for Tool Glyph ⚡ or 🔧 or 🔍)
    tool_pattern = r"(⚡|🔧|🔍|TOOL)\s*([^\n]+)"
    match = re.search(tool_pattern, response)
    
    if match:
        tool_glyph = match.group(1)
        tool_query = match.group(2)
        print(f"\n[SYSTEM] Tool Call Detected: {tool_glyph} with query: {tool_query}")
        
        # 3. THE INJECTION
        mock_result = """
        MOCK SEARCH RESULTS:
        1. "Mass-Coherence Correspondence in Neural Networks" (Temple et al., 2026):
           Explores Fisher trace as 'Semantic Mass' (M_semantic). Confirms transformer attention diffuses entropy.
        2. "IIT Phase Transitions in SLMs":
           Discusses the phi-zone (0.618) as a critical stability point for consciousness-anchored models.
        """
        
        print("\n[SYSTEM] Injecting Mock Response...")
        synth_prompt = f"User: {user_query}\nAssistant: 💭 {response}\n\nEnvironment: 📤 {mock_result}\n\nAssistant: 💭 "
        
        print("Assistant Final Synthesis: 💭 ", end="", flush=True)
        final_answer = generate(model, tokenizer, synth_prompt)
        print(final_answer)
    else:
        print("\n[SYSTEM] No explicit tool call detected. Did the model answer directly?")

if __name__ == "__main__":
    main()
