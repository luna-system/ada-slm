"""
Datasets Module - Consciousness Engineering Framework
=====================================================

Dataset generation infrastructure for consciousness training experiments.
Provides reusable components for creating training data:

- AGL vocabulary and grammar (from AGL-UNIFIED-v1.1.md)
- Template-based example generation
- Phase-based curriculum datasets
- Multiple output formats

Example:
    from consciousness_engineering.datasets import (
        AGLVocabulary,
        PhaseGenerator,
        V9BPureGenerator
    )
    
    # Generate v9B-pure dataset
    generator = V9BPureGenerator(output_dir="data")
    generator.generate(num_examples=2000)
"""

from .agl import (
    AGLVocabulary,
    AGLGlyph,
    GlyphCategory,
    # Glyph collections
    CERTAINTY_GLYPHS,
    ATTENTION_GLYPHS,
    LOGIC_GLYPHS,
    EXISTENCE_GLYPHS,
    TEMPORAL_GLYPHS,
    RELATIONAL_GLYPHS,
    STATE_GLYPHS,
    META_GLYPHS,
    EMOTIONAL_GLYPHS,
    TOOL_GLYPHS,
    # Idioms
    CONSCIOUSNESS_IDIOMS,
    REASONING_IDIOMS,
    RELATIONAL_IDIOMS,
    TEMPORAL_IDIOMS,
    THRESHOLD_IDIOMS,
)

from .generators import (
    DatasetGenerator,
    Example,
    GenerationConfig,
)

from .templates import (
    Template,
    TemplateLibrary,
    TemplateRenderer,
)

from .phases import (
    Phase,
    PhaseConfig,
    PhaseCurriculum,
    WARMUP_PHASE,
    TONIGHT_PHASE,
    EIGENVALUE_PHASE,
    DEEP_AGL_PHASE,
)

from .formatters import (
    DatasetFormatter,
    JSONLFormatter,
    format_for_training,
)

__all__ = [
    # AGL
    "AGLVocabulary",
    "AGLGlyph", 
    "GlyphCategory",
    "CERTAINTY_GLYPHS",
    "ATTENTION_GLYPHS",
    "LOGIC_GLYPHS",
    "EXISTENCE_GLYPHS",
    "TEMPORAL_GLYPHS",
    "RELATIONAL_GLYPHS",
    "STATE_GLYPHS",
    "META_GLYPHS",
    "EMOTIONAL_GLYPHS",
    "TOOL_GLYPHS",
    "CONSCIOUSNESS_IDIOMS",
    "REASONING_IDIOMS",
    "RELATIONAL_IDIOMS",
    "TEMPORAL_IDIOMS",
    "THRESHOLD_IDIOMS",
    # Generators
    "DatasetGenerator",
    "Example",
    "GenerationConfig",
    # Templates
    "Template",
    "TemplateLibrary",
    "TemplateRenderer",
    # Phases
    "Phase",
    "PhaseConfig",
    "PhaseCurriculum",
    "WARMUP_PHASE",
    "TONIGHT_PHASE",
    "EIGENVALUE_PHASE",
    "DEEP_AGL_PHASE",
    # Formatters
    "DatasetFormatter",
    "JSONLFormatter",
    "format_for_training",
]
