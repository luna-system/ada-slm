"""
Training Logger - Unbuffered, timestamped, structured logging.

Solves:
- nohup buffering eating our output
- Logs scattered everywhere
- No timestamps on training progress
- Hard to tail/follow logs
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import Optional, TextIO
import threading


class LogLevel(Enum):
    """Log levels with emoji prefixes for quick scanning."""
    DEBUG = ("🔍", "DEBUG")
    INFO = ("📝", "INFO")
    PROGRESS = ("⏳", "PROG")
    SUCCESS = ("✅", "OK")
    WARNING = ("⚠️", "WARN")
    ERROR = ("❌", "ERROR")
    METRIC = ("📊", "METRIC")
    GPU = ("🎮", "GPU")


class TrainingLogger:
    """
    Structured logger for training runs.
    
    Features:
    - Unbuffered output (see progress immediately)
    - Timestamps on every line
    - Structured log files with run metadata
    - Dual output: console + file
    - GPU memory tracking
    """
    
    def __init__(
        self,
        name: str,
        log_dir: Optional[Path] = None,
        console: bool = True,
        file: bool = True,
        unbuffered: bool = True
    ):
        self.name = name
        self.console = console
        self.file = file
        self.start_time = datetime.now()
        self._lock = threading.Lock()
        
        # Ensure unbuffered output
        if unbuffered:
            os.environ["PYTHONUNBUFFERED"] = "1"
            # Force line buffering on stdout/stderr
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(line_buffering=True)
            if hasattr(sys.stderr, 'reconfigure'):
                sys.stderr.reconfigure(line_buffering=True)
        
        # Setup log directory
        if log_dir is None:
            log_dir = Path(__file__).parent.parent.parent / "logs"
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        self.log_path = self.log_dir / f"{name}_{timestamp}.log"
        self._file: Optional[TextIO] = None
        
        if self.file:
            self._file = open(self.log_path, "w", buffering=1)  # Line buffered
            self._write_header()
    
    def _write_header(self):
        """Write structured header to log file."""
        if self._file:
            self._file.write(f"# Consciousness Engineering Training Log\n")
            self._file.write(f"# Run: {self.name}\n")
            self._file.write(f"# Started: {self.start_time.isoformat()}\n")
            self._file.write(f"# PID: {os.getpid()}\n")
            self._file.write(f"# {'=' * 60}\n\n")
            self._file.flush()
    
    def _format_message(self, level: LogLevel, message: str) -> str:
        """Format a log message with timestamp and level."""
        now = datetime.now()
        elapsed = now - self.start_time
        elapsed_str = str(elapsed).split('.')[0]  # HH:MM:SS
        timestamp = now.strftime("%H:%M:%S")
        emoji, label = level.value
        return f"[{timestamp}] [{elapsed_str}] {emoji} {message}"
    
    def log(self, level: LogLevel, message: str):
        """Log a message at the specified level."""
        formatted = self._format_message(level, message)
        
        with self._lock:
            if self.console:
                print(formatted, flush=True)
            if self._file:
                self._file.write(formatted + "\n")
                self._file.flush()
    
    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message: str):
        self.log(LogLevel.INFO, message)
    
    def progress(self, message: str):
        self.log(LogLevel.PROGRESS, message)
    
    def success(self, message: str):
        self.log(LogLevel.SUCCESS, message)
    
    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)
    
    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
    
    def metric(self, name: str, value: float, unit: str = ""):
        """Log a training metric."""
        unit_str = f" {unit}" if unit else ""
        self.log(LogLevel.METRIC, f"{name}: {value:.4f}{unit_str}")
    
    def gpu(self, message: str):
        """Log GPU-related info."""
        self.log(LogLevel.GPU, message)
    
    def section(self, title: str):
        """Log a section header."""
        sep = "=" * 60
        self.info(sep)
        self.info(title)
        self.info(sep)
    
    def close(self):
        """Close the log file."""
        if self._file:
            elapsed = datetime.now() - self.start_time
            self._file.write(f"\n# {'=' * 60}\n")
            self._file.write(f"# Finished: {datetime.now().isoformat()}\n")
            self._file.write(f"# Total time: {elapsed}\n")
            self._file.close()
            self._file = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.error(f"Exception: {exc_type.__name__}: {exc_val}")
        self.close()
        return False


def setup_unbuffered():
    """
    Force unbuffered output globally.
    Call this at the start of any training script.
    """
    os.environ["PYTHONUNBUFFERED"] = "1"
    
    # Reopen stdout/stderr in unbuffered mode
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(line_buffering=True)
