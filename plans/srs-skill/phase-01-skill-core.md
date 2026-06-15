# Phase 1: Skill Core

## Goal
Create `SKILL.md` — the behavioral instruction file for `srs-generator`. Orchestrates all steps: input detection, structured extraction, gap scanning, 3-round priority-gated clarification, IEEE 830 SRS generation with "shall" clauses and GWT acceptance stubs, compliance verdict, and path-confirmed file save. Stays under 300 lines by delegating template content to `references/srs-template.md` and gap patterns to `references/gap-detection-guide.md`.

## Files to Create / Edit

| Path | Action |
|------|--------|
| `.claude/skills/srs-generator/SKILL.md` | Create |

## Step-by-Step Implementation

1. **Write YAML frontmatter** with these fields:
   ```yaml
   name: srs-generator
   description: >
     Generate IEEE 830 SRS from raw requirements. Use when the user says
     "write SRS", "generate requirements doc", "analyze requirements",
     "I have raw requirements from a client", or pastes an email/chat/PRD.
   user-invocable: true
   metadata:
     use_when: User provides raw client requirements (email, chat, bullets, PRD fragment) to be formalized into IEEE 830 SRS
     do_not_use_when: Requirements already exist in a complete SRS; a more specific upstream skill owns the task
     required_inputs: Raw requirement text in any format
     quality_standards: All FRs use "shall" clauses; all NFRs use numeric thresholds; no content fabricated beyond what user provides
     anti_patterns: >
       Do not invent requirements absent from input — tag as [CONTEXT-GAP].
       Do not use vague adjectives (fast, easy, many) in FR/NFR statements — tag as [VERIFIABILITY-FAIL].
       Do not skip clarification rounds. Do not save without path confirmation.
     outputs: IEEE 830 SRS at docs/srs-{slug}-{YYYYMMDD}.md + compliance verdict
     references: references/srs-template.md, references/gap-detection-guide.md
   ```

2. **Write Step 0 — Receive Input.** Skill reads full input silently (no questions yet), then emits a one-line receipt:
   ```
   Input received: ~{N} words | type: [email prose | bullet list | partial PRD | mixed]
   ```
   Never ask questions at this step.

3. **Write Step 1 — Extract & Classify.** Skill identifies and lists in a structured block:
   - **Actors** — all named and implied stakeholders. For any actor lacking a role definition, append `[GLOSSARY-GAP: {actor}]`.
   - **Features** — each extracted as a pre-numbered item in "Subject can do X" form (FR-01, FR-02…). Note extraction strategy used: prose / bullets / PRD.
   - **Constraints** — technology, deadline, compliance, budget — verbatim fragments only, no paraphrase.
   - **Out-of-Scope signals** — anything the input explicitly excludes or defers. Tag if absent: `[CONTEXT-GAP: no out-of-scope boundary stated]`.
   - **Traceability** — append `[Source: {location in input}]` to each extracted item so every claim traces back.

4. **Write Step 2 — Gap Scan.** Read `references/gap-detection-guide.md`. Run all 7 patterns against extracted items and full input. Output a prioritized gap table:

   | # | Priority | Pattern | Verbatim fragment / missing element |
   |---|----------|---------|-------------------------------------|

   If zero gaps: state explicitly and jump to **SRS Generation**. Otherwise continue to Round 1.

5. **Write Step 3 — Round 1 Clarification (P1 — Blockers).** If P1 gaps exist: compose ≤7 numbered questions. Label batch:
   ```
   Round 1 of 3 — Scope & Actors (P1 — must resolve before writing SRS)
   ```
   Emit `AskUserQuestion` gate. Wait for answers.

   On receipt:
   - Integrate clarifications; strike resolved gaps.
   - If answer is vague or "I don't know": state assumption, tag location in SRS as `[CONTEXT-GAP: {what is missing}]`, add to Appendix B list, continue.
   - BLOCK only if zero actors AND zero scope remain after this round.

   Then proceed to Round 2.

6. **Write Step 4 — Round 2 Clarification (P2 — Functional Details).** If P2 gaps remain: compose ≤7 questions. Label:
   ```
   Round 2 of 3 — Functional Details (P2)
   ```
   Emit `AskUserQuestion` gate. On receipt: integrate; for unanswered P2 gaps, log assumed default in SRS and Appendix B. Then proceed to Round 3.

