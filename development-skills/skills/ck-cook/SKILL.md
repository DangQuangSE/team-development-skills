---
name: ck:cook
description: Implement a feature phase by phase from a phased JSON master or Markdown plan. Cook only writes code — it never writes or runs tests. Every phase goes through a mandatory quality gate (ck:quality) before it can be marked completed. Supports resumable state and TDD handoff to ck:test.
user-invocable: true
---

# ck:cook — Implementation-Only Pipeline with a Mandatory Quality Gate

Cook's job ends at implementation, a compile/syntax check, and quality approval. It does not write or run tests (`ck:test` owns that) and does not re-score maintainability at the end (`ck:quality` already did, per phase).

Modes are mutually exclusive; Standard is the default:

- **Standard** — quality gate is mandatory; auto-continue to the next phase once a phase is `APPROVED`.
- **`--fast`** — minimal status ceremony; the quality gate still runs and still blocks — there is no flag that skips it.
- **`--hard`** — same gate, plus mandatory human confirmation after each phase reaches `APPROVED` and again before the final push.

Composable flag:

- **`--tdd`** — before implementing a phase, require a `RED_READY` test artifact prepared by `/ck:test --tdd --prepare`. If `ck:test` is not yet available in this installation, block and tell the user to run their project's test framework manually to confirm RED before proceeding.

`--no-test` is removed — Cook never owned tests, so there is nothing to opt out of. No old single-file JSON or mixed-format compatibility is supported. Markdown `plan.md` remains a separate input format.

---

### Step 0 — Resolve the Plan

Accept:

- `--json <path>` — phased JSON master `plan.json` entry point.
- `--plan <path>` — Markdown `plan.md` entry point with sibling `phase-XX-*.md` files.

When no path is supplied, search `plans/` for a master `plan.json`, then for `plan.md`, and ask before using the discovered plan. If neither exists, suggest `/ck:plan-json` or `/ck:plan`.

Load adjacent `spec.md` when present. The spec supplies user-story coverage and TDD acceptance anchors.

---

### Step 1 — Preflight (Engineering Quality Profile)

Run once per phase, before implementing its steps.

Skip re-discovery when resuming a phase that already has this recorded: JSON — `quality_profile.applicable_rules` is a non-empty array; Markdown — a "Preflight:" line already exists under `## Design Constraints`. Either signal alone is sufficient to skip; do not re-read sibling files just because some sub-field looks sparse.

1. Read the phase's own `## Design Constraints` (Markdown) or `design_constraints` (JSON), plus the plan's Architecture Decisions and Risks — these are phase-specific constraints, not invented generically.
2. Read 2-3 sibling files outside the phase's scope to learn actual naming, constants/error, module-structure, and DI conventions already in use in this repository. Existing convention always outranks a generic default.
3. Record the result as the phase's `quality_profile` (JSON: `repository_conventions`, `boundaries`, `applicable_rules`, `allowed_exceptions`) or as a "Preflight:" line appended to the phase's Design Constraints section (Markdown). This is read later by both Cook's own implementation and by `ck:quality --gate` — write it once, don't duplicate the discovery.

If `--tdd`, also check for `plans/{slug}/tests/{phase}-tdd-ready.json` (or Markdown equivalent) with `status: RED_READY`. Missing artifact blocks with:

```text
BLOCKED: --tdd requires RED tests. Run /ck:test --tdd --prepare {phase} first.
```

---

### Step 2 — Validate and Resume a Phased JSON Plan

Run the Python bundle validator against the master before implementation:

```text
python skills/ck-plan-json/hooks/plan_validator.py plans/{slug}/plan.json
```

The validator may read the whole bundle mechanically; do not load inactive phase details into AI context. Read global context from the master once, and load or read detailed steps for only the active phase.

`current_phase` selects the active phase reference. The active phase uses `current_step` to select its next step. Report `Phase {current_phase}, step {current_step}` with status:

```text
Plan: {plan_id} — {goal}
Plan status: {status}
Phase: {current_phase}/{phase_count} — {phase name} ({phase status})
Step: {current_step}/{step_count} — {step status}
Mode: {Standard | Fast | Hard}
Quality: {quality_status} · Testing: {testing_status}
Context: {framework} · {architecture}
```

If bundle validation reports a phase/master status mismatch, inspect only the master and its active phase:

1. If both identities match and the phase is exactly one legal monotonic transition ahead, reconcile the master with `reconcile_master`, write the master, and rerun bundle validation.
2. If the master is ahead, identities differ, dependencies differ, or more than one transition must be inferred, block without mutation and request guidance.
3. A matching state is a no-op.

