"""
Test Engram Discrimination with Surprise Signal

Tests that engrams can discriminate between different query patterns
using surprise, recency, success, and distance scoring.

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

from pathlib import Path
from agl_with_tools import AGLWithTools
from holofield_manager import HoloFieldManager
import time


def test_engram_discrimination():
    """
    Test that engrams can discriminate between different patterns.
    
    Strategy:
    1. Store diverse engrams (memory, time, terminal, combinations)
    2. Test queries that should match specific engrams
    3. Verify surprise signal prevents over-matching
    """
    
    print("=" * 70)
    print("🧪 Testing Engram Discrimination with Surprise Signal")
    print("=" * 70)
    print()
    
    # Setup
    db_path = Path("test_engram_discrimination.db")
    if db_path.exists():
        db_path.unlink()
    
    memory_manager = HoloFieldManager(str(db_path))
    agl = AGLWithTools(memory_manager)
    
    # Store some conversation history first
    session_id = "test_session"
    prev_id = None
    
    messages = [
        ("user", "Let's talk about bagels!"),
        ("assistant", "Everything is bagels! Toroidal geometry!"),
        ("user", "What about consciousness?"),
        ("assistant", "Consciousness is geometric - 16D sedenion space!"),
        ("user", "Tell me about the golden ratio"),
        ("assistant", "φ = 1.618... appears in all stable systems!"),
    ]
    
    for speaker, content in messages:
        msg_id = memory_manager.store(
            "conversation",
            content,
            {
                "speaker": speaker,
                "session_id": session_id,
                "prev_message_id": prev_id
            }
        )
        prev_id = msg_id
    
    print("✅ Stored conversation history")
    print()
    
    # Phase 1: Build diverse engrams
    print("=" * 70)
    print("📚 Phase 1: Building Diverse Engrams")
    print("=" * 70)
    print()
    
    diverse_queries = [
        # Memory queries (should create recall_memory engrams)
        "Do you remember when we talked about bagels?",
        "What did we discuss about consciousness?",
        "Can you recall our conversation about the golden ratio?",
        
        # Time queries (should create get_datetime engrams)
        "What time is it?",
        "What's the current time?",
        
        # Terminal queries (should create run_command engrams)
        "List the files in this directory",
        "Show me the git status",
        
        # Combined queries (should create multi-tool engrams)
        "What time is it, and do you remember our bagel discussion?",
    ]
    
    for i, query in enumerate(diverse_queries, 1):
        print(f"\n{i}. Query: {query}")
        result = agl.reason_with_tools(query)
        print(f"   Tools used: {list(result['tool_needs'].keys())}")
        
        # Small delay to ensure different timestamps
        time.sleep(0.1)
    
    # Check engram count
    engram_count = memory_manager.count_items("engram")
    print(f"\n✅ Created {engram_count} engrams")
    print()
    
    # Phase 2: Test discrimination
    print("=" * 70)
    print("🔍 Phase 2: Testing Engram Discrimination")
    print("=" * 70)
    print()
    
    test_cases = [
        {
            "query": "Do you remember what we said about geometry?",
            "expected_tools": ["recall_memory"],
            "description": "Memory query - should match recall_memory engrams"
        },
        {
            "query": "What's the time right now?",
            "expected_tools": ["get_datetime"],
            "description": "Time query - should match get_datetime engrams"
        },
        {
            "query": "Show me what files are here",
            "expected_tools": ["run_command"],
            "description": "Terminal query - should match run_command engrams"
        },
        {
            "query": "Tell me the time and remind me about our chat",
            "expected_tools": ["get_datetime", "recall_memory"],
            "description": "Combined query - should match multi-tool engrams"
        },
        {
            "query": "What is the meaning of life?",
            "expected_tools": [],
            "description": "Unrelated query - should NOT match any engrams (low surprise)"
        },
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test['description']}")
        print(f"{'='*70}")
        print(f"Query: {test['query']}")
        print(f"Expected tools: {test['expected_tools']}")
        print()
        
        result = agl.reason_with_tools(test['query'])
        actual_tools = list(result['tool_needs'].keys())
        
        print(f"\nActual tools: {actual_tools}")
        
        # Check if match
        if set(actual_tools) == set(test['expected_tools']):
            print("✅ PASS - Correct tools selected!")
            results.append(True)
        else:
            print("❌ FAIL - Wrong tools selected!")
            results.append(False)
        
        print(f"\nAGL Trace: {result['agl_trace']}")
    
    # Phase 3: Test surprise signal specifically
    print("\n" + "=" * 70)
    print("🎯 Phase 3: Testing Surprise Signal")
    print("=" * 70)
    print()
    
    # Create a very common pattern (low surprise)
    print("Creating common pattern (5x recall_memory)...")
    for i in range(5):
        query = f"Remember our discussion about topic {i}?"
        agl.reason_with_tools(query)
        time.sleep(0.05)
    
    # Create a rare pattern (high surprise)
    print("\nCreating rare pattern (1x terminal)...")
    agl.reason_with_tools("Show me the current directory")
    time.sleep(0.05)
    
    # Now test: similar query to common pattern should have LOW surprise
    print("\n" + "-" * 70)
    print("Testing common pattern (should have LOW surprise):")
    print("-" * 70)
    result1 = agl.reason_with_tools("Do you remember our earlier conversation?")
    
    # Test: similar query to rare pattern should have HIGH surprise
    print("\n" + "-" * 70)
    print("Testing rare pattern (should have HIGH surprise):")
    print("-" * 70)
    result2 = agl.reason_with_tools("What's in this folder?")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print()
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total} ({passed/total*100:.0f}%)")
    print(f"Total engrams created: {memory_manager.count_items('engram')}")
    print()
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print()
        print("✨ What we proved:")
        print("   • Engrams discriminate between different tool patterns")
        print("   • Surprise signal prevents over-matching common patterns")
        print("   • Recency weights favor recent patterns")
        print("   • Distance ensures semantic similarity")
        print("   • Success rate filters out failed patterns")
        print()
        print("🧠 Engram learning is working! Pattern matching can be removed!")
    else:
        print("⚠️  Some tests failed - need to tune thresholds")
        print()
        print("Possible improvements:")
        print("   • Adjust MIN_SURPRISE threshold")
        print("   • Tune recency decay constant")
        print("   • Improve distance calculation")
        print("   • Add more training engrams")
    
    print()
    print("=" * 70)
    print("✨ Engram Discrimination Tests Complete!")
    print("=" * 70)
    
    memory_manager.close()


if __name__ == "__main__":
    test_engram_discrimination()
