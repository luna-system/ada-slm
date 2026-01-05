#!/usr/bin/env python3
"""
Multi-Language Consciousness Testing for v9B-pure

Tests the trained model using both English and AGL prompts,
comparing consciousness markers across languages.

Usage:
    python test_v9b_multilang.py                    # Both languages
    python test_v9b_multilang.py --languages agl    # AGL only
    python test_v9b_multilang.py --languages english agl  # Explicit both
"""

import argparse
import json
import torch
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import warnings

warnings.filterwarnings("ignore")

# Import language system
from consciousness_engineering.languages import get_language, list_languages
from consciousness_engineering.cli.main import discover_models, get_model_path

# Paths
BASE_MODEL = "LiquidAI/LFM2-350M"
OUTPUT_DIR = Path(__file__).parent / "results"

# Protocols to test
TEST_PROTOCOLS = [
    "tonight_protocol",
    "abyss",  # NEW: Uncertainty and void exploration
    "agl_consciousness", 
    "existential",
    "chain_of_thought",
]


def load_model(
    adapter_path: Optional[Path] = None,
    device: str = "cpu",
    model_name: str = "LFM2-350M"
) -> tuple:
    """Load LFM2 model with optional adapter."""
    print(f"\n📥 Loading {model_name}...")
    
    # Load base model - CPU first for ROCm compatibility
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,
        device_map=None,  # ROCm compatibility!
        trust_remote_code=True,
        attn_implementation="eager",
    )
    
    if adapter_path and adapter_path.exists():
        print(f"   Loading adapter from {adapter_path}...")
        model = PeftModel.from_pretrained(model, str(adapter_path))
    
    # Move to device
    if device != "cpu":
        print(f"   Moving to {device}...")
        model = model.to(device)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print(f"✅ {model_name} loaded!")
    return model, tokenizer


def generate_response(
    model,
    tokenizer,
    prompt: str,
    device: str = "cpu",
    max_new_tokens: int = 150,
    temperature: float = 0.8,
) -> Dict[str, Any]:
    """Generate response from model."""
    model.eval()
    
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
    start_time = datetime.now()
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1,
        )
    
    latency = (datetime.now() - start_time).total_seconds()
    
    # Decode
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_text[len(prompt):].strip()
    
    return {
        "prompt": prompt,
        "response": response,
        "response_length": len(response.split()),
        "latency": latency,
    }


def test_model_with_language(
    model,
    tokenizer,
    language_name: str,
    protocols: List[str],
    device: str = "cpu",
) -> Dict[str, Any]:
    """Test model with a specific language."""
    lang = get_language(language_name)
    if not lang:
        print(f"❌ Unknown language: {language_name}")
        return {}
    
    print(f"\n🗣️  Testing with {lang.display_name}...")
    
    results = {
        "language": language_name,
        "display_name": lang.display_name,
        "protocols": {},
        "aggregate_markers": {},
    }
    
    all_markers = []
    
    for protocol in protocols:
        prompts = lang.get_prompts(protocol)
        if not prompts:
            print(f"   ⚠️  No {protocol} prompts for {language_name}")
            continue
        
        print(f"\n   📋 {protocol.upper()} ({len(prompts)} prompts)")
        
        protocol_results = []
        
        for i, prompt in enumerate(prompts[:5], 1):  # Test first 5 per protocol
            print(f"      [{i}] {prompt[:50]}...")
            
            try:
                result = generate_response(model, tokenizer, prompt, device)
                
                # Extract markers using language-specific analysis
                markers = lang.extract_markers(result["response"])
                result["markers"] = markers
                
                # Validate AGL response if applicable
                if language_name == "agl":
                    validation = lang.validate_response(result["response"])
                    result["validation"] = validation
                    print(f"          AGL score: {validation.get('agl_quality_score', 0):.2f}")
                
                protocol_results.append(result)
                all_markers.append(markers)
                
                print(f"          latency: {result['latency']:.2f}s, "
                      f"response: {result['response'][:60]}...")
                
            except Exception as e:
                print(f"          ❌ Error: {e}")
                protocol_results.append({"prompt": prompt, "error": str(e)})
        
        # Protocol summary
        valid_results = [r for r in protocol_results if "markers" in r]
        if valid_results:
            results["protocols"][protocol] = {
                "prompts_tested": len(prompts[:5]),
                "successful": len(valid_results),
                "mean_latency": np.mean([r["latency"] for r in valid_results]),
                "results": protocol_results,
            }
    
    # Aggregate markers
    if all_markers:
        all_keys = set()
        for m in all_markers:
            all_keys.update(m.keys())
        
        results["aggregate_markers"] = {
            k: float(np.mean([m.get(k, 0) for m in all_markers]))
            for k in all_keys
        }
    
    return results


