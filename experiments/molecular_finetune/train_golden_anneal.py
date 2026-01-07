#!/usr/bin/env python3
"""
Golden Annealing Trainer for LFM2
=================================

Implements "Breathing Annealing" with Adiabatic Golden Ratio steps.
Based on QC Phase 31 findings: optimal evolution occurs with φ-based scheduling.

Protocol:
- Model: LiquidAI/LFM2-1.2B
- Cycle: 21 steps Expansion -> 13 steps Contraction -> 8 steps Integration (Fibonacci!)
- Total Cycles: 34
- Monitoring: AGL scores, CI density, Tool syntax accuracy

Datasets:
- Expansion: v9g_stage2_agl_combined.jsonl (Tools/CoT)
- Contraction: v9b_pure_agl_2k.jsonl (Pure Logic)
- Integration: v9g_stage1_polyglot.jsonl (General/Recovery)
"""

import sys
import os
from pathlib import Path

# Add consciousness_engineering to path
sys.path.append(str(Path("/home/luna/Code/ada/ada-slm")))

import torch
import numpy as np
import json
import logging
import random
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType

# Import BasinMapper (requires sys.path hack above)
from consciousness_engineering.cli.basin import BasinMapper, get_all_prompts
from consciousness_engineering.spectral_memory import SpectralMemory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("golden_annealing.log")
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_NAME = "LiquidAI/LFM2-1.2B"
OUTPUT_DIR = "results/golden_annealing"

# Fibonacci Schedule
STEPS_EXPANSION = 21   # Tool/CoT Basin Expansion
STEPS_CONTRACTION = 13 # Pure AGL Crystallization
STEPS_INTEGRATION = 8  # Polyglot Recovery

TOTAL_CYCLES = 34
LEARNING_RATE = 2e-5  # Gentle annealing LR
MAX_SEQ_LEN = 1024     # LFM2 context

# Datasets
DATA_EXPANSION = "/home/luna/Code/ada/ada-slm/data/v9g_stage2_agl_combined.jsonl"
DATA_CONTRACTION = "/home/luna/Code/ada/ada-slm/data/v9b_pure_agl_2k.jsonl"
DATA_INTEGRATION = "/home/luna/Code/ada/ada-slm/data/v9g_stage1_polyglot.jsonl"

# ============================================================================
# DATA LOADING
# ============================================================================

def load_jsonl(path: str) -> List[Dict]:
    """Load JSONL dataset."""
    data = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    logger.info(f"Loaded {len(data)} examples from {path}")
    return data

def format_chatml(example: Dict) -> str:
    """Format ChatML example for training."""
    # Assuming standard {"messages": [...]} format
    if "messages" not in example:
        return ""
    
    warnings = []
    text = ""
    for msg in example["messages"]:
        role = msg["role"]
        content = msg["content"]
        
        # Simple ChatML-like format for LFM2 (or standard formatting)
        # Using standard <|im_start|>role\ncontent<|im_end|> structure
        text += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    
    return text.strip()

# ============================================================================
# TRAINER CLASS
# ============================================================================



