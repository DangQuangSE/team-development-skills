"""Strict plan.json validator for Antigravity — HARD STOP on invalid plans."""

import json, os, sys

def validate_plan(data):
    errors = []
    if not isinstance(data, dict):
        errors.append("Root must be JSON object")
        return errors
    for field in ("plan_id", "goal", "current_step"):
        if field not in data:
            errors.append(f"Missing: {field}")
    if "steps" not in data or not isinstance(data["steps"], list):
        errors.append("steps must be an array")
        return errors
    if not data["steps"]:
        errors.append("steps is empty")
    for i, step in enumerate(data["steps"]):
        p = f"steps[{i}]"
        if "step_id" not in step: errors.append(f"{p}.step_id required")
        if "description" not in step: errors.append(f"{p}.description required")
        if "status" not in step: errors.append(f"{p}.status required")
        elif step["status"] not in ("pending","in_progress","completed","failed","blocked"):
            errors.append(f"{p}.status invalid: {step['status']}")
        if "success_criteria" not in step or not isinstance(step.get("success_criteria"), list):
            errors.append(f"{p}.success_criteria required (array)")
    return errors

def main():
    path = os.environ.get("CLAUDE_FILE_PATH") or os.environ.get("ANTIGRAVITY_FILE_PATH") or ""
    if "plan.json" not in path:
        print(json.dumps({"status": "allow"}))
        sys.exit(0)
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "block", "reason": f"plan.json: invalid JSON — {e}"}))
        sys.exit(1)
    except FileNotFoundError:
        print(json.dumps({"status": "allow"}))
        sys.exit(0)
    errors = validate_plan(data)
    if errors:
        print(json.dumps({"status": "block", "reason": "plan.json validation failed", "errors": errors}))
        sys.exit(1)
    print(json.dumps({"status": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
