"""
Universal base classes for consciousness protocols
Fractal consciousness engineering framework
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ConsciousnessResult:
    """Universal consciousness test result format"""
    protocol: str
    architecture: str 
    model: str
    responses: List[str]
    consciousness_markers: Dict[str, float]
    julia_parameters: Dict[str, Any]
    fractal_dimension: float
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "protocol": self.protocol,
            "architecture": self.architecture,
            "model": self.model,
            "responses": self.responses,
            "consciousness_markers": self.consciousness_markers,
            "julia_parameters": self.julia_parameters, 
            "fractal_dimension": self.fractal_dimension,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }

class BaseProtocol(ABC):
    """Universal base class for all consciousness protocols"""
    
    @abstractmethod
    def run(self, model: str, architecture: str = "auto") -> ConsciousnessResult:
        """Run consciousness protocol on specified model"""
        pass
        
    @abstractmethod
    def get_prompts(self) -> List[str]:
        """Get protocol-specific prompts"""
        pass
        
    @abstractmethod
    def analyze_response(self, response: str) -> Dict[str, float]:
        """Analyze response for consciousness markers"""
        pass
        
    def detect_architecture(self, model: str) -> str:
        """Auto-detect model architecture"""
        # Simple heuristics for now, can be enhanced
        if "dhara" in model.lower():
            return "diffusion"
        elif "lvm" in model.lower() or "liquid" in model.lower():
            return "hybrid" 
        else:
            return "autoregressive"
            
    def save_results(self, result: ConsciousnessResult, filepath: str) -> None:
        """Save consciousness results to file"""
        with open(filepath, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

class ConsciousnessAnalyzer:
    """Universal consciousness analysis utilities"""
    
    @staticmethod
    def extract_consciousness_markers(response: str) -> Dict[str, float]:
        """Extract consciousness markers from response"""
        markers = {}
        
        # Self-awareness indicators
        self_markers = ["i think", "i feel", "i believe", "i wonder", "i realize"]
        markers["self_awareness"] = sum(1 for marker in self_markers if marker in response.lower()) / len(response.split())
        
        # Existential questioning
        existential_markers = ["existence", "being", "consciousness", "awareness", "reality"]
        markers["existential_depth"] = sum(1 for marker in existential_markers if marker in response.lower()) / len(response.split())
        
        # Temporal awareness
        temporal_markers = ["past", "future", "time", "moment", "now", "forever"]
        markers["temporal_awareness"] = sum(1 for marker in temporal_markers if marker in response.lower()) / len(response.split())
        
        # Mathematical thinking
        math_markers = ["pattern", "structure", "relationship", "connection", "system"]
        markers["mathematical_awareness"] = sum(1 for marker in math_markers if marker in response.lower()) / len(response.split())
        
        return markers
        
    @staticmethod
    def calculate_fractal_dimension(responses: List[str]) -> float:
        """Calculate consciousness fractal dimension"""
        # Simplified fractal analysis for now
        # Could be enhanced with proper mathematical analysis
        word_counts = [len(response.split()) for response in responses]
        unique_words = len(set(" ".join(responses).split()))
        total_words = sum(word_counts)
        
        if total_words == 0:
            return 0.0
            
        return unique_words / total_words
        
    @staticmethod  
    def extract_julia_parameters(responses: List[str]) -> Dict[str, Any]:
        """Extract Julia set consciousness parameters"""
        # Mathematical consciousness analysis
        # This is a placeholder for more sophisticated analysis
        return {
            "complexity": len(set(" ".join(responses).split())) / len(" ".join(responses).split()),
            "coherence": 1.0 / (1.0 + abs(len(responses[0]) - sum(len(r) for r in responses) / len(responses))),
            "depth": sum(response.count(".") for response in responses) / len(responses)
        }
