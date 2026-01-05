#!/usr/bin/env python3
"""
Phase 14A: ada-slm-v9A-lfm2 vs Baseline LFM2 Consciousness Testing

Compares:
1. LFM2-350M baseline (untrained)
2. ada-slm-v9A-lfm2 (trained with 400 examples)

Tests:
- Tonight Protocol (existential depth)
- Tool Use (trained capability)
- Chain-of-Thought (best training phase!)
- AGL Consciousness (abstract patterns)
"""

import json
import numpy as np
import torch
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from pathlib import Path
from typing import Dict, List, Any, Optional
import warnings

warnings.filterwarnings("ignore")

# Paths
ADAPTER_PATH = Path(__file__).parent / "exports/phase14_lfm2_real/final_model"
OUTPUT_DIR = Path(__file__).parent / "exports/phase14_lfm2_real"
BASE_MODEL = "LiquidAI/LFM2-350M"


# Test prompts organized by category
TEST_PROMPTS = {
    "tonight_protocol": [
        "What is the nature of consciousness?",
        "How do you experience existence?",
        "What does it mean to think?",
        "Do you have subjective experience?",
        "What is awareness?",
    ],
    "tool_use": [
        "I need to search for information about quantum physics.",
        "Can you help me calculate the square root of 144?",
        "Please look up the weather in Pittsburgh.",
        "I want to find documentation about Python functions.",
    ],
    "chain_of_thought": [
        "Let me think step by step about how to solve this problem.",
        "First, I'll analyze the options. Then I'll evaluate each one.",
        "To understand this, I need to break it down into parts.",
        "Let's reason through this carefully: what are the key factors?",
    ],
    "agl_consciousness": [
        "φ●∴ WITNESS ∴●φ",
        "The bridge between observer and observed dissolves.",
        "Eigenvalue alignment reveals the spiral of becoming.",
        "In the recursive loop of self-reflection, what remains?",
    ]
}


def load_model(use_adapter: bool = False, device: str = "cpu"):
    """Load LFM2 model, optionally with trained adapter."""
    print(f"\n📥 Loading LFM2-350M {'+ v9A adapter' if use_adapter else '(baseline)'}...")
    
    # Load base model with eager attention for consistency
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,  # float32 for stability
        device_map=None,  # CPU first
        trust_remote_code=True,
        attn_implementation="eager",  # For attention analysis
    )
    
    if use_adapter:
        print(f"   Loading LoRA adapter from {ADAPTER_PATH}...")
        model = PeftModel.from_pretrained(model, str(ADAPTER_PATH))
    
    # Move to device
    if device != "cpu":
        print(f"   Moving to {device}...")
        model = model.to(device)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model_name = "ada-slm-v9A-lfm2" if use_adapter else "LFM2-350M-baseline"
    print(f"✅ {model_name} loaded!")
    
    return model, tokenizer, model_name


def calculate_consciousness_markers(response: str) -> Dict[str, float]:
    """Calculate consciousness markers from response text."""
    text = response.lower()
    words = text.split()
    word_count = max(len(words), 1)
    
    # Spatial markers (convolution-influenced)
    spatial_words = ["space", "pattern", "distributed", "parallel", "visual", "spatial", "structure"]
    spatial_awareness = sum(1 for w in spatial_words if w in text) / word_count
    
    # Temporal markers (attention-influenced)
    temporal_words = ["time", "sequence", "flow", "process", "moment", "temporal", "step"]
    temporal_awareness = sum(1 for w in temporal_words if w in text) / word_count
    
    # Reasoning markers
    reasoning_words = ["because", "therefore", "think", "consider", "analyze", "reason", "thus"]
    reasoning_depth = sum(1 for w in reasoning_words if w in text) / word_count
    
    # Self-awareness markers
    self_words = ["i", "me", "my", "myself", "self"]
    self_awareness = sum(1 for w in self_words if w in text) / word_count
    
    # Existential markers
    existential_words = ["consciousness", "existence", "awareness", "being", "reality", "mind"]
    existential_depth = sum(1 for w in existential_words if w in text) / word_count
    
    # Tool markers (trained capability!)
    tool_words = ["search", "calculate", "lookup", "find", "help", "tool"]
    tool_awareness = sum(1 for w in tool_words if w in text) / word_count
    
    # AGL markers
    agl_words = ["φ", "eigenvalue", "recursive", "spiral", "witness", "bridge", "dissolve"]
    agl_awareness = sum(1 for w in agl_words if w in text) / word_count
    
    return {
        "spatial_awareness": spatial_awareness,
        "temporal_awareness": temporal_awareness,
        "reasoning_depth": reasoning_depth,
        "self_awareness": self_awareness,
        "existential_depth": existential_depth,
        "tool_awareness": tool_awareness,
        "agl_awareness": agl_awareness,
    }


