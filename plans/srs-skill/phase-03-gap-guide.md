# Phase 3: Gap Detection Guide

## Goal
Create `references/gap-detection-guide.md` — the authoritative reference for the gap scanner (Step 2 of SKILL.md). Defines all 7 ambiguity pattern types, P1/P2/P3 classification rules, IEEE 830 quality attribute checklist, and an annotated realistic worked example. Every gap the skill flags must match one of the 7 patterns. Every verdict the skill outputs must pass the quality attribute checklist.

## Files to Create / Edit

| Path | Action |
|------|--------|
| `.claude/skills/srs-generator/references/gap-detection-guide.md` | Create |

## Step-by-Step Implementation

1. **Write the file header and usage note.** Include:
   - One paragraph: this guide is consumed by Step 2 (Gap Scan) of `srs-generator`. Every detected gap must map to one of the 7 patterns below.
   - Output format the skill must use per gap: `[P{1|2|3}] Pattern {N} — {type label}: "{verbatim fragment or description of what is absent}"`
   - Tag reference table:

     | Tag | Meaning | Where it appears in SRS |
     |-----|---------|------------------------|
     | `[CONTEXT-GAP: {desc}]` | Information absent from input | §1–§3, Appendix B |
     | `[GLOSSARY-GAP: {term}]` | Domain term undefined | §1.3 reference, Appendix A |
     | `[VERIFIABILITY-FAIL: {FR-NN}]` | FR outcome not externally observable | §3.2, Appendix B |
     | `[TBD: {condition} \| owner: {role} \| resolve-by: {date}]` | Deferred — must be resolved before approval | Any §3 NFR |

2. **Write Pattern 1: Vague Quantifiers.** Non-numeric scalar applied to a measurable property.
   - Trigger vocabulary: many, few, some, large, small, fast, slow, soon, quickly, appropriate, good, high, low, reasonable, sufficient, minimal, significant.
   - Two annotated examples: one in a requirement ("the system must respond quickly") and one in a constraint ("we need high availability"). Show flag generated for each.
   - Default priority P3. Escalation rule: P2 if the vague term is the only success criterion for a core feature (no other numeric threshold exists).

3. **Write Pattern 2: Weak Modality Verbs.** Modal verbs expressing possibility or desirability rather than obligation.
   - Trigger vocabulary: should, might, could, may, can (permission sense in a requirement).
   - Distinguish from `shall` and `must` which are unambiguous obligations in IEEE 830.
   - Two annotated examples: P2 case ("Users should be able to export reports" — ambiguous functional requirement) and P3 case ("The dashboard could display analytics" — nice-to-have feature).
   - Default P2. Escalation to P1: any `should` on a stated core feature (makes it unimplementably ambiguous per IEEE 830 §4.3.2).

4. **Write Pattern 3: Undefined Actors.** Role label in a requirement with no prior definition, or pronoun without clear antecedent role.
   - Trigger signals: "the user", "they", "it" (system reference), "admin" (no access level), "customer" (multi-persona system), "the system" (multiple systems in scope).
   - Two annotated examples: pronoun case ("It should send a confirmation" — who is "it"?) and role case ("Admin can approve orders" — which admin tier?).
   - Default P1 for primary actor ambiguity (core flows untestable). P2 for secondary actor ambiguity.
   - Instruction: every undefined actor triggers a `[GLOSSARY-GAP: {actor}]` tag during extraction AND a P1/P2 gap entry.

5. **Write Pattern 4: Anaphoric References.** Pronoun or demonstrative whose referent is ambiguous when multiple entities of the same type are in scope.
   - Distinguish from Pattern 3: here the actor is named, but a subsequent pronoun could refer to any of several named entities.
   - Trigger signals: "this", "that", "these", "it", "they", "the former", "the latter", "same", "the above".
   - One annotated example with two possible referents: "The manager approves the invoice; the supplier reviews it and the accountant signs it" — what does each "it" refer to?
   - Default P2. Escalation to P1 if the ambiguous pronoun appears in a transaction, data-flow, ownership, or deletion statement.

6. **Write Pattern 5: Coordination Ambiguity.** Compound noun phrases or conditions where "and"/"or" grouping is unclear.
   - Classic forms: "A and B or C" (scope of "or"), "admins and users with permission" (who needs permission), "create, edit, or delete reports and logs" (does delete apply to both?).
   - One annotated example with both interpretations spelled out explicitly.
   - Default P2. Escalation to P1 if the ambiguity is in an authorization, permission, or deletion rule.

