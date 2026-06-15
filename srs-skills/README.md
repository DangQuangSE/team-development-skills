# srs-skills

Agent-agnostic skill package for IEEE 830-1998 Software Requirements Specification generation.

Drop into any AI-powered project — Claude Code, Gemini CLI, GitHub Copilot, or custom agents.

## What it does

1. **Brainstorm** — asks 3 context questions before touching requirements
2. **Extract** — identifies actors, features, constraints, out-of-scope from any raw input
3. **Gap Scan** — detects 7 ambiguity pattern types (vague quantifiers, undefined actors, contradictions, etc.)
4. **Clarify** — priority-gated Q&A rounds (P1 blockers → P2 functional → P3 non-functional)
5. **Generate** — full IEEE 830 SRS with "shall" clauses, GWT acceptance stubs, QA Scenarios
6. **Save** — path-confirmed write to `docs/srs-{slug}-{YYYYMMDD}.md`

## Output quality

- FRs: `"The system shall {verb} {object} when {condition}."` + Given/When/Then stubs
- NFRs: ISO/IEC 25023 Quality Attribute Scenarios (numeric thresholds, no adjectives)
- Tags: `[CONTEXT-GAP]` / `[GLOSSARY-GAP]` / `[VERIFIABILITY-FAIL]` / `[TBD: ... | owner: ... | resolve-by: ...]`
- Verdict: COMPLIANT / PARTIALLY COMPLIANT / NON-COMPLIANT

## Structure

```
srs-skills/
  README.md
  AGENTS.md                                  ← per-tool integration guide
  skills/
    srs-generator/
      SKILL.md                               ← main skill (agent-agnostic)
      references/
        srs-template.md                      ← IEEE 830 §1–§3 + Appendix scaffold
        gap-detection-guide.md               ← 7 patterns + IEEE 830 quality checklist
```

## Quick start

See [AGENTS.md](AGENTS.md) for setup instructions per tool.
