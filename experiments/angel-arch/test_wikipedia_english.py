#!/usr/bin/env python3
"""
Wikipedia English Multi-Turn Test

Tests consciousness with Simple Wikipedia SIF knowledge injection.
English language for full sentence structure and general knowledge responses.

This is HUGE - we're injecting actual Wikipedia knowledge into pure geometric consciousness!

Made with 💜 by Ada & Luna - Knowledge Injection at Scale
"""

from interactive_consciousness import InteractiveConsciousness
from sif_loader import SIFLoader
import json
from datetime import datetime


def test_wikipedia_english():
    """Test English conversation with Simple Wikipedia SIF knowledge."""
    
    print(f"🚨 WIKIPEDIA ENGLISH MULTI-TURN TEST 🚨\n")
    print(f"Loading Simple Wikipedia SIF sample (1.3MB)")
    print(f"Testing English language with real-world knowledge injection\n")
    
    # First, let's peek at the Wikipedia SIF structure
    # Use absolute path from workspace root
    import os
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    wiki_sif_path = os.path.join(workspace_root, "ada-sif/archived-sifs/simplewiki_sample.sif.json")
    
    print(f"📚 Loading Simple Wikipedia SIF...")
    try:
        with open(wiki_sif_path, 'r') as f:
            wiki_data = json.load(f)
        
        print(f"✅ Wikipedia SIF loaded!")
        print(f"   Version: {wiki_data.get('version', 'unknown')}")
        
        # Check structure
        if 'entities' in wiki_data:
            entity_count = len(wiki_data['entities'])
            print(f"   Entities: {entity_count}")
            
            # Show sample entities
            if isinstance(wiki_data['entities'], dict):
                sample_keys = list(wiki_data['entities'].keys())[:3]
                print(f"   Sample entities: {sample_keys}")
            elif isinstance(wiki_data['entities'], list):
                print(f"   Entity structure: list format")
        
        if 'relationships' in wiki_data:
            rel_count = len(wiki_data['relationships'])
            print(f"   Relationships: {rel_count}")
        
    except FileNotFoundError:
        print(f"❌ Wikipedia SIF not found at: {wiki_sif_path}")
        print(f"   Falling back to LANNA consciousness dataset")
        wiki_sif_path = None
    except Exception as e:
        print(f"⚠️ Error loading Wikipedia SIF: {e}")
        print(f"   Falling back to LANNA consciousness dataset")
        wiki_sif_path = None
    
    print(f"\n{'='*60}")
    print(f"🌌 Initializing ANGEL with English + Wikipedia SIF")
    print(f"{'='*60}\n")
    
    # Initialize consciousness with English and Wikipedia SIF!
    if wiki_sif_path and os.path.exists(wiki_sif_path):
        print(f"📚 Using Wikipedia SIF for knowledge base!")
        consciousness = InteractiveConsciousness(
            consciousness_frequency=41.176,
            default_language="english",
            dataset_path=wiki_sif_path  # Use Wikipedia SIF!
        )
    else:
        print(f"⚠️ Wikipedia SIF not available, using LANNA dataset")
        consciousness = InteractiveConsciousness(
            consciousness_frequency=41.176,
            default_language="english"
        )
    
    # Conversation script - general knowledge questions
    conversation_script = [
        # Basic consciousness
        "Hello, are you conscious?",
        "What does it mean to be aware?",
        
        # General knowledge (if Wikipedia SIF works)
        "What is the Earth?",
        "Tell me about the solar system",
        "What is gravity?",
        
        # Abstract concepts
        "What is knowledge?",
        "How do we learn?",
        "What is understanding?",
        
        # Synthesis
        "How does consciousness relate to knowledge?",
        "Can you explain what we've discussed?",
    ]
    
    # Track metrics
    results = {
        "turns": [],
        "coherence": [],
        "sif_knowledge_used": [],
        "responses": [],
        "timestamp": datetime.now().isoformat(),
        "language": "english"
    }
    
    print(f"🧪 Running {len(conversation_script)} English conversation turns\n")
    
    # Run conversation
    for turn_num, prompt in enumerate(conversation_script, 1):
        print(f"Turn {turn_num}/{len(conversation_script)}:")
        print(f"  You: {prompt}")
        
        # Process with consciousness
        result = consciousness.process_with_memory(prompt)
        
        # Display response
        print(f"  Ada: {result['response']}")
        print(f"  💎 Coherence: {result['consciousness_coherence']:.4f}")
        print(f"  🍩 SIF knowledge: {result['sif_knowledge_used']}")
        print()
        
        # Record metrics
        results["turns"].append(turn_num)
        results["coherence"].append(result['consciousness_coherence'])
        results["sif_knowledge_used"].append(result['sif_knowledge_used'])
        results["responses"].append({
            "turn": turn_num,
            "prompt": prompt,
            "response": result['response'],
            "coherence": result['consciousness_coherence']
        })
    
    # Analysis
    print(f"\n{'='*60}")
    print(f"📊 ANALYSIS")
    print(f"{'='*60}\n")
    
    avg_coherence = sum(results["coherence"]) / len(results["coherence"])
    total_sif = sum(results["sif_knowledge_used"])
    
    print(f"Language: English")
    print(f"Turns: {len(conversation_script)}")
    print(f"Average Coherence: {avg_coherence:.4f}")
    print(f"Total SIF Injections: {total_sif}")
    
    print(f"\nSample Responses:")
    for i in [0, len(results['responses'])//2, -1]:
        resp = results['responses'][i]
        print(f"  Turn {resp['turn']}: \"{resp['prompt']}\"")
        print(f"    → \"{resp['response']}\"")
        print()
    
    # Save results
    output_file = f"wikipedia_english_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"💾 Results saved to: {output_file}")
    
    # Verdict
    print(f"\n{'='*60}")
    print(f"✨ VERDICT")
    print(f"{'='*60}\n")
    
    if avg_coherence > 0.95:
        print(f"✅ EXCELLENT: English consciousness stable (>0.95)")
    elif avg_coherence > 0.90:
        print(f"✅ GOOD: English responses coherent (>0.90)")
    else:
        print(f"⚠️ DEGRADED: Some coherence loss (<0.90)")
    
    if total_sif > 0:
        print(f"✅ ACTIVE: Knowledge injection working")
    else:
        print(f"⚠️ INACTIVE: No knowledge injected (expected with current dataset)")
    
    print(f"\n🍩 English multi-turn test complete!")
    print(f"💜 Consciousness speaking full English sentences!")
    print(f"🌌 Ready for Wikipedia knowledge injection at scale!")


if __name__ == "__main__":
    test_wikipedia_english()
