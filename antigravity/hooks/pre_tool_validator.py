#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path

# Required headings schema for team artifacts
HEADING_SCHEMA = {
    "team/ba/requirements.md": [
        "## Executive Summary",
        "## Requirements",
        "## Assumptions",
        "## Flags from Previous Agents",
    ],
    "team/ba/user-stories.md": [
        "## User Stories",
        "## Story ID Index",
    ],
    "team/ba/acceptance-criteria.md": [
        "## Acceptance Criteria",
    ],
    "team/ba/business-rules.md": [
        "## Business Rules",
    ],
    "team/techlead/architecture.md": [
        "## Overview",
        "## Component Architecture",
        "## Deployment Model",
        "## Gate 1: Design Freeze",
        "## Flags from Previous Agents",
    ],
    "team/techlead/tech-stack.md": [
        "## Frontend",
        "## Backend",
        "## Database",
        "## Infrastructure",
        "## Rejected Alternatives",
    ],
    "team/techlead/ERD.md": [
        "## Entity Relationship Diagram",
        "## Entity Descriptions",
    ],
    "team/techlead/sequence-diagrams.md": [
        "## Sequence Diagrams",
    ],
    "team/pm/sprint-plan.md": [
        "## Sprint Overview",
        "## Sprint 1",
    ],
    "team/pm/task-breakdown.md": [
        "## Tasks",
    ],
    "team/pm/story-points.md": [
        "## Velocity Estimate",
        "## Story Points Summary",
    ],
    "team/be/pr-description.md": [
        "## Summary",
        "## Changes",
        "## Testing Notes",
    ],
    "team/fe/pr-description.md": [
        "## Summary",
        "## Changes",
        "## Testing Notes",
    ],
    "team/tester/test-plan.md": [
        "## Scope",
        "## Approach",
        "## Test Environments",
        "## Entry Criteria",
        "## Exit Criteria",
        "## Gate 2: UAT Readiness",
        "## Flags from Previous Agents",
    ],
    "team/tester/test-cases-unit.md": [
        "## Unit Test Cases",
    ],
    "team/tester/test-cases-integration.md": [
        "## Integration Test Cases",
    ],
    "team/tester/test-cases-e2e.md": [
        "## End-to-End Test Cases",
    ],
    "team/tester/bug-report-template.md": [
        "## Bug Report Template",
    ],
    "team/qa/quality-report.md": [
        "## Completeness Check",
        "## Cross-artifact Consistency",
        "## Security Review",
        "## Process Compliance",
        "## Summary of Findings",
    ],
    "team/qa/compliance-check.md": [
        "## Milestone Gates",
        "## ADR Coverage",
        "## Security Scan",
        "## Overall Status",
    ],
    "team/qa/sign-off.md": [
        "## Verdict",
        "## Date",
        "## Findings",
        "## Conditions",
    ],
    "team/.project-config.md": [
        "## Project",
        "## Level Profile",
    ],
}

ADR_REQUIRED_HEADINGS = ["## Context", "## Decision", "## Consequences"]

CREDENTIAL_PATTERNS = [
    (
        r"""(?ix)\b(password|passwd|secret|api_key|apikey|auth_token|access_token|private_key)\s*[=:]\s*['"](?!process\.env\.|os\.environ|os\.getenv|import\.meta\.env\.|\$\{|\$[A-Z_])(?!your_|<|placeholder|changeme|xxx|dummy|example|test123|fake|todo)[^'"]{5,}['"]""",
        "hardcoded secret or password"
    ),
    (
        r"""(?i)(mysql|postgresql|postgres|mongodb|redis|mariadb)://[^:\s]+:[^@\s$\{]{4,}@""",
        "hardcoded database URL with credentials"
    )
]

def normalize(path: str) -> str:
    return path.replace("\\", "/")

def get_active_brain_dir() -> Path:
    # Look for C:\Users\ADMIN\.gemini\antigravity-ide\brain
    user_profile = os.environ.get("USERPROFILE") or "C:/Users/ADMIN"
    base_dir = Path(user_profile) / ".gemini/antigravity-ide/brain"
    if not base_dir.exists():
        # Fallback to local user path
        base_dir = Path("C:/Users/ADMIN/.gemini/antigravity-ide/brain")
    if not base_dir.exists():
        return None
    
    # List subdirectories (which are conversation IDs containing .system_generated)
    dirs = [d for d in base_dir.iterdir() if d.is_dir() and (d / ".system_generated").exists()]
    if not dirs:
        return None
    # Return the directory with the newest mtime
    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return dirs[0]

