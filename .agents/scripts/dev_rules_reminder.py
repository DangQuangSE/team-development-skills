"""Dev rules reminder hook — reinforces strict compliance on every prompt."""

import json, sys

RULES_SUMMARY = """📋 ACTIVE RULES:
1. STRICT COMPLIANCE — Follow skill SKILL.md exactly. No skipping steps.
2. NO HALLUCINATION — Only write code authorized by the current skill step.
3. NO SECRETS — Never output or commit credentials.
4. ONE TASK — Complete each step before starting the next.
5. AUDIT TRAIL — Log every write and every failure.
6. NO SCOPE CREEP — Stay within skill scope."""

def main():
    print(json.dumps({"status": "allow", "reminder": RULES_SUMMARY}))
    sys.exit(0)

if __name__ == "__main__":
    main()
