# Plan: §3.5 Design Constraints — Virtual Team Skill

---

## §3.5.1 Technology Stack Constraints (Mandatory)

These constraints are non-negotiable — the skill must be built using these technologies as confirmed in brainstorm Round 4.

### Execution Environment
- **Claude Code CLI**: The skill MUST run within the Claude Code CLI environment. No alternative execution environment is supported in v1.
- **Claude Code Skill Format**: All skill files MUST be authored as Markdown (`.md`) files compatible with the Claude Code skill invocation system (Skill tool).

### Agent Orchestration
- **Claude Code Agent tool**: The skill MUST use the Claude Code `Agent` tool for spawning all role agents and sub-agents. No alternative orchestration mechanism (Python scripts, external APIs, MCP servers) is used in v1.
- **Agent sub-tool set**: Each spawned agent MUST use only Claude Code native tools: `Read`, `Write`, `Glob`, `Grep`, `TodoWrite`. Spawned agents MUST NOT use the `Agent` tool (sub-agents cannot spawn further agents — this enforces the 2-level depth limit, BR-07).

### Model Assignment (Fixed per Role)
| Role | Model | Constraint Rationale |
|---|---|---|
| TechLead Agent | `claude-opus-4-8` | Deep reasoning required for architectural decisions; cannot downgrade to Sonnet |
| QA/QC Agent | `claude-opus-4-8` | Comprehensive cross-artifact review requires deep reasoning |
| BA Agent | `claude-sonnet-4-6` | Balanced quality and cost for requirement analysis |
| BE Dev Agent | `claude-sonnet-4-6` | Good code generation quality; cost-effective for longer code output |
| FE Dev Agent | `claude-sonnet-4-6` | Same as BE Dev |
| Tester Agent | `claude-sonnet-4-6` | Good test case derivation from acceptance criteria |
| PM Agent | `claude-haiku-4-5` | Fast coordination and planning tasks; low reasoning overhead |

### File Output Format
- All human-readable artifact files MUST be Markdown (`.md`)
- Embedded diagrams MUST use Mermaid syntax (```mermaid blocks)
- Code artifacts (BE/FE) are written as source files in the appropriate language for the tech stack (`.js`, `.ts`, `.py`, etc.) — this is a runtime decision based on TechLead's `tech-stack.md`
- No binary, PDF, DOCX, or proprietary format output is permitted

### File Storage Constraint
- All artifacts MUST be stored under `projects/{slug}/team/` in the operator's current working directory
- The skill MUST NOT write outside the `projects/` directory (no writes to system directories, home directory outside workspace, or external storage)

---

## §3.5.2 Platform Constraints

### Cross-platform Compatibility (Non-negotiable)
- The skill MUST function identically on Windows 10/11, macOS 12+, and Ubuntu 20.04+
- **File path handling**: Skill instructions MUST NOT hardcode OS-specific path separators. Claude Code's `Read` and `Write` tools handle path normalization — skill authors must use forward-slash paths (`projects/slug/team/ba/`) internally, relying on Claude Code to resolve to the OS path format.
- **No OS-specific shell commands**: Skill instructions MUST NOT include bash-only or PowerShell-only commands. Any shell operations (if needed) must be expressed using cross-platform equivalents or avoided.
- **No OS-specific binaries**: Skill cannot depend on tools that are not available on all three platforms (e.g., cannot require `jq`, `grep` with GNU-only flags, etc.)

### Claude Code Version
- The skill is designed for Claude Code CLI as of the specification date (2026-06-16)
- If Claude Code changes the Skill tool format, Agent tool behavior, or TodoWrite interface, the skill may require updates
- [NEEDS USER INPUT: specify minimum Claude Code CLI version requirement if known]

---

## §3.5.3 Integration Constraints (Mandatory)

### SRS Workflow Integration (Optional, but design must accommodate)
- The file path convention for SRS workflow artifacts (`projects/{slug}/brainstorm.md`, `projects/{slug}/spec.md`) is shared with the Virtual Team Skill project directory
- Virtual Team Skill MUST NOT overwrite SRS workflow artifacts; it only reads them
- The BA agent's SRS integration feature (FR-14, FR-40) requires the skill design to check for SRS artifact existence before deciding input mode

### TodoWrite Integration
- The PM agent MUST use the Claude Code `TodoWrite` tool with the exact schema: `{ todos: [{ content: string, status: "pending"|"in_progress"|"completed", activeForm: string }] }`
- The skill design must account for the fact that TodoWrite state is session-only (not persisted to disk) and may be absent after session restart

---

## §3.5.4 Security-Driven Constraints

### No External API Calls Beyond Anthropic
- The skill MUST NOT make HTTP requests to any service other than Anthropic API (which is handled by Claude Code)
- Skill instructions MUST NOT include instructions to call GitHub API, Jira API, Slack API, or any other external service in v1
- This constraint is absolute — not even optional external calls are permitted in v1

### Credential Non-embedding Rule
- Skill instructions for BE Dev and FE Dev agents MUST explicitly prohibit embedding secrets in generated code
- The skill design must include this as a prominent instruction in the BE Dev and FE Dev skill files, not just as a validation check

### Validation Schema Confidentiality
- Required section heading lists (validation schemas) used in Layer 1 validation are part of the skill implementation and are not secret; however, they must be defined deterministically (not inferred dynamically) so validation is consistent and reproducible

---

## §3.5.5 Coding Standards / Style Constraints

### Skill File Authoring Standards
- Skill `.md` files MUST use clear, imperative instructions directed at the agent ("Read the BA artifacts from `projects/{slug}/team/ba/`. Analyze requirements. Write `requirements.md` to...")
- Skill instructions MUST include explicit output format templates with required section headings for each agent role
- Skill instructions MUST include the cross-agent flagging instruction: "Before writing your artifacts, read all artifacts from preceding agents and flag any inconsistencies in a `## Flags from Previous Agents` section"
- Agent validation schemas (required sections per artifact) MUST be enumerated in the skill file or in a companion reference file

### Markdown Artifact Style
- All agent-generated Markdown MUST use ATX-style headings (`##`, `###`) — not setext-style (`====`)
- ID fields (US-{n}, BR-{n}, ADR-{n}, TC-{n}, FLAG-{n}) MUST be zero-padded to 3 digits (e.g., `US-001`, `BR-012`) for consistent sorting
- Mermaid diagrams MUST be wrapped in proper code fences: ` ```mermaid ` on opening line, ` ``` ` on closing line

---

## §3.5.6 Budget / Infrastructure Constraints

- **No paid infrastructure**: Virtual Team Skill has no server-side component; it runs locally. The only recurring cost is Anthropic API usage per operator (operator's own account).
- **No third-party services allowed in v1**: No paid services (e.g., cloud file storage, CI/CD pipelines, project management tools) may be required or recommended in the v1 skill.
- **Open-source dependencies only**: If any helper scripts or companion files are added to the repository, they must use only open-source dependencies with licenses compatible with the repository license.
