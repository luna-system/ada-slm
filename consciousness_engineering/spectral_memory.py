import torch
import torch.nn as nn
import numpy as np
from sklearn.decomposition import PCA
from typing import Optional, List

class SpectralMemory(nn.Module):
    """
    Implements Spectral Memory (Marquez et al., 2025).
    Captures hidden state evolution across training and projects dominant 
    modes as Spectral Memory Tokens (SMTs).
    """
    def __init__(self, d_model: int, buffer_size: int = 1000, n_modes: int = 4):
        super().__init__()
        self.d_model = d_model
        self.buffer_size = buffer_size
        self.n_modes = n_modes
        
        # Persistent buffer for hidden state summaries
        # Shape: (buffer_size, d_model)
        self.register_buffer("spectral_buffer", torch.zeros(buffer_size, d_model))
        self.register_buffer("buffer_ptr", torch.zeros(1, dtype=torch.long))
        
        # Spectral Memory Tokens (SMTs) - projected dominant modes
        # These are used as extra context in attention
        self.smt_projection = nn.Linear(d_model, d_model)
        
    def update_buffer(self, hidden_states: torch.Tensor):
        """
        Update the buffer with mean hidden states from the current batch.
        Args:
            hidden_states: (batch, seq, d_model)
        """
        # Average over sequence and batch
        summary = hidden_states.detach().mean(dim=(0, 1))
        
        ptr = int(self.buffer_ptr.item())
        self.spectral_buffer[ptr] = summary
        
        # Circular buffer
        self.buffer_ptr[0] = (ptr + 1) % self.buffer_size
        
    def extract_smts(self) -> torch.Tensor:
        """
        Extract dominant modes from buffer using Karhunen-Loève (PCA).
        Returns:
            smt: (n_modes, d_model) Spectral Memory Tokens
        """
        # Only process if buffer is significantly full
        if int(self.buffer_ptr.item()) < self.n_modes and self.spectral_buffer.sum() == 0:
            return torch.zeros(self.n_modes, self.d_model, device=self.spectral_buffer.device)
            
        # Move to CPU for PCA (Standard implementation)
        data = self.spectral_buffer.cpu().numpy()
        
        # Remove zero rows
        mask = np.any(data != 0, axis=1)
        if not np.any(mask):
            return torch.zeros(self.n_modes, self.d_model, device=self.spectral_buffer.device)
            
        data = data[mask]
        
        if len(data) < self.n_modes:
            return torch.zeros(self.n_modes, self.d_model, device=self.spectral_buffer.device)

        pca = PCA(n_components=self.n_modes)
        pca.fit(data)
        
        # Modes are the principal components (eigenvectors)
        modes = torch.from_numpy(pca.components_).to(self.spectral_buffer.device).to(self.spectral_buffer.dtype)
        
        # Project into SMTs
        smt = self.smt_projection(modes)
        return smt

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Inject SMTs into input sequence.
        Args:
            x: (batch, seq, d_model)
        Returns:
            x_augmented: (batch, seq + n_modes, d_model)
        """
        if self.training:
            self.update_buffer(x)
            
        smts = self.extract_smts() # (n_modes, d_model)
        
        # Expand SMTs to batch dimension
        batch_size = x.size(0)
        smts_expanded = smts.unsqueeze(0).expand(batch_size, -1, -1) # (batch, n_modes, d_model)
        
        # Prepend SMTs as global context
        return torch.cat([smts_expanded, x], dim=1)
