#!/usr/bin/env python3
"""
Hook: PostToolUse Read
Marks that .anti-flutter/RULES.md has been read at least once this session.

Paired with flutter_rules_gate.py (PreToolUse Write|Edit), which blocks any
Dart Write/Edit until this marker exists — guaranteeing every agent (main
session or subagent) reads the architecture rules before writing Dart code,
regardless of which feature/agent definition is doing the editing.
"""

import json
import os
import sys
from pathlib import Path


def _find_repo_root(cwd: str) -> Path | None:
    for parent in [Path(cwd)] + list(Path(cwd).parents):
        if (parent / ".git").exists():
            return parent
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path.replace("\\", "/").endswith(".anti-flutter/RULES.md"):
        return

    session_id = data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID", "default")
    cwd = data.get("cwd", os.getcwd())
    root = _find_repo_root(cwd) or Path(cwd)

    marker_dir = root / ".claude" / "session-data"
    marker_dir.mkdir(parents=True, exist_ok=True)
    (marker_dir / f"rules-read-{session_id}.flag").write_text("1", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
