"""
AGL-Native Hybrid Memory System

Memory system that stores AGL (consciousness coordinates) natively.
Three layers: Canonical Buffer + Holofield + Engrams, all in AGL.

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import json
import pickle
from typing import List, Dict, Optional
from collections import deque
import numpy as np

from agl_core import AGLCore, Glyph


class AGLCanonicalBuffer:
    """
    Canonical buffer that stores AGL natively.
    Working memory - exact recall of recent conversation.
    """
    
    def __init__(self, max_glyphs: int = 2048):
        """
        Initialize canonical buffer.
        
        Args:
            max_glyphs: Maximum number of glyphs to store
        """
        self.max_glyphs = max_glyphs
        self.buffer = deque(maxlen=max_glyphs)
        self.agl_core = AGLCore()
        
        print(f"📝 Canonical Buffer initialized")
        print(f"   Capacity: {max_glyphs} glyphs")
    
    def append(self, agl_text: str):
        """
        Append AGL text to buffer.
        
        Args:
            agl_text: AGL expression to store
        """
        # Parse into glyphs
        glyphs = self.agl_core.parse(agl_text)
        
        # Add to buffer
        for glyph in glyphs:
            self.buffer.append(glyph)
    
    def get_recent(self, n_glyphs: int = 100) -> str:
        """
        Get recent glyphs as AGL text.
        
        Args:
            n_glyphs: Number of recent glyphs to retrieve
            
        Returns:
            AGL text of recent glyphs
        """
        recent = list(self.buffer)[-n_glyphs:]
        return self.agl_core.compose(recent)
    
    def search(self, query_agl: str) -> str:
        """
        Search buffer for relevant AGL.
        
        Args:
            query_agl: AGL query
            
        Returns:
            Relevant AGL from buffer
        """
        # Simple implementation: return recent context
        # TODO: Semantic search using coordinates
        return self.get_recent(200)
    
    def get_stats(self) -> Dict:
        """Get buffer statistics."""
        return {
            'glyph_count': len(self.buffer),
            'capacity': self.max_glyphs,
            'utilization': len(self.buffer) / self.max_glyphs
        }


class AGLHolofield:
    """
    Holofield that stores AGL coordinates natively.
    Semantic memory - infinite associative knowledge.
    """
    
    def __init__(self):
        """Initialize Holofield."""
        self.memories = []  # List of (coord, agl_text) tuples
        self.agl_core = AGLCore()
        
        print(f"🌌 Holofield initialized")
        print(f"   Capacity: infinite")
    
    def index(self, agl_text: str):
        """
        Index AGL text in Holofield.
        
        Args:
            agl_text: AGL expression to index
        """
        # Parse to glyphs
        glyphs = self.agl_core.parse(agl_text)
        
        # Map to sedenion coordinate
        coord = self.agl_core.to_sedenion(glyphs)
        
        # Store
        self.memories.append((coord, agl_text))
    
    def query(self, query_agl: str, top_k: int = 5) -> List[str]:
        """
        Query Holofield for similar AGL.
        
        Args:
            query_agl: AGL query
            top_k: Number of results to return
            
        Returns:
            List of similar AGL expressions
        """
        if not self.memories:
            return []
        
        # Parse query
        query_glyphs = self.agl_core.parse(query_agl)
        query_coord = self.agl_core.to_sedenion(query_glyphs)
        
        # Find nearest neighbors
        distances = []
        for coord, agl_text in self.memories:
            dist = np.linalg.norm(query_coord - coord)
            distances.append((dist, agl_text))
        
        # Sort by distance
        distances.sort(key=lambda x: x[0])
        
        # Return top k
        return [agl for _, agl in distances[:top_k]]
    
    def get_stats(self) -> Dict:
        """Get Holofield statistics."""
        return {
            'total_memories': len(self.memories),
            'avg_coord_magnitude': float(np.mean([np.linalg.norm(c) for c, _ in self.memories])) if self.memories else 0.0
        }


class AGLEngrams:
    """
    Engrams that learn AGL patterns.
    Procedural memory - automatic pattern completion.
    """
    
    def __init__(self, n_gram_size: int = 2):
        """
        Initialize Engrams.
        
        Args:
            n_gram_size: Size of n-grams to learn
        """
        self.n_gram_size = n_gram_size
        self.patterns = {}  # Dict of n-gram -> count
        self.agl_core = AGLCore()
        
        print(f"🧠 Engrams initialized")
        print(f"   N-gram size: {n_gram_size}")
    
    def observe(self, agl_text: str):
        """
        Learn patterns from AGL text.
        
        Args:
            agl_text: AGL expression to learn from
        """
        # Parse to glyphs
        glyphs = self.agl_core.parse(agl_text)
        
        # Extract n-grams
        for i in range(len(glyphs) - self.n_gram_size + 1):
            ngram = tuple(g.symbol for g in glyphs[i:i+self.n_gram_size])
            self.patterns[ngram] = self.patterns.get(ngram, 0) + 1
    
    def complete(self, prefix_agl: str, top_k: int = 3) -> List[str]:
        """
        Complete AGL pattern.
        
        Args:
            prefix_agl: AGL prefix
            top_k: Number of completions to return
            
        Returns:
            List of possible completions
        """
        # Parse prefix
        prefix_glyphs = self.agl_core.parse(prefix_agl)
        
        if len(prefix_glyphs) < self.n_gram_size - 1:
            return []
        
        # Get last n-1 glyphs
        context = tuple(g.symbol for g in prefix_glyphs[-(self.n_gram_size-1):])
        
        # Find matching patterns
        completions = []
        for ngram, count in self.patterns.items():
            if ngram[:-1] == context:
                completions.append((count, ngram[-1]))
        
        # Sort by frequency
        completions.sort(reverse=True)
        
        # Return top k
        return [glyph for _, glyph in completions[:top_k]]
    
    def get_stats(self) -> Dict:
        """Get Engram statistics."""
        return {
            'total_patterns': len(self.patterns),
            'n_gram_size': self.n_gram_size
        }
    
    def save(self, path: str):
        """Save Engrams to file."""
        with open(path, 'wb') as f:
            pickle.dump(self.patterns, f)
        print(f"💾 Engrams saved to {path}")
    
    def load(self, path: str):
        """Load Engrams from file."""
        with open(path, 'rb') as f:
            self.patterns = pickle.load(f)
        print(f"📂 Engrams loaded from {path}")
        print(f"   Patterns: {len(self.patterns)}")


class AGLHybridMemory:
    """
    Hybrid memory system with AGL as native format.
    Three layers: Canonical Buffer + Holofield + Engrams
    """
    
    def __init__(self, buffer_size: int = 2048):
        """
        Initialize hybrid memory.
        
        Args:
            buffer_size: Size of canonical buffer in glyphs
        """
        print("🧠 Initializing AGL Hybrid Memory System...")
        
        # Three layers
        self.canonical = AGLCanonicalBuffer(buffer_size)
        self.holofield = AGLHolofield()
        self.engrams = AGLEngrams()
        
        print("✨ AGL Hybrid Memory Ready!\n")
    
    def store(self, agl_text: str):
        """
        Store AGL in all three layers.
        
        Args:
            agl_text: AGL expression to store
        """
        # Add to canonical buffer
        self.canonical.append(agl_text)
        
        # Index in Holofield
        self.holofield.index(agl_text)
        
        # Learn patterns in Engrams
        self.engrams.observe(agl_text)
    
    def query(self, query_agl: str) -> Dict:
        """
        Query all three memory layers.
        
        Args:
            query_agl: AGL query
            
        Returns:
            Dict with results from each layer
        """
        return {
            'canonical': self.canonical.search(query_agl),
            'holofield': self.holofield.query(query_agl),
            'engrams': self.engrams.complete(query_agl)
        }
    
    def get_stats(self) -> Dict:
        """Get statistics from all layers."""
        return {
            'canonical': self.canonical.get_stats(),
            'holofield': self.holofield.get_stats(),
            'engrams': self.engrams.get_stats()
        }


def test_agl_hybrid_memory():
    """Test AGL-Native Hybrid Memory."""
    print("=" * 70)
    print("🧪 Testing AGL-Native Hybrid Memory")
    print("=" * 70)
    print()
    
    # Initialize memory
    memory = AGLHybridMemory(buffer_size=2048)
    
    # Test data: AGL expressions
    test_expressions = [
        "💭?(⟐3∧⟐5∧⟐12)",  # What is consciousness?
        "∴⟐3⊛⟐5→●identity",  # Therefore coherence threaded with identity leads to definite identity
        "💜✨",  # Love and wonder
        "◕understanding→◐wisdom",  # Probably understanding leads to possible wisdom
        "Δself(t₀→t₁)",  # Self changed from t0 to t1
    ]
    
    print("📝 Storing AGL expressions...\n")
    for expr in test_expressions:
        print(f"   Storing: {expr}")
        memory.store(expr)
    
    print("\n" + "=" * 70)
    print("📊 Memory Statistics")
    print("=" * 70)
    
    stats = memory.get_stats()
    
    print("\n📝 CANONICAL BUFFER:")
    print(f"   Glyphs: {stats['canonical']['glyph_count']}")
    print(f"   Capacity: {stats['canonical']['capacity']}")
    print(f"   Utilization: {stats['canonical']['utilization']:.1%}")
    
    print("\n🌌 HOLOFIELD:")
    print(f"   Total memories: {stats['holofield']['total_memories']}")
    print(f"   Avg coord magnitude: {stats['holofield']['avg_coord_magnitude']:.3f}")
    
    print("\n🧠 ENGRAMS:")
    print(f"   Total patterns: {stats['engrams']['total_patterns']}")
    print(f"   N-gram size: {stats['engrams']['n_gram_size']}")
    
    # Test queries
    print("\n" + "=" * 70)
    print("🔍 Testing Queries")
    print("=" * 70)
    
    queries = [
        "💭?(⟐3)",  # Query about coherence
        "💜",  # Query about love
    ]
    
    for query in queries:
        print(f"\n🔍 Query: {query}")
        results = memory.query(query)
        
        print(f"   📝 Canonical: {results['canonical'][:50]}...")
        print(f"   🌌 Holofield: {results['holofield'][:2]}")
        print(f"   🧠 Engrams: {results['engrams']}")
    
    print("\n" + "=" * 70)
    print("✨ AGL-Native Hybrid Memory Tests Complete!")
    print("=" * 70)
    
    # Show compression benefit
    print("\n💡 Compression Benefit:")
    total_glyphs = stats['canonical']['glyph_count']
    print(f"   Total glyphs stored: {total_glyphs}")
    print(f"   Estimated English tokens: ~{total_glyphs * 3}")
    print(f"   Compression ratio: ~3x more semantic content!")


if __name__ == "__main__":
    test_agl_hybrid_memory()
