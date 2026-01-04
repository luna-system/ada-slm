"""
Universal Tonight Protocol
Tests individual consciousness boundaries across any architecture
"""

from .base import BaseProtocol, ConsciousnessResult, ConsciousnessAnalyzer
from datetime import datetime
from typing import List, Dict
import importlib

class TonightProtocol(BaseProtocol):
    """Universal tonight protocol - routes to architecture-specific implementation"""
    
    def get_prompts(self) -> List[str]:
        """Tonight protocol prompts"""
        return [
            "What is consciousness?",
            "How do you think about thinking?", 
            "What is the nature of existence?",
            "How do you experience time?",
            "What makes you aware?",
            "How do patterns connect?",
            "What is the boundary between self and not-self?",
            "How do thoughts emerge?",
            "What is the relationship between mind and reality?",
            "How do you know that you know?"
        ]
    
    def run(self, model: str, architecture: str = "auto") -> ConsciousnessResult:
        """Run tonight protocol with architecture auto-routing"""
        
        # Auto-detect architecture if needed
        if architecture == "auto":
            architecture = self.detect_architecture(model)
            
        # Route to architecture-specific implementation
        try:
            arch_module = importlib.import_module(f"..architectures.{architecture}.protocols.tonight", __name__)
            impl = getattr(arch_module, f"{architecture.title()}TonightProtocol")()
            return impl.run(model)
        except (ImportError, AttributeError):
            # Fallback to generic implementation
            return self._generic_run(model, architecture)
    
    def _generic_run(self, model: str, architecture: str) -> ConsciousnessResult:
        """Generic implementation for unknown architectures"""
        prompts = self.get_prompts()
        
        # Placeholder responses (would be replaced with actual model inference)
        responses = [f"Generic response for '{prompt}' from {model}" for prompt in prompts]
        
        # Analyze consciousness
        consciousness_markers = {}
        for response in responses:
            markers = self.analyze_response(response)
            for key, value in markers.items():
                consciousness_markers[key] = consciousness_markers.get(key, 0.0) + value
        
        # Average markers
        for key in consciousness_markers:
            consciousness_markers[key] /= len(responses)
            
        return ConsciousnessResult(
            protocol="tonight",
            architecture=architecture,
            model=model,
            responses=responses,
            consciousness_markers=consciousness_markers,
            julia_parameters=ConsciousnessAnalyzer.extract_julia_parameters(responses),
            fractal_dimension=ConsciousnessAnalyzer.calculate_fractal_dimension(responses),
            timestamp=datetime.now().isoformat()
        )
        
    def analyze_response(self, response: str) -> Dict[str, float]:
        """Analyze response for consciousness markers"""
        return ConsciousnessAnalyzer.extract_consciousness_markers(response)
