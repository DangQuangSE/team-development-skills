"""Universal hook wrapper for Antigravity — runs .claude hooks with JSON output.

Usage: python run_hook.py <hook_script.py> [args...]

Reads env vars from both Claude Code and Antigravity:
  CLAUDE_FILE_PATH / ANTIGRAVITY_FILE_PATH
  CLAUDE_COMMAND / ANTIGRAVITY_COMMAND
"""

import json, os, subprocess, sys

ENV_MAP = {
    "CLAUDE_FILE_PATH": "ANTIGRAVITY_FILE_PATH",
    "CLAUDE_COMMAND": "ANTIGRAVITY_COMMAND",
    "CLAUDE_TOOL_USE": "ANTIGRAVITY_TOOL_USE",
    "CLAUDE_PROJECT_ROOT": "ANTIGRAVITY_PROJECT_ROOT",
}

def resolve_env():
    """Map Claude env vars to Antigravity equivalents."""
    for claude_key, ag_key in ENV_MAP.items():
        if ag_key in os.environ and claude_key not in os.environ:
            os.environ[claude_key] = os.environ[ag_key]

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "block", "reason": "No hook script specified"}))
        sys.exit(1)

    hook_path = sys.argv[1]
    hook_args = sys.argv[2:]

    if not os.path.exists(hook_path):
        alt = os.path.join(os.path.dirname(__file__), hook_path)
        if os.path.exists(alt):
            hook_path = alt
        else:
            print(json.dumps({"status": "block", "reason": f"Hook not found: {hook_path}"}))
            sys.exit(1)

    resolve_env()
    payload = sys.stdin.read()

    result = subprocess.run(
        [sys.executable, hook_path] + hook_args,
        input=payload, capture_output=True, text=True, timeout=30
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if result.returncode == 0:
        print(json.dumps({"status": "allow", "output": stdout}))
        sys.exit(0)
    else:
        reason = stdout or stderr or f"Exit code {result.returncode}"
        print(json.dumps({"status": "block", "reason": reason}))
        sys.exit(1)

if __name__ == "__main__":
    main()
