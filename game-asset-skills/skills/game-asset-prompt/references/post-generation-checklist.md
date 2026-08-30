# Post-Generation Checklist

Run through all five after the chat tool returns an image, before accepting the asset.

1. **Size** — does the image match the technical spec sent in the prompt (icon: square fixed size; sprite: bible sprite default; background: bible background default / tile size)? If not → post-processing guide, "Wrong aspect ratio/dimensions".
2. **Background** — for icon/sprite: is the subject isolated on a flat background with no gradient/shadow (ready to key out)? For background/tileset: does the scene composition match what was asked (no unwanted foreground subject)? If not → post-processing guide, "Background not actually transparent".
3. **Palette** — do the colors visibly match `[PALETTE_HEX]`? Flag any visible saturation/brightness shift. If drifted → try again with palette hex codes repeated more explicitly, or accept if the shift is minor and consistent with other approved assets.
4. **Pose/Angle** — does the result match the Framing instruction sent (view angle, centered, orthographic/front-on as applicable)? If not → two-turn fallback (see below), or regenerate with stronger Framing language.
5. **Style** — does the overall look match `[STYLE_ANCHOR_PHRASE]` and, if used, the reference image? If not → check whether the style anchor phrase was actually included in the prompt sent; if it was and still drifted, consider the P2 bible-drift flow.

## If only a technical criterion failed (size/background) but style/pose passed

Don't regenerate from scratch. Send a narrow follow-up in the same chat turn asking only for that one fix (e.g. "same image, but on a plain white background" or "same image, resized to exactly 128x128"). This converges faster than a full re-prompt.

## If you have a reference image and the result still doesn't match it

Confirm the reference image was actually attached in the chat message, not just described — some chat tools ignore images that weren't attached to the specific turn. Re-attach and resend if needed.

## If nothing above resolves it

See "When Post-Processing Isn't Enough" in `references/post-processing-guide.md`.
