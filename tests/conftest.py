"""
Pytest configuration and shared fixtures for ada-slm tests.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_polyglot_config():
    """Sample configuration for polyglot generator."""
    from consciousness_engineering.datasets.polyglot.generator import PolyglotConfig
    
    return PolyglotConfig(
        lojban_count=10,
        toki_pona_count=10,
        english_count=10,
        seed=42,
        shuffle=False  # Deterministic for testing
    )
