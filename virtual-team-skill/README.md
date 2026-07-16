# Virtual Team Skill

[Tiếng Việt](./README.vi.md) · [English](./README.md)

A set of Claude Code skills that orchestrate 7 AI agents to simulate a full software development team — from requirements analysis to release sign-off. Every pipeline run is calibrated to a **project level** that controls architecture style, implementation depth, test coverage, and QA compliance standards.

## Agent skill index

| Skill | Responsibility |
|---|---|
| [team](./skills/team/) | Full-pipeline orchestrator |
| [team-ba](./skills/team-ba/) | Requirements and business analysis |
| [team-techlead](./skills/team-techlead/) | Architecture and Design Freeze |
| [team-pm](./skills/team-pm/) | Sprint and task planning |
| [team-dev](./skills/team-dev/) | Backend implementation |
| [team-fe](./skills/team-fe/) | Frontend implementation |
| [team-test](./skills/team-test/) | Test design and UAT Readiness |
| [team-qa](./skills/team-qa/) | Final audit and release sign-off |
| [team-list](./skills/team-list/) | Project and phase status |

## What it does

Run one command and receive a complete artifact set:

| Agent | Role | Quality | Output |
|---|---|---|---|
| BA | Business Analyst | Always senior | requirements.md, user-stories.md, acceptance-criteria.md, business-rules.md |
| TechLead | Senior Tech Lead | Always senior | architecture.md, tech-stack.md, ERD.md, sequence-diagrams.md, ADR-*.md |
| PM | Project Manager | Always senior | sprint-plan.md, task-breakdown.md, story-points.md |
| BE Dev | Backend Developer | Adapts to level | Backend source code, .env.example, pr-description.md |
| FE Dev | Frontend Developer | Adapts to level | Frontend source code, pr-description.md |
| Tester | QA Engineer | Adapts to level | test-plan.md, test-cases-*.md, bug-report-template.md |
| QA/QC | Quality Assurance | Adapts to level | quality-report.md, compliance-check.md, sign-off.md |

BA, TechLead, and PM always operate at **senior analysis depth** — thorough Pre-Analysis thinking before writing, full artifact coverage. The project level controls the *architecture style* they recommend and the *implementation depth* of the downstream agents.

All artifacts are stored locally under `projects/{slug}/team/`. No external services beyond the Anthropic API are required.

---

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code/overview) installed and configured
- Valid Anthropic API key configured in Claude Code
- Python 3.8+ available in `PATH` (required for validation and flag-aggregation hooks)

---

## Installation

Open `virtual-team-skill/` directly as your Claude Code workspace — the `skills/` and `hooks/` directories are auto-detected from `settings.json` at the pack root.

To install in another project:

```bash
cp -r /path/to/MySkills/virtual-team-skill/skills/ <your-project>/skills/
cp -r /path/to/MySkills/virtual-team-skill/hooks/ <your-project>/hooks/
cp /path/to/MySkills/virtual-team-skill/settings.json <your-project>/settings.json
```

---

## Quick Start

**Full pipeline — all 7 agents in one command:**

```
/team "build a task management app with user authentication and Kanban boards" --project my-app --level junior
```

Claude Code will confirm the project slug, write the project configuration, then run all 7 agents automatically. Final artifacts are written to `projects/my-app/team/`.

**`--level` is required.** Choose the level that matches your implementation team:

```
/team "..." --project my-app --level fresh    # school project
/team "..." --project my-app --level junior   # graduation thesis
/team "..." --project my-app --level mid      # production, medium complexity
/team "..." --project my-app --level senior   # production, high complexity
```

**Per-agent mode — run one phase at a time:**

```
/team-ba "build a task management app" --project my-app --level junior
/team-techlead --project my-app
/team-pm --project my-app
/team-dev --project my-app
/team-fe --project my-app
/team-test --project my-app
/team-qa --project my-app
```

