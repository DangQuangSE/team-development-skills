# Plan: Development Quality Pipeline

**Mode:** Hard
**Status:** in_progress

## Phases

- [x] Phase 1: Shared quality core and standalone `ck:quality`
- [x] Phase 2: Receipt validator and completion gate
- [x] Phase 3: Plan, Cook, Fix, and Review integration
- [ ] Phase 4: Standalone `ck:test` and TDD handoff
- [ ] Phase 5: Platform sync, documentation, and validation

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

**Last active:** 2026-07-11 02:00
**Phase in progress:** phase-04-test-skill
**Status:** Phase 1, 2, and 3 completed with issued receipts. Phase 4 not started.

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

### Next immediate action

Start Phase 4: Standalone `ck:test` and TDD Handoff (`plans/development-quality-pipeline/phase-04-test-skill.md`) — `ck-cook`'s `--tdd` path currently blocks waiting for a `RED_READY` artifact from `/ck:test --tdd --prepare`, but that skill does not exist yet.

