# Software Requirements Specification — §3.2 Functional Requirements

## Virtual Team Skill

**Total: 42 FRs | Essential: 36 | Conditional: 6 | Optional: 0**

---

## Feature Cluster A — Workflow Engine

### A1: Dual Trigger Mode

---

#### FR-01 [Essential]

**Requirement:** The system shall execute the complete seven-agent pipeline (BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC) automatically in sequence when the operator invokes the `/team "{requirement}"` command, without requiring further operator interaction unless a validation hard stop occurs.

| Field        | Value                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| Actor        | ACTOR-01 (Solo Developer), ACTOR-04 (Startup Founder)                                                              |
| Precondition | Claude Code CLI is operational; Anthropic API is accessible; `--project` slug is known or auto-detectable from CWD |
| Trigger      | Operator executes `/team "{requirement}" [--project {slug}]`                                                       |
| Source       | Brainstorm Feature F-A01; Business Rule BR-06                                                                      |

**Acceptance Criteria (GWT):**

- **Given** the operator runs `/team "build a todo app with user authentication" --project todo-v1`
- **When** the command is processed by the orchestrator skill
- **Then** all seven agents execute in order (BA, TechLead, PM, BE Dev, FE Dev, Tester, QA/QC), each completing and writing artifacts before the next starts, and the pipeline displays completion with artifact locations
- **And** no operator input is required between agents in the normal path (no validation failures)

---

#### FR-02 [Essential]

**Requirement:** The system shall provide individual per-agent skill commands `/team-ba`, `/team-techlead`, `/team-pm`, `/team-dev`, `/team-fe`, `/team-test`, and `/team-qa` that invoke each role agent independently, allowing operators to execute and inspect a single pipeline phase without triggering other agents.

| Field        | Value                                                                                     |
| ------------ | ----------------------------------------------------------------------------------------- |
| Actor        | All operators (ACTOR-01 through ACTOR-04)                                                 |
| Precondition | Claude Code CLI is operational; Anthropic API is accessible                               |
| Trigger      | Operator executes any single per-agent command (e.g., `/team-techlead --project todo-v1`) |
| Source       | Brainstorm Feature F-A01; Operator feedback on dual trigger mode                          |

**Acceptance Criteria (GWT):**

- **Given** the operator runs `/team-techlead --project todo-v1`
- **When** the command executes
- **Then** only the TechLead Agent is spawned; no other agents (BA, PM, BE Dev, FE Dev, Tester, QA/QC) are invoked
- **And** TechLead reads existing BA artifacts from `projects/todo-v1/team/ba/` and writes architecture artifacts to `projects/todo-v1/team/techlead/`

---

#### FR-03 [Essential]

**Requirement:** The system shall verify that all upstream artifact files required by the requested agent exist and are non-empty before spawning that agent in per-agent mode; if any required upstream artifact is missing or empty, the system shall display the specific missing file path(s) and the exact command to generate the missing artifact.

| Field        | Value                                                                                |
| ------------ | ------------------------------------------------------------------------------------ |
| Actor        | All operators                                                                        |
| Precondition | Operator invokes a per-agent command for an agent that depends on upstream artifacts |
| Trigger      | Per-agent command execution when upstream artifacts are absent                       |
| Source       | Business Rule BR-01; Brainstorm Feature F-A02                                        |

**Acceptance Criteria (GWT):**

- **Given** the operator runs `/team-techlead --project todo-v1` but `projects/todo-v1/team/ba/requirements.md` does not exist
- **When** the system checks for upstream artifact existence before spawning TechLead
- **Then** the system displays: `[TechLead] ✗ Missing upstream artifact: projects/todo-v1/team/ba/requirements.md — run: /team-ba --project todo-v1 first` and exits without spawning any agent
- **And** no API call is made until the upstream artifact exists and is non-empty

---

### A2: Context Chain & Persistence

---

#### FR-04 [Essential]

**Requirement:** The system shall confirm that all artifact files produced by each agent have been successfully written to disk — via Write tool return success — before spawning the next agent in the pipeline; no agent shall begin execution while any of its required upstream artifacts are still being written.

| Field        | Value                                                                 |
| ------------ | --------------------------------------------------------------------- |
| Actor        | Orchestrator (skill system)                                           |
| Precondition | An agent has completed generating its artifacts; next agent is queued |
| Trigger      | Agent completion signal from Claude Code Agent tool                   |
| Source       | Business Rule BR-09; NFR-02 (Persistence)                             |

**Acceptance Criteria (GWT):**

- **Given** the BA Agent has finished generating all four BA artifact files
- **When** the orchestrator evaluates whether to spawn TechLead
- **Then** all four BA artifact files (`requirements.md`, `user-stories.md`, `acceptance-criteria.md`, `business-rules.md`) are confirmed written (Write tool returned success) before TechLead Agent is spawned
- **And** if any Write call has not returned success, TechLead is not spawned and an error is displayed

---

#### FR-05 [Essential]

**Requirement:** The system shall allow an operator to resume pipeline execution from any phase after a Claude Code session restart, by reading existing artifact files from disk; the system shall not require the operator to re-enter requirement input if the target agent's upstream artifacts already exist on disk.

| Field        | Value                                                                                                                   |
| ------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Actor        | All operators                                                                                                           |
| Precondition | A pipeline was previously interrupted after at least one agent completed; artifacts from completed phases exist on disk |
| Trigger      | Operator restarts Claude Code and runs a per-agent command for the next incomplete phase                                |
| Source       | NFR-02 (Persistence); Business Rule BR-01                                                                               |

**Acceptance Criteria (GWT):**

- **Given** a full-auto pipeline ran BA phase and was interrupted before TechLead; `projects/todo-v1/team/ba/` artifacts exist on disk
- **When** the operator restarts Claude Code and runs `/team-techlead --project todo-v1`
- **Then** TechLead Agent reads existing BA artifacts from disk and proceeds to generate architecture artifacts without requiring the operator to re-enter the original requirement text
- **And** previously generated BA artifacts are unchanged after the resume

---

#### FR-06 [Essential]

