# Phase 4: Standalone Test Skill

## Goal

Create `ck:test` for focused testing, regression, report generation, and two-pass TDD.

## Design Constraints

- Tester may edit only test code, fixtures, mocks, and test helpers.
- Planned testing requires a fresh quality receipt except TDD prepare.
- Test failures never silently trigger production edits.
- TDD verify detects weakened or unexpectedly modified prepared tests.

## Files

- Add `development-skills/skills/ck-test/**`.
- Generalize `development-skills/agents/tester.md`.
- Add `development-skills/commands/ck/test.md`.

## Success Criteria

- Default, type-specific, all-phase, verify, and TDD commands are documented.
- Structured report distinguishes RED_READY, PASSED, FAILED, and BLOCKED.
- Failed reports hand off explicitly to `ck:fix --from-test`.

