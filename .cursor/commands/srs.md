`/srs` — Run full SRS pipeline

1. Load the `srs-workflow` skill from `.cursor/skills/srs-workflow/SKILL.md`
2. Execute all phases in order:
   - sr-brainstorm → sr-spec → sr-plan → sr-generate → sr-validate → sr-improve → sr-save
3. Each phase loads its own skill from `.cursor/skills/sr-*/SKILL.md`
4. Output the final SRS document path