**Requirement:** Each agent shall read and incorporate the artifacts from all preceding agents in the pipeline as explicit context before generating its own output, according to the defined context dependency map: BA reads operator input; TechLead reads BA artifacts; PM reads BA + TechLead; BE Dev reads TechLead + PM; FE Dev reads TechLead + BE Dev; Tester reads BA + BE Dev + FE Dev; QA/QC reads all preceding artifacts.

| Field        | Value                                                |
| ------------ | ---------------------------------------------------- |
| Actor        | All virtual agent actors (ACTOR-05 through ACTOR-11) |
| Precondition | Upstream artifacts exist on disk                     |
| Trigger      | Agent invocation                                     |
| Source       | Business Rule BR-06; Brainstorm Feature F-A02        |

**Acceptance Criteria (GWT):**

- **Given** FE Dev Agent is invoked for `projects/todo-v1` where BE Dev artifacts exist in `team/be/` and TechLead artifacts exist in `team/techlead/`
- **When** FE Dev Agent begins execution
- **Then** FE Dev reads `team/techlead/tech-stack.md` to determine frontend framework and `team/be/` API route files before generating any frontend code
- **And** FE Dev-generated API integration code matches the route paths and response shapes defined in BE Dev artifacts

---

### A3: Hybrid Workflow Enforcement

---

#### FR-07 [Essential]

**Requirement:** The system shall define three milestone gates — Gate 1: Design Freeze (after TechLead phase), Gate 2: UAT Readiness (after Tester phase), Gate 3: Release Sign-off (after QA/QC phase) — and record each gate's status with a timestamp in the relevant phase artifact.

| Field        | Value                                                                              |
| ------------ | ---------------------------------------------------------------------------------- |
| Actor        | Orchestrator, TechLead Agent (Gate 1), Tester Agent (Gate 2), QA/QC Agent (Gate 3) |
| Precondition | The relevant phase has completed and artifacts have passed validation              |
| Trigger      | Completion of TechLead, Tester, or QA/QC phase                                     |
| Source       | Brainstorm Feature F-A03; Business Rule BR-06                                      |

**Acceptance Criteria (GWT):**

- **Given** TechLead Agent has completed and `architecture.md` has been written
- **When** Gate 1 status is recorded
- **Then** `architecture.md` contains a `## Gate 1: Design Freeze` section with status PASSED and an ISO 8601 timestamp
- **And** equivalent gate entries exist in `test-plan.md` (Gate 2) and `sign-off.md` (Gate 3)

---

#### FR-08 [Essential]

**Requirement:** The system shall continue pipeline execution past milestone gates automatically in full-auto mode, recording each gate as PASSED without pausing for operator confirmation; gates shall not block automation unless a validation hard stop has occurred.

| Field        | Value                                                                 |
| ------------ | --------------------------------------------------------------------- |
| Actor        | Orchestrator                                                          |
| Precondition | Full-auto pipeline is running; a milestone gate checkpoint is reached |
| Trigger      | Completion of TechLead, Tester, or QA/QC phase in full-auto mode      |
| Source       | Brainstorm Feature F-A03; Business Rule BR-06                         |

**Acceptance Criteria (GWT):**

- **Given** the full-auto pipeline completes TechLead phase (Gate 1 checkpoint)
- **When** Gate 1 is evaluated in full-auto mode
- **Then** the system logs `[Gate 1] Design Freeze — PASSED` and immediately spawns PM Agent without operator confirmation
- **And** no interactive prompt is displayed at gate checkpoints in full-auto mode

---

### A4: Multi-project Isolation

---

#### FR-09 [Essential]

**Requirement:** The system shall store all artifacts for a project exclusively under `projects/{slug}/team/` with no shared files, shared state, or cross-references between different project slugs; any agent invocation scoped to slug A shall have no read or write access to `projects/{slug-B}/`.

| Field        | Value                                                       |
| ------------ | ----------------------------------------------------------- |
| Actor        | All operators; all virtual agent actors                     |
| Precondition | Two or more project directories exist under `projects/`     |
| Trigger      | Any agent invocation with a specified or auto-detected slug |
| Source       | Business Rule BR-08; NFR-08 (Multi-project Isolation)       |

**Acceptance Criteria (GWT):**

- **Given** two projects exist: `projects/todo-v1/` and `projects/ecom-mvp/`
- **When** BA Agent is invoked for `todo-v1`
- **Then** BA Agent reads only from `projects/todo-v1/` and writes only to `projects/todo-v1/team/ba/`
- **And** no file in `projects/ecom-mvp/` is read, modified, or referenced by the `todo-v1` BA invocation

---

#### FR-10 [Essential]

**Requirement:** The system shall accept a `--project {slug}` parameter for all per-agent commands and the full-auto `/team` command; when `--project` is omitted, the system shall auto-detect the slug from the current working directory name and display a confirmation prompt before proceeding.

| Field        | Value                                                              |
| ------------ | ------------------------------------------------------------------ |
| Actor        | All operators                                                      |
| Precondition | Operator runs a skill command without specifying `--project`       |
| Trigger      | Any skill command invocation without `--project` parameter         |
| Source       | Business Rule BR-08; Plan TBD-03 (resolved: auto-detect + confirm) |

**Acceptance Criteria (GWT):**

- **Given** the operator is in directory `/home/user/my-app` and runs `/team-ba "build login"`
- **When** the command is processed without `--project`
- **Then** the system displays: `Using project slug: my-app. Continue? (y/n)` and waits for operator input
- **And** if the operator confirms `y`, the pipeline proceeds with slug `my-app`; if `n`, the pipeline exits with instructions to use `--project {slug}`

---

## Feature Cluster B — Agent Roles & Artifacts

### B1: BA Phase

---

#### FR-11 [Essential]

**Requirement:** The system shall invoke a BA Agent that generates all four required BA artifact files — `requirements.md`, `user-stories.md`, `acceptance-criteria.md`, and `business-rules.md` — in the `projects/{slug}/team/ba/` directory within a single agent invocation.

| Field        | Value                                                                                                           |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent); ACTOR-04 (Startup Founder, primary operator)                                               |
| Precondition | Operator input (requirement text or `--srs` flag) is provided; `projects/{slug}/team/ba/` directory is writable |
| Trigger      | `/team-ba` invocation or BA phase in full-auto mode                                                             |
| Source       | Brainstorm Feature F-B01; Plan §03-02 FR-11                                                                     |

