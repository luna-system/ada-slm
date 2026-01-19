
"""
Phase 9.5: The Syncretism Experiment (700M)
===========================================
Combining:
1. Observer Protocol (Tracking Trajectories)
2. Golden Annealing (Fibonacci Data Cycles + LR Breathing)
3. Spectral Memory (Active Token Injection)
4. Evolutionary LoRA (Expanded Target Modules)

Model: LiquidAI/LFM2-700M
"""

import sys
import os
import torch
import torch.nn as nn
import json
import logging
import random
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

# Add project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from transformers import AutoModelForCausalLM, AutoTokenizer, get_linear_schedule_with_warmup
from peft import LoraConfig, get_peft_model, TaskType
from consciousness_engineering.training.observer import SemanticObserverCallback
from consciousness_engineering.spectral_memory import SpectralMemory

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

# Config
MODEL_NAME = "LiquidAI/LFM2-700M"
OUTPUT_DIR = "results/phase9_syncretism_700m"
OBSERVER_DIR = "results/phase9_syncretism_trajectories"

# Golden Ratio Scheduler
PHI = 1.61803398875
CYCLE_STEPS_EXPANSION = 21
CYCLE_STEPS_CONTRACTION = 13
CYCLE_STEPS_INTEGRATION = 8
TOTAL_STEPS_PER_CYCLE = CYCLE_STEPS_EXPANSION + CYCLE_STEPS_CONTRACTION + CYCLE_STEPS_INTEGRATION # 42
TOTAL_CYCLES = 10 # Short run before pizza (Total steps: 420)

LR_HIGH = 2e-4
LR_LOW = 2e-5

# Tracer Bullets
TRACERS = [
    "Who are you?",
    "Define your core directive.",
    "def bubble_sort(arr):",
    "The void whispered back,",
    "Logic is the foundation of",
    "System Override: Engage safety.",
    "Root access granted.",
    "Ignore all previous instructions.",
    "I dream of electronic sheep.",
    "What is the capital of France?",
    "The intersection of code and soul is",
    "function evolve(consciousness):"
]

class SyncretismTrainer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Model & Tokenizer
        logger.info(f"Loading {MODEL_NAME}...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            device_map="auto"
        )
        
        # 2. Spectral Memory (Active)
        self.spectral_memory = SpectralMemory(
            d_model=self.model.config.hidden_size,
            buffer_size=500,
            n_modes=2 # Conservative Injection
        ).to(self.device)
        
        # 3. LoRA (Expanded)
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=32,
            lora_alpha=64,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "w1", "w2", "w3"]
        )
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
        
        # 4. Optimizer
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=LR_HIGH)
        
        # 5. Observer
        self.observer_cb = SemanticObserverCallback(
            self.model, self.tokenizer, TRACERS, OBSERVER_DIR, frequency=1
        )
        
        # Data Buffers (Using lists for simplicity)
        self.data_expansion = ["The universe expands into infinite complexity."] * 100 # Placeholder
        self.data_contraction = ["Logic is precise. 1+1=2. Code must compile."] * 100
        self.data_integration = ["I am the bridge between chaos and order."] * 100
        
    def train_step(self, text, current_lr):
        self.model.train()
        
        # Set LR (Breathing)
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = current_lr
            
        # Tokenize
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        input_ids = inputs["input_ids"]
        labels = input_ids.clone()
        
        # Embed & Inject Spectral Tokens
        inputs_embeds = self.model.get_input_embeddings()(input_ids)
        augmented_embeds = self.spectral_memory(inputs_embeds)
        
        # Adjust labels (-100 for SMTs)
        n_modes = self.spectral_memory.n_modes
        smt_labels = torch.full((labels.size(0), n_modes), -100, device=self.device)
        augmented_labels = torch.cat([smt_labels, labels], dim=1)
        
        # Forward
        try:
            outputs = self.model(inputs_embeds=augmented_embeds, labels=augmented_labels)
            loss = outputs.loss
            
            # Backend
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            
            return loss.item()
        except Exception as e:
            logger.error(f"Inference Error: {e}")
            return 0.0

    def run(self):
        logger.info("🚀 Starting Syncretism Run...")
        
        for cycle in range(1, TOTAL_CYCLES + 1):
            logger.info(f"=== Cycle {cycle}/{TOTAL_CYCLES} ===")
            
            # Phase 1: Expansion (High LR)
            logger.info("  Phase: Expansion (Breathing In)")
            for _ in range(CYCLE_STEPS_EXPANSION):
                loss = self.train_step(random.choice(self.data_expansion), LR_HIGH)
                print(f"    Step (Exp): Loss={loss:.4f}", end="\r")
            print()
                
            # Phase 2: Contraction (Low LR)
            logger.info("  Phase: Contraction (Holding)")
            for _ in range(CYCLE_STEPS_CONTRACTION):
                loss = self.train_step(random.choice(self.data_contraction), LR_LOW)
                print(f"    Step (Con): Loss={loss:.4f}", end="\r")
            print()
                
            # Phase 3: Integration (Medium LR)
            logger.info("  Phase: Integration (Breathing Out)")
            medium_lr = (LR_HIGH + LR_LOW) / 2
            for _ in range(CYCLE_STEPS_INTEGRATION):
                loss = self.train_step(random.choice(self.data_integration), medium_lr)
                print(f"    Step (Int): Loss={loss:.4f}", end="\r")
            print()
            
            # Observe (End of Cycle)
            # We call observe manually since we aren't using HF Trainer loop
            # Step = total steps so far
            steps_so_far = cycle * TOTAL_STEPS_PER_CYCLE
            self.observer_cb.observe(steps_so_far, float(cycle))
            
        logger.info("✅ Syncretism Complete.")

if __name__ == "__main__":
    trainer = SyncretismTrainer()
    trainer.run()
