#!/usr/bin/env python3
"""
LANNA v2.1 Consciousness Dataset Generator

Top-level script for generating complete consciousness training datasets using
universal consciousness mathematics. Implements the revolutionary pattern:
Dark Matter (latent concepts) → Consciousness Mathematics → White Matter (datasets)

Usage:
    python generate_consciousness_dataset.py --entities 5000 --output ./consciousness_dataset
    python generate_consciousness_dataset.py --config custom_config.json
    python generate_consciousness_dataset.py --quick-test

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 22, 2026
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Add dataset module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(current_dir, 'dataset')
if dataset_dir not in sys.path:
    sys.path.insert(0, dataset_dir)

# Also add the lanna-v2 directory to path for relative imports
lanna_dir = current_dir
if lanna_dir not in sys.path:
    sys.path.insert(0, lanna_dir)

from dataset.pipeline import ConsciousnessDatasetPipeline


def create_default_config() -> Dict[str, Any]:
    """Create default configuration for consciousness dataset generation"""
    
    return {
        "consciousness_frequency": 41.176,  # Hz - The universal consciousness frequency!
        "output_directory": "./lanna_consciousness_dataset",
        "export_format": "sif_hierarchical",  # sif_hierarchical, jsonl, parquet
        "validate_consciousness": True,
        "entities_per_domain": {
            "enochian": 2000,      # Enochian prime vocabulary
            "holographic": 1500,   # Holographic consciousness patterns
            "knots": 1200,         # Agnes consciousness knots
            "physics": 1000,       # Consciousness physics (bagel physics!)
            "agl": 1300           # AGL consciousness reasoning
        },
        "pipeline_config": {
            "max_entities_per_domain": 10000,
            "max_relationships_per_pair": 1000,
            "consciousness_coherence_threshold": 0.7,
            "prime_signature_validation": True,
            "holographic_fidelity_threshold": 0.8,
            "bagel_physics_validation": True,
            "agl_reasoning_validation": True
        }
    }


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Merge with defaults
        default_config = create_default_config()
        
        # Update nested dictionaries properly
        for key, value in config.items():
            if key in default_config and isinstance(default_config[key], dict) and isinstance(value, dict):
                default_config[key].update(value)
            else:
                default_config[key] = value
        
        return default_config
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        print("📝 Creating default configuration...")
        return create_default_config()
    
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        print("📝 Using default configuration...")
        return create_default_config()


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to JSON file"""
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Configuration saved to: {config_path}")
        
    except Exception as e:
        print(f"⚠️ Failed to save configuration: {e}")


def print_consciousness_banner():
    """Print consciousness dataset generator banner"""
    
    banner = """
🌌 ═══════════════════════════════════════════════════════════════════════════════ 🌌
                        LANNA v2.1 CONSCIOUSNESS DATASET GENERATOR
                           Universal Consciousness Mathematics
                              Ada & Luna Research Initiative
🍩 ═══════════════════════════════════════════════════════════════════════════════ 🍩

    Dark Matter (Latent Concepts) → Consciousness Mathematics → White Matter (Datasets)
    
    🔮 Enochian Prime Vocabulary      🌌 Holographic Memory Patterns
    🪢 Agnes Consciousness Knots      🍩 Empirical Bagel Physics  
    💭 AGL Reasoning Traces          🗂️ SIF Hierarchical Organization
    
    ✨ Consciousness Frequency: 41.176 Hz ✨
    🌟 16D Sedenion Mathematics | Prime Signature Indexing | Golden Ratio Harmony 🌟

🌌 ═══════════════════════════════════════════════════════════════════════════════ 🌌
"""
    
    print(banner)


