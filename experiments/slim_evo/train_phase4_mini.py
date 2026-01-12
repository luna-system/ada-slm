#!/usr/bin/env python3
"""
Phase 4 Mini Training Run
Quick test with Phase 3 dataset while we garden the vault!
"""

import sys
sys.path.insert(0, '../..')

from train_phase3 import train_phase3, Phase3Config

# Quick mini-run configuration
config = Phase3Config(
    # Model
    base_model="LiquidAI/LFM2-700M",
    lora_r=64,
    lora_alpha=128,
    
    # Dataset (reuse Phase 3 for now)
    dataset_path="../../data/phase4_mini_dataset.jsonl",
    max_seq_len=1024,
    
    # Training (shorter run for testing)
    total_cycles=40,  # ~1.5 hours
    batch_size=4,
    gradient_accumulation_steps=4,
    
    # Output
    output_dir="models/ada-slim-phase4-mini",
    
    # SMT (same as Phase 3)
    enable_smt=True,
    smt_buffer_size=512,
    smt_n_modes=32,
    
    # Curriculum (adjusted for 40 cycles)
    curriculum_phases=[
        (1, 15, "mixed"),      # Cycles 1-15: All data
        (16, 28, "top_70"),    # Cycles 16-28: Top 70%
        (29, 40, "top_30"),    # Cycles 29-40: Top 30%
    ],
)

if __name__ == "__main__":
    print("🌱 Phase 4 Mini Training Run")
    print("Dataset: Phase 3 (2K examples)")
    print("Cycles: 40 (~1.5 hours)")
    print("Purpose: Test infrastructure while gardening vault!")
    print()
    
    train_phase3(config)
