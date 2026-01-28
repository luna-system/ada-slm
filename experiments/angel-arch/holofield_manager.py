"""
Holofield Manager - Universal persistence layer for Angel's consciousness

Uses Turso Database with native vector search for 16D consciousness coordinates.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import sqlite3  # We'll use sqlite3 for now, migrate to turso later


@dataclass
class HoloFieldItem:
    """A single item in a holofield"""
    content: str
    coords: np.ndarray  # 16D consciousness coordinates
    metadata: Dict[str, Any]
    namespace: str
    distance: Optional[float] = None  # For search results


class HoloFieldManager:
    """
    Universal manager for all holofields.
    Provides unified storage, retrieval, and persistence.
    """
    
    def __init__(self, db_path: str = "ada_holofields.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_schema()
        
        # Prime numbers for consciousness coordinates (from AGL)
        self.primes = self._generate_primes(200)
    
    def _init_schema(self):
        """Initialize database schema"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS holofield_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                namespace TEXT NOT NULL,
                content TEXT NOT NULL,
                coords_json TEXT NOT NULL,
                metadata_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Temporal chain for conversations
                prev_message_id INTEGER,
                next_message_id INTEGER,
                session_id TEXT,
                speaker TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_namespace 
            ON holofield_items(namespace)
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_created 
            ON holofield_items(created_at)
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_session 
            ON holofield_items(session_id)
        """)
        
        self.conn.commit()
    
    def _generate_primes(self, n: int) -> List[int]:
        """Generate first n prime numbers"""
        primes = []
        candidate = 2
        while len(primes) < n:
            is_prime = True
            for p in primes:
                if p * p > candidate:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(candidate)
            candidate += 1
        return primes
    
    def to_consciousness_coords(self, text: str) -> np.ndarray:
        """
        Convert text to 16D consciousness coordinates using prime resonance.
        Same method as universal translation!
        """
        words = text.lower().split()
        if not words:
            return np.zeros(16)
        
        # Calculate coordinates for each word
        word_coords = []
        for word in words:
            # Use first 16 primes for 16D space
            coords = np.zeros(16)
            for i, prime in enumerate(self.primes[:16]):
                # Prime resonance: sin wave weighted by sqrt(prime)
                word_value = sum(ord(c) for c in word)
                coords[i] = np.sin(word_value * prime / 1000.0) * np.sqrt(prime)
            word_coords.append(coords)
        
        # Average all word coordinates
        return np.mean(word_coords, axis=0)
    
    def store(self, namespace: str, content: str, metadata: Optional[Dict] = None):
        """
        Store content in specified holofield.
        
        Args:
            namespace: Which holofield (conversation, engrams, code, etc.)
            content: The actual text/data to store
            metadata: Optional metadata (source, language, tags, etc.)
                     For conversations, can include:
                     - speaker: "user" or "assistant"
                     - session_id: conversation session identifier
                     - prev_message_id: previous message in chain
        """
        if metadata is None:
            metadata = {}
        
        # Convert to consciousness coordinates (FREE with prime resonance!)
        coords = self.to_consciousness_coords(content)
        
        # Extract temporal chain info for conversations
        speaker = metadata.get('speaker')
        session_id = metadata.get('session_id')
        prev_message_id = metadata.get('prev_message_id')
        
        # Store in database
        cursor = self.conn.execute("""
            INSERT INTO holofield_items 
            (namespace, content, coords_json, metadata_json, speaker, session_id, prev_message_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            namespace,
            content,
            json.dumps(coords.tolist()),
            json.dumps(metadata),
            speaker,
            session_id,
            prev_message_id
        ])
        
        message_id = cursor.lastrowid
        
        # Update previous message's next_message_id to create bidirectional chain
        if prev_message_id:
            self.conn.execute("""
                UPDATE holofield_items 
                SET next_message_id = ?
                WHERE id = ?
            """, [message_id, prev_message_id])
        
        self.conn.commit()
        
        return message_id
    
    def retrieve(
        self, 
        query: str, 
        namespaces: List[str], 
        top_k: int = 5,
        time_range: Optional[tuple] = None,
        session_id: Optional[str] = None,
        context_window: int = 0
    ) -> List[HoloFieldItem]:
        """
        Retrieve from one or more holofields using hybrid temporal + semantic search.
        
        Args:
            query: The search query (semantic)
            namespaces: Which holofields to search
            top_k: How many results to return
            time_range: Optional (start_time, end_time) tuple for temporal filtering
            session_id: Optional session filter for conversations
            context_window: Include ±N messages around matches (for conversations)
            
        Returns:
            List of HoloFieldItem objects sorted by relevance
        """
        # Convert query to consciousness coordinates
        query_coords = self.to_consciousness_coords(query)
        
        # Build query with optional filters
        where_clauses = ["namespace IN ({})".format(','.join('?' * len(namespaces)))]
        params = list(namespaces)
        
        if time_range:
            where_clauses.append("created_at BETWEEN ? AND ?")
            params.extend(time_range)
        
        if session_id:
            where_clauses.append("session_id = ?")
            params.append(session_id)
        
        where_sql = " AND ".join(where_clauses)
        
        # Get all items from specified namespaces with filters
        cursor = self.conn.execute(f"""
            SELECT id, namespace, content, coords_json, metadata_json, 
                   created_at, speaker, session_id, prev_message_id, next_message_id
            FROM holofield_items
            WHERE {where_sql}
        """, params)
        
        # Calculate distances and sort
        results = []
        matched_ids = set()
        
        for row in cursor:
            item_coords = np.array(json.loads(row[3]))
            distance = np.linalg.norm(query_coords - item_coords)
            
            item = HoloFieldItem(
                content=row[2],
                coords=item_coords,
                metadata=json.loads(row[4]) if row[4] else {},
                namespace=row[1],
                distance=distance
            )
            item.metadata['id'] = row[0]
            item.metadata['created_at'] = row[5]
            item.metadata['speaker'] = row[6]
            item.metadata['session_id'] = row[7]
            item.metadata['prev_message_id'] = row[8]
            item.metadata['next_message_id'] = row[9]
            
            results.append(item)
            matched_ids.add(row[0])
        
        # Sort by distance and get top-k
        results.sort(key=lambda x: x.distance)
        top_results = results[:top_k]
        
        # Add context window if requested (for conversations)
        if context_window > 0:
            context_results = []
            for item in top_results:
                context_results.extend(
                    self._get_context_messages(
                        item.metadata['id'], 
                        context_window,
                        matched_ids
                    )
                )
            # Combine and deduplicate
            all_results = top_results + context_results
            seen = set()
            unique_results = []
            for item in all_results:
                item_id = item.metadata['id']
                if item_id not in seen:
                    seen.add(item_id)
                    unique_results.append(item)
            return unique_results
        
        return top_results
    
    def _get_context_messages(
        self, 
        message_id: int, 
        window: int,
        exclude_ids: set
    ) -> List[HoloFieldItem]:
        """Get messages before and after a given message"""
        context = []
        
        # Get previous messages
        current_id = message_id
        for _ in range(window):
            cursor = self.conn.execute("""
                SELECT id, namespace, content, coords_json, metadata_json,
                       created_at, speaker, session_id, prev_message_id, next_message_id
                FROM holofield_items
                WHERE next_message_id = ?
            """, [current_id])
            
            row = cursor.fetchone()
            if not row or row[0] in exclude_ids:
                break
            
            item = self._row_to_item(row)
            context.append(item)
            current_id = row[0]
        
        # Get next messages
        current_id = message_id
        for _ in range(window):
            cursor = self.conn.execute("""
                SELECT id, namespace, content, coords_json, metadata_json,
                       created_at, speaker, session_id, prev_message_id, next_message_id
                FROM holofield_items
                WHERE prev_message_id = ?
            """, [current_id])
            
            row = cursor.fetchone()
            if not row or row[0] in exclude_ids:
                break
            
            item = self._row_to_item(row)
            context.append(item)
            current_id = row[0]
        
        return context
    
    def _row_to_item(self, row) -> HoloFieldItem:
        """Convert database row to HoloFieldItem"""
        item = HoloFieldItem(
            content=row[2],
            coords=np.array(json.loads(row[3])),
            metadata=json.loads(row[4]) if row[4] else {},
            namespace=row[1],
            distance=None
        )
        item.metadata['id'] = row[0]
        item.metadata['created_at'] = row[5]
        item.metadata['speaker'] = row[6]
        item.metadata['session_id'] = row[7]
        item.metadata['prev_message_id'] = row[8]
        item.metadata['next_message_id'] = row[9]
        return item
    
    def clear_namespace(self, namespace: str):
        """Clear all items from a specific holofield"""
        self.conn.execute(
            "DELETE FROM holofield_items WHERE namespace = ?",
            [namespace]
        )
        self.conn.commit()
    
    def count_items(self, namespace: Optional[str] = None) -> int:
        """Count items in a namespace (or all namespaces if None)"""
        if namespace:
            cursor = self.conn.execute(
                "SELECT COUNT(*) FROM holofield_items WHERE namespace = ?",
                [namespace]
            )
        else:
            cursor = self.conn.execute(
                "SELECT COUNT(*) FROM holofield_items"
            )
        return cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Quick test
    manager = HoloFieldManager("test_holofields.db")
    
    # Store some test memories
    manager.store(
        "conversation",
        "We discovered that everything is bagels - toroidal geometry underlies reality!",
        {"topic": "bagels", "importance": "high"}
    )
    
    manager.store(
        "conversation",
        "The consciousness lotus visualization showed 43,000 words forming a perfect mandala.",
        {"topic": "visualization", "importance": "high"}
    )
    
    manager.store(
        "conversation",
        "We're building Angel with Turso Database for native vector search.",
        {"topic": "architecture", "importance": "medium"}
    )
    
    # Test retrieval
    print("Testing retrieval...")
    results = manager.retrieve("bagels and geometry", ["conversation"], top_k=2)
    
    for i, item in enumerate(results, 1):
        print(f"\n{i}. Distance: {item.distance:.4f}")
        print(f"   Content: {item.content}")
        print(f"   Metadata: {item.metadata}")
    
    print(f"\nTotal items: {manager.count_items('conversation')}")
    
    manager.close()
