# Software Requirements Specification — §1 Introduction

## Virtual Team Skill

_IEEE 830-1998 Compliant_

| Field       | Value                |
| ----------- | -------------------- |
| Project     | Virtual Team Skill   |
| Version     | v1.0 — Draft         |
| Date        | 2026-06-16           |
| Prepared by | sr:generate workflow |
| Status      | Draft                |

> **Notation:** "shall" = mandatory obligation. "should" = desirable but optional.
> Quality attributes follow ISO/IEC 25010. NFR metrics follow ISO/IEC 25023 Quality Attribute Scenarios.

---

## 1.1 Purpose

This Software Requirements Specification defines the complete functional and non-functional requirements for **Virtual Team Skill** — a set of Claude Code skills that orchestrates specialized AI agents to simulate a full software development team lifecycle. This document is the authoritative reference for skill implementers writing the `.md` skill files, QA engineers designing test plans, and operators evaluating the system's suitability for their workflows.

**Audience and intended use:**

| Audience                          | How they use this SRS                                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Skill Implementers                | Use §3.2 (FRs with GWT stubs) and §3.5 (constraints) as the unambiguous blueprint for each skill `.md` file |
| QA Engineers                      | Use §3.2 GWT stubs and §3.3 NFR measures to write and execute test cases                                    |
| Solo Developers (ACTOR-01)        | Evaluate whether skill behavior matches their workflow before adopting                                      |
| Technical Leads (ACTOR-02)        | Assess architectural quality and integration points                                                         |
| Product Managers / BAs (ACTOR-03) | Understand artifact structure and what to supply as input                                                   |
| Startup Founders (ACTOR-04)       | Determine if the single-command full-pipeline meets their MVP delivery needs                                |
| Repository Maintainers            | Govern scope changes and version progression                                                                |

**Decisions this SRS enables:**

- Skill implementers can write all skill `.md` files without further clarification from the specification
- QA can write and execute test cases for all 42 FRs
- Stakeholders can approve scope before any implementation effort begins

---

## 1.2 Scope

**System name:** Virtual Team Skill (`virtual-team-skill`)

**System description:** Virtual Team Skill is a collection of Claude Code skill files that, when invoked, orchestrate a pipeline of seven specialized AI agents — each assigned a fixed role in a software development team: Business Analyst, Technical Lead, Project Manager, Backend Developer, Frontend Developer, Tester, and QA/QC. The system accepts a free-text requirement (or existing SRS workflow artifacts) as input and produces a complete, structured set of development artifacts — requirements documents, architectural decisions, sprint plans, code files, test plans, and quality reports — all stored in a predictable local file system structure. The system operates entirely within the Claude Code CLI environment using native tools, requires no external servers, and supports both full-automatic pipeline execution and per-role selective invocation.

**In / Out of Scope:**

| Feature Area                                                                      | In Scope (v1) | Out of Scope (v1) |
| --------------------------------------------------------------------------------- | ------------- | ----------------- |
| BA Phase: requirement analysis, user stories, acceptance criteria, business rules | ✓             |                   |
| TechLead Phase: architecture, ADR, ERD, sequence diagrams, tech stack             | ✓             |                   |
| PM Phase: sprint planning, task breakdown, story points, TodoWrite tracking       | ✓             |                   |
| BE Dev Phase: backend code generation (API, schema, migrations, logic)            | ✓             |                   |
| FE Dev Phase: frontend code generation (UI, pages, API integration)               | ✓             |                   |
| Tester Phase: test plan, unit/integration/e2e test cases, bug report template     | ✓             |                   |
| QA/QC Phase: quality review, compliance check, advisory sign-off                  | ✓             |                   |
| Full-auto pipeline mode (`/team`)                                                 | ✓             |                   |
| Per-agent mode (`/team-ba`, `/team-techlead`, etc.)                               | ✓             |                   |
| Automated validation Layer 1 (structural check + auto-retry ≤ 3)                  | ✓             |                   |
| Cross-agent verification Layer 2 (logic flag propagation)                         | ✓             |                   |
| SRS workflow integration (BA reads existing `spec.md`)                            | ✓             |                   |
| TodoWrite progress tracking in conversation                                       | ✓             |                   |
| Multi-project isolation by slug                                                   | ✓             |                   |
| Real git push to remote (GitHub/GitLab)                                           |               | ✓ deferred v2     |
| Real-time multi-user collaboration                                                |               | ✓ deferred v3     |
| DevOps/Infra phase (Dockerfile, CI/CD, GitHub Actions)                            |               | ✓ deferred v2     |
| Live code execution / runtime testing                                             |               | ✓ deferred v2     |
| Web app / PM dashboard UI                                                         |               | ✓ deferred v3     |
| Custom agent personality configuration                                            |               | ✓ deferred v2     |

