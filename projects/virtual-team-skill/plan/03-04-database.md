# Plan: §3.4 Database / Data Requirements — Virtual Team Skill

**Note**: Virtual Team Skill does not use a traditional database (no SQL/NoSQL data store). All data persistence is via the local file system. This section describes the logical data model of the artifact file system, data retention policies, volume projections, and data sensitivity classifications.

---

## §3.4.1 Logical Data Model (File System Entities)

### Entity: Project

| Attribute | Type | Description |
|---|---|---|
| slug | String (kebab-case) | Unique identifier for the project (e.g., `todo-v1`, `ecom-mvp`) |
| root_path | Path | `projects/{slug}/` — root directory |
| created_at | ISO 8601 date (from first artifact timestamp) | When the first artifact was written |
| srs_linked | Boolean | Whether an SRS `spec.md` / `brainstorm.md` exists in the root |

**Relationships**: One Project contains one Team Artifact Set + optional SRS artifacts + optional Validation Errors.

---

### Entity: Team Artifact Set

The complete set of directories and files produced by all 7 agents for a project.

```
projects/{slug}/team/
├── ba/                      ← BA Artifact Group
│   ├── requirements.md
│   ├── user-stories.md
│   ├── acceptance-criteria.md
│   └── business-rules.md
├── techlead/                ← TechLead Artifact Group
│   ├── architecture.md
│   ├── tech-stack.md
│   ├── ERD.md
│   ├── sequence-diagrams.md
│   ├── ADR-001.md
│   └── ADR-{n}.md (1..N)
├── pm/                      ← PM Artifact Group
│   ├── sprint-plan.md
│   ├── task-breakdown.md
│   └── story-points.md
├── be/                      ← BE Dev Artifact Group
│   ├── {tech-stack specific source files}
│   ├── .env.example
│   └── pr-description.md
├── fe/                      ← FE Dev Artifact Group
│   ├── {tech-stack specific source files}
│   └── pr-description.md
├── tester/                  ← Tester Artifact Group
│   ├── test-plan.md
│   ├── test-cases-unit.md
│   ├── test-cases-integration.md
│   ├── test-cases-e2e.md
│   └── bug-report-template.md
└── qa/                      ← QA/QC Artifact Group
    ├── quality-report.md
    ├── compliance-check.md
    └── sign-off.md
```

---

### Entity: BA Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `requirements.md` | Yes | Executive summary, requirements list, `## Assumptions` section |
| `user-stories.md` | Yes | User story entries (US-{n}), actor, action, benefit |
| `acceptance-criteria.md` | Yes | Given/When/Then per US-{n} |
| `business-rules.md` | Yes | Numbered business rules (BR-{n}), testable statements |

**Relationships**: Each user story (US-{n}) in `user-stories.md` is referenced in `acceptance-criteria.md`. Business rules may cross-reference user stories.

---

### Entity: TechLead Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `architecture.md` | Yes | System overview, component diagram (Mermaid), Gate 1 status |
| `tech-stack.md` | Yes | Layer-by-layer tech decisions with justifications and rejected alternatives |
| `ERD.md` | Yes | Mermaid ER diagram with all entities, attributes, relationships |
| `sequence-diagrams.md` | Yes | Mermaid sequence diagrams for primary flows (auth, core transaction, error path) |
| `ADR-001.md` ... `ADR-{n}.md` | Yes (min 1) | Architecture Decision Record per major decision: Context / Decision / Consequences |

**Relationships**: `tech-stack.md` informs BE Dev and FE Dev artifact generation. `ERD.md` informs BE Dev schema generation. `ADR-{n}.md` count depends on number of major decisions.

---

### Entity: PM Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `sprint-plan.md` | Yes | Sprint definitions (Sprint 1..N), goals, story list per sprint |
| `task-breakdown.md` | Yes | Task ID, title, description, story reference, assigned agent role, effort (S/M/L/XL) |
| `story-points.md` | Yes | Velocity estimate, total story points, sprint capacity breakdown |

---

### Entity: BE Dev Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `{source files}` | Yes | Tech-stack-appropriate source files (routes, models, migrations, services) |
| `.env.example` | Yes | All required environment variables with placeholder values |
| `pr-description.md` | Yes | PR title, summary, changes list, testing notes |

**Note**: Source file structure under `team/be/` mirrors the target project's directory convention for the chosen tech stack (e.g., `src/routes/`, `src/models/` for Node.js/Express).

---

### Entity: FE Dev Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `{source files}` | Yes | Tech-stack-appropriate source files (components, pages, services, store) |
| `pr-description.md` | Yes | PR title, summary, changes list, testing notes |

---

### Entity: Tester Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `test-plan.md` | Yes | Scope, approach, environments, entry/exit criteria, Gate 2 status |
| `test-cases-unit.md` | Yes | Unit test cases (TC-UNIT-{n}): scenario, inputs, expected outputs |
| `test-cases-integration.md` | Yes | Integration test cases (TC-INT-{n}): API contract tests, data flow tests |
| `test-cases-e2e.md` | Yes | E2E test cases (TC-E2E-{n}): user journey steps from acceptance criteria |
| `bug-report-template.md` | Yes | Template: Bug ID, severity, title, steps to reproduce, expected vs actual, environment |

