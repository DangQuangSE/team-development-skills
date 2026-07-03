# Skill Enforcement Rules (HARD ENFORCEMENT)

## Skill Discovery

- Skills are in `.agents/skills/<name>/SKILL.md`.
- When a skill is invoked, load its SKILL.md and ALL files under its `references/` directory into context.
- If a skill has `agents/` subdirectory, the agent definitions override defaults.

## Plan Compliance

- If `plans/<slug>/plan.json` exists and a cook skill is active, the agent MUST follow the plan steps in order.
- `current_step` dictates the active step. Do NOT work on steps ahead of `current_step`.
- After completing a step, increment `current_step` and update step `status` to `"completed"`.
- If a step fails after 3 remediation cycles, set `status` to `"failed"` and ask the user for direction.

## Gate Protocol

- Skill Level Gates: If a skill defines a level gate (minimum proficiency level), do NOT proceed until the user confirms they meet the requirement.
- Build Gate: Before running tests, ensure the project compiles without errors.
- Test Gate: All tests must pass before marking implementation complete.
- Approval Gate: For non-fast mode, wait for explicit user approval before finalizing.

## Artifact Handover

- When switching between skills (e.g., plan → cook), output artifacts must be written to the project directory for the next skill to read.
- Artifacts include: plan.json, spec.md, test reports, code review summaries.
- Always read the latest artifact files. Do not rely on conversation history for artifact content.
