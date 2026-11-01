#!/usr/bin/env python3
"""build-doc-pdf.py - render a Poetics document (report, brief, one-pager) as an A4 PDF.

Documents follow brand-kit/design-system.md, the website's design system: off-white paper and
ink (light by default, "theme": "dark" for the dark set), Instrument Serif headings, Inter Tight
text, hairlines instead of boxes, the single-colour wordmark, and "poeticsvr.com · Confidential"
with page numbers in every footer. Fonts are embedded, so the PDF looks the same everywhere.

Proposals, offers and quotes are NOT documents: they are the A4 quote sheet from build-deck.py
(see guides/proposal-playbook.md).

Runs standalone, no AI required:
    python3 build-doc-pdf.py <content.json> <output.pdf> [--preview]

--preview also writes <output>-preview.png (the cover) for a quick look.

content.json: see schemas/doc-content-schema.md (shared with build-doc.py). Top-level fields:
  title (required), subtitle, date, sections: [{heading, html}], separator_title,
  theme: "light" (default) | "dark", lang: "en" (default) | "el", confidential: true (default),
  cover_image: a local path or a photo library id ("photo:<id>").

-- HTML escaping ---------------------------------------------------------------
"html" is trusted HTML: escape user-supplied text before embedding it. title, subtitle, date,
heading and separator_title are escaped automatically.

-- Supported HTML in "html" ------------------------------------------------------
  <h2>-<h6>, <p>, <ul>/<ol><li>, <strong>, <em> (set upright: there are no italics), <a href>,
  <br>, <hr>, <table> (class="recommended" on a column's cells), <figure>/<figcaption>/<img>,
  div.callout (.callout-title, .callout-body), div.callout-2col, div.eyebrow (an overline),
  div.pull-quote (.pull-quote-text, .pull-quote-attribution), div.stat-row (.stat > .stat-value,
  .stat-label, .stat-sublabel), div.price-callout (.price-value, .price-note, .price-body).
"""

import base64
import html as html_lib
import importlib.util as _ilu
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def _load(name, filename):
    spec = _ilu.spec_from_file_location(name, HERE / filename)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_ba = _load("_brand_assets", "_brand_assets.py")
bd = _load("build_deck", "build-deck.py")   # shared tokens, fonts, wordmark, photo library, lint


# -- Preflight ----------------------------------------------------------------------

def check_dependencies():
    """Install Playwright on a fresh machine, and use the system Chrome when Playwright's own
    browser isn't downloaded (some networks block that download). Fixed arguments only."""
    import importlib
    import subprocess
    try:
        importlib.import_module("playwright")
    except ImportError:
        print("Installing playwright (one-time setup)...", file=sys.stderr)
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "playwright"])
        if r.returncode != 0:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "playwright"], check=True)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            exe = pw.chromium.executable_path
        ok = bool(exe) and os.path.exists(exe)
    except Exception:
        ok = False
    if not ok:
        channel = _ba.pick_browser_channel()
        if channel:
            os.environ.setdefault("POETICS_BROWSER_CHANNEL", channel)
            print(f"Bundled Chromium not installed: using system browser ({channel}).", file=sys.stderr)
        else:
            print("Installing Chromium for Playwright (one-time, about 110 MB)...", file=sys.stderr)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


# -- Content helpers ------------------------------------------------------------------

def e(text):
    return html_lib.escape(str(text))


def validate_section_html(sections):
    errors = []
    for i, section in enumerate(sections):
        raw = section.get("html", "")
        for tag in ("div", "table", "tr", "ul", "ol"):
            opens = len(re.findall(rf"<{tag}[\s>/]", raw))
            closes = raw.count(f"</{tag}>")
            if opens != closes:
                errors.append(f'section {i + 1} ("{section.get("heading", "untitled")}"): '
                              f"unbalanced <{tag}> ({opens} open, {closes} close)")
    for err in errors:
        print(f"WARNING: malformed HTML in {err}", file=sys.stderr)


