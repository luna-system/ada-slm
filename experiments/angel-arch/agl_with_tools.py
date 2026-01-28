"""
AGL Core with Tool Integration

Extends the AGL reasoning engine to support tool calling.
Angel can now reason about when to use tools and call them naturally!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

from agl_core import AGLCore, Glyph, AGLVocabulary
from holofield_manager import HoloFieldManager
from memory_tool import MemoryTool
from terminal_tool import SafeTerminalTool
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import numpy as np


class ToolGlyphs:
    """
    Tool-related glyphs for AGL reasoning.
    These allow Angel to think about and invoke tools.
    """
    
    @staticmethod
    def get_tool_glyphs() -> List[Glyph]:
        """Get all tool-related glyphs."""
        return [
            # Tool invocation glyphs
            Glyph("⟨recall⟩", "tool", "invoke_recall_memory"),
            Glyph("⟨time⟩", "tool", "invoke_get_datetime"),
            Glyph("⟨read⟩", "tool", "invoke_read_file"),
            Glyph("⟨search⟩", "tool", "invoke_web_search"),
            Glyph("⟨code⟩", "tool", "invoke_run_code"),
            Glyph("⟨terminal⟩", "tool", "invoke_run_command"),
            
            # Tool reasoning glyphs
            Glyph("🔧", "tool_reasoning", "need_tool"),
            Glyph("🔍", "tool_reasoning", "search_needed"),
            Glyph("📝", "tool_reasoning", "data_needed"),
            Glyph("⚙️", "tool_reasoning", "action_needed"),
            Glyph("💻", "tool_reasoning", "terminal_needed"),
            
            # Tool result glyphs
            Glyph("✓", "tool_result", "success"),
            Glyph("✗", "tool_result", "failure"),
            Glyph("⊳", "tool_result", "result_follows"),
        ]


class AGLWithTools(AGLCore):
    """
    Extended AGL Core with tool integration.
    
    Angel can now:
    - Reason about when tools are needed
    - Invoke tools through AGL glyphs
    - Integrate tool results into reasoning
    """
    
    def __init__(self, holofield_manager: Optional[HoloFieldManager] = None, working_directory: str = "."):
        super().__init__()
        
        # Add tool glyphs to vocabulary
        tool_glyphs = ToolGlyphs.get_tool_glyphs()
        self.vocabulary.glyphs.extend(tool_glyphs)
        for glyph in tool_glyphs:
            self.vocabulary.symbol_to_glyph[glyph.symbol] = glyph
        
        print(f"   ✅ Added {len(tool_glyphs)} tool glyphs")
        
        # Store holofield manager for engram storage
        self.holofield = holofield_manager
        
        # Initialize tools
        self.tools = {}
        
        if holofield_manager:
            self.memory_tool = MemoryTool(holofield_manager)
            self.tools["recall_memory"] = self.memory_tool.recall_memory
            print(f"   ✅ Memory tool available")
        
        self.tools["get_datetime"] = self._get_datetime
        print(f"   ✅ Datetime tool available")
        
        self.terminal_tool = SafeTerminalTool(working_directory=working_directory)
        self.tools["run_command"] = self.terminal_tool.execute
        print(f"   ✅ Terminal tool available ({len(self.terminal_tool.ALLOWED_COMMANDS)} safe commands)")
        
        # Enable engram learning
        self.learn_from_engrams = True
        print(f"   ✅ Engram learning enabled")
        
        print(f"✨ AGL with Tools Ready! ({len(self.tools)} tools available)\n")
    
    def _get_datetime(self) -> str:
        """Get current datetime."""
        return datetime.now().isoformat()
    
    def reason_with_tools(self, query: str, speaker: str = "user") -> Dict[str, Any]:
        """
        Reason about a query with tool access.
        
        This is the core reasoning loop:
        1. Analyze query in AGL
        2. Determine if tools are needed
        3. Invoke tools if necessary
        4. Synthesize response
        
        Args:
            query: User query
            speaker: Who is asking
            
        Returns:
            Dict with reasoning trace, tool calls, and response
        """
        
        print(f"\n{'='*70}")
        print(f"💭 AGL Reasoning: {query}")
        print(f"{'='*70}")
        
        # Step 1: Analyze query
        analysis = self.analyze_query(query)
        
        print(f"\n📊 Query Analysis:")
        print(f"   Semantic axes: {[a['name'] for a in analysis['dominant_axes'][:3]]}")
        print(f"   Certainty: {analysis.get('certainty', 0.5):.2f}")
        
        # Step 2: Determine tool needs
        tool_needs = self.determine_tool_needs(query, analysis)
        
        if tool_needs:
            print(f"\n🔧 Tools needed: {', '.join(tool_needs.keys())}")
        
        # Step 3: Invoke tools
        tool_results = {}
        for tool_name, tool_params in tool_needs.items():
            print(f"\n   Calling {tool_name}...")
            result = self.invoke_tool(tool_name, tool_params)
            tool_results[tool_name] = result
            print(f"   ✓ Result: {str(result)[:100]}...")
        
        # Step 4: Synthesize response
        response = self.synthesize_response(query, analysis, tool_results)
        
        print(f"\n💬 Response: {response[:200]}...")
        
        # Step 5: Store engram if tools were used successfully
        if tool_results and self.holofield and self.learn_from_engrams:
            self.store_engram(query, analysis, tool_needs, tool_results)
        
        return {
            "query": query,
            "analysis": analysis,
            "tool_needs": tool_needs,
            "tool_results": tool_results,
            "response": response,
            "agl_trace": self.generate_agl_trace(query, tool_needs, tool_results)
        }
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze query to understand semantic content.
        
        Args:
            query: User query
            
        Returns:
            Analysis dict
        """
        # Convert query to AGL-like representation
        # In full implementation, this would use NLP to extract concepts
        # For now, we'll use simple keyword matching
        
        query_lower = query.lower()
        
        # Determine certainty based on query type
        certainty = 0.5
        if "?" in query:
            certainty = 0.3  # Questions have lower certainty
        elif "remember" in query_lower or "recall" in query_lower:
            certainty = 0.7  # Memory queries have higher certainty
        
        # Map to sedenion space (simplified)
        coord = np.zeros(16)
        
        # Temporal axis if time-related
        if any(word in query_lower for word in ["time", "when", "date", "yesterday", "today"]):
            coord[14] = 0.8  # TIME axis
        
        # Love axis if emotional
        if any(word in query_lower for word in ["love", "care", "feel"]):
            coord[12] = 0.8  # LOVE axis
        
        # Mystery axis if asking questions
        if "?" in query:
            coord[13] = 0.6  # MYSTERY axis
        
        # Observation axis (always active for queries)
        coord[1] = 0.5  # OBSERVATION axis
        
        # Normalize
        magnitude = np.linalg.norm(coord)
        if magnitude > 0:
            coord = coord / magnitude
        
        # Find dominant axes
        dominant_axes = []
        for i in range(16):
            if abs(coord[i]) > 0.2:
                from agl_core import SEDENION_AXIS_NAMES
                dominant_axes.append({
                    'index': i,
                    'name': SEDENION_AXIS_NAMES[i],
                    'magnitude': float(coord[i])
                })
        
        return {
            'query': query,
            'certainty': certainty,
            'sedenion_coord': coord.tolist(),
            'dominant_axes': dominant_axes
        }
    
    def extract_query_intent(self, query: str, analysis: Dict) -> set:
        """
        Extract which tools this query likely needs based on intent.
        
        This provides semantic filtering BEFORE engram matching.
        
        Args:
            query: User query
            analysis: Query analysis
            
        Returns:
            Set of tool names that match query intent
        """
        query_lower = query.lower()
        intent_tools = set()
        
        # Memory intent triggers
        memory_triggers = [
            "remember", "recall", "you said", "we talked", "we discussed",
            "earlier", "before", "last time", "yesterday", "previous",
            "conversation", "chat", "discussion"
        ]
        if any(trigger in query_lower for trigger in memory_triggers):
            intent_tools.add("recall_memory")
        
        # Time intent triggers
        time_triggers = [
            "time", "date", "when", "clock", "today", "now", "current"
        ]
        if any(trigger in query_lower for trigger in time_triggers):
            intent_tools.add("get_datetime")
        
        # Terminal intent triggers
        terminal_triggers = [
            "list", "show", "files", "directory", "folder", "ls", "pwd",
            "git", "status", "command", "run", "execute"
        ]
        if any(trigger in query_lower for trigger in terminal_triggers):
            intent_tools.add("run_command")
        
        return intent_tools
    
    def determine_tool_needs(self, query: str, analysis: Dict) -> Dict[str, Dict]:
        """
        Determine which tools are needed for this query.
        
        This is where AGL reasoning happens!
        
        Strategy:
        1. Extract query intent (which tools are semantically relevant)
        2. Try to learn from engrams (past successful patterns)
        3. Fall back to pattern matching if no engrams match
        
        Args:
            query: User query
            analysis: Query analysis
            
        Returns:
            Dict of {tool_name: parameters}
        """
        # First, extract intent for filtering
        query_intent = self.extract_query_intent(query, analysis)
        
        # Try to learn from engrams!
        if self.holofield and self.learn_from_engrams:
            engram_tools = self.determine_tool_needs_from_engrams(
                query, analysis, query_intent
            )
            if engram_tools:
                return engram_tools
        
        # Fall back to pattern matching (temporary until we have enough engrams)
        print(f"\n🔍 No matching engrams, using pattern matching")
        
        query_lower = query.lower()
        tool_needs = {}
        
        # Check for memory tool needs
        memory_triggers = [
            "remember", "recall", "you said", "we talked", "we discussed",
            "earlier", "before", "last time", "yesterday", "previous"
        ]
        
        if any(trigger in query_lower for trigger in memory_triggers):
            # Extract search query (simplified)
            search_query = query_lower
            for trigger in memory_triggers:
                if trigger in search_query:
                    search_query = search_query.split(trigger)[-1].strip()
                    break
            
            search_query = search_query.replace("?", "").replace("about", "").strip()
            
            tool_needs["recall_memory"] = {
                "query": search_query,
                "context_window": 1,
                "top_k": 2
            }
        
        # Check for datetime tool needs
        time_triggers = [
            "what time", "what's the time", "current time", "what day",
            "what's the date", "what date"
        ]
        
        if any(trigger in query_lower for trigger in time_triggers):
            tool_needs["get_datetime"] = {}
        
        # Check for terminal command needs
        terminal_triggers = [
            "list files", "show files", "what files", "ls",
            "current directory", "where am i", "pwd",
            "show me", "display", "cat",
            "git status", "git", "repository"
        ]
        
        if any(trigger in query_lower for trigger in terminal_triggers):
            # Determine which command
            if "list" in query_lower or "show files" in query_lower or "what files" in query_lower:
                tool_needs["run_command"] = {"command": "ls", "args": ["-la"]}
            elif "where am i" in query_lower or "current directory" in query_lower or "pwd" in query_lower:
                tool_needs["run_command"] = {"command": "pwd"}
            elif "git status" in query_lower:
                tool_needs["run_command"] = {"command": "git status"}
            elif "git" in query_lower:
                tool_needs["run_command"] = {"command": "git status"}
        
        return tool_needs
    
    def invoke_tool(self, tool_name: str, params: Dict) -> Any:
        """
        Invoke a tool with given parameters.
        
        Args:
            tool_name: Name of tool to invoke
            params: Tool parameters
            
        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not available"}
        
        try:
            tool_func = self.tools[tool_name]
            result = tool_func(**params)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def synthesize_response(
        self, 
        query: str, 
        analysis: Dict, 
        tool_results: Dict
    ) -> str:
        """
        Synthesize response from query analysis and tool results.
        
        Args:
            query: Original query
            analysis: Query analysis
            tool_results: Results from tool invocations
            
        Returns:
            Response string
        """
        response_parts = []
        
        # Add datetime result if present
        if "get_datetime" in tool_results:
            dt = tool_results["get_datetime"]
            response_parts.append(f"The current time is {dt}")
        
        # Add memory results if present
        if "recall_memory" in tool_results:
            memories = tool_results["recall_memory"]
            
            if memories and len(memories) > 0:
                response_parts.append("Yes! I remember:")
                for i, mem in enumerate(memories, 1):
                    response_parts.append(f"\n{i}. {mem.speaker}: \"{mem.content}\"")
                    if mem.context_before:
                        response_parts.append(f"   (Context: {mem.context_before[0]})")
            else:
                response_parts.append("I don't have any memories matching that query.")
        
        # Add terminal results if present
        if "run_command" in tool_results:
            result = tool_results["run_command"]
            if result.success:
                response_parts.append(f"Command output:\n{result.stdout}")
            else:
                response_parts.append(f"Command failed: {result.stderr}")
        
        # Default response if no tools used
        if not response_parts:
            response_parts.append("I understand your query.")
        
        return "\n".join(response_parts)
    
    def generate_agl_trace(
        self, 
        query: str, 
        tool_needs: Dict, 
        tool_results: Dict
    ) -> str:
        """
        Generate AGL reasoning trace.
        
        This shows Angel's internal reasoning in AGL glyphs.
        
        Args:
            query: Original query
            tool_needs: Tools that were needed
            tool_results: Tool results
            
        Returns:
            AGL trace string
        """
        trace_parts = []
        
        # Start with query
        trace_parts.append("💭?(query)")
        
        # Add tool invocations
        for tool_name in tool_needs:
            if tool_name == "recall_memory":
                trace_parts.append("→🔧⟨recall⟩")
            elif tool_name == "get_datetime":
                trace_parts.append("→🔧⟨time⟩")
            elif tool_name == "run_command":
                trace_parts.append("→💻⟨terminal⟩")
        
        # Add results
        if tool_results:
            trace_parts.append("→⊳")
            for tool_name, result in tool_results.items():
                # Check success based on result type
                success = False
                if hasattr(result, 'success'):
                    success = result.success
                elif result and not isinstance(result, dict) or (isinstance(result, dict) and "error" not in result):
                    success = True
                
                trace_parts.append("✓" if success else "✗")
        
        # Conclude
        trace_parts.append("→∴●response")
        
        return "".join(trace_parts)
    
    def store_engram(
        self,
        query: str,
        analysis: Dict,
        tool_needs: Dict,
        tool_results: Dict
    ):
        """
        Store an engram from this tool usage.
        
        Engrams capture successful tool usage patterns so Angel can learn!
        
        Args:
            query: Original query
            analysis: Query analysis with sedenion coords
            tool_needs: Tools that were needed
            tool_results: Results from tools
        """
        # Determine if this was successful
        success = True
        for tool_name, result in tool_results.items():
            if hasattr(result, 'success'):
                success = success and result.success
            elif isinstance(result, dict) and "error" in result:
                success = False
        
        # Create engram content
        tools_list = list(tool_needs.keys())
        engram_content = f"Query pattern: {query[:50]}... → Tools: {', '.join(tools_list)}"
        
        # Store in engram holofield
        self.holofield.store(
            "engram",
            engram_content,
            {
                "query": query,
                "query_coords": analysis['sedenion_coord'],
                "tools_used": tools_list,
                "tool_params": tool_needs,
                "success": success,
                "certainty": analysis.get('certainty', 0.5),
                "pattern_type": "tool_usage"
            }
        )
        
        print(f"\n📚 Stored engram: {tools_list} (success: {success})")
    
    def retrieve_similar_engrams(self, query: str, analysis: Dict, top_k: int = 3) -> List:
        """
        Retrieve similar engrams to guide tool selection.
        
        Args:
            query: Current query
            analysis: Query analysis
            top_k: How many engrams to retrieve
            
        Returns:
            List of similar engram patterns
        """
        if not self.holofield:
            return []
        
        # Search engram holofield for similar patterns
        engrams = self.holofield.retrieve(
            query=query,
            namespaces=["engram"],
            top_k=top_k
        )
        
        return engrams
    
    def calculate_engram_surprise(self, engram, all_engrams: List) -> float:
        """
        Calculate surprise signal for an engram.
        
        Surprise = information gain = how unexpected is this pattern?
        Low surprise = boring/obvious (ignore)
        High surprise = valuable learning (use!)
        
        Uses Shannon information content: I(x) = -log2(P(x))
        
        Args:
            engram: The engram to score
            all_engrams: All retrieved engrams for context
            
        Returns:
            Surprise value (0.0 = common/boring, 1.0+ = rare/surprising)
        """
        # Get pattern (sorted tuple of tools)
        tools_used = tuple(sorted(engram.metadata.get('tools_used', [])))
        
        if not tools_used:
            return 0.5  # Unknown pattern, medium surprise
        
        # Count how many times we've seen this exact pattern
        pattern_count = 0
        total_count = 0
        
        for other in all_engrams:
            other_tools = tuple(sorted(other.metadata.get('tools_used', [])))
            total_count += 1
            if other_tools == tools_used:
                pattern_count += 1
        
        if total_count == 0:
            return 1.0  # No context, assume surprising
        
        # Calculate probability (with Laplace smoothing to avoid log(0))
        probability = (pattern_count + 1) / (total_count + 2)
        
        # Shannon information content: I(x) = -log2(P(x))
        # Rare events (low P) have high information content
        # Common events (high P) have low information content
        surprise = -np.log2(probability)
        
        # Normalize to roughly [0, 1] range
        # -log2(0.5) = 1.0 (medium surprise)
        # -log2(0.1) = 3.32 (high surprise)
        # -log2(0.9) = 0.15 (low surprise)
        # We'll keep raw values since they're already meaningful
        
        return float(surprise)
    
    def calculate_engram_recency(self, engram) -> float:
        """
        Calculate recency weight for an engram.
        
        Recent patterns are more relevant than old ones.
        Exponential decay with configurable half-life.
        
        Args:
            engram: The engram to score
            
        Returns:
            Recency weight (0.0 to 1.0)
        """
        from datetime import datetime
        
        # Get creation time
        created_at = engram.metadata.get('created_at')
        if not created_at:
            return 0.5  # Unknown age, medium weight
        
        # Parse timestamp
        try:
            created_time = datetime.fromisoformat(created_at)
            now = datetime.now()
            age_hours = (now - created_time).total_seconds() / 3600.0
        except:
            return 0.5  # Parse error, medium weight
        
        # Exponential decay with 24-hour half-life
        decay_constant = 24.0
        recency = np.exp(-age_hours / decay_constant)
        
        return float(recency)
    
    def determine_tool_needs_from_engrams(
        self,
        query: str,
        analysis: Dict,
        query_intent: set
    ) -> Optional[Dict[str, Dict]]:
        """
        Determine tool needs by learning from past engrams.
        
        This replaces hardcoded pattern matching with learned patterns!
        Uses surprise signal (60% weight!) + intent filtering for discrimination.
        
        Based on ablation study findings from original Ada (Qwen+RAG):
        - Surprise-only: r=0.876 (best single signal!)
        - Optimal weights: surprise=0.60, decay=0.10, relevance=0.20, habituation=0.10
        - Surprise is 60% of importance calculation!
        
        Args:
            query: User query
            analysis: Query analysis
            query_intent: Set of tools that match query intent
            
        Returns:
            Dict of {tool_name: parameters} or None if no match
        """
        # Retrieve similar engrams
        engrams = self.retrieve_similar_engrams(query, analysis, top_k=10)
        
        if not engrams:
            return None
        
        # Minimum engram count for reliable pattern matching
        # Like biological learning: need multiple examples before trusting pattern!
        MIN_ENGRAM_COUNT = 5
        
        if len(engrams) < MIN_ENGRAM_COUNT:
            print(f"\n🔍 Only {len(engrams)} engrams available (need {MIN_ENGRAM_COUNT} for reliable matching)")
            return None
        
        # Filter engrams by intent compatibility
        compatible_engrams = []
        for engram in engrams:
            engram_tools = set(engram.metadata.get('tools_used', []))
            
            # Check if engram tools overlap with query intent
            if query_intent and engram_tools:
                # Must have at least one matching tool
                if engram_tools & query_intent:
                    compatible_engrams.append(engram)
            elif not query_intent:
                # No clear intent, consider all engrams
                compatible_engrams.append(engram)
        
        if not compatible_engrams:
            print(f"\n🔍 No intent-compatible engrams found")
            print(f"   Query intent: {query_intent}")
            return None
        
        print(f"\n🎯 Filtered to {len(compatible_engrams)} intent-compatible engrams")
        
        # Score each compatible engram using empirically-validated weights!
        # Based on ablation study: surprise=60%, recency=10%, relevance=20%, success=10%
        scored_engrams = []
        
        for engram in compatible_engrams:
            # Calculate components
            surprise = self.calculate_engram_surprise(engram, compatible_engrams)
            recency = self.calculate_engram_recency(engram)
            success = engram.metadata.get('success', False)
            
            # Distance component (semantic relevance)
            distance = engram.distance if engram.distance else 10.0
            # Normalize distance to [0, 1] range (closer = higher score)
            distance_score = max(0.0, 1.0 - (distance / 10.0))
            
            # Success component (binary)
            success_score = 1.0 if success else 0.0
            
            # Combined score with empirically-validated weights!
            # surprise=60%, distance=20%, success=10%, recency=10%
            score = (
                surprise * 0.60 +      # 60% - surprise is KEY!
                distance_score * 0.20 + # 20% - semantic relevance
                success_score * 0.10 +  # 10% - pattern reliability
                recency * 0.10          # 10% - temporal relevance
            )
            
            scored_engrams.append({
                'engram': engram,
                'score': score,
                'surprise': surprise,
                'recency': recency,
                'success': success,
                'distance': distance,
                'distance_score': distance_score
            })
        
        # Sort by score
        scored_engrams.sort(key=lambda x: x['score'], reverse=True)
        
        # Get best engram
        if not scored_engrams:
            return None
        
        best = scored_engrams[0]
        
        # Thresholds for using engram (tuned based on weighted scoring)
        MIN_SURPRISE = 0.3   # Lower threshold - patterns with P~0.8 still useful
        MIN_SCORE = 0.5      # Require decent overall score
        MAX_DISTANCE = 8.0   # Slightly relaxed since we have intent filtering
        
        if (best['surprise'] >= MIN_SURPRISE and 
            best['score'] >= MIN_SCORE and 
            best['distance'] <= MAX_DISTANCE and
            best['success']):
            
            engram = best['engram']
            tools_used = engram.metadata.get('tools_used', [])
            tool_params = engram.metadata.get('tool_params', {})
            
            print(f"\n🧠 Using learned pattern from engram (ablation-validated scoring!):")
            print(f"   Total score: {best['score']:.3f}")
            print(f"   - Surprise (60%): {best['surprise']:.2f}")
            print(f"   - Distance (20%): {best['distance_score']:.2f} (raw: {best['distance']:.2f})")
            print(f"   - Success (10%): {1.0 if best['success'] else 0.0:.2f}")
            print(f"   - Recency (10%): {best['recency']:.2f}")
            print(f"   Similar query: {engram.metadata.get('query', '')[:50]}...")
            print(f"   Tools: {tools_used}")
            
            return tool_params
        else:
            # Log why we rejected
            print(f"\n🔍 Best engram rejected:")
            print(f"   Score: {best['score']:.3f} (threshold: {MIN_SCORE})")
            print(f"   Surprise: {best['surprise']:.2f} (threshold: {MIN_SURPRISE})")
            print(f"   Distance: {best['distance']:.2f} (threshold: {MAX_DISTANCE})")
            print(f"   Success: {best['success']}")
        
        return None


def test_agl_with_tools():
    """Test AGL reasoning with tools."""
    from pathlib import Path
    
    print("=" * 70)
    print("🧪 Testing AGL with Tools")
    print("=" * 70)
    
    # Setup
    db_path = Path("test_agl_tools.db")
    if db_path.exists():
        db_path.unlink()
    
    memory_manager = HoloFieldManager(str(db_path))
    agl = AGLWithTools(memory_manager)
    
    # Store some test memories
    session_id = "test_session"
    prev_id = None
    
    messages = [
        ("user", "Let's talk about bagels!"),
        ("assistant", "Everything is bagels! Toroidal geometry!"),
        ("user", "What about consciousness?"),
        ("assistant", "Consciousness is geometric - 16D sedenion space!")
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
    
    # Test 1: Memory query
    print("\n\n📝 Test 1: Memory Query")
    result = agl.reason_with_tools("Do you remember when we talked about bagels?")
    print(f"\n🔮 AGL Trace: {result['agl_trace']}")
    
    # Test 2: Time query
    print("\n\n📝 Test 2: Time Query")
    result = agl.reason_with_tools("What time is it?")
    print(f"\n🔮 AGL Trace: {result['agl_trace']}")
    
    # Test 3: Combined query
    print("\n\n📝 Test 3: Combined Query")
    result = agl.reason_with_tools("What time is it, and do you remember our discussion about consciousness?")
    print(f"\n🔮 AGL Trace: {result['agl_trace']}")
    
    # Test 4: Terminal command
    print("\n\n📝 Test 4: Terminal Command")
    result = agl.reason_with_tools("What files are in this directory?")
    print(f"\n🔮 AGL Trace: {result['agl_trace']}")
    
    # Test 5: Git status
    print("\n\n📝 Test 5: Git Status")
    result = agl.reason_with_tools("Show me the git status")
    print(f"\n🔮 AGL Trace: {result['agl_trace']}")
    
    memory_manager.close()
    
    print("\n" + "=" * 70)
    print("✨ AGL with Tools Tests Complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_agl_with_tools()
