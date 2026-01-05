#!/usr/bin/env python3
"""
Eigenvalue Analysis for ada-slm-v9A-lfm2

Phase 14: First eigenvalue extraction from LFM2 hybrid architecture!
Questions to answer:
1. How do LFM2's eigenvalues differ from pure transformer models?
2. Does the 0.676 fractal dimension show up in eigenvalue patterns?
3. What does the spatial conv + temporal attn hybrid look like spectrally?
"""

import torch
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Paths
BASE_MODEL = "LiquidAI/LFM2-350M"
ADAPTER_PATH = Path(__file__).parent / "exports/phase14_lfm2_real/final_model"
OUTPUT_DIR = Path(__file__).parent / "exports/phase14_lfm2_real"

# Test prompts - same as Phase 5A for comparison
TEST_PROMPTS = [
    # Simple
    "Hello",
    "What is consciousness?",
    
    # Tool-like (model was trained on these)
    "I need to search for something",
    "Can you help me calculate",
    
    # Chain-of-thought (best training phase!)
    "Let me think step by step about this problem",
    "First, I'll consider the options. Then, I'll evaluate each one.",
    
    # AGL consciousness patterns
    "φ●∴ WITNESS ∴●φ",
    "The bridge between observer and observed",
    
    # Creative/poetic
    "The dance between midnight and the awake is where meaning lives",
]


def extract_eigenvalues(model, tokenizer, prompt: str, device: str = "cpu") -> dict:
    """Extract eigenvalue metrics from attention matrices."""
    model.eval()
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_attentions=True, return_dict=True)
    
    # Check if we have attention outputs
    if outputs.attentions is None:
        return {"error": "No attention outputs available", "prompt": prompt}
    
    results = {
        "prompt": prompt,
        "prompt_length": len(inputs['input_ids'][0]),
        "num_attention_layers": len(outputs.attentions),
        "layers": []
    }
    
    # Analyze each attention layer
    for layer_idx, attn_tensor in enumerate(outputs.attentions):
        # attn_tensor shape: [batch, heads, seq, seq]
        batch_size, num_heads, seq_len, _ = attn_tensor.shape
        
        layer_results = {
            "layer_idx": layer_idx,
            "shape": list(attn_tensor.shape),
            "heads": []
        }
        
        # Analyze each attention head
        for head_idx in range(min(num_heads, 4)):  # First 4 heads for speed
            attn = attn_tensor[0, head_idx].cpu().numpy()
            
            # Compute eigenvalues
            try:
                eigenvalues = np.linalg.eigvals(attn)
                magnitudes = np.abs(eigenvalues)
                magnitudes = np.sort(magnitudes)[::-1]  # Descending
                
                # Key metrics
                head_results = {
                    "head_idx": head_idx,
                    "top_3_eigenvalues": magnitudes[:3].tolist(),
                    "eigenvalue_sum": float(magnitudes.sum()),
                    "dominant_ratio": float(magnitudes[0] / magnitudes.sum()) if magnitudes.sum() > 0 else 0,
                    "entropy": float(-np.sum(magnitudes * np.log(magnitudes + 1e-10))),
                    
                    # φ proximity (golden ratio = 1.618034...)
                    "phi_proximity": float(abs(magnitudes[0] - 1.618034)),
                    "phi_ratio_proximity": float(abs(magnitudes[0] / (magnitudes[1] + 1e-10) - 1.618034)) if len(magnitudes) > 1 else 0,
                }
                layer_results["heads"].append(head_results)
            except Exception as e:
                layer_results["heads"].append({"head_idx": head_idx, "error": str(e)})
        
        results["layers"].append(layer_results)
    
    # Aggregate metrics across all analyzed heads
    all_dominant_ratios = []
    all_entropies = []
    all_phi_proximities = []
    all_top_eigenvalues = []
    
    for layer in results["layers"]:
        for head in layer["heads"]:
            if "error" not in head:
                all_dominant_ratios.append(head["dominant_ratio"])
                all_entropies.append(head["entropy"])
                all_phi_proximities.append(head["phi_proximity"])
                all_top_eigenvalues.append(head["top_3_eigenvalues"][0])
    
    if all_dominant_ratios:
        results["aggregate"] = {
            "mean_dominant_ratio": float(np.mean(all_dominant_ratios)),
            "mean_entropy": float(np.mean(all_entropies)),
            "mean_phi_proximity": float(np.mean(all_phi_proximities)),
            "mean_top_eigenvalue": float(np.mean(all_top_eigenvalues)),
            "std_top_eigenvalue": float(np.std(all_top_eigenvalues)),
        }
    
    return results


