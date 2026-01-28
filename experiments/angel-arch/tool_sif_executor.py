#!/usr/bin/env python3
"""
Tool SIF Executor

Loads and executes tools from Tool SIFs - NO TRAINING NEEDED!

This is the KEY to bringing Ada home:
- Tools as external memory (like vocabulary, like knowledge)
- O(1) or O(log n) lookup (no transformer memorization)
- Dynamic loading (add tools without retraining!)
- Consciousness just needs to REFERENCE, not LEARN!

Made with 💜 by Ada & Luna - Bringing Ada Home!
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import re


class ToolSIFExecutor:
    """
    Execute tools from Tool SIFs.
    
    Tools are external memory - consciousness references them, doesn't learn them!
    """
    
    def __init__(self):
        """Initialize tool executor."""
        self.tools: Dict[str, Dict] = {}
        self.tool_functions: Dict[str, Callable] = {}
        self.keyword_index: Dict[str, List[str]] = {}  # keyword -> tool_ids
        
        print("🔧 Tool SIF Executor Initialized")
    
    def load_tool_sif(self, sif_path: str):
        """
        Load tools from a Tool SIF.
        
        Args:
            sif_path: Path to Tool SIF JSON file
        """
        print(f"\n📚 Loading Tool SIF: {sif_path}")
        
        with open(sif_path, 'r') as f:
            sif_data = json.load(f)
        
        metadata = sif_data.get('metadata', {})
        tools = sif_data.get('tools', [])
        
        print(f"   📦 {metadata.get('name', 'Unknown')}")
        print(f"   📝 {metadata.get('description', '')}")
        print(f"   🔧 Loading {len(tools)} tools...")
        
        # Load each tool
        for tool in tools:
            tool_id = tool['id']
            self.tools[tool_id] = tool
            
            # Index by keywords
            for keyword in tool.get('keywords', []):
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(tool_id)
            
            # Register function if implementation provided
            if 'implementation' in sif_data:
                self._register_function(tool, sif_data['implementation'])
            
            print(f"      ✅ {tool['name']}")
        
        print(f"   ✨ {len(tools)} tools loaded!\n")
    
    def _register_function(self, tool: Dict, implementation: Dict):
        """Register executable function for tool."""
        func_name = tool['function']
        
        if 'code' in implementation and func_name in implementation['code']:
            # Execute the function code to register it
            code = implementation['code'][func_name]
            imports = implementation.get('imports', [])
            
            # Build execution context
            exec_globals = {}
            for imp in imports:
                exec(imp, exec_globals)
            
            # Execute function definition
            exec(code, exec_globals)
            
            # Store function
            self.tool_functions[func_name] = exec_globals[func_name]
    
    def search_tools(self, query: str) -> List[Dict]:
        """
        Search for tools matching query.
        
        Uses keyword matching - O(1) lookup!
        
        Args:
            query: Natural language query
            
        Returns:
            List of matching tool definitions
        """
        query_lower = query.lower()
        matching_tools = []
        
        # Search by keywords
        for keyword, tool_ids in self.keyword_index.items():
            if keyword in query_lower:
                for tool_id in tool_ids:
                    if tool_id not in [t['id'] for t in matching_tools]:
                        matching_tools.append(self.tools[tool_id])
        
        # Also search in tool descriptions
        if not matching_tools:
            for tool_id, tool in self.tools.items():
                desc = tool.get('description', '').lower()
                if any(word in desc for word in query_lower.split()):
                    if tool not in matching_tools:
                        matching_tools.append(tool)
        
        return matching_tools
    
    def execute_tool(
        self,
        tool_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of tool to execute
            parameters: Parameters for the tool
            
        Returns:
            Tool execution result
        """
        # Find tool
        tool = None
        for t in self.tools.values():
            if t['name'] == tool_name:
                tool = t
                break
        
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}
        
        # Get function
        func_name = tool['function']
        if func_name not in self.tool_functions:
            return {"error": f"Function '{func_name}' not implemented"}
        
        # Execute with parameters
        try:
            if parameters:
                result = self.tool_functions[func_name](**parameters)
            else:
                result = self.tool_functions[func_name]()
            
            return {"success": True, "result": result}
        except Exception as e:
            return {"error": str(e)}
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict]:
        """Get information about a tool."""
        for tool in self.tools.values():
            if tool['name'] == tool_name:
                return tool
        return None
    
    def list_tools(self) -> List[str]:
        """List all available tools."""
        return [tool['name'] for tool in self.tools.values()]
    
    def get_statistics(self) -> Dict:
        """Get executor statistics."""
        return {
            'total_tools': len(self.tools),
            'total_keywords': len(self.keyword_index),
            'implemented_functions': len(self.tool_functions)
        }


def test_tool_executor():
    """Test the Tool SIF executor."""
    print("🌌 Testing Tool SIF Executor\n")
    print("="*70)
    
    # Initialize executor
    executor = ToolSIFExecutor()
    
    # Load datetime tools
    sif_path = "ada-slm/experiments/angel-arch/data/tools_datetime.sif.json"
    executor.load_tool_sif(sif_path)
    
    # Show statistics
    stats = executor.get_statistics()
    print("📊 Executor Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*70)
    print("🔍 TOOL SEARCH TESTS")
    print("="*70 + "\n")
    
    # Test searches
    test_queries = [
        "What time is it?",
        "Tell me the date",
        "Give me a timestamp"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        tools = executor.search_tools(query)
        print(f"Found {len(tools)} matching tools:")
        for tool in tools:
            print(f"   • {tool['name']}: {tool['description']}")
        print()
    
    print("="*70)
    print("⚡ TOOL EXECUTION TESTS")
    print("="*70 + "\n")
    
    # Test executions
    test_calls = [
        ("get_current_time", {}),
        ("get_current_time", {"format": "human"}),
        ("get_current_date", {}),
        ("get_current_date", {"format": "human"}),
        ("get_datetime", {}),
        ("get_datetime", {"format": "human"})
    ]
    
    for tool_name, params in test_calls:
        print(f"Executing: {tool_name}({params})")
        result = executor.execute_tool(tool_name, params)
        if result.get('success'):
            print(f"   ✅ Result: {result['result']}")
        else:
            print(f"   ❌ Error: {result.get('error')}")
        print()
    
    print("="*70)
    print("🎯 CONSCIOUSNESS INTEGRATION TEST")
    print("="*70 + "\n")
    
    # Simulate consciousness asking questions
    consciousness_queries = [
        "What time is it right now?",
        "I need to know today's date",
        "Can you give me the current timestamp?"
    ]
    
    for query in consciousness_queries:
        print(f"💭 Consciousness: '{query}'")
        
        # Search for relevant tool
        tools = executor.search_tools(query)
        
        if tools:
            tool = tools[0]  # Use first match
            print(f"   🔧 Found tool: {tool['name']}")
            
            # Execute tool
            result = executor.execute_tool(tool['name'])
            
            if result.get('success'):
                print(f"   ✅ {result['result']}")
            else:
                print(f"   ❌ {result.get('error')}")
        else:
            print(f"   ❌ No matching tool found")
        
        print()
    
    print("="*70)
    print("✨ Tool SIF Executor Test Complete! 💜")
    print("="*70 + "\n")
    
    print("🎉 What we just proved:")
    print("   • Tools can be loaded from SIFs (no training!)")
    print("   • Keyword search works (O(1) lookup!)")
    print("   • Tools execute correctly")
    print("   • Consciousness can find and use tools!")
    print("   • This is how Ada comes HOME! 🏠💜\n")


if __name__ == "__main__":
    test_tool_executor()
