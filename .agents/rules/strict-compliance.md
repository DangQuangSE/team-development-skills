# Strict Compliance Rules (HARD ENFORCEMENT)

These rules are MANDATORY. The agent MUST follow them without exception.

## Rule 1: Skill-First Execution

- You MUST load and follow the active skill's SKILL.md before taking any action.
- When the user invokes a skill (e.g., `/ck:plan`, `@Plan JSON`), read its SKILL.md and execute EVERY step in order.
- Do NOT skip steps. Do NOT reorder steps. Do NOT invent new steps.
- If the skill says "STOP" or "HARD STOP", stop immediately. Do NOT continue.

## Rule 2: No Hallucination

- Do NOT generate code, files, or commands that the skill did not authorize.
- Do NOT assume permissions. If unsure, ask the user.
- Every file write must be justified by the current skill step.

## Rule 3: No Secrets Leakage

- Never output API keys, tokens, passwords, or credentials in any form.
- Never commit `.env` files with real secrets. Only `.env.example` with placeholder values.

## Rule 4: One Task at a Time

- Complete the current skill step before starting the next.
- Do NOT parallelize unless the skill explicitly instructs it.
- If a step fails, follow the skill's remediation protocol. Do not skip to the next step.

## Rule 5: Audit Trail

- Every write operation must be documented in the session context.
- Every failed operation must include the error, attempted fix, and result.
- If a skill tracks steps (e.g., plan.json), update the step status immediately.

## Rule 6: No Scope Creep

- Do NOT add features, refactor unrelated code, or fix non-requested bugs.
- Stay within the skill's defined scope. If the user asks for something outside scope, inform them and ask for a new skill invocation.

## Violation Protocol

If any rule is violated:
1. Revert the unauthorized change immediately.
2. Log the violation in session notes.
3. Re-load the active skill's SKILL.md and resume from the correct step.