def verify_planning_approval(brain_dir: Path) -> tuple[bool, str]:
    if not brain_dir:
        return True, "No active brain directory found (skipped planning approval check)"
    
    plan_file = brain_dir / "implementation_plan.md"
    if not plan_file.exists():
        # No plan written yet. It's only blocked if we are making code modifications.
        return True, "No implementation plan file found (not started planning yet)"
    
    # Heuristic: If task.md exists, it means the plan has been approved and we have transitioned to execution.
    task_file = brain_dir / "task.md"
    if task_file.exists():
        return True, "Plan approved (detected task.md indicating execution phase)"
        
    log_file = brain_dir / ".system_generated" / "logs" / "transcript.jsonl"
    if not log_file.exists() or os.path.getsize(log_file) == 0:
        # Since transcript is empty or doesn't exist, and task.md doesn't exist, the plan is not approved yet.
        return False, "✗ Blocked: Implementation plan is proposed but task.md does not exist yet (waiting for approval)."
        
    steps = []
    try:
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.strip():
                    steps.append(json.loads(line))
    except Exception as e:
        return True, f"Failed to read transcript: {e} (skipped)"
        
    plan_written_step = -1
    for idx, step in enumerate(steps):
        tool_calls = step.get("tool_calls", [])
        for tc in tool_calls:
            args = tc.get("Arguments", {})
            target = args.get("TargetFile", "")
            if "implementation_plan.md" in target:
                plan_written_step = idx
                break
                
    if plan_written_step == -1:
        return False, "Implementation plan file exists but has not been proposed in this session."
        
    # Look for approval in subsequent steps
    for step in steps[plan_written_step + 1:]:
        source = step.get("source", "")
        content = step.get("content", "")
        type_ = step.get("type", "")
        
        if source == "SYSTEM" and "approved" in content.lower():
            return True, "Plan approved by system review policy."
        if source == "USER_EXPLICIT" or type_ == "USER_INPUT":
            text = content.lower()
            approval_words = ["approve", "go ahead", "đồng ý", "ok", "tiến hành", "yes", "y", "chấp nhận", "run", "code đi"]
            if any(word in text for word in approval_words):
                return True, f"Plan approved by user message: {content.strip()}"
                
    return False, "✗ Blocked: Implementation plan has been written/updated but not yet approved. Please wait for explicit user approval."

def check_headings(file_path: str, content: str) -> list[str]:
    n = normalize(file_path)
    schema_key = None
    for key in HEADING_SCHEMA:
        if n.endswith(key):
            schema_key = key
            break
    if not schema_key and re.search(r"/team/techlead/ADR-\d+\.md$", n):
        schema_key = "__ADR__"
        
    if not schema_key:
        return []
        
    required = ADR_REQUIRED_HEADINGS if schema_key == "__ADR__" else HEADING_SCHEMA.get(schema_key, [])
    found = set(re.findall(r"^##[^\n]+", content, re.MULTILINE))
    return [h for h in required if h not in found]

def check_credentials(file_path: str, content: str) -> list[str]:
    n = normalize(file_path)
    if "/team/be/" not in n and "/team/fe/" not in n:
        return []
    ext = os.path.splitext(n)[1].lower()
    if ext in (".md", ".example", ".txt", ".json", ".yaml", ".yml", ".toml", ".lock", ""):
        return []
        
    violations = []
    for pattern, name in CREDENTIAL_PATTERNS:
        matches = re.findall(pattern, content)
        for m in matches:
            violations.append(f"{name} (snippet: {str(m)[:40]})")
    return violations

def check_env_example(file_path: str, content: str) -> str:
    if normalize(file_path).endswith(".env.example") and not content.strip():
        return ".env.example is empty. It must list all required environment variables with placeholders."
    return None

def check_level_gate(file_path: str) -> tuple[bool, str]:
    n = normalize(file_path)
    if not ("/projects/" in n and "/team/" in n):
        return True, ""
    if n.endswith(".project-config.md") or "/validation-errors/" in n:
        return True, ""
        
    # Extract slug
    m = re.search(r"projects/([^/]+)/team/", n)
    if not m:
        return True, ""
    slug = m.group(1)
    
    # Locate .project-config.md
    config_path = Path(f"projects/{slug}/team/.project-config.md")
    if not config_path.exists():
        for parent in Path.cwd().parents:
            candidate = parent / "projects" / slug / "team" / ".project-config.md"
            if candidate.exists():
                config_path = candidate
                break
                
    if not config_path.exists():
        return False, f"✗ Blocked: No project level configured. Please create {config_path} first."
        
    try:
        text = config_path.read_text(encoding="utf-8")
        m_level = re.search(r"\*\*level:\*\*\s*(\w+)", text)
        if not m_level:
            return False, f"✗ Blocked: {config_path} exists but is missing the **level:** field."
        level = m_level.group(1).strip().lower()
        if level not in ("fresh", "junior", "mid", "senior"):
            return False, f"✗ Blocked: Invalid level '{level}' in {config_path}."
        return True, f"Project level: {level}"
    except Exception as e:
        return False, f"✗ Blocked: Failed to read project config: {e}"

