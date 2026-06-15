# Integration Guide — srs-skills

This package contains agent-agnostic skills. The SKILL.md files use plain markdown instructions
readable by any LLM. No tool-specific syntax is required to follow them.

---

## Claude Code

`srs-skills` có sẵn `.claude/` tích hợp — dùng ngay khi mở folder này trong Claude Code:

```
srs-skills/
  .claude/skills/srs-generator/SKILL.md   ← tự động được pick up
  skills/srs-generator/references/        ← shared references
```

Invoke bằng: `/cl:srs`

Hoặc copy vào project khác:

```bash
cp -r srs-skills/.claude/skills/srs-generator <your-project>/.claude/skills/
cp -r srs-skills/skills/srs-generator/references <your-project>/.claude/skills/srs-generator/
```

---

## Gemini CLI

Add the skill directory to your project and reference it in the Gemini system prompt or config:

```bash
cp -r srs-skills/skills/srs-generator .gemini/skills/
```

In `.gemini/system.md` (or equivalent):
```
When the user types @srs or "generate srs", load and follow:
.gemini/skills/srs-generator/SKILL.md
```

---

## GitHub Copilot (Workspace Instructions)

Copy skill content into your `.github/copilot-instructions.md` or a custom instruction file:

```bash
# Or reference the file directly in Copilot settings
```

In `.github/copilot-instructions.md`:
```
When asked to generate an SRS or analyze requirements, follow the instructions in:
srs-skills/skills/srs-generator/SKILL.md
```

---

## Any Other LLM / Agent

1. Load `skills/srs-generator/SKILL.md` into the agent's context or system prompt
2. Also load `skills/srs-generator/references/srs-template.md` and `references/gap-detection-guide.md`
3. The skill is self-contained — no external APIs or tool calls required

**Activation:** teach the agent to trigger on keywords listed at the top of SKILL.md:
`srs`, `write srs`, `generate srs`, `analyze requirements`, `I have raw requirements`

---

## Keyword / Alias Convention

| Tool | Config location | Example alias |
|------|----------------|---------------|
| Claude Code | SKILL.md `name:` frontmatter | `/cl:srs` |
| Gemini CLI | system prompt | `@srs` |
| GitHub Copilot | copilot-instructions.md | `#srs` |
| Custom agent | system prompt / router | `!srs` |
