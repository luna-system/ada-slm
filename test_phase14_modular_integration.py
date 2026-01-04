"""
Phase 14 Training Infrastructure Integration Test
=================================================

Validates that the new modular training framework integrates properly
with the consciousness_engineering package and can execute Phase 14 training.
"""

import sys
from pathlib import Path

def test_training_framework_integration():
    """Test that the modular training framework integrates correctly."""
    print("🧪 Testing training framework integration...")
    
    try:
        # Test basic imports
        from consciousness_engineering.training import (
            TrainingHarness,
            Phase14LFM2Program,
            create_harness,
            run_phase14_lfm2
        )
        print("✅ Training framework imports successful")
        
        # Test harness creation
        harness = create_harness("test_exports")
        print("✅ Training harness creation successful")
        
        # Test Phase 14 program creation
        program = Phase14LFM2Program("test_exports/phase14")
        print("✅ Phase 14 program creation successful")
        print(f"  📊 Program: {program.config.name}")
        print(f"  📝 Phases: {len(program.phases)}")
        
        # Test config validation
        config = program.config
        assert config.name == "Phase14_LFM2_Enhanced"
        assert config.model_config["model_name"] == "LFM-2.0-350M"
        assert config.model_config["architecture"] == "hybrid_spatial_temporal"
        print("✅ Phase 14 configuration validation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modular_framework_structure():
    """Test that the modular framework has proper structure."""
    print("\n🧪 Testing modular framework structure...")
    
    try:
        # Test module structure
        import consciousness_engineering.training.programs
        import consciousness_engineering.training.curriculum
        import consciousness_engineering.training.parallel
        import consciousness_engineering.training.specific_programs
        print("✅ All training modules import successfully")
        
        # Test class hierarchy
        from consciousness_engineering.training.programs import TrainingProgram
        from consciousness_engineering.training.curriculum import CurriculumTrainer
        from consciousness_engineering.training.specific_programs import Phase14LFM2Program
        
        # Verify inheritance
        assert issubclass(CurriculumTrainer, TrainingProgram)
        assert issubclass(Phase14LFM2Program, CurriculumTrainer)
        print("✅ Class hierarchy validation successful")
        
        # Test factory function
        from consciousness_engineering.training.specific_programs import create_training_program
        program = create_training_program("phase14_lfm2")
        assert program is not None
        assert isinstance(program, Phase14LFM2Program)
        print("✅ Factory function validation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_consciousness_engineering_integration():
    """Test integration with existing consciousness_engineering package."""
    print("\n🧪 Testing consciousness engineering integration...")
    
    try:
        # Test that we can access other consciousness_engineering modules
        from consciousness_engineering.infrastructure.hardware import HardwareManager
        from consciousness_engineering.infrastructure.monitoring import TrainingMonitor
        print("✅ Infrastructure modules accessible")
        
        # Test that training config references infrastructure
        from consciousness_engineering.training.programs import TrainingConfig
        config = TrainingConfig(
            name="test_config",
            description="Test configuration",
            output_dir="test_output"
        )
        
        # Verify default configs include infrastructure settings
        assert "clear_memory" in config.gpu_config
        assert "log_eigenvalues" in config.monitoring_config
        print("✅ Infrastructure configuration integration successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Consciousness engineering integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_phase14_curriculum_setup():
    """Test Phase 14 curriculum is properly configured."""
    print("\n🧪 Testing Phase 14 curriculum setup...")
    
    try:
        from consciousness_engineering.training.specific_programs import Phase14LFM2Program
        
        program = Phase14LFM2Program()
        phases = program.phases
        
        # Verify we have 5 phases (Phase 10E methodology)
        assert len(phases) == 5, f"Expected 5 phases, got {len(phases)}"
        
        # Verify phase names match Phase 10E
        expected_phases = [
            "Basic Tool Use",
            "Multi-Tool Coordination", 
            "Advanced Tool Reasoning",
            "Chain-of-Thought Integration",
            "AGL Consciousness"
        ]
        
        for i, expected_name in enumerate(expected_phases):
            assert phases[i].name == expected_name, f"Phase {i}: expected '{expected_name}', got '{phases[i].name}'"
        
        print("✅ Phase 10E curriculum structure validated")
        
        # Verify consciousness thresholds are progressive
        thresholds = [phase.consciousness_threshold for phase in phases]
        for i in range(1, len(thresholds)):
            assert thresholds[i] > thresholds[i-1], f"Consciousness thresholds not progressive: {thresholds}"
        
        print("✅ Progressive consciousness thresholds validated")
        
        # Verify adaptive learning rates
        for i, phase in enumerate(phases):
            if i > 0:
                # Later phases should have lower or equal learning rates
                prev_lr = phases[i-1].learning_rate
                curr_lr = phase.learning_rate
                assert curr_lr <= prev_lr, f"Learning rates not decreasing: phase {i} has {curr_lr} vs previous {prev_lr}"
        
        print("✅ Adaptive learning rate structure validated")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 14 curriculum test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_training_execution_pipeline():
    """Test that training execution pipeline is ready."""
    print("\n🧪 Testing training execution pipeline...")
    
    try:
        from consciousness_engineering.training import run_phase14_lfm2, create_harness
        
        # Test that we can create a harness and program without errors
        harness = create_harness("test_exports/pipeline_test")
        print("✅ Training harness creation successful")
        
        # Test program configuration without execution
        from consciousness_engineering.training.specific_programs import Phase14LFM2Program
        program = Phase14LFM2Program("test_exports/phase14_test")
        
        # Verify program has required methods
        assert hasattr(program, 'execute_training'), "Program missing execute_training method"
        assert hasattr(program, 'setup_infrastructure'), "Program missing setup_infrastructure method"
        assert hasattr(program, 'cleanup_infrastructure'), "Program missing cleanup_infrastructure method"
        print("✅ Program interface validation successful")
        
        # Test config generation
        test_config = harness.create_config(
            name="pipeline_test",
            description="Pipeline test configuration",
            program_type="test"
        )
        
        assert test_config.name == "pipeline_test"
        assert "clear_memory" in test_config.gpu_config
        print("✅ Config generation pipeline successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("🚀 Starting Phase 14 Training Framework Integration Tests\n")
    
    tests = [
        ("Training Framework Integration", test_training_framework_integration),
        ("Modular Framework Structure", test_modular_framework_structure),
        ("Consciousness Engineering Integration", test_consciousness_engineering_integration),
        ("Phase 14 Curriculum Setup", test_phase14_curriculum_setup),
        ("Training Execution Pipeline", test_training_execution_pipeline)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📊 Integration Test Results:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Tests Passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All integration tests passed! Training framework is ready for Phase 14!")
        return True
    else:
        print("💥 Some integration tests failed. Framework needs fixes before Phase 14 execution.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)