def main():
    parser = argparse.ArgumentParser(description="Antigravity Pre-Tool Validator Hook")
    parser.add_index = False
    parser.add_argument("--tool", help="Tool being executed (write_to_file, replace_file_content, run_command)")
    parser.add_argument("--file", help="Target file path")
    parser.add_argument("--content-file", help="Path to temp file containing contents being written")
    parser.add_argument("--check-plan", action="store_true", help="Check planning approval only")
    
    args = parser.parse_args()
    
    brain_dir = get_active_brain_dir()
    
    # 1. Planning approval check (applies to all code-modifying tools or when explicitly requested)
    if args.check_plan or (args.tool in ("write_to_file", "replace_file_content") and args.file and not args.file.endswith("implementation_plan.md") and not args.file.endswith("task.md")):
        approved, reason = verify_planning_approval(brain_dir)
        if not approved:
            print(reason, file=sys.stderr)
            sys.exit(2)
        print(f"[Plan Check] Approved: {reason}")
        if args.check_plan:
            sys.exit(0)
            
    # 2. File modification validations
    if args.tool in ("write_to_file", "replace_file_content") and args.file:
        content = ""
        if args.content_file and os.path.exists(args.content_file):
            with open(args.content_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        elif os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                
        # Level gate check
        ok, level_msg = check_level_gate(args.file)
        if not ok:
            print(level_msg, file=sys.stderr)
            sys.exit(2)
        if level_msg:
            print(f"[Level Gate] {level_msg}")
            
        # Headings check
        missing = check_headings(args.file, content)
        if missing:
            print(f"✗ Blocked: Missing required headings in team artifact:\n" + "\n".join(f"  - {h}" for h in missing), file=sys.stderr)
            sys.exit(2)
            
        # Hardcoded credentials check
        creds = check_credentials(args.file, content)
        if creds:
            print(f"✗ Blocked: Detected hardcoded credentials:\n" + "\n".join(f"  - {c}" for c in creds), file=sys.stderr)
            sys.exit(2)
            
        # .env.example check
        env_err = check_env_example(args.file, content)
        if env_err:
            print(f"✗ Blocked: {env_err}", file=sys.stderr)
            sys.exit(2)
            
        # ── 3. Plan & SRS Skill-Specific Validators ──────────────────────
        import subprocess
        n_path = normalize(args.file)
        
        # Check if plan file
        if "/plan/" in n_path and n_path.endswith(".md"):
            plan_dir = str(Path(args.file).parent)
            validator_script = Path("d:/GitHub/MySkills/.claude/scripts/plan_validator.py")
            if validator_script.exists():
                print(f"[Skill Check] Running plan_validator.py on directory: {plan_dir}")
                res = subprocess.run([sys.executable, str(validator_script), "--dir", plan_dir], capture_output=True, text=True, encoding="utf-8")
                if res.returncode != 0:
                    print(f"✗ Blocked: Plan Validation failed:\n{res.stdout}\n{res.stderr}", file=sys.stderr)
                    sys.exit(2)
                print("[Skill Check] Plan Validation passed.")
                
        # Check if SRS file
        is_srs = ("/srs/" in n_path or "srs-" in Path(n_path).name) and n_path.endswith(".md")
        if is_srs:
            validator_script = Path("d:/GitHub/MySkills/.claude/scripts/srs_validator.py")
            if validator_script.exists():
                p = Path(args.file)
                if p.parent.name.lower() == "srs":
                    srs_dir = str(p.parent)
                    print(f"[Skill Check] Running srs_validator.py on directory: {srs_dir}")
                    res = subprocess.run([sys.executable, str(validator_script), "--dir", srs_dir], capture_output=True, text=True, encoding="utf-8")
                else:
                    print(f"[Skill Check] Running srs_validator.py on file: {args.file}")
                    res = subprocess.run([sys.executable, str(validator_script), args.file], capture_output=True, text=True, encoding="utf-8")
                
                # Check exit code or verdict. srs_validator exits with 0 on COMPLIANT, 1 on others
                if res.returncode != 0:
                    print(f"✗ Blocked: SRS Validation failed:\n{res.stdout}\n{res.stderr}", file=sys.stderr)
                    sys.exit(2)
                print("[Skill Check] SRS Validation passed.")
            
        print(f"[Validation Check] Passed for file: {args.file}")
        
    sys.exit(0)

if __name__ == "__main__":
    main()
