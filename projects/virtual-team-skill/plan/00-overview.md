# Plan Overview — Virtual Team Skill
**Project**: virtual-team-skill
**SRS Version**: 1.0
**Date**: 2026-06-16
**Planned by**: sr:plan workflow

---

## System One-Liner

Virtual Team Skill is a set of Claude Code skills that spawns and orchestrates seven specialized AI agents (BA, TechLead, PM, BE Dev, FE Dev, Tester, QA/QC), each producing professional-grade artifacts in a Hybrid Agile + Waterfall lifecycle — enabling a solo operator to receive the output of a full software development team from a single requirement input.

---

## FR Count by Priority

| Priority | Count | FR IDs |
|---|---|---|
| Essential | 36 | FR-01–FR-13, FR-15–FR-19, FR-21–FR-39 |
| Conditional | 6 | FR-14, FR-20, FR-40, FR-41, FR-42 |
| Optional | 0 | — |
| **Total** | **42** | FR-01 → FR-42 |

---

## NFR Count by ISO/IEC 25010 Characteristic

| Characteristic | NFR IDs | Count | Status |
|---|---|---|---|
| Functional Suitability — Completeness | NFR-01 | 1 | Confirmed |
| Reliability — Recoverability | NFR-02 | 1 | Confirmed |
| Functional Suitability — Appropriateness | NFR-03 | 1 | Confirmed |
| Reliability — Fault Tolerance | NFR-04 | 1 | Confirmed |
| Security — Confidentiality | NFR-05 | 1 | Confirmed |
| Security — Integrity | NFR-06 | 1 | Confirmed |
| Portability — Adaptability | NFR-07 | 1 | Confirmed |
| Security — Isolation | NFR-08 | 1 | Confirmed |
| Functional Suitability — Correctness | NFR-09 | 1 | Confirmed |
| Compatibility — Co-existence | NFR-10 | 1 | Confirmed |
| Performance Efficiency — Time Behaviour | NFR-11 | 1 | **[TBD]** |
| Performance Efficiency — Time Behaviour | NFR-12 | 1 | Confirmed |
| **Total** | | **12** | 11 confirmed / 1 TBD |

---

## Plan File List

| File | SRS Section | Est. Size | FRs | NFRs |
|---|---|---|---|---|
| 00-overview.md | Master map | Medium | — | — |
| 01-introduction.md | §1 Introduction | Medium | — | — |
| 02-overall-description.md | §2 Overall Description | Large | — | — |
| 03-01-external-interfaces.md | §3.1 External Interfaces | Medium | — | — |
| 03-02-functional-requirements.md | §3.2 Functional Requirements | Very Large | 42 | — |
| 03-03-performance.md | §3.3 Performance | Medium | — | 12 |
| 03-04-database.md | §3.4 Database | Medium | — | — |
| 03-05-design-constraints.md | §3.5 Design Constraints | Medium | — | — |
| 03-06-system-attributes.md | §3.6 System Attributes | Large | — | — |
| 03-07-other-requirements.md | §3.7 Other Requirements | Small | — | — |
| appendix-a-glossary.md | Appendix A Glossary | Large | — | — |
| appendix-b-open-issues.md | Appendix B Open Issues | Medium | — | — |

---

## Actor Table

| ID | Name | Type | Description | Data Access |
|---|---|---|---|---|
| ACTOR-01 | Solo Developer | Operator | Individual developer using skill as a full team replacement | Full operator |
| ACTOR-02 | Technical Lead / Architect | Operator | Senior dev validating designs, reviewing architectural decisions | Full operator |
| ACTOR-03 | Product Manager / BA (Human) | Operator | PM/BA simulating team estimation and story breakdown | Full operator |
| ACTOR-04 | Startup Founder / Solo Maker | Operator | Solo builder using virtual team to ship product | Full operator |
| ACTOR-05 | BA Agent | Virtual Agent | Analyzes requirements, writes user stories, acceptance criteria, business rules | Read operator input; Write team/ba/ |
| ACTOR-06 | TechLead Agent | Virtual Agent | Designs architecture, selects tech stack, writes ADRs, ERD, sequence diagrams | Read BA artifacts; Write team/techlead/ |
| ACTOR-07 | PM Agent | Virtual Agent | Plans sprints, breaks down tasks, assigns story points, tracks with TodoWrite | Read BA+TechLead artifacts; Write team/pm/ |
| ACTOR-08 | BE Dev Agent | Virtual Agent | Generates backend code (API, schema, migrations, business logic) | Read TechLead+PM artifacts; Write team/be/ |
| ACTOR-09 | FE Dev Agent | Virtual Agent | Generates frontend code (UI, pages, API integration, state management) | Read TechLead+BE artifacts; Write team/fe/ |
| ACTOR-10 | Tester Agent | Virtual Agent | Writes test plan, unit/integration/e2e test cases, bug report template | Read BA+BE+FE artifacts; Write team/tester/ |
| ACTOR-11 | QA/QC Agent | Virtual Agent | Reviews all artifacts, checks quality gates, issues advisory sign-off | Read ALL artifacts; Write team/qa/ |

---

## External Interface Table

| System | Protocol | Direction | Purpose |
|---|---|---|---|
| Anthropic Claude API | HTTP (managed by Claude Code) | Skill → API | LLM inference calls per agent |
| Claude Code TodoWrite | Built-in tool call | PM Agent → TodoWrite | Sprint task tracking in conversation |
| Local file system | File read/write via Read/Write tools | Agents ↔ Disk | All artifact persistence |
| SRS Workflow (`sr-brainstorm`, `sr-spec`) | File read (Markdown) | SRS → BA Agent | Optional: read existing SRS artifacts as BA input |

---

## Key Planning Assumptions

1. Operator has Claude Code CLI installed and configured with valid Anthropic API key.
2. Operator has sufficient Anthropic API quota for 7+ LLM calls per full pipeline run (including Opus calls for TechLead and QA/QC).
3. Each agent can complete its task in a single LLM call plus optional sub-agent calls — no interactive back-and-forth required in full-auto mode.
4. File system artifacts alone are sufficient to carry context between agents — no conversation history sharing is needed.
5. Operator's initial requirement input contains enough information for BA to analyze without interactive clarification; BA will document assumptions rather than blocking.
6. Tech stack selected by TechLead agent is acceptable to operator; operator can provide constraints via `--context` at trigger time.
7. All diagram output uses Mermaid syntax renderable in operator's environment (VS Code, GitHub, Notion).
8. Sub-agents spawned by role agents write their outputs back to the role agent (merged before disk write) — not directly to disk.

---

## Open Items Status

| ID | Description | Status |
|---|---|---|
| TBD-01 | Validation schemas (required headings per artifact) | ✅ RESOLVED — see appendix-b-open-issues.md |
| TBD-02 | Command naming convention | ✅ RESOLVED — `/team-{role}` prefix |
| TBD-03 | Default slug when --project omitted | ✅ RESOLVED — auto-detect from cwd + confirm |
| TBD-04 | BA conflict resolution in full-auto mode | ✅ RESOLVED — SRS takes precedence; document conflict |
| TBD-05 | `--context` parameter format | ✅ RESOLVED — both inline + file path, auto-detect |
| TBD-06 | NFR-11 agent response time baseline | ⏳ Pending — measure after first e2e run |
| TBD-07–12 | Remaining P2/P3 items | ⏳ Pending — non-blocking for SRS generation |
