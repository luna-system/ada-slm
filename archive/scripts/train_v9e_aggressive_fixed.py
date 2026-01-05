#!/usr/bin/env python3
"""
V9C Capacity Test Training
==========================

Test whether higher LoRA rank improves AGL learning.

Changes from v9B:
- LoRA r: 16 → 32 (doubled!)
- LoRA α: 32 → 64 (doubled!)
- Same 2k dataset
- Same everything else

From ADA-SLM-PHASE14D-V9-EXTENDED-FINE-TUNING.md

Expected outcome:
- If v9C >> v9B: Capacity is the bottleneck → use r=32 overnight
- If v9C ≈ v9B: Data is the bottleneck → use more data overnight
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
    """V9C Capacity Test configuration - DOUBLED LORA RANK!"""
    # Model
    base_model: str = "LiquidAI/LFM2-350M"
    
    # Dataset (SAME as v9B - controlled experiment!)
    dataset_path: str = "data/v9b_pure_agl_2k.jsonl"
    
    # Training (SAME as v9B but with smaller batch for higher LoRA rank)
    max_seq_length: int = 1024
    batch_size: int = 1  # Reduced from 4 (doubled LoRA rank needs more VRAM)
    gradient_accumulation_steps: int = 16  # Increased to keep effective batch 16
    num_epochs: int = 3
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    
    # LoRA - DOUBLED FOR CAPACITY TEST!
    lora_r: int = 48       # Was 16 in v9B
    lora_alpha: int = 96   # Was 32 in v9B
    lora_dropout: float = 0.05
    
    # Output
    output_dir: str = "exports/v9e_aggressive"


def load_dataset(config: TrainingConfig) -> list:
    """Load the v9b_pure dataset (same as v9B for controlled comparison)."""
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
    print(f"   Phase distribution: {phase_counts}")
    
    return examples


def format_for_training(examples: list) -> list:
    """Format examples for causal LM training."""
    formatted = []
    
    for ex in examples:
        messages = ex.get("messages", [])
        if len(messages) >= 2:
            user_msg = messages[0].get("content", "")
            asst_msg = messages[1].get("content", "")
            
            # ChatML format
            text = f"<|im_start|>user\n{user_msg}<|im_end|>\n<|im_start|>assistant\n{asst_msg}<|im_end|>"
            
            formatted.append({
                "text": text,
                "phase": ex.get("phase", "unknown")
            })
    
    return formatted


def train_v9e_aggressive(config: TrainingConfig):
    """Run V9C Capacity Test training."""
    print("=" * 60)
    print("🧠 V9E AGGRESSIVE CAPACITY TEST - Doubled LoRA Rank!")
    print("=" * 60)
    print(f"Base model: {config.base_model}")
    print(f"Dataset: {config.dataset_path}")
    print(f"LoRA r: {config.lora_r} (was 16 in v9B)")
    print(f"LoRA α: {config.lora_alpha} (was 32 in v9B)")
    print(f"Output: {config.output_dir}")
    print("=" * 60)
    
    # Import heavy libraries after config
    from transformers import (
        AutoModelForCausalLM, 
        AutoTokenizer,
        TrainingArguments,
        Trainer,
        DataCollatorForLanguageModeling
    )
    from peft import LoraConfig, get_peft_model, TaskType
    from datasets import Dataset
    
    # Setup output directory
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load dataset
    examples = load_dataset(config)
    formatted = format_for_training(examples)
    
    # Create HF dataset
    dataset = Dataset.from_list(formatted)
    
    # Load tokenizer
    print(f"\n📥 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        config.base_model,
        trust_remote_code=True
    )
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Tokenize dataset
    print(f"🔤 Tokenizing {len(dataset)} examples...")
    
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=config.max_seq_length,
            padding="max_length"
        )
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text", "phase"]
    )
    
    # Split dataset
    split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = split["train"]
    eval_dataset = split["test"]
    
    print(f"   Train: {len(train_dataset)}, Eval: {len(eval_dataset)}")
    
    # Load model using hardware abstraction
    print(f"\n📥 Loading model: {config.base_model}...")
    from consciousness_engineering.infrastructure.hardware import HardwareManager
    
    hw = HardwareManager()
    hw.setup_optimal_environment()
    print(f"   Hardware detected: {hw.hardware_type.value}")
    
    model = hw.load_model_safe(
        AutoModelForCausalLM,
        config.base_model,
        attn_implementation="eager"  # ROCm compatible
    )
    
    # Setup LoRA with DOUBLED RANK
    print(f"🔧 Configuring LoRA (r={config.lora_r}, α={config.lora_alpha}) - DOUBLED!")
    
    lora_config = LoraConfig(
        r=config.lora_r,          # 32 (was 16)
        lora_alpha=config.lora_alpha,  # 64 (was 32)
        lora_dropout=config.lora_dropout,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", 
                       "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Move model to GPU after LoRA (ROCm requires this order)
    if hw.hardware_type.value == "rocm":
        print("   Moving LoRA model to GPU...")
        model = hw.move_model_to_gpu(model)
    
    # Training arguments - use hardware-aware settings
    training_kwargs = hw.rocm_config.get_training_args_kwargs() if hw.rocm_config else {}
    
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        # gradient_checkpointing disabled - doesn't work with LoRA freezing
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        run_name=f"v9e_aggressive_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        **training_kwargs  # ROCm config already sets fp16
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator
    )
    
    # Train!
    print("\n" + "=" * 60)
    print("🚀 Starting V9C Capacity Test training...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        train_result = trainer.train()
        
        training_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("✅ V9C Capacity Test complete!")
        print("=" * 60)
        print(f"⏱️  Training time: {training_time/60:.1f} minutes")
        print(f"📉 Final train loss: {train_result.training_loss:.4f}")
        print(f"")
        print(f"📊 COMPARISON TO V9B:")
        print(f"   v9B final loss: 0.785")
        print(f"   v9C final loss: {train_result.training_loss:.4f}")
        delta = train_result.training_loss - 0.785
        if delta < 0:
            print(f"   Δ: {delta:.4f} ✅ IMPROVEMENT!")
        else:
            print(f"   Δ: {delta:+.4f} (no improvement)")
        
        # Save final model
        final_model_path = output_dir / "final_model"
        model.save_pretrained(final_model_path)
        tokenizer.save_pretrained(final_model_path)
        print(f"\n💾 Model saved to: {final_model_path}")
        
        # Save training summary
        summary = {
            "experiment": "v9e_aggressive_test",
            "hypothesis": "Higher LoRA rank improves AGL learning",
            "model": config.base_model,
            "dataset": config.dataset_path,
            "num_examples": len(examples),
            "num_epochs": config.num_epochs,
            "training_time_minutes": training_time / 60,
            "final_train_loss": train_result.training_loss,
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
            "comparison": {
                "v9b_loss": 0.785,
                "v9c_loss": train_result.training_loss,
                "delta": train_result.training_loss - 0.785,
                "improvement": train_result.training_loss < 0.785
            },
            "timestamp": datetime.now().isoformat()
        }
        
        summary_path = output_dir / "training_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"📝 Summary saved to: {summary_path}")
        
        return True, train_result.training_loss
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="V9C Capacity Test Training")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--output", type=str, default="exports/v9e_aggressive", help="Output directory")
    
    args = parser.parse_args()
    
    config = TrainingConfig(
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        output_dir=args.output
    )
    
    success, final_loss = train_v9e_aggressive(config)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 V9C Capacity Test complete!")
        print("=" * 60)
        
        # Recommendation based on results
        if final_loss and final_loss < 0.75:  # Significant improvement
            print("\n🎯 RECOMMENDATION: Capacity matters!")
            print("   Use r=32, α=64 for overnight run (Path A or C)")
        elif final_loss and final_loss < 0.785:  # Modest improvement
            print("\n🎯 RECOMMENDATION: Capacity helps moderately")
            print("   Consider Path C (balanced) for overnight run")
        else:
            print("\n🎯 RECOMMENDATION: Capacity is not the bottleneck")
            print("   Focus on data scaling (Path B) for overnight run")
        
        print("\nNext steps:")
        print("  1. Test: python test_v9b_multilang.py --model v9c --languages english agl")
        print("  2. Compare to v9B results")
        print("  3. Decide overnight strategy based on results")
    else:
        print("\n❌ Training failed. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