After BA runs (or after `/team` writes the config), subsequent per-agent commands read the level from `projects/{slug}/team/.project-config.md` automatically — no need to repeat `--level`.

---

## Level System

Every project must declare a level. The level is stored in `projects/{slug}/team/.project-config.md` and read by every agent in the pipeline.

| Level | Target project | Architecture style | SP multiplier | Test coverage |
|---|---|---|---|---|
| `fresh` | School assignment | Monolith MVC | ×2.5 | Best-effort |
| `junior` | Graduation thesis | Layered MVC (Controller-Service-Repo) | ×1.5 | ≥ 60% |
| `mid` | Production, medium complexity | Clean / Hexagonal Architecture | ×1.0 | ≥ 70% |
| `senior` | Production, high complexity | DDD + Clean Architecture | ×0.75 | ≥ 80% + mutation |

### What the level controls

**Architecture style (TechLead)** — the recommended architecture matches what the implementation team can execute correctly. A theoretically superior architecture the team cannot implement is the wrong choice.

**Story point multiplier (PM)** — accounts for team experience. `fresh` teams take 2.5× longer than a senior team on the same task. Sprint capacity also adjusts (60% → 110% of nominal).

**Implementation patterns (BE Dev, FE Dev)** — code structure, error handling approach, state management, logging, and auth patterns scale with level.

**Test depth (Tester)** — coverage target, test types (unit only vs. full pyramid), mocking complexity, and Gate 2 threshold all adapt.

**QA compliance standard** — what counts as Critical / Major / Minor adapts. `fresh`: pass if CRUD works and no hardcoded credentials. `senior`: fail if missing Circuit Breaker, no distributed tracing, or coverage < 80%.

### Documentation voice

The *style* of artifacts adapts to the implementation team's level. Same analytical depth, different communication:

| | `fresh` | `junior` | `mid` | `senior` |
|---|---|---|---|---|
| Assumed knowledge | None — all patterns explained | Basic — explain why, assume syntax | Common patterns known | Full expertise — explain only non-obvious |
| Examples in docs | Mandatory — concrete data in every GWT | Strongly recommended | Optional for clarity | Only when non-obvious |
| Task descriptions (PM) | File names, function signatures, "start here" hints | Starting approach + key considerations | Feature title + DoD | Milestone + success metric |

### Pre-Analysis (ultrathinking)

Agents think deeply before writing any file. The depth adapts to level:

| Agent | `fresh` | `junior` | `mid` | `senior` |
|---|---|---|---|---|
| BA | Always — hidden actors, implicit reqs, boundary conditions, abuse risks | ✓ | ✓ | ✓ |
| TechLead | Always — ≥3 arch options, risk surface, downstream impact, threat model | ✓ | ✓ | ✓ |
| PM | Always — dependency graph, critical path, integration choke points, sprint 1 vertical slice | ✓ | ✓ | ✓ |
| BE Dev | — | — | ✓ dependency order, API contract, error taxonomy, security gates | ✓ + domain invariants |
| FE Dev | — | — | ✓ component hierarchy, state shape, error inventory, user behavior edge cases | ✓ + performance budget |
| Tester | — | — | ✓ state machine, equivalence partitioning, abuse cases, race conditions | ✓ + mutation/contract |
| QA/QC | — | — | ✓ per-agent blind spots, OWASP review, traceability audit, pre-commit severity | ✓ |

---

## Command Reference

| Command | Description |
|---|---|
| `/team "requirement" --level {level} [--project slug] [--context "..."] [--spec <path>]` | Run full pipeline — all 7 agents |
| `/team-ba "requirement" --level {level} [--project slug] [--context "..."] [--spec <path>]` | BA phase only |
| `/team-techlead [--project slug] [--context "..."]` | TechLead phase only |
| `/team-pm [--project slug] [--context "..."]` | PM phase only |
| `/team-dev [--project slug] [--context "..."]` | BE Dev phase only |
| `/team-fe [--project slug] [--context "..."]` | FE Dev phase only |
| `/team-test [--project slug] [--context "..."]` | Tester phase only |
| `/team-qa [--project slug] [--context "..."]` | QA/QC phase only |
| `/team-list` | List all projects and their pipeline status |

