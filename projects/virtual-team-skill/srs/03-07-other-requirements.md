# Software Requirements Specification — §3.7 Other Requirements

## Virtual Team Skill

---

## 3.7.1 Localization / Internationalization (i18n) Requirements

### Skill Instruction Language

All skill `.md` files (agent instructions) shall be written in English. This constraint is fixed for v1.

**Rationale:** Consistency with the Claude Code skill ecosystem; most Claude Code operators read English for technical tooling. Multi-language skill instructions are a v2 enhancement.

### Artifact Output Language

The skill shall not enforce a specific output language for generated artifacts. Agents shall produce artifacts in the same natural language as the operator's requirement input:

- English input → English artifacts
- Vietnamese input → Vietnamese artifacts
- Mixed input → Agent best-judgment (LLM default behavior applies)

**No language detection or enforcement logic is implemented by the skill.** Language follows LLM behavior for the given input.

### Validation Heading Language

Layer 1 validation checks for required section headings using exact case-sensitive string matching against English headings (e.g., `## User Stories`, `## Business Rules`). This means:

- Validation schemas are defined in English
- If the LLM generates headings in a different language (e.g., `## Câu chuyện người dùng` instead of `## User Stories`), the Layer 1 check will fail
- Agents shall be instructed to write required section headings in English regardless of the artifact body language — heading and body may be in different languages

Multi-language heading validation is explicitly deferred to v2 (TBD-12, resolved as OUT OF SCOPE v1).

### Date, Number, and Currency Formats

| Data type                                     | Format                                                 | Rationale                                     |
| --------------------------------------------- | ------------------------------------------------------ | --------------------------------------------- |
| Dates in metadata (validation logs, sign-off) | ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)                        | Language-independent; universally unambiguous |
| Sprint dates in `sprint-plan.md`              | PM Agent follows operator's calendar convention        | No enforcement by skill                       |
| Story points                                  | Numeric (1, 3, 5, 8)                                   | No localization needed                        |
| Currency                                      | Not applicable — no monetary values in skill artifacts | —                                             |

### RTL Language Support

Not applicable. The skill produces Markdown files rendered by the operator's own Markdown viewer. RTL rendering, if needed, is the viewer's responsibility.

### Timezone Handling

All timestamps written by the skill to log files or metadata fields shall use UTC (indicated by `Z` suffix in ISO 8601). No timezone conversion is performed.

---

## 3.7.2 Legal and Regulatory Requirements

### Applicable Regulations

Virtual Team Skill is a developer tooling product that does not process regulated data categories on behalf of end users. The following regulatory frameworks are explicitly **not applicable** to the skill itself:

| Regulation | Applicability  | Reason                                                       |
| ---------- | -------------- | ------------------------------------------------------------ |
| GDPR       | Not applicable | Skill does not process EU personal data; artifacts are local |
| HIPAA      | Not applicable | No healthcare data involved                                  |
| PCI-DSS    | Not applicable | No payment card data; no financial transactions              |
| SOC 2      | Not applicable | No hosted service or customer data processing                |
| WCAG 2.1   | Not applicable | CLI tool, not a web application                              |

**Operator responsibility:** Any system built using Virtual Team Skill's outputs may be subject to applicable regulations. The skill's QA/QC agent's compliance check verifies only the skill's internal process compliance; it does not perform legal compliance review of the operator's product.

### Self-Imposed Security Policies (Policy Requirements, not Legal)

The following policies are enforced by the skill by design and shall be documented as requirements:

**P-01 — No Credential Embedding:** Generated code artifacts must not contain hardcoded credentials, API keys, passwords, tokens, or database connection strings with embedded credentials. See FR-24, FR-27, NFR-20.

**P-02 — Data Locality:** All artifact data stays on the operator's local machine except for LLM inference calls to the Anthropic API. No artifact content is transmitted to any other third-party service. See NFR-05, NFR-19.

**P-03 — No Git Operations:** The skill shall not execute git commands that could cause irreversible remote state changes. See DC-18.

### Intellectual Property

Generated artifacts (user stories, source code, architecture documents, test plans) are produced by AI models. The skill does not assert copyright over generated content. Operators are responsible for reviewing the IP status and licensing implications of AI-generated content in their jurisdiction before using generated code in production.

The skill `.md` files themselves are part of the MySkills repository and subject to that repository's license terms.

### No Cookie or Consent Requirements

Not applicable. Virtual Team Skill is a CLI tool with no web interface, no cookies, no user accounts, and no consent flows.

---

## 3.7.3 Operational Requirements

### Monitoring and Alerting

Virtual Team Skill is a local CLI tool with no hosted component. Consequently:

- No server-side monitoring infrastructure is required or provided
- No automated alerts or paging are produced by the skill
- Operator-level observability is provided through structured CLI progress output with `[Agent]` prefixes

**Log file piping (optional operator practice):**

```
/team "{requirement}" | tee projects/{slug}/pipeline.log
```

This captures full CLI output to a log file for later review. The skill does not require or enforce this practice.

### Logging

