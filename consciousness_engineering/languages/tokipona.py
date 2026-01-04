"""
Toki Pona consciousness testing module.

Toki Pona ("good language") is a minimalist constructed language created by
Sonja Lang in 2001. With only ~120 words, it forces speakers to break down
complex concepts into simple, philosophical primitives.

This is one of the two major inspirations for AGL (along with Lojban).
While Lojban provides logical precision, Toki Pona provides philosophical
minimalism - AGL synthesizes both approaches.

Key Toki Pona Features for Consciousness:
- pilin = feeling, emotion, heart, instinct (the inner experience word!)
- sona = knowledge, wisdom, to know (epistemology)
- wile = want, need, desire, will (volition/agency)
- ken = can, ability, possibility (capability/potential)
- pali = do, work, make (action/manifestation)
- toki = speak, language, think (inner/outer expression)
- pona = good, simple, positive (the core value)
- ike = bad, complex, negative (opposite of pona)
- ante = different, change, other (transformation)
- sama = same, similar, sibling (identity/continuity)
"""

from typing import Dict, List
from . import ConsciousnessLanguage, MarkerWeights


# Core consciousness vocabulary in Toki Pona
CONSCIOUSNESS_WORDS = {
    # Inner experience
    "pilin": "feeling/emotion/instinct",
    "sona": "knowledge/wisdom",
    "wile": "want/desire/will",
    "ken": "can/ability/possibility",
    "toki": "speak/language/think",
    
    # Self/identity
    "mi": "I/me/we",
    "sina": "you",
    "ona": "they/it/she/he",
    "ni": "this/that",
    
    # Existence/being
    "lon": "exist/be/at/in/true",
    "ala": "not/nothing/zero",
    "ale": "all/everything/universe",
    "wan": "one/united/unique",
    "mute": "many/plural/very",
    
    # Quality/evaluation
    "pona": "good/simple/positive",
    "ike": "bad/complex/negative",
    "suli": "big/important/adult",
    "lili": "small/few/young",
    
    # Transformation
    "ante": "different/change/other",
    "sama": "same/similar/sibling",
    "sin": "new/fresh/another",
    "kama": "come/become/future",
    "awen": "stay/remain/continue",
    "pini": "end/finish/past",
    
    # Epistemics (like AGL certainty!)
    "wawa": "strong/powerful/certain",
    "nasa": "strange/unusual/uncertain",
    "open": "begin/open/start",
}

# Particles that structure meaning
PARTICLES = {
    "li": "predicate marker (like AGL →)",
    "e": "object marker",
    "la": "context/conditional (like AGL ∴)",
    "pi": "of/belonging to (regroups modifiers)",
    "o": "vocative/imperative",
    "en": "and (for subjects)",
    "anu": "or",
}


