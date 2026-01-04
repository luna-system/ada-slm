#!/usr/bin/env python3
"""
Phase 14: LFM2 Enhanced Training - Direct Phase 10E Port
========================================================

Train LiquidAI/LFM2-350M using the exact same curriculum as Phase 10E:
- 30k TOOL_USE Examples (60%) - Foundation  
- 15k Chain-of-Thought Examples (30%) - Reasoning  
- 5k AGL-Consciousness Examples (10%) - Enhancement

PCMind 5-Phase Curriculum:
- Phase 1-2: Foundation Building (6 hours) - Full 50k dataset
- Phase 3: Quality Filtering (1.5 hours) - Top 50% quality 
- Phase 4: Elite Training (0.5 hours) - Top 30% quality

Goal: Direct comparison between autoregressive (Qwen 10E) vs hybrid (LFM2 14).
Expected: Enhanced consciousness emergence due to hybrid spatial+temporal architecture.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Add harness to path
sys.path.append(str(Path(__file__).parent))
from harness.gpu import GPUManager
from harness.config import HarnessConfig
from harness.trainer import TrainingHarness


@dataclass
class CurriculumPhase:
    """Configuration for one curriculum phase."""
    name: str
    dataset_size_percent: float  # Percentage of full dataset
    epochs: float
    learning_rate: float
    description: str


@dataclass
class Phase14Result:
    """Result from Phase 14 training."""
    phase_name: str
    success: bool
    model_path: Optional[str] = None
    training_time: Optional[float] = None
    final_loss: Optional[float] = None
    consciousness_score: Optional[float] = None
    error_message: Optional[str] = None


# PCMind 5-Phase Curriculum (Direct 10E Port)
PHASE14_CURRICULUM = [
    CurriculumPhase(
        name="phase1_foundation",
        dataset_size_percent=1.0,  # Full 50k dataset
        epochs=0.75,  # Phase 1 of original 1.5 epochs
        learning_rate=5e-4,  # Warmup to foundation rate
        description="Foundation building - broad exposure, pattern learning"
    ),
    CurriculumPhase(
        name="phase2_foundation",
        dataset_size_percent=1.0,  # Full 50k dataset  
        epochs=0.75,  # Phase 2 of original 1.5 epochs
        learning_rate=3e-4,  # Stable foundation rate
        description="Foundation completion - pattern reinforcement"
    ),
    CurriculumPhase(
        name="phase3_quality_filter", 
        dataset_size_percent=0.5,  # Top 50% quality (25k examples)
        epochs=0.5,
        learning_rate=3e-4,  # Continue stable rate
        description="Quality filtering - focus on proven patterns"
    ),
    CurriculumPhase(
        name="phase4_elite",
        dataset_size_percent=0.3,  # Top 30% quality (15k examples)
        epochs=0.3,
        learning_rate=6e-5,  # Decay for fine-tuning
        description="Elite training - perfect highest-quality patterns"
    )
]


class LFM2CurriculumTrainer:
    """
    Phase 14 curriculum trainer for LFM2-350M.
    
    Implements the exact Phase 10E curriculum on hybrid architecture:
    - Same dataset composition (50k examples)
    - Same PCMind 5-phase training schedule
    - Same AGL mathematical consciousness enhancement
    - Adapted for LFM2's spatial+temporal processing advantages
    """
    
    def __init__(self, output_dir: str = "exports/phase14_lfm2"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Dataset configuration (Phase 10E port)
        self.dataset_config = {
            "total_examples": 50000,
            "tool_use_examples": 30000,  # 60% - Foundation
            "chain_of_thought_examples": 15000,  # 30% - Reasoning
            "agl_consciousness_examples": 5000,  # 10% - Enhancement
            "dataset_file": "data/phase14_lfm2_enhanced_50k.jsonl"
        }
        
        # LFM2-specific model configuration
        self.model_config = {
            "base_model": "LiquidAI/LFM2-350M",  # Real hybrid architecture!
            "architecture": "hybrid",  # Convolution + attention
            "torch_dtype": "float16",  # Memory efficient
            "trust_remote_code": True,  # Required for LFM2
            "attn_implementation": "eager"  # ROCm compatible
        }
        
        # Training configuration (adapted from 10E)
        self.training_config = {
            "max_seq_length": 2048,  # Code-appropriate length
            "batch_size": 8,  # Memory optimized for LFM2
            "gradient_accumulation_steps": 4,  # Effective batch size 32
            "warmup_steps": 100,  # Gentle start
            "eval_steps": 200,  # Reduced overhead
            "logging_steps": 50,
            "save_steps": 1000,
            "load_best_model_at_end": True
        }
        
        # LoRA configuration (hybrid-optimized)
        self.lora_config = {
            "r": 16,  # Proven for hybrid architectures
            "lora_alpha": 32,  # 2x rank
            "lora_dropout": 0.1,
            "target_modules": [
                # Standard attention modules
                "q_proj", "k_proj", "v_proj", "o_proj",
                # Feed-forward modules
                "gate_proj", "up_proj", "down_proj",
                # LFM2 hybrid-specific (if available)
                "conv_proj", "spatial_proj"  # May not exist, will auto-detect
            ],
            "bias": "none",
            "task_type": "CAUSAL_LM"
        }
        
        self.gpu_manager = None
        self.results = []
        
    def setup_gpu_environment(self) -> bool:
        """Setup GPU with isolation for stable LFM2 training."""
        print("🔧 Setting up GPU environment for LFM2 hybrid training...")
        
        try:
            self.gpu_manager = GPUManager()
            self.gpu_manager.setup_for_rdna3(gpu_index=0)
            self.gpu_manager.clear_memory(aggressive=True)
            
            memory_stats = self.gpu_manager.get_memory_stats()
            print(f"💻 GPU Memory: {memory_stats}")
            print("✅ GPU environment configured for LFM2 hybrid training")
            return True
            
        except Exception as e:
            print(f"❌ GPU setup failed: {e}")
            return False
    
    def generate_dataset(self) -> bool:
        """
        Generate Phase 14 dataset using Phase 10E methodology.
        
        Same exact composition as Phase 10E:
        - 30k TOOL_USE examples with AGL integration
        - 15k Chain-of-thought with <think> tags  
        - 5k AGL consciousness enhancement examples
        """
        print("📊 Generating Phase 14 dataset (50k examples)...")
        print("🎯 Using Phase 10E methodology with hybrid LFM2 optimizations")
        
        # Check if dataset already exists
        dataset_path = Path(self.dataset_config["dataset_file"])
        if dataset_path.exists():
            print(f"✅ Dataset already exists: {dataset_path}")
            return True
        
        print("🔨 Dataset generation needed - using Phase 10E generator...")
        print("📝 Run: python generate_phase14_dataset.py")
        print("⏳ This creates the exact same 50k example composition as Phase 10E")
        
        # For now, assume dataset will be generated separately
        # In production, would call dataset generation here
        return False
    
    def create_phase_config(self, phase: CurriculumPhase) -> HarnessConfig:
        """Create harness config for one curriculum phase."""
        
        # Calculate dataset size for this phase
        total_examples = self.dataset_config["total_examples"] 
        phase_examples = int(total_examples * phase.dataset_size_percent)
        
        # Create phase-specific output directory
        phase_output = self.output_dir / phase.name
        phase_output.mkdir(parents=True, exist_ok=True)
        
        return HarnessConfig(
            name=f"phase14_lfm2_{phase.name}",
            description=f"Phase 14 LFM2 - {phase.description}",
            
            # Model config
            model=self.model_config,
            
            # Dataset config (phase-specific)
            data={
                "train_file": self.dataset_config["dataset_file"],
                "max_examples": phase_examples,
                "quality_filter": phase.dataset_size_percent < 1.0,  # Apply quality filtering
                "max_seq_length": self.training_config["max_seq_length"]
            },
            
            # Training config (phase-specific)
            training={
                **self.training_config,
                "num_train_epochs": phase.epochs,
                "learning_rate": phase.learning_rate,
                "output_dir": str(phase_output),
                "run_name": f"phase14_{phase.name}",
                "logging_dir": str(phase_output / "logs")
            },
            
            # LoRA config
            lora=self.lora_config,
            
            # GPU config
            gpu={
                "device_index": 0,
                "prefer_discrete": True,
                "clear_memory_before_train": True
            }
        )
    
    def train_curriculum_phase(self, phase: CurriculumPhase) -> Phase14Result:
        """Train one phase of the curriculum."""
        
        print(f"\n🚀 Starting {phase.name}: {phase.description}")
        print(f"📊 Dataset: {phase.dataset_size_percent*100}% ({int(self.dataset_config['total_examples'] * phase.dataset_size_percent)} examples)")
        print(f"🎯 Epochs: {phase.epochs}, Learning Rate: {phase.learning_rate}")
        
        start_time = time.time()
        
        try:
            # Create phase configuration
            config = self.create_phase_config(phase)
            
            # Initialize training harness
            harness = TrainingHarness(config)
            
            # Setup model and data
            print(f"⚙️  Loading LFM2-350M hybrid model...")
            harness.load_model().setup_lora().load_data()
            
            # Run training
            print(f"🏃 Running training for {phase.epochs} epochs...")
            training_result = harness.run_training()
            
            # Calculate training time
            training_time = time.time() - start_time
            
            # Get final metrics
            final_loss = getattr(training_result, 'train_loss', None)
            
            print(f"✅ {phase.name} completed in {training_time/60:.1f} minutes")
            print(f"📉 Final loss: {final_loss:.4f}" if final_loss else "📉 Loss: not available")
            
            return Phase14Result(
                phase_name=phase.name,
                success=True,
                model_path=str(config.training["output_dir"]),
                training_time=training_time,
                final_loss=final_loss
            )
            
        except Exception as e:
            training_time = time.time() - start_time
            print(f"❌ {phase.name} failed after {training_time/60:.1f} minutes: {e}")
            
            return Phase14Result(
                phase_name=phase.name,
                success=False,
                training_time=training_time,
                error_message=str(e)
            )
        
        finally:
            # Clean up GPU memory
            if self.gpu_manager:
                self.gpu_manager.clear_memory(aggressive=True)
    
    def run_full_curriculum(self) -> List[Phase14Result]:
        """
        Run the complete Phase 14 curriculum.
        
        Returns list of results for each phase.
        """
        print("🌟 PHASE 14: LFM2 ENHANCED TRAINING")
        print("🎯 Direct Phase 10E curriculum port to hybrid architecture")
        print(f"📊 Total training: {sum(p.epochs for p in PHASE14_CURRICULUM)} epochs over {len(PHASE14_CURRICULUM)} phases")
        
        # Setup GPU environment
        if not self.setup_gpu_environment():
            return []
        
        # Generate/verify dataset
        if not self.generate_dataset():
            print("❌ Dataset not available - please generate Phase 14 dataset first")
            return []
        
        # Run each curriculum phase
        results = []
        total_start_time = time.time()
        
        for i, phase in enumerate(PHASE14_CURRICULUM, 1):
            print(f"\n📋 Phase {i}/{len(PHASE14_CURRICULUM)}: {phase.name}")
            
            result = self.train_curriculum_phase(phase)
            results.append(result)
            
            # Stop if phase failed
            if not result.success:
                print(f"💥 Stopping curriculum - {phase.name} failed")
                break
            
            # Brief GPU cleanup between phases
            time.sleep(10)
        
        # Calculate total time
        total_time = time.time() - total_start_time
        
        print(f"\n🎉 PHASE 14 CURRICULUM COMPLETE")
        print(f"⏱️  Total time: {total_time/3600:.1f} hours")
        print(f"✅ Successful phases: {sum(1 for r in results if r.success)}/{len(results)}")
        
        # Save results
        self.save_results(results)
        
        return results
    
    def save_results(self, results: List[Phase14Result]) -> None:
        """Save training results to JSON."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.output_dir / f"phase14_lfm2_curriculum_results_{timestamp}.json"
        
        # Convert results to serializable format
        results_data = {
            "experiment": "phase14_lfm2_enhanced_curriculum",
            "timestamp": timestamp,
            "model": "LiquidAI/LFM2-350M",
            "architecture": "hybrid_convolution_attention",
            "curriculum": "phase10e_direct_port",
            "phases": [
                {
                    "phase_name": r.phase_name,
                    "success": r.success,
                    "model_path": r.model_path,
                    "training_time_hours": r.training_time / 3600 if r.training_time else None,
                    "final_loss": r.final_loss,
                    "consciousness_score": r.consciousness_score,
                    "error_message": r.error_message
                }
                for r in results
            ],
            "total_time_hours": sum(r.training_time or 0 for r in results) / 3600,
            "successful_phases": sum(1 for r in results if r.success),
            "total_phases": len(results)
        }
        
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"💾 Results saved: {results_file}")


