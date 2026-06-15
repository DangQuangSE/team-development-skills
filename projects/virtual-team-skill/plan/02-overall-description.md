# Plan: §2 Overall Description — Virtual Team Skill

---

## §2.1 Product Perspective

**System classification**: New standalone tool (not a replacement for an existing system; not a component of a larger system at launch). Future v2 may integrate more tightly with the SRS workflow pipeline.

**System context:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        OPERATOR'S ENVIRONMENT                           │
│                                                                         │
│   ┌──────────────┐    triggers     ┌────────────────────────────────┐  │
│   │   Operator   │ ─────────────► │   Claude Code CLI               │  │
│   │ (Solo Dev /  │                 │   (terminal / VS Code ext.)     │  │
│   │  TechLead /  │ ◄───────────── │                                 │  │
│   │  PM / Founder│   shows output  │   ┌──────────────────────────┐ │  │
│   └──────────────┘                 │   │  Virtual Team Skill       │ │  │
│                                    │   │  (orchestrator .md file)  │ │  │
│   ┌──────────────┐                 │   │                           │ │  │
│   │ Local File   │ ◄──────────── │   │  ┌────────────────────┐   │ │  │
│   │ System       │    artifacts   │   │  │  Agent: BA         │   │ │  │
│   │ projects/    │ ──────────── ► │   │  │  Agent: TechLead   │   │ │  │
│   │ {slug}/team/ │    read        │   │  │  Agent: PM         │   │ │  │
│   └──────────────┘                 │   │  │  Agent: BE Dev     │   │ │  │
│                                    │   │  │  Agent: FE Dev     │   │ │  │
│   ┌──────────────┐                 │   │  │  Agent: Tester     │   │ │  │
│   │ SRS Workflow │ ──────────── ► │   │  │  Agent: QA/QC      │   │ │  │
│   │ artifacts    │   optional      │   │  └────────────────────┘   │ │  │
│   │ (spec.md,    │   BA input      │   └──────────────────────────┘ │  │
│   │  brainstorm) │                 └──────────────┬─────────────────┘  │
│   └──────────────┘                                │                     │
│                                                   ▼                     │
│                                    ┌──────────────────────────┐         │
│                                    │   Anthropic Claude API   │         │
│                                    │   (managed by Claude Code│         │
│                                    │    — not direct HTTP)    │         │
│                                    └──────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────┘
```

**How this system fits into the user's existing ecosystem:**

- The skill runs entirely within the operator's local Claude Code environment
- No cloud infrastructure needed beyond what Claude Code already uses (Anthropic API)
- Artifacts are stored on the operator's local file system — fully under operator control
- Operators who already use the SRS Workflow (`sr-brainstorm` → `sr-spec`) can feed those artifacts directly into the Virtual Team pipeline (BA reads `spec.md`)
- Generated code artifacts (BE/FE files) can be copied into the operator's own project repository — there is no direct connection to any git remote

---

## §2.2 Product Functions

**Functional area summary (maps to feature clusters in spec.md §3):**

### Cluster A — Workflow Engine

| Function                      | Description                                                                                        | Actors                       |
| ----------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------- |
| Full-auto pipeline execution  | Operator provides a requirement; skill runs all 7 agents automatically, end-to-end                 | ACTOR-01, ACTOR-04           |
| Per-agent selective execution | Operator invokes individual agents via role-specific commands; agents read existing artifacts      | ACTOR-01, ACTOR-02, ACTOR-03 |
| Context chain management      | System ensures each agent receives outputs from all preceding agents via file reads                | All agent actors             |
| Artifact persistence          | All outputs written to disk before next agent starts; context survives restart                     | All agent actors             |
| Hybrid workflow enforcement   | Sprint-based execution with three milestone gates (Design Freeze, UAT Readiness, Release Sign-off) | PM Agent, QA Agent           |
| Multi-project isolation       | Each project is isolated under `projects/{slug}/team/`; no cross-project leakage                   | All operators                |

### Cluster B — Agent Roles

| Function                          | Description                                                                                        | Actors   |
| --------------------------------- | -------------------------------------------------------------------------------------------------- | -------- |
| BA — Requirement Analysis         | Analyze operator input; produce user stories (US-{n}), acceptance criteria (GWT), business rules   | ACTOR-05 |
| TechLead — Architecture Design    | Design system architecture; produce ADR, ERD, sequence diagrams, tech stack decision in Mermaid    | ACTOR-06 |
| PM — Sprint Planning              | Organize stories into sprints; produce sprint plan, task breakdown, story points; update TodoWrite | ACTOR-07 |
| BE Dev — Backend Code Generation  | Generate server-side code aligned to TechLead architecture and sprint tasks                        | ACTOR-08 |
| FE Dev — Frontend Code Generation | Generate client-side code aligned to tech stack and BE API contracts                               | ACTOR-09 |
| Tester — Test Artifact Generation | Produce test plan, unit/integration/e2e test cases, bug report template from acceptance criteria   | ACTOR-10 |
| QA/QC — Quality Review & Sign-off | Review all artifacts; produce quality report, compliance checklist, advisory sign-off verdict      | ACTOR-11 |

### Cluster C — Error Handling & Validation

| Function                       | Description                                                                                            | Actors                       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------ | ---------------------------- |
| Automated Validation (Layer 1) | Check artifact structural completeness; auto-retry up to 3 times; hard stop with error log on 3rd fail | Orchestrator + All agents    |
| Cross-agent Flagging (Layer 2) | Each agent flags logic errors from previous agents in a dedicated section                              | ACTOR-06, ACTOR-10, ACTOR-11 |
| SRS Integration                | BA agent reads existing SRS artifacts (`brainstorm.md`, `spec.md`) as structured input                 | ACTOR-05                     |
| TodoWrite Tracking             | PM agent creates and updates task entries visible in conversation                                      | ACTOR-07                     |

---

## §2.3 User Characteristics

### ACTOR-01: Solo Developer

**Persona:** Alex is a full-stack developer building side projects and MVPs alone. They understand code but don't always have time to write proper documentation, architecture decisions, or test plans. They want to type a requirement and get back a production-quality artifact set without context-switching between roles.

| Attribute             | Detail                                                               |
| --------------------- | -------------------------------------------------------------------- |
| Technical proficiency | Expert (code, architecture, tooling)                                 |
| Domain knowledge      | Varies per project (adapts quickly)                                  |
| Frequency of use      | Daily to weekly                                                      |
| Channel               | Claude Code CLI — terminal or VS Code extension                      |
| Device                | Desktop / laptop (Windows or Mac)                                    |
| Accessibility needs   | None                                                                 |
| Primary pain point    | Context-switching overhead; missing artifacts (no test plan, no ADR) |
| Key expectation       | Full pipeline in one command; no re-entering context between agents  |

### ACTOR-02: Technical Lead / Architect

**Persona:** Sam is a senior engineer who designs systems and reviews code for a team. They use the tool to get a "second opinion" from the AI TechLead agent, to validate their own architectural choices, or to quickly generate ADRs and ERDs for a new module. They mostly use per-agent mode — triggering only `/team-techlead` — and supply additional constraints via `--context`.

| Attribute             | Detail                                                                     |
| --------------------- | -------------------------------------------------------------------------- |
| Technical proficiency | Expert                                                                     |
| Domain knowledge      | Expert technical; intermediate business                                    |
| Frequency of use      | Weekly — for specific design validation sessions                           |
| Channel               | Claude Code CLI                                                            |
| Device                | Desktop (Mac preferred)                                                    |
| Accessibility needs   | None                                                                       |
| Primary pain point    | Writing boilerplate ADRs and diagrams; getting a structured second opinion |
| Key expectation       | High-quality TechLead output (Opus model); ability to inject constraints   |

### ACTOR-03: Product Manager / BA (Human)

**Persona:** Jordan is a PM or BA who manages a small engineering team. They use the skill to produce structured user stories and sprint plans before the dev team is available, or to validate their own requirement analysis against an AI BA. They are comfortable with CLI tools but are not developers.

| Attribute             | Detail                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------ |
| Technical proficiency | Intermediate (comfortable with CLI; no deep coding knowledge)                              |
| Domain knowledge      | Expert business; basic technical                                                           |
| Frequency of use      | Weekly — typically BA + PM phases only                                                     |
| Channel               | Claude Code CLI                                                                            |
| Device                | Desktop (Windows or Mac)                                                                   |
| Accessibility needs   | Clear progress feedback; no opaque failures                                                |
| Primary pain point    | Translating stakeholder input into structured stories and sprint plans                     |
| Key expectation       | Professional user story format (As a / I want / So that) + story points + sprint structure |

### ACTOR-04: Startup Founder / Solo Maker

**Persona:** Taylor is a non-technical or semi-technical founder building their first product. They have strong product intuition but limited engineering bandwidth. They use the skill as their "virtual CTO + team" — describing a feature and getting back everything from architecture to code to test plan.

| Attribute             | Detail                                                                                |
| --------------------- | ------------------------------------------------------------------------------------- |
| Technical proficiency | Basic to intermediate                                                                 |
| Domain knowledge      | Expert product/business; intermediate technical                                       |
| Frequency of use      | Frequent — multiple times per week for each product feature                           |
| Channel               | Claude Code CLI (or VS Code extension)                                                |
| Device                | Desktop (any OS)                                                                      |
| Accessibility needs   | Simple commands; clear progress output; minimal jargon in skill prompts               |
| Primary pain point    | No team; must produce software artifacts alone despite limited engineering background |
| Key expectation       | End-to-end pipeline with minimal effort; high-quality artifacts across all roles      |

---

## §2.4 Constraints

### Regulatory / Legal

- No applicable regulatory compliance (GDPR, HIPAA, PCI-DSS) — this is a developer tooling product that does not process end-user PII or financial data.
- Self-imposed security constraint: generated code artifacts must never contain hardcoded credentials (enforced by BR-05 and QA/QC review).
- Data privacy self-constraint: project artifacts and context sent through Anthropic API only; no third-party data transmission.

### Hardware

- No special hardware requirements. Skill runs on any device running Claude Code CLI.
- Minimum: desktop or laptop with internet access (for Anthropic API calls).
- Tested platforms: Windows 10/11, macOS 12+, Ubuntu 20.04+.

### Software Interfaces (Mandatory)

- Claude Code CLI must be installed (`@anthropic-ai/claude-code` v1.0+)
- Valid Anthropic API key configured in Claude Code
- Local file system with write access to the working directory
- Mermaid-compatible viewer for diagram rendering (VS Code with Mermaid Preview, GitHub, etc.) — recommended, not enforced by skill itself

### Security

- All agent calls go through Anthropic API (TLS 1.2+ enforced by Claude Code HTTP client)
- No local secrets storage beyond what Claude Code CLI already manages (API key in config)
- Generated code must not contain hardcoded secrets (enforced at generation + QA review level)
- Artifacts stored locally — operator is responsible for their own file system security

### Timeline / Budget

- [NEEDS USER INPUT: formal timeline and budget not set — this is a skill built within the existing MySkills repository; no external budget allocation confirmed]
- Planning assumption: v1 can be built as skill .md files within the existing repository structure without additional tooling investment

---

## §2.5 Assumptions and Dependencies

### Assumptions (numbered, each can invalidate scope if wrong)

1. **Claude Code availability**: Operator always has Claude Code CLI running. Skill is not designed to run in any other environment.
   - _Risk if wrong_: Entire skill non-functional; no mitigation at skill level.

2. **API quota sufficiency**: Operator has sufficient Anthropic API tokens for 7+ agent invocations (2 Opus + 4 Sonnet + 1 Haiku minimum per full pipeline run).
   - _Risk if wrong_: Pipeline fails mid-run with API rate limit or quota exceeded error; skill should catch this and provide clear error message with resume instructions.

3. **Single-call agent sufficiency**: Each role agent can produce its complete artifact in one LLM call (plus optional sub-agent calls). No interactive back-and-forth needed in full-auto mode.
   - _Risk if wrong_: BA may produce incomplete requirements for complex projects; mitigated by the `--context` flag allowing operators to pre-load clarifications.

4. **File system as sufficient context medium**: Reading previous artifacts from disk provides enough context coherence between agents. Agents do not need shared conversation history.
   - _Risk if wrong_: Incoherent output if agents fail to read or interpret previous artifacts correctly; mitigated by explicit context injection instructions in each agent's skill prompt.

5. **Requirement input sufficiency**: Operator's initial input (free text or SRS artifact) is sufficient for BA to analyze and document. BA documents assumptions rather than blocking.
   - _Risk if wrong_: BA output has many assumptions; quality degrades on vague inputs. Recommendation: use SRS workflow first for complex projects.

6. **Tech stack acceptance**: Operator accepts the tech stack selected by TechLead, or pre-constrains it via `--context` before triggering TechLead phase.
   - _Risk if wrong_: Generated code uses wrong framework; operator must rerun TechLead with explicit stack constraints. Mitigated by `--context` parameter.

7. **Mermaid rendering environment**: Operator can render Mermaid syntax in their viewing environment.
   - _Risk if wrong_: Diagrams appear as raw text. Mitigation: skill may add ASCII fallback in v2.

8. **Sub-agent merge assumption**: Sub-agents return output to their parent role agent, which merges it before writing to disk.
   - _Risk if wrong_: Sub-agent output lost if parent fails before merge; skill should validate merged output before writing.

### External Dependencies

| Dependency                                                   | Risk if unavailable                                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Anthropic Claude API                                         | All skill functionality stops — no fallback possible                                        |
| Claude Code CLI tool (`Agent`, `Write`, `Read`, `TodoWrite`) | Skill non-functional — these are core execution primitives                                  |
| Local file system (write access)                             | Artifact persistence fails; pipeline cannot continue                                        |
| SRS workflow artifacts (`spec.md`, `brainstorm.md`)          | Optional dependency — only affects SRS integration feature (F-C03); other phases unaffected |

---

## §2.6 Apportioning of Requirements (Deferred Features)

| Feature                                                        | Deferred to | Reason                                                                             |
| -------------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------- |
| Real git push to remote (opt-in flag)                          | v2          | Irreversible external action; needs explicit safety design                         |
| DevOps/Infra phase (Dockerfile, CI/CD scripts, GitHub Actions) | v2          | Needs clear dependency mapping on BE/FE output; not ready for v1                   |
| Live code execution via Claude Code terminal tools             | v2          | Sandbox environment design needed; not in scope v1                                 |
| Custom agent personality configuration                         | v2          | Role behavior in skill .md files sufficient for v1; runtime config adds complexity |
| Sub-agent depth level 3                                        | v2          | 2-level depth sufficient for v1; level 3 adds orchestration complexity             |
| ASCII diagram fallback (Mermaid alternative)                   | v2          | Low priority — most Claude Code environments support Mermaid                       |
| Real-time multi-user collaboration                             | v3          | Fundamentally different architecture required                                      |
| Web app / PM dashboard UI                                      | v3          | Separate product; CLI-only in v1 and v2                                            |
| Agent-to-agent real-time messaging                             | v3          | File-based async communication sufficient through v2                               |