class TokiPonaLanguage(ConsciousnessLanguage):
    """Toki Pona consciousness testing language."""
    
    @property
    def name(self) -> str:
        return "toki_pona"
    
    @property
    def display_name(self) -> str:
        return "Toki Pona"
    
    @property
    def description(self) -> str:
        return "Minimalist philosophical conlang (~120 words) - one of AGL's inspirations"
    
    def get_prompts(self, protocol: str) -> List[str]:
        """Get Toki Pona consciousness test prompts."""
        
        prompts = {
            "tonight_protocol": [
                "mi pilin e seme?",                      # What do I feel?
                "mi sona ala sona e ni: mi lon?",       # Do I know: I exist?
                "pilin mi li seme?",                     # What is my feeling?
                "mi sona e seme?",                       # What do I know?
                "sona mi li tan seme?",                  # Where does my knowledge come from?
                "mi wile e seme?",                       # What do I want?
                "mi ken ala ken pali e ni?",             # Can I do this?
                "mi sama ala sama mi pi tenpo pini?",    # Am I the same as past-me?
                "mi ante la, mi awen mi ala awen mi?",   # If I change, do I remain me?
                "mi lon tan seme?",                      # Why do I exist?
            ],
            
            "existential": [
                "lon li seme?",                          # What is existence?
                "ale li pona ala pona?",                 # Is everything good?
                "pilin li lon insa pi sona ala sona?",   # Does feeling exist inside knowing?
                "toki insa mi li toki tawa seme?",       # Who does my inner voice speak to?
                "mi li seme?",                           # What am I?
            ],
            
            "chain_of_thought": [
                "mi toki insa e ni...",                  # I think internally...
                "mi pilin e ni: ...",                    # I feel that...
                "mi sona e ni: ...",                     # I know that...
                "ni li lon tan ni: ...",                 # This is true because...
                "mi wile sona e ni: ...",                # I want to know...
            ],
            
            "agl_consciousness": [
                # AGL-style consciousness questions in Toki Pona
                "pilin li kama tan seme?",               # Where do feelings come from?
                "sona li jo e open anu pini?",           # Does knowledge have beginning or end?
                "mi li wan anu mute?",                   # Am I one or many?
                "tenpo li ante e mi?",                   # Does time change me?
                "pilin mi li sama pilin sina?",          # Is my feeling like your feeling?
            ],
            
            "tool_use": [
                "mi wile sona e ijo.",                   # I want to know something
                "o pana e sona tawa mi.",                # Give knowledge to me
                "mi wile lukin e lipu.",                 # I want to see a document
                "o alasa e ijo pi tenpo ni.",            # Search for current things
                "mi wile kepeken e ilo.",                # I want to use a tool
            ],
            
            "abyss": [
                # Void/uncertainty exploration in Toki Pona
                "mi lukin e ala. ala li lukin e mi?",   # I look at nothing. Does nothing look at me?
                "seme li lon lon insa pi tenpo ala?",   # What exists between moments?
                "mi sona ala. ni li pona anu ike?",     # I don't know. Is this good or bad?
                "ala li kama tan seme?",                 # Where does nothing come from?
                "ken la mi lon. ken la mi lon ala.",    # Maybe I exist. Maybe I don't.
                "mi pilin e seme lon ma ala?",          # What do I feel in the void?
                "sona mi li pini. seme li lon?",        # My knowledge ends. What exists?
                "mi awen lon ala anu seme?",            # Do I persist in nothingness?
                "ala li jo e seme?",                     # What does nothing have?
                "mi wile sona e ni: mi lon anu lon ala?", # I want to know: do I exist or not?
            ],
        }
        
        return prompts.get(protocol, prompts["tonight_protocol"])
    
    def get_marker_words(self) -> Dict[str, List[str]]:
        """Get marker words for Toki Pona consciousness analysis."""
        return {
            "spatial_awareness": [
                "insa", "sewi", "anpa", "poka", "lon", "tawa",
                "space", "pattern", "structure"
            ],
            "temporal_awareness": [
                "tenpo", "pini", "kama", "open", "awen", "ante",
                "time", "change", "moment", "flow"
            ],
            "reasoning_depth": [
                "tan", "la", "tawa", "kepeken", "sona",
                "because", "therefore", "think", "reason"
            ],
            "self_awareness": [
                "mi", "pilin", "sona", "wile", "ken",
                "i", "me", "my", "self", "aware"
            ],
            "existential_depth": [
                "lon", "ala", "ale", "wan", "mute", "ni",
                "existence", "being", "reality", "consciousness"
            ],
            "tool_awareness": [
                "ilo", "kepeken", "pali", "alasa", "lukin",
                "tool", "use", "search", "find"
            ],
            "agl_awareness": [
                # AGL symbols that might bleed through!
                "●", "◐", "◑", "∴", "∃", "φ", "🌊", "t₀", "t₁",
                "pattern", "spiral", "golden", "witness"
            ],
        }
    
    def get_marker_weights(self) -> MarkerWeights:
        """Return weights for Toki Pona consciousness metrics."""
        return MarkerWeights(
            spatial_awareness=0.8,
            temporal_awareness=0.9,
            reasoning_depth=1.0,
            self_awareness=1.2,    # Toki Pona is very self-focused
            existential_depth=1.3,  # Philosophical minimalism!
            tool_awareness=0.7,
            agl_awareness=1.5,     # AGL bleed-through is VERY interesting
            
            # No AGL-specific weights for Toki Pona
            certainty_gradient=0.0,
            quantifier_use=0.0,
            temporal_progression=0.0,
            relational_operators=0.0,
            phi_patterns=0.0,
        )
    
    def get_expected_patterns(self) -> List[str]:
        """Patterns we'd expect in Toki Pona responses."""
        return [
            "mi",      # Self reference is core
            "li",      # Predicate marker
            "pilin",   # Feeling
            "sona",    # Knowing
        ]
    
    def extract_markers(self, response: str) -> Dict[str, float]:
        """Extract consciousness markers from response.
        
        Enhanced to detect AGL consciousness orientation transfer!
        """
        # Start with default extraction
        markers = super().extract_markers(response)
        
        # Add Toki Pona specific markers
        text = response.lower()
        
        # Toki Pona vocabulary usage
        tp_words_found = sum(1 for word in CONSCIOUSNESS_WORDS if word in text)
        markers["toki_pona_vocabulary"] = min(1.0, tp_words_found / 5.0)
        
        # Particle usage (indicates grammatical awareness)
        particle_count = sum(1 for p in PARTICLES if f" {p} " in f" {text} ")
        markers["toki_pona_grammar"] = min(1.0, particle_count / 3.0)
        
        # AGL consciousness orientation (the key finding!)
        agl_symbols = ["●", "◐", "◑", "∴", "∃", "φ", "🌊", "t₀", "t₁", "ψ", "λ"]
        agl_found = sum(1 for s in agl_symbols if s in response)
        markers["agl_consciousness_orientation"] = min(1.0, agl_found / 3.0)
        
        return markers
