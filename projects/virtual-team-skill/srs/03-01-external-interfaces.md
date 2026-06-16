# Software Requirements Specification — §3.1 External Interface Requirements

## Virtual Team Skill

---

## 3.1.1 User Interfaces

Virtual Team Skill is a CLI-based tool. There is no graphical user interface. All operator interaction occurs through Claude Code CLI commands in a terminal (Windows PowerShell, macOS/Linux Bash/Zsh) or the VS Code integrated terminal.

### CLI Command Reference

| Command                                                                     | Mode      | Description                                                            | Primary Actor      |
| --------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------- | ------------------ |
| `/team "{requirement}" [--project {slug}] [--context "{extra}"]`            | Full-auto | Execute complete BA→TechLead→PM→BE→FE→Tester→QA pipeline automatically | ACTOR-01, ACTOR-04 |
| `/team-ba "{requirement}" [--project {slug}] [--context "{extra}"] [--srs]` | Per-agent | Run BA Agent only                                                      | All operators      |
| `/team-techlead [--project {slug}] [--context "{extra}"]`                   | Per-agent | Run TechLead Agent only (reads BA artifacts)                           | ACTOR-02           |
| `/team-pm [--project {slug}] [--context "{extra}"]`                         | Per-agent | Run PM Agent only (reads BA + TechLead artifacts)                      | ACTOR-03           |
| `/team-dev [--project {slug}] [--context "{extra}"]`                        | Per-agent | Run BE Dev Agent only                                                  | ACTOR-01           |
| `/team-fe [--project {slug}] [--context "{extra}"]`                         | Per-agent | Run FE Dev Agent only                                                  | ACTOR-01           |
| `/team-test [--project {slug}] [--context "{extra}"]`                       | Per-agent | Run Tester Agent only                                                  | All operators      |
| `/team-qa [--project {slug}] [--context "{extra}"]`                         | Per-agent | Run QA/QC Agent only                                                   | All operators      |
| `/team-list`                                                                | Utility   | List all project slugs under `projects/`                               | All operators      |

**Parameter specifications:**

- `--project {slug}`: Specifies project context. If omitted: system auto-detects from current working directory name and requests confirmation: _"Using project slug: {dir-name}. Continue? (y/n)"_
- `--context "{extra}"`: Supplemental context injected into the agent's prompt. Auto-detection: if value starts with `./` or `/` → treat as file path and read contents; otherwise → treat as inline text string. Context is prepended to the agent prompt and is ephemeral (not written to artifact files).
- `--srs`: Flag for `/team-ba` only. Causes BA Agent to read `projects/{slug}/spec.md` (and `brainstorm.md` if present) as primary input instead of free-text requirement.

### CLI Output Format

**Full-auto mode — progress display:**

```
[Virtual Team] Starting pipeline for project: {slug}
[BA] Analyzing requirements...
[BA] ✓ Written: projects/{slug}/team/ba/requirements.md
[BA] ✓ Written: projects/{slug}/team/ba/user-stories.md
[BA] ✓ Written: projects/{slug}/team/ba/acceptance-criteria.md
[BA] ✓ Written: projects/{slug}/team/ba/business-rules.md
[BA] ✓ Validation passed (attempt 1)
[Gate 1 Check] Preparing for TechLead phase...
[TechLead] Designing architecture...
...
[QA/QC] ✓ Sign-off: APPROVED
[Virtual Team] Pipeline complete.
Artifacts: projects/{slug}/team/
```

**Validation retry:**

```
[BA] ✗ Validation failed — missing: [## Business Rules]
[BA] Retrying (attempt 2/3)...
[BA] ✓ Validation passed (attempt 2)
```

**Hard stop:**

```
[BA] ✗ Validation failed on attempt 3/3 — HARD STOP
Error log: projects/{slug}/validation-errors/ba-attempt-3.md
Action: run /team-ba --project {slug} to retry manually
```

**Flags detected:**

```
[Virtual Team] Pipeline complete.
⚠️  2 cross-agent flags detected — see: projects/{slug}/flags-summary.md
```

### UI Constraints

- **No interactive prompts** in full-auto mode except for the slug confirmation dialog and hard stops
- **Output encoding**: UTF-8 plain text; ANSI color codes for `✓` / `✗` indicators (enhancement, not required for functionality)
- **Screen reader compatible**: Plain text output; all status information conveyed through text, not color alone
- **WCAG**: Not applicable — CLI tool

---

## 3.1.2 Hardware Interfaces

None required. Virtual Team Skill is a pure software tool with no hardware dependencies.

The system does not interface with: printers, cameras, scanners, sensors, hardware security modules, biometric devices, or any other peripheral hardware.

**Operator hardware minimum requirement**: Any desktop or laptop capable of running Claude Code CLI with an active internet connection for Anthropic API calls. No minimum RAM, CPU, or storage specifications are imposed by the skill itself.

---

## 3.1.3 Software Interfaces

### Interface SI-01: Anthropic Claude API

