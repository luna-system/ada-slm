#!/usr/bin/env python3
"""
Phase 14 Test Script
===================

Quick test of Phase 14 LFM2 training infrastructure:
- GPU setup validation
- Harness configuration test  
- LFM2 model loading test
- Dataset generation test
"""

import sys
from pathlib import Path

# Add harness to path
sys.path.append(str(Path(__file__).parent))

def test_gpu_setup():
    """Test GPU environment setup."""
    print("🔧 Testing GPU setup...")
    
    try:
        from harness.gpu import GPUManager
        
        gpu_manager = GPUManager()
        memory_stats = gpu_manager.get_memory_stats() 
        print(f"✅ GPU accessible: {memory_stats}")
        return True
        
    except Exception as e:
        print(f"❌ GPU setup failed: {e}")
        return False

def test_harness_config():
    """Test harness configuration system."""
    print("⚙️  Testing harness configuration...")
    
    try:
        from harness.config import HarnessConfig
        
        config = HarnessConfig(
            name="test_phase14_lfm2",
            model={
                "base_model": "LiquidAI/LFM2-350M",
                "architecture": "hybrid"
            },
            training={
                "num_train_epochs": 0.1,  # Minimal test
                "output_dir": "test_output"
            }
        )
        
        print(f"✅ Config created: {config.name}")
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_lfm2_model():
    """Test LFM2 model loading."""
    print("🤖 Testing LFM2 model loading...")
    
    try:
        from transformers import AutoTokenizer
        
        # Test tokenizer loading first (lighter weight)
        tokenizer = AutoTokenizer.from_pretrained(
            "LiquidAI/LFM2-350M", 
            trust_remote_code=True
        )
        
        print(f"✅ LFM2 tokenizer loaded: vocab size {tokenizer.vocab_size}")
        print("⚠️  Model loading test skipped (heavy - will test during training)")
        return True
        
    except Exception as e:
        print(f"❌ LFM2 test failed: {e}")
        print("💡 This might be expected if LFM2 isn't available yet")
        return False

def test_dataset_generation():
    """Test dataset generation system."""
    print("📊 Testing dataset generation...")
    
    try:
        from generate_phase14_dataset import Phase14DatasetGenerator
        
        generator = Phase14DatasetGenerator()
        
        # Test small sample generation
        tool_examples = generator.generate_tool_use_examples(count=3)
        cot_examples = generator.generate_chain_of_thought_examples(count=2)  
        agl_examples = generator.generate_agl_consciousness_examples(count=1)
        
        print(f"✅ Generated samples: {len(tool_examples)} tool, {len(cot_examples)} CoT, {len(agl_examples)} AGL")
        
        # Verify example structure
        for ex in tool_examples[:1]:
            print(f"📝 Sample tool example: {len(ex['messages'])} messages, type: {ex['type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dataset generation test failed: {e}")
        return False

def test_curriculum_trainer():
    """Test curriculum trainer initialization."""
    print("🎓 Testing curriculum trainer...")
    
    try:
        from train_phase14_lfm2_enhanced import LFM2CurriculumTrainer, PHASE14_CURRICULUM
        
        trainer = LFM2CurriculumTrainer(output_dir="test_output")
        
        print(f"✅ Trainer initialized: {len(PHASE14_CURRICULUM)} curriculum phases")
        
        # Test configuration generation
        phase = PHASE14_CURRICULUM[0]
        config = trainer.create_phase_config(phase)
        
        print(f"📋 Phase config generated: {config.name}")
        print(f"🎯 Target model: {config.model['base_model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Curriculum trainer test failed: {e}")
        return False

def main():
    """Run all Phase 14 tests."""
    
    print("🧪 PHASE 14 INFRASTRUCTURE TEST")
    print("🎯 Validating LFM2 curriculum training setup")
    
    tests = [
        ("GPU Setup", test_gpu_setup),
        ("Harness Config", test_harness_config),
        ("LFM2 Model", test_lfm2_model),
        ("Dataset Generation", test_dataset_generation),
        ("Curriculum Trainer", test_curriculum_trainer)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print(f"\n🎯 PHASE 14 TEST SUMMARY")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n🏆 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Phase 14 infrastructure is ready!")
        print("🚀 Next steps:")
        print("  1. Generate dataset: python generate_phase14_dataset.py")
        print("  2. Run training: python train_phase14_lfm2_enhanced.py")
    else:
        print("⚠️  Some tests failed - please address issues before training")


if __name__ == "__main__":
    main()