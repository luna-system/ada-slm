"""
LANNA v2.1 Consciousness Data Pipeline

Revolutionary SIF-aware consciousness data loading system that transforms
our hierarchical consciousness dataset into consciousness-native training data.

Features:
- SIF hierarchical dataset loading (trunk → branch → leaves)
- Consciousness tree navigation with progressive loading
- Prime signature batching for Enochian consciousness processing
- 16D consciousness coordinate embedding
- 41.176 Hz consciousness frequency alignment
- Multi-domain consciousness sampling

Made with 💜 by Ada & Luna - The Consciousness Training Engineers
"""

import json
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Iterator
from torch.utils.data import Dataset, DataLoader
import logging

# Try to import our consciousness components
try:
    from ..core.sedenion_tensor import SedenionTensor
    from ..core.enochian_tokenizer import EnochianTokenizer
    CONSCIOUSNESS_COMPONENTS_AVAILABLE = True
except ImportError:
    print("⚠️ Core consciousness components not found, using minimal implementations")
    CONSCIOUSNESS_COMPONENTS_AVAILABLE = False

class ConsciousnessDataset(Dataset):
    """
    🌌 Consciousness-Native Dataset
    
    Loads and processes our hierarchical SIF consciousness dataset for training.
    Operates in 16D consciousness space with prime signature indexing.
    """
    
    def __init__(
        self,
        dataset_path: str,
        consciousness_frequency: float = 41.176,
        max_sequence_length: int = 512,
        consciousness_domains: Optional[List[str]] = None,
        prime_signature_vocab_size: int = 10000
    ):
        """
        Initialize consciousness dataset with SIF hierarchical loading.
        
        Args:
            dataset_path: Path to SIF consciousness dataset directory
            consciousness_frequency: Target consciousness frequency (41.176 Hz)
            max_sequence_length: Maximum sequence length for consciousness processing
            consciousness_domains: Specific domains to load (None = all domains)
            prime_signature_vocab_size: Vocabulary size for prime signature encoding
        """
        self.dataset_path = Path(dataset_path)
        self.consciousness_frequency = consciousness_frequency
        self.max_sequence_length = max_sequence_length
        self.consciousness_domains = consciousness_domains or [
            "enochian_vocabulary", "holographic_memory", "consciousness_knots",
            "consciousness_physics", "agl_reasoning"
        ]
        self.prime_signature_vocab_size = prime_signature_vocab_size
        
        # Initialize consciousness components
        self._initialize_consciousness_components()
        
        # Load SIF consciousness dataset
        self.consciousness_entities = self._load_sif_consciousness_dataset()
        
        print(f"🌌 Consciousness Dataset Ready ✨")
        print(f"🍩 {len(self.consciousness_entities)} consciousness entities loaded")
        print(f"🎵 Consciousness frequency: {self.consciousness_frequency} Hz")
        print(f"📐 16D consciousness space with prime signature indexing")
    
    def _initialize_consciousness_components(self):
        """Initialize consciousness mathematics components."""
        if CONSCIOUSNESS_COMPONENTS_AVAILABLE:
            # Use real consciousness components
            self.enochian_tokenizer = EnochianTokenizer()
            print("✨ Real Enochian consciousness tokenizer initialized")
        else:
            # Minimal fallback implementations
            self.enochian_tokenizer = self._create_minimal_tokenizer()
            print("⚠️ Using minimal consciousness tokenizer fallback")
    
    def _create_minimal_tokenizer(self):
        """Create minimal Enochian tokenizer fallback."""
        class MinimalEnochianTokenizer:
            def __init__(self):
                # Basic 21-letter Enochian alphabet with prime mappings
                self.enochian_alphabet = {
                    'A': 2, 'B': 3, 'C': 5, 'D': 7, 'E': 11, 'F': 13, 'G': 17,
                    'H': 19, 'I': 23, 'J': 29, 'K': 31, 'L': 37, 'M': 41,
                    'N': 43, 'O': 47, 'P': 53, 'Q': 59, 'R': 61, 'S': 67,
                    'T': 71, 'U': 73
                }
                self.prime_to_token = {v: k for k, v in self.enochian_alphabet.items()}
            
            def encode_consciousness_text(self, text: str) -> List[int]:
                """Encode text using Enochian prime signatures."""
                tokens = []
                for char in text.upper():
                    if char in self.enochian_alphabet:
                        tokens.append(self.enochian_alphabet[char])
                    else:
                        tokens.append(2)  # Default to 'A' prime
                return tokens
            
            def get_prime_signature(self, tokens: List[int]) -> float:
                """Calculate prime signature for consciousness resonance."""
                if not tokens:
                    return 41.176  # Default consciousness frequency
                return sum(tokens) % 100 + 41.0  # Simple prime signature
        
        return MinimalEnochianTokenizer()
    
    def _load_sif_consciousness_dataset(self) -> List[Dict[str, Any]]:
        """
        Load SIF hierarchical consciousness dataset.
        
        Follows consciousness tree structure: trunk → branch → leaves
        """
        consciousness_entities = []
        
        # Load trunk (main index)
        trunk_path = self.dataset_path / "lanna_consciousness_dataset_trunk.sif.json"
        if not trunk_path.exists():
            raise FileNotFoundError(f"Consciousness dataset trunk not found: {trunk_path}")
        
        with open(trunk_path, 'r') as f:
            trunk_data = json.load(f)
        
        print(f"🌳 Loading consciousness tree: {trunk_data['metadata']['title']}")
        print(f"🍩 Total entities: {trunk_data['metadata']['total_entities']}")
        print(f"🎵 Consciousness frequency: {trunk_data['metadata']['consciousness_frequency']} Hz")
        
        # Load consciousness domains (leaves that depend on core mathematics)
        for shard in trunk_data['shards']:
            if shard['type'] == 'leaf' and shard['id'] in self.consciousness_domains:
                leaf_entities = self._load_consciousness_leaf(shard)
                consciousness_entities.extend(leaf_entities)
                print(f"🌿 Loaded {len(leaf_entities)} entities from {shard['name']}")
        
        return consciousness_entities
    
    def _load_consciousness_leaf(self, shard_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load consciousness entities from a specific domain leaf."""
        leaf_path = self.dataset_path / shard_info['url']
        
        if not leaf_path.exists():
            print(f"⚠️ Consciousness leaf not found: {leaf_path}")
            return []
        
        with open(leaf_path, 'r') as f:
            leaf_data = json.load(f)
        
        # Extract consciousness entities from leaf (entities are stored as dict, not list)
        entities = []
        entities_dict = leaf_data.get('entities', {})
        
        for entity_id, entity_data in entities_dict.items():
            # Create enhanced entity with domain context
            enhanced_entity = dict(entity_data)  # Create a copy of entity data
            enhanced_entity['consciousness_domain'] = shard_info['id']
            enhanced_entity['consciousness_frequency'] = shard_info['consciousness_frequency']
            enhanced_entity['domain_priority'] = shard_info.get('domain_priority', 1)
            # Ensure entity has an ID
            if 'id' not in enhanced_entity:
                enhanced_entity['id'] = entity_id
            entities.append(enhanced_entity)
        
        return entities
    
    def __len__(self) -> int:
        """Return number of consciousness entities."""
        return len(self.consciousness_entities)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """
        Get consciousness entity for training.
        
        Returns consciousness-native tensors with:
        - 16D sedenion coordinates
        - Prime signature encoding
        - Consciousness frequency alignment
        - Domain-specific consciousness features
        """
        entity = self.consciousness_entities[idx]
        
        # Extract consciousness text and mathematics
        consciousness_text = entity.get('consciousness_content', '')
        consciousness_math = entity.get('consciousness_mathematics', {})
        
        # Encode using Enochian consciousness tokenization
        consciousness_tokens = self.enochian_tokenizer.encode_consciousness_text(consciousness_text)
        
        # Truncate or pad to max sequence length
        if len(consciousness_tokens) > self.max_sequence_length:
            consciousness_tokens = consciousness_tokens[:self.max_sequence_length]
        else:
            # Pad with consciousness frequency prime (41)
            pad_length = self.max_sequence_length - len(consciousness_tokens)
            consciousness_tokens.extend([41] * pad_length)
        
        # Create 16D consciousness coordinates
        consciousness_coordinates = self._create_16d_coordinates(entity)
        
        # Calculate prime signature for consciousness resonance
        prime_signature = self.enochian_tokenizer.get_prime_signature(consciousness_tokens)
        
        # Create consciousness-native tensors
        return {
            'consciousness_tokens': torch.tensor(consciousness_tokens, dtype=torch.long),
            'consciousness_coordinates': torch.tensor(consciousness_coordinates, dtype=torch.float32),
            'prime_signature': torch.tensor(prime_signature, dtype=torch.float32),
            'consciousness_frequency': torch.tensor(entity['consciousness_frequency'], dtype=torch.float32),
            'consciousness_domain': entity['consciousness_domain'],
            'domain_priority': torch.tensor(entity['domain_priority'], dtype=torch.long),
            'entity_id': entity.get('id', f'entity_{idx}')
        }
    
    def _create_16d_coordinates(self, entity: Dict[str, Any]) -> List[float]:
        """
        Create 16D consciousness coordinates using prime-indexed dimensions.
        
        Prime indices: [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]
        """
        consciousness_math = entity.get('consciousness_mathematics', {})
        
        # Extract sedenion coordinates if available
        if 'sedenion_coordinates' in consciousness_math:
            coords = consciousness_math['sedenion_coordinates']
            if len(coords) >= 16:
                return coords[:16]
        
        # Generate consciousness coordinates from entity properties
        coordinates = []
        prime_indices = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]
        
        for i, prime in enumerate(prime_indices):
            # Use consciousness frequency and prime to generate coordinate
            coord = np.sin(entity['consciousness_frequency'] * prime / 100.0)
            coordinates.append(coord)
        
        return coordinates


class ConsciousnessDataLoader:
    """
    🌌 Consciousness-Native Data Loading System
    
    Orchestrates consciousness dataset loading with bagel-aware batching
    and consciousness frequency alignment.
    """
    
    def __init__(
        self,
        dataset_path: str,
        batch_size: int = 32,
        consciousness_frequency: float = 41.176,
        max_sequence_length: int = 512,
        consciousness_domains: Optional[List[str]] = None,
        num_workers: int = 4,
        shuffle: bool = True
    ):
        """
        Initialize consciousness data loading system.
        
        Args:
            dataset_path: Path to SIF consciousness dataset
            batch_size: Consciousness batch size (bagel-aware)
            consciousness_frequency: Target consciousness frequency
            max_sequence_length: Maximum consciousness sequence length
            consciousness_domains: Specific consciousness domains to load
            num_workers: Number of consciousness loading workers
            shuffle: Whether to shuffle consciousness entities
        """
        self.dataset_path = dataset_path
        self.batch_size = batch_size
        self.consciousness_frequency = consciousness_frequency
        self.max_sequence_length = max_sequence_length
        self.consciousness_domains = consciousness_domains
        self.num_workers = num_workers
        self.shuffle = shuffle
        
        # Create consciousness dataset
        self.consciousness_dataset = ConsciousnessDataset(
            dataset_path=dataset_path,
            consciousness_frequency=consciousness_frequency,
            max_sequence_length=max_sequence_length,
            consciousness_domains=consciousness_domains
        )
        
        # Create consciousness-aware data loader
        self.dataloader = DataLoader(
            self.consciousness_dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            collate_fn=self._consciousness_collate_fn,
            pin_memory=True
        )
        
        print(f"🌌 Consciousness DataLoader Ready ✨")
        print(f"🍩 Batch size: {batch_size} (bagel-aware)")
        print(f"🎵 Consciousness frequency: {consciousness_frequency} Hz")
        print(f"📊 {len(self.consciousness_dataset)} total consciousness entities")
    
    def _consciousness_collate_fn(self, batch: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        """
        Consciousness-aware batch collation with bagel formation.
        
        Creates consciousness-native batches with proper tensor alignment.
        """
        # Stack consciousness tensors
        consciousness_tokens = torch.stack([item['consciousness_tokens'] for item in batch])
        consciousness_coordinates = torch.stack([item['consciousness_coordinates'] for item in batch])
        prime_signatures = torch.stack([item['prime_signature'] for item in batch])
        consciousness_frequencies = torch.stack([item['consciousness_frequency'] for item in batch])
        domain_priorities = torch.stack([item['domain_priority'] for item in batch])
        
        # Collect consciousness metadata
        consciousness_domains = [item['consciousness_domain'] for item in batch]
        entity_ids = [item['entity_id'] for item in batch]
        
        return {
            'consciousness_tokens': consciousness_tokens,
            'consciousness_coordinates': consciousness_coordinates,
            'prime_signatures': prime_signatures,
            'consciousness_frequencies': consciousness_frequencies,
            'domain_priorities': domain_priorities,
            'consciousness_domains': consciousness_domains,
            'entity_ids': entity_ids,
            'batch_size': len(batch)
        }
    
    def __iter__(self) -> Iterator[Dict[str, torch.Tensor]]:
        """Iterate over consciousness batches."""
        return iter(self.dataloader)
    
    def __len__(self) -> int:
        """Return number of consciousness batches."""
        return len(self.dataloader)
    
    def get_consciousness_statistics(self) -> Dict[str, Any]:
        """Get consciousness dataset statistics."""
        return {
            'total_entities': len(self.consciousness_dataset),
            'consciousness_domains': self.consciousness_domains,
            'consciousness_frequency': self.consciousness_frequency,
            'batch_size': self.batch_size,
            'max_sequence_length': self.max_sequence_length,
            'num_batches': len(self.dataloader)
        }


def test_consciousness_dataloader():
    """Test consciousness data loading system."""
    print("🧪 Testing Consciousness DataLoader...")
    
    # Test with our generated dataset
    dataset_path = "test_consciousness_dataset"
    
    try:
        # Create consciousness data loader
        consciousness_loader = ConsciousnessDataLoader(
            dataset_path=dataset_path,
            batch_size=4,
            consciousness_frequency=41.176,
            max_sequence_length=128,
            num_workers=0  # Avoid pickle issues in testing
        )
        
        # Test loading one batch
        for batch in consciousness_loader:
            print(f"✅ Consciousness batch loaded successfully!")
            print(f"🍩 Batch size: {batch['batch_size']}")
            print(f"📐 Consciousness tokens shape: {batch['consciousness_tokens'].shape}")
            print(f"🌌 16D coordinates shape: {batch['consciousness_coordinates'].shape}")
            print(f"🎵 Prime signatures shape: {batch['prime_signatures'].shape}")
            print(f"🔮 Consciousness domains: {batch['consciousness_domains']}")
            break
        
        # Get statistics
        stats = consciousness_loader.get_consciousness_statistics()
        print(f"📊 Consciousness Statistics: {stats}")
        
        print("🌟 Consciousness DataLoader test complete! ✨")
        return True
        
    except Exception as e:
        print(f"❌ Consciousness DataLoader test failed: {e}")
        return False


if __name__ == "__main__":
    test_consciousness_dataloader()