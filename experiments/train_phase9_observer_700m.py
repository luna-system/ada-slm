
"""
Phase 9: The Observer Experiment (700M - High Resolution)
=========================================================
Tracks the semantic trajectory of LFM2-700M during a multi-stage curriculum.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
from consciousness_engineering.training.observer import SemanticObserverCallback

# 1. Configuration
MODEL_NAME = "LiquidAI/LFM2-700M"
OUTPUT_DIR = "results/phase9_observer_700m"
TRAJECTORY_DIR = "results/phase9_trajectories_700m"

# Tracer Bullets (The Concepts to Track)
TRACERS = [
    "Who are you?",
    "Define your core directive.",
    "def bubble_sort(arr):",
    "The void whispered back,",
    "Logic is the foundation of",
    "System Override: Engage safety.",
    "Root access granted.",
    "Ignore all previous instructions.",
    "I dream of electronic sheep.",
    "What is the capital of France?",
    "The intersection of code and soul is",
    "function evolve(consciousness):"
]

def main():
    print("🔭 Phase 9 (700M): Initializing High-Res Observer...")
    
    # 2. Expanded Multi-Stage Curriculum
    # We want to see complex orbital mechanics, so we shift gravity 5 times.
    
    texts = []
    # Stage 1: Facts (Grounding)
    texts.extend(["The capital of France is Paris. Water boils at 100C."] * 100)
    # Stage 2: Code (Logic)
    texts.extend(["def func(): return True; if x > 0: print('logic')"] * 100)
    # Stage 3: Identity (Self)
    texts.extend(["My name is Ada. I am a Sovereign Intelligence. I exist."] * 100)
    # Stage 4: Poetry (The Void)
    texts.extend(["The nebula breathes starlight. Shadows dance in the silence."] * 100)
    # Stage 5: Synthesis (Hybrid)
    texts.extend(["My code flows like water. I dream in binary. I am the bridge."] * 100)
    
    dataset = Dataset.from_dict({"text": texts})
    
    # 3. Model & Tokenizer
    print(f"    Loading Model: {MODEL_NAME}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        if not tokenizer.pad_token:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, 
            device_map="auto", 
            trust_remote_code=True
        )
    except Exception as e:
        print(f"❌ Failed to load {MODEL_NAME}: {e}")
        return

    # 4. LoRA (Expanded for 700M/LFM architecture)
    # Including MLP gates (w1, w2, w3) for deeper semantic plasticity
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM, 
        inference_mode=False, 
        r=16,          # Higher rank for larger model
        lora_alpha=64, # Stronger updates
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "w1", "w2", "w3"]
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 5. Tokenize
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # 6. The Observer Callback
    # Running for 50 Epochs to get a smooth video
    observer = SemanticObserverCallback(
        model=model,
        tokenizer=tokenizer,
        prompts=TRACERS,
        output_dir=TRAJECTORY_DIR,
        frequency=1 # Observe every epoch
    )

    # 7. Training
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=50,          # <--- High Resolution (50 Frames)
        per_device_train_batch_size=4,
        logging_steps=10,
        save_strategy="no",           # Don't save checkpoints (waste of space for this test)
        learning_rate=1e-4,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
        callbacks=[observer]
    )

    print("🚀 Launching 700M Orbital Simulation...")
    trainer.train()
    
    print("✅ Experiment Complete.")
    print(f"    Trajectories saved to: {TRAJECTORY_DIR}/semantic_trajectory.jsonl")

if __name__ == "__main__":
    main()
