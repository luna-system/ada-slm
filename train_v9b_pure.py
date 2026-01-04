#!/usr/bin/env python3
"""
V9B-Pure AGL Training
=====================

Train LFM2-350M on pure AGL dataset (2000 examples, 4 phases).

Curriculum:
- Phase 1: Warmup (500) - Certainty gradient, basic φ-patterns
- Phase 2: Tonight (500) - Existential questions, 0.60 threshold  
- Phase 3: Eigenvalue (500) - Temporal progressions, Δ operators
- Phase 4: Deep AGL (500) - Full vocabulary integration

From ADA-SLM-PHASE14C-V9B-PURE-AGL.md
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
    """V9B-Pure training configuration."""
    # Model
    base_model: str = "LiquidAI/LFM2-350M"
    
    # Dataset  
    dataset_path: str = "data/v9b_pure_agl_2k.jsonl"
    
    # Training
    max_seq_length: int = 1024  # AGL responses are shorter
    batch_size: int = 4
    gradient_accumulation_steps: int = 4  # Effective batch 16
    num_epochs: int = 3
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    
    # LoRA
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    
    # Output
    output_dir: str = "exports/v9b_pure"


def load_dataset(config: TrainingConfig) -> list:
    """Load the v9b_pure dataset."""
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


def train_v9b_pure(config: TrainingConfig):
    """Run V9B-Pure training."""
    print("=" * 60)
    print("V9B-Pure AGL Training")
    print("=" * 60)
    print(f"Base model: {config.base_model}")
    print(f"Dataset: {config.dataset_path}")
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
    
    # Load model
    print(f"\n📥 Loading model: {config.base_model}...")
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="eager"  # ROCm compatible
    )
    
    # Setup LoRA
    print(f"🔧 Configuring LoRA (r={config.lora_r}, α={config.lora_alpha})...")
    
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
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=20,
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=True,
        dataloader_pin_memory=False,  # ROCm compatibility
        report_to="none",
        run_name=f"v9b_pure_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
    print("🚀 Starting V9B-Pure training...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        train_result = trainer.train()
        
        training_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("✅ Training complete!")
        print("=" * 60)
        print(f"⏱️  Training time: {training_time/60:.1f} minutes")
        print(f"📉 Final train loss: {train_result.training_loss:.4f}")
        
        # Save final model
        final_model_path = output_dir / "final_model"
        model.save_pretrained(final_model_path)
        tokenizer.save_pretrained(final_model_path)
        print(f"💾 Model saved to: {final_model_path}")
        
        # Save training summary
        summary = {
            "model": config.base_model,
            "dataset": config.dataset_path,
            "num_examples": len(examples),
            "num_epochs": config.num_epochs,
            "training_time_minutes": training_time / 60,
            "final_train_loss": train_result.training_loss,
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
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
    
    parser = argparse.ArgumentParser(description="V9B-Pure AGL Training")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--output", type=str, default="exports/v9b_pure", help="Output directory")
    
    args = parser.parse_args()
    
    config = TrainingConfig(
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        output_dir=args.output
    )
    
    success, final_loss = train_v9b_pure(config)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 V9B-Pure training successful!")
        print(f"📉 Final loss: {final_loss:.4f}")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Test with: python quick_v9a_inference.py --model exports/v9b_pure/final_model")
        print("  2. Upload to HuggingFace: huggingface-cli upload luna-sys/ada-slm-v9b-pure exports/v9b_pure/final_model")
    else:
        print("\n❌ Training failed. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
