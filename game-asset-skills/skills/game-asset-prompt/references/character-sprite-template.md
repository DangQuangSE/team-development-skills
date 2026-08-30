# Character/Sprite Prompt Template

For any single-subject animated or posed sprite: character, creature, vehicle, ship — anything that needs one or more consistent frames/poses.

## Gather before generating

- Subject name/description (what it is, if not obvious from context)
- Pose/frame list: which frames are needed (e.g. idle, walk, attack — or for a vehicle: default, banking-left, banking-right, destroyed)
- Any per-subject identifying details that must stay identical across every frame in the set (colors, markings, silhouette, proportions)

If a reference image exists (bible-level `[REFERENCE_IMAGE_PATH]` or a per-asset image the user just provided), skip asking for a text description of appearance — tell the user to attach the image alongside the prompt below instead.

## Prompt anatomy (6-part, fill every slot)

```text
Job: Generate a single [pose/frame name] game sprite, isolated subject, no scene.
Subject: [subject name/description — identifying details repeated verbatim across every frame's prompt in the same set].
Medium/Style: [STYLE_ANCHOR_PHRASE], line weight [LINE_WEIGHT].
Lighting: flat/even lighting consistent with [ART_DIRECTION], no dramatic shadow unless the art direction calls for it.
Framing: [VIEW_ANGLE] — camera-facing, not a side or three-quarter flyby angle unless [VIEW_ANGLE] explicitly says otherwise. Full subject in frame, centered.
Mood/Palette: render the subject using only these colors as actual surface color ([PALETTE_HEX]) — do not display the hex codes, a color chart, swatch strip, or legend anywhere in the image; colors appear only on the subject itself.

Technical spec: [DEFAULT_RESOLUTION — sprite value], isolated subject on flat white or black background, no gradient, no shadow (chat tool can't guarantee true alpha — see post-processing guide after generation).

Negative constraints: no watermark, no text/logos, no crop of the main subject, no style drift from the described art direction, no background scene elements, no additional subjects in frame, no color palette/swatch/chart/legend anywhere in the image.
```

If generating multiple frames/poses for the same subject in one session: paste `[STYLE_ANCHOR_PHRASE]` once at the start of the chat session instead of repeating the full style description in every single frame's prompt — keep repeating the Subject's identifying details every time, though, since that's what keeps the character/vehicle itself consistent across frames.

## After sending

Continue to the post-generation checklist and, if a technical spec is missed, the post-processing guide (`references/post-generation-checklist.md`, `references/post-processing-guide.md`).
