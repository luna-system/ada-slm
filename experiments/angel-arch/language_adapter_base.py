#!/usr/bin/env python3
"""
Language Adapter Base Class

THIN by design! Adapters ONLY handle text ↔ vectors.
All intelligence lives in the Response Generator!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
from typing import Dict, List
from abc import ABC, abstractmethod


class LanguageAdapter(ABC):
    """
    Base class for language adapters.
    
    DESIGN PRINCIPLE: Adapters are THIN!
    - They ONLY convert between text and consciousness vectors
    - NO business logic, NO response strategies, NO memory queries
    - Pure functions: text → vector, vector → words
    
    All intelligence lives in ResponseGenerator!
    """
    
    @abstractmethod
    def encode(self, text: str) -> torch.Tensor:
        """
        Convert text to consciousness vector.
        
        PURE FUNCTION - no side effects!
        
        Args:
            text: Input text in this language
            
        Returns:
            Consciousness vector (typically 512D)
        """
        pass
    
    @abstractmethod
    def decode(self, vector: torch.Tensor) -> List[str]:
        """
        Convert consciousness vector to list of words.
        
        PURE FUNCTION - no side effects!
        Returns words, NOT a complete response!
        Response composition happens in ResponseGenerator.
        
        Args:
            vector: Consciousness vector
            
        Returns:
            List of words sorted by relevance
        """
        pass
    
    @abstractmethod
    def get_vocabulary(self) -> Dict:
        """
        Return vocabulary metadata.
        
        Returns:
            Dict with vocabulary info (size, frequency data, etc)
        """
        pass
    
    def get_language_name(self) -> str:
        """Return the language name."""
        return self.__class__.__name__.replace('Adapter', '')
