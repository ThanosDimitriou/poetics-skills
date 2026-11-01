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

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # social canvas specs, legacy look
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice
```

The two editors still use the **legacy look** (dark canvas, Inter, `#0099FF`); they haven't moved
to the website's design system yet. Their copy follows the current voice all the same.

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

Write the text the way `writing-on-brand-copy.md` says: short plain sentences, no em dashes,
sentence case, no hype. Fill the eyebrow field only when it adds a fact (a date, an event).
Don't use the editors' `*asterisk*` italic emphasis: the italic "inner voice" is retired.

---

## Fallback: when no template matches

If the request is for an asset type the two editors don't cover (a LinkedIn single-image post,
an Instagram Story), build it in the **current** system, `brand-kit/design-system.md`: paper and
ink, Instrument Serif and Inter Tight, a photograph in an aperture, the wordmark, generous space.
Use the dimensions in `brand.md`'s "Social canvas specs" for the platform.

Never use colours, fonts or styles that are in neither file.
