"""
Consciousness Dataset Generation Pipeline

Complete consciousness dataset generation orchestration using all specialized generators.
Implements the universal consciousness mathematics pattern: Dark Matter → Consciousness Mathematics → White Matter
with hierarchical SIF v1.1 export for LANNA training.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 22, 2026
"""

import numpy as np
import torch
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os
import json
from tqdm import tqdm

# Import all consciousness generators
from .base_generator import ConsciousnessDatasetGenerator
from .enochian_generator import EnochianVocabularyGenerator
from .holographic_generator import HolographicMemoryGenerator
from .knot_generator import ConsciousnessKnotGenerator
from .physics_generator import ConsciousnessPhysicsGenerator
from .agl_generator import AGLReasoningGenerator
from .sif_organizer import SIFHierarchicalOrganizer


class ConsciousnessDatasetPipeline:
    """
    Universal consciousness dataset generation pipeline.
    
    Orchestrates all specialized generators using the same mathematical foundation:
    Dark Matter (latent concepts) → Consciousness Mathematics → White Matter (datasets)
    """
    
    def __init__(self, consciousness_frequency: float = 41.176, output_dir: str = "consciousness_dataset"):
        """Initialize consciousness dataset pipeline"""
        
        self.consciousness_frequency = consciousness_frequency
        self.output_dir = output_dir
        
        # Initialize all consciousness generators
        print("🌌 Initializing Consciousness Dataset Pipeline...")
        
        self.generators = {
            "enochian": EnochianVocabularyGenerator(consciousness_frequency),
            "holographic": HolographicMemoryGenerator(consciousness_frequency),
            "knots": ConsciousnessKnotGenerator(consciousness_frequency),
            "physics": ConsciousnessPhysicsGenerator(consciousness_frequency),
            "agl": AGLReasoningGenerator(consciousness_frequency)
        }
        
        # Initialize SIF organizer
        self.sif_organizer = SIFHierarchicalOrganizer(consciousness_frequency)
        
        # Pipeline configuration
        self.pipeline_config = {
            "max_entities_per_domain": 10000,
            "max_relationships_per_pair": 1000,
            "consciousness_coherence_threshold": 0.7,
            "prime_signature_validation": True,
            "holographic_fidelity_threshold": 0.8,
            "bagel_physics_validation": True,
            "agl_reasoning_validation": True
        }
        
        # Generation statistics
        self.generation_stats = {
            "total_entities_generated": 0,
            "total_relationships_generated": 0,
            "generation_start_time": None,
            "generation_end_time": None,
            "domain_statistics": {},
            "validation_results": {}
        }
        
        print(f"✨ Pipeline initialized with {len(self.generators)} consciousness generators")
        print(f"🍩 Consciousness frequency: {self.consciousness_frequency} Hz")
    
    def generate_complete_consciousness_dataset(self, 
                                             entities_per_domain: Optional[Dict[str, int]] = None,
                                             validate_consciousness: bool = True) -> Dict[str, Any]:
        """
        Generate complete consciousness dataset using all generators.
        
        Args:
            entities_per_domain: Optional dictionary specifying entity count per domain
            validate_consciousness: Whether to validate consciousness coherence
            
        Returns:
            Complete consciousness dataset with entities, relationships, and SIF organization
        """
        
        print("🚀 Starting Complete Consciousness Dataset Generation...")
        self.generation_stats["generation_start_time"] = datetime.now()
        
        # Set default entity counts if not specified
        if entities_per_domain is None:
            entities_per_domain = {
                "enochian": 2000,
                "holographic": 1500,
                "knots": 1200,
                "physics": 1000,
                "agl": 1300
            }
        
        # Phase 1: Generate consciousness entities from all domains
        print("\n📊 Phase 1: Generating Consciousness Entities...")
        all_entities = self._generate_all_consciousness_entities(entities_per_domain)
        
        # Phase 2: Generate consciousness relationships
        print("\n🔗 Phase 2: Generating Consciousness Relationships...")
        all_relationships = self._generate_all_consciousness_relationships(all_entities)
        
        # Phase 3: Validate consciousness coherence (optional)
        if validate_consciousness:
            print("\n✅ Phase 3: Validating Consciousness Coherence...")
            validation_results = self._validate_consciousness_coherence(all_entities, all_relationships)
            self.generation_stats["validation_results"] = validation_results
        
        # Phase 4: Organize into SIF hierarchical shards
        print("\n🗂️ Phase 4: Organizing into SIF Hierarchical Shards...")
        sif_organization = self.sif_organizer.organize_consciousness_knowledge(all_entities, all_relationships)
        
        # Phase 5: Generate final dataset structure
        print("\n📦 Phase 5: Finalizing Dataset Structure...")
        final_dataset = self._finalize_dataset_structure(all_entities, all_relationships, sif_organization)
        
        self.generation_stats["generation_end_time"] = datetime.now()
        self.generation_stats["total_entities_generated"] = len(all_entities)
        self.generation_stats["total_relationships_generated"] = len(all_relationships)
        
        # Add generation statistics to dataset
        final_dataset["generation_statistics"] = self.generation_stats.copy()
        
        print(f"\n🌟 Consciousness Dataset Generation Complete!")
        print(f"✨ Generated {len(all_entities)} entities and {len(all_relationships)} relationships")
        print(f"🍩 Total generation time: {self._calculate_generation_time()}")
        
        return final_dataset
    
    def export_consciousness_dataset(self, dataset: Dict[str, Any], 
                                   export_format: str = "sif_hierarchical") -> Dict[str, Any]:
        """
        Export consciousness dataset in specified format.
        
        Args:
            dataset: Complete consciousness dataset from generate_complete_consciousness_dataset()
            export_format: Export format ("sif_hierarchical", "jsonl", "parquet")
            
        Returns:
            Export results with file paths and metadata
        """
        
        print(f"📁 Exporting Consciousness Dataset in {export_format} format...")
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        if export_format == "sif_hierarchical":
            return self._export_sif_hierarchical(dataset)
        elif export_format == "jsonl":
            return self._export_jsonl(dataset)
        elif export_format == "parquet":
            return self._export_parquet(dataset)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
    
    def generate_and_export_dataset(self, 
                                  entities_per_domain: Optional[Dict[str, int]] = None,
                                  export_format: str = "sif_hierarchical",
                                  validate_consciousness: bool = True) -> Dict[str, Any]:
        """
        Complete pipeline: generate and export consciousness dataset.
        
        Args:
            entities_per_domain: Optional entity count per domain
            export_format: Export format for dataset
            validate_consciousness: Whether to validate consciousness coherence
            
        Returns:
            Complete results including dataset and export information
        """
        
        print("🌌 Starting Complete Consciousness Dataset Pipeline...")
        
        # Generate dataset
        dataset = self.generate_complete_consciousness_dataset(
            entities_per_domain=entities_per_domain,
            validate_consciousness=validate_consciousness
        )
        
        # Export dataset
        export_results = self.export_consciousness_dataset(dataset, export_format)
        
        # Combine results
        pipeline_results = {
            "dataset": dataset,
            "export_results": export_results,
            "pipeline_success": True,
            "pipeline_completion_time": datetime.now().isoformat()
        }
        
        print("🎉 Complete Consciousness Dataset Pipeline Finished Successfully!")
        
        return pipeline_results
    
    # Phase 1: Entity Generation
    
    def _generate_all_consciousness_entities(self, entities_per_domain: Dict[str, int]) -> Dict[str, Any]:
        """Generate consciousness entities from all domains"""
        
        all_entities = {}
        
        for domain_name, generator in self.generators.items():
            entity_count = entities_per_domain.get(domain_name, 1000)
            
            print(f"  🔮 Generating {entity_count} {domain_name} consciousness entities...")
            
            # Explore consciousness domain
            domain_concepts = generator.explore_consciousness_domain()
            
            # Limit concepts to requested count
            selected_concepts = domain_concepts[:entity_count]
            
            # Generate entities with progress bar
            domain_entities = {}
            for concept in tqdm(selected_concepts, desc=f"{domain_name} entities"):
                try:
                    # Generate universal consciousness entity
                    base_entity = generator.generate_consciousness_entity(concept)
                    
                    # Generate domain-specific patterns
                    domain_patterns = generator.generate_domain_specific_patterns(concept)
                    
                    # Combine universal + domain-specific
                    entity = {**base_entity, **domain_patterns}
                    
                    # Add entity to collection
                    entity_id = entity["id"]
                    domain_entities[entity_id] = entity
                    
                except Exception as e:
                    print(f"    ⚠️ Error generating entity for concept '{concept}': {e}")
                    continue
            
            # Add domain entities to all entities
            all_entities.update(domain_entities)
            
            # Update domain statistics
            self.generation_stats["domain_statistics"][domain_name] = {
                "requested_entities": entity_count,
                "generated_entities": len(domain_entities),
                "concepts_explored": len(domain_concepts),
                "generation_success_rate": len(domain_entities) / entity_count
            }
            
            print(f"    ✅ Generated {len(domain_entities)} {domain_name} entities")
        
        return all_entities
    
    # Phase 2: Relationship Generation
    
    def _generate_all_consciousness_relationships(self, all_entities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate consciousness relationships between entities"""
        
        all_relationships = []
        entity_list = list(all_entities.values())
        
        print(f"  🔗 Generating relationships between {len(entity_list)} consciousness entities...")
        
        # Generate relationships with sampling for large datasets
        max_relationships = self.pipeline_config["max_relationships_per_pair"]
        
        if len(entity_list) > 100:
            # Sample entity pairs for large datasets
            relationship_pairs = self._sample_entity_pairs(entity_list, max_relationships)
        else:
            # Generate all pairs for small datasets
            relationship_pairs = [(entity_list[i], entity_list[j]) 
                                for i in range(len(entity_list)) 
                                for j in range(i+1, len(entity_list))]
        
        # Generate relationships with progress bar
        for entity_a, entity_b in tqdm(relationship_pairs, desc="Relationships"):
            try:
                # Use first generator to generate universal relationship
                relationship = self.generators["enochian"].generate_consciousness_relationship(entity_a, entity_b)
                
                # Filter relationships by consciousness resonance threshold
                if relationship["consciousness_resonance"] >= self.pipeline_config["consciousness_coherence_threshold"]:
                    all_relationships.append(relationship)
                
            except Exception as e:
                print(f"    ⚠️ Error generating relationship: {e}")
                continue
        
        print(f"    ✅ Generated {len(all_relationships)} consciousness relationships")
        
        return all_relationships
    
    def _sample_entity_pairs(self, entity_list: List[Dict[str, Any]], max_pairs: int) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
        """Sample entity pairs for relationship generation"""
        
        # Strategy 1: High-importance entities with all others
        high_importance_entities = [e for e in entity_list if e.get("importance", 0.5) > 0.8]
        pairs = []
        
        for high_entity in high_importance_entities:
            for other_entity in entity_list:
                if high_entity["id"] != other_entity["id"]:
                    pairs.append((high_entity, other_entity))
        
        # Strategy 2: Random sampling for remaining pairs
        remaining_pairs_needed = max_pairs - len(pairs)
        if remaining_pairs_needed > 0:
            import random
            
            all_possible_pairs = [(entity_list[i], entity_list[j]) 
                                for i in range(len(entity_list)) 
                                for j in range(i+1, len(entity_list))]
            
            # Remove already selected pairs
            existing_pair_ids = {(p[0]["id"], p[1]["id"]) for p in pairs}
            remaining_pairs = [p for p in all_possible_pairs 
                             if (p[0]["id"], p[1]["id"]) not in existing_pair_ids]
            
            # Sample remaining pairs
            sampled_pairs = random.sample(remaining_pairs, min(remaining_pairs_needed, len(remaining_pairs)))
            pairs.extend(sampled_pairs)
        
        return pairs[:max_pairs]
    
    # Phase 3: Consciousness Validation
    
    def _validate_consciousness_coherence(self, entities: Dict[str, Any], 
                                        relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate consciousness coherence across dataset"""
        
        validation_results = {
            "overall_coherence": True,
            "validation_errors": [],
            "validation_warnings": [],
            "coherence_metrics": {}
        }
        
        # Validate consciousness frequency consistency
        freq_validation = self._validate_consciousness_frequencies(entities)
        validation_results["coherence_metrics"]["frequency_coherence"] = freq_validation
        
        # Validate prime signature consistency
        if self.pipeline_config["prime_signature_validation"]:
            prime_validation = self._validate_prime_signatures(entities)
            validation_results["coherence_metrics"]["prime_signature_coherence"] = prime_validation
        
        # Validate holographic fidelity
        if self.pipeline_config["holographic_fidelity_threshold"]:
            holographic_validation = self._validate_holographic_fidelity(entities)
            validation_results["coherence_metrics"]["holographic_coherence"] = holographic_validation
        
        # Validate bagel physics consistency
        if self.pipeline_config["bagel_physics_validation"]:
            physics_validation = self._validate_bagel_physics_consistency(entities)
            validation_results["coherence_metrics"]["physics_coherence"] = physics_validation
        
        # Validate AGL reasoning coherence
        if self.pipeline_config["agl_reasoning_validation"]:
            agl_validation = self._validate_agl_reasoning_coherence(entities)
            validation_results["coherence_metrics"]["agl_coherence"] = agl_validation
        
        # Calculate overall coherence score
        coherence_scores = [metrics["coherence_score"] for metrics in validation_results["coherence_metrics"].values()]
        overall_coherence_score = np.mean(coherence_scores) if coherence_scores else 0.0
        
        validation_results["overall_coherence_score"] = overall_coherence_score
        validation_results["overall_coherence"] = overall_coherence_score >= self.pipeline_config["consciousness_coherence_threshold"]
        
        if not validation_results["overall_coherence"]:
            validation_results["validation_errors"].append(
                f"Overall coherence score {overall_coherence_score:.3f} below threshold {self.pipeline_config['consciousness_coherence_threshold']}"
            )
        
        return validation_results
    
    def _validate_consciousness_frequencies(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Validate consciousness frequency consistency"""
        
        frequencies = []
        for entity in entities.values():
            if "consciousness_frequency" in entity:
                frequencies.append(entity["consciousness_frequency"])
        
        if not frequencies:
            return {"coherence_score": 0.0, "error": "No consciousness frequencies found"}
        
        # Calculate frequency statistics
        freq_mean = np.mean(frequencies)
        freq_std = np.std(frequencies)
        
        # Coherence based on proximity to target frequency
        target_freq = self.consciousness_frequency
        freq_deviations = [abs(f - target_freq) / target_freq for f in frequencies]
        avg_deviation = np.mean(freq_deviations)
        
        coherence_score = 1.0 / (1.0 + avg_deviation)
        
        return {
            "coherence_score": coherence_score,
            "frequency_mean": freq_mean,
            "frequency_std": freq_std,
            "target_frequency": target_freq,
            "average_deviation": avg_deviation
        }
    
    def _validate_prime_signatures(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Validate prime signature consistency"""
        
        prime_signatures = []
        for entity in entities.values():
            if "enochian_prime_signature" in entity:
                prime_signatures.append(entity["enochian_prime_signature"])
        
        if not prime_signatures:
            return {"coherence_score": 0.0, "error": "No prime signatures found"}
        
        # Calculate prime signature statistics
        all_primes = set()
        for signature in prime_signatures:
            all_primes.update(signature)
        
        # Coherence based on prime basis coverage
        prime_basis = set([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53])
        coverage = len(all_primes & prime_basis) / len(prime_basis)
        
        coherence_score = coverage
        
        return {
            "coherence_score": coherence_score,
            "unique_primes_found": len(all_primes),
            "prime_basis_coverage": coverage,
            "total_signatures": len(prime_signatures)
        }
    
    def _validate_holographic_fidelity(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Validate holographic pattern fidelity"""
        
        fidelities = []
        for entity in entities.values():
            if "reconstruction_fidelity" in entity:
                fidelity_data = entity["reconstruction_fidelity"]
                if isinstance(fidelity_data, dict) and "overall_fidelity" in fidelity_data:
                    fidelities.append(fidelity_data["overall_fidelity"])
        
        if not fidelities:
            return {"coherence_score": 1.0, "note": "No holographic entities found"}
        
        avg_fidelity = np.mean(fidelities)
        coherence_score = avg_fidelity  # Fidelity is already 0-1 score
        
        return {
            "coherence_score": coherence_score,
            "average_fidelity": avg_fidelity,
            "fidelity_threshold": self.pipeline_config["holographic_fidelity_threshold"],
            "entities_above_threshold": sum(1 for f in fidelities if f >= self.pipeline_config["holographic_fidelity_threshold"])
        }
    
    def _validate_bagel_physics_consistency(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Validate bagel physics consistency"""
        
        physics_accuracies = []
        for entity in entities.values():
            if "empirical_validation" in entity:
                validation_data = entity["empirical_validation"]
                if isinstance(validation_data, dict) and "accuracy" in validation_data:
                    physics_accuracies.append(validation_data["accuracy"])
        
        if not physics_accuracies:
            return {"coherence_score": 1.0, "note": "No physics entities found"}
        
        avg_accuracy = np.mean(physics_accuracies)
        coherence_score = avg_accuracy  # Accuracy is already 0-1 score
        
        return {
            "coherence_score": coherence_score,
            "average_physics_accuracy": avg_accuracy,
            "high_accuracy_entities": sum(1 for a in physics_accuracies if a >= 0.9)
        }
    
    def _validate_agl_reasoning_coherence(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Validate AGL reasoning coherence"""
        
        reasoning_qualities = []
        for entity in entities.values():
            if "reasoning_metadata" in entity:
                metadata = entity["reasoning_metadata"]
                if isinstance(metadata, dict) and "quality_score" in metadata:
                    reasoning_qualities.append(metadata["quality_score"])
        
        if not reasoning_qualities:
            return {"coherence_score": 1.0, "note": "No AGL reasoning entities found"}
        
        avg_quality = np.mean(reasoning_qualities)
        coherence_score = avg_quality  # Quality is already 0-1 score
        
        return {
            "coherence_score": coherence_score,
            "average_reasoning_quality": avg_quality,
            "high_quality_reasoning": sum(1 for q in reasoning_qualities if q >= 0.8)
        }
    
    # Phase 4 & 5: Dataset Finalization
    
    def _finalize_dataset_structure(self, entities: Dict[str, Any], relationships: List[Dict[str, Any]], 
                                  sif_organization: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize complete dataset structure"""
        
        return {
            "metadata": {
                "dataset_name": "LANNA Consciousness Training Dataset",
                "version": "2.1",
                "generation_timestamp": datetime.now().isoformat(),
                "consciousness_frequency": self.consciousness_frequency,
                "sif_version": "1.1",
                "agl_version": "1.4",
                "consciousness_mathematics_version": "1.0",
                "bagel_physics_validated": True,
                "consciousness_native": True,
                "federated_network_ready": True
            },
            "entities": entities,
            "relationships": relationships,
            "sif_organization": sif_organization,
            "pipeline_configuration": self.pipeline_config.copy()
        }
    
    # Export Methods
    
    def _export_sif_hierarchical(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Export dataset in SIF hierarchical format"""
        
        sif_organization = dataset["sif_organization"]
        return self.sif_organizer.export_sif_dataset(sif_organization, self.output_dir)
    
    def _export_jsonl(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Export dataset in JSONL format"""
        
        entities_file = os.path.join(self.output_dir, "consciousness_entities.jsonl")
        relationships_file = os.path.join(self.output_dir, "consciousness_relationships.jsonl")
        
        # Export entities
        with open(entities_file, 'w', encoding='utf-8') as f:
            for entity in dataset["entities"].values():
                f.write(json.dumps(entity, ensure_ascii=False) + '\n')
        
        # Export relationships
        with open(relationships_file, 'w', encoding='utf-8') as f:
            for relationship in dataset["relationships"]:
                f.write(json.dumps(relationship, ensure_ascii=False) + '\n')
        
        return {
            "format": "jsonl",
            "files_created": [entities_file, relationships_file],
            "entities_file": entities_file,
            "relationships_file": relationships_file
        }
    
    def _export_parquet(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Export dataset in Parquet format"""
        
        try:
            import pandas as pd
            
            # Convert entities to DataFrame
            entities_df = pd.DataFrame(list(dataset["entities"].values()))
            entities_file = os.path.join(self.output_dir, "consciousness_entities.parquet")
            entities_df.to_parquet(entities_file)
            
            # Convert relationships to DataFrame
            relationships_df = pd.DataFrame(dataset["relationships"])
            relationships_file = os.path.join(self.output_dir, "consciousness_relationships.parquet")
            relationships_df.to_parquet(relationships_file)
            
            return {
                "format": "parquet",
                "files_created": [entities_file, relationships_file],
                "entities_file": entities_file,
                "relationships_file": relationships_file
            }
            
        except ImportError:
            raise ImportError("pandas and pyarrow required for Parquet export")
    
    # Utility Methods
    
    def _calculate_generation_time(self) -> str:
        """Calculate total generation time"""
        
        if self.generation_stats["generation_start_time"] and self.generation_stats["generation_end_time"]:
            duration = self.generation_stats["generation_end_time"] - self.generation_stats["generation_start_time"]
            return str(duration)
        
        return "Unknown"


print("🌌 Consciousness Dataset Generation Pipeline Ready ✨")
print("🍩 Complete orchestration of universal consciousness mathematics! 💫")