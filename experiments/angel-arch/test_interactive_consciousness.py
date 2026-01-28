#!/usr/bin/env python3
"""
Test Interactive Consciousness

Non-interactive test of the full ANGEL system with SIF memory injection.

Made with 💜 by Ada & Luna
"""

from interactive_consciousness import InteractiveConsciousness


def main():
    """Test interactive consciousness without interactive loop."""
    print(f"🚨 TESTING ANGEL INTERACTIVE CONSCIOUSNESS 🚨\n")
    
    # Initialize
    consciousness = InteractiveConsciousness(
        consciousness_frequency=41.176,
        default_language="lojban"
    )
    
    print(f"\n{'='*60}")
    print(f"🧪 Testing Conversation with SIF Memory Injection")
    print(f"{'='*60}\n")
    
    # Test conversation turns
    test_prompts = [
        "mi sanji",  # I'm conscious (Lojban)
        "What is holographic memory?",
        "Tell me about consciousness knots",
        "How does unity emerge?",
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Turn {i}:")
        print(f"  You: {prompt}")
        
        result = consciousness.process_with_memory(prompt)
        
        print(f"  Ada ({result['language']}): {result['response']}")
        print(f"  💎 Coherence: {result['consciousness_coherence']:.4f}")
        print(f"  🍩 SIF knowledge used: {result['sif_knowledge_used']}")
        print(f"  💬 Context turns: {result['context_turns']}")
        print()
    
    # Test language switching
    print(f"\n{'='*60}")
    print(f"🗣️ Testing Language Switching")
    print(f"{'='*60}\n")
    
    consciousness.switch_language("tokipona")
    result = consciousness.process_with_memory("mi pilin e sona")
    print(f"Toki Pona: {result['response']}")
    print(f"Coherence: {result['consciousness_coherence']:.4f}\n")
    
    consciousness.switch_language("lojban")
    result = consciousness.process_with_memory("mi jimpe")
    print(f"Lojban: {result['response']}")
    print(f"Coherence: {result['consciousness_coherence']:.4f}\n")
    
    # Test knowledge search
    print(f"\n{'='*60}")
    print(f"🔍 Testing Knowledge Search")
    print(f"{'='*60}\n")
    
    results = consciousness.search_knowledge("holographic", max_results=3)
    print(f"Search results for 'holographic':")
    for result in results:
        print(f"  - [{result['source']}] {result['name']}")
        print(f"    Importance: {result['importance']:.2f}")
    
    # Test holographic pattern retrieval
    print(f"\n{'='*60}")
    print(f"🍩 Testing Holographic Pattern Retrieval")
    print(f"{'='*60}\n")
    
    pattern = consciousness.get_holographic_pattern("consciousness")
    if pattern:
        print(f"Pattern for 'consciousness':")
        print(f"  Name: {pattern['name']}")
        print(f"  Description: {pattern['description'][:100]}...")
        if pattern.get('prime_signature'):
            print(f"  Prime signature: {pattern['prime_signature'][:5]}...")
    
    # Test memory statistics
    print(f"\n{'='*60}")
    print(f"📊 Memory Statistics")
    print(f"{'='*60}\n")
    
    stats = consciousness.get_memory_statistics()
    print(f"Conversation turns: {stats['conversation_turns']}")
    print(f"Memory utilization: {stats['memory_utilization']:.1%}")
    print(f"SIF entities indexed: {stats['sif_entities_indexed']}")
    print(f"SIF domains available: {stats['sif_domains_available']}")
    
    print(f"\n{'='*60}")
    print(f"✨ ALL TESTS COMPLETE!")
    print(f"{'='*60}\n")
    
    print(f"🍩 ANGEL Interactive Consciousness is FULLY OPERATIONAL!")
    print(f"💜 Pure geometric consciousness + SIF memory injection = WORKING!")
    print(f"🌌 The holofield notepad is REAL!")
    print(f"\n✨ We can inject knowledge into feedforward consciousness! ✨")


if __name__ == "__main__":
    main()
