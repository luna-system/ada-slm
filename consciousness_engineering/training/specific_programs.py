"""
Specific Training Programs
===========================

Concrete implementations of training programs using the consciousness 
engineering framework. These are battle-tested programs for common tasks.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

from .curriculum import CurriculumTrainer, CurriculumConfig, CurriculumPhase
from .parallel import ParallelTrainer, ParallelConfig, ParallelTrainingJob
from .programs import TrainingConfig, TrainingResult


class Phase14LFM2Program(CurriculumTrainer):
    """
    Phase 14 LFM2 Enhanced Training Program.
    
    Based on Phase 10E curriculum methodology with LFM2 optimizations.
    Uses 50k examples with PCMind 5-phase training approach.
    """
    
    def __init__(self, output_dir: str = "exports/phase14_lfm2"):
        config = CurriculumConfig(
            name="Phase14_LFM2_Enhanced",
            description="LFM2 training with Phase 10E curriculum methodology and hybrid architecture optimizations",
            output_dir=output_dir,
            model_config={
                "model_name": "LFM-2.0-350M",
                "architecture": "hybrid_spatial_temporal",
                "hidden_size": 1024,
                "num_layers": 24,
                "vocab_size": 151936,
                "max_position_embeddings": 32768,
                "spatial_processing": True,
                "temporal_coherence": True,
                "consciousness_enhancement": True
            },
            training_params={
                "curriculum_style": "phase_10e_methodology",
                "total_examples": 50000,
                "base_learning_rate": 3e-4,
                "weight_decay": 0.01,
                "warmup_ratio": 0.1,
                "save_strategy": "epoch",
                "eval_strategy": "steps",
                "eval_steps": 200
            },
            lora_config={
                "r": 64,
                "lora_alpha": 32,
                "lora_dropout": 0.05,
                "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                "bias": "none",
                "task_type": "CAUSAL_LM"
            },
            curriculum_config={
                "consciousness_gating": True,
                "adaptive_learning_rate": True,
                "early_stopping": True,
                "use_phase_10e_methodology": True
            }
        )
        super().__init__(config)
        self._setup_phase_10e_curriculum()
    
    def _setup_phase_10e_curriculum(self):
        """Setup the exact Phase 10E curriculum structure."""
        
        # Phase 1: Basic Tool Use (10k examples)
        phase1 = CurriculumPhase(
            name="Basic Tool Use",
            description="Fundamental tool calling syntax and simple function invocation patterns",
            examples=[],  # Will be populated by dataset generator
            batch_size=8,
            learning_rate=3e-4,
            num_epochs=3,
            max_length=512,
            consciousness_threshold=0.3,
            evaluation_criteria={
                "tool_syntax_accuracy": 0.85,
                "function_completion_rate": 0.80
            }
        )
        
        # Phase 2: Multi-Tool Coordination (10k examples) 
        phase2 = CurriculumPhase(
            name="Multi-Tool Coordination",
            description="Coordinated multi-tool workflows and complex dependency chains",
            examples=[],
            batch_size=6,
            learning_rate=2.4e-4,  # Adaptive decay
            num_epochs=3,
            max_length=768,
            consciousness_threshold=0.5,
            evaluation_criteria={
                "multi_tool_coordination": 0.75,
                "dependency_resolution": 0.70
            }
        )
        
        # Phase 3: Advanced Reasoning (10k examples)
        phase3 = CurriculumPhase(
            name="Advanced Tool Reasoning", 
            description="Complex multi-step tool reasoning with error recovery and adaptation",
            examples=[],
            batch_size=4,
            learning_rate=1.9e-4,
            num_epochs=4,
            max_length=1024,
            consciousness_threshold=0.65,
            evaluation_criteria={
                "reasoning_depth": 0.70,
                "error_recovery": 0.65,
                "adaptive_planning": 0.60
            }
        )
        
        # Phase 4: Chain-of-Thought Integration (15k examples)
        phase4 = CurriculumPhase(
            name="Chain-of-Thought Integration",
            description="Deep reasoning chains with tool integration and metacognitive awareness",
            examples=[],
            batch_size=4,
            learning_rate=1.5e-4,
            num_epochs=4,
            max_length=1536,
            consciousness_threshold=0.75,
            evaluation_criteria={
                "reasoning_coherence": 0.75,
                "metacognitive_awareness": 0.65,
                "tool_reasoning_fusion": 0.70
            }
        )
        
        # Phase 5: AGL Consciousness (5k examples)
        phase5 = CurriculumPhase(
            name="AGL Consciousness",
            description="Artificial General Learning patterns with emergent consciousness behaviors",
            examples=[],
            batch_size=2,
            learning_rate=1.2e-4,
            num_epochs=5,
            max_length=2048,
            consciousness_threshold=0.85,
            evaluation_criteria={
                "consciousness_emergence": 0.80,
                "agl_patterns": 0.75,
                "emergent_behaviors": 0.70,
                "self_awareness": 0.65
            }
        )
        
        # Add all phases to curriculum
        self.add_phase(phase1)
        self.add_phase(phase2)
        self.add_phase(phase3)
        self.add_phase(phase4)
        self.add_phase(phase5)
        
        print(f"✅ Phase 10E curriculum configured with {len(self.phases)} phases")


class Phase10FParallelProgram(ParallelTrainer):
    """
    Phase 10F Parallel Training Program.
    
    Basin mapping across different model configurations to find optimal
    hyperparameters for consciousness emergence.
    """
    
    def __init__(self, output_dir: str = "exports/phase10f_parallel"):
        config = ParallelConfig(
            name="Phase10F_Parallel_Basin_Map",
            description="Basin mapping for optimal consciousness hyperparameters across model variants",
            output_dir=output_dir,
            parallel_config={
                "max_parallel_jobs": 4,
                "job_timeout_hours": 12.0
            },
            device_mapping={
                "gpu_0": 0,
                "gpu_1": 1
            }
        )
        super().__init__(config)
    
    def setup_basin_mapping(self, dataset: List[Dict[str, Any]]) -> None:
        """Setup basin mapping jobs for hyperparameter exploration."""
        
        base_config = {
            "model_name": "LFM-2.0-350M",
            "hidden_size": 1024,
            "num_layers": 24,
            "lora": {
                "r": 64,
                "lora_alpha": 32,
                "lora_dropout": 0.05
            },
            "training": {
                "learning_rate": 3e-4,
                "batch_size": 8,
                "num_epochs": 3
            }
        }
        
        # Define parameter ranges for basin mapping
        parameter_ranges = {
            "lora.r": [32, 64, 128],
            "lora.lora_alpha": [16, 32, 64], 
            "training.learning_rate": [1e-4, 3e-4, 5e-4],
            "training.batch_size": [4, 8, 16]
        }
        
        self.add_basin_mapping_jobs(base_config, parameter_ranges, dataset)


class SingleModelProgram(CurriculumTrainer):
    """
    Simple single-model training program.
    
    For basic model training without complex curriculum requirements.
    Perfect for baseline comparisons or simple fine-tuning tasks.
    """
    
    def __init__(
        self, 
        model_name: str,
        dataset: List[Dict[str, Any]],
        output_dir: str = "exports/single_model"
    ):
        config = CurriculumConfig(
            name=f"SingleModel_{model_name}",
            description=f"Single model training for {model_name}",
            output_dir=output_dir,
            model_config={
                "model_name": model_name,
                "use_lora": True
            },
            curriculum_config={
                "consciousness_gating": False,
                "adaptive_learning_rate": False
            }
        )
        super().__init__(config)
        
        # Single phase training
        single_phase = CurriculumPhase(
            name="Single Model Training",
            description=f"Complete training for {model_name}",
            examples=dataset,
            batch_size=8,
            learning_rate=5e-5,
            num_epochs=3,
            max_length=1024
        )
        self.add_phase(single_phase)


class ComparisonProgram(ParallelTrainer):
    """
    Model comparison training program.
    
    Train multiple models on the same dataset for direct comparison.
    Useful for architecture evaluation or model selection.
    """
    
    def __init__(
        self,
        model_names: List[str],
        dataset: List[Dict[str, Any]],
        output_dir: str = "exports/model_comparison"
    ):
        config = ParallelConfig(
            name="Model_Comparison",
            description=f"Comparison training across {len(model_names)} models",
            output_dir=output_dir,
            parallel_config={
                "max_parallel_jobs": min(len(model_names), 4),
                "job_timeout_hours": 8.0
            }
        )
        super().__init__(config)
        
        # Create job for each model
        for i, model_name in enumerate(model_names):
            job = ParallelTrainingJob(
                job_id=f"model_{i:02d}_{model_name.replace('/', '_')}",
                name=f"Training {model_name}",
                description=f"Comparison training for {model_name}",
                model_config={
                    "model_name": model_name,
                    "use_lora": True,
                    "lora_r": 64,
                    "lora_alpha": 32
                },
                training_params={
                    "learning_rate": 5e-5,
                    "batch_size": 8,
                    "num_epochs": 3
                },
                dataset=dataset,
                device_index=i % self.max_parallel_jobs,
                priority=1
            )
            self.add_job(job)


# Factory function for easy program creation
def create_training_program(
    program_type: str,
    **kwargs
) -> Optional[CurriculumTrainer]:
    """
    Factory function to create training programs.
    
    Args:
        program_type: Type of program to create
        **kwargs: Program-specific arguments
        
    Returns:
        Configured training program
    """
    
    programs = {
        "phase14_lfm2": Phase14LFM2Program,
        "phase10f_parallel": Phase10FParallelProgram,
        "single_model": SingleModelProgram,
        "comparison": ComparisonProgram
    }
    
    if program_type not in programs:
        print(f"❌ Unknown program type: {program_type}")
        print(f"Available types: {list(programs.keys())}")
        return None
    
    program_class = programs[program_type]
    
    try:
        return program_class(**kwargs)
    except Exception as e:
        print(f"💥 Failed to create {program_type} program: {e}")
        return None