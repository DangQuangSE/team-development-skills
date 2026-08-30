# Background/Tileset Prompt Template

For scene-scale art: full backgrounds, parallax layers, or repeating tiles.

## Gather before generating

- Scene/layer description (what it depicts; if part of a parallax set, which layer — e.g. far/mid/near)
- Tileable or not — if tileable, note that edges must align for seamless repeat
- Aspect ratio/resolution, if different from the bible default for backgrounds

If a reference image exists (bible-level `[REFERENCE_IMAGE_PATH]` or a per-asset image the user just provided), skip asking for a text description of appearance — tell the user to attach the image alongside the prompt below instead.

## Prompt anatomy (6-part, fill every slot)

```text
Job: Generate a [background / parallax layer / seamless tile] game environment image.
Subject: [scene description — what's depicted, and which parallax layer if applicable].
Medium/Style: [STYLE_ANCHOR_PHRASE], line weight [LINE_WEIGHT].
Lighting: [lighting mood consistent with ART_DIRECTION and the scene's depth/layer].
Framing: [VIEW_ANGLE], full scene width, no foreground character/subject unless explicitly requested.
Mood/Palette: render the scene using only these colors as actual scene color ([PALETTE_HEX]) — do not display the hex codes, a color chart, swatch strip, or legend anywhere in the image; colors appear only in the scene itself.

Technical spec: [DEFAULT_RESOLUTION — background value]. If tileable: seamless repeating pattern, edges must align on all tiled sides, no visible seams.

Negative constraints: no watermark, no text/logos, no style drift from the described art direction, no foreground character/subject unless requested, no visible tile seams if tileable, no color palette/swatch/chart/legend anywhere in the image.
```

If generating multiple layers/tiles in one session (e.g. a full parallax set): paste `[STYLE_ANCHOR_PHRASE]` once at the start of the chat session instead of repeating the full style description per layer — keep restating which layer/depth each one is, though, since that's what keeps the set coherent.

## After sending

Continue to the post-generation checklist and, if a technical spec is missed, the post-processing guide (`references/post-generation-checklist.md`, `references/post-processing-guide.md`).