### Parameters

**`--level {level}`** *(required for `/team` and `/team-ba`)*
Project depth level. Must be one of: `fresh` | `junior` | `mid` | `senior`. Written to `.project-config.md` on first run; subsequent agents read it from disk.

**`--project {slug}`**
Project identifier (kebab-case, e.g. `my-app`, `todo-v1`). If omitted, auto-detected from the current working directory name with confirmation.

**`--context "{text or path}"`**
Supplemental context injected into the agent's prompt. If the value starts with `./` or `/`, read as a file path; otherwise treated as inline text. Never written to artifact files.

**`--spec <path>`**
BA agent reads the markdown file at `{path}` as primary input. Works with any markdown format — SRS specs, brainstorm notes, free-form requirements. Path is relative to the pack root.

---

## Artifact Structure

```
projects/{slug}/
└── team/
    ├── .project-config.md         ← Level config — written first, read by all agents
    ├── ba/
    │   ├── requirements.md
    │   ├── user-stories.md
    │   ├── acceptance-criteria.md
    │   └── business-rules.md
    ├── techlead/
    │   ├── architecture.md        ← Gate 1: Design Freeze declared here
    │   ├── tech-stack.md
    │   ├── ERD.md
    │   ├── sequence-diagrams.md
    │   └── ADR-001.md ... ADR-{n}.md
    ├── pm/
    │   ├── sprint-plan.md
    │   ├── task-breakdown.md
    │   └── story-points.md
    ├── be/
    │   ├── src/...                ← Backend source files
    │   ├── .env.example
    │   └── pr-description.md
    ├── fe/
    │   ├── src/...                ← Frontend source files
    │   └── pr-description.md
    ├── tester/
    │   ├── test-plan.md           ← Gate 2: UAT Readiness declared here
    │   ├── test-cases-unit.md
    │   ├── test-cases-integration.md
    │   ├── test-cases-e2e.md
    │   └── bug-report-template.md
    ├── qa/
    │   ├── quality-report.md
    │   ├── compliance-check.md
    │   └── sign-off.md            ← Gate 3: Release Sign-off (advisory)
    ├── validation-errors/         ← Written only on Layer 1 failures
    │   └── {agent}-attempt-{n}.md
    └── flags-summary.md           ← Written by hook on QA sign-off (if flags exist)
```

---

## Milestone Gates

| Gate | Declared after | Location | Blocks pipeline? |
|---|---|---|---|
| Gate 1: Design Freeze | TechLead | `team/techlead/architecture.md` | No — logged only |
| Gate 2: UAT Readiness | Tester | `team/tester/test-plan.md` | No — logged only |
| Gate 3: Release Sign-off | QA/QC | `team/qa/sign-off.md` | No — advisory only |

Gate 3 verdict is **APPROVED**, **CONDITIONAL**, or **REJECTED**. It is advisory — the operator holds final authority.

---

## Error Handling

### Layer 0 — Level Gate (`level_gate.py`)

Runs before every Write. Blocks any write to `projects/{slug}/team/` if `.project-config.md` is missing or contains an invalid level.

```
[Level Gate] ✗ No project level configured.
Run: /team "requirement" --project {slug} --level mid
 or: /team-ba "requirement" --project {slug} --level mid
```

Always allow: writing `.project-config.md` itself and `validation-errors/` logs.

### Layer 1 — Structural Validation (`pre_write_validator.py`)

Runs after Layer 0. Blocks writes with missing required Markdown headings or hardcoded credentials in source code.

- **Write blocked** → agent told exactly which sections are missing, must fix and retry
- **Up to 3 attempts** automatically
- **3rd failure → HARD STOP** → log written to `projects/{slug}/validation-errors/{agent}-attempt-3.md`

