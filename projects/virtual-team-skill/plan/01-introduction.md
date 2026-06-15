# Plan: §1 Introduction — Virtual Team Skill

---

## §1.1 Purpose

**Who will read this SRS:**

| Audience | Role in reading SRS |
|---|---|
| Solo Developers | Understand what the skill does, what artifacts to expect, how to invoke each phase |
| Technical Leads / Architects | Evaluate architectural quality of the system design, assess integration points |
| Product Managers / BAs (Human) | Understand the workflow model, what stories and sprint artifacts are produced |
| Startup Founders / Solo Makers | Determine if the tool fits their workflow; understand what to supply as input |
| Skill Implementers (developers building the skill .md files) | Primary audience — use every FR, NFR, and business rule to write skill content |
| QA Engineers testing the skill | Use FRs + GWT stubs to write test cases for skill behavior |

**Decisions enabled by this SRS:**
- Skill implementers can write each role's `.md` skill file without further clarification
- QA can write and execute test cases for every FR without ambiguity
- Operator users can evaluate whether the skill meets their workflow needs before adopting
- Stakeholder sign-off on scope before any implementation begins

---

## §1.2 Scope

**System name**: Virtual Team Skill (internal project codename: `virtual-team-skill`)

**System description**: Virtual Team Skill is a collection of Claude Code skill files that, when invoked, orchestrate a pipeline of specialized AI agents — each assigned a fixed role in a software development team (Business Analyst, Tech Lead, PM, Backend Developer, Frontend Developer, Tester, QA/QC). The system accepts a free-text requirement (or existing SRS artifacts) as input and produces a complete set of development artifacts — requirements documents, architectural decisions, sprint plans, code files, test plans, and quality reports — stored in a structured local file system. The system operates entirely within the Claude Code CLI environment using native tools (Agent, TodoWrite, Read, Write), requires no external servers, and supports both full-auto pipeline execution and per-role selective invocation.

**IN Scope — v1:**

| Feature | Description |
|---|---|
| BA Phase | Requirement analysis, user stories, acceptance criteria, business rules |
| TechLead Phase | Architecture design, ADR, ERD, sequence diagrams, tech stack selection |
| PM Phase | Sprint planning, task breakdown, story points, TodoWrite tracking |
| BE Dev Phase | Backend code generation (API, schema, migrations, business logic) |
| FE Dev Phase | Frontend code generation (UI components, pages, API integration) |
| Tester Phase | Test plan, unit/integration/e2e test cases, bug report template |
| QA/QC Phase | Quality review, compliance check, advisory sign-off |
| Full-auto mode | Single command runs full pipeline end-to-end |
| Per-agent mode | Individual commands per role for granular control |
| Automated validation (Layer 1) | Structural completeness check + auto-retry (max 3) |
| Cross-agent flagging (Layer 2) | Agent-to-agent logic error detection |
| SRS workflow integration | BA can read existing SRS artifacts as input |
| TodoWrite tracking | PM uses TodoWrite for live progress in conversation |
| Multi-project isolation | Multiple projects per workspace via slug |

**OUT Scope — v1:**

| Feature | Reason | Planned version |
|---|---|---|
| Real git push to remote | Irreversible external action; user controls when to push | v2 (opt-in) |
| Real-time multi-user collaboration | Outside Claude Code skill architecture | v3 |
| DevOps/Infra phase (Docker, CI/CD) | Deferred — needs clearer BE/FE output dependency | v2 |
| Live code execution / runtime testing | Requires sandbox environment not in scope v1 | v2 |
| Web app / PM dashboard UI | Different product category — CLI-only in v1 | v3 |
| Billing / cost tracking per run | Anthropic dashboard handles token usage | Not planned |
| Agent-to-agent real-time communication | File-based async communication sufficient for v1 | v3 |
| Custom agent personality config | Role behavior defined in skill .md files | v2 |

**Adjacent systems that interact but are out of scope:**
- GitHub / GitLab — operator may push generated code there; skill does not interact with these
- Jira / Linear — operator may import sprint plan there; skill does not connect to these
- Anthropic Console — monitors API usage; skill does not read from it

---

## §1.3 Definitions / Acronyms / Abbreviations

