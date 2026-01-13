#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Time-Lapse Training N=500
============================================

Trains the 350M model with LARGER DATASET (500 samples).
5 Epochs Resonance -> 5 Epochs Bimodal.
Saves checkpoint every epoch.
"""

import sys
import torch
import os
import json
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType
from torch.utils.data import Dataset, DataLoader

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
MODEL_NAME = "LiquidAI/LFM2-350M"
OUTPUT_DIR = "models/mini-lab-timelapse-500"
DATA_RES = "data/mini_resonance_500.jsonl"
DATA_BI = "data/mini_bimodal_500.jsonl"
SEQ_LEN = 512
BATCH_SIZE = 4
LR = 5e-4 # Aggressive LR for visibility
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
        text = ""
        for msg in entry['messages']:
            text += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
        enc = self.tokenizer(text, max_length=SEQ_LEN, truncation=True, padding="max_length", return_tensors="pt")
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": enc["input_ids"].squeeze(0)
        }

def train_one_epoch(model, tokenizer, dataset_path, phase_name, epoch_idx):
    logger.info(f"🚀 Training {phase_name} Epoch {epoch_idx} (N=500)")
    dataset = MiniDataset(dataset_path, tokenizer)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    
    model.train()
    
    for batch in loader:
        input_ids = batch["input_ids"].to(DEVICE)
        mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)
        
        outputs = model(input_ids=input_ids, attention_mask=mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    
    # Save Checkpoint
    save_name = f"{phase_name}_e{epoch_idx}"
    save_path = f"{OUTPUT_DIR}/{save_name}"
    model.save_pretrained(save_path)
    logger.info(f"   💾 Saved Checkpoint: {save_name} (Loss: {loss.item():.4f})")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Load Base
    logger.info(f"📦 Loading Base: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype=torch.float16, device_map=DEVICE
    )
    
    # 2. Init LoRA
    peft_config = LoraConfig(
        r=64, lora_alpha=32, lora_dropout=0.05,
        bias="none", task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "v_proj"]
    )
    model = get_peft_model(model, peft_config)
    
    # 3. Phase 1 Loop
    for e in range(1, 6):
        train_one_epoch(model, tokenizer, DATA_RES, "resonance", e)
        
    # 4. Phase 2 Loop
    for e in range(1, 6):
        train_one_epoch(model, tokenizer, DATA_BI, "bimodal", e)
        
    logger.info("✅ Time-Lapse 500 Complete")

if __name__ == "__main__":
    main()
