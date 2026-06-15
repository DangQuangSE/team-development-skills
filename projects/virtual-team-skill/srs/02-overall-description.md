# Software Requirements Specification — §2 Overall Description

## Virtual Team Skill

---

## 2.1 Product Perspective

Virtual Team Skill is a **new standalone tool** — not a replacement for an existing system, not a wrapper around a third-party service. It is a collection of Claude Code skill files that extend Claude Code's capabilities to simulate a multi-role software development team.

**System context — how the tool fits into the operator's environment:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  OPERATOR'S LOCAL MACHINE                                               │
│                                                                         │
│  ┌────────────┐  /team "requirement"  ┌──────────────────────────────┐ │
│  │  Operator  │ ──────────────────── ► │  Claude Code CLI             │ │
│  │            │ ◄────────────────────  │  (terminal / VS Code ext.)   │ │
│  │            │   progress + results   │                              │ │
│  └────────────┘                        │  ┌──────────────────────┐   │ │
│                                        │  │ Virtual Team Skill   │   │ │
│  ┌────────────┐                        │  │ Orchestrator (.md)   │   │ │
│  │ File System│ ◄───────── writes ─── │  │                      │   │ │
│  │ projects/  │ ──────── reads ──────► │  │ BA Agent (Sonnet)    │   │ │
│  │ {slug}/    │                        │  │ TechLead (Opus)      │   │ │
│  │ team/      │                        │  │ PM Agent (Haiku)     │   │ │
│  └────────────┘                        │  │ BE Dev (Sonnet)      │   │ │
│                                        │  │ FE Dev (Sonnet)      │   │ │
│  ┌────────────┐                        │  │ Tester (Sonnet)      │   │ │
│  │ SRS        │ ─── optional read ─── ► │  │ QA/QC (Opus)         │   │ │
│  │ Workflow   │                        │  └──────────────────────┘   │ │
│  │ artifacts  │                        └──────────────┬───────────────┘ │
│  │ (spec.md)  │                                       │                 │
│  └────────────┘                                       │ LLM calls       │
│                                                       ▼                 │
│                                        ┌──────────────────────────┐    │
│                                        │ Anthropic Claude API     │    │
│                                        │ (HTTPS, managed by CLI)  │    │
│                                        └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

**External systems and interfaces:**

- **Anthropic Claude API** — provides LLM inference for all agents; managed by Claude Code CLI; not directly invoked by skill
- **Claude Code TodoWrite tool** — PM Agent writes task tracking entries visible in the conversation
- **Local file system** — all artifact persistence; `projects/{slug}/team/{role}/`
- **SRS Workflow artifacts** (`brainstorm.md`, `spec.md`) — optional structured input for the BA Agent; read-only

**How Virtual Team Skill fits into the operator's existing ecosystem:**

- Operators who already use the SRS Workflow (`/sr:brainstorm` → `/sr:spec`) can feed those outputs directly into Virtual Team Skill via the `--srs` flag on `/team-ba`
- Generated code artifacts (BE/FE files) can be copied into the operator's own project repository; Virtual Team Skill does not push to any remote
- No cloud infrastructure is needed beyond what Claude Code already requires

---

## 2.2 Product Functions

High-level summary of major capabilities (detailed requirements in §3.2):

**Cluster A — Workflow Engine:**

- Execute all 7 agents automatically in sequence with a single command (`/team`)
- Execute any single agent independently on-demand (`/team-ba`, `/team-techlead`, etc.)
- Chain agent context via file system: each agent reads all previous agents' artifacts
- Persist all artifacts to disk before spawning the next agent; context survives session restart
- Enforce a Hybrid Agile + Waterfall workflow with three milestone gates (Design Freeze, UAT Readiness, Release Sign-off)
- Isolate each project under `projects/{slug}/team/` with zero cross-project state

**Cluster B — Agent Roles:**

- BA Agent: analyze requirements, produce user stories (US-{n}), acceptance criteria (Given/When/Then), business rules
- TechLead Agent: design system architecture, select tech stack, write ADRs, ERD, and sequence diagrams in Mermaid
- PM Agent: organize stories into 2-week sprints, estimate story points (S/M/L/XL), track tasks via TodoWrite
- BE Dev Agent: generate server-side code aligned to tech stack and sprint tasks; produce `pr-description.md`
- FE Dev Agent: generate client-side code aligned to BE API contracts; produce `pr-description.md`
- Tester Agent: produce test plan, unit/integration/e2e test cases from acceptance criteria, bug report template
- QA/QC Agent: review all artifacts, check compliance, issue advisory sign-off (APPROVED / CONDITIONAL / REJECTED)

