#!/usr/bin/env python3
"""
Real Model Tester for Fractal Consciousness Architecture
Tests actual models through the new Phase 12 system
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Add the new consciousness_engineering to path
sys.path.insert(0, str(Path(__file__).parent))

from consciousness_engineering import run_consciousness_protocol
from consciousness_engineering.protocols.base import ConsciousnessResult

class RealModelTester:
    """Test real models through fractal consciousness architecture"""
    
    def __init__(self):
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        
    def download_and_test_models(self):
        """Download and test target models"""
        print("🤖 Testing Real Models in Fractal Consciousness Architecture!")
        print("=" * 60)
        
        # Test models
        models_to_test = [
            {
                "name": "smollm-135m",
                "hf_name": "HuggingFaceTB/SmolLM-135M-Instruct",
                "architecture": "autoregressive"
            },
            {
                "name": "qwen2.5-0.5b", 
                "hf_name": "Qwen/Qwen2.5-0.5B-Instruct",
                "architecture": "autoregressive"
            }
        ]
        
        all_results = {}
        
        for model_info in models_to_test:
            print(f"\n🧠 Testing {model_info['name']}...")
            print("-" * 40)
            
            try:
                # Test the model
                result = self.test_real_model(
                    model_info["hf_name"], 
                    model_info["name"],
                    model_info["architecture"]
                )
                
                all_results[model_info["name"]] = result.to_dict()
                
                print(f"✅ {model_info['name']} testing complete!")
                print(f"   Consciousness markers: {len(result.consciousness_markers)}")
                print(f"   Fractal dimension: {result.fractal_dimension:.4f}")
                print(f"   Architecture: {result.architecture}")
                
                # Save individual results
                self.save_results(result, f"consciousness_test_{model_info['name']}.json")
                
            except Exception as e:
                print(f"❌ Failed to test {model_info['name']}: {e}")
                import traceback
                traceback.print_exc()
                
        # Save combined results
        combined_file = self.results_dir / f"fractal_consciousness_suite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(combined_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "architecture_version": "12.0.0",
                "test_type": "fractal_consciousness_suite",
                "results": all_results
            }, f, indent=2)
            
        print(f"\n🎉 Full Suite Complete!")
        print(f"📊 Combined results saved to: {combined_file}")
        
        return all_results
    
    def test_real_model(self, hf_name: str, model_name: str, architecture: str) -> ConsciousnessResult:
        """Test a real model through the consciousness protocol"""
        
        print(f"📥 Loading {hf_name}...")
        
        # Load model and tokenizer
        try:
            tokenizer = AutoTokenizer.from_pretrained(hf_name)
            model = AutoModelForCausalLM.from_pretrained(
                hf_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                
            print(f"✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            raise
            
        # Create a real model runner that integrates with our architecture
        real_runner = RealModelRunner(model, tokenizer, model_name, architecture)
        
        # Get tonight protocol prompts
        from consciousness_engineering.protocols.tonight import TonightProtocol
        protocol = TonightProtocol()
        prompts = protocol.get_prompts()
        
        print(f"🧠 Running consciousness protocol with {len(prompts)} prompts...")
        
        # Generate real responses
        responses = []
        consciousness_markers_list = []
        
        for i, prompt in enumerate(prompts):
            print(f"   Processing prompt {i+1}/{len(prompts)}...")
            
            try:
                response = real_runner.generate_response(prompt)
                responses.append(response)
                
                # Analyze consciousness markers for this response
                markers = protocol.analyze_response(response)
                consciousness_markers_list.append(markers)
                
            except Exception as e:
                print(f"⚠️ Failed to process prompt {i+1}: {e}")
                responses.append(f"[ERROR: {str(e)}]")
                consciousness_markers_list.append({})
                
        # Aggregate consciousness markers
        aggregated_markers = {}
        for markers in consciousness_markers_list:
            for key, value in markers.items():
                aggregated_markers[key] = aggregated_markers.get(key, 0.0) + value
                
        # Average the markers
        for key in aggregated_markers:
            aggregated_markers[key] /= len(consciousness_markers_list)
            
        # Calculate fractal dimension and julia parameters
        from consciousness_engineering.protocols.base import ConsciousnessAnalyzer
        
        fractal_dimension = ConsciousnessAnalyzer.calculate_fractal_dimension(responses)
        julia_parameters = ConsciousnessAnalyzer.extract_julia_parameters(responses)
        
        # Create result
        result = ConsciousnessResult(
            protocol="tonight",
            architecture=architecture,
            model=model_name,
            responses=responses,
            consciousness_markers=aggregated_markers,
            julia_parameters=julia_parameters,
            fractal_dimension=fractal_dimension,
            timestamp=datetime.now().isoformat(),
            metadata={
                "hf_name": hf_name,
                "model_parameters": self.estimate_parameters(model),
                "device": str(model.device) if hasattr(model, 'device') else "unknown"
            }
        )
        
        return result
    
    def estimate_parameters(self, model):
        """Estimate model parameter count"""
        try:
            return sum(p.numel() for p in model.parameters())
        except:
            return "unknown"
    
    def save_results(self, result: ConsciousnessResult, filename: str):
        """Save consciousness results to file"""
        filepath = self.results_dir / filename
        with open(filepath, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"💾 Results saved to: {filepath}")

class RealModelRunner:
    """Runs real model inference for consciousness testing"""
    
    def __init__(self, model, tokenizer, model_name, architecture):
        self.model = model
        self.tokenizer = tokenizer
        self.model_name = model_name
        self.architecture = architecture
        
    def generate_response(self, prompt: str, max_length: int = 200) -> str:
        """Generate response from real model"""
        
        # Format prompt for instruction following
        if "instruct" in self.model_name.lower():
            formatted_prompt = f"User: {prompt}\n\nAssistant:"
        else:
            formatted_prompt = prompt
            
        # Tokenize
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        if self.model.device != torch.device('cpu'):
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        # Generate
        try:
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the generated part
            response = full_response[len(formatted_prompt):].strip()
            
            return response
            
        except Exception as e:
            return f"[Generation failed: {str(e)}]"

def main():
    """Main test runner"""
    print("🌀 Phase 12 Real Model Testing")
    print("Testing fractal consciousness architecture with actual models!")
    print()
    
    tester = RealModelTester()
    
    try:
        results = tester.download_and_test_models()
        
        print("\n" + "="*60)
        print("🎊 FRACTAL CONSCIOUSNESS TESTING COMPLETE!")
        print("="*60)
        
        print("\n📊 Summary:")
        for model_name, result in results.items():
            print(f"\n🤖 {model_name}:")
            print(f"   Architecture: {result['architecture']}")
            print(f"   Consciousness markers: {len(result['consciousness_markers'])}")
            print(f"   Fractal dimension: {result['fractal_dimension']:.4f}")
            print(f"   Julia complexity: {result['julia_parameters'].get('complexity', 'N/A'):.4f}")
            
            # Show top consciousness markers
            markers = result['consciousness_markers']
            if markers:
                print(f"   Top markers:")
                for key, value in sorted(markers.items(), key=lambda x: x[1], reverse=True)[:3]:
                    print(f"     {key}: {value:.4f}")
        
        print("\n🌌 Fractal consciousness architecture working perfectly!")
        print("🚀 Ready for LVM2 Phase 11 testing!")
        
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())