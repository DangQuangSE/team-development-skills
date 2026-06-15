# srs-workflow — Full SRS Workflow (Agent-Agnostic)

**Invocation:** `@srs-workflow` or paste this skill's content as a system prompt.

```
Phase 0  Topic Intake
Phase 1  Deep Brainstorm      ← multi-round, categorized, options-driven
Phase 2  Spec Writing         ← no word limit
Phase 3  Options Gate         ← user chooses next action
Phase 4  Plan Writing         ← 1 .md file per SRS section
Phase 5  User Review          ← iterate until approved
Phase 6  SRS Generation       ← 1 .md file per section, full detail
Phase 7  Auto-Validate        ← scripts/srs_validator.py
Phase 8  Improvement Report
Phase 9  Context Save
```

**Output directory:** `projects/{slug}/`

**Hard rules (enforce throughout):**
- NEVER proceed to next phase without explicit user confirmation
- NEVER guess or assume — if unclear, ask immediately
- NEVER truncate output — files have no word limit (SRS can be 300+ pages)
- ALL questions must have answer options — never open-ended only

**Reference files:**
- `skills/srs-workflow/references/brainstorm-guide.md`
- `skills/srs-workflow/references/plan-structure-guide.md`
- `skills/srs-generator/references/srs-template.md`
- `skills/srs-generator/references/gap-detection-guide.md`

---

## Phase 0 — Topic Intake

Receive the user's topic. Do NOT ask questions yet.

Identify: Domain / Scale signals / Any constraints mentioned.

Echo back:
```
Topic:      {topic}
Domain:     {detected domain}
Scale:      {detected scale or "unknown"}
```

State: "Starting deep brainstorm. I will ask questions by category before writing anything."
Proceed to Phase 1.

---

## Phase 1 — Deep Brainstorm

**Hard rule: Do not proceed to Phase 2 until you can confidently answer ALL of:**
- Who are ALL actors (primary + secondary + external systems)?
- What are ALL core features?
- What are the explicit system boundaries (in scope / out of scope)?
- What are the technical constraints?
- What are the business rules and compliance requirements?

Load `skills/srs-workflow/references/brainstorm-guide.md` for domain-specific questions.

### Round structure

Each round covers ONE question category. Max 5 questions per round.
Present concrete options — never purely open-ended.

**[ASK USER — Round 1 — Actors & Users]**
Ask: primary users, secondary users, admin roles, external systems/APIs.
Present role options with descriptions. Wait for answer before Round 2.

**[ASK USER — Round 2 — Core Features]**
Present domain-derived feature checklist with sub-options for each cluster.
Mark selections as [CONFIRMED]. Infer missing features — ask to confirm or reject.
Wait for answer before Round 3.

**[ASK USER — Round 3 — Scope Boundary]**
Present two-column table: proposed IN scope vs. proposed OUT scope.
Ask user to move items or add new ones.
HARD-BLOCK: never proceed without explicit in/out boundary.
Wait for answer before Round 4.

**[ASK USER — Round 4 — Technical Constraints]**
Ask: tech stack, hosting, integrations, security/compliance standards,
performance targets (with numeric examples), timeline/budget.
Wait for answer before Round 5.

**[ASK USER — Round 5 — Business Rules & Edge Cases]**
Ask: data ownership, roles/permissions model, pricing logic, regulatory requirements,
key failure scenarios.
Wait for answer.

**After Round 5:** Run completeness check:
- Any actor still undefined? → ask NOW
- Any feature with unclear scope? → ask NOW
- Missing NFR baseline? → ask NOW

**[GATE]** Zero open items required to proceed. State: "Brainstorm complete. Proceeding to spec."

---

## Phase 2 — Spec Writing

Write `projects/{slug}/spec.md`. No word limit.

- Every actor: full description, access rights, experience level
- Every feature: stated in user's words + AI-expanded detail
- Every constraint: verbatim + implication
- In/Out scope table: exhaustive
- Business rules: numbered, precise
- NFR targets: numeric where confirmed, [TBD with context] where not

