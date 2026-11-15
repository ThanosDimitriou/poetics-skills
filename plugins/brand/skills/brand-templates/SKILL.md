---
name: brand-templates
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for social media assets and video thumbnails. Trigger on: "social carousel",
  "LinkedIn carousel", "Instagram carousel", "case study post", "video thumb", "video thumbnail",
  "youtube thumbnail", "thumbnail for a video", "social template", "Instagram post", "LinkedIn
  post", "Instagram story", "promoted post", "ad creative", "brand template", "brand starter".

---

# Brand templates

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"                  # the look (the editors apply it)
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # social canvas specs
```

## The two editors (Aperture look)

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

A carousel is several exports, one slide at a time. There is no footer or slide count: Instagram
and LinkedIn show the account name and the carousel dots.

**Video thumbnail**: 1920 × 1080, "Title and photo" (the photograph bleeds off the right edge) or
"Title only". People see thumbnails small: a few large words.

## Your part

Open the editor for the user, or give them the path. Draft the text with them first, in the
website's voice: short plain sentences with a full stop, no em dashes, no hype, sentence case,
overlines only when they add a fact, no asterisks (there are no italics). The editor's copy check
flags what slips through. The user picks the photo (their own file, or one from the Poetics photo
library folder) and exports; you can't click Export for them.

## Feed styles: build a whole post or story yourself

The editor makes one slide at a time and only in the Aperture look. For a finished carousel or
story (Claude Code only: it needs Playwright and Chrome), write a JSON deck and render it:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-social.py" deck.json OUT_DIR
```

Add `--pdf` for LinkedIn: it also writes `slides.pdf`, one page per slide, to post as a document.
It writes `01-….png` onward (1080 × 1350, or 1080 × 1920 with `"format": "story"`) and a
`contact-sheet.png`, checks every slide (margins, wordmark clearance, the story's top 270px and bottom 380px, text over
photographs, text under 44px, contrast against what is behind each line) and the copy, and exits non-zero if something is wrong.
The wordmark goes on the first and last slide only, since Instagram shows the account name above every
slide; `"wordmark": "all"` in the deck puts it back everywhere. Read the "Social feed styles"
section of `design-system.md` first: it says which layout to use for what and which brand rules
the feed relaxes. Copy a starting deck from `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/social-styles/examples/`:

| Layout | Look | Use it for | Example |
|---|---|---|---|
| `type` | Solid ground, big serif, grain; `lens` ground is brand blue | Ideas, questions, "why" | `type-post.json` |
| `photo` | Full-bleed photograph, shade under the type; `"treatment": "duotone"` | Ads, energy, stories | `photo-post.json` |
| `framed` | Light, photographs in pills and lenses | Agencies, venues, B2B proof | `framed-post.json` |

Each example has a picture next to it (`photo-post.jpg`, `framed-post.jpg`, `type-post.jpg`): look
at the one for the layout you chose before you write the deck, so you aim at the same quality.
`styles.json` (and `styles.jpg`) has one slide of each look to copy from. The examples use only
photographs without people. Photographs are ids from the photo library
(`photos/index.json`) or file paths. The workflow: draft the copy first (short lines, one idea a
slide, nothing the website doesn't say), pick the layout from the table, render, look at the
contact sheet, fix the PROBLEM and COPY lines. If two posts will be pinned together, give them
different layouts. Say in your reply which brand rules the style relaxes, and that photographs
showing identifiable people need consent for advertising use.

## Formats the editors don't cover

For anything else (a LinkedIn 1200 × 627 image, a banner), build it in the same system from
`design-system.md`, with the dimensions in `brand.md`'s "Social canvas specs".

## Changing the editors

Edit the sources in `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/_src/`, then rebuild:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-social-editors.py"
```

Never edit `editor.html` by hand: the build embeds the fonts and the wordmark.
