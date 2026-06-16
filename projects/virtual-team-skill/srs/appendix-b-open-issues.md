# Software Requirements Specification — Appendix B: Open Issues

## Virtual Team Skill

**Purpose:** Canonical tracking list for all unresolved items, TBDs, and design questions that require resolution before this SRS can reach FINAL status. All items listed here must be resolved, deferred, or explicitly out-of-scoped before implementation begins.

**Last updated:** 2026-06-16
**SRS Status:** DRAFT
**Open items blocking FINAL status:** 6 (TBD-06 through TBD-11)
**Resolved/closed items:** 6 (TBD-01 through TBD-05, TBD-12)

---

## Open Issues Table

| ID     | Description                                                                                                                                                                                                        | Source Section                       | Owner               | Priority         | Status              | Resolve-by                        |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ | ------------------- | ---------------- | ------------------- | --------------------------------- |
| TBD-01 | **Validation Schema definition (BLOCKER)**: The exact list of required section headings for each agent's artifact files, used by Layer 1 Validation (FR-34, FR-35), must be defined before implementation.         | FR-34, FR-35, §3.5.10                | Skill Implementer   | **P0 — BLOCKER** | **RESOLVED**        | Resolved during sr:plan           |
| TBD-02 | **Skill command naming convention**: Final command names must be confirmed before authoring skill `.md` files. Affects FR-02 GWT stubs, §3.1.1 CLI Entry Points, and all skill file names.                         | §3.1.1, FR-02                        | Operator            | **P1**           | **RESOLVED**        | Resolved 2026-06-16               |
| TBD-03 | **Default project slug behavior**: When `--project {slug}` is omitted, what behavior is expected? Options were: (A) auto-detect from CWD name and confirm, (B) require always, (C) use fixed `default`.            | FR-10, §3.1.1                        | Operator            | **P1**           | **RESOLVED**        | Resolved 2026-06-16               |
| TBD-04 | **Conflict resolution in full-auto mode (BA vs SRS artifacts)**: When `--srs` flag and runtime operator input conflict, what happens in full-auto mode?                                                            | FR-41, §3.1.3 SI-04                  | Operator            | **P1**           | **RESOLVED**        | Resolved 2026-06-16               |
| TBD-05 | **Extra context `--context` parameter format**: Accepts inline text string, file path, or both? Is context prepended or appended to agent prompt? Is it written to artifact files?                                 | §3.1.1, FR-10                        | Operator            | **P1**           | **RESOLVED**        | Resolved 2026-06-16               |
| TBD-06 | **NFR-11 — Agent response time baseline**: No numeric target set because operator chose no timeout. Must be measured after first end-to-end pipeline test run to set operator expectations.                        | NFR-11, §3.3                         | Implementation team | **P2**           | **OPEN**            | After first full e2e pipeline run |
| TBD-07 | **Context window warning threshold**: At what combined artifact size or token estimate should the skill warn the operator that TechLead or QA/QC agents may approach context window limits?                        | §3.1.3 SI-01, §3.3 Performance Notes | Implementation team | **P2**           | **OPEN**            | During implementation             |
| TBD-08 | **Minimum Claude Code CLI version**: The minimum version of Claude Code CLI required to run Virtual Team Skill is not specified. Latest version should be targeted at time of v1 release.                          | §3.5.2, DC-02                        | Skill Implementer   | **P2**           | **OPEN**            | Before v1 release documentation   |
| TBD-09 | **`--help` flag feasibility**: Is it feasible to support a `--help` flag on each skill command in the Claude Code skill file format? What format should inline help take?                                          | §3.6.6 (Usability), §3.7.5           | Skill Implementer   | **P2**           | **OPEN**            | During implementation             |
| TBD-10 | **Onboarding document format**: Is a dedicated onboarding document required (separate file) or is README.md sufficient? Is CLAUDE.md the right place for operator guidance?                                        | §3.6.6, §3.7.5                       | Operator            | **P3**           | **OPEN**            | Before v1 release                 |
| TBD-11 | **Runbook format**: Should the runbook (common operational scenarios: resume failed pipeline, interpret error log, override QA verdict) be a standalone document or part of README?                                | §3.7.3                               | Operator            | **P3**           | **OPEN**            | Before v1 release                 |
| TBD-12 | **Vietnamese heading validation**: Multi-language heading validation for operators writing requirements in non-English languages. If LLM generates headings in Vietnamese, English-based Layer 1 schema will fail. | §3.7.1                               | Operator            | **P3**           | **OUT OF SCOPE v1** | v2 planning                       |

