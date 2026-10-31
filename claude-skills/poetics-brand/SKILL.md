---
name: poetics-brand
description: >
  Use this skill for anything related to Poetics's brand: answering brand questions (colors,
  fonts, logo rules, voice/tone), reviewing an asset for brand compliance, or generating a
  branded document, PDF, slide deck, or social media asset (Instagram/LinkedIn carousel, video
  thumbnail). Trigger on: "Poetics brand", "brand colors", "what font does Poetics use", "logo
  rules", "is this on-brand", "brand review", "brand guidelines", "write this on-brand", "make
  this sound like Poetics", "write a doc/document/report/brief/one-pager for Poetics", "create a
  pdf", "make a Poetics deck/presentation/slides/pitch deck", "curation deck", "program for a
  venue", "quote sheet", "write a proposal", "proposal for", "make an offer", "quote",
  "quotation", "προσφορά", "social carousel", "LinkedIn/
  Instagram carousel", "video thumbnail", "what is Poetics", "about Poetics", "Poetics company
  overview". This skill takes priority over generic docx/pdf/pptx generation for any Poetics-
  related request — never hand-build a Poetics document/deck without using the bundled renderer
  scripts below, and never invent brand colors, fonts, or facts not present in brand.md.
---

# Poetics brand skill

Self-contained: everything this skill needs (the brand spec, fonts, logos, renderer scripts,
templates) is bundled inside this skill's own folder, alongside this file. All paths below are
relative to that folder — locate it (the directory containing this SKILL.md) before running
anything.

**Always read `brand.md` (in this skill's folder) before answering any brand question or
generating any output.** It is the single source of truth for colors, typography, logo rules,
voice/tone, and company facts. If something isn't covered there, say so — never invent brand
values.

---

## What's bundled here

```
brand.md                              ← the brand spec — read this first, always
design-system.md                      ← the visual system decks follow (the website's, for slides)
assets/
  logos/                                wordmark-mono.svg (decks), wordmark-{light,dark}, mark-*
  fonts/                                Instrument Serif + Inter Tight (decks); Inter, Cormorant,
                                        Space Mono, Bricolage (documents, social)
  backgrounds/                          gradients + photo/ drop-in folder (documents only)
scripts/
  build-doc.py                          renders a branded .docx from content JSON
  build-doc-pdf.py                      renders a branded .pdf from the same content JSON
  build-deck.py                         renders a deck or A4 quote sheet (.html / .pdf / .pptx)
  audit-deck.py                         checks a deck's links, images and sources
  photo-library.py                      Poetics' photo library (local machines only, see Decks)
  doc-pdf-styles*.css, _brand_assets.py supporting files — don't edit or call directly
templates/
  decks/                                standard, curation, proposal, quote, catalog (deck JSON)
  social-carousel/editor.html           self-contained HTML editor — open in a browser
  video-thumb/editor.html               self-contained HTML editor — open in a browser
schemas/
  doc-content-schema.md                 the JSON schema build-doc.py / build-doc-pdf.py consume
guides/
  writing-on-brand-copy.md              voice/tone checklist and before/after copy examples
  deck-copy.md                          how decks are written: the website's voice
  anti-slop.md                          the deck rules, and what never to do
  proposal-playbook.md                  proposal modes and pricing rules
```

---

## Routing: what to do for each kind of request

### Brand Q&A ("what are our colors", "can I use this font for X", "is this on-brand")

Read `brand.md` and answer directly from it. For "can I do X" questions: answer yes/no first,
then the rule, then the reason — don't pad. If `brand.md` is silent on the exact situation, say so
rather than extrapolating a confident answer.

For voice/tone or copy-writing requests, also read `guides/writing-on-brand-copy.md` and apply its
checklist (concrete over abstract, no invented facts, no named films, correct register).

### Documents and PDFs ("write a doc", "create a pdf", "one-pager", "report", "brief")

1. Determine mode:
   - **Create** (default, no existing file): draft content from scratch.
   - **Edit** (user attaches an existing file): read and edit that file directly instead — this
     skill's renderers are for fresh documents, not in-place edits.
   - **Extraction** (user provides a URL/thread/pasted text and asks to "turn this into a doc"):
     extract and restructure the source content first, then proceed as create mode.
2. For create/extraction mode, build the content as JSON matching `schemas/doc-content-schema.md`
   (title, subtitle, date, sections[] with heading + html, optional separator_title, optional
   `"theme": "light"` for print/procurement contexts). Escape any user-provided text before
   embedding it in the `html` field.

   Beyond plain `<p>`/`<table>`/`<ul>`, the `html` field supports richer blocks — use the one that
   matches the content, don't force everything into a bullet: `eyebrow` (small kicker label above
   a heading), `pull-quote` (inner-voice/testimonial moments), `stat-row` (a number that matters
   gets this, never a bullet), `price-callout` (the single most important block in any
   proposal/quote — always use this over a plain `callout` for a price), and `class="recommended"`
   on a table column to highlight a tiered comparison's suggested option. Full structures in
   `schemas/doc-content-schema.md`.

3. Write that JSON to a temp file, then run the renderer from this skill's own directory:
   ```bash
   python3 scripts/build-doc-pdf.py /tmp/content.json output.pdf   # recommended — full dark-brand fidelity
   python3 scripts/build-doc.py     /tmp/content.json output.docx  # editable Word alternative
   ```
