#!/usr/bin/env python3
"""
Hook: PostToolUse (Write)
Fires after Claude writes a file.

If the written file looks like an SRS (path contains 'srs' and ends in .md),
auto-runs srs_validator.py and injects the verdict as additionalContext.
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"


def is_srs_file(file_path: str) -> bool:
    p = Path(file_path)
    if p.suffix != ".md":
        return False
    # Match: srs-*.md name OR file inside a path component named 'srs'
    path_str = str(p).lower().replace("\\", "/")
    return "srs" in p.name.lower() or "/srs/" in path_str


def run_validator(file_path: str) -> str | None:
    validator = SCRIPTS_DIR / "srs_validator.py"
    if not validator.exists():
        return None
    p = Path(file_path)
    # If file is inside a directory named 'srs', validate the whole directory
    if p.parent.name.lower() == "srs":
        cmd = [sys.executable, str(validator), "--dir", str(p.parent)]
    else:
        cmd = [sys.executable, str(validator), file_path]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=25, encoding="utf-8"
        )
        return result.stdout.strip()
    except Exception:
        return None


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = event.get("tool_name", "")
    if tool_name != "Write":
        sys.exit(0)

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not file_path or not is_srs_file(file_path):
        sys.exit(0)

    validation = run_validator(file_path)
    if not validation:
        sys.exit(0)

    output = {
        "additionalContext": (
            f"## Post-save: SRS Validation\n\n"
            f"{validation}\n\n"
            "> Fix any ERROR findings before marking the SRS as ready for review. "
            "WARN items should be resolved or explicitly acknowledged."
        )
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