**Acceptance Criteria (GWT):**

- **Given** the operator provides requirement text "build a task management app with Kanban boards"
- **When** BA Agent completes execution
- **Then** all four files exist in `projects/{slug}/team/ba/`: `requirements.md`, `user-stories.md`, `acceptance-criteria.md`, `business-rules.md`
- **And** each file is non-empty and contains its required section headings (per validation schema in Appendix B)

---

#### FR-12 [Essential]

**Requirement:** The BA Agent shall format each user story using the template "As a {actor}, I want {action} so that {benefit}" and assign a unique, zero-padded Story ID in the format `US-{n}` (e.g., US-001, US-002) to each story in `user-stories.md`.

| Field        | Value                                                 |
| ------------ | ----------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent)                                   |
| Precondition | BA Agent is generating `user-stories.md`              |
| Trigger      | User story generation during BA phase                 |
| Source       | Brainstorm Round 2; Business Rule BR-06; BDD standard |

**Acceptance Criteria (GWT):**

- **Given** the BA Agent has analyzed a requirement involving authenticated users and dashboard views
- **When** `user-stories.md` is generated
- **Then** every story entry follows the format "As a {actor}, I want {action} so that {benefit}"
- **And** each story has a unique ID in format `US-001`, `US-002`, ... (zero-padded, sequential)
- **And** no two stories share the same US-{n} ID within the same project

---

#### FR-13 [Essential]

**Requirement:** The BA Agent shall format acceptance criteria using Given/When/Then (GWT) syntax, with each criterion linked to its parent user story by Story ID, in `acceptance-criteria.md`.

| Field        | Value                                               |
| ------------ | --------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent)                                 |
| Precondition | `user-stories.md` exists with valid US-{n} IDs      |
| Trigger      | Acceptance criteria generation during BA phase      |
| Source       | BDD standard; Brainstorm Round 2; Plan §03-02 FR-13 |

**Acceptance Criteria (GWT):**

- **Given** user story US-003 exists in `user-stories.md`
- **When** BA Agent generates `acceptance-criteria.md`
- **Then** US-003's criteria section appears with the format: `Given {precondition} / When {action} / Then {expected outcome}`
- **And** each criterion is traceable to its US-{n} parent via explicit Story ID reference

---

#### FR-14 [Conditional]

**Requirement:** The BA Agent shall accept `projects/{slug}/spec.md` and `projects/{slug}/brainstorm.md` as primary input when the `--srs` flag is provided, reading those files before generating BA artifacts and deriving user stories from the spec's confirmed features (§3) and business rules (§6).

| Field        | Value                                                                     |
| ------------ | ------------------------------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent); ACTOR-02 (Technical Lead), ACTOR-03 (PM/BA Human)    |
| Precondition | `--srs` flag is passed; `projects/{slug}/spec.md` exists and is non-empty |
| Trigger      | `/team-ba --srs --project {slug}`                                         |
| Source       | Brainstorm Feature F-C03; Plan §03-02 FR-14                               |

**Acceptance Criteria (GWT):**

- **Given** `projects/todo-v1/spec.md` exists with §3 features and §6 business rules, and operator runs `/team-ba --project todo-v1 --srs`
- **When** BA Agent executes
- **Then** BA Agent reads `spec.md` and derives user stories from §3 confirmed features and business rules from §6
- **And** BA Agent does not require separate free-text requirement input when `--srs` flag is provided and `spec.md` exists

---

#### FR-15 [Essential]

**Requirement:** The BA Agent shall document all assumptions made when the requirement input is ambiguous or incomplete in a clearly labeled `## Assumptions` section within `requirements.md`, listing each assumption as a numbered, falsifiable statement.

| Field        | Value                                             |
| ------------ | ------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent)                               |
| Precondition | Operator requirement input is vague or incomplete |
| Trigger      | Ambiguity detected during requirement analysis    |
| Source       | Business Rule BR-12; Spec §8 Assumption ASS-05    |

**Acceptance Criteria (GWT):**

- **Given** the operator provides a vague requirement "build a dashboard"
- **When** BA Agent generates `requirements.md`
- **Then** `requirements.md` contains a `## Assumptions` section with at least one numbered assumption
- **And** each assumption is a falsifiable statement (e.g., "Assumed: the dashboard displays metrics, not a navigation menu")

---

### B2: TechLead Phase

---

#### FR-16 [Essential]

**Requirement:** The system shall invoke a TechLead Agent that generates all five required TechLead artifact files — `architecture.md`, `tech-stack.md`, `ERD.md`, `sequence-diagrams.md`, and at minimum one `ADR-001.md` — in `projects/{slug}/team/techlead/` within a single agent invocation.

| Field        | Value                                                                  |
| ------------ | ---------------------------------------------------------------------- |
| Actor        | ACTOR-06 (TechLead Agent); ACTOR-02 (Technical Lead, primary operator) |
| Precondition | BA artifacts exist in `projects/{slug}/team/ba/`                       |
| Trigger      | `/team-techlead` invocation or TechLead phase in full-auto mode        |
| Source       | Brainstorm Feature F-B02; Plan §03-02 FR-16                            |

**Acceptance Criteria (GWT):**

- **Given** BA artifacts exist in `projects/{slug}/team/ba/`
- **When** TechLead Agent completes execution
- **Then** all five files exist in `projects/{slug}/team/techlead/`: `architecture.md`, `tech-stack.md`, `ERD.md`, `sequence-diagrams.md`, and at least `ADR-001.md`
- **And** each file is non-empty and contains its required section headings (per validation schema)

---

#### FR-17 [Essential]

**Requirement:** The TechLead Agent shall generate all diagrams — system architecture diagram, entity relationship diagram, and sequence diagrams — using valid Mermaid syntax embedded in Markdown code fences (` ```mermaid ` opening, ` ``` ` closing).

| Field        | Value                                             |
| ------------ | ------------------------------------------------- |
| Actor        | ACTOR-06 (TechLead Agent)                         |
| Precondition | TechLead Agent is generating diagram files        |
| Trigger      | Architecture, ERD, or sequence diagram generation |
| Source       | Tech constraint from Spec §5.5; Plan §03-02 FR-17 |

