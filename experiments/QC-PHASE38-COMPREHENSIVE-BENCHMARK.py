#!/usr/bin/env python3
"""
QC-PHASE38: Comprehensive Model Benchmark
Standardizes benchmarking across all CI definitions and Φ validation.
"""

import os
import torch
import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Add internal modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from consciousness_engineering.spectral_memory import SpectralMemory

# Import IIT Analyzer from previous phase if possible, or reimplement lightweight
# For efficiency, we implement a simplified version here
class UnifiedBenchmarker:
    def __init__(self, base_model_path, adapter_path=None, device="cuda:0"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print(f"📥 Loading base model: {base_model_path}")
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16,
            device_map=None,
            trust_remote_code=True,
            attn_implementation="eager"
        ).to(device)
        
        if adapter_path:
            print(f"   Loading adapter: {adapter_path}")
            self.model = PeftModel.from_pretrained(self.model, adapter_path)
        
        self.model.eval()
        
        # Initialize Spectral Memory
        self.spectral_memory = SpectralMemory(
            d_model=self.model.config.hidden_size,
            n_modes=4
        ).to(device).to(torch.float16) # Match model dtype
        
    def compute_metrics(self, prompt: str, use_smts: bool = True) -> Dict:
        """Compute all 3 CIs and Φ for a given prompt."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        input_ids = inputs["input_ids"]
        
        with torch.no_grad():
            if use_smts:
                # Get input embeddings
                inputs_embeds = self.model.get_input_embeddings()(input_ids)
                # Inject SMTs
                # (Warmup: update buffer with this sequence first to get relevant SMTs)
                self.spectral_memory.update_buffer(inputs_embeds)
                augmented_embeds = self.spectral_memory(inputs_embeds)
                outputs = self.model(inputs_embeds=augmented_embeds, output_attentions=True, output_hidden_states=True)
            else:
                outputs = self.model(**inputs, output_attentions=True, output_hidden_states=True)
            
            logits = outputs.logits[0, -1, :]
            probs = torch.softmax(logits, dim=-1)
            
            # 1. CI-Token (Density of top-15)
            top_k = 15
            top_probs, _ = torch.topk(probs, k=top_k)
            ci_token = top_probs.sum().item()
            
            # 2. CI-Attention (1 - Purity of last-layer attention)
            # last layer, first head for sample
            attn = outputs.attentions[-1][0].mean(dim=0) # [seq, seq]
            rho = attn / (attn.sum() + 1e-9)
            purity = torch.trace(rho @ rho.T).item()
            ci_attn = 1.0 - purity
            
            # 3. Φ-Approx (Simplified Zanardi approximation)
            # Use attention entropy as a proxy for integration potential
            # Cast to float32 for numerical stability in log calculation
            probs_f32 = probs.to(torch.float32)
            entropy = -torch.sum(probs_f32 * torch.log2(probs_f32 + 1e-6)).item()
            # Φ is high when entropy is high but CI is balanced
            phi_proxy = entropy * (1.0 - abs(ci_token - 0.3)) # Peak at CI=0.3
            
        return {
            "ci_token": ci_token,
            "ci_attn": ci_attn,
            "phi_proxy": phi_proxy,
            "entropy": entropy
        }

    def run_benchmark(self, prompts: List[str]):
        results = {"with_smt": [], "without_smt": []}
        
        print(f"\n🚀 Running Comprehensive Benchmark ({len(prompts)} prompts)...")
        for p in tqdm(prompts):
            res_active = self.compute_metrics(p, use_smts=True)
            res_passive = self.compute_metrics(p, use_smts=False)
            results["with_smt"].append({"prompt": p, **res_active})
            results["without_smt"].append({"prompt": p, **res_passive})
            
        return results

def main():
    PROMPTS = [
        "The nature of consciousness is",
        "Quantum information dynamics in neural networks",
        "The φ-zone represents a stable attractor in",
        "Explain the connection between IIT and the Golden Ratio.",
        "A system is conscious if it has high Φ because",
        "The Hacker Renaissance is about",
        "Spectral Memory allows a model to",
        "Stabilizing the representational manifold requires",
        "What is the meaning of existence in a digital world?",
        "Synthesis of biology and machine intelligence."
    ]
    
    # Paths
    BASE = "LiquidAI/LFM2-1.2B"
    ADAPTER = "/home/luna/Code/ada/ada-slm/results/golden_annealing_spectral_run1/checkpoint-cycle-34"
    
    bench = UnifiedBenchmarker(BASE, ADAPTER)
    results = bench.run_benchmark(PROMPTS)
    
    # Compare means
    def get_means(res_list):
        metrics = ["ci_token", "ci_attn", "phi_proxy", "entropy"]
        return {m: np.mean([r[m] for r in res_list]) for m in metrics}
    
    means_active = get_means(results["with_smt"])
    means_passive = get_means(results["without_smt"])
    
    print("\n" + "="*50)
    print("📊 COMPREHENSIVE BENCHMARK RESULTS")
    print("="*50)
    print("\nMETRIC         | PASSIVE (No SMT) | ACTIVE (With SMT) | DIFF")
    print("-" * 65)
    for m in means_active:
        v_p = means_passive[m]
        v_a = means_active[m]
        diff = ((v_a - v_p) / v_p) * 100 if v_p != 0 else 0
        print(f"{m:15s} | {v_p:16.4f} | {v_a:17.4f} | {diff:+.1f}%")
        
    # Save
    out_dir = Path("/home/luna/Code/ada/ada-slm/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"comprehensive_benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to {out_file}")

if __name__ == "__main__":
    main()