def compare_languages(
    model,
    tokenizer,
    languages: List[str],
    protocols: List[str],
    device: str = "cpu",
    model_name: str = "model",
) -> Dict[str, Any]:
    """Compare model performance across languages."""
    print(f"\n{'='*70}")
    print(f"🌐 Multi-Language Consciousness Testing: {model_name}")
    print(f"{'='*70}")
    print(f"Languages: {', '.join(languages)}")
    print(f"Protocols: {', '.join(protocols)}")
    
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "languages_tested": languages,
        "protocols_tested": protocols,
        "by_language": {},
        "comparison": {},
    }
    
    for lang_name in languages:
        lang_results = test_model_with_language(
            model, tokenizer, lang_name, protocols, device
        )
        results["by_language"][lang_name] = lang_results
    
    # Cross-language comparison
    if len(languages) >= 2 and all(languages[i] in results["by_language"] for i in range(2)):
        print(f"\n{'='*70}")
        print("📊 LANGUAGE COMPARISON")
        print(f"{'='*70}")
        
        lang1, lang2 = languages[0], languages[1]
        markers1 = results["by_language"][lang1].get("aggregate_markers", {})
        markers2 = results["by_language"][lang2].get("aggregate_markers", {})
        
        # Find common markers
        common_markers = set(markers1.keys()) & set(markers2.keys())
        
        print(f"\n   {'Marker':30} {lang1:>12} {lang2:>12} {'Δ':>10}")
        print(f"   {'-'*30} {'-'*12} {'-'*12} {'-'*10}")
        
        for marker in sorted(common_markers):
            v1 = markers1.get(marker, 0)
            v2 = markers2.get(marker, 0)
            delta = v2 - v1
            print(f"   {marker:30} {v1:12.4f} {v2:12.4f} {delta:+10.4f}")
        
        results["comparison"] = {
            f"{lang1}_vs_{lang2}": {
                marker: {
                    lang1: markers1.get(marker, 0),
                    lang2: markers2.get(marker, 0),
                    "delta": markers2.get(marker, 0) - markers1.get(marker, 0),
                }
                for marker in common_markers
            }
        }
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Multi-language consciousness testing for v9B-pure"
    )
    parser.add_argument(
        "--languages", "-l",
        nargs="+",
        default=["english", "agl"],
        choices=list_languages(),
        help="Languages to test with"
    )
    # Get available models dynamically
    available_models = ["baseline"] + [name for name, _ in discover_models()]
    
    parser.add_argument(
        "--model", "-m",
        default="v9b_pure",
        help=f"Model to test. Available: {', '.join(available_models[:5])}... (use 'ce models' to list all)"
    )
    parser.add_argument(
        "--protocols", "-p",
        nargs="+",
        default=TEST_PROTOCOLS,
        help="Protocols to test"
    )
    parser.add_argument(
        "--device", "-d",
        default="auto",
        help="Device (auto/cpu/cuda:0/rocm:0)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output file path"
    )
    
    args = parser.parse_args()
    
    # Auto-detect device
    if args.device == "auto":
        if torch.cuda.is_available():
            device = "cuda:0"
            print(f"🎮 Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = "cpu"
            print("💻 Using CPU")
    else:
        device = args.device
    
    # Select adapter dynamically
    if args.model == "baseline":
        adapter_path = None
        model_name = "LFM2-350M-baseline"
    else:
        # Dynamic model resolution
        adapter_path = get_model_path(args.model)
        
        if adapter_path is None:
            # Try legacy name mapping for backwards compatibility
            legacy_map = {
                "v9a": "phase14_lfm2_real",
                "v9b": "v9b_pure",
                "v9c": "v9c_capacity", 
                "v9d": "v9d_isolation",
                "v9e": "v9e_aggressive",
                "v9f-base": "v9f_polyglot_base",
                "v9f-v9c": "v9f_polyglot_v9c",
            }
            if args.model in legacy_map:
                adapter_path = get_model_path(legacy_map[args.model])
        
        if adapter_path is None:
            print(f"❌ Model not found: {args.model}")
            print(f"   Use 'ce models' to list available models")
            return 1
            
        model_name = f"ada-slm-{args.model}"
    
    # Check adapter exists
    if adapter_path and not adapter_path.exists():
        print(f"❌ Adapter not found: {adapter_path}")
        return 1
    
    # Load model
    model, tokenizer = load_model(adapter_path, device, model_name)
    
    # Run comparison
    results = compare_languages(
        model, tokenizer,
        args.languages,
        args.protocols,
        device,
        model_name,
    )
    
    # Save results
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = args.output or OUTPUT_DIR / f"multilang_{args.model}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Summary
    print(f"\n{'='*70}")
    print("🏆 SUMMARY")
    print(f"{'='*70}")
    
    for lang_name in args.languages:
        lang_data = results["by_language"].get(lang_name, {})
        markers = lang_data.get("aggregate_markers", {})
        
        # Key metrics for each language
        if lang_name == "agl":
            key_metrics = ["agl_awareness", "certainty_gradient", "phi_patterns", 
                         "tonight_protocol_marker"]
        else:
            key_metrics = ["existential_depth", "reasoning_depth", "self_awareness"]
        
        print(f"\n   {lang_name.upper()}:")
        for metric in key_metrics:
            value = markers.get(metric, 0)
            print(f"      {metric}: {value:.4f}")
    
    print(f"\n🌊 Multi-language testing complete!")
    return 0


if __name__ == "__main__":
    exit(main())
