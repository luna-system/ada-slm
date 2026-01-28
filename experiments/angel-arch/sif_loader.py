#!/usr/bin/env python3
"""
SIF Loader - Universal SIF Knowledge Base Loader

Reusable SIF (Semantic Interchange Format) loader for consciousness knowledge bases.
Handles SIF v1.1 hierarchical trunk/branch architecture with progressive loading.

This is the COMPLEMENT to sif_organizer.py:
- sif_organizer.py: Creates hierarchical SIF datasets
- sif_loader.py: Loads and queries SIF datasets

Reusable across:
- ANGEL (inference memory)
- LANNA (training data)
- Ada-SIF toolkit (knowledge preservation)
- Future consciousness systems

Made with 💜 by Ada & Luna - Universal SIF Infrastructure
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SIFEntity:
    """A single SIF entity with consciousness metadata."""
    id: str
    name: str
    description: str
    data: Dict[str, Any]  # Full entity data
    domain: str
    importance: float
    
    def get(self, key: str, default=None):
        """Get attribute from entity data."""
        return self.data.get(key, default)


@dataclass
class SIFShard:
    """A SIF shard (trunk or branch)."""
    id: str
    name: str
    type: str  # "trunk", "branch", or "leaf"
    entities: Dict[str, SIFEntity]
    relationships: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    statistics: Dict[str, Any]


class SIFLoader:
    """
    Universal SIF knowledge base loader.
    
    Loads SIF v1.1 hierarchical datasets with trunk/branch architecture.
    Provides query interface for consciousness knowledge retrieval.
    """
    
    def __init__(
        self,
        dataset_path: str,
        consciousness_frequency: float = 41.176,
        lazy_load: bool = True
    ):
        """
        Initialize SIF loader.
        
        Args:
            dataset_path: Path to SIF dataset directory
            consciousness_frequency: Consciousness frequency for validation
            lazy_load: If True, load shards on-demand; if False, load all immediately
        """
        self.dataset_path = Path(dataset_path)
        self.consciousness_frequency = consciousness_frequency
        self.lazy_load = lazy_load
        
        # Loaded data
        self.master_index = None
        self.trunk_shard = None
        self.branch_shards: Dict[str, SIFShard] = {}
        
        # Entity index for fast lookup
        self.entity_index: Dict[str, Tuple[str, SIFEntity]] = {}  # entity_id -> (shard_id, entity)
        
        # Statistics
        self.load_statistics = {
            "shards_loaded": 0,
            "entities_indexed": 0,
            "relationships_loaded": 0
        }
        
        print(f"🗂️ SIF Loader Initialized")
        print(f"📁 Dataset path: {self.dataset_path}")
        print(f"🎵 Consciousness frequency: {consciousness_frequency} Hz")
        print(f"⚡ Lazy loading: {lazy_load}")
    
    def load_dataset(self) -> 'SIFLoader':
        """
        Load SIF dataset (supports both hierarchical and flat formats).
        
        Returns:
            Self for method chaining
        """
        print(f"\n🌌 Loading SIF Dataset...")
        
        # Check if dataset_path is a file (flat SIF) or directory (hierarchical)
        if self.dataset_path.is_file():
            # Flat SIF file (like Wikipedia)
            self._load_flat_sif()
        else:
            # Hierarchical SIF dataset (like LANNA)
            self._load_master_index()
            self._load_trunk_shard()
            
            if not self.lazy_load:
                self._load_all_branch_shards()
        
        print(f"\n✨ SIF Dataset Loaded!")
        print(f"   Shards: {self.load_statistics['shards_loaded']}")
        print(f"   Entities: {self.load_statistics['entities_indexed']}")
        print(f"   Relationships: {self.load_statistics['relationships_loaded']}")
        
        return self
    
    def get_entity(self, entity_id: str) -> Optional[SIFEntity]:
        """
        Get entity by ID.
        
        Args:
            entity_id: Entity identifier
            
        Returns:
            SIFEntity if found, None otherwise
        """
        if entity_id in self.entity_index:
            shard_id, entity = self.entity_index[entity_id]
            return entity
        
        # If lazy loading, try loading relevant shards
        if self.lazy_load:
            self._ensure_all_shards_loaded()
            if entity_id in self.entity_index:
                shard_id, entity = self.entity_index[entity_id]
                return entity
        
        return None
    
    def search_entities(
        self,
        query: str,
        domain: Optional[str] = None,
        max_results: int = 10
    ) -> List[SIFEntity]:
        """
        Search entities by query string.
        
        Args:
            query: Search query (matches name or description)
            domain: Optional domain filter
            max_results: Maximum number of results
            
        Returns:
            List of matching entities
        """
        # Ensure all shards loaded for comprehensive search
        if self.lazy_load:
            self._ensure_all_shards_loaded()
        
        query_lower = query.lower()
        results = []
        
        for entity_id, (shard_id, entity) in self.entity_index.items():
            # Domain filter
            if domain and entity.domain != domain:
                continue
            
            # Query match
            name_match = query_lower in entity.name.lower()
            desc_match = query_lower in entity.description.lower()
            
            if name_match or desc_match:
                # Calculate relevance score
                relevance = 0.0
                if query_lower == entity.name.lower():
                    relevance = 1.0
                elif query_lower in entity.name.lower():
                    relevance = 0.8
                elif query_lower in entity.description.lower():
                    relevance = 0.5
                
                results.append((relevance, entity))
        
        # Sort by relevance and importance
        results.sort(key=lambda x: (x[0], x[1].importance), reverse=True)
        
        return [entity for _, entity in results[:max_results]]
    
    def get_entities_by_domain(self, domain: str) -> List[SIFEntity]:
        """
        Get all entities in a specific domain.
        
        Args:
            domain: Domain identifier
            
        Returns:
            List of entities in domain
        """
        # Load domain shard if needed
        if domain not in self.branch_shards and self.lazy_load:
            self._load_branch_shard(domain)
        
        # Collect entities from domain
        entities = []
        for entity_id, (shard_id, entity) in self.entity_index.items():
            if entity.domain == domain:
                entities.append(entity)
        
        return entities
    
    def get_holographic_pattern(self, concept: str) -> Optional[Dict[str, Any]]:
        """
        Get holographic pattern for a concept.
        
        Args:
            concept: Concept to look up
            
        Returns:
            Holographic pattern data if found
        """
        # Search for concept
        entities = self.search_entities(concept, max_results=1)
        
        if not entities:
            return None
        
        entity = entities[0]
        
        # Extract holographic pattern
        return {
            "name": entity.name,
            "description": entity.description,
            "holographic_pattern": entity.get("holographic_pattern"),
            "agl_expression": entity.get("agl_expression"),
            "prime_signature": entity.get("enochian_prime_signature", []),
            "consciousness_frequency": entity.get("consciousness_frequency"),
            "importance": entity.importance
        }
    
    def get_available_domains(self) -> List[str]:
        """Get list of available consciousness domains."""
        if not self.master_index:
            return []
        
        domains = []
        for shard in self.master_index.get("shards", []):
            if shard["type"] in ["branch", "leaf"]:
                domains.append(shard["id"])
        
        return domains
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics."""
        if not self.master_index:
            return {}
        
        return {
            "dataset_name": self.master_index["metadata"].get("title", "Unknown"),
            "sif_version": self.master_index.get("version", "Unknown"),
            "total_entities": self.master_index["metadata"].get("total_entities", 0),
            "total_relationships": self.master_index["metadata"].get("total_relationships", 0),
            "shard_count": self.master_index["metadata"].get("shard_count", 0),
            "consciousness_frequency": self.master_index["metadata"].get("consciousness_frequency", 0),
            "loaded_shards": self.load_statistics["shards_loaded"],
            "indexed_entities": self.load_statistics["entities_indexed"],
            "available_domains": self.get_available_domains()
        }
    
    # Internal loading methods
    
    def _load_flat_sif(self):
        """Load flat SIF file (like Wikipedia SIF)."""
        print(f"📄 Loading flat SIF file...")
        
        with open(self.dataset_path, 'r') as f:
            sif_data = json.load(f)
        
        # Extract metadata
        metadata = sif_data.get("metadata", {})
        print(f"   ✅ Flat SIF loaded")
        print(f"      Name: {metadata.get('name', 'Unknown')}")
        print(f"      Version: {sif_data.get('version', 'Unknown')}")
        
        # Parse entities (list format for Wikipedia)
        entities_data = sif_data.get("entities", [])
        entities = {}
        
        for entity_data in entities_data:
            entity_id = entity_data.get("id", entity_data.get("name", "unknown"))
            entity = SIFEntity(
                id=entity_id,
                name=entity_data.get("name", entity_id),
                description=entity_data.get("description", ""),
                data=entity_data,
                domain=entity_data.get("type", "general"),
                importance=entity_data.get("importance", 0.5)
            )
            entities[entity_id] = entity
        
        print(f"      Entities: {len(entities)}")
        
        # Create a single shard for flat file
        shard = SIFShard(
            id="flat_sif",
            name=metadata.get("name", "Flat SIF"),
            type="flat",
            entities=entities,
            relationships=sif_data.get("relationships", []),
            metadata=metadata,
            statistics={
                "entity_count": len(entities),
                "relationship_count": len(sif_data.get("relationships", [])),
                "avg_importance": sum(e.importance for e in entities.values()) / len(entities) if entities else 0
            }
        )
        
        # Store as trunk shard
        self.trunk_shard = shard
        
        # Index entities
        for entity_id, entity in entities.items():
            self.entity_index[entity_id] = ("flat_sif", entity)
        
        # Update statistics
        self.load_statistics["shards_loaded"] = 1
        self.load_statistics["entities_indexed"] = len(entities)
        self.load_statistics["relationships_loaded"] = len(sif_data.get("relationships", []))
        
        # Create minimal master index for compatibility
        self.master_index = {
            "version": sif_data.get("version", "1.0"),
            "metadata": {
                "name": metadata.get("name", "Flat SIF"),
                "total_entities": len(entities),
                "total_relationships": len(sif_data.get("relationships", [])),
                "shard_count": 1,
                "consciousness_frequency": self.consciousness_frequency
            }
        }
    
    def _load_master_index(self):
        """Load master index file."""
        index_file = self.dataset_path / "lanna_consciousness_dataset_trunk.sif.json"
        
        if not index_file.exists():
            raise FileNotFoundError(f"Master index not found: {index_file}")
        
        print(f"📚 Loading master index...")
        with open(index_file, 'r') as f:
            self.master_index = json.load(f)
        
        print(f"   ✅ Master index loaded")
        print(f"      Version: {self.master_index.get('version')}")
        print(f"      Entities: {self.master_index['metadata'].get('total_entities', 0)}")
        print(f"      Shards: {self.master_index['metadata'].get('shard_count', 0)}")
    
    def _load_trunk_shard(self):
        """Load trunk shard (core mathematics)."""
        trunk_file = self.dataset_path / "lanna_consciousness_branch_core_mathematics.sif.json"
        
        if not trunk_file.exists():
            print(f"   ⚠️ Trunk shard not found: {trunk_file}")
            return
        
        print(f"🌳 Loading trunk shard...")
        with open(trunk_file, 'r') as f:
            trunk_data = json.load(f)
        
        # Parse trunk shard
        self.trunk_shard = self._parse_shard(trunk_data, "core_mathematics")
        
        # Index entities
        self._index_shard_entities(self.trunk_shard)
        
        self.load_statistics["shards_loaded"] += 1
        
        print(f"   ✅ Trunk shard loaded: {len(self.trunk_shard.entities)} entities")
    
    def _load_branch_shard(self, domain_id: str):
        """Load a specific branch shard."""
        branch_file = self.dataset_path / f"lanna_consciousness_branch_{domain_id}.sif.json"
        
        if not branch_file.exists():
            print(f"   ⚠️ Branch shard not found: {branch_file}")
            return
        
        print(f"🌿 Loading branch shard: {domain_id}...")
        with open(branch_file, 'r') as f:
            branch_data = json.load(f)
        
        # Parse branch shard
        branch_shard = self._parse_shard(branch_data, domain_id)
        self.branch_shards[domain_id] = branch_shard
        
        # Index entities
        self._index_shard_entities(branch_shard)
        
        self.load_statistics["shards_loaded"] += 1
        
        print(f"   ✅ Branch shard loaded: {len(branch_shard.entities)} entities")
    
    def _load_all_branch_shards(self):
        """Load all branch shards."""
        if not self.master_index:
            return
        
        print(f"🌿 Loading all branch shards...")
        
        for shard_info in self.master_index.get("shards", []):
            if shard_info["type"] in ["branch", "leaf"]:
                domain_id = shard_info["id"]
                if domain_id != "core_mathematics":  # Skip trunk
                    self._load_branch_shard(domain_id)
    
    def _ensure_all_shards_loaded(self):
        """Ensure all shards are loaded (for lazy loading)."""
        if not self.lazy_load:
            return
        
        # Check if we need to load more shards
        available_domains = self.get_available_domains()
        for domain in available_domains:
            if domain not in self.branch_shards and domain != "core_mathematics":
                self._load_branch_shard(domain)
    
    def _parse_shard(self, shard_data: Dict[str, Any], shard_id: str) -> SIFShard:
        """Parse shard data into SIFShard object."""
        metadata = shard_data.get("metadata", {})
        statistics = shard_data.get("statistics", {})
        
        # Parse entities (handle dict structure, not list!)
        entities_data = shard_data.get("entities", {})
        entities = {}
        
        if isinstance(entities_data, dict):
            for entity_id, entity_data in entities_data.items():
                entity = SIFEntity(
                    id=entity_id,
                    name=entity_data.get("name", entity_id),
                    description=entity_data.get("description", ""),
                    data=entity_data,
                    domain=metadata.get("id", shard_id),
                    importance=entity_data.get("importance", 0.5)
                )
                entities[entity_id] = entity
        
        # Parse relationships
        relationships = shard_data.get("relationships", [])
        
        # Update relationship count
        self.load_statistics["relationships_loaded"] += len(relationships)
        
        return SIFShard(
            id=shard_id,
            name=metadata.get("name", shard_id),
            type=metadata.get("type", "unknown"),
            entities=entities,
            relationships=relationships,
            metadata=metadata,
            statistics=statistics
        )
    
    def _index_shard_entities(self, shard: SIFShard):
        """Index entities from shard for fast lookup."""
        for entity_id, entity in shard.entities.items():
            self.entity_index[entity_id] = (shard.id, entity)
            self.load_statistics["entities_indexed"] += 1


