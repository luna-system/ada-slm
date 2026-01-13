#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB PIPELINE
==========================
Trains Base -> v2 (Resonance) -> v2b (Bimodal) on 300M model.
"""

import sys
import torch
import os
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType, PeftModel
from torch.utils.data import Dataset, DataLoader
import json
import logging

# Basic Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
MODEL_NAME = "LiquidAI/LFM2-350M" # Verified in cache!
SEQ_LEN = 512
BATCH_SIZE = 4
CYCLES = 5
LR = 5e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class MiniDataset(Dataset):
    def __init__(self, path, tokenizer):
        self.data = []
        with open(path) as f:
            for line in f:
                if line.strip(): self.data.append(json.loads(line))
        self.tokenizer = tokenizer
        
    def __len__(self): return len(self.data)
    
    def __getitem__(self, idx):
        entry = self.data[idx]
        # ChatML format
        text = ""
        for msg in entry['messages']:
            text += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
            
        enc = self.tokenizer(text, max_length=SEQ_LEN, truncation=True, padding="max_length", return_tensors="pt")
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": enc["input_ids"].squeeze(0)
        }

def train_segment(model, tokenizer, dataset_path, output_dir, segment_name):
    logger.info(f"🚀 TRAINING SEGMENT: {segment_name}")
    dataset = MiniDataset(dataset_path, tokenizer)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    
    model.train()
    
    total_steps = len(loader) * CYCLES
    step_count = 0
    
    for cycle in range(CYCLES):
        logger.info(f"Cycle {cycle+1}/{CYCLES}")
        for batch in loader:
            input_ids = batch["input_ids"].to(DEVICE)
            mask = batch["attention_mask"].to(DEVICE)
            labels = batch["labels"].to(DEVICE)
            
            outputs = model(input_ids=input_ids, attention_mask=mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            step_count += 1
            if step_count % 10 == 0:
                logger.info(f"  Step {step_count}/{total_steps} Loss: {loss.item():.4f}")

    # Save
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info(f"✅ Saved {segment_name} to {output_dir}")

def main():
    # 1. Load Base
    logger.info(f"📦 Loading Base Model: {MODEL_NAME}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
        
        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, 
            torch_dtype=torch.float16, 
            device_map=DEVICE
        )
    except Exception as e:
        logger.error(f"Failed to load model {MODEL_NAME}: {e}")
        # Fallback to local 1.2B if 300M not found? Or just error.
        # Let's error so user can fix name.
        return

    # 2. Phase A: Resonance
    # Apply LoRA
    peft_config = LoraConfig(
        r=32, lora_alpha=64, 
        target_modules=["q_proj", "v_proj"], # Safe default for LLaMA-likes
        task_type=TaskType.CAUSAL_LM
    )
    model_v2 = get_peft_model(base_model, peft_config)
    model_v2.print_trainable_parameters()
    
    train_segment(
        model_v2, tokenizer, 
        "data/mini_resonance.jsonl", 
        "models/mini-lab/v2-resonance", 
        "v2 (Resonance)"
    )
    
    # 3. Phase B: Bimodal
    # We load v2 adapter, merge it (or stack it), then train v2b?
    # Actually, for simplicity in this script, let's just train ON TOP of the current weights.
    # But wait, `model_v2` is a PeftModel. If we continue training, we are updating the SAME adapter.
    # The user wants "Base -> v2" AND "v2 -> v2b".
    # So we have the v2 adapter saved.
    # Now we want to train v2b. We can continue training the SAME adapter on the NEW data.
    # This creates a "Cumulative" model. 
    # v2b will contain v2 knowledge. That's what we want.
    
    train_segment(
        model_v2, tokenizer,
        "data/mini_bimodal.jsonl",
        "models/mini-lab/v2b-bimodal",
        "v2b (Bimodal)"
    )

if __name__ == "__main__":
    main()
