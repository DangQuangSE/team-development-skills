# Software Requirements Specification — §3.4 Logical Database Requirements
## Virtual Team Skill

**Note:** Virtual Team Skill does not use a relational or NoSQL database. All data persistence is via the local file system. This section defines the logical data model as a file system entity model, covering entity definitions, key attributes, relationships, retention policies, volume projections, and PII classification.

---

## 3.4.1 Entity Model

### Entity: Project

| Attribute | Type | Description |
|---|---|---|
| `slug` | String (kebab-case) | Unique project identifier; serves as the root directory name (e.g., `todo-v1`) |
| `root_path` | File path | `projects/{slug}/` — root of all project artifacts |
| `first_artifact_date` | ISO 8601 timestamp | Inferred from earliest artifact file creation time |
| `srs_linked` | Boolean (inferred) | True if `projects/{slug}/spec.md` or `brainstorm.md` exists |
| `pipeline_phase` | Enum (inferred) | Last completed phase, derived by checking which artifact groups exist on disk |

**Relationships:**
- One Project → contains one Team Artifact Set
- One Project → may contain zero or one SRS Artifact Set (brainstorm.md, spec.md)
- One Project → may contain zero or more Validation Error Logs
- One Project → may contain zero or one Flags Summary

---

### Entity: Team Artifact Set

The complete collection of artifact groups produced by all seven agents.

**Root path:** `projects/{slug}/team/`

| Sub-entity | Directory | Status |
|---|---|---|
| BA Artifact Group | `team/ba/` | Required before TechLead can run |
| TechLead Artifact Group | `team/techlead/` | Required before PM can run |
| PM Artifact Group | `team/pm/` | Required before BE Dev can run |
| BE Dev Artifact Group | `team/be/` | Required before FE Dev can run |
| FE Dev Artifact Group | `team/fe/` | Required before Tester can run |
| Tester Artifact Group | `team/tester/` | Required before QA/QC can run |
| QA/QC Artifact Group | `team/qa/` | Terminal — no downstream dependencies |

---

### Entity: BA Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| `requirements.md` | Yes | Executive summary, requirements list, assumptions, conflicts (if any) | `## Executive Summary`, `## Requirements`, `## Assumptions`, `## Flags from Previous Agents` |
| `user-stories.md` | Yes | US-{n} stories in "As a / I want / So that" format | `## User Stories`, `## Story ID Index` |
| `acceptance-criteria.md` | Yes | Given/When/Then criteria per US-{n} | `## Acceptance Criteria` |
| `business-rules.md` | Yes | Numbered testable business rules (BR-{n}) | `## Business Rules` |

**Relationships:** Each US-{n} in `user-stories.md` has one or more GWT entries in `acceptance-criteria.md`. Business rules in `business-rules.md` may reference US-{n} IDs.

---

### Entity: TechLead Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| `architecture.md` | Yes | System overview, component diagram (Mermaid), deployment model, Gate 1 status | `## Overview`, `## Component Architecture`, `## Deployment Model`, `## Gate 1: Design Freeze`, `## Flags from Previous Agents` |
| `tech-stack.md` | Yes | Per-layer technology selection with justification and rejected alternatives | `## Frontend`, `## Backend`, `## Database`, `## Infrastructure`, `## Rejected Alternatives` |
| `ERD.md` | Yes | Entity Relationship Diagram in Mermaid `erDiagram` syntax | `## Entity Relationship Diagram`, `## Entity Descriptions` |
| `sequence-diagrams.md` | Yes | Key flow sequence diagrams in Mermaid syntax | `## Sequence Diagrams` |
| `ADR-001.md` ... `ADR-{n}.md` | Yes (min 1) | Context / Decision / Consequences per major decision | `## Context`, `## Decision`, `## Consequences` |

**Relationships:** `tech-stack.md` is read by BE Dev Agent and FE Dev Agent. `ERD.md` informs BE Dev schema generation. The number of ADR files equals the number of major architectural decisions made.

