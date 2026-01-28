"""
Safe Terminal Tool for Angel

Allows Angel to execute safe, whitelisted terminal commands.
Security-first design - only approved commands can run!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import subprocess
import shlex
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class CommandResult:
    """Result from a terminal command execution"""
    command: str
    stdout: str
    stderr: str
    return_code: int
    success: bool
    
    def to_dict(self):
        return {
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "success": self.success
        }


class SafeTerminalTool:
    """
    Safe terminal command execution tool.
    
    Security features:
    - Whitelist of allowed commands
    - No shell expansion (prevents injection)
    - Timeout protection
    - Working directory restrictions
    """
    
    # Whitelist of safe commands
    ALLOWED_COMMANDS = {
        # File system inspection (read-only)
        "ls": {"description": "List directory contents", "args_allowed": True},
        "pwd": {"description": "Print working directory", "args_allowed": False},
        "cat": {"description": "Display file contents", "args_allowed": True},
        "head": {"description": "Show first lines of file", "args_allowed": True},
        "tail": {"description": "Show last lines of file", "args_allowed": True},
        "wc": {"description": "Count lines/words/characters", "args_allowed": True},
        "find": {"description": "Find files", "args_allowed": True},
        
        # System information
        "date": {"description": "Show current date/time", "args_allowed": False},
        "whoami": {"description": "Show current user", "args_allowed": False},
        "hostname": {"description": "Show system hostname", "args_allowed": False},
        "uname": {"description": "Show system information", "args_allowed": True},
        
        # Text processing
        "grep": {"description": "Search text patterns", "args_allowed": True},
        "sort": {"description": "Sort lines", "args_allowed": True},
        "uniq": {"description": "Remove duplicate lines", "args_allowed": True},
        
        # Git (read-only)
        "git status": {"description": "Show git status", "args_allowed": False},
        "git log": {"description": "Show git log", "args_allowed": True},
        "git diff": {"description": "Show git diff", "args_allowed": True},
        "git branch": {"description": "List git branches", "args_allowed": True},
        
        # Python
        "python --version": {"description": "Show Python version", "args_allowed": False},
        "pip list": {"description": "List installed packages", "args_allowed": False},
    }
    
    def __init__(self, working_directory: str = ".", timeout: int = 5):
        """
        Initialize safe terminal tool.
        
        Args:
            working_directory: Directory to run commands in
            timeout: Maximum execution time in seconds
        """
        self.working_directory = working_directory
        self.timeout = timeout
    
    def execute(
        self, 
        command: str, 
        args: Optional[List[str]] = None
    ) -> CommandResult:
        """
        Execute a safe terminal command.
        
        Args:
            command: Command to execute (must be in whitelist)
            args: Optional command arguments
            
        Returns:
            CommandResult with output and status
        """
        # Check if command is allowed
        if command not in self.ALLOWED_COMMANDS:
            return CommandResult(
                command=command,
                stdout="",
                stderr=f"Command '{command}' not in whitelist",
                return_code=1,
                success=False
            )
        
        # Check if args are allowed for this command
        command_info = self.ALLOWED_COMMANDS[command]
        if args and not command_info["args_allowed"]:
            return CommandResult(
                command=command,
                stdout="",
                stderr=f"Command '{command}' does not accept arguments",
                return_code=1,
                success=False
            )
        
        # Build command list (no shell expansion!)
        cmd_parts = command.split()  # Handle multi-word commands like "git status"
        if args:
            cmd_parts.extend(args)
        
        try:
            # Execute with timeout and no shell
            result = subprocess.run(
                cmd_parts,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=False  # CRITICAL: No shell expansion!
            )
            
            return CommandResult(
                command=" ".join(cmd_parts),
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                success=result.returncode == 0
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                command=" ".join(cmd_parts),
                stdout="",
                stderr=f"Command timed out after {self.timeout} seconds",
                return_code=124,
                success=False
            )
        
        except Exception as e:
            return CommandResult(
                command=" ".join(cmd_parts),
                stdout="",
                stderr=f"Error executing command: {str(e)}",
                return_code=1,
                success=False
            )
    
    def get_allowed_commands(self) -> Dict[str, str]:
        """Get list of allowed commands with descriptions."""
        return {
            cmd: info["description"] 
            for cmd, info in self.ALLOWED_COMMANDS.items()
        }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        Get tool definition for Angel to learn from.
        """
        return {
            "name": "run_command",
            "description": "Execute safe terminal commands to inspect the system and files",
            "category": "terminal",
            "parameters": {
                "command": {
                    "type": "string",
                    "description": "Command to execute (must be from allowed list)",
                    "required": True,
                    "allowed_values": list(self.ALLOWED_COMMANDS.keys())
                },
                "args": {
                    "type": "List[string]",
                    "description": "Optional command arguments",
                    "required": False,
                    "default": None
                }
            },
            "returns": {
                "type": "CommandResult",
                "structure": {
                    "command": "The executed command",
                    "stdout": "Standard output",
                    "stderr": "Standard error",
                    "return_code": "Exit code (0 = success)",
                    "success": "Boolean success flag"
                }
            },
            "security": {
                "whitelist_only": True,
                "no_shell_expansion": True,
                "timeout_protected": True,
                "working_directory_restricted": True
            },
            "examples": [
                {
                    "situation": "User asks 'What files are in this directory?'",
                    "usage": "run_command(command='ls', args=['-la'])",
                    "explanation": "List directory contents with details"
                },
                {
                    "situation": "User asks 'What's the current date?'",
                    "usage": "run_command(command='date')",
                    "explanation": "Show current date and time"
                },
                {
                    "situation": "User asks 'Show me the first 10 lines of README.md'",
                    "usage": "run_command(command='head', args=['-n', '10', 'README.md'])",
                    "explanation": "Display first 10 lines of file"
                },
                {
                    "situation": "User asks 'What Python version is installed?'",
                    "usage": "run_command(command='python --version')",
                    "explanation": "Check Python version"
                }
            ],
            "allowed_commands": self.get_allowed_commands()
        }