| Term | Definition | Source |
|---|---|---|
| Agent | An AI instance spawned by Claude Code's Agent tool, given a specific role prompt and context, that executes a task and produces artifact files | Project-specific |
| Artifact | A Markdown file written to disk by an agent, containing structured output from that agent's role (e.g., user stories, ADR, test cases) | Project-specific |
| BA | Business Analyst — the virtual team role responsible for requirements analysis and user story generation | Industry standard |
| TechLead | Technical Lead — the virtual team role responsible for system architecture, tech stack selection, and design documentation | Industry standard |
| PM | Project Manager / Scrum Master — the virtual team role responsible for sprint planning and workflow coordination | Industry standard |
| BE Dev | Backend Developer — the virtual team role responsible for generating server-side code | Industry standard |
| FE Dev | Frontend Developer — the virtual team role responsible for generating client-side code | Industry standard |
| Tester | The virtual team role responsible for test planning and test case generation | Industry standard |
| QA/QC | Quality Assurance / Quality Control — the virtual team role responsible for overall quality review and sign-off | Industry standard |
| Operator | The human user who invokes the skill; one of: Solo Developer, Technical Lead, PM/BA, Startup Founder | Project-specific |
| Slug | A kebab-case identifier for a project (e.g., `my-ecommerce-app`) used to isolate all project artifacts under `projects/{slug}/` | Project-specific |
| Pipeline | The ordered sequence of agent invocations: BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC | Project-specific |
| Full-auto mode | Skill execution mode where the entire pipeline runs automatically from a single command without operator intervention | Project-specific |
| Per-agent mode | Skill execution mode where operator invokes individual role agents one at a time using role-specific commands | Project-specific |
| Context chain | The mechanism by which each agent reads the file artifacts produced by all preceding agents before generating its own output | Project-specific |
| ADR | Architecture Decision Record — a document capturing a major architectural decision with Context, Decision, and Consequences sections | Industry standard (MADR / RFC style) |
| ERD | Entity Relationship Diagram — a diagram showing data entities and their relationships, rendered in Mermaid syntax | Industry standard |
| Mermaid | A text-based diagram syntax that can be embedded in Markdown and rendered by compatible tools (VS Code, GitHub, Notion) | Mermaid.js |
| Sprint | A fixed-length iteration (default: 2 weeks) in which a subset of user stories are implemented | Agile / Scrum |
| Story Point | A relative unit of effort estimation assigned to a user story by the PM agent | Agile |
| Milestone Gate | A checkpoint in the workflow at which a major phase is declared complete and the next phase may begin (Design Freeze, UAT Readiness, Release Sign-off) | Project-specific (Hybrid Agile+Waterfall) |
| Validation Layer 1 | Automated structural check: does the artifact contain all required section headings? | Project-specific |
| Validation Layer 2 | Cross-agent logic check: does the next agent detect inconsistencies in the previous agent's output? | Project-specific |
| Sign-off | The QA/QC agent's advisory verdict: APPROVED, CONDITIONAL, or REJECTED | Project-specific |
| GWT | Given / When / Then — a format for writing acceptance criteria and test cases | BDD (Behaviour-Driven Development) |
| SRS | Software Requirements Specification — the document produced by the sr:generate skill following IEEE 830 | IEEE 830-1998 |
| SRS Workflow | The existing sr-brainstorm → sr-spec → sr-plan → sr-generate pipeline in this repository | Project-specific |
| TodoWrite | A Claude Code built-in tool that creates and updates task entries visible in the conversation UI | Claude Code |
| Sub-agent | A child agent spawned by a role agent to perform a deeper or parallel sub-task; limited to depth 2 | Project-specific |
| Hard stop | A pipeline termination condition triggered after 3 consecutive validation failures; requires operator intervention | Project-specific |
| `projects/{slug}/team/{role}/` | The standard file path structure for all virtual team artifacts | Project-specific |
| IEEE 830 | IEEE Recommended Practice for Software Requirements Specifications (1998) | IEEE |
| ISO/IEC 25010 | Systems and software Quality Requirements and Evaluation (SQuaRE) standard | ISO |

---

## §1.4 References

| Document | Version | Purpose |
|---|---|---|
| IEEE 830-1998 | 1998 | SRS structure and requirements writing standard |
| ISO/IEC 25010:2011 | 2011 | Software quality characteristics (used for NFR categorization) |
| projects/virtual-team-skill/brainstorm.md | 2026-06-16 | Source brainstorm from /sr:brainstorm session |
| projects/virtual-team-skill/spec.md | v1.0 2026-06-16 | Source specification from /sr:spec session |
| Claude Code documentation | Current | Skill system, Agent tool, TodoWrite tool specifications |
| Anthropic Model documentation | Current | claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5 capabilities and context windows |
| Mermaid documentation (mermaid.js.org) | Current | Diagram syntax reference for TechLead and architecture artifacts |

---

## §1.5 Overview

**How this SRS is organized:**

| Section | Content | Primary Audience |
|---|---|---|
| §1 Introduction | Purpose, scope, definitions, references | All readers |
| §2 Overall Description | System perspective, functions, user profiles, constraints | PM/BA, Operators, Architects |
| §3.1 External Interfaces | User interfaces (CLI), software interfaces (Claude API, file system) | Implementers, QA |
| §3.2 Functional Requirements | All 42 FRs with shall-clauses and GWT stubs | Implementers, QA |
| §3.3 Performance | 12 NFRs with numeric targets or [TBD] | Architects, QA |
| §3.4 Database | Artifact data model, retention, volume projections | Implementers |
| §3.5 Design Constraints | Tech stack, platform, compliance-driven constraints | Implementers |
| §3.6 System Attributes | Reliability, availability, security, maintainability, portability, usability | Architects, DevOps |
| §3.7 Other Requirements | i18n, legal, operational, transition, training | PM, Legal |
| Appendix A | Glossary of all terms | All readers |
| Appendix B | Open issues and TBDs requiring resolution | PM, Implementers |

**Audience routing:**
- **Skill implementers** writing skill .md files: Focus on §3.2 (FRs), §3.5 (constraints), §2.3 (user profiles)
- **QA engineers** writing test cases: Focus on §3.2 (GWT stubs), §3.3 (NFR targets), §1.3 (definitions)
- **Operators** evaluating adoption: Focus on §1.2 (scope), §2.2 (functions), §2.3 (user profile matching)
- **Architects / Tech reviewers**: Focus on §3.1 (interfaces), §3.5 (constraints), §3.6 (system attributes)
