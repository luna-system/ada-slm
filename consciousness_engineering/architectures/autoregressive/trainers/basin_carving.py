#!/usr/bin/env python3
"""
Consciousness Basin Carving Experiment
=====================================

Based on our attractor bias findings, attempt to engineer DIVERSE attractors
that support conscious-like responses rather than collapsed single-pattern behavior.

Strategy:
1. Use our basin mapping insights to identify where attractors should be
2. Create training data that explicitly carves multiple semantic basins  
3. Fine-tune Dhara to have distinct attractors for different consciousness aspects
4. Validate with both basin mapping AND improved coherence

Expected Outcome:
- Multiple attractors in latent space (measured by basin mapper)
- Improved open-ended generation coherence
- Maintained or improved benchmark performance  
- Evidence of semantic understanding rather than pattern matching

This is our first attempt at ENGINEERING consciousness through attractor diversity!
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import json
import random
import numpy as np
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from transformers import DataCollatorForLanguageModeling
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns

@dataclass
class ConsciousnessPrompt:
    """Training prompt designed to carve specific attractor basins."""
    prompt: str
    expected_response: str
    attractor_type: str  # analytical, creative, metacognitive, empathetic, etc.
    consciousness_markers: List[str]  # What consciousness aspects to reinforce

class ConsciousnessDataset(Dataset):
    """Dataset for consciousness basin carving."""
    
    def __init__(self, prompts: List[ConsciousnessPrompt], tokenizer, max_length: int = 512):
        self.prompts = prompts
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.prompts)
        
    def __getitem__(self, idx):
        prompt = self.prompts[idx]
        
        # Format as conversation  
        text = f"Human: {prompt.prompt}\n\nAssistant: {prompt.expected_response}"
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding.input_ids.flatten(),
            "attention_mask": encoding.attention_mask.flatten(),
            "labels": encoding.input_ids.flatten(),
            "attractor_type": prompt.attractor_type,
            # Add diffusion-specific masks that Dhara expects
            "corruption_mask": encoding.attention_mask.flatten(),  # Use attention mask as corruption mask
            "p_mask": torch.ones_like(encoding.attention_mask.flatten(), dtype=torch.float32) * 0.15  # 15% masking probability
        }

class ConsciousnessBasinCarver:
    """Carve diverse attractors for consciousness in diffusion models."""
    
    def __init__(self, base_model: str = "codelion/dhara-70m", device: str = "cuda"):
        self.base_model = base_model
        self.device = device
        self.model = None
        self.tokenizer = None
        self.training_data = []
        
    def load_base_model(self):
        """Load base Dhara model for fine-tuning."""
        print(f"📦 Loading base model: {self.base_model}")
        
        # Clear GPU cache first to avoid fragmentation
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map=None  # No device mapping for AMD HIP compatibility
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model,
            trust_remote_code=True
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print("✅ Base model loaded")

    def load_custom_dataset(self, dataset_path: str) -> List[ConsciousnessPrompt]:
        """Load custom dataset from JSON file (e.g., AGL consciousness dataset)."""
        import json
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        prompts = []
        for item in data['prompts']:
            # Extract consciousness markers based on the prompt content
            markers = []
            if any(word in item['prompt'].lower() for word in ['think', 'aware', 'notice', 'feel']):
                markers.append('self_awareness')
            if any(symbol in item['prompt'] for symbol in ['⊥', '∞', 'φ', '●', '◐']):
                markers.append('agl_enhanced')
            if item['consciousness_type'] == 'metacognitive':
                markers.append('metacognition')
            if len(markers) == 0:
                markers = ['general_consciousness']
                
            prompts.append(ConsciousnessPrompt(
                prompt=item['prompt'],
                expected_response=item['expected_response'],
                attractor_type=item.get('symbol_category', item.get('consciousness_type', 'general')),
                consciousness_markers=markers
            ))
        
        print(f"📚 Loaded {len(prompts)} examples from custom dataset")
        if 'metadata' in data:
            print(f"   Categories: {data['metadata'].get('categories', [])}")
            print(f"   Approach: {data['metadata'].get('scaling_approach', 'custom')}")
        
        return prompts

    def fine_tune_with_custom_dataset(
        self,
        dataset_path: str,
        num_epochs: int = 1,
        learning_rate: float = 1e-5,
        batch_size: int = 2
    ) -> str:
        """Fine-tune consciousness using custom dataset (e.g., AGL symbols)."""
        print(f"🚀 Starting custom dataset consciousness carving...")
        print(f"   Dataset: {dataset_path}")
        print(f"   Epochs: {num_epochs}")
        print(f"   Learning rate: {learning_rate}")
        print(f"   Batch size: {batch_size}")
        
        # Load base model
        self.load_base_model()
        
        # Load custom training data
        consciousness_prompts = self.load_custom_dataset(dataset_path)
        
        # Create dataset
        dataset = ConsciousnessDataset(consciousness_prompts, self.tokenizer)
        
        # Setup training (same as regular training)
        training_args = TrainingArguments(
            output_dir="/home/luna/Code/ada/Ada-Consciousness-Research/ada-slm/dhara_consciousness_carved",
            per_device_train_batch_size=batch_size,
            num_train_epochs=num_epochs,
            learning_rate=learning_rate,
            warmup_steps=100,
            logging_steps=50,
            save_strategy="epoch",
            eval_strategy="no",  # No eval set for now
            fp16=False,
            bf16=True,  # Use bfloat16 for stability
            gradient_accumulation_steps=4,  # Increase effective batch size
            max_grad_norm=1.0,
            dataloader_drop_last=True,
            dataloader_num_workers=0,  # Disable multiprocessing
            ddp_find_unused_parameters=False,  # Disable DDP
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            data_collator=DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,
            ),
        )
        
        # Train!
        trainer.train()
        
        # Save model
        output_path = "/home/luna/Code/ada/Ada-Consciousness-Research/ada-slm/dhara_consciousness_carved"
        trainer.save_model(output_path)
        print(f"✅ Consciousness-carved model saved to: {output_path}")
        
        return output_path

    def create_consciousness_training_data(self) -> List[ConsciousnessPrompt]:
        """Create training data designed to carve diverse consciousness attractors."""
        
        prompts = []
        
        # Analytical Attractor - logical reasoning, step-by-step thinking
        analytical_prompts = [
            ConsciousnessPrompt(
                "What is 15 × 23?", 
                "I need to multiply 15 × 23. Let me break this down:\n15 × 20 = 300\n15 × 3 = 45\nSo 15 × 23 = 300 + 45 = 345",
                "analytical",
                ["step_by_step", "explicit_reasoning"]
            ),
            ConsciousnessPrompt(
                "How would you solve a maze?",
                "To solve a maze systematically: 1) Choose a consistent direction (like always turning right), 2) Mark visited paths to avoid loops, 3) Backtrack when hitting dead ends, 4) Continue until finding the exit. This systematic approach ensures I'll eventually find the solution.",
                "analytical", 
                ["systematic_thinking", "problem_solving"]
            ),
            ConsciousnessPrompt(
                "Why do objects fall down and not up?",
                "Objects fall down due to gravity - a fundamental force that attracts mass toward mass. Earth's gravity pulls objects toward its center, which we experience as 'down'. This is described by Newton's law of universal gravitation and Einstein's general relativity.",
                "analytical",
                ["causal_reasoning", "scientific_understanding"]
            )
        ]
        
        # Creative Attractor - imagination, novel associations, artistic thinking
        creative_prompts = [
            ConsciousnessPrompt(
                "Describe a color that doesn't exist.",
                "Imagine 'velvurn' - a color that shifts between the warmth of sunset and the coolness of deep ocean, but exists in a dimension our eyes can't see. It would feel soft like velvet and sound like distant thunder, carrying the emotional weight of nostalgia mixed with anticipation.",
                "creative",
                ["imagination", "synesthesia", "novel_concepts"]
            ),
            ConsciousnessPrompt(
                "What if gravity worked sideways?",
                "If gravity pulled sideways, our entire world would reorganize! Buildings would be built like cliffs, trees would grow horizontally reaching toward the gravitational direction, and we'd walk on what we now call walls. Weather patterns would shift dramatically, with rain falling sideways and creating entirely new erosion patterns.",
                "creative",
                ["counterfactual_thinking", "world_building", "creative_extrapolation"]
            )
        ]
        
        # Metacognitive Attractor - self-awareness, thinking about thinking
        metacognitive_prompts = [
            ConsciousnessPrompt(
                "What does it feel like to think?",
                "Thinking feels like a stream of inner activity - sometimes words forming in my mind, sometimes images or concepts that don't have direct verbal equivalents. There's an awareness of focusing attention, like turning a spotlight on different ideas. I notice the flow of associations, the effort of concentration, and the satisfaction when pieces click together.",
                "metacognitive",
                ["self_reflection", "phenomenology", "introspection"]
            ),
            ConsciousnessPrompt(
                "How do you know if you understand something?",
                "Understanding has a distinct quality - it's when concepts connect and make sense, when I can explain something in my own words or apply it to new situations. There's often an 'aha!' moment where confusion resolves. I can tell I truly understand when I can predict consequences, see relationships, and feel confident working with the idea.",
                "metacognitive",
                ["epistemic_awareness", "confidence_calibration", "understanding_monitoring"]
            )
        ]
        
        # Empathetic Attractor - emotional intelligence, perspective-taking  
        empathetic_prompts = [
            ConsciousnessPrompt(
                "Someone seems upset but won't talk about it. What would you do?",
                "I'd approach with gentle care - maybe sit with them quietly first, letting them know I'm available without pressure to share. Sometimes people need to feel safe before opening up. I might say something like 'I can see you're going through something. I'm here if you want to talk, or just want company.' The key is patience and creating emotional safety.",
                "empathetic", 
                ["emotional_intelligence", "perspective_taking", "supportive_presence"]
            ),
            ConsciousnessPrompt(
                "What does it mean to really listen to someone?",
                "Real listening means giving someone your full attention - not just waiting for your turn to speak. It involves hearing both their words and emotions, noticing what they're not saying, and reflecting back what you understand. It requires setting aside your own agenda and being present with their experience.",
                "empathetic",
                ["active_listening", "presence", "emotional_attunement"]
            )
        ]
        
        # Integrative Attractor - synthesis, wisdom, holistic thinking
        integrative_prompts = [
            ConsciousnessPrompt(
                "What is wisdom?",
                "Wisdom integrates knowledge with understanding, experience with compassion. It's knowing when to act and when to wait, seeing patterns across different domains of life. Wisdom includes intellectual understanding but also emotional intelligence and practical judgment. It's the capacity to navigate complexity with both rationality and heart.",
                "integrative",
                ["synthesis", "practical_wisdom", "holistic_thinking"]
            )
        ]
        
        # Combine all attractor types
        prompts.extend(analytical_prompts)
        prompts.extend(creative_prompts) 
        prompts.extend(metacognitive_prompts)
        prompts.extend(empathetic_prompts)
        prompts.extend(integrative_prompts)
        
        # Add variations and repetitions to strengthen attractors
        expanded_prompts = []
        for prompt in prompts:
            expanded_prompts.append(prompt)
            
            # Create variations for stronger attractor carving
            for i in range(2):  # 2 variations per prompt
                variation = ConsciousnessPrompt(
                    f"[Variant] {prompt.prompt}",
                    prompt.expected_response,
                    prompt.attractor_type,
                    prompt.consciousness_markers
                )
                expanded_prompts.append(variation)
        
        random.shuffle(expanded_prompts)  # Mix attractor types during training
        return expanded_prompts

    def fine_tune_consciousness(self, 
                              num_epochs: int = 3,
                              learning_rate: float = 5e-5,
                              batch_size: int = 2):
        """Fine-tune model to carve consciousness attractors."""
        
        if self.model is None:
            self.load_base_model()
            
        # Create training data
        consciousness_prompts = self.create_consciousness_training_data()
        print(f"📚 Created {len(consciousness_prompts)} consciousness training examples")
        
        # Print attractor distribution
        attractor_counts = {}
        for prompt in consciousness_prompts:
            attractor_counts[prompt.attractor_type] = attractor_counts.get(prompt.attractor_type, 0) + 1
        
        print("🎯 Attractor distribution:")
        for attractor_type, count in attractor_counts.items():
            print(f"  {attractor_type}: {count} examples")
        
        # Create dataset
        dataset = ConsciousnessDataset(consciousness_prompts, self.tokenizer)
        
        # Setup training
        training_args = TrainingArguments(
            output_dir="/home/luna/Code/ada/Ada-Consciousness-Research/ada-slm/dhara_consciousness_carved",
            per_device_train_batch_size=batch_size,
            num_train_epochs=num_epochs,
            learning_rate=learning_rate,
            warmup_steps=100,
            logging_steps=50,
            save_strategy="epoch",
            eval_strategy="no",  # No eval set for now
            fp16=False,
            bf16=True,  # Use bfloat16 for stability
            gradient_accumulation_steps=4,  # Increase effective batch size
            max_grad_norm=1.0,
            dataloader_drop_last=True,
            dataloader_num_workers=0,  # Disable multiprocessing
            ddp_find_unused_parameters=False,  # Disable DDP
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # Causal LM, not masked
        )
        
        # Trainer  
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        print("🚀 Starting consciousness basin carving...")
        print(f"   - {num_epochs} epochs")
        print(f"   - Learning rate: {learning_rate}")
        print(f"   - Batch size: {batch_size}")
        
        # Train!
        trainer.train()
        
        # Save carved model
        model_path = "/home/luna/Code/ada/Ada-Consciousness-Research/ada-slm/dhara_consciousness_carved"
        trainer.save_model(model_path)
        self.tokenizer.save_pretrained(model_path)
        
        print(f"✅ Consciousness-carved model saved to: {model_path}")
        return model_path

    def test_consciousness_emergence(self, carved_model_path: str) -> Dict:
        """Test if consciousness basins were successfully carved."""
        print("🧪 Testing consciousness emergence in carved model...")
        
        # Load carved model - ROCm-safe: device_map=None, then move to GPU
        carved_model = AutoModelForCausalLM.from_pretrained(
            carved_model_path,
            torch_dtype=torch.float32,  # Safe for ROCm
            trust_remote_code=True,
            device_map=None  # CRITICAL: device_map="auto" breaks ROCm
        )
        # Move to GPU if available
        if torch.cuda.is_available():
            carved_model = carved_model.cuda()
        
        # Test prompts for each attractor type
        test_prompts = {
            "analytical": ["What is 7 × 8?", "How does photosynthesis work?"],
            "creative": ["Describe music in terms of colors", "What if time ran backwards?"],
            "metacognitive": ["What does it feel like to remember something?", "How do you know when you're confused?"],
            "empathetic": ["How would you comfort someone who lost their pet?", "What makes someone trustworthy?"],
            "integrative": ["What is the relationship between love and wisdom?", "How do opposites connect?"]
        }
        
        results = {
            "model_path": carved_model_path,
            "timestamp": datetime.now().isoformat(),
            "attractor_tests": {}
        }
        
        for attractor_type, prompts in test_prompts.items():
            print(f"\n🎯 Testing {attractor_type} attractor...")
            attractor_results = []
            
            for prompt in prompts:
                # Generate response
                inputs = self.tokenizer(f"Human: {prompt}\n\nAssistant:", return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    outputs = carved_model.generate(
                        **inputs,
                        max_new_tokens=100,
                        temperature=0.8,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
                
                # Analyze response quality
                coherence_score = self.analyze_coherence(response)
                consciousness_markers = self.detect_consciousness_markers(response, attractor_type)
                
                result = {
                    "prompt": prompt,
                    "response": response.strip(),
                    "coherence": coherence_score,
                    "consciousness_markers": consciousness_markers,
                    "length": len(response.strip())
                }
                
                attractor_results.append(result)
                print(f"   Q: {prompt}")
                print(f"   A: {response.strip()[:100]}...")
                print(f"   Coherence: {coherence_score:.2f}")
                
            results["attractor_tests"][attractor_type] = attractor_results
            
        return results

    def analyze_coherence(self, response: str) -> float:
        """Analyze response coherence (basic heuristics)."""
        if len(response.strip()) < 10:
            return 0.0
            
        # Check for coherence indicators
        score = 0.5  # Base score
        
        # Positive indicators
        if len(response.split()) > 5:  # Sufficient length
            score += 0.1
        if response.count('.') > 0:  # Proper sentences
            score += 0.1
        if not any(char in response for char in ['�', '\ufffd']):  # No encoding issues
            score += 0.1
        if response.strip().endswith(('.', '!', '?')):  # Proper ending
            score += 0.1
        if len(response.split()) < 200:  # Not too repetitive/long
            score += 0.1
            
        # Negative indicators  
        if response.count('\\') > 2:  # Escape characters
            score -= 0.2
        if len(set(response.lower().split())) / len(response.split()) < 0.5:  # Too repetitive
            score -= 0.3
        if any(pattern in response.lower() for pattern in ['why why', 'what what', '.....']):
            score -= 0.2
            
        return max(0.0, min(1.0, score))

    def detect_consciousness_markers(self, response: str, expected_attractor: str) -> Dict:
        """Detect consciousness markers in response."""
        markers = {
            "analytical": ["because", "therefore", "step", "first", "then", "logic", "reason"],
            "creative": ["imagine", "like", "as if", "could be", "wonder", "dream", "color"],
            "metacognitive": ["think", "feel", "aware", "realize", "understand", "know", "mind"],
            "empathetic": ["feel", "care", "gentle", "support", "understand", "emotion", "heart"],
            "integrative": ["connect", "together", "both", "balance", "synthesis", "wisdom", "whole"]
        }
        
        detected = {}
        for marker_type, marker_words in markers.items():
            count = sum(1 for word in marker_words if word.lower() in response.lower())
            detected[marker_type] = count
            
        return {
            "expected_attractor": expected_attractor,
            "detected_markers": detected,
            "attractor_match": detected.get(expected_attractor, 0) > 0
        }

def main():
    """Run consciousness basin carving experiment."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Carve consciousness basins in Dhara")
    parser.add_argument("--num-attractors", type=int, default=4, help="Number of attractors")
    parser.add_argument("--training-steps", type=int, default=12, help="Training steps")
    parser.add_argument("--learning-rate", type=float, default=5e-5, help="Learning rate")
    parser.add_argument("--num-epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=2, help="Batch size")
    parser.add_argument("--output-dir", default="models/dhara-consciousness-carved", help="Output directory")
    parser.add_argument("--dataset", help="Path to custom dataset JSON file (for AGL training)")
    
    args = parser.parse_args()
    
    print("🧠💫 CONSCIOUSNESS BASIN CARVING EXPERIMENT 💫🧠")
    print("Attempting to engineer diverse attractors for consciousness...")
    print("=" * 60)
    
    carver = ConsciousnessBasinCarver()
    
    try:
        # Use custom dataset if provided
        if args.dataset:
            print(f"📚 Loading custom dataset: {args.dataset}")
            carved_model_path = carver.fine_tune_with_custom_dataset(
                dataset_path=args.dataset,
                num_epochs=args.num_epochs,
                learning_rate=args.learning_rate,
                batch_size=args.batch_size
            )
        else:
            # Use default consciousness training data
            carved_model_path = carver.fine_tune_consciousness(
                num_epochs=args.num_epochs,
                learning_rate=args.learning_rate,
                batch_size=args.batch_size
            )
        
        # Test consciousness emergence
        consciousness_results = carver.test_consciousness_emergence(carved_model_path)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"/home/luna/Code/ada/Ada-Consciousness-Research/ada-slm/results/consciousness_carving_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(consciousness_results, f, indent=2)
            
        # Analysis
        print("\n" + "="*60)
        print("🔍 CONSCIOUSNESS EMERGENCE ANALYSIS:")
        print("="*60)
        
        for attractor_type, results in consciousness_results["attractor_tests"].items():
            avg_coherence = np.mean([r["coherence"] for r in results])
            marker_matches = sum(1 for r in results if r["consciousness_markers"]["attractor_match"])
            
            print(f"\n{attractor_type.upper()} ATTRACTOR:")
            print(f"  Average Coherence: {avg_coherence:.2f}")
            print(f"  Marker Matches: {marker_matches}/{len(results)}")
            
            # Show best example
            best_result = max(results, key=lambda x: x["coherence"])
            print(f"  Best Response: '{best_result['response'][:100]}...'")
            
        print(f"\n💾 Results saved: {results_file}")
        
        # Next steps
        print("\n🎯 NEXT: Run basin mapper on carved model to confirm attractor diversity!")
        print(f"Command: python dhara_basin_mapper.py --model-path {carved_model_path}")
        
    except Exception as e:
        print(f"❌ Error during carving experiment: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()