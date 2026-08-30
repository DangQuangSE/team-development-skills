# Bible Bootstrap Q&A

Ask via `AskUserQuestion`, 1-2 questions per turn, in this order. Field names below match `bible-field-names.md`.

1. **Art Direction** — "Phong cách nghệ thuật chủ đạo?" Options: Pixel art (8/16-bit), Flat vector / cartoon, Painterly / hand-drawn, Low-poly 3D rendered as 2D — plus free text.
2. **Style Reference** — "Có game/tác phẩm nào bạn muốn tham chiếu style không?" Free text (e.g. "SNES JRPG", "Hollow Knight", "Stardew Valley"). If none, allow "không có, chỉ theo mô tả Art Direction ở trên".
   - **Follow-up**: "Bạn có sẵn ảnh mẫu (concept art, reference image, asset cũ) muốn AI bám theo không?" If yes, ask the user to save it inside the project (e.g. `assets/_reference/`) and give the relative path — store it as the optional `Reference Image Path` bible field. A real reference image is stronger signal than any text description (chat tools ground generation on visual fact, not prose interpretation) — when present, every generated prompt must tell the user to attach that image alongside the text prompt in the chat tool, not just describe the style in words.
3. **Palette Hex Codes** — "Bảng màu chủ đạo (2-5 mã hex)?" If the user doesn't have hex codes yet, offer to infer 3 reasonable hex codes from Art Direction + Style Reference and let the user confirm/adjust.
4. **Default Resolution** — "Kích thước mặc định theo từng loại asset?" Suggest sane defaults per asset-type as a starting point (character sprite 64×64 or 128×128, icon 128×128, background 1920×1080 or tileable 32×32/64×64 tile) and let the user override.
5. **View Angle** — "Góc nhìn chuẩn cho toàn bộ asset?" Options: Top-down, Side-scroller front-facing, Isometric, 3/4 view.
6. **Line Weight** — "Kiểu render đường nét?" Options: Crisp pixel outline, Soft painterly edge, No outline (flat shapes), Cel-shaded with hard shadow.

**Field-completion validation**: after all 6 answers are collected, confirm none are empty. If any answer is missing or was skipped, re-ask that specific question — never proceed to write the bible with a gap, since every downstream template substitutes these fields unconditionally.

## Bible file template

Write to `art-style-bible.md` at project root with this exact structure:

```markdown
# Art Style Bible

## Art Direction
{answer 1}

## Style Reference
{answer 2}

## Reference Image Path
{path given in the Style Reference follow-up, or "none" if the user has no reference image}

## Style Anchor Phrase
{derived: "{answer 1}, {answer 2} inspired" — or just "{answer 1}" if answer 2 was "không có"}

## Palette Hex Codes
{answer 3 — list each hex code on its own line}

## Default Resolution
- Character/Sprite: {value}
- Icon/UI/Item: {value}
- Background/Tileset: {value}

## View Angle
{answer 5}

## Line Weight
{answer 6}
```

This structure is the single source `SKILL.md` reads on every subsequent invocation — do not change field headings without updating `bible-field-names.md` and every template that reads them.

## Per-asset reference image (separate from the bible-level one)

Independent of the bible's project-wide `Reference Image Path`, the user may have a reference image for one specific asset only (e.g. "ren cho tôi nhân vật này giống cái concept art này"). When the user mentions or implies they have an image for the current request, tell them to attach it directly in the chat message alongside the generated prompt — this overrides/supplements the bible-level reference for that one asset. Do not ask the user to describe an image they already have in hand; describing it in words throws away the signal the image itself carries.
