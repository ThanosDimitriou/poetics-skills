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
- `theme` — optional, PDF renderer only: `"dark"` (default, canonical brand canvas) or
  `"light"` (white body pages for print-friendly/procurement contexts — the dark brand cover and
  separator pages are kept, and the body logo mark switches to the dark variant). The Word
  renderer already renders light body pages by design and ignores this field.

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
| `<hr>` | Section divider (hairline rule) |
| `<table><tr><th><td>` | Data table. Add `class="recommended"` to a `<th>`/`<td>` to highlight that column (tiered-comparison proposals) |
| `<div class="callout">` | Single-column callout box |
| `<div class="callout-2col">` | Two-column callout — wraps two `.callout` children |
| `<div class="callout-title">` / `<div class="callout-body">` | Callout heading / body, used inside a `.callout` div |
| `<div class="eyebrow">` | Small mono kicker label above a heading (e.g. `01 — The Experience`) |
| `<div class="pull-quote">` | Inner-voice / testimonial quote. Wraps `.pull-quote-text` (required) and `.pull-quote-attribution` (optional) |
| `<div class="stat-row">` | Row of big accent numbers. Wraps 2–4 `.stat` children, each with `.stat-value` (required), `.stat-label`, `.stat-sublabel` |
| `<div class="price-callout">` | Elevated pricing block — the proposal playbook's price figure. Wraps `.price-value`, `.price-note`, `.price-body` |
| `<figure>` / `<figcaption>` | Image with a caption |
| `<img src="local/path.png">` | Local image only (no remote URLs or data URIs in the Word path) |

Unknown tags are ignored but their text content is preserved.

### New block structures

```html
<div class="eyebrow">01 — The Experience</div>

<div class="pull-quote">
  <div class="pull-quote-text">It was overwhelming, in the best way.</div>
  <div class="pull-quote-attribution">Marina Spanou, Songwriter &amp; Performer</div>
</div>

<div class="stat-row">
  <div class="stat">
    <div class="stat-value">1,500+</div>
    <div class="stat-label">screenings delivered</div>
    <div class="stat-sublabel">across three venue types</div>
  </div>
  <!-- 1-3 more .stat siblings -->
</div>

<div class="price-callout">
  <div class="price-value">€ 18,600</div>
  <div class="price-note">All-inclusive · Gallery configuration</div>
  <div class="price-body">Curation, delivery, installation, operation, hygiene, and strike. Excludes VAT.</div>
</div>

<table>
  <tr><th>Configuration</th><th class="recommended">Gallery (recommended)</th><th>Forum</th></tr>
  <tr><td>Price</td><td class="recommended" style="text-align:right;white-space:nowrap">€ 18,600</td><td style="text-align:right;white-space:nowrap">€ 32,400</td></tr>
</table>

<figure>
  <img src="/tmp/pod-photo.jpg">
  <figcaption>Single-seat pod, installed at Technopolis.</figcaption>
</figure>
```

A number that matters gets `stat-row`, not a bullet. A price gets `price-callout`, not a plain
`callout` — it's the block a client scans for first, per the proposal playbook's pricing rules,
and it earns a dedicated, more prominent treatment.

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
