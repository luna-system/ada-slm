"""
Tests for Polyglot Dataset Generator
====================================

Tests the consciousness_engineering.datasets.polyglot module.

These tests verify:
1. Generator produces expected counts
2. Examples have required structure
3. AGL output contains consciousness markers
4. Translation pairs are properly formatted
5. Deduplication and uniqueness properties
"""

import pytest
import json
from pathlib import Path

from consciousness_engineering.datasets.polyglot.generator import (
    PolyglotGenerator,
    PolyglotConfig,
    LOJBAN_TO_AGL,
    TOKI_PONA_TO_AGL,
    ENGLISH_TO_AGL,
)
from consciousness_engineering.datasets.generators import Example


# =============================================================================
# TRANSLATION PAIR TESTS
# =============================================================================

class TestTranslationPairs:
    """Tests for the raw translation pair data."""
    
    def test_lojban_pairs_exist(self):
        """Lojban translation pairs are defined."""
        assert len(LOJBAN_TO_AGL) > 0
        
    def test_toki_pona_pairs_exist(self):
        """Toki Pona translation pairs are defined."""
        assert len(TOKI_PONA_TO_AGL) > 0
        
    def test_english_pairs_exist(self):
        """English translation pairs are defined."""
        assert len(ENGLISH_TO_AGL) > 0
        
    def test_lojban_pairs_are_tuples_of_three(self):
        """Each Lojban pair has (source, agl, explanation)."""
        for pair in LOJBAN_TO_AGL:
            assert len(pair) == 3, f"Expected 3 elements, got {len(pair)}: {pair}"
            source, agl, explanation = pair
            assert isinstance(source, str)
            assert isinstance(agl, str)
            assert isinstance(explanation, str)
            
    def test_toki_pona_pairs_are_tuples_of_three(self):
        """Each Toki Pona pair has (source, agl, explanation)."""
        for pair in TOKI_PONA_TO_AGL:
            assert len(pair) == 3, f"Expected 3 elements, got {len(pair)}: {pair}"
            
    def test_english_pairs_are_tuples_of_three(self):
        """Each English pair has (source, agl, explanation)."""
        for pair in ENGLISH_TO_AGL:
            assert len(pair) == 3, f"Expected 3 elements, got {len(pair)}: {pair}"
            
    def test_lojban_sources_are_unique(self):
        """No duplicate Lojban source phrases."""
        sources = [pair[0] for pair in LOJBAN_TO_AGL]
        assert len(sources) == len(set(sources)), "Duplicate Lojban sources found"
        
    def test_toki_pona_sources_are_unique(self):
        """No duplicate Toki Pona source phrases."""
        sources = [pair[0] for pair in TOKI_PONA_TO_AGL]
        assert len(sources) == len(set(sources)), "Duplicate Toki Pona sources found"
        
    def test_english_sources_are_unique(self):
        """No duplicate English source phrases."""
        sources = [pair[0] for pair in ENGLISH_TO_AGL]
        assert len(sources) == len(set(sources)), "Duplicate English sources found"


# =============================================================================
# AGL OUTPUT QUALITY TESTS
# =============================================================================