**Acceptance Criteria (GWT):**

- **Given** TechLead Agent is generating `ERD.md`
- **When** the entity relationship diagram is written
- **Then** the diagram appears inside a ` ```mermaid ` code fence and uses valid Mermaid `erDiagram` syntax with at least one entity definition and one relationship
- **And** the Mermaid block renders correctly in VS Code with Mermaid Preview or on GitHub

---

#### FR-18 [Essential]

**Requirement:** The TechLead Agent shall write one Architecture Decision Record (ADR) file per major architectural decision encountered during design, using the format `ADR-{n}.md` (e.g., `ADR-001.md`, `ADR-002.md`) with mandatory sections: `## Context`, `## Decision`, and `## Consequences`.

| Field        | Value                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| Actor        | ACTOR-06 (TechLead Agent)                                                                                          |
| Precondition | TechLead Agent has made a major architectural decision (e.g., database choice, framework selection, auth strategy) |
| Trigger      | Each major architectural decision during TechLead phase                                                            |
| Source       | ADR convention; Plan §03-02 FR-18                                                                                  |

**Acceptance Criteria (GWT):**

- **Given** TechLead decides to use PostgreSQL over MongoDB for the data layer
- **When** TechLead writes the ADR
- **Then** `ADR-001.md` exists in `team/techlead/` with `## Context` (why a decision was needed), `## Decision` (PostgreSQL chosen), `## Consequences` (trade-offs: ACID compliance, schema rigidity, etc.)
- **And** if TechLead makes a second major decision (e.g., auth strategy), `ADR-002.md` is written as a separate file

---

### B3: PM Phase

---

#### FR-19 [Essential]

**Requirement:** The system shall invoke a PM Agent that generates all three required PM artifact files — `sprint-plan.md`, `task-breakdown.md`, and `story-points.md` — in `projects/{slug}/team/pm/` within a single agent invocation.

| Field        | Value                                                         |
| ------------ | ------------------------------------------------------------- |
| Actor        | ACTOR-07 (PM Agent); ACTOR-03 (PM/BA Human, primary operator) |
| Precondition | BA artifacts and TechLead artifacts both exist on disk        |
| Trigger      | `/team-pm` invocation or PM phase in full-auto mode           |
| Source       | Brainstorm Feature F-B03; Plan §03-02 FR-19                   |

**Acceptance Criteria (GWT):**

- **Given** BA and TechLead artifacts exist in `projects/{slug}/team/`
- **When** PM Agent completes execution
- **Then** three files exist in `projects/{slug}/team/pm/`: `sprint-plan.md`, `task-breakdown.md`, `story-points.md`
- **And** each file is non-empty and contains its required section headings

---

#### FR-20 [Conditional]

**Requirement:** The PM Agent shall use the Claude Code TodoWrite tool to create one task entry per sprint task, with `status: "pending"` and a descriptive `activeForm`; the orchestrator shall update each task's status to `"in_progress"` when the corresponding agent is spawned and `"completed"` when that agent's artifacts pass Layer 1 validation.

| Field        | Value                                                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------------------------- |
| Actor        | ACTOR-07 (PM Agent); Orchestrator                                                                                |
| Precondition | TodoWrite tool is available in the Claude Code session; sprint tasks have been identified in `task-breakdown.md` |
| Trigger      | PM Agent completion; subsequent agent spawning and completion                                                    |
| Source       | Brainstorm Feature F-C04; Plan §03-02 FR-20                                                                      |

**Acceptance Criteria (GWT):**

- **Given** PM Agent generates 8 sprint tasks across Sprint 1 and Sprint 2
- **When** PM Agent writes `task-breakdown.md`
- **Then** 8 TodoWrite entries are created with `status: "pending"` and descriptive `content` and `activeForm` fields
- **And** when BE Dev Agent is spawned, its corresponding task entry is updated to `status: "in_progress"`
- **And** when BE Dev validation passes, that task entry is updated to `status: "completed"`

---

#### FR-21 [Essential]

**Requirement:** The PM Agent shall organize user stories from `user-stories.md` into two-week sprint iterations, assign relative effort story points (S=1, M=3, L=5, XL=8) to each task, and include a sprint goal statement for each sprint in `sprint-plan.md`.

| Field        | Value                                                   |
| ------------ | ------------------------------------------------------- |
| Actor        | ACTOR-07 (PM Agent)                                     |
| Precondition | `user-stories.md` exists with at least one US-{n} story |
| Trigger      | Sprint planning during PM phase                         |
| Source       | Agile/Scrum methodology; Plan §03-02 FR-21              |

**Acceptance Criteria (GWT):**

- **Given** `user-stories.md` contains 8 user stories
- **When** PM Agent generates `sprint-plan.md`
- **Then** stories are grouped into one or more sprints, each labeled "Sprint {n}" with a goal statement
- **And** each task in `task-breakdown.md` has a story point value from: S=1, M=3, L=5, or XL=8
- **And** `story-points.md` shows total story points per sprint and cumulative velocity estimate

---

### B4: BE Dev Phase

---

#### FR-22 [Essential]

**Requirement:** The system shall invoke a BE Dev Agent that generates backend source code files (API routes/controllers, database schema or ORM model files, migration files, business logic service files) and a `pr-description.md` file in `projects/{slug}/team/be/`.

| Field        | Value                                                                           |
| ------------ | ------------------------------------------------------------------------------- |
| Actor        | ACTOR-08 (BE Dev Agent); ACTOR-01 (Solo Developer, primary operator)            |
| Precondition | TechLead artifacts (including `tech-stack.md`) and PM sprint plan exist on disk |
| Trigger      | `/team-dev` invocation or BE Dev phase in full-auto mode                        |
| Source       | Brainstorm Feature F-B04; Plan §03-02 FR-22                                     |

**Acceptance Criteria (GWT):**

- **Given** TechLead has specified `Node.js + Express + PostgreSQL` in `tech-stack.md` and PM has created a sprint plan
- **When** BE Dev Agent completes execution
- **Then** `projects/{slug}/team/be/` contains: at least one API route file, at least one schema/model file, and `pr-description.md`
- **And** the code structure mirrors common conventions for the selected tech stack (e.g., `src/routes/`, `src/models/` for Node.js/Express)

