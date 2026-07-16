# srs-skills

[Tiếng Việt](./README.md) · [English](./README.en.md)

AI skill package that generates a complete **Software Requirements Specification (IEEE 830-1998)** from a raw idea to a fully structured, validated document.

Works with Claude Code out of the box. Compatible with Gemini CLI, GitHub Copilot, and any LLM that can follow a markdown instruction file.

## Skill index

| Skill | Role |
|---|---|
| [srs-workflow](./skills/srs-workflow/) | Orchestrates the complete idea-to-handoff pipeline |
| [srs-generator](./skills/srs-generator/) | Quickly generates an SRS from existing requirements |
| [sr-brainstorm](./skills/sr-brainstorm/) | Elicits requirements in five rounds |
| [sr-spec](./skills/sr-spec/) | Consolidates brainstorm results into a spec |
| [sr-plan](./skills/sr-plan/) | Plans every SRS section |
| [sr-generate](./skills/sr-generate/) | Generates the IEEE 830 document set |
| [sr-validate](./skills/sr-validate/) | Validates structure and fixes errors |
| [sr-improve](./skills/sr-improve/) | Builds an improvement backlog |
| [sr-save](./skills/sr-save/) | Saves context for future sessions |

---

## What it does

Turn an idea or topic into a standards-compliant SRS without writing a single word of requirements manually. The pipeline handles structured elicitation, spec writing, plan generation, SRS generation, IEEE 830 validation, and improvement recommendations.

```
Idea / Topic → Brainstorm → Spec → Plan → SRS (multi-file) → Validate → Improve → Save
```

Or, if you already have requirements written down:

```
Existing requirements text → /cl:srs → IEEE 830 SRS
```

---

## Prerequisites

- **Claude Code CLI** installed and configured with a valid Anthropic API key
- **Python 3.8+** in `PATH` (required for validation scripts and optional CLI tools)

No external services beyond the Anthropic API are required.

---

## Installation

**Quickest option — open the folder directly:**

Open `srs-skills/` as your Claude Code workspace. All skills and scripts are immediately available.

**Copy to an existing project:**

```bash
# Quick SRS skill only
cp -r srs-skills/skills/srs-generator <your-project>/skills/srs-generator/

# Full pipeline skill
cp -r srs-skills/skills/srs-workflow <your-project>/skills/srs-workflow/

# Automation scripts (optional)
cp -r srs-skills/scripts <your-project>/
cp -r srs-skills/hooks <your-project>/hooks/
cp srs-skills/settings.json <your-project>/settings.json
```

---

## Choose your workflow

| Situation | Command |
|---|---|
| You have a topic or idea — no requirements written yet | Use the full pipeline below (`/sr:*`) |
| You already have requirements text | `/cl:srs` — jump straight to SRS generation |

---

## Full Pipeline: `/sr:*` commands

Run the steps in order. Each step reads the output of the previous one.

### Step 1 — `/sr:brainstorm`

**Purpose:** Structured requirements elicitation through 5 rounds of targeted questions.

Start with your topic. The AI asks questions with selectable options across 5 rounds:

| Round | Focus |
|---|---|
| 1 | Actors & Users — who uses the system and how |
| 2 | Core Features — what the system must do |
| 3 | Scope — what is IN and explicitly OUT |
| 4 | Tech Constraints + NFR targets — performance, security, platform |
| 5 | Business Rules & Edge Cases — constraints and exceptional flows |

The AI **never guesses** — it asks clarification questions whenever something is unclear. The round closes only when there are no remaining open items.

**Output:** `projects/{slug}/brainstorm.md`

---

### Step 2 — `/sr:spec`

**Purpose:** Translate brainstorm output into a structured prose specification.

Reads `brainstorm.md` and writes a complete spec covering: actors, feature list, business rules, NFR baselines, assumptions, and open items. No word limit — all captured detail is preserved.

**Output:** `projects/{slug}/spec.md`

---

