"""Universal strict gate for Antigravity — HARD STOP on violations.

Usage: strict_gate.py <gate_type>
  gate_type: write, edit, bash, agent, post_write
"""

import json, os, sys, re

BLOCKED_PATTERNS = [
    (r"(?i)(api[_-]?key|secret|password|token|credential)\s*[=:]\s*['\"][^'\"]+['\"]", "Hardcoded credential detected"),
    (r"\.env\b(?!\.example)", "Committed .env file with potential secrets"),
    (r"eval\s*\(", "Use of eval() — security risk"),
    (r"exec\s*\(", "Use of exec() — security risk"),
    (r"git\s+push\s+--force", "Force push detected — requires explicit user approval"),
    (r"npm\s+publish", "npm publish detected — requires explicit user approval"),
]

WRITE_RESTRICTED_DIRS = [
    r"\\bin\\", r"\\obj\\", r"\\.git\\", r"\\node_modules\\",
    r"\\__pycache__\\", r"\\.next\\", r"\\dist\\",
]

def check_path_blocked(path):
    for pattern in WRITE_RESTRICTED_DIRS:
        if re.search(pattern, path):
            return f"Write to restricted directory: {pattern.strip('\\\\')}"
    return None

def check_content_blocked(content):
    for pattern, msg in BLOCKED_PATTERNS:
        if re.search(pattern, content):
            return msg
    return None

def gate_write():
    path = os.environ.get("CLAUDE_FILE_PATH") or os.environ.get("ANTIGRAVITY_FILE_PATH") or ""
    reason = check_path_blocked(path)
    if reason:
        print(json.dumps({"status": "block", "reason": reason}))
        sys.exit(1)
    print(json.dumps({"status": "allow"}))
    sys.exit(0)

def gate_edit():
    print(json.dumps({"status": "allow"}))
    sys.exit(0)

def gate_bash():
    cmd = os.environ.get("CLAUDE_COMMAND") or os.environ.get("ANTIGRAVITY_COMMAND") or ""
    for pattern, msg in BLOCKED_PATTERNS:
        if re.search(pattern, cmd):
            print(json.dumps({"status": "block", "reason": msg}))
            sys.exit(1)
    print(json.dumps({"status": "allow"}))
    sys.exit(0)

def gate_agent():
    print(json.dumps({"status": "allow"}))
    sys.exit(0)

def gate_post_write():
    print(json.dumps({"status": "allow"}))
    sys.exit(0)

GATES = {
    "write": gate_write,
    "edit": gate_edit,
    "bash": gate_bash,
    "agent": gate_agent,
    "post_write": gate_post_write,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "block", "reason": "No gate type specified"}))
        sys.exit(1)
    gate_type = sys.argv[1]
    handler = GATES.get(gate_type)
    if not handler:
        print(json.dumps({"status": "block", "reason": f"Unknown gate: {gate_type}"}))
        sys.exit(1)
    handler()