| Attribute      | Value                                                                                                                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System         | Anthropic Claude API                                                                                                                                                                                                        |
| Protocol       | HTTPS REST (managed entirely by Claude Code CLI — skill does not make direct HTTP calls)                                                                                                                                    |
| Direction      | Skill → Anthropic API (via Claude Code Agent tool invocations)                                                                                                                                                              |
| Data exchanged | Agent prompt text + artifact content (input) → generated artifact text (output)                                                                                                                                             |
| Authentication | API key configured in Claude Code local config (`~/.claude/`); skill does not access or store the key                                                                                                                       |
| Models used    | `claude-opus-4-8` (TechLead, QA/QC); `claude-sonnet-4-6` (BA, BE Dev, FE Dev, Tester); `claude-haiku-4-5` (PM)                                                                                                              |
| Rate limits    | Subject to operator's Anthropic plan tier; skill has no built-in rate limit backoff in v1                                                                                                                                   |
| Error handling | API failures (timeout, rate limit, server error) are surfaced by Claude Code; pipeline halts with the error message; operator retries the failed command                                                                    |
| Context window | TechLead and QA/QC agents reading all preceding artifacts for large projects may approach context window limits; skill shall warn operator if combined artifact size exceeds an implementation-defined threshold `[TBD-07]` |
| SLA            | Anthropic API SLA applies; not controlled by or guaranteed by this skill                                                                                                                                                    |

### Interface SI-02: Claude Code TodoWrite Tool

| Attribute      | Value                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| System         | Claude Code built-in TodoWrite tool                                                                        |
| Protocol       | Internal Claude Code tool call (not an HTTP interface)                                                     |
| Direction      | PM Agent → TodoWrite (write); Claude Code UI → TodoWrite (display to operator)                             |
| Data schema    | `{ todos: [{ content: string, status: "pending"\|"in_progress"\|"completed", activeForm: string }] }`      |
| Authentication | None — internal to the Claude Code session                                                                 |
| Error handling | If TodoWrite call fails: PM Agent continues without live tracking; logs warning in `sprint-plan.md`        |
| Persistence    | TodoWrite entries are session-only; not written to disk; disk persistence is via `team/pm/` artifact files |

### Interface SI-03: Local File System

| Attribute      | Value                                                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| System         | OS file system (Windows NTFS / macOS HFS+ / Linux ext4)                                                                                 |
| Protocol       | File read/write via Claude Code `Read` and `Write` tools                                                                                |
| Direction      | Agents → disk (write artifacts); Agents ← disk (read previous artifacts)                                                                |
| Data exchanged | Markdown files (`.md`); source code files (`.js`, `.ts`, `.py`, etc.); `.env.example`                                                   |
| Path structure | `projects/{slug}/team/{role}/` for artifacts; `projects/{slug}/validation-errors/` for failure logs; `projects/{slug}/flags-summary.md` |
| Authentication | OS file system permissions; Claude Code operates as the current OS user                                                                 |
| Path handling  | Forward-slash paths used internally; Claude Code resolves to OS-native paths                                                            |
| Error handling | Write failure (disk full, permission denied) → hard stop; error message displayed; no retry for file system errors                      |

### Interface SI-04: SRS Workflow Artifacts (Optional Integration)

| Attribute         | Value                                                                                                                                                                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System            | SRS Workflow skills (`sr-brainstorm`, `sr-spec`) — same repository                                                                                                                                                                                  |
| Protocol          | File read via Claude Code `Read` tool; no active inter-skill communication                                                                                                                                                                          |
| Direction         | SRS artifacts → BA Agent (read-only)                                                                                                                                                                                                                |
| Files consumed    | `projects/{slug}/brainstorm.md` and/or `projects/{slug}/spec.md`                                                                                                                                                                                    |
| When used         | Only when operator provides `--srs` flag to `/team-ba`                                                                                                                                                                                              |
| Conflict handling | If SRS artifact conflicts with runtime operator input: BA Agent records conflict in `## Conflicts Detected` section of `requirements.md`; SRS artifact content takes precedence in full-auto mode; per-agent mode pauses for operator clarification |
| Coupling          | Loose — Virtual Team Skill only reads; never writes SRS workflow artifacts                                                                                                                                                                          |

---

## 3.1.4 Communication Interfaces

### Network Communication

- **Protocol**: HTTPS (TLS 1.2 minimum), used exclusively for Anthropic API calls
- **Direction**: Outbound only — from operator's local machine to Anthropic API endpoints
- **Offline behavior**: No offline mode. Skill requires active internet for all agent invocations. File reads and validation checks are local-only.
- **Payload format**: JSON request/response (managed by Claude Code; not visible to skill instructions)

### Data Formats in Generated Artifacts

| Format                             | Usage                                                                                     |
| ---------------------------------- | ----------------------------------------------------------------------------------------- |
| Markdown (`.md`)                   | All human-readable artifacts — requirements, architecture, test plans, quality reports    |
| Mermaid syntax (embedded in `.md`) | Architecture diagrams, ERDs, sequence diagrams in TechLead artifacts                      |
| Language-appropriate source files  | BE Dev / FE Dev code artifacts (`.js`, `.ts`, `.py`, `.sql`, etc. — tech-stack-dependent) |
| Plain text (`.example`)            | `.env.example` listing environment variable placeholders                                  |

### No Additional Communication Interfaces

- No email, SMS, or push notifications
- No WebSocket, AMQP, gRPC, or streaming protocols
- No real-time inter-agent communication (agents communicate via file system artifacts only)
