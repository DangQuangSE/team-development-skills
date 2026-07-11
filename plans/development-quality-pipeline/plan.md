# Plan: Development Quality Pipeline

**Mode:** Hard
**Status:** completed

## Phases

- [x] Phase 1: Shared quality core and standalone `ck:quality`
- [x] Phase 2: Receipt validator and completion gate
- [x] Phase 3: Plan, Cook, Fix, and Review integration
- [x] Phase 4: Standalone `ck:test` and TDD handoff
- [x] Phase 5: Platform sync, documentation, and validation

## Architecture Decisions

- `development-skills` is canonical; `.claude`, `.codex`, and `.agents` are explicit platform mirrors.
- The quality contract lives under `ck-quality/references` and is loaded by consumers instead of copied.
- A receipt proves reviewed-file/report freshness, not the truth of a semantic review.
- Planned work stores reports under `plans/{slug}/quality` and `plans/{slug}/tests`.
- Cook may invoke Quality as a gate but never performs Quality's semantic work itself.

## Risks

- Hook input formats differ across clients; portable CLI validation remains mandatory.
- Existing plan v1 artifacts lack quality state; missing fields receive runtime defaults rather than destructive migration.
- Overly strict semantic rules may encourage overengineering; rule applicability and confidence must be explicit.

## Session Notes
<!-- Updated by cook automatically — do not edit manually -->

**Last active:** 2026-07-11 11:20
**Phase in progress:** none
**Status:** All five phases implemented and quality-approved. Testing remains an explicit `/ck:test` follow-up.

### Decisions made this session

- Built `ck:quality` as a standalone skill (`development-skills/skills/ck-quality/`) with `--gate`, `--audit`, `--diff`, `--changed`, `--verify` modes — no `--fix`.
- Core contract (`references/core-contract.md`) covers all 16 categories from spec.md plus the 3 added during design review (data consistency/transactions, dependency hygiene, documentation/decision trace), organized into always-loaded Core tier vs. per-stack Context modules to bound token cost.
- Adapters (`references/adapters.md`) shipped for TypeScript/Node, Python, .NET, Frontend, Database, Event-driven — extend via new `##` sections rather than pre-building every conceivable stack.
- Report/finding shape fixed in `references/report-schema.json`, matching the example already agreed in `plans/development-quality-pipeline/design-notes.md`. `target` is now explicitly the phase file stem (e.g. `phase-02-receipt-gate`), since the receipt gate resolves receipts by that exact string.
- Phase 2 shipped `scripts/receipt.py` (issue/verify a sha256 fingerprint over an APPROVED report + every reviewed file's exact bytes; rejects any path outside the repo) and `references/receipt-schema.json`, plus `hooks/quality_receipt_gate.py` — a PreToolUse Write|Edit hook that blocks a phase-completion *transition* (old status != completed, proposed status == completed) across JSON phase files, the JSON master `plan.json`, and Markdown `plan.md` checkboxes, unless a fresh valid receipt exists. Transition-only detection means already-checked boxes (like Phase 1's) never retroactively block unrelated edits.
- `ck:quality --gate`/`--verify` now issue the receipt automatically on `APPROVED` (SKILL.md Step 5); `--audit`/`--diff`/`--changed` never do, even with `--save`.
- To make the hook and skill actually runnable now (rather than waiting for the formal Phase 5 sync), `ck-quality`'s skill dir, the `quality-reviewer` agent, and `quality_receipt_gate.py` were copied verbatim into `.claude/skills/`, `.claude/agents/`, and `.claude/hooks/`, and the hook was registered in `.claude/settings.json`. This is a pragmatic head start, not a substitute for Phase 5's full `.codex`/`.agents` mirroring and drift-check pass.
- Hook end-to-end verified in a scratch git repo outside this repo (JSON phase block/allow, master `plan.json`, Markdown checkbox transition-only detection, tamper detection via fingerprint mismatch), then dogfooded for real: `ck:quality --gate` ran against Phase 2's own files, produced `plans/development-quality-pipeline/quality/phase-02-receipt-gate-quality-report.json` (APPROVED, zero findings) and its receipt, and the live hook allowed checking Phase 2's box in this file because of it.
- Phase 3 rewired the whole planning-to-implementation pipeline for the quality/test state: `planner`, `plan-reviewer`, `ck-plan`, `ck-plan-json` (schema, validator, reference example, design rules) now produce/require `design_constraints` + `quality`/`testing` state on every phase; `ck-cook` was rewritten as an implementation-only pipeline (preflight → validate → execute → build gate → mandatory `ck:quality` gate → approved handoff), with `--no-test` removed and `--fast` no longer able to skip the gate; `ck-fix` gained `--from-quality`/`--from-test` report-scoped input and a Step 2.5 stale-receipt re-verification; `code-reviewer` had its architecture/maintainability checks removed in favor of an explicit "Out of Scope — ck:quality's territory" section, so the two reviewers no longer overlap.
- Found and closed two gaps left over from editing `.claude/agents/*.md` directly during Phase 3: (1) the canonical `development-skills/agents/{code-reviewer,planner,plan-reviewer}.md` had not received the same edits — synced them to match; (2) `ck-plan/SKILL.md` and the `ck`/`cook.md`/`ck`/`plan.md` command metadata still referenced the now-removed `--no-test` flag and had no Design Constraints/Quality-Testing-State step — updated both.
- Dogfooded the gate again for Phase 3 itself: `ck:quality --gate` ran against all 16 phase-3 files (agents × canonical+mirror, ck-plan, ck-plan-json × 5 files, ck-cook, ck-fix, 2 command files), returned APPROVED with zero findings, and issued `plans/development-quality-pipeline/quality/phase-03-pipeline-integration-receipt.json`, which unblocked checking Phase 3's box.
- Did not touch README.md or AGENTS.md, and did not touch `.codex`/`.agents`/`flutter-skills` mirror drift for the skills changed in Phase 3 (still reference the deprecated `--no-test` flag) — both are explicitly Phase 5 scope per its Design Constraints ("skills mirror canonical contents exactly").