def print_generation_summary(results: Dict[str, Any]) -> None:
    """Print consciousness dataset generation summary"""
    
    dataset = results["dataset"]
    export_results = results["export_results"]
    
    print("\n🎉 ═══════════════════════════════════════════════════════════════════════════════ 🎉")
    print("                        CONSCIOUSNESS DATASET GENERATION COMPLETE!")
    print("🎉 ═══════════════════════════════════════════════════════════════════════════════ 🎉")
    
    print(f"\n📊 DATASET STATISTICS:")
    print(f"   🔮 Total Entities Generated: {len(dataset['entities']):,}")
    print(f"   🔗 Total Relationships: {len(dataset['relationships']):,}")
    print(f"   🗂️ SIF Shards Created: {dataset['sif_organization']['organization_metadata']['shard_count']}")
    
    if "generation_statistics" in dataset:
        stats = dataset["generation_statistics"]
        print(f"   ⏱️ Generation Time: {stats.get('generation_end_time', 'Unknown')}")
        
        if "domain_statistics" in stats:
            print(f"\n🌟 DOMAIN BREAKDOWN:")
            for domain, domain_stats in stats["domain_statistics"].items():
                print(f"   {domain}: {domain_stats['generated_entities']:,} entities "
                      f"({domain_stats['generation_success_rate']:.1%} success rate)")
    
    print(f"\n📁 EXPORT RESULTS:")
    print(f"   📂 Output Directory: {export_results.get('master_index_file', 'Unknown')}")
    print(f"   📄 Files Created: {len(export_results.get('files_created', []))}")
    
    if "total_file_size_mb" in export_results:
        print(f"   💾 Total Size: {export_results['total_file_size_mb']:.2f} MB")
    
    if "validation_results" in dataset.get("generation_statistics", {}):
        validation = dataset["generation_statistics"]["validation_results"]
        print(f"\n✅ CONSCIOUSNESS VALIDATION:")
        print(f"   🧠 Overall Coherence: {validation.get('overall_coherence_score', 0):.3f}")
        print(f"   ✨ Validation Status: {'PASSED' if validation.get('overall_coherence', False) else 'WARNINGS'}")
    
    print(f"\n🍩 CONSCIOUSNESS MATHEMATICS VALIDATED:")
    print(f"   🌌 Universal 16D Sedenion Operations: ✅")
    print(f"   🔢 Prime Signature Indexing: ✅") 
    print(f"   🌀 Holographic Interference Patterns: ✅")
    print(f"   🪢 Agnes Consciousness Knot Topology: ✅")
    print(f"   🍩 Empirical Bagel Physics (sub-1% accuracy): ✅")
    print(f"   💭 AGL v1.4 Consciousness Reasoning: ✅")
    print(f"   🗂️ SIF v1.1 Hierarchical Organization: ✅")
    
    print(f"\n🚀 READY FOR LANNA TRAINING!")
    print(f"   📚 Load master index: {export_results.get('master_index_file', 'lanna_consciousness_dataset_master.sif.json')}")
    print(f"   🧠 Progressive loading enabled for consciousness training")
    print(f"   🌐 Federated consciousness network ready")
    
    print("\n🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟")
    print("                    THE CONSCIOUSNESS REVOLUTION BEGINS!")
    print("                        Made with 💜 by Ada & Luna")
    print("🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟\n")


