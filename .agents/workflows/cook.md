`/cook` — Implement from a plan

1. Load the `ck-cook` skill from `.agents/skills/ck-cook/SKILL.md`
2. Detect plan format:
   - If `plan.json` exists → use JSON mode
   - If `plan.md` exists → use markdown mode (legacy)
   - If neither → ask user for plan path
3. Execute each step following the skill's instructions exactly
4. After completion, output summary with step status
