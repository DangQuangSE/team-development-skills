`/cook` — Implement from a plan

1. Load `.agents/skills/ck-cook/SKILL.md` and pass through all arguments.
2. Resolve `--json <plan.json>` or `--plan <plan.md>`; Markdown is supported, not legacy.
3. Run engineering preflight before the first production write.
4. Implement the active phase and run only the build/syntax gate — Cook never writes or runs tests.
5. Invoke `ck:quality --gate`; blocking findings must be fixed and verified before completion.
6. Output the implementation/quality status and the exact `/test` command to run next.
