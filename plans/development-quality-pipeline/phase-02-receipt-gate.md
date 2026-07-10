# Phase 2: Receipt Gate

## Goal

Create deterministic report/receipt validation and hook enforcement for phase completion.

## Design Constraints

- Hash exact normalized reviewed files and report content.
- Reject paths outside the repository.
- Never claim that a hash validates SOLID or architecture.
- Hooks must fail closed for an attempted completion transition, but allow ordinary source edits for remediation.

## Files

- Add receipt script and schemas under `ck-quality`.
- Add canonical `development-skills/hooks/quality_receipt_gate.py`.
- Register the hook without replacing unrelated settings.

## Success Criteria

- Receipt creation requires `APPROVED` and zero open blockers.
- Verification rejects modified reports, missing files, changed files, invalid paths, and policy mismatches.
- Markdown and JSON phase-completion attempts without a fresh receipt are blocked.

