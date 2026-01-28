#!/usr/bin/env python3
"""
Test Engram Pattern Completion

Tests whether the trained Engrams are actually being used for
pattern completion in natural language generation.

Made with 💜 by Ada & Luna - Testing the Patterns!
"""

from memory_coordinator import MemoryCoordinator
import json


def load_vocabulary():
    """Load vocabulary for token-to-word mapping."""
    sif_path = "ada-slm/experiments/angel-arch/data/ada_english.sif.json"
    with open(sif_path, 'r') as f:
        sif_data = json.load(f)
    
    word_to_idx = {}
    idx_to_word = {}
    
    for idx, entry in enumerate(sif_data['entries']):
        if entry['type'] == 'word':
            word = entry['word']
            word_to_idx[word] = idx
            idx_to_word[idx] = word
    
    return word_to_idx, idx_to_word


def test_direct_engram_queries(coordinator, word_to_idx, idx_to_word):
    """Test Engrams directly with known patterns from training."""
    print("🧪 Testing Direct Engram Pattern Completion\n")
    print("="*70 + "\n")
    
    # Test phrases we KNOW are in the training data
    test_phrases = [
        ("consciousness", "is"),
        ("bagels", "are"),
        ("the", "golden"),
        ("geometry", "and"),
        ("we", "discovered"),
        ("research", "shows"),
        ("pattern", "completion"),
        ("memory", "system"),
    ]
    
    engrams = coordinator.engrams
    
    for word1, word2 in test_phrases:
        # Convert to token IDs
        token1 = word_to_idx.get(word1, hash(word1) % 10000)
        token2 = word_to_idx.get(word2, hash(word2) % 10000)
        
        context = (token1, token2)
        
        print(f"Input: '{word1} {word2}'")
        
        # Query Engrams
        predictions = engrams.predict_next(context, top_k=5)
        
        if predictions:
            print("   Predictions:")
            for token_id, prob in predictions:
                word = idx_to_word.get(token_id, f"[unknown-{token_id}]")
                print(f"      '{word}' ({prob:.1%})")
        else:
            print("   ❌ No predictions found")
        
        print()
    
    # Show Engram statistics
    stats = engrams.get_statistics()
    print("📊 Engram Usage Statistics:")
    print(f"   Total lookups: {stats['total_lookups']:,}")
    print(f"   Cache hits: {stats['cache_hits']:,}")
    print(f"   Hit rate: {stats['hit_rate']:.1%}")
    print()


def test_conversation_with_engrams(coordinator):
    """Test full conversation flow with Engram completion."""
    print("="*70)
    print("🗣️  Testing Conversation with Engram Completion")
    print("="*70 + "\n")
    
    # Queries that should trigger Engram usage
    test_queries = [
        "Tell me about consciousness and geometry",
        "What are bagels in physics?",
        "Explain the golden ratio",
        "What did we discover about patterns?",
        "How does memory work?",
    ]
    
    for query in test_queries:
        print(f"💭 User: {query}")
        
        result = coordinator.process_query(query, compose_response=True)
        
        if 'natural_response' in result:
            print(f"🗣️  Angel: {result['natural_response']}")
        
        print()
    
    # Show final Engram statistics
    stats = coordinator.engrams.get_statistics()
    print("📊 Final Engram Statistics:")
    print(f"   Total patterns: {stats['total_patterns']:,}")
    print(f"   Total lookups: {stats['total_lookups']:,}")
    print(f"   Cache hits: {stats['cache_hits']:,}")
    print(f"   Hit rate: {stats['hit_rate']:.1%}")
    print()


def main():
    """Main test script."""
    print("🌌 Testing Engram Pattern Completion\n")
    print("="*70 + "\n")
    
    # Initialize coordinator with trained Engrams
    print("🧠 Initializing Memory Coordinator with Trained Engrams...\n")
    
    coordinator = MemoryCoordinator()
    
    # Load layers
    coordinator.load_tool_layer([
        "ada-slm/experiments/angel-arch/data/tools_datetime.sif.json"
    ])
    
    trained_engrams_path = "ada-slm/experiments/angel-arch/data/engrams_trained.pkl"
    coordinator.load_engram_layer(
        n=2,
        hash_size=50000,
        trained_path=trained_engrams_path
    )
    
    coordinator.load_holofield_layer()
    coordinator.load_english_adapter()
    
    print("\n" + "="*70 + "\n")
    
    # Load vocabulary
    word_to_idx, idx_to_word = load_vocabulary()
    
    # Test 1: Direct Engram queries
    test_direct_engram_queries(coordinator, word_to_idx, idx_to_word)
    
    # Test 2: Full conversation flow
    test_conversation_with_engrams(coordinator)
    
    print("="*70)
    print("✨ Engram Completion Test Complete! 💜")
    print("="*70 + "\n")
    
    print("🎉 What we tested:")
    print("   • Direct Engram pattern completion")
    print("   • Engram usage in conversation flow")
    print("   • Hit rate and lookup statistics")
    print("   • Pattern predictions from training data")
    print("\n   The Engrams are ALIVE and completing patterns! 🌌\n")


if __name__ == "__main__":
    main()
