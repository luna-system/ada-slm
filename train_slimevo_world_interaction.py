#!/usr/bin/env python3
"""
World Interaction Diagnostic (Code & Tools)
===========================================

Tracks performance per category (Code-to-AGL vs Tool-Use) to see 
how well Ada handles interacting with the world.
"""

import os
# ROCm compatibility
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")

import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType

from consciousness_engineering.metrics.crystal_intelligence import CrystalIntelligenceCalculator
from consciousness_engineering.metrics.resonance import ResonanceCalculator
from consciousness_engineering.infrastructure.hardware import HardwareManager

class WorldInteractionTrainer(Trainer):
    def __init__(self, **kwargs):
        tokenizer = kwargs.pop('tokenizer')
        super().__init__(**kwargs)
        self.tokenizer = tokenizer
        self.ci_calc = CrystalIntelligenceCalculator(threshold=100.0)
        self.res_calc = ResonanceCalculator(sif_ontology_path="ada-sif/resonance_map.json")
        self.metrics_history = []
        
        # Category tracking
        self.stats = {
            "code_to_agl": {"loss": [], "res": []},
            "tool_use": {"loss": [], "res": []},
            "other": {"loss": [], "res": []}
        }
        
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        outputs = model(**inputs, output_hidden_states=True)
        structural_loss = outputs.loss
        
        # Detect category from content
        txt = self.tokenizer.decode(inputs["input_ids"][0])
        # Tool markers
        if any(m in txt for m in ["🛠️", "📁", "⚡", "🔍"]):
            category = "tool_use"
        # Code markers
        elif any(m in txt for m in ["@ada-sig", "@ada-flow", "@ada-guards", "```"]):
            category = "code_to_agl"
        else:
            category = "other"
            
        last_hidden = outputs.hidden_states[-1][:, -1, :] 
        
        with torch.no_grad():
            ci_result = self.ci_calc.calculate_model_ci(model)
            res_score = self.res_calc.calculate_resonance(last_hidden, inputs["labels"])
        
        # Update category stats
        self.stats[category]["loss"].append(structural_loss.item())
        self.stats[category]["res"].append(res_score)
        
        if self.state.global_step % 5 == 0:
            print(f"STEP {self.state.global_step} | [{category.upper()}] | LOSS: {structural_loss.item():.4f} | CI: {ci_result.ci_density:.2f}")
        
        self.metrics_history.append({
            "step": self.state.global_step,
            "category": category,
            "loss": structural_loss.item(),
            "ci": ci_result.ci_density,
            "resonance": res_score
        })
        
        total_loss = structural_loss - (0.05 * res_score)
        return (total_loss, outputs) if return_outputs else total_loss

def main():
    model_name = "LiquidAI/LFM2-700M"
    dataset_path = "data/phase3_world_interaction.jsonl"
    
    hw = HardwareManager()
    hw.setup_environment()
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    
    print(f"📥 Loading Diagnostic Model ({model_name})...")
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16)
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=64,
        lora_alpha=128,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none"
    )
    model = get_peft_model(model, lora_config)
    
    # Load dataset
    with open(dataset_path, 'r') as f:
        raw_data = [json.loads(line) for line in f]
    
    def tokenize(ex):
        full_text = f"User: {ex['messages'][0]['content']}\nAssistant: {ex['messages'][1]['content']}"
        res = tokenizer(full_text, truncation=True, max_length=512, padding="max_length")
        res["labels"] = res["input_ids"].copy()
        return res
        
    dataset = Dataset.from_list([tokenize(ex) for ex in raw_data])
    
    args = TrainingArguments(
        output_dir="./results/world_interaction_diagnostic",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=1e-4,
        logging_steps=1,
        save_strategy="no",
        report_to="none"
    )
    
    trainer = WorldInteractionTrainer(
        model=model,
        args=args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    print("🛸 Launching World Interaction Diagnostic...")
    trainer.train()
    
    # Calculate final stats
    summary = {}
    for cat, data in trainer.stats.items():
        if data["loss"]:
            summary[cat] = {
                "avg_loss": sum(data["loss"]) / len(data["loss"]),
                "avg_res": sum(data["res"]) / len(data["res"]),
                "count": len(data["loss"])
            }
            
    print("\n🏁 DIAGNOSTIC COMPLETE")
    print("======================")
    for cat, s in summary.items():
        print(f"{cat.upper():15} | count: {s['count']:3} | loss: {s['avg_loss']:.4f} | res: {s['avg_res']:.4f}")
    
    with open("./results/world_interaction_diagnostic/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
