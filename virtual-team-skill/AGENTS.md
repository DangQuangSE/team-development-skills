# Virtual Team Skill — AGENTS.md

## Overview

This project provides a Claude Code skill set that simulates a full enterprise software development team. Seven AI agents collaborate in a structured pipeline to go from a plain-text requirement to production-ready artifacts.

## Pipeline

```
Operator requirement
        ↓
   /team-ba        ← BA Agent (claude-sonnet-4-6)
        ↓              requirements.md, user-stories.md,
                       acceptance-criteria.md, business-rules.md
   /team-techlead    ← TechLead Agent (claude-opus-4-8)
        ↓              architecture.md, tech-stack.md, ERD.md,
                       sequence-diagrams.md, ADR-{n}.md
                       [Gate 1: Design Freeze]
   /team-pm        ← PM Agent (claude-haiku-4-5)
        ↓              sprint-plan.md, task-breakdown.md, story-points.md
   /team-dev       ← BE Dev Agent (claude-sonnet-4-6)
        ↓              source code + .env.example + pr-description.md
   /team-fe        ← FE Dev Agent (claude-sonnet-4-6)
        ↓              source code + pr-description.md
   /team-test      ← Tester Agent (claude-sonnet-4-6)
        ↓              test-plan.md, test-cases-*.md, bug-report-template.md
                       [Gate 2: UAT Readiness]
   /team-qa        ← QA/QC Agent (claude-opus-4-8)
                       quality-report.md, compliance-check.md, sign-off.md
                       [Gate 3: Release Sign-off — advisory]
```

## Commands

| Command | Description |
|---|---|
| `/team "requirement" [--project slug] [--context "..."] [--spec <path>]` | Full pipeline — all 7 agents |
| `/team-ba "requirement" [--project slug] [--context "..."] [--spec <path>]` | BA phase only |
| `/team-techlead [--project slug] [--context "..."]` | TechLead phase only |
| `/team-pm [--project slug] [--context "..."]` | PM phase only |
| `/team-dev [--project slug] [--context "..."]` | BE Dev phase only |
| `/team-fe [--project slug] [--context "..."]` | FE Dev phase only |
| `/team-test [--project slug] [--context "..."]` | Tester phase only |
| `/team-qa [--project slug] [--context "..."]` | QA/QC phase only |
| `/team-list` | List all projects and their phase status |

## Output Structure

All artifacts are written to `projects/{slug}/team/`:

```
projects/{slug}/
└── team/
    ├── ba/                    ← BA artifacts
    ├── techlead/              ← TechLead artifacts + ADRs
    ├── pm/                    ← Sprint plan + tasks
    ├── be/                    ← Backend source code
    ├── fe/                    ← Frontend source code
    ├── tester/                ← Test plan + test cases
    ├── qa/                    ← Quality report + sign-off
    ├── validation-errors/     ← Layer 1 failure logs (if any)
    └── flags-summary.md       ← Cross-agent flags (if any)
```

## Error Handling

- **Layer 1 (Structural Validation):** After each agent writes artifacts, the agent validates required section headings. Auto-retry up to 3 times. Hard stop on 3rd failure with detailed log.
- **Layer 2 (Cross-agent Flags):** Agents flag logic errors in preceding artifacts via `## Flags from Previous Agents` sections. QA/QC aggregates all flags.

## Resuming After Interruption

Artifacts survive session restarts. To resume from a specific phase:
```
/team-techlead --project {slug}   ← resumes from TechLead phase
```

## Security

- No credentials, API keys, passwords, or tokens are ever hardcoded in generated code
- All sensitive values use environment variable references
- `.env.example` documents all required variables with placeholder values
- QA/QC agent scans all code artifacts for credential violations
