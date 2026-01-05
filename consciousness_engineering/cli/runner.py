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
import time
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
    
    # Terminal settings
    use_tmux: bool = True
    tmux_session_name: Optional[str] = None


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
        
        # Enable AO Triton experimental features (we've tested it works great!)
        env["TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL"] = "1"
        
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
    
    def _create_tmux_session(self, session_name: str) -> bool:
        """Create a new tmux session if it doesn't exist."""
        try:
            # Check if session exists
            result = subprocess.run(
                ["tmux", "has-session", "-t", session_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True  # Session already exists
            
            # Create new detached session with explicit bash shell
            # This ensures compatibility regardless of user's default shell (nu, fish, etc.)
            result = subprocess.run(
                ["tmux", "new-session", "-d", "-s", session_name, "bash"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            print("⚠️  tmux not found, falling back to direct execution")
            return False
    
    def _generate_session_name(self, script: str, timestamp: str = None) -> str:
        """Generate a unique tmux session name."""
        if timestamp is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
        script_base = Path(script).stem
        return f"ce-{script_base}-{timestamp}"
    
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
            # Pass the FULL environment setup, not just user overrides!
            return self.process_manager.start_background(
                script=config.script,
                name=config.name,
                args=config.args,
                env=env  # Full environment with ROCm settings!
            )
        else:
            # Foreground mode - optionally use tmux for better terminal handling
            python = self._get_python()
            
            if python.name == "uv":
                cmd = ["uv", "run", "python", "-u", str(script_path)] + config.args
            else:
                cmd = [str(python), "-u", str(script_path)] + config.args
            
            if config.use_tmux:
                # Generate session name if not provided
                session_name = config.tmux_session_name or self._generate_session_name(config.script)
                
                if self._create_tmux_session(session_name):
                    print(f"🖥️  Running in tmux session: {session_name}")
                    print(f"   Attach with: tmux attach-session -t {session_name}")
                    print(f"   Detach with: Ctrl+B, then D")
                    print()
                    
                    # Export environment variables to tmux session
                    for key, value in env.items():
                        if key not in os.environ or os.environ[key] != value:
                            subprocess.run([
                                "tmux", "set-environment", "-t", session_name,
                                key, value
                            ], capture_output=True)
                    
                    # Run command in tmux session using explicit bash
                    # This prevents issues with non-bash default shells (nu, fish, etc.)
                    cmd_string = f"cd {self.base_dir} && {' '.join(cmd)}"
                    tmux_cmd = [
                        "tmux", "send-keys", "-t", session_name,
                        f"bash -c '{cmd_string}'",
                        "Enter"
                    ]
                    
                    subprocess.run(tmux_cmd)
                    
                    # Attach to session (this will block until user detaches)
                    attach_result = subprocess.run([
                        "tmux", "attach-session", "-t", session_name
                    ])
                    return attach_result.returncode
            
            # Fallback to direct execution
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
