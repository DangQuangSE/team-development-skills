# Post-Processing Guide

Manual steps only — this skill never executes image processing itself. Use these when the checklist flags a technical miss.

## Background not actually transparent

**Symptom**: chat tool returned the subject on a white/black/flat background instead of true alpha transparency.

**Steps**:
1. Free option: upload the image to remove.bg (or a similar free background-removal web tool) — works well when the background is a flat, uniform color as instructed in the prompt.
2. Free/offline option: open in GIMP → Select → By Color, click the flat background, Delete, then export as PNG (keeps alpha channel).
3. Check the result for a color "halo" around the subject edge (common with light-colored subjects on white backgrounds) — if present, use GIMP's Select → Shrink by 1-2px before deleting, or manually erase the fringe with the eraser tool at 100% zoom.

**Expected end state**: PNG with real alpha channel, subject fully isolated, no color halo at the edges.

## Wrong aspect ratio/dimensions

**Symptom**: returned image isn't the exact size specified in the prompt (icon not square, sprite not matching bible default, background not matching target resolution).

**Steps**:
1. Open in any free image editor (GIMP, Photopea, Paint.NET).
2. Image → Canvas Size (not Image Size, to avoid stretching) to crop/pad to the exact target dimensions, keeping the subject centered.
3. If the subject itself is the wrong proportions (not just the canvas), use Image → Scale Image instead, then re-check it still reads clearly at the target size.

**Expected end state**: exact target dimensions from the bible/template, subject not stretched or distorted.

## Not power-of-2 / not matching engine's expected tile size

**Symptom**: dimensions aren't a power of 2 (e.g. 100x100 instead of 128x128), or don't match the game engine's expected tile grid.

**Steps**:
1. Open in any free image editor.
2. Image → Scale Image to the nearest power-of-2 or engine-expected size (e.g. 64, 128, 256, 512).
3. For pixel-art styles, use nearest-neighbor/no-interpolation scaling to avoid blurring; for painterly styles, standard bicubic scaling is fine.

**Expected end state**: dimensions confirmed as an exact power-of-2 (or the exact tile size the engine expects), no visible blur from scaling if pixel-art.

## When Post-Processing Isn't Enough

Some chat-tool outputs can't be fully fixed this way — e.g. a model that keeps injecting scene background or shadow no matter how the prompt is worded, so no clean isolation is possible. If you've tried the steps above and the result still doesn't meet spec:

1. **Try a different chat tool** — Gemini, ChatGPT, and Claude chat differ in how strictly they follow isolation/technical instructions; a prompt that fails in one may work in another.
2. **Relax the isolation constraint** — accept a wider scene with some background context, then crop/mask by hand in a free editor even if the result is imperfect, rather than fighting the model for a perfect isolated cutout.
3. **Simplify competing constraints** — drop one technical ask from the prompt (e.g. don't demand exact size in the same request) and fix that one thing in post-processing instead of asking the model to nail everything simultaneously.

This is documented guidance only — no new automation is added to the skill for this case.
