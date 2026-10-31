---
name: brand-proposals
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for any proposal, offer, or quote document from Poetics to another company —
  venues, museums, festivals, schools, event spaces. Takes priority over brand-documents and the
  generic docx/pdf skills for these. Trigger on: "write a proposal", "proposal for", "make an
  offer", "send them an offer", "quote", "quotation", "pricing document", "how much for", "put
  together a pitch document". Do NOT trigger for pitch decks or slides (those go to brand-decks)
  or for general reports/briefs with no commercial ask (those go to brand-documents).
---

# Brand proposals

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first — it defines create/edit/extraction mode and
the full routing rules.

---

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/proposal-playbook.md"
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/schemas/doc-content-schema.md"
```

The playbook is the heart of this skill: it defines the four proposal modes, their exact section
structures, the pricing rules, and the questions to ask. Follow it, not memory.

---

## Input handling

The user can start from either end — both land in the same content JSON → renderer pipeline:

- **Describes the document** (create): interview per the playbook checklist (client, occasion,
  scale, dates, price…), write the content yourself following the mode's structure, render.
- **Provides their own text** (paste, file, notes, URL): first determine intent — **verbatim** or
  **raw material**. If unclear, ask once: "Use your text as-is, or should I rewrite it in the
  Poetics voice?"
  - *Verbatim*: preserve their wording; your job is only to map it onto the mode's structure
    (sections, tables, callouts, price callout) and HTML-escape it. Fix nothing but obvious
    typos; flag structural gaps (no price, no validity, no acceptance close) instead of silently
    inventing content to fill them.
  - *Raw material*: extract the facts (client, scope, dates, figures), then write the document
    in brand voice per the playbook, as in create mode. Facts still come only from their text or
    their answers — never invented.

Either way the brand (fonts, colors, logo, cover, layout) is applied entirely by the renderer —
never hand-style.

---

## Decision tree

```
User request
│
├── Deck/slides asked for? → NOT this skill → brand-decks
│
├── Text/source material provided? → verbatim or raw material (see Input handling)
│
├── Which mode? (ask once if unclear — see playbook)
│   ├── First contact, sell the experience      → pitch   (6–7 sections)
│   ├── Warm client, firm scope, ready to sign  → offer   (3 sections + signatures)
│   ├── Budget/scale unknown, offer sizes       → tiered  (4 sections, Chamber/Gallery/Forum)
│   └── "Just send the price", repeat client    → quote   (1 section)
│
└── Build content JSON per the playbook's structures, then render:
    python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-doc-pdf.py" \
      /tmp/<name>.json "Poetics-Proposal-<Client>-<YYYY-MM>.pdf"
    (.docx via build-doc.py only if the client needs an editable file)
    Printable/procurement context? Add "theme": "light" to the JSON —
    white body pages, dark brand cover kept.
```

---

## Hard rules

- **One all-inclusive figure** is the default pricing presentation (per proposal, or per tier).
  Itemized line prices only if the user explicitly asks. Add-ons may carry their own prices.
- **Never invent a price, date, term, or proposal number** — every commercial fact comes from the
  user. Unconfirmed figures render as an explicit `€ [TBC]`, never a plausible-looking guess.
- **Never name or visually identify a specific film** — themes only, per `brand.md`.
- Escape all user-provided text before embedding it in the `html` field (the renderer escapes
  `title`, `subtitle`, `date`, `heading`, and `separator_title` automatically).
- Table cells holding prices need `style="text-align:right;white-space:nowrap"`.

---

## Asking the right questions

The playbook's final section has the full checklist (mode, client, occasion, scale & dates,
price, terms, number). Ask one question at a time and skip anything already given. The price is
the one question that can never be skipped or guessed.
