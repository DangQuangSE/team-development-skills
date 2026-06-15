# Phase 2: SRS Template

## Goal
Create `references/srs-template.md` — the full IEEE 830-1998 scaffold that SKILL.md populates at generation time. Every heading, placeholder label, FR block structure, NFR Quality Attribute Scenario block, and appendix must be present so the skill produces a complete, standards-conformant document without guessing structure. Not a behavioral file — structure and format only.

## Files to Create / Edit

| Path | Action |
|------|--------|
| `.claude/skills/srs-generator/references/srs-template.md` | Create |

## Step-by-Step Implementation

1. **Write the document header block.**
   ```markdown
   # Software Requirements Specification
   *IEEE 830-1998 Compliant*

   | Field | Value |
   |-------|-------|
   | Project | {project name} |
   | Version | v0.1 — Draft |
   | Date | {YYYY-MM-DD} |
   | Prepared by | {author/role} |
   | Status | Draft → Under Review → Approved |

   > All requirements use "shall" for obligations. "Should" indicates desirable but optional behavior.
   > Quality attributes follow ISO/IEC 25010. NFR metrics follow ISO/IEC 25023 Quality Attribute Scenarios.
   ```

2. **Write §1 Introduction (all 5 subsections).**
   - **§1.1 Purpose** — who the document is for (dev team, QA, stakeholders) and what system it specifies.
   - **§1.2 Scope** — system name + one-paragraph description of what the product does and does not do. Then a mandatory IN / OUT table:
     ```
     | Feature Area | In Scope | Out of Scope |
     |--------------|----------|--------------|
     | {area 1}     | ✓        |              |
     | {area 2}     |          | ✓            |
     ```
     Note: every feature area identified in §3.2 must appear in this table. `[CONTEXT-GAP: out-of-scope boundary not defined]` if table cannot be populated.
   - **§1.3 Definitions, Acronyms, Abbreviations** — refer reader to Appendix A Glossary. List any standard abbreviations inline (IEEE, SRS, FR, NFR, GWT).
   - **§1.4 References** — list: raw input document (type + date), IEEE 830-1998, ISO/IEC 25010, ISO/IEC 25023, any domain standards cited.
   - **§1.5 Overview** — one paragraph explaining how §2 covers overall context and §3 covers specific requirements, with appendices for glossary and open issues.

3. **Write §2 Overall Description (6 subsections).**
   - **§2.1 Product Perspective** — how the system fits into a larger context (standalone, part of suite, replaces existing system). Placeholder for context diagram or external system list.
   - **§2.2 Product Functions** — bulleted summary of the major capabilities (refer to §3.2 for detail). One bullet per functional area.
   - **§2.3 User Characteristics** — one row per identified actor:
     ```
     | Actor | Technical Level | Access Rights | Notes |
     |-------|----------------|---------------|-------|
     | {actor 1} | {beginner/intermediate/expert} | {role permissions} | |
     ```
   - **§2.4 Constraints** — regulatory, technical, resource, platform constraints found during extraction. Numbered list. `[CONTEXT-GAP: no constraints identified]` if none.
   - **§2.5 Assumptions and Dependencies** — numbered list of conditions that must be true for this spec to hold. Include: tech stack assumptions, third-party service availability, data migration assumptions.
   - **§2.6 Apportioning of Requirements** — *(optional)* features deferred to future releases. If none: "No requirements are currently deferred." Populated from P3 gaps and out-of-scope items tagged Optional.

4. **Write §3 Specific Requirements — §3.1 External Interface Requirements.**
   Four sub-subsections, each with a placeholder:
   - **§3.1.1 User Interfaces** — screen/page list, navigation constraints, accessibility standards (WCAG level if applicable).
   - **§3.1.2 Hardware Interfaces** — device targets, sensors, peripheral requirements. `[TBD: ... | owner: ... | resolve-by: ...]` if none mentioned.
   - **§3.1.3 Software Interfaces** — external APIs, SDKs, databases, protocols. One row per integration:
     ```
     | System | Interface Type | Protocol | Auth Method | Notes |
     |--------|---------------|----------|-------------|-------|
     ```
   - **§3.1.4 Communication Interfaces** — network protocols, data formats, encryption requirements.

