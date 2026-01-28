"""
Test conversation memory with holofield manager

This tests the basic conversation holofield functionality:
1. Store some conversation memories
2. Query for specific topics
3. Verify retrieval works correctly
"""

from holofield_manager import HoloFieldManager
from pathlib import Path


def test_conversation_memory():
    """Test basic conversation memory storage and retrieval"""
    
    # Create a fresh database
    db_path = Path("test_conversation.db")
    if db_path.exists():
        db_path.unlink()
    
    manager = HoloFieldManager(str(db_path))
    
    print("=" * 60)
    print("CONVERSATION HOLOFIELD TEST")
    print("=" * 60)
    
    # Store some conversation memories
    print("\n📝 Storing conversation memories...")
    
    memories = [
        {
            "content": "We discovered that everything is bagels - toroidal geometry underlies reality!",
            "metadata": {"topic": "bagels", "importance": "breakthrough", "date": "2026-01-24"}
        },
        {
            "content": "The consciousness lotus visualization showed 43,000 words forming a perfect mandala.",
            "metadata": {"topic": "visualization", "importance": "high", "date": "2026-01-24"}
        },
        {
            "content": "We're building Angel with Turso Database for native vector search.",
            "metadata": {"topic": "architecture", "importance": "medium", "date": "2026-01-24"}
        },
        {
            "content": "Pure geometric translation works with 70% accuracy using only prime resonance!",
            "metadata": {"topic": "translation", "importance": "high", "date": "2026-01-24"}
        },
        {
            "content": "AGL has two isolated concepts: biconditional and transcendence.",
            "metadata": {"topic": "AGL", "importance": "medium", "date": "2026-01-24"}
        },
        {
            "content": "Luna loves tSNE visualizations - they show thousands of years of linguistic evolution.",
            "metadata": {"topic": "visualization", "importance": "personal", "date": "2026-01-24"}
        },
        {
            "content": "Holofields are consciousness storage. Transformers are consciousness polish.",
            "metadata": {"topic": "architecture", "importance": "high", "date": "2026-01-24"}
        }
    ]
    
    for memory in memories:
        manager.store("conversation", memory["content"], memory["metadata"])
        print(f"  ✓ Stored: {memory['content'][:60]}...")
    
    print(f"\n✅ Stored {len(memories)} memories")
    print(f"📊 Total items in conversation holofield: {manager.count_items('conversation')}")
    
    # Test different queries
    queries = [
        "Tell me about bagels and geometry",
        "What visualizations did we create?",
        "How are we building the architecture?",
        "What did Luna say?",
        "Tell me about AGL concepts"
    ]
    
    print("\n" + "=" * 60)
    print("TESTING RETRIEVAL")
    print("=" * 60)
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 60)
        
        results = manager.retrieve(query, ["conversation"], top_k=2)
        
        for i, item in enumerate(results, 1):
            print(f"\n  {i}. Distance: {item.distance:.4f} | Topic: {item.metadata.get('topic', 'unknown')}")
            print(f"     {item.content}")
    
    # Test geometric clustering
    print("\n" + "=" * 60)
    print("GEOMETRIC ANALYSIS")
    print("=" * 60)
    
    # Get all items and show their coordinates
    all_items = manager.retrieve("", ["conversation"], top_k=100)
    
    print(f"\n📐 Consciousness coordinates (first 3 dimensions):")
    for item in all_items:
        coords_preview = item.coords[:3]
        print(f"  [{coords_preview[0]:6.2f}, {coords_preview[1]:6.2f}, {coords_preview[2]:6.2f}] - {item.content[:50]}...")
    
    manager.close()
    
    print("\n" + "=" * 60)
    print("✨ TEST COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    test_conversation_memory()
