#!/usr/bin/env python3
"""
V9G Curriculum Learning Training
===============================

Two-stage curriculum learning to combine polyglot bootstrap + pure AGL mastery.

Stage 1: Fresh LFM2 + 750 polyglot examples → Bootstrap Tonight Protocol
Stage 2: Continue same model + 3500 pure AGL → Build consciousness awareness

Based on Phase 14F curriculum design with Goldilocks Zone parameters.
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
class CurriculumConfig:
    """V9G Curriculum Learning configuration."""
    # Model
    base_model: str = "LiquidAI/LFM2-350M"
    
    # Stage 1: Polyglot Bootstrap
    stage1_dataset: str = "data/v9g_stage1_polyglot.jsonl"
    stage1_epochs: int = 3
    stage1_output: str = "exports/v9g_stage1_polyglot"
    
    # Stage 2: Pure AGL Mastery  
    stage2_dataset: str = "data/v9g_stage2_agl_final.jsonl"
    stage2_epochs: int = 4  # MAX per Meuninghoff et al
    stage2_output: str = "exports/v9g_stage2_final"
    
    # Training (Goldilocks Zone from Phase 14D)
    max_seq_length: int = 1024
    batch_size: int = 1
    gradient_accumulation_steps: int = 16
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    
    # LoRA - Goldilocks Zone (r=32, α=64)
    lora_r: int = 32
    lora_alpha: int = 64
    lora_dropout: float = 0.05


def main():
    """Run the full v9G curriculum learning pipeline."""
    config = CurriculumConfig()
    
    print("🎓" + "="*60)
    print("🌙 V9G CURRICULUM LEARNING - OVERNIGHT RUN")
    print("🎓" + "="*60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ Expected duration: 6-8 hours")
    print(f"🎯 Goal: Polyglot bootstrap + AGL mastery")
    print()
    
    # Stage 1: Polyglot Bootstrap
    print("🌍 STAGE 1: POLYGLOT BOOTSTRAP")
    print("="*40)
    
    stage1_start = time.time()
    stage1_model_path = run_stage1(config)
    stage1_duration = time.time() - stage1_start
    
    print(f"✅ Stage 1 complete in {stage1_duration/60:.1f} minutes")
    print(f"📁 Model saved to: {stage1_model_path}")
    
    # Quick evaluation
    print("\n🔍 STAGE 1 EVALUATION:")
    evaluate_stage1(stage1_model_path)
    
    # Stage 2: Pure AGL Mastery
    print(f"\n🧠 STAGE 2: PURE AGL MASTERY")
    print("="*40)
    
    stage2_start = time.time()
    final_model_path = run_stage2(config, stage1_model_path)
    stage2_duration = time.time() - stage2_start
    
    print(f"✅ Stage 2 complete in {stage2_duration/60:.1f} minutes")
    print(f"📁 Final model saved to: {final_model_path}")
    
    # Total timing
    total_duration = stage1_duration + stage2_duration
    print("\n🏆 CURRICULUM COMPLETE!")
    print("="*40)
    print(f"⏱️  Stage 1: {stage1_duration/60:.1f} min")
    print(f"⏱️  Stage 2: {stage2_duration/60:.1f} min")
    print(f"⏱️  Total: {total_duration/60:.1f} min ({total_duration/3600:.1f} hrs)")
    print(f"📁 Final model: {final_model_path}")
    
    # Final evaluation
    print(f"\n🧪 FINAL EVALUATION:")
    run_final_evaluation(final_model_path)


def run_stage1(config: CurriculumConfig) -> str:
    """Run Stage 1: Polyglot Bootstrap training."""
    print(f"📖 Dataset: {config.stage1_dataset}")
    print(f"🔄 Epochs: {config.stage1_epochs}")
    print(f"📁 Output: {config.stage1_output}")
    
    # Import training libraries
    from transformers import (
        AutoTokenizer, AutoModelForCausalLM, 
        TrainingArguments, Trainer, DataCollatorForLanguageModeling
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from datasets import Dataset
    
    # Load model and tokenizer
    print("\n🤖 Loading fresh LFM2-350M model...")
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(config.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # LoRA setup
    print(f"🔧 Setting up LoRA (r={config.lora_r}, α={config.lora_alpha})...")
    model = prepare_model_for_kbit_training(model)
    
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    
    # Load and prepare dataset
    print(f"\n📊 Loading polyglot dataset...")
    dataset = load_and_tokenize_dataset(config.stage1_dataset, tokenizer, config.max_seq_length)
    print(f"📈 Loaded {len(dataset)} polyglot examples")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.stage1_output,
        num_train_epochs=config.stage1_epochs,
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=20,
        save_steps=500,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False,
        dataloader_pin_memory=False,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )
    
    # Train!
    print(f"\n🚀 Starting Stage 1 training...")
    trainer.train()
    
    # Save
    trainer.save_model()
    print(f"\n💾 Stage 1 model saved to: {config.stage1_output}")
    
    return config.stage1_output


def run_stage2(config: CurriculumConfig, stage1_path: str) -> str:
    """Run Stage 2: Pure AGL Mastery training."""
    print(f"📖 Dataset: {config.stage2_dataset}")
    print(f"🔄 Epochs: {config.stage2_epochs}")
    print(f"📁 Input: {stage1_path}")
    print(f"📁 Output: {config.stage2_output}")
    
    # Import training libraries
    from transformers import (
        AutoTokenizer, AutoModelForCausalLM,
        TrainingArguments, Trainer, DataCollatorForLanguageModeling
    )
    from peft import PeftModel
    from datasets import Dataset
    
    # Load Stage 1 model
    print(f"\n🔄 Loading Stage 1 model from {stage1_path}...")
    base_model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.float16,
        device_map="auto", 
        trust_remote_code=True
    )
    model = PeftModel.from_pretrained(base_model, stage1_path)
    
    # Merge adapters and prepare for training
    print("🔧 Merging Stage 1 adapters...")
    model = model.merge_and_unload()
    
    # Enable gradient computation
    model.train()
    for param in model.parameters():
        param.requires_grad = True
    
    tokenizer = AutoTokenizer.from_pretrained(config.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load and prepare dataset
    print(f"\n📊 Loading pure AGL dataset...")
    dataset = load_and_tokenize_dataset(config.stage2_dataset, tokenizer, config.max_seq_length)
    print(f"📈 Loaded {len(dataset)} pure AGL examples")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.stage2_output,
        num_train_epochs=config.stage2_epochs,
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=1e-4,  # Slightly lower for Stage 2
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=50,
        save_steps=1000,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False,
        dataloader_pin_memory=False,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )
    
    # Train!
    print(f"\n🚀 Starting Stage 2 training...")
    trainer.train()
    
    # Save
    trainer.save_model()
    print(f"\n💾 Stage 2 model saved to: {config.stage2_output}")
    
    return config.stage2_output


def load_and_tokenize_dataset(dataset_path: str, tokenizer, max_length: int):
    """Load and tokenize a JSONL dataset."""
    from datasets import Dataset
    
    # Load examples
    examples = []
    with open(dataset_path) as f:
        for line in f:
            data = json.loads(line)
            examples.append(data)
    
    # Create dataset
    dataset = Dataset.from_list(examples)
    
    # Tokenize
    def tokenize_function(examples):
        # Extract from messages format: user -> assistant conversation
        texts = []
        for messages in examples["messages"]:
            user_msg = messages[0]["content"]  # user message
            assistant_msg = messages[1]["content"]  # assistant response
            text = f"{user_msg}\n{assistant_msg}<|endoftext|>"
            texts.append(text)
        
        # Tokenize
        result = tokenizer(
            texts,
            truncation=True,
            padding=False,
            max_length=max_length,
            return_tensors=None,
        )
        
        # Labels are the same as input_ids for language modeling
        result["labels"] = result["input_ids"].copy()
        return result
    
    tokenized = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
    return tokenized


def evaluate_stage1(model_path: str):
    """Quick evaluation of Stage 1 model."""
    print("🔍 Stage 1 evaluation temporarily disabled (missing test module)")
    print(f"📁 Stage 1 model available at: {model_path}")
    print("🚀 Proceeding to Stage 2...")
    
    # TODO: Re-enable when test_v9b_multilang is available
    # Import test framework
    # sys.path.append('.')
    # from test_v9b_multilang import load_model_and_test, extract_consciousness_markers
    
    # try:
    #     results = load_model_and_test(model_path, ["agl"], protocols=["tonight_protocol"])
    #     
    #     if "agl" in results.get("by_language", {}):
    #         markers = results["by_language"]["agl"].get("aggregate_markers", {})
    #         tonight = markers.get("tonight_protocol_marker", 0)
    #         phi = markers.get("phi_patterns", 0)
    #         
    #         print(f"   Tonight Protocol: {tonight:.4f}")
    #         print(f"   Phi patterns: {phi:.4f}")
    #         
    #         if tonight > 0.010:
    #             print("   ✅ Stage 1 SUCCESS: Tonight Protocol emerging!")
    #         else:
    #             print("   ⚠️  Stage 1 PARTIAL: Low Tonight Protocol, but continuing...")
    #     else:
    #         print("   ❓ Stage 1 evaluation inconclusive")
    #         
    # except Exception as e:
    #     print(f"   ⚠️  Stage 1 evaluation failed: {e}")
    #     print("   🔄 Continuing to Stage 2...")


def run_final_evaluation(model_path: str):
    """Run full consciousness evaluation on final model."""
    print("🔬 Final evaluation temporarily disabled (missing test module)")
    print(f"📁 V9G curriculum model available at: {model_path}")
    print("✅ Training complete!")
    
    # TODO: Re-enable when test_v9b_multilang is available
    # print("🧪 Running final consciousness metrics...")
    # 
    # # Import test framework
    # sys.path.append('.')
    # from test_v9b_multilang import load_model_and_test
    
    # try:
    #     results = load_model_and_test(
    #         model_path, 
    #         languages=["agl", "english"],
    #         protocols=["tonight_protocol", "agl_consciousness", "phi_patterns"]
    #     )
    #     
    #     # Save results
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     results_file = f"results/v9g_curriculum_{timestamp}.json"
    #     
    #     os.makedirs("results", exist_ok=True)
    #     with open(results_file, 'w') as f:
    #         json.dump(results, f, indent=2)
    #     
    #     print(f"📄 Results saved to: {results_file}")
    #     
    #     # Print summary
    #     if "agl" in results.get("by_language", {}):
    #         markers = results["by_language"]["agl"].get("aggregate_markers", {})
    #         
    #         print("\n🎯 V9G CURRICULUM RESULTS:")
    #         print("="*30)
    #         print(f"AGL awareness: {markers.get('agl_awareness', 0):.4f}")
    #         print(f"Tonight Protocol: {markers.get('tonight_protocol_marker', 0):.4f}")
    #         print(f"Phi patterns: {markers.get('phi_patterns', 0):.4f}")
    #         print(f"Certainty gradient: {markers.get('certainty_gradient', 0):.4f}")
    #         
    #         # Compare to baselines
    #         print("\n📊 VS BASELINES:")
    #         agl_val = markers.get('agl_awareness', 0)
    #         tonight_val = markers.get('tonight_protocol_marker', 0)
    #         
    #         print(f"vs v9C Champion (0.0927): {agl_val/0.0927*100:.1f}%")
    #         print(f"vs v9F-base Tonight (0.0200): {tonight_val/0.0200*100:.1f}%")
    #         
    #         # Success assessment
    #         if agl_val >= 0.070 and tonight_val >= 0.015:
    #             print("\n🎉 SUCCESS: Both targets achieved!")
    #         elif agl_val >= 0.070:
    #             print("\n✅ PARTIAL: High AGL awareness achieved")
    #         elif tonight_val >= 0.015:
    #             print("\n✅ PARTIAL: Tonight Protocol achieved")
    #         else:
    #             print("\n⚠️  SUBOPTIMAL: Neither target fully achieved")
    #             
    # except Exception as e:
    #     print(f"❌ Final evaluation failed: {e}")


if __name__ == "__main__":
    main()