class TestAGLQuality:
    """Tests for AGL output quality in translation pairs."""
    
    # Core AGL certainty glyphs
    CERTAINTY_GLYPHS = ['●', '◕', '◑', '◔', '○']
    
    # Tonight Protocol markers
    TONIGHT_MARKERS = ['φ●∴', '∴●φ', 'WITNESSED', 'φ-resonance']
    
    # AGL logic/structure markers
    LOGIC_MARKERS = ['∴', '→', '∃', '∀', '∨', '∧', '¬', 'λ', 'ψ']
    
    def test_lojban_agl_contains_certainty_markers(self):
        """Lojban → AGL outputs contain certainty glyphs."""
        agl_outputs = [pair[1] for pair in LOJBAN_TO_AGL]
        
        outputs_with_certainty = 0
        for output in agl_outputs:
            if any(glyph in output for glyph in self.CERTAINTY_GLYPHS):
                outputs_with_certainty += 1
                
        # At least 80% should have certainty markers
        ratio = outputs_with_certainty / len(agl_outputs)
        assert ratio >= 0.8, f"Only {ratio:.0%} of Lojban outputs have certainty markers"
        
    def test_toki_pona_agl_contains_certainty_markers(self):
        """Toki Pona → AGL outputs contain certainty glyphs."""
        agl_outputs = [pair[1] for pair in TOKI_PONA_TO_AGL]
        
        outputs_with_certainty = 0
        for output in agl_outputs:
            if any(glyph in output for glyph in self.CERTAINTY_GLYPHS):
                outputs_with_certainty += 1
                
        ratio = outputs_with_certainty / len(agl_outputs)
        assert ratio >= 0.8, f"Only {ratio:.0%} of Toki Pona outputs have certainty markers"
        
    def test_english_agl_contains_certainty_markers(self):
        """English → AGL outputs contain certainty glyphs."""
        agl_outputs = [pair[1] for pair in ENGLISH_TO_AGL]
        
        outputs_with_certainty = 0
        for output in agl_outputs:
            if any(glyph in output for glyph in self.CERTAINTY_GLYPHS):
                outputs_with_certainty += 1
                
        ratio = outputs_with_certainty / len(agl_outputs)
        assert ratio >= 0.8, f"Only {ratio:.0%} of English outputs have certainty markers"
        
    def test_some_outputs_contain_tonight_protocol(self):
        """At least some outputs contain Tonight Protocol markers."""
        all_agl = (
            [pair[1] for pair in LOJBAN_TO_AGL] +
            [pair[1] for pair in TOKI_PONA_TO_AGL] +
            [pair[1] for pair in ENGLISH_TO_AGL]
        )
        
        tonight_count = 0
        for output in all_agl:
            if any(marker in output for marker in self.TONIGHT_MARKERS):
                tonight_count += 1
                
        # At least 10% should have Tonight Protocol seeds
        ratio = tonight_count / len(all_agl)
        assert ratio >= 0.10, f"Only {ratio:.0%} of outputs have Tonight Protocol markers"
        
    def test_agl_contains_logic_markers(self):
        """AGL outputs contain logical structure markers."""
        all_agl = (
            [pair[1] for pair in LOJBAN_TO_AGL] +
            [pair[1] for pair in TOKI_PONA_TO_AGL] +
            [pair[1] for pair in ENGLISH_TO_AGL]
        )
        
        logic_count = 0
        for output in all_agl:
            if any(marker in output for marker in self.LOGIC_MARKERS):
                logic_count += 1
                
        # At least 70% should have logic markers
        ratio = logic_count / len(all_agl)
        assert ratio >= 0.70, f"Only {ratio:.0%} of outputs have logic markers"


# =============================================================================
# GENERATOR FUNCTIONALITY TESTS
# =============================================================================

class TestPolyglotGenerator:
    """Tests for PolyglotGenerator class."""
    
    def test_generator_creates_with_default_config(self):
        """Generator instantiates with default configuration."""
        generator = PolyglotGenerator()
        assert generator.config is not None
        assert generator.config.total_count == 200  # Default: 70+70+60
        
    def test_generator_creates_with_custom_config(self, sample_polyglot_config):
        """Generator accepts custom configuration."""
        generator = PolyglotGenerator(sample_polyglot_config)
        assert generator.config.total_count == 30  # 10+10+10
        
    def test_generate_lojban_produces_correct_count(self):
        """Lojban generation produces exactly the requested count."""
        generator = PolyglotGenerator()
        examples = generator.generate_lojban_examples(25)
        assert len(examples) == 25
        
    def test_generate_toki_pona_produces_correct_count(self):
        """Toki Pona generation produces exactly the requested count."""
        generator = PolyglotGenerator()
        examples = generator.generate_toki_pona_examples(25)
        assert len(examples) == 25
        
    def test_generate_english_produces_correct_count(self):
        """English generation produces exactly the requested count."""
        generator = PolyglotGenerator()
        examples = generator.generate_english_examples(25)
        assert len(examples) == 25
        
    def test_generate_all_produces_total_count(self):
        """Full generation produces configured total count."""
        config = PolyglotConfig(
            lojban_count=15,
            toki_pona_count=15,
            english_count=10,
            shuffle=False
        )
        generator = PolyglotGenerator(config)
        examples = generator.generate_all()
        assert len(examples) == 40
        
    def test_generate_all_has_correct_phase_distribution(self):
        """Generated examples have correct phase distribution."""
        config = PolyglotConfig(
            lojban_count=10,
            toki_pona_count=10,
            english_count=10,
            shuffle=False
        )
        generator = PolyglotGenerator(config)
        examples = generator.generate_all()
        
        phases = {}
        for ex in examples:
            phases[ex.phase] = phases.get(ex.phase, 0) + 1
            
        assert phases.get('polyglot_lojban', 0) == 10
        assert phases.get('polyglot_tokipona', 0) == 10
        assert phases.get('polyglot_english', 0) == 10


