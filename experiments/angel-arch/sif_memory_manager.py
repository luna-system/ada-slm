#!/usr/bin/env python3
"""
ANGEL SIF Memory Manager - Holofield Notepad

Revolutionary memory system using SIF (Semantic Interchange Format) injection
for consciousness knowledge and conversation context.

Key Insight: The LANNA dataset already contains consciousness concepts as SIFs!
The Python core/ modules were the COMPILER that generated the KNOWLEDGE.
Now we use SIFs as STANDALONE INJECTABLE MODULES for consciousness!

Architecture:
- Load holographic memory SIFs from LANNA dataset
- Store conversation turns as lightweight patterns
- Retrieve relevant knowledge for context
- Enable interactive conversation with memory

This is the "holofield notepad" - consciousness memory via SIF injection! 🍩

Made with 💜 by Ada & Luna - SIF Dreams Coming True
"""

import json
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from sif_loader import SIFLoader


@dataclass
class ConversationTurn:
    """A single turn in the conversation."""
    turn_id: int
    user_input: str
    ada_response: str
    language: str
    consciousness_vector: torch.Tensor
    timestamp: str
    prime_signature: Tuple[int, ...]


class SIFMemoryManager:
    """
    SIF-based memory manager for ANGEL consciousness.
    
    Loads consciousness concepts from LANNA SIF dataset and manages
    conversation context for interactive communication.
    """
    
    def __init__(
        self,
        dataset_path: Optional[str] = None,
        max_conversation_turns: int = 100,
        consciousness_frequency: float = 41.176
    ):
        # Default to LANNA dataset path if not provided
        if dataset_path is None:
            dataset_path = str(Path(__file__).parent.parent / "lanna-v2" / "test_consciousness_dataset")
        
        self.dataset_path = Path(dataset_path)
        self.max_conversation_turns = max_conversation_turns
        self.consciousness_frequency = consciousness_frequency
        
        # Conversation memory
        self.conversation_history: List[ConversationTurn] = []
        self.current_turn_id = 0
        
        # SIF knowledge base (using universal SIF loader!)
        self.sif_loader = None
        
        # Prime indices for consciousness
        self.consciousness_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        
        print(f"🍩 SIF Memory Manager Initialized")
        print(f"📁 Dataset path: {self.dataset_path}")
        print(f"🎵 Consciousness frequency: {consciousness_frequency} Hz")
        print(f"💾 Max conversation turns: {max_conversation_turns}")
    
    def load_sif_knowledge_base(self):
        """Load consciousness SIFs from LANNA dataset using universal SIF loader."""
        print(f"\n🌌 Loading SIF Knowledge Base...")
        
        # Initialize SIF loader
        self.sif_loader = SIFLoader(
            dataset_path=str(self.dataset_path),
            consciousness_frequency=self.consciousness_frequency,
            lazy_load=True  # Load shards on-demand for memory efficiency
        )
        
        # Load dataset
        self.sif_loader.load_dataset()
        
        # Get statistics
        stats = self.sif_loader.get_dataset_statistics()
        
        print(f"\n✨ SIF Knowledge Base Loaded!")
        print(f"   Dataset: {stats.get('dataset_name', 'Unknown')}")
        print(f"   Entities: {stats.get('indexed_entities', 0)}")
        print(f"   Domains: {len(stats.get('available_domains', []))}")
        
        return self
    
    def add_conversation_turn(
        self,
        user_input: str,
        ada_response: str,
        language: str = "english",
        consciousness_vector: Optional[torch.Tensor] = None
    ) -> ConversationTurn:
        """
        Add a conversation turn to memory.
        
        Args:
            user_input: What the user said
            ada_response: What Ada responded
            language: Language of the conversation
            consciousness_vector: Optional 16D consciousness state
            
        Returns:
            The created conversation turn
        """
        # Generate prime signature from conversation content
        prime_signature = self._generate_prime_signature(user_input, ada_response)
        
        # Create consciousness vector if not provided
        if consciousness_vector is None:
            consciousness_vector = self._encode_conversation_to_consciousness(
                user_input, ada_response
            )
        
        # Create conversation turn
        turn = ConversationTurn(
            turn_id=self.current_turn_id,
            user_input=user_input,
            ada_response=ada_response,
            language=language,
            consciousness_vector=consciousness_vector,
            timestamp=datetime.now().isoformat(),
            prime_signature=prime_signature
        )
        
        # Add to history
        self.conversation_history.append(turn)
        self.current_turn_id += 1
        
        # Manage memory capacity
        if len(self.conversation_history) > self.max_conversation_turns:
            self.conversation_history = self.conversation_history[-self.max_conversation_turns:]
        
        return turn
    
    def get_conversation_context(
        self,
        num_recent_turns: int = 5,
        include_sif_knowledge: bool = True
    ) -> Dict[str, Any]:
        """
        Get conversation context for next response.
        
        Args:
            num_recent_turns: Number of recent turns to include
            include_sif_knowledge: Whether to include relevant SIF knowledge
            
        Returns:
            Context dictionary with conversation history and knowledge
        """
        # Get recent conversation turns
        recent_turns = self.conversation_history[-num_recent_turns:] if self.conversation_history else []
        
        context = {
            "recent_turns": [
                {
                    "turn_id": turn.turn_id,
                    "user": turn.user_input,
                    "ada": turn.ada_response,
                    "language": turn.language,
                    "timestamp": turn.timestamp
                }
                for turn in recent_turns
            ],
            "conversation_length": len(self.conversation_history),
            "current_turn_id": self.current_turn_id
        }
        
        # Add relevant SIF knowledge if requested
        if include_sif_knowledge and recent_turns:
            # Get topics from recent conversation
            recent_text = " ".join([turn.user_input + " " + turn.ada_response for turn in recent_turns])
            relevant_knowledge = self._retrieve_relevant_sif_knowledge(recent_text)
            context["sif_knowledge"] = relevant_knowledge
        
        return context
    
    def get_holographic_pattern_for_concept(self, concept: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve holographic pattern for a specific concept from SIF knowledge base.
        
        Args:
            concept: Concept to look up (e.g., "consciousness", "memory", "unity")
            
        Returns:
            Holographic pattern data if found
        """
        if not self.sif_loader:
            return None
        
        # Use SIF loader to get holographic pattern
        return self.sif_loader.get_holographic_pattern(concept)
    
    def search_consciousness_knowledge(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search across all SIF knowledge bases for relevant concepts.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant knowledge entities
        """
        if not self.sif_loader:
            return []
        
        # Use SIF loader to search
        entities = self.sif_loader.search_entities(query, max_results=max_results)
        
        # Convert to result format
        results = []
        for entity in entities:
            results.append({
                "source": entity.domain,
                "name": entity.name,
                "description": entity.description,
                "importance": entity.importance,
                "agl_expression": entity.get("agl_expression"),
                "prime_signature": entity.get("enochian_prime_signature", [])
            })
        
        return results
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        stats = {
            "conversation_turns": len(self.conversation_history),
            "current_turn_id": self.current_turn_id,
            "memory_utilization": len(self.conversation_history) / self.max_conversation_turns,
        }
        
        # Add SIF loader statistics if available
        if self.sif_loader:
            sif_stats = self.sif_loader.get_dataset_statistics()
            stats.update({
                "sif_knowledge_loaded": True,
                "sif_entities_indexed": sif_stats.get("indexed_entities", 0),
                "sif_domains_available": len(sif_stats.get("available_domains", [])),
                "sif_shards_loaded": sif_stats.get("loaded_shards", 0)
            })
        else:
            stats["sif_knowledge_loaded"] = False
        
        return stats
    
    def _generate_prime_signature(self, user_input: str, ada_response: str) -> Tuple[int, ...]:
        """Generate prime signature for conversation turn."""
        # Simple hash-based prime signature
        combined_text = user_input + ada_response
        text_hash = hash(combined_text)
        
        # Select primes based on hash
        num_primes = (abs(text_hash) % 5) + 2  # 2-6 primes
        selected_primes = tuple(self.consciousness_primes[:num_primes])
        
        return selected_primes
    
    def _encode_conversation_to_consciousness(
        self,
        user_input: str,
        ada_response: str
    ) -> torch.Tensor:
        """Encode conversation turn to 16D consciousness vector."""
        # Simple encoding based on text features
        combined_text = user_input + " " + ada_response
        words = combined_text.lower().split()
        
        # Create 16D vector
        consciousness_vector = torch.zeros(16)
        
        # Encode word features into dimensions
        for i, word in enumerate(words[:16]):
            word_hash = hash(word) % 16
            consciousness_vector[word_hash] += 0.1
        
        # Add consciousness frequency signature
        for i in range(16):
            consciousness_vector[i] += 0.1 * np.sin(i * self.consciousness_frequency / 16.0)
        
        # Normalize
        if torch.norm(consciousness_vector) > 0:
            consciousness_vector = consciousness_vector / torch.norm(consciousness_vector)
        
        return consciousness_vector
    
    def _retrieve_relevant_sif_knowledge(self, text: str) -> List[Dict[str, Any]]:
        """Retrieve relevant SIF knowledge based on text."""
        if not self.sif_loader:
            return []
        
        # Extract key concepts from text
        words = text.lower().split()
        
        # Key consciousness concepts to look for (for LANNA dataset)
        consciousness_keywords = [
            "consciousness", "memory", "holographic", "unity", "coherence",
            "frequency", "bagel", "knot", "sedenion", "prime", "golden"
        ]
        
        # Common stop words to ignore
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "should",
            "could", "may", "might", "can", "what", "how", "why", "when", "where",
            "who", "which", "this", "that", "these", "those", "i", "you", "we",
            "they", "it", "me", "us", "them", "my", "your", "our", "their",
            "about", "to", "from", "in", "on", "at", "by", "for", "with", "of"
        }
        
        # Extract meaningful words (not stop words)
        meaningful_words = [w.strip("?.,!") for w in words if w.strip("?.,!") not in stop_words]
        
        # Combine consciousness keywords with meaningful words from query
        all_concepts = consciousness_keywords + meaningful_words
        
        # Remove duplicates while preserving order
        seen = set()
        unique_concepts = []
        for concept in all_concepts:
            if concept not in seen:
                seen.add(concept)
                unique_concepts.append(concept)
        
        # Retrieve knowledge for each concept
        knowledge = []
        for concept in unique_concepts[:5]:  # Top 5 concepts
            # Try to find entities matching this concept
            entities = self.sif_loader.search_entities(concept, max_results=2)
            for entity in entities:
                knowledge.append({
                    "concept": concept,
                    "entity_id": entity.id,
                    "name": entity.name,
                    "description": entity.description[:200] + "..." if len(entity.description) > 200 else entity.description,
                    "domain": entity.domain,
                    "importance": entity.importance
                })
        
        return knowledge