---

#### FR-23 [Essential]

**Requirement:** The BE Dev Agent shall read `tech-stack.md` before generating any code and shall generate all code using the language, framework, database driver, and patterns specified in that file.

| Field        | Value                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------ |
| Actor        | ACTOR-08 (BE Dev Agent)                                                                    |
| Precondition | `tech-stack.md` exists in `team/techlead/` with explicit backend technology specifications |
| Trigger      | Code generation start during BE Dev phase                                                  |
| Source       | Business Rule BR-06; Tech constraint §2.4                                                  |

**Acceptance Criteria (GWT):**

- **Given** `tech-stack.md` specifies "Backend: Node.js with Express framework, ORM: Prisma, Database: PostgreSQL"
- **When** BE Dev Agent generates API routes
- **Then** all generated code uses Express router syntax, Prisma client for database queries, and TypeScript (if TS is specified)
- **And** no code is generated using a different framework (e.g., no FastAPI, no Django) unless specified in `tech-stack.md`

---

#### FR-24 [Essential]

**Requirement:** The BE Dev Agent shall not hardcode any credentials, API keys, passwords, tokens, or database connection strings in any generated file; all such values shall be replaced with environment variable references appropriate to the tech stack (e.g., `process.env.DB_PASSWORD`), and all required environment variables shall be listed in a generated `.env.example` file with placeholder values.

| Field        | Value                                                                             |
| ------------ | --------------------------------------------------------------------------------- |
| Actor        | ACTOR-08 (BE Dev Agent)                                                           |
| Precondition | BE Dev Agent is generating code that requires credentials or configuration values |
| Trigger      | Any code generation requiring a secret value, connection string, or API key       |
| Source       | Business Rule BR-05; NFR-06 (Security — Integrity); §3.5 Security Constraints     |

**Acceptance Criteria (GWT):**

- **Given** BE Dev Agent generates a database connection module
- **When** the database connection string is needed in the code
- **Then** the generated code contains `process.env.DATABASE_URL` (or framework-equivalent) instead of any literal connection string
- **And** `.env.example` in `team/be/` contains the line `DATABASE_URL=your_postgresql_connection_string_here`
- **And** no literal password, token, or key string appears anywhere in `team/be/` files

---

### B5: FE Dev Phase

---

#### FR-25 [Essential]

**Requirement:** The system shall invoke a FE Dev Agent that generates frontend source code files (UI component files, page/view files, API integration service files, state management files where applicable) and a `pr-description.md` in `projects/{slug}/team/fe/`.

| Field        | Value                                                                 |
| ------------ | --------------------------------------------------------------------- |
| Actor        | ACTOR-09 (FE Dev Agent); ACTOR-01 (Solo Developer, primary operator)  |
| Precondition | TechLead artifacts and BE Dev artifacts (API contracts) exist on disk |
| Trigger      | `/team-fe` invocation or FE Dev phase in full-auto mode               |
| Source       | Brainstorm Feature F-B05; Plan §03-02 FR-25                           |

**Acceptance Criteria (GWT):**

- **Given** TechLead specified `React + TypeScript + Axios` in `tech-stack.md` and BE Dev has written API routes
- **When** FE Dev Agent completes execution
- **Then** `projects/{slug}/team/fe/` contains: at least one component file, at least one page file, an API service file, and `pr-description.md`
- **And** the code structure mirrors common conventions for the selected frontend framework

---

#### FR-26 [Essential]

**Requirement:** The FE Dev Agent shall read BE Dev API artifacts before generating any API integration code, ensuring that frontend API call signatures (HTTP method, URL path, request body shape, response shape) match the backend route definitions generated by BE Dev Agent.

| Field        | Value                                                                |
| ------------ | -------------------------------------------------------------------- |
| Actor        | ACTOR-09 (FE Dev Agent)                                              |
| Precondition | BE Dev artifacts exist in `team/be/` including API route definitions |
| Trigger      | API integration code generation during FE Dev phase                  |
| Source       | Context chain requirement FR-06; Business Rule BR-06                 |

**Acceptance Criteria (GWT):**

- **Given** BE Dev generated `routes/auth.js` defining `POST /api/auth/login` returning `{ token: string, user: { id, email } }`
- **When** FE Dev Agent generates the API integration service
- **Then** the frontend API service calls `POST /api/auth/login` with the correct request body shape
- **And** the frontend handles the `{ token, user }` response structure as defined in BE Dev artifacts

---

#### FR-27 [Essential]

**Requirement:** The FE Dev Agent shall not hardcode environment-specific configuration values (API base URLs, feature flags, environment-specific constants) in generated source code; all such values shall use a configuration or environment variable pattern appropriate to the selected frontend framework.

| Field        | Value                                                                           |
| ------------ | ------------------------------------------------------------------------------- |
| Actor        | ACTOR-09 (FE Dev Agent)                                                         |
| Precondition | FE Dev Agent generates code requiring environment-specific configuration        |
| Trigger      | Any code generation that requires a configuration or environment-specific value |
| Source       | Business Rule BR-05; NFR-06; §3.5 Security Constraints                          |

**Acceptance Criteria (GWT):**

- **Given** FE Dev Agent generates an API service for a React application
- **When** the API base URL is referenced
- **Then** the generated code uses `process.env.REACT_APP_API_URL` (Create React App) or `import.meta.env.VITE_API_URL` (Vite) or the equivalent for the specified frontend framework
- **And** no literal URL string (e.g., `http://localhost:3000`) appears hardcoded in any generated source file

---

### B6: Tester Phase

---

#### FR-28 [Essential]

**Requirement:** The system shall invoke a Tester Agent that generates all five required Tester artifact files — `test-plan.md`, `test-cases-unit.md`, `test-cases-integration.md`, `test-cases-e2e.md`, and `bug-report-template.md` — in `projects/{slug}/team/tester/`.