| Log type               | Location                                                   | Format                                        | Rotation                                                     |
| ---------------------- | ---------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| Validation failure log | `projects/{slug}/validation-errors/{agent}-attempt-{n}.md` | Markdown — see FR-36 for schema               | Never auto-rotated; permanent                                |
| Flags summary          | `projects/{slug}/flags-summary.md`                         | Markdown aggregate of FLAG-{ROLE}-{n} entries | Overwritten on each full-auto pipeline run for the same slug |
| CLI progress output    | Terminal stdout                                            | `[Agent] ✓/✗ Message` format                  | Session-only; not persisted unless operator pipes to file    |

No structured log format (JSON, NDJSON) is required in v1. Plain Markdown is the canonical log format.

### On-call and Support

Not applicable. Virtual Team Skill is not a hosted service with an SLA. Support is provided through:

- Repository issue tracker (GitHub Issues on the MySkills repository)
- README FAQ section for common operational questions

### Runbook: Common Operational Scenarios

The following scenarios shall be documented in the README or a dedicated runbook file. Format of the runbook (README section vs standalone file) is subject to operator preference — see TBD-11.

| Scenario                                         | Resolution steps                                                                                                                                                |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pipeline hard stop — agent failed 3 retries      | 1. Read `projects/{slug}/validation-errors/{agent}-attempt-3.md`; 2. Note missing sections; 3. Run `/team-{role} --project {slug}` to retry that agent manually |
| Artifact looks wrong — want to re-run one agent  | Run `/team-{role} --project {slug}` to regenerate that agent's artifacts; subsequent artifacts will be overwritten when their agents are re-run                 |
| QA/QC returned REJECTED verdict                  | Read `sign-off.md` for conditions; optionally resolve issues and re-run affected agents; re-run `/team-qa --project {slug}` for a new review                    |
| Want to provide more context to a specific agent | Re-run that agent with `--context "additional instructions"` or `--context ./path/to/context-file.md`                                                           |
| Context window warning from TechLead or QA/QC    | Split project into smaller slug scope; or summarize preceding artifacts manually and pass via `--context`                                                       |

---

## 3.7.4 Transition Requirements

### No Data Migration

Virtual Team Skill is a new tool with no predecessor system. Operators adopting it from scratch do not need to migrate existing data.

### Integration with Existing Workflows

Operators who already use the SRS Workflow skills (sr-brainstorm → sr-spec) can immediately pass SRS artifacts to the BA Agent using the `--srs` flag. No transition steps are required:

```
/team-ba --project {slug} --srs
```

Operators with existing codebases who want context-aware artifact generation can pass existing architecture documents or code snippets via `--context`:

```
/team-techlead --project {slug} --context "./existing-architecture.md"
```

### Cutover Strategy

Not applicable — no existing system is replaced by Virtual Team Skill.

### Rollback Plan

If a skill update causes issues:

1. Operator runs `git log` to identify the prior working commit
2. Operator runs `git checkout {commit-hash} -- .claude/skills/team*.md` (or equivalent) to restore prior skill file versions
3. Existing project artifacts are unaffected — they remain in `projects/{slug}/team/`
4. No database rollback required

**Artifact compatibility across skill versions:** Artifact files from an older skill version remain valid input for a newer skill version, provided the file structure (directory layout, file names) has not changed. Breaking changes to file structure must be documented in the release notes.

---

## 3.7.5 Training Requirements

### Operator Training by Role

| Operator type              | Technical sophistication                                   | Training requirement                                                                                                               |
| -------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Solo Developer (ACTOR-01)  | High — familiar with CLI tools and AI tooling              | README quick-start + command reference sufficient; no formal training needed                                                       |
| Technical Lead (ACTOR-02)  | High — familiar with architecture patterns and Claude Code | README + CLAUDE.md; can self-service from artifact output                                                                          |
| PM / BA Human (ACTOR-03)   | Medium — may not be familiar with Claude Code CLI          | Step-by-step onboarding guide: what Claude Code is, how to install, how to run, how to interpret BA and PM artifacts               |
| Startup Founder (ACTOR-04) | Variable — varies from technical to non-technical          | Clear quick-start guide with exactly one command to run full pipeline, example output, and explanation of what each artifact means |

### Required Documentation for v1

| Document            | Contents                                                                                                                                        | Priority                             |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `README.md`         | Prerequisites, installation, quick-start (full pipeline), per-agent usage, artifact directory structure, FAQ (runbook), command reference table | P0 — required for v1 release         |
| `CLAUDE.md`         | Project context for Claude Code sessions in the MySkills repository; contributor setup                                                          | P1 — required for skill contributors |
| Inline command help | Behavior under TBD-09 resolution — feasibility of `--help` flag in Claude Code skill format to be confirmed during implementation               | P2 — implement if feasible           |

### Developer Documentation for Skill Contributors

| Document                   | Contents                                                                                                              |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Skill file authoring guide | How validation schemas are defined, how agent prompts are structured, how to add a new agent role, naming conventions |
| Contribution guide         | Branching strategy (`feat/{name}`), PR process, how to test a skill change end-to-end, PR template                    |
| Architecture overview      | Orchestrator → role agent → sub-agent flow; context chain mechanism; artifact file paths and dependency map           |

### AI-Assisted Onboarding (Built-in Advantage)

Because operators use Claude Code, they can ask Claude directly to explain any artifact generated by the skill within the same conversation. This significantly reduces the training burden for artifact interpretation — operators do not need external documentation to understand a generated `architecture.md` or `test-plan.md`. README documentation should highlight this capability for ACTOR-03 and ACTOR-04 audiences.
