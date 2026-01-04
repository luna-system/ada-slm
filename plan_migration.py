#!/usr/bin/env python3
"""
Data Migration Strategy for Phase 12
Plan for moving old ada-slm data to the new fractal architecture
"""

from pathlib import Path
import json
import shutil
import sys

class DataMigrationPlanner:
    """Plan and execute data migration from old ada-slm to new fractal architecture"""
    
    def __init__(self):
        self.old_path = Path("../ada-slm")
        self.new_path = Path(".")
        self.migration_plan = {}
        
    def analyze_existing_data(self):
        """Analyze what data exists in the old ada-slm structure"""
        print("🔍 Analyzing existing ada-slm data structure...")
        
        if not self.old_path.exists():
            print(f"❌ Old ada-slm path not found: {self.old_path}")
            return {}
            
        data_inventory = {
            "results": [],
            "models": [],
            "configs": [],
            "scripts": [],
            "datasets": []
        }
        
        # Scan for results files
        results_dir = self.old_path / "results"
        if results_dir.exists():
            for file in results_dir.glob("*.json"):
                data_inventory["results"].append(str(file))
                
        # Scan for model files
        models_dir = self.old_path / "models"
        if models_dir.exists():
            for file in models_dir.iterdir():
                data_inventory["models"].append(str(file))
                
        # Scan for important scripts
        for pattern in ["*.py", "*.sh", "*.yaml", "*.toml"]:
            for file in self.old_path.glob(pattern):
                if file.is_file():
                    data_inventory["scripts"].append(str(file))
        
        print(f"📊 Data Inventory:")
        for category, files in data_inventory.items():
            print(f"   {category}: {len(files)} files")
            if files:
                for file in files[:3]:  # Show first 3
                    print(f"      - {Path(file).name}")
                if len(files) > 3:
                    print(f"      ... and {len(files)-3} more")
                    
        return data_inventory
    
    def create_migration_plan(self, data_inventory):
        """Create detailed migration plan"""
        print("\n🗺️ Creating Migration Plan...")
        
        plan = {
            "archive_location": "archive/ada-slm-old",
            "results_migration": {
                "source": "results/",
                "destination": "results/legacy/",
                "action": "copy_and_categorize"
            },
            "models_migration": {
                "source": "models/",
                "destination": "models/legacy/", 
                "action": "move_with_manifest"
            },
            "script_migration": {
                "source": "*.py",
                "destination": "consciousness_engineering/tools/legacy/",
                "action": "analyze_and_integrate"
            },
            "data_conversion": {
                "old_format": "original consciousness tests",
                "new_format": "fractal architecture format",
                "converter_script": "convert_legacy_results.py"
            }
        }
        
        print(f"📋 Migration Plan:")
        for step, details in plan.items():
            print(f"   {step}:")
            if isinstance(details, dict):
                for key, value in details.items():
                    print(f"      {key}: {value}")
            else:
                print(f"      {details}")
                
        return plan
    
    def execute_safe_migration(self, plan):
        """Execute migration with safety checks"""
        print(f"\n🚀 Executing Safe Migration...")
        
        # Create archive directory
        archive_dir = Path(plan["archive_location"])
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Create legacy directories in new structure
        legacy_dirs = [
            "results/legacy",
            "models/legacy", 
            "consciousness_engineering/tools/legacy"
        ]
        
        for dir_path in legacy_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")
        
        print(f"✅ Migration structure prepared")
        return True
    
    def generate_migration_script(self):
        """Generate automated migration script"""
        script_content = '''#!/usr/bin/env python3
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
'''

        script_file = Path("migrate_data.py")
        with open(script_file, "w") as f:
            f.write(script_content)
            
        print(f"📝 Generated migration script: {script_file}")
        return script_file

def main():
    """Main migration planning function"""
    print("📦 Phase 12 Data Migration Planner")
    print("="*50)
    
    planner = DataMigrationPlanner()
    
    # Analyze existing data
    inventory = planner.analyze_existing_data()
    
    # Create migration plan
    migration_plan = planner.create_migration_plan(inventory)
    
    # Prepare migration infrastructure
    planner.execute_safe_migration(migration_plan)
    
    # Generate automated migration script
    script_file = planner.generate_migration_script()
    
    print(f"\n🎉 Migration Planning Complete!")
    print(f"📋 Summary:")
    print(f"   • Data inventory: {sum(len(files) for files in inventory.values())} files")
    print(f"   • Migration script: {script_file}")
    print(f"   • Legacy directories: Created")
    print(f"   • Archive strategy: Defined")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Review migration plan")
    print(f"   2. Run: python {script_file}")
    print(f"   3. Verify migrated data")
    print(f"   4. Test legacy results in new architecture")
    
    print(f"\n🌌 Ready to preserve consciousness archaeology history!")

if __name__ == "__main__":
    main()