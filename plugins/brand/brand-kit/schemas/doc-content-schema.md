# Document content schema

This is the JSON schema for `scripts/build-doc.py` (Word) and `scripts/build-doc-pdf.py` (PDF).
Both scripts consume the **same payload** — write it once, render to either format.

This schema is tool-agnostic: any AI assistant (or a person) can produce a JSON file matching
this shape, save it, and run the renderer directly from a terminal. The look comes from
`design-system.md` (the website's system: A4, off-white paper, Instrument Serif and Inter Tight,
hairlines, the wordmark, "poeticsvr.com · Confidential" footers) and is applied entirely by the
script. Write the words in the voice of `guides/writing-on-brand-copy.md`.

Proposals, offers and quotes are not documents: they use the A4 quote sheet
(`guides/proposal-playbook.md`).

## Shape

```json
{
  "title":    "Document title",
  "subtitle": "Optional subtitle or omit",
  "date":     "November 2026 · Poetics",
  "theme":    "light",
  "lang":     "en",
  "cover_image": "photo:events-two-visitors-cinematic-11",
  "sections": [
    {
      "heading": "Section heading",
      "html": "<p>Body text.</p><table>...</table>"
    }
  ],
  "separator_title": "Appendix"
}
```

- `title` — required. Set large in the display face on the cover. A short sentence with a full stop.
- `subtitle` — optional, omit or leave `""` to hide.
- `date` — shown at the bottom of the cover. Convention: `"Month YYYY · Poetics"` (no personal names unless asked).
- `sections` — ordered list. Each becomes its own page (PDF) or page break (Word). `heading` is
  optional (renders as an H1 at the top of the section); `html` is required.
- `separator_title` — optional. If present, adds a quiet divider page (e.g. "Appendix.") after
  the last section.
- `theme` — optional: `"light"` (default, off-white paper) or `"dark"` (the dark set, for screen).
  Both renderers follow it.
- `lang` — optional: `"en"` (default) or `"el"`; the footer's own words follow it.
- `confidential` — optional, default `true`: "poeticsvr.com · Confidential" in every footer.
- `cover_image` — optional: a photograph for the cover, as a photo library id (`"photo:<id>"`) or
  a local path.

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
| `<em>`/`<i>` | Rendered upright: the system has no italics. Use words, not styling, for emphasis |
| `<a href="...">` | Link, in the lens blue, underlined (blue means you can act here) |
| `<br>` | Line break |
| `<hr>` | Section divider (hairline rule) |
| `<table><tr><th><td>` | Rows on hairlines, headers in small grey type. Add `class="recommended"` to a column's `<th>`/`<td>` cells to set it on paper-deep |
| `<div class="callout">` | A titled block under a hairline (never a filled box) |
| `<div class="callout-2col">` | Two callouts side by side — wraps two `.callout` children |
| `<div class="callout-title">` / `<div class="callout-body">` | Callout heading / body, used inside a `.callout` div |
| `<div class="eyebrow">` | An overline: small grey sentence-case line above a heading, only when it adds a fact (`As of September 2026`) |
| `<div class="pull-quote">` | A person's words beside a hairline. Wraps `.pull-quote-text` (required) and `.pull-quote-attribution` (optional: name, role) |
| `<div class="stat-row">` | Figures on hairlines, in the display face. Wraps 2–4 `.stat` children, each with `.stat-value` (required), `.stat-label`, `.stat-sublabel` |
| `<div class="price-callout">` | A price set large under a hairline. Wraps `.price-value`, `.price-note`, `.price-body` |
| `<figure>` / `<figcaption>` | Image with a caption |
| `<img src="photo:<id>">` or `<img src="local/path.png">` | A library photograph or a local image (no remote URLs) |

Unknown tags are ignored but their text content is preserved.

### New block structures

```html
<div class="eyebrow">As of September 2026</div>

<div class="pull-quote">
  <div class="pull-quote-text">It was overwhelming, in the best way.</div>
  <div class="pull-quote-attribution">Marina Spanou, composer and performer</div>
</div>

<div class="stat-row">
  <div class="stat">
    <div class="stat-value">5,000+</div>
    <div class="stat-label">screenings at live events</div>
    <div class="stat-sublabel">as of September 2026</div>
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

A number that matters gets `stat-row`, not a bullet, with its as-of date. A price gets
`price-callout`, not a plain `callout`.

## Running the renderers directly (no AI required)

```bash
# Word
python3 scripts/build-doc.py content.json output.docx

# PDF: the version to send (add --preview for a cover image)
python3 scripts/build-doc-pdf.py content.json output.pdf
```

Both scripts self-install their Python dependencies on first run. Nothing about invoking them
requires Claude or any AI — hand a content JSON file to anyone with Python 3 installed and they
get a correctly branded file back.
