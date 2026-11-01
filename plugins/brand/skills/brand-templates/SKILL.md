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

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"                  # the look (the editors apply it)
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # social canvas specs
```

## The two editors

Self-contained HTML files: open them in a browser (double-click works, no server, nothing is
uploaded). They draw in the website's design system (paper and ink, light or dark, Instrument
Serif and Inter Tight, photographs in rounded frames, the wordmark), preview live, check the copy
as you type, and export a PNG.

| Request | Editor | Path |
|---|---|---|
| Instagram, LinkedIn or TikTok post or carousel, story | Social post | `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/social-carousel/editor.html` |
| YouTube thumbnail, video cover | Video thumbnail | `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/video-thumb/editor.html` |

**Social post**: formats 4:5 (feed and carousels, the default), 1:1, 9:16 (stories, keeping clear
of the app's interface). Layouts mirror the deck's page templates:

| Layout | Use it for |
|---|---|
| Cover | The first slide: heading, one line, an optional photograph |
| Photo with caption | One photograph that tells it |
| Statement | One sentence that matters |
| Heading and rows | Up to five short lines |
| Figure | One real number, with its as-of date in the overline |
| Quote | A person's words, name, role, optional portrait |
| Closing | Where to write: "Tell us about your space." and hello@poeticsvr.com |

A carousel is several exports: one slide at a time, with "2 of 6" in the slide field. Use the
true count of slides; don't pad to a round number.

**Video thumbnail**: 1920 × 1080, "Title and photo" (the photograph bleeds off the right edge) or
"Title only". People see thumbnails small: a few large words.

## Your part

Open the editor for the user, or give them the path. Draft the text with them first, in the
website's voice: short plain sentences with a full stop, no em dashes, no hype, sentence case,
overlines only when they add a fact, no asterisks (there are no italics). The editor's copy check
flags what slips through. The user picks the photo (their own file, or one from the Poetics photo
library folder) and exports; you can't click Export for them.

## Formats the editors don't cover

For anything else (a LinkedIn 1200 × 627 image, a banner), build it in the same system from
`design-system.md`, with the dimensions in `brand.md`'s "Social canvas specs".

## Changing the editors

Edit the sources in `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/_src/`, then rebuild:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-social-editors.py"
```

Never edit `editor.html` by hand: the build embeds the fonts and the wordmark.
