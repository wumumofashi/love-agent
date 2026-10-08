#!/usr/bin/env python3
"""Harness entry: rule scenarios + LLM pipeline tests, machine-readable summary."""
import subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
ok = True
for script in ["tests/run_tests.py", "tests/test_llm_pipeline.py"]:
    r = subprocess.run([sys.executable, str(root/script)], capture_output=True, text=True)
    print(r.stdout); print(r.stderr, file=sys.stderr)
    if r.returncode != 0: ok = False
print(f"HARNESS_RESULT={'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