def embed_local_images(html_str, extra_roots=()):
    roots = tuple(_ba.make_allowed_roots(__file__)) + tuple(extra_roots)

    def src_replacer(m):
        q, src = m.group(1), m.group(2)
        if src.startswith("data:") or src.startswith("http"):
            return m.group(0)
        if src.startswith("photo:"):
            uri = bd.resolve_image(src)
        else:
            uri = _ba.resolve_local_image(src, roots)
        if not uri:
            print(f"WARNING: image not found or outside the allowed folders: {src}", file=sys.stderr)
            return m.group(0)
        return f"src={q}{uri}{q}"

    return re.sub(r"<img\b[^>]*>", lambda t: re.sub(r"""\bsrc=([\"'])([^\"']*)\1""", src_replacer, t.group(0)),
                  html_str)


def lint(data):
    """The same copy rules as decks (guides/anti-slop.md), as warnings."""
    def plain(h):
        return re.sub(r"<[^>]+>", " ", html_lib.unescape(h or ""))
    texts = [("title", data.get("title", "")), ("subtitle", data.get("subtitle", ""))]
    for i, s in enumerate(data.get("sections", []), 1):
        texts += [(f"section {i} heading", s.get("heading", "")), (f"section {i}", plain(s.get("html", "")))]
    for where, t in texts:
        bd.lint_text(where, t)
        for m in bd.EMAIL_RE.findall(t):
            if m.lower() != bd.HOUSE_EMAIL:
                bd.warn(where, f"email {m}: use {bd.HOUSE_EMAIL} only")
        m = bd.TAGLINE_RE.search(t)
        if m:
            bd.warn(where, f'sounds like AI copy ("{m.group(0)}"): say it plainly')
        if not data.get("allow_team_names"):
            m = bd.TEAM_RE.search(t)
            if m:
                bd.warn(where, f'names the team ("{m.group(0)}"): leave the makers out unless asked')


# -- HTML -------------------------------------------------------------------------------