7. **Write Step 5 — Round 3 Clarification (P3 — Optional).** Present ≤7 questions. Label:
   ```
   Round 3 of 3 — Non-Functional & Secondary Details (P3 — optional)
   Reply 'skip' to use [TBD] placeholders.
   ```
   Emit `AskUserQuestion` gate. On "skip": mark all P3 gaps `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`. Then proceed to **SRS Generation**.

8. **Write SRS Generation step.** Populate the IEEE 830 skeleton from `references/srs-template.md` using all gathered information. Enforce these rules:

   **§1.2 Scope:** Must include an explicit IN / OUT table listing every identified feature area as IN scope or OUT scope. If out-of-scope signals were absent from input, write `[CONTEXT-GAP: no out-of-scope boundary stated]` and add to Appendix B.

   **§3.2 Functional Requirements — FR format:**
   Each FR must use this exact block structure:
   ```
   FR-NN [Essential|Conditional|Optional]
   Requirement: The system shall {verb} {object} when {condition}.
   Actor: {role}
   Precondition: {state that must be true}
   Given: {initial context}
   When: {trigger/action}  ← exactly one When per FR
   Then: {observable outcome}
   Source: [{location in input}]
   ```
   - "shall" is mandatory — never "should", "might", "can"
   - If outcome is not externally observable: tag `[VERIFIABILITY-FAIL: {FR-NN}]` and add to Appendix B
   - Priority: Essential = must ship, Conditional = nice-to-have, Optional = future release

   **§3.3–§3.6 Non-Functional Requirements — NFR format:**
   Each NFR uses Quality Attribute Scenario per ISO/IEC 25023:
   ```
   NFR-NN [{ISO/IEC 25010 characteristic}]
   Source: {who/what triggers the quality concern}
   Stimulus: {the event or load condition}
   Environment: {normal | peak | failure mode}
   Artifact: {the system component affected}
   Response: {the system's measurable behavior}
   Response Measure: {numeric threshold — no adjectives}
   ```
   Unresolved NFR → `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`

   **Tagging rules:**
   - Undefined domain terms → `[GLOSSARY-GAP: {term}]` → feeds Appendix A
   - Missing info → `[CONTEXT-GAP: {description}]` → feeds Appendix B
   - Non-verifiable FR outcome → `[VERIFIABILITY-FAIL: {FR-NN}]` → feeds Appendix B

   **After populating all sections**, run the IEEE 830 quality attribute checklist from `references/gap-detection-guide.md` and output compliance verdict:
   - `COMPLIANT` — all sections present, zero unresolved gaps
   - `PARTIALLY COMPLIANT` — sections present but Appendix B has open items
   - `NON-COMPLIANT` — required sections missing

9. **Write Human Review Gate.** After showing the full SRS and verdict, emit:
   ```
   Review complete. SRS is {verdict}.
   Open issues: {count} (see Appendix B).
   Proceed to save? [Y / n]
   ```
   Wait for explicit confirmation before writing any file.

10. **Write Save & Report step.** On confirmation:
    - Derive slug from product name in §1.2 (lowercase, hyphenated).
    - **Fallback:** if no product name found, ask inline: "What should I name this SRS file? (used as slug)"
    - Assemble path: `docs/srs-{slug}-{YYYYMMDD}.md`
    - Echo resolved **absolute** path: "Saving to `{absolute_path}`…"
    - Create `docs/` if absent, write file, confirm with: "Saved. ✓ {absolute_path}"

## Success Criteria
Mapped from spec.md:

- [spec P1-1] Skill identifies ≥1 actor, ≥3 FRs, ≥1 constraint from a 200-word test email
- [spec P1-2] Gap scanner flags Pattern 1–7 types including ambiguous verbs, undefined actors, missing scope, missing NFRs, contradictions
- [spec P1-3] ≤7 questions per round; P1 completes before P2 shown; P2 before P3; user can skip P3
- [spec P1-4] SRS contains all IEEE 830 sections; FRs use "shall" + GWT; NFRs use QA Scenario; saved at correct path
- [spec P2-2] "skip P3" → valid SRS with `[TBD: ... | owner: ... | resolve-by: ...]` in NFR sections
- Line count ≤ 300 — verify before finalizing SKILL.md

## Spec Stories Covered
- [P1] Input detection and extraction story
- [P1] Gap detection story
- [P1] Priority-gated clarification story
- [P1] IEEE 830 SRS generation and file save story
- [P2] Skip P3 → draft SRS with TBD placeholders story
