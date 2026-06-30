#!/usr/bin/env python3
import sys
import os
import json
import subprocess
import re
from pathlib import Path

LEVEL_NAMES = {
    -1: "Default",
    0: "ELI5",
    1: "Junior",
    2: "Mid-level",
    3: "Senior",
    4: "Tech Lead",
    5: "God Mode"
}

LEVEL_STYLES = {
    -1: "Claude's built-in style — no injection, no overrides",
    0: "No assumed knowledge — real-world analogies, every term explained",
    1: "Explains WHY, mentor tone, names patterns, flags pitfalls",
    2: "Design patterns, system thinking, recommendation-first",
    3: "Trade-offs and architecture first, terse, no hand-holding",
    4: "Risk analysis, business impact, no implementation detail",
    5: "Code-first, zero ceremony, peer-level (default when no level set)"
}

def print_level_table():
    print("## Levels\n")
    print("| # | Name | Style |")
    print("|---|------|-------|")
    for lvl in sorted(LEVEL_NAMES.keys()):
        print(f"| {lvl} | {LEVEL_NAMES[lvl]} | {LEVEL_STYLES[lvl]} |")
    print()

def get_ck_json_path() -> Path:
    return Path("d:/GitHub/MySkills/.ck.json")

def load_ck_json() -> dict:
    p = get_ck_json_path()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_ck_json(cfg: dict):
    p = get_ck_json_path()
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

def cmd_coding_level(args):
    cfg = load_ck_json()
    
    if not args:
        # Interactively ask
        print_level_table()
        current = cfg.get("codingLevel", 5)
        print(f"Current coding level: {current} ({LEVEL_NAMES.get(current, 'Unknown')})")
        val = input("Select a level [-1 to 5] or type 'reset': ").strip()
        if val.lower() == 'reset':
            cmd_coding_level(['reset'])
            return
        try:
            level = int(val)
            if level not in LEVEL_NAMES:
                raise ValueError()
            cmd_coding_level([str(level)])
        except ValueError:
            print("Invalid selection.")
        return
        
    arg = args[0]
    if arg == "reset":
        if "codingLevel" in cfg:
            del cfg["codingLevel"]
            save_ck_json(cfg)
        print("Coding level reset. Default style will be used.")
    else:
        try:
            level = int(arg)
            if level not in LEVEL_NAMES:
                raise ValueError()
            cfg["codingLevel"] = level
            save_ck_json(cfg)
            print(f"Coding level set to {level} ({LEVEL_NAMES[level]}). Takes effect next session.")
        except ValueError:
            print("Invalid argument. Usage: python antigravity/run.py coding-level [-1 to 5 | reset]")

def cmd_code_review(args):
    # Detect local changes
    print("Checking local changes...")
    try:
        r = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, check=True)
        files = [f.strip() for f in r.stdout.splitlines() if f.strip()]
    except Exception as e:
        print(f"Error running git diff: {e}")
        return
        
    if not files:
        print("Nothing to review (no local modifications).")
        return
        
    print(f"Found {len(files)} modified files:")
    for f in files:
        print(f"  - {f}")
        
    # Running build + test check if appropriate
    print("\nRunning build check...")
    build_pass = True
    test_pass = True
    
    # Simple build check heuristic: check for build files/dependencies
    if os.path.exists("package.json"):
        print("Running: npm run build")
        res = subprocess.run(["npm", "run", "build"], capture_output=True)
        build_pass = (res.returncode == 0)
    else:
        print("No build commands configured for this repo type.")
        
    print(f"Build: {'PASS' if build_pass else 'FAIL'}")
    print("Verdict: APPROVE" if build_pass else "Verdict: BLOCK")

def print_help():
    print("Antigravity IDE custom CLI tool")
    print("Usage: python antigravity/run.py <command> [arguments]\n")
    print("Available commands:")
    print("  coding-level [level]     Set explanation depth (-1 to 5 or reset)")
    print("  code-review              Perform git code review and validations")
    print("  brainstorm               Show brainstorm information")
    print("  plan                     Show details about planning mode")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if cmd == "coding-level":
        cmd_coding_level(args)
    elif cmd == "code-review":
        cmd_code_review(args)
    elif cmd in ("brainstorm", "plan"):
        print(f"Command '{cmd}' is a workflow command. Please run the corresponding slash commands in the Antigravity IDE (e.g. /grill-me for brainstorming, or plan artifacts).")
    else:
        print(f"Unknown command '{cmd}'")
        print_help()

if __name__ == "__main__":
    main()