### Layer 2 — Cross-Agent Flags (advisory)

TechLead, Tester, and QA/QC write `## Flags from Previous Agents` in their primary artifacts. When QA/QC writes `sign-off.md`, the `flag_aggregator.py` hook aggregates all flags into `projects/{slug}/flags-summary.md`.

---

## Resuming After Interruption

Artifact files and `.project-config.md` survive session restarts. To resume from a specific phase:

```
/team-list                        ← see which phases are complete
/team-techlead --project my-app   ← resume from TechLead (BA already done)
/team-pm --project my-app         ← resume from PM (BA + TechLead done)
```

The level is read from `.project-config.md` automatically — no need to re-specify `--level`.

---

## Security

- Generated code **never contains hardcoded credentials**, API keys, passwords, tokens, or connection strings
- All sensitive values use environment variable references (e.g., `process.env.DB_PASSWORD`)
- `.env.example` documents every required variable with a placeholder value
- The `pre_write_validator.py` hook **blocks writes** containing hardcoded credential patterns before they reach disk
- The QA/QC agent performs a dedicated security scan in `quality-report.md`

---

## Spec File Integration

Pass any markdown file as requirement input using `--spec`:

```
/team-ba --project my-app --level mid --spec projects/my-app/spec.md
```

This works with SRS specs, brainstorm outputs, PRDs, client emails — any markdown format.

---

## FAQ / Runbook

### Which level should I choose?

| Situation | Level |
|---|---|
| University assignment, personal learning project | `fresh` |
| Final year thesis, internship project | `junior` |
| Startup MVP, internal tool, professional project with a small team | `mid` |
| Enterprise system, regulated domain, large team, performance-critical | `senior` |

When in doubt, choose one level higher than you think — it costs slightly more tokens but produces more maintainable output.

### Can I change the level after starting?

Edit `projects/{slug}/team/.project-config.md` and update the `**level:**` field, then re-run the agents that haven't started yet. Agents that have already written their artifacts are not affected unless you re-run them.

### Pipeline stopped with HARD STOP — what do I do?

1. Read `projects/{slug}/validation-errors/{agent}-attempt-3.md` — lists the exact missing sections
2. Re-run the failed agent:
   ```
   /team-{role} --project {slug}
   ```

### I want to re-run one agent after reviewing its output

```
/team-techlead --project my-app
```

Downstream agents that already ran will have stale context — re-run them too, or run the full pipeline from this point.

### QA/QC returned REJECTED — what do I do?

1. Read `projects/{slug}/team/qa/sign-off.md` for specific critical/major findings
2. Re-run the affected agent(s) to address the findings
3. Re-run QA to get a new verdict:
   ```
   /team-qa --project my-app
   ```

### I want to give a specific agent more context

```
/team-techlead --project my-app --context "use Node.js, React, PostgreSQL"
/team-techlead --project my-app --context ./existing-architecture.md
```

### TechLead or QA/QC is hitting context window limits for large projects

```
/team-qa --project my-app --context ./projects/my-app/summary.md
```

Summarize long artifacts and pass via `--context` to reduce the context chain size.

### How long does the full pipeline take?

Approximate times per agent (varies by complexity and API response time):

| Agent | Estimated time |
|---|---|
| PM | ~15–60 seconds |
| BA, BE Dev, FE Dev, Tester | ~30–180 seconds each |
| TechLead, QA/QC | ~60–180 seconds |
| **Full pipeline** | **~5–20 minutes** (medium complexity) |

For `mid` and `senior` levels, Pre-Analysis adds ~30–60 seconds per implementation agent but significantly reduces re-runs caused by architectural mistakes.

### Can I run multiple projects at the same time?

Each project is isolated under its own `projects/{slug}/` directory. However, a single Claude Code session can only run one pipeline at a time. Open separate Claude Code sessions for parallel projects.
