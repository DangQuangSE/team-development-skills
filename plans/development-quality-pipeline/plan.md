# Plan: Development Quality Pipeline

**Mode:** Hard
**Status:** in_progress

## Phases

- [x] Phase 1: Shared quality core and standalone `ck:quality`
- [ ] Phase 2: Receipt validator and completion gate
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

**Last active:** 2026-07-11 00:00
**Phase in progress:** phase-02-receipt-gate
**Status:** Phase 1 implemented and pending test/review; Phase 2 not started.

### Decisions made this session

- Built `ck:quality` as a standalone skill (`development-skills/skills/ck-quality/`) with `--gate`, `--audit`, `--diff`, `--changed`, `--verify` modes — no `--fix`.
- Core contract (`references/core-contract.md`) covers all 16 categories from spec.md plus the 3 added during design review (data consistency/transactions, dependency hygiene, documentation/decision trace), organized into always-loaded Core tier vs. per-stack Context modules to bound token cost.
- Adapters (`references/adapters.md`) shipped for TypeScript/Node, Python, .NET, Frontend, Database, Event-driven — extend via new `##` sections rather than pre-building every conceivable stack.
- Report/finding shape fixed in `references/report-schema.json`, matching the example already agreed in `plans/development-quality-pipeline/design-notes.md`.
- Receipt issuance intentionally deferred to Phase 2 per the phase file split — `ck:quality` currently states in its own Constraints that it never issues a receipt.
- Did not touch `code-reviewer.md`, README.md, or AGENTS.md — those are Phase 3 and Phase 5 scope respectively.

### Next immediate action

Run the Standard pipeline's Test/Review steps for this phase (tester + code-reviewer), then start Phase 2: Receipt Gate (`plans/development-quality-pipeline/phase-02-receipt-gate.md`).

