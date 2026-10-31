---
name: brand-templates
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for social media assets and video thumbnails. Trigger on: "social carousel",
  "LinkedIn carousel", "Instagram carousel", "case study post", "video thumb", "video thumbnail",
  "youtube thumbnail", "thumbnail for a video", "social template", "Instagram post", "LinkedIn
  post", "brand template", "brand starter".

---

# Brand templates

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

---

## Reference file

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"
```

---

## Routing

Both templates are self-contained HTML editors — no hosting, no server, no upload. They run
entirely client-side in a browser (Canvas 2D rendering with embedded brand fonts and logo).

| Request signal | Template | Path |
|---|---|---|
| social carousel, LinkedIn/Instagram/TikTok post, case study post | social-carousel | `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/social-carousel/editor.html` |
| video thumbnail, YouTube thumbnail, video cover | video-thumb | `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/video-thumb/editor.html` |

**Open the editor file for the user** (or tell them the path to open locally — it's a plain HTML
file, works via `file://` with no server). The editor has form fields for layout type, eyebrow,
title, and body copy — pre-fill guidance in chat if you know the content, but the user fills and
exports interactively (export happens client-side, there's no way to hand back a finished PNG
without the user clicking Export in the browser).

**Social carousel** exports at 1080×1350 (4:5, the primary format across IG/LinkedIn/TikTok per
`brand.md`'s Social canvas specs), with layout options: cover/title, bullet list, stat callout,
quote. Each export is a single slide — for a multi-page carousel, the user fills and exports each
page in turn, cycling through layouts.

**Video thumbnail** exports at 1920×1080, with eyebrow/title/subtitle fields.

Tell the user to wrap 2-4 word phrases in `*asterisks*` in the text fields to get the Cormorant
Garamond italic emphasis voice.

---

## Fallback: when no template matches

If the request is for a social/brand asset type not covered by the two templates above (e.g. a
LinkedIn single-image post, an Instagram Story), generate a brand-compliant starter using
`brand.md`'s tokens directly — dark canvas, one accent color, correct fonts, restrained layout.
Use the dimension table in `brand.md`'s "Social canvas specs" section for the target platform.

Never use colors, fonts, or styles not in `brand.md`.
