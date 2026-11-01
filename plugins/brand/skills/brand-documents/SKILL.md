---
name: brand-documents
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill to create any branded Poetics document or PDF. Takes priority over the generic
  docx and pdf skills for all document creation requests. Trigger on: "write a doc", "create a
  doc", "make a report", "write a brief", "one-pager", "Word doc", "branded document",
  "Poetics document", "create a pdf", "pdf report", "turn this into a doc", "convert this to a
  pdf". Do NOT trigger for deck/presentation requests (those go to brand-decks), for
  proposals/offers/quotes to other companies (those go to brand-proposals), or for
  reading/editing an existing PDF (that goes to the pdf skill).
---

# Brand documents

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first — it defines create/edit/extraction mode and
the full routing rules.

---

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/schemas/doc-content-schema.md"     # the content JSON
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"                  # how it looks (applied by the scripts)
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # company facts
```

Documents follow the website's design system, like decks: A4, off-white paper (or `"theme":
"dark"`), Instrument Serif headings, Inter Tight text, hairlines instead of boxes, the
wordmark, and "poeticsvr.com · Confidential" with page numbers in every footer. The scripts
apply all of it; your job is the content.

---

## Decision tree

```
User request
│
├── Provides source material (URL, file, thread, paste)?
│   └── YES → Content extraction mode (see GLOBAL_RULES.md): extract → structure → generate
│
├── Attaches existing .docx?
│   └── YES → Edit mode: read with the docx skill, apply changes, preserve brand styles
│
└── No existing file → Create mode
    │
    ├── Output: PDF? (default: the version to send, fonts embedded)
    │   └── python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-doc-pdf.py" \
    │         /tmp/<name>.json <output.pdf> --preview
    │
    └── Output: Word doc (.docx)? (only when someone must edit it in Word)
        └── python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-doc.py" \
              /tmp/<name>.json <output.docx>
            Same look; needs Instrument Serif and Inter Tight installed to show as designed.
```

Both renderers consume the same content JSON schema — write it once. Build the content as
structured JSON matching `doc-content-schema.md`, write it to a temp file, run the renderer,
present the file to the user. Do not hand-build the document with the bare `docx`/`pdf` skills —
the renderer applies the brand's type scale, colors, and fonts mechanically; your job is
well-structured content, not styling.

**Escaping rule:** escape all user-provided text with an HTML-escape step before embedding it in
the `html` field. The scripts auto-escape `title`, `subtitle`, `date`, `heading`, and
`separator_title`.

---

## Asking the right questions

Ask before generating if any of these are missing (one question at a time, skip what's already
given):

| Missing | Ask |
|---|---|
| Topic / purpose | "What's this document about?" |
| Audience | "Who's reading it — a venue, a partner, internal?" |
| Key sections | "What are the main sections? Give me headings or a rough outline." |
| Output format | "Word doc or PDF?" (ask only if not clear from the request) |

For content extraction mode, ask only if the source doesn't make the audience or key message
obvious — one question maximum.

## Writing rules

The website's voice (`writing-on-brand-copy.md`): plain, concrete, "we" and "you", short
sentences, headings as short sentences with a full stop, no em dashes, no hype. Overlines
(`eyebrow`) only when they add a fact; true counts, not threes; figures with their as-of date;
hello@poeticsvr.com only; no names of the people who made it unless asked. The PDF renderer warns
on em dashes, stock phrases, other emails and team names: fix them.

Photographs: `<img src="photo:<id>">` uses the Poetics photo library (see the deck skill), or a
local path. `"cover_image"` puts one on the cover.

**Never name or visually identify a specific film**: describe the program by theme only.
**Proposals, offers and quotes are not documents**: they go to `brand-proposals` (the A4 quote
sheet).
