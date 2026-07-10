# Document content schema

This is the JSON schema for `scripts/build-doc.py` (Word) and `scripts/build-doc-pdf.py` (PDF).
Both scripts consume the **same payload** — write it once, render to either format.

This schema is tool-agnostic: any AI assistant (or a person) can produce a JSON file matching
this shape, save it, and run the renderer script directly from a terminal. The brand (colors,
fonts, logo, layout) is applied entirely by the script — the content author never has to think
about styling.

## Shape

```json
{
  "title":    "Document title",
  "subtitle": "Optional subtitle or omit",
  "date":     "July 2026 · Author or team name",
  "sections": [
    {
      "heading": "Section heading",
      "html": "<p>Body text.</p><table>...</table>"
    }
  ],
  "separator_title": "Appendix"
}
```

- `title` — required. Rendered large on the dark cover page.
- `subtitle` — optional, omit or leave `""` to hide.
- `date` — shown at the bottom of the cover page. Convention: `"Month YYYY · context"`.
- `sections` — ordered list. Each becomes its own page (PDF) or page break (Word). `heading` is
  optional (renders as an H1 at the top of the section); `html` is required.
- `separator_title` — optional. If present, adds a divider page (e.g. for an "Appendix") after
  the last section.

## The `html` field

A limited, well-formed HTML subset. **Escape all user-provided text with an HTML-escape function
before embedding it** — the renderer escapes `title`, `subtitle`, `date`, `heading`, and
`separator_title` automatically, but not the contents of `html`.

Supported elements:

| Tag | Renders as |
|---|---|
| `<h2>`–`<h6>` | Sub-headings (h1 is reserved for the section `heading`) |
| `<p>` | Body paragraph |
| `<ul><li>` | Bullet list |
| `<strong>`/`<b>` | Bold inline |
| `<em>`/`<i>` | Italic inline — in Poetics documents, prefer this for the Cormorant Garamond emphasis voice (short 2–4 word phrases only, per `brand.md`) |
| `<a href="...">` | Link, inherits body color, no underline |
| `<br>` | Line break |
| `<table><tr><th><td>` | Data table |
| `<div class="callout">` | Single-column callout box |
| `<div class="callout-2col">` | Two-column callout — wraps two `.callout` children |
| `<div class="callout-title">` / `<div class="callout-body">` | Callout heading / body, used inside a `.callout` div |
| `<img src="local/path.png">` | Local image only (no remote URLs or data URIs in the Word path) |

Unknown tags are ignored but their text content is preserved.

## Running the renderers directly (no AI required)

```bash
# Word
python3 scripts/build-doc.py content.json output.docx

# PDF (recommended when the dark brand background matters — see brand.md)
python3 scripts/build-doc-pdf.py content.json output.pdf
```

Both scripts self-install their Python dependencies on first run. Nothing about invoking them
requires Claude or any AI — hand a content JSON file to anyone with Python 3 installed and they
get a correctly branded file back.