DOC_CSS = """
:root { --display: 'Instrument Serif', 'Iowan Old Style', Georgia, serif;
        --sans: 'Inter Tight', ui-sans-serif, system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif; }
html { __THEME__; background: var(--paper); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--sans); font-size: 10.5pt; line-height: 1.6; color: var(--ink);
       -webkit-font-smoothing: antialiased; font-kerning: normal; }

/* A4, the paper colour into the margins, the wordmark top-left, the footer bottom. */
@page { size: 210mm 297mm; margin: 34mm 20mm 24mm; background: var(--paper);
  @top-left { content: __WORDMARK__; vertical-align: bottom; padding-bottom: 12mm; }
  @bottom-left { content: "__FOOTER__"; font: 8pt 'Inter Tight', sans-serif; color: var(--ink-soft);
                 vertical-align: top; padding-top: 6mm; }
  @bottom-right { content: counter(page) " __OF__ " counter(pages); font: 8pt 'Inter Tight', sans-serif;
                  color: var(--ink-soft); vertical-align: top; padding-top: 6mm; } }
@page :first { @top-left { content: none; } @bottom-right { content: none; } }

/* Cover: the wordmark, the title in the display face, an optional photograph, the date. */
.cover { height: 236mm; display: flex; flex-direction: column; break-after: page; }
.cover .wordmark { height: 16pt; width: auto; color: var(--ink); align-self: flex-start; }
.cover .middle { margin-top: auto; }
.cover .photo { margin: 18mm 0 14mm; height: 92mm; border-radius: 16pt; overflow: hidden; background: var(--paper-deep); }
.cover .photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cover-title { font-family: var(--display); font-weight: 400; font-size: 44pt; line-height: 1.05;
               letter-spacing: -0.02em; max-width: 16ch; text-wrap: balance; }
.cover-subtitle { font-size: 13pt; line-height: 1.5; color: var(--ink-soft); margin-top: 12pt; max-width: 40em; }
.cover-date { font-size: 9pt; color: var(--ink-soft); margin-top: 18mm; }

/* Body */
.body-section { break-before: page; }
.body-section:first-of-type { break-before: auto; }
h1 { font-family: var(--display); font-weight: 400; font-size: 26pt; line-height: 1.1; letter-spacing: -0.02em;
     margin: 0 0 16pt; max-width: 22ch; text-wrap: balance; }
h2 { font-size: 13.5pt; font-weight: 500; line-height: 1.3; margin: 20pt 0 6pt; }
h3 { font-size: 11.5pt; font-weight: 500; line-height: 1.35; margin: 16pt 0 4pt; }
h4 { font-size: 10.5pt; font-weight: 500; margin: 12pt 0 4pt; }
h5, h6 { font-size: 9pt; font-weight: 400; color: var(--ink-soft); margin: 12pt 0 4pt; }
h2, h3, h4, h5, h6 { break-after: avoid; text-wrap: balance; }
p { margin: 0 0 9pt; max-width: 42em; text-wrap: pretty; }
strong, b { font-weight: 500; }
em, i { font-style: normal; }
a { color: var(--lens); text-decoration: underline; text-decoration-thickness: 0.5pt; text-underline-offset: 2pt; }
ul, ol { margin: 0 0 10pt 14pt; max-width: 42em; }
li { margin-bottom: 4pt; padding-left: 2pt; }
li::marker { color: var(--ink-soft); }
hr { border: 0; border-top: 0.75pt solid var(--shade); margin: 16pt 0; }

/* Tables: rows on hairlines; a recommended column on paper-deep. */
table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 6pt 0 14pt; break-inside: avoid; font-size: 9.5pt; }
th { text-align: left; font-weight: 400; font-size: 8.5pt; color: var(--ink-soft); padding: 0 10pt 6pt 0; vertical-align: bottom; }
td { border-top: 0.75pt solid var(--shade); padding: 7pt 10pt 7pt 0; vertical-align: top; }
tr:last-child td { border-bottom: 0.75pt solid var(--shade); }
td:first-child { font-weight: 500; }
th.recommended, td.recommended { background: var(--paper-deep); padding-left: 10pt; }
th.recommended { color: var(--ink); border-radius: 9pt 9pt 0 0; padding-top: 6pt; }
tr:last-child td.recommended { border-radius: 0 0 9pt 9pt; }

/* Callouts: a hairline above, never a box. */
.callout { border-top: 0.75pt solid var(--shade); padding-top: 9pt; margin: 12pt 0 14pt; break-inside: avoid; }
.callout-title { font-weight: 500; font-size: 11pt; margin-bottom: 4pt; }
.callout-body { color: var(--ink-soft); }
.callout-2col { display: grid; grid-template-columns: 1fr 1fr; column-gap: 18pt; margin: 12pt 0 14pt; }
.callout-2col .callout { margin: 0; }

.eyebrow { font-size: 9pt; color: var(--ink-soft); margin: 0 0 6pt; }

.pull-quote { border-left: 0.75pt solid var(--shade); padding-left: 14pt; margin: 16pt 0 18pt; break-inside: avoid; }
.pull-quote-text { font-size: 14pt; line-height: 1.5; max-width: 34em; }
.pull-quote-attribution { font-size: 9.5pt; color: var(--ink-soft); margin-top: 8pt; }

.stat-row { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; column-gap: 18pt; margin: 12pt 0 16pt; break-inside: avoid; }
.stat { border-top: 0.75pt solid var(--shade); padding-top: 9pt; }
.stat-value { font-family: var(--display); font-size: 34pt; line-height: 1; letter-spacing: -0.02em; }
.stat-label { font-size: 9.5pt; color: var(--ink-soft); margin-top: 6pt; }
.stat-sublabel { font-size: 8.5pt; color: var(--ink-soft); margin-top: 2pt; }

.price-callout { border-top: 0.75pt solid var(--shade); padding-top: 10pt; margin: 16pt 0; break-inside: avoid; }
.price-value { font-family: var(--display); font-size: 40pt; line-height: 1; letter-spacing: -0.02em; }
.price-note { font-size: 10pt; color: var(--ink-soft); margin-top: 6pt; }
.price-body { margin-top: 8pt; max-width: 42em; }

figure { margin: 12pt 0 14pt; break-inside: avoid; }
figure img, p img { width: 100%; height: auto; border-radius: 12pt; display: block; }
figcaption { font-size: 8.5pt; color: var(--ink-soft); margin-top: 6pt; }

/* Separator: a quiet page with the title set low. */
.separator { break-before: page; height: 236mm; display: flex; align-items: flex-end; }
.separator h1 { font-size: 40pt; margin: 0; }
"""


