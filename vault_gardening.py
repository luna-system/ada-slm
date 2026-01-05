#!/usr/bin/env python3
"""
Ada-SLM Vault Gardening - Organize training artifacts and cleanup.
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_training_artifacts():
    """Organize ada-slm training artifacts for better vault management."""
    
    print("🌱 Ada-SLM Vault Gardening Starting...")
    
    # Create archive directories
    archive_dir = Path("archive")
    archive_dir.mkdir(exist_ok=True)
    
    (archive_dir / "logs").mkdir(exist_ok=True)
    (archive_dir / "scripts").mkdir(exist_ok=True)
    (archive_dir / "experiments").mkdir(exist_ok=True)
    
    # Move completed experiment logs to archive
    log_files = [
        "phase14_training.log",
        "v9b_pure_training.log", 
        "v9c_capacity_training.log",
        "v9d_isolation_training.log",
        "v9d_training_run2.log",
        "v9d_eval.log",
        "v9e_aggressive_training.log",
        "v9e_evaluation.log", 
        "v9e_proper_training.log",
        "v9f_polyglot_base_test.log",
        "v9f_polyglot_v9c_test.log"
    ]
    
    for log_file in log_files:
        if Path(log_file).exists():
            shutil.move(log_file, archive_dir / "logs" / log_file)
            print(f"📦 Archived: {log_file}")
    
    # Archive old training scripts (keep current v9g for reference)
    training_scripts = [
        "run_phase14_training.py",
        "run_phase14_real_training.py", 
        "train_phase14_lfm2_enhanced.py",
        "train_v9b_pure.py",
        "train_v9c_capacity.py",
        "train_v9d_isolation.py",
        "train_v9e_aggressive.py",
        "train_v9e_aggressive_fixed.py",
        "train_v9e_aggressive_proper.py",
        "train_v9e_from_v9c.py",
        "train_v9f_polyglot_base.py",
        "train_v9f_polyglot_v9c.py"
    ]
    
    for script in training_scripts:
        if Path(script).exists():
            shutil.move(script, archive_dir / "scripts" / script)
            print(f"📦 Archived: {script}")
    
    # Move analysis/test scripts
    analysis_scripts = [
        "analyze_v9a_eigenvalues.py",
        "quick_v9a_inference.py", 
        "test_v9a_vs_baseline.py",
        "test_v9b_import.py",
        "test_v9b_multilang.py",
        "test_phase14_infrastructure.py",
        "test_phase14_modular_integration.py",
        "test_real_models.py",
        "visualize_results.py"
    ]
    
    for script in analysis_scripts:
        if Path(script).exists():
            shutil.move(script, archive_dir / "experiments" / script)
            print(f"🧪 Archived analysis: {script}")
    
    # Create a README for the archive
    readme_content = f"""# Ada-SLM Archive
    
Organized on: {datetime.now().isoformat()}

## Structure

- `logs/` - Training run logs from v9 experimental series
- `scripts/` - Historical training scripts (Phase 14, v9a-v9f)  
- `experiments/` - Analysis and testing utilities

## Active Files (Not Archived)

- `train_v9g_curriculum.py` - Phase 14F curriculum learning (current)
- `train_v9g_curriculum_fixed.py` - Fixed version for messages format
- `consciousness_engineering/` - Core framework (v12.0.0)
- `data/` - Training datasets
- `exports/` - Model artifacts
- `results/` - Evaluation results

## Notes

All archived experiments contributed to the Goldilocks Zone discovery:
- r=32, α=64, batch=1 
- Tonight Protocol emergence threshold: 0.0200
- Polyglot/AGL interference patterns documented in Phase 14F

The v9 series established the foundation for curriculum learning approach.
"""
    
    with open(archive_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"📚 Created archive README")
    
    # Summary
    print("\n✨ Vault Gardening Complete!")
    print(f"📁 Archive created at: {archive_dir.absolute()}")
    print(f"🗂️  Logs archived: {len(log_files)} files")
    print(f"🐍 Scripts archived: {len(training_scripts)} files")
    print(f"🔬 Analysis archived: {len(analysis_scripts)} files")
    
    print("\n🚀 Active workspace now focused on:")
    print("  - train_v9g_curriculum_fixed.py (ready to run)")
    print("  - consciousness_engineering/ framework")
    print("  - Clean exports/ and results/ structure")
    
    return True

if __name__ == "__main__":
    organize_training_artifacts()