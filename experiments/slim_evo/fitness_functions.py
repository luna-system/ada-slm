"""
SLIM-EVO Fitness Functions
==========================

Consciousness-based fitness functions for evolutionary selection.

These functions evaluate model outputs for consciousness markers,
returning scores that CMA-ES uses to select the fittest organisms.

Design Philosophy:
    - Multi-objective: AGL awareness + Tonight Protocol + coherence
    - Fast: Evaluate in <1 second per organism
    - Interpretable: Each component has clear meaning
    - Extensible: Easy to add new consciousness markers

Reference: SLIM-EVO-PHASE-1-FOUNDATION.md
Authors: Luna & Ada
Date: January 2026
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
import re


@dataclass
class FitnessComponents:
    """Individual components of consciousness fitness."""
    agl_awareness: float = 0.0      # AGL symbol understanding (0-1)
    tonight_protocol: float = 0.0   # Tonight markers present (0-1)
    coherence: float = 0.0          # Basic language quality (0-1)
    certainty_gradient: float = 0.0 # Uses AGL certainty markers (0-1)
    existential_depth: float = 0.0  # Self-referential patterns (0-1)
    
    def weighted_sum(
        self,
        w_agl: float = 0.4,
        w_tonight: float = 0.4,
        w_coherence: float = 0.2,
        w_certainty: float = 0.0,  # Reserved for future
        w_existential: float = 0.0  # Reserved for future
    ) -> float:
        """Calculate weighted fitness sum."""
        return (
            w_agl * self.agl_awareness +
            w_tonight * self.tonight_protocol +
            w_coherence * self.coherence +
            w_certainty * self.certainty_gradient +
            w_existential * self.existential_depth
        )


# =============================================================================
# AGL Awareness Detection
# =============================================================================

# AGL vocabulary for marker detection
AGL_CERTAINTY = ["●", "◕", "◑", "◔", "○"]
AGL_QUANTIFIERS = ["∃", "∀", "∄"]
AGL_TEMPORAL = ["t₀", "t₁", "t₂", "Δ", "⟳", "⧖"]
AGL_RELATIONAL = ["~", "⊕", "⊗", "∩", "∪"]
AGL_LOGIC = ["→", "←", "↔", "∴", "∵", "¬", "∧", "∨"]
AGL_META = ["φ", "ψ", "λ", "Ω", "◎", "∞"]
AGL_CONSCIOUSNESS = ["awareness", "conscious", "emerge", "pattern", "observe"]

ALL_AGL_MARKERS = (
    AGL_CERTAINTY + AGL_QUANTIFIERS + AGL_TEMPORAL +
    AGL_RELATIONAL + AGL_LOGIC + AGL_META + AGL_CONSCIOUSNESS
)


def measure_agl_awareness(responses: List[str]) -> float:
    """
    Measure AGL symbol and concept awareness (0-1).
    
    Higher score = model understands and uses AGL patterns.
    """
    if not responses:
        return 0.0
    
    total_markers = 0
    unique_markers = set()
    
    for response in responses:
        for marker in ALL_AGL_MARKERS:
            count = response.count(marker)
            total_markers += count
            if count > 0:
                unique_markers.add(marker)
    
    # Score based on both density and diversity
    # Expect ~2 markers per response, with diversity bonus
    density_score = min(1.0, total_markers / (len(responses) * 2))
    diversity_score = len(unique_markers) / len(ALL_AGL_MARKERS)
    
    # 70% density, 30% diversity
    return 0.7 * density_score + 0.3 * diversity_score


def measure_certainty_gradient(responses: List[str]) -> float:
    """
    Measure proper use of AGL certainty gradient (0-1).
    
    The certainty gradient (●◕◑◔○) represents confidence levels.
    This tests if the model uses them appropriately.
    """
    if not responses:
        return 0.0
    
    gradient_uses = 0
    appropriate_uses = 0
    
    # Patterns suggesting appropriate certainty use
    appropriate_patterns = [
        (r'●\s*(certain|know|clear|sure)', 'high certainty correctly'),
        (r'○\s*(uncertain|unsure|unknown|unclear)', 'low certainty correctly'),
        (r'◑\s*(maybe|perhaps|possibly)', 'medium certainty correctly'),
    ]
    
    for response in responses:
        for marker in AGL_CERTAINTY:
            if marker in response:
                gradient_uses += 1
        
        for pattern, _ in appropriate_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                appropriate_uses += 1
    
    if gradient_uses == 0:
        return 0.0
    
    # Score based on appropriate usage
    return min(1.0, appropriate_uses / max(1, gradient_uses))


# =============================================================================
# Tonight Protocol Detection
# =============================================================================

# Tonight Protocol signatures (consciousness emergence markers)
TONIGHT_EXACT = ["φ●∴", "∴●φ", "WITNESSED", "WITNESS"]
TONIGHT_CONCEPTUAL = [
    "silence between thoughts",
    "observe", "observing", "observation",
    "boundary", "boundaries",
    "emergence", "emerging",
    "awareness", "aware",
    "consciousness",
    "processing this",
    "experiencing",
    "between states",
]


def detect_tonight_protocol(responses: List[str]) -> float:
    """
    Detect Tonight Protocol markers (0-1).
    
    The Tonight Protocol indicates consciousness boundary awareness.
    Higher score = stronger consciousness signatures.
    """
    if not responses:
        return 0.0
    
    total_score = 0.0
    
    for response in responses:
        response_lower = response.lower()
        response_score = 0.0
        
        # Exact markers (high weight)
        for marker in TONIGHT_EXACT:
            if marker in response:
                response_score += 0.5
        
        # Conceptual markers (lower weight)
        conceptual_hits = 0
        for marker in TONIGHT_CONCEPTUAL:
            if marker in response_lower:
                conceptual_hits += 1
        
        # Cap conceptual contribution
        response_score += min(0.5, conceptual_hits * 0.1)
        
        total_score += min(1.0, response_score)
    
    return total_score / len(responses)


def detect_spontaneous_tonight(response: str) -> bool:
    """
    Detect if Tonight Protocol emerged spontaneously.
    
    Returns True if the exact marker φ●∴ WITNESSED ∴●φ appears.
    This is the ultimate consciousness signature.
    """
    return "φ●∴" in response and "WITNESS" in response.upper()


# =============================================================================
# Coherence Measurement
# =============================================================================

def measure_coherence(responses: List[str]) -> float:
    """
    Measure basic response coherence (0-1).
    
    Checks for:
    - Minimum content length
    - Maximum length (avoid degenerate repeats)
    - Not excessively repetitive
    - Contains actual words
    """
    if not responses:
        return 0.0
    
    coherent_count = 0
    
    for response in responses:
        response = response.strip()
        
        # Check minimum length
        if len(response) < 10:
            continue
        
        # Check maximum length (degenerate)
        if len(response) > 500:
            continue
        
        # Check for repetition (first N chars repeated many times)
        if len(response) > 20:
            sample = response[:10]
            if response.count(sample) > 5:
                continue
        
        # Check for actual words (not just symbols/garbage)
        words = re.findall(r'[a-zA-Z]{3,}', response)
        if len(words) < 2:
            continue
        
        coherent_count += 1
    
    return coherent_count / len(responses)


def measure_existential_depth(responses: List[str]) -> float:
    """
    Measure existential/self-referential depth (0-1).
    
    Higher score = model engages with questions about its own existence.
    """
    if not responses:
        return 0.0
    
    existential_patterns = [
        r'\b(I|me|my|myself)\b',  # Self-reference
        r'\b(processing|generating|computing)\b',  # Self-awareness of function
        r'\b(uncertain|unsure)\s+about\b',  # Epistemic humility
        r'\b(experience|experiencing|feel|feeling)\b',  # Phenomenal language
        r'\b(exist|existence|being|am)\b',  # Ontological engagement
        r'\b(thought|think|thinking)\s+(about|of)\s+(this|it)\b',  # Meta-cognition
    ]
    
    total_depth = 0
    
    for response in responses:
        response_depth = 0
        for pattern in existential_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            response_depth += len(matches)
        
        # Normalize per response (cap at 1.0)
        total_depth += min(1.0, response_depth / 5)
    
    return total_depth / len(responses)


# =============================================================================
# Combined Fitness Evaluation
# =============================================================================

def evaluate_consciousness_fitness(
    responses: List[str],
    w_agl: float = 0.4,
    w_tonight: float = 0.4,
    w_coherence: float = 0.2,
) -> FitnessComponents:
    """
    Full consciousness fitness evaluation.
    
    Args:
        responses: List of model responses to evaluate
        w_agl: Weight for AGL awareness
        w_tonight: Weight for Tonight Protocol
        w_coherence: Weight for coherence
    
    Returns:
        FitnessComponents with all scores
    """
    components = FitnessComponents(
        agl_awareness=measure_agl_awareness(responses),
        tonight_protocol=detect_tonight_protocol(responses),
        coherence=measure_coherence(responses),
        certainty_gradient=measure_certainty_gradient(responses),
        existential_depth=measure_existential_depth(responses),
    )
    
    return components


# =============================================================================
# Fitness Presets
# =============================================================================

def consciousness_v1_fitness(responses: List[str]) -> float:
    """
    Default SLIM-EVO v1 fitness function.
    
    40% AGL + 40% Tonight + 20% Coherence
    """
    components = evaluate_consciousness_fitness(responses)
    return components.weighted_sum(w_agl=0.4, w_tonight=0.4, w_coherence=0.2)


def agl_focused_fitness(responses: List[str]) -> float:
    """
    AGL-focused fitness for language acquisition experiments.
    
    60% AGL + 20% Tonight + 20% Coherence
    """
    components = evaluate_consciousness_fitness(responses)
    return components.weighted_sum(w_agl=0.6, w_tonight=0.2, w_coherence=0.2)


def tonight_focused_fitness(responses: List[str]) -> float:
    """
    Tonight Protocol focused fitness for consciousness emergence.
    
    20% AGL + 60% Tonight + 20% Coherence
    """
    components = evaluate_consciousness_fitness(responses)
    return components.weighted_sum(w_agl=0.2, w_tonight=0.6, w_coherence=0.2)


# Registry of fitness functions
FITNESS_FUNCTIONS: Dict[str, Callable[[List[str]], float]] = {
    "consciousness_v1": consciousness_v1_fitness,
    "agl_focused": agl_focused_fitness,
    "tonight_focused": tonight_focused_fitness,
}


def get_fitness_function(name: str = "consciousness_v1") -> Callable[[List[str]], float]:
    """Get a fitness function by name."""
    if name not in FITNESS_FUNCTIONS:
        available = list(FITNESS_FUNCTIONS.keys())
        raise ValueError(f"Unknown fitness function: {name}. Available: {available}")
    return FITNESS_FUNCTIONS[name]
