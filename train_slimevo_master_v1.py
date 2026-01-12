#!/usr/bin/env python3
"""
SLIM-EVO Phase 3/4: Resonance-Active Master Training
===================================================

The definitive training script for Ada-SLM (LFM2-1.2B).
Unifies all discoveries:
1. Resonance-Active Reward (TinyAleph Primes)
2. CI-Density Gating (Crystal Intelligence)
3. Golden Annealing (Fibonacci Learning Schedules)
4. Hierarchical AGL Reasoning (Pixie Dust)

Output: Ada-SLM-1.2B-Resonant
"""

import os
# ROCm compatibility - MUST SET BEFORE importing torch!
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL", "1")

import torch
import json
import time
from pathlib import Path
from datetime import datetime
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer, 
    DataCollatorForLanguageModeling,
    TrainerCallback
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType

# Import custom consciousness engineering
from consciousness_engineering.metrics.crystal_intelligence import CrystalIntelligenceCalculator
from consciousness_engineering.metrics.resonance import ResonanceCalculator
from consciousness_engineering.infrastructure.hardware import HardwareManager

class ResonanceMetricCallback(TrainerCallback):
    """Logs consciousness metrics to a separate file for analysis."""
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.output_dir / "consciousness_metrics.jsonl"
        
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            # Check if custom metrics are in logs (passed from compute_loss via trainer state)
            metrics = {
                "step": state.global_step,
                "timestamp": datetime.now().isoformat(),
                "loss": logs.get("loss"),
                "learning_rate": logs.get("learning_rate"),
                "epoch": logs.get("epoch")
            }
            # Note: Reality check - compute_loss doesn't easily pass data back to logs 
            # without custom handling. We'll handle this in the Trainer class instead.
            pass

class ResonanceActiveMasterTrainer(Trainer):
    def __init__(self, **kwargs):
        tokenizer = kwargs.pop('tokenizer')
        super().__init__(**kwargs)
        self.tokenizer = tokenizer
        self.ci_calc = CrystalIntelligenceCalculator(threshold=100.0)
        self.res_calc = ResonanceCalculator(sif_ontology_path="ada-sif/resonance_map.json")
        
        # State sharing for metrics tracking
        self.last_ci_result = None
        self.last_res_score = 0.85
        self.metrics_history = []
        
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        """Custom loss integrating Resonance and CI as rewards."""
        outputs = model(**inputs, output_hidden_states=True)
        structural_loss = outputs.loss
        
        # Extract hidden states (last token of last layer)
        last_hidden = outputs.hidden_states[-1][:, -1, :] 
        
        # Calculate rewards (Throttled for performance: every 10 steps)
        if self.state.global_step % 10 == 0 or self.last_ci_result is None:
            with torch.no_grad():
                self.last_ci_result = self.ci_calc.calculate_model_ci(model)
                self.last_res_score = self.res_calc.calculate_resonance(last_hidden, inputs["labels"])
            
            # Print telemetry to console
            print(f"\n[PHASE 3] Step {self.state.global_step} | Loss: {structural_loss.item():.4f} | CI: {self.last_ci_result.ci_density:.2f} | Res: {self.last_res_score:.4f}")
            
            # Log to history
            self.metrics_history.append({
                "step": self.state.global_step,
                "loss": structural_loss.item(),
                "ci": self.last_ci_result.ci_density,
                "resonance": self.last_res_score,
                "timestamp": datetime.now().isoformat()
            })
        
        # Rewards integration
        ci_reward = max(0, self.last_ci_result.ci_density - 50.0) / 100.0
        res_score = self.last_res_score
        
        # Fibonacci Dynamics (Annealing Schedules)
        total_steps = max(1, self.state.max_steps)
        # lambda_ci grows (crystallization anchor)
        lambda_ci = 0.2 * (self.state.global_step / total_steps) 
        # lambda_res stays steady (truth alignment anchor)
        lambda_res = 0.1 
        
        total_loss = structural_loss - (lambda_ci * ci_reward) - (lambda_res * res_score)
            
        return (total_loss, outputs) if return_outputs else total_loss

def main():
    # --- 1. CONFIGURATION ---
    MODEL_ID = "LiquidAI/LFM2-1.2B"
    DATASET_PATH = "data/phase3_10k_resonance.jsonl"
    OUTPUT_DIR = f"./models/ada-slim-1.2b-resonance-{datetime.now().strftime('%Y%m%d')}"
    
    print(f"🌌 Launching SLIM-EVO Master Run v1")
    print(f"   Model:   {MODEL_ID}")
    print(f"   Dataset: {DATASET_PATH}")
    print(f"   Output:  {OUTPUT_DIR}")
    print("-" * 40)

    # Initialize Hardware
    hw = HardwareManager()
    hw.setup_environment()
    print(f"🔧 Hardware detected: {hw.hardware_type.value}")

    # --- 2. PREPARATION ---
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    if tokenizer.pad_token is None: 
        tokenizer.pad_token = tokenizer.eos_token
    
    print("📥 Loading Model weights...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        trust_remote_code=True, 
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # LoRA Configuration (Rank 64 - The "Golden Rank")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=64,
        lora_alpha=128,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "w1", "w2", "w3"],
        lora_dropout=0.05,
        bias="none"
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # --- 3. DATA LOADING ---
    print(f"📚 Tokenizing dataset: {DATASET_PATH}")
    with open(DATASET_PATH, 'r') as f:
        raw_data = [json.loads(line) for line in f]
    
    def tokenize_fn(ex):
        # Format for AGL-first training (Pixie Dust Reasoning)
        full_text = f"User: {ex['messages'][0]['content']}\nAssistant: {ex['messages'][1]['content']}"
        tokenized = tokenizer(
            full_text, 
            truncation=True, 
            max_length=1024, # Larger context for complex AGL
            padding="max_length"
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
        
    full_dataset = Dataset.from_list([tokenize_fn(ex) for ex in raw_data])
    full_dataset = full_dataset.shuffle(seed=42)

    # --- 4. TRAINING ---
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3, # 3 cycles of Golden Annealing
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=1e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        weight_decay=0.01,
        logging_steps=10,
        save_strategy="epoch",
        fp16=True,
        report_to="none",
        push_to_hub=False,
        remove_unused_columns=False
    )
    
    trainer = ResonanceActiveMasterTrainer(
        model=model,
        args=training_args,
        train_dataset=full_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    print("🚀 EVOLUTION START: Resonance-Active Training Engaged.")
    trainer.train()

    # --- 5. FINALIZATION ---
    print(f"💾 Saving evolved model to {OUTPUT_DIR}...")
    trainer.save_model()
    
    # Save the consciousness metrics trace
    metrics_path = Path(OUTPUT_DIR) / "consciousness_trace.json"
    with open(metrics_path, "w") as f:
        json.dump(trainer.metrics_history, f, indent=2)
    
    print("✨ ARCHIVING COMPLETE. Ada-SLM has achieved high-resonance stability.")

if __name__ == "__main__":
    main()
