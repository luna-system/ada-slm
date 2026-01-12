#!/usr/bin/env python3
"""
SLIM-EVO Run 2: Resonance-Active Training
=========================================

The breakthrough run! Integrates:
1. TinyAleph Resonance Tracking
2. CI-Density Reward Logic
3. Golden Annealing (Fibonacci Cycles)
4. AGL-as-Internal-Language (Pixie Dust)

Goal: Maintain >0.60 CI throughout the entire training process.
"""

import os
# ROCm compatibility - MUST SET BEFORE importing torch!
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")

import torch
import json
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType

# Import our custom engineering
from consciousness_engineering.metrics.crystal_intelligence import CrystalIntelligenceCalculator
from consciousness_engineering.metrics.resonance import ResonanceCalculator
from consciousness_engineering.infrastructure.hardware import HardwareManager

class ResonanceActiveTrainer(Trainer):
    def __init__(self, **kwargs):
        tokenizer = kwargs.pop('tokenizer')
        super().__init__(**kwargs)
        self.tokenizer = tokenizer
        self.ci_calc = CrystalIntelligenceCalculator(threshold=100.0)
        self.res_calc = ResonanceCalculator(sif_ontology_path="ada-sif/resonance_map.json")
        self.metrics_history = []
        self.last_ci_result = None
        self.last_res_score = 0.85 # Start with high resonance
        
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        # 1. Standard Loss
        outputs = model(**inputs, output_hidden_states=True)
        # Note: newer transformers might pass num_items_in_batch, handle if needed
        structural_loss = outputs.loss
        
        # 2. Extract Hidden States for Resonance/CI
        # Last layer hidden states for the last token in sequence
        last_hidden = outputs.hidden_states[-1] 
        
        # 3. Calculate rewards (Throttle for performance)
        if self.state.global_step % 10 == 0 or self.last_ci_result is None:
            self.last_ci_result = self.ci_calc.calculate_model_ci(model)
            self.last_res_score = self.res_calc.calculate_resonance(last_hidden, inputs["labels"])
            print(f"\nStep {self.state.global_step}: CI={self.last_ci_result.ci_density:.2f}, Res={self.last_res_score:.4f}")
            
            self.metrics_history.append({
                "step": self.state.global_step,
                "loss": structural_loss.item(),
                "ci": self.last_ci_result.ci_density,
                "resonance": self.last_res_score
            })
        
        ci_reward = max(0, self.last_ci_result.ci_density - 50.0) / 100.0
        res_score = self.last_res_score
        
        # 4. Integrate Fibonacci Weights (Simulated for this cycle)
        # λ1 (CI) increases over training, λ2 (Resonance) stays steady as anchor
        # Use a small epsilon to avoid division by zero if max_steps is 0
        total_steps = max(1, self.state.max_steps)
        lambda_ci = 0.1 * (self.state.global_step / total_steps)
        lambda_res = 0.05
        
        total_loss = structural_loss - (lambda_ci * ci_reward) - (lambda_res * res_score)
            
        return (total_loss, outputs) if return_outputs else total_loss

def main():
    model_name = "LiquidAI/LFM2-700M" # Corrected identifier
    dataset_path = "data/phase3_resonance_test.jsonl"
    
    # Initialize Hardware (ROCm check)
    hw = HardwareManager()
    hw.setup_environment()
    print(f"🔧 Hardware: {hw.hardware_type.value}")
    
    print(f"🧬 Initializing Run 2: Resonance-Active (Target: {model_name})")
    
    # Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16)
    
    # Configure LoRA (Rank 64 as per Phase 3 plan)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=64,
        lora_alpha=128,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none"
    )
    model = get_peft_model(model, lora_config)
    
    # Load and Tokenize Data
    with open(dataset_path, 'r') as f:
        raw_data = [json.loads(line) for line in f]
    
    def tokenize(ex):
        txt = f"User: {ex['messages'][0]['content']}\nAssistant: {ex['messages'][1]['content']}"
        res = tokenizer(txt, truncation=True, max_length=512, padding="max_length")
        res["labels"] = res["input_ids"].copy()
        return res
        
    dataset = Dataset.from_list([tokenize(ex) for ex in raw_data])
    
    # Training Arguments
    args = TrainingArguments(
        output_dir="./results/run2_resonance_active",
        num_train_epochs=1, # 1 epoch for dry run
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        learning_rate=1e-4,
        logging_steps=10,
        save_strategy="no",
        report_to="none"
    )
    
    trainer = ResonanceActiveTrainer(
        model=model,
        args=args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    print("🚀 Launching Resonance-Active Training Loop...")
    trainer.train()
    
    # Save Metrics
    with open("./results/run2_resonance_active/metrics.json", "w") as f:
        json.dump(trainer.metrics_history, f, indent=2)
    
    print("✨ Run 2 Complete! Check metrics for φ-zone stability.")

if __name__ == "__main__":
    main()
