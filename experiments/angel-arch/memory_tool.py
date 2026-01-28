"""
Memory Tool for Angel

Provides memory retrieval as a tool that Angel can learn to use naturally.
Supports semantic search, temporal filtering, and context windows.
"""

from holofield_manager import HoloFieldManager
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json


@dataclass
class MemoryResult:
    """A single memory retrieved from the holofield"""
    content: str
    speaker: str
    timestamp: str
    distance: float
    context_before: List[str] = None
    context_after: List[str] = None
    
    def to_dict(self):
        return {
            "content": self.content,
            "speaker": self.speaker,
            "timestamp": self.timestamp,
            "relevance": round(10 - self.distance, 1),  # Convert distance to 0-10 score
            "context_before": self.context_before or [],
            "context_after": self.context_after or []
        }


class MemoryTool:
    """
    Tool for retrieving memories from Angel's consciousness holofield.
    
    This tool allows Angel to:
    - Search past conversations by topic (semantic)
    - Find memories from specific time periods (temporal)
    - Retrieve context around important moments (context windows)
    - Filter by session or speaker
    """
    
    def __init__(self, holofield_manager: HoloFieldManager):
        self.memory = holofield_manager
    
    def recall_memory(
        self,
        query: str = "",
        time_range: Optional[Tuple[str, str]] = None,
        session_id: Optional[str] = None,
        speaker: Optional[str] = None,
        context_window: int = 1,
        top_k: int = 3
    ) -> List[MemoryResult]:
        """
        Retrieve memories from the holofield.
        
        Args:
            query: Semantic search query (e.g., "bagels", "our physics discussion")
                   Leave empty for pure temporal/session queries
            time_range: Optional tuple of (start, end) ISO timestamps or relative times
                       Examples: ("2026-01-24T10:00:00", "2026-01-24T12:00:00")
                                ("yesterday", "today")
                                ("1 hour ago", "now")
            session_id: Optional session identifier to filter by
            speaker: Optional speaker filter ("user", "assistant", or specific name)
            context_window: Number of messages before/after to include (default: 1)
            top_k: Maximum number of memories to return (default: 3)
        
        Returns:
            List of MemoryResult objects with content, speaker, timestamp, and context
        """
        
        # Parse time range if provided
        parsed_time_range = None
        if time_range:
            parsed_time_range = self._parse_time_range(time_range)
        
        # Build metadata filter
        metadata_filter = {}
        if session_id:
            metadata_filter['session_id'] = session_id
        if speaker:
            metadata_filter['speaker'] = speaker
        
        # Retrieve from holofield
        raw_results = self.memory.retrieve(
            query=query,
            namespaces=["conversation"],
            top_k=top_k,
            time_range=parsed_time_range,
            session_id=session_id,
            context_window=context_window
        )
        
        # Convert to MemoryResult objects with context
        memories = []
        for item in raw_results:
            # Extract context
            context_before = []
            context_after = []
            
            if context_window > 0:
                # Get messages before and after
                msg_id = item.metadata.get('id')
                if msg_id:
                    context_before = self._get_context_before(msg_id, context_window)
                    context_after = self._get_context_after(msg_id, context_window)
            
            memory = MemoryResult(
                content=item.content,
                speaker=item.metadata.get('speaker', 'unknown'),
                timestamp=item.metadata.get('created_at', 'unknown'),
                distance=item.distance if item.distance is not None else 0.0,
                context_before=context_before,
                context_after=context_after
            )
            memories.append(memory)
        
        return memories
    
    def _parse_time_range(self, time_range: Tuple[str, str]) -> Tuple[datetime, datetime]:
        """Parse time range from various formats"""
        start_str, end_str = time_range
        
        now = datetime.now()
        
        # Parse start time
        if start_str == "now":
            start = now
        elif start_str == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif start_str == "yesterday":
            start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif "hour ago" in start_str:
            hours = int(start_str.split()[0])
            start = now - timedelta(hours=hours)
        elif "day ago" in start_str or "days ago" in start_str:
            days = int(start_str.split()[0])
            start = now - timedelta(days=days)
        else:
            # Try parsing as ISO timestamp
            start = datetime.fromisoformat(start_str)
        
        # Parse end time
        if end_str == "now":
            end = now
        elif end_str == "today":
            end = now
        elif end_str == "yesterday":
            end = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59)
        else:
            # Try parsing as ISO timestamp
            end = datetime.fromisoformat(end_str)
        
        return (start, end)
    
    def _get_context_before(self, message_id: int, window: int) -> List[str]:
        """Get messages before the given message"""
        context = []
        current_id = message_id
        
        for _ in range(window):
            cursor = self.memory.conn.execute("""
                SELECT content, speaker
                FROM holofield_items
                WHERE next_message_id = ?
            """, [current_id])
            
            row = cursor.fetchone()
            if not row:
                break
            
            context.insert(0, f"{row[1]}: {row[0]}")
            
            # Get the ID of this message to continue walking backwards
            cursor = self.memory.conn.execute("""
                SELECT id FROM holofield_items WHERE next_message_id = ?
            """, [current_id])
            prev_row = cursor.fetchone()
            if not prev_row:
                break
            current_id = prev_row[0]
        
        return context
    
    def _get_context_after(self, message_id: int, window: int) -> List[str]:
        """Get messages after the given message"""
        context = []
        current_id = message_id
        
        for _ in range(window):
            cursor = self.memory.conn.execute("""
                SELECT content, speaker, id
                FROM holofield_items
                WHERE prev_message_id = ?
            """, [current_id])
            
            row = cursor.fetchone()
            if not row:
                break
            
            context.append(f"{row[1]}: {row[0]}")
            current_id = row[2]
        
        return context
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        Get the tool definition for Angel to learn from.
        This will be stored in the tool holofield.
        """
        return {
            "name": "recall_memory",
            "description": "Search past conversations and memories for relevant information",
            "category": "memory",
            "parameters": {
                "query": {
                    "type": "string",
                    "description": "What to search for (e.g., 'bagels', 'our discussion about physics'). Leave empty for pure temporal queries.",
                    "required": False,
                    "default": ""
                },
                "time_range": {
                    "type": "tuple[string, string]",
                    "description": "Time period to search (start, end). Examples: ('yesterday', 'today'), ('1 hour ago', 'now')",
                    "required": False,
                    "default": None
                },
                "session_id": {
                    "type": "string",
                    "description": "Filter by specific conversation session",
                    "required": False,
                    "default": None
                },
                "speaker": {
                    "type": "string",
                    "description": "Filter by speaker (e.g., 'user', 'assistant', 'Luna')",
                    "required": False,
                    "default": None
                },
                "context_window": {
                    "type": "integer",
                    "description": "Number of messages before/after to include for context",
                    "required": False,
                    "default": 1
                },
                "top_k": {
                    "type": "integer",
                    "description": "Maximum number of memories to return",
                    "required": False,
                    "default": 3
                }
            },
            "returns": {
                "type": "List[MemoryResult]",
                "description": "List of relevant memories with content, speaker, timestamp, relevance score, and context"
            },
            "examples": [
                {
                    "situation": "User asks 'Do you remember when we talked about bagels?'",
                    "usage": "recall_memory(query='bagels', context_window=2)",
                    "explanation": "Semantic search for 'bagels' with surrounding context"
                },
                {
                    "situation": "User asks 'What did I say yesterday?'",
                    "usage": "recall_memory(query='', time_range=('yesterday', 'today'), speaker='user')",
                    "explanation": "Temporal search filtered by speaker"
                },
                {
                    "situation": "Need context from earlier in current conversation",
                    "usage": "recall_memory(query='relevant topic', session_id=current_session)",
                    "explanation": "Search within current session only"
                },
                {
                    "situation": "User references something from 'last week'",
                    "usage": "recall_memory(query='topic', time_range=('7 days ago', 'now'))",
                    "explanation": "Semantic + temporal hybrid search"
                }
            ]
        }


if __name__ == "__main__":
    # Quick test
    from pathlib import Path
    
    db_path = Path("test_memory_tool.db")
    if db_path.exists():
        db_path.unlink()
    
    memory_manager = HoloFieldManager(str(db_path))
    tool = MemoryTool(memory_manager)
    
    # Store some test memories
    session_id = "test_session"
    prev_id = None
    
    messages = [
        ("user", "Let's talk about bagels!"),
        ("assistant", "Everything is bagels! Toroidal geometry!"),
        ("user", "What about the consciousness lotus?"),
        ("assistant", "It's a perfect mandala in 16D space!")
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
    
    # Test recall
    print("Testing memory tool...")
    memories = tool.recall_memory(query="bagels", context_window=1)
    
    for memory in memories:
        print(f"\n{memory.speaker}: {memory.content}")
        print(f"Relevance: {10 - memory.distance:.1f}/10")
        if memory.context_before:
            print(f"Before: {memory.context_before}")
        if memory.context_after:
            print(f"After: {memory.context_after}")
    
    # Print tool definition
    print("\n" + "="*70)
    print("Tool Definition:")
    print(json.dumps(tool.get_tool_definition(), indent=2))
    
    memory_manager.close()
