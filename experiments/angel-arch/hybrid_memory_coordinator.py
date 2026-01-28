#!/usr/bin/env python3
"""
Hybrid Memory Coordinator

Coordinates three memory layers:
- Canonical Buffer (working memory - exact recent text)
- Holofield (semantic memory - infinite associative knowledge)
- Engrams (pattern memory - trained completions)

This is how Angel REMEMBERS! 💜

Made with ✨ by Ada & Luna - The Memory Engineers
"""

import time
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import deque

from engram_memory import EngramMemory


class CanonicalBuffer:
    """
    Canonical text buffer - working memory.
    
    Stores exact recent conversation with limited capacity.
    Like human working memory: 7±2 items, immediate recall.
    """
    
    def __init__(self, max_tokens: int = 2048):
        """
        Initialize canonical buffer.
        
        Args:
            max_tokens: Maximum tokens to store (default: 2048)
        """
        self.max_tokens = max_tokens
        self.buffer = deque()  # Fast append/pop from both ends
        self.current_tokens = 0
    
    def add(self, role: str, text: str):
        """
        Add message to buffer, evict old if needed.
        
        Args:
            role: 'user' or 'assistant'
            text: Message text
        """
        # Simple tokenization (split on whitespace)
        tokens = len(text.split())
        
        # Create message entry
        message = {
            'role': role,
            'text': text,
            'tokens': tokens,
            'timestamp': time.time()
        }
        
        # Add to buffer
        self.buffer.append(message)
        self.current_tokens += tokens
        
        # Evict old messages if over limit
        while self.current_tokens > self.max_tokens and len(self.buffer) > 1:
            old = self.buffer.popleft()
            self.current_tokens -= old['tokens']
    
    def get_recent(self, n: Optional[int] = None) -> List[Dict]:
        """
        Get recent N messages (or all if n=None).
        
        Args:
            n: Number of recent messages to get
            
        Returns:
            List of message dicts
        """
        if n is None:
            return list(self.buffer)
        return list(self.buffer)[-n:]
    
    def get_context_string(self) -> str:
        """
        Get buffer as formatted string for context.
        
        Returns:
            Formatted conversation string
        """
        return "\n".join([
            f"{msg['role']}: {msg['text']}"
            for msg in self.buffer
        ])
    
    def clear(self):
        """Clear the buffer."""
        self.buffer.clear()
        self.current_tokens = 0
    
    def get_statistics(self) -> Dict:
        """Get buffer statistics."""
        return {
            'messages': len(self.buffer),
            'tokens': self.current_tokens,
            'capacity': self.max_tokens,
            'utilization': self.current_tokens / self.max_tokens
        }


