#!/usr/bin/env python3
"""Compatibility entry point for the deep foundation validator."""

from __future__ import annotations

from pathlib import Path
from runpy import run_path

ROOT = Path(__file__).resolve().parents[1]
run_path(str(ROOT / "scripts/validate_foundation.py"), run_name="__main__")