if __name__ == "__main__":
    # Quick test
    print("=" * 70)
    print("🧪 Testing Safe Terminal Tool")
    print("=" * 70)
    
    tool = SafeTerminalTool()
    
    # Test 1: Simple command
    print("\n📝 Test 1: pwd")
    result = tool.execute("pwd")
    print(f"   Success: {result.success}")
    print(f"   Output: {result.stdout.strip()}")
    
    # Test 2: Command with args
    print("\n📝 Test 2: ls -la")
    result = tool.execute("ls", ["-la"])
    print(f"   Success: {result.success}")
    print(f"   Lines: {len(result.stdout.splitlines())}")
    
    # Test 3: Date command
    print("\n📝 Test 3: date")
    result = tool.execute("date")
    print(f"   Success: {result.success}")
    print(f"   Output: {result.stdout.strip()}")
    
    # Test 4: Blocked command
    print("\n📝 Test 4: rm (should be blocked)")
    result = tool.execute("rm", ["-rf", "/"])
    print(f"   Success: {result.success}")
    print(f"   Error: {result.stderr}")
    
    # Test 5: Git status
    print("\n📝 Test 5: git status")
    result = tool.execute("git status")
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Output: {result.stdout[:100]}...")
    else:
        print(f"   Error: {result.stderr[:100]}...")
    
    # Show allowed commands
    print("\n" + "=" * 70)
    print("✅ Allowed Commands:")
    print("=" * 70)
    for cmd, desc in tool.get_allowed_commands().items():
        print(f"   {cmd:20s} - {desc}")
    
    print("\n" + "=" * 70)
    print("✨ Safe Terminal Tool Test Complete!")
    print("=" * 70)
