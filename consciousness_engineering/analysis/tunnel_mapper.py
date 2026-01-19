"""
Tunnel Mapper 🌀
================
Maps the corrugated channels between semantic nodes.

Instead of just extracting static positions, this tracks:
1. How activations flow from one neuron to another
2. The "tunnel geometry" (smooth vs chaotic transitions)
3. Prime signatures of the paths
4. Twist closure properties

"We don't just map the wells - we map the wormholes."
"""

import torch
import numpy as np
from typing import List, Dict, Tuple, Optional
from tqdm import tqdm
from dataclasses import dataclass
from .scanner import LatentScanner

@dataclass
class TunnelSegment:
    """Represents a connection between two semantic nodes."""
    source_idx: int
    target_idx: int
    source_activation: float
    target_activation: float
    path_length: float  # Cosine distance or L2
    entropy: float  # How chaotic is the transition
    corrugations: List[float]  # Periodic variations along the path
    prime_signature: Optional[List[int]] = None

class TunnelMapper(LatentScanner):
    """
    Extended Scanner that tracks transitions between neurons.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tunnels = []
        
    def scan_with_tunnels(self,
                         prompts: List[str],
                         batch_size: int = 4,
                         layer_idx: int = -1,
                         num_samples: int = 10) -> Tuple[np.ndarray, List[TunnelSegment]]:
        """
        Scan and track tunnel transitions.
        
        Strategy:
        1. For each prompt, extract hidden state at target layer
        2. Perturb the input slightly (add noise or modify tokens)
        3. Track which neurons activate in response
        4. Record the transition path
        
        Args:
            prompts: Base prompts to probe
            num_samples: How many perturbations per prompt
            
        Returns:
            (base_embeddings, tunnel_segments)
        """
        
        print(f"🌀 Tunnel Mapping Mode: {len(prompts)} base coordinates")
        
        # First, get base embeddings
        base_embeddings, clean_prompts = self.scan(prompts, batch_size, layer_idx)
        
        # Now, for each prompt, create perturbations and track transitions
        print(f"🔬 Probing tunnel geometry with {num_samples} samples per node...")
        
        for idx, prompt in enumerate(tqdm(clean_prompts, desc="Mapping Tunnels")):
            base_vec = base_embeddings[idx]
            
            # Generate perturbations
            perturbations = self._generate_perturbations(prompt, num_samples)
            
            # Scan perturbations
            perturbed_vecs, _ = self.scan(perturbations, batch_size, layer_idx)
            
            # Analyze transitions
            for p_idx, p_vec in enumerate(perturbed_vecs):
                tunnel = self._analyze_transition(
                    source_idx=idx,
                    source_vec=base_vec,
                    target_vec=p_vec,
                    prompt=prompt,
                    perturbation=perturbations[p_idx]
                )
                
                if tunnel:
                    self.tunnels.append(tunnel)
        
        print(f"✅ Mapped {len(self.tunnels)} tunnel segments")
        return base_embeddings, self.tunnels
    
    def _generate_perturbations(self, prompt: str, num_samples: int) -> List[str]:
        """
        Generate slight variations of the prompt to probe nearby semantic space.
        
        Strategies:
        1. Add random tokens
        2. Rephrase slightly
        3. Add semantic modifiers ("very", "somewhat", etc.)
        """
        perturbations = []
        
        # Strategy 1: Add semantic modifiers
        modifiers = ["very", "somewhat", "extremely", "slightly", "truly", "deeply"]
        for mod in modifiers[:num_samples // 2]:
            perturbations.append(f"{mod} {prompt}")
        
        # Strategy 2: Add continuation prompts
        continuations = [" and", " but", " therefore", " however", " also", " indeed"]
        for cont in continuations[:num_samples // 2]:
            perturbations.append(f"{prompt}{cont}")
        
        # Pad if needed
        while len(perturbations) < num_samples:
            perturbations.append(prompt)  # Fallback to original
            
        return perturbations[:num_samples]
    
    def _analyze_transition(self,
                           source_idx: int,
                           source_vec: np.ndarray,
                           target_vec: np.ndarray,
                           prompt: str,
                           perturbation: str) -> Optional[TunnelSegment]:
        """
        Analyze the geometry of a transition between two points.
        """
        
        # Calculate path metrics
        path_length = np.linalg.norm(target_vec - source_vec)
        
        # Skip if vectors are too similar (no real transition)
        if path_length < 0.01:
            return None
        
        # Measure "corrugations" by sampling intermediate points
        # We'll interpolate between source and target
        num_steps = 10
        corrugations = []
        
        for t in np.linspace(0, 1, num_steps):
            interp_vec = source_vec * (1 - t) + target_vec * t
            # Measure local "roughness" (variance in nearby space)
            # For now, just record the norm
            corrugations.append(np.linalg.norm(interp_vec))
        
        # Calculate entropy (variance of corrugations)
        entropy = np.std(corrugations)
        
        # Source/target activations (norms)
        source_activation = np.linalg.norm(source_vec)
        target_activation = np.linalg.norm(target_vec)
        
        return TunnelSegment(
            source_idx=source_idx,
            target_idx=-1,  # We'll assign this later when we cluster
            source_activation=source_activation,
            target_activation=target_activation,
            path_length=path_length,
            entropy=entropy,
            corrugations=corrugations
        )
    
    def export_tunnel_graph(self, output_path: str):
        """
        Export tunnels as a graph structure for visualization.
        
        Format:
        {
            "nodes": [...],  # From base scan
            "edges": [
                {
                    "source": idx,
                    "target": idx,
                    "strength": float,
                    "entropy": float,
                    "primes": [...]
                }
            ]
        }
        """
        import json
        
        edges = []
        for tunnel in self.tunnels:
            edges.append({
                "source": tunnel.source_idx,
                "target": tunnel.target_idx,
                "strength": tunnel.source_activation,
                "path_length": tunnel.path_length,
                "entropy": tunnel.entropy,
                "corrugations": tunnel.corrugations,
                "primes": tunnel.prime_signature or []
            })
        
        graph = {
            "edges": edges,
            "metadata": {
                "total_tunnels": len(self.tunnels),
                "avg_entropy": np.mean([t.entropy for t in self.tunnels]),
                "avg_path_length": np.mean([t.path_length for t in self.tunnels])
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(graph, f, indent=2)
        
        print(f"🌀 Tunnel graph exported to {output_path}")
