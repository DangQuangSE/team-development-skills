# Spec: virtual-team-skill & srs-skills — Self-Contained Pack Refactor

**Date:** 2026-07-02
**Status:** Ready

---

## Problem Statement

`virtual-team-skill/` và `srs-skills/` hiện nhúng `.claude/` bên trong, khiến chúng trông như "thành phần cần merge vào .claude của project" thay vì standalone pack. `virtual-team-skill` cũng bị ràng buộc bởi format output của `srs-skills` qua `--srs` flag.

---

## User Stories

- **[P1]** As a user, I want `virtual-team-skill/` to have skills/hooks directly at pack root so that the structure is self-explanatory without a `.claude/` wrapper.
  Accepted when: `virtual-team-skill/skills/`, `virtual-team-skill/hooks/` exist; `virtual-team-skill/.claude/` is gone.

- **[P1]** As a user, I want `srs-skills/` to have the same flat structure so that both packs are consistent.
  Accepted when: `srs-skills/skills/`, `srs-skills/hooks/` exist; `srs-skills/.claude/` is gone.

- **[P1]** As a user, I want `virtual-team-skill` to accept `--spec <path>` pointing to any markdown file so that it does not require srs-skills to have run first.
  Accepted when: `/team-ba --project foo --spec path/to/any.md` works; `--srs` flag removed.

- **[P2]** As a user, I want `settings.json` at pack root to correctly declare skillsDir and hooksDir so that Claude picks up skills/hooks from the new locations.
  Accepted when: skills and hooks load correctly after restructure.

---

## Functional Requirements

1. **FR-01:** Move `virtual-team-skill/.claude/skills/*` → `virtual-team-skill/skills/*`
2. **FR-02:** Move `virtual-team-skill/.claude/hooks/*` → `virtual-team-skill/hooks/`
3. **FR-03:** Move `virtual-team-skill/.claude/settings.json` → `virtual-team-skill/settings.json`, update skillsDir/hooksDir paths
4. **FR-04:** Delete `virtual-team-skill/.claude/` after migration
5. **FR-05:** Same FR-01–04 for `srs-skills/`
6. **FR-06:** In `team-ba/SKILL.md` and `team/SKILL.md`: replace `--srs` flag with `--spec <path>`; BA reads any markdown file at that path, extracts requirements without assuming srs-skills format
7. **FR-07:** Update `AGENTS.md`, `README.md`, `README.vi.md` in both packs to reflect new paths and `--spec` flag
8. **FR-08:** Remove all references to "Requires SRS Workflow skills" prerequisite

---

## Non-Functional Requirements

- No functional behavior change to the 7-agent pipeline
- Skills must still be discovered by Claude after restructure
- Hooks must still fire correctly (pre_write_validator, level_gate, flag_aggregator, retry_controller)

---

## Success Criteria

- [ ] `find virtual-team-skill/.claude` returns no results
- [ ] `find srs-skills/.claude` returns no results
- [ ] `virtual-team-skill/skills/` contains 9 skill folders
- [ ] `srs-skills/skills/` contains 9 skill folders
- [ ] `team-ba/SKILL.md` contains `--spec` and zero occurrences of `--srs`
- [ ] `team/SKILL.md` contains `--spec` and zero occurrences of `--srs`
- [ ] README files updated

---

## Out of Scope

- Root `D:\GitHub\MySkills\.claude` — không thay đổi (Phase 2 sau)
- Thêm install script để link vào project khác (Phase 2)
- Thay đổi logic 7-agent pipeline

---

## Assumptions

- Claude `settings.json` hỗ trợ `skillsDir` và `hooksDir` với relative path từ file location
- Không cần thay đổi Python hook scripts — chỉ thay đổi vị trí và settings.json path declarations

---

## [NEEDS CLARIFICATION]

- [ ] Verify: Claude settings.json syntax cho skillsDir/hooksDir khi nằm ngoài .claude/ — cần test sau khi restructure
