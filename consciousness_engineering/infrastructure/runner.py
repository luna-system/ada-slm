"""
Script Runner - Eliminates path jank and buffering issues.
==========================================================

Handles:
- Auto path resolution (always runs from ada-slm root)
- Unbuffered output (see progress immediately)
- Structured logging (timestamped, organized)
- Background execution (proper daemonization)
- Process management (PID files, status checks)
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


def get_project_root() -> Path:
    """Get ada-slm project root, regardless of current directory."""
    # Walk up from this file to find pyproject.toml
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not find ada-slm project root!")


PROJECT_ROOT = get_project_root()
LOGS_DIR = PROJECT_ROOT / "logs"
PIDS_DIR = PROJECT_ROOT / ".pids"


@dataclass
class RunConfig:
    """Configuration for script execution."""
    script: str
    args: List[str] = field(default_factory=list)
    background: bool = False
    log_name: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)
    gpu_index: int = 0


@dataclass 
class RunResult:
    """Result of a script execution."""
    success: bool
    pid: Optional[int] = None
    log_path: Optional[Path] = None
    exit_code: Optional[int] = None
    error: Optional[str] = None


class ScriptRunner:
    """
    Robust script runner for consciousness engineering.
    
    Eliminates common issues:
    - Path confusion (always runs from project root)
    - Buffered output (PYTHONUNBUFFERED=1)
    - Lost logs (structured logging with timestamps)
    - Zombie processes (proper signal handling)
    """
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        LOGS_DIR.mkdir(exist_ok=True)
        PIDS_DIR.mkdir(exist_ok=True)
    
    def _get_log_path(self, name: str) -> Path:
        """Generate timestamped log path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return LOGS_DIR / f"{name}_{timestamp}.log"
    
    def _get_pid_path(self, name: str) -> Path:
        """Get PID file path for a named process."""
        return PIDS_DIR / f"{name}.pid"
    
    def _build_env(self, config: RunConfig) -> Dict[str, str]:
        """Build environment with all necessary variables."""
        env = os.environ.copy()
        
        # Force unbuffered Python output
        env["PYTHONUNBUFFERED"] = "1"
        
        # ROCm/CUDA settings
        env["PYTORCH_HIP_ALLOC_CONF"] = "max_split_size_mb:512"
        env["HSA_FORCE_FINE_GRAIN_PCIE"] = "1"
        env["HIP_VISIBLE_DEVICES"] = str(config.gpu_index)
        
        # Add any custom env vars
        env.update(config.env)
        
        return env
    
    def _build_command(self, config: RunConfig) -> List[str]:
        """Build the full command to execute."""
        # Use uv run for proper venv handling
        cmd = ["uv", "run", "python", "-u"]  # -u for unbuffered
        
        # Add script (resolve relative to project root)
        script_path = self.project_root / config.script
        if not script_path.exists():
            # Try as-is (might be absolute)
            script_path = Path(config.script)
        
        cmd.append(str(script_path))
        cmd.extend(config.args)
        
        return cmd
    
    def run(self, config: RunConfig) -> RunResult:
        """
        Run a script with proper environment and logging.
        
        Args:
            config: RunConfig with script, args, and options
            
        Returns:
            RunResult with status, PID (if background), and log path
        """
        # Setup
        log_name = config.log_name or Path(config.script).stem
        log_path = self._get_log_path(log_name)
        env = self._build_env(config)
        cmd = self._build_command(config)
        
        print(f"🚀 Running: {' '.join(cmd)}")
        print(f"📁 Working dir: {self.project_root}")
        print(f"📝 Log file: {log_path}")
        
        if config.background:
            return self._run_background(config, cmd, env, log_path, log_name)
        else:
            return self._run_foreground(config, cmd, env, log_path)
    
    def _run_foreground(
        self, 
        config: RunConfig,
        cmd: List[str], 
        env: Dict[str, str],
        log_path: Path
    ) -> RunResult:
        """Run script in foreground with live output."""
        try:
            with open(log_path, "w") as log_file:
                # Write header
                log_file.write(f"# Started: {datetime.now().isoformat()}\n")
                log_file.write(f"# Command: {' '.join(cmd)}\n")
                log_file.write(f"# Working dir: {self.project_root}\n")
                log_file.write("=" * 60 + "\n\n")
                log_file.flush()
                
                # Run with tee-like behavior
                process = subprocess.Popen(
                    cmd,
                    cwd=self.project_root,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1  # Line buffered
                )
                
                # Stream output to both console and log
                for line in process.stdout:
                    print(line, end="")
                    log_file.write(line)
                    log_file.flush()
                
                process.wait()
                
                # Write footer
                log_file.write(f"\n" + "=" * 60 + "\n")
                log_file.write(f"# Finished: {datetime.now().isoformat()}\n")
                log_file.write(f"# Exit code: {process.returncode}\n")
                
                return RunResult(
                    success=process.returncode == 0,
                    exit_code=process.returncode,
                    log_path=log_path
                )
                
        except Exception as e:
            return RunResult(success=False, error=str(e), log_path=log_path)
    
    def _run_background(
        self,
        config: RunConfig,
        cmd: List[str],
        env: Dict[str, str], 
        log_path: Path,
        log_name: str
    ) -> RunResult:
        """Run script in background with proper daemonization."""
        try:
            with open(log_path, "w") as log_file:
                # Write header
                log_file.write(f"# Started: {datetime.now().isoformat()}\n")
                log_file.write(f"# Command: {' '.join(cmd)}\n")
                log_file.write(f"# Working dir: {self.project_root}\n")
                log_file.write(f"# Mode: BACKGROUND\n")
                log_file.write("=" * 60 + "\n\n")
                log_file.flush()
                
                # Start process
                process = subprocess.Popen(
                    cmd,
                    cwd=self.project_root,
                    env=env,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    start_new_session=True  # Detach from terminal
                )
                
                # Save PID
                pid_path = self._get_pid_path(log_name)
                pid_path.write_text(str(process.pid))
                
                print(f"✅ Started in background (PID: {process.pid})")
                print(f"📝 Follow logs: tail -f {log_path}")
                print(f"🛑 Stop with: ce stop {log_name}")
                
                return RunResult(
                    success=True,
                    pid=process.pid,
                    log_path=log_path
                )
                
        except Exception as e:
            return RunResult(success=False, error=str(e))
    
    def status(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of running processes."""
        results = {}
        
        pid_files = list(PIDS_DIR.glob("*.pid")) if name is None else [self._get_pid_path(name)]
        
        for pid_file in pid_files:
            if not pid_file.exists():
                continue
                
            proc_name = pid_file.stem
            pid = int(pid_file.read_text().strip())
            
            # Check if process is still running
            try:
                os.kill(pid, 0)  # Signal 0 = check existence
                running = True
            except OSError:
                running = False
            
            # Find latest log
            logs = sorted(LOGS_DIR.glob(f"{proc_name}_*.log"), reverse=True)
            latest_log = logs[0] if logs else None
            
            results[proc_name] = {
                "pid": pid,
                "running": running,
                "log": str(latest_log) if latest_log else None
            }
            
            # Clean up stale PID file
            if not running:
                pid_file.unlink()
        
        return results
    
    def stop(self, name: str, force: bool = False) -> bool:
        """Stop a background process."""
        pid_path = self._get_pid_path(name)
        
        if not pid_path.exists():
            print(f"❌ No process found: {name}")
            return False
        
        pid = int(pid_path.read_text().strip())
        
        try:
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, sig)
            print(f"✅ Stopped {name} (PID: {pid})")
            pid_path.unlink()
            return True
        except OSError as e:
            print(f"❌ Failed to stop {name}: {e}")
            pid_path.unlink()  # Clean up stale PID
            return False
    
    def logs(self, name: str, follow: bool = False, lines: int = 50) -> Optional[Path]:
        """Get or tail logs for a process."""
        # Find latest log
        logs = sorted(LOGS_DIR.glob(f"{name}_*.log"), reverse=True)
        
        if not logs:
            print(f"❌ No logs found for: {name}")
            return None
        
        latest = logs[0]
        
        if follow:
            print(f"📝 Following: {latest}")
            print("   (Ctrl+C to stop)\n")
            subprocess.run(["tail", "-f", str(latest)])
        else:
            print(f"📝 Latest log: {latest}\n")
            subprocess.run(["tail", f"-{lines}", str(latest)])
        
        return latest


# Convenience functions
_runner = None

def get_runner() -> ScriptRunner:
    """Get singleton runner instance."""
    global _runner
    if _runner is None:
        _runner = ScriptRunner()
    return _runner


def run(script: str, *args, background: bool = False, **kwargs) -> RunResult:
    """Quick run a script."""
    config = RunConfig(
        script=script,
        args=list(args),
        background=background,
        **kwargs
    )
    return get_runner().run(config)
