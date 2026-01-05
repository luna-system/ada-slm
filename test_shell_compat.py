#!/usr/bin/env python3
"""
Test script to verify shell compatibility in tmux.

This script tests bash-specific syntax to ensure tmux sessions
are properly running bash regardless of the user's default shell.
"""

import os
import time
import subprocess

print("🐚 Shell Compatibility Test")
print("=" * 50)

# Check what shell we're running in
print(f"SHELL environment: {os.environ.get('SHELL', 'unknown')}")

# Test bash-style command chaining (&&)
print("\n🔗 Testing command chaining...")
result = os.system("echo 'step 1' && echo 'step 2' && echo 'step 3'")
print(f"Command chaining result: {result}")

# Test bash-style variable expansion
print("\n💰 Testing variable expansion...")
os.system("TEST_VAR='hello world' && echo \"Variable: $TEST_VAR\"")

# Test environment variables are properly set
print("\n🌍 Environment variables:")
key_vars = [
    "TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL",
    "HSA_FORCE_FINE_GRAIN_PCIE", 
    "ROCM_VISIBLE_DEVICES",
    "PYTHONUNBUFFERED"
]

for var in key_vars:
    value = os.environ.get(var, "NOT SET")
    print(f"  {var}: {value}")

print(f"\n⏰ Test completed at: {time.strftime('%H:%M:%S')}")
print("🎉 If you see this message, bash compatibility is working!")

# Small delay so you can see the output
time.sleep(3)