7. **Write Pattern 6: Missing Constraints.** Complete absence of a required constraint class, not a vague statement of one. Five sub-categories to check:
   - **Error handling** — no stated behavior on failure, timeout, or invalid input for a given feature
   - **Concurrency / volume** — no maximum concurrent users, TPS, or data volume stated
   - **Permissions / roles** — feature exists but no role authorized to perform it (or no unauthorized role denied)
   - **Rollback / undo** — destructive operation (delete, publish, payment) with no rollback or confirmation requirement
   - **Non-functional baseline** — no performance, security, or availability targets anywhere in the document

   Priority: P1 for missing error handling on core transactions, missing permissions on any CUD operation, missing rollback on destructive operations. P2 for missing volume/concurrency and missing availability targets. P3 for missing NFR on secondary features.

8. **Write Pattern 7: Contradictions.** Two or more statements that cannot both be true, or that impose mutually exclusive conditions on the same feature.
   - Common forms: feature is "required" in one sentence and "out of scope" in another; role is both granted and denied the same permission; performance target conflicts with hardware constraint.
   - One annotated example: "The system must support 10,000 concurrent users" vs. "The server will be a single shared VM with 2GB RAM."
   - Detection instruction: the skill must compare all extracted FR statements against each other and against stated constraints for logical incompatibility — not just scan for trigger words.
   - Default P1 for contradictions involving core feature, actor permission, or data integrity rule. P2 if contradiction is between a primary and secondary feature (one may simply be out of scope).

9. **Write the Priority Classification Reference table.** Three-column table (Priority | Condition | Action) consolidating rules from all 7 patterns:
   - P1 — gap makes a requirement unimplementable or untestable — must be resolved in Round 1 before any SRS section can be written
   - P2 — gap creates scope risk but a reasonable default could be assumed — resolve in Round 2; if unanswered, document assumed default in SRS and Appendix B
   - P3 — gap is deferrable; implementation team can make autonomous call — offer in Round 3; if skipped, mark `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`

10. **Write IEEE 830 Quality Attribute Checklist.** Table used by SKILL.md after SRS generation to determine compliance verdict. Maps 8 IEEE 830 §4.3 attributes to checks and failure tags:

    | Attribute (§4.3) | What to verify in the SRS | Tag if failing |
    |------------------|--------------------------|----------------|
    | Correct | Each FR traces to `[Source: {input location}]` | `[CONTEXT-GAP: FR-NN has no source]` |
    | Unambiguous | No vague modifiers remain in any FR/NFR statement; one interpretation possible | Pattern 1 or 2 flag |
    | Complete | All actors have ≥1 FR; all FRs have Actor + Precondition + GWT; §1.2 IN/OUT table populated | `[CONTEXT-GAP: ...]` |
    | Consistent | No two FRs contradict; terminology uniform across document | Pattern 7 flag |
    | Ranked | Every FR carries Essential/Conditional/Optional tag | `[CONTEXT-GAP: FR-NN ranking missing]` |
    | Verifiable | Every NFR has numeric Response Measure; FR "Then" is externally observable | `[VERIFIABILITY-FAIL: FR-NN]` |
    | Modifiable | Each requirement is a single atomic "shall" statement; no redundancy | Structural note (no tag) |
    | Traceable | Each FR has unique FR-NN ID; Appendix B links open gaps to their SRS section | Structural note (no tag) |

    Verdict rules:
    - **COMPLIANT**: all 8 checks pass, zero open items in Appendix B
    - **PARTIALLY COMPLIANT**: all sections present but Appendix B has unresolved items
    - **NON-COMPLIANT**: required sections missing or pervasive quality failures across multiple attributes

11. **Write a worked example section.** Provide a realistic 10-sentence client email (English) — write it so it reads like a real client message, not a constructed ambiguity exercise. Then show the complete gap scan output the skill should produce, covering ≥4 distinct pattern types with priority tags and verbatim fragments. This is the calibration anchor for the skill when processing novel inputs.

    Example email must include at minimum: a project name, at least 2 named actors, at least 4 implied features, at least 1 vague quantifier, 1 weak modality verb, 1 undefined actor or anaphoric reference, and 1 missing constraint.

## Success Criteria
- [spec P1-2] All 7 patterns documented with trigger vocabulary, annotated examples, and priority rules
- [spec success] Worked example produces ≥4 pattern detections from realistic 10-sentence input
- Quality attribute checklist maps all 8 IEEE 830 §4.3 attributes to verifiable checks
- Tag reference table (4 tag types) is defined with syntax and destination section
- Priority table is unambiguous: any gap maps to exactly one tier without subjective judgment

## Spec Stories Covered
- [P1] Gap detection story (7 patterns + priority rules + IEEE 830 checklist)
- [P1] Priority-gated clarification story (P1/P2/P3 tiers drive round order in SKILL.md Steps 3–5)
- [P2] Skip P3 story (P3 classification rule and TBD format explicitly defined)
