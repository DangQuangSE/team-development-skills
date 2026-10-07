import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HOOKS = ROOT / ".codex" / "hooks"


def apply_patch_event(patch: str) -> dict:
    return {"tool_name": "apply_patch", "tool_input": {"command": patch}}


def run_hook(script: str, event: dict, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        cwd=cwd,
        env=environment,
        check=False,
    )


class CodexHookTests(unittest.TestCase):
    def test_plan_validator_blocks_invalid_add_file(self) -> None:
        result = run_hook(
            "plan_validator.py",
            apply_patch_event(
                """*** Begin Patch
*** Add File: plan.json
+{"goal":"missing required fields"}
*** End Patch"""
            ),
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("[Plan Validator] BLOCKED", result.stderr)

    def test_plan_validator_allows_valid_add_file(self) -> None:
        result = run_hook(
            "plan_validator.py",
            apply_patch_event(
                """*** Begin Patch
*** Add File: plan.json
+{"plan_id":"smoke","goal":"test","current_step":1,"steps":[{"step_id":1,"description":"test","status":"pending","success_criteria":[],"input_files":[],"output_files":[]}]}
*** End Patch"""
            ),
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_post_srs_returns_codex_context_json(self) -> None:
        result = run_hook(
            "post_srs.py",
            apply_patch_event(
                """*** Begin Patch
*** Update File: .codex/skills/srs-generator/references/srs-template.md
@@
-old
+new
*** End Patch"""
            ),
        )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        output = payload["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PostToolUse")
        self.assertIn("Post-save: SRS Validation", output["additionalContext"])

    @unittest.skipUnless(os.name == "nt", "Windows runner regression")
    def test_windows_runner_resolves_repo_root_from_subdirectory(self) -> None:
        event = apply_patch_event(
            """*** Begin Patch
*** Add File: plan.json
+{"goal":"missing required fields"}
*** End Patch"""
        )
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(HOOKS / "run_from_git_root.ps1"),
                "plan_validator.py",
            ],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            cwd=ROOT / "development-skills",
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("[Plan Validator] BLOCKED", result.stderr)


if __name__ == "__main__":
    unittest.main()
