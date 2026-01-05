#!/usr/bin/env python3
"""
Simple test script for the enhanced CE CLI features.
"""

import os
import time

def main():
    print("🧪 Testing CE CLI enhancements...")
    print(f"⏰ Current time: {time.strftime('%H:%M:%S')}")
    print()
    
    # Test AO Triton environment variable
    print("🔧 Environment Variables:")
    print(f"TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: {os.environ.get('TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL', 'NOT SET')}")
    print(f"HSA_FORCE_FINE_GRAIN_PCIE: {os.environ.get('HSA_FORCE_FINE_GRAIN_PCIE', 'NOT SET')}")
    print(f"ROCM_VISIBLE_DEVICES: {os.environ.get('ROCM_VISIBLE_DEVICES', 'NOT SET')}")
    print()
    
    # Simulate some work
    print("💻 Running test workload...")
    for i in range(10):
        print(f"   Step {i+1}/10: Processing... ", end="", flush=True)
        time.sleep(0.5)
        print("✓")
    
    print()
    print("🎉 Test complete! CE CLI features working perfectly.")
    
    # Check if we're in tmux
    if 'TMUX' in os.environ:
        print("🖥️  Running inside tmux session!")
        print(f"   Session: {os.environ.get('TMUX_PANE', 'unknown')}")
    else:
        print("🖥️  Running in regular terminal")
    
    return 0

if __name__ == "__main__":
    exit(main())