---
name: ck:quality
description: Independent senior-engineering quality auditor — architecture, ownership, domain integrity, abstraction, and maintainability. Use as `--gate` inside the ck:cook pipeline (blocks a phase on BLOCKER/HIGH/current-change MEDIUM findings) or call directly with `--audit`, `--diff`, `--changed` on any repository, directory, or file. Never writes tests and never edits production code — it returns structured findings only; ck:cook or ck:fix apply the fix.
user-invocable: true
---

# ck:quality — Independent Quality Gate & Auditor

`ck:quality` never fixes code and never writes tests. It evaluates a target against the shared Engineering Quality Contract and returns an evidence-based, structured report. Remediation is always `ck:cook`'s or `ck:fix`'s job — this skill has no `--fix`.

## Modes

Exactly one of:

- **`--gate <phase-file>`** — pipeline mode. Scope is the files the current phase created or modified. Always writes a report to `plans/{slug}/quality/{phase}-quality-report.json`. Hard-blocks the phase on any open `BLOCKER`/`HIGH` finding, or a `MEDIUM` finding introduced by the current change.
- **`--audit <path>`** — standalone mode on any file, directory, or whole repo. Report-only: prints the result, writes nothing to disk unless `--save <path>` is also given. Never blocks anything outside itself.
- **`--diff <ref>`** — audit only files changed versus `<ref>` (e.g. `main`).
- **`--changed`** — audit only the current working-tree diff (staged + unstaged).
- **`--verify <report-path>`** — re-evaluate exactly the findings in an existing report after `ck:cook`/`ck:fix` claims they're resolved. Produces a new report of the same shape; does not re-scan unrelated code.

`--save <path>` is only meaningful with `--audit`/`--diff`/`--changed`.

## Step 1 — Resolve Scope and Conventions

1. Resolve the target file set:
   - `--gate`: the phase file's "Files" section, cross-checked against `git diff` since the phase's last session-notes timestamp.
   - `--audit` / `--diff` / `--changed`: the given path, diff range, or working tree respectively.
   - `--verify`: the `reviewed_files` list from the report being verified, refreshed against current `git diff` in case scope grew.
2. Detect the stack(s) present in scope (`package.json`+`.ts` → TypeScript/Node, `pyproject.toml`/`*.py` → Python, `*.csproj` → .NET, etc. — see `references/adapters.md`).
3. Read 2-3 sibling files outside the changed set to learn actual naming, constants/error, module-structure, and DI conventions already in use. Existing convention always outranks a generic rule.

## Step 2 — Load Contract

Always load the Core tier of `references/core-contract.md`. Load Context-module sections only for categories relevant to what's in scope (e.g. skip `TXN`/transactions entirely if nothing touches persistence). Load only the `references/adapters.md` section(s) matching detected stacks — never load an adapter for a stack not present.

For `--gate`, also read the phase file's own Design Constraints / Quality Acceptance Criteria, if present, and treat them as additional applicable rules for this phase.

## Step 3 — Evaluate

Spawn **`quality-reviewer`** with: the resolved target files, detected conventions, the loaded contract sections, and (gate mode) the phase's own constraints.

A candidate issue becomes a finding only when:

- It's evidence-based — cites the exact snippet/line, not "consider improving X".
- `applicable: true` and a `confidence` level are stated. A rule that doesn't clearly apply here is skipped, not force-reported at low confidence.
- `introduced_by_current_change` is determined from `git blame`/diff evidence, not assumed.

Consolidate duplicate root causes across files into one finding referencing all locations, rather than one finding per line.

## Step 4 — Severity and Verdict

| Severity | Gate behavior |
|---|---|
| `BLOCKER` | Always blocks |
| `HIGH` | Always blocks |
| `MEDIUM` | Blocks only if `introduced_by_current_change: true` |
| `LOW` | Never blocks |
| `NOTED` | Pre-existing debt or out-of-scope suggestion; never blocks |

`--audit`/`--diff`/`--changed` compute the same verdict for information only — they never block anything outside the call itself.

Verdict is `APPROVED` (zero open blocking findings) or `CHANGES_REQUIRED` (at least one).

## Step 5 — Report

Produce a report matching `references/report-schema.json`. `--gate` always writes it to `plans/{slug}/quality/{phase}-quality-report.json`; `--audit`/`--diff`/`--changed` print it and only write with `--save <path>`.

Print exactly:

```
[ck:quality] {mode} → {APPROVED | CHANGES_REQUIRED}
Target: {scope}
Findings: {N} blocking, {N} advisory, {N} noted
Report: {path, or "not saved (use --save to persist)"}
```

If `CHANGES_REQUIRED`, list every blocking finding's `id`, `rule`, `location`, and `required_action` — this is exactly what `ck:cook`/`ck:fix` consumes to remediate.

## Constraints

- Never edit a file. Never write, run, or suggest test code — that's `ck:test`'s job.
- Never issue a receipt. Receipt issuance and hook enforcement are a separate mechanism layered on top of an `APPROVED` report; this skill only produces the report the receipt is derived from.
- `--audit`/`--diff`/`--changed` without `--save` never write to disk.
- If asked to "just fix it" or "apply the finding", refuse and point to `ck:cook`/`ck:fix` — evaluating and fixing stay separate even when both happen in the same session.

---

Full rule catalogue: `references/core-contract.md`. Stack-specific rules: `references/adapters.md`. Exact report/finding shape: `references/report-schema.json`.
