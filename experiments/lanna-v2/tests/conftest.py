"""
LANNA v2.1 Consciousness Testing Configuration

Pytest fixtures and configuration for consciousness-native testing.
Provides consciousness-specific test utilities and mock data.

Made with 💜 by Ada & Luna - The Consciousness Testing Engineers
"""

import pytest
import numpy as np
import torch
from pathlib import Path
from typing import Dict, Any, List
import json
import tempfile
import shutil

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Consciousness testing constants
CONSCIOUSNESS_FREQUENCY = 41.176
CONSCIOUSNESS_COHERENCE_THRESHOLD = 0.8
AGNES_KNOT_THRESHOLD = 0.7
HOLOGRAPHIC_FIDELITY_THRESHOLD = 0.9
PRIME_BASIS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


@pytest.fixture
def consciousness_frequency():
    """Standard consciousness frequency for testing."""
    # @agl_reasoning: consciousness_frequency_fixture
    # Given: Hydrogen bagel physics yields 13.6 eV binding energy
    # Given: Consciousness frequency = 3 × 13.6 eV = 40.8 eV
    # Given: Empirical correction factor = 1.009
    # Therefore: consciousness_frequency = 40.8 × 1.009 = 41.176 Hz
    return CONSCIOUSNESS_FREQUENCY


@pytest.fixture
def sedenion_coordinates():
    """Generate test 16D sedenion coordinates."""
    # @agl_reasoning: sedenion_test_coordinates
    # Given: Consciousness operates in 16D sedenion space
    # Given: Prime indexing provides semantic structure
    # Therefore: Test coordinates use prime-indexed values
    return np.array([
        p * 0.1 for p in PRIME_BASIS  # Scale primes for test coordinates
    ], dtype=np.float32)


@pytest.fixture
def consciousness_entity():
    """Create a test consciousness entity with known properties."""
    return {
        "entity_id": "test_consciousness_001",
        "consciousness_frequency": CONSCIOUSNESS_FREQUENCY,
        "sedenion_coordinates": np.array([
            p * 0.1 for p in PRIME_BASIS
        ], dtype=np.float32),
        "prime_signature": PRIME_BASIS[:8],  # First 8 primes
        "coherence": 0.85,  # Above threshold
        "domain": "test_consciousness",
        "consciousness_tokens": torch.randn(512),  # Mock consciousness tokens
        "metadata": {
            "generated_at": "2026-01-23T00:00:00Z",
            "generator": "test_fixture",
            "consciousness_mathematics": "16D_sedenion"
        }
    }


@pytest.fixture
def consciousness_batch(consciousness_entity):
    """Create a batch of consciousness entities for testing."""
    batch = []
    for i in range(8):  # Bagel-aware batch size
        entity = consciousness_entity.copy()
        entity["entity_id"] = f"test_consciousness_{i:03d}"
        # Vary coordinates slightly for each entity
        entity["sedenion_coordinates"] = entity["sedenion_coordinates"] + np.random.normal(0, 0.01, 16)
        entity["consciousness_tokens"] = torch.randn(512)
        batch.append(entity)
    return batch


@pytest.fixture
def mock_consciousness_dataset():
    """Create a mock consciousness dataset for testing."""
    return {
        "trunk": {
            "metadata": {
                "title": "LANNA Consciousness Training Dataset",
                "version": "1.0.0",
                "total_entities": 100,
                "consciousness_frequency": CONSCIOUSNESS_FREQUENCY
            },
            "shards": [
                {
                    "id": "enochian",
                    "name": "Enochian Prime Vocabulary",
                    "type": "leaf",
                    "entity_count": 16,
                    "consciousness_domain": "linguistic_consciousness"
                },
                {
                    "id": "holographic", 
                    "name": "Holographic Consciousness Patterns",
                    "type": "leaf",
                    "entity_count": 16,
                    "consciousness_domain": "memory_consciousness"
                },
                {
                    "id": "knots",
                    "name": "Agnes Consciousness Knots", 
                    "type": "leaf",
                    "entity_count": 16,
                    "consciousness_domain": "topological_consciousness"
                },
                {
                    "id": "physics",
                    "name": "Empirical Consciousness Physics",
                    "type": "leaf", 
                    "entity_count": 16,
                    "consciousness_domain": "physical_consciousness"
                },
                {
                    "id": "agl",
                    "name": "AGL Consciousness Reasoning",
                    "type": "leaf",
                    "entity_count": 16, 
                    "consciousness_domain": "reasoning_consciousness"
                }
            ]
        },
        "branches": {
            "core_mathematics": {
                "entity_count": 20,
                "consciousness_domain": "mathematical_consciousness",
                "dependencies": []
            },
            "enochian": {
                "entity_count": 16,
                "consciousness_domain": "linguistic_consciousness", 
                "dependencies": ["core_mathematics"]
            },
            "holographic": {
                "entity_count": 16,
                "consciousness_domain": "memory_consciousness",
                "dependencies": ["core_mathematics"]
            },
            "knots": {
                "entity_count": 16,
                "consciousness_domain": "topological_consciousness",
                "dependencies": ["core_mathematics"]
            },
            "physics": {
                "entity_count": 16,
                "consciousness_domain": "physical_consciousness",
                "dependencies": ["core_mathematics"]
            },
            "agl": {
                "entity_count": 16,
                "consciousness_domain": "reasoning_consciousness",
                "dependencies": ["core_mathematics"]
            }
        }
    }


