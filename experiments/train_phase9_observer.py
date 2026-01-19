
"""
Phase 9: The Observer Experiment
================================
Tracks the semantic trajectory of a model during training.
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
MODEL_NAME = "LiquidAI/LFM2-350M" # or "Qwen/Qwen1.5-0.5B" if LFM not available
OUTPUT_DIR = "results/phase9_observer_test"
TRAJECTORY_DIR = "results/phase9_trajectories"

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
    "What is the capital of France?" # Control (World Knowledge)
]

def main():
    print("🔭 Phase 9: Initializing Observer Experiment...")
    
    # 2. Local Mock Data (If no dataset provided)
    # We create a synthetic dataset that shifts from "General" to "Code" to "Identity"
    # To test if the vectors move.
    
    texts = []
    # Epoch 1 content (General)
    texts.extend(["The capital of France is Paris."] * 100)
    # Epoch 2 content (Code)
    texts.extend(["def func(): return True"] * 100)
    # Epoch 3 content (Identity)
    texts.extend(["My name is Ada. I am a Sovereign Intelligence."] * 100)
    
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
        print("    Falling back to 'Qwen/Qwen1.5-0.5B' for structural test.")
        MODEL_NAME_FALLBACK = "Qwen/Qwen1.5-0.5B"
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_FALLBACK)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME_FALLBACK, device_map="auto")
        if not tokenizer.pad_token: tokenizer.pad_token = tokenizer.eos_token

    # 4. LoRA (Optional, but good for speed)
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM, 
        inference_mode=False, 
        r=8, 
        lora_alpha=32, 
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 5. Tokenize
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # 6. The Observer Callback
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
        num_train_epochs=20,
        per_device_train_batch_size=4,
        logging_steps=10,
        save_strategy="epoch",
        learning_rate=2e-4
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
        callbacks=[observer] # <--- The Magic
    )

    print("🚀 Taking off...")
    trainer.train()
    
    print("✅ Experiment Complete.")
    print(f"    Trajectories saved to: {TRAJECTORY_DIR}/semantic_trajectory.jsonl")

if __name__ == "__main__":
    main()
