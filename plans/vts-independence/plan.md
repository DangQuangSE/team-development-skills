# Plan: virtual-team-skill & srs-skills — Self-Contained Pack Refactor

**Date:** 2026-07-02
**Spec:** plans/vts-independence/spec.md
**Mode:** Hard (multi-folder move + SKILL.md edits + settings.json path updates)

---

## Phase 1: Restructure virtual-team-skill/

### Step 1.1 — Move skills directory
```
FROM: virtual-team-skill/.claude/skills/*
TO:   virtual-team-skill/skills/*
```
Move each skill folder (team, team-ba, team-dev, team-fe, team-list, team-pm, team-qa, team-techlead, team-test) directly under `virtual-team-skill/skills/`.

### Step 1.2 — Move hooks directory
```
FROM: virtual-team-skill/.claude/hooks/*
TO:   virtual-team-skill/hooks/*
```
Move all Python hook scripts: flag_aggregator.py, level_gate.py, pre_write_validator.py, retry_controller.py.

### Step 1.3 — Move and update settings.json
```
FROM: virtual-team-skill/.claude/settings.json
TO:   virtual-team-skill/settings.json
```
Update hook command paths from `python .claude/hooks/...` → `python hooks/...` (relative to pack root where settings.json lives).

### Step 1.4 — Delete .claude/ directory
Remove `virtual-team-skill/.claude/` entirely after all files migrated.

### Step 1.5 — Update AGENTS.md
- Remove `.claude/` references in directory structure
- Update copy commands to reflect new flat structure
- Update `--srs` → `--spec <path>` in command table

---

## Phase 2: Restructure srs-skills/

### Step 2.1 — Move skills directory
```
FROM: srs-skills/.claude/skills/*
TO:   srs-skills/skills/*
```
Move: sr-brainstorm, sr-generate, sr-improve, sr-plan, sr-save, sr-spec, sr-validate, srs-generator, srs-workflow.

### Step 2.2 — Move hooks directory
```
FROM: srs-skills/.claude/hooks/*
TO:   srs-skills/hooks/*
```
Move: pre_srs.py, post_srs.py.

### Step 2.3 — Move and update settings.json
```
FROM: srs-skills/.claude/settings.json
TO:   srs-skills/settings.json
```
Update hook paths from `python .claude/hooks/...` → `python hooks/...`.

### Step 2.4 — Delete .claude/ directory
Remove `srs-skills/.claude/` entirely.

### Step 2.5 — Update AGENTS.md and README files
- Update copy commands to reflect new flat structure
- Update any `.claude/` path references

---

## Phase 3: Decouple --srs → --spec

### Step 3.1 — Edit team-ba/SKILL.md
- Line 6, 10, 30, 79-88: Replace `--srs` with `--spec <path>`
- Change logic: `--spec {path}` reads any markdown file (not srs-specific format)
- Remove: "Run /sr:spec first" error message
- New logic: read file at `{path}`, extract requirements from any markdown format
- Update Step 1 (Load Requirement Input) to handle generic markdown

### Step 3.2 — Edit team/SKILL.md
- Line 10, 27, 36, 91: Replace `--srs` with `--spec <path>`
- Forward `--spec` to BA agent instead of `--srs`

### Step 3.3 — Update AGENTS.md (virtual-team-skill)
- Command table: `/team "requirement" [--project slug] [--context "..."] [--srs]` → `[--spec <path>]`
- Same for `/team-ba`

---

## Phase 4: Verification

### Step 4.1 — Structural verification
```bash
# No .claude/ remaining
find virtual-team-skill/.claude    # should return nothing
find srs-skills/.claude            # should return nothing

# Skills present
ls virtual-team-skill/skills/      # 9 folders
ls srs-skills/skills/              # 9 folders

# Hooks present
ls virtual-team-skill/hooks/       # 4 files
ls srs-skills/hooks/               # 2 files

# Settings at root
ls virtual-team-skill/settings.json
ls srs-skills/settings.json
```

### Step 4.2 — Content verification
```bash
# No --srs references remaining
grep -r "\-\-srs" virtual-team-skill/skills/
grep -r "\-\-srs" virtual-team-skill/AGENTS.md

# --spec present
grep -r "\-\-spec" virtual-team-skill/skills/team-ba/SKILL.md
grep -r "\-\-spec" virtual-team-skill/skills/team/SKILL.md

# Hook paths updated
grep "python .claude/" virtual-team-skill/settings.json  # should return nothing
grep "python hooks/" virtual-team-skill/settings.json    # should match
```

---

## Execution Order

1. Phase 1 (virtual-team-skill restructure) — independent
2. Phase 2 (srs-skills restructure) — independent, can run parallel with Phase 1
3. Phase 3 (--srs → --spec) — depends on Phase 1 complete
4. Phase 4 (verification) — depends on all phases complete

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| settings.json relative paths may not work outside .claude/ | Test immediately after Phase 1; if fails, fallback to install script that copies into project .claude/ |
| Python hook paths break after move | Verified: hooks use `python .claude/hooks/X.py` → change to `python hooks/X.py` |
| Some team-* SKILL.md files may also reference --srs | Grep all team-*/SKILL.md for --srs during Phase 3 |

---

## Files Modified

| File | Change |
|------|--------|
| `virtual-team-skill/.claude/skills/**` | Moved to `virtual-team-skill/skills/` |
| `virtual-team-skill/.claude/hooks/**` | Moved to `virtual-team-skill/hooks/` |
| `virtual-team-skill/.claude/settings.json` | Moved + paths updated |
| `virtual-team-skill/.claude/` | Deleted |
| `virtual-team-skill/AGENTS.md` | Updated paths + --spec |
| `srs-skills/.claude/skills/**` | Moved to `srs-skills/skills/` |
| `srs-skills/.claude/hooks/**` | Moved to `srs-skills/hooks/` |
| `srs-skills/.claude/settings.json` | Moved + paths updated |
| `srs-skills/.claude/` | Deleted |
| `srs-skills/AGENTS.md` | Updated paths |
| `virtual-team-skill/skills/team-ba/SKILL.md` | --srs → --spec |
| `virtual-team-skill/skills/team/SKILL.md` | --srs → --spec |
| `virtual-team-skill/README.md` | Updated install + --spec docs |
| `virtual-team-skill/README.vi.md` | Updated install + --spec docs |
| `virtual-team-skill/AGENTS.md` | Updated --spec + paths |
| `srs-skills/AGENTS.md` | Updated .claude/ → flat paths |
| `srs-skills/README.md` | Updated copy commands |
| `srs-skills/README.en.md` | Updated copy commands + --spec example |

## Session Notes
<!-- Updated by cook automatically -- do not edit manually -->

**Last active:** 2026-07-02
**Phase in progress:** Flexibility refactor complete
**Status:** All skills updated with --input-dir, --output-dir, graceful fallback, orchestrator resilience.

### Decisions made this session
- HARD STOP in Layer 1 validation (attempt 3/3) kept — internal retry gate, not pipeline killer
- team-list left as-is (read-only utility)
- $INPUT_DIR / $OUTPUT_DIR convention used across all skills for consistency
- --skip-{phase} flags added to orchestrator for non-linear pipeline execution

### Next immediate action
None — feature complete. Ready for Phase 2 (install script, root .claude sync).
