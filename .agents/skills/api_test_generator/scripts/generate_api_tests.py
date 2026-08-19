#!/usr/bin/env python3
"""Compatibility wrapper for the HW06 generator."""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "hw06" / "test-generator"))
runpy.run_path(str(ROOT / "hw06" / "test-generator" / "generator.py"), run_name="__main__")
