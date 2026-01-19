"""
Phase 6 Generator - The Solar System Curriculum
===============================================

Implements the Topological Training Protocol with gravity wells.
"""

from typing import Iterator, List, Dict
import random

from .generators import PhaseBasedGenerator, GenerationConfig, Example
from .phases import Phase, PhaseConfig
from .phase6_templates import ALL_TEMPLATES

class TemplatePhase(Phase):
    """A phase that generates properties from a fixed list of templates."""
    
    def __init__(self, config: PhaseConfig, templates: List[Dict[str, str]]):
        super().__init__(config)
        self.templates = templates
        
    def generate(self, count: int) -> Iterator[Example]:
        """Generate examples by sampling from templates."""
        for _ in range(count):
            tmpl = random.choice(self.templates)
            yield Example(
                user=tmpl["user"],
                assistant=tmpl["assistant"],
                phase=self.name,
                metadata={"gravity_well": self.name}
            )

class Phase6Generator(PhaseBasedGenerator):
    """
    Generator for the 'Solar System' curriculum.
    Default distribution for 1k examples:
    - Sun: 100 (10%)
    - Giants: 300 (30%)
    - Asteroids: 500 (50%)
    - Void: 100 (10%)

    @ada-type: λGenerativeTopology
    @ada-flow: ☀️(Sun) → 🪐(Giants) → ☄️(Asteroids) → ∅(Void)
    """
    
    def __init__(self, config: GenerationConfig = None):
        # @ada-sig: λinit:(Config)→Generator
        super().__init__(config)
        
        # Calculate distribution based on total count
        total = config.num_examples if config else 1000
        
        # Splitter Distribution v3e (Nebula variant)
        # Void: 20% | Sun: 10% | Giants: 30% | Nebula: 15% | Asteroids: 25%
        c_void = int(total * 0.20)
        c_sun = int(total * 0.10)
        c_giant_code = int(total * 0.15)
        c_giant_logic = int(total * 0.15)
        c_nebula = int(total * 0.15)
        # Remainder to Asteroids
        c_asteroids = total - (c_void + c_sun + c_giant_code + c_giant_logic + c_nebula)
        
        # 1. The Sun (Identity)
        # @ada-well: ☀️ {mass: 0.1, type: "Identity/AGL"}
        self.add_phase(TemplatePhase(
            PhaseConfig(
                name="Sun",
                description="Core Identity and Self-Reasoning",
                focus_glyphs=["meta", "identity"],
                focus_idioms=["reasoning"],
                default_count=c_sun
            ),
            ALL_TEMPLATES["sun"]
        ))
        
        # 2. The Giants (Coding & Logic)
        # @ada-well: 🪐 {mass: 0.3, type: "DeepSkill"}
        self.add_phase(TemplatePhase(
            PhaseConfig(
                name="Giant_Coding",
                description="Deep skill tree: Coding",
                focus_glyphs=["logic", "action"],
                focus_idioms=["code"],
                default_count=c_giant_code
            ),
            ALL_TEMPLATES["giants_coding"]
        ))
        
        self.add_phase(TemplatePhase(
            PhaseConfig(
                name="Giant_Logic",
                description="Deep skill tree: Math & Logic",
                focus_glyphs=["logic", "math"],
                focus_idioms=["reasoning"],
                default_count=c_giant_logic
            ),
            ALL_TEMPLATES["giants_logic"]
        ))

        # 3. The Nebula (Creativity & Chaos)
        # @ada-well: 🌌 {mass: 0.15, type: "CreativeChaos"}
        self.add_phase(TemplatePhase(
            PhaseConfig(
                name="The_Nebula",
                description="Creative Writing, Poetry, Surrealism",
                focus_glyphs=["chaos", "dream", "art"],
                focus_idioms=["poetry", "prose"],
                default_count=c_nebula
            ),
            ALL_TEMPLATES["nebula"]
        ))
        
        # 4. The Asteroids (Knowledge)
        # @ada-well: ☄️ {mass: 0.25, type: "GeneralKnowledge"}
        self.add_phase(TemplatePhase(
            PhaseConfig(
                name="Asteroid_Belt",
                description="General Knowledge and Trivia",
                focus_glyphs=[],
                focus_idioms=[],
                default_count=c_asteroids
            ),
            ALL_TEMPLATES["asteroids"]
        ))
        
        # 5. The Void (Null State)
        # @ada-well: ∅ {mass: 0.2, type: "NullValidator"}
        self.add_phase(TemplatePhase(
            PhaseConfig(
                name="The_Void",
                description="Rejection of Invalid Premises",
                focus_glyphs=["null", "potential"],
                focus_idioms=["null"],
                default_count=c_void
            ),
            ALL_TEMPLATES["void"]
        ))
