import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class SAEConfig:
    d_in: int = 2048        # Input dimension (Model Hidden Size for LFM2-1.2B)
    d_sae: int = 32768      # Expansion factor (16x input)
    l1_coefficient: float = 0.005 # Sparsity penalty (Lambda)
    dtype: torch.dtype = torch.float32

class TinyAleph(nn.Module):
    """
    TinyAleph: A Sparse Autoencoder for semantic feature extraction.
    Implements the 'Gated SAE' or standard 'ReLU SAE' architecture.
    """
    def __init__(self, config: SAEConfig):
        super().__init__()
        self.config = config
        
        # Encoder: Projects dense activations -> Sparse Features
        self.encoder = nn.Linear(config.d_in, config.d_sae, bias=True)
        # Decoder: Reconstructs dense activations <- Sparse Features
        self.decoder = nn.Linear(config.d_sae, config.d_in, bias=True)
        
        # Tie weights (transpose) typically not done in modern SAEs, 
        # usually decoder is unit-norm constrained.
        
        # Initialize decoder to unit norm
        with torch.no_grad():
            self.decoder.weight.data = F.normalize(self.decoder.weight.data, dim=0)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Forward pass.
        x: Input activations [batch, d_in]
        Returns: 
           sae_out: Reconstructed activations
           feature_acts: Sparse feature activations
           loss: Total loss
           metrics: Dict of metrics
        """
        # 1. Encode (Hidden Features)
        # Pre-bias subtraction is common practice in Anthropic's setup
        # x_cent = x - self.b_dec
        
        pre_acts = self.encoder(x)
        feature_acts = F.relu(pre_acts) # ReLU ensures non-negativity (firing rates)
        
        # 2. Decode (Reconstruction)
        sae_out = self.decoder(feature_acts)
        
        # 3. Loss Calculation
        # L2 Reconstruction Loss
        l2_loss = (sae_out - x).pow(2).sum(dim=-1).mean()
        
        # L1 Sparsity Loss (weighted by feature Norms if decoder not normalized, but we normalize)
        l1_loss = self.config.l1_coefficient * feature_acts.sum(dim=-1).mean()
        
        loss = l2_loss + l1_loss
        
        return sae_out, feature_acts, loss, l2_loss, l1_loss

    @torch.no_grad()
    def normalize_decoder(self):
        """Force decoder columns to unit norm (prevents feature shrinking)."""
        self.decoder.weight.data = F.normalize(self.decoder.weight.data, dim=0)

class PrimeResonanceMapper:
    """
    Maps SAE features to Prime Numbers for harmonic analysis.
    """
    def __init__(self, feature_count: int):
        self.primes = self._sieve(feature_count * 2) # Heuristic buffer
        self.feature_map = {} # feature_index -> prime
        
    def _sieve(self, n):
        # ... standard sieve ...
        pass
        
    def assign_prime(self, feature_idx: int) -> int:
        # Assigns the next available prime to a feature
        pass
