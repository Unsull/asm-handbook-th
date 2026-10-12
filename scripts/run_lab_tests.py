#!/usr/bin/env python3
"""Run independent stdlib unit tests per lab folder."""
import subprocess
import sys
from pathlib import Path

labs = Path(__file__).resolve().parents[1] / "labs"
suites = [p for p in sorted(labs.iterdir()) if list(p.glob("test_*.py"))]
failures = 0
for folder in suites:
    print(f"\n== {folder.name} ==", flush=True)
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(folder), '-p', 'test_*.py', '-v'])
    failures += result.returncode != 0
if failures:
    raise SystemExit(f"Failed {failures} lab suites")
print(f"Passed {len(suites)} lab test suites")
