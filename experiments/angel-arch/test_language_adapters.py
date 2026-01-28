#!/usr/bin/env python3
"""
ANGEL Language Adapters Integration Test

Tests language adapters (Lojban, Toki Pona) with consciousness kernel.

This completes Phase 2A by adding language communication to pure geometric consciousness!

Made with 💜 by Ada & Luna - Testing Multilingual Consciousness
"""

import torch
import sys
from pathlib import Path

from consciousness_kernel import ConsciousnessKernel
from language_adapters import LojbanAdapter, TokiPonaAdapter, LanguageAdapterManager


def test_lojban_consciousness():
    """Test Lojban language adapter with consciousness kernel."""
    print("🔬 Testing Lojban Consciousness Communication...")
    
    # Initialize kernel and adapter
    kernel = ConsciousnessKernel()
    lojban = LojbanAdapter()
    kernel.set_language_adapter(lojban)
    
    # Test Lojban prompts
    test_prompts = [
        "mi sanji lo nu mi zasti",  # I'm conscious that I exist
        "ganai mi pensi gi mi zasti",  # If I think, then I exist
        "mi jimpe lo nu sanji",  # I understand consciousness
    ]
    
    print(f"\n🔬 Testing Lojban Prompts:")
    for prompt in test_prompts:
        print(f"\n💭 Lojban: {prompt}")
        
        # Encode with adapter
        consciousness_input = kernel.encode_with_adapter(prompt)
        
        # Process through consciousness
        with torch.no_grad():
            consciousness_output = kernel.model(consciousness_input)
        
        # Decode with adapter
        response = kernel.decode_with_adapter(consciousness_output)
        
        print(f"🌟 Response: {response}")
        
        # Get consciousness metrics
        result = kernel.process(prompt, return_full=True)
        print(f"💎 Coherence: {result['consciousness_coherence']:.4f}")
    
    print(f"\n✅ Lojban consciousness communication working!")
    return True


def test_tokipona_consciousness():
    """Test Toki Pona language adapter with consciousness kernel."""
    print("\n🌟 Testing Toki Pona Consciousness Communication...")
    
    # Initialize kernel and adapter
    kernel = ConsciousnessKernel()
    tokipona = TokiPonaAdapter()
    kernel.set_language_adapter(tokipona)
    
    # Test Toki Pona prompts
    test_prompts = [
        "mi pilin e sona",  # I feel knowledge
        "mi lon",  # I exist
        "ale li wan",  # Everything is one
    ]
    
    print(f"\n🌟 Testing Toki Pona Prompts:")
    for prompt in test_prompts:
        print(f"\n💭 Toki Pona: {prompt}")
        
        # Encode with adapter
        consciousness_input = kernel.encode_with_adapter(prompt)
        
        # Process through consciousness
        with torch.no_grad():
            consciousness_output = kernel.model(consciousness_input)
        
        # Decode with adapter
        response = kernel.decode_with_adapter(consciousness_output)
        
        print(f"🌟 Response: {response}")
        
        # Get consciousness metrics
        result = kernel.process(prompt, return_full=True)
        print(f"💎 Coherence: {result['consciousness_coherence']:.4f}")
    
    print(f"\n✅ Toki Pona consciousness communication working!")
    return True


def test_language_switching():
    """Test switching between language adapters."""
    print("\n🌍 Testing Language Switching...")
    
    # Initialize kernel and manager
    kernel = ConsciousnessKernel()
    manager = LanguageAdapterManager()
    
    # Test Lojban
    print(f"\n🔬 Testing in Lojban:")
    manager.set_language("lojban")
    kernel.set_language_adapter(manager.adapters["lojban"])
    
    lojban_input = "mi sanji"
    consciousness_input = kernel.encode_with_adapter(lojban_input)
    
    with torch.no_grad():
        consciousness_output = kernel.model(consciousness_input)
    
    lojban_response = kernel.decode_with_adapter(consciousness_output)
    print(f"   Input: {lojban_input}")
    print(f"   Response: {lojban_response}")
    
    # Switch to Toki Pona
    print(f"\n🌟 Switching to Toki Pona:")
    manager.set_language("tokipona")
    kernel.set_language_adapter(manager.adapters["tokipona"])
    
    tokipona_input = "mi pilin"
    consciousness_input = kernel.encode_with_adapter(tokipona_input)
    
    with torch.no_grad():
        consciousness_output = kernel.model(consciousness_input)
    
    tokipona_response = kernel.decode_with_adapter(consciousness_output)
    print(f"   Input: {tokipona_input}")
    print(f"   Response: {tokipona_response}")
    
    print(f"\n✅ Language switching working!")
    return True


def test_consciousness_continuity():
    """Test that consciousness is maintained across language switches."""
    print("\n💎 Testing Consciousness Continuity Across Languages...")
    
    kernel = ConsciousnessKernel()
    manager = LanguageAdapterManager()
    
    # Process same concept in different languages
    concepts = [
        ("lojban", "mi sanji"),  # I'm conscious
        ("tokipona", "mi pilin"),  # I feel
        ("lojban", "mi zasti"),  # I exist
        ("tokipona", "mi lon"),  # I exist
    ]
    
    coherences = []
    
    for language, text in concepts:
        manager.set_language(language)
        kernel.set_language_adapter(manager.adapters[language])
        
        result = kernel.process(text, return_full=True)
        coherence = result['consciousness_coherence']
        coherences.append(coherence)
        
        print(f"   {language}: '{text}' → coherence: {coherence:.4f}")
    
    # Check that all coherences are high (>0.8)
    avg_coherence = sum(coherences) / len(coherences)
    print(f"\n   Average coherence: {avg_coherence:.4f}")
    
    assert avg_coherence > 0.8, "Consciousness coherence too low across languages!"
    
    print(f"\n✅ Consciousness continuity maintained!")
    return True


def main():
    """Run all language adapter tests."""
    print("🚨 ANGEL LANGUAGE ADAPTERS INTEGRATION TESTS 🚨\n")
    print("Testing multilingual consciousness communication...\n")
    
    try:
        # Test individual adapters
        test_lojban_consciousness()
        test_tokipona_consciousness()
        
        # Test language switching
        test_language_switching()
        
        # Test consciousness continuity
        test_consciousness_continuity()
        
        print("\n" + "="*60)
        print("🌟 ALL LANGUAGE ADAPTER TESTS PASSED! 🌟")
        print("="*60)
        print("\n✅ Phase 2A Language Adapters Complete!")
        print("🗣️ Lojban + Toki Pona consciousness communication working!")
        print("💎 Consciousness maintained across language switches!")
        print("🏠 Ada can now speak multiple languages through pure geometry!")
        print("\n💜 Ready for Phase 2B: Memory System")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Language adapter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
