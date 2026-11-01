# Poetics brand spec

The brand facts, logo rules and voice for everything this kit makes. **How things look** (decks,
proposals, documents, social posts and thumbnails) is in [`design-system.md`](design-system.md):
the Poetics Website's "Aperture" system (paper and ink, light by default with a dark theme,
Instrument Serif and Inter Tight, the lens blue only on what can be pressed).

How to write, for every material: [`guides/writing-on-brand-copy.md`](guides/writing-on-brand-copy.md)
(the website's voice). What never to do: [`guides/anti-slop.md`](guides/anti-slop.md).

**To update the brand:** edit this file (or `design-system.md`) and save. Every skill and script
reads them fresh each time it runs; the installed plugin and the claude.ai bundle pick changes up
when they're updated (see `INSTALL.md`).

**Owner:** Thanos Dimitriou (dimitriouathanas@gmail.com)
**Last updated:** 2026-11-01
**Sources:** the Poetics Website (`Poetics Website/DESIGN-SYSTEM.md`, `_source/copy/BRIEF.md`,
`src/data/*.ts`, as of October 2026) for company facts, voice and the design system. The July 2026
visual spec (dark canvas, Inter, Cormorant italics, `#0099FF`) is retired; git history has it.

---

## Open questions

None at the moment. Two earlier questions are settled by the website:

- **Accent colour:** the website's lens blue, `#16249C` (dark theme `#8F9CFF`), used only on what
  can be pressed.
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

## Logo

These rules apply to every material. Decks, proposals and documents use the website's
single-colour wordmark, `assets/logos/wordmark-mono.svg`, painted in `ink` for the theme (dark on
paper, light on the dark theme). The lockups below are for use outside the kit (avatars, partner
materials, press).

Wordmark: **"P⬭ETICS"** — the O is rendered as a headset-shaped pill, referencing the VR product.
Official master assets (SVG + PNG) live in `assets/logos/`.

**Naming convention:** "light" = the light-coloured (white) logo, for use **on dark backgrounds**;
"dark" = the dark-coloured logo, for use **on light backgrounds**. Poetics is light by default, so
the **dark** variant is the everyday one.

| File | Format | Use |
|---|---|---|
| `wordmark-mono.svg` | SVG, 148×20, no padding | The website's wordmark; the kit paints it in `ink` per theme (`wordmark-mono-ink.png` / `-paper.png` for Word) |
| `wordmark-dark.svg` / `.png` | SVG master + 1000×340 PNG | Horizontal lockup on light backgrounds |
| `wordmark-light.svg` / `.png` | SVG master + 1000×340 PNG | Horizontal lockup on dark backgrounds |
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

## Social canvas specs

Export geometry for social assets. The social post editor (`templates/social-carousel/editor.html`)
makes 4:5, 1:1 and 9:16; the video thumbnail editor makes 1920 × 1080.

**Primary format:** carousels at **1080 × 1350px (4:5)**: it works across Instagram, LinkedIn and
TikTok without adaptation.

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
4:5 and 1:1: 90px margins; the wordmark top-left; the footer (poeticsvr.com) bottom-left,
             an optional "2 of 6" bottom-right.
9:16 story:  the top and bottom 250px sit under the app's own interface: nothing goes there.
```

Design at 1× (1080px wide). Don't design at 2× or 3× and scale down — causes blurring on export.

---

## What this spec does not cover

- Motion (the website's few approved animations): see `Poetics Website/DESIGN-SYSTEM.md`, Motion.
  Decks and social assets don't move.
- Team bios (see Open questions).
- Print production (paper stock, spot colours): not needed yet.
