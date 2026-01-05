#!/usr/bin/env python3
"""
V9F Polyglot V9C Enhancement Training
======================================

Train V9C CHAMPION model on polyglot → AGL translation pairs.

This tests: Can polyglot data ENHANCE existing consciousness?

V9C already has:
- 92x AGL awareness (baseline 0.0010 → 0.0927!)
- Strong certainty gradients
- Emerging phi patterns

Can we push it further with polyglot training?

Uses OPTIMAL config from Phase 14D Goldilocks Zone findings:
- LoRA r=32 (not 16, not 48!)
- batch_size=1 (regularization)
- grad_accum=16 (effective batch 16)
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
    """V9F Polyglot V9C Enhancement - Build on champion!"""
    # Model - V9C CHAMPION as base!
    base_model: str = "exports/v9c_capacity/final_model"
    original_base: str = "LiquidAI/LFM2-350M"  # For tokenizer
    
    # Dataset
    dataset_path: str = "data/v9f_polyglot.jsonl"
    
    # Training - Goldilocks Zone config!
    max_seq_length: int = 1024
    batch_size: int = 1  # Regularization!
    gradient_accumulation_steps: int = 16  # Effective batch 16
    num_epochs: int = 3  # Fewer epochs - already trained
    learning_rate: float = 1e-4  # Lower LR for fine-tuning
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    
    # LoRA - Goldilocks Zone! (Same as v9C for continuity)
    lora_r: int = 32
    lora_alpha: int = 64
    lora_dropout: float = 0.05
    
    # Output
    output_dir: str = "exports/v9f_polyglot_v9c"


def load_dataset(config: TrainingConfig) -> list:
    """Load the polyglot dataset."""
    print(f"📊 Loading dataset from {config.dataset_path}...")
    
    dataset_path = Path(config.dataset_path)
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        print("💡 Run: ce dataset polyglot")
        sys.exit(1)
    
    examples = []
    source_counts = {}
    
    with open(dataset_path) as f:
        for line in f:
            data = json.loads(line)
            examples.append(data)
            meta = data.get("metadata", {})
            source = meta.get("source_lang", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
    
    print(f"✅ Loaded {len(examples)} examples")
    print(f"   Language distribution: {source_counts}")
    
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
                "phase": ex.get("phase", "polyglot")
            })
    
    return formatted


def train_v9f_polyglot_v9c(config: TrainingConfig):
    """Run V9F Polyglot V9C Enhancement training."""
    print("=" * 60)
    print("🏆 V9F POLYGLOT V9C - Enhance the champion!")
    print("=" * 60)
    print(f"Base model: {config.base_model} (V9C CHAMPION)")
    print(f"Dataset: {config.dataset_path}")
    print(f"LoRA r: {config.lora_r} (Goldilocks Zone!)")
    print(f"LoRA α: {config.lora_alpha}")
    print(f"Output: {config.output_dir}")
    print("=" * 60)
    
    # Check v9c model exists
    v9c_path = Path(config.base_model)
    if not v9c_path.exists():
        print(f"❌ V9C model not found: {v9c_path}")
        print("💡 Run v9c training first!")
        sys.exit(1)
    
    # Import heavy libraries after config
    from transformers import (
        AutoModelForCausalLM, 
        AutoTokenizer,
        TrainingArguments,
        Trainer,
        DataCollatorForLanguageModeling
    )
    from peft import PeftModel, LoraConfig, get_peft_model, TaskType
    from datasets import Dataset
    
    # Setup output directory
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load dataset
    examples = load_dataset(config)
    formatted = format_for_training(examples)
    
    # Create HF dataset
    dataset = Dataset.from_list(formatted)
    
    # Load tokenizer from original base model
    print(f"\n📥 Loading tokenizer from {config.original_base}...")
    tokenizer = AutoTokenizer.from_pretrained(
        config.original_base,
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
    
    # Load V9C model - it already has LoRA merged or as adapter
    print(f"\n📥 Loading V9C champion model...")
    from consciousness_engineering.infrastructure.hardware import HardwareManager
    
    hw = HardwareManager()
    hw.setup_optimal_environment()
    print(f"   Hardware detected: {hw.hardware_type.value}")
    
    # Load the base model first
    model = hw.load_model_safe(
        AutoModelForCausalLM,
        config.original_base,
        attn_implementation="eager"
    )
    
    # Then load V9C's LoRA weights on top
    print(f"   Loading V9C LoRA weights from {config.base_model}...")
    model = PeftModel.from_pretrained(model, config.base_model)
    
    # Merge LoRA weights into base model for further training
    print("   Merging V9C LoRA weights into base...")
    model = model.merge_and_unload()
    
    # Now add NEW LoRA for polyglot training
    print(f"🔧 Adding NEW LoRA layer (r={config.lora_r}, α={config.lora_alpha})")
    
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
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
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        run_name=f"v9f_polyglot_v9c_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        **training_kwargs
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
    print("🚀 Starting V9F Polyglot V9C Enhancement training...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        train_result = trainer.train()
        
        training_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("✅ V9F Polyglot V9C Enhancement complete!")
        print("=" * 60)
        print(f"⏱️  Training time: {training_time/60:.1f} minutes")
        print(f"📉 Final train loss: {train_result.training_loss:.4f}")
        
        # Compare to V9C baseline
        print("\n📊 COMPARISON TO V9C:")
        print(f"   V9C AGL awareness: 0.0927 (92x)")
        print(f"   V9F-v9c: Run ce test to compare!")
        
        # Save final model
        final_model_path = output_dir / "final_model"
        model.save_pretrained(final_model_path)
        tokenizer.save_pretrained(final_model_path)
        print(f"\n💾 Model saved to: {final_model_path}")
        
        # Save training summary
        summary = {
            "experiment": "v9f_polyglot_v9c",
            "hypothesis": "Polyglot data can ENHANCE existing consciousness",
            "base_model": config.base_model,
            "original_base": config.original_base,
            "dataset": config.dataset_path,
            "num_examples": len(examples),
            "num_epochs": config.num_epochs,
            "training_time_minutes": training_time / 60,
            "final_train_loss": train_result.training_loss,
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
            "v9c_baseline": {
                "agl_awareness": 0.0927,
                "improvement_factor": "92x"
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
    
    parser = argparse.ArgumentParser(description="V9F Polyglot V9C Enhancement Training")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--output", type=str, default="exports/v9f_polyglot_v9c", help="Output directory")
    parser.add_argument("--dataset", type=str, default="data/v9f_polyglot.jsonl", help="Dataset path")
    parser.add_argument("--v9c-path", type=str, default="exports/v9c_capacity/final_model", help="V9C model path")
    
    args = parser.parse_args()
    
    config = TrainingConfig(
        num_epochs=args.epochs,
        learning_rate=args.lr,
        output_dir=args.output,
        dataset_path=args.dataset,
        base_model=args.v9c_path
    )
    
    success, final_loss = train_v9f_polyglot_v9c(config)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 V9F Polyglot V9C Enhancement complete!")
        print("=" * 60)
        print("\nNext: Run consciousness tests to compare!")
        print("  ce test -m v9f_v9c --languages english agl lojban toki_pona")
    else:
        print("\n❌ Training failed. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