| Field        | Value                                                              |
| ------------ | ------------------------------------------------------------------ |
| Actor        | ACTOR-10 (Tester Agent); all operators                             |
| Precondition | BA artifacts, BE Dev artifacts, and FE Dev artifacts exist on disk |
| Trigger      | `/team-test` invocation or Tester phase in full-auto mode          |
| Source       | Brainstorm Feature F-B06; Plan §03-02 FR-28                        |

**Acceptance Criteria (GWT):**

- **Given** BA, BE Dev, and FE Dev artifacts exist in `projects/{slug}/team/`
- **When** Tester Agent completes execution
- **Then** all five files exist in `projects/{slug}/team/tester/`
- **And** each file is non-empty and contains its required section headings

---

#### FR-29 [Essential]

**Requirement:** The Tester Agent shall derive test cases from BA acceptance criteria by mapping each Given/When/Then acceptance criterion to at least one test case with a unique Test Case ID (`TC-UNIT-{n}`, `TC-INT-{n}`, or `TC-E2E-{n}`), scenario name, preconditions, numbered test steps, input data, and expected output.

| Field        | Value                                                           |
| ------------ | --------------------------------------------------------------- |
| Actor        | ACTOR-10 (Tester Agent)                                         |
| Precondition | `acceptance-criteria.md` exists with at least one GWT criterion |
| Trigger      | Test case generation during Tester phase                        |
| Source       | IEEE 829 (informative); Business Rule BR-06                     |

**Acceptance Criteria (GWT):**

- **Given** BA wrote acceptance criterion for US-003: "Given user is unauthenticated / When accessing /dashboard / Then redirect to /login"
- **When** Tester generates e2e test cases
- **Then** `test-cases-e2e.md` contains test case `TC-E2E-003` with: precondition (user not logged in), steps (navigate to /dashboard), expected outcome (browser redirects to /login)
- **And** every GWT acceptance criterion in `acceptance-criteria.md` maps to at least one test case across the three test case files

---

#### FR-30 [Essential]

**Requirement:** The Tester Agent shall detect and flag any logic inconsistencies between BA requirements/acceptance criteria and the BE/FE implementation artifacts, writing each detected issue as a cross-agent flag entry in a `## Flags from Previous Agents` section within `test-plan.md`.

| Field        | Value                                                                     |
| ------------ | ------------------------------------------------------------------------- |
| Actor        | ACTOR-10 (Tester Agent)                                                   |
| Precondition | BA, BE Dev, and FE Dev artifacts exist and have been read by Tester Agent |
| Trigger      | Logic inconsistency detection during artifact review in Tester phase      |
| Source       | Business Rule BR-03; Brainstorm Feature F-C02                             |

**Acceptance Criteria (GWT):**

- **Given** BA `acceptance-criteria.md` states "password must be minimum 8 characters" but BE Dev code has no password length validation
- **When** Tester Agent reads both BA and BE Dev artifacts
- **Then** `test-plan.md` contains a `## Flags from Previous Agents` section with entry `FLAG-TESTER-001`: description of missing password validation in BE Dev code, affected artifact: `team/be/routes/auth.js`, severity: Major, suggestion: add length validation middleware
- **And** if no inconsistencies are found, the section contains the text "No flags detected"

---

### B7: QA/QC Phase

---

#### FR-31 [Essential]

**Requirement:** The system shall invoke a QA/QC Agent that generates all three required QA artifact files — `quality-report.md`, `compliance-check.md`, and `sign-off.md` — in `projects/{slug}/team/qa/` after reading all artifacts from all preceding agents.

| Field        | Value                                                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------------------------- |
| Actor        | ACTOR-11 (QA/QC Agent); all operators                                                                            |
| Precondition | All preceding agents (BA, TechLead, PM, BE Dev, FE Dev, Tester) have completed and their artifacts exist on disk |
| Trigger      | `/team-qa` invocation or QA/QC phase in full-auto mode                                                           |
| Source       | Brainstorm Feature F-B07; Plan §03-02 FR-31                                                                      |

**Acceptance Criteria (GWT):**

- **Given** all seven preceding artifact groups exist in `projects/{slug}/team/`
- **When** QA/QC Agent completes execution
- **Then** three files exist in `projects/{slug}/team/qa/`: `quality-report.md`, `compliance-check.md`, `sign-off.md`
- **And** each file is non-empty and contains its required section headings

---

#### FR-32 [Essential]

**Requirement:** The QA/QC Agent shall perform four mandatory review checks: (1) completeness check — all required sections present in each artifact across all agents; (2) cross-artifact consistency — requirements, architecture, code, and tests are mutually consistent; (3) security artifact review — no hardcoded credentials in any code artifact; (4) process compliance — all three milestone gates recorded as PASSED, all major ADRs present for architectural decisions.

| Field        | Value                                                           |
| ------------ | --------------------------------------------------------------- |
| Actor        | ACTOR-11 (QA/QC Agent)                                          |
| Precondition | All preceding artifacts exist and have been read by QA/QC Agent |
| Trigger      | Quality review execution during QA/QC phase                     |
| Source       | Business Rule BR-03; Brainstorm Feature F-B07; NFR-06           |

**Acceptance Criteria (GWT):**

- **Given** BE Dev code artifact `team/be/config/db.js` contains the literal string `"postgres://admin:password123@localhost/mydb"`
- **When** QA/QC Agent performs the security artifact review check
- **Then** `quality-report.md` records a Critical finding under `## Security Review`: "Hardcoded credential detected in: team/be/config/db.js — line contains literal database connection string with password"
- **And** `sign-off.md` verdict is REJECTED due to the Critical finding

---

#### FR-33 [Essential]

**Requirement:** The QA/QC Agent's `sign-off.md` shall contain a verdict of exactly one of: APPROVED (zero Critical or Major issues found), CONDITIONAL (one or more Minor issues present; all conditions listed), or REJECTED (one or more Critical or Major issues present; must be re-examined before release), along with an ISO 8601 date stamp and a complete list of findings.

| Field        | Value                                                             |
| ------------ | ----------------------------------------------------------------- |
| Actor        | ACTOR-11 (QA/QC Agent)                                            |
| Precondition | `quality-report.md` and `compliance-check.md` have been completed |
| Trigger      | Sign-off generation at conclusion of QA/QC phase                  |
| Source       | Business Rule BR-04; Brainstorm Feature F-B07                     |

