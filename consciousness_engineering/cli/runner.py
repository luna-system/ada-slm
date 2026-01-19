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
        
        # Force RDNA3 GFX Version for consumer cards (7900 series)
        env["HSA_OVERRIDE_GFX_VERSION"] = "11.0.0"
        
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
        python = self._get_python()
        
        # Build base command
        if python.name == "uv":
            base_cmd = ["uv", "run", "python", "-u", str(script_path)] + config.args
        else:
            base_cmd = [str(python), "-u", str(script_path)] + config.args

        if config.background:
            # Background mode: Use libtmux for robust detached sessions
            import libtmux
            
            server = libtmux.Server()
            session_name = config.tmux_session_name or self._generate_session_name(config.script)
            
            # Create session (detached)
            if server.has_session(session_name):
                print(f"⚠️  Session {session_name} already exists. Attaching...")
                # We can't easily return ProcessInfo for existing session without more logic
                return 0
            
            session = server.new_session(session_name=session_name, attach=False, window_command="bash")
            pane = session.active_pane
            
            # Inject Environment
            for key, value in env.items():
                # Set session environment for future panes
                session.set_environment(key, value)
                # Also explicitly export in the running pane to be sure
                pane.send_keys(f"export {key}={value}")
            
            # Run Command
            cmd_str = f"cd {self.base_dir} && {' '.join(base_cmd)}"
            pane.send_keys(cmd_str)
            
            # Track it using ProcessManager (Hybrid approach)
            # We treat the tmux session name as the "PID" equivalent for tracking purposes
            # functionality for stopping/logging needs to know it's tmux
            # For now, we returns a ProcessInfo that points to the log file (handling logs via tmux capture?)
            # Actually, standard ProcessManager relies on PID. 
            # To keep it simple for tonight: We just rely on tmux for persistence.
            # But ProcessManager writes JSONs that `ce status` reads.
            # I will create a dummy entry so `ce status` sees it.
            
            # Extract actual PID of the python process? Hard to get immediately.
            # We'll use a placeholder PID or try to find it later. 
            # Let's just return a ProcessInfo with the Session Name as 'name'
            
            info = ProcessInfo(
                pid=0, # optimized out
                name=session_name,
                script=config.script,
                args=config.args,
                started=time.strftime("%Y-%m-%dT%H:%M:%S"),
                log_file=f"tmux:{session_name}", # Indicator
                status="running"
            )
            self.process_manager._save_process(info)
            
            return info

        else:
            # Foreground mode: Direct stdout (Simpler, cleaner)
            print(f"🚀 Running {script_path.name}...")
            print(f"   Environment: AOTriton={'1' if 'TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL' in env else '0'}")
            
            result = subprocess.run(
                base_cmd,
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
