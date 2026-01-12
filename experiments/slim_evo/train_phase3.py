#!/usr/bin/env python3
"""
SLIM-EVO Phase 3 Trainer
========================

Unified training script for Ada-Slim 0.7B with:
- Golden Annealing (Fibonacci-step cosine LR schedule)
- Spectral Memory Tokens (progressive injection, SPEAR-inspired)
- PCMind Multi-Domain Curriculum (3 phases)
- AGL-First Dataset (💭 pixie dust reasoning traces)

Based on:
- SLIM-EVO-PHASE3-PLAN.md
- SPEAR-PCMIND-SYNTHESIS.md
- SCOPE-SYNTHESIS.md (hierarchical planning)

Model: LiquidAI/LFM2-700M (0.7B parameters)
Dataset: phase3_full_dataset.jsonl (2000 examples, 27 templates)
Total Cycles: 34 (Fibonacci sequence)
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
import math
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer, get_cosine_schedule_with_warmup
from peft import get_peft_model, LoraConfig, TaskType
from torch.utils.data import Dataset, DataLoader

# Import consciousness engineering tools
from consciousness_engineering.spectral_memory import SpectralMemory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("phase3_training.log")
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Phase3Config:
    """Configuration for Phase 3 training."""
    
    # Model
    base_model: str = "LiquidAI/LFM2-700M"
    lora_r: int = 32
    lora_alpha: int = 64
    lora_dropout: float = 0.05
    
    # Dataset
    dataset_path: str = "data/phase3_full_dataset.jsonl"
    max_seq_len: int = 1024
    
    # Golden Annealing
    total_cycles: int = 34  # Fibonacci number
    base_lr: float = 3e-4
    min_lr: float = 1e-5
    warmup_steps: int = 100
    
    # Spectral Memory (SPEAR-inspired)
    enable_smt: bool = True
    smt_buffer_size: int = 512
    smt_num_tokens: int = 32
    smt_projection_dim: int = 1024  # LFM2-700M hidden size
    smt_positive_advantage: bool = True  # Only store high-CI states
    smt_progressive_injection: bool = True  # Weight increases with cycle
    
    # PCMind Curriculum (3 phases)
    curriculum_phases: List[Tuple[int, int, str]] = field(default_factory=lambda: [
        (1, 10, "mixed"),      # Cycles 1-10: All data
        (11, 20, "top_70"),    # Cycles 11-20: Top 70% by quality
        (21, 34, "top_30"),    # Cycles 21-34: Top 30% by quality
    ])
    
    # Training
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    max_grad_norm: float = 1.0
    
    # Checkpointing
    output_dir: str = "models/ada-slim-phase3"
    checkpoint_every: int = 10
    
    # Device
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================================
# DATASET
# ============================================================================

class Phase3Dataset(Dataset):
    """Phase 3 AGL-first dataset with quality filtering."""
    
    def __init__(self, data_path: str, tokenizer, max_length: int = 1024, quality_filter: str = "mixed"):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.quality_filter = quality_filter
        
        # Load data
        self.examples = self._load_jsonl(data_path)
        
        # Apply quality filtering (PCMind curriculum)
        self.examples = self._apply_quality_filter(self.examples, quality_filter)
        
        logger.info(f"Loaded {len(self.examples)} examples (filter: {quality_filter})")
    
    def _load_jsonl(self, path: str) -> List[Dict]:
        """Load JSONL dataset."""
        data = []
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return data
    
    def _apply_quality_filter(self, examples: List[Dict], filter_type: str) -> List[Dict]:
        """Apply PCMind-style quality filtering."""
        if filter_type == "mixed":
            return examples  # Use all data
        
        # Compute quality scores (based on category from metadata)
        quality_scores = []
        for ex in examples:
            category = ex.get("metadata", {}).get("category", "unknown")
            # Quality tiers (from phase3.py selective repetition)
            quality_map = {
                "self_evolving": 3,
                "process_supervised": 2,
                "tool_use": 2,
                "consciousness": 2,
                "code_to_agl": 1,
            }
            quality_scores.append(quality_map.get(category, 1))
        
        # Sort by quality
        sorted_indices = np.argsort(quality_scores)[::-1]  # Descending
        
        if filter_type == "top_70":
            cutoff = int(len(examples) * 0.7)
            selected_indices = sorted_indices[:cutoff]
        elif filter_type == "top_30":
            cutoff = int(len(examples) * 0.3)
            selected_indices = sorted_indices[:cutoff]
        else:
            selected_indices = sorted_indices
        
        return [examples[i] for i in selected_indices]
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # Format as ChatML
        messages = example.get("messages", [])
        text = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            text += f"<|im_start|>{role}\n{content}<|im_end|>\n"
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": encoding["input_ids"].squeeze(0),
        }


# ============================================================================
# GOLDEN ANNEALING SCHEDULER
# ============================================================================

def get_fibonacci_sequence(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms."""
    fib = [1, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib[:n]


def create_golden_annealing_schedule(optimizer, num_cycles: int, steps_per_cycle: int, base_lr: float, min_lr: float):
    """Create Fibonacci-step cosine annealing schedule."""
    total_steps = num_cycles * steps_per_cycle
    
    def lr_lambda(current_step):
        # Cosine annealing with Fibonacci-based modulation
        cycle = current_step // steps_per_cycle
        progress = (current_step % steps_per_cycle) / steps_per_cycle
        
        # Cosine decay
        cosine_decay = 0.5 * (1 + math.cos(math.pi * progress))
        
        # Fibonacci modulation (φ-zone optimization)
        phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        fib_mod = 1.0 / (1 + cycle / phi)  # Decay with golden ratio
        
        # Combined LR
        lr_scale = min_lr + (base_lr - min_lr) * cosine_decay * fib_mod
        return lr_scale / base_lr  # Return as ratio
    
    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


# ============================================================================
# CI DENSITY COMPUTATION
# ============================================================================

def compute_ci_density(hidden_states: torch.Tensor) -> float:
    """
    Compute CI (Consciousness Index) density from hidden states.
    
    Simplified version: measures information integration via correlation.
    Handles edge cases (NaN, insufficient data) gracefully.
    """
    try:
        # hidden_states: (batch, seq_len, hidden_dim)
        batch_size, seq_len, hidden_dim = hidden_states.shape
        
        # Need at least 2 samples for correlation
        if batch_size * seq_len < 2:
            return 0.0
        
        # Flatten batch and sequence
        flat_states = hidden_states.reshape(-1, hidden_dim)  # (batch*seq, hidden)
        
        # Remove any NaN or Inf values
        if torch.isnan(flat_states).any() or torch.isinf(flat_states).any():
            flat_states = torch.nan_to_num(flat_states, nan=0.0, posinf=1.0, neginf=-1.0)
        
        # Check for zero variance (would cause NaN in corrcoef)
        if flat_states.std() < 1e-8:
            # Fallback: use simple variance as integration measure
            return flat_states.var().item()
        
        # Compute correlation matrix (can still fail with FP16)
        try:
            corr_matrix = torch.corrcoef(flat_states.T)  # (hidden, hidden)
            
            # Check for NaN in result
            if torch.isnan(corr_matrix).any():
                # Fallback: use variance-based measure
                return flat_states.var().item()
            
            # CI ≈ mean absolute correlation (integration measure)
            ci = torch.abs(corr_matrix).mean().item()
            
            # Sanity check
            if math.isnan(ci) or math.isinf(ci):
                return flat_states.var().item()
            
            return ci
            
        except RuntimeError:
            # torch.corrcoef can fail with FP16 or small matrices
            # Fallback: use variance as integration proxy
            return flat_states.var().item()
    
    except Exception as e:
        # Ultimate fallback
        logger.warning(f"CI computation failed: {e}, returning 0.0")
        return 0.0



# ============================================================================
# TRAINING LOOP
# ============================================================================

def train_phase3(config: Phase3Config):
    """Main Phase 3 training loop."""
    
    logger.info("=" * 80)
    logger.info("SLIM-EVO PHASE 3 TRAINING")
    logger.info("=" * 80)
    logger.info(f"Model: {config.base_model}")
    logger.info(f"Dataset: {config.dataset_path}")
    logger.info(f"Total Cycles: {config.total_cycles}")
    logger.info(f"Spectral Memory: {'ENABLED' if config.enable_smt else 'DISABLED'}")
    logger.info("=" * 80)
    
    # Load model and tokenizer
    logger.info("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(config.base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.float16 if config.device == "cuda" else torch.float32,
        device_map=config.device
    )
    
    # Apply LoRA
    logger.info("Applying LoRA...")
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        task_type=TaskType.CAUSAL_LM
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Initialize Spectral Memory (if enabled)
    spectral_memory = None
    if config.enable_smt:
        logger.info("Initializing Spectral Memory...")
        spectral_memory = SpectralMemory(
            d_model=config.smt_projection_dim,  # 1024 for LFM2-700M
            buffer_size=config.smt_buffer_size,  # 512
            n_modes=config.smt_num_tokens  # 32
        )
    
    # Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.base_lr)
    
    # Training metrics
    metrics = {
        "cycle": [],
        "loss": [],
        "ci_density": [],
        "lr": [],
    }
    
    # Training loop
    steps_per_cycle = 50  # Adjust based on dataset size
    
    for cycle in range(1, config.total_cycles + 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"CYCLE {cycle}/{config.total_cycles}")
        logger.info(f"{'='*80}")
        
        # Determine curriculum phase
        quality_filter = "mixed"
        for start, end, filter_type in config.curriculum_phases:
            if start <= cycle <= end:
                quality_filter = filter_type
                break
        
        logger.info(f"Curriculum: {quality_filter}")
        
        # Load dataset for this cycle
        dataset = Phase3Dataset(
            config.dataset_path,
            tokenizer,
            max_length=config.max_seq_len,
            quality_filter=quality_filter
        )
        
        dataloader = DataLoader(
            dataset,
            batch_size=config.batch_size,
            shuffle=True
        )
        
        # Create scheduler for this cycle
        scheduler = create_golden_annealing_schedule(
            optimizer,
            num_cycles=config.total_cycles,
            steps_per_cycle=steps_per_cycle,
            base_lr=config.base_lr,
            min_lr=config.min_lr
        )
        
        # Training steps for this cycle
        model.train()
        cycle_loss = 0.0
        cycle_ci = 0.0
        num_batches = 0
        
        for step, batch in enumerate(dataloader):
            if step >= steps_per_cycle:
                break
            
            # Move to device
            input_ids = batch["input_ids"].to(config.device)
            attention_mask = batch["attention_mask"].to(config.device)
            labels = batch["labels"].to(config.device)
            
            # Forward pass
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels,
                output_hidden_states=True
            )
            
            loss = outputs.loss
            hidden_states = outputs.hidden_states[-1]  # Last layer
            
            # Compute CI density
            ci_density = compute_ci_density(hidden_states)
            
            # Update Spectral Memory (if enabled)
            if spectral_memory and config.smt_positive_advantage:
                # Only store high-CI states (SPEAR positive advantage)
                if ci_density > 0.25:  # Threshold (can tune)
                    spectral_memory.update(hidden_states.detach().cpu())
            
            # Backward pass
            loss.backward()
            
            if (step + 1) % config.gradient_accumulation_steps == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
            
            # Metrics
            cycle_loss += loss.item()
            cycle_ci += ci_density
            num_batches += 1
            
            if step % 10 == 0:
                logger.info(f"  Step {step}/{steps_per_cycle} | Loss: {loss.item():.4f} | CI: {ci_density:.4f} | LR: {scheduler.get_last_lr()[0]:.2e}")
        
        # Cycle metrics
        avg_loss = cycle_loss / num_batches
        avg_ci = cycle_ci / num_batches
        
        metrics["cycle"].append(cycle)
        metrics["loss"].append(avg_loss)
        metrics["ci_density"].append(avg_ci)
        metrics["lr"].append(scheduler.get_last_lr()[0])
        
        logger.info(f"\nCycle {cycle} Summary:")
        logger.info(f"  Avg Loss: {avg_loss:.4f}")
        logger.info(f"  Avg CI Density: {avg_ci:.4f}")
        logger.info(f"  Learning Rate: {scheduler.get_last_lr()[0]:.2e}")
        
        # Checkpoint
        if cycle % config.checkpoint_every == 0:
            checkpoint_dir = Path(config.output_dir) / f"checkpoint-cycle-{cycle}"
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            
            model.save_pretrained(checkpoint_dir)
            tokenizer.save_pretrained(checkpoint_dir)
            
            # Save metrics
            with open(checkpoint_dir / "metrics.json", "w") as f:
                json.dump(metrics, f, indent=2)
            
            logger.info(f"✅ Checkpoint saved: {checkpoint_dir}")
    
    # Final save
    final_dir = Path(config.output_dir) / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    
    with open(final_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    logger.info(f"\n{'='*80}")
    logger.info("TRAINING COMPLETE!")
    logger.info(f"Final model saved: {final_dir}")
    logger.info(f"{'='*80}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SLIM-EVO Phase 3 Training")
    parser.add_argument("--model", type=str, default="LiquidAI/LFM2-700M", help="Base model")
    parser.add_argument("--dataset", type=str, default="data/phase3_full_dataset.jsonl", help="Dataset path")
    parser.add_argument("--cycles", type=int, default=34, help="Total training cycles")
    parser.add_argument("--output-dir", type=str, default="models/ada-slim-phase3", help="Output directory")
    parser.add_argument("--no-smt", action="store_true", help="Disable Spectral Memory")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (1 cycle only)")
    
    args = parser.parse_args()
    
    config = Phase3Config(
        base_model=args.model,
        dataset_path=args.dataset,
        total_cycles=1 if args.dry_run else args.cycles,
        output_dir=args.output_dir,
        enable_smt=not args.no_smt,
    )
    
    train_phase3(config)
