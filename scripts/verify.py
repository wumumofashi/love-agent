#!/usr/bin/env python3
"""Harness entry: run all scenarios and print a machine-readable summary."""
import subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
r = subprocess.run([sys.executable, str(root/"tests/run_tests.py")], capture_output=True, text=True)
print(r.stdout)
print(r.stderr, file=sys.stderr)
ok = r.returncode == 0 and "24 passed, 0 failed" in r.stdout
print(f"HARNESS_RESULT={'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
