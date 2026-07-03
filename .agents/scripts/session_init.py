"""Session init hook for Antigravity — loads rules into context."""

import json, os, sys

RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")

def main():
    rules = [f for f in os.listdir(RULES_DIR) if f.endswith(".md")]
    loaded = []
    for r in sorted(rules):
        path = os.path.join(RULES_DIR, r)
        with open(path) as f:
            content = f.read()
        loaded.append({"rule": r, "size": len(content)})
    print(json.dumps({
        "status": "allow",
        "session": {
            "rules_loaded": len(loaded),
            "rules": loaded,
            "skills_path": ".agents/skills/"
        }
    }))
    sys.exit(0)

if __name__ == "__main__":
    main()
