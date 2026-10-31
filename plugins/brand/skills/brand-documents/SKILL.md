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
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/schemas/doc-content-schema.md"
```

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
    ├── Output: Word doc (.docx)?
    │   └── python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-doc.py" \
    │         /tmp/<name>.json <output.docx>
    │       Dark cover page + light, readable body pages (see the script's docstring for why).
    │
    └── Output: PDF? (recommended — the canonical branded format, full dark-brand fidelity)
        └── python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-doc-pdf.py" \
              /tmp/<name>.json <output.pdf>
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

**Never name or visually identify a specific film** in generated content — describe the program
by theme only, per `brand.md`.
