# Software Requirements Specification — §3.6 System Attributes

## Virtual Team Skill

System attributes define the quality characteristics the system must exhibit across its lifetime. Each attribute is stated as a Quality Attribute Scenario following ISO/IEC 25023 format. NFR numbers continue from §3.3 (NFR-01–NFR-12); this section defines NFR-13 through NFR-24.

---

## 3.6.1 Reliability

#### NFR-13 — Reliability: Maturity (First-try Success Rate)

| Field              | Value                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Operator invoking any skill command with a syntactically valid requirement                                                                                                |
| Stimulus           | Skill command invoked with correct parameters for a standard-complexity requirement (≤ 15 user stories)                                                                   |
| Environment        | Normal operation — Anthropic API responsive; file system writable                                                                                                         |
| Artifact           | Pipeline execution from first agent invocation to artifact write                                                                                                          |
| Response           | Agent produces complete artifact set that passes Layer 1 validation without any retry                                                                                     |
| Response Measure   | ≥ 95% of skill invocations complete on the first attempt without requiring automated retry; measured over a sample of ≥ 20 invocations across different requirement types |

---

#### NFR-14 — Reliability: Maturity (Post-retry Success Rate)

| Field              | Value                                                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Layer 1 validation detecting missing sections after agent first attempt                                                                                                      |
| Stimulus           | Automated retry loop triggered (attempt 2 or 3)                                                                                                                              |
| Environment        | First attempt failed Layer 1 validation; retry prompt includes list of missing sections                                                                                      |
| Artifact           | Retry execution and post-retry artifact validation                                                                                                                           |
| Response           | Agent produces complete artifact set with all required sections on retry attempt                                                                                             |
| Response Measure   | ≥ 99% of skill invocations produce a complete artifact set after up to 3 attempts; the remaining ≤ 1% result in a documented hard stop with actionable recovery instructions |

---

#### NFR-15 — Reliability: Fault Tolerance (Graceful Degradation on Hard Stop)

| Field              | Value                                                                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Hard stop triggered after 3 consecutive Layer 1 validation failures                                                                                                                                                       |
| Stimulus           | Pipeline terminates at the failing agent                                                                                                                                                                                  |
| Environment        | Preceding agents have written complete, validated artifacts                                                                                                                                                               |
| Artifact           | Artifacts from all phases preceding the failing agent; validation error log                                                                                                                                               |
| Response           | System preserves all artifacts from completed phases; writes detailed failure log to `validation-errors/{agent}-attempt-3.md`; displays recovery command to operator; does not delete or overwrite any preceding artifact |
| Response Measure   | 100% of artifacts from phases preceding the hard-stop agent are preserved unchanged; recovery command is displayed within the same CLI session; validation error log is written before session exits                      |

---

#### NFR-16 — Reliability: Recoverability (Session Crash Recovery)

| Field              | Value                                                                                                                                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Unexpected Claude Code session termination (OS crash, terminal close, network loss)                                                                                                                                                               |
| Stimulus           | Claude Code session closes mid-pipeline at any point after at least one agent has written artifacts                                                                                                                                               |
| Environment        | Mid-pipeline execution; some agents complete, some not yet started                                                                                                                                                                                |
| Artifact           | Local file system — `projects/{slug}/team/` directories                                                                                                                                                                                           |
| Response           | All previously written artifact files survive session termination; on next session start, operator invokes the next incomplete agent via per-agent command and pipeline resumes from that point without re-entering the original requirement text |
| Response Measure   | 100% of artifact files written before session termination survive with zero content loss; operator can resume pipeline within one per-agent command invocation after session restart                                                              |

---

## 3.6.2 Availability

#### NFR-17 — Availability: Time Behaviour (Session Independence)

| Field              | Value                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Operator closing Claude Code between pipeline phases and reopening it later                                                                                               |
| Stimulus           | Operator runs `/team-techlead --project {slug}` in a new Claude Code session, after BA artifacts were produced in a prior session                                         |
| Environment        | New Claude Code session; BA artifacts present on disk from prior session                                                                                                  |
| Artifact           | TechLead agent reading BA artifact files at invocation time                                                                                                               |
| Response           | TechLead agent reads all BA artifacts from disk; proceeds with architecture design without requiring re-entry of original requirement or previous session context         |
| Response Measure   | 100% of per-agent commands succeed when invoked in a fresh session, provided all prerequisite artifacts exist on disk; zero dependency on prior session's in-memory state |

