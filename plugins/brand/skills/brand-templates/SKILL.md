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

## The social studio and the thumbnail editor

Self-contained HTML files: open them in a browser (double-click works, no server, nothing is
uploaded, the fonts and wordmark are inside).

| Request | Editor | Path |
|---|---|---|
| Instagram, LinkedIn or TikTok post, carousel or story, made by hand | Social studio | `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/social-carousel/editor.html` |
| YouTube thumbnail, video cover | The studio, on the thumbnail format | `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/video-thumb/editor.html` |

**Social studio**: the whole feed system, by hand. It draws the same three layouts as
`build-social.py`, to the pixel: type (paper, deeper paper, ink, deeper ink, lens blue; an optional
empty oval), photo (full bleed or duotone, with the soft shade) and framed (cover, three rows, lens,
pair, closing). It does:

- **Carousels:** a strip of slides to add, duplicate, delete and reorder by dragging.
- **Formats:** 4:5, 1:1 and 9:16 (the story keeps its top 270px and bottom 380px clear).
- **The wordmark:** first and last slide (default), every slide, the first only or none, with an
  override on any slide.
- **Text:** one row per line, each with its own size (a line fills the width up to it), a line
  under, an email or link.
- **Repositioning:** drag the text block (it snaps to top, middle and bottom), drag an oval, drag
  a photo to reframe it, scroll or use the slider to zoom. Arrow keys nudge; Cmd+Z undoes.
- **Photos:** added from the computer or dropped on a frame; a frame remembers the photo's name.
- **Editing on the slide:** double-click any text to edit it in place; clicking text highlights
  its field in the inspector.
- **Previews:** Phone shows the post in an Instagram feed (swipe, dots, the caption's first line,
  optionally as an ad), a story with the app's bands and ad button, or a thumbnail on YouTube at
  real size; Grid shows the cover as a 3:4 profile tile.
- **Caption and alt text:** a caption field (first-line counter, copy button) and alt text per
  slide, checked against the copy guide: first line under 125 characters, the email repeated,
  three to five CamelCase hashtags, alt text on every photo slide.
- **Checks, live:** margins, the story's safe zone, text under 44px, contrast against what is
  behind each line, text over a photo, empty frames, and the copy check. Export warns first.
- **Export:** this slide (PNG), all slides (ZIP with caption.md and deck.json), a LinkedIn PDF,
  deck.json alone, or a project file that keeps the photos inside. It opens a saved project or
  any `deck.json` you write. Photos also stay in the browser between sessions.
- **Video thumbnails** are a format in the same studio (1920 × 1080, title and photo or title
  only, light or dark); `templates/video-thumb/editor.html` is the studio opening on that format.
- Shortcuts: ← → slides, ⌘Z undo, ⌘D duplicate, ⌘S save, ⌘E export, G guides, P phone, ? for all.

So you can hand off either way: write a deck JSON (the format below), give it to the user to
open in the studio and finish by hand, or render a deck they saved from the studio with
`build-social.py` (add the photos by library id or path).

**Video thumbnail**: 1920 × 1080, "Title and photo" (the photograph bleeds off the right edge) or
"Title only". People see thumbnails small: a few large words (the studio warns past eight).

## Your part

Open the studio for the user, or give them the path. Draft the text with them first, in the
website's voice: short plain sentences with a full stop, no em dashes, no hype, sentence case, no
asterisks (there are no italics). The studio's checks flag what slips through. The user adds the
photos (their own files, or ones from the Poetics photo library folder) and exports; you can't
click Export for them.

## Feed styles: build a whole post or story yourself

When you can run code (Claude Code: Playwright and Chrome), render a finished carousel or story
yourself from a JSON deck, the same format the studio saves:

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

Never edit `editor.html` by hand: the build embeds the fonts, the wordmark and the example decks
(from `templates/social-styles/examples/`). The studio's drawing follows `build-social.py`: change
both together, then check a deck renders the same in each.
