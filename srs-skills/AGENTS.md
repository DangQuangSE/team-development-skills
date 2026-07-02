# Integration Guide — srs-skills

This package contains agent-agnostic skills. The SKILL.md files use plain markdown instructions
readable by any LLM. No tool-specific syntax is required to follow them.

---

## Claude Code

Mở `srs-skills/` trực tiếp trong Claude Code — skills và hooks được phát hiện tự động từ `settings.json`:

```
srs-skills/
  skills/srs-generator/SKILL.md   ← /cl:srs  (quick SRS from existing reqs)
  skills/srs-workflow/SKILL.md    ← /cl:srs-flow  (full pipeline: brainstorm → SRS)
  skills/srs-generator/references/  ← shared references (srs-template, gap-guide)
  skills/srs-workflow/references/   ← workflow references (brainstorm-guide, plan-structure)
```

| Skill | Invoke | Use when |
|-------|--------|----------|
| `cl:srs` | `/cl:srs` | User already has raw requirements text |
| `cl:srs-flow` | `/cl:srs-flow` | User has only a topic/idea — needs full brainstorm → SRS pipeline |

Copy to another project:

```bash
# Quick SRS skill only
cp -r srs-skills/skills/srs-generator <your-project>/skills/srs-generator/

# Full workflow skill (includes above references)
cp -r srs-skills/skills/srs-workflow <your-project>/skills/srs-workflow/

# Automation scripts
cp -r srs-skills/scripts <your-project>/
cp -r srs-skills/hooks <your-project>/hooks/
cp srs-skills/settings.json <your-project>/settings.json
```

---

## Gemini CLI

```bash
cp -r srs-skills/skills/srs-generator .gemini/skills/
cp -r srs-skills/skills/srs-workflow .gemini/skills/
```

In `.gemini/system.md`:
```
When the user types @srs: follow .gemini/skills/srs-generator/SKILL.md
When the user types @srs-flow: follow .gemini/skills/srs-workflow/SKILL.md
```

---

## GitHub Copilot (Workspace Instructions)

In `.github/copilot-instructions.md`:
```
For quick SRS from existing requirements, follow: srs-skills/skills/srs-generator/SKILL.md
For full brainstorm-to-SRS pipeline, follow: srs-skills/skills/srs-workflow/SKILL.md
```

---

## Any Other LLM / Agent

Load the appropriate SKILL.md into the agent's system prompt:

| Goal | Files to load |
|------|--------------|
| Quick SRS from existing reqs | `skills/srs-generator/SKILL.md` + `references/srs-template.md` + `references/gap-detection-guide.md` |
| Full pipeline from topic | `skills/srs-workflow/SKILL.md` + both reference dirs |

The skills are self-contained — no external APIs required. Python scripts are optional enhancements
(gap_scanner.py, srs_validator.py) callable from Claude hooks or manually from CLI.

---

## Keyword / Alias Convention

| Tool | Skill | Alias |
|------|-------|-------|
| Claude Code | cl:srs | `/cl:srs` |
| Claude Code | cl:srs-flow | `/cl:srs-flow` |
| Gemini CLI | srs-generator | `@srs` |
| Gemini CLI | srs-workflow | `@srs-flow` |
| GitHub Copilot | srs-generator | `#srs` |
| GitHub Copilot | srs-workflow | `#srs-flow` |
| Custom agent | either | `!srs` / `!srs-flow` |
