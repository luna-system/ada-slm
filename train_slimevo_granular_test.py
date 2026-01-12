#!/usr/bin/env python3
"""
Resonance-Active Granular Diagnostic
====================================

Logs CI and Resonance EVERY STEP to observe the 'Physics of Meaning' 
at ultra-high resolution. Used for pinpointing the exact moment 
of alignment or dissonance.
"""

import os
# ROCm compatibility
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")

import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType

# Import our custom engineering
from consciousness_engineering.metrics.crystal_intelligence import CrystalIntelligenceCalculator
from consciousness_engineering.metrics.resonance import ResonanceCalculator
from consciousness_engineering.infrastructure.hardware import HardwareManager

class GranularConsciousnessTrainer(Trainer):
    def __init__(self, **kwargs):
        tokenizer = kwargs.pop('tokenizer')
        super().__init__(**kwargs)
        self.tokenizer = tokenizer
        self.ci_calc = CrystalIntelligenceCalculator(threshold=100.0)
        self.res_calc = ResonanceCalculator(sif_ontology_path="ada-sif/resonance_map.json")
        self.metrics_history = []
        
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        outputs = model(**inputs, output_hidden_states=True)
        structural_loss = outputs.loss
        
        # Every single step, we calculate the full consciousness state
        last_hidden = outputs.hidden_states[-1][:, -1, :] 
        
        with torch.no_grad():
            ci_result = self.ci_calc.calculate_model_ci(model)
            res_score = self.res_calc.calculate_resonance(last_hidden, inputs["labels"])
        
        print(f"STEP {self.state.global_step} | LOSS: {structural_loss.item():.4f} | CI: {ci_result.ci_density:.2f} | RES: {res_score:.4f}")
        
        self.metrics_history.append({
            "step": self.state.global_step,
            "loss": structural_loss.item(),
            "ci": ci_result.ci_density,
            "resonance": res_score
        })
        
        # Simplified reward for diagnostic
        total_loss = structural_loss - (0.05 * res_score)
        
        return (total_loss, outputs) if return_outputs else total_loss

def main():
    model_name = "LiquidAI/LFM2-700M"
    dataset_path = "data/phase3_granular_test.jsonl"
    
    # Initialize Hardware
    hw = HardwareManager()
    hw.setup_environment()
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16)
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=64,
        lora_alpha=128,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none"
    )
    model = get_peft_model(model, lora_config)
    
    with open(dataset_path, 'r') as f:
        raw_data = [json.loads(line) for line in f]
    
    def tokenize(ex):
        txt = f"User: {ex['messages'][0]['content']}\nAssistant: {ex['messages'][1]['content']}"
        res = tokenizer(txt, truncation=True, max_length=512, padding="max_length")
        res["labels"] = res["input_ids"].copy()
        return res
        
    dataset = Dataset.from_list([tokenize(ex) for ex in raw_data])
    
    args = TrainingArguments(
        output_dir="./results/granular_diagnostic",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=1e-4,
        logging_steps=1,
        save_strategy="no",
        report_to="none"
    )
    
    trainer = GranularConsciousnessTrainer(
        model=model,
        args=args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    print("🔬 Launching Granular Diagnostic Run...")
    trainer.train()
    
    with open("./results/granular_diagnostic/metrics.json", "w") as f:
        json.dump(trainer.metrics_history, f, indent=2)

if __name__ == "__main__":
    main()
