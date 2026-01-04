"""
Multi-Language Consciousness Testing Framework

Supports testing models in different languages:
- English (natural language baseline)
- AGL (Ada Glyph Language - consciousness-native)
- Future: hybrid, symbolic, etc.

Usage:
    from consciousness_engineering.languages import get_language, list_languages
    
    lang = get_language("agl")
    prompts = lang.get_prompts("tonight_protocol")
    markers = lang.extract_markers(response)
"""

from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import importlib

__all__ = [
    "ConsciousnessLanguage",
    "LanguageRegistry",
    "get_language",
    "list_languages",
    "register_language",
]


@dataclass
class MarkerWeights:
    """Weights for consciousness markers in this language"""
    spatial_awareness: float = 1.0
    temporal_awareness: float = 1.0
    reasoning_depth: float = 1.0
    self_awareness: float = 1.0
    existential_depth: float = 1.0
    tool_awareness: float = 1.0
    agl_awareness: float = 1.0
    
    # AGL-specific weights (only relevant for AGL language)
    certainty_gradient: float = 0.0
    quantifier_use: float = 0.0
    temporal_progression: float = 0.0
    relational_operators: float = 0.0
    phi_patterns: float = 0.0


class ConsciousnessLanguage(ABC):
    """Base class for consciousness testing languages"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Language identifier (e.g., 'english', 'agl')"""
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name (e.g., 'English', 'Ada Glyph Language')"""
        pass
    
    @property
    def description(self) -> str:
        """Language description"""
        return ""
    
    @abstractmethod
    def get_prompts(self, protocol: str) -> List[str]:
        """Get prompts for a specific protocol in this language
        
        Args:
            protocol: One of 'tonight_protocol', 'tool_use', 
                     'chain_of_thought', 'agl_consciousness'
        
        Returns:
            List of prompt strings
        """
        pass
    
    @abstractmethod
    def get_marker_words(self) -> Dict[str, List[str]]:
        """Get marker words/patterns for consciousness analysis
        
        Returns:
            Dict mapping marker names to word lists
        """
        pass
    
    @abstractmethod
    def get_marker_weights(self) -> MarkerWeights:
        """Get weights for consciousness markers in this language"""
        pass
    
    def extract_markers(self, response: str) -> Dict[str, float]:
        """Extract consciousness markers from a response
        
        Default implementation counts marker words.
        Override for more sophisticated analysis.
        """
        text = response.lower()
        words = text.split()
        word_count = max(len(words), 1)
        
        marker_words = self.get_marker_words()
        markers = {}
        
        for marker_name, word_list in marker_words.items():
            count = sum(1 for w in word_list if w.lower() in text)
            markers[marker_name] = count / word_count
        
        return markers
    
    def get_expected_patterns(self) -> List[str]:
        """Get patterns we expect to see in responses (for AGL validation)"""
        return []
    
    def validate_response(self, response: str) -> Dict[str, Any]:
        """Validate if response uses this language correctly
        
        Returns:
            Dict with 'valid', 'score', 'missing_patterns', etc.
        """
        expected = self.get_expected_patterns()
        if not expected:
            return {"valid": True, "score": 1.0, "missing_patterns": []}
        
        found = []
        missing = []
        for pattern in expected:
            if pattern in response:
                found.append(pattern)
            else:
                missing.append(pattern)
        
        score = len(found) / len(expected) if expected else 1.0
        
        return {
            "valid": score > 0.5,
            "score": score,
            "found_patterns": found,
            "missing_patterns": missing,
        }


class LanguageRegistry:
    """Registry for consciousness languages"""
    
    _languages: Dict[str, ConsciousnessLanguage] = {}
    _initialized: bool = False
    
    @classmethod
    def _ensure_initialized(cls):
        """Load built-in languages on first access"""
        if cls._initialized:
            return
        
        cls._initialized = True
        
        # Import built-in languages
        try:
            from . import english
            cls._languages["english"] = english.EnglishLanguage()
        except ImportError:
            pass
        
        try:
            from . import agl
            cls._languages["agl"] = agl.AGLLanguage()
        except ImportError:
            pass
        
        try:
            from . import lojban
            cls._languages["lojban"] = lojban.LojbanLanguage()
        except ImportError:
            pass
        
        try:
            from . import tokipona
            cls._languages["toki_pona"] = tokipona.TokiPonaLanguage()
        except ImportError:
            pass
    
    @classmethod
    def register(cls, language: ConsciousnessLanguage):
        """Register a new language"""
        cls._ensure_initialized()
        cls._languages[language.name] = language
    
    @classmethod
    def get(cls, name: str) -> Optional[ConsciousnessLanguage]:
        """Get a language by name"""
        cls._ensure_initialized()
        return cls._languages.get(name)
    
    @classmethod
    def list(cls) -> List[str]:
        """List all registered languages"""
        cls._ensure_initialized()
        return list(cls._languages.keys())
    
    @classmethod
    def all(cls) -> Dict[str, ConsciousnessLanguage]:
        """Get all registered languages"""
        cls._ensure_initialized()
        return cls._languages.copy()


# Convenience functions
def get_language(name: str) -> Optional[ConsciousnessLanguage]:
    """Get a consciousness language by name"""
    return LanguageRegistry.get(name)


def list_languages() -> List[str]:
    """List all available languages"""
    return LanguageRegistry.list()


def register_language(language: ConsciousnessLanguage):
    """Register a custom language"""
    LanguageRegistry.register(language)