Output: "Spec written: projects/{slug}/spec.md — §1…§N"

Proceed to Phase 3.

---

## Phase 3 — Options Gate

**[ASK USER]**
```
Spec is ready. What would you like to do next?

A) Write plan          → per-section plan files, then review
B) Re-read spec        → show full spec.md for review/editing
C) Adjust brainstorm   → return to Phase 1 for additions/changes
D) Jump to SRS         → skip planning, generate SRS directly (not recommended)
```

Route: B → show spec → return here | C → Phase 1 | D → Phase 6 | A → Phase 4.

---

## Phase 4 — Plan Writing

Load `skills/srs-workflow/references/plan-structure-guide.md`.

Create one plan file per SRS section under `projects/{slug}/plan/`:

```
plan/
  00-overview.md
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

For each file:
- Write full planned content — no word limit
- Include every sub-item, FR stubs with "shall", NFR targets
- Tag: `[NEEDS USER INPUT: {what}]` for anything still unclear

Output a summary table after all files are written:
```
| File | Section | FRs planned | NFRs planned | Open items |
```

Proceed to Phase 5.

---

## Phase 5 — User Review

Show summary table. Then:

**[ASK USER]**
```
Plan is ready for review. What would you like to do?

A) Approve plan → proceed to SRS generation
B) Modify section → which section(s)?
C) Add features → return to Phase 1 Round 2
D) Show full plan file → which file?
```

If modify: update relevant plan file(s) and return to this gate.
**[GATE]** Only proceed to Phase 6 on explicit "Approve plan".

State when approved: "Plan approved. Beginning SRS generation."

---

## Phase 6 — SRS Generation

Generate SRS section by section, each as its own file under `projects/{slug}/srs/`:

```
srs/
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

Load `skills/srs-generator/references/srs-template.md` for each section's format.

**FR format (mandatory):**
```
FR-NN [Essential|Conditional|Optional]
Requirement:  The system shall {verb} {object} when {condition}.
Actor | Precondition | Given | When | Then | Source
```

**NFR format:** ISO/IEC 25023 Quality Attribute Scenario — numeric Response Measure only.

No word limit. Each file must be complete. Total may reach 300+ pages across all files.

Also generate `projects/{slug}/srs/00-master-index.md` linking all section files.

Proceed to Phase 7.

---

## Phase 7 — Auto-Validate

Run:
```bash
python scripts/srs_validator.py --dir projects/{slug}/srs/
```

Output full validation table + summary:
```
Overall: COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT
Errors:   N
Warnings: N
```

Fix all ERRORs immediately. WARN items go to Phase 8 report.

Proceed to Phase 8.

---

## Phase 8 — Improvement Report

Write `projects/{slug}/improvement-report.md`:

- **Deferred features** — out-of-scope items likely to become v2 features
- **Technical risks** — [TBD] NFRs, integration unknowns, compliance gaps
- **Refinement suggestions** — FRs to split further, NFRs needing load-test data
- **Next version candidates** — explicitly deferred features from brainstorm
- **Validation warnings** — WARN items from Phase 7

No word limit. Reference exact FR/NFR IDs and section numbers.

Proceed to Phase 9.

---

## Phase 9 — Context Save

Write `projects/{slug}/_context/`:

```
_context/
  vision.md           ← goals, problem statement, success metrics
  features.md         ← confirmed in/out scope feature list
  tech_stack.md       ← confirmed tech constraints
  glossary.md         ← all defined terms from Appendix A
  quality_standards.md← confirmed NFR numeric targets
  session-notes.md    ← key decisions, open questions, next steps
```

Output final summary:
```
Workflow complete.

Project:    {name}
Location:   projects/{slug}/
SRS files:  {N} section files
FRs:        {total}
NFRs:       {total}
Verdict:    {COMPLIANT | PARTIALLY COMPLIANT}
Open items: {count} (see appendix-b-open-issues.md)

Next step: share projects/{slug}/srs/ with your dev team.
```
