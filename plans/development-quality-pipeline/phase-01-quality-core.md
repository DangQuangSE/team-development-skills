# Phase 1: Shared Quality Core

## Goal

Create standalone `ck:quality`, its quality reviewer agent, contract, adapters, and machine-readable report schema.

## Design Constraints

- Existing project conventions take precedence.
- Rules use stable IDs and explain applicability.
- Audit mode is read-only unless `--save` is explicit.
- Gate mode never modifies production code.

## Files

- Add `development-skills/skills/ck-quality/**`.
- Add `development-skills/agents/quality-reviewer.md`.
- Add `development-skills/commands/ck/quality.md`.

## Success Criteria

- Skill supports `--gate`, `--audit`, `--changed`, `--diff`, and `--verify`.
- Core contract covers correctness, ownership, boundaries, domain integrity, constants/messages, abstraction, errors, data consistency/transactions, concurrency, security, compatibility, observability, performance, readability, change safety, dependency hygiene, and documentation/decision trace.
- Core contract loads in three tiers (always-on core, stack/change context modules, review-only triggers) so a phase never pays token cost for irrelevant rules.
- Report schema has evidence-based findings and an unambiguous verdict.

See `design-notes.md` in this plan folder for the full rule catalogue, the preflight `quality_profile` shape, and the hook-vs-AI-reviewer split this phase must implement.

