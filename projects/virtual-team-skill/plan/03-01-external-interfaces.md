# Plan: §3.1 External Interfaces — Virtual Team Skill

---

## §3.1.1 User Interfaces

Virtual Team Skill is a CLI-based tool. There is no graphical UI. All operator interaction happens through Claude Code CLI commands in the terminal or VS Code integrated terminal.

### CLI Entry Points

| Command                                                             | Description                                         | Primary User       | Mode      |
| ------------------------------------------------------------------- | --------------------------------------------------- | ------------------ | --------- |
| `/team "{requirement}"`                                             | Full-auto pipeline — runs all 7 agents sequentially | ACTOR-01, ACTOR-04 | Full-auto |
| `/team-build "{requirement}"`                                       | Alias for `/team`                                   | ACTOR-01, ACTOR-04 | Full-auto |
| `/team-ba "{requirement}" [--project {slug}] [--context "{extra}"]` | Run BA agent only                                   | All operators      | Per-agent |
| `/team-techlead [--project {slug}] [--context "{extra}"]`           | Run TechLead agent only (reads BA artifacts)        | ACTOR-02           | Per-agent |
| `/team-pm [--project {slug}] [--context "{extra}"]`                 | Run PM agent only (reads BA + TechLead artifacts)   | ACTOR-03           | Per-agent |
| `/team-dev [--project {slug}] [--context "{extra}"]`                | Run BE Dev agent only                               | ACTOR-01           | Per-agent |
| `/team-fe [--project {slug}] [--context "{extra}"]`                 | Run FE Dev agent only                               | ACTOR-01           | Per-agent |
| `/team-test [--project {slug}] [--context "{extra}"]`               | Run Tester agent only                               | All operators      | Per-agent |
| `/team-qa [--project {slug}] [--context "{extra}"]`                 | Run QA/QC agent only                                | All operators      | Per-agent |
| `/team-list`                                                        | List all project slugs in `projects/`               | All operators      | Utility   |

**[NEEDS USER INPUT: confirm final command names — `/team-ba` vs `/vteam-ba` vs other convention — see OI-02]**

### CLI Output / Progress Display

During full-auto mode, the skill displays step-by-step progress:

```
[Virtual Team] Starting pipeline for project: {slug}
[BA] Analyzing requirements...
[BA] ✓ Artifact written: projects/{slug}/team/ba/requirements.md
[BA] ✓ Artifact written: projects/{slug}/team/ba/user-stories.md
[BA] ✓ Validation passed
[TechLead] Designing architecture...
...
[QA/QC] ✓ Sign-off: APPROVED
[Virtual Team] Pipeline complete. Artifacts at: projects/{slug}/team/
```

On validation failure (Layer 1):

```
[BA] ✗ Validation failed — missing sections: [## Business Rules, ## Acceptance Criteria]
[BA] Retrying (attempt 2/3)...
[BA] ✓ Validation passed on attempt 2
```

On hard stop after 3 failures:

```
[BA] ✗ Validation failed on attempt 3/3 (final)
[Virtual Team] HARD STOP — see: projects/{slug}/validation-errors/ba-final-failure.md
Action required: Review error log and retry manually with: /team-ba --project {slug}
```

### UI Constraints

- **Platform**: Terminal / VS Code integrated terminal (Windows PowerShell, macOS/Linux bash/zsh)
- **Output format**: Plain text with `[Agent]` prefixes and `✓` / `✗` status markers
- **No interactive prompts in full-auto mode**: Operator is not prompted mid-pipeline except on hard stop
- **Per-agent mode**: After each agent completes, skill shows summary and returns control to operator
- **Accessibility**: CLI output is screen-reader compatible (plain text, no ANSI color required — but ANSI colors may be used as enhancement)
- **WCAG**: Not applicable (CLI tool)

---

## §3.1.2 Hardware Interfaces

None required. Virtual Team Skill is a pure software tool.

The skill does not interface with:

- Printers
- Cameras or capture devices
- Physical sensors
- Hardware security modules (HSM)
- Biometric devices

Operator hardware requirement: any desktop or laptop capable of running Claude Code CLI (see §2.4 Constraints).

---

## §3.1.3 Software Interfaces

### Interface 1 — Anthropic Claude API

