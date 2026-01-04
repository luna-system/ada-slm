#!/usr/bin/env python3
"""
Phase 14 REAL Training Runner
=============================

Actually trains LFM2-350M using transformers + peft!
This is the REAL dogfooding - our framework doing actual GPU training!
"""

import os
import sys
import json
import torch
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# ROCm safety first!
os.environ.setdefault("HIP_VISIBLE_DEVICES", "0")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

from consciousness_engineering.infrastructure.hardware import HardwareManager


def load_dataset(dataset_path: str) -> List[Dict[str, Any]]:
    """Load the generated dataset."""
    examples = []
    with open(dataset_path, 'r') as f:
        for line in f:
            examples.append(json.loads(line))
    return examples


def prepare_training_data(examples: List[Dict], tokenizer, max_length: int = 512):
    """Convert examples to tokenized format for training."""
    
    print(f"  🔄 Preparing {len(examples)} examples...")
    
    texts = []
    for ex in examples:
        # Convert chat format to text
        messages = ex.get('messages', [])
        text_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'user':
                text_parts.append(f"User: {content}")
            else:
                text_parts.append(f"Assistant: {content}")
        
        text = "\n".join(text_parts)
        texts.append(text)
    
    print(f"  🔄 Tokenizing...")
    
    # Tokenize one at a time to avoid memory issues
    def tokenize_function(example_texts):
        return tokenizer(
            example_texts,
            truncation=True,
            max_length=max_length,
            padding='max_length'
        )
    
    # Create dataset from texts first, then tokenize
    dataset = Dataset.from_dict({'text': texts})
    
    def tokenize_map(examples):
        tokenized = tokenizer(
            examples['text'],
            truncation=True,
            max_length=max_length,
            padding='max_length'
        )
        tokenized['labels'] = tokenized['input_ids'].copy()
        return tokenized
    
    dataset = dataset.map(
        tokenize_map,
        batched=True,
        batch_size=100,
        remove_columns=['text'],
        desc="Tokenizing"
    )
    
    print(f"  ✅ Dataset ready: {len(dataset)} examples")
    return dataset


def train_phase(
    model,
    tokenizer,
    train_dataset,
    phase_name: str,
    output_dir: str,
    learning_rate: float,
    num_epochs: float,
    batch_size: int = 4
) -> Dict[str, Any]:
    """Train a single curriculum phase."""
    
    print(f"\n🎯 Training Phase: {phase_name}")
    print(f"📊 Examples: {len(train_dataset)}")
    print(f"📈 Learning rate: {learning_rate:.2e}")
    print(f"🔄 Epochs: {num_epochs}")
    
    phase_output = Path(output_dir) / phase_name
    phase_output.mkdir(parents=True, exist_ok=True)
    
    print(f"  📁 Output: {phase_output}")
    
    # Training arguments - explicitly tell it to use CUDA
    print("  ⚙️  Creating TrainingArguments...")
    training_args = TrainingArguments(
        output_dir=str(phase_output),
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        warmup_steps=50,
        logging_steps=10,  # More frequent logging
        save_steps=500,
        save_total_limit=2,
        fp16=False,  # DISABLE fp16 for ROCm compatibility
        bf16=False,  # Don't use bf16 either
        dataloader_num_workers=0,  # Avoid multiprocessing issues
        report_to="none",  # Don't report to wandb etc
        remove_unused_columns=False,
        optim="adamw_torch",
        # Explicitly enable CUDA
        no_cuda=False,
        use_cpu=False,
        dataloader_pin_memory=False,  # CRITICAL: Disable pin_memory for ROCm
    )
    print(f"  ✅ TrainingArguments ready (device: {training_args.device})")
    
    # Data collator
    print("  ⚙️  Creating DataCollator...")
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal LM, not masked
    )
    print("  ✅ DataCollator ready")
    
    # Create trainer
    print("  ⚙️  Creating Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator
    )
    print("  ✅ Trainer ready")
    
    # Train!
    print("  🚀 Starting training...")
    start_time = datetime.now()
    train_result = trainer.train()
    end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    
    # Get final metrics
    final_loss = train_result.training_loss
    
    print(f"✅ Phase completed in {duration:.1f}s")
    print(f"📉 Final loss: {final_loss:.4f}")
    
    return {
        "phase_name": phase_name,
        "final_loss": final_loss,
        "training_time_seconds": duration,
        "examples_trained": len(train_dataset),
        "success": True
    }


