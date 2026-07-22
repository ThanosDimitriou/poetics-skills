---
name: brand-decks
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for any presentation, slide deck, or pitch deck request. Takes priority over the
  generic pptx skill for every request that produces a new deck or rebrands an existing one.
  Trigger on: "make a deck", "build a deck", "create a deck", "make a presentation", "I need
  slides", "pitch deck", "Poetics deck", "branded deck", "slides for", "presentation about",
  "make a ppt", "PowerPoint". This applies even when the user mentions an existing .pptx as
  input — the output is always a fresh Poetics-branded deck, so this skill still owns the
  workflow.
---

# Brand decks

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

---

## Reference file

```bash
cat "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/brand.md"
```

---

## How to build a deck

1. Draft the deck as structured JSON matching this schema (see
   `${CLAUDE_PLUGIN_ROOT}/../../brand-kit/scripts/build-deck.py`'s docstring for the authoritative
   version):

```json
{
  "title": "Deck title",
  "footer": "poeticsvr.com",
  "slides": [
    {"type": "title", "eyebrow": "Partner overview · July 2026", "title": "A new way *to experience* art", "subtitle": "..."},
    {"type": "statement", "eyebrow": "Poetics is on a mission to", "text": "Curate and distribute *high-quality* immersive experiences.", "credit": "..."},
    {"type": "section", "title": "The Experience"},
    {"type": "agenda", "title": "What we'll cover", "items": ["The experience", "How it works", "Next steps"]},
    {"type": "content", "eyebrow": "Why it matters", "title": "A new grammar of storytelling", "bullets": ["...", "..."]},
    {"type": "timeline", "title": "How it works", "steps": [{"title": "Curate", "body": "..."}, {"title": "Install", "body": "..."}, {"title": "Operate", "body": "..."}]},
    {"type": "split", "title": "Station setup", "subtitle": "...", "items": [{"title": "VR headsets", "body": "..."}], "image": "/tmp/photo.jpg", "side": "right"},
    {"type": "stats", "title": "Our work in numbers", "stats": [{"value": "1,500+", "label": "screenings delivered", "sublabel": "..."}]},
    {"type": "cards", "title": "Why venues choose Poetics", "cards": [{"title": "Turnkey", "body": "..."}]},
    {"type": "quote", "quote": "It was overwhelming, in the best way.", "attribution": "Marina Spanou, Songwriter & Performer"},
    {"type": "closing", "title": "Thank you.", "contact": "Book a short call or say hello@poeticsvr.com", "cta": "Book a call"}
  ]
}
```

   Wrap 2-4 word phrases in `*asterisks*` to render them in the Cormorant Garamond italic
   emphasis voice (per `brand.md` — use sparingly, once or twice per slide at most).

2. Write it to a temp JSON file, then run the renderer. **Output format is chosen by the output
   file's extension:**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/scripts/build-deck.py" /tmp/deck.json /tmp/deck.html   # primary — self-contained, open anywhere
python3 "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/scripts/build-deck.py" /tmp/deck.json /tmp/deck.pdf    # rendered from the same HTML via Playwright
python3 "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/scripts/build-deck.py" /tmp/deck.json /tmp/deck.pptx   # editable PowerPoint (styled approximation, not pixel-identical to HTML/PDF — see script docstring)
```

3. Present the requested format(s) to the user. Default to HTML + PDF unless they specifically
   need an editable PPTX to hand off.

---

## Slide types — pick the one that matches the content shape

| Type | Use for |
|---|---|
| `title` | Cover: big display bottom-left, optional eyebrow + subtitle |
| `statement` | One centered mission-statement line — the emotional beat of the deck |
| `section` | Divider with an automatic huge ghost numeral (01, 02, ...) |
| `agenda` | Numbered index of what's coming (auto two-column when > 4 items) |
| `content` | Title + bullets (auto two-column when > 5) |
| `timeline` | A process/sequence: numbered steps joined by a hairline (3-5 steps) |
| `split` | Text + rounded image panel — equipment, venues, product shots. Pass a local `image` path; without one a quiet branded placeholder renders |
| `stats` | Big accent numbers — never bury key figures in bullets, give them this slide |
| `cards` | 2-6 parallel points of equal weight |
| `quote` | One testimonial, full-bleed serif |
| `closing` | Thank-you: contact line + CTA pill + huge display title |

Vary the rhythm: don't chain three `content` slides in a row — a stat, quote, or split slide
between text-heavy ones keeps the deck alive. A number that matters deserves `stats`, not a
bullet. One idea per slide.

**Never name or visually identify a specific film** on any slide — describe the program by theme
only.

---

## Asking the right questions

Ask before generating if missing: audience (venue pitch? internal update? investor deck?), topic,
and roughly how many slides / which sections. One question at a time.