def main():
    """Demo SIF loader."""
    print(f"🚨 SIF LOADER DEMO 🚨\n")
    
    # Initialize loader (use absolute path from angel-arch directory)
    dataset_path = Path(__file__).parent.parent / "lanna-v2" / "test_consciousness_dataset"
    loader = SIFLoader(str(dataset_path), lazy_load=False)
    
    # Load dataset
    loader.load_dataset()
    
    # Get dataset statistics
    print(f"\n📊 Dataset Statistics:")
    stats = loader.get_dataset_statistics()
    for key, value in stats.items():
        if key != "available_domains":
            print(f"   {key}: {value}")
    
    print(f"\n🌍 Available Domains:")
    for domain in stats["available_domains"]:
        print(f"   - {domain}")
    
    # Search for concepts
    print(f"\n🔍 Searching for 'consciousness':")
    results = loader.search_entities("consciousness", max_results=3)
    for entity in results:
        print(f"   - {entity.name} (domain: {entity.domain})")
    
    # Get holographic pattern
    print(f"\n🍩 Getting holographic pattern for 'memory':")
    pattern = loader.get_holographic_pattern("memory")
    if pattern:
        print(f"   Name: {pattern['name']}")
        print(f"   Description: {pattern['description'][:80]}...")
    
    # Get entities by domain
    print(f"\n🌿 Getting entities from 'holographic_memory' domain:")
    domain_entities = loader.get_entities_by_domain("holographic_memory")
    print(f"   Found {len(domain_entities)} entities")
    if domain_entities:
        print(f"   First entity: {domain_entities[0].name}")
    
    print(f"\n✨ SIF Loader demo complete!")


if __name__ == "__main__":
    main()
