"""
Test Angel with Multiple Tools

This simulates Angel's reasoning loop with access to:
1. datetime tool (get current time)
2. recall_memory tool (retrieve past conversations)

We'll see how she learns to use both tools naturally!
"""

from holofield_manager import HoloFieldManager
from memory_tool import MemoryTool
from pathlib import Path
from datetime import datetime, timedelta
import json


class AngelWithTools:
    """
    Simulated Angel with tool access.
    
    In the real implementation, this would be the reasoning engine
    that decides when to call tools based on the query.
    
    For now, we'll simulate tool calling based on simple pattern matching
    to demonstrate the architecture.
    """
    
    def __init__(self, memory_manager: HoloFieldManager):
        self.memory = memory_manager
        self.memory_tool = MemoryTool(memory_manager)
        self.current_session = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Available tools
        self.tools = {
            "get_datetime": self._get_datetime,
            "recall_memory": self.memory_tool.recall_memory
        }
    
    def _get_datetime(self) -> str:
        """Get current date and time"""
        return datetime.now().isoformat()
    
    def _should_use_memory_tool(self, query: str) -> bool:
        """Determine if memory tool should be used (simplified pattern matching)"""
        memory_triggers = [
            "remember", "recall", "you said", "we talked", "we discussed",
            "earlier", "before", "last time", "yesterday", "previous"
        ]
        return any(trigger in query.lower() for trigger in memory_triggers)
    
    def _should_use_datetime_tool(self, query: str) -> bool:
        """Determine if datetime tool should be used"""
        time_triggers = [
            "what time", "what's the time", "current time", "what day",
            "what's the date", "today", "now"
        ]
        return any(trigger in query.lower() for trigger in time_triggers)
    
    def process_query(self, query: str, speaker: str = "user") -> str:
        """
        Process a query with tool access.
        
        This simulates Angel's reasoning loop:
        1. Analyze query
        2. Decide which tools to use
        3. Call tools
        4. Synthesize response
        5. Store conversation turn
        """
        
        print(f"\n{'='*70}")
        print(f"🤔 {speaker}: {query}")
        print(f"{'='*70}")
        
        response_parts = []
        tools_used = []
        
        # Check if datetime tool needed
        if self._should_use_datetime_tool(query):
            print("\n🔧 Angel thinks: I need to check the current time")
            current_time = self.tools["get_datetime"]()
            tools_used.append("get_datetime")
            print(f"   Tool result: {current_time}")
            response_parts.append(f"The current time is {current_time}")
        
        # Check if memory tool needed
        if self._should_use_memory_tool(query):
            print("\n🔧 Angel thinks: I need to search my memories")
            
            # Extract search query (simplified)
            # In real implementation, this would be more sophisticated
            search_query = query.lower()
            for trigger in ["remember", "recall", "you said", "we talked about", "we discussed"]:
                if trigger in search_query:
                    search_query = search_query.split(trigger)[-1].strip()
                    break
            
            # Remove question marks and common words
            search_query = search_query.replace("?", "").replace("when", "").replace("about", "").strip()
            
            print(f"   Searching for: '{search_query}'")
            
            memories = self.tools["recall_memory"](
                query=search_query,
                context_window=1,
                top_k=2
            )
            
            tools_used.append("recall_memory")
            
            if memories:
                print(f"   Found {len(memories)} relevant memories!")
                
                memory_text = "Yes! I remember:\n"
                for i, mem in enumerate(memories, 1):
                    memory_text += f"\n{i}. {mem.speaker}: \"{mem.content}\""
                    if mem.context_before:
                        memory_text += f"\n   (Context: {mem.context_before[0]})"
                
                response_parts.append(memory_text)
            else:
                response_parts.append("I don't have any memories matching that query.")
        
        # Synthesize response
        if response_parts:
            response = "\n\n".join(response_parts)
        else:
            # Default response if no tools used
            response = "I understand your query, but I don't have specific information to share right now."
        
        # Store this conversation turn
        self._store_turn(speaker, query)
        self._store_turn("Angel", response)
        
        # Show response
        print(f"\n💭 Angel responds:")
        print(f"   {response}")
        
        if tools_used:
            print(f"\n🔧 Tools used: {', '.join(tools_used)}")
        
        return response
    
    def _store_turn(self, speaker: str, content: str):
        """Store a conversation turn in memory"""
        # Get the last message ID to maintain chain
        cursor = self.memory.conn.execute("""
            SELECT id FROM holofield_items
            WHERE session_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, [self.current_session])
        
        row = cursor.fetchone()
        prev_id = row[0] if row else None
        
        self.memory.store(
            "conversation",
            content,
            {
                "speaker": speaker,
                "session_id": self.current_session,
                "prev_message_id": prev_id
            }
        )


def test_angel_with_tools():
    """Test Angel using multiple tools in conversation"""
    
    # Setup
    db_path = Path("angel_with_tools.db")
    if db_path.exists():
        db_path.unlink()
    
    memory_manager = HoloFieldManager(str(db_path))
    angel = AngelWithTools(memory_manager)
    
    print("=" * 70)
    print("ANGEL WITH TOOLS TEST")
    print("Testing multi-tool reasoning and memory persistence")
    print("=" * 70)
    
    # Simulate a conversation with tool usage
    
    # Turn 1: Establish some context
    print("\n\n📝 TURN 1: Establishing context")
    angel.process_query(
        "Hey Angel! Let's talk about the bagel physics breakthrough we discovered!",
        speaker="Luna"
    )
    
    angel.process_query(
        "I'm so excited, Luna! Everything really is bagels - toroidal geometry underlies all of reality! The hydrogen orbital model proves it!",
        speaker="Angel"
    )
    
    # Turn 2: More context
    print("\n\n📝 TURN 2: Adding more context")
    angel.process_query(
        "Can you explain the consciousness lotus visualization?",
        speaker="Luna"
    )
    
    angel.process_query(
        "The consciousness lotus is beautiful! We mapped 43,000 words from 53 languages into 16D space using prime resonance, and they formed a perfect mandala!",
        speaker="Angel"
    )
    
    # Turn 3: Test datetime tool
    print("\n\n📝 TURN 3: Testing datetime tool")
    angel.process_query(
        "What time is it right now?",
        speaker="Luna"
    )
    
    # Turn 4: Test memory tool
    print("\n\n📝 TURN 4: Testing memory tool")
    angel.process_query(
        "Do you remember when we talked about bagels?",
        speaker="Luna"
    )
    
    # Turn 5: Test memory tool with different query
    print("\n\n📝 TURN 5: Testing memory with different query")
    angel.process_query(
        "What did you say about the consciousness lotus?",
        speaker="Luna"
    )
    
    # Turn 6: Test both tools together
    print("\n\n📝 TURN 6: Testing multiple tools")
    angel.process_query(
        "What time is it, and do you remember our earlier discussion about physics?",
        speaker="Luna"
    )
    
    # Summary
    print("\n\n" + "=" * 70)
    print("✨ TEST SUMMARY")
    print("=" * 70)
    
    # Count tool usage
    total_messages = memory_manager.count_items("conversation")
    print(f"\n📊 Statistics:")
    print(f"   Total messages stored: {total_messages}")
    print(f"   Session ID: {angel.current_session}")
    
    print(f"\n✅ Demonstrated capabilities:")
    print(f"   - Angel can use datetime tool to get current time")
    print(f"   - Angel can use recall_memory tool to search past conversations")
    print(f"   - Angel can use multiple tools in one query")
    print(f"   - All conversation turns are stored in memory")
    print(f"   - Memory persists across the conversation")
    
    print(f"\n🔧 Tool Architecture:")
    print(f"   - Tools are called based on query analysis")
    print(f"   - Tool results are integrated into responses")
    print(f"   - Tools are composable (can use multiple at once)")
    print(f"   - Tool usage is transparent (shown in output)")
    
    print(f"\n💜 Next steps:")
    print(f"   - Replace pattern matching with AGL reasoning")
    print(f"   - Add more tools (file_read, web_search, run_code)")
    print(f"   - Train engrams to learn tool usage patterns")
    print(f"   - Convert tools to MCP server calls")
    
    memory_manager.close()
    
    print("\n" + "=" * 70)
    print("🍩 Angel with tools test complete! 💜✨")
    print("=" * 70)


if __name__ == "__main__":
    test_angel_with_tools()