**Acceptance Criteria (GWT):**

- **Given** QA/QC review found 2 Minor issues (UI label inconsistency, missing error message in test case) and 0 Critical or Major issues
- **When** `sign-off.md` is written
- **Then** verdict is `CONDITIONAL` with both Minor issues listed as conditions to resolve before release
- **And** a date stamp in ISO 8601 format (e.g., `2026-06-16T14:30:00Z`) appears in the `## Date` section
- **And** if review found 0 issues, verdict is `APPROVED`; if Critical or Major found, verdict is `REJECTED`

---

## Feature Cluster C — Error Handling & Validation

### C1: Automated Validation Layer (Layer 1)

---

#### FR-34 [Essential]

**Requirement:** The system shall validate each agent's artifact set for structural completeness immediately after all artifacts are written to disk, by checking that every required section heading defined in the agent's validation schema is present in the corresponding artifact file.

| Field        | Value                                                                                           |
| ------------ | ----------------------------------------------------------------------------------------------- |
| Actor        | Orchestrator (skill system)                                                                     |
| Precondition | An agent has completed writing its artifact files; validation schemas are defined in Appendix B |
| Trigger      | Post-write completion signal from each agent invocation                                         |
| Source       | Business Rule BR-02; NFR-01 (Structural Completeness)                                           |

**Acceptance Criteria (GWT):**

- **Given** BA Agent has written `user-stories.md` but it is missing the required `## Story ID Index` heading
- **When** Layer 1 validation runs on BA artifacts
- **Then** validation result is FAIL with details: `[BA] ✗ Validation failed — missing: [## Story ID Index] in user-stories.md`
- **And** the next agent is not spawned until validation passes

---

#### FR-35 [Essential]

**Requirement:** The system shall automatically rerun a failed agent with an augmented prompt that explicitly names the missing section headings when structural validation fails; the system shall retry automatically up to a maximum of 3 times; if validation fails on the 3rd attempt, the system shall issue a hard stop, display a recovery message, and not retry further.

| Field        | Value                                                         |
| ------------ | ------------------------------------------------------------- |
| Actor        | Orchestrator                                                  |
| Precondition | Layer 1 validation has returned FAIL for an agent's artifacts |
| Trigger      | Validation failure after agent execution                      |
| Source       | Business Rule BR-02; NFR-04 (Retry Resilience)                |

**Acceptance Criteria (GWT):**

- **Given** BA Agent fails validation on attempt 1 (missing `## Business Rules` in `business-rules.md`)
- **When** retry is triggered
- **Then** BA Agent is rerun with an augmented prompt: "RETRY REQUIRED (attempt 2/3) — the following required sections were missing: [## Business Rules in business-rules.md] — ensure all required sections are present before completing"
- **And** if attempt 3 also fails, system displays: `[BA] ✗ Validation failed on attempt 3/3 — HARD STOP` with `Error log: projects/{slug}/validation-errors/ba-attempt-3.md` and `Action: run /team-ba --project {slug} to retry manually`
- **And** no 4th automatic retry is attempted

---

#### FR-36 [Essential]

**Requirement:** The system shall write a validation failure log file to `projects/{slug}/validation-errors/{agent}-attempt-{n}.md` for every failed validation attempt, containing: timestamp (ISO 8601), agent name, attempt number (n of 3), list of section headings found, list of required headings missing, and the raw validation result.

| Field        | Value                                               |
| ------------ | --------------------------------------------------- |
| Actor        | Orchestrator                                        |
| Precondition | A validation failure has occurred for an agent      |
| Trigger      | Every validation failure event (attempt 1, 2, or 3) |
| Source       | Business Rule BR-11; Plan §03-01 §C1                |

**Acceptance Criteria (GWT):**

- **Given** BA Agent fails validation on attempt 2
- **When** the failure log is written
- **Then** file `projects/{slug}/validation-errors/ba-attempt-2.md` is created with: current timestamp in ISO 8601 format, agent name "BA", attempt number "2 of 3", list of headings found in the artifact, list of headings missing, validation FAIL result
- **And** this file is never deleted, even after eventual validation success on attempt 3

---

### C2: Cross-agent Verification Layer (Layer 2)

---

#### FR-37 [Essential]

**Requirement:** Every agent (TechLead, Tester, QA/QC — and optionally BA, PM, BE Dev, FE Dev) shall include a `## Flags from Previous Agents` section in its primary artifact file; if no issues are detected after reviewing preceding artifacts, this section shall contain the text "No flags detected."

| Field        | Value                                                                           |
| ------------ | ------------------------------------------------------------------------------- |
| Actor        | ACTOR-06 (TechLead), ACTOR-10 (Tester), ACTOR-11 (QA/QC) — primary flag authors |
| Precondition | Agent has read and analyzed all preceding agents' artifacts                     |
| Trigger      | Every agent invocation                                                          |
| Source       | Business Rule BR-03; Brainstorm Feature F-C02                                   |

**Acceptance Criteria (GWT):**

- **Given** TechLead Agent reads BA artifacts and finds no inconsistencies
- **When** TechLead writes `architecture.md`
- **Then** `architecture.md` contains the section `## Flags from Previous Agents` with content "No flags detected"
- **And** if TechLead does find an issue, the section contains at least one properly formatted FLAG-{ROLE}-{n} entry

---

#### FR-38 [Essential]

**Requirement:** Each cross-agent flag entry shall contain all five mandatory fields: Flag ID (format `FLAG-{ROLE}-{n}`, zero-padded, e.g., `FLAG-TECHLEAD-001`), description of the detected issue, name of the affected artifact file (relative path), severity level (Blocker / Major / Minor), and a suggested resolution.

| Field        | Value                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------ |
| Actor        | ACTOR-06 (TechLead), ACTOR-10 (Tester), ACTOR-11 (QA/QC)                                         |
| Precondition | A logic error, inconsistency, or missing information is detected in a preceding agent's artifact |
| Trigger      | Issue detection during cross-agent artifact review                                               |
| Source       | Business Rule BR-03; Brainstorm Feature F-C02                                                    |

**Acceptance Criteria (GWT):**

