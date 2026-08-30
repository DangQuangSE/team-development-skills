# Bible Field Names

Canonical field names for `art-style-bible.md` and the exact placeholder token each maps to. Every template and checklist file in this skill must use these tokens verbatim — never invent a new spelling.

| Bible field (heading in `art-style-bible.md`) | Placeholder token | Source question |
|---|---|---|
| Art Direction | `[ART_DIRECTION]` | genre/art style, e.g. "pixel art 16-bit", "flat vector", "painterly" |
| Style Reference | `[STYLE_REFERENCE]` | named influence, e.g. "SNES JRPG", "Hollow Knight" |
| Reference Image Path | `[REFERENCE_IMAGE_PATH]` | optional project-relative path to a real reference image the user already has; "none" if absent |
| Style Anchor Phrase | `[STYLE_ANCHOR_PHRASE]` | derived: `{Art Direction}, {Style Reference} inspired` — the exact phrase repeated verbatim in every generated prompt |
| Palette Hex Codes | `[PALETTE_HEX]` | 2-5 hex codes, primary/secondary/accent |
| Default Resolution | `[DEFAULT_RESOLUTION]` | per-asset-type default size/aspect rules |
| View Angle | `[VIEW_ANGLE]` | top-down, side-scroller front-facing, isometric, 3/4 view |
| Line Weight | `[LINE_WEIGHT]` | crisp pixel outline, soft painterly edge, no outline, cel-shaded |

`[STYLE_ANCHOR_PHRASE]` is not asked directly — SKILL.md derives it from Art Direction + Style Reference when writing the bible, so the exact same sentence gets reused everywhere style-locking matters (per-prompt Medium/Style slot, session-level style-lock line).