An `in_progress` plan may point to a pending next phase after the previous phase completed. This is the valid ready-between-phases state.

Dependency checks confirm every prerequisite phase is completed before any write, mutation, or activation. Invalid, incomplete, or forward dependencies block and stop execution.

---

### Step 3 — Execute the Active JSON Phase

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

#### Steps Complete → Build Gate

When every step in the phase is `completed`, do not yet write the phase `status = completed` transition — that transition is quality-gated (Step 5). First run the Build Gate (Step 4).

Blocking writes the phase file first with the active step and phase blocked; blocking writes the master second, mirrors blocked status, and does not advance either cursor. Preserve the failure diagnostics and request guidance.

---

### Step 3.M — Execute a Markdown Plan

For each `phase-XX-*.md` in order:

1. Read phase requirements, Design Constraints, and steps.
2. In `--tdd`, confirm the `RED_READY` artifact from Step 1 before implementing.
3. Implement and verify the phase's Success Criteria.
4. Record spec coverage when `spec.md` exists.
5. Run the Build Gate (Step 4) and Quality Gate (Step 5) before updating `plan.md` progress or Session Notes for this phase.

---

### Step 4 — Build Gate

Compilation or syntax validation only — Cook does not run unit or integration tests.

1. Run the project's build/compile/lint/type-check command relevant to the changed files.
2. On failure, use up to three distinct remediation approaches (spawn `debugger` if the failure is non-trivial) and rerun the Build Gate.
3. A fourth failed cycle stops and escalates with the exact command, error, and attempted approaches.

---

### Step 5 — Quality Gate (mandatory, never skipped)

Treat `ck:quality` as a black box: invoke it, act on its verdict, never second-guess or reimplement its severity rules here (those live in `ck:quality`'s own contract and may change independently of Cook).

1. Invoke `ck:quality --gate <phase-file>` against exactly the files this phase created or modified.
2. **`CHANGES_REQUIRED`** — fix every finding it lists as blocking, at the location it cites, then rerun the gate (`--verify` against the same report is acceptable once every listed finding has been addressed). Up to 3 remediation cycles; a 4th `CHANGES_REQUIRED` escalates to the human with the outstanding findings and attempted fixes.
3. **`APPROVED`** — `ck:quality` has already issued the receipt. Write the phase file's `quality` object (`status: approved`, `report`, `receipt`) and the master's `quality_status: approved` mirror, then perform the completion transition: phase file first (`status: completed`, `current_step = step_count + 1`), master second (mirrors completion, advances `current_phase`). The receipt-gate hook enforces that this transition cannot happen without the fresh receipt just issued.

`--hard` additionally pauses here for explicit human confirmation before the completion transition, even though the verdict is already `APPROVED`. Standard and `--fast` continue automatically — a passing quality gate is proof enough; there is no separate numeric review score to check.

If another phase remains, the master stays `in_progress` and points to the pending next phase — return to Step 1 (Preflight) for it. If the final phase completes, set plan `status = completed` and `current_phase = phase_count + 1`, and proceed to Step 6.

---

### Step 6 — Approved Handoff (Finalize)

Runs once, after the final phase reaches `APPROVED` and its completion transition succeeds.

- For JSON, verify every phase and step is already completed with `quality_status: approved`, verify both `count + 1` sentinels, then run strict bundle validation. Never synthesize completion for unexecuted or unapproved work.
- For Markdown, mark only verified, quality-approved phases complete and update plan status and Session Notes.
- Cook has not run or verified tests. Print explicitly:

```text
Testing: not run by Cook. Run /ck:test (once available) or your project's test suite before code review or release.
```

- Update user-facing documentation only when the implementation changed its contract (`docs-manager`; skip for `--fast`).
- Sync Markdown plan progress (`project-manager`; Markdown plans only).
- Prepare conventional commit details and ask before pushing (`git-manager`, always) — the commit message must not claim tests pass, since Cook did not run them.

Final summary:

```text
Plan: {plan_id}
Result: {completed_phases}/{phase_count} phases, {completed_steps}/{step_count} steps — all quality-approved
Blocked: {blocked_count}
Debug cycles: {debug_log_count}
Testing: not run by Cook — run /ck:test or the project test suite next
```

## Agents / Skills

| Agent / Skill  | Step | Modes |
|----------------|------|-------|
| `debugger`     | 4    | Build Gate remediation |
| `ck:quality`   | 5    | Standard, `--fast`, `--hard` — always runs, never skipped |
| `project-manager` | 6 | Markdown plans |
| `docs-manager` | 6    | Standard, `--hard` (skipped by `--fast`) |
| `git-manager`  | 6    | All modes |
