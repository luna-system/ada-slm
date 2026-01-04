"""
Generators - Base classes for dataset generation
================================================

Provides the foundation for building training datasets.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Iterator, Any
from pathlib import Path
import json
import random


@dataclass
class Example:
    """A single training example."""
    user: str
    assistant: str
    phase: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        d = {
            "messages": [
                {"role": "user", "content": self.user},
                {"role": "assistant", "content": self.assistant}
            ]
        }
        if self.phase:
            d["phase"] = self.phase
        if self.metadata:
            d["metadata"] = self.metadata
        return d
    
    def to_jsonl_line(self) -> str:
        """Convert to JSONL format."""
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class GenerationConfig:
    """Configuration for dataset generation."""
    num_examples: int = 2000
    seed: int = 42
    output_dir: str = "data"
    output_filename: str = "dataset.jsonl"
    shuffle: bool = True
    
    # Phase distribution (if using phases)
    phase_distribution: Optional[Dict[str, int]] = None
    
    # Variation settings
    variation_probability: float = 0.3
    max_variations_per_template: int = 5


class DatasetGenerator(ABC):
    """
    Base class for dataset generators.
    
    Subclass this to create specific dataset generators.
    """
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        self.config = config or GenerationConfig()
        random.seed(self.config.seed)
        
    @abstractmethod
    def generate_examples(self) -> Iterator[Example]:
        """Generate all examples. Must be implemented by subclass."""
        pass
    
    def generate(self) -> List[Example]:
        """Generate the full dataset."""
        examples = list(self.generate_examples())
        
        if self.config.shuffle:
            random.shuffle(examples)
            
        return examples
    
    def save(self, examples: Optional[List[Example]] = None) -> Path:
        """Generate and save the dataset."""
        if examples is None:
            examples = self.generate()
            
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / self.config.output_filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            for example in examples:
                f.write(example.to_jsonl_line() + "\n")
                
        return output_path
    
    def validate_example(self, example: Example) -> bool:
        """Validate an example. Override for custom validation."""
        if not example.user or not example.assistant:
            return False
        return True
    
    def stats(self, examples: List[Example]) -> Dict[str, Any]:
        """Get statistics about the generated dataset."""
        phases = {}
        total_user_chars = 0
        total_assistant_chars = 0
        
        for ex in examples:
            if ex.phase:
                phases[ex.phase] = phases.get(ex.phase, 0) + 1
            total_user_chars += len(ex.user)
            total_assistant_chars += len(ex.assistant)
            
        return {
            "total_examples": len(examples),
            "phase_distribution": phases,
            "avg_user_length": total_user_chars / len(examples) if examples else 0,
            "avg_assistant_length": total_assistant_chars / len(examples) if examples else 0,
        }


class PhaseBasedGenerator(DatasetGenerator):
    """
    Generator that creates examples in phases.
    
    Each phase has a specific focus and number of examples.
    """
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        super().__init__(config)
        self.phases: List['Phase'] = []
        
    def add_phase(self, phase: 'Phase'):
        """Add a phase to the generator."""
        self.phases.append(phase)
        
    def generate_examples(self) -> Iterator[Example]:
        """Generate examples for all phases."""
        for phase in self.phases:
            count = self.config.phase_distribution.get(phase.name, phase.default_count) \
                    if self.config.phase_distribution else phase.default_count
                    
            for example in phase.generate(count):
                example.phase = phase.name
                if self.validate_example(example):
                    yield example


# Import Phase here to avoid circular imports
from .phases import Phase