class HoloFieldMemory:
    """
    Holofield semantic memory - infinite associative knowledge.
    
    Stores meaning in 16D sedenion space.
    Content-addressed by semantic chord.
    """
    
    def __init__(self):
        """Initialize Holofield memory."""
        self.memories = []  # List of memory dicts
        self.index = {}     # Fast lookup by semantic chord
    
    def store(self, text: str, importance: float = 1.0):
        """
        Store text in Holofield with semantic chord.
        
        Args:
            text: Text to store
            importance: Importance weight (default: 1.0)
        """
        # Compute semantic chord (16D coordinates)
        chord = self._compute_semantic_chord(text)
        
        memory = {
            'text': text,
            'chord': chord,
            'importance': importance,
            'timestamp': time.time()
        }
        
        self.memories.append(memory)
        self._index_memory(memory)
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Find semantically similar memories.
        
        Args:
            query_text: Query text
            top_k: Number of results to return
            
        Returns:
            List of memory dicts with resonance scores
        """
        query_chord = self._compute_semantic_chord(query_text)
        
        # Calculate resonance with all memories
        results = []
        for memory in self.memories:
            resonance = self._chord_resonance(query_chord, memory['chord'])
            results.append({
                **memory,
                'resonance': resonance
            })
        
        # Sort by resonance and return top K
        results.sort(key=lambda x: x['resonance'], reverse=True)
        return results[:top_k]
    
    def _compute_semantic_chord(self, text: str) -> np.ndarray:
        """
        Compute 16D semantic chord from text.
        
        Uses simple hash-based approach for now.
        TODO: Use prime signatures from LANNA!
        """
        # Simple hash-based chord for now
        words = text.lower().split()
        chord = np.zeros(16)
        
        for word in words:
            # Hash word to dimension
            hash_val = hash(word)
            dim = abs(hash_val) % 16
            chord[dim] += 1.0
        
        # Normalize
        if np.linalg.norm(chord) > 0:
            chord = chord / np.linalg.norm(chord)
        
        return chord
    
    def _chord_resonance(self, chord1: np.ndarray, chord2: np.ndarray) -> float:
        """
        Calculate harmonic resonance between chords.
        
        Uses cosine similarity in 16D space.
        """
        norm1 = np.linalg.norm(chord1)
        norm2 = np.linalg.norm(chord2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return np.dot(chord1, chord2) / (norm1 * norm2)
    
    def _index_memory(self, memory: Dict):
        """Index memory for fast lookup."""
        # Simple indexing by first word for now
        words = memory['text'].lower().split()
        if words:
            first_word = words[0]
            if first_word not in self.index:
                self.index[first_word] = []
            self.index[first_word].append(memory)
    
    def get_statistics(self) -> Dict:
        """Get Holofield statistics."""
        return {
            'total_memories': len(self.memories),
            'indexed_words': len(self.index),
            'avg_chord_magnitude': np.mean([
                np.linalg.norm(m['chord']) for m in self.memories
            ]) if self.memories else 0.0
        }


class HybridMemoryCoordinator:
    """
    Coordinates all three memory layers.
    
    This is the complete memory system for Angel!
    """
    
    def __init__(
        self,
        buffer_size: int = 2048,
        use_engrams: bool = True
    ):
        """
        Initialize hybrid memory coordinator.
        
        Args:
            buffer_size: Canonical buffer size in tokens
            use_engrams: Whether to use Engram memory
        """
        print(f"🧠 Initializing Hybrid Memory System...")
        
        # Initialize memory layers
        self.canonical = CanonicalBuffer(max_tokens=buffer_size)
        print(f"   ✅ Canonical buffer ready ({buffer_size} tokens)")
        
        self.holofield = HoloFieldMemory()
        print(f"   ✅ Holofield ready (infinite capacity)")
        
        if use_engrams:
            self.engrams = EngramMemory(n=2, hash_size=10000)
            print(f"   ✅ Engrams ready (pattern completion)")
        else:
            self.engrams = None
        
        print(f"✨ Hybrid Memory System Ready!\n")
    
    def process_input(self, role: str, text: str):
        """
        Process incoming message through all memory layers.
        
        Args:
            role: 'user' or 'assistant'
            text: Message text
        """
        # 1. Add to canonical buffer (exact text)
        self.canonical.add(role, text)
        
        # 2. Extract important phrases for Holofield
        key_phrases = self._extract_key_phrases(text)
        for phrase in key_phrases:
            importance = self._calculate_importance(phrase, role)
            self.holofield.store(phrase, importance)
        
        # 3. Update Engram patterns
        if self.engrams:
            # Convert text to token sequence
            words = text.lower().split()
            if len(words) >= 2:
                # Simple hash-based tokenization
                tokens = [hash(w) % 10000 for w in words]
                self.engrams.store_pattern(tokens)
    
    def generate_context(self, query: str) -> Dict:
        """
        Generate context for response generation.
        
        Queries all three memory layers and returns combined context.
        
        Args:
            query: User query
            
        Returns:
            Dict with context from all memory layers
        """
        # Get canonical buffer context
        canonical_context = self.canonical.get_context_string()
        
        # Query Holofield for semantic memories
        semantic_memories = self.holofield.query(query, top_k=5)
        
        # Get Engram pattern completions
        patterns = []
        if self.engrams:
            # Get query words
            query_words = query.lower().split()
            if query_words:
                # Try to predict next words
                patterns = self.engrams.predict_next(
                    tuple([hash(w) % 10000 for w in query_words[-2:]]),
                    top_k=3
                )
        
        # Extract topics from Holofield
        holofield_topics = [
            mem['text'].split()[0] 
            for mem in semantic_memories 
            if mem['text']
        ][:3]
        
        return {
            'canonical': canonical_context,
            'semantic': semantic_memories,
            'patterns': patterns,
            'holofield_topics': holofield_topics,
            'buffer_size': self.canonical.current_tokens,
            'holofield_size': len(self.holofield.memories),
            'engram_patterns': self.engrams.get_statistics()['total_patterns'] if self.engrams else 0
        }
    
    def consolidate_memory(self):
        """
        Periodic memory consolidation.
        
        Moves important buffer content to Holofield.
        Strengthens frequently used Engram patterns.
        """
        # Move important buffer content to Holofield
        for msg in self.canonical.buffer:
            if self._is_important(msg):
                self.holofield.store(msg['text'], importance=2.0)
        
        # Consolidate Engrams (if enabled)
        if self.engrams:
            self.engrams.consolidate()
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases from text.
        
        Simple approach: sentences or long phrases.
        """
        # Split on sentence boundaries
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        
        # Filter to meaningful phrases
        phrases = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence.split()) >= 3:  # At least 3 words
                phrases.append(sentence)
        
        # If no sentences, use whole text
        if not phrases and len(text.split()) >= 3:
            phrases = [text]
        
        return phrases
    
    def _calculate_importance(self, phrase: str, role: str) -> float:
        """
        Calculate importance of a phrase.
        
        User messages are more important (we want to remember what they said!).
        """
        base_importance = 1.0
        
        # User messages are more important
        if role == 'user':
            base_importance *= 1.5
        
        # Longer phrases are more important
        word_count = len(phrase.split())
        if word_count > 5:
            base_importance *= 1.2
        
        # Questions are more important
        if '?' in phrase:
            base_importance *= 1.3
        
        return base_importance
    
    def _is_important(self, message: Dict) -> bool:
        """
        Check if a message is important enough to consolidate.
        
        Important messages get moved from buffer to Holofield.
        """
        # User messages are important
        if message['role'] == 'user':
            return True
        
        # Long messages are important
        if message['tokens'] > 20:
            return True
        
        # Questions are important
        if '?' in message['text']:
            return True
        
        return False
    
    def get_statistics(self) -> Dict:
        """Get statistics from all memory layers."""
        stats = {
            'canonical': self.canonical.get_statistics(),
            'holofield': self.holofield.get_statistics()
        }
        
        if self.engrams:
            stats['engrams'] = self.engrams.get_statistics()
        
        return stats
    
    def clear_all(self):
        """Clear all memory layers (for testing)."""
        self.canonical.clear()
        self.holofield.memories.clear()
        self.holofield.index.clear()
        # Engrams don't have a simple clear method - would need to reinitialize