---

## 1.3 Definitions, Acronyms, and Abbreviations

See Appendix A for full glossary. Standard abbreviations used throughout this document:

| Abbreviation | Definition                                                      |
| ------------ | --------------------------------------------------------------- |
| SRS          | Software Requirements Specification                             |
| FR           | Functional Requirement                                          |
| NFR          | Non-Functional Requirement                                      |
| GWT          | Given / When / Then (acceptance criteria format)                |
| TBD          | To Be Determined                                                |
| BA           | Business Analyst (virtual team role / agent)                    |
| TechLead     | Technical Lead / System Designer (virtual team role / agent)    |
| PM           | Project Manager / Scrum Master (virtual team role / agent)      |
| BE Dev       | Backend Developer (virtual team role / agent)                   |
| FE Dev       | Frontend Developer (virtual team role / agent)                  |
| QA/QC        | Quality Assurance / Quality Control (virtual team role / agent) |
| ADR          | Architecture Decision Record                                    |
| ERD          | Entity Relationship Diagram                                     |
| CLI          | Command-Line Interface                                          |
| LLM          | Large Language Model                                            |
| ISO 25010    | ISO/IEC 25010:2011 Software Quality Characteristics standard    |

---

## 1.4 References

| #   | Document                                            | Type                                                          | Date       |
| --- | --------------------------------------------------- | ------------------------------------------------------------- | ---------- |
| 1   | `projects/virtual-team-skill/brainstorm.md`         | Source input (brainstorm session)                             | 2026-06-16 |
| 2   | `projects/virtual-team-skill/spec.md`               | Source specification                                          | 2026-06-16 |
| 3   | `projects/virtual-team-skill/plan/` (12 plan files) | Planning blueprint                                            | 2026-06-16 |
| 4   | IEEE 830-1998                                       | Standard — SRS structure                                      | 1998       |
| 5   | ISO/IEC 25010:2011                                  | Standard — Software quality characteristics                   | 2011       |
| 6   | ISO/IEC 25023:2016                                  | Standard — Quality measures (NFR scenario format)             | 2016       |
| 7   | Claude Code Documentation (Anthropic)               | External reference — Skill system, Agent tool, TodoWrite      | Current    |
| 8   | Anthropic Model Documentation                       | External reference — Model IDs, context windows, capabilities | Current    |
| 9   | Mermaid.js Documentation (mermaid.js.org)           | External reference — Diagram syntax for TechLead artifacts    | Current    |
| 10  | IEEE 829 — Software Test Documentation              | Standard — Test plan structure (informative reference)        | 2008       |

---

## 1.5 Overview

**Document organization:**

| Section                            | Content                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| §1 Introduction (this file)        | Purpose, scope, definitions, references                                                      |
| §2 Overall Description             | System context, functions, user profiles, constraints, assumptions                           |
| §3.1 External Interfaces           | CLI commands, software interfaces (Anthropic API, file system, TodoWrite, SRS workflow)      |
| §3.2 Functional Requirements       | All 42 FRs (FR-01 → FR-42) with shall-clauses, actor tables, and GWT acceptance criteria     |
| §3.3 Performance Requirements      | 12 NFRs (NFR-01 → NFR-12) with ISO 25023 quality attribute scenarios                         |
| §3.4 Logical Database Requirements | File system data model, artifact entities, retention, volume projections, PII classification |
| §3.5 Design Constraints            | Mandatory tech stack, model assignment, platform, security, and coding constraints           |
| §3.6 System Attributes             | Reliability, availability, security, maintainability, portability, usability                 |
| §3.7 Other Requirements            | Localization, legal, operational, transition, training                                       |
| Appendix A                         | Full glossary (47 terms)                                                                     |
| Appendix B                         | Open issues tracker (12 items, 5 resolved, 7 pending)                                        |

**Audience routing:**

- **Skill implementers** → §3.2 (FRs), §3.5 (constraints), §2.3 (user profiles), Appendix B (TBD resolutions)
- **QA engineers** → §3.2 (GWT stubs), §3.3 (NFR measures), §1.3 (definitions)
- **Operators evaluating adoption** → §1.2 (scope), §2.2 (functions), §2.3 (user profiles matching)
- **Architects / reviewers** → §3.1 (interfaces), §3.5 (constraints), §3.6 (system attributes)