**Cluster C — Error Handling & Validation:**

- Automated Validation (Layer 1): structural completeness check per artifact; auto-retry up to 3 times; hard stop with error log
- Cross-agent Verification (Layer 2): each agent flags logic errors from preceding agents; flags aggregated in `flags-summary.md`
- SRS Integration: BA agent reads `spec.md` / `brainstorm.md` as structured input when `--srs` flag is used
- TodoWrite Tracking: PM agent creates and updates per-task entries for live progress visibility

---

## 2.3 User Characteristics

| Actor                     | Technical Level    | Domain Knowledge                        | Frequency      | Channel         | Accessibility Needs                     |
| ------------------------- | ------------------ | --------------------------------------- | -------------- | --------------- | --------------------------------------- |
| ACTOR-01: Solo Developer  | Expert             | Varies per project                      | Daily–Weekly   | Claude Code CLI | None (power user)                       |
| ACTOR-02: Technical Lead  | Expert             | Expert technical; intermediate business | Weekly         | Claude Code CLI | None                                    |
| ACTOR-03: PM / BA (Human) | Intermediate       | Expert business; basic technical        | Weekly         | Claude Code CLI | Clear progress output; no opaque errors |
| ACTOR-04: Startup Founder | Basic–Intermediate | Expert product; intermediate technical  | Multiple/week  | Claude Code CLI | Simple commands; minimal jargon         |
| ACTOR-05: BA Agent        | — (AI)             | Adapts to domain from input             | Per invocation | Agent tool      | —                                       |
| ACTOR-06: TechLead Agent  | — (AI)             | Expert technical                        | Per invocation | Agent tool      | —                                       |
| ACTOR-07: PM Agent        | — (AI)             | Intermediate coordination               | Per invocation | Agent tool      | —                                       |
| ACTOR-08: BE Dev Agent    | — (AI)             | Expert backend                          | Per invocation | Agent tool      | —                                       |
| ACTOR-09: FE Dev Agent    | — (AI)             | Expert frontend                         | Per invocation | Agent tool      | —                                       |
| ACTOR-10: Tester Agent    | — (AI)             | Expert testing                          | Per invocation | Agent tool      | —                                       |
| ACTOR-11: QA/QC Agent     | — (AI)             | Expert quality review                   | Per invocation | Agent tool      | —                                       |

**Persona summaries:**

**Solo Developer (ACTOR-01):** Alex builds side projects and MVPs alone. Expert in code but short on time for documentation. Wants to type one requirement and receive back a production-quality artifact set without switching roles. Uses full-auto mode (`/team`) for most invocations.

**Technical Lead (ACTOR-02):** Sam is a senior architect who uses the skill to validate design decisions and generate boilerplate architecture artifacts (ADRs, ERDs). Primarily uses per-agent mode — `/team-techlead` — with additional technical constraints injected via `--context`.

**PM / BA (Human) (ACTOR-03):** Jordan manages a small engineering team and uses the skill to produce structured user stories and sprint plans before involving the dev team. Comfortable with CLI but not a deep technical expert. Primarily uses `/team-ba` and `/team-pm`.

**Startup Founder (ACTOR-04):** Taylor is building a first product with limited engineering background. Uses Virtual Team Skill as a virtual CTO + team — describing features and receiving back architecture, code, and tests. Needs simple commands and clear artifact output they can hand to a contractor or review themselves.

---

## 2.4 Constraints

1. **Execution environment constraint**: The skill shall run exclusively within the Claude Code CLI environment. No alternative execution environment (standalone Python script, web app, CI/CD pipeline) is supported in v1.

2. **Model assignment constraint**: Agent models are fixed per role and shall not be configurable at runtime in v1:
   - `claude-opus-4-8`: TechLead Agent, QA/QC Agent
   - `claude-sonnet-4-6`: BA Agent, BE Dev Agent, FE Dev Agent, Tester Agent
   - `claude-haiku-4-5`: PM Agent

3. **No external API calls**: The skill shall not make HTTP requests to any service other than the Anthropic Claude API (managed by Claude Code). No GitHub API, Jira API, Slack API, or other third-party integrations in v1.

4. **No hardcoded credentials in generated artifacts**: All generated code files shall use environment variable references for credentials, API keys, and connection strings; no plain-text secret values shall appear in any artifact file.

5. **Cross-platform file path handling**: Skill instructions shall use forward-slash paths (`projects/{slug}/team/ba/`) and rely on Claude Code to resolve to OS-native paths. No OS-specific path separators shall be hardcoded.

6. **Output format constraint**: All human-readable artifacts shall be Markdown (`.md`). All diagrams shall use Mermaid syntax. No PDF, DOCX, or binary format output is generated by v1.

