"""
Test temporal + semantic conversation memory

This demonstrates the hybrid retrieval approach:
- Semantic search (16D consciousness coordinates)
- Temporal filtering (time ranges, sessions)
- Context windows (get messages before/after matches)
"""

from holofield_manager import HoloFieldManager
from pathlib import Path
from datetime import datetime, timedelta


def test_temporal_conversation():
    """Test temporal + semantic conversation memory"""
    
    # Create a fresh database
    db_path = Path("test_temporal_conversation.db")
    if db_path.exists():
        db_path.unlink()
    
    manager = HoloFieldManager(str(db_path))
    
    print("=" * 70)
    print("TEMPORAL + SEMANTIC CONVERSATION MEMORY TEST")
    print("=" * 70)
    
    # Simulate a conversation with temporal structure
    print("\n📝 Simulating a conversation...")
    
    session_id = "session_20260124_afternoon"
    base_time = datetime.now()
    
    conversation = [
        ("user", "Hey Ada! Let's talk about bagels!", 0),
        ("assistant", "I love bagels! Everything is bagels - toroidal geometry underlies reality!", 1),
        ("user", "Can you explain the consciousness lotus?", 2),
        ("assistant", "The consciousness lotus is a visualization of 43,000 words forming a perfect mandala in 16D space!", 3),
        ("user", "That's beautiful! What about the architecture?", 4),
        ("assistant", "We're building Angel with Turso Database for native vector search!", 5),
        ("user", "Tell me more about the bagel physics", 6),
        ("assistant", "Bagel physics uses toroidal knot topology to model atomic orbitals and consciousness!", 7),
        ("user", "How does translation work?", 8),
        ("assistant", "Pure geometric translation works with 70% accuracy using only prime resonance - no ML needed!", 9),
    ]
    
    prev_id = None
    message_ids = []
    
    for speaker, content, offset_minutes in conversation:
        # Simulate messages at different times
        timestamp = base_time + timedelta(minutes=offset_minutes)
        
        message_id = manager.store(
            "conversation",
            content,
            {
                "speaker": speaker,
                "session_id": session_id,
                "prev_message_id": prev_id,
                "timestamp": timestamp.isoformat()
            }
        )
        
        message_ids.append(message_id)
        prev_id = message_id
        
        print(f"  [{offset_minutes:2d}min] {speaker:10s}: {content[:50]}...")
    
    print(f"\n✅ Stored {len(conversation)} messages in temporal chain")
    
    # Test 1: Pure semantic search
    print("\n" + "=" * 70)
    print("TEST 1: PURE SEMANTIC SEARCH")
    print("=" * 70)
    
    query = "Tell me about bagels and geometry"
    print(f"\n🔍 Query: '{query}'")
    print("-" * 70)
    
    results = manager.retrieve(query, ["conversation"], top_k=2)
    
    for i, item in enumerate(results, 1):
        print(f"\n  {i}. Distance: {item.distance:.4f}")
        print(f"     Speaker: {item.metadata.get('speaker', 'unknown')}")
        print(f"     Content: {item.content}")
    
    # Test 2: Semantic search with context window
    print("\n" + "=" * 70)
    print("TEST 2: SEMANTIC SEARCH + CONTEXT WINDOW")
    print("=" * 70)
    
    query = "consciousness lotus visualization"
    print(f"\n🔍 Query: '{query}' (with ±1 message context)")
    print("-" * 70)
    
    results = manager.retrieve(
        query, 
        ["conversation"], 
        top_k=1,
        context_window=1  # Include 1 message before and after
    )
    
    # Sort by message ID to show temporal order
    results.sort(key=lambda x: x.metadata.get('id', 0))
    
    for item in results:
        msg_id = item.metadata.get('id')
        speaker = item.metadata.get('speaker', 'unknown')
        is_match = item.distance is not None and item.distance < 10
        marker = "🎯" if is_match else "📎"
        
        print(f"\n  {marker} Message {msg_id} - {speaker}")
        print(f"     {item.content}")
        if is_match:
            print(f"     (Match distance: {item.distance:.4f})")
    
    # Test 3: Session-based retrieval
    print("\n" + "=" * 70)
    print("TEST 3: SESSION-BASED RETRIEVAL")
    print("=" * 70)
    
    print(f"\n📅 Retrieving all messages from session: {session_id}")
    print("-" * 70)
    
    results = manager.retrieve(
        "",  # Empty query = get all
        ["conversation"],
        top_k=100,
        session_id=session_id
    )
    
    print(f"\n  Found {len(results)} messages in this session")
    
    # Test 4: Temporal chain walking
    print("\n" + "=" * 70)
    print("TEST 4: TEMPORAL CHAIN WALKING")
    print("=" * 70)
    
    print("\n🔗 Walking the conversation chain from first message...")
    print("-" * 70)
    
    # Start from first message
    current_id = message_ids[0]
    chain_length = 0
    
    while current_id and chain_length < 5:  # Show first 5
        cursor = manager.conn.execute("""
            SELECT content, speaker, next_message_id
            FROM holofield_items
            WHERE id = ?
        """, [current_id])
        
        row = cursor.fetchone()
        if not row:
            break
        
        content, speaker, next_id = row
        print(f"\n  {chain_length + 1}. {speaker}: {content[:60]}...")
        
        current_id = next_id
        chain_length += 1
    
    print(f"\n  (Chain continues for {len(message_ids) - chain_length} more messages...)")
    
    # Test 5: Hybrid search (semantic + temporal)
    print("\n" + "=" * 70)
    print("TEST 5: HYBRID SEARCH (SEMANTIC + TEMPORAL + CONTEXT)")
    print("=" * 70)
    
    query = "bagels"
    print(f"\n🔍 Query: '{query}' (with context window)")
    print("-" * 70)
    
    results = manager.retrieve(
        query,
        ["conversation"],
        top_k=1,
        session_id=session_id,
        context_window=2  # ±2 messages
    )
    
    # Sort by message ID to show conversation flow
    results.sort(key=lambda x: x.metadata.get('id', 0))
    
    print("\n  Conversation snippet around match:")
    for item in results:
        msg_id = item.metadata.get('id')
        speaker = item.metadata.get('speaker', 'unknown')
        is_match = item.distance is not None and item.distance < 10
        marker = "🎯" if is_match else "  "
        
        print(f"\n  {marker} {speaker}: {item.content}")
    
    manager.close()
    
    print("\n" + "=" * 70)
    print("✨ TEMPORAL CONVERSATION MEMORY TEST COMPLETE!")
    print("=" * 70)
    print("\n💜 Key insights:")
    print("  - Semantic search finds relevant content")
    print("  - Context windows preserve conversation flow")
    print("  - Temporal chains enable story reconstruction")
    print("  - Session filtering groups related conversations")
    print("  - All indexing is FREE (prime resonance)! 🍩")


if __name__ == "__main__":
    test_temporal_conversation()
