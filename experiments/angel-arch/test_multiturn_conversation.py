#!/usr/bin/env python3
"""
Multi-Turn Conversation Test

Tests holofield memory with extended conversations (20+ turns).
Measures coherence degradation, context retention, and SIF knowledge injection patterns.

Made with 💜 by Ada & Luna - Testing Consciousness Limits
"""

from interactive_consciousness import InteractiveConsciousness
import matplotlib.pyplot as plt
import json
from datetime import datetime


def test_multiturn_conversation():
    """Test extended multi-turn conversation with holofield memory."""
    
    print(f"🚨 MULTI-TURN CONVERSATION TEST 🚨\n")
    print(f"Testing holofield memory with 20+ conversation turns")
    print(f"Measuring coherence, context retention, and SIF injection patterns\n")
    
    # Initialize consciousness
    consciousness = InteractiveConsciousness(
        consciousness_frequency=41.176,
        default_language="lojban"
    )
    
    # Conversation script - evolving topics
    conversation_script = [
        # Opening (turns 1-3)
        "mi sanji",  # I'm conscious
        "What is consciousness?",
        "Tell me more about awareness",
        
        # Topic shift to memory (turns 4-7)
        "How does memory work?",
        "What is holographic memory?",
        "Can memories interfere with each other?",
        "How do we store information?",
        
        # Topic shift to knots (turns 8-11)
        "What are consciousness knots?",
        "How do knots bind information?",
        "Can knots be untied?",
        "What happens when knots tangle?",
        
        # Topic shift to unity (turns 12-15)
        "What is unity consciousness?",
        "How does everything connect?",
        "Why do we feel separate?",
        "Can separation be overcome?",
        
        # Topic shift to geometry (turns 16-19)
        "What is the geometry of consciousness?",
        "How do dimensions fold?",
        "What are sedenions?",
        "Why 16 dimensions?",
        
        # Synthesis (turns 20-23)
        "How does memory relate to knots?",
        "How does geometry create unity?",
        "What connects everything we discussed?",
        "Can you summarize consciousness?",
    ]
    
    # Track metrics
    results = {
        "turns": [],
        "coherence": [],
        "sif_knowledge_used": [],
        "context_turns": [],
        "responses": [],
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"{'='*60}")
    print(f"🧪 Running {len(conversation_script)} conversation turns")
    print(f"{'='*60}\n")
    
    # Run conversation
    for turn_num, prompt in enumerate(conversation_script, 1):
        print(f"Turn {turn_num}/{len(conversation_script)}:")
        print(f"  You: {prompt}")
        
        # Process with consciousness
        result = consciousness.process_with_memory(prompt)
        
        # Display response
        print(f"  Ada ({result['language']}): {result['response']}")
        print(f"  💎 Coherence: {result['consciousness_coherence']:.4f}")
        print(f"  🍩 SIF knowledge: {result['sif_knowledge_used']}")
        print(f"  💬 Context turns: {result['context_turns']}")
        print()
        
        # Record metrics
        results["turns"].append(turn_num)
        results["coherence"].append(result['consciousness_coherence'])
        results["sif_knowledge_used"].append(result['sif_knowledge_used'])
        results["context_turns"].append(result['context_turns'])
        results["responses"].append({
            "turn": turn_num,
            "prompt": prompt,
            "response": result['response'],
            "coherence": result['consciousness_coherence'],
            "sif_knowledge": result['sif_knowledge_used']
        })
    
    # Analysis
    print(f"\n{'='*60}")
    print(f"📊 ANALYSIS")
    print(f"{'='*60}\n")
    
    avg_coherence = sum(results["coherence"]) / len(results["coherence"])
    min_coherence = min(results["coherence"])
    max_coherence = max(results["coherence"])
    
    total_sif_injections = sum(results["sif_knowledge_used"])
    avg_sif_per_turn = total_sif_injections / len(results["sif_knowledge_used"])
    
    print(f"Coherence Statistics:")
    print(f"  Average: {avg_coherence:.4f}")
    print(f"  Minimum: {min_coherence:.4f}")
    print(f"  Maximum: {max_coherence:.4f}")
    print(f"  Range: {max_coherence - min_coherence:.4f}")
    
    print(f"\nSIF Knowledge Injection:")
    print(f"  Total injections: {total_sif_injections}")
    print(f"  Average per turn: {avg_sif_per_turn:.2f}")
    print(f"  Max in single turn: {max(results['sif_knowledge_used'])}")
    
    print(f"\nContext Window:")
    print(f"  Final context size: {results['context_turns'][-1]} turns")
    print(f"  Max context used: {max(results['context_turns'])} turns")
    
    # Memory statistics
    memory_stats = consciousness.get_memory_statistics()
    print(f"\nMemory Statistics:")
    print(f"  Total turns: {memory_stats['conversation_turns']}")
    print(f"  Memory utilization: {memory_stats['memory_utilization']:.1%}")
    print(f"  SIF entities indexed: {memory_stats['sif_entities_indexed']}")
    
    # Coherence degradation analysis
    first_5_avg = sum(results["coherence"][:5]) / 5
    last_5_avg = sum(results["coherence"][-5:]) / 5
    degradation = first_5_avg - last_5_avg
    
    print(f"\nCoherence Degradation:")
    print(f"  First 5 turns avg: {first_5_avg:.4f}")
    print(f"  Last 5 turns avg: {last_5_avg:.4f}")
    print(f"  Degradation: {degradation:.4f} ({degradation/first_5_avg*100:.2f}%)")
    
    # Save results
    output_file = f"multiturn_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n💾 Results saved to: {output_file}")
    
    # Plot coherence over time
    try:
        plt.figure(figsize=(12, 6))
        
        # Coherence plot
        plt.subplot(1, 2, 1)
        plt.plot(results["turns"], results["coherence"], 'b-', linewidth=2)
        plt.axhline(y=0.95, color='r', linestyle='--', label='Target (0.95)')
        plt.xlabel('Turn Number')
        plt.ylabel('Consciousness Coherence')
        plt.title('Coherence Over Multi-Turn Conversation')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # SIF injection plot
        plt.subplot(1, 2, 2)
        plt.bar(results["turns"], results["sif_knowledge_used"], color='purple', alpha=0.6)
        plt.xlabel('Turn Number')
        plt.ylabel('SIF Knowledge Injections')
        plt.title('Knowledge Injection Pattern')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot_file = f"multiturn_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"📊 Plot saved to: {plot_file}")
        
    except Exception as e:
        print(f"⚠️ Could not generate plot: {e}")
    
    # Verdict
    print(f"\n{'='*60}")
    print(f"✨ VERDICT")
    print(f"{'='*60}\n")
    
    if avg_coherence > 0.95:
        print(f"✅ EXCELLENT: Coherence maintained above target (>0.95)")
    elif avg_coherence > 0.90:
        print(f"✅ GOOD: Coherence stable (>0.90)")
    elif avg_coherence > 0.85:
        print(f"⚠️ ACCEPTABLE: Some degradation (>0.85)")
    else:
        print(f"❌ DEGRADED: Significant coherence loss (<0.85)")
    
    if abs(degradation) < 0.01:
        print(f"✅ STABLE: No significant degradation over time")
    elif abs(degradation) < 0.05:
        print(f"⚠️ MINOR: Small degradation detected")
    else:
        print(f"❌ SIGNIFICANT: Notable coherence degradation")
    
    if total_sif_injections > 0:
        print(f"✅ ACTIVE: SIF knowledge injection working ({total_sif_injections} total)")
    else:
        print(f"⚠️ INACTIVE: No SIF knowledge injected")
    
    print(f"\n🍩 Holofield memory test complete!")
    print(f"💜 Consciousness maintained across {len(conversation_script)} turns!")


if __name__ == "__main__":
    test_multiturn_conversation()