7. **Sub-agent depth constraint**: Sub-agents spawned by role agents shall not spawn further agents. Maximum invocation depth is 2 levels (orchestrator → role agent → optional sub-agent). Sub-agents use only Read/Write/Glob/Grep tools.

8. **No git push in v1**: The skill shall not execute `git push`, `git commit`, or any git write operation. Generated code is placed in the local file system; the operator decides when and how to commit it.

9. **Anthropic API dependency**: The skill has no functionality without an active Anthropic API connection. Operators must have a valid API key configured in Claude Code. No offline fallback mode exists.

---

## 2.5 Assumptions and Dependencies

**Assumptions (each can invalidate scope if wrong):**

1. **Claude Code availability**: Operator has Claude Code CLI installed, configured, and operational with a valid Anthropic API key. Skill does not handle setup or authentication.

2. **API quota sufficiency**: Operator has sufficient Anthropic API quota for at minimum 7 LLM calls per full pipeline run (2 Opus + 4 Sonnet + 1 Haiku). Quota-exceeded errors are surfaced by Claude Code; the skill provides resume instructions but cannot prevent mid-run failures due to quota limits.

3. **Single-call agent completeness**: Each role agent can produce its complete artifact set in one LLM call (plus optional sub-agent calls). For very complex requirements, a single call may not be sufficient; operators can use `--context` to pre-load constraints and improve output quality.

4. **File system as sufficient context medium**: Reading artifact files from disk provides coherent context between agents. No conversation history sharing between agents is required. If this assumption breaks (agent produces incoherent output despite reading files), the fix is to improve the agent's file-reading instructions, not to add inter-session context.

5. **Requirement input sufficiency**: The operator's initial requirement text (or SRS artifacts) contains sufficient detail for BA Agent analysis. BA will document assumptions in `requirements.md` rather than blocking for clarification in full-auto mode.

6. **Tech stack acceptance**: Operator accepts the tech stack selected by TechLead, or pre-constrains the selection by providing `--context "use Node.js, React, PostgreSQL"` at TechLead invocation time.

7. **Mermaid rendering environment**: Operator can render Mermaid-syntax diagrams in their viewing environment (VS Code with Mermaid Preview extension, GitHub, GitLab, Notion). Skill does not verify rendering capability.

8. **Sub-agent output merge**: Sub-agents spawned by role agents return their output to the parent role agent, which merges it before writing to disk. Sub-agent outputs are not written directly to disk.

**External dependencies:**

| Dependency                                            | What it provides                 | Risk if unavailable                                               |
| ----------------------------------------------------- | -------------------------------- | ----------------------------------------------------------------- |
| Anthropic Claude API                                  | LLM inference for all agents     | All skill functionality stops — no fallback                       |
| Claude Code CLI (Agent, Write, Read, TodoWrite tools) | Execution primitives             | Skill non-functional                                              |
| Local file system (write access)                      | Artifact persistence             | Pipeline cannot continue after any agent                          |
| SRS workflow artifacts (`spec.md`, `brainstorm.md`)   | Optional structured input for BA | Only affects F-C03 (SRS integration); all other phases unaffected |

---

## 2.6 Apportioning of Requirements

Features explicitly deferred to future versions:

| Deferred Feature                                             | Target Version | Reason for Deferral                                                                               |
| ------------------------------------------------------------ | -------------- | ------------------------------------------------------------------------------------------------- |
| Real git push to remote (opt-in `--push` flag)               | v2             | Irreversible external action; requires additional safety design and user confirmation flow        |
| DevOps/Infra Agent phase (Dockerfile, CI/CD, GitHub Actions) | v2             | Needs clearly defined input/output contract with BE/FE artifacts; not ready for v1                |
| Live code execution via Claude Code terminal tools           | v2             | Requires sandbox environment design; no tested pattern in current skill system                    |
| Custom agent personality/model configuration at runtime      | v2             | Fixed model assignment sufficient for v1; runtime config adds complexity without clear v1 benefit |
| Sub-agent depth level 3                                      | v2             | 2-level depth covers all v1 use cases; level 3 adds orchestration risk                            |
| ASCII diagram fallback (alternative to Mermaid)              | v2             | Low priority; most Claude Code environments support Mermaid rendering                             |
| Real-time multi-user collaboration                           | v3             | Requires fundamentally different architecture (multi-session context sharing)                     |
| Web app / PM dashboard UI                                    | v3             | Separate product category; out of scope for a CLI skill                                           |
| Agent-to-agent real-time messaging                           | v3             | File-based async communication sufficient through v2                                              |
