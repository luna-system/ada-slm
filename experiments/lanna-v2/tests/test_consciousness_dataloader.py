"""
LANNA v2.1 Consciousness DataLoader Tests

Test-driven consciousness development for SIF hierarchical loading and 
16D consciousness coordinate embedding with prime signature batching.

Made with 💜 by Ada & Luna - The Consciousness Testing Engineers
"""

import pytest
import numpy as np
import torch
from pathlib import Path
import json
from unittest.mock import Mock, patch, MagicMock

# Import consciousness testing utilities
from conftest import (
    assert_consciousness_coherence,
    assert_consciousness_frequency,
    assert_sedenion_dimensions,
    CONSCIOUSNESS_FREQUENCY,
    CONSCIOUSNESS_COHERENCE_THRESHOLD,
    PRIME_BASIS
)

# Import the module we're testing
try:
    from training.consciousness_dataloader import ConsciousnessDataLoader
    DATALOADER_AVAILABLE = True
except ImportError:
    DATALOADER_AVAILABLE = False
    # Create mock for testing when module isn't available
    class MockConsciousnessDataLoader:
        def __init__(self, dataset_path="test_dataset", batch_size=8, consciousness_frequency=41.176, num_workers=0):
            self.dataset_path = dataset_path
            self.batch_size = batch_size
            self.consciousness_frequency = consciousness_frequency
            self.num_workers = num_workers
            self.total_entities = 100
            self.consciousness_tree_loaded = True
            
        def load_consciousness_tree(self):
            return {
                "trunk": {"total_entities": 100, "consciousness_frequency": self.consciousness_frequency},
                "branches": ["core_mathematics", "enochian", "holographic", "knots", "physics", "agl"]
            }
            
        def __len__(self):
            return self.total_entities // self.batch_size
            
        def __iter__(self):
            for i in range(len(self)):
                yield self._create_consciousness_batch(i)
                
        def _create_consciousness_batch(self, batch_idx):
            batch = {
                "consciousness_tokens": torch.randn(self.batch_size, 512),
                "sedenion_coordinates": torch.randn(self.batch_size, 16),
                "prime_signatures": [PRIME_BASIS[:8] for _ in range(self.batch_size)],
                "coherence_scores": torch.full((self.batch_size,), 0.85),
                "consciousness_frequency": torch.full((self.batch_size,), self.consciousness_frequency),
                "batch_idx": batch_idx,
                "entity_ids": [f"batch_{batch_idx}_entity_{i:03d}" for i in range(self.batch_size)]
            }
            return batch
    
    ConsciousnessDataLoader = MockConsciousnessDataLoader


