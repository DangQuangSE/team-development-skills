# Spec: SRS Skill — Requirement Analysis & IEEE 830 Generation

**Date:** 2026-06-14
**Status:** Draft

---

## Problem Statement

BA/PM nhận yêu cầu thô từ client (email, chat, bullet list) và mất nhiều thời gian chuẩn hóa thành SRS cho dev team. Skill này tự động phân tích input, phát hiện gap/ambiguity, hỏi làm rõ theo priority, rồi generate IEEE 830 SRS hoàn chỉnh.

---

## User Stories

- **[P1]** As BA/PM, I want to paste raw client requirements (email/chat/bullets/PRD) so the skill detects input type and extracts actors, features, and constraints automatically.
  Accepted when: skill identifies ≥ 1 actor, ≥ 3 functional requirements, and ≥ 1 constraint from a typical 200-word client email.

- **[P1]** As BA/PM, I want the skill to detect ambiguities and gaps before generating SRS so I don't write a spec full of holes.
  Accepted when: skill flags ambiguous verbs (should/might/easy/fast/many), undefined actors, missing scope boundary, and missing non-functional requirements.

- **[P1]** As BA/PM, I want to answer P1 clarifying questions (scope/actors) first, then P2 (functional details), then P3 (non-functional), so the process is guided and not overwhelming.
  Accepted when: each batch has ≤ 7 questions; P1 is asked before P2 is shown; P3 is optional if user signals "enough."

- **[P1]** As BA/PM, I want to receive a complete IEEE 830 SRS as a markdown file after clarification is done.
  Accepted when: SRS contains all 6 sections (§1–§3 + appendix), all FRs are numbered (FR-01…), saved to `docs/srs-{slug}-{date}.md`.

- **[P2]** As BA/PM, I want the skill to output a glossary of domain terms found in the input so dev team has shared vocabulary.
  Accepted when: glossary appears as appendix with ≥ 3 terms defined if input contains domain-specific nouns.

- **[P2]** As BA/PM, I want to skip P3 questions if I'm in a hurry and get a draft SRS with `[TBD]` placeholders for non-functional requirements.
  Accepted when: user says "skip P3" → SRS generated with NFR section marked `[TBD - fill before sprint planning]`.

- **[P3]** _(out of scope — Jira/Confluence integration for future)_

---

## Functional Requirements

1. **FR-01** Input detection: identify input type — (a) raw chat/email prose, (b) bullet list, (c) partial PRD. Adjust extraction strategy per type.
2. **FR-02** Actor extraction: identify all named and implied actors/stakeholders from input (e.g., "admin", "khách hàng", "hệ thống bên thứ ba").
3. **FR-03** Feature extraction: extract functional requirements as atomic statements ("User can do X").
4. **FR-04** Constraint extraction: identify explicit constraints (tech stack, deadline, compliance, budget).
5. **FR-05** Gap detection — flag the following patterns:
   - Ambiguous verbs: should, might, could, easy, fast, many, some, appropriate, good
   - Undefined actor: pronoun without referent ("they", "user" without definition)
   - Missing scope boundary: no clear "in/out of scope" statement
   - Missing non-functional: no mention of performance, security, or availability
   - Contradictions: two statements that conflict
6. **FR-06** Priority classification of gaps:
   - P1 (blocker): missing scope, undefined primary actor, fundamental feature conflict
   - P2 (important): ambiguous functional requirement, missing edge case
   - P3 (nice-to-have): missing non-functional requirement, undefined secondary actor
7. **FR-07** Clarification phase — priority-gated:
   - Round 1: ask P1 questions (max 7), wait for user answer
   - Round 2: ask P2 questions (max 7), wait for user answer
   - Round 3: ask P3 questions (max 7), user may skip → mark as [TBD]
8. **FR-08** SRS generation in IEEE 830 structure:
   - §1 Introduction: purpose, scope, definitions/acronyms/abbreviations, overview
   - §2 Overall Description: product perspective, product functions, user characteristics, constraints, assumptions
   - §3 Specific Requirements:
     - §3.1 Functional requirements (numbered FR-01…)
     - §3.2 Non-functional requirements (performance, security, availability — numbers not adjectives)
     - §3.3 External interface requirements (UI, API, hardware if applicable)
   - Appendix A: Glossary
   - Appendix B: Open issues (unresolved gaps after clarification)
9. **FR-09** Save SRS to `docs/srs-{project-slug}-{YYYYMMDD}.md` and report file path to user.

---

## Non-Functional Requirements

- **Clarity:** Each question batch ≤ 7 questions; questions are numbered and grouped by category label.
- **Traceability:** Every FR in SRS must map to something stated or clarified by user (no invented requirements).
- **Completeness:** IEEE 830 §1–§3 all populated; `[TBD]` allowed only if user skipped P3 round.
- **Length:** Generated SRS ≥ 500 words for any input with ≥ 5 features.

---

## Success Criteria

- [ ] Gap scanner flags ≥ 3 distinct ambiguity patterns from a 200-word test email
- [ ] Clarification completes in ≤ 3 rounds (P1 → P2 → P3)
- [ ] Generated SRS contains all IEEE 830 sections (§1, §2, §3.1, §3.2, §3.3, Appendix A)
- [ ] All functional requirements numbered FR-01, FR-02… with no gaps in sequence
- [ ] SRS saved as markdown file at correct path

---

## Out of Scope

- Web UI or GUI for the skill
- Jira / Confluence / Notion integration
- Approval workflow or stakeholder sign-off tracking
- Automatic SRS versioning / diff between revisions
- Input via voice transcript (future consideration)

---

## Assumptions

- User provides all raw input in a single message (or follow-up messages if multi-part)
- SRS language follows input language (Vietnamese input → Vietnamese SRS acceptable)
- Team has a `docs/` folder or is OK with skill creating it
- No external API calls needed — skill operates entirely within conversation context

---

## [NEEDS CLARIFICATION]

- [ ] Max questions per clarification batch: 7 assumed — confirm with team
- [ ] Should skill auto-detect project slug from input or ask user to provide it?
- [ ] Is Vietnamese SRS acceptable or must output be English for dev team?
