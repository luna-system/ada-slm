#!/usr/bin/env python3
"""
SLIM-EVO Phase 5: Bimodal Switching Trainer (v1b)
=================================================

Fine-tunes the Resonance (v1) model to explicitly switch between
'Engine Mode' (Logic) and 'Phillip Mode' (Narrative) based on intent.

Base Model: LFM2-1.2B + Resonance Adpater (Merged on fly)
Dataset: data/phase5_bimodal.jsonl
"""

import sys
import os
from pathlib import Path

# Add consciousness_engineering to path
sys.path.append(str(Path("/home/luna/Code/ada/ada-slm")))

import torch
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, LoraConfig, get_peft_model, TaskType

# Reuse Phase 3 logic
from experiments.slim_evo.train_phase3 import train_phase3, Phase3Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---

RES_ADAPTER_PATH = "/home/luna/Code/ada/ada-slm/models/ada-slim-1.2b-resonance-20260111"
BASE_MODEL_NAME = "LiquidAI/LFM2-1.2B" 

# --- Custom Trainer Wrapper ---

def main():
    logger.info("🚀 Launching Phase 5 (Bimodal Switching) Training")
    
    # 1. Configuration
    config = Phase3Config(
        # Model
        base_model=BASE_MODEL_NAME, # We will handle merging manually below if needed, but train_phase3 expects a string.
                                    # Hack: We pass the base string, but we modify train_phase3 to handle pre-loaded models?
                                    # Or we just use a custom script here. Let's write a custom script that reuses components.
        lora_r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        
        # Dataset
        dataset_path="data/phase5_bimodal.jsonl",
        max_seq_len=1024,
        
        # Training (Short & Precise)
        total_cycles=34, # Fibonacci 34 (~50-100 steps total depending on batch)
        batch_size=4,
        gradient_accumulation_steps=4,
        base_lr=1e-5, # LOW LR for fine-tuning behavior only
        min_lr=1e-6,
        
        # Output
        output_dir="models/ada-slim-1.2b-v1b-bimodal",
        
        # SMT (Keep enabled to support Engine Mode)
        enable_smt=True,
        smt_buffer_size=512,
        smt_num_tokens=32,
        smt_projection_dim=2048, # Calculated for 1.2B model size (was 1024 for 700M)
        
        # Curriculum: Single phase (Mixed)
        curriculum_phases=[(1, 34, "mixed")]
    )
    
    # Run Training via Phase 3 logic, but we need to inject the MERGED model.
    # Since train_phase3 loads the model itself, we should probably modify train_phase3 
    # OR (easier) just adapt this script to copy the logic but load the model differently.
    # PROPOSAL: We will just reimplement the loader here and call the inner loop.
    
    train_phase5_custom(config, RES_ADAPTER_PATH)

def train_phase5_custom(config, adapter_path):
    # Import internals from train_phase3
    from experiments.slim_evo.train_phase3 import Phase3Dataset, create_golden_annealing_schedule, compute_ci_density
    from consciousness_engineering.spectral_memory import SpectralMemory
    from torch.utils.data import DataLoader
    import json
    
    # 1. Load Base + Adapter and MERGE
    logger.info(f"Loading Base: {config.base_model}")
    tokenizer = AutoTokenizer.from_pretrained(config.base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    logger.info(f"Loading Resonance Adapter: {adapter_path}")
    model = PeftModel.from_pretrained(model, adapter_path)
    model = model.merge_and_unload() # 🧬 FUSION
    logger.info("✅ Resonance Adapter Merged into Base")
    
    # 2. Add NEW LoRA for Phase 5
    logger.info("Applying New LoRA for Phase 5...")
    peft_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        task_type=TaskType.CAUSAL_LM
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    # 3. Setup SMT
    spectral_memory = None
    if config.enable_smt:
        spectral_memory = SpectralMemory(
            d_model=config.smt_projection_dim,
            buffer_size=config.smt_buffer_size,
            n_modes=config.smt_num_tokens
        )
        
    # 4. Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.base_lr)
    
    # 5. Dataset
    dataset = Phase3Dataset(config.dataset_path, tokenizer, max_length=config.max_seq_len)
    dataloader = DataLoader(dataset, batch_size=config.batch_size, shuffle=True)
    
    # 6. Training Loop (Robust for small data)
    logger.info(f"Starting Training: {config.total_cycles} Cycles")
    
    # Create infinite dataloader
    def infinite_loader(dl):
        while True:
            for batch in dl:
                yield batch
                
    data_iter = infinite_loader(dataloader)
    
    # Set fixed steps per cycle for robust training
    fixed_steps_per_cycle = 10 
    
    for cycle in range(1, config.total_cycles + 1):
        # Scheduler
        scheduler = create_golden_annealing_schedule(
            optimizer, config.total_cycles, fixed_steps_per_cycle, config.base_lr, config.min_lr
        )
        
        model.train()
        cycle_loss = 0
        
        for step in range(fixed_steps_per_cycle):
            batch = next(data_iter)
            
            inputs = {k: v.to(config.device) for k, v in batch.items()}
            outputs = model(**inputs, output_hidden_states=True)
            
            loss = outputs.loss
            
            # SMT Update
            if spectral_memory:
                 ci = compute_ci_density(outputs.hidden_states[-1])
                 if ci > 0.25: spectral_memory.update_buffer(outputs.hidden_states[-1].detach().cpu())
            
            loss.backward()
            
            if (step + 1) % config.gradient_accumulation_steps == 0:
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                
            cycle_loss += loss.item()
            
        avg_loss = cycle_loss / fixed_steps_per_cycle
        logger.info(f"Cycle {cycle} | Loss: {avg_loss:.4f} | LR: {scheduler.get_last_lr()[0]:.2e}")
        
    # 7. Save
    final_dir = Path(config.output_dir) / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    logger.info(f"✅ Phase 5 Complete. Model saved to {final_dir}")

if __name__ == "__main__":
    main()