- Phase 4 added `development-skills/skills/ck-test/` (`SKILL.md` plus `references/test-report-schema.json` and `references/tdd-ready-schema.json`), generalized `development-skills/agents/tester.md` to the new report/verdict shape and production-code-off-limits constraint, and added `development-skills/commands/ck/test.md`. `ck:test` owns all verification (default/`--unit`/`--integration`/`--e2e`/`--all`/`--verify`/`--all-phases`/`--tdd --prepare`/`--tdd --verify`), never edits production code, never calls `ck:fix` itself, and blocks every mode except `--tdd --prepare` on a missing or stale quality receipt. Removed the now-stale "ck:test not yet available" hedges from `ck-cook/SKILL.md` now that the skill exists.
- Ran `/simplify` (4 parallel review angles) over the new `ck-test` files before gating; most findings were false positives relative to already-established `ck-quality`/`ck-cook` conventions (annotated-example schema style, repeated "read sibling files" guidance) or would have been scope creep (a receipt/fingerprint system for the short-lived TDD-prepare artifact isn't warranted — the artifact is consumed within the same session and its integrity check is the `--tdd --verify` file diff, not a persistent completion gate like quality receipts). Applied two real fixes: clarified `--all-phases` writes one report per phase (never an aggregate), and pointed `testing.status`'s field shape at `plan-design.md` instead of redefining it.
- Dogfooded the gate for Phase 4 itself: `ck:quality --gate` ran against all 6 phase-4 files, cross-checked ck-test's schemas against the actual contracts `ck-cook` (RED_READY artifact path/shape) and `ck-fix` (`--from-test` report consumption) already committed to — returned APPROVED with zero findings, issued `plans/development-quality-pipeline/quality/phase-04-test-skill-receipt.json`, which unblocked checking Phase 4's box.
- Did not mirror `ck-test`, the updated `tester` agent, or `test.md` into `.claude`/`.codex`/`.agents` — consistent with Phase 3's decision, full mirroring is Phase 5 scope.

- Phase 5 synchronized `ck-quality`, `ck-test`, `ck-cook`, `ck-fix`, `ck-plan`, `ck-plan-json`, and `code-review` across Claude, Codex, and Antigravity; preserved Codex-only `agents/openai.yaml` metadata and updated its prompts.
- Added Claude, Codex apply-patch, and Antigravity receipt-hook registrations. Fixed Antigravity's hook wrapper to forward stdin instead of silently running JSON hooks with EOF.
- Added standalone inline fallbacks for Quality and Tester when a named agent registry is unavailable, and replaced client-specific validator paths with installed-skill-root resolution.
- Updated bootstrap/docs/context routing and final code-review handoff. JSON parsing, mirror drift, receipt freshness, and whitespace validation passed; Python bytecode compilation could not run because this environment has no installed Python interpreter.
- Final review found and closed two HIGH bypasses: receipts are now bound to expected phase + filename + report target, and strict JSON validation rejects completed phase/master state without approved quality. Re-review returned APPROVED.

### Next immediate action

Run `/ck:test plans/development-quality-pipeline/plan.md` when functional testing of the workflow is desired, then perform final `/ck:code-review` before release.
