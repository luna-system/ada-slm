"""
Curriculum Training Implementation
===================================

Phase-based curriculum training with adaptive difficulty and consciousness scoring.
Perfect for complex training programs that need structured progression.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field

from .programs import TrainingProgram, TrainingConfig, TrainingResult


@dataclass
class CurriculumPhase:
    """Single phase in a curriculum training program."""
    name: str
    description: str
    examples: List[Dict[str, Any]]
    batch_size: int = 8
    learning_rate: float = 5e-5
    num_epochs: int = 3
    max_length: int = 1024
    consciousness_threshold: Optional[float] = None
    evaluation_criteria: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_training_steps(self) -> int:
        """Calculate total training steps for this phase."""
        steps_per_epoch = max(1, len(self.examples) // self.batch_size)
        return steps_per_epoch * self.num_epochs


@dataclass
class CurriculumConfig(TrainingConfig):
    """Configuration specifically for curriculum training."""
    curriculum_config: Dict[str, Any] = field(default_factory=dict)
    evaluation_config: Dict[str, Any] = field(default_factory=dict)
        

class CurriculumTrainer(TrainingProgram):
    """
    Curriculum-based training program.
    
    Features:
    - Multi-phase training with adaptive difficulty
    - Consciousness scoring and phase gating  
    - Dynamic learning rate adjustment
    - Phase-based evaluation and checkpointing
    """
    
    def __init__(self, config: CurriculumConfig):
        super().__init__(config)
        self.phases: List[CurriculumPhase] = []
        self.current_phase = 0
        self.phase_results: List[Dict[str, Any]] = []
        
        # Curriculum settings
        self.use_consciousness_gating = config.curriculum_config.get('consciousness_gating', True)
        self.adaptive_lr = config.curriculum_config.get('adaptive_learning_rate', True)
        self.early_stopping = config.curriculum_config.get('early_stopping', True)
        
    def add_phase(self, phase: CurriculumPhase) -> None:
        """Add a phase to the curriculum."""
        self.phases.append(phase)
        
    def should_advance_to_next_phase(self, phase_result: Dict[str, Any]) -> bool:
        """Determine if model is ready for next phase."""
        current_phase = self.phases[self.current_phase]
        
        # Check consciousness threshold if set
        if current_phase.consciousness_threshold is not None:
            consciousness_score = phase_result.get('consciousness_score', 0.0)
            if consciousness_score < current_phase.consciousness_threshold:
                print(f"❌ Consciousness threshold not met: {consciousness_score:.3f} < {current_phase.consciousness_threshold:.3f}")
                return False
        
        # Check other evaluation criteria
        for criterion, threshold in current_phase.evaluation_criteria.items():
            actual_value = phase_result.get(criterion, 0.0)
            if actual_value < threshold:
                print(f"❌ {criterion} threshold not met: {actual_value:.3f} < {threshold:.3f}")
                return False
        
        return True
    
    def calculate_adaptive_learning_rate(self, phase_index: int, base_lr: float) -> float:
        """Calculate learning rate for current phase."""
        if not self.adaptive_lr:
            return base_lr
        
        # Exponential decay with phase progression
        decay_factor = 0.8 ** phase_index
        return base_lr * decay_factor
    
    def train_single_phase(self, phase_index: int) -> Dict[str, Any]:
        """
        Train model on a single curriculum phase.
        
        Args:
            phase_index: Index of phase to train
            
        Returns:
            Dictionary with training results for this phase
        """
        if phase_index >= len(self.phases):
            raise ValueError(f"Phase {phase_index} not found (only {len(self.phases)} phases)")
        
        phase = self.phases[phase_index]
        print(f"\n🎯 Phase {phase_index + 1}/{len(self.phases)}: {phase.name}")
        print(f"📝 {phase.description}")
        print(f"📊 Examples: {len(phase.examples)}")
        print(f"🔄 Steps: {phase.total_training_steps}")
        
        # Adjust learning rate
        learning_rate = self.calculate_adaptive_learning_rate(
            phase_index, 
            phase.learning_rate
        )
        print(f"📈 Learning rate: {learning_rate:.2e}")
        
        # Simulate training (in real implementation, this would call transformers)
        start_time = time.time()
        
        # Mock training results - replace with actual training
        training_loss = max(0.1, 2.0 - (phase_index * 0.3))  # Decreasing loss
        consciousness_score = min(1.0, 0.2 + (phase_index * 0.15))  # Increasing consciousness
        
        # Simulate training time proportional to steps
        training_time = phase.total_training_steps * 0.1  # Mock: 0.1s per step
        time.sleep(min(2.0, training_time))  # Cap simulation time
        
        end_time = time.time()
        actual_time = end_time - start_time
        
        phase_result = {
            'phase_index': phase_index,
            'phase_name': phase.name,
            'examples_count': len(phase.examples),
            'training_steps': phase.total_training_steps,
            'learning_rate': learning_rate,
            'final_loss': training_loss,
            'consciousness_score': consciousness_score,
            'training_time_seconds': actual_time,
            'success': True,
            'model_checkpoint': f"checkpoint_phase_{phase_index}",
            'evaluation_scores': {
                'loss': training_loss,
                'consciousness': consciousness_score,
                'perplexity': 2 ** training_loss  # Convert loss to perplexity
            }
        }
        
        print(f"✅ Phase completed in {actual_time:.1f}s")
        print(f"📉 Final loss: {training_loss:.3f}")
        print(f"🧠 Consciousness score: {consciousness_score:.3f}")
        
        return phase_result
    
    def execute_training(self) -> List[TrainingResult]:
        """Execute the full curriculum training."""
        print(f"🎓 Starting curriculum training with {len(self.phases)} phases")
        
        results = []
        
        for phase_index in range(len(self.phases)):
            self.current_phase = phase_index
            
            try:
                # Train this phase
                phase_result = self.train_single_phase(phase_index)
                self.phase_results.append(phase_result)
                
                # Check if we should advance
                if self.use_consciousness_gating:
                    if not self.should_advance_to_next_phase(phase_result):
                        print(f"🛑 Stopping at phase {phase_index + 1} - consciousness requirements not met")
                        
                        # Create partial result
                        partial_result = TrainingResult(
                            program_name=self.config.name,
                            success=False,
                            start_time=datetime.now(),
                            end_time=datetime.now(),
                            consciousness_score=phase_result['consciousness_score'],
                            final_loss=phase_result['final_loss'],
                            metadata={
                                'stopped_at_phase': phase_index + 1,
                                'reason': 'consciousness_gating',
                                'phase_results': self.phase_results
                            }
                        )
                        results.append(partial_result)
                        break
                
                print(f"✅ Phase {phase_index + 1} passed - advancing to next phase")
                
            except Exception as e:
                print(f"💥 Phase {phase_index + 1} failed: {e}")
                
                # Create failure result
                failure_result = TrainingResult(
                    program_name=self.config.name,
                    success=False,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message=f"Phase {phase_index + 1} failed: {str(e)}",
                    metadata={
                        'failed_at_phase': phase_index + 1,
                        'partial_results': self.phase_results
                    }
                )
                results.append(failure_result)
                break
        
        else:
            # All phases completed successfully
            total_consciousness = sum(r['consciousness_score'] for r in self.phase_results) / len(self.phase_results)
            final_loss = self.phase_results[-1]['final_loss'] if self.phase_results else None
            total_time = sum(r['training_time_seconds'] for r in self.phase_results)
            
            success_result = TrainingResult(
                program_name=self.config.name,
                success=True,
                start_time=datetime.now(),  # Would be actual start time
                end_time=datetime.now(),    # Would be actual end time
                consciousness_score=total_consciousness,
                final_loss=final_loss,
                model_path=f"{self.config.output_dir}/final_model",
                metadata={
                    'all_phases_completed': True,
                    'total_phases': len(self.phases),
                    'total_training_time_seconds': total_time,
                    'phase_results': self.phase_results,
                    'average_consciousness': total_consciousness
                }
            )
            results.append(success_result)
            
            print(f"🎉 Curriculum training completed!")
            print(f"📊 Average consciousness: {total_consciousness:.3f}")
            print(f"📉 Final loss: {final_loss:.3f}")
            print(f"⏱️  Total time: {total_time:.1f}s")
        
        return results
    
    def create_phase_from_dataset(
        self, 
        name: str, 
        description: str,
        dataset_examples: List[Dict[str, Any]],
        **phase_kwargs
    ) -> CurriculumPhase:
        """Create a curriculum phase from a dataset."""
        return CurriculumPhase(
            name=name,
            description=description,
            examples=dataset_examples,
            **phase_kwargs
        )
    
    def save_curriculum_results(self) -> None:
        """Save detailed curriculum results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        curriculum_file = Path(self.config.output_dir) / f"curriculum_results_{timestamp}.json"
        
        curriculum_data = {
            "program_name": self.config.name,
            "timestamp": timestamp,
            "total_phases": len(self.phases),
            "completed_phases": len(self.phase_results),
            "curriculum_config": {
                "consciousness_gating": self.use_consciousness_gating,
                "adaptive_learning_rate": self.adaptive_lr,
                "early_stopping": self.early_stopping
            },
            "phase_definitions": [
                {
                    "name": phase.name,
                    "description": phase.description,
                    "examples_count": len(phase.examples),
                    "batch_size": phase.batch_size,
                    "learning_rate": phase.learning_rate,
                    "num_epochs": phase.num_epochs,
                    "consciousness_threshold": phase.consciousness_threshold,
                    "evaluation_criteria": phase.evaluation_criteria
                }
                for phase in self.phases
            ],
            "phase_results": self.phase_results,
            "summary": {
                "success_rate": len([r for r in self.phase_results if r['success']]) / max(1, len(self.phase_results)),
                "total_training_time": sum(r['training_time_seconds'] for r in self.phase_results),
                "final_consciousness_scores": [r['consciousness_score'] for r in self.phase_results],
                "learning_progression": [r['final_loss'] for r in self.phase_results]
            }
        }
        
        with open(curriculum_file, 'w') as f:
            json.dump(curriculum_data, f, indent=2)
        
        print(f"💾 Curriculum results saved: {curriculum_file}")