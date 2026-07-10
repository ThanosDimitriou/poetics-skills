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
    {"type": "title", "title": "A new way *to experience* art", "subtitle": "Curate → Install → Operate"},
    {"type": "section", "title": "The Experience"},
    {"type": "content", "title": "How it works", "bullets": ["Curate: ...", "Install: ...", "Operate: ..."]},
    {"type": "cards", "title": "Why venues choose Poetics", "cards": [{"title": "Turnkey", "body": "..."}]},
    {"type": "quote", "quote": "It was overwhelming, in the best way.", "attribution": "Marina Spanou, Songwriter & Performer"},
    {"type": "closing", "title": "Bring it to your venue", "cta": "Book a call"}
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

## Slide types

`title` (cover), `section` (divider), `content` (title + bullets), `cards` (title + 2-3 cards),
`quote` (pull quote + attribution), `closing` (title + CTA pill). Pick the type that matches the
content shape — don't force everything into `content`.

**Never name or visually identify a specific film** on any slide — describe the program by theme
only.

---

## Asking the right questions

Ask before generating if missing: audience (venue pitch? internal update? investor deck?), topic,
and roughly how many slides / which sections. One question at a time.