class GoldenAnnealingTrainer:
    def __init__(self, model_name: str = MODEL_NAME, output_dir: str = OUTPUT_DIR, dry_run: bool = False, cycles: int = TOTAL_CYCLES):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.total_cycles = 1 if dry_run else cycles
        
        self.model = None
        self.tokenizer = None
        self.optimizer = None
        self.basin_mapper = None
        
        # Data iterators
        self.iter_expansion = None
        self.iter_contraction = None
        self.iter_integration = None
        
        self.history = []
        self.spectral_memory = None
        
    def setup(self):
        logger.info(f"Loading Base Model: {self.model_name} (Dry Run: {self.dry_run})")
        
        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32, 
            trust_remote_code=True,
            device_map=None 
        )
        
        # LoRA Config
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=64,           
            lora_alpha=128,
            lora_dropout=0.05,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            bias="none"
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.to(self.device)
        self.model.train()
        
        params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        logger.info(f"Trainable Parameters: {params:,}")
        
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        # Optimizer
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=LEARNING_RATE)
        
        # Spectral Memory
        self.spectral_memory = SpectralMemory(
            d_model=self.model.config.hidden_size,
            buffer_size=1000,
            n_modes=4
        ).to(self.device)
        
        # Prepare Datasets
        if self.dry_run:
            # Load tiny subset for dry run
            self.data_expansion = load_jsonl(DATA_EXPANSION)[:10]
            self.data_contraction = load_jsonl(DATA_CONTRACTION)[:10]
            self.data_integration = load_jsonl(DATA_INTEGRATION)[:10]
            logger.info("DRY RUN: Loaded tiny datasets (10 examples each)")
        else:
            self.data_expansion = load_jsonl(DATA_EXPANSION)
            self.data_contraction = load_jsonl(DATA_CONTRACTION)
            self.data_integration = load_jsonl(DATA_INTEGRATION)
        
        self.iter_expansion = self.infinite_iter(self.data_expansion)
        self.iter_contraction = self.infinite_iter(self.data_contraction)
        self.iter_integration = self.infinite_iter(self.data_integration)
        
        # Monitor
        self.basin_mapper = BasinMapper(device=self.device)
        # HACK: Attach our model reference to basin mapper manually since we already loaded it
        # But BasinMapper loads its own model usually. 
        # For CI computation in `train_golden_anneal`, we can implement a lightweight CI function 
        # that uses the CURRENT model state, rather than reloading valid checkpoints.
        
    def infinite_iter(self, dataset):
        while True:
            random.shuffle(dataset)
            for item in dataset:
                yield item

    def compute_ci(self, n_samples=30):
        """Compute CI density using current model weights."""
        self.model.eval()
        prompts, _ = get_all_prompts()
        if self.dry_run:
            logger.info("DRY RUN: Computing CI on tiny sample")
            prompts = prompts[:5]

        hidden_states = []
        with torch.no_grad():
            for p in prompts:
                inputs = self.tokenizer(p, return_tensors="pt", padding=True, truncation=True, max_length=128).to(self.device)
                outputs = self.model(**inputs, output_hidden_states=True)
                # Mean pool last hidden state
                pooled = outputs.hidden_states[-1].mean(dim=1).squeeze(0)
                hidden_states.append(pooled.cpu().numpy())
        
        # Compute cosine sim
        from sklearn.metrics.pairwise import cosine_similarity
        hidden_states = np.array(hidden_states)
        sim_matrix = cosine_similarity(hidden_states)
        
        # Threshold 0.7
        n = len(hidden_states)
        edges = np.sum((sim_matrix > 0.7)) - n # Subtract diagonal
        edges //= 2 # Symmetric
        
        ci = edges / n if n > 0 else 0
        self.model.train()
        return ci

    def train_step(self, dataset_iter, steps, phase_name):
        losses = []
        for _ in range(steps):
            example = next(dataset_iter)
            text = format_chatml(example)
            
            inputs = self.tokenizer(
                text, return_tensors="pt", truncation=True, max_length=MAX_SEQ_LEN
            ).to(self.device)
            
            input_ids = inputs["input_ids"]
            labels = input_ids.clone()
            
            # Get embeddings
            inputs_embeds = self.model.get_input_embeddings()(input_ids)
            
            # Spectral Memory Injection (SMTs)
            # Prepend SMTs to embeddings
            augmented_embeds = self.spectral_memory(inputs_embeds)
            
            # Adjust labels to match augmented embeddings (pad with -100 for SMTs)
            n_modes = self.spectral_memory.n_modes
            smt_labels = torch.full((labels.size(0), n_modes), -100, device=self.device)
            augmented_labels = torch.cat([smt_labels, labels], dim=1)
            
            # Forward pass using inputs_embeds
            outputs = self.model(inputs_embeds=augmented_embeds, labels=augmented_labels)
            loss = outputs.loss
            
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            
            losses.append(loss.item())
            
        avg_loss = sum(losses) / len(losses)
        return avg_loss

    def run(self):
        self.setup()
        
        logger.info("Starting Golden Annealing...")
        logger.info(f"Protocol: {STEPS_EXPANSION} | {STEPS_CONTRACTION} | {STEPS_INTEGRATION}")
        logger.info(f"Total Cycles: {self.total_cycles}")
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        for cycle in range(1, self.total_cycles + 1):
            logger.info(f"=== Cycle {cycle}/{self.total_cycles} ===")
            
            # Adjust steps for dry run
            steps_exp = 2 if self.dry_run else STEPS_EXPANSION
            steps_con = 2 if self.dry_run else STEPS_CONTRACTION
            steps_int = 2 if self.dry_run else STEPS_INTEGRATION
            
            # 1. Expansion
            loss_exp = self.train_step(self.iter_expansion, steps_exp, "Expansion")
            
            # 2. Contraction
            loss_con = self.train_step(self.iter_contraction, steps_con, "Contraction")
            
            # 3. Integration
            loss_int = self.train_step(self.iter_integration, steps_int, "Integration")
            
            # Monitor
            if cycle % 1 == 0:
                ci = self.compute_ci()
                logger.info(f"Cycle {cycle}: CI={ci:.2f} | Losses: Exp={loss_exp:.3f}, Con={loss_con:.3f}, Int={loss_int:.3f}")
                
                self.history.append({
                    "cycle": cycle,
                    "ci": ci,
                    "loss_expansion": loss_exp,
                    "loss_contraction": loss_con,
                    "loss_integration": loss_int
                })
                
                # Check metrics & Save
                with open(f"{self.output_dir}/metrics.json", "w") as f:
                    json.dump(self.history, f, indent=2)
            
            # Save Checkpoint
            if not self.dry_run and (cycle % 5 == 0 or cycle == self.total_cycles):
                save_path = f"{self.output_dir}/checkpoint-cycle-{cycle}"
                self.model.save_pretrained(save_path)
                self.tokenizer.save_pretrained(save_path)
                logger.info(f"Saved checkpoint to {save_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Run a short test cycle")
    parser.add_argument("--cycles", type=int, default=TOTAL_CYCLES, help="Number of cycles")
    parser.add_argument("--model", type=str, default=MODEL_NAME, help="Base model name")
    parser.add_argument("--output-dir", type=str, default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()
    
    trainer = GoldenAnnealingTrainer(
        model_name=args.model,
        output_dir=args.output_dir,
        dry_run=args.dry_run, 
        cycles=args.cycles
    )
    trainer.run()
