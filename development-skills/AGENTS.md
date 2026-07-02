# Development Skills — AGENTS.md

## Overview

This package bundles all general-purpose development skills that are not part of `srs-skills` (requirements/SRS) or `virtual-team-skill` (team pipeline). Skills are independent — use any combination.

## Quick Start

Open `development-skills/` in Claude Code. Skills appear in autocomplete.

## Commands

| Command | Description |
|---------|-------------|
| `/backend-mindset` | Backend development guidance |
| `/ck:brainstorm` | Explore solutions before coding |
| `/ck:cook` | Implement from a plan |
| `/ck:fix` | Diagnose and fix bugs |
| `/ck:plan` | Create implementation plans |
| `/code-review` | Request structured code review |
| `/mermaidjs-v11` | Create diagrams |
| `/playwright-skill` | Browser automation |
| `/problem-solving` | Creative problem-solving toolkit |
| `/sequential-thinking` | Structured reasoning |
| `/strategic-compact` | Context window management |

## Copy to Another Project

```bash
cp -r development-skills/skills/* <your-project>/skills/
```

Individual skills can be copied separately:

```bash
cp -r development-skills/skills/ck-plan <your-project>/skills/ck-plan
cp -r development-skills/skills/ck-cook <your-project>/skills/ck-cook
```
