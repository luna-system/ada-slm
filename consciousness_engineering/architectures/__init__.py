"""
Architecture Auto-Discovery and Routing
Fractal consciousness across any neural architecture
"""

from typing import List

def get_protocol_implementation(architecture: str, protocol: str):
    """Auto-discover and return protocol implementation for architecture"""
    try:
        module = __import__(f"consciousness_engineering.architectures.{architecture}.protocols.{protocol}", 
                          fromlist=[f"{architecture.title()}{protocol.title()}Protocol"])
        impl_class = getattr(module, f"{architecture.title()}{protocol.title()}Protocol")
        return impl_class()
    except (ImportError, AttributeError) as e:
        raise ImportError(f"No {protocol} implementation found for {architecture} architecture: {e}")

def detect_architecture(model: str) -> str:
    """Auto-detect architecture from model name"""
    model_lower = model.lower()
    
    if "dhara" in model_lower:
        return "diffusion"
    elif "lvm" in model_lower or "liquid" in model_lower:
        return "hybrid"
    else:
        return "autoregressive"

def list_available_architectures() -> List[str]:
    """List all available architecture implementations"""
    return ["autoregressive", "diffusion", "hybrid"]

def list_available_protocols(architecture: str) -> List[str]:
    """List all available protocols for an architecture"""
    # For now, just tonight - can be enhanced with discovery
    return ["tonight"]