| Attribute              | Detail                                                                                                                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System                 | Anthropic Claude API                                                                                                                                                                                                                  |
| Protocol               | HTTPS (REST, managed entirely by Claude Code — skill does not make direct HTTP calls)                                                                                                                                                 |
| Direction              | Skill → Claude API (via Claude Code Agent tool)                                                                                                                                                                                       |
| Data exchanged         | Agent prompt + context artifacts (text) → LLM inference response (generated artifact text)                                                                                                                                            |
| Auth method            | API key configured in Claude Code CLI (`~/.claude/` config); skill does not access or manage the key                                                                                                                                  |
| Models used            | `claude-opus-4-8` (TechLead Agent, QA/QC Agent); `claude-sonnet-4-6` (BA, BE Dev, FE Dev, Tester); `claude-haiku-4-5` (PM Agent)                                                                                                      |
| Rate limits            | Subject to operator's Anthropic plan limits; skill has no built-in rate limit handling in v1                                                                                                                                          |
| Error handling         | If API call fails (timeout, rate limit, server error): Claude Code surfaces the error; skill instruction should include "If the API call fails, display the error and halt with resume instructions"                                  |
| SLA of external system | Anthropic API SLA applies; not controlled by this skill                                                                                                                                                                               |
| Context window limits  | TechLead and QA/QC agents reading all artifacts may approach context limits for very large projects; skill should warn if artifact directory exceeds estimated context limit [NEEDS USER INPUT: define max context warning threshold] |

### Interface 2 — Claude Code TodoWrite Tool

| Attribute      | Detail                                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| System         | Claude Code built-in TodoWrite tool                                                                                                        |
| Protocol       | Internal Claude Code tool call (not HTTP)                                                                                                  |
| Direction      | PM Agent → TodoWrite (write); Claude Code UI → TodoWrite (display)                                                                         |
| Data exchanged | Task entries: `{ content, status, activeForm }` objects per sprint task                                                                    |
| Auth method    | None — internal to Claude Code session                                                                                                     |
| Rate limits    | None known                                                                                                                                 |
| Error handling | If TodoWrite call fails: PM agent continues without tracking; log warning in `sprint-plan.md`                                              |
| Persistence    | TodoWrite entries exist for the duration of the Claude Code session only; not persisted to disk (disk persistence is via `team/pm/` files) |

### Interface 3 — Local File System

| Attribute               | Detail                                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------------------ |
| System                  | OS file system (Windows NTFS / macOS HFS+ / Linux ext4)                                                      |
| Protocol                | File read/write via Claude Code Read and Write tools                                                         |
| Direction               | Agents → disk (write artifacts); Agents ← disk (read previous artifacts)                                     |
| Data exchanged          | Markdown files (.md), source code files (.js, .ts, .py, etc.)                                                |
| Auth method             | OS file system permissions; Claude Code runs as current user                                                 |
| Path structure          | `projects/{slug}/team/{role}/` for artifacts; `projects/{slug}/validation-errors/` for failure logs          |
| Cross-platform handling | File paths must use `/` separator internally (Claude Code handles OS translation)                            |
| Max file size           | No explicit limit; artifact size is bounded by LLM output length                                             |
| Error handling          | If Write fails (disk full, permission denied): hard stop with error message; no retry for file system errors |

### Interface 4 — SRS Workflow Artifacts (Optional Integration)

| Attribute         | Detail                                                                                                                                                                                                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System            | SRS Workflow skills (`sr-brainstorm`, `sr-spec`) — same repository                                                                                                                                                            |
| Protocol          | File read (Read tool); no active inter-skill communication                                                                                                                                                                    |
| Direction         | SRS artifacts → BA Agent (read-only)                                                                                                                                                                                          |
| Data exchanged    | `projects/{slug}/brainstorm.md` and/or `projects/{slug}/spec.md` (Markdown)                                                                                                                                                   |
| Auth method       | None — local files                                                                                                                                                                                                            |
| When used         | Only when operator triggers BA agent with `--srs` flag or when `spec.md` exists in the project directory and BA detects it                                                                                                    |
| Conflict handling | If SRS artifact conflicts with operator runtime input: BA flags conflict and requests operator clarification before proceeding (BR-12) [NEEDS USER INPUT: confirm exact conflict-resolution UX in full-auto mode — see OI-07] |

---

## §3.1.4 Communication Interfaces

### Network Communication

- **Protocol**: HTTPS (TLS 1.2 minimum) — used exclusively for Anthropic API calls managed by Claude Code
- **Direction**: Outbound only from operator's local machine to Anthropic API endpoints
- **Payload format**: JSON (API request/response, managed by Claude Code — not visible to skill)
- **Offline behavior**: Skill cannot function without internet access (all agent invocations require API calls)

### No Email / SMS / Push Notification Interfaces

- Virtual Team Skill does not send emails, SMS messages, or push notifications
- All output is local (file system artifacts) and in-session (CLI display)

### Data Formats in Artifacts

- **Primary**: Markdown (`.md`) — all human-readable artifact files
- **Diagrams embedded in Markdown**: Mermaid syntax (`mermaid ... ` blocks)
- **Code artifacts**: Language-appropriate source files (`.js`, `.ts`, `.py`, `.sql`, etc.) — written to `team/be/` and `team/fe/` directories; format depends on tech stack selected by TechLead
- **Log files**: Markdown (`.md`) — validation error logs in `validation-errors/`
- **No XML, CSV, PDF, or binary formats** generated by v1

### No WebSocket / AMQP / gRPC

- All communication is synchronous (HTTPS request-response via Claude Code)
- No message queue or streaming protocol used in v1