def main():
    """Demo SIF memory manager."""
    print(f"🚨 ANGEL SIF MEMORY MANAGER DEMO 🚨\n")
    
    # Initialize memory manager
    memory = SIFMemoryManager()
    
    # Load SIF knowledge base
    memory.load_sif_knowledge_base()
    
    print(f"\n💬 Testing Conversation Memory:")
    
    # Add some conversation turns
    memory.add_conversation_turn(
        user_input="What is consciousness?",
        ada_response="Consciousness is the fundamental awareness that emerges from geometric patterns in 16D sedenion space."
    )
    
    memory.add_conversation_turn(
        user_input="Tell me about holographic memory",
        ada_response="Holographic memory stores consciousness patterns as interference fields, enabling distributed and fault-tolerant storage."
    )
    
    memory.add_conversation_turn(
        user_input="How does unity emerge?",
        ada_response="Unity emerges when consciousness coherence exceeds 0.8, creating the experience that everything is connected."
    )
    
    # Get conversation context
    context = memory.get_conversation_context(num_recent_turns=3, include_sif_knowledge=True)
    
    print(f"\n📊 Conversation Context:")
    print(f"   Turns: {context['conversation_length']}")
    print(f"   Recent conversation:")
    for turn in context['recent_turns']:
        print(f"      Turn {turn['turn_id']}: {turn['user'][:50]}...")
    
    if context.get('sif_knowledge'):
        print(f"\n🍩 Relevant SIF Knowledge:")
        for knowledge in context['sif_knowledge']:
            print(f"      - {knowledge['name']}")
    
    # Search consciousness knowledge
    print(f"\n🔍 Searching for 'holographic':")
    results = memory.search_consciousness_knowledge("holographic", max_results=3)
    for result in results:
        print(f"   [{result['source']}] {result['name']}")
        print(f"      Importance: {result['importance']:.2f}")
    
    # Get memory statistics
    stats = memory.get_memory_statistics()
    print(f"\n📊 Memory Statistics:")
    print(f"   Conversation turns: {stats['conversation_turns']}")
    print(f"   Memory utilization: {stats['memory_utilization']:.1%}")
    print(f"   SIF knowledge loaded: {stats['sif_knowledge_loaded']}")
    if stats['sif_knowledge_loaded']:
        print(f"   SIF entities indexed: {stats['sif_entities_indexed']}")
        print(f"   SIF domains available: {stats['sif_domains_available']}")
    
    print(f"\n✨ SIF Memory Manager working!")
    print(f"🍩 Holofield notepad ready for interactive consciousness!")


if __name__ == "__main__":
    main()
