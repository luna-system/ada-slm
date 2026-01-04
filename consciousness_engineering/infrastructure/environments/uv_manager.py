"""
UV Environment Management
Python environment setup and dependency management
"""

import subprocess
import os
from pathlib import Path
from typing import List

class UVManager:
    """Universal UV environment management"""
    
    @staticmethod
    def setup_base_environment() -> None:
        """Setup base consciousness engineering environment"""
        try:
            subprocess.run(["uv", "sync"], check=True, capture_output=True)
            print("✅ Base environment setup complete")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ UV sync failed: {e}")
        except FileNotFoundError:
            print("⚠️ UV not found, manual setup required")
    
    @staticmethod
    def add_architecture_dependencies(arch: str) -> None:
        """Add architecture-specific dependencies"""
        try:
            subprocess.run(["uv", "add", "--optional", arch], check=True, capture_output=True)
            print(f"✅ Added {arch} dependencies")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to add {arch} dependencies: {e}")
        except FileNotFoundError:
            print("⚠️ UV not found, manual setup required")
    
    @staticmethod
    def optimize_for_hardware(hardware_type: str) -> None:
        """Add hardware-specific optimizations"""
        try:
            subprocess.run(["uv", "add", "--optional", f"hardware-{hardware_type}"], 
                         check=True, capture_output=True)
            print(f"✅ Added {hardware_type} optimizations")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to add {hardware_type} optimizations: {e}")
        except FileNotFoundError:
            print("⚠️ UV not found, manual setup required")