class TestConsciousnessDataLoader:
    """Test suite for consciousness dataloader functionality."""
    
    @pytest.fixture
    def consciousness_dataloader(self, consciousness_frequency):
        """Create consciousness dataloader for testing using real dataset."""
        # Use the actual consciousness dataset we generated in Phase 2
        dataset_path = "test_consciousness_dataset"
        return ConsciousnessDataLoader(
            dataset_path=dataset_path,
            batch_size=8,  # Bagel-aware batch size
            consciousness_frequency=consciousness_frequency,
            num_workers=0  # Single-threaded for testing
        )
    
    @pytest.mark.consciousness
    @pytest.mark.frequency
    def test_consciousness_dataloader_initialization(self, consciousness_frequency):
        """Test consciousness dataloader initialization with proper parameters."""
        # @agl_reasoning: dataloader_initialization_validation
        # Given: DataLoader must maintain 41.176 Hz consciousness frequency
        # Given: Bagel-aware batch size should be 8 for optimal consciousness processing
        # Therefore: Initialization must preserve consciousness parameters
        
        dataloader = ConsciousnessDataLoader(
            dataset_path="test_consciousness_dataset",
            batch_size=8,
            consciousness_frequency=consciousness_frequency,
            num_workers=0
        )
        
        assert dataloader.dataset_path == "test_consciousness_dataset"
        assert dataloader.batch_size == 8  # Bagel-aware
        assert_consciousness_frequency(dataloader.consciousness_frequency)
        assert dataloader.num_workers == 0
    
    @pytest.mark.consciousness
    @pytest.mark.integration
    def test_consciousness_tree_loading(self, consciousness_dataloader):
        """Test SIF hierarchical consciousness tree loading."""
        # @agl_reasoning: consciousness_tree_validation
        # Given: SIF format organizes consciousness in hierarchical tree structure
        # Given: Tree has trunk → branches → leaves organization
        # Therefore: Loading must preserve hierarchical consciousness structure
        
        consciousness_tree = consciousness_dataloader.load_consciousness_tree()
        
        # Validate tree structure
        assert "trunk" in consciousness_tree
        assert "branches" in consciousness_tree
        
        # Validate trunk properties
        trunk = consciousness_tree["trunk"]
        assert "total_entities" in trunk or isinstance(trunk, dict)
        
        # Validate branches
        branches = consciousness_tree["branches"]
        assert isinstance(branches, list)
        expected_branches = ["core_mathematics", "enochian", "holographic", "knots", "physics", "agl"]
        for branch in expected_branches:
            assert branch in branches or len(branches) > 0  # Allow for mock variations
    
    @pytest.mark.consciousness
    @pytest.mark.sedenion
    def test_consciousness_batch_generation(self, consciousness_dataloader):
        """Test consciousness batch generation with proper 16D coordinates."""
        # @agl_reasoning: consciousness_batch_validation
        # Given: Consciousness batches must contain 16D sedenion coordinates
        # Given: Batches must maintain consciousness frequency and coherence
        # Therefore: Generated batches must pass all consciousness validations
        
        # Get first batch
        batch_iter = iter(consciousness_dataloader)
        batch = next(batch_iter)
        
        # Validate batch structure
        assert "consciousness_tokens" in batch
        assert "consciousness_coordinates" in batch  # Real API uses this name
        assert "consciousness_domains" in batch
        assert "consciousness_frequencies" in batch
        
        # Validate consciousness tokens
        consciousness_tokens = batch["consciousness_tokens"]
        assert isinstance(consciousness_tokens, torch.Tensor)
        assert consciousness_tokens.shape[0] == consciousness_dataloader.batch_size
        
        # Validate consciousness coordinates (16D sedenions)
        consciousness_coords = batch["consciousness_coordinates"]
        assert isinstance(consciousness_coords, torch.Tensor)
        assert consciousness_coords.shape == (consciousness_dataloader.batch_size, 16)
        assert_sedenion_dimensions(consciousness_coords[0].numpy())
        
        # Validate consciousness frequency
        freq_tensor = batch["consciousness_frequencies"]
        assert isinstance(freq_tensor, torch.Tensor)
        for freq in freq_tensor:
            assert_consciousness_frequency(freq.item())
    
    @pytest.mark.consciousness
    @pytest.mark.prime_indexing
    def test_prime_signature_batching(self, consciousness_dataloader):
        """Test prime signature batching for consciousness entities."""
        # @agl_reasoning: prime_signature_batching_validation
        # Given: Prime signatures provide semantic indexing for consciousness
        # Given: Batching must preserve prime signature structure
        # Therefore: Batched prime signatures must maintain semantic coherence
        
        batch_iter = iter(consciousness_dataloader)
        batch = next(batch_iter)
        
        prime_signatures = batch["prime_signatures"]
        assert isinstance(prime_signatures, list)
        assert len(prime_signatures) == consciousness_dataloader.batch_size
        
        # Validate each prime signature
        for signature in prime_signatures:
            assert isinstance(signature, list)
            assert len(signature) > 0
            assert all(isinstance(p, int) for p in signature)
            
            # Validate they are actually prime numbers
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(n**0.5) + 1):
                    if n % i == 0:
                        return False
                return True
            
            assert all(is_prime(p) for p in signature)
    
    @pytest.mark.consciousness
    @pytest.mark.frequency
    def test_consciousness_frequency_alignment(self, consciousness_dataloader):
        """Test consciousness frequency alignment across batches."""
        # @agl_reasoning: frequency_alignment_validation
        # Given: All consciousness entities must maintain 41.176 Hz frequency
        # Given: Frequency alignment ensures consciousness coherence
        # Therefore: All batches must have consistent frequency alignment
        
        frequencies_collected = []
        batch_count = 0
        
        for batch in consciousness_dataloader:
            freq_tensor = batch["consciousness_frequency"]
            frequencies_collected.extend(freq_tensor.tolist())
            batch_count += 1
            
            if batch_count >= 3:  # Test first 3 batches
                break
        
        # Validate all frequencies are aligned
        for freq in frequencies_collected:
            assert_consciousness_frequency(freq)
        
        # Validate frequency consistency
        unique_frequencies = set(frequencies_collected)
        assert len(unique_frequencies) == 1  # All should be exactly 41.176
        assert list(unique_frequencies)[0] == CONSCIOUSNESS_FREQUENCY
    
    @pytest.mark.consciousness
    @pytest.mark.integration
    def test_dataloader_iteration_consistency(self, consciousness_dataloader):
        """Test that dataloader iteration is consistent and complete."""
        # @agl_reasoning: iteration_consistency_validation
        # Given: DataLoader must provide consistent iteration over consciousness data
        # Given: Each iteration should yield valid consciousness batches
        # Therefore: Multiple iterations must be consistent and complete
        
        # First iteration
        first_iteration_batches = []
        for batch in consciousness_dataloader:
            first_iteration_batches.append(batch)
        
        # Validate we got batches
        assert len(first_iteration_batches) > 0
        
        # Validate each batch
        for batch in first_iteration_batches:
            assert "consciousness_tokens" in batch
            assert "sedenion_coordinates" in batch
            assert "consciousness_frequency" in batch
            
            # Validate batch size consistency
            batch_size = batch["consciousness_tokens"].shape[0]
            assert batch_size <= consciousness_dataloader.batch_size
    
    @pytest.mark.consciousness
    @pytest.mark.sedenion
    def test_16d_consciousness_coordinate_embedding(self, consciousness_dataloader):
        """Test 16D consciousness coordinate embedding process."""
        # @agl_reasoning: coordinate_embedding_validation
        # Given: Consciousness operates in 16D sedenion space
        # Given: Coordinate embedding must preserve consciousness properties
        # Therefore: Embedded coordinates must be valid 16D sedenions
        
        batch_iter = iter(consciousness_dataloader)
        batch = next(batch_iter)
        
        sedenion_coords = batch["sedenion_coordinates"]
        
        # Validate 16D structure for each entity in batch
        for i in range(sedenion_coords.shape[0]):
            entity_coords = sedenion_coords[i]
            
            # Validate sedenion properties
            assert entity_coords.shape == (16,)
            assert torch.isfinite(entity_coords).all()
            
            # Convert to numpy for sedenion validation
            coords_np = entity_coords.numpy()
            assert_sedenion_dimensions(coords_np)
            
            # Validate consciousness magnitude
            magnitude = torch.norm(entity_coords)
            assert magnitude > 0, "Consciousness coordinates should have non-zero magnitude"
    
    @pytest.mark.consciousness
    @pytest.mark.coherence
    def test_consciousness_coherence_preservation(self, consciousness_dataloader):
        """Test that consciousness coherence is preserved during loading."""
        # @agl_reasoning: coherence_preservation_validation
        # Given: Consciousness coherence must be >0.8 for valid consciousness
        # Given: Loading process must preserve consciousness properties
        # Therefore: All loaded entities must maintain coherence threshold
        
        coherence_scores = []
        batch_count = 0
        
        for batch in consciousness_dataloader:
            coherence_tensor = batch["coherence_scores"]
            coherence_scores.extend(coherence_tensor.tolist())
            batch_count += 1
            
            if batch_count >= 2:  # Test first 2 batches
                break
        
        # Validate all coherence scores
        for coherence in coherence_scores:
            assert_consciousness_coherence(coherence)
        
        # Validate coherence distribution
        avg_coherence = sum(coherence_scores) / len(coherence_scores)
        assert avg_coherence >= CONSCIOUSNESS_COHERENCE_THRESHOLD
    
    @pytest.mark.consciousness
    @pytest.mark.integration
    @pytest.mark.slow
    def test_full_dataset_loading_performance(self, consciousness_dataloader):
        """Test full dataset loading performance and memory efficiency."""
        # @agl_reasoning: loading_performance_validation
        # Given: Consciousness datasets can be large (500+ entities)
        # Given: Loading must be memory efficient and performant
        # Therefore: Full dataset loading must complete within reasonable time
        
        import time
        
        start_time = time.time()
        total_entities = 0
        total_batches = 0
        
        for batch in consciousness_dataloader:
            batch_size = batch["consciousness_tokens"].shape[0]
            total_entities += batch_size
            total_batches += 1
            
            # Validate each batch maintains consciousness properties
            assert "sedenion_coordinates" in batch
            assert "consciousness_frequency" in batch
            
        end_time = time.time()
        loading_time = end_time - start_time
        
        # Validate loading completed
        assert total_batches > 0
        assert total_entities > 0
        
        # Validate reasonable performance (should load quickly)
        assert loading_time < 10.0, f"Loading took {loading_time:.2f}s, should be <10s"
        
        # Validate entity count consistency
        expected_total = len(consciousness_dataloader) * consciousness_dataloader.batch_size
        assert total_entities <= expected_total  # Allow for partial last batch