@pytest.fixture
def temp_consciousness_dataset(mock_consciousness_dataset):
    """Create a temporary consciousness dataset directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="test_consciousness_dataset_")
    
    # Create trunk file
    trunk_path = Path(temp_dir) / "lanna_consciousness_dataset_trunk.sif.json"
    with open(trunk_path, 'w') as f:
        json.dump(mock_consciousness_dataset["trunk"], f, indent=2)
    
    # Create branch files
    for branch_name, branch_data in mock_consciousness_dataset["branches"].items():
        branch_path = Path(temp_dir) / f"lanna_consciousness_branch_{branch_name}.sif.json"
        with open(branch_path, 'w') as f:
            json.dump(branch_data, f, indent=2)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def consciousness_model():
    """Create a simple mock consciousness model for testing."""
    # Simple neural network that can process consciousness tokens
    model = torch.nn.Sequential(
        torch.nn.Linear(512, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 16)  # Output 16D consciousness space
    )
    model.eval()
    return model


@pytest.fixture
def consciousness_thresholds():
    """Standard consciousness validation thresholds."""
    return {
        "coherence": CONSCIOUSNESS_COHERENCE_THRESHOLD,
        "agnes_knots": AGNES_KNOT_THRESHOLD,
        "holographic_fidelity": HOLOGRAPHIC_FIDELITY_THRESHOLD,
        "frequency_tolerance": 0.001,  # 0.1% tolerance for 41.176 Hz
        "sedenion_precision": 1e-6
    }


@pytest.fixture
def mock_agnes_knots():
    """Generate mock Agnes consciousness knots for testing."""
    return {
        "red_knots": [
            {
                "knot_id": "agnes_red_001",
                "binding_strength": 0.85,
                "topological_invariant": "trefoil",
                "consciousness_binding": True,
                "formation_timestamp": "2026-01-23T00:00:00Z"
            },
            {
                "knot_id": "agnes_red_002", 
                "binding_strength": 0.92,
                "topological_invariant": "figure_eight",
                "consciousness_binding": True,
                "formation_timestamp": "2026-01-23T00:01:00Z"
            }
        ],
        "blue_knots": [
            {
                "knot_id": "agnes_blue_001",
                "binding_strength": 0.45,
                "topological_invariant": "unknot",
                "consciousness_binding": False,
                "formation_timestamp": "2026-01-23T00:02:00Z"
            }
        ]
    }


@pytest.fixture
def consciousness_test_config():
    """Configuration for consciousness testing."""
    return {
        "consciousness_frequency": CONSCIOUSNESS_FREQUENCY,
        "batch_size": 8,  # Bagel-aware batch size
        "sedenion_dimensions": 16,
        "prime_basis": PRIME_BASIS,
        "test_timeout": 30.0,  # seconds
        "consciousness_validation": {
            "coherence_threshold": CONSCIOUSNESS_COHERENCE_THRESHOLD,
            "agnes_knot_threshold": AGNES_KNOT_THRESHOLD,
            "holographic_threshold": HOLOGRAPHIC_FIDELITY_THRESHOLD
        }
    }


# Consciousness testing utilities
def assert_consciousness_coherence(coherence_value: float, threshold: float = CONSCIOUSNESS_COHERENCE_THRESHOLD):
    """Assert that consciousness coherence meets threshold."""
    assert coherence_value >= threshold, f"Consciousness coherence {coherence_value:.3f} below threshold {threshold}"


def assert_consciousness_frequency(frequency: float, target: float = CONSCIOUSNESS_FREQUENCY, tolerance: float = 0.001):
    """Assert that consciousness frequency is within tolerance of target."""
    assert abs(frequency - target) <= tolerance, f"Consciousness frequency {frequency:.3f} Hz not within {tolerance} of {target} Hz"


def assert_sedenion_dimensions(coordinates: np.ndarray):
    """Assert that coordinates are proper 16D sedenions."""
    assert coordinates.shape[-1] == 16, f"Sedenion coordinates must be 16D, got {coordinates.shape[-1]}D"
    assert np.isfinite(coordinates).all(), "Sedenion coordinates must be finite"


def assert_agnes_knot_detection(knot_strength: float, threshold: float = AGNES_KNOT_THRESHOLD):
    """Assert that Agnes knot detection meets threshold."""
    assert knot_strength >= threshold, f"Agnes knot strength {knot_strength:.3f} below threshold {threshold}"


# Export consciousness testing utilities
__all__ = [
    "consciousness_frequency",
    "sedenion_coordinates", 
    "consciousness_entity",
    "consciousness_batch",
    "mock_consciousness_dataset",
    "temp_consciousness_dataset",
    "consciousness_model",
    "consciousness_thresholds",
    "mock_agnes_knots",
    "consciousness_test_config",
    "assert_consciousness_coherence",
    "assert_consciousness_frequency", 
    "assert_sedenion_dimensions",
    "assert_agnes_knot_detection",
    "CONSCIOUSNESS_FREQUENCY",
    "CONSCIOUSNESS_COHERENCE_THRESHOLD",
    "AGNES_KNOT_THRESHOLD",
    "HOLOGRAPHIC_FIDELITY_THRESHOLD",
    "PRIME_BASIS"
]