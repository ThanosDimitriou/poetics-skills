---
name: poetics-brand
description: >
  Use this skill for anything related to Poetics's brand: answering brand questions (colors,
  fonts, logo rules, voice/tone), reviewing an asset for brand compliance, or generating a
  branded document, PDF, slide deck, or social media asset (Instagram/LinkedIn carousel, video
  thumbnail). Trigger on: "Poetics brand", "brand colors", "what font does Poetics use", "logo
  rules", "is this on-brand", "brand review", "brand guidelines", "write this on-brand", "make
  this sound like Poetics", "write a doc/document/report/brief/one-pager for Poetics", "create a
  pdf", "make a Poetics deck/presentation/slides/pitch deck", "social carousel", "LinkedIn/
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
assets/
  logos/                                wordmark-{light,dark}.{svg,png}, mark-{light,dark}.png
  fonts/                                self-hosted Inter, Cormorant Garamond, Space Mono, Bricolage
  backgrounds/                          generated cinematic gradients + photo/ drop-in folder
scripts/
  build-doc.py                          renders a branded .docx from content JSON
  build-doc-pdf.py                      renders a branded .pdf from the same content JSON (canonical format)
  build-deck.py                         renders a branded deck (.html / .pdf / .pptx) from deck JSON
  doc-pdf-styles.css, _brand_assets.py  supporting files for the above — don't edit or call directly
templates/
  social-carousel/editor.html           self-contained HTML editor — open in a browser
  video-thumb/editor.html               self-contained HTML editor — open in a browser
schemas/
  doc-content-schema.md                 the JSON schema build-doc.py / build-doc-pdf.py consume
guides/
  writing-on-brand-copy.md              voice/tone checklist and before/after copy examples
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

**Proposals, offers, and quotes to another company** (venues, museums, festivals, schools) follow
a distinct playbook, not ad-hoc structure — read `guides/proposal-playbook.md` first. It defines
four modes (pitch / offer / tiered / quote), their exact section order, and hard pricing rules
(one all-inclusive figure, never invent a price, always note excl. VAT).

Ask before generating if missing: topic, audience, key sections, and (only if unclear) Word vs.
PDF. One question at a time; skip anything already given.

### Decks ("make a deck", "presentation", "pitch deck", "slides")

1. Draft the deck as JSON: `{"title", "footer"?, "slides": [...]}`, where each slide has a "type"
   (`title`, `statement`, `section`, `agenda`, `content`, `timeline`, `split`, `stats`, `cards`,
   `quote`, `closing`) — see `scripts/build-deck.py`'s docstring for the exact per-type fields.
   Vary the rhythm: don't chain three text slides in a row — put a `stats`, `quote`, or `split`
   between them; a number that matters deserves a `stats` slide, not a bullet. Wrap 2–4 word
   emotional phrases in `*asterisks*` for the Cormorant Garamond italic emphasis voice
   (sparingly — once or twice per slide at most).
2. Run the renderer — output format is chosen by the output file's extension:
   ```bash
   python3 scripts/build-deck.py /tmp/deck.json output.html   # primary — self-contained, open anywhere
   python3 scripts/build-deck.py /tmp/deck.json output.pdf    # rendered from the same HTML
   python3 scripts/build-deck.py /tmp/deck.json output.pptx   # editable PowerPoint approximation
   ```
3. Default to HTML (+ PDF if they want something to send/print); only produce PPTX if they
   specifically need to edit it in PowerPoint.

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

- Never name or visually identify a specific film, in any generated material.
- Never invent colors, fonts, logo treatments, or company facts not present in `brand.md`.
- Never invent statistics, dates, attendance numbers, team bios, or quotes — flag missing facts
  instead of estimating them.
- One accent color only — never introduce a second one.
