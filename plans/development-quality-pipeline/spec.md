# Development Quality Pipeline

## Goal

Make senior engineering rules available before production code is written, enforce quality approval with a fresh hash-based receipt, and separate implementation, quality review, and testing into independently callable skills.

## User Stories

- **P1:** As a developer, I want `ck:cook` to load repository conventions and a shared engineering contract before writing code.
- **P1:** As a maintainer, I want `ck:quality` to audit a phase, diff, path, or whole repository without modifying production code.
- **P1:** As a pipeline operator, I want phase completion and testing blocked when the quality receipt is missing, rejected, or stale.
- **P1:** As a developer, I want `ck:test` to own test creation and execution independently from Cook.
- **P2:** As a TDD user, I want Tester to prepare RED tests before Cook and verify them after Cook.
- **P2:** As a multi-client user, I want equivalent skills in Claude, Codex, and Antigravity.

## Functional Requirements

1. One rule-ID based quality contract is authoritative for Cook and Quality.
2. `ck:quality` supports gate, audit, changed/diff, and verify workflows.
3. Gate reports contain structured findings and create receipts only for `APPROVED` reports with zero blocking findings.
4. Receipts hash the report and exact reviewed files; any later reviewed-file edit makes the receipt invalid.
5. Hooks validate receipts when a phase is marked completed; skills also invoke the validator for portability.
6. `ck:cook` performs preflight, implementation, compile/syntax validation, and the mandatory quality loop. It does not write or run tests.
7. `ck:test` verifies quality first for planned work, owns test artifacts only, and never edits production code.
8. `ck:fix` accepts quality and test reports, applies scoped fixes, and requires quality re-verification after production changes.
9. New phased JSON plans expose compact master quality/test status plus detailed phase-local state; old plans remain readable.

## Quality and Architecture Constraints

- Semantic rules are evaluated by `ck:quality`; hooks enforce only deterministic receipt/state integrity.
- Quality Reviewer never fixes production code or approves its own changes.
- `BLOCKER`, `HIGH`, and mandatory current-change `MEDIUM` findings block a gate.
- Pre-existing debt is reported as `NOTED` or accepted debt and does not expand scope.
- No rule mandates a `common/` folder, interfaces everywhere, or constants for meaningless one-use literals.
- Core rules are language-neutral; adapters are loaded only for detected stacks.
- Platform settings are merged surgically and never replaced wholesale.

## Success Criteria

- `ck:quality` and `ck:test` exist in the canonical pack and all three client skill trees.
- Quality report, receipt, and test report schemas parse as JSON.
- Receipt issue/verify succeeds for unchanged files and fails after a reviewed file changes.
- A missing, rejected, or stale receipt prevents planned testing and phase completion.
- `ck:cook` contains no tester step and cannot bypass quality in fast mode.
- `--tdd` routes through `ck:test --tdd --prepare` and `--tdd --verify`.
- All modified settings/hook JSON parses, Python scripts compile, and mirrored skill directories match the canonical copies.

