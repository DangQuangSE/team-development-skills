---
name: ck:cook
description: Implement a feature phase by phase from a phased JSON master or Markdown plan. Supports resumable state, TDD, tests, review, and controlled finalization.
user-invocable: true
---

# ck:cook — Structured Implementation Pipeline

Modes are mutually exclusive; Standard is the default:

- **Standard** — test and review; auto-approve only at score 9.5+ with no CRITICAL finding.
- **`--fast`** — skip tester and code reviewer.
- **`--hard`** — mandatory tests, review, and human approval.

Composable flags:

- **`--no-test`** — skip test generation and execution.
- **`--tdd`** — write failing tests before each implementation phase, then implement until green.

No old or single-file JSON compatibility is supported. Markdown `plan.md` remains a separate input format.

---

### Step 0 — Resolve the Plan

Accept:

- `--json <path>` — phased JSON master `plan.json` entry point.
- `--plan <path>` — Markdown `plan.md` entry point with sibling `phase-XX-*.md` files.

When no path is supplied, search `plans/` for a master `plan.json`, then for `plan.md`, and ask before using the discovered plan. If neither exists, suggest `/ck:plan-json` or `/ck:plan`.

Load adjacent `spec.md` when present. The spec supplies user-story coverage and TDD acceptance anchors.

---

### Step 1 — Validate and Resume a Phased JSON Plan

Run the Python bundle validator against the master before implementation:

```text
python skills/ck-plan-json/hooks/plan_validator.py plans/{slug}/plan.json
```

The validator may read the whole bundle mechanically; do not load inactive phase details into AI context. Read global context from the master once, and load or read detailed steps for only the active phase.

`current_phase` selects the active phase reference. The active phase uses `current_step` to select its next step. Report `Phase {current_phase}, step {current_step}` with both statuses:

```text
Plan: {plan_id} — {goal}
Plan status: {status}
Phase: {current_phase}/{phase_count} — {phase name} ({phase status})
Step: {current_step}/{step_count} — {step status}
Mode: {Standard | Fast | Hard}
Context: {framework} · {architecture}
```

If bundle validation reports a phase/master status mismatch, inspect only the master and its active phase:

1. If both identities match and the phase is exactly one legal monotonic transition ahead, reconcile the master with `reconcile_master`, write the master, and rerun bundle validation.
2. If the master is ahead, identities differ, dependencies differ, or more than one transition must be inferred, block without mutation and request guidance.
3. A matching state is a no-op.

An `in_progress` plan may point to a pending next phase after the previous phase completed. This is the valid ready-between-phases state.

Dependency checks confirm every prerequisite phase is completed before any write, mutation, or activation. Invalid, incomplete, or forward dependencies block and stop execution.

---

### Step 2 — Execute the Active JSON Phase

Use full-document writes or reconstructable edits so the PreToolUse validator checks proposed content.

#### Activate

Activation writes the phase file first, setting its status and active step to `in_progress`; activation writes the master second, mirroring phase and plan status without advancing `current_phase`. Rerun bundle validation at the stable checkpoint.

#### Implement Steps

For the current step:

1. Read its `input_files` for context.
2. Implement its `description` and update only declared `output_files`.
3. Verify every `success_criteria`.
4. Record written paths in `ai_generated_code`.

Step success only advances the phase `current_step`; step success does not update the master or `current_phase`. Mark the successful step `completed`, and activate the next phase-local step when one remains.

On failure, keep `debug_logs` step-local in the phase file. Append a concise `{timestamp, error, attempted_fix}` record and retry with a different approach for up to 3 remediation cycles. Cycle 4 stops and escalates.

#### Complete or Block

Completion writes the phase file first with every step completed, `status = completed`, and `current_step = step_count + 1`; completion writes the master second, mirrors completion, and advances `current_phase`.

If another phase remains, the master stays `in_progress` and points to the pending next phase. If the final phase completes, set plan `status = completed` and `current_phase = phase_count + 1`.

Blocking writes the phase file first with the active step and phase blocked; blocking writes the master second, mirrors blocked status, and does not advance either cursor. Preserve the failure diagnostics and request guidance.

Review Gate runs after each JSON phase:

- Standard and `--hard`: pause for the configured approval policy.
- `--fast`: continue automatically.

---

### Step 2.M — Execute a Markdown Plan

For each `phase-XX-*.md` in order:

1. Read phase requirements, steps, and success criteria.
2. In `--tdd`, write and confirm failing tests first.
3. Implement and verify the phase.
4. Record spec coverage when `spec.md` exists.
5. Update `plan.md` progress and overwrite its Session Notes.

Review Gate runs after each Markdown phase under the same mode policy. Markdown behavior does not use JSON cursors.

---

### Step 3 — Test

Skip for `--fast` or `--no-test`.

1. **Build Gate:** compilation or syntax validation must succeed.
2. Run the focused and full test suites; 100% must pass.
3. On failure, use up to three distinct remediation approaches and rerun the full suite.
4. A fourth failed cycle stops and escalates with the exact command, error, and attempted approaches.

With `--tdd`, confirm red before implementation and green afterward for every phase.

---

### Step 4 — Code Review

Skip only for `--fast`. Require a passing Test Gate first.

Review correctness, security, regressions, and maintainability. Standard may auto-approve only at score 9.5+ with zero CRITICAL findings; `--hard` always requires human approval. Fix and re-review up to three cycles, then escalate.

---

### Step 5 — Finalize

Finalization requires successful tests, review, and approval before the completion transition. It must not mark remaining or unfinished work completed.

- For JSON, verify every phase and step is already completed, verify both `count + 1` sentinels, then run strict bundle validation. Never synthesize completion for unexecuted work.
- For Markdown, mark only verified phases complete and update plan status and Session Notes.
- Update user-facing documentation only when the implementation changed its contract.
- Report spec coverage and unresolved items.
- Prepare conventional commit details and ask before pushing.

Final JSON summary:

```text
Plan: {plan_id}
Result: {completed_phases}/{phase_count} phases, {completed_steps}/{step_count} steps
Blocked: {blocked_count}
Debug cycles: {debug_log_count}
```

## Agents

| Agent / Skill | Step | Modes |
|---|---|---|
| `tester` | 3 | Standard, `--hard`; skipped by `--fast`/`--no-test` |
| `debugger` | 3 | Test remediation |
| `code-reviewer` | 4 | Standard, `--hard` |
| `project-manager` | 5 | Standard, `--hard` |
| `docs-manager` | 5 | Standard, `--hard` |
| `git-manager` | 5 | All modes |
