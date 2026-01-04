"""
V9B Pure - Pure AGL Dataset Generator
=====================================

4-phase curriculum for pure AGL training:
1. Warmup - Certainty gradient, basic φ-patterns
2. Tonight - Existential questions, quantifiers, 0.60 threshold
3. Eigenvalue - Temporal progressions, attention metaphors
4. Deep AGL - Full vocabulary integration

From ADA-SLM-PHASE14C-V9B-PURE-AGL.md

Usage:
    from consciousness_engineering.datasets.v9b_pure import V9BPureGenerator
    
    generator = V9BPureGenerator(output_dir="data")
    generator.generate_and_save()
"""

# Import phase generators
from .warmup import generate_warmup_examples, get_all_warmup_templates
from .tonight import generate_tonight_examples, get_all_tonight_templates
from .eigenvalue import generate_eigenvalue_examples, get_all_eigenvalue_templates
from .deep_agl import generate_deep_agl_examples, get_all_deep_agl_templates
from .generator import V9BPureGenerator

__all__ = [
    "V9BPureGenerator",
    "generate_warmup_examples",
    "generate_tonight_examples",
    "generate_eigenvalue_examples",
    "generate_deep_agl_examples",
    "get_all_warmup_templates",
    "get_all_tonight_templates",
    "get_all_eigenvalue_templates",
    "get_all_deep_agl_templates",
]