---

## Priority Legend

| Priority         | Meaning                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| **P0 — BLOCKER** | Implementation cannot proceed without resolution                                                                |
| **P1**           | Must be resolved before authoring skill `.md` files; directly impacts FR GWT stubs and interface specifications |
| **P2**           | Must be resolved before v1 release; impacts NFR targets, implementation quality, or release documentation       |
| **P3**           | Should be resolved before v1 release; impacts operator experience but not core functionality                    |

---

## Resolution Log

| ID     | Resolution                                                                                                                                                                                                                                                                                                   | Decided by         | Date       |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ---------- |
| TBD-01 | **RESOLVED** — Validation schemas defined in §Validation Schemas section below and in §3.5.10 (DC-14). Full schema tables define exact required headings per artifact file, used for Layer 1 Validation (FR-34, FR-35).                                                                                      | sr:plan session    | 2026-06-16 |
| TBD-02 | **RESOLVED** — Convention adopted: `/team-{role}` format (e.g., `/team-ba`, `/team-techlead`, `/team-pm`, `/team-dev`, `/team-fe`, `/team-test`, `/team-qa`). Full pipeline command: `/team`. Utility command: `/team-list`.                                                                                 | Operator           | 2026-06-16 |
| TBD-03 | **RESOLVED** — Auto-detect slug from current working directory name, then confirm with operator before proceeding: _"Using project slug: {dir-name}. Continue? (y/n)"_. Operator can override by providing `--project {slug}`.                                                                               | Operator           | 2026-06-16 |
| TBD-04 | **RESOLVED** — In full-auto mode with `--srs` + conflicting runtime input: BA Agent writes the conflict to `## Conflicts Detected` section of `requirements.md` and continues execution, with SRS artifact content taking precedence. In per-agent mode: BA Agent pauses for operator clarification (FR-41). | Operator           | 2026-06-16 |
| TBD-05 | **RESOLVED** — `--context` accepts both inline text and file path. Auto-detection: if value starts with `./` or `/` → treat as file path and read contents; otherwise → treat as inline text string. Context is prepended to agent prompt and is ephemeral (not written to any artifact file).               | Operator           | 2026-06-16 |
| TBD-06 | _Pending — measure after first full end-to-end pipeline run._ Hypothesis: PM (haiku) ≈ 15–60s; BA/BE/FE/Tester (sonnet) ≈ 30–120s each; TechLead/QA (opus) ≈ 60–180s each; total ≈ 5–20 minutes for medium complexity (8–12 stories). No timeout will be enforced per operator decision.                     | —                  | —          |
| TBD-07 | _Pending — define threshold during implementation._ Suggested starting threshold: warn if combined artifact byte size for a project exceeds 500 KB (configurable). Implementation team to tune.                                                                                                              | —                  | —          |
| TBD-08 | _Pending — document minimum Claude Code CLI version before v1 release._ Target: latest stable release at time of v1 authoring.                                                                                                                                                                               | —                  | —          |
| TBD-09 | _Pending — verify feasibility during implementation._ If `--help` is not supported natively in Claude Code skill format, document command reference in README as the equivalent.                                                                                                                             | —                  | —          |
| TBD-10 | _Pending — operator preference._ Default assumption: README.md covers all operator audiences; a separate onboarding document is optional.                                                                                                                                                                    | —                  | —          |
| TBD-11 | _Pending — operator preference._ Default assumption: runbook is a README section (FAQ / Troubleshooting), not a standalone document.                                                                                                                                                                         | —                  | —          |
| TBD-12 | **OUT OF SCOPE v1** — Multi-language heading validation deferred to v2. In v1, all required section headings must be in English as defined in the validation schemas below. Agents are instructed to write required headings in English even if the artifact body language differs.                          | Brainstorm session | 2026-06-16 |

