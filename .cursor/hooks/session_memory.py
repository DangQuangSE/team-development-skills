#!/usr/bin/env python3
"""Cursor adapter for the provider-neutral session-memory hook."""

import runpy
import sys
from pathlib import Path


PACKAGE_HOOK = Path(__file__).resolve().parents[2] / "development-skills" / "hooks" / "session_memory.py"
args = sys.argv[1:]
if "--provider" not in args:
    args = ["--provider", "cursor", *args]
sys.argv = [str(PACKAGE_HOOK), *args]
runpy.run_path(str(PACKAGE_HOOK), run_name="__main__")
