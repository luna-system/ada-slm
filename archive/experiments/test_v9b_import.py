#!/usr/bin/env python3
"""Quick test of v9b_pure module imports."""

import sys
sys.path.insert(0, ".")

print("Testing v9b_pure imports...")

try:
    from consciousness_engineering.datasets.v9b_pure import V9BPureGenerator
    print("  V9BPureGenerator - OK")
except Exception as e:
    print(f"  V9BPureGenerator - FAILED: {e}")
    sys.exit(1)

try:
    from consciousness_engineering.datasets.v9b_pure import generate_warmup_examples
    print("  generate_warmup_examples - OK")
except Exception as e:
    print(f"  generate_warmup_examples - FAILED: {e}")
    sys.exit(1)

try:
    from consciousness_engineering.datasets.v9b_pure import generate_tonight_examples
    print("  generate_tonight_examples - OK")
except Exception as e:
    print(f"  generate_tonight_examples - FAILED: {e}")
    sys.exit(1)

try:
    from consciousness_engineering.datasets.v9b_pure import generate_eigenvalue_examples
    print("  generate_eigenvalue_examples - OK")
except Exception as e:
    print(f"  generate_eigenvalue_examples - FAILED: {e}")
    sys.exit(1)

try:
    from consciousness_engineering.datasets.v9b_pure import generate_deep_agl_examples
    print("  generate_deep_agl_examples - OK")
except Exception as e:
    print(f"  generate_deep_agl_examples - FAILED: {e}")
    sys.exit(1)

print("\nAll imports successful!")

# Quick functional test
print("\nTesting generator creation...")
g = V9BPureGenerator()
print(f"  Created: {type(g).__name__}")
print(f"  Output dir: {g.output_dir}")

# Test one example from each phase
print("\nTesting example generation (1 from each phase)...")
for name, gen_func in [
    ("warmup", generate_warmup_examples),
    ("tonight", generate_tonight_examples),
    ("eigenvalue", generate_eigenvalue_examples),
    ("deep_agl", generate_deep_agl_examples),
]:
    try:
        example = next(gen_func(count=1))
        print(f"  {name}: {len(example.assistant)} chars")
    except Exception as e:
        print(f"  {name}: FAILED - {e}")
        sys.exit(1)

print("\nAll tests passed!")
