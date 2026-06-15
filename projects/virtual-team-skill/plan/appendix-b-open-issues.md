# Plan: Appendix B — Open Issues — Virtual Team Skill

**Purpose**: Canonical tracking list for all [NEEDS USER INPUT] items and unresolved TBDs from all plan files. Every item here must be resolved before or during SRS generation.

Last updated: 2026-06-16

---

## Open Issues Table

| ID     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Source                                 | Owner               | Priority                        | Resolve-by                          |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------- | ------------------------------- | ----------------------------------- |
| TBD-01 | **Validation Schema definition (BLOCKER)**: The exact list of required section headings for each agent's artifact files (used by Layer 1 Validation) has not been defined. Without this, FR-34 (structural completeness check) and FR-35 (auto-retry) cannot be implemented.                                                                                                                                                                                                                                                                               | OI-01 / FR-34 / FR-35 / 00-overview.md | Skill Implementer   | **P0 — BLOCKER**                | During sr:generate / implementation |
| TBD-02 | **Skill command naming convention**: Final command names not confirmed. Options: `/team-ba`, `/vteam-ba`, `/virtual-ba`. Chosen convention affects all FR-02 GWT stubs, §3.1.1 CLI Entry Points table, and all skill file names.                                                                                                                                                                                                                                                                                                                           | OI-02 / §3.1.1 / FR-02                 | Operator (User)     | **P1**                          | Before skill file authoring         |
| TBD-03 | **Default project slug behavior**: When `--project {slug}` is omitted from a command, what should happen? Options: (A) use current working directory name as slug and confirm with operator, (B) require `--project` always (fail with helpful error), (C) use `default` as fixed slug. FR-10 describes option A but needs user confirmation.                                                                                                                                                                                                              | OI-08 / FR-10                          | Operator (User)     | **P1**                          | Before implementation               |
| TBD-04 | **Conflict resolution in full-auto mode (BA vs SRS artifacts)**: When BA receives both `--srs` flag (SRS artifacts) and runtime operator input that conflict, what happens in full-auto mode? Option A: BA writes conflict to `## Conflicts Detected` and continues with SRS content taking precedence. Option B: BA halts and writes conflict, operator must resolve before continuing. Option C: BA always prefers runtime input over SRS if both provided. FR-41 covers per-agent mode (pause for operator) but full-auto mode behavior is unspecified. | OI-07 / FR-41 / §3.1.4                 | Operator (User)     | **P1**                          | Before implementation               |
| TBD-05 | **Extra context `--context` parameter format**: The `--context "{text}"` parameter is referenced in §3.1.1 and multiple FRs, but the exact format is not confirmed. Options: (A) inline text string only (e.g., `--context "use PostgreSQL"`), (B) file path pointing to a context file, (C) both. Also: is extra context appended to the agent prompt, or prepended? Does it appear in artifacts?                                                                                                                                                         | OI-08 / §3.1.1 / FR-10                 | Operator (User)     | **P1**                          | Before implementation               |
| TBD-06 | **NFR-11 — Agent response time baseline**: No numeric target set because operator chose no timeout. Typical wall-clock time per agent must be measured after first e2e test run to set operator expectations. Hypothesis: haiku=15–60s, sonnet=30–120s, opus=60–180s per agent; full pipeline ~5–20 minutes.                                                                                                                                                                                                                                               | NFR-11 / §3.3                          | Implementation team | **P2**                          | After first full e2e pipeline run   |
| TBD-07 | **Context window warning threshold**: When QA/QC or TechLead reads all preceding artifacts and total artifact size may approach context window limit, at what file size / token estimate should the skill warn the operator? Referenced in §3.1.3 (Software Interface 1) and §3.3 Performance Notes.                                                                                                                                                                                                                                                       | §3.1.3 / §3.3                          | Implementation team | **P2**                          | During implementation               |
| TBD-08 | **Minimum Claude Code CLI version**: The minimum version of Claude Code CLI required to run Virtual Team Skill is not specified. As of 2026-06-16, the latest version should be targeted. Referenced in §3.5.2.                                                                                                                                                                                                                                                                                                                                            | §3.5.2                                 | Skill Implementer   | **P2**                          | Before v1 release documentation     |
| TBD-09 | **`--help` flag in skill commands**: Is it feasible to support `--help` on each skill command in the Claude Code skill format? If yes, what format should inline help take? Referenced in §3.6.6 (Usability) and §3.7.5 (Training).                                                                                                                                                                                                                                                                                                                        | §3.6.6 / §3.7.5                        | Skill Implementer   | **P2**                          | During implementation               |
| TBD-10 | **Onboarding document format**: Is a dedicated onboarding document required (separate file) or is README.md sufficient? Is CLAUDE.md the right place for operator guidance? Referenced in §3.6.6 and §3.7.5.                                                                                                                                                                                                                                                                                                                                               | §3.6.6 / §3.7.5                        | Operator (User)     | **P3**                          | Before v1 release                   |
| TBD-11 | **Runbook format**: Should a runbook (for common operational scenarios: resume failed pipeline, interpret error log, override QA verdict) be a standalone document or part of README? Referenced in §3.7.3.                                                                                                                                                                                                                                                                                                                                                | §3.7.3                                 | Operator (User)     | **P3**                          | Before v1 release                   |
| TBD-12 | **Vietnamese heading validation**: If an operator wants artifact headings in Vietnamese, the English-based validation schema will fail. Is multi-language heading validation required for v1? Referenced in §3.7.1.                                                                                                                                                                                                                                                                                                                                        | §3.7.1                                 | Operator (User)     | **P3 — likely Out of Scope v1** | v2 planning                         |