---

### Entity: QA/QC Artifact Group

| File | Required | Key Contents |
|---|---|---|
| `quality-report.md` | Yes | Per-artifact findings (severity: Critical / Major / Minor), issue descriptions |
| `compliance-check.md` | Yes | Process checklist: milestone gates, ADR coverage, security scan, cross-artifact consistency |
| `sign-off.md` | Yes | Verdict (APPROVED / CONDITIONAL / REJECTED), date stamp, conditions list (if CONDITIONAL), issues list (if REJECTED) |

---

### Entity: Validation Error Log

| File | Required | Key Contents |
|---|---|---|
| `validation-errors/{agent}-attempt-{n}.md` | On validation failure | Timestamp (ISO 8601), agent name, attempt number, sections found, sections missing, raw result |

**Note**: These files are written only on validation failure and are not deleted after eventual success — they serve as a debug audit trail.

---

### Entity: Flags Summary

| File | Required | Key Contents |
|---|---|---|
| `flags-summary.md` | When any agent produces flags | Aggregated FLAG-{ROLE}-{n} entries from all agents: description, affected artifact, severity, suggestion |

---

## §3.4.2 Data Retention

| Entity | Retention Policy | Rationale |
|---|---|---|
| Project artifacts (team/) | Indefinite — operator-controlled | Artifacts are the primary product; not auto-deleted |
| Validation error logs (validation-errors/) | Indefinite — operator-controlled | Debug trail; not auto-deleted even after successful pipeline |
| Flags summary (flags-summary.md) | Indefinite — operator-controlled | Audit record of cross-agent issues |
| TodoWrite entries | Session-only — lost on Claude Code session end | In-memory tracking only; disk artifacts are authoritative |
| SRS workflow artifacts (brainstorm.md, spec.md) | Managed by SRS workflow — not by Virtual Team Skill | Virtual Team Skill reads but does not manage SRS artifacts |

---

## §3.4.3 Data Volume Projections

| Metric | Typical (MVP project) | Large (complex project) |
|---|---|---|
| BA artifacts total size | 10–50 KB | 100–500 KB |
| TechLead artifacts total size | 20–100 KB | 200–1,000 KB |
| PM artifacts total size | 5–20 KB | 50–200 KB |
| BE Dev code artifacts total size | 50–500 KB | 500 KB–5 MB |
| FE Dev code artifacts total size | 50–500 KB | 500 KB–5 MB |
| Tester artifacts total size | 20–100 KB | 200–1,000 KB |
| QA/QC artifacts total size | 10–50 KB | 100–500 KB |
| **Full pipeline total** | **~165 KB – ~1.3 MB** | **~1.7 MB – ~13 MB** |
| Number of projects per workspace | 1–10 typical | Up to hundreds |
| Disk usage per workspace | < 50 MB typical | < 1 GB large deployments |

---

## §3.4.4 PII / Sensitive Data Classification

Virtual Team Skill does not process end-user PII or regulated sensitive data in normal operation. The sensitivity of artifacts depends entirely on the project content the operator provides.

| Data Type | Classification | Handling |
|---|---|---|
| Requirement text (operator input) | Internal (operator-determined) | Stored in BA artifacts; operator responsible for what they input |
| Generated code (BE/FE) | Internal | Must not contain hardcoded credentials (BR-05, FR-24, FR-27) |
| Architecture documents (TechLead) | Internal | May contain system design details; stored locally |
| Sprint plans, story points | Internal | Business process information; stored locally |
| Test cases | Internal | Derived from requirements; stored locally |
| QA reports | Internal | Quality findings; stored locally |
| Validation error logs | Internal | Technical debug info; stored locally |
| Anthropic API key | Secret | Managed by Claude Code CLI; NOT accessible by skill; NOT stored in artifacts |

**No PII fields** are required in Virtual Team Skill artifacts. If an operator's requirement input inadvertently contains PII (e.g., "build an app for John Smith, user ID 12345"), that PII will appear in BA-generated artifacts. This is an operator responsibility, not a skill responsibility.

---

## §3.4.5 Backup and Recovery

| Aspect | Policy |
|---|---|
| Backup responsibility | Operator's own file system backup solution (git, cloud sync, etc.) |
| Recovery point objective (RPO) | Artifacts persist to disk in real-time; RPO = time since last successful Write tool call |
| Recovery time objective (RTO) | Immediate — operator can resume from last completed phase at any time (FR-05) |
| Crash recovery | Partial pipeline runs are recoverable; operator can rerun from last incomplete agent using per-agent mode |
| Skill-managed backups | None — Virtual Team Skill does not implement backup functionality |

---

## §3.4.6 Multi-tenancy / Isolation Model

Virtual Team Skill uses **slug-based directory isolation** — not tenant-based isolation (there is no concept of separate user accounts or database rows).

- Each project (`{slug}`) has a completely independent directory tree
- No shared data files between projects
- No shared in-memory state between project pipeline runs
- Isolation is enforced by: (1) all file paths including the slug, (2) agent instructions scoped to a single slug per invocation
- If two pipeline runs for different projects were to execute concurrently (not supported in v1), file isolation would still hold because paths are slug-scoped
