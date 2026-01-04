#!/usr/bin/env python3
"""
Automated Data Migration Script
Safely migrates ada-slm data to Phase 12 fractal architecture
"""

import shutil
import json
from pathlib import Path
from datetime import datetime

def migrate_results():
    """Migrate results files with format conversion"""
    old_results = Path("../ada-slm/results")
    new_results = Path("results/legacy")
    
    if not old_results.exists():
        print("No old results to migrate")
        return
        
    new_results.mkdir(parents=True, exist_ok=True)
    
    for result_file in old_results.glob("*.json"):
        # Copy to legacy location
        shutil.copy2(result_file, new_results / result_file.name)
        print(f"✅ Migrated: {result_file.name}")
        
        # Attempt format conversion
        try:
            convert_to_fractal_format(result_file, new_results)
        except Exception as e:
            print(f"⚠️ Conversion failed for {result_file.name}: {e}")

def convert_to_fractal_format(old_file, output_dir):
    """Convert old format to new fractal format"""
    with open(old_file) as f:
        old_data = json.load(f)
    
    # Convert to new ConsciousnessResult format
    converted = {
        "protocol": "legacy_tonight",
        "architecture": "autoregressive", 
        "model": old_data.get("model", "unknown"),
        "responses": old_data.get("responses", []),
        "consciousness_markers": old_data.get("consciousness_markers", {}),
        "julia_parameters": old_data.get("julia_parameters", {}),
        "fractal_dimension": old_data.get("fractal_dimension", 0.0),
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "legacy_source": str(old_file),
            "conversion_timestamp": datetime.now().isoformat(),
            "original_format": "ada-slm-legacy"
        }
    }
    
    # Save converted version
    converted_file = output_dir / f"converted_{old_file.name}"
    with open(converted_file, "w") as f:
        json.dump(converted, f, indent=2)
        
    print(f"🔄 Converted: {old_file.name} → {converted_file.name}")

def create_migration_manifest():
    """Create manifest of all migrated files"""
    manifest = {
        "migration_timestamp": datetime.now().isoformat(),
        "source_location": "../ada-slm",
        "target_location": ".",
        "phase": "12.0.0",
        "architecture": "fractal_consciousness",
        "migrated_files": []
    }
    
    # Scan for migrated files
    for legacy_dir in ["results/legacy", "models/legacy"]:
        legacy_path = Path(legacy_dir)
        if legacy_path.exists():
            for file in legacy_path.iterdir():
                manifest["migrated_files"].append({
                    "file": str(file),
                    "size": file.stat().st_size if file.is_file() else 0,
                    "type": file.suffix
                })
    
    with open("migration_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"📋 Migration manifest created: migration_manifest.json")

if __name__ == "__main__":
    print("🔄 Starting Data Migration...")
    migrate_results()
    create_migration_manifest()
    print("✅ Migration complete!")