---

#### NFR-18 — Availability: Resource Utilisation (No Background Process)

| Field              | Value                                                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Operator's machine operating normally between skill invocations                                                                                                              |
| Stimulus           | Skill is installed but not currently being invoked                                                                                                                           |
| Environment        | Any OS state (idle, sleep, under load)                                                                                                                                       |
| Artifact           | Skill `.md` files on disk                                                                                                                                                    |
| Response           | The skill consumes zero CPU, zero memory, and zero network bandwidth when not actively invoked; no background daemon, watcher, or scheduler is started                       |
| Response Measure   | 0 CPU cycles consumed by the skill when not invoked; 0 network packets sent between invocations; verified by absence of any background process started by skill installation |

---

## 3.6.3 Security

#### NFR-19 — Security: Confidentiality (Data Transmission Scope)

| Field              | Value                                                                                                                                                                                                                                         |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Pipeline execution transmitting requirement text and agent context to Anthropic API                                                                                                                                                           |
| Stimulus           | Any agent invocation sending prompt data to the Claude API                                                                                                                                                                                    |
| Environment        | Normal operation — all agents across full pipeline run                                                                                                                                                                                        |
| Artifact           | All data transmission paths from operator's machine                                                                                                                                                                                           |
| Response           | Requirement text, artifact content, and context chain data are transmitted only to the Anthropic Claude API via HTTPS; zero bytes of this data are transmitted to any other endpoint, logging service, analytics platform, or third-party API |
| Response Measure   | Zero outbound network connections from the skill to any endpoint other than Anthropic API endpoints; verifiable by network inspection showing only HTTPS traffic to `api.anthropic.com` during skill execution                                |

---

#### NFR-20 — Security: Integrity (No Hardcoded Credentials in Generated Artifacts)

| Field              | Value                                                                                                                                                                                                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | BE Dev Agent or FE Dev Agent generating source code that requires database connections, API integrations, or authentication logic                                                                                                                                      |
| Stimulus           | Code generation involving credential-dependent operations                                                                                                                                                                                                              |
| Environment        | BE Dev phase or FE Dev phase of pipeline                                                                                                                                                                                                                               |
| Artifact           | All source code files in `team/be/` and `team/fe/`; `.env.example`                                                                                                                                                                                                     |
| Response           | Agent substitutes all credential values with environment variable references matching the tech stack convention; `.env.example` lists each required variable with a placeholder value, never a real value                                                              |
| Response Measure   | Zero literal credentials (passwords, tokens, keys, connection strings with embedded credentials) in any generated artifact file; 100% of credential references use environment variable pattern; QA/QC security review in `quality-report.md` confirms zero violations |

---

#### NFR-21 — Security: Non-repudiation (Pipeline Audit Trail)

| Field              | Value                                                                                                                                                                                                                                                     |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Operator or auditor reviewing the pipeline execution history                                                                                                                                                                                              |
| Stimulus           | Request to determine which agents ran, what validation outcomes occurred, and what flags were raised                                                                                                                                                      |
| Environment        | After pipeline completion (successful or partial)                                                                                                                                                                                                         |
| Artifact           | Validation error logs (`validation-errors/`); flags summary (`flags-summary.md`); agent artifact files with timestamps                                                                                                                                    |
| Response           | System provides permanent, unmodified logs of every Layer 1 validation failure; agent artifacts include ISO 8601 timestamps; flags summary records all cross-agent flags with their source agent, severity, and affected artifact                         |
| Response Measure   | 100% of Layer 1 validation failures are logged to `validation-errors/` with agent name, attempt number, timestamp, and specific missing sections; validation logs are never auto-deleted; flags summary includes 100% of flags raised during the pipeline |

---

## 3.6.4 Maintainability

#### NFR-22 — Maintainability: Modularity (Role Isolation)

| Field              | Value                                                                                                                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Skill contributor modifying the TechLead Agent skill file to add a new ADR requirement                                                                                                                           |
| Stimulus           | Change to `team-techlead.md` skill file                                                                                                                                                                          |
| Environment        | Development / maintenance mode — operator edits skill files in repository                                                                                                                                        |
| Artifact           | Individual skill `.md` files for each role                                                                                                                                                                       |
| Response           | Changes to one role's skill file do not require changes to any other role's skill file, provided the artifact file paths and required section headings are unchanged                                             |
| Response Measure   | 100% of single-role behavior changes can be implemented by editing only the affected role's skill file and the validation schema reference; zero forced edits to other role skill files for a single-role change |

