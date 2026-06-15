# Plan: SRS Generator Skill
Status: ✅ Complete
Date: 2026-06-14
Mode: Fast

## Overview
Build a Claude Code skill (`srs-generator`) that accepts raw client requirement input, detects ambiguities using 6 pattern categories, guides the BA/PM through up to 3 priority-gated clarification rounds, then generates and saves a complete IEEE 830 SRS as a markdown file.

## Phases
- [x] Phase 1: Skill Core — Write SKILL.md with steps 0–7 covering input detection, gap scanning, 3-round priority-gated Q&A (P2 and P3 as separate gated steps), P1 evasion handling, SRS generation, slug fallback, and path-confirmed file save
- [x] Phase 2: SRS Template — Write references/srs-template.md with full IEEE 830 §1–§3 + Appendix A/B skeleton
- [x] Phase 3: Gap Detection Guide — Write references/gap-detection-guide.md with all 7 ambiguity patterns, P1/P2/P3 classification rules, IEEE 830 quality checklist, and worked example

## Research Summary
N/A

## Dependencies
- `.claude/skills/srs-generator/` directory must be created
- `docs/` folder expected at project root at runtime (skill creates it if absent)
- Mirrors structural conventions from `ck-brainstorm` skill (YAML frontmatter, numbered Step headings, `AskUserQuestion` gates, `references/` offload)

## Session Notes
<!-- Updated by cook automatically — do not edit manually -->

**Last active:** 2026-06-14 (current session)
**Phase in progress:** —
**Status:** All 3 phases complete

### Decisions made this session
- Adopted "shall" clause + GWT stub format for FRs (from peterbamuhigire/srs-skills reference)
- Adopted ISO/IEC 25023 Quality Attribute Scenario format for NFRs
- [CONTEXT-GAP] / [GLOSSARY-GAP] / [VERIFIABILITY-FAIL] tag system from reference repo
- Compliance verdict: COMPLIANT / PARTIALLY COMPLIANT / NON-COMPLIANT
- Human review gate before file save
- 7 gap patterns (added Contradictions as Pattern 7)
- IEEE 830 §4.3 quality attribute checklist in gap-detection-guide.md

### Next immediate action
—

## Risks
- HIGH: SKILL.md exceeds 300-line soft limit — Mitigation: all template content and gap-pattern details live in `references/`; SKILL.md contains only behavioral steps. Add line-count checkpoint to Phase 1 success criteria.
- MEDIUM: Gap scanner misses ambiguities in terse bullet-list inputs — Mitigation: gap-detection-guide.md includes realistic 8–12 sentence worked example covering ≥4 pattern types
- LOW: User skips P3 round mid-session leaving NFR section empty — Mitigation: skill marks skipped sections `[TBD - fill before sprint planning]` per FR-07 / P2 story
- NOTED: §2.6 Apportioning of Requirements is IEEE 830 optional and rarely populated in first drafts — collapse into a single optional line under §2.5 in the SRS template
- NOTED: Gap pattern count in spec FR-05 (5 patterns) vs guide (7 patterns) — guide is authoritative; spec to be updated after implementation
