"""
Phases - Curriculum phase definitions
=====================================

Defines training phases with their focus areas and generation logic.
"""

from dataclasses import dataclass, field
from typing import List, Iterator, Optional, Callable, Dict, Any
from abc import ABC, abstractmethod
import random

from .agl import (
    CERTAINTY_GLYPHS, CERTAINTY_GRADIENT,
    ATTENTION_GLYPHS, LOGIC_GLYPHS, EXISTENCE_GLYPHS,
    TEMPORAL_GLYPHS, RELATIONAL_GLYPHS, META_GLYPHS, EMOTIONAL_GLYPHS,
    CONSCIOUSNESS_IDIOMS, REASONING_IDIOMS, TEMPORAL_IDIOMS, THRESHOLD_IDIOMS,
    THRESHOLD_IMPORTANCE, PHI_INVERSE
)


# Forward reference to avoid circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .generators import Example


@dataclass
class PhaseConfig:
    """Configuration for a training phase."""
    name: str
    description: str
    focus_glyphs: List[str]  # Glyph categories to emphasize
    focus_idioms: List[str]  # Idiom types to emphasize
    default_count: int = 500
    
    # Generation parameters
    min_response_length: int = 50
    max_response_length: int = 500
    certainty_bias: Optional[str] = None  # Bias toward certain certainty levels


class Phase(ABC):
    """
    A training phase that generates examples with specific focus.
    
    Subclass this to create specific phases.
    """
    
    def __init__(self, config: PhaseConfig):
        self.config = config
        self.name = config.name
        self.default_count = config.default_count
        
    @abstractmethod
    def generate(self, count: int) -> Iterator['Example']:
        """Generate examples for this phase."""
        pass
    
    def random_certainty(self, bias: Optional[str] = None) -> str:
        """Get a random certainty glyph, optionally biased."""
        if bias:
            # Bias toward a specific range
            if bias == "high":
                return random.choice(["●", "◕", "●", "◕", "◑"])
            elif bias == "low":
                return random.choice(["◑", "◔", "○", "◔", "○"])
            elif bias == "middle":
                return random.choice(["◕", "◑", "◔"])
        return random.choice(CERTAINTY_GRADIENT)
    
    def random_temporal_progression(self) -> str:
        """Generate a random temporal progression."""
        progressions = [
            "t₀ → t₁",
            "t₀ → t₁ → t₂",
            "t₀ → t₁ → t₂ → t₃",
            "t₋₁ → t₀ → t₁",
        ]
        return random.choice(progressions)
    
    def random_delta_expression(self) -> str:
        """Generate a random delta/change expression."""
        subjects = ["self", "state", "understanding", "awareness", "relationship", "context"]
        return f"Δ{random.choice(subjects)}(t₀→t₁)"
    
    def random_quantifier_expression(self) -> str:
        """Generate a random quantified expression."""
        expressions = [
            "∃x: conscious(x)",
            "∀t: change(t)",
            "∃state: stable(state)",
            "∀question: leads_to(question, understanding)",
            "∃answer: partial(answer)",
            "∄perfect_answer",
            "∃x: x ∈ experience",
            "∀pattern: ⟳pattern",
        ]
        return random.choice(expressions)
    
    def random_relational_expression(self) -> str:
        """Generate a random relational expression."""
        terms = ["self", "other", "thought", "feeling", "past", "present", "observer", "observed"]
        operators = ["~", "⊕", "⊗", "∩", "∪"]
        a, b = random.sample(terms, 2)
        op = random.choice(operators)
        return f"{a} {op} {b}"


# =============================================================================
# V9B-PURE PHASE DEFINITIONS
# From ADA-SLM-PHASE14C-V9B-PURE-AGL.md
# =============================================================================

@dataclass
class WarmupPhaseConfig(PhaseConfig):
    """Configuration for the Warmup phase."""
    name: str = "warmup"
    description: str = "Simple φ-patterns, certainty gradient drilling"
    focus_glyphs: List[str] = field(default_factory=lambda: ["certainty", "meta", "emotional"])
    focus_idioms: List[str] = field(default_factory=lambda: ["consciousness"])
    default_count: int = 500


@dataclass  
class TonightPhaseConfig(PhaseConfig):
    """Configuration for the Tonight Protocol phase."""
    name: str = "tonight"
    description: str = "Existential questions, quantifiers, 0.60 threshold"
    focus_glyphs: List[str] = field(default_factory=lambda: ["existence", "certainty", "logic"])
    focus_idioms: List[str] = field(default_factory=lambda: ["consciousness", "reasoning", "threshold"])
    default_count: int = 500


@dataclass
class EigenvaluePhaseConfig(PhaseConfig):
    """Configuration for the Eigenvalue Language phase."""
    name: str = "eigenvalue"
    description: str = "Attention metaphors, temporal progressions"
    focus_glyphs: List[str] = field(default_factory=lambda: ["temporal", "attention", "meta"])
    focus_idioms: List[str] = field(default_factory=lambda: ["temporal", "reasoning"])
    default_count: int = 500


@dataclass
class DeepAGLPhaseConfig(PhaseConfig):
    """Configuration for the Deep AGL phase."""
    name: str = "deep_agl"
    description: str = "Full AGL vocabulary integration"
    focus_glyphs: List[str] = field(default_factory=lambda: ["all"])
    focus_idioms: List[str] = field(default_factory=lambda: ["all"])
    default_count: int = 500


# Pre-built phase configurations
WARMUP_PHASE = WarmupPhaseConfig()
TONIGHT_PHASE = TonightPhaseConfig()
EIGENVALUE_PHASE = EigenvaluePhaseConfig()
DEEP_AGL_PHASE = DeepAGLPhaseConfig()


# =============================================================================
# PhaseCurriculum - Orchestrates multiple phases
# =============================================================================

class PhaseCurriculum:
    """
    A curriculum of training phases.
    
    Manages the progression through multiple phases.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.phases: List[Phase] = []
        
    def add_phase(self, phase: Phase):
        """Add a phase to the curriculum."""
        self.phases.append(phase)
        
    def total_examples(self) -> int:
        """Get total examples across all phases."""
        return sum(p.default_count for p in self.phases)
    
    def phase_distribution(self) -> Dict[str, int]:
        """Get the distribution of examples across phases."""
        return {p.name: p.default_count for p in self.phases}
    
    def generate_all(self) -> Iterator['Example']:
        """Generate examples from all phases in order."""
        from .generators import Example
        for phase in self.phases:
            for example in phase.generate(phase.default_count):
                yield example