---

## Validation Schemas (TBD-01 Resolution)

Required section headings per artifact file for Layer 1 Validation (FR-34). Validation passes if ALL required headings are present in the written artifact. Headings are checked case-sensitively using exact string match.

### BA Agent — Validation Schema

| File                     | Required Headings                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| `requirements.md`        | `## Executive Summary`, `## Requirements`, `## Assumptions`, `## Flags from Previous Agents` |
| `user-stories.md`        | `## User Stories`, `## Story ID Index`                                                       |
| `acceptance-criteria.md` | `## Acceptance Criteria`                                                                     |
| `business-rules.md`      | `## Business Rules`                                                                          |

### TechLead Agent — Validation Schema

| File                        | Required Headings                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `architecture.md`           | `## Overview`, `## Component Architecture`, `## Deployment Model`, `## Gate 1: Design Freeze`, `## Flags from Previous Agents` |
| `tech-stack.md`             | `## Frontend`, `## Backend`, `## Database`, `## Infrastructure`, `## Rejected Alternatives`                                    |
| `ERD.md`                    | `## Entity Relationship Diagram`, `## Entity Descriptions`                                                                     |
| `sequence-diagrams.md`      | `## Sequence Diagrams`                                                                                                         |
| `ADR-001.md` (and each ADR) | `## Context`, `## Decision`, `## Consequences`                                                                                 |

### PM Agent — Validation Schema

| File                | Required Headings                                 |
| ------------------- | ------------------------------------------------- |
| `sprint-plan.md`    | `## Sprint Overview`, `## Sprint 1`               |
| `task-breakdown.md` | `## Tasks`                                        |
| `story-points.md`   | `## Velocity Estimate`, `## Story Points Summary` |

### BE Dev Agent — Validation Schema

| File                | Required Headings                                                       |
| ------------------- | ----------------------------------------------------------------------- |
| `pr-description.md` | `## Summary`, `## Changes`, `## Testing Notes`                          |
| `.env.example`      | _(content check: file must be non-empty; no literal credential values)_ |

### FE Dev Agent — Validation Schema

| File                | Required Headings                              |
| ------------------- | ---------------------------------------------- |
| `pr-description.md` | `## Summary`, `## Changes`, `## Testing Notes` |

### Tester Agent — Validation Schema

| File                        | Required Headings                                                                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test-plan.md`              | `## Scope`, `## Approach`, `## Test Environments`, `## Entry Criteria`, `## Exit Criteria`, `## Gate 2: UAT Readiness`, `## Flags from Previous Agents` |
| `test-cases-unit.md`        | `## Unit Test Cases`                                                                                                                                    |
| `test-cases-integration.md` | `## Integration Test Cases`                                                                                                                             |
| `test-cases-e2e.md`         | `## End-to-End Test Cases`                                                                                                                              |
| `bug-report-template.md`    | `## Bug Report Template`                                                                                                                                |

### QA/QC Agent — Validation Schema

| File                  | Required Headings                                                                                                                 |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `quality-report.md`   | `## Completeness Check`, `## Cross-artifact Consistency`, `## Security Review`, `## Process Compliance`, `## Summary of Findings` |
| `compliance-check.md` | `## Milestone Gates`, `## ADR Coverage`, `## Security Scan`, `## Overall Status`                                                  |
| `sign-off.md`         | `## Verdict`, `## Date`, `## Findings`, `## Conditions`                                                                           |