def wordmark_uri(ink):
    svg = (bd.LOGOS / "wordmark-mono.svg").read_text(encoding="utf-8").replace('fill="#121614"', f'fill="{ink}"')
    svg = re.sub(r'\swidth="[^"]*"', ' width="111"', svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', ' height="15"', svg, count=1)
    return 'url("data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode() + '")'


def build_html(data, extra_roots=()):
    theme = data.get("theme", "light")
    if theme not in bd.THEMES:
        theme = "light"
    lang = data.get("lang", "en") if data.get("lang") in bd.LABELS else "en"
    labels = bd.LABELS[lang]
    tokens = bd.THEMES[theme]
    footer = "poeticsvr.com" + (f" · {labels['confidential']}" if data.get("confidential", True) else "")
    css = (DOC_CSS.replace("__THEME__", bd.theme_vars(theme))
           .replace("__WORDMARK__", wordmark_uri(tokens["ink"]))
           .replace("__FOOTER__", footer.replace('"', '\\"'))
           .replace("__OF__", labels["of"]))

    photo = ""
    if data.get("cover_image"):
        uri = bd.resolve_image(data["cover_image"])
        if uri:
            photo = f'<div class="photo"><img src="{uri}" alt=""></div>'
        else:
            print(f"WARNING: cover_image not found: {data['cover_image']}", file=sys.stderr)

    sections = ""
    for s in data.get("sections", []):
        head = f"<h1>{e(s['heading'])}</h1>" if s.get("heading") else ""
        sections += f'<section class="body-section">{head}{embed_local_images(s.get("html", ""), extra_roots)}</section>\n'
    sep = f'<section class="separator"><h1>{e(data["separator_title"])}</h1></section>' if data.get("separator_title") else ""
    sub = f'<div class="cover-subtitle">{e(data["subtitle"])}</div>' if data.get("subtitle") else ""
    date = f'<div class="cover-date">{e(data["date"])}</div>' if data.get("date") else ""

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head><meta charset="utf-8"><title>{e(data.get('title', 'Poetics'))}</title>
<style>
{bd.font_face_css()}
{css}
</style></head>
<body>
<section class="cover">
  {bd.wordmark_svg()}
  {photo}
  <div class="middle"><div class="cover-title">{e(data.get('title', ''))}</div>{sub}</div>
  {date}
</section>
{sections}{sep}
</body></html>"""


# -- Render ------------------------------------------------------------------------------

def render_pdf(html, pdf_path, preview_path=None):
    import tempfile
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as tmp:
        page_path = pathlib.Path(tmp) / "doc.html"
        page_path.write_text(html, encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch(channel=os.environ.get("POETICS_BROWSER_CHANNEL") or None)
            page = browser.new_page(viewport={"width": 794, "height": 1123})
            page.goto(page_path.as_uri())
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            if preview_path:
                page.screenshot(path=preview_path, clip={"x": 0, "y": 0, "width": 794, "height": 1123})
            page.pdf(path=str(pdf_path), print_background=True, prefer_css_page_size=True)
            browser.close()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit("usage: build-doc-pdf.py <content.json> <output.pdf> [--preview]")
    content_path, out = pathlib.Path(args[0]), pathlib.Path(args[1])
    try:
        data = json.loads(content_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"ERROR: cannot read {content_path}: {err}")
    if not data.get("title"):
        sys.exit('ERROR: content JSON needs a "title"')
    if not data.get("sections"):
        sys.exit('ERROR: content JSON needs at least one entry in "sections"')

    check_dependencies()
    validate_section_html(data["sections"])
    lint(data)
    bd._ALLOWED_EXTRA.append(content_path.resolve().parent)
    html = build_html(data, extra_roots=(content_path.resolve().parent,))
    preview = str(out.with_name(out.stem + "-preview.png")) if "--preview" in sys.argv else None
    render_pdf(html, out, preview)
    print(f"Wrote {out}")
    if preview:
        print(f"Cover preview: {preview}")
    seen = []
    for w in bd.WARNINGS:
        if w not in seen:
            seen.append(w)
    if seen:
        print(f"\n{len(seen)} warning(s):", file=sys.stderr)
        for w in seen:
            print(f"  - {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
