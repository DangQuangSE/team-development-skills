# Plan: Development Quality Pipeline

**Mode:** Hard
**Status:** in_progress

## Phases

- [x] Phase 1: Shared quality core and standalone `ck:quality`
- [x] Phase 2: Receipt validator and completion gate
- [ ] Phase 3: Plan, Cook, Fix, and Review integration
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

**Last active:** 2026-07-11 01:00
**Phase in progress:** phase-03-pipeline-integration
**Status:** Phase 1 and Phase 2 completed with issued receipts. Phase 3 not started.

### Decisions made this session

- Built `ck:quality` as a standalone skill (`development-skills/skills/ck-quality/`) with `--gate`, `--audit`, `--diff`, `--changed`, `--verify` modes — no `--fix`.
- Core contract (`references/core-contract.md`) covers all 16 categories from spec.md plus the 3 added during design review (data consistency/transactions, dependency hygiene, documentation/decision trace), organized into always-loaded Core tier vs. per-stack Context modules to bound token cost.
- Adapters (`references/adapters.md`) shipped for TypeScript/Node, Python, .NET, Frontend, Database, Event-driven — extend via new `##` sections rather than pre-building every conceivable stack.
- Report/finding shape fixed in `references/report-schema.json`, matching the example already agreed in `plans/development-quality-pipeline/design-notes.md`. `target` is now explicitly the phase file stem (e.g. `phase-02-receipt-gate`), since the receipt gate resolves receipts by that exact string.
- Phase 2 shipped `scripts/receipt.py` (issue/verify a sha256 fingerprint over an APPROVED report + every reviewed file's exact bytes; rejects any path outside the repo) and `references/receipt-schema.json`, plus `hooks/quality_receipt_gate.py` — a PreToolUse Write|Edit hook that blocks a phase-completion *transition* (old status != completed, proposed status == completed) across JSON phase files, the JSON master `plan.json`, and Markdown `plan.md` checkboxes, unless a fresh valid receipt exists. Transition-only detection means already-checked boxes (like Phase 1's) never retroactively block unrelated edits.
- `ck:quality --gate`/`--verify` now issue the receipt automatically on `APPROVED` (SKILL.md Step 5); `--audit`/`--diff`/`--changed` never do, even with `--save`.
- To make the hook and skill actually runnable now (rather than waiting for the formal Phase 5 sync), `ck-quality`'s skill dir, the `quality-reviewer` agent, and `quality_receipt_gate.py` were copied verbatim into `.claude/skills/`, `.claude/agents/`, and `.claude/hooks/`, and the hook was registered in `.claude/settings.json`. This is a pragmatic head start, not a substitute for Phase 5's full `.codex`/`.agents` mirroring and drift-check pass.
- Hook end-to-end verified in a scratch git repo outside this repo (JSON phase block/allow, master `plan.json`, Markdown checkbox transition-only detection, tamper detection via fingerprint mismatch), then dogfooded for real: `ck:quality --gate` ran against Phase 2's own files, produced `plans/development-quality-pipeline/quality/phase-02-receipt-gate-quality-report.json` (APPROVED, zero findings) and its receipt, and the live hook allowed checking Phase 2's box in this file because of it.
- Did not touch `code-reviewer.md`, README.md, or AGENTS.md — those are Phase 3 and Phase 5 scope respectively.

### Next immediate action

Start Phase 3: Pipeline Integration (`plans/development-quality-pipeline/phase-03-pipeline-integration.md`) — update planner/plan-reviewer/ck-plan/ck-plan-json for quality+test state, then rewrite `ck-cook` as preflight → implement → quality gate → remediation → approved handoff, then update `ck-fix`/code-reviewer to consume quality/test artifacts.

