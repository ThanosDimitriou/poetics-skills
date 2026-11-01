---
name: brand-review
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill to review any asset against Poetics brand guidelines and get structured feedback
  with a compliance score. Trigger on: "review this", "check this against brand", "is this
  on-brand", "brand review", "brand check", "brand audit", "review my deck", "review this
  document", "review this proposal", "review this social post". Accepts: screenshots, images,
  PPTX/DOCX/PDF files, deck JSON, URLs.

---

# Brand review

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"                  # visuals: decks, proposals, documents
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/anti-slop.md"               # the deck rules and slop patterns
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # company, logo, legacy social spec
```

Review against the system that applies: decks, proposals and documents against
`design-system.md`; the social templates against `brand.md`'s legacy spec. Copy, for everything,
against the voice guide and `anti-slop.md`.

**If it's a deck or proposal made with this kit** (a deck JSON, or you can get one), let the
renderer check it first. It catches most rule breaks mechanically:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-deck.py" deck.json /tmp/review.html --sheet
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/audit-deck.py" deck.json    # curation decks, external facts
```

Use its warnings and layout problems as findings, then look at the page images for what a script
can't judge.

## What to check, in order

1. **Hard rules:** a named or shown film outside a curation deck; an invented figure, quote, name
   or price; confidential material; a personal email or the makers named without being asked.
2. **Visual system:** the colour roles (blue only on what can be pressed, one accent, off-white
   paper, never `#FFFFFF`); Instrument Serif and Inter Tight at the right sizes; the wordmark;
   space and hairlines, not boxes, shadows or gradients; the spacing guardrail (72px clear below
   the wordmark, no overlaps, nothing crowding the footer).
3. **Deck rules:** say less, white space, few overlines, true counts not threes, filler pages
   justified, footer "poeticsvr.com · Confidential", the closing page offers only the email.
   Proposals: no cover or closing page, the price never guessed, the date and scope disclaimer in
   the footer.
4. **Voice:** website voice, headings as short plain sentences with a full stop, no em dashes,
   no stock phrases from `anti-slop.md`.

## Review format

**Brand compliance score: X/10**
- Critical issues, −1.5 to −2 each: anything under hard rules; the wrong visual system (the old
  dark look on a deck, a second accent colour, wrong fonts); logo misuse.
- Minor issues, −0.5 to −1 each: a deck-rule break, a spacing or size slip, a voice slip.
- Never give a score without the issues that drove it. 8+ is ready with small fixes; under 6
  needs rework.

**What's on-brand:** specific elements, and why they pass.

**What needs fixing:** for each, the element, the problem (with the value used), the fix (citing
the exact token or rule, e.g. "the heading uses #0099FF; links and buttons use lens `#16249C`"),
and the severity.

**Summary:** one or two sentences, and the single most important fix.