---

### Entity: PM Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| `sprint-plan.md` | Yes | Sprint definitions (Sprint 1..N), sprint goals, user story allocation | `## Sprint Overview`, `## Sprint 1` |
| `task-breakdown.md` | Yes | Task ID, title, description, US-{n} reference, assigned agent role, effort size (S/M/L/XL) | `## Tasks` |
| `story-points.md` | Yes | Story point per task, sprint total, velocity estimate | `## Velocity Estimate`, `## Story Points Summary` |

**Relationships:** Tasks in `task-breakdown.md` reference US-{n} IDs from `user-stories.md`. Task effort estimates feed into `story-points.md`.

---

### Entity: BE Dev Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| Source code files | Yes | API route/controller files, ORM model/schema files, migration files, business logic services | *(content check: non-empty source files)* |
| `.env.example` | Yes | All required environment variables with placeholder values | *(content check: non-empty; no literal secrets)* |
| `pr-description.md` | Yes | PR title, summary, list of changes, testing notes | `## Summary`, `## Changes`, `## Testing Notes` |

**Note:** Source file structure under `team/be/` mirrors the tech stack convention (e.g., `src/routes/`, `src/models/` for Node.js/Express).

---

### Entity: FE Dev Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| Source code files | Yes | UI component files, page files, API service files, state management files | *(content check: non-empty source files)* |
| `pr-description.md` | Yes | PR title, summary, list of changes, testing notes | `## Summary`, `## Changes`, `## Testing Notes` |

---

### Entity: Tester Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| `test-plan.md` | Yes | Test scope, approach, environments, entry/exit criteria, Gate 2 UAT status, flags | `## Scope`, `## Approach`, `## Test Environments`, `## Entry Criteria`, `## Exit Criteria`, `## Gate 2: UAT Readiness`, `## Flags from Previous Agents` |
| `test-cases-unit.md` | Yes | TC-UNIT-{n} test cases with steps, inputs, expected outputs | `## Unit Test Cases` |
| `test-cases-integration.md` | Yes | TC-INT-{n} integration test cases covering API contracts and data flows | `## Integration Test Cases` |
| `test-cases-e2e.md` | Yes | TC-E2E-{n} end-to-end user journey test cases derived from acceptance criteria | `## End-to-End Test Cases` |
| `bug-report-template.md` | Yes | Template for bug reports: ID, severity, title, steps, expected vs actual, environment | `## Bug Report Template` |

**Relationships:** TC-{n} IDs reference US-{n} and acceptance criteria GWT conditions from BA artifacts.

---

### Entity: QA/QC Artifact Group

| File | Required | Key Content | Min. Required Headings |
|---|---|---|---|
| `quality-report.md` | Yes | Per-artifact findings organized by severity (Critical / Major / Minor) | `## Completeness Check`, `## Cross-artifact Consistency`, `## Security Review`, `## Process Compliance`, `## Summary of Findings` |
| `compliance-check.md` | Yes | Checklist of process gates: milestone gates passed, ADR coverage, security scan, consistency | `## Milestone Gates`, `## ADR Coverage`, `## Security Scan`, `## Overall Status` |
| `sign-off.md` | Yes | Verdict (APPROVED / CONDITIONAL / REJECTED), date stamp, conditions, issue list | `## Verdict`, `## Date`, `## Findings`, `## Conditions` |

---

### Entity: Validation Error Log

| File | Created when | Key Content |
|---|---|---|
| `validation-errors/{agent}-attempt-{n}.md` | Every failed Layer 1 validation | ISO 8601 timestamp, agent name, attempt number (1–3), sections found, sections missing, result |

**Retention:** Permanent (not deleted after eventual success). Serves as audit trail.

---

### Entity: Flags Summary

| File | Created when | Key Content |
|---|---|---|
| `flags-summary.md` | Full-auto mode when any agent produces flags | Aggregated FLAG-{ROLE}-{n} entries with description, affected artifact, severity, suggestion |