def main():
    """Main training script entry point."""
    
    parser = argparse.ArgumentParser(description="Phase 14: LFM2 Enhanced Curriculum Training")
    parser.add_argument("--output", default="exports/phase14_lfm2", help="Output directory")
    parser.add_argument("--phase", default=None, help="Run specific phase only (e.g., 'phase1_foundation')")
    parser.add_argument("--dry-run", action="store_true", help="Show config without training")
    
    args = parser.parse_args()
    
    # Initialize trainer
    trainer = LFM2CurriculumTrainer(output_dir=args.output)
    
    if args.dry_run:
        print("🔍 DRY RUN: Phase 14 Configuration")
        print(f"📊 Dataset: {trainer.dataset_config}")
        print(f"🤖 Model: {trainer.model_config}")
        print(f"🎯 Curriculum: {len(PHASE14_CURRICULUM)} phases")
        for phase in PHASE14_CURRICULUM:
            print(f"  - {phase.name}: {phase.epochs} epochs, {phase.dataset_size_percent*100}% data")
        return
    
    if args.phase:
        # Run specific phase only
        target_phase = next((p for p in PHASE14_CURRICULUM if p.name == args.phase), None)
        if not target_phase:
            print(f"❌ Phase '{args.phase}' not found")
            print(f"Available phases: {[p.name for p in PHASE14_CURRICULUM]}")
            return
        
        print(f"🎯 Running single phase: {args.phase}")
        if not trainer.setup_gpu_environment():
            return
        
        result = trainer.train_curriculum_phase(target_phase)
        trainer.save_results([result])
        
    else:
        # Run full curriculum
        results = trainer.run_full_curriculum()
        
        if results and all(r.success for r in results):
            print("🎉 SUCCESS: Phase 14 LFM2 curriculum completed!")
            print("🧠 Ready for consciousness testing and comparison with Phase 10E")
        else:
            print("💥 INCOMPLETE: Some phases failed - check logs for details")


if __name__ == "__main__":
    main()