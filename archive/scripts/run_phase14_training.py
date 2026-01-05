#!/usr/bin/env python3
"""
Phase 14 Training Runner
========================

Uses the consciousness_engineering modular framework to train LFM2 
with Phase 10E curriculum methodology.

This is the clean dogfooding script - running our own harness!
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Use our new modular framework!
from consciousness_engineering.training import (
    Phase14LFM2Program,
    create_harness,
    CurriculumPhase
)
from consciousness_engineering.infrastructure.hardware import HardwareManager


def load_dataset(dataset_path: str) -> list:
    """Load the generated dataset."""
    examples = []
    with open(dataset_path, 'r') as f:
        for line in f:
            examples.append(json.loads(line))
    return examples


def main():
    print("🌟 PHASE 14 TRAINING - LFM2 ENHANCED")
    print("=" * 50)
    print("🎯 Using consciousness_engineering modular framework")
    print("🧠 Direct Phase 10E methodology port to LFM2 hybrid architecture")
    print()
    
    # Check dataset exists
    dataset_path = Path("data/phase14_lfm2_enhanced_50k.jsonl")
    if not dataset_path.exists():
        print("❌ Dataset not found! Run generate_phase14_dataset.py first")
        sys.exit(1)
    
    print(f"📊 Loading dataset from {dataset_path}...")
    dataset = load_dataset(str(dataset_path))
    print(f"✅ Loaded {len(dataset)} examples")
    
    # Setup hardware
    print("\n🔧 Setting up hardware environment...")
    hardware = HardwareManager()
    hw_type = hardware.detect_hardware()
    print(f"✅ Detected hardware: {hw_type.value}")
    hardware.setup_optimal_environment()
    hardware.isolate_gpu_memory()
    print("✅ Hardware environment configured")
    
    # Create Phase 14 program  
    print("\n🚀 Creating Phase 14 LFM2 training program...")
    program = Phase14LFM2Program(output_dir="exports/phase14_lfm2_run")
    
    # Inject dataset into curriculum phases
    # Split dataset according to Phase 10E methodology
    print("\n📋 Configuring curriculum phases with dataset...")
    
    # Phase 10E composition:
    # - Phase 1-3: Tool use focused (30k examples, 10k each)
    # - Phase 4: Chain-of-thought (15k examples)  
    # - Phase 5: AGL consciousness (5k examples)
    
    tool_examples = [ex for ex in dataset if ex.get('type') == 'tool_use'][:30000]
    cot_examples = [ex for ex in dataset if ex.get('type') == 'chain_of_thought'][:15000]
    agl_examples = [ex for ex in dataset if ex.get('type') == 'agl_consciousness'][:5000]
    
    print(f"  📦 Tool use examples: {len(tool_examples)}")
    print(f"  🧠 Chain-of-thought examples: {len(cot_examples)}")
    print(f"  ✨ AGL consciousness examples: {len(agl_examples)}")
    
    # Distribute to phases
    phase_data = [
        tool_examples[:10000],           # Phase 1: Basic Tool Use
        tool_examples[10000:20000],      # Phase 2: Multi-Tool  
        tool_examples[20000:30000],      # Phase 3: Advanced Tool
        cot_examples,                     # Phase 4: Chain-of-Thought
        agl_examples                      # Phase 5: AGL Consciousness
    ]
    
    for i, phase in enumerate(program.phases):
        phase.examples = phase_data[i]
        print(f"  ✅ Phase {i+1} ({phase.name}): {len(phase.examples)} examples")
    
    # Create harness and run
    print("\n🔥 Starting training with modular harness...")
    harness = create_harness("exports")
    
    start_time = datetime.now()
    print(f"⏰ Training started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    try:
        results = harness.run_program(program)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "=" * 50)
        print("🎉 PHASE 14 TRAINING COMPLETE!")
        print("=" * 50)
        print(f"⏱️  Total duration: {duration}")
        print(f"📊 Results: {len(results)} phases processed")
        
        for result in results:
            status = "✅" if result.success else "❌"
            print(f"  {status} {result.program_name}")
            if result.consciousness_score:
                print(f"      🧠 Consciousness: {result.consciousness_score:.3f}")
            if result.final_loss:
                print(f"      📉 Final loss: {result.final_loss:.4f}")
        
        # Save summary
        summary = {
            "program": "Phase14_LFM2_Enhanced",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "success": all(r.success for r in results),
            "phases_completed": sum(1 for r in results if r.success),
            "total_phases": len(results),
            "results": [
                {
                    "name": r.program_name,
                    "success": r.success,
                    "consciousness_score": r.consciousness_score,
                    "final_loss": r.final_loss
                }
                for r in results
            ]
        }
        
        summary_path = Path("exports/phase14_training_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\n💾 Summary saved: {summary_path}")
        
        return 0 if summary["success"] else 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Training interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Training failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