4. Present the resulting file. Do not hand-style the document yourself — the script applies
   brand.md's tokens mechanically; your job is only the content JSON.

**Proposals, offers, and quotes to another company** never use the document renderers. Every
proposal is the practical A4 quote sheet from the deck renderer: read `guides/proposal-playbook.md`
and follow the Decks section below (proposal variant, `templates/decks/quote.json` or
`proposal.json`).

Ask before generating if missing: topic, audience, key sections, and (only if unclear) Word vs.
PDF. One question at a time; skip anything already given.

### Decks ("make a deck", "presentation", "pitch deck", "slides", "curation deck", "quote sheet")

Read `design-system.md`, `guides/deck-copy.md` and `guides/anti-slop.md` first.

**1. Question tree, every time.** Skip any question the request already answers.
- What is the deck for? Introduce Poetics → **standard** (16:9). Show the titles we chose for one
  venue → **curation** (16:9, the only deck that names films). Put a price or terms in front of a
  client as slides or a quote sheet → **proposal** (practical A4), then: just the price (quote,
  one page) · scope agreed (offer, quote page + terms and signatures) · budget unknown (tiered).
- Photographs: the Poetics photo library isn't reachable here, so ask the user to upload theirs.
  Uploaded files can be used by path. Curation stills come from official sources, never from event
  photos.
- Only if the brief is unclear: who will see it, presented or sent, what they should do after,
  what they already know. Suggest additions and cuts for that audience, and let the user decide.
- Filler pages (O3 statement, N1 section, N2 agenda, S3 full photo, S4 gallery) carry no
  information: ask which to keep. Proposals never get filler, a cover or a closing page.

**2. Headings first.** List each page as its template code and heading, and show the list before
rendering. Headings are short plain sentences with a full stop, written like the website ("We run
it ourselves.", "Tell us about your space."). Reuse the website lines in `guides/deck-copy.md`.

**3. Build from page templates** (by code, `{"template": "E3", ...}`; every field in
`scripts/build-deck.py`'s docstring): O1–O3 open · N1–N2 navigate · E1–E5 explain · P1–P2 prove ·
S1–S4 show · V1–V2 voices · T1 steps · C1 closing (email only) · D1 price · D2 acceptance ·
D3 quote sheet · W1 curation title card · A1 stacked A4 page. Start from the matching file in
`templates/decks/` and rewrite it for the brief. Proposals in Greek set `"lang": "el"`.

**4. Curation decks get a research and audit round.** Take each title's facts only from official
sources (distributor, studio, festival), record them in `sources`, credit every still
(`image_credit`), and add an official `link`. Then check each source again against the slide and
mark it `"checked": true`, and run `python3 scripts/audit-deck.py deck.json`. Report the audit with
the deck.

**5. Render and look:**
```bash
python3 scripts/build-deck.py /tmp/deck.json output.html --sheet   # HTML + a PNG per page + overview sheet
python3 scripts/build-deck.py /tmp/deck.json output.pdf            # A4 proposals print on real A4 pages
python3 scripts/build-deck.py /tmp/deck.json output.pptx           # 16:9 decks only, editable approximation
```
Look at the page images before delivering, and fix every warning: overflow, the spacing guardrail
(72px clear below the wordmark, no overlaps, nothing crowding the footer), AI-sounding copy, em
dashes, placeholders. Fix the content, not the CSS.

Deck rules: say less; leave white space; few overlines; true counts, not threes; no names of the
people who made the deck unless asked; the only email is hello@poeticsvr.com; every footer reads
"poeticsvr.com · Confidential"; the closing page has one path, the email.

### Social assets ("carousel", "Instagram/LinkedIn post", "video thumbnail")

Point to (or open, if this environment can) the relevant self-contained editor:
`templates/social-carousel/editor.html` (1080×1350, layouts: cover/bullets/stat/quote) or
`templates/video-thumb/editor.html` (1920×1080). These are interactive HTML forms — the user fills
them in and clicks Export themselves; this skill can prefill guidance in chat but can't complete
the interactive export step for them.

### Brand review ("review this", "is this on-brand", "brand audit")

Produce:
- **Brand compliance score: X/10** (start at 10; critical issues −1.5 to −2 each — wrong colors/
  fonts, logo misuse, a named film appearing anywhere, a second accent color; minor issues −0.5 to
  −1 each)
- **What's on-brand** — specific, named elements
- **What needs fixing** — element / problem / fix (citing the exact `brand.md` value) / severity
- **Summary** — one or two sentences, the single most important fix

Always check the hard rules first: no named/identifiable films anywhere, one accent color only,
correct voice register for the content type.

### Company / "about Poetics"

Answer from `brand.md`'s Company section (what Poetics does, the Curate → Install → Operate
pitch, where it's based, who it serves). If asked for a fuller company story or team bios, say
that content doesn't exist yet rather than inventing one — `brand.md`'s "Open questions" section
flags this as a known gap.

---

## Hard rules (always enforce, regardless of what's asked)

- Never name or visually identify a specific film, in any generated material, except in a
  curation deck sent to the one venue it was made for.
- Never invent colors, fonts, logo treatments, or company facts not present in `brand.md`.
- Never invent statistics, dates, attendance numbers, team bios, or quotes — flag missing facts
  instead of estimating them.
- One accent color only — never introduce a second one. In decks it appears only on the one
  action (the email link, or a curation title's official link).
