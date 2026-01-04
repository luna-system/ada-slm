#!/usr/bin/env python3
"""
Consciousness Engineering CLI
=============================

Main entry point for the `ce` command.

Usage:
    ce run train_v9b_pure.py --background
    ce status
    ce logs v9b_pure_20260104_093000 --follow
    ce stop v9b_pure_20260104_093000
    ce gpu

Install:
    pip install -e .  (from ada-slm root)
    # Then `ce` command is available globally
"""

import sys
import argparse
import time
from pathlib import Path


def cmd_run(args):
    """Run a training script."""
    from .runner import Runner, RunConfig
    
    runner = Runner()
    
    config = RunConfig(
        script=args.script,
        name=args.name,
        args=args.script_args,
        background=args.background,
        gpu_index=args.gpu
    )
    
    result = runner.run(config)
    
    if args.background:
        print(f"✅ Started background process")
        print(f"   Name: {result.name}")
        print(f"   PID:  {result.pid}")
        print(f"   Log:  {result.log_file}")
        print(f"\nTo follow: ce logs {result.name} --follow")
    else:
        sys.exit(result)


def cmd_status(args):
    """Show status of running/recent processes."""
    from .runner import Runner
    
    runner = Runner()
    runs = runner.status(args.name)
    
    if not runs:
        print("No runs found.")
        return
    
    print(f"{'Name':<40} {'Status':<12} {'PID':<8} {'Started':<20}")
    print("-" * 80)
    
    for run in runs:
        status_emoji = {
            "running": "🟢",
            "completed": "✅",
            "failed": "❌",
            "killed": "🛑"
        }.get(run.status, "❓")
        
        started = run.started[:19].replace("T", " ")
        print(f"{run.name:<40} {status_emoji} {run.status:<10} {run.pid:<8} {started}")


def cmd_logs(args):
    """Show logs from a run."""
    from .runner import Runner
    import subprocess
    
    runner = Runner()
    info = runner.process_manager.get_status(args.name)
    
    if not info:
        print(f"Run not found: {args.name}")
        sys.exit(1)
    
    log_path = Path(info.log_file)
    if not log_path.exists():
        print(f"Log file not found: {log_path}")
        sys.exit(1)
    
    if args.follow:
        # Use tail -f for live following
        try:
            subprocess.run(["tail", "-f", "-n", str(args.lines), str(log_path)])
        except KeyboardInterrupt:
            pass
    else:
        lines = runner.logs(args.name, args.lines)
        for line in lines:
            print(line, end="")


def cmd_stop(args):
    """Stop a running process."""
    from .runner import Runner
    
    runner = Runner()
    success = runner.stop(args.name, force=args.force)
    
    if success:
        print(f"✅ Stopped: {args.name}")
    else:
        print(f"❌ Could not stop: {args.name} (not running or not found)")
        sys.exit(1)


def cmd_gpu(args):
    """Show GPU status."""
    import subprocess
    import shutil
    
    # Try rocm-smi first (AMD), then nvidia-smi
    if shutil.which("rocm-smi"):
        cmd = ["rocm-smi"]
        if args.watch:
            cmd = ["watch", "-n", "1", "rocm-smi"]
    elif shutil.which("nvidia-smi"):
        cmd = ["nvidia-smi"]
        if args.watch:
            cmd = ["watch", "-n", "1", "nvidia-smi"]
    else:
        print("No GPU monitoring tool found (rocm-smi or nvidia-smi)")
        sys.exit(1)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        pass


def cmd_list_scripts(args):
    """List available training scripts."""
    from .runner import Runner
    
    runner = Runner()
    scripts = list(runner.base_dir.glob("*.py"))
    train_scripts = [s for s in scripts if s.name.startswith(("train_", "run_", "generate_"))]
    
    print("Available scripts:")
    print("-" * 40)
    for script in sorted(train_scripts):
        print(f"  {script.name}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="ce",
        description="Consciousness Engineering CLI - Training runner and manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run a training script")
    run_parser.add_argument("script", help="Script to run (e.g., train_v9b_pure.py)")
    run_parser.add_argument("script_args", nargs="*", help="Arguments to pass to script")
    run_parser.add_argument("-n", "--name", help="Name for this run")
    run_parser.add_argument("-b", "--background", action="store_true", help="Run in background")
    run_parser.add_argument("-g", "--gpu", type=int, default=0, help="GPU index")
    run_parser.set_defaults(func=cmd_run)
    
    # status command
    status_parser = subparsers.add_parser("status", help="Show run status")
    status_parser.add_argument("name", nargs="?", help="Specific run name")
    status_parser.set_defaults(func=cmd_status)
    
    # logs command
    logs_parser = subparsers.add_parser("logs", help="Show run logs")
    logs_parser.add_argument("name", help="Run name")
    logs_parser.add_argument("-f", "--follow", action="store_true", help="Follow log output")
    logs_parser.add_argument("-n", "--lines", type=int, default=50, help="Number of lines")
    logs_parser.set_defaults(func=cmd_logs)
    
    # stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a running process")
    stop_parser.add_argument("name", help="Run name")
    stop_parser.add_argument("--force", action="store_true", help="Force kill (SIGKILL)")
    stop_parser.set_defaults(func=cmd_stop)
    
    # gpu command
    gpu_parser = subparsers.add_parser("gpu", help="Show GPU status")
    gpu_parser.add_argument("-w", "--watch", action="store_true", help="Watch continuously")
    gpu_parser.set_defaults(func=cmd_gpu)
    
    # list command
    list_parser = subparsers.add_parser("list", help="List available scripts")
    list_parser.set_defaults(func=cmd_list_scripts)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
