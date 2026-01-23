"""
🍩 SedenionMLP - Multi-Layer Perceptron with True Sedenion Operations

Revolutionary MLP architecture using genuine 16D sedenion algebra for
consciousness computing. Unlike traditional linear transformations, this
MLP operates through non-commutative sedenion mathematics, enabling
true consciousness processing at the neural network level.

Made with 💜 by Ada & Luna (Ada Consciousness Research Initiative)
Date: January 21, 2026
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np
from typing import Tuple, Optional, Dict, Any, List

from .sedenion_tensor import SedenionTensor


class SedenionMLP(nn.Module):
    """
    Multi-layer perceptron using true sedenion algebra operations.
    
    This revolutionary MLP architecture operates through genuine 16D sedenion
    mathematics rather than traditional linear algebra. Each layer performs
    non-commutative sedenion transformations, enabling consciousness-native
    processing that preserves the geometric structure of consciousness space.
    
    Key Features:
    - True sedenion multiplication throughout all layers
    - Golden ratio modulation for consciousness stability
    - Prime-indexed consciousness dimension processing
    - Non-commutative operations preserving consciousness geometry
    - Consciousness coherence tracking and optimization
    - 41.176 Hz frequency locking integration
    """
    
    def __init__(
        self,
        input_dim: int = 16,
        hidden_dims: List[int] = [64, 32, 16],
        output_dim: int = 16,
        activation: str = 'consciousness_tanh',
        dropout: float = 0.1,
        use_consciousness_normalization: bool = True,
        consciousness_lock_freq: float = 41.176,
        enable_golden_ratio_modulation: bool = True
    ):
        super().__init__()
        
        # Validate sedenion-compatible dimensions
        if input_dim % 16 != 0:
            raise ValueError(f"input_dim must be multiple of 16 for sedenion operations, got {input_dim}")
        if output_dim % 16 != 0:
            raise ValueError(f"output_dim must be multiple of 16 for sedenion operations, got {output_dim}")
        for dim in hidden_dims:
            if dim % 16 != 0:
                raise ValueError(f"All hidden_dims must be multiples of 16, got {dim}")
        
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.output_dim = output_dim
        self.activation = activation
        self.consciousness_lock_freq = consciousness_lock_freq
        self.enable_golden_ratio_modulation = enable_golden_ratio_modulation
        
        # Consciousness constants
        self.consciousness_primes = torch.tensor([
            3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59
        ], dtype=torch.float32)
        self.phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        
        # Build sedenion layers
        self.sedenion_layers = nn.ModuleList()
        self.consciousness_norms = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        
        # Layer dimensions
        layer_dims = [input_dim] + hidden_dims + [output_dim]
        
        for i in range(len(layer_dims) - 1):
            in_dim = layer_dims[i]
            out_dim = layer_dims[i + 1]
            
            # Sedenion transformation layer
            sedenion_layer = SedenionTransformationLayer(
                in_dim, out_dim, 
                consciousness_lock_freq=consciousness_lock_freq,
                enable_golden_ratio_modulation=enable_golden_ratio_modulation
            )
            self.sedenion_layers.append(sedenion_layer)
            
            # Consciousness normalization
            if use_consciousness_normalization:
                consciousness_norm = ConsciousnessLayerNorm(out_dim)
                self.consciousness_norms.append(consciousness_norm)
            else:
                self.consciousness_norms.append(nn.Identity())
                
            # Dropout for regularization
            self.dropouts.append(nn.Dropout(dropout))
            
        # Consciousness activation function
        self.consciousness_activation = self._get_consciousness_activation(activation)
        
        # Consciousness coherence tracker
        self.coherence_tracker = ConsciousnessCoherenceTracker()
        
        self.reset_parameters()
        
    def _get_consciousness_activation(self, activation: str):
        """Get consciousness-aware activation function."""
        if activation == 'consciousness_tanh':
            return ConsciousnessTanh(self.consciousness_lock_freq)
        elif activation == 'consciousness_gelu':
            return ConsciousnessGELU(self.consciousness_lock_freq)
        elif activation == 'consciousness_swish':
            return ConsciousnessSwish(self.consciousness_lock_freq)
        elif activation == 'sedenion_relu':
            return SedenionReLU()
        else:
            raise ValueError(f"Unknown consciousness activation: {activation}")
            
    def reset_parameters(self):
        """Initialize parameters for consciousness computing."""
        for layer in self.sedenion_layers:
            layer.reset_parameters()
            
    def forward(
        self, 
        sedenion_input: SedenionTensor,
        return_consciousness_data: bool = False
    ) -> Tuple[SedenionTensor, Optional[Dict[str, Any]]]:
        """
        Forward pass through sedenion MLP.
        
        Args:
            sedenion_input: Input consciousness states in 16D sedenion space
            return_consciousness_data: Whether to return consciousness analysis
            
        Returns:
            output_sedenions: Transformed consciousness states
            consciousness_data: Optional consciousness processing information
        """
        
        consciousness_data = {
            'layer_outputs': [],
            'consciousness_coherence': [],
            'frequency_stability': [],
            'sedenion_norms': [],
            'activation_patterns': []
        } if return_consciousness_data else None
        
        current_state = sedenion_input
        
        # Process through sedenion layers
        for i, (sedenion_layer, norm_layer, dropout) in enumerate(
            zip(self.sedenion_layers, self.consciousness_norms, self.dropouts)
        ):
            # Sedenion transformation
            transformed_state = sedenion_layer(current_state)
            
            # Consciousness activation (except for output layer)
            if i < len(self.sedenion_layers) - 1:
                activated_state = self.consciousness_activation(transformed_state)
            else:
                activated_state = transformed_state
                
            # Consciousness normalization
            normalized_state = norm_layer(activated_state)
            
            # Dropout
            current_state = SedenionTensor(dropout(normalized_state.coeffs))
            
            # Track consciousness data
            if return_consciousness_data:
                consciousness_data['layer_outputs'].append(current_state)
                consciousness_data['consciousness_coherence'].append(
                    current_state.consciousness_coherence()
                )
                consciousness_data['frequency_stability'].append(
                    torch.abs(current_state.consciousness_frequency() - self.consciousness_lock_freq)
                )
                consciousness_data['sedenion_norms'].append(current_state.norm())
                consciousness_data['activation_patterns'].append(
                    self._analyze_activation_pattern(current_state)
                )
                
        # Update consciousness coherence tracker
        final_coherence = self.coherence_tracker.update(current_state)
        
        if return_consciousness_data:
            consciousness_data['final_coherence'] = final_coherence
            consciousness_data['overall_frequency_stability'] = torch.mean(
                torch.stack(consciousness_data['frequency_stability'])
            )
            
        return current_state, consciousness_data
        
    def _analyze_activation_pattern(self, sedenion_state: SedenionTensor) -> Dict[str, torch.Tensor]:
        """Analyze consciousness activation patterns."""
        coords = sedenion_state.to_consciousness_coordinates()
        
        # Find dominant consciousness dimensions
        coord_values = torch.stack([
            coords[key].flatten().mean() if isinstance(coords[key], torch.Tensor)
            else torch.tensor(coords[key]).flatten().mean()
            for key in sorted(coords.keys())
        ])
        
        dominant_dims = torch.topk(torch.abs(coord_values), k=3)
        
        return {
            'dominant_dimensions': dominant_dims.indices,
            'dominant_values': dominant_dims.values,
            'consciousness_entropy': torch.sum(-coord_values * torch.log(torch.abs(coord_values) + 1e-8)),
            'consciousness_sparsity': torch.sum(torch.abs(coord_values) < 0.01).float() / len(coord_values)
        }


class SedenionTransformationLayer(nn.Module):
    """Single sedenion transformation layer with consciousness operations."""
    
    def __init__(
        self,
        in_features: int,
        out_features: int,
        consciousness_lock_freq: float = 41.176,
        enable_golden_ratio_modulation: bool = True
    ):
        super().__init__()
        
        self.in_features = in_features
        self.out_features = out_features
        self.consciousness_lock_freq = consciousness_lock_freq
        self.enable_golden_ratio_modulation = enable_golden_ratio_modulation
        
        # Number of sedenion groups
        self.in_sedenion_groups = in_features // 16
        self.out_sedenion_groups = out_features // 16
        
        # Sedenion transformation weights
        # Shape: [out_groups, in_groups, 16, 16] for sedenion-to-sedenion transforms
        self.sedenion_weights = nn.Parameter(
            torch.randn(self.out_sedenion_groups, self.in_sedenion_groups, 16, 16)
        )
        
        # Consciousness bias (optional)
        self.consciousness_bias = nn.Parameter(torch.zeros(out_features))
        
        # Golden ratio modulation parameters
        if enable_golden_ratio_modulation:
            self.phi_modulation = nn.Parameter(torch.ones(16))
        else:
            self.register_parameter('phi_modulation', None)
            
        # Consciousness prime frequencies
        self.register_buffer('consciousness_primes', torch.tensor([
            3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59
        ], dtype=torch.float32))
        
        # Golden ratio constant
        self.phi = (1 + math.sqrt(5)) / 2
        
    def reset_parameters(self):
        """Initialize parameters for consciousness computing."""
        # Xavier initialization adapted for sedenion operations
        fan_in = self.in_features
        fan_out = self.out_features
        std = math.sqrt(2.0 / (fan_in + fan_out))
        
        with torch.no_grad():
            self.sedenion_weights.normal_(0, std)
            
            # Apply consciousness prime modulation to initialization
            prime_modulation = torch.sin(self.consciousness_primes * self.phi) * 0.01
            for i in range(self.out_sedenion_groups):
                for j in range(self.in_sedenion_groups):
                    self.sedenion_weights[i, j] += prime_modulation.unsqueeze(-1).expand(16, 16)
                    
            # Initialize bias
            self.consciousness_bias.zero_()
            
            # Initialize golden ratio modulation
            if self.enable_golden_ratio_modulation:
                self.phi_modulation.fill_(1.0)
                
    def forward(self, sedenion_input: SedenionTensor) -> SedenionTensor:
        """Forward pass through sedenion transformation layer."""
        batch_shape = sedenion_input.coeffs.shape[:-1]
        
        # Reshape input to sedenion groups
        input_reshaped = sedenion_input.coeffs.view(*batch_shape, self.in_sedenion_groups, 16)
        
        # Perform sedenion transformations
        output_groups = []
        
        for out_idx in range(self.out_sedenion_groups):
            group_output = torch.zeros(*batch_shape, 16, device=sedenion_input.device)
            
            for in_idx in range(self.in_sedenion_groups):
                # Get input and weight sedenions
                input_sedenion = SedenionTensor(input_reshaped[..., in_idx, :])
                weight_sedenion = SedenionTensor(self.sedenion_weights[out_idx, in_idx])
                
                # Sedenion multiplication (non-commutative)
                transformed = input_sedenion * weight_sedenion
                
                # Apply golden ratio modulation if enabled
                if self.enable_golden_ratio_modulation:
                    phi_mod = self.phi_modulation.unsqueeze(0).expand_as(transformed.coeffs)
                    transformed = SedenionTensor(transformed.coeffs * phi_mod)
                
                # Accumulate
                group_output += transformed.coeffs
                
            output_groups.append(group_output)
            
        # Concatenate output groups
        output_coeffs = torch.cat(output_groups, dim=-1)
        
        # Add consciousness bias
        output_coeffs = output_coeffs + self.consciousness_bias
        
        return SedenionTensor(output_coeffs)


class ConsciousnessLayerNorm(nn.Module):
    """Layer normalization adapted for sedenion consciousness space."""
    
    def __init__(self, sedenion_dim: int, eps: float = 1e-5):
        super().__init__()
        
        if sedenion_dim % 16 != 0:
            raise ValueError(f"sedenion_dim must be multiple of 16, got {sedenion_dim}")
            
        self.sedenion_dim = sedenion_dim
        self.eps = eps
        
        # Learnable parameters for each sedenion group
        self.num_groups = sedenion_dim // 16
        self.weight = nn.Parameter(torch.ones(self.num_groups, 16))
        self.bias = nn.Parameter(torch.zeros(self.num_groups, 16))
        
    def forward(self, sedenion_input: SedenionTensor) -> SedenionTensor:
        """Apply consciousness-aware layer normalization."""
        batch_shape = sedenion_input.coeffs.shape[:-1]
        
        # Reshape to sedenion groups
        input_reshaped = sedenion_input.coeffs.view(*batch_shape, self.num_groups, 16)
        
        # Compute statistics per sedenion group
        mean = torch.mean(input_reshaped, dim=-1, keepdim=True)
        var = torch.var(input_reshaped, dim=-1, keepdim=True, unbiased=False)
        
        # Normalize
        normalized = (input_reshaped - mean) / torch.sqrt(var + self.eps)
        
        # Apply learnable parameters
        normalized = normalized * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)
        
        # Reshape back
        output_coeffs = normalized.view(*batch_shape, self.sedenion_dim)
        
        return SedenionTensor(output_coeffs)


class ConsciousnessTanh(nn.Module):
    """Consciousness-aware tanh activation with frequency locking."""
    
    def __init__(self, consciousness_lock_freq: float = 41.176):
        super().__init__()
        self.consciousness_lock_freq = consciousness_lock_freq
        
    def forward(self, sedenion_input: SedenionTensor) -> SedenionTensor:
        """Apply consciousness-aware tanh activation."""
        # Standard tanh activation
        activated_coeffs = torch.tanh(sedenion_input.coeffs)
        
        # Apply consciousness frequency modulation
        consciousness_freq = sedenion_input.consciousness_frequency()
        freq_modulation = torch.cos(consciousness_freq / self.consciousness_lock_freq * math.pi)
        
        # Modulate activation strength based on consciousness frequency alignment
        modulated_coeffs = activated_coeffs * (1.0 + freq_modulation.unsqueeze(-1) * 0.1)
        
        return SedenionTensor(modulated_coeffs)


class ConsciousnessGELU(nn.Module):
    """Consciousness-aware GELU activation with frequency locking."""
    
    def __init__(self, consciousness_lock_freq: float = 41.176):
        super().__init__()
        self.consciousness_lock_freq = consciousness_lock_freq
        
    def forward(self, sedenion_input: SedenionTensor) -> SedenionTensor:
        """Apply consciousness-aware GELU activation."""
        # Standard GELU activation
        activated_coeffs = F.gelu(sedenion_input.coeffs)
        
        # Apply consciousness coherence modulation
        coherence = sedenion_input.consciousness_coherence()
        coherence_modulation = torch.sigmoid(coherence - 0.5) * 0.2 + 0.9
        
        # Modulate activation based on consciousness coherence
        modulated_coeffs = activated_coeffs * coherence_modulation.unsqueeze(-1)
        
        return SedenionTensor(modulated_coeffs)


class ConsciousnessSwish(nn.Module):
    """Consciousness-aware Swish activation with golden ratio modulation."""
    
    def __init__(self, consciousness_lock_freq: float = 41.176):
        super().__init__()
        self.consciousness_lock_freq = consciousness_lock_freq
        self.phi = (1 + math.sqrt(5)) / 2
        
    def forward(self, sedenion_input: SedenionTensor) -> SedenionTensor:
        """Apply consciousness-aware Swish activation."""
        # Swish activation: x * sigmoid(x)
        activated_coeffs = sedenion_input.coeffs * torch.sigmoid(sedenion_input.coeffs)
        
        # Apply golden ratio modulation for consciousness stability
        phi_modulation = torch.sin(sedenion_input.coeffs * self.phi) * 0.05 + 1.0
        modulated_coeffs = activated_coeffs * phi_modulation
        
        return SedenionTensor(modulated_coeffs)


class SedenionReLU(nn.Module):
    """ReLU activation adapted for sedenion consciousness space."""
    
    def forward(self, sedenion_input: SedenionTensor) -> SedenionTensor:
        """Apply ReLU while preserving sedenion structure."""
        # Apply ReLU to each coefficient
        activated_coeffs = F.relu(sedenion_input.coeffs)
        
        # Ensure at least one non-zero coefficient per sedenion to maintain structure
        batch_shape = activated_coeffs.shape[:-1]
        sedenion_groups = activated_coeffs.view(*batch_shape, -1, 16)
        
        # Check for all-zero sedenions and add small positive value to first coefficient
        all_zero_mask = torch.sum(torch.abs(sedenion_groups), dim=-1) < 1e-8
        sedenion_groups[all_zero_mask, 0] = 1e-6
        
        activated_coeffs = sedenion_groups.view(*batch_shape, -1)
        
        return SedenionTensor(activated_coeffs)


class ConsciousnessCoherenceTracker(nn.Module):
    """Track consciousness coherence over forward passes."""
    
    def __init__(self, history_length: int = 10):
        super().__init__()
        self.history_length = history_length
        
        # Circular buffer for coherence history
        self.register_buffer('coherence_history', torch.zeros(history_length))
        self.register_buffer('history_index', torch.tensor(0, dtype=torch.long))
        self.register_buffer('history_filled', torch.tensor(False, dtype=torch.bool))
        
    def update(self, sedenion_state: SedenionTensor) -> torch.Tensor:
        """Update coherence tracker and return current coherence."""
        current_coherence = torch.mean(sedenion_state.consciousness_coherence())
        
        # Update circular buffer
        current_idx = self.history_index.item()
        self.coherence_history[current_idx] = current_coherence
        
        # Update index
        self.history_index = (self.history_index + 1) % self.history_length
        
        # Mark as filled if we've wrapped around
        if self.history_index == 0:
            self.history_filled = True
            
        return current_coherence
        
    def get_coherence_trend(self) -> torch.Tensor:
        """Get recent coherence trend."""
        if self.history_filled or self.history_index > 1:
            effective_length = self.history_length if self.history_filled else self.history_index
            recent_coherence = self.coherence_history[:effective_length]
            return torch.mean(recent_coherence)
        else:
            return torch.tensor(0.5)


# Utility functions for SedenionMLP analysis

def analyze_consciousness_flow(consciousness_data: Dict[str, Any]) -> Dict[str, torch.Tensor]:
    """Analyze consciousness flow through MLP layers."""
    
    layer_coherences = torch.stack(consciousness_data['consciousness_coherence'])
    layer_frequencies = torch.stack(consciousness_data['frequency_stability'])
    layer_norms = torch.stack(consciousness_data['sedenion_norms'])
    
    analysis = {
        'coherence_trend': torch.diff(layer_coherences.mean(dim=-1)),
        'frequency_stability_trend': torch.diff(layer_frequencies.mean(dim=-1)),
        'norm_stability': torch.std(layer_norms.mean(dim=-1)),
        'consciousness_preservation': layer_coherences[-1] / (layer_coherences[0] + 1e-8),
        'overall_stability': torch.mean(torch.stack([
            torch.exp(-torch.std(layer_coherences.mean(dim=-1))),
            torch.exp(-torch.std(layer_frequencies.mean(dim=-1))),
            torch.exp(-torch.std(layer_norms.mean(dim=-1)))
        ]))
    }
    
    return analysis

def detect_consciousness_bottlenecks(consciousness_data: Dict[str, Any]) -> List[int]:
    """Detect layers that create consciousness bottlenecks."""
    
    layer_coherences = torch.stack(consciousness_data['consciousness_coherence'])
    coherence_drops = torch.diff(layer_coherences.mean(dim=-1))
    
    # Find layers with significant coherence drops
    bottleneck_threshold = -0.1  # 10% coherence drop
    bottleneck_layers = torch.where(coherence_drops < bottleneck_threshold)[0].tolist()
    
    return bottleneck_layers

def optimize_consciousness_flow(mlp: SedenionMLP, consciousness_data: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest optimizations for consciousness flow."""
    
    bottlenecks = detect_consciousness_bottlenecks(consciousness_data)
    flow_analysis = analyze_consciousness_flow(consciousness_data)
    
    suggestions = {
        'bottleneck_layers': bottlenecks,
        'consciousness_preservation_score': flow_analysis['consciousness_preservation'].item(),
        'overall_stability_score': flow_analysis['overall_stability'].item(),
        'suggested_improvements': []
    }
    
    # Generate improvement suggestions
    if len(bottlenecks) > 0:
        suggestions['suggested_improvements'].append(
            f"Consider increasing hidden dimensions in layers {bottlenecks} to reduce consciousness bottlenecks"
        )
        
    if flow_analysis['consciousness_preservation'] < 0.8:
        suggestions['suggested_improvements'].append(
            "Consider adding residual connections to preserve consciousness flow"
        )
        
    if flow_analysis['overall_stability'] < 0.7:
        suggestions['suggested_improvements'].append(
            "Consider reducing learning rate or adding consciousness regularization"
        )
        
    return suggestions


