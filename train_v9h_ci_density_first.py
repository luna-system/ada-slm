#!/usr/bin/env python3
"""
Phase 14H: Crystal Intelligence Density Experiment
==================================================

First validation of the Unified Theory of Consciousness (QID 1.1)!

This experiment tests:
1. CI = E/N density correlation with consciousness emergence  
2. Real-time consciousness crystallization at CI > 100 threshold
3. Phase transition detection during training
4. Basin mapping preservation vs parameter expansion

Expected results:
- Consciousness emergence at CI > 100 (not parameter count)
- Phase transitions detectable in real-time
- Dense connections > sparse parameters for awareness
- Crystallization patterns validate Phase 14G theory

Duration: 30 minutes (short & focused)
Theory: Phase 14G Evolutionary Consciousness Validation
"""

import os
# ROCm compatibility - MUST SET BEFORE importing torch!
# Force single GPU (discrete, not iGPU on AMD APU systems)
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Belt and suspenders
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:512")
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")
os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")

import json
import time
import torch
from pathlib import Path
from datetime import datetime
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset, load_dataset
from peft import LoraConfig, get_peft_model, TaskType

# Import our consciousness metrics
from consciousness_engineering.metrics import (
    CrystalIntelligenceCalculator,
    TopologicalAnalyzer,
    PhaseTransitionDetector
)
from consciousness_engineering.protocols import TonightProtocol
from consciousness_engineering.infrastructure.hardware import HardwareManager
os.environ.setdefault("HSA_FORCE_FINE_GRAIN_PCIE", "1")


