# Brainstorm: virtual-team-skill & srs-skills independence

**Date:** 2026-07-02

## Ideas Explored

- **Keep .claude/ wrapper** — đổi tên thành pack/ hoặc config/. Ít thay đổi nhưng chỉ cosmetic, không giải quyết gốc rễ. Dismissed.
- **Flat pack (Direction A)** — xóa .claude/ wrapper, skills/hooks/settings.json trực tiếp dưới pack root. Cấu trúc tự giải thích, không gây nhầm lẫn.
- **--spec flag generic** — thay --srs bằng --spec <path>, BA đọc bất kỳ markdown nào, tự extract. Format-agnostic.
- **Auto-detect input** — BA tự nhận path hoặc text. Mượt hơn nhưng ambiguous. Dismissed.

## User's Direction

Flat pack + --spec flag. Root .claude ở D:\GitHub\MySkills\.claude giữ nguyên.
Phase 1: sửa skill-pack structure. Phase 2 (sau): sync lại root .claude.

## Open Questions

- settings.json syntax cho skillsDir relative path trong Claude cần verify trước khi implement
- srs-skills/skills/ vs srs-skills/skills/ — cần confirm folder name không đổi

## Risks

1. Claude settings.json có thể không hỗ trợ skillsDir relative path — cần test
2. Hooks ngoài .claude/ có thể cần path update trong settings.json
