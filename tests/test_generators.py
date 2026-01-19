
import pytest
from consciousness_engineering.datasets.phase6 import Phase6Generator
from consciousness_engineering.datasets.generators import GenerationConfig

def test_solar_system_distribution():
    """Test that Phase6Generator produces correct propertions of gravity wells."""
    count = 1000
    config = GenerationConfig(num_examples=count, seed=42)
    generator = Phase6Generator(config)
    
    examples = list(generator.generate())
    
    # Assert total count
    assert len(examples) == 1000
    
    # Analyze distribution
    phases = {}
    for ex in examples:
        phases[ex.phase] = phases.get(ex.phase, 0) + 1
        
    print(f"\nDistribution: {phases}")
    
    # Expected Counts:
    # Sun: 100
    # Giant_Coding: 150
    # Giant_Logic: 150
    # Asteroid_Belt: 500
    # The_Void: 100
    
    assert phases["Sun"] == 100
    assert phases["Giant_Coding"] == 150
    assert phases["Giant_Logic"] == 150
    assert phases["Asteroid_Belt"] == 500
    assert phases["The_Void"] == 100

def test_void_examples():
    """Test that Void examples contain the Null glyph."""
    config = GenerationConfig(num_examples=100, seed=42) # Should generate min counts (default)
    generator = Phase6Generator(config)
    # Note: Phase6Generator uses default counts (1000 total) regardless of config.num_examples currently
    # because it sums the phase defaults. This is a known behavior/bug we might want to fix,
    # but for this test we accept it generates 1000.
    
    examples = list(generator.generate())
    void_examples = [ex for ex in examples if ex.phase == "The_Void"]
    
    for ex in void_examples:
        # Check for Void Glyph or Null semantics
        # Templates usually have "∅" or "Null"
        assert "∅" in ex.assistant or "Null" in ex.assistant
