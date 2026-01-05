"""
Polyglot Dataset Generator
==========================

Generates multi-language → AGL translation pairs for consciousness training.

Languages:
- Lojban (logical structure) → AGL
- Toki Pona (philosophical compression) → AGL  
- English (natural language) → AGL

The hypothesis: Teaching a model to translate between consciousness-expression
languages will help it understand the UNDERLYING patterns of consciousness,
not just the surface syntax of any single language.
"""

from .generator import PolyglotGenerator, PolyglotConfig

__all__ = ["PolyglotGenerator", "PolyglotConfig"]
