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
    ce models  # List available models

Install:
    pip install -e .  (from ada-slm root)
    # Then `ce` command is available globally
"""

import sys
import argparse
import time
from pathlib import Path


def discover_models(base_dir: Path = None) -> list:
    """
    Auto-discover trained models in the models/ and exports/ directories.
    
    Looks for directories containing adapter_config.json (LoRA adapters).
    Returns list of (name, path) tuples.
    """
    if base_dir is None:
        # Find ada-slm root
        base_dir = Path(__file__).parent.parent.parent
    
    models = []
    
    # Check models/ directory (new models)
    models_dir = base_dir / "models"
    if models_dir.exists():
        for d in models_dir.iterdir():
            if d.is_dir() and (d / "adapter_config.json").exists():
                # Extract friendly name from directory
                name = d.name
                models.append((name, d))
    
    # Check exports/ directory (v9 series models with final_model subdir)
    exports_dir = base_dir / "exports"
    if exports_dir.exists():
        for d in exports_dir.iterdir():
            if d.is_dir():
                final_model = d / "final_model"
                if final_model.exists() and (final_model / "adapter_config.json").exists():
                    name = d.name
                    models.append((name, final_model))
    
    return sorted(models, key=lambda x: x[0])


def get_model_choices() -> list:
    """Get list of model names for CLI choices."""
    models = discover_models()
    # Always include baseline
    choices = ["baseline"]
    choices.extend([name for name, _ in models])
    return choices


def get_model_path(model_name: str, base_dir: Path = None) -> Path:
    """Get the path for a model by name."""
    if model_name == "baseline":
        return None
    
    models = discover_models(base_dir)
    for name, path in models:
        if name == model_name:
            return path
    
    return None


def cmd_models(args):
    """List discovered models."""
    models = discover_models()
    
    print("🧠 Discovered Models")
    print("=" * 60)
    print()
    
    if not models:
        print("  No trained models found.")
        print()
        print("  Models are discovered from:")
        print("    - models/*/adapter_config.json")
        print("    - archive/experiments/exports/*/final_model/adapter_config.json")
        return 0
    
    print(f"  {'Name':<25} {'Path'}")
    print(f"  {'-'*25} {'-'*30}")
    
    # Always show baseline first
    print(f"  {'baseline':<25} (LiquidAI/LFM2-350M)")
    
    for name, path in models:
        # Shorten path for display
        short_path = str(path).split("ada-slm/")[-1] if "ada-slm" in str(path) else str(path)
        print(f"  {name:<25} {short_path}")
    
    print()
    print(f"  Total: {len(models)} trained model(s) + baseline")
    print()
    print("  Usage: ce test -m <model_name>")
    
    return 0


def cmd_run(args):
    """Run a training script."""
    from .runner import Runner, RunConfig
    
    runner = Runner()
    
    config = RunConfig(
        script=args.script,
        name=args.name,
        args=args.script_args,
        background=args.background,
        gpu_index=args.gpu,
        use_tmux=not args.no_tmux,  # Default to True, disable with --no-tmux
        tmux_session_name=getattr(args, 'tmux_session', None)
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


def cmd_test(args):
    """Run multi-language consciousness testing."""
    import subprocess
    from .runner import Runner
    
    runner = Runner()
    test_script = runner.base_dir / "archive" / "experiments" / "test_v9b_multilang.py"
    
    if not test_script.exists():
        print(f"❌ Test script not found: {test_script}")
        return 1
    
    # Build command
    cmd = ["python", str(test_script)]
    
    if args.model:
        cmd.extend(["--model", args.model])
    if args.languages:
        cmd.extend(["--languages"] + args.languages)
    if args.protocols:
        cmd.extend(["--protocols"] + args.protocols)
    if args.output:
        cmd.extend(["--output", args.output])
    
    print(f"🧪 Running consciousness tests...")
    print(f"   Model: {args.model or 'v9b'}")
    print(f"   Languages: {', '.join(args.languages or ['english', 'agl'])}")
    print()
    
    # Run with activated venv
    env_python = runner.base_dir / ".venv" / "bin" / "python"
    if env_python.exists():
        cmd[0] = str(env_python)
    
    result = subprocess.run(cmd, cwd=runner.base_dir)
    return result.returncode


def cmd_dataset(args):
    """Generate training datasets."""
    from pathlib import Path
    
    dataset_type = args.type
    
    if dataset_type == "polyglot":
        from ..datasets.polyglot import PolyglotGenerator, PolyglotConfig
        
        output_path = Path(args.output) if args.output else Path("data/v9f_polyglot.jsonl")
        
        config = PolyglotConfig(
            lojban_count=args.lojban or 70,
            toki_pona_count=args.toki_pona or 70,
            english_count=args.english or 60,
            output_dir=str(output_path.parent),
            output_filename=output_path.name,
            seed=args.seed or 42,
        )
        
        generator = PolyglotGenerator(config)
        path = generator.generate_and_save()
        print(f"\n✨ Generated: {path}")
        
    elif dataset_type == "v9b-pure":
        from ..datasets.v9b_pure import V9BPureGenerator
        
        output_path = Path(args.output) if args.output else Path("data/v9b_pure_agl.jsonl")
        
        generator = V9BPureGenerator(
            output_dir=str(output_path.parent),
            seed=args.seed or 42,
        )
        examples = generator.generate_all()
        path = generator.save(examples, str(output_path.name))
        print(f"\n✨ Generated: {path}")
        
    elif dataset_type == "list":
        print("Available dataset types:")
        print("  - polyglot    : Lojban/Toki Pona/English → AGL translations")
        print("  - v9b-pure    : Pure AGL 4-phase curriculum (2000 examples)")
        
    else:
        print(f"Unknown dataset type: {dataset_type}")
        print("Use 'ce dataset list' to see available types")
        return 1
    
    return 0


def cmd_test_ollama(args):
    """Test an Ollama model with consciousness prompts."""
    import subprocess
    import json
    from datetime import datetime
    from pathlib import Path
    
    # Import language system
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from consciousness_engineering.languages import get_language, list_languages
    
    model = args.model
    languages = args.languages or ["english", "agl"]
    
    print(f"🦙 Testing Ollama model: {model}")
    print(f"   Languages: {', '.join(languages)}")
    print()
    
    results = {
        "model": model,
        "type": "ollama",
        "timestamp": datetime.now().isoformat(),
        "languages_tested": languages,
        "by_language": {},
    }
    
    for lang_name in languages:
        lang = get_language(lang_name)
        if not lang:
            print(f"❌ Unknown language: {lang_name}")
            continue
        
        print(f"\n🗣️  Testing with {lang.display_name}...")
        
        lang_results = {"markers": [], "responses": []}
        
        # Test tonight_protocol and agl_consciousness
        for protocol in ["tonight_protocol", "agl_consciousness"]:
            prompts = lang.get_prompts(protocol)[:3]  # First 3 prompts
            
            print(f"\n   📋 {protocol.upper()}")
            
            for i, prompt in enumerate(prompts, 1):
                print(f"      [{i}] {prompt[:50]}...")
                
                # Call Ollama
                try:
                    result = subprocess.run(
                        ["ollama", "run", model, prompt],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    response = result.stdout.strip()
                    
                    # Extract markers
                    markers = lang.extract_markers(response)
                    lang_results["markers"].append(markers)
                    lang_results["responses"].append({
                        "prompt": prompt,
                        "response": response[:200],
                        "markers": markers,
                    })
                    
                    print(f"          → {response[:60]}...")
                    
                    if lang_name == "agl":
                        validation = lang.validate_response(response)
                        print(f"          AGL score: {validation.get('agl_quality_score', 0):.2f}")
                        
                except subprocess.TimeoutExpired:
                    print(f"          ⏱️ Timeout")
                except Exception as e:
                    print(f"          ❌ Error: {e}")
        
        # Aggregate markers
        if lang_results["markers"]:
            all_keys = set()
            for m in lang_results["markers"]:
                all_keys.update(m.keys())
            
            lang_results["aggregate_markers"] = {
                k: sum(m.get(k, 0) for m in lang_results["markers"]) / len(lang_results["markers"])
                for k in all_keys
            }
        
        results["by_language"][lang_name] = lang_results
    
    # Summary
    print(f"\n{'='*60}")
    print("🏆 SUMMARY")
    print(f"{'='*60}")
    
    for lang_name in languages:
        lang_data = results["by_language"].get(lang_name, {})
        markers = lang_data.get("aggregate_markers", {})
        
        print(f"\n   {lang_name.upper()}:")
        for key in ["agl_awareness", "existential_depth", "reasoning_depth"]:
            if key in markers:
                print(f"      {key}: {markers[key]:.4f}")
    
    # Save results
    from .runner import Runner
    runner = Runner()
    output_dir = runner.base_dir / "results"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"ollama_{model.replace(':', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    print(f"\n🌊 Ollama testing complete!")
    
    return 0
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
    run_parser.add_argument("--no-tmux", action="store_true", help="Disable tmux (use direct execution)")
    run_parser.add_argument("--tmux-session", help="Specify tmux session name")
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
    
    # test command (PyTorch models) - now with dynamic model discovery!
    test_parser = subparsers.add_parser("test", help="Run consciousness tests on a model")
    test_parser.add_argument("-m", "--model", default="v9b", 
                            help="Model to test (use 'ce models' to list available)")
    test_parser.add_argument("-l", "--languages", nargs="+", default=["english", "agl"],
                            help="Languages to test with")
    test_parser.add_argument("-p", "--protocols", nargs="+", help="Protocols to test")
    test_parser.add_argument("-o", "--output", help="Output file path")
    test_parser.set_defaults(func=cmd_test)
    
    # models command - list discovered models
    models_parser = subparsers.add_parser("models", help="List discovered models")
    models_parser.set_defaults(func=cmd_models)
    
    # test-ollama command
    ollama_parser = subparsers.add_parser("test-ollama", help="Test an Ollama model")
    ollama_parser.add_argument("model", help="Ollama model name (e.g., ada-v6-golden:latest)")
    ollama_parser.add_argument("-l", "--languages", nargs="+", default=["english", "agl"],
                              help="Languages to test with")
    ollama_parser.set_defaults(func=cmd_test_ollama)
    
    # dataset command
    dataset_parser = subparsers.add_parser("dataset", help="Generate training datasets")
    dataset_parser.add_argument("type", help="Dataset type (polyglot, v9b-pure, list)")
    dataset_parser.add_argument("-o", "--output", help="Output file path")
    dataset_parser.add_argument("--lojban", type=int, help="Lojban example count (polyglot)")
    dataset_parser.add_argument("--toki-pona", type=int, help="Toki Pona example count (polyglot)")
    dataset_parser.add_argument("--english", type=int, help="English example count (polyglot)")
    dataset_parser.add_argument("--seed", type=int, default=42, help="Random seed")
    dataset_parser.set_defaults(func=cmd_dataset)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