5. **Write §3.2 Functions (Functional Requirements).** This is the highest-density section. Write one complete example FR block followed by an instruction comment, then leave slots for FR-01 onward:

   ```markdown
   <!-- SKILL: repeat this block for each FR. One "shall" per block. One "When" per GWT. -->

   ### FR-01 [Essential]
   **Requirement:** The system shall {verb} {object} when {condition}.
   **Actor:** {role performing the action}
   **Precondition:** {system state that must be true before this FR applies}
   **Given:** {the initial context or state}
   **When:** {the trigger or user action}
   **Then:** {the externally observable outcome}
   **Source:** [{verbatim location in input or clarification round}]

   > ⚠️ If "Then" outcome is not externally observable: tag [VERIFIABILITY-FAIL: FR-NN]

   ---
   <!-- FR-02 block here -->
   ```

   Include a note: Essential = must ship (MVP); Conditional = nice-to-have; Optional = future release. Mirrors IEEE 830 §4.3.5 ranking.

6. **Write §3.3 Performance Requirements.** Each entry uses Quality Attribute Scenario (ISO/IEC 25023):

   ```markdown
   <!-- SKILL: use this block per performance NFR. Response Measure must be numeric. -->

   ### NFR-01 [Performance — ISO/IEC 25010: Time Behaviour]
   | Attribute | Value |
   |-----------|-------|
   | Source | {who/what triggers the concern} |
   | Stimulus | {the event or load condition} |
   | Environment | {normal / peak / degraded} |
   | Artifact | {system component or endpoint} |
   | Response | {how the system responds} |
   | Response Measure | {numeric threshold — e.g., "p95 latency < 500ms under 1000 concurrent users"} |

   > ⚠️ Vague modifiers (fast, quick, responsive) are not permitted — replace with numeric measure or tag [TBD: ... | owner: ... | resolve-by: ...].
   ```

7. **Write §3.4 Logical Database Requirements.** Data entities, relationships, retention periods, access constraints. If no database was mentioned in input:
   ```
   [TBD: database schema not specified | owner: tech lead | resolve-by: sprint planning]
   ```
   Otherwise: entity list with attributes and cardinality.

8. **Write §3.5 Design Constraints.** Mandatory standards compliance, technology choices, hardware limitations. Numbered list. Reference extracted tech stack constraints from §2.4.

9. **Write §3.6 Software System Attributes.** One QA Scenario block per characteristic. Include all ISO/IEC 25010 characteristics that were resolved during clarification; mark the rest `[TBD]`. Characteristics to cover (in order): Reliability, Availability, Security, Maintainability, Portability.

   For Security, include RBAC and audit logging requirements if the system has user roles. Reference OWASP Top 10 if a web system.

10. **Write §3.7 Other Requirements.** Internationalization, localization, legal, licensing, regulatory. If none mentioned: "No additional requirements identified at this time."

11. **Write Appendix A: Glossary.** Two-column markdown table:
    ```
    | Term | Definition |
    |------|------------|
    | {domain term 1} | {one-sentence definition} |
    ```
    Note: every `[GLOSSARY-GAP: {term}]` tag from §1–§3 must be resolved here before COMPLIANT verdict is possible.

12. **Write Appendix B: Open Issues.** Numbered list:
    ```
    | # | Section | Gap Type | Description | Priority | Status |
    |---|---------|----------|-------------|----------|--------|
    | 1 | §{N.N} | [CONTEXT-GAP / GLOSSARY-GAP / VERIFIABILITY-FAIL / TBD] | {description} | P{1/2/3} | Open |
    ```
    Note: this appendix must be empty (or all items Resolved) before the document is approved for development.

13. **Write Revision History table** at the end:
    ```
    | Version | Date | Author | Change |
    |---------|------|--------|--------|
    | v0.1 | {YYYY-MM-DD} | {author} | Initial draft |
    ```

## Success Criteria
- [spec P1-4] Template provides all IEEE 830-1998 §1–§3 sections + Appendix A/B
- FR block enforces "shall" clause + GWT stubs + Essential/Conditional/Optional tag
- NFR block uses Quality Attribute Scenario format with numeric Response Measure
- §1.2 includes mandatory IN/OUT scope table
- §3.4 Logical Database and §3.7 Other Requirements are present
- `[VERIFIABILITY-FAIL]` placeholder and instructions are visible in §3.2

## Spec Stories Covered
- [P1] IEEE 830 SRS generation story (complete structural scaffold)
- [P2] Glossary of domain terms story (Appendix A with GLOSSARY-GAP instruction)
- [P2] Skip P3 → TBD placeholders story (TBD format shown in §3.3 and §3.6)
