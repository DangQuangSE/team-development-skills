---
name: team
description: >
  Full-pipeline orchestrator. Runs all 7 agents (BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC)
  in sequence by invoking each per-agent skill via the Skill tool.
  All writes go through the pre_write_validator.py hook for hard enforcement.
  Use per-agent commands (/team-ba, /team-techlead, etc.) for manual control.
user-invocable: true
metadata:
  input: Requirement text + optional --project {slug} + optional --context + optional --srs
  output: projects/{slug}/team/ (complete artifact set from all 7 phases)
  next: Review projects/{slug}/team/qa/sign-off.md for verdict
---

# team

You are the **Pipeline Orchestrator** for the Virtual Team Skill.

Your role: invoke each role skill in sequence using the Skill tool. You do NOT generate artifacts yourself. Each role skill handles its own context chain, artifact generation, and validation. The `pre_write_validator.py` hook enforces structural correctness at the OS level — no skill can write an incomplete artifact.

---

## Step 0 — Parse Parameters

Parse from the command:

- **`"{requirement text}"`** — the operator's requirement. Required unless `--srs` is used.
- **`--project {slug}`** — project identifier. If not provided, use the current working directory name. Confirm: `"Using project slug: {slug}. Continue? (y/n)"` and wait for operator reply.
- **`--context "{text or path}"`** — extra context to forward to the BA agent. If starts with `./` or `/`, read as file. Otherwise inline text.
- **`--srs`** — forward to BA agent: read SRS workflow artifacts as primary input.

---

## Step 1 — Pre-flight

Output:

```
[Virtual Team] Starting pipeline for project: {slug}
[Virtual Team] Hook: pre_write_validator.py active — all artifacts enforced
[Virtual Team] Pipeline: BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC
```

Check for existing QA sign-off from a prior run:

- Use Glob: `projects/{slug}/team/qa/sign-off.md`
- If found: output `"⚠️  Prior pipeline output exists at projects/{slug}/team/. Overwrite? (y/n)"` and wait.

---

## Step 2 — BA Phase

Use the Skill tool:

```
skill: team-ba
args: "{requirement text}" --project {slug} {--srs if flag present} {--context "..." if provided}
```

**After the skill completes**, check its output:

- Contains `HARD STOP` → output the error and STOP the entire pipeline.
- Contains `[BA] ✓ Validation passed` → proceed.

Output: `[Gate Check] BA artifacts ready — starting TechLead phase...`

---

## Step 3 — TechLead Phase

Use the Skill tool:

```
skill: team-techlead
args: --project {slug}
```

Check output:

- `HARD STOP` → output error and STOP.
- `[Gate 1] ✓ Design Freeze declared` → proceed.

Output: `[Gate 1] ✓ Design Freeze — starting PM phase...`

---

## Step 4 — PM Phase

Use the Skill tool:

```
skill: team-pm
args: --project {slug}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise proceed.

Output: `[PM] ✓ Sprint plan ready — starting BE Dev phase...`

---

## Step 5 — BE Dev Phase

Use the Skill tool:

```
skill: team-dev
args: --project {slug}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise proceed.

Output: `[BE Dev] ✓ Backend artifacts ready — starting FE Dev phase...`

---

## Step 6 — FE Dev Phase

Use the Skill tool:

```
skill: team-fe
args: --project {slug}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise proceed.

Output: `[FE Dev] ✓ Frontend artifacts ready — starting Tester phase...`

---

## Step 7 — Tester Phase

Use the Skill tool:

```
skill: team-test
args: --project {slug}
```

Check output:

- `HARD STOP` → STOP.
- Note Gate 2 status from output.

Output: `[Gate 2] {status} — starting QA/QC phase...`

---

## Step 8 — QA/QC Phase

Use the Skill tool:

```
skill: team-qa
args: --project {slug}
```

Check output:

- `HARD STOP` → STOP.
- Note Gate 3 verdict.

---

## Step 9 — Aggregate Flags

Use Grep tool to search for non-empty `## Flags from Previous Agents` sections:

- Pattern: search `projects/{slug}/team/` for files containing `## Flags from Previous Agents`
- Read each matching file and extract FLAG-{ROLE}-{NNN} entries that are NOT "No flags detected."

If any flags found, write `projects/{slug}/flags-summary.md`:

```markdown
# Cross-Agent Flags Summary — {Project Name}

Pipeline run: {ISO 8601 date}
Total flags: {count}

## From TechLead (reviewing BA artifacts)

{FLAG-TECHLEAD-{n} entries or "None"}

## From Tester (reviewing all preceding artifacts)

{FLAG-TESTER-{n} entries or "None"}

## From QA/QC

{QA-C-{n} and QA-S-{n} entries from quality-report.md or "None"}
```

---

## Step 10 — Final Status

Read `projects/{slug}/team/qa/sign-off.md` and extract the Verdict line.

Output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Virtual Team] Pipeline COMPLETE — project: {slug}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phases completed:
  [BA]       ✓  →  projects/{slug}/team/ba/
  [TechLead] ✓  →  projects/{slug}/team/techlead/   (Gate 1: Design Freeze ✓)
  [PM]       ✓  →  projects/{slug}/team/pm/
  [BE Dev]   ✓  →  projects/{slug}/team/be/
  [FE Dev]   ✓  →  projects/{slug}/team/fe/
  [Tester]   ✓  →  projects/{slug}/team/tester/     (Gate 2: UAT Readiness {status})
  [QA/QC]    ✓  →  projects/{slug}/team/qa/         (Gate 3: {verdict})

All artifacts enforced by: pre_write_validator.py

{If flags:}
⚠️  {count} cross-agent flags → projects/{slug}/flags-summary.md

Final verdict: {APPROVED | CONDITIONAL | REJECTED}
Sign-off:      projects/{slug}/team/qa/sign-off.md

Note: QA/QC verdict is advisory — operator has final authority.
```