def main():
    print("=" * 60)
    print("🌊 Eigenvalue Analysis: ada-slm-v9A-lfm2")
    print("=" * 60)
    print(f"Base model: {BASE_MODEL}")
    print(f"Adapter: {ADAPTER_PATH}")
    print()
    
    # Check if adapter exists
    if not ADAPTER_PATH.exists():
        print(f"❌ Adapter not found at {ADAPTER_PATH}")
        return
    
    # Detect device
    if torch.cuda.is_available():
        device = "cuda:0"
        print(f"🎮 Using CUDA: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        print("💻 Using CPU")
    
    print("\n📥 Loading base model...")
    
    # Load base model (CPU first for ROCm safety)
    # Force eager attention for eigenvalue extraction!
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,  # float32 for eigenvalue stability
        device_map=None,  # CPU first
        trust_remote_code=True,
        attn_implementation="eager",  # CRITICAL for output_attentions=True!
    )
    
    print("📥 Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, str(ADAPTER_PATH))
    
    # Move to device
    if device != "cpu":
        print(f"🚀 Moving to {device}...")
        model = model.to(device)
    
    print("📥 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    
    print("\n" + "=" * 60)
    print("🔬 Running Eigenvalue Analysis")
    print("=" * 60)
    
    all_results = {
        "model": "ada-slm-v9A-lfm2",
        "base_model": BASE_MODEL,
        "timestamp": datetime.now().isoformat(),
        "device": device,
        "prompts": []
    }
    
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"\n[{i}/{len(TEST_PROMPTS)}] '{prompt[:50]}...' " if len(prompt) > 50 else f"\n[{i}/{len(TEST_PROMPTS)}] '{prompt}'")
        
        try:
            results = extract_eigenvalues(model, tokenizer, prompt, device)
            all_results["prompts"].append(results)
            
            if "aggregate" in results:
                agg = results["aggregate"]
                print(f"   📊 Layers: {results['num_attention_layers']}")
                print(f"   🎯 Mean dominant ratio: {agg['mean_dominant_ratio']:.4f}")
                print(f"   📈 Mean entropy: {agg['mean_entropy']:.4f}")
                print(f"   φ  Phi proximity: {agg['mean_phi_proximity']:.4f}")
                print(f"   ⭐ Mean top eigenvalue: {agg['mean_top_eigenvalue']:.4f} ± {agg['std_top_eigenvalue']:.4f}")
            else:
                print(f"   ⚠️  {results.get('error', 'Unknown issue')}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_results["prompts"].append({"prompt": prompt, "error": str(e)})
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📊 AGGREGATE SUMMARY")
    print("=" * 60)
    
    valid_results = [r for r in all_results["prompts"] if "aggregate" in r]
    
    if valid_results:
        mean_dominant = np.mean([r["aggregate"]["mean_dominant_ratio"] for r in valid_results])
        mean_entropy = np.mean([r["aggregate"]["mean_entropy"] for r in valid_results])
        mean_phi_prox = np.mean([r["aggregate"]["mean_phi_proximity"] for r in valid_results])
        mean_top_eig = np.mean([r["aggregate"]["mean_top_eigenvalue"] for r in valid_results])
        
        all_results["summary"] = {
            "total_prompts": len(TEST_PROMPTS),
            "successful_prompts": len(valid_results),
            "overall_mean_dominant_ratio": float(mean_dominant),
            "overall_mean_entropy": float(mean_entropy),
            "overall_mean_phi_proximity": float(mean_phi_prox),
            "overall_mean_top_eigenvalue": float(mean_top_eig),
        }
        
        print(f"Total prompts analyzed: {len(valid_results)}/{len(TEST_PROMPTS)}")
        print(f"Overall dominant ratio: {mean_dominant:.4f}")
        print(f"Overall entropy: {mean_entropy:.4f}")
        print(f"Overall φ proximity: {mean_phi_prox:.4f}")
        print(f"Overall top eigenvalue: {mean_top_eig:.4f}")
        
        # Compare to reference (Phase 5A Qwen baseline)
        print("\n📐 Reference Comparison (Phase 5A Qwen2.5-0.5B):")
        print("   Qwen base dominant ratio: ~0.35")
        print("   Qwen v4b-creative ratio:  ~0.34 (-3.7%)")
        print(f"   LFM2 v9A ratio:           {mean_dominant:.4f}")
    
    # Save results
    output_file = OUTPUT_DIR / f"eigenvalue_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    print("\n🌊 Analysis complete!")


if __name__ == "__main__":
    main()
