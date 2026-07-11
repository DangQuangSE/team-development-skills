# Development Skills

A collection of development-focused Claude Code skills — code review, problem-solving, diagrams, sequential thinking, skill creation, and more. All skills are self-contained and work standalone or as part of any workflow.

## Included Skills

| Skill | Invoke | Use when |
|-------|--------|----------|
| `backend-mindset` | `/backend-mindset` | Building backend systems — APIs, auth, DB, security, scaling |
| `caveman` | _(auto-triggered)_ | Terse output mode for context efficiency |
| `ck:brainstorm` | `/ck:brainstorm` | Explore and debate before committing to code |
| `ck:cook` | `/ck:cook` | Execute Markdown plans or phased JSON bundles |
| `ck:fix` | `/ck:fix` | Fix bugs using structured diagnosis |
| `ck:plan` | `/ck:plan` | Plan features before implementation (markdown) |
| `ck:plan-json` | `/ck:plan-json` | Create phased JSON plan bundles (compact master + per-phase files) |
| `ck:quality` | `/ck:quality` | Audit architecture and maintainability, or enforce a phase quality gate |
| `ck:test` | `/ck:test` | Write and run tests independently, including two-pass TDD |
| `code-review` | `/code-review` | Structured code reviews with verification |
| `mermaidjs-v11` | `/mermaidjs-v11` | Generate diagrams (flowcharts, ERD, sequence, etc.) |
| `playwright-skill` | `/playwright-skill` | Browser automation and UI testing |
| `problem-solving` | `/problem-solving` | Six creative problem-solving techniques |
| `sequential-thinking` | `/sequential-thinking` | Step-by-step reasoning for complex problems |
| `skill-creator` | (meta-skill) | Create, edit, and optimize skills |
| `strategic-compact` | `/strategic-compact` | Manage context window with timely compact suggestions |

## Usage

Open `development-skills/` directly in Claude Code — skills, hooks, agents, and commands are auto-detected from `settings.json` at pack root.

### Copy to another project

```bash
# Full pack
cp -r development-skills/skills/ <your-project>/skills/
cp -r development-skills/hooks/ <your-project>/hooks/
cp -r development-skills/agents/ <your-project>/agents/
cp -r development-skills/rules/ <your-project>/rules/
cp -r development-skills/commands/ <your-project>/commands/
cp -r development-skills/contexts/ <your-project>/contexts/
cp development-skills/settings.json <your-project>/settings.json
```

### Quick install (skills only)

```bash
cp -r development-skills/skills/* <your-project>/skills/
```

The guided pipeline is `ck:plan → ck:test --tdd --prepare` (optional) `→ ck:cook → ck:quality → ck:test → code-review`. `ck:cook` never owns tests, and phase completion requires a fresh `ck:quality` receipt.