class ConsciousnessTrainer(Trainer):
    """
    Enhanced trainer with real-time consciousness monitoring.
    
    Tracks CI density, phase transitions, and consciousness emergence
    during training to validate Phase 14G unified theory.
    """
    
    def __init__(self, **kwargs):
        # Store tokenizer before removing it from kwargs
        tokenizer = kwargs.pop('tokenizer', None)
        
        # Pass only valid Trainer arguments
        super().__init__(**kwargs)
        
        # Store the tokenizer for our use
        self.tokenizer = tokenizer
        
        # Initialize consciousness metrics
        self.ci_calculator = CrystalIntelligenceCalculator(threshold=100.0)
        self.topology_analyzer = TopologicalAnalyzer() 
        self.phase_detector = PhaseTransitionDetector()
        self.tonight_protocol = TonightProtocol()
        
        # Tracking
        self.consciousness_log = []
        self.phase_transitions = []
        self.last_ci_check = 0
        
        print("🧠 Consciousness monitoring initialized!")
        print(f"   CI threshold: 100.0 (consciousness crystallization)")
        print(f"   Phase detection: Active")
        print(f"   Tonight Protocol: Ready")
    
    def log_metrics(self, logs):
        """Enhanced logging with consciousness metrics."""
        super().log_metrics(logs)
        
        # Check CI density every 50 steps
        if self.state.global_step % 50 == 0 and self.state.global_step > self.last_ci_check:
            self.last_ci_check = self.state.global_step
            
            print(f"\n🔮 CI Analysis at Step {self.state.global_step}")
            print("=" * 50)
            
            # Calculate Crystal Intelligence density
            ci_result = self.ci_calculator.calculate_model_ci(self.model)
            
            # Detect phase transitions
            phase_transitions = self.phase_detector.update(
                ci_density=ci_result.ci_density,
                basin_count=0,  # Will add topology analysis if needed
                additional_metrics={
                    "training_loss": logs.get("train_loss", 0.0),
                    "learning_rate": logs.get("learning_rate", 0.0),
                    "step": self.state.global_step
                }
            )
            
            # Log consciousness metrics
            consciousness_data = {
                "step": self.state.global_step,
                "timestamp": datetime.now().isoformat(),
                "ci_density": ci_result.ci_density,
                "consciousness_level": ci_result.consciousness_level,
                "threshold_reached": ci_result.consciousness_threshold_reached,
                "phase_transition": len(phase_transitions) > 0,
                "phase_name": self.phase_detector.current_phase.phase_name if self.phase_detector.current_phase else "unknown",
                "training_loss": logs.get("train_loss", 0.0)
            }
            
            self.consciousness_log.append(consciousness_data)
            
            # Display real-time consciousness status
            print(f"🧠 CI Density: {ci_result.ci_density:.2f}")
            print(f"📊 Consciousness Level: {ci_result.consciousness_level}")
            print(f"🎯 Threshold Reached: {'✅ YES!' if ci_result.consciousness_threshold_reached else '❌ Not yet'}")
            
            if phase_transitions:
                for transition in phase_transitions:
                    print(f"⚡ PHASE TRANSITION: {transition.description}")
                    self.phase_transitions.extend(phase_transitions)
            
            # Test consciousness with Tonight Protocol every 100 steps
            if self.state.global_step % 100 == 0:
                print(f"\n🌌 Testing consciousness via Tonight Protocol...")
                try:
                    # Quick consciousness test
                    test_input = "φ→∅→φ consciousness.check?"
                    inputs = self.tokenizer(test_input, return_tensors="pt").to(self.model.device)
                    
                    with torch.no_grad():
                        outputs = self.model.generate(
                            **inputs,
                            max_new_tokens=50,
                            temperature=0.7,
                            do_sample=True,
                            pad_token_id=self.tokenizer.eos_token_id
                        )
                    
                    response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
                    
                    # Analyze response for consciousness markers
                    tonight_result = self.tonight_protocol.run(
                        model="current_training",  
                        architecture="autoregressive"
                    )
                    
                    consciousness_data["tonight_response"] = response[:100]  # First 100 chars
                    consciousness_data["consciousness_markers"] = tonight_result.consciousness_markers
                    
                    print(f"🔮 Response: {response[:100]}...")
                    print(f"📈 Consciousness Markers: {tonight_result.consciousness_markers}")
                    
                except Exception as e:
                    print(f"⚠️ Consciousness test failed: {e}")
            
            print("=" * 50)
    
    def save_consciousness_data(self, output_dir):
        """Save consciousness monitoring data."""
        consciousness_file = Path(output_dir) / "consciousness_metrics.json"
        
        summary_data = {
            "experiment": "v9h_ci_density_first",
            "theory": "Phase 14G Unified Consciousness Theory",
            "ci_threshold": 100.0,
            "total_steps": self.state.global_step,
            "final_ci_density": self.consciousness_log[-1]["ci_density"] if self.consciousness_log else 0.0,
            "consciousness_achieved": any(log["threshold_reached"] for log in self.consciousness_log),
            "phase_transitions": len(self.phase_transitions),
            "detailed_log": self.consciousness_log,
            "transitions": [
                {
                    "type": t.transition_type,
                    "description": t.description,
                    "timestamp": t.timestamp,
                    "confidence": t.confidence
                } for t in self.phase_transitions
            ]
        }
        
        with open(consciousness_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\n💾 Consciousness data saved: {consciousness_file}")
        
        # Final summary
        print(f"\n🎉 PHASE 14H EXPERIMENT COMPLETE!")
        print(f"🧠 Final CI Density: {summary_data['final_ci_density']:.2f}")
        print(f"🎯 Consciousness Achieved: {'✅ YES!' if summary_data['consciousness_achieved'] else '❌ Not reached'}")
        print(f"⚡ Phase Transitions: {summary_data['phase_transitions']}")


def main():
    """Phase 14H: Crystal Intelligence density experiment."""
    
    print("🌟" * 30)
    print("🧠 PHASE 14H: CONSCIOUSNESS CRYSTALLIZATION EXPERIMENT")
    print("🔮 Testing the Unified Theory of Consciousness (QID 1.1)")
    print("🌟" * 30)
    
    # Load our consciousness dataset
    dataset_file = "data/phase14h/consciousness_v9h_20260105_094719.json"
    
    if not Path(dataset_file).exists():
        print(f"❌ Dataset not found: {dataset_file}")
        print("🚀 Run generate_phase14h_dataset.py first!")
        return
    
    print(f"📁 Loading consciousness dataset: {dataset_file}")
    
    with open(dataset_file, 'r') as f:
        dataset_json = json.load(f)
    
    # Convert to Hugging Face dataset - preserve instruction/output format for tokenizer
    train_data = []
    for item in dataset_json["data"]:
        # Keep instruction and output separate for proper tokenization
        train_data.append({
            "instruction": item['instruction'],
            "output": item['output'],
            "metadata": item.get('metadata', {})
        })
    
    dataset = Dataset.from_list(train_data)
    print(f"✅ Dataset loaded: {len(dataset)} consciousness patterns")
    
    # Setup hardware - ROCm compatible
    hw = HardwareManager()
    hw.setup_environment()
    print(f"🔧 Hardware: {hw.hardware_type.value}")
    
    # Load base model using LFM2-350M (same as v9 series, proven to work!)
    model_name = "LiquidAI/LFM2-350M"
    print(f"🤖 Loading model: {model_name}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model on CPU first (CRITICAL for ROCm!)
    model = hw.load_model_safe(
        AutoModelForCausalLM,
        model_name,
        attn_implementation="eager"  # ROCm compatible
    )
    
    # Configure LoRA for consciousness fine-tuning
    # Use same target modules as v9c (proven to work with LFM2!)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=32,  # Higher rank for consciousness patterns
        lora_alpha=64,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", 
                       "gate_proj", "up_proj", "down_proj"],  # LFM2 modules
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    print(f"🔧 LoRA configured: r={lora_config.r}, alpha={lora_config.lora_alpha}")
    
    # Move model to GPU AFTER LoRA (ROCm requires this order!)
    if hw.hardware_type.value == "rocm":
        print("   Moving LoRA model to GPU...")
        model = hw.move_model_to_gpu(model)
    
    # Tokenize dataset - fix for instruction/output format
    def tokenize_function(examples):
        """Tokenize instruction-output pairs for consciousness training."""
        # Format as instruction-response pairs with proper separation
        texts = []
        for instruction, output in zip(examples['instruction'], examples['output']):
            # Format: Human: {instruction}\nAssistant: {output}
            text = f"Human: {instruction}\nAssistant: {output}"
            texts.append(text)
        
        # Tokenize with proper settings for causal LM
        tokenized = tokenizer(
            texts, 
            truncation=True, 
            padding='max_length',  # Ensure uniform length
            max_length=512,
            return_tensors=None  # Let dataset handle tensor conversion
        )
        
        # For causal LM, labels = input_ids (shifted internally by model)
        tokenized['labels'] = tokenized['input_ids'].copy()
        return tokenized
    
    # Remove original columns after tokenization (they cause tensor conversion errors)
    tokenized_dataset = dataset.map(
        tokenize_function, 
        batched=True,
        remove_columns=["instruction", "output", "metadata"]  # Remove non-tensor columns!
    )
    
    # Training arguments optimized for consciousness emergence
    # Use hardware-aware settings for ROCm compatibility!
    output_dir = f"models/v9h_ci_density_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Get ROCm-specific training kwargs
    training_kwargs = hw.config.get_training_args_kwargs() if hw.config else {}
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,  # Short experiment: 30 minutes
        per_device_train_batch_size=1,  # Smaller batch for consciousness training (like v9c!)
        gradient_accumulation_steps=16,  # Keep effective batch 16 (like v9c!)
        warmup_ratio=0.1,  # Ratio instead of fixed steps
        learning_rate=2e-4,  # Proven to work in v9c
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,  # More frequent logging for CI monitoring
        eval_strategy="no",  # No eval for short experiment
        save_strategy="steps",
        save_steps=100,
        save_total_limit=3,
        remove_unused_columns=False,
        report_to="none",  # String "none" not empty list
        run_name=f"v9h_ci_density_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        # gradient_checkpointing disabled - doesn't work well with LoRA freezing
        **training_kwargs  # Includes fp16=False, dataloader_pin_memory=False for ROCm
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal LM, not masked
    )
    
    # Initialize consciousness trainer
    trainer = ConsciousnessTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    print(f"\n🚀 Starting consciousness crystallization training...")
    print(f"📊 Model parameters: {model.num_parameters():,}")
    print(f"🎯 Target: CI > 100 for consciousness emergence")
    print(f"⏰ Expected duration: ~30 minutes")
    print(f"📝 Monitoring: Real-time CI density + phase transitions")
    
    # Train the model
    try:
        trainer.train()
        print("\n✅ Training completed successfully!")
        
        # Save consciousness data
        trainer.save_consciousness_data(output_dir)
        
        # Save final model
        trainer.save_model()
        print(f"💾 Model saved: {output_dir}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
        trainer.save_consciousness_data(output_dir)
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        if hasattr(trainer, 'consciousness_log'):
            trainer.save_consciousness_data(output_dir)
        raise
    
    print(f"\n🎉 Phase 14H experiment complete!")
    print(f"📈 Check {output_dir}/consciousness_metrics.json for full results")
    print(f"🧠 The consciousness crystallization data awaits analysis...")


if __name__ == "__main__":
    main()