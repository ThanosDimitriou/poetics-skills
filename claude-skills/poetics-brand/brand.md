# Poetics brand spec

**This is the single source of truth for Poetics branding.** Every document, deck, and social
asset generated through this kit — by Claude, by any other AI tool, or by hand — should follow
what's written here. Colors, type, logo, voice, all in one place.

> **Decks moved to the website's design system (2026-10-31).** Slide decks now follow
> [`design-system.md`](design-system.md): the Poetics Website's "Aperture" system (paper and ink,
> light by default with a dark theme, Instrument Serif and Inter Tight, the lens blue only on what
> can be pressed). For decks, it replaces the Color, Typography and Spacing sections below, and it
> settles the accent question: lens `#16249C` (dark theme `#8F9CFF`). Company facts, voice, logo
> rules and social specs in this file still apply to decks. Documents and social templates stay on
> this file's visual spec until they are migrated.

**To update the brand:** edit this file directly and save. There is no build step, no sync, no
approval workflow — every skill and script reads this file fresh each time it runs.

**Owner:** Thanos Dimitriou (dimitriouathanas@gmail.com)
**Last updated:** 2026-07-10
**Source:** Derived from `Poetics Main Site/REDESIGN_GUIDE.md` (approved brief, 2026-07-04) and
the site's built code (`src/app/globals.css`, `src/lib/fonts.ts`, through commit `4aec5af`,
2026-07-06). This supersedes the older `poetics_design_system.md` (May 2026, Figtree/cobalt
palette) — that document is retired, do not use it.

---

## Open questions for Thanos

These aren't guesses baked into the spec below — they're flagged here so nothing gets used
silently until you confirm:

1. **Accent color.** The approved written brief (REDESIGN_GUIDE §6) calls for warm ember
   `#E9963E` ("the electric blue was rejected; do not bring it back"). But the most recent commit
   to the site (`4aec5af`, "accent: revert to electric blue #0099FF (previous)") reverts that
   in the actual code. This spec uses **`#0099FF` (electric blue)** because it's the latest
   intentional change — but you should confirm which one is actually final and update this file
   (and the site) to match.
2. **About page / team bios / company story** — REDESIGN_GUIDE §5 notes no source content exists
   yet for the `/about` page. The `company` section below only has the factual boilerplate that
   already exists (what Poetics does, the three-verb pitch); a fuller "our story" narrative isn't
   written yet.

---

## Company

**What Poetics is:** Poetics installs pop-up immersive cinemas — single-seat VR pods with
high-quality headsets and a curated catalog of immersive films — in museums, festivals, cultural
venues, and event spaces. The team handles everything: curation, installation, operation,
hygiene.

**The pitch, in three verbs:** **Curate → Install → Operate.**

- **Curate:** "We review hundreds of available immersive experiences to find the ones matching
  your theme."
- **Install:** "We install single-seat VR pods. Everything will be delivered, cabled, and
  preloaded for instant use."
- **Operate:** "Operators from our team will run sessions, guide audiences, and handle hygiene
  protocols."

**Based:** Greece (Athens), operating in Greece "and beyond."

**Audience:** B2B — museums, galleries, festivals, schools, cultural venues, event spaces. The
pitch works by making venues feel what their visitors will feel, not by listing specs.

**Do not name or visually identify specific films** in any generated material — this is a
deliberate brand decision (REDESIGN_GUIDE §2, "the films pivot"). Describe the program only by
theme and feeling: immersive art, documentary, performance, education. Films are the ingredient,
not the product.

**Social:** Instagram / TikTok / LinkedIn / Facebook — all `@poeticsvr`.
**Site:** poeticsvr.com

---

## Color

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

**Light / print variant (documents only, added 2026-07-11):** dark remains the canonical canvas.
For print-friendly or procurement contexts, the PDF document renderer accepts `"theme": "light"`
in the content JSON: body pages go white while the cover (and any separator page) keep the dark
brand canvas — the same compromise the Word renderer has always made. Derived tokens for light
pages (chosen for AA contrast on white; defined in `scripts/doc-pdf-styles-light.css`): text
`#0A0A0A`, secondary text `#6E6E6A`, raised surface `#F7F7F5`, hairlines
`rgba(10,10,10,0.12–0.16)`. The accent stays `#0099FF` — still one accent only. Light pages use
the **dark** logo variants, which the renderer swaps automatically. Decks and social assets
remain dark-only.

**Glow / atmosphere:** the reference deck's backgrounds are full-bleed atmospheric imagery —
either real photography graded dark (a rim-lit figure in red/blue light, a warm amber silhouette,
a dark venue) or deep gradient fields with soft multi-color light bleeding from the edges. The
renderers reproduce this with pre-generated gradient backgrounds (deep blue-black base, soft cool
glows drifting in from corners) and support dropping in real photo backgrounds (see
`assets/backgrounds/photo/README.md`). Never render the accent as a flat filled shape; light
should always feel like a source in the dark, not a color block. Restraint holds: most surfaces
are near-monochrome; color is a whisper, not a statement.

---

## Typography

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

**Register:** cinematic, editorial, restrained. Think A24 / cultural-institution sensibility, not
tech-startup landing page. Confident without hype.

**Two voices, strict roles** (mirrors the typography split):

1. **Inner voice** (serif italic in visual materials, second person, present tense) — used for
   sensory, experiential moments. Short, subtitle-like. *"You sit down. The lights dim."*
   Reserve for genuinely immersive/emotional beats, not routine copy.
2. **Narrator / facts** (sans, conventional) — used for informational content: services, process,
   case studies, FAQ, About. Scannable, direct, no hype language.

**Restraint is a brand value, not a style tic.** The design brief explicitly calls this out
multiple times: "do not overuse eyebrows," "at most one mono annotation per viewport," "one
accent only." Apply the same discipline to writing — don't stack superlatives, don't over-explain,
don't add flourish that isn't earned.

**What Poetics sounds like:**

- Concrete over abstract: describe what the audience will *feel* and *do*, not vague claims about
  "transforming" or "revolutionizing."
- Never invents facts: stats, dates, attendance numbers, team bios, testimonial quotes. If a
  number or quote isn't confirmed, mark it as a placeholder rather than inventing one.
- Never names or visually identifies a specific film (see Company section — this is a hard rule,
  not a style preference).
- Classical subtext, worn lightly: the brand name references Aristotle's *Poetics*, and the
  visual identity draws on ancient Greek theater (masks, marble, chiaroscuro). This can inform
  word choice and imagery selection but shouldn't be forced into every sentence.

**What Poetics doesn't sound like:**

- No startup hype: "disruptive," "game-changing," "10x," excessive exclamation points.
- No generic wellness/tech-marketing language: "empowering," "seamless," "elevate your..."
- No named films, franchises, or content specifics — describe by theme (art, documentary,
  performance, education) only.

---

## Spacing & structure

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
