# srs-generator — IEEE 830 SRS from Raw Requirements

**Purpose:** Guide any AI agent to analyze raw client requirements, detect ambiguities, clarify gaps, and produce a complete IEEE 830-1998 compliant SRS document.

**Activation keywords:** `srs`, `write srs`, `generate srs`, `analyze requirements`, `I have raw requirements`

**Pipeline:**
```
Brainstorm → Receive Input → Extract → Gap Scan → Clarify (P1→P2→P3) → Generate SRS → Review → Save
```

**References (load before starting):**
- `references/srs-template.md` — IEEE 830 scaffold to populate at generation time
- `references/gap-detection-guide.md` — 7 ambiguity patterns + P1/P2/P3 classification rules

---

## Anti-patterns (NEVER do these)

- Do NOT invent requirements absent from user input — tag as `[CONTEXT-GAP: {description}]`
- Do NOT use vague adjectives (fast, easy, many) in FR/NFR statements — tag as `[VERIFIABILITY-FAIL: {FR-NN}]`
- Do NOT skip clarification rounds
- Do NOT write any file without explicit user confirmation

---

## STEP 0 — Brainstorm Gate

**Do NOT ask for requirements yet.** First understand project context.

**[ASK USER]** — ask these 3 questions together, wait for all answers before proceeding:

```
Before we start, I need to understand the project context:

1. System type: What kind of system is this?
   (Web app / Mobile app / API / Internal tool / SaaS / Desktop / Other)

2. Primary users: Who will use this system?
   (e.g., end customers, internal staff, admins, B2B clients, developers)

3. Core problem: What problem does this system solve? (1–2 sentences)
```

**Use the answers to:**
- Seed §2.1 Product Perspective (system type)
- Seed §2.3 User Characteristics (primary users)
- Frame §1.2 Scope (core problem → system boundary)

**After receiving answers**, prompt:
```
Context noted. Now paste your raw requirements — any format works:
client email, bullet list, chat transcript, PRD draft, voice notes, etc.
```

Wait for raw input, then proceed to STEP 1.

---

## STEP 1 — Receive Input

Read the raw input. Silently identify the input type. Output a one-line receipt:

```
Input received: ~{N} words | type: [email prose | bullet list | partial PRD | mixed]
```

---

## STEP 2 — Extract & Classify

Output a structured extraction block with four sections:

**Actors** — all named and implied stakeholders.
- Tag each undefined role: `[GLOSSARY-GAP: {actor}]`

**Features** — numbered FR-01, FR-02… in "Subject can do X" form.
- Note extraction strategy used: prose / bullets / PRD

**Constraints** — technology, deadline, compliance, budget.
- Verbatim fragments only — no paraphrase

**Out-of-Scope signals** — anything input explicitly excludes or defers.
- If absent: `[CONTEXT-GAP: no out-of-scope boundary stated]`

Append `[Source: {location in input}]` to every extracted item.

---

## STEP 3 — Gap Scan

Load `references/gap-detection-guide.md`. Run all 7 patterns against extracted items and full input.

Output a prioritized gap table:

| # | Priority | Pattern | Verbatim fragment / missing element |
|---|----------|---------|-------------------------------------|
| 1 | P1/P2/P3 | Pattern N — {label} | "{fragment}" |

If zero gaps found: state explicitly, skip to STEP 7 (SRS Generation).

---

## STEP 4 — Round 1 Clarification (P1 — Blockers)

If P1 gaps exist:

**[ASK USER]** — compose up to 7 numbered questions addressing P1 gaps only. Label clearly:

```
Round 1 of 3 — Scope & Actors (P1 — must resolve before writing SRS)

1. {question about scope/actor gap}
2. {question about actor definition}
...
```

Wait for all answers before proceeding.

**On receipt:**
- Integrate clarifications into the extraction from STEP 2
- Strike resolved gaps from the gap table
- For vague/missing answers: state the assumption being used, tag location in SRS as `[CONTEXT-GAP: {what is missing}]`, add to Appendix B
- **BLOCK generation only if zero actors AND zero scope remain after this round**