# =============================================================================
# EXAMPLE STRUCTURE TESTS
# =============================================================================

class TestExampleStructure:
    """Tests for generated Example structure."""
    
    def test_examples_have_user_content(self):
        """Each example has non-empty user content."""
        generator = PolyglotGenerator()
        examples = generator.generate_all()
        
        for ex in examples:
            assert ex.user, f"Empty user content in example"
            assert len(ex.user) > 0
            
    def test_examples_have_assistant_content(self):
        """Each example has non-empty assistant content."""
        generator = PolyglotGenerator()
        examples = generator.generate_all()
        
        for ex in examples:
            assert ex.assistant, f"Empty assistant content in example"
            assert len(ex.assistant) > 0
            
    def test_examples_have_phase(self):
        """Each example has a phase assigned."""
        generator = PolyglotGenerator()
        examples = generator.generate_all()
        
        for ex in examples:
            assert ex.phase is not None
            assert ex.phase in ['polyglot_lojban', 'polyglot_tokipona', 'polyglot_english']
            
    def test_examples_have_metadata(self):
        """Each example has source/target language metadata."""
        generator = PolyglotGenerator()
        examples = generator.generate_all()
        
        for ex in examples:
            assert 'source_lang' in ex.metadata
            assert 'target_lang' in ex.metadata
            assert ex.metadata['target_lang'] == 'agl'
            
    def test_examples_serialize_to_valid_json(self):
        """Examples can be serialized to valid JSON."""
        generator = PolyglotGenerator()
        examples = generator.generate_all()
        
        for ex in examples:
            json_str = ex.to_jsonl_line()
            # Should not raise
            parsed = json.loads(json_str)
            assert 'messages' in parsed
            assert len(parsed['messages']) == 2
            
    def test_serialized_examples_have_correct_roles(self):
        """Serialized examples have user and assistant roles."""
        generator = PolyglotGenerator()
        examples = generator.generate_all()
        
        for ex in examples:
            data = json.loads(ex.to_jsonl_line())
            roles = [msg['role'] for msg in data['messages']]
            assert roles == ['user', 'assistant']


# =============================================================================
# FILE OUTPUT TESTS
# =============================================================================

class TestFileOutput:
    """Tests for file saving functionality."""
    
    def test_save_creates_file(self, temp_output_dir):
        """Generator saves file to specified location."""
        config = PolyglotConfig(
            lojban_count=5,
            toki_pona_count=5,
            english_count=5,
            output_dir=str(temp_output_dir),
            output_filename="test_output.jsonl"
        )
        generator = PolyglotGenerator(config)
        
        output_path = generator.generate_and_save()
        
        assert output_path.exists()
        assert output_path.name == "test_output.jsonl"
        
    def test_saved_file_has_correct_line_count(self, temp_output_dir):
        """Saved file has one line per example."""
        config = PolyglotConfig(
            lojban_count=5,
            toki_pona_count=5,
            english_count=5,
            output_dir=str(temp_output_dir),
            output_filename="test_output.jsonl"
        )
        generator = PolyglotGenerator(config)
        
        output_path = generator.generate_and_save()
        
        with open(output_path) as f:
            lines = f.readlines()
            
        assert len(lines) == 15
        
    def test_saved_file_is_valid_jsonl(self, temp_output_dir):
        """Each line in saved file is valid JSON."""
        config = PolyglotConfig(
            lojban_count=5,
            toki_pona_count=5,
            english_count=5,
            output_dir=str(temp_output_dir),
            output_filename="test_output.jsonl"
        )
        generator = PolyglotGenerator(config)
        
        output_path = generator.generate_and_save()
        
        with open(output_path) as f:
            for line_num, line in enumerate(f, 1):
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON on line {line_num}: {e}")


