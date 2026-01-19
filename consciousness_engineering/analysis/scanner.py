"""
Latent Scanner 🛰️
================
Extracts high-dimensional semantic states from models.

This module is responsible for:
1. Loading models (Base or LoRA).
2. Running inference on a "Probe Dataset".
3. Extracting hidden states (residual stream).
4. Formatting for projection (t-SNE/UMAP).

"We map the invisible to make it navigateable."
"""

import torch
from typing import List, Dict, Optional, Union, Tuple
import numpy as np
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

class LatentScanner:
    """
    Scans the latent space of a model using a probe dataset.
    """
    
    def __init__(self, 
                 model_name_or_path: str, 
                 device: str = "cuda" if torch.cuda.is_available() else "cpu",
                 dtype: torch.dtype = torch.float16):
        self.device = device
        self.dtype = dtype
        self.model_name = model_name_or_path
        
        print(f"🛰️  Allocating Scanner on {device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print(f"    Loading Model: {model_name_or_path}")
        # Determine if we need 4-bit (bitsandbytes) or standard load
        # For now, standard load for stability
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            torch_dtype=dtype,
            device_map=device,
            trust_remote_code=True
        )
        self.model.eval()
        print("    Scan Array Ready.")

    def load_adapter(self, adapter_path: str):
        """Load a LoRA adapter for scanning."""
        print(f"    Mounting LoRA Adapter: {adapter_path}")
        self.model = PeftModel.from_pretrained(self.model, adapter_path)
        self.model.eval()

    def scan(self, 
             prompts: List[str], 
             batch_size: int = 4,
             layer_idx: int = -1,
             pooling: str = "last") -> Tuple[np.ndarray, List[str]]:
        """
        Run the scan on the provided prompts.
        
        Args:
            prompts: List of text inputs to probe.
            batch_size: Inference batch size.
            layer_idx: Which layer to extract (-1 is last hidden state).
            pooling: 'last' (last token) or 'mean' (average of all tokens).
            
        Returns:
            (embeddings, prompts)
        """
        all_embeddings = []
        clean_prompts = [] # To keep track of what we actually processed
        
        print(f"    Scanning {len(prompts)} coordinates...")
        
        # Batch processing
        for i in tqdm(range(0, len(prompts), batch_size), desc="Scanning"):
            batch_texts = prompts[i : i + batch_size]
            
            try:
                inputs = self.tokenizer(
                    batch_texts, 
                    return_tensors="pt", 
                    padding=True, 
                    truncation=True, 
                    max_length=512
                ).to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(**inputs, output_hidden_states=True)
                    
                # Extract Hidden States
                # outputs.hidden_states is a tuple of (layer_0, ..., layer_N)
                # We usually want the last one (-1) or second to last
                hidden_state = outputs.hidden_states[layer_idx] # Shape: [batch, seq_len, dim]
                
                # Pooling Strategy
                batch_embeddings = []
                for j, text in enumerate(batch_texts):
                    # Get sequence length for this specific sample (attention mask)
                    mask = inputs.attention_mask[j]
                    valid_length = mask.sum().item()
                    
                    if pooling == "last":
                        # The last valid token (before padding)
                        # Note: In Llama-2/LFM architecture, this is usually valid_length - 1
                        vec = hidden_state[j, valid_length - 1, :].float().cpu().numpy()
                    elif pooling == "mean":
                        # Average of valid tokens
                        vec = hidden_state[j, :valid_length, :].mean(dim=0).float().cpu().numpy()
                    else:
                        raise ValueError(f"Unknown pooling method: {pooling}")
                        
                    batch_embeddings.append(vec)
                    clean_prompts.append(text)
                
                all_embeddings.extend(batch_embeddings)
                
            except Exception as e:
                print(f"⚠️  Sector Scan Error at index {i}: {e}")
                continue

        # Convert to single numpy matrix
        result_matrix = np.array(all_embeddings)
        print(f"✅ Scan Complete. Matrix Shape: {result_matrix.shape}")
        return result_matrix, clean_prompts
        
    def save_scan(self, embeddings: np.ndarray, prompts: List[str], output_path: str):
        """Save the raw scan data."""
        # We save as a dictionary: { "vectors": [...], "prompts": [...] }
        # Or separately. Let's do a simple .npz or .json wrapper.
        # Ideally, we want format compatible with the Projector.
        
        data = {
            "vectors": embeddings,
            "metadata": [{"label": p} for p in prompts]
        }
        
        # For numpy saving
        np.savez_compressed(output_path, vectors=embeddings, prompts=prompts)
        print(f"💾 Scan Data Saved to: {output_path}")

