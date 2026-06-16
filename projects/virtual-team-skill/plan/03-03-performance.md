# Plan: §3.3 Performance Requirements — Virtual Team Skill

**Total NFRs: 12 (11 Confirmed / 1 [TBD])**

---

## NFR Table — ISO/IEC 25010 Quality Attribute Scenarios

| NFR-ID | ISO 25010 Characteristic | Quality Attribute Scenario | Status |
|---|---|---|---|
| NFR-01 | Functional Suitability — Completeness | **Stimulus**: Any agent writes its artifact set to disk. **Response**: Validation Layer 1 confirms all required section headings are present in every artifact file. **Measure**: 100% of artifacts must pass structural completeness validation before the next agent is spawned; zero artifacts with missing required sections may be passed forward. | Confirmed |
| NFR-02 | Reliability — Recoverability | **Stimulus**: Claude Code session is interrupted or restarted at any point in the pipeline. **Response**: System reads existing artifacts from disk and allows operator to resume from the last completed phase. **Measure**: 100% of completed artifacts survive a session restart; 0 loss of previously-generated artifact content. | Confirmed |
| NFR-03 | Functional Suitability — Appropriateness | **Stimulus**: An agent generates an artifact. **Response**: Artifact content is complete and detailed — not truncated due to output limits or formatting constraints. **Measure**: No artificial word limit or size cap is imposed on any artifact; content depth is bounded only by the underlying LLM's output capacity. | Confirmed |
| NFR-04 | Reliability — Fault Tolerance | **Stimulus**: An agent produces an artifact that fails structural validation. **Response**: System automatically retries the agent with an augmented prompt. **Measure**: System retries automatically up to 3 times before issuing a hard stop; no human intervention required for attempts 1 and 2; hard stop on attempt 3 with a detailed failure report. | Confirmed |
| NFR-05 | Security — Confidentiality | **Stimulus**: Any project artifact or requirement text is processed by an agent. **Response**: The data transits only through Anthropic Claude API; no third-party service receives project data. **Measure**: Zero external API calls made by the skill beyond Anthropic API; zero artifact content uploaded to any service other than Anthropic. | Confirmed |
| NFR-06 | Security — Integrity | **Stimulus**: BE Dev or FE Dev agent generates code artifacts. **Response**: Generated code contains no hardcoded credentials, API keys, tokens, passwords, or connection strings. **Measure**: Zero hardcoded secrets in any generated code file; all secrets use environment variable references; QA/QC review confirms zero violations. | Confirmed |
| NFR-07 | Portability — Adaptability | **Stimulus**: Operator installs and runs the skill on different operating systems. **Response**: Skill executes correctly without OS-specific modifications. **Measure**: 100% functional on Windows 10/11, macOS 12+, Ubuntu 20.04+; no OS-specific file path hardcoding; all paths use cross-platform conventions. | Confirmed |
| NFR-08 | Security — Isolation | **Stimulus**: Operator runs pipeline for two different projects (slug A and slug B) in the same workspace. **Response**: Each project's artifacts are fully isolated in their respective slug directories. **Measure**: Zero artifact files shared between `projects/{slug-A}/` and `projects/{slug-B}/`; zero cross-project context leakage; agent for project A cannot read or write project B's files. | Confirmed |
| NFR-09 | Functional Suitability — Correctness | **Stimulus**: Any role agent spawns a sub-agent to perform a deep-dive sub-task. **Response**: The spawned sub-agent completes its task and does not itself spawn further agents. **Measure**: Sub-agent depth never exceeds 2 levels (role agent → sub-agent); zero cases where a sub-agent invokes the Agent tool to spawn another agent. | Confirmed |
| NFR-10 | Compatibility — Co-existence | **Stimulus**: Virtual Team Skill is installed and invoked within the same Claude Code workspace as other skills (e.g., SRS workflow skills). **Response**: No conflicts, namespace collisions, or interference with other skills. **Measure**: 100% functional co-existence with existing skills; skill command names do not conflict with any existing skill commands in the repository. | Confirmed |
| NFR-11 | Performance Efficiency — Time Behaviour | **Stimulus**: Operator invokes full-auto pipeline (`/team`) for a typical medium-complexity requirement. **Response**: All 7 agents complete and artifacts are written. **Measure**: [TBD — no timeout enforced per operator decision; typical wall-clock time to be measured after first e2e test run. Baseline hypothesis: 5–20 minutes for full pipeline depending on Opus model response time for TechLead and QA/QC. Operator expectation: < 15 minutes for medium requirements] | **[TBD: Measure in first e2e test run — owner: implementation team — resolve-by: after first full pipeline execution]** |
| NFR-12 | Performance Efficiency — Time Behaviour | **Stimulus**: Structural validation runs on a completed artifact set (Layer 1 check). **Response**: Validation parses artifact files and checks for required headings. **Measure**: Validation check completes in < 5 seconds per artifact; this is a local file read operation with regex heading detection — no LLM call involved. | Confirmed |

---

## Performance Notes by Category

### Response Time
- **Per-agent response time**: Not bounded by an enforced timeout (operator chose unlimited depth/time). Expected times by model:
  - `claude-haiku-4-5` (PM Agent): Typically 15–60 seconds
  - `claude-sonnet-4-6` (BA, BE Dev, FE Dev, Tester): Typically 30–120 seconds
  - `claude-opus-4-8` (TechLead, QA/QC): Typically 60–180 seconds
  - Sub-agents add additional time proportionally
- **Validation time**: < 5 seconds (NFR-12, local read + regex match)
- **Total pipeline time**: Sum of individual agent times + validation time; no hard cap

### Throughput
- **Concurrent pipelines**: Not supported in v1 — one pipeline per Claude Code session
- **Concurrent projects**: Multiple projects can exist in the file system but only one pipeline runs at a time per session
- **Sub-agent concurrency**: Sub-agents within a single role agent run sequentially (Claude Code Agent tool is synchronous within a single agent context)

### Availability
- Availability is determined by Anthropic API uptime — not controlled by this skill
- Skill itself has no server-side component; availability depends entirely on: (1) Anthropic API, (2) operator's local machine, (3) Claude Code CLI

### Data Capacity
- **Artifact file size**: Unbounded (NFR-03) — no size cap enforced
- **Context window consideration**: TechLead and QA/QC agents that read all preceding artifacts may approach context window limits for very large projects; recommended mitigation: use SRS workflow to pre-structure requirements before feeding to Virtual Team; [NEEDS USER INPUT: define context-window warning threshold — see OI from 03-01]
- **Number of projects**: Unlimited — bounded only by operator's local disk space

### Scalability
- v1 is not designed for horizontal scaling — it is a local tool
- Growth expectation: number of artifacts and file sizes grow linearly with project complexity
- No auto-scaling component; all computation is LLM inference via Anthropic API
