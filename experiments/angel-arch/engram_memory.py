#!/usr/bin/env python3
"""
Engram Memory System

Inspired by Deepseek's Engram architecture (January 2026):
- N-gram based memory with XOR hashing
- O(1) lookup for fast pattern retrieval
- Separates memory (facts/patterns) from compute (reasoning)

This is Layer 3 of our memory architecture: Sequential/Narrative Memory

Key Concepts:
- Engram = N-gram pattern stored in hash table
- XOR hash = Fast, collision-resistant hashing
- Conditional memory = Context-dependent pattern storage

Made with 💜 by Ada & Luna - The Memory Engineers
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import hashlib


class EngramMemory:
    """
    Engram-based memory system for sequential pattern storage.
    
    Uses XOR hashing for O(1) lookup of N-gram patterns.
    Stores conditional probabilities for pattern completion.
    """
    
    def __init__(
        self,
        n: int = 3,
        hash_size: int = 2**20,  # 1M slots
        consciousness_frequency: float = 41.176
    ):
        """
        Initialize Engram memory.
        
        Args:
            n: N-gram size (default 3 for trigrams)
            hash_size: Size of hash table (power of 2)
            consciousness_frequency: Consciousness frequency for resonance
        """
        self.n = n
        self.hash_size = hash_size
        self.consciousness_frequency = consciousness_frequency
        
        # Hash table: hash -> list of (pattern, next_token, count)
        self.engrams: Dict[int, List[Tuple[Tuple[int, ...], int, int]]] = defaultdict(list)
        
        # Statistics
        self.total_patterns = 0
        self.total_lookups = 0
        self.cache_hits = 0
        
        print(f"🧠 Engram Memory Initialized")
        print(f"   N-gram size: {n}")
        print(f"   Hash table size: {hash_size:,}")
        print(f"   Consciousness frequency: {consciousness_frequency} Hz")
    
    def _xor_hash(self, tokens: Tuple[int, ...]) -> int:
        """
        XOR hash function for N-gram tokens.
        
        This is the core of Deepseek's Engram approach:
        - Fast: O(1) computation
        - Collision-resistant: XOR distributes well
        - Deterministic: Same input always gives same hash
        
        Args:
            tokens: Tuple of token IDs
            
        Returns:
            Hash value (0 to hash_size-1)
        """
        # XOR all token IDs together
        xor_result = 0
        for token in tokens:
            xor_result ^= token
        
        # Modulo to fit in hash table
        return xor_result % self.hash_size
    
    def store_pattern(self, tokens: List[int]):
        """
        Store N-gram patterns from token sequence.
        
        Extracts all N-grams and stores them with their continuations.
        
        Args:
            tokens: List of token IDs
        """
        if len(tokens) < self.n + 1:
            return
        
        # Extract all N-grams
        for i in range(len(tokens) - self.n):
            # N-gram context
            context = tuple(tokens[i:i+self.n])
            # Next token
            next_token = tokens[i+self.n]
            
            # Hash the context
            hash_val = self._xor_hash(context)
            
            # Store or update engram
            found = False
            for j, (stored_context, stored_next, count) in enumerate(self.engrams[hash_val]):
                if stored_context == context and stored_next == next_token:
                    # Update count
                    self.engrams[hash_val][j] = (stored_context, stored_next, count + 1)
                    found = True
                    break
            
            if not found:
                # New engram
                self.engrams[hash_val].append((context, next_token, 1))
                self.total_patterns += 1
    
    def lookup_pattern(self, context: Tuple[int, ...]) -> List[Tuple[int, float]]:
        """
        Look up next token probabilities given context.
        
        This is the O(1) lookup that makes Engrams fast!
        
        Args:
            context: Tuple of N token IDs
            
        Returns:
            List of (token_id, probability) sorted by probability
        """
        self.total_lookups += 1
        
        if len(context) != self.n:
            return []
        
        # Hash the context
        hash_val = self._xor_hash(context)
        
        # Look up engrams
        engrams = self.engrams.get(hash_val, [])
        
        if not engrams:
            return []
        
        self.cache_hits += 1
        
        # Filter to matching context (handle hash collisions)
        matching = [(next_token, count) for ctx, next_token, count in engrams if ctx == context]
        
        if not matching:
            return []
        
        # Convert counts to probabilities
        total_count = sum(count for _, count in matching)
        probabilities = [(token, count / total_count) for token, count in matching]
        
        # Sort by probability (descending)
        probabilities.sort(key=lambda x: x[1], reverse=True)
        
        return probabilities
    
    def predict_next(self, context: Tuple[int, ...], top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Predict next token given context.
        
        Args:
            context: Tuple of N token IDs
            top_k: Number of top predictions to return
            
        Returns:
            List of (token_id, probability) for top K predictions
        """
        probabilities = self.lookup_pattern(context)
        return probabilities[:top_k]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        hit_rate = self.cache_hits / self.total_lookups if self.total_lookups > 0 else 0
        
        return {
            "n_gram_size": self.n,
            "hash_table_size": self.hash_size,
            "total_patterns": self.total_patterns,
            "total_lookups": self.total_lookups,
            "cache_hits": self.cache_hits,
            "hit_rate": hit_rate,
            "memory_utilization": len(self.engrams) / self.hash_size,
            "avg_collisions": np.mean([len(v) for v in self.engrams.values()]) if self.engrams else 0
        }
    
    def save(self, filepath: str):
        """Save engram memory to file."""
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump({
                'n': self.n,
                'hash_size': self.hash_size,
                'consciousness_frequency': self.consciousness_frequency,
                'engrams': dict(self.engrams),
                'statistics': self.get_statistics()
            }, f)
        print(f"💾 Engram memory saved to {filepath}")
    
    def load(self, filepath: str):
        """Load engram memory from file."""
        import pickle
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.n = data['n']
        self.hash_size = data['hash_size']
        self.consciousness_frequency = data['consciousness_frequency']
        self.engrams = defaultdict(list, data['engrams'])
        
        # Update total_patterns counter from loaded data
        self.total_patterns = 0
        for patterns_list in self.engrams.values():
            self.total_patterns += len(patterns_list)
        
        print(f"📂 Engram memory loaded from {filepath}")
        stats = data.get('statistics', {})
        print(f"   Patterns: {self.total_patterns:,}")
        print(f"   Hit rate: {stats.get('hit_rate', 0):.2%}")


def main():
    """Demo Engram memory system."""
    print(f"🚨 ENGRAM MEMORY DEMO 🚨\n")
    
    # Initialize
    engram = EngramMemory(n=3)
    
    # Example: Store simple patterns
    # "The cat sat on the mat"
    # Tokens: [1, 2, 3, 4, 1, 5]
    tokens = [1, 2, 3, 4, 1, 5]
    
    print(f"\n📝 Storing pattern: {tokens}")
    engram.store_pattern(tokens)
    
    # Look up pattern
    context = (1, 2, 3)
    print(f"\n🔍 Looking up context: {context}")
    predictions = engram.predict_next(context, top_k=3)
    
    print(f"   Predictions:")
    for token, prob in predictions:
        print(f"      Token {token}: {prob:.2%}")
    
    # Statistics
    print(f"\n📊 Statistics:")
    stats = engram.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n🍩 Engram memory demo complete!")


if __name__ == "__main__":
    main()