---

## Priority Legend

| Priority         | Meaning                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------- |
| **P0 — BLOCKER** | SRS generation or implementation cannot proceed without this resolved                        |
| **P1**           | Must be resolved before writing skill `.md` files; directly impacts FR GWT stubs             |
| **P2**           | Must be resolved before v1 release; impacts NFR targets or implementation quality            |
| **P3**           | Should be resolved before v1 release; impacts operator experience but not core functionality |

---

## Resolution Log

| ID     | Resolution                                                                                                                                                                                                                              | Date       | Decided by          |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------- |
| TBD-01 | **RESOLVED** — Validation schemas defined below in §Validation Schemas                                                                                                                                                                  | 2026-06-16 | sr:plan             |
| TBD-02 | **RESOLVED** — Convention: `/team-{role}` (e.g., `/team-ba`, `/team-techlead`, `/team-pm`, `/team-dev`, `/team-fe`, `/team-test`, `/team-qa`). Full pipeline: `/team`.                                                                  | 2026-06-16 | Operator            |
| TBD-03 | **RESOLVED** — Auto-detect slug from current working directory name, confirm with operator before proceeding: "Using project slug: {dir-name}. Continue? (y/n)"                                                                         | 2026-06-16 | Operator            |
| TBD-04 | **RESOLVED** — In full-auto mode with `--srs` + runtime input conflict: BA writes conflict to `## Conflicts Detected` in `requirements.md` and continues, with SRS artifact content taking precedence.                                  | 2026-06-16 | Operator            |
| TBD-05 | **RESOLVED** — `--context` accepts both inline text and file path. Auto-detect: if value starts with `./` or `/` → read as file; otherwise → treat as inline text. Context is prepended to agent prompt; not written to artifact files. | 2026-06-16 | Operator            |
| TBD-06 | _(pending — measure after first e2e pipeline run)_                                                                                                                                                                                      | —          | Implementation team |
| TBD-07 | _(pending — define threshold during implementation)_                                                                                                                                                                                    | —          | Implementation team |
| TBD-08 | _(pending — document min version before release)_                                                                                                                                                                                       | —          | Implementation team |
| TBD-09 | _(pending — verify feasibility in skill format)_                                                                                                                                                                                        | —          | Implementation team |
| TBD-10 | _(pending — operator preference for doc format)_                                                                                                                                                                                        | —          | Operator            |
| TBD-11 | _(pending — operator preference for runbook format)_                                                                                                                                                                                    | —          | Operator            |
| TBD-12 | **OUT OF SCOPE v1** — Vietnamese heading validation deferred to v2                                                                                                                                                                      | 2026-06-16 | Brainstorm session  |

---

## Validation Schemas (TBD-01 Resolution)

Required section headings per artifact file for Layer 1 Validation (FR-34). Validation passes if ALL required headings are present. Headings are checked case-sensitively using exact match.

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

| File                | Required Headings                              |
| ------------------- | ---------------------------------------------- |
| `pr-description.md` | `## Summary`, `## Changes`, `## Testing Notes` |
| `.env.example`      | _(content check only: file must be non-empty)_ |

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