---

#### NFR-23 — Maintainability: Analysability (Error Diagnosis Speed)

| Field              | Value                                                                                                                                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Source of Stimulus | Operator investigating a hard stop or unexpected artifact content                                                                                                                                                                    |
| Stimulus           | Operator opens the validation error log and flags summary to diagnose the failure                                                                                                                                                    |
| Environment        | Post-failure; validation error log and/or flags summary exist on disk                                                                                                                                                                |
| Artifact           | `projects/{slug}/validation-errors/{agent}-attempt-{n}.md`; `projects/{slug}/flags-summary.md`                                                                                                                                       |
| Response           | Validation error log clearly states: which sections were expected, which were found, which are missing; flags summary clearly states: which agent raised each flag, the affected artifact, severity, and suggested resolution        |
| Response Measure   | An operator with intermediate technical proficiency (ACTOR-02) can identify the specific failing section and the correct remediation command within 5 minutes of reading the error log; no additional tool or documentation required |

---

## 3.6.5 Portability

#### NFR-24 — Portability: Adaptability (Cross-platform Equivalence)

| Field              | Value                                                                                                                                                                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source of Stimulus | Operator installing Virtual Team Skill on a different OS than the development environment                                                                                                                                                                       |
| Stimulus           | Skill commands invoked on a non-development platform (e.g., developed on macOS, used on Windows 11)                                                                                                                                                             |
| Environment        | Any supported OS (Windows 10/11, macOS 12+, Ubuntu 20.04+) with Claude Code CLI installed                                                                                                                                                                       |
| Artifact           | Skill `.md` files; artifact files written to local file system                                                                                                                                                                                                  |
| Response           | All 42 FRs execute identically; artifact directory structure matches `projects/{slug}/team/` on all platforms; no path separator, shell syntax, or OS-specific behavior causes functional difference                                                            |
| Response Measure   | 100% of FR-01 through FR-42 behaviors are functionally equivalent across Windows 10/11, macOS 12+, and Ubuntu 20.04+; zero OS-specific failures in cross-platform testing; verified by running full pipeline on each platform and comparing artifact structures |

---

## 3.6.6 Usability

### Learnability

The CLI command structure follows a single consistent pattern across all invocations:

```
/team-{role} [--project {slug}] [--context "{extra}"] [--srs]
```

An operator who has used one per-agent command can apply the same pattern to any other agent without additional training.

### Efficiency Targets

| Scenario                                        | Target Steps                          |
| ----------------------------------------------- | ------------------------------------- |
| Run full pipeline end-to-end                    | 1 command                             |
| Re-run a single agent after reviewing artifacts | 1 command                             |
| Pass supplemental context to a specific agent   | 1 command with `--context` parameter  |
| List all projects in the workspace              | 1 command (`/team-list`)              |
| Resume a pipeline after a hard stop             | 1 command (per recovery instructions) |

### Error Message Quality Requirement

Every error message produced by the skill shall include all four of the following elements:

1. **Which agent failed** — e.g., `[BA]`
2. **What was expected** — e.g., `missing sections: [## Business Rules]`
3. **What was found** — sections present in the artifact
4. **The exact command to resolve the issue** — e.g., `run: /team-ba --project {slug} to retry`

Hard stop messages shall additionally include the path to the failure log file.

### Output Readability

All CLI progress output uses the `[AgentName] ✓/✗ Message` prefix format, making it parseable both by human reading and by piped log processing (e.g., `tee pipeline.log`).

### WCAG Compliance

Not applicable — CLI tool, not a web application. All status information is conveyed through text, not color alone, ensuring compatibility with screen readers that process terminal output.

### Onboarding Requirement

The following operator documentation shall be provided with v1:

| Document              | Content                                                                                                                                        | Target audience         |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `README.md`           | Installation, quick-start (full pipeline + per-agent), command reference, artifact structure, FAQ                                              | All operator types      |
| Per-skill inline help | Reference available via documentation for each command; behavior of `--help` flag subject to Claude Code skill format feasibility — see TBD-09 | ACTOR-01, ACTOR-02      |
| `CLAUDE.md`           | Project context for Claude Code sessions in this repository                                                                                    | Contributors / ACTOR-02 |