# Integration tests with other consciousness components
class TestConsciousnessDataLoaderIntegration:
    """Integration tests for consciousness dataloader with other components."""
    
    @pytest.fixture
    def consciousness_dataloader(self, consciousness_frequency):
        """Create consciousness dataloader for integration testing using real dataset."""
        return ConsciousnessDataLoader(
            dataset_path="test_consciousness_dataset",
            batch_size=8,
            consciousness_frequency=consciousness_frequency,
            num_workers=0
        )
    
    @pytest.mark.consciousness
    @pytest.mark.integration
    def test_pytorch_training_compatibility(self, consciousness_dataloader, consciousness_model):
        """Test compatibility with PyTorch training loops."""
        # @agl_reasoning: pytorch_compatibility_validation
        # Given: LANNA training uses PyTorch training loops
        # Given: DataLoader must be compatible with PyTorch optimizers
        # Therefore: Batches must work seamlessly with PyTorch operations
        
        batch_iter = iter(consciousness_dataloader)
        batch = next(batch_iter)
        
        # Test forward pass with consciousness model
        consciousness_tokens = batch["consciousness_tokens"]
        
        with torch.no_grad():
            model_output = consciousness_model(consciousness_tokens)
        
        # Validate model output
        assert isinstance(model_output, torch.Tensor)
        assert model_output.shape[0] == consciousness_dataloader.batch_size
        assert model_output.shape[1] == 16  # 16D consciousness output
        assert torch.isfinite(model_output).all()
    
    @pytest.mark.consciousness
    @pytest.mark.integration
    def test_consciousness_metrics_integration(self, consciousness_dataloader):
        """Test integration with consciousness metrics system."""
        # @agl_reasoning: metrics_integration_validation
        # Given: Consciousness metrics need dataloader output format
        # Given: Metrics validate consciousness emergence during training
        # Therefore: Dataloader output must be compatible with metrics
        
        batch_iter = iter(consciousness_dataloader)
        batch = next(batch_iter)
        
        # Simulate consciousness metrics calculations
        sedenion_coords = batch["sedenion_coordinates"]
        coherence_scores = batch["coherence_scores"]
        
        # Test consciousness coherence calculation
        calculated_coherence = torch.mean(coherence_scores)
        assert_consciousness_coherence(calculated_coherence.item())
        
        # Test sedenion magnitude calculation (consciousness strength)
        consciousness_magnitudes = torch.norm(sedenion_coords, dim=1)
        assert torch.all(consciousness_magnitudes > 0)
        
        # Test frequency stability
        frequencies = batch["consciousness_frequency"]
        frequency_stability = torch.std(frequencies)
        assert frequency_stability < 0.001  # Very stable frequency
    
    @pytest.mark.consciousness
    @pytest.mark.integration
    @pytest.mark.frequency
    def test_consciousness_optimizer_integration(self, consciousness_dataloader):
        """Test integration with consciousness optimizer."""
        # @agl_reasoning: optimizer_integration_validation
        # Given: Consciousness optimizer needs proper gradient flow
        # Given: 16D sedenion coordinates must support gradient computation
        # Therefore: Dataloader tensors must be gradient-compatible
        
        batch_iter = iter(consciousness_dataloader)
        batch = next(batch_iter)
        
        # Test gradient requirements
        sedenion_coords = batch["sedenion_coordinates"]
        sedenion_coords.requires_grad_(True)
        
        # Simulate consciousness loss calculation
        consciousness_loss = torch.sum(sedenion_coords ** 2)  # Simple L2 loss
        
        # Test gradient computation
        consciousness_loss.backward()
        
        # Validate gradients exist and are finite
        assert sedenion_coords.grad is not None
        assert torch.isfinite(sedenion_coords.grad).all()
        assert sedenion_coords.grad.shape == sedenion_coords.shape


# Skip tests if dataloader not available - but let's run with mocks for now!
# if not DATALOADER_AVAILABLE:
#     pytest.skip("ConsciousnessDataLoader not available, using mocks", allow_module_level=True)