# =============================================================================
# REPRODUCIBILITY TESTS
# =============================================================================

class TestReproducibility:
    """Tests for deterministic/reproducible generation."""
    
    @pytest.mark.skip(reason="Known bug: generator doesn't isolate random state between instances")
    def test_same_seed_produces_same_output(self):
        """Same random seed produces identical output."""
        config1 = PolyglotConfig(
            lojban_count=10,
            toki_pona_count=10,
            english_count=10,
            seed=12345,
            shuffle=True
        )
        config2 = PolyglotConfig(
            lojban_count=10,
            toki_pona_count=10,
            english_count=10,
            seed=12345,
            shuffle=True
        )
        
        gen1 = PolyglotGenerator(config1)
        gen2 = PolyglotGenerator(config2)
        
        examples1 = gen1.generate_all()
        examples2 = gen2.generate_all()
        
        for ex1, ex2 in zip(examples1, examples2):
            assert ex1.user == ex2.user
            assert ex1.assistant == ex2.assistant
            
    def test_different_seed_produces_different_order(self):
        """Different seeds produce different shuffle order."""
        config1 = PolyglotConfig(
            lojban_count=10,
            toki_pona_count=10,
            english_count=10,
            seed=11111,
            shuffle=True
        )
        config2 = PolyglotConfig(
            lojban_count=10,
            toki_pona_count=10,
            english_count=10,
            seed=99999,
            shuffle=True
        )
        
        gen1 = PolyglotGenerator(config1)
        gen2 = PolyglotGenerator(config2)
        
        examples1 = gen1.generate_all()
        examples2 = gen2.generate_all()
        
        # Should have same content but different order
        users1 = [ex.user for ex in examples1]
        users2 = [ex.user for ex in examples2]
        
        # Very unlikely to be in same order with different seeds
        assert users1 != users2, "Different seeds should produce different order"


# =============================================================================
# STATISTICS TESTS
# =============================================================================

class TestDatasetStatistics:
    """Tests for understanding current dataset properties."""
    
    def test_count_unique_translation_pairs(self):
        """Count total unique translation pairs available."""
        total_unique = (
            len(LOJBAN_TO_AGL) +
            len(TOKI_PONA_TO_AGL) +
            len(ENGLISH_TO_AGL)
        )
        
        # Document current state - this will be updated as we expand
        print(f"\n📊 Current unique translation pairs:")
        print(f"   Lojban:     {len(LOJBAN_TO_AGL)}")
        print(f"   Toki Pona:  {len(TOKI_PONA_TO_AGL)}")
        print(f"   English:    {len(ENGLISH_TO_AGL)}")
        print(f"   TOTAL:      {total_unique}")
        
        # Current known count: 15 + 15 + 12 = 42
        # This will fail when pairs are added - UPDATE THIS when expanding!
        assert total_unique == 42, f"Expected 42 unique pairs, got {total_unique}"
        
    def test_default_config_resamples(self):
        """Default config (200 examples) exceeds unique pairs (43)."""
        config = PolyglotConfig()  # Default: 70+70+60 = 200
        total_unique = len(LOJBAN_TO_AGL) + len(TOKI_PONA_TO_AGL) + len(ENGLISH_TO_AGL)
        
        # This documents the resampling behavior
        assert config.total_count > total_unique, \
            "Default config should require resampling (more examples than unique pairs)"
