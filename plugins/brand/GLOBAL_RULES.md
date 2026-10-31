# Global rules, brand plugin

These rules apply to every skill in this plugin. Read this before doing anything else.

---

## Where the brand knowledge lives

The brand spec, assets, and renderer scripts live in `brand-kit/` inside this plugin
(`${CLAUDE_PLUGIN_ROOT}/brand-kit`), so an installed copy of the plugin carries everything it needs.
The repo root has a `brand-kit` symlink to the same folder, so the MCP server, the docs and anyone
working outside Claude Code use the same files (see `brand-kit/guides/using-outside-claude-code.md`).

Before answering any brand question, generating any output, or reviewing any asset, read the
spec:

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"
```

This is the source of truth for colors, typography, logo rules, voice/tone, and company
facts. **Decks are the exception for visuals:** they follow `brand-kit/design-system.md` (the
website's design system for slides), and `brand-kit/guides/anti-slop.md` lists the patterns no
generated asset should carry. If it hasn't been populated yet on some point, say so — do not invent values. If the file
flags an "Open question," surface it rather than picking silently.

---

## Skill routing priority

When the user's request involves a **presentation, slide deck, or pitch deck**, the `brand-decks`
skill takes priority over the generic `pptx` skill. Use `brand-decks` for every request that
produces a new deck or rebrands an existing one.

Trigger phrases that route to `brand-decks`, not `pptx`: "make a deck", "build a deck", "create a
deck", "Poetics deck", "branded deck", "pitch deck", "slides for", "presentation about", "make a
ppt", "PowerPoint".

**When the user asks for a Word document, report, brief, one-pager, or `.docx` file**, this
plugin takes priority over the generic `docx` skill. Determine intent first:

- **Create mode** (default): no existing file — generate from scratch via `brand-documents`,
  which calls `brand-kit/scripts/build-doc.py`. Produce structured content JSON per
  `brand-kit/schemas/doc-content-schema.md`; do not hand-build the document with the bare `docx`
  skill.
- **Edit mode**: user attaches an existing `.docx` — read it with the `docx` skill, apply
  changes, preserve brand styles as closely as possible. Don't rebuild from scratch.
- **Content extraction mode**: user provides a URL, doc link, Slack thread, or pasted text and
  asks to "turn this into a doc" — extract and structure the content first, then proceed as
  create mode.

**When the user asks for a PDF document** (not a PDF export of a deck), this plugin takes
priority over the generic `pdf` skill, via `brand-documents` calling
`brand-kit/scripts/build-doc-pdf.py`. PDF is the **canonical** branded document format — it
renders the full dark brand canvas end-to-end with embedded fonts, unlike the Word path's
pragmatic light-body-page compromise (see the docstring in `build-doc.py`). Prefer it whenever
strict brand fidelity matters.

Trigger phrases: "write a doc/document/report/brief", "one-pager", "Word doc", "branded
document", "create a pdf", "pdf report", "turn this into a doc/pdf".

**When the user asks for a proposal, offer, quote, or quotation to another company** (venues,
museums, festivals, brands, agencies, schools), route to `brand-proposals`. It takes priority over
`brand-documents` and the generic `docx`/`pdf` skills. **Every proposal is the practical A4 quote
sheet** rendered by `brand-kit/scripts/build-deck.py` (the deck skill's proposal variant), never
the document scripts. It follows `brand-kit/guides/proposal-playbook.md` (four modes: quote /
offer / tiered / pitch). Trigger phrases: "write a proposal", "proposal for", "make an offer",
"send them an offer", "quote", "quotation", "pricing document", "proposal deck", "προσφορά". A
**pitch deck** with photographs and a story is a standard deck: that routes to `brand-decks`.

**For avatars, video thumbnails, or social carousels**, route to `brand-templates`, which opens
the relevant self-contained editor in `brand-kit/templates/`.

**For "is this on-brand" / review requests**, route to `brand-review`.

**For raw spec lookups** ("what are our colors", "what font do we use"), route to
`brand-identity`. **For "can I do X" application questions**, route to `brand-guidelines`.

---

## Content extraction

When the user provides source material (URL, doc link, Slack thread, attached PDF, pasted text)
and asks to turn it into a doc, PDF, or deck:

1. **Fetch/read the source** using the appropriate tool available in the session.
2. **Structure the content**: identify title, sections, and supporting details. Summarize and
   reorganize into the target format's natural hierarchy — don't copy verbatim.
3. **Clarify gaps**: if title, date, or audience isn't obvious from the source, ask once before
   generating.
4. **Route to the correct generator**: `build-doc.py` / `build-doc-pdf.py` for documents,
   `build-deck.py` for decks. Don't mix generators.

---

## Output rules

- Never invent brand values, colors, fonts, or company facts not present in `brand.md`.
- Never name or visually identify a specific film in any generated material (hard rule from
  `brand.md`'s Company section).
- When reviewing assets, produce specific and actionable feedback — "off-brand" is not feedback;
  "the heading uses #333 instead of the brand accent #0099FF" is.
- All renderer scripts run standalone from a terminal too — when in doubt about a styling
  decision, prefer letting the script apply it mechanically over hand-crafting HTML/CSS/DOCX
  styling inline.

---

## Who maintains this

Owner: Thanos Dimitriou (dimitriouathanas@gmail.com). To update the brand, edit
`brand-kit/brand.md` directly — no build step, no PR review required.
