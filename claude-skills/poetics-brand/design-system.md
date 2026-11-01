# Poetics design system, for slides

**Decks follow this file.** It is the website's design system (`Poetics Website/DESIGN-SYSTEM.md`,
the "Aperture" system, as of website commit `caa2f43`, 2026-10-29) translated to a 1920 × 1080
slide. Where the two disagree, the website wins: update this file to match. `brand.md` still owns
company facts, voice and the logo rules; documents and social assets stay on `brand.md`'s older
visual spec until they are migrated.

`scripts/build-deck.py` applies everything below mechanically. Read this to make content decisions
(which slide type, how much text, which photograph), not to hand-write CSS.

---

## Principles

1. **Aperture.** Every photograph and module is a form taken from the pill in the wordmark's O. A
   slide is a viewport the audience looks through.
2. **Sleek, minimal, direct.** When a choice isn't covered here, take the quieter, shorter option.
3. **Blue means you can act here.** The lens colour appears only on things that can be pressed: the
   email link on the closing slide, the deck's one path. Figures, highlights, bullets and numerals
   are never blue; they are ink.
4. **One idea per slide.** A heading and one or two sentences on show. More detail goes to the
   speaker notes or to a following slide, never to smaller type.
5. **Space separates.** Space and 1px hairlines, never boxes around content, never shadows on cards.
6. **Nothing moves.** Slides change at once. No transitions, builds or animated reveals.
7. **Two themes, one set of roles.** Light is the default; `"theme": "dark"` swaps every role to its
   dark value. Check both if a deck will be shown in a dark room.

## Colour

Seven roles, two themes. The renderer reads them from the tokens below; never type a hex value into
deck content.

