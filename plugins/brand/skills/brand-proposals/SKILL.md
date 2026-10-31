---
name: brand-proposals
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for any proposal, offer, or quote from Poetics to another company: venues,
  museums, festivals, brands, agencies, schools. Every proposal is a practical A4 document (the
  quote sheet) built with the deck renderer. Takes priority over brand-documents and the generic
  docx/pdf skills for these. Trigger on: "write a proposal", "proposal for", "make an offer", "send
  them an offer", "quote", "quotation", "pricing document", "how much for", "προσφορά". Do NOT
  trigger for general reports or briefs with no commercial ask (those go to brand-documents), or
  for a pitch that needs photographs and a story (that is a standard deck: brand-decks).
---

# Brand proposals

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/proposal-playbook.md"   # the shape, modes, pricing rules
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/deck-copy.md"           # the voice
cat "${CLAUDE_PLUGIN_ROOT}/skills/brand-decks/SKILL.md"             # page templates, rules, render
```

A proposal is the deck skill's **proposal variant**: a practical A4 document, no cover, no closing
page, no photographs. The playbook defines its shape (the D3 quote sheet: to, heading, intro,
scope, capacity, price; the date and scope disclaimer in every footer) and the four modes.

---

## Workflow

1. **Mode** (ask once if unclear): just the price → **quote** (1 page) · scope agreed →
   **offer** (quote sheet + terms and signatures) · size unknown → **tiered** · first contact →
   **pitch** (practical; a pitch that needs photos and a story is a standard deck instead).
2. **Facts**, one question at a time, skipping what's given (playbook, last section): client and
   addressee, event or venue and dates, scope, **the price** (never guessed), terms, number,
   Greek or English.
3. **The user's own text** (an earlier proposal, notes): ask once, verbatim or raw material, then
   map it onto the quote sheet (playbook, "Working from provided text").
4. **Build** from `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/decks/quote.json` or `proposal.json`.
   Set `"kind": "proposal"`, `"mode"`, `"to"`, `"date"`, `"number"`, `"lang"` (`"el"` for Greek),
   and `"disclaimer"` when the client's wording differs from the default. Remove `"draft"` once
   every figure is confirmed.
5. **Render and look:**
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-deck.py" proposal.json proposal.html --sheet
   python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-deck.py" proposal.json "Poetics-Proposal-<Client>-<YYYY-MM>.pdf"
   ```
   Read the page images. Fix every warning (spacing guardrail, overflow, copy) by changing the
   content, then re-render. Deliver the PDF; say what's still a placeholder.

## Hard rules

- **One all-inclusive figure**, excl. VAT. Line-item prices only if the user asks; add-ons may
  have their own prices.
- **Never invent a price, date, term or number.** An unconfirmed figure makes the document a
  draft, and you say so.
- Never name or show a film: describe the program by theme.
- The deck rules apply: say less, the website's voice, hello@poeticsvr.com only, no personal
  names unless asked, "Confidential" in the footer.
