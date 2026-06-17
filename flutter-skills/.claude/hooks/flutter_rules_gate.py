#!/usr/bin/env python3
"""
Hook: PreToolUse Write|Edit
Blocks creating or modifying any .dart file until .anti-flutter/RULES.md has
been read at least once this session. Exit code 2 = block (tool call denied,
stderr is surfaced to the agent as the reason).

Forces every agent (main session or subagent) touching Dart code to read the
project's architecture rules first, instead of relying on each individual
agent definition to remember to say so.

Paired with rules_read_tracker.py (PostToolUse Read), which sets the marker.
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
    if not file_path.lower().endswith(".dart"):
        return

    session_id = data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID", "default")
    cwd = data.get("cwd", os.getcwd())
    root = _find_repo_root(cwd) or Path(cwd)

    marker = root / ".claude" / "session-data" / f"rules-read-{session_id}.flag"
    if marker.exists():
        return

    sys.stderr.write(
        "[flutter-rules-gate] Blocked: .anti-flutter/RULES.md has not been read yet "
        "this session. Read .anti-flutter/RULES.md (and .claude/rules/"
        "flutter-grading-standards.md) first, then retry this Dart edit.\n"
    )
    sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