| Token        | Light     | Dark      | Use on a slide                                                     |
| ------------ | --------- | --------- | ------------------------------------------------------------------ |
| `paper`      | `#EFF0EC` | `#121614` | Slide ground (off-white; the website's is `#F4F5F3`, see below)    |
| `paper-deep` | `#E5E8E3` | `#1C211E` | Ground for section, statement and quote slides; the closing band; an empty photo frame |
| `shade`      | `#C5CBC4` | `#3A423D` | Hairlines and the Ring; decoration only                            |
| `ink`        | `#121614` | `#F4F5F3` | Text, wordmark, figures, numerals, anything highlighted            |
| `ink-soft`   | `#5B625C` | `#8A918B` | Overlines, captions, descriptions, footer                          |
| `lens`       | `#16249C` | `#8F9CFF` | The closing slide's email link. Nothing else                       |
| `lens-deep`  | `#0E1769` | `#BCC4FF` | Hover on those, in the HTML deck                                    |

No gradients, no tints of the accent, no glows, no colour that only works in one theme.

**Decks are a step deeper than the website (2026-10-31, at the owner's request):** the website's
light paper is `#F4F5F3`; decks use `#EFF0EC` (paper-deep `#E5E8E3`, shade `#C5CBC4`) so the
light theme always reads as off-white on screens and projectors, never as `#FFFFFF`. Same hue,
same roles, same contrast for ink and ink-soft. The dark theme is unchanged.

## Type

**Instrument Serif** 400 for display, never under 48px on a slide (32px on the web), tracking
-0.02em. Its Greek comes from Noto Serif Display, registered under the same name, so Greek decks
work without changes. **Inter Tight** 400 and 500 for everything else. No italics, no bold beyond
500, no capitals, no letter-spacing on text, sentence case everywhere.

Slide sizes are the web scale × 1.5 (a 1920px slide shown on a laptop lands near the web sizes).

| Token        | Slide px      | Role on a slide                                              |
| ------------ | ------------- | ------------------------------------------------------------ |
| `display-xl` | 156, lh 1     | Cover title only                                             |
| `stat`       | 144, lh 1     | Feature figures (the stats slide)                            |
| `display-l`  | 102, lh 1.05  | Section-divider titles, a statement, the closing call to action |
| `display-m`  | 66, lh 1.1    | Every slide heading; a quote                                 |
| `title`      | 36, 500       | Column, row and step titles                                  |
| `body-l`     | 32, lh 1.5    | Leads, bullets in speaker-led decks                          |
| `body`       | 26, lh 1.6    | Descriptions, bullets in reading-first decks                 |
| `caption`    | 21, lh 1.5    | Overlines, captions, footer, numerals                        |

- **Every slide heading is display-m.** Display-l is for section dividers, the statement and the
  closing, nothing else. Display-xl is the cover.
- A slide uses at most two text sizes below its heading, and one weight pair.
- Measure: running text 50ch, display headings 18ch, the cover title 24ch. The renderer steps a
  long heading down one size rather than letting it run past the measure; if it still doesn't fit,
  the heading is too long. Rewrite it.
- Headings left-aligned and balanced. Nothing is centred.
- The **overline** replaces the old mono eyebrow: caption size, ink-soft, sentence case, Inter Tight.
  At most one per slide, and only when it adds something (a date, who it's for, a part number).
- `*asterisks*` from the old emphasis voice are accepted and rendered as plain text. There is no
  italic emphasis voice in this system.

## Spacing

The web scale × 1.5, in px: **6, 12, 18, 24, 30, 36, 48, 72, 96, 120, 144, 192, 240**. The same
relationship always gets the same gap.

| Between                                                   | Slide px |
| --------------------------------------------------------- | -------- |
| Overline and title, in a column                           | 6        |
| Title and its description, in a ruled row                 | 12       |
| Title and body in a column; caption under a photograph    | 18       |
| Overline and a slide heading                              | 24       |
| Row padding in a ruled list (top and bottom)              | 30       |
| Columns (gutter)                                          | 36       |
| Heading and lead                                          | 48       |
| Heading or lead and the slide's content                   | 96       |

## Layout

- Canvas 1920 × 1080. Margins 120px left and right. The wordmark sits 72px from the top (30px tall,
  the website header's 20px × 1.5); content starts at 192px and ends 168px from the bottom; the
  footer's baseline is 72px from the bottom.
- Footer, on every slide: `poeticsvr.com · Confidential` at the left; at the right the proposal
  number (if any) and `3 of 12` (not on the cover or closing). Caption size, ink-soft, no rule.
  Proposals add "Created <date>" at the left and a first line above: "Any change in scope requires
  an adjusted quotation."
- **A4 portrait** (proposals): practical documents with no cover and no closing page; the first page
  is the D3 quote sheet. 1480 × 2092 px, printed on real 210 × 297 mm pages. The same type
  tokens, so body text lands near 10.5pt; margins 120px; content from 192px to 264px above the
  foot. Layouts stack (photos above text, steps as rows) and A1 stacked pages put two or three
  templates on one page.
- **Closing:** one path only. The heading ("Write to us.", "Tell us about your space.") and the
  email, hello@poeticsvr.com, as a lens link in the display face. No buttons, no second option.
- A twelve-column grid with a 36px gutter. Split slides use columns 1 to 6 for text and 7 to 12
  for the photograph.
- **Decoration: the wordmark's O, and nothing else**, once per deck: a large 1px `shade` outline of
  it (the Ring) behind the closing slide's band, so one arc crosses the band and runs off its end.
  No ghost numerals, no accent bars, no lines under titles, no background images, no icons used as
  ornament.
- Grounds: slides with photographs and most content sit on `paper`. Section dividers, statements and
  quotes sit on `paper-deep`, so the deck alternates the way the website's sections do.

## Shape and media

- Three radii, nothing else: **pill** (buttons, small crops, the closing band), **lens** 48px
  (photographs, large modules), **small** 18px (fields, table cells).
- Every photograph goes through an aperture: a lens (4:3 default, 3:4 portrait, 3:2, 16:9, 21:9
  band), a pill, or the mark (upright 5:9, for a quote portrait). Set a `focal` point so faces
  survive the crop.
- A photograph may **bleed** to one slide edge only, and that side is square.
- A missing photograph renders as an empty `paper-deep` frame with no text, and the renderer warns.
- **The photo library:** `photos/index.json` lists Poetics' own photographs (what each shows, who
  is in it, its shape and uses). The files stay on the owner's machine, by default the website's
  image folder (`$POETICS_PHOTO_ROOT` overrides); slides use `"image": "photo:<id>"`. Browse with
  `scripts/photo-library.py sheet`.

## Documents

Reports, briefs and one-pagers (`scripts/build-doc-pdf.py`, and `build-doc.py` for an editable
Word file) use the same system on A4:

- Off-white paper into the margins (or the dark set with `"theme": "dark"`), ink text.
- A cover with the wordmark, an optional photograph in a lens, the title in the display face, the
  date. Body pages carry the wordmark top-left with clear space below it, and
  "poeticsvr.com · Confidential" with the page number in the footer.
- Section headings in Instrument Serif (26pt), sub-headings in Inter Tight, body 10.5pt.
- Tables, callouts, figures and prices on hairlines; a recommended table column on paper-deep.
  No filled boxes, no shadows, no italics.

The Word file names the fonts rather than embedding them: install Instrument Serif and Inter
Tight to see it as designed. The PDF is the version to send.

## Spacing guardrail

Every render is checked (`build-deck.py --check`), and a deck that fails isn't finished:

- **72px of clear space below the wordmark.** No heading, text or photograph starts closer.
  (Photographs start with the content, at 192px; they never tuck up under the wordmark.)
- **Nothing overlaps:** text against text, text against a photograph.
- **Nothing crowds the footer** (132px above the slide's foot; 180px with a proposal disclaimer).
- **Nothing runs past the side margins** except a photograph that bleeds off one edge on purpose.
  Never put the logo, an icon or "image here" in it.

## Writing for slides

The deck rules in `guides/anti-slop.md` ("Poetics deck rules") come first: say less, leave white
space, no cheesy taglines, few overlines, true counts instead of threes, no makers' names,
hello@poeticsvr.com only. Then the website's content rules, which apply to decks unchanged:

- **Never invent** a figure, date, quote, name, partner or photograph.
- **No visible placeholders.** Write an unknown as a capitalised bracket (`[ATTENDANCE]`,
  `[CONFIRM: venue name]`). The renderer drops any item containing one, warns, and keeps the gap
  out of the deck. A heading that is a placeholder is a slide that isn't ready.
- **No em dashes.** A colon, a comma, a full stop or parentheses. En dashes in ranges (10–50).
- Sentence case, American spelling ("program", "organization").
- Confidential until Poetics clears it: pricing amounts, the franchise model, roadmap dates, the
  streaming platform's status, internal tooling, survey methodology.
- Never name or visually identify a specific film (`brand.md`, Company).

## Fonts and files

| File                                                   | Use                                               |
| ------------------------------------------------------ | ------------------------------------------------- |
| `assets/fonts/InstrumentSerif-Regular-latin.woff2`     | Display, embedded in HTML/PDF                     |
| `assets/fonts/NotoSerifDisplay-w70-greek*.woff2`       | Display Greek, embedded under the same family     |
| `assets/fonts/InterTight-{400,500}-{latin,greek}.woff2`| Text, embedded in HTML/PDF                        |
| `assets/fonts/InstrumentSerif-Regular.ttf`, `InterTight-Variable.ttf` | Install these to edit the PPTX     |
| `assets/logos/wordmark-mono.svg`                       | The website's wordmark, recoloured to `ink` per theme |

All fonts are SIL Open Font License (licences beside them in `assets/fonts/`).