### Step 3 — `/sr:plan`

**Purpose:** Generate a detailed plan for each SRS section before generating the SRS itself.

Reads `spec.md` and creates **12 separate plan files** — one blueprint per SRS section (§1 through §3, Appendix A and B). Each blueprint includes FR stubs, NFR targets, and the structural decisions that will drive generation.

At the end of this step, the AI presents the plan for your review and asks for approval before proceeding to generation.

**Output:** `projects/{slug}/plan/` (12 files)

---

### Step 4 — `/sr:generate`

**Purpose:** Generate the complete SRS document from the approved plan.

Reads the approved plan files and produces a full IEEE 830-compliant SRS with no word limit — it can reach 300+ pages for complex systems. Each section is a separate file for manageability.

**Mandatory rules enforced during generation:**

- Every Functional Requirement uses `The system shall ...` phrasing
- Every FR has a Given / When / Then acceptance criterion
- Every Non-Functional Requirement has a numeric Response Measure (no vague adjectives like "fast" or "secure")

**Output:** `projects/{slug}/srs/` (11 section files + master index)

---

### Step 5 — `/sr:validate`

**Purpose:** Automated IEEE 830 compliance check.

Runs `srs_validator.py` against the entire `srs/` directory and checks:

| Check | What it verifies |
|---|---|
| Required sections | All IEEE 830 mandatory sections are present |
| FR numbering | No gaps in the FR numbering sequence |
| Shall clauses | Every FR contains "shall" phrasing |
| GWT coverage | Every FR has a Given / When / Then criterion |
| NFR targets | All NFRs have numeric response measures |
| Unresolved tags | No `[TBD]` or `[CONTEXT-GAP]` tags remaining |

**Behavior:**
- **ERRORs** — fixed immediately in the current session
- **WARNs** — passed to the next step for consideration

**Verdict:** `COMPLIANT` / `PARTIALLY COMPLIANT` / `NON-COMPLIANT`

---

### Step 6 — `/sr:improve`

**Purpose:** Generate a structured improvement report.

Produces a prioritized improvement report covering: deferred features and why, technical risks identified in the spec, NFR gaps (areas where targets were set but may be unrealistic), FRs that should be split into smaller requirements, and all warnings carried from the validate step.

**Output:** `projects/{slug}/improvement-report.md`

---

### Step 7 — `/sr:save`

**Purpose:** Save a compact project context snapshot for future Claude Code sessions.

Persists the key decisions from the entire pipeline into 6 small files so a new session can reload project context without re-reading the entire SRS.

**Output:** `projects/{slug}/_context/` — 6 files:
- `vision.md` — project goal and actors
- `features.md` — feature list with priorities
- `tech-stack.md` — confirmed technology decisions
- `glossary.md` — domain terms and definitions
- `quality-standards.md` — NFR targets and compliance notes
- `session-notes.md` — open items and decisions made

---

## Quick SRS: `/cl:srs`

Use this when you already have requirements text and want to go straight to an IEEE 830 SRS.

**How it works:**

1. Paste your requirements text (or provide a file reference)
2. The AI scans for 7 types of ambiguity: vague quantifiers, undefined actors, missing error flows, contradictions, unsupported claims, scope creep signals, and testability gaps
3. Clarification questions are asked in priority order — P1 blockers first
4. A single-file IEEE 830-compliant SRS is generated

**When to use `/cl:srs` vs the full pipeline:**

| Use `/cl:srs` | Use `/sr:*` pipeline |
|---|---|
| You have a written requirements doc or brief | You're starting from scratch with only a topic |
| Time-constrained, want a quick output | You want thorough elicitation and a multi-file SRS |
| Internal tool, small scope | Client-facing, academic, or production-grade system |

---

## CLI Scripts (optional)

The `scripts/` directory contains standalone Python tools you can run directly:

