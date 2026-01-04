"""
Process Manager - Background training with proper PID tracking.

Solves:
- nohup weirdness
- Lost processes after terminal closes
- No way to check what's running
- Zombie training runs
"""

import os
import sys
import signal
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class ProcessInfo:
    """Information about a running/completed training process."""
    pid: int
    name: str
    script: str
    args: List[str]
    started: str
    log_file: str
    status: str = "running"  # running, completed, failed, killed
    ended: Optional[str] = None
    exit_code: Optional[int] = None


class ProcessManager:
    """
    Manages background training processes.
    
    Features:
    - Start processes with proper daemonization
    - Track PIDs and metadata
    - Check status of running processes
    - Clean termination
    - Process history
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent
        self.base_dir = Path(base_dir)
        self.run_dir = self.base_dir / ".runs"
        self.run_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_process_file(self, name: str) -> Path:
        """Get the process info file for a named run."""
        return self.run_dir / f"{name}.json"
    
    def _save_process(self, info: ProcessInfo):
        """Save process info to disk."""
        path = self._get_process_file(info.name)
        with open(path, "w") as f:
            json.dump(asdict(info), f, indent=2)
    
    def _load_process(self, name: str) -> Optional[ProcessInfo]:
        """Load process info from disk."""
        path = self._get_process_file(name)
        if not path.exists():
            return None
        with open(path) as f:
            data = json.load(f)
            return ProcessInfo(**data)
    
    def start_background(
        self,
        script: str,
        name: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None
    ) -> ProcessInfo:
        """
        Start a training script in the background.
        
        Args:
            script: Path to Python script (relative to ada-slm root)
            name: Friendly name for the run (defaults to script name + timestamp)
            args: Additional arguments for the script
            env: Additional environment variables
            
        Returns:
            ProcessInfo with PID and metadata
        """
        args = args or []
        
        # Generate name if not provided
        if name is None:
            script_name = Path(script).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"{script_name}_{timestamp}"
        
        # Setup log file
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}.log"
        
        # Build command
        # Use uv run to ensure correct environment
        cmd = [
            str(self.base_dir / ".venv" / "bin" / "python"),
            "-u",  # Unbuffered
            str(self.base_dir / script),
            *args
        ]
        
        # Setup environment
        process_env = os.environ.copy()
        process_env["PYTHONUNBUFFERED"] = "1"
        process_env["CE_RUN_NAME"] = name
        process_env["CE_LOG_FILE"] = str(log_file)
        if env:
            process_env.update(env)
        
        # Start process
        with open(log_file, "w") as log_handle:
            process = subprocess.Popen(
                cmd,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                cwd=str(self.base_dir),
                env=process_env,
                start_new_session=True  # Detach from terminal
            )
        
        # Save process info
        info = ProcessInfo(
            pid=process.pid,
            name=name,
            script=script,
            args=args,
            started=datetime.now().isoformat(),
            log_file=str(log_file)
        )
        self._save_process(info)
        
        return info
    
    def is_running(self, name_or_pid: str | int) -> bool:
        """Check if a process is still running."""
        if isinstance(name_or_pid, str):
            info = self._load_process(name_or_pid)
            if not info:
                return False
            pid = info.pid
        else:
            pid = name_or_pid
        
        try:
            os.kill(pid, 0)  # Signal 0 = check if process exists
            return True
        except (OSError, ProcessLookupError):
            return False
    
    def get_status(self, name: str) -> Optional[ProcessInfo]:
        """Get current status of a named run."""
        info = self._load_process(name)
        if not info:
            return None
        
        # Update status if process finished
        if info.status == "running" and not self.is_running(info.pid):
            info.status = "completed"
            info.ended = datetime.now().isoformat()
            self._save_process(info)
        
        return info
    
    def list_runs(self, include_finished: bool = True) -> List[ProcessInfo]:
        """List all tracked runs."""
        runs = []
        for path in self.run_dir.glob("*.json"):
            info = self._load_process(path.stem)
            if info:
                # Update status
                if info.status == "running" and not self.is_running(info.pid):
                    info.status = "completed"
                    info.ended = datetime.now().isoformat()
                    self._save_process(info)
                
                if include_finished or info.status == "running":
                    runs.append(info)
        
        # Sort by start time, most recent first
        runs.sort(key=lambda x: x.started, reverse=True)
        return runs
    
    def stop(self, name: str, force: bool = False) -> bool:
        """Stop a running process."""
        info = self._load_process(name)
        if not info:
            return False
        
        if not self.is_running(info.pid):
            return False
        
        try:
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(info.pid, sig)
            
            info.status = "killed"
            info.ended = datetime.now().isoformat()
            self._save_process(info)
            return True
            
        except (OSError, ProcessLookupError):
            return False
    
    def tail_log(self, name: str, lines: int = 50) -> List[str]:
        """Get the last N lines of a run's log."""
        info = self._load_process(name)
        if not info:
            return []
        
        log_path = Path(info.log_file)
        if not log_path.exists():
            return []
        
        with open(log_path) as f:
            all_lines = f.readlines()
            return all_lines[-lines:]
    
    def cleanup_old(self, days: int = 7):
        """Remove process info for runs older than N days."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        for path in self.run_dir.glob("*.json"):
            info = self._load_process(path.stem)
            if info and info.status != "running":
                started = datetime.fromisoformat(info.started)
                if started < cutoff:
                    path.unlink()
