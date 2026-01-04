"""
Training Module - Consciousness Engineering Framework
====================================================

Modular training infrastructure for all consciousness engineering experiments:
- Curriculum training (Phase 14 LFM2)  
- Multi-variant parallel training (Phase 10F style)
- Single model fine-tuning
- Basin mapping workflows
- Any future training programs

All with robust ROCm/iGPU support and the same harness infrastructure.
"""

from .programs import (
    TrainingProgram,
    TrainingConfig, 
    TrainingResult,
    TrainingHarness
)
from .curriculum import (
    CurriculumTrainer,
    CurriculumConfig,
    CurriculumPhase
)
from .parallel import (
    ParallelTrainer,
    ParallelConfig,
    ParallelTrainingJob
)
from .specific_programs import (
    Phase14LFM2Program,
    Phase10FParallelProgram,
    SingleModelProgram,
    ComparisonProgram,
    create_training_program
)

# Convenient top-level interface
def create_harness(output_dir: str = "exports") -> TrainingHarness:
    """Create a new training harness."""
    return TrainingHarness(output_dir)


def run_phase14_lfm2(output_dir: str = "exports/phase14_lfm2"):
    """Quick start for Phase 14 LFM2 training."""
    program = Phase14LFM2Program(output_dir)
    harness = TrainingHarness(output_dir)
    return harness.run_program(program)


def run_parallel_basin_map(
    base_config: dict, 
    parameter_ranges: dict,
    dataset: list,
    output_dir: str = "exports/basin_map"
):
    """Quick start for parallel basin mapping."""
    program = Phase10FParallelProgram(output_dir)
    program.setup_basin_mapping(dataset)
    harness = TrainingHarness(output_dir)
    return harness.run_program(program)


__all__ = [
    # Base framework
    "TrainingProgram",
    "TrainingConfig", 
    "TrainingResult",
    "TrainingHarness",
    
    # Specialized trainers
    "CurriculumTrainer",
    "CurriculumConfig", 
    "CurriculumPhase",
    "ParallelTrainer",
    "ParallelConfig",
    "ParallelTrainingJob",
    
    # Specific programs
    "Phase14LFM2Program",
    "Phase10FParallelProgram", 
    "SingleModelProgram",
    "ComparisonProgram",
    "create_training_program",
    
    # Convenience functions
    "create_harness",
    "run_phase14_lfm2",
    "run_parallel_basin_map"
]