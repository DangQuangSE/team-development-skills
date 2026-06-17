#!/usr/bin/env python3
"""
Hook: PostToolUse Write|Edit
Reminds the agent to follow Rule 12 in .anti-flutter/RULES.md (UI strings must
live in lib/core/constants/app_strings.dart) when a Dart edit introduces a
literal string inside a user-facing widget instead of an AppStrings.* constant.

Advisory only — never blocks, just injects additionalContext so the agent
self-corrects or justifies an exception (debug/log text, route names, asset
paths, API endpoints are allowed per Rule 12).
"""

import json
import re
import sys
from pathlib import Path

# Widgets/params that render literal text to the user.
UI_TEXT_PATTERN = re.compile(
    r"""\b(?:Text|SnackBar|AlertDialog|Tooltip|title|content|hintText|labelText|
        helperText|errorText|tooltip)\s*[:(]\s*['"]""",
    re.VERBOSE,
)

# Skip strings that are empty/whitespace/punctuation-only (spacers, separators).
TRIVIAL_LITERAL = re.compile(r"""^['"]\s*[\W_]{0,3}\s*['"]$""")

SKIP_DIR_MARKERS = ("core\\constants\\", "core/constants/", "test\\", "test/")


def extract_literal(line: str, match_end: int) -> str | None:
    quote = line[match_end - 1]
    rest = line[match_end:]
    closing = rest.find(quote)
    if closing == -1:
        return None
    return line[match_end - 1 : match_end + closing + 1]


def scan(content: str) -> list[str]:
    findings = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if "AppStrings." in line:
            continue
        if "debugPrint" in line or "print(" in line or "log(" in line:
            continue
        for match in UI_TEXT_PATTERN.finditer(line):
            literal = extract_literal(line, match.end())
            if not literal or TRIVIAL_LITERAL.match(literal):
                continue
            findings.append(f"  line {lineno}: {stripped[:100]}")
            break
    return findings


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    tool_input = data.get("tool_input", {})
    raw_path = tool_input.get("file_path", "")
    if not raw_path or not raw_path.endswith(".dart"):
        return

    normalized = raw_path.replace("/", "\\")
    if any(marker.replace("/", "\\") in normalized for marker in SKIP_DIR_MARKERS):
        return
    if Path(raw_path).name == "app_strings.dart":
        return

    content = tool_input.get("content") or tool_input.get("new_string") or ""
    if not content:
        return

    findings = scan(content)
    if not findings:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "RULE 12 CHECK (.anti-flutter/RULES.md): "
                f"possible hardcoded UI string literal(s) in {Path(raw_path).name} — "
                "move user-facing text to lib/core/constants/app_strings.dart "
                "(AppStrings.xyz) for i18n-readiness, unless this is a debug/log "
                "string or non-UI identifier (route name, asset path, API endpoint):\n"
                + "\n".join(findings[:8])
            ),
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
