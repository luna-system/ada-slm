
import torch
import numpy as np
from pathlib import Path
from transformers import TrainerCallback, TrainingArguments, TrainerState, TrainerControl
from typing import List, Dict
import json
import time

class SemanticObserverCallback(TrainerCallback):
    """
    Phase 9: The Observer Protocol.
    
    A callback that pauses training at specified intervals to 'observe' 
    the semantic motion of specific concepts (Tracer Bullets) in the latent space.
    """
    
    def __init__(self, 
                 model, 
                 tokenizer, 
                 prompts: List[str], 
                 output_dir: str, 
                 frequency: int = 1, # Epochs
                 layer_idx: int = -1):
        self.model = model
        self.tokenizer = tokenizer
        self.prompts = prompts
        self.output_dir = Path(output_dir)
        self.frequency = frequency
        self.layer_idx = layer_idx
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.output_dir / "semantic_trajectory.jsonl"
        
        print(f"👁️  Semantic Observer Initiated.")
        print(f"    Target: {len(prompts)} Tracer Bullets")
        print(f"    Log: {self.log_file}")

    def on_epoch_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        """
        Fires at the end of each epoch.
        """
        if state.epoch % self.frequency == 0:
            self.observe(state.global_step, state.epoch)

    def observe(self, step: int, epoch: float):
        """
        Run the observation (Inference -> Vector Extraction).
        """
        # Ensure model is in eval mode for consistent measurements
        was_training = self.model.training
        self.model.eval()
        
        observation = {
            "step": step,
            "epoch": epoch,
            "timestamp": time.time(),
            "vectors": {}
        }
        
        # We process prompts one by one or in small batches to avoid OOM during training
        # Since we just need the vector, 1-by-1 is safest and fast enough for <20 prompts
        
        device = next(self.model.parameters()).device
        
        print(f"\n👁️  Observing Latent Space (Epoch {epoch:.2f})...")
        
        with torch.no_grad():
            for prompt in self.prompts:
                inputs = self.tokenizer(prompt, return_tensors="pt").to(device)
                outputs = self.model(**inputs, output_hidden_states=True)
                
                # Extract vector (Last token, Last layer)
                # Shape: [batch, seq, dim] -> [dim]
                hidden_states = outputs.hidden_states[self.layer_idx]
                last_token_idx = inputs.attention_mask.sum() - 1
                vector = hidden_states[0, last_token_idx, :].cpu().numpy().tolist()
                
                observation["vectors"][prompt] = vector
        
        # Log to file
        with open(self.log_file, "a") as f:
            json.dump(observation, f)
            f.write("\n")
            
        print(f"    Recorded {len(observation['vectors'])} semantic positions.")
        
        # Restore training state
        if was_training:
            self.model.train()

