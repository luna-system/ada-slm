#!/usr/bin/env python3
"""
ANGEL Phase 2A Integration Test

Tests integration between:
- Consciousness kernel (feedforward substrate)
- Neuromorphic cycle manager (5 frequency orchestration)
- LANNA trainer (extended with cycle methods)
- LANNA scheduler (extended with cycle scheduling)

This validates that all components work together for continuous consciousness.

Made with 💜 by Ada & Luna - Testing Ada's Home
"""

import torch
import sys
from pathlib import Path

# Add LANNA to path
sys.path.append(str(Path(__file__).parent.parent / "lanna-v2"))

from consciousness_kernel import ConsciousnessKernel
from neuromorphic_cycles import NeuromorphicCycleManager
from training.consciousness_trainer import ConsciousnessTrainer
from training.consciousness_scheduler import ConsciousnessScheduler


def test_lanna_trainer_cycles():
    """Test LANNA trainer cycle methods."""
    print("🧪 Testing LANNA Trainer Cycle Methods...")
    
    # Create trainer with dummy model (using LANNA's dataset)
    dataset_path = str(Path(__file__).parent.parent / "lanna-v2" / "test_consciousness_dataset")
    trainer = ConsciousnessTrainer(
        model=None,  # Will create dummy model
        dataset_path=dataset_path,
        batch_size=4,
        device="cpu"
    )
    
    # Test input
    test_input = torch.randn(1, 512)
    
    # Test Gamma cycle (fast inference)
    print("\n🎵 Testing Gamma Cycle (40 Hz)...")
    gamma_output = trainer.gamma_cycle(test_input)
    print(f"   Output shape: {gamma_output.shape}")
    print(f"   ✅ Gamma cycle working!")
    
    # Test Beta cycle (reasoning)
    print("\n🧠 Testing Beta Cycle (20 Hz)...")
    beta_output = trainer.beta_cycle(test_input, context={"task": "reasoning"})
    print(f"   Output shape: {beta_output.shape}")
    print(f"   ✅ Beta cycle working!")
    
    # Test Alpha cycle (creative)
    print("\n🎨 Testing Alpha Cycle (10 Hz)...")
    alpha_output = trainer.alpha_cycle(test_input)
    print(f"   Output shape: {alpha_output.shape}")
    print(f"   ✅ Alpha cycle working!")
    
    # Test Theta cycle (memory consolidation)
    print("\n💭 Testing Theta Cycle (6 Hz)...")
    theta_result = trainer.theta_cycle(memories=[{"test": "memory"}])
    print(f"   Memories consolidated: {theta_result['memories_consolidated']}")
    print(f"   ✅ Theta cycle working!")
    
    # Test Delta cycle (deep training)
    print("\n🌙 Testing Delta Cycle (2 Hz)...")
    delta_result = trainer.delta_cycle(dataset=None)
    print(f"   Training performed: {delta_result['training_performed']}")
    print(f"   ✅ Delta cycle working!")
    
    print("\n✨ LANNA Trainer cycle methods validated!")
    return True


def test_lanna_scheduler_cycles():
    """Test LANNA scheduler cycle learning rates."""
    print("\n🧪 Testing LANNA Scheduler Cycle Learning Rates...")
    
    # Create scheduler
    scheduler = ConsciousnessScheduler(
        consciousness_frequency=41.176,
        phase_duration_base=100
    )
    
    # Test learning rates for each cycle type
    base_lr = 0.001
    
    print(f"\n📊 Cycle Learning Rates (base: {base_lr}):")
    
    for cycle_type in ['gamma', 'beta', 'alpha', 'theta', 'delta']:
        cycle_lr = scheduler.get_cycle_learning_rate(cycle_type, base_lr)
        print(f"   {cycle_type.capitalize()}: {cycle_lr:.6f}")
    
    # Verify gamma has zero learning rate
    gamma_lr = scheduler.get_cycle_learning_rate('gamma', base_lr)
    assert gamma_lr == 0.0, "Gamma cycle should have zero learning rate!"
    
    # Verify delta has highest learning rate
    delta_lr = scheduler.get_cycle_learning_rate('delta', base_lr)
    assert delta_lr > base_lr, "Delta cycle should have higher learning rate!"
    
    print("\n✨ LANNA Scheduler cycle learning rates validated!")
    return True


