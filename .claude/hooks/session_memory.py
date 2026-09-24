#!/usr/bin/env python3
"""Claude entrypoint for the bundled session-memory skill."""

import os
import runpy
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
configured_hook = os.environ.get("SESSION_MEMORY_HOOK")
candidates = ([Path(configured_hook).expanduser()] if configured_hook else []) + [
    PROJECT_ROOT / ".claude" / "skills" / "session-memory" / "hooks" / "session_memory.py",
    PROJECT_ROOT / "development-skills" / "skills" / "session-memory" / "hooks" / "session_memory.py",
    PROJECT_ROOT / "development-skills" / "hooks" / "session_memory.py",
]
PACKAGE_HOOK = next((path for path in candidates if path.is_file()), None)
if PACKAGE_HOOK is None:
    raise SystemExit(
        "session-memory implementation not found; install the session-memory skill bundle "
        "or set SESSION_MEMORY_HOOK to its session_memory.py path"
    )

args = sys.argv[1:]
if "--provider" not in args:
    args = ["--provider", "claude", *args]
sys.argv = [str(PACKAGE_HOOK), *args]
runpy.run_path(str(PACKAGE_HOOK), run_name="__main__")
