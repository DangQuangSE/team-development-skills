# Brainstorm: AI Skill — Requirement Analysis & SRS Generation

**Date:** 2026-06-14

## Ideas Explored

- **Full auto (no questions)** — parse input, generate SRS immediately. Fast but produces low-quality SRS for ambiguous input. Dismissed.
- **Batch questions** — ask all gaps at once in one message. One round-trip but overwhelming if input is messy. Considered.
- **Priority-gated questions (chosen)** — ask P1 gaps (scope/actors) first, then P2 (functional details), then P3 (non-functional). More rounds but guided and manageable.
- **Iterative draft → refine** — write draft SRS first, then ask. User preferred "ask first, write after."
- **Structured intake form** — walk user through fixed questions regardless of input. Too rigid, ignores what's already in the input.

## User's Direction

Team-internal use: BA/PM receives raw requirements, skill helps standardize into IEEE 830 SRS for dev team.

Input: raw client chat/email, bullet point lists, partial PRD/brief.
Output: IEEE 830 SRS saved as markdown.
Flow: parse input → detect gaps → ask P1 questions → ask P2 questions → ask P3 questions → generate SRS.

User wants the skill to be "thật chi tiết" (very detailed) — thorough gap detection and complete IEEE 830 output.

## Open Questions

- Should skill detect input language and output SRS in same language?
- Max number of questions per P1/P2/P3 batch?
- Should SRS be saved to a specific folder or user-specified path?
- Should skill generate a glossary from domain terms found in input?

## Risks

1. **Ambiguity overload** — if input is very raw, gap list may be huge → too many questions → user fatigue
2. **IEEE 830 rigidity** — strict structure may not fit all team workflows; consider whether §3 sub-sections should be configurable
3. **Context length** — long raw emails + multi-round Q&A + full SRS generation may hit context limits
