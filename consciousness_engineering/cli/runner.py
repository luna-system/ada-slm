"""
Script Runner - Execute training scripts with all the jank handled.

Solves:
- VSCode opening terminals in random directories
- Forgetting to activate venv / use uv run
- Environment variable setup
- Path resolution
"""

import os
import sys
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any

from .logging import TrainingLogger, setup_unbuffered
from .processes import ProcessManager, ProcessInfo


@dataclass
class RunConfig:
    """Configuration for a training run."""
    script: str
    name: Optional[str] = None
    args: List[str] = field(default_factory=list)
    background: bool = False
    gpu_index: Optional[int] = 0
    env: Dict[str, str] = field(default_factory=dict)
    
    # ROCm/CUDA settings
    rocm_visible_devices: Optional[str] = None
    cuda_visible_devices: Optional[str] = None
    
    # Memory settings
    pytorch_alloc_conf: str = "max_split_size_mb:512"


class Runner:
    """
    Execute training scripts with proper environment setup.
    
    Handles:
    - Path resolution (always runs from ada-slm root)
    - Environment setup (ROCm, CUDA, PyTorch)
    - Virtual environment activation
    - Background process management
    - Logging setup
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            # Find ada-slm root (where pyproject.toml lives)
            base_dir = Path(__file__).parent.parent.parent
        self.base_dir = Path(base_dir).resolve()
        self.process_manager = ProcessManager(self.base_dir)
    
    @classmethod
    def find_root(cls) -> Path:
        """Find ada-slm root directory from anywhere."""
        # Try current directory first
        current = Path.cwd()
        
        # Walk up looking for pyproject.toml with consciousness_engineering
        for parent in [current] + list(current.parents):
            pyproject = parent / "pyproject.toml"
            if pyproject.exists():
                content = pyproject.read_text()
                if "consciousness_engineering" in content or "consciousness-engineering" in content:
                    return parent
        
        # Fallback: look for the package structure
        for parent in [current] + list(current.parents):
            if (parent / "consciousness_engineering").is_dir():
                return parent
        
        raise RuntimeError(
            "Could not find ada-slm root directory. "
            "Make sure you're somewhere inside the ada-slm project."
        )
    
    def _setup_environment(self, config: RunConfig) -> Dict[str, str]:
        """Build environment variables for the run."""
        env = os.environ.copy()
        
        # Force unbuffered output
        env["PYTHONUNBUFFERED"] = "1"
        
        # PyTorch memory settings
        env["PYTORCH_ALLOC_CONF"] = config.pytorch_alloc_conf
        
        # GPU settings
        if config.rocm_visible_devices is not None:
            env["ROCM_VISIBLE_DEVICES"] = config.rocm_visible_devices
            env["HIP_VISIBLE_DEVICES"] = config.rocm_visible_devices
        elif config.gpu_index is not None:
            env["ROCM_VISIBLE_DEVICES"] = str(config.gpu_index)
            env["HIP_VISIBLE_DEVICES"] = str(config.gpu_index)
        
        if config.cuda_visible_devices is not None:
            env["CUDA_VISIBLE_DEVICES"] = config.cuda_visible_devices
        elif config.gpu_index is not None:
            env["CUDA_VISIBLE_DEVICES"] = str(config.gpu_index)
        
        # ROCm optimizations
        env["HSA_FORCE_FINE_GRAIN_PCIE"] = "1"
        
        # User overrides
        env.update(config.env)
        
        return env
    
    def _get_python(self) -> Path:
        """Get the Python executable from the venv."""
        venv_python = self.base_dir / ".venv" / "bin" / "python"
        if venv_python.exists():
            return venv_python
        
        # Fallback to uv run
        return Path("uv")
    
    def run(self, config: RunConfig) -> int | ProcessInfo:
        """
        Run a training script.
        
        Args:
            config: Run configuration
            
        Returns:
            Exit code (foreground) or ProcessInfo (background)
        """
        # Resolve script path
        script_path = self.base_dir / config.script
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        # Setup environment
        env = self._setup_environment(config)
        
        if config.background:
            # Background mode - use process manager
            return self.process_manager.start_background(
                script=config.script,
                name=config.name,
                args=config.args,
                env=config.env
            )
        else:
            # Foreground mode - run directly with output
            python = self._get_python()
            
            if python.name == "uv":
                cmd = ["uv", "run", "python", "-u", str(script_path)] + config.args
            else:
                cmd = [str(python), "-u", str(script_path)] + config.args
            
            result = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                env=env
            )
            return result.returncode
    
    def status(self, name: Optional[str] = None) -> List[ProcessInfo]:
        """Get status of running/recent processes."""
        if name:
            info = self.process_manager.get_status(name)
            return [info] if info else []
        return self.process_manager.list_runs()
    
    def stop(self, name: str, force: bool = False) -> bool:
        """Stop a background process."""
        return self.process_manager.stop(name, force)
    
    def logs(self, name: str, lines: int = 50) -> List[str]:
        """Get recent log lines."""
        return self.process_manager.tail_log(name, lines)


# Convenience function for quick runs
def run_script(
    script: str,
    args: Optional[List[str]] = None,
    background: bool = False,
    **kwargs
) -> int | ProcessInfo:
    """
    Quick way to run a training script.
    
    Usage:
        from consciousness_engineering.cli import run_script
        
        # Foreground
        run_script("train_v9b_pure.py", args=["--epochs", "3"])
        
        # Background
        info = run_script("train_v9b_pure.py", background=True)
        print(f"Started with PID {info.pid}")
    """
    runner = Runner()
    config = RunConfig(
        script=script,
        args=args or [],
        background=background,
        **kwargs
    )
    return runner.run(config)
