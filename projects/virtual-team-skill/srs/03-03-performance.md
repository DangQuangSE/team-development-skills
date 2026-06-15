# Software Requirements Specification — §3.3 Performance Requirements
## Virtual Team Skill

**Total NFRs in this section: 12 (11 Confirmed / 1 [TBD])**
Quality attribute scenarios follow ISO/IEC 25023 format.

> **Rule:** Response Measure must be numeric. No adjectives ("fast", "good", "acceptable").

---

#### NFR-01 — Functional Suitability: Completeness

| Field | Value |
|---|---|
| Source of Stimulus | Any role agent (BA, TechLead, PM, BE Dev, FE Dev, Tester, QA/QC) completing its execution |
| Stimulus | Agent writes artifact files to `projects/{slug}/team/{role}/` |
| Environment | Normal operation — Anthropic API responsive; file system writable |
| Artifact | Post-write artifact validation (Layer 1 check) |
| Response | System reads each artifact file and checks for all required section headings defined in the agent's validation schema; if all headings are present → PASS; if any heading is missing → FAIL with retry trigger |
| Response Measure | 100% of artifact files must contain all required section headings before the next agent is spawned; zero artifact files with missing required sections may progress to the next pipeline stage |

---

#### NFR-02 — Reliability: Recoverability

| Field | Value |
|---|---|
| Source of Stimulus | OS process termination, Claude Code session crash, or operator closes terminal mid-pipeline |
| Stimulus | Claude Code session is interrupted at any point during the pipeline |
| Environment | Any pipeline phase; at least one agent has completed writing artifacts to disk |
| Artifact | Local file system — `projects/{slug}/team/` artifact directories |
| Response | Operator reopens Claude Code and invokes the next incomplete phase via per-agent command; the system reads existing artifacts from disk and resumes from the interrupted phase without requiring re-entry of the original requirement text |
| Response Measure | 100% of previously completed artifact files survive session restart with zero content loss; operator can resume from any completed phase within one per-agent command invocation |

---

#### NFR-03 — Functional Suitability: Appropriateness

| Field | Value |
|---|---|
| Source of Stimulus | Role agent generating an artifact |
| Stimulus | Agent completes generating artifact content |
| Environment | Normal operation |
| Artifact | All artifact files in `team/{role}/` |
| Response | System writes the complete agent output to disk without applying word count caps, truncation, or size limits |
| Response Measure | Zero artificial size limits applied to any artifact file; artifact content is bounded only by the underlying LLM context window output capacity; no file shall be truncated mid-section due to imposed limits |

---

#### NFR-04 — Reliability: Fault Tolerance

| Field | Value |
|---|---|
| Source of Stimulus | Layer 1 structural validation detecting missing required headings |
| Stimulus | Validation failure after agent writes artifacts |
| Environment | Normal operation; agent has written at least one artifact file |
| Artifact | Orchestrator retry mechanism |
| Response | System automatically reruns the failed agent with an augmented prompt listing missing sections; this retry continues up to 3 attempts; on 3rd failure, a hard stop is issued with a detailed error log and recovery instructions |
| Response Measure | System retries automatically without operator intervention for attempts 1 and 2; hard stop on 3rd failure; maximum retry count = 3; no infinite retry loops; recovery instructions displayed within the same CLI session |

---

#### NFR-05 — Security: Confidentiality

| Field | Value |
|---|---|
| Source of Stimulus | Any role agent processing operator requirement input and generating artifact content |
| Stimulus | Artifact content (including operator requirement text and generated documents) traverses the system |
| Environment | Normal operation — pipeline executing |
| Artifact | All data transmission channels |
| Response | All data processing occurs through Anthropic Claude API (HTTPS) only; no artifact content, requirement text, or context is transmitted to any third-party service, external endpoint, or remote storage |
| Response Measure | Zero external API calls made by the skill beyond Anthropic API; zero bytes of artifact content transmitted to any service other than Anthropic; verifiable by network inspection showing only outbound connections to Anthropic API endpoints |

---

#### NFR-06 — Security: Integrity

| Field | Value |
|---|---|
| Source of Stimulus | BE Dev Agent or FE Dev Agent generating source code files |
| Stimulus | Code generation requiring database connection strings, API keys, passwords, tokens, or other credentials |
| Environment | Code generation phase (BE Dev or FE Dev phase) |
| Artifact | Generated code files in `team/be/` and `team/fe/`; `.env.example` |
| Response | Agent substitutes all credential values with environment variable references appropriate to the tech stack; credentials are documented in `.env.example` with placeholder values |
| Response Measure | Zero literal credential strings in any generated artifact file; 100% of credential references use environment variable pattern (e.g., `process.env.DB_PASSWORD`); QA/QC security review confirms zero violations in `quality-report.md` |

---

#### NFR-07 — Portability: Adaptability

| Field | Value |
|---|---|
| Source of Stimulus | Operator installing and running Virtual Team Skill on a different operating system |
| Stimulus | Skill commands invoked on Windows 10/11, macOS 12+, or Ubuntu 20.04+ |
| Environment | Any supported operating system with Claude Code CLI installed |
| Artifact | Skill `.md` files; file path handling in skill instructions |
| Response | Skill executes correctly and produces identical artifact structures on all three platforms; no OS-specific errors, path separator issues, or missing behaviors |
| Response Measure | 100% of FR-01 through FR-42 behaviors function identically on Windows 10/11, macOS 12+, and Ubuntu 20.04+; zero OS-specific code or path separators hardcoded in skill files |

