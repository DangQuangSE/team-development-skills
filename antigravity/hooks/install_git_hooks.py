#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parents[2]
    git_hooks_dir = root / ".git" / "hooks"
    
    if not git_hooks_dir.exists():
        print(f"Error: Git hooks directory not found at {git_hooks_dir}. Is git initialized?", file=sys.stderr)
        sys.exit(1)
        
    pre_commit_path = git_hooks_dir / "pre-commit"
    
    hook_content = """#!/bin/sh
# Antigravity Git Validation Hook Gateway

# Run the optimized staged check in Python
python antigravity/hooks/pre_tool_validator.py --check-staged
if [ $? -ne 0 ]; then
  echo "Git commit blocked: Validation check failed."
  exit 1
fi

exit 0
"""
    
    try:
        pre_commit_path.write_text(hook_content, encoding="utf-8")
        # Make the hook executable if on Unix/Linux/macOS
        if os.name != 'nt':
            mode = pre_commit_path.stat().st_mode
            pre_commit_path.chmod(mode | 0o111)
        print(f"Successfully installed Git Pre-Commit Hook at: {pre_commit_path}")
    except Exception as e:
        print(f"Error installing git hook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
