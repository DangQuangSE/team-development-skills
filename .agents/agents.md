# Agent Teams

## Default Agent

Use this agent for all general-purpose development tasks. Always load the relevant skill from `.agents/skills/<name>/SKILL.md` before starting work.

- **Model**: Gemini 3 Pro (default)
- **Skills path**: `.agents/skills/`
- **Rules path**: `.agents/rules/`
- **Strict mode**: ON — all rules are hard-enforced

## Available Skills

| Skill | Path | Description |
|-------|------|-------------|
| backend-mindset | `.agents/skills/backend-mindset/` | Backend development guidance |
| caveman | `.agents/skills/caveman/` | Terse output mode |
| ck-brainstorm | `.agents/skills/ck-brainstorm/` | Explore solutions before coding |
| ck-cook | `.agents/skills/ck-cook/` | Implement from a plan |
| ck-fix | `.agents/skills/ck-fix/` | Diagnose and fix bugs |
| ck-plan | `.agents/skills/ck-plan/` | Create implementation plans (markdown) |
| ck-plan-json | `.agents/skills/ck-plan-json/` | Create structured JSON plans |
| code-review | `.agents/skills/code-review/` | Request structured code review |
| mermaidjs-v11 | `.agents/skills/mermaidjs-v11/` | Create diagrams |
| playwright-skill | `.agents/skills/playwright-skill/` | Browser automation |
| problem-solving | `.agents/skills/problem-solving/` | Creative problem-solving |
| sequential-thinking | `.agents/skills/sequential-thinking/` | Structured reasoning |
| skill-creator | `.agents/skills/skill-creator/` | Create and modify skills |
| strategic-compact | `.agents/skills/strategic-compact/` | Context window management |
| sr-brainstorm | `.agents/skills/sr-brainstorm/` | SRS brainstorm phase |
| sr-generate | `.agents/skills/sr-generate/` | SRS generation phase |
| sr-improve | `.agents/skills/sr-improve/` | SRS improvement report |
| sr-plan | `.agents/skills/sr-plan/` | SRS planning phase |
| sr-save | `.agents/skills/sr-save/` | SRS context save |
| sr-spec | `.agents/skills/sr-spec/` | SRS spec writing |
| sr-validate | `.agents/skills/sr-validate/` | SRS validation |
| srs-generator | `.agents/skills/srs-generator/` | Generate IEEE 830 SRS |
| srs-workflow | `.agents/skills/srs-workflow/` | Full SRS workflow pipeline |
| team | `.agents/skills/team/` | Full-pipeline orchestrator |
| team-ba | `.agents/skills/team-ba/` | Business Analyst agent |
| team-dev | `.agents/skills/team-dev/` | Backend Developer agent |
| team-fe | `.agents/skills/team-fe/` | Frontend Developer agent |
| team-list | `.agents/skills/team-list/` | List projects |
| team-pm | `.agents/skills/team-pm/` | Project Manager agent |
| team-qa | `.agents/skills/team-qa/` | QA/QC agent |
| team-techlead | `.agents/skills/team-techlead/` | Technical Lead agent |
| team-test | `.agents/skills/team-test/` | Tester agent |

## Pipeline Mode (Multi-Agent)

For complex multi-step workflows, Antigravity can spawn sub-agents. Each sub-agent loads the relevant skill and executes its steps independently.

### Example: Full SRS Pipeline
1. sr-brainstorm → sr-spec → sr-plan → sr-generate → sr-validate → sr-improve → sr-save

### Example: Feature Development Pipeline
1. ck-brainstorm → ck-plan-json → ck-cook → code-review
