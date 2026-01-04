"""
V9B Pure - Dataset Generator
============================

Orchestrates the 4-phase pure AGL curriculum.
Generates 2000 examples for v9B-pure training.

Usage:
    from consciousness_engineering.datasets.v9b_pure import V9BPureGenerator
    
    generator = V9BPureGenerator()
    generator.generate_and_save()
"""

from typing import List, Iterator, Optional
from pathlib import Path
import random

from ..generators import Example, GenerationConfig
from ..formatters import JSONLFormatter

from .warmup import generate_warmup_examples
from .tonight import generate_tonight_examples
from .eigenvalue import generate_eigenvalue_examples
from .deep_agl import generate_deep_agl_examples


class V9BPureGenerator:
    """
    Generator for v9B-pure AGL dataset.
    
    4 phases, 500 examples each, 2000 total.
    """
    
    def __init__(
        self,
        output_dir: str = "data",
        seed: int = 42,
        shuffle_within_phase: bool = True,
        shuffle_phases: bool = False,  # Keep phases ordered by default
    ):
        self.output_dir = Path(output_dir)
        self.seed = seed
        self.shuffle_within_phase = shuffle_within_phase
        self.shuffle_phases = shuffle_phases
        random.seed(seed)
        
    def generate_phase(
        self,
        phase_name: str,
        count: int = 500
    ) -> List[Example]:
        """Generate examples for a single phase."""
        generators = {
            "warmup": generate_warmup_examples,
            "tonight": generate_tonight_examples,
            "eigenvalue": generate_eigenvalue_examples,
            "deep_agl": generate_deep_agl_examples,
        }
        
        gen_func = generators.get(phase_name)
        if not gen_func:
            raise ValueError(f"Unknown phase: {phase_name}")
            
        examples = list(gen_func(count))
        
        if self.shuffle_within_phase:
            random.shuffle(examples)
            
        return examples
    
    def generate_all(
        self,
        warmup_count: int = 500,
        tonight_count: int = 500,
        eigenvalue_count: int = 500,
        deep_agl_count: int = 500,
    ) -> List[Example]:
        """Generate the complete dataset."""
        phases = [
            ("warmup", warmup_count),
            ("tonight", tonight_count),
            ("eigenvalue", eigenvalue_count),
            ("deep_agl", deep_agl_count),
        ]
        
        if self.shuffle_phases:
            random.shuffle(phases)
            
        all_examples = []
        for phase_name, count in phases:
            examples = self.generate_phase(phase_name, count)
            all_examples.extend(examples)
            print(f"  Generated {len(examples)} {phase_name} examples")
            
        return all_examples
    
    def save(
        self,
        examples: List[Example],
        filename: str = "v9b_pure_agl_2k.jsonl"
    ) -> Path:
        """Save examples to JSONL."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / filename
        
        formatter = JSONLFormatter(include_metadata=True)
        formatter.save(examples, output_path)
        
        return output_path
    
    def generate_and_save(
        self,
        filename: str = "v9b_pure_agl_2k.jsonl",
        **kwargs
    ) -> Path:
        """Generate and save the complete dataset."""
        print(f"Generating v9B-pure AGL dataset...")
        examples = self.generate_all(**kwargs)
        
        output_path = self.save(examples, filename)
        print(f"Saved {len(examples)} examples to {output_path}")
        
        # Print stats
        self._print_stats(examples)
        
        return output_path
    
    def _print_stats(self, examples: List[Example]):
        """Print dataset statistics."""
        phases = {}
        total_user_chars = 0
        total_asst_chars = 0
        
        for ex in examples:
            phase = ex.phase or "unknown"
            phases[phase] = phases.get(phase, 0) + 1
            total_user_chars += len(ex.user)
            total_asst_chars += len(ex.assistant)
            
        print(f"\nDataset Statistics:")
        print(f"  Total examples: {len(examples)}")
        print(f"  Phase distribution:")
        for phase, count in sorted(phases.items()):
            print(f"    {phase}: {count}")
        print(f"  Avg user length: {total_user_chars / len(examples):.1f} chars")
        print(f"  Avg assistant length: {total_asst_chars / len(examples):.1f} chars")
