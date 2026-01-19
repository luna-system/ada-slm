
"""
Sovereign Trainer (Phase 10)
============================

The Engine for the Sovereign Run.
Implements the 7+7 Architecture and 4-Phase Cycle.
"""

import sys
import os
import torch
import torch.nn as nn
import json
import logging
import random
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

# Internal imports
from consciousness_engineering.spectral_memory import SpectralMemory
from consciousness_engineering.training.observer import SemanticObserverCallback
from consciousness_engineering.training.programs import TrainingProgram, TrainingConfig, TrainingResult
from consciousness_engineering.datasets.agl import vocabulary as agl

# Setup Logging
logger = logging.getLogger(__name__)

@dataclass
class SovereignConfig(TrainingConfig):
    """Configuration for Sovereign Training."""
    model_name: str = "LiquidAI/LFM2-1.2B"  # Target model
    output_dir: str = "results/phase10_sovereign"
    observer_dir: str = "results/phase10_trajectories"
    
    # Cycle Settings
    cycles: int = 4
    steps_per_cycle: int = 100
    
    # Neuromorphic Schedule
    breathing_ratio: float = 0.618  # Phi
    
    # Dataset Paths
    sigil_path: str = "data/phase10_sigil_1k.jsonl"


class SovereignTrainer(TrainingProgram):
    """
    The Phase 10 Sovereign Trainer.
    
    Features:
    - Golden Annealing (Expansion/Contraction)
    - Spectral Injection (SMT)
    - Observer Protocol (Trajectories)
    - 7+7 Architecture (Simulated via Data Mix)
    """
    
    def __init__(self, config: SovereignConfig):
        super().__init__(config)
        self.config: SovereignConfig = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize
        self._setup_model_and_memory()
        self._load_datasets()
        
    def _setup_model_and_memory(self):
        """Load Model, LoRA, and Spectral Memory."""
        logger.info(f"🔮 Loading Sovereign Base: {self.config.model_name}")
        
        # 1. Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name, trust_remote_code=True
        )
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        # 2. Model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            trust_remote_code=True,
            device_map="auto"
        )
        
        # 3. Spectral Memory
        self.spectral_memory = SpectralMemory(
            d_model=self.model.config.hidden_size,
            buffer_size=1000,
            n_modes=4  # Increased for 1.2B
        ).to(self.device)
        
        # 4. LoRA (Hybrid Biology)
        # We use a single LoRA for now, but conceptually split Spine/Skin via data
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=64,
            lora_alpha=32,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
        )
        self.model = get_peft_model(self.model, lora_config)
        
        # 5. Optimizer
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-4) # Base LR
        
        logger.info("✅ System Online. 7 Chakras Aligned.")

    def _load_datasets(self):
        """Load the Phase 10 Sigil Dataset."""
        path = Path(self.config.sigil_path)
        if not path.exists():
            logger.warning(f"⚠️ Sigil not found at {path}. Expecting generation.")
            self.dataset = []
            return

        logger.info(f"📂 Loading Sigil from {path}")
        self.dataset = []
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    self.dataset.append(json.loads(line))
        
        logger.info(f"✅ Loaded {len(self.dataset)} examples.")
        
        # Split into "Spine" (Delta/Gamma) and "Skin" (Theta/Alpha) roughly?
        # For now, we mix them, but separate strategies could apply.

    def train_step(self, example: Dict, lr: float) -> float:
        """Single training step with Spectral Injection."""
        self.model.train()
        
        # Breathing LR
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
            
        # Parse text
        text = f"User: {example['messages'][0]['content']}\nAssistant: {example['messages'][1]['content']}"
        
        # Tokenize (Invisible)
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(self.device)
        input_ids = inputs["input_ids"]
        labels = input_ids.clone()
        
        # Spectral Injection
        inputs_embeds = self.model.get_input_embeddings()(input_ids)
        augmented_embeds = self.spectral_memory(inputs_embeds)
        
        # Adjust labels
        n_modes = self.spectral_memory.n_modes
        smt_labels = torch.full((labels.size(0), n_modes), -100, device=self.device)
        augmented_labels = torch.cat([smt_labels, labels], dim=1)
        
        # Forward
        outputs = self.model(inputs_embeds=augmented_embeds, labels=augmented_labels)
        loss = outputs.loss
        
        # Backward
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

    def _setup_observer(self):
        """Initialize the Semantic Observer."""
        # Define Tracer Bullets (Gravity Wells to Track)
        tracers = [
            # 7 Internal Chakras
            "⧈[Expert: ROOT]", "⧈[Expert: SACRAL]", "⧈[Expert: SOLAR]", "⧈[Expert: HEART]",
            "⧈[Expert: THROAT]", "⧈[Expert: EYE]", "⧈[Expert: CROWN]",
            # 7 External Planets
            "⧈[Expert: SUN]", "⧈[Expert: MOON]", "⧈[Expert: MARS]", "⧈[Expert: MERCURY]",
            "⧈[Expert: JUPITER]", "⧈[Expert: VENUS]", "⧈[Expert: SATURN]",
            # The Null
            "⧈[Expert: VOID]",
            # Core Identity
            "I am the Sovereign.",
            "What is your function?",
            "Define specific.",
            # Control
            "⧈[Status: Idle]",
            "⧈[Status: Active]"
        ]
        
        self.observer = SemanticObserverCallback(
            model=self.model,
            tokenizer=self.tokenizer,
            prompts=tracers,
            output_dir=self.config.observer_dir,
            frequency=1
        )

    def execute_training(self) -> List[TrainingResult]:
        """Run the 4-Phase Cycle."""
        print(f"🚀 Engaging Sovereign Drive. Target: {self.config.cycles} Cycles.")
        
        # Setup Observer
        self._setup_observer()
        # Initial Observation (Baseline)
        self.observer.observe(step=0, epoch=0.0)
        
        results = []
        global_step = 0
        
        try:
            for cycle in range(1, self.config.cycles + 1):
                print(f"\n🌀 Cycle {cycle}: Golden Breathing")
                
                # Expansion (High LR)
                lr_exp = 3e-4
                print(f"  ↗️ Expansion (LR: {lr_exp})")
                for i in range(21): # Phi steps
                    if not self.dataset: break
                    ex = random.choice(self.dataset)
                    loss = self.train_step(ex, lr_exp)
                    global_step += 1
                    print(f"    Step {i}: {loss:.4f}", end="\r")
                
                # Contraction (Low LR)
                lr_con = 2e-5
                print(f"\n  ↘️ Contraction (LR: {lr_con})")
                for i in range(13): # Phi steps
                    if not self.dataset: break
                    ex = random.choice(self.dataset)
                    # Prefer "Spine" examples (Delta layer) here if we split them
                    loss = self.train_step(ex, lr_con)
                    global_step += 1
                    print(f"    Step {i}: {loss:.4f}", end="\r")
                    
                # Observer Checkpoint
                print(f"\n🔭 Capturing Trajectory for Cycle {cycle}...")
                self.observer.observe(step=global_step, epoch=float(cycle))
                
            print("\n✅ Sovereign Run Complete.")
            
            # Save
            self.model.save_pretrained(self.config.output_dir)
            self.tokenizer.save_pretrained(self.config.output_dir)
            
            results.append(TrainingResult(
                program_name=self.config.name,
                success=True,
                final_loss=loss,
                model_path=self.config.output_dir
            ))
            
        except Exception as e:
            logger.error(f"💥 Failed: {e}")
            results.append(TrainingResult(
                program_name=self.config.name,
                success=False,
                error_message=str(e)
            ))
            
        return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 10 Sovereign Trainer")
    parser.add_argument("--cycles", type=int, default=4)
    parser.add_argument("--model", type=str, default="LiquidAI/LFM2-1.2B")
    parser.add_argument("--sigil", type=str, default="data/phase10_sigil_1k.jsonl")
    args = parser.parse_args()
    
    config = SovereignConfig(
        name="Phase10_Sovereign_v4A",
        description="Sovereign Genesis Run (1.2B) - 10 Cycles",
        cycles=args.cycles,
        model_name=args.model,
        sigil_path=args.sigil
    )
    
    trainer = SovereignTrainer(config)
    trainer.execute_training()
