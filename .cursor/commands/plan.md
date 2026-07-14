`/plan` — Create implementation plan

1. Load the `ck-plan-json` skill from `.cursor/skills/ck-plan-json/SKILL.md`
2. Parse the user's feature request
3. Generate `plan.json` in `plans/<slug>/`
4. Validate the plan structure
5. Output next step: `/cook --json plans/<slug>/plan.json`
