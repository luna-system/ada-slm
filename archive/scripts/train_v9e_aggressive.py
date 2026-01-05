#!/usr/bin/env python3
"""
V9E Aggressive Capacity Test Training
======================================

Push LoRA capacity even higher to test if more capacity = more consciousness.

Changes from v9C:
- LoRA r: 32 → 48 (50% increase!)
- LoRA α: 64 → 96 (matched ratio)
- batch_size: 1, grad_accum: 16 (proven regularization)

From v9D isolation results:
- Capacity (r=32) alone gave 60x improvement
- Let's see if r=48 gives even more!
"""

import os
import sys
import json
import time
import torch
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any

# ROCm/CUDA setup
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")


@dataclass
class TrainingConfig:
    """V9E Aggressive - PUSH CAPACITY HIGHER!"""
    # Model
    base_model: str = "LiquidAI/LFM2-350M"
    
    # Dataset (SAME as v9C - controlled experiment!)
    dataset_path: str = "data/v9b_pure_agl_2k.jsonl"
    
    # Training (proven config from v9C)
    max_seq_length: int = 1024
    batch_size: int = 1          # Proven regularization benefit
    gradient_accumulation_steps: int = 16  # Effective batch 16
    num_epochs: int = 3
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    
    # LoRA - PUSHED HIGHER!
    lora_r: int = 48       # Was 32 in v9C (50% increase!)
    lora_alpha: int = 96   # Maintain 2:1 ratio with r
    lora_dropout: float = 0.05
    
    # Output
    output_dir: str = "exports/v9e_aggressive"


def load_dataset(config: TrainingConfig) -> list:
    """Load the v9b_pure dataset (same as v9C for controlled comparison)."""
    print(f"📊 Loading dataset from {config.dataset_path}...")
    
    dataset_path = Path(config.dataset_path)
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        print("💡 Run: python generate_v9b_pure.py")
        sys.exit(1)
    
    examples = []
    phase_counts = {}
    
    with open(dataset_path) as f:
        for line in f:
            data = json.loads(line)
            examples.append(data)
            phase = data.get("phase", "unknown")
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    print(f"✅ Loaded {len(examples)} examples")
    for phase, count in sorted(phase_counts.items()):
        print(f"   {phase}: {count}")
    
    return examples


def format_for_training(examples: list, tokenizer) -> list:
    """Format examples for causal LM training."""
    formatted = []
    
    for ex in examples:
        if "messages" in ex:
            # Chat format
            text = tokenizer.apply_chat_template(
                ex["messages"],
                tokenize=False,
                add_generation_prompt=False
            )
        elif "instruction" in ex and "output" in ex:
            # Instruction format
            text = f"### Instruction:\n{ex['instruction']}\n\n### Response:\n{ex['output']}"
        else:
            continue
        
        formatted.append({"text": text})
    
    return formatted


def main():
    from transformers import (
        AutoModelForCausalLM, 
        AutoTokenizer,
        TrainingArguments,
        Trainer,
        DataCollatorForLanguageModeling
    )
    from peft import LoraConfig, get_peft_model, TaskType
    from datasets import Dataset
    
    print("="*70)
    print("🚀 V9E AGGRESSIVE CAPACITY TEST")
    print("   LoRA r=48, α=96 (50% more capacity than v9C!)")
    print("   batch=1, grad_accum=16 (proven regularization)")
    print("="*70)
    
    config = TrainingConfig()
    start_time = time.time()
    
    # Load tokenizer and model
    print(f"\n📦 Loading {config.base_model}...")
    tokenizer = AutoTokenizer.from_pretrained(config.base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # LoRA configuration - PUSHED TO r=48!
    print(f"\n🔧 Configuring LoRA (r={config.lora_r}, α={config.lora_alpha})...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)
    trainable, total = model.get_nb_trainable_parameters()
    print(f"   Trainable: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)")
    
    # Load and format dataset
    examples = load_dataset(config)
    formatted = format_for_training(examples, tokenizer)
    dataset = Dataset.from_list(formatted)
    
    # Tokenize
    print("\n🔤 Tokenizing dataset...")
    def tokenize(example):
        return tokenizer(
            example["text"],
            truncation=True,
            max_length=config.max_seq_length,
            padding=False
        )
    
    tokenized = dataset.map(tokenize, remove_columns=["text"], num_proc=4)
    
    # Training arguments
    output_path = Path(config.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    training_args = TrainingArguments(
        output_dir=str(output_path),
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=10,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=2,
        bf16=True,
        optim="adamw_torch",
        report_to=[],  # Disable wandb etc
        dataloader_num_workers=0,
        remove_unused_columns=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    
    # Train!
    print("\n" + "="*70)
    print("🏋️ TRAINING V9E-AGGRESSIVE (r=48, batch=1)")
    print("="*70 + "\n")
    
    result = trainer.train()
    
    # Save
    final_path = output_path / "final_model"
    print(f"\n💾 Saving to {final_path}...")
    trainer.save_model(str(final_path))
    tokenizer.save_pretrained(str(final_path))
    
    # Summary
    elapsed = time.time() - start_time
    summary = {
        "experiment": "v9e_aggressive",
        "description": "Push capacity to r=48 (50% more than v9C)",
        "config": {
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
            "batch_size": config.batch_size,
            "grad_accum": config.gradient_accumulation_steps,
            "epochs": config.num_epochs
        },
        "results": {
            "final_loss": result.training_loss,
            "training_time_minutes": elapsed / 60,
            "trainable_params": trainable
        },
        "timestamp": datetime.now().isoformat()
    }
    
    summary_path = output_path / "training_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*70)
    print("✅ V9E-AGGRESSIVE COMPLETE!")
    print(f"   Final Loss: {result.training_loss:.4f}")
    print(f"   Training Time: {elapsed/60:.1f} minutes")
    print(f"   Model saved to: {final_path}")
    print("="*70)
    print("\n🔬 To evaluate:")
    print(f"   python test_v9b_multilang.py --model v9e --languages english agl")


if __name__ == "__main__":
    main()