```bash
# Scan a requirements text file for gaps before feeding it to the AI
python scripts/gap_scanner.py requirements.txt

# Validate an SRS directory against IEEE 830
python scripts/srs_validator.py --dir projects/{slug}/srs/

# Strict mode — treat WARNs as ERRORs
python scripts/srs_validator.py --dir projects/{slug}/srs/ --strict

# Output as JSON (for CI integration or downstream tooling)
python scripts/srs_validator.py --dir projects/{slug}/srs/ --format json

# Initialize the project scaffold for a new project
python scripts/init_project.py {slug}
```

---

## Output structure

```
projects/{slug}/
├── brainstorm.md              ← Step 1 output — structured Q&A results
├── spec.md                    ← Step 2 output — full specification prose
├── plan/                      ← Step 3 output — 12 section blueprints
│   ├── plan-01-introduction.md
│   ├── plan-02-overall-desc.md
│   └── ... (12 files total)
├── srs/                       ← Step 4 output — full IEEE 830 SRS
│   ├── INDEX.md               ← Master index with section links
│   ├── section-1-introduction.md
│   ├── section-2-overall-description.md
│   ├── section-3-requirements.md
│   └── ... (11 files total)
├── improvement-report.md      ← Step 6 output
└── _context/                  ← Step 7 output — compact session-reload snapshots
    ├── vision.md
    ├── features.md
    ├── tech-stack.md
    ├── glossary.md
    ├── quality-standards.md
    └── session-notes.md
```

---

## Integration with other tools

The skill files are plain Markdown — any LLM that can follow written instructions can use them.

### Claude Code (built-in)

```
skills/srs-generator/SKILL.md  ← /cl:srs
skills/srs-workflow/SKILL.md   ← /cl:srs-flow
```

Skills appear automatically in Claude Code's autocomplete when the workspace is opened.

### Gemini CLI

```bash
cp -r srs-skills/skills/srs-generator .gemini/skills/
cp -r srs-skills/skills/srs-workflow .gemini/skills/
```

Add to `.gemini/system.md`:
```
When the user types @srs: follow .gemini/skills/srs-generator/SKILL.md
When the user types @srs-flow: follow .gemini/skills/srs-workflow/SKILL.md
```

### GitHub Copilot (Workspace Instructions)

Add to `.github/copilot-instructions.md`:
```
For quick SRS from existing requirements, follow: srs-skills/skills/srs-generator/SKILL.md
For full brainstorm-to-SRS pipeline, follow: srs-skills/skills/srs-workflow/SKILL.md
```

### Any other LLM or agent

Load the skill file into the agent's system prompt:

| Goal | Files to load |
|---|---|
| Quick SRS from existing requirements | `skills/srs-generator/SKILL.md` + `references/srs-template.md` + `references/gap-detection-guide.md` |
| Full pipeline from a topic | `skills/srs-workflow/SKILL.md` + both `references/` directories |

No external APIs required. Python scripts are optional enhancements.

### Alias convention across tools

| Tool | Quick SRS | Full pipeline |
|---|---|---|
| Claude Code | `/cl:srs` | `/cl:srs-flow` |
| Gemini CLI | `@srs` | `@srs-flow` |
| GitHub Copilot | `#srs` | `#srs-flow` |
| Custom agent | `!srs` | `!srs-flow` |

---

## Integration with Virtual Team Skill

If you use the [Virtual Team Skill](../virtual-team-skill/README.md), you can feed the generated spec directly to the BA agent:

```
/team-ba --project my-app --level mid --spec projects/my-app/spec.md
```

The BA agent reads `projects/my-app/spec.md` (and `brainstorm.md` if present) instead of asking for a requirement description. This gives the entire team pipeline a precise, validated spec as its starting point.

---

## Command summary

```
Full pipeline (start from idea):
  /sr:brainstorm → /sr:spec → /sr:plan → /sr:generate → /sr:validate → /sr:improve → /sr:save

  or shorthand full pipeline:  /cl:srs-flow

Quick SRS (start from existing requirements text):
  /cl:srs
```
