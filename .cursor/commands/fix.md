`/fix` — Diagnose and fix bugs

1. Load the `ck-fix` skill from `.cursor/skills/ck-fix/SKILL.md`
2. Accept a bug description, `--from-quality <report>`, or `--from-test <report>`.
3. Apply only the report-scoped/root-cause fix.
4. Production changes invalidate the prior receipt; run `ck:quality --verify` before finalizing.
5. Output the fix summary, changed files, and next verification command.
