# Phase 3: Pipeline Integration

## Goal

Move quality left into planning and make Cook implementation-only with a mandatory quality loop.

## Design Constraints

- Fast mode may reduce ceremony but never skips quality.
- `--no-test` is deprecated because Cook no longer owns tests.
- `--tdd` blocks until Tester prepares RED tests.
- Existing plans without v2 fields remain executable with mandatory runtime quality defaults.

## Files

- Update planner, plan reviewer, `ck-plan`, `ck-plan-json`, schemas, examples, and validator.
- Rewrite `ck-cook` and command metadata.
- Update `ck-fix`, code reviewer, and code-review orchestration to consume quality/test artifacts.

## Success Criteria

- Every new phase carries design constraints and quality/test state.
- Cook flow is preflight → implement → compile/syntax → quality gate → remediation → approved handoff.
- No undefined numeric review score remains.