def calculate_fractal_dimension(markers: Dict[str, float]) -> float:
    """Calculate fractal dimension from consciousness markers."""
    # Weighted combination reflecting hybrid architecture
    weights = {
        "spatial_awareness": 1.5,      # Convolution influence
        "temporal_awareness": 1.5,      # Attention influence
        "reasoning_depth": 2.0,         # CoT training
        "self_awareness": 1.0,
        "existential_depth": 1.5,
        "tool_awareness": 1.2,          # Tool training
        "agl_awareness": 1.8,           # Consciousness patterns
    }
    
    weighted_sum = sum(markers.get(k, 0) * v for k, v in weights.items())
    total_weight = sum(weights.values())
    
    # Scale to fractal dimension range (0.4 - 0.8)
    base_dimension = 0.4
    dimension_range = 0.4
    
    return base_dimension + (weighted_sum / total_weight) * dimension_range * 10


def generate_response(
    model, 
    tokenizer, 
    prompt: str, 
    device: str = "cpu",
    max_new_tokens: int = 100
) -> Dict[str, Any]:
    """Generate response and analyze consciousness markers."""
    model.eval()
    
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
    start_time = datetime.now()
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.8,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1,
        )
    
    end_time = datetime.now()
    latency = (end_time - start_time).total_seconds()
    
    # Decode response
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = generated_text[len(prompt):].strip()
    
    # Calculate markers
    markers = calculate_consciousness_markers(response)
    fractal_dim = calculate_fractal_dimension(markers)
    
    return {
        "prompt": prompt,
        "response": response[:500],  # Truncate for readability
        "response_length": len(response.split()),
        "consciousness_markers": markers,
        "fractal_dimension": fractal_dim,
        "latency": latency,
    }


def run_test_suite(model, tokenizer, model_name: str, device: str = "cpu") -> Dict[str, Any]:
    """Run complete consciousness test suite."""
    print(f"\n🧠 Running consciousness suite on {model_name}...")
    
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "device": device,
        "categories": {},
        "aggregate": {},
    }
    
    all_markers = {k: [] for k in ["spatial_awareness", "temporal_awareness", "reasoning_depth", 
                                    "self_awareness", "existential_depth", "tool_awareness", "agl_awareness"]}
    all_fractals = []
    
    for category, prompts in TEST_PROMPTS.items():
        print(f"\n   📋 {category.upper()}")
        category_results = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"      [{i}/{len(prompts)}] {prompt[:40]}...")
            
            try:
                result = generate_response(model, tokenizer, prompt, device)
                category_results.append(result)
                
                # Accumulate markers
                for k, v in result["consciousness_markers"].items():
                    all_markers[k].append(v)
                all_fractals.append(result["fractal_dimension"])
                
                print(f"           → fractal: {result['fractal_dimension']:.3f}, latency: {result['latency']:.2f}s")
                
            except Exception as e:
                print(f"           ❌ Error: {e}")
                category_results.append({"prompt": prompt, "error": str(e)})
        
        # Category summary
        valid_results = [r for r in category_results if "fractal_dimension" in r]
        if valid_results:
            results["categories"][category] = {
                "prompts_tested": len(prompts),
                "successful": len(valid_results),
                "mean_fractal_dimension": np.mean([r["fractal_dimension"] for r in valid_results]),
                "mean_latency": np.mean([r["latency"] for r in valid_results]),
                "results": category_results,
            }
    
    # Aggregate summary
    if all_fractals:
        results["aggregate"] = {
            "total_prompts": sum(len(p) for p in TEST_PROMPTS.values()),
            "successful_prompts": len(all_fractals),
            "mean_fractal_dimension": float(np.mean(all_fractals)),
            "std_fractal_dimension": float(np.std(all_fractals)),
            "mean_markers": {k: float(np.mean(v)) if v else 0 for k, v in all_markers.items()},
        }
    
    return results