---

#### NFR-08 — Security: Isolation

| Field | Value |
|---|---|
| Source of Stimulus | Operator running pipeline for two different projects (slug A and slug B) in the same workspace |
| Stimulus | Any agent invocation scoped to one project slug |
| Environment | Multiple project directories exist under `projects/` in the same workspace |
| Artifact | File system isolation — `projects/{slug-A}/team/` vs `projects/{slug-B}/team/` |
| Response | Each agent invocation reads exclusively from and writes exclusively to `projects/{slug}/team/` where `{slug}` matches the operator's specified or auto-detected project identifier |
| Response Measure | Zero artifact files shared between `projects/{slug-A}/` and `projects/{slug-B}/`; zero cross-project context leakage; verifiable by confirming no Read or Write tool call in a {slug-A} invocation references a `{slug-B}` path |

---

#### NFR-09 — Functional Suitability: Correctness (Sub-agent Depth)

| Field | Value |
|---|---|
| Source of Stimulus | A role agent deciding to spawn a sub-agent for a deep-dive or parallel sub-task |
| Stimulus | Role agent invokes Claude Code Agent tool to spawn a sub-agent |
| Environment | Any role agent phase during pipeline execution |
| Artifact | Sub-agent spawning logic in role agent skill instructions |
| Response | Sub-agent executes its task using only Read/Write/Glob/Grep tools and returns output to the parent role agent; sub-agent does not itself spawn further agents |
| Response Measure | Maximum invocation depth never exceeds 2 levels (orchestrator → role agent → sub-agent); zero instances of a sub-agent invoking the Agent tool; verifiable by absence of Agent tool calls in any sub-agent prompt |

---

#### NFR-10 — Compatibility: Co-existence

| Field | Value |
|---|---|
| Source of Stimulus | Operator installing Virtual Team Skill alongside other skills in the same Claude Code workspace |
| Stimulus | Operator invokes Virtual Team Skill commands in a workspace where other skills (e.g., SRS Workflow skills) are also present |
| Environment | Claude Code workspace with multiple skill directories |
| Artifact | Skill command namespace; skill file names; output directory structure |
| Response | Virtual Team Skill commands do not conflict with other skill command names; skill files do not overwrite other skill files; artifact paths do not collide with SRS workflow output paths |
| Response Measure | 100% of `/team-{role}` commands execute without conflict with any existing skill in the `srs-skills/` or other skill directories; zero file namespace collisions between Virtual Team Skill outputs and SRS workflow outputs |

---

#### NFR-11 — Performance Efficiency: Time Behaviour

| Field | Value |
|---|---|
| Source of Stimulus | Operator invoking full-auto pipeline for a medium-complexity requirement |
| Stimulus | `/team "{requirement}"` command execution for a project with approximately 8–12 user stories |
| Environment | Normal operation; Anthropic API responsive at typical response times |
| Artifact | All seven agents executing in sequence |
| Response | All seven agents complete their artifact generation; all artifacts pass Layer 1 validation; QA/QC sign-off is produced |
| Response Measure | `[TBD: baseline wall-clock time to be measured after first end-to-end test run — owner: Implementation team — resolve-by: after first full pipeline execution. Hypothesis: haiku (PM) ≈ 15–60s; sonnet (BA/BE/FE/Tester) ≈ 30–120s each; opus (TechLead/QA) ≈ 60–180s each; total pipeline ≈ 5–20 minutes for medium complexity. No timeout enforced per operator decision.]` |

---

#### NFR-12 — Performance Efficiency: Time Behaviour (Validation Speed)

| Field | Value |
|---|---|
| Source of Stimulus | Layer 1 validation running after an agent completes |
| Stimulus | Structural completeness check on a set of artifact files (4–5 files per agent on average) |
| Environment | Normal operation; files already on local disk |
| Artifact | Validation logic reading artifact files and checking section headings |
| Response | System reads each artifact file, applies heading detection (regex or equivalent), and returns PASS or FAIL with a list of missing headings |
| Response Measure | Validation check completes in < 5 seconds per artifact set; this is a local file read + heading detection operation requiring no API calls; measured from Write tool completion to validation result display |

---

## Performance Notes

### Response Time Summary
| Agent | Model | Estimated per-call time |
|---|---|---|
| PM Agent | claude-haiku-4-5 | ~15–60 seconds |
| BA Agent | claude-sonnet-4-6 | ~30–120 seconds |
| BE Dev Agent | claude-sonnet-4-6 | ~60–180 seconds (code generation is longer) |
| FE Dev Agent | claude-sonnet-4-6 | ~60–180 seconds |
| Tester Agent | claude-sonnet-4-6 | ~30–120 seconds |
| TechLead Agent | claude-opus-4-8 | ~60–180 seconds |
| QA/QC Agent | claude-opus-4-8 | ~60–180 seconds (reads all artifacts) |
| Layer 1 Validation | Local operation | < 5 seconds (NFR-12) |

### Throughput
- **Concurrent pipelines**: Not supported (v1 is single-user, single-pipeline)
- **Sub-agent concurrency**: Sequential within each role agent's context

### Data Capacity
- **Artifact size**: Unbounded (NFR-03); bounded by LLM output capacity
- **Number of projects**: Unlimited (disk space permitting)
- **Context window risk**: TechLead and QA/QC reading all artifacts for very large projects may approach model context limits; see TBD-07 for planned warning threshold
