"""Session end hook for Antigravity — cleanup and summary."""

import json, sys

def main():
    print(json.dumps({"status": "allow", "cleanup": "ok"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