---

## 3.4.2 Data Retention

| Entity | Retention Policy | Rationale |
|---|---|---|
| Team artifacts (`team/`) | Indefinite — operator-controlled; never auto-deleted by skill | Primary output of the system |
| Validation error logs (`validation-errors/`) | Indefinite — operator-controlled; not deleted on success | Debug audit trail |
| Flags summary (`flags-summary.md`) | Indefinite — operator-controlled | Cross-agent quality record |
| SRS workflow artifacts (`spec.md`, `brainstorm.md`) | Managed by SRS workflow; Virtual Team Skill reads but does not manage | Out of scope for Virtual Team Skill retention |
| TodoWrite entries | Session-only — lost when Claude Code session ends | In-memory tracking only; disk artifacts are authoritative |

---

## 3.4.3 Data Volume Projections

| Metric | Typical (MVP, ~8 stories) | Large (complex, ~30+ stories) |
|---|---|---|
| BA artifacts total | 10–50 KB | 100–500 KB |
| TechLead artifacts total | 20–100 KB | 200–1,000 KB |
| PM artifacts total | 5–20 KB | 50–200 KB |
| BE Dev code artifacts total | 50–500 KB | 500 KB–5 MB |
| FE Dev code artifacts total | 50–500 KB | 500 KB–5 MB |
| Tester artifacts total | 20–100 KB | 200–1,000 KB |
| QA/QC artifacts total | 10–50 KB | 100–500 KB |
| **Full pipeline total** | **~165 KB – ~1.3 MB** | **~1.7 MB – ~13 MB** |
| Validation error logs (if any) | Negligible (< 5 KB per file) | Negligible |
| Projects per workspace | 1–10 typical | Up to hundreds |
| Total workspace disk usage | < 50 MB typical | < 1 GB large |

---

## 3.4.4 PII / Sensitive Data Classification

Virtual Team Skill does not require PII fields in any artifact. Artifact content sensitivity depends solely on what the operator inputs as requirement text.

| Data Type | Classification | Handling |
|---|---|---|
| Requirement text (operator input) | Internal — operator-determined | Stored in BA artifacts; operator responsible for data classification |
| Generated code (BE/FE) | Internal | Must not contain credentials (FR-24, FR-27, NFR-06) |
| Architecture documents (TechLead) | Internal | System design details; stored locally |
| Sprint plans, story points (PM) | Internal | Business process artifacts; stored locally |
| Test cases (Tester) | Internal | Quality artifacts; stored locally |
| QA reports (QA/QC) | Internal | Quality findings; stored locally |
| Validation error logs | Internal / Technical | Debug data; stored locally |
| Anthropic API key | **Secret** | Managed by Claude Code CLI; NOT accessible to or stored in any skill artifact |

**PII risk**: If operator requirement input inadvertently contains personal data (e.g., real user names, email examples), that data will appear in BA artifacts. This is an operator responsibility; the skill does not sanitize operator input.

---

## 3.4.5 Backup and Recovery

| Aspect | Policy |
|---|---|
| Backup | Operator's responsibility (git commit, cloud sync, etc.); skill does not implement backup |
| Recovery Point Objective (RPO) | Artifacts persist in real-time; RPO = time since last successful Write tool call for each artifact |
| Recovery Time Objective (RTO) | Immediate — operator can resume from last completed phase at any time via per-agent command (FR-05) |
| Crash recovery | Artifacts from completed phases survive; operator reruns from the last incomplete agent |

---

## 3.4.6 Isolation Model

Project isolation is implemented via **slug-scoped directory isolation**:

- Each project occupies a completely independent directory tree under `projects/{slug}/`
- No shared files between projects
- No shared in-memory state between pipeline runs for different projects
- Agent invocation scope is explicitly tied to one slug per invocation (FR-09)
- Isolation holds even if two pipeline runs were theoretically concurrent, because all file paths are slug-prefixed