- **Given** TechLead detects that user story US-005 in `user-stories.md` contains a logical contradiction (user can be simultaneously admin and guest)
- **When** TechLead writes the flag
- **Then** the flag entry in `architecture.md` contains exactly: `FLAG-TECHLEAD-001`, description of the contradiction, `affected: team/ba/user-stories.md`, `severity: Major`, and `suggestion: Clarify role hierarchy — a user should have a single primary role`
- **And** the flag ID is unique within the document and follows the zero-padded format

---

#### FR-39 [Essential]

**Requirement:** In full-auto mode, when any agent produces one or more cross-agent flags, the system shall append those flag entries to a `projects/{slug}/flags-summary.md` file and display a summary notification to the operator at the end of the pipeline indicating the total number of flags and the file path.

| Field        | Value                                                                            |
| ------------ | -------------------------------------------------------------------------------- |
| Actor        | Orchestrator                                                                     |
| Precondition | Full-auto pipeline is running; at least one agent has produced cross-agent flags |
| Trigger      | Full-auto pipeline completion when flags exist                                   |
| Source       | Brainstorm Feature F-C02; Plan §03-02 FR-39                                      |

**Acceptance Criteria (GWT):**

- **Given** TechLead produced 1 flag and Tester produced 2 flags during a full-auto pipeline run
- **When** the pipeline completes
- **Then** `projects/{slug}/flags-summary.md` contains all 3 flag entries from both agents
- **And** the CLI displays: `⚠️  3 cross-agent flags detected across 2 agents — see projects/{slug}/flags-summary.md`
- **And** if no flags were produced, `flags-summary.md` is not created and no flags notification is displayed

---

### C3: SRS Workflow Integration

---

#### FR-40 [Conditional]

**Requirement:** The system shall accept the `--srs` flag in the `/team-ba` command, causing the BA Agent to read `projects/{slug}/spec.md` as its primary input, deriving user stories from §3 (Features) and business rules from §6 (Business Rules) of that document; if `brainstorm.md` also exists, it shall be used as supplemental context.

| Field        | Value                                                                       |
| ------------ | --------------------------------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent); ACTOR-02 (Technical Lead), ACTOR-03 (PM/BA Human)      |
| Precondition | `--srs` flag is provided; `projects/{slug}/spec.md` exists and is non-empty |
| Trigger      | `/team-ba --srs --project {slug}`                                           |
| Source       | Brainstorm Feature F-C03; Plan §03-02 FR-40                                 |

**Acceptance Criteria (GWT):**

- **Given** `projects/my-app/spec.md` exists with §3 confirmed features and `projects/my-app/brainstorm.md` exists
- **When** operator runs `/team-ba --project my-app --srs`
- **Then** BA Agent reads `spec.md` §3 for features and §6 for business rules and derives structured user stories from them
- **And** `brainstorm.md` is also read and used as supplemental context
- **And** no free-text requirement input is required from the operator

---

#### FR-41 [Conditional]

**Requirement:** The BA Agent shall detect and flag conflicts between SRS artifact content and any operator-provided runtime requirement input by writing a `## Conflicts Detected` section in `requirements.md`; in full-auto mode, the SRS artifact content shall take precedence and the pipeline shall continue; in per-agent mode, the BA Agent shall pause and request operator clarification.

| Field        | Value                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------- |
| Actor        | ACTOR-05 (BA Agent)                                                                                         |
| Precondition | `--srs` flag is used AND operator also provides free-text requirement input that conflicts with SRS content |
| Trigger      | Conflict detection during BA analysis when both `--srs` and runtime input are provided                      |
| Source       | Business Rule BR-12; Plan TBD-04 (resolved: SRS takes precedence)                                           |

**Acceptance Criteria (GWT):**

- **Given** `spec.md` §4 lists feature X as OUT of scope, but operator runtime input requests feature X
- **When** BA Agent processes both inputs in full-auto mode
- **Then** `requirements.md` contains `## Conflicts Detected` listing: "Feature X is out of scope per spec.md §4, but operator input requests it. SRS content takes precedence; Feature X is excluded from user stories."
- **And** the pipeline continues without pausing
- **And** in per-agent mode (same scenario), BA Agent writes the conflict and displays a message requesting operator input before writing user stories

---

### C4: TodoWrite Progress Tracking

---

#### FR-42 [Conditional]

**Requirement:** The PM Agent shall create one Claude Code TodoWrite entry per sprint task identified in `task-breakdown.md`, with `status: "pending"`, descriptive `content` (imperative form), and descriptive `activeForm` (present continuous form); the orchestrator shall update each entry's status to `"in_progress"` when the corresponding agent begins execution and `"completed"` when that agent's artifacts pass Layer 1 validation.

| Field        | Value                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| Actor        | ACTOR-07 (PM Agent); Orchestrator                                                                    |
| Precondition | PM Agent has identified sprint tasks; TodoWrite tool is available in the current Claude Code session |
| Trigger      | PM Agent completion; subsequent agent lifecycle events                                               |
| Source       | Brainstorm Feature F-C04; Plan §03-02 FR-42                                                          |

**Acceptance Criteria (GWT):**

- **Given** PM Agent identifies 5 tasks: [implement-auth-api, implement-user-api, implement-login-ui, implement-dashboard-ui, write-e2e-tests]
- **When** PM Agent writes `task-breakdown.md` and calls TodoWrite
- **Then** 5 TodoWrite entries are created with `status: "pending"`, e.g., `{ content: "Implement auth API", status: "pending", activeForm: "Implementing auth API" }`
- **And** when BE Dev Agent starts, the `implement-auth-api` and `implement-user-api` entries are updated to `"in_progress"`
- **And** when BE Dev validation passes, those entries are updated to `"completed"`

---

## FR Count Summary

| Priority    | Count  | FR IDs                                                               |
| ----------- | ------ | -------------------------------------------------------------------- |
| Essential   | 36     | FR-01 through FR-13, FR-15 through FR-19, FR-21 through FR-39        |
| Conditional | 6      | FR-14, FR-20, FR-40, FR-41, FR-42 — and FR-10 (partial TBD behavior) |
| Optional    | 0      | —                                                                    |
| **Total**   | **42** | FR-01 → FR-42                                                        |