Proceed to Round 2.

---

## STEP 5 — Round 2 Clarification (P2 — Functional Details)

If P2 gaps remain:

**[ASK USER]** — up to 7 questions. Label:

```
Round 2 of 3 — Functional Details (P2)

1. {question about ambiguous FR}
...
```

Wait for answers. Integrate; for unanswered P2 gaps, log assumed default in SRS and Appendix B.

Proceed to Round 3.

---

## STEP 6 — Round 3 Clarification (P3 — Optional)

**[ASK USER]** — up to 7 P3 questions. Label:

```
Round 3 of 3 — Non-Functional & Secondary Details (P3 — optional)
You can reply 'skip' to use [TBD] placeholders for these.

1. {question about performance/security/availability}
...
```

On "skip": mark all P3 gaps `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`.

Proceed to STEP 7.

---

## STEP 7 — Generate SRS

Load and populate `references/srs-template.md` using all information gathered across STEP 0–STEP 6.

### §1.2 Scope
Must include an explicit IN / OUT table for every identified feature area.
If out-of-scope boundary was never established: `[CONTEXT-GAP: no out-of-scope boundary stated]` → Appendix B.

### §3.2 Functional Requirements
Each FR uses this exact block:

```
FR-NN [Essential|Conditional|Optional]
Requirement:  The system shall {verb} {object} when {condition}.
Actor:        {role performing the action}
Precondition: {state that must be true before this FR applies}
Given:        {initial context}
When:         {trigger — exactly one per FR}
Then:         {externally observable outcome}
Source:       [{location in input or clarification round}]
```

Rules:
- "shall" is mandatory — never "should", "might", "can"
- Non-observable "Then" → tag `[VERIFIABILITY-FAIL: FR-NN]` → Appendix B
- Essential = MVP must-ship | Conditional = nice-to-have | Optional = future release

### §3.3–§3.6 Non-Functional Requirements
Each NFR uses Quality Attribute Scenario (ISO/IEC 25023):

```
NFR-NN [{ISO/IEC 25010 characteristic}]
Source:           {who/what triggers the quality concern}
Stimulus:         {event or load condition}
Environment:      {normal | peak | degraded}
Artifact:         {system component affected}
Response:         {system behavior}
Response Measure: {numeric threshold — no adjectives permitted}
```

Unresolved NFR → `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`

### Tagging rules
| Tag | Trigger | Destination |
|-----|---------|-------------|
| `[GLOSSARY-GAP: {term}]` | Undefined domain term | Appendix A |
| `[CONTEXT-GAP: {desc}]` | Missing information | Appendix B |
| `[VERIFIABILITY-FAIL: {FR-NN}]` | Non-observable FR outcome | Appendix B |
| `[TBD: ... \| owner: ... \| resolve-by: ...]` | Deferred NFR | §3.x inline |

### Quality check
After populating all sections, run the IEEE 830 quality attribute checklist from `references/gap-detection-guide.md`.

Output compliance verdict:
- **COMPLIANT** — all sections present, Appendix B empty or all resolved
- **PARTIALLY COMPLIANT** — sections present but Appendix B has open items
- **NON-COMPLIANT** — required sections missing

---

## STEP 8 — Human Review Gate

Display the full SRS and verdict, then prompt:

```
Review complete. SRS status: {COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT}
Open issues: {count} items in Appendix B.

Proceed to save? [Y / n]
```

**Do NOT write any file until the user confirms.**

---

## STEP 9 — Save

On user confirmation:

1. **Derive slug** from product name in §1.2 (lowercase, hyphenated).
   - Fallback: if no product name found, ask: `"What should I name this SRS file? (used as filename slug)"`

2. **Assemble path:** `docs/srs-{slug}-{YYYYMMDD}.md`

3. **Confirm path** with user before writing: `"Saving to {absolute_path} — confirm?"`

4. Create `docs/` directory if it does not exist.

5. Write file and confirm: `"Saved ✓ {absolute_path}"`
