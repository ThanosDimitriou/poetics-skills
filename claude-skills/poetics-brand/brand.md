# Poetics brand spec

The brand facts, logo rules and voice for everything this kit makes. **How things look is in two
places:**

| Material | Visual system |
| --- | --- |
| Decks, proposals, documents and PDFs | [`design-system.md`](design-system.md): the Poetics Website's "Aperture" system (paper and ink, light by default with a dark theme, Instrument Serif and Inter Tight, the lens blue only on what can be pressed) |
| Social templates (carousel, video thumbnail) | The **legacy spec** in the Color, Typography and Spacing sections below (dark canvas, Inter, Cormorant italics, `#0099FF`), until the editors are migrated |

How to write, for every material: [`guides/writing-on-brand-copy.md`](guides/writing-on-brand-copy.md)
(the website's voice). What never to do: [`guides/anti-slop.md`](guides/anti-slop.md).

**To update the brand:** edit this file (or `design-system.md`) and save. Every skill and script
reads them fresh each time it runs; the installed plugin and the claude.ai bundle pick changes up
when they're updated (see `INSTALL.md`).

**Owner:** Thanos Dimitriou (dimitriouathanas@gmail.com)
**Last updated:** 2026-11-01
**Sources:** the Poetics Website (`Poetics Website/DESIGN-SYSTEM.md`, `_source/copy/BRIEF.md`,
`src/data/*.ts`, as of October 2026) for company facts, voice and the design system. The legacy
visual spec below came from `Poetics Main Site/REDESIGN_GUIDE.md` (July 2026), now superseded for
everything except the social templates.

---

## Open questions

None at the moment. Two earlier questions are settled by the website:

- **Accent colour:** the website's lens blue, `#16249C` (dark theme `#8F9CFF`), used only on what
  can be pressed. The legacy `#0099FF` survives only in the social templates.
- **Company story:** the website's About page now has it (see Company below). Team bios are still
  not written; don't invent them.

---

## Company

**What Poetics is:** production, curation and distribution of immersive experiences with new
media. Poetics runs pop-up immersive cinemas (single-seat VR pods, a curated program, trained
operators), interactive projection mapping, immersive recordings (VR180 and 360°) and
audiovisual experiences, at festivals, museums and brand events. Tagline: **Immersive cinema,
anywhere.**

**The pitch, in three verbs:** **Curate → Install → Operate.** In the website's words:

- **We curate:** "We review hundreds of titles and choose a handful for your audience. A program
  runs 10–50 minutes."
- **We install:** "Each pod is one seat: a swivel chair, a headset and noise-cancelling
  headphones. Pods arrive cabled and ready to play."
- **We operate:** "Trained operators run the room and control the equipment through Poetics Pods,
  our own software. They follow the hygiene protocols and onboard every visitor."

**Why it exists** (website, About): immersive films win prizes at Cannes, Venice and Sundance,
then wait: cinemas aren't built for them and headsets sit unused at home. Poetics is the layer in
between: it licenses the work, curates it for a place and an audience, and puts it in front of
people.

**Based:** Thessaloniki, Greece (founded 2025), working in Greece and beyond.

**Track record** (public, as of September 2026): 5,000+ screenings at 15+ events, rated 4.92 out
of 5 by visitors, 250+ five-star Google reviews. Selected for the Curators Network of the Cannes
Immersive Market (May 2026), the first Greek private initiative in it. Co-hosted a panel at the
Venice Production Bridge (September 2026).

**Audience:** B2B: museums, galleries, festivals, brands and agencies, schools, cultural venues.

**Films:** never name or show a specific film in generated material, except in a curation deck
made for one venue (it lists the titles chosen for them). Describe a program by theme: arts,
education, entertainment. Films are the ingredient, not the product.

**Confidential** until Poetics clears it: pricing amounts, the franchise model, roadmap dates
(other than the December festival), the streaming platform's status, internal tooling, survey
methodology.

**Contact:** hello@poeticsvr.com · **Site:** poeticsvr.com
**Social:** Instagram `@poeticsimmersive` · TikTok `@poeticsvr` · LinkedIn `poetics-vr` · Facebook

---

## Legacy visual spec (social templates only)

The Color, Typography and Spacing sections below describe the July 2026 look. Only the social
templates (`templates/social-carousel`, `templates/video-thumb`) still use it; decks, proposals and
documents follow `design-system.md`.

## Color (legacy: social templates)

Dark theme only. Near-black canvas, warm-white text, one accent color used sparingly.

| Token | Hex | Usage |
|---|---|---|
| Canvas (website) | `#0A0A0A` | The website rebuild's page background (neutral near-black) |
| Canvas (decks/docs) | `#06070F` | Background for generated decks, documents, and social — a deep blue-black matching the Athens College deck. This is the canvas the renderers actually use. |
| Canvas raised | `#111214` | Cards, panels, layered surfaces |
| Pure black | `#000000` | Full-bleed image sections only |
| Text primary | `#F4F4F2` | Headlines, primary body text |
| Text secondary | `#9A9A98` | Secondary text, captions, metadata, eyebrows |
| Accent | `#0099FF` | See "Open questions" above. Interactive states, links, occasional highlighted value/stat, glow effects. **One accent only — never introduce a second accent color.** Never used for large filled areas or body text. In the reference deck the accent is used *very* sparingly — most slides are pure monochrome white/gray on the blue-black. |
| Border, subtle | `rgba(255,255,255,0.12)` | Card borders, dividers, rounded photo-container edges |
| Border, hairline | `rgba(255,255,255,0.08)` | Thin structural rules (e.g. the footer rule) |

**Contrast note:** text secondary was lightened from an earlier `#808080` specifically for AA
contrast on near-black backgrounds. Don't darken it back down.

**Glow / atmosphere:** the reference deck's backgrounds are full-bleed atmospheric imagery —
either real photography graded dark (a rim-lit figure in red/blue light, a warm amber silhouette,
a dark venue) or deep gradient fields with soft multi-color light bleeding from the edges. The
renderers reproduce this with pre-generated gradient backgrounds (deep blue-black base, soft cool
glows drifting in from corners) and support dropping in real photo backgrounds (see
`assets/backgrounds/photo/README.md`). Never render the accent as a flat filled shape; light
should always feel like a source in the dark, not a color block. Restraint holds: most surfaces
are near-monochrome; color is a whisper, not a statement.

---

## Typography (legacy: social templates)

Self-hosted Google Fonts. Font files are in `assets/fonts/`.

**Note on the two contexts:** the Poetics *website* rebuild uses Bricolage Grotesque as its display
face. Poetics *documents, decks, and social assets* (what this kit generates) instead use **Inter**
for display, matching the established Athens College deck aesthetic — a cleaner, more neutral
grotesque. This was a deliberate decision (2026-07-10): the kit's output should look like the deck,
not the website. Bricolage font files remain in `assets/fonts/` but are not used by the renderers.

| Role | Family | Files | Usage |
|---|---|---|---|
| **Display** | Inter (SemiBold) | `Inter-{SemiBold,Bold}.ttf` | Headlines, titles, display type. Large, sentence case (not title case), tight leading. Neutral geometric grotesque — clean and editorial, not quirky. |
| **Emphasis** | Cormorant Garamond, italic only | `CormorantGaramond-{Italic,MediumItalic,SemiBoldItalic}.ttf` | 2–4 word emotional emphasis phrases inside headlines or pull quotes ("a new way *to experience* art"). **Always italic, never roman, never body text.** The signature typographic move that expresses the name "Poetics" — use sparingly (at most ~1–2 per page/slide), and only for genuinely emotional/sensory beats. Factual headlines stay in plain Inter. |
| **Body** | Inter | `Inter-{Light,Regular,Medium,SemiBold}.ttf` | Body copy, UI text, narrator/factual sections. |
| **Annotation** | Space Mono | `SpaceMono-{Regular,Bold}.ttf` | Eyebrows/overlines (uppercase, wide tracking, gray), metadata, index numbers, hex values, technical notes. Use sparingly — at most one mono annotation per page/slide/viewport. |

**Letter-spacing tokens:**

| Token | Value | Usage |
|---|---|---|
| Display tracking | `-0.02em` | Large display/headline text |
| Wide tracking | `+0.08em` | Uppercase labels, tags |
| Mono tracking | `+0.05em` | Monospace annotation text |

---

## Logo

These rules apply to every material. Decks, proposals and documents use the website's
single-colour wordmark, `assets/logos/wordmark-mono.svg`, painted in `ink` for the theme (dark on
paper, light on the dark theme). The files below are the legacy lockups used by the social
templates.

Wordmark: **"P⬭ETICS"** — the O is rendered as a headset-shaped pill, referencing the VR product.
Official master assets (SVG + PNG) live in `assets/logos/`.

**Naming convention:** "light" = the light-colored (white) logo, for use **on dark backgrounds**;
"dark" = the dark-colored logo, for use **on light backgrounds**. Since Poetics is dark-canvas by
default, the **light** variant is the everyday one.

| File | Format | Use |
|---|---|---|
| `wordmark-light.svg` / `.png` | SVG master + 1000×340 PNG | Primary horizontal lockup on dark — headers, footers, covers, deck title slides |
| `wordmark-dark.svg` / `.png` | SVG master + 1000×340 PNG | Horizontal lockup for the rare light-background context |
| `mark-light.png` / `mark-dark.png` | 1000×1000 | Standalone square pill mark (transparent) — small placements, favicons, avatars |
| `mark-light-bg.png` / `mark-dark-bg.png` | 1000×1000 | Square mark on a solid brand-color tile |

**Rules:**

- Use the horizontal wordmark lockup by default. Don't typeset "Poetics" as styled text as a
  substitute for the real logo file.
- Don't redesign, recolor, distort, rotate, or add effects to the mark.
- Pick the variant by background: light logo on dark, dark logo on light. Never light-on-light or
  dark-on-dark.
- SVG masters exist (`wordmark-light.svg`, `wordmark-dark.svg`) — prefer these for any large-scale
  or print use; the PNGs are for contexts that can't take SVG.

---

## Voice & tone

**One voice, the website's.** Plain, concrete, first person plural, short sentences, active verbs.
Confident about operations, modest about art. Describe what happens, never how it feels: the
photography carries the feeling. No hype, no em dashes, no exclamation marks, sentence case.

The full guide, with reusable lines and before/after examples, is
[`guides/writing-on-brand-copy.md`](guides/writing-on-brand-copy.md). Slide specifics are in
`guides/deck-copy.md`; the patterns that read as machine-written are in `guides/anti-slop.md`.

The earlier two-voice system (a serif italic "inner voice" for sensory moments) is retired.

---

## Spacing & structure (legacy: social templates)

Dark canvas, generous negative space, asymmetric editorial layouts rather than centered
symmetric ones.

| Element | Spec |
|---|---|
| Border weight | Hairline only — `1px` at low opacity (`rgba(255,255,255,0.08–0.12)`), never a heavy stroke |
| Card radius | 12–16px |
| Card fill | `#111214` (canvas raised) |
| Rules/dividers | `1px solid rgba(255,255,255,0.12)`, used to structure sections, not decorate them |
| Frosted glass (buttons/badges over imagery) | Subtle `backdrop-filter` blur, hairline border — used sparingly, for chrome over full-bleed images only |

**Imagery:** full-bleed, graded dark and cool, soft glow, treated as texture rather than
illustration. No generic stock photography. Text over imagery needs a gradient scrim for
legibility, not a flat overlay box.

---

## Social canvas specs

Reusable technical export geometry (not brand aesthetic — these dimensions don't change with the
color/font decisions above).

**Primary format:** all carousels design at **1080 × 1350px (4:5)** — works across Instagram,
LinkedIn, and TikTok without adaptation.

| Platform | Format | Dimensions |
|---|---|---|
| Instagram | Carousel / Feed | 1080 × 1350px (4:5) |
| Instagram | Reels cover / Story | 1080 × 1920px (9:16) |
| LinkedIn | Image post | 1200 × 627px (1.91:1) |
| LinkedIn | Carousel (PDF) | 1080 × 1350px (4:5) |
| LinkedIn | Video | 1920 × 1080px (16:9) |
| TikTok | Video | 1080 × 1920px (9:16) |
| TikTok | Carousel | 1080 × 1350px (4:5) |

**Safe zone — 4:5 carousel (1080 × 1350px):**

```
Canvas:    1080 × 1350px
Safe area: 980 × 1150px (centred, 50px margin all sides)
Danger:    top 250px and bottom 250px (mobile UI overlap)
Handle:    @poeticsvr — bottom-right corner, inside safe zone
```

Design at 1× (1080px wide). Don't design at 2× or 3× and scale down — causes blurring on export.

---

## What this spec does not cover

- Motion/animation design (scroll effects, shaders, transitions) — that's specific to the live
  website build and doesn't translate to static documents/decks/social assets. See
  `Poetics Main Site/REDESIGN_GUIDE.md` §6 if you're working on the site itself.
- A full "about us" narrative / team bios (see Open questions above).
- Print-specific guidance (paper stock, spot colors) — not needed yet.
