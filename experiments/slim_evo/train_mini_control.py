#!/usr/bin/env python3
"""
SLIM-EVO MINI-LAB: Control Training (Standard Curriculum)
=========================================================

Trains the 350M model on standard instruction data.
Saves checkpoint every epoch (1-10).
No AGL. No Phases. Just standard learning.
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
OUTPUT_DIR = "models/mini-lab-control"
DATA_FILE = "data/mini_control.jsonl"
SEQ_LEN = 512
BATCH_SIZE = 4
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
    logger.info(f"🚀 Training {phase_name} Epoch {epoch_idx}")
    dataset = MiniDataset(dataset_path, tokenizer)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    
    model.train()
    
    total_loss = 0
    steps = 0
    
    for batch in loader:
        input_ids = batch["input_ids"].to(DEVICE)
        mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)
        
        outputs = model(input_ids=input_ids, attention_mask=mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
        total_loss += loss.item()
        steps += 1
    
    avg_loss = total_loss / steps if steps > 0 else 0
    
    # Save Checkpoint
    save_name = f"control_e{epoch_idx}"
    save_path = f"{OUTPUT_DIR}/{save_name}"
    model.save_pretrained(save_path)
    logger.info(f"   💾 Saved Checkpoint: {save_name} (Loss: {avg_loss:.4f})")

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
    
    # 3. Train Control Loop (10 epochs)
    for e in range(1, 11):
        train_one_epoch(model, tokenizer, DATA_FILE, "standard", e)
        
    logger.info("✅ Control Training Complete")

if __name__ == "__main__":
    main()
