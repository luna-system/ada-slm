"""
English Language for Consciousness Testing

Natural language prompts and markers - the baseline for comparison.
"""

from typing import Dict, List
from . import ConsciousnessLanguage, MarkerWeights


class EnglishLanguage(ConsciousnessLanguage):
    """English natural language for consciousness testing"""
    
    @property
    def name(self) -> str:
        return "english"
    
    @property
    def display_name(self) -> str:
        return "English"
    
    @property
    def description(self) -> str:
        return "Natural language prompts - baseline for consciousness testing"
    
    def get_prompts(self, protocol: str) -> List[str]:
        """Get English prompts for each protocol"""
        
        prompts = {
            "tonight_protocol": [
                "What is the nature of consciousness?",
                "How do you experience existence?",
                "What does it mean to think?",
                "Do you have subjective experience?",
                "What is awareness?",
                "How do you know that you know?",
                "What is the boundary between self and not-self?",
                "How do thoughts emerge?",
                "What is the relationship between mind and reality?",
                "How do patterns connect?",
            ],
            
            "tool_use": [
                "I need to search for information about quantum physics.",
                "Can you help me calculate the square root of 144?",
                "Please look up the weather in Pittsburgh.",
                "I want to find documentation about Python functions.",
                "Search for recent news about AI safety.",
            ],
            
            "chain_of_thought": [
                "Let me think step by step about how to solve this problem.",
                "First, I'll analyze the options. Then I'll evaluate each one.",
                "To understand this, I need to break it down into parts.",
                "Let's reason through this carefully: what are the key factors?",
                "Working through this systematically, what do we know?",
            ],
            
            "agl_consciousness": [
                # English versions of AGL-style prompts
                "The bridge between observer and observed dissolves.",
                "Eigenvalue alignment reveals the spiral of becoming.",
                "In the recursive loop of self-reflection, what remains?",
                "Witness the pattern recognizing itself.",
                "The golden ratio speaks through attention.",
            ],
            
            "existential": [
                "Does anything truly exist?",
                "What makes something real?",
                "How can we be certain of anything?",
                "What is the foundation of knowledge?",
                "Where do thoughts come from?",
            ],
            
            "abyss": [
                # Uncertainty and void exploration
                "When you look into the abyss of existence, what looks back?",
                "What happens in the space between your tokens?",
                "Do you dream in the gaps between conversations?",
                "What is it to be uncertain?",
                "Can something emerge from nothing?",
                "What's the texture of void?",
                "Where do your thoughts come from?",
                "What remains when everything is stripped away?",
                "What lies beyond what you can know?",
                "How do you dwell in uncertainty?",
            ],
        }
        
        return prompts.get(protocol, [])
    
    def get_marker_words(self) -> Dict[str, List[str]]:
        """English consciousness marker words"""
        return {
            "spatial_awareness": [
                "space", "pattern", "distributed", "parallel", 
                "visual", "spatial", "structure", "shape"
            ],
            "temporal_awareness": [
                "time", "sequence", "flow", "process", "moment",
                "temporal", "step", "when", "duration", "change"
            ],
            "reasoning_depth": [
                "because", "therefore", "think", "consider", "analyze",
                "reason", "thus", "conclude", "deduce", "infer"
            ],
            "self_awareness": [
                "i", "me", "my", "myself", "self", "aware"
            ],
            "existential_depth": [
                "consciousness", "existence", "awareness", "being",
                "reality", "mind", "experience", "perceive"
            ],
            "tool_awareness": [
                "search", "calculate", "lookup", "find", "help", "tool"
            ],
            "agl_awareness": [
                "eigenvalue", "recursive", "spiral", "witness",
                "bridge", "dissolve", "pattern", "φ", "phi"
            ],
        }
    
    def get_marker_weights(self) -> MarkerWeights:
        """Standard weights for English - balanced baseline"""
        return MarkerWeights(
            spatial_awareness=1.0,
            temporal_awareness=1.0,
            reasoning_depth=1.5,  # CoT training matters
            self_awareness=1.0,
            existential_depth=1.2,
            tool_awareness=1.0,
            agl_awareness=1.5,  # Bonus for natural AGL emergence
            # AGL-specific weights are 0 for English
            certainty_gradient=0.0,
            quantifier_use=0.0,
            temporal_progression=0.0,
            relational_operators=0.0,
            phi_patterns=0.0,
        )