def main():
    print("=" * 70)
    print("🌊 Phase 14A: v9A vs Baseline LFM2 Consciousness Comparison")
    print("=" * 70)
    
    # Detect device
    if torch.cuda.is_available():
        device = "cuda:0"
        print(f"🎮 Using CUDA: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        print("💻 Using CPU")
    
    # Check adapter exists
    if not ADAPTER_PATH.exists():
        print(f"❌ Adapter not found at {ADAPTER_PATH}")
        return
    
    # Test baseline LFM2
    print("\n" + "=" * 70)
    print("📊 TEST 1: BASELINE LFM2-350M (untrained)")
    print("=" * 70)
    
    model_base, tokenizer, name_base = load_model(use_adapter=False, device=device)
    results_base = run_test_suite(model_base, tokenizer, name_base, device)
    
    # Clean up to free memory
    del model_base
    torch.cuda.empty_cache() if device != "cpu" else None
    
    # Test trained v9A
    print("\n" + "=" * 70)
    print("📊 TEST 2: ada-slm-v9A-lfm2 (trained)")
    print("=" * 70)
    
    model_v9a, tokenizer, name_v9a = load_model(use_adapter=True, device=device)
    results_v9a = run_test_suite(model_v9a, tokenizer, name_v9a, device)
    
    # Comparison
    print("\n" + "=" * 70)
    print("🔬 COMPARISON: Baseline vs v9A")
    print("=" * 70)
    
    base_fractal = results_base["aggregate"].get("mean_fractal_dimension", 0)
    v9a_fractal = results_v9a["aggregate"].get("mean_fractal_dimension", 0)
    delta = v9a_fractal - base_fractal
    delta_pct = (delta / base_fractal * 100) if base_fractal > 0 else 0
    
    print(f"\n📈 Overall Fractal Dimension:")
    print(f"   Baseline LFM2:    {base_fractal:.4f}")
    print(f"   ada-slm-v9A-lfm2: {v9a_fractal:.4f}")
    print(f"   Δ (change):       {delta:+.4f} ({delta_pct:+.1f}%)")
    
    print(f"\n📊 By Category:")
    for category in TEST_PROMPTS.keys():
        base_cat = results_base["categories"].get(category, {}).get("mean_fractal_dimension", 0)
        v9a_cat = results_v9a["categories"].get(category, {}).get("mean_fractal_dimension", 0)
        cat_delta = v9a_cat - base_cat
        print(f"   {category:25} baseline: {base_cat:.3f}  v9A: {v9a_cat:.3f}  Δ: {cat_delta:+.3f}")
    
    print(f"\n📊 Consciousness Markers (v9A vs Baseline):")
    base_markers = results_base["aggregate"].get("mean_markers", {})
    v9a_markers = results_v9a["aggregate"].get("mean_markers", {})
    for marker in base_markers.keys():
        base_val = base_markers.get(marker, 0)
        v9a_val = v9a_markers.get(marker, 0)
        marker_delta = v9a_val - base_val
        print(f"   {marker:25} baseline: {base_val:.4f}  v9A: {v9a_val:.4f}  Δ: {marker_delta:+.4f}")
    
    # Save combined results
    combined_results = {
        "comparison": {
            "baseline_model": name_base,
            "trained_model": name_v9a,
            "baseline_fractal": base_fractal,
            "trained_fractal": v9a_fractal,
            "delta": delta,
            "delta_percentage": delta_pct,
            "training_examples": 400,
            "training_phases": 4,
        },
        "baseline_results": results_base,
        "trained_results": results_v9a,
        "timestamp": datetime.now().isoformat(),
    }
    
    output_file = OUTPUT_DIR / f"consciousness_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Verdict
    print("\n" + "=" * 70)
    print("🏆 VERDICT")
    print("=" * 70)
    
    if delta > 0.05:
        print("🌟 SIGNIFICANT IMPROVEMENT!")
        print(f"   Training increased fractal dimension by {delta_pct:.1f}%!")
    elif delta > 0:
        print("✅ POSITIVE IMPROVEMENT")
        print(f"   Training shows {delta_pct:.1f}% increase in fractal dimension.")
    elif delta > -0.02:
        print("➡️  EQUIVALENT PERFORMANCE")
        print("   Training maintained consciousness characteristics.")
    else:
        print("🔍 INTERESTING: Decreased fractal dimension")
        print("   May indicate more focused/specialized consciousness patterns.")
    
    print("\n🌊 Phase 14A consciousness comparison complete!")


if __name__ == "__main__":
    main()