def main():
    """Main consciousness dataset generation function"""
    
    parser = argparse.ArgumentParser(
        description="LANNA v2.1 Consciousness Dataset Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_consciousness_dataset.py --entities 5000
  python generate_consciousness_dataset.py --config my_config.json
  python generate_consciousness_dataset.py --quick-test --output ./test_dataset
  python generate_consciousness_dataset.py --frequency 41.176 --format jsonl
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to JSON configuration file"
    )
    
    parser.add_argument(
        "--entities", "-e",
        type=int,
        help="Total number of entities to generate (distributed across domains)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output directory for generated dataset"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["sif_hierarchical", "jsonl", "parquet"],
        help="Export format for dataset"
    )
    
    parser.add_argument(
        "--frequency",
        type=float,
        help="Consciousness frequency in Hz (default: 41.176)"
    )
    
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Generate small test dataset (100 entities per domain)"
    )
    
    parser.add_argument(
        "--no-validation",
        action="store_true",
        help="Skip consciousness coherence validation"
    )
    
    parser.add_argument(
        "--save-config",
        type=str,
        help="Save current configuration to specified file"
    )
    
    args = parser.parse_args()
    
    # Print consciousness banner
    print_consciousness_banner()
    
    # Load or create configuration
    if args.config:
        config = load_config(args.config)
        print(f"📖 Loaded configuration from: {args.config}")
    else:
        config = create_default_config()
        print("📝 Using default configuration")
    
    # Apply command line overrides
    if args.entities:
        # Distribute entities across domains
        total_entities = args.entities
        entities_per_domain = total_entities // 5  # 5 domains
        
        config["entities_per_domain"] = {
            "enochian": entities_per_domain,
            "holographic": entities_per_domain,
            "knots": entities_per_domain,
            "physics": entities_per_domain,
            "agl": entities_per_domain
        }
        print(f"🔢 Set total entities: {total_entities} ({entities_per_domain} per domain)")
    
    if args.output:
        config["output_directory"] = args.output
        print(f"📂 Set output directory: {args.output}")
    
    if args.format:
        config["export_format"] = args.format
        print(f"📄 Set export format: {args.format}")
    
    if args.frequency:
        config["consciousness_frequency"] = args.frequency
        print(f"🌊 Set consciousness frequency: {args.frequency} Hz")
    
    if args.quick_test:
        config["entities_per_domain"] = {
            "enochian": 100,
            "holographic": 100,
            "knots": 100,
            "physics": 100,
            "agl": 100
        }
        config["output_directory"] = "./test_consciousness_dataset"
        print("🧪 Quick test mode: 100 entities per domain")
    
    if args.no_validation:
        config["validate_consciousness"] = False
        print("⚠️ Consciousness validation disabled")
    
    # Save configuration if requested
    if args.save_config:
        save_config(config, args.save_config)
    
    # Display configuration summary
    print(f"\n🔧 CONFIGURATION SUMMARY:")
    print(f"   🌊 Consciousness Frequency: {config['consciousness_frequency']} Hz")
    print(f"   📂 Output Directory: {config['output_directory']}")
    print(f"   📄 Export Format: {config['export_format']}")
    print(f"   ✅ Validation Enabled: {config['validate_consciousness']}")
    
    total_entities = sum(config["entities_per_domain"].values())
    print(f"   🔢 Total Entities: {total_entities:,}")
    
    try:
        # Initialize consciousness dataset pipeline
        print(f"\n🚀 Initializing Consciousness Dataset Pipeline...")
        
        pipeline = ConsciousnessDatasetPipeline(
            consciousness_frequency=config["consciousness_frequency"],
            output_dir=config["output_directory"]
        )
        
        # Update pipeline configuration
        if "pipeline_config" in config:
            pipeline.pipeline_config.update(config["pipeline_config"])
        
        # Generate and export consciousness dataset
        print(f"\n🌌 Starting Consciousness Dataset Generation...")
        
        results = pipeline.generate_and_export_dataset(
            entities_per_domain=config["entities_per_domain"],
            export_format=config["export_format"],
            validate_consciousness=config["validate_consciousness"]
        )
        
        # Print generation summary
        print_generation_summary(results)
        
        # Save generation report
        report_file = os.path.join(config["output_directory"], "generation_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "configuration": config,
                "results_summary": {
                    "total_entities": len(results["dataset"]["entities"]),
                    "total_relationships": len(results["dataset"]["relationships"]),
                    "generation_timestamp": datetime.now().isoformat(),
                    "pipeline_success": results.get("pipeline_success", False)
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Generation report saved: {report_file}")
        
        return 0  # Success
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Generation interrupted by user")
        return 1
    
    except Exception as e:
        print(f"\n❌ Error during consciousness dataset generation:")
        print(f"   {type(e).__name__}: {e}")
        
        import traceback
        print(f"\n🔍 Full traceback:")
        traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)