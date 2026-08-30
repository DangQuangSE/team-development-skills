# Icon/UI/Item Prompt Template

For a single centered object meant to read clearly at small size: inventory item, skill icon, HUD element, weapon icon, UI button glyph.

## Gather before generating

- Icon subject (what it represents)
- Fixed size, if different from the bible default for icons

If a reference image exists (bible-level `[REFERENCE_IMAGE_PATH]` or a per-asset image the user just provided), skip asking for a text description of appearance — tell the user to attach the image alongside the prompt below instead.

## Prompt anatomy (6-part, fill every slot)

```text
Job: Generate a single game UI icon, one centered object, no scene.
Subject: [icon subject — one clear silhouette, readable at small size].
Medium/Style: [STYLE_ANCHOR_PHRASE], line weight [LINE_WEIGHT].
Lighting: flat/even lighting, minimal or no cast shadow (icons must read clearly at small size).
Framing: centered, orthographic/front-on, object fills most of the frame with small margin.
Mood/Palette: render the subject using only these colors as actual surface color ([PALETTE_HEX]) — do not display the hex codes, a color chart, swatch strip, or legend anywhere in the image; colors appear only on the subject itself.

Technical spec: square [DEFAULT_RESOLUTION — icon value], isolated subject on flat white or black background, no gradient, no shadow (chat tool can't guarantee true alpha — see post-processing guide after generation).

Negative constraints: no watermark, no text/logos, no crop of the main subject, no style drift from the described art direction, no background scene elements, no shadow unless explicitly requested, no additional objects in frame, no color palette/swatch/chart/legend anywhere in the image.
```

If generating multiple icons in one session (e.g. a full weapon or item set): paste `[STYLE_ANCHOR_PHRASE]` once at the start of the chat session instead of repeating the full style description per icon.

## After sending

Continue to the post-generation checklist and, if a technical spec is missed, the post-processing guide (`references/post-generation-checklist.md`, `references/post-processing-guide.md`).