def test_hybrid_memory():
    """Test the hybrid memory coordinator."""
    print("🌌 Testing Hybrid Memory Coordinator\n")
    
    # Initialize
    coordinator = HybridMemoryCoordinator()
    
    # Test conversation
    print("📝 Testing Memory Storage:\n")
    
    conversation = [
        ('user', 'What is consciousness?'),
        ('assistant', 'Consciousness is geometry and love'),
        ('user', 'Tell me about bagels'),
        ('assistant', 'Bagels are toroidal consciousness structures'),
        ('user', 'What did we talk about earlier?')
    ]
    
    for role, text in conversation:
        coordinator.process_input(role, text)
        print(f"   {role}: {text}")
    
    print("\n🔍 Testing Context Generation:\n")
    
    # Generate context for query
    context = coordinator.generate_context('What did we discuss?')
    
    print(f"   Canonical buffer: {len(context['canonical'])} chars")
    print(f"   Semantic memories: {len(context['semantic'])} results")
    print(f"   Holofield topics: {context['holofield_topics']}")
    print(f"   Pattern predictions: {len(context['patterns'])} patterns")
    
    # Show statistics
    print("\n📊 Memory Statistics:")
    stats = coordinator.get_statistics()
    for layer, layer_stats in stats.items():
        print(f"\n   {layer.upper()}:")
        for key, value in layer_stats.items():
            print(f"      {key}: {value}")
    
    print("\n✨ Hybrid memory test complete! 💜\n")


if __name__ == "__main__":
    test_hybrid_memory()