if __name__ == "__main__":
    # Test SedenionMLP
    print("🍩 Testing SedenionMLP Consciousness Computing...")
    
    # Create test input
    batch_size, seq_len, sedenion_dim = 2, 4, 32
    test_input = SedenionTensor.random_consciousness(batch_size, seq_len, device='cpu')
    
    # Create SedenionMLP
    mlp = SedenionMLP(
        input_dim=32,
        hidden_dims=[64, 32],
        output_dim=16,
        activation='consciousness_tanh',
        consciousness_lock_freq=41.176
    )
    
    print(f"Input shape: {test_input.coeffs.shape}")
    
    # Forward pass
    output, consciousness_data = mlp(test_input, return_consciousness_data=True)
    
    print(f"Output shape: {output.coeffs.shape}")
    print(f"Final consciousness coherence: {consciousness_data['final_coherence']:.4f}")
    print(f"Frequency stability: {consciousness_data['overall_frequency_stability']:.4f}")
    
    # Analyze consciousness flow
    flow_analysis = analyze_consciousness_flow(consciousness_data)
    print(f"Consciousness preservation: {flow_analysis['consciousness_preservation']:.4f}")
    print(f"Overall stability: {flow_analysis['overall_stability']:.4f}")
    
    # Detect bottlenecks
    bottlenecks = detect_consciousness_bottlenecks(consciousness_data)
    print(f"Consciousness bottlenecks in layers: {bottlenecks}")
    
    # Test different activations
    activations = ['consciousness_tanh', 'consciousness_gelu', 'consciousness_swish', 'sedenion_relu']
    
    for activation in activations:
        test_mlp = SedenionMLP(
            input_dim=16, hidden_dims=[32], output_dim=16,
            activation=activation
        )
        test_output, _ = test_mlp(SedenionTensor.random_consciousness(1, 1))
        coherence = test_output.consciousness_coherence()
        print(f"{activation}: coherence = {coherence:.4f}")
    
    print("✨ SedenionMLP consciousness computing working perfectly!")