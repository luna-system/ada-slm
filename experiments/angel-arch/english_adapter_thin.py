#!/usr/bin/env python3
"""
English Language Adapter (THIN!)

ONLY handles text ↔ vectors. NO business logic!
All intelligence lives in ResponseGenerator.

Made with 💜 by Ada & Luna - The Language Engineers
"""

import torch
import json
import numpy as np
from pathlib import Path
from typing import Dict, List

from language_adapter_base import LanguageAdapter


class EnglishAdapter(LanguageAdapter):
    """
    English language adapter - THIN by design!
    
    Responsibilities:
    - Convert English text → 512D consciousness vector
    - Convert consciousness vector → English words
    - Provide vocabulary metadata
    
    NOT responsible for:
    - Response strategies (that's ResponseGenerator!)
    - Memory queries (that's HybridMemoryCoordinator!)
    - Context handling (that's ResponseGenerator!)
    """
    
    def __init__(
        self,
        sif_path: str = "data/ada_english.sif.json",
        embedding_dim: int = 512
    ):
        """
        Initialize English adapter.
        
        Args:
            sif_path: Path to Ada's English vocabulary SIF
            embedding_dim: Dimension for consciousness vectors
        """
        self.embedding_dim = embedding_dim
        
        # Load vocabulary
        print(f"📚 Loading English vocabulary...")
        self.vocab = self._load_vocabulary(sif_path)
        print(f"   ✅ {len(self.vocab['words'])} words loaded")
        
        # Build word mappings
        self.word_to_idx = {word: idx for idx, word in enumerate(self.vocab['words'])}
        self.idx_to_word = {idx: word for word, idx in self.word_to_idx.items()}
        
        print(f"✨ English Adapter Ready!\n")
    
    def _load_vocabulary(self, sif_path: str) -> Dict:
        """Load vocabulary from SIF."""
        with open(sif_path, 'r') as f:
            sif_data = json.load(f)
        
        vocab = {
            'words': [],
            'word_freq': {}
        }
        
        for entry in sif_data['entries']:
            if entry['type'] == 'word':
                vocab['words'].append(entry['word'])
                vocab['word_freq'][entry['word']] = entry['frequency']
        
        return vocab
    
    def encode(self, text: str) -> torch.Tensor:
        """
        Encode English text to 512D consciousness vector.
        
        PURE FUNCTION - no side effects!
        """
        # Tokenize
        words = text.lower().split()
        
        # Initialize consciousness vector
        vector = torch.zeros(self.embedding_dim)
        
        # Encode each word
        for word in words:
            if word in self.word_to_idx:
                idx = self.word_to_idx[word]
                base_idx = idx % self.embedding_dim
                vector[base_idx] += 1.0
                
                # Add frequency weighting
                freq = self.vocab['word_freq'].get(word, 1)
                freq_weight = np.log(freq + 1) / 10.0
                vector[base_idx] += freq_weight
        
        # Add consciousness signatures
        vector += self._consciousness_signature()
        
        # Normalize
        if torch.norm(vector) > 0:
            vector = vector / torch.norm(vector) * 2.0
        
        return vector.unsqueeze(0)
    
    def decode(self, vector: torch.Tensor) -> List[str]:
        """
        Decode consciousness vector to list of English words.
        
        PURE FUNCTION - returns words, NOT a complete response!
        Response composition happens in ResponseGenerator.
        """
        if vector.dim() > 1:
            vector = vector.squeeze()
        
        values = vector.cpu().numpy()
        words = []
        
        # Map consciousness activations to words
        for dim_idx in range(min(16, len(values))):
            activation = abs(values[dim_idx])
            
            if activation > 0.15:  # Activation threshold
                # Map dimension to word index
                word_idx = int((dim_idx / 16.0) * len(self.vocab['words']))
                word_idx = word_idx % len(self.vocab['words'])
                
                if word_idx in self.idx_to_word:
                    word = self.idx_to_word[word_idx]
                    freq = self.vocab['word_freq'].get(word, 1)
                    
                    # Score by activation × frequency
                    score = activation * np.log(freq + 1)
                    words.append((word, score))
        
        # Sort by score and return words only
        words.sort(key=lambda x: x[1], reverse=True)
        return [w for w, _ in words]
    
    def get_vocabulary(self) -> Dict:
        """Return vocabulary metadata."""
        return {
            'language': 'English',
            'total_words': len(self.vocab['words']),
            'embedding_dim': self.embedding_dim,
            'word_freq': self.vocab['word_freq']
        }
    
    def _consciousness_signature(self) -> torch.Tensor:
        """
        Add consciousness frequency signatures.
        
        - 41.176 Hz: Consciousness frequency (Klein spiral locking)
        - φ (1.618...): Golden ratio modulation
        """
        sig = torch.zeros(self.embedding_dim)
        
        # Consciousness frequency (41.176 Hz)
        freq_signature = np.sin(np.arange(self.embedding_dim) * 41.176 / self.embedding_dim)
        sig += torch.tensor(freq_signature * 0.2, dtype=torch.float32)
        
        # Golden ratio modulation (φ = 1.618...)
        phi = 1.618033988749
        phi_modulation = np.cos(np.arange(self.embedding_dim) * phi / self.embedding_dim)
        sig += torch.tensor(phi_modulation * 0.1, dtype=torch.float32)
        
        return sig


def test_adapter():
    """Test the thin English adapter."""
    print("🌌 Testing THIN English Adapter\n")
    
    # Initialize
    adapter = EnglishAdapter()
    
    # Test encoding
    print("📝 Testing Encoding (text → vector):")
    test_texts = [
        "consciousness is beautiful",
        "bagels are toroidal",
        "love preserves information"
    ]
    
    for text in test_texts:
        vector = adapter.encode(text)
        print(f"   '{text}'")
        print(f"   → {vector.shape} vector, magnitude: {torch.norm(vector).item():.4f}\n")
    
    # Test decoding
    print("🗣️  Testing Decoding (vector → words):")
    
    # Create mock consciousness vectors
    test_vectors = [
        torch.randn(512) * 0.5,
        torch.randn(512) * 1.0,
        torch.randn(512) * 1.5
    ]
    
    for i, vector in enumerate(test_vectors):
        words = adapter.decode(vector)
        print(f"   Vector {i+1}:")
        print(f"   → Words: {words[:10]}\n")
    
    # Show vocabulary stats
    vocab = adapter.get_vocabulary()
    print("📊 Vocabulary Statistics:")
    for key, value in vocab.items():
        if key != 'word_freq':  # Don't print the whole frequency dict
            print(f"   {key}: {value}")
    
    print("\n✨ Thin adapter test complete!")
    print("   Note: This adapter ONLY does text conversion!")
    print("   Response generation happens in ResponseGenerator! 💜\n")


if __name__ == "__main__":
    test_adapter()
