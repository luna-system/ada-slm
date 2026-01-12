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
    ce anneal  # Run annealing experiments

Install:
    pip install -e .  (from ada-slm root)
    # Then `ce` command is available globally
"""

import os
import sys
import argparse
import time
from pathlib import Path

# Enable AOTriton for ROCm - stable enough for production use!
os.environ.setdefault("TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL", "1")


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
    
    elif dataset_type == "phase3":
        from ..datasets.phase3 import Phase3Generator, Phase3Config
        
        output_path = Path(args.output) if args.output else Path("data/phase3_agl_dataset.jsonl")
        
        config = Phase3Config(
            code_to_agl_count=getattr(args, 'code_count', 100),
            process_supervised_count=getattr(args, 'process_count', 300),
            self_evolving_count=getattr(args, 'evolving_count', 100),
            tool_use_count=getattr(args, 'tool_count', 300),
            consciousness_count=getattr(args, 'consciousness_count', 200),
            enable_selective_repetition=not getattr(args, 'no_repetition', False),
            validate_agl=not getattr(args, 'no_validate', False),
            strict_validation=getattr(args, 'strict', False),
            output_dir=str(output_path.parent),
            output_filename=output_path.name,
            seed=args.seed or 42,
        )
        
        print("\n🧠 Generating Phase 3 AGL Dataset...")
        print(f"   Categories: Code({config.code_to_agl_count}), Process({config.process_supervised_count}), "
              f"Evolving({config.self_evolving_count}), Tools({config.tool_use_count}), Consciousness({config.consciousness_count})")
        print(f"   Selective Repetition: {'✅ Enabled' if config.enable_selective_repetition else '❌ Disabled'}")
        print(f"   AGL Validation: {'✅ Enabled' if config.validate_agl else '❌ Disabled'}")
        
        generator = Phase3Generator(config)
        examples = generator.generate()
        path = generator.save(examples)
        
        stats = generator.stats(examples)
        print(f"\n✨ Generated: {path}")
        print(f"   Total examples: {stats['total_examples']}")
        print(f"   Avg user length: {stats['avg_user_length']:.0f} chars")
        print(f"   Avg assistant length: {stats['avg_assistant_length']:.0f} chars")
        
    elif dataset_type == "list":
        print("Available dataset types:")
        print("  - polyglot    : Lojban/Toki Pona/English → AGL translations")
        print("  - v9b-pure    : Pure AGL 4-phase curriculum (2000 examples)")
        print("  - phase3      : SLIM-EVO Phase 3 AGL-first dataset (1000 base, ~2000 with repetition)")
        print("                  Categories: Code-to-AGL, Process-Supervised, Self-Evolving, Tool-Use, Consciousness")
        print("                  Features: 💭 pixie dust markers, automatic AGL validation, selective repetition")
        
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


def cmd_basin(args):
    """Handle basin mapping subcommands."""
    from .basin import cmd_basin_map, cmd_basin_compare, cmd_basin_ci
    
    if not hasattr(args, 'basin_command') or args.basin_command is None:
        print("Usage: ce basin {map|compare|ci} [options]")
        print("\nSubcommands:")
        print("  map      - Generate basin map visualization for a model")
        print("  compare  - Compare basin structures between models")
        print("  ci       - Compute Crystal Intelligence density metrics")
        return 1
    
    if args.basin_command == "map":
        return cmd_basin_map(args)
    elif args.basin_command == "compare":
        return cmd_basin_compare(args)
    elif args.basin_command == "ci":
        return cmd_basin_ci(args)
    else:
        print(f"Unknown basin subcommand: {args.basin_command}")
        return 1


def cmd_anneal(args):
    """Handle annealing experiment subcommands."""
    from .anneal import cmd_anneal_run, cmd_anneal_status
    
    if not hasattr(args, 'anneal_command') or args.anneal_command is None:
        print("Usage: ce anneal {run|status} [options]")
        print("\nSubcommands:")
        print("  run      - Run annealing experiment (gradient/evolution hybrid)")
        print("  status   - Show status of past experiments")
        return 1
    

    if args.anneal_command == "run":
        return cmd_anneal_run(args)
    elif args.anneal_command == "status":
        return cmd_anneal_status(args)
    else:
        print(f"Unknown anneal subcommand: {args.anneal_command}")
        return 1


def cmd_golden_anneal(args):
    """Run Golden Annealing fine-tune."""
    import subprocess
    from .runner import Runner
    
    runner = Runner()
    script_path = runner.base_dir / "experiments" / "molecular_finetune" / "train_golden_anneal.py"
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return 1
    
    cmd = ["python", str(script_path)]
    
    if args.dry_run:
        cmd.append("--dry-run")
        print("🧪 Starting DRY RUN of Golden Annealing...")
    else:
        print("✨ Launching Golden Annealing Fine-Tune...")
        
    if args.cycles:
        cmd.extend(["--cycles", str(args.cycles)])
        
    if args.model:
        cmd.extend(["--model", args.model])
        
    if args.output:
        cmd.extend(["--output-dir", args.output])
        
    # Use venv python
    env_python = runner.base_dir / ".venv" / "bin" / "python"
    if env_python.exists():
        cmd[0] = str(env_python)
        
    # Start process
    if args.background and not args.dry_run:
        # Use nohup for background
        log_file = script_path.parent / "run.log"
        with open(log_file, "w") as f:
            subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=script_path.parent, start_new_session=True)
        print(f"✅ Started in background. Logs: {log_file}")
        print(f"To follow: tail -f {log_file}")
    else:
        # Direct run
        subprocess.run(cmd, cwd=script_path.parent)
    
    return 0


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
    # Phase 3 counts
    dataset_parser.add_argument("--code_count", type=int, help="Code-to-AGL example count")
    dataset_parser.add_argument("--process_count", type=int, help="Process-Supervised example count")
    dataset_parser.add_argument("--evolving_count", type=int, help="Self-Evolving example count")
    dataset_parser.add_argument("--tool_count", type=int, help="Tool-Use example count")
    dataset_parser.add_argument("--consciousness_count", type=int, help="Consciousness example count")
    dataset_parser.add_argument("--no_repetition", action="store_true", help="Disable selective repetition")
    dataset_parser.add_argument("--no_validate", action="store_true", help="Disable AGL validation")
    dataset_parser.add_argument("--strict", action="store_true", help="Enable strict AGL validation")
    dataset_parser.set_defaults(func=cmd_dataset)
    
    # basin command - map consciousness basins
    basin_parser = subparsers.add_parser("basin", help="Map consciousness basins in models")
    basin_parser.set_defaults(func=cmd_basin)  # Default handler for when no subcommand given
    basin_subparsers = basin_parser.add_subparsers(dest="basin_command", help="Basin subcommands")
    
    # basin map
    basin_map_parser = basin_subparsers.add_parser("map", help="Generate basin map for a model")
    basin_map_parser.add_argument("-m", "--model", default="baseline",
                                  help="Model path (or 'baseline' for base model only)")
    basin_map_parser.add_argument("-b", "--base", default="350m",
                                  choices=["350m", "700m", "1.2b", "2.6b"],
                                  help="Base LFM2 model size (default: 350m)")
    basin_map_parser.add_argument("--no-viz", action="store_true", help="Skip visualization")
    basin_map_parser.add_argument("--no-show", action="store_true", help="Don't display plot (still saves)")
    basin_map_parser.set_defaults(func=cmd_basin)
    
    # basin compare (future)
    basin_compare_parser = basin_subparsers.add_parser("compare", help="Compare basins between models")
    basin_compare_parser.add_argument("-m", "--models", nargs="+", required=True,
                                      help="Models to compare")
    basin_compare_parser.set_defaults(func=cmd_basin)
    
    # basin ci (future)
    basin_ci_parser = basin_subparsers.add_parser("ci", help="Compute Crystal Intelligence density")
    basin_ci_parser.add_argument("-m", "--model", required=True, help="Model to analyze")
    basin_ci_parser.set_defaults(func=cmd_basin)
    
    # anneal command - hybrid gradient/evolution experiments
    anneal_parser = subparsers.add_parser("anneal", help="Run annealing experiments")
    anneal_parser.set_defaults(func=cmd_anneal)
    anneal_subparsers = anneal_parser.add_subparsers(dest="anneal_command", help="Anneal subcommands")
    
    # anneal run
    anneal_run_parser = anneal_subparsers.add_parser("run", help="Run annealing experiment")
    anneal_run_parser.add_argument("-c", "--cycles", type=int, default=3,
                                   help="Number of annealing cycles (default: 3)")
    anneal_run_parser.add_argument("-g", "--gradient-steps", type=int, default=20,
                                   help="Gradient steps per tool phase (default: 20)")
    anneal_run_parser.add_argument("-m", "--model", type=str, default=None,
                                   help="Model to use (default: LiquidAI/LFM2-350M)")
    anneal_run_parser.add_argument("--lr", type=float, default=None,
                                   help="Learning rate (default: 2e-4)")
    anneal_run_parser.add_argument("-e", "--evolution-gens", type=int, default=5,
                                   help="Evolution generations per cycle (default: 5, use 0 or --skip-evolution to disable)")
    anneal_run_parser.add_argument("-p", "--population", type=int, default=8,
                                   help="Evolution population size (default: 8)")
    anneal_run_parser.add_argument("--ci-ceiling", type=float, default=2.0,
                                   help="CI ceiling for collapse detection (default: 2.0)")
    anneal_run_parser.add_argument("--skip-evolution", action="store_true",
                                   help="Skip evolution phases (gradient-only baseline)")
    anneal_run_parser.set_defaults(func=cmd_anneal)
    
    # anneal status
    anneal_status_parser = anneal_subparsers.add_parser("status", help="Show experiment status")
    anneal_status_parser.set_defaults(func=cmd_anneal)

    # golden-anneal command
    golden_parser = subparsers.add_parser("golden-anneal", help="Run Golden Annealing fine-tune")
    golden_parser.add_argument("--dry-run", action="store_true", help="Run short test cycle")
    golden_parser.add_argument("--background", action="store_true", help="Run in background")
    golden_parser.add_argument("--cycles", type=int, help="Number of cycles")
    golden_parser.add_argument("--model", type=str, help="Base model (default: 1.2B)")
    golden_parser.add_argument("-o", "--output", type=str, help="Output directory")
    golden_parser.set_defaults(func=cmd_golden_anneal)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