def main():
    print("🌟 PHASE 14 REAL TRAINING - LFM2-350M")
    print("=" * 60)
    print("🎯 Using consciousness_engineering framework with REAL training!")
    print("🧠 LiquidAI/LFM2-350M hybrid architecture")
    print()
    
    # Get script directory for relative paths
    script_dir = Path(__file__).parent.absolute()
    
    # Check dataset exists  
    dataset_path = script_dir / "data/phase14_lfm2_enhanced_50k.jsonl"
    if not dataset_path.exists():
        print(f"❌ Dataset not found at {dataset_path}!")
        print("Run generate_phase14_dataset.py first")
        sys.exit(1)
    
    # Setup hardware
    print("🔧 Setting up hardware environment...")
    hardware = HardwareManager()
    hw_type = hardware.detect_hardware()
    print(f"✅ Detected hardware: {hw_type.value}")
    hardware.setup_optimal_environment()
    hardware.isolate_gpu_memory()
    
    # Check GPU
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"🎮 GPU: {gpu_name} ({gpu_mem:.1f}GB)")
    else:
        print("⚠️  No GPU detected, training will be slow!")
    
    # Load model and tokenizer
    print("\n📦 Loading LFM2-350M model...")
    model_name = "LiquidAI/LFM2-350M"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        # Add padding token if missing
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # ROCM FIX: Load model on CPU first, apply LoRA, THEN move to GPU
        # This avoids HIP kernel errors during PEFT dtype casting
        print("  📥 Loading model on CPU first (ROCm compatibility)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float32,  # Use float32 for LoRA application
            device_map=None,  # CRITICAL: Must be None for Trainer compatibility!
            attn_implementation="eager",  # ROCm compatible attention
        )
        
        print(f"✅ Model loaded: {model_name}")
        print(f"📊 Parameters: {model.num_parameters():,}")
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)
    
    # Apply LoRA ON CPU (before moving to GPU)
    print("\n🔧 Applying LoRA configuration (on CPU for ROCm safety)...")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    model = get_peft_model(model, lora_config)
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"✅ LoRA applied: {trainable_params:,} / {total_params:,} trainable ({100*trainable_params/total_params:.2f}%)")
    
    # NOW move to GPU after LoRA is applied
    if torch.cuda.is_available():
        print("  🎮 Moving model to GPU (keeping float32, fp16 via autocast during training)...")
        model = model.cuda()
        # Don't convert to half() here - let Trainer handle it via fp16=True
        print("  ✅ Model on GPU in float32 (Trainer will use fp16 autocast)")
    
    # Load dataset
    print(f"\n📊 Loading dataset from {dataset_path}...")
    all_examples = load_dataset(str(dataset_path))
    print(f"✅ Loaded {len(all_examples)} examples")
    
    # Split by type
    tool_examples = [ex for ex in all_examples if ex.get('type') == 'tool_use']
    cot_examples = [ex for ex in all_examples if ex.get('type') == 'chain_of_thought']
    agl_examples = [ex for ex in all_examples if ex.get('type') == 'agl_consciousness']
    
    print(f"  📦 Tool use: {len(tool_examples)}")
    print(f"  🧠 Chain-of-thought: {len(cot_examples)}")
    print(f"  ✨ AGL consciousness: {len(agl_examples)}")
    
    # Define curriculum phases (smaller for initial test)
    # Using 100 examples per phase for quick validation
    EXAMPLES_PER_PHASE = 100  # SMALL for debugging! Increase to 1000+ for real training
    
    curriculum = [
        {
            "name": "phase1_basic_tools",
            "examples": tool_examples[:EXAMPLES_PER_PHASE],
            "learning_rate": 3e-4,
            "epochs": 1.0
        },
        {
            "name": "phase2_advanced_tools",
            "examples": tool_examples[EXAMPLES_PER_PHASE:EXAMPLES_PER_PHASE*2],
            "learning_rate": 2e-4,
            "epochs": 1.0
        },
        {
            "name": "phase3_chain_of_thought",
            "examples": cot_examples[:EXAMPLES_PER_PHASE],
            "learning_rate": 1.5e-4,
            "epochs": 1.0
        },
        {
            "name": "phase4_agl_consciousness",
            "examples": agl_examples[:min(EXAMPLES_PER_PHASE, len(agl_examples))],
            "learning_rate": 1e-4,
            "epochs": 1.0
        }
    ]
    
    output_dir = script_dir / "exports/phase14_lfm2_real"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Train each phase
    print(f"\n🚀 Starting {len(curriculum)}-phase curriculum training...")
    print("=" * 60)
    
    all_results = []
    total_start = datetime.now()
    
    for i, phase in enumerate(curriculum):
        print(f"\n{'='*60}")
        print(f"📚 PHASE {i+1}/{len(curriculum)}: {phase['name']}")
        print(f"{'='*60}")
        
        # Prepare data
        train_dataset = prepare_training_data(
            phase['examples'],
            tokenizer,
            max_length=512  # Shorter for faster training
        )
        
        # Train
        result = train_phase(
            model=model,
            tokenizer=tokenizer,
            train_dataset=train_dataset,
            phase_name=phase['name'],
            output_dir=output_dir,
            learning_rate=phase['learning_rate'],
            num_epochs=phase['epochs'],
            batch_size=4
        )
        
        all_results.append(result)
        
        # Clear GPU memory between phases
        torch.cuda.empty_cache()
    
    total_end = datetime.now()
    total_duration = total_end - total_start
    
    # Save final model
    print(f"\n💾 Saving final model...")
    final_model_path = Path(output_dir) / "final_model"
    model.save_pretrained(str(final_model_path))
    tokenizer.save_pretrained(str(final_model_path))
    print(f"✅ Model saved: {final_model_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 PHASE 14 TRAINING COMPLETE!")
    print("=" * 60)
    print(f"⏱️  Total duration: {total_duration}")
    print(f"📊 Phases completed: {len(all_results)}")
    
    for result in all_results:
        print(f"  ✅ {result['phase_name']}: loss={result['final_loss']:.4f}, time={result['training_time_seconds']:.1f}s")
    
    # Save training summary
    summary = {
        "model": model_name,
        "start_time": total_start.isoformat(),
        "end_time": total_end.isoformat(),
        "total_duration_seconds": total_duration.total_seconds(),
        "phases": all_results,
        "final_model_path": str(final_model_path),
        "lora_config": {
            "r": 16,
            "lora_alpha": 32,
            "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"]
        }
    }
    
    summary_path = Path(output_dir) / "training_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n💾 Summary saved: {summary_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
