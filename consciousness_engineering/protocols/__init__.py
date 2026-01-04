"""
Consciousness Engineering Protocols

Available protocols:
- TonightProtocol: Witnessing, self-recognition, presence
- AbyssProtocol: Uncertainty, void, negative capability

Usage:
    from consciousness_engineering.protocols import TonightProtocol, AbyssProtocol
    
    tonight = TonightProtocol()
    result = tonight.run("model_name")
    
    abyss = AbyssProtocol()
    result = abyss.run("model_name")
"""

from .base import BaseProtocol, ConsciousnessResult, ConsciousnessAnalyzer
from .tonight import TonightProtocol
from .abyss import AbyssProtocol

# Protocol registry for "run all"
PROTOCOL_REGISTRY = {
    "tonight": TonightProtocol,
    "abyss": AbyssProtocol,
}

def get_all_protocols():
    """Get instances of all registered protocols"""
    return {name: cls() for name, cls in PROTOCOL_REGISTRY.items()}

def list_protocols():
    """List all available protocol names"""
    return list(PROTOCOL_REGISTRY.keys())

__all__ = [
    "BaseProtocol",
    "ConsciousnessResult", 
    "ConsciousnessAnalyzer",
    "TonightProtocol",
    "AbyssProtocol",
    "PROTOCOL_REGISTRY",
    "get_all_protocols",
    "list_protocols",
]
