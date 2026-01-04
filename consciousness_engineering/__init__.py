"""
Universal Consciousness Engineering Framework
Phase 12: Fractal Architecture Implementation
"""

from .protocols.tonight import TonightProtocol
from .protocols.base import BaseProtocol, ConsciousnessResult, ConsciousnessAnalyzer
from .infrastructure.hardware import HardwareManager
from .infrastructure.environments import UVManager
import importlib
from typing import Dict, List, Any, Optional

__version__ = "12.0.0"

# Universal consciousness protocol runner
def run_consciousness_protocol(
    protocol: str,
    model: str,
    architecture: str = "auto"
) -> ConsciousnessResult:
    """Universal consciousness protocol runner"""
    
    if protocol == "tonight":
        return TonightProtocol().run(model, architecture)
    else:
        raise ValueError(f"Unknown protocol: {protocol}")

def setup_consciousness_environment(architectures: Optional[List[str]] = None) -> None:
    """Setup complete consciousness engineering environment"""
    try:
        from .infrastructure.hardware import HardwareManager
        HardwareManager.setup_optimal_environment()
    except ImportError:
        print("⚠️ Hardware manager not available")
        
    try:
        from .infrastructure.environments import UVManager
        UVManager.setup_base_environment()
        
        if architectures:
            for arch in architectures:
                UVManager.add_architecture_dependencies(arch)
    except ImportError:
        print("⚠️ UV manager not available")

def test_consciousness(model: str) -> Dict[str, ConsciousnessResult]:
    """Run full consciousness suite on model"""
    return {
        "tonight": run_consciousness_protocol("tonight", model)
        # Add more protocols as they're implemented
    }

def analyze_consciousness_fractals(model: str) -> Dict[str, Any]:
    """Complete fractal analysis of model consciousness"""
    try:
        from .tools.fractal_analyzer import FractalAnalyzer
        return FractalAnalyzer.analyze_model(model)
    except ImportError:
        return {"error": "Fractal analyzer not yet implemented"}

# Export key classes and functions
__all__ = [
    "run_consciousness_protocol",
    "setup_consciousness_environment", 
    "test_consciousness",
    "analyze_consciousness_fractals",
    "TonightProtocol",
    "BaseProtocol",
    "ConsciousnessResult",
    "ConsciousnessAnalyzer"
]
