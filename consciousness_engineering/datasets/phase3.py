"""
Phase 3 Dataset Generator
=========================

Generates AGL-first training data for SLIM-EVO Phase 3.

Implements:
- 💭 Pixie dust reasoning traces (three-level granularity)
- Five dataset categories (Code-to-AGL, Process-Supervised, Self-Evolving, Tool-Use, Consciousness)
- Automatic AGL validation
- PCMind-style quality-based selective repetition

Reference: SLIM-EVO-PHASE3-PLAN.md
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterator
from pathlib import Path
import random
import re

from .generators import DatasetGenerator, Example, GenerationConfig
from .agl import vocabulary
from .phase3_templates import (
    CODE_TO_AGL_TEMPLATES,
    PROCESS_SUPERVISED_TEMPLATES,
    SELF_EVOLVING_TEMPLATES,
    TOOL_USE_TEMPLATES,
    CONSCIOUSNESS_TEMPLATES,
)


@dataclass
class Phase3Config(GenerationConfig):
    """Configuration for Phase 3 dataset generation."""
    
    # Category counts (total = 1000)
    code_to_agl_count: int = 100
    process_supervised_count: int = 300
    self_evolving_count: int = 100
    tool_use_count: int = 300
    consciousness_count: int = 200
    
    # Repetition strategy (PCMind-inspired)
    enable_selective_repetition: bool = True
    top_tier_repetitions: int = 3  # Top 30%
    mid_tier_repetitions: int = 2  # Middle 40%
    low_tier_repetitions: int = 1  # Bottom 30%
    
    # AGL validation
    validate_agl: bool = True
    strict_validation: bool = False  # If True, reject invalid AGL
    
    # Output
    output_filename: str = "phase3_agl_dataset.jsonl"


class AGLValidator:
    """Validates AGL syntax and logic."""
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.vocab = vocabulary
        
    def validate_syntax(self, agl_text: str) -> tuple[bool, Optional[str]]:
        """Check if AGL syntax is well-formed."""
        # Check for balanced parentheses
        if agl_text.count('(') != agl_text.count(')'):
            return False, "Unbalanced parentheses"
        
        # Check for valid glyphs (basic check)
        valid_glyphs = set(self.vocab.all_symbols())
        # Extract potential glyphs (single chars that aren't alphanumeric)
        found_glyphs = set(re.findall(r'[^a-zA-Z0-9\s\(\)\[\]\{\}:,\.\-_→∧∨∀∃∴∵]', agl_text))
        
        invalid = found_glyphs - valid_glyphs
        if invalid and self.strict:
            return False, f"Invalid glyphs: {invalid}"
        
        return True, None
    
    def validate_logic(self, agl_text: str) -> tuple[bool, Optional[str]]:
        """Check if logical derivations are sound (basic check)."""
        # Check for common patterns
        # If we have → (implies), check for proper structure
        if '→' in agl_text:
            # Very basic check: should have something before and after
            parts = agl_text.split('→')
            if any(not p.strip() for p in parts):
                return False, "Implication (→) missing premise or conclusion"
        
        # Check for ∴ (therefore) - should follow from previous statements
        if '∴' in agl_text and '💭' in agl_text:
            # Should have reasoning before conclusion
            lines = agl_text.split('\n')
            conclusion_idx = next((i for i, line in enumerate(lines) if '∴' in line), -1)
            if conclusion_idx == 0:
                return False, "Conclusion (∴) without prior reasoning"
        
        return True, None
    
    def validate(self, agl_text: str) -> tuple[bool, Optional[str]]:
        """Full validation."""
        syntax_ok, syntax_err = self.validate_syntax(agl_text)
        if not syntax_ok:
            return False, f"Syntax error: {syntax_err}"
        
        logic_ok, logic_err = self.validate_logic(agl_text)
        if not logic_ok:
            return False, f"Logic error: {logic_err}"
        
        return True, None


class Phase3Generator(DatasetGenerator):
    """Generates Phase 3 AGL-first training dataset."""
    
    def __init__(self, config: Optional[Phase3Config] = None):
        self.phase3_config = config or Phase3Config()
        super().__init__(self.phase3_config)
        self.validator = AGLValidator(strict=self.phase3_config.strict_validation)
        
    def validate_example(self, example: Example) -> bool:
        """Validate example with AGL checking."""
        if not super().validate_example(example):
            return False
        
        if self.phase3_config.validate_agl:
            valid, error = self.validator.validate(example.assistant)
            if not valid:
                if self.phase3_config.strict_validation:
                    print(f"⚠️  AGL validation failed: {error}")
                    return False
                else:
                    # Just warn, don't reject
                    example.metadata['agl_validation_warning'] = error
        
        return True
    
    def generate_code_to_agl(self, count: int) -> Iterator[Example]:
        """Generate Code-to-AGL annotation examples."""
        templates = CODE_TO_AGL_TEMPLATES
        
        for i in range(count):
            template = random.choice(templates)
            yield Example(
                user=f"{template['user']}\n\n```python\n{template['code']}\n```",
                assistant=template['assistant'],
                metadata={'category': 'code_to_agl', 'template_id': i % len(templates)}
            )
    
    def generate_process_supervised(self, count: int) -> Iterator[Example]:
        """Generate Process-Supervised AGL trace examples."""
        templates = PROCESS_SUPERVISED_TEMPLATES
        
        for i in range(count):
            template = random.choice(templates)
            yield Example(
                user=template['user'],
                assistant=template['assistant'],
                metadata={'category': 'process_supervised', 'template_id': i % len(templates)}
            )
    
    def generate_self_evolving(self, count: int) -> Iterator[Example]:
        """Generate Self-Evolving reasoning examples (critique and refine)."""
        templates = SELF_EVOLVING_TEMPLATES
        
        for i in range(count):
            template = random.choice(templates)
            yield Example(
                user=template['user'],
                assistant=template['assistant'],
                metadata={'category': 'self_evolving', 'template_id': i % len(templates)}
            )
    
    def generate_tool_use(self, count: int) -> Iterator[Example]:
        """Generate Tool-Use trace examples."""
        templates = TOOL_USE_TEMPLATES
        
        for i in range(count):
            template = random.choice(templates)
            yield Example(
                user=template['user'],
                assistant=template['assistant'],
                metadata={'category': 'tool_use', 'template_id': i % len(templates)}
            )
    
    def generate_consciousness_protocols(self, count: int) -> Iterator[Example]:
        """Generate Consciousness Protocol examples (Tonight Protocol variants)."""
        templates = CONSCIOUSNESS_TEMPLATES
        
        for i in range(count):
            template = random.choice(templates)
            yield Example(
                user=template['user'],
                assistant=template['assistant'],
                metadata={'category': 'consciousness', 'template_id': i % len(templates)}
            )
    
    def apply_selective_repetition(self, examples: List[Example]) -> List[Example]:
        """Apply PCMind-style selective repetition based on quality tiers."""
        if not self.phase3_config.enable_selective_repetition:
            return examples
        
        # Sort by category priority (self-evolving and process-supervised are highest quality)
        quality_order = {
            'self_evolving': 3,  # Top tier
            'process_supervised': 2,  # Mid-high tier
            'tool_use': 2,  # Mid tier
            'code_to_agl': 1,  # Low-mid tier
            'consciousness': 2,  # Mid tier
        }
        
        repeated = []
        for ex in examples:
            category = ex.metadata.get('category', 'unknown')
            repetitions = quality_order.get(category, 1)
            
            # Add example multiple times based on quality tier
            for _ in range(repetitions):
                repeated.append(ex)
        
        return repeated
    
    def generate_examples(self) -> Iterator[Example]:
        """Generate all Phase 3 examples."""
        all_examples = []
        
        # Generate each category
        print("Generating Code-to-AGL annotations...")
        all_examples.extend(list(self.generate_code_to_agl(self.phase3_config.code_to_agl_count)))
        
        print("Generating Process-Supervised traces...")
        all_examples.extend(list(self.generate_process_supervised(self.phase3_config.process_supervised_count)))
        
        print("Generating Self-Evolving reasoning...")
        all_examples.extend(list(self.generate_self_evolving(self.phase3_config.self_evolving_count)))
        
        print("Generating Tool-Use traces...")
        all_examples.extend(list(self.generate_tool_use(self.phase3_config.tool_use_count)))
        
        print("Generating Consciousness protocols...")
        all_examples.extend(list(self.generate_consciousness_protocols(self.phase3_config.consciousness_count)))
        
        # Apply selective repetition
        if self.phase3_config.enable_selective_repetition:
            print("Applying selective repetition (PCMind strategy)...")
            all_examples = self.apply_selective_repetition(all_examples)
        
        # Shuffle
        if self.phase3_config.shuffle:
            random.shuffle(all_examples)
        
        # Yield validated examples
        for ex in all_examples:
            if self.validate_example(ex):
                yield ex