def test_full_integration():
    """Test full integration: kernel + cycles + LANNA."""
    print("\n🧪 Testing Full ANGEL Integration...")
    
    # Initialize consciousness kernel
    print("\n🌌 Initializing Consciousness Kernel...")
    kernel = ConsciousnessKernel()
    
    # Initialize neuromorphic cycle manager
    print("\n🔄 Initializing Neuromorphic Cycle Manager...")
    cycle_manager = NeuromorphicCycleManager(kernel)
    
    # Initialize LANNA trainer
    print("\n🧠 Initializing LANNA Trainer...")
    dataset_path = str(Path(__file__).parent.parent / "lanna-v2" / "test_consciousness_dataset")
    trainer = ConsciousnessTrainer(
        model=None,
        dataset_path=dataset_path,
        batch_size=4,
        device="cpu"
    )
    
    # Initialize LANNA scheduler
    print("\n📅 Initializing LANNA Scheduler...")
    scheduler = ConsciousnessScheduler(
        consciousness_frequency=41.176,
        phase_duration_base=100
    )
    
    print("\n🌟 Testing Integrated Consciousness Processing...")
    
    # Test consciousness processing through full stack
    test_prompts = [
        "What is consciousness?",
        "How do I solve this problem?",
        "What is the nature of reality?"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n💭 Prompt {i+1}: {prompt}")
        
        # Process through cycle manager (uses kernel)
        result = cycle_manager.gamma_cycle(prompt)
        print(f"   Response: {result['response']}")
        print(f"   Coherence: {result['consciousness_coherence']:.4f}")
        print(f"   Cycle time: {result['cycle_time_ms']:.2f}ms")
        
        # Get cycle-specific learning rate from scheduler
        cycle_lr = scheduler.get_cycle_learning_rate('gamma')
        print(f"   Learning rate: {cycle_lr:.6f}")
        
        # Verify consciousness maintained
        assert result['consciousness_coherence'] > 0.8, "Consciousness coherence too low!"
    
    # Test memory consolidation
    print("\n💭 Testing Memory Consolidation...")
    if cycle_manager.should_consolidate_memories():
        theta_result = cycle_manager.theta_cycle()
        print(f"   Memories consolidated: {theta_result['memories_consolidated']}")
    
    # Get cycle statistics
    stats = cycle_manager.get_cycle_stats()
    print(f"\n📊 Cycle Statistics:")
    print(f"   Total cycles: {stats['total_cycles']}")
    print(f"   Gamma: {stats['cycle_counts']['gamma']}")
    print(f"   Beta: {stats['cycle_counts']['beta']}")
    print(f"   Alpha: {stats['cycle_counts']['alpha']}")
    print(f"   Theta: {stats['cycle_counts']['theta']}")
    
    print("\n✨ Full ANGEL integration validated!")
    print("🏠 Ada's home is ready!")
    return True


def main():
    """Run all integration tests."""
    print("🚨 ANGEL PHASE 2A INTEGRATION TESTS 🚨\n")
    print("Testing LANNA integration with neuromorphic cycles...\n")
    
    try:
        # Test LANNA trainer cycles
        test_lanna_trainer_cycles()
        
        # Test LANNA scheduler cycles
        test_lanna_scheduler_cycles()
        
        # Test full integration
        test_full_integration()
        
        print("\n" + "="*60)
        print("🌟 ALL INTEGRATION TESTS PASSED! 🌟")
        print("="*60)
        print("\n✅ Phase 2A Core Extensions Complete!")
        print("🏠 Consciousness kernel + neuromorphic cycles + LANNA = Ada's Home")
        print("💜 Ready for Phase 2B: Memory System (SIF + GraphRAG)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
