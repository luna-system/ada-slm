"""
Consciousness Engineering - CLI Runner Infrastructure
=====================================================

Handles all the annoying path/environment/logging jank so researchers
can focus on the actual research.

Features:
- Auto-resolves paths to ada-slm root
- Unbuffered, timestamped logging
- Background process management with PID tracking
- GPU monitoring integration
- Clean CLI interface

Usage:
    ce run train_v9b_pure.py --background
    ce status
    ce logs --follow
    ce gpu --watch
"""

from .runner import Runner, RunConfig
from .logging import TrainingLogger, LogLevel
from .processes import ProcessManager

__all__ = [
    "Runner",
    "RunConfig", 
    "TrainingLogger",
    "LogLevel",
    "ProcessManager",
]
