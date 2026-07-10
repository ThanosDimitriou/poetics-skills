#!/usr/bin/env python3
"""build-doc-pdf.py - render a branded Poetics document as PDF via HTML + Playwright.

This is the CANONICAL branded document format: unlike build-doc.py (Word),
this renders the full document on the dark brand canvas end-to-end, matching
brand.md exactly (fonts physically embed, glow backgrounds render, accent
color is correct). Use this whenever brand fidelity matters more than
in-place editability.

Runs standalone, no AI required:
    python3 build-doc-pdf.py <content.json> <output.pdf>

content.json schema: see schemas/doc-content-schema.md (same schema shared
with build-doc.py).

-- HTML escaping rules ------------------------------------------------------
The "html" field is trusted HTML - the caller is responsible for escaping
all user-supplied strings before passing them in. Use html.escape(text) on
any value that comes from user input before embedding it in tags. This
script escapes title, subtitle, date, heading, and separator_title
automatically.

-- Supported HTML elements in "html" ----------------------------------------
  <h2>-<h6>        sub-headings (h1 is reserved for "heading" field)
  <p>              body paragraph
  <ul><li>         bullet list
  <strong>/<em>    bold / italic inline (italic renders in Cormorant Garamond)
  <a href="...">   link
  <table><tr><th><td>          data table (break-inside: avoid)
  <div class="callout">        single-column callout box
  <div class="callout-2col">   two-column callout
"""

import asyncio
import base64
import html as html_lib
import importlib.util as _ilu
import json
import os
import pathlib
import re
import sys


# -- Preflight checks ---------------------------------------------------------

def check_dependencies():
    """Verify (and, on a fresh machine, install) the renderer's dependencies.
    Every command uses fixed arguments (no user input), so there is no
    shell-injection surface."""
    import importlib
    import subprocess

    def have(mod):
        try:
            importlib.import_module(mod)
            return True
        except ImportError:
            return False

    for mod, pip_name in (("playwright", "playwright"),):
        if have(mod):
            continue
        print(f"Installing {pip_name} (one-time setup)...", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", pip_name],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            # Older pip (pre-PEP 668) doesn't recognize --break-system-packages.
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", pip_name],
                capture_output=True, text=True,
            )
        if result.returncode != 0 or not have(mod):
            print(f"ERROR: could not install {pip_name}. "
                  f"Run manually: pip install {pip_name}", file=sys.stderr)
            if result.stderr:
                print(result.stderr.strip()[:500], file=sys.stderr)
            sys.exit(1)

    chromium_ok = False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            exe = pw.chromium.executable_path
        chromium_ok = bool(exe) and os.path.exists(exe)
    except Exception:
        chromium_ok = False
    if not chromium_ok:
        print("Installing Chromium for Playwright (one-time, about 110 MB)...", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print("ERROR: could not install Chromium. "
                  "Run manually: python3 -m playwright install chromium", file=sys.stderr)
            if result.stderr:
                print(result.stderr.strip()[:500], file=sys.stderr)
            sys.exit(1)


# -- Asset discovery ------------------------------------------------------------

def find_kit_root():
    script_parent = pathlib.Path(__file__).resolve().parent.parent
    candidates = [
        os.environ.get('BRAND_KIT_ROOT', ''),
        str(script_parent),
    ]
    for c in candidates:
        if c and pathlib.Path(c, 'brand.md').exists():
            return c
    raise FileNotFoundError(
        'Cannot locate brand-kit root (expected to find brand.md there). '
        'Set BRAND_KIT_ROOT or run from within the repo.'
    )


def b64(path):
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Asset not found: {path}')
    return base64.b64encode(p.read_bytes()).decode()


def _bg(root, slot, default_name):
    """Photo override from assets/backgrounds/photo/ if present, else the gradient."""
    photo_dir = pathlib.Path(root) / 'assets/backgrounds/photo'
    for ext in ('.jpg', '.jpeg', '.png', '.webp'):
        cand = photo_dir / f'{slot}{ext}'
        if cand.exists():
            return cand
    return pathlib.Path(root) / 'assets/backgrounds' / default_name


def load_assets(root):
    r = pathlib.Path(root)
    fonts = r / 'assets/fonts'
    required = {
        'cover_bg':   _bg(root, 'doc-cover', 'doc-cover-bg.jpg'),
        'section_bg': _bg(root, 'doc-section', 'doc-section-bg.jpg'),
        'logo_wordmark': r / 'assets/logos/wordmark-light.png',
        'logo_mark':  r / 'assets/logos/mark-light.png',
        'inter_reg':  fonts / 'Inter-Regular.ttf',
        'inter_med':  fonts / 'Inter-Medium.ttf',
        'inter_sb':   fonts / 'Inter-SemiBold.ttf',
        'inter_bold': fonts / 'Inter-Bold.ttf',
        'cormorant_it':  fonts / 'CormorantGaramond-Italic.ttf',
        'mono_reg':   fonts / 'SpaceMono-Regular.ttf',
    }
    missing = [str(v) for v in required.values() if not v.exists()]
    if missing:
        raise FileNotFoundError('Missing assets:\n' + '\n'.join(f'  {m}' for m in missing))

    css_path = r / 'scripts/doc-pdf-styles.css'
    if not css_path.exists():
        raise FileNotFoundError(f'CSS not found: {css_path}')

    assets = {k: b64(str(v)) for k, v in required.items()}
    assets['css'] = css_path.read_text()
    return assets


# -- HTML builder -----------------------------------------------------------------

def e(text):
    """Escape user-provided plain text for safe HTML insertion."""
    return html_lib.escape(str(text))


def validate_section_html(sections):
    try:
        from lxml import etree
    except ImportError:
        return

    errors = []
    for i, section in enumerate(sections):
        raw = section.get('html', '')
        if not raw.strip():
            continue
        etree.fromstring(f'<div>{raw}</div>', parser=etree.HTMLParser(recover=True))
        for tag in ('div', 'table', 'tr', 'ul', 'ol'):
            opens = len(re.findall(rf'<{tag}[\s>/]', raw))
            closes = raw.count(f'</{tag}>')
            if opens != closes:
                errors.append(f'Section {i} ("{section.get("heading","untitled")}"): '
                               f'unbalanced <{tag}> ({opens} open, {closes} close)')

    if errors:
        print('WARNING: malformed HTML detected in sections (will attempt to render anyway):')
        for err in errors:
            print(f'  {err}')


_ba_path = pathlib.Path(__file__).parent / '_brand_assets.py'
_ba_spec = _ilu.spec_from_file_location('_brand_assets', _ba_path)
_ba = _ilu.module_from_spec(_ba_spec)
_ba_spec.loader.exec_module(_ba)  # type: ignore[union-attr]
_IMAGE_EXTS = _ba.IMAGE_EXTS
_IMAGE_MIME = _ba.IMAGE_MIME
_EMBED_ALLOWED_ROOTS = _ba.make_allowed_roots(__file__)


def embed_local_images(html_str):
    def img_replacer(img_match):
        tag = img_match.group(0)

        def src_replacer(m):
            q, src = m.group(1), m.group(2)
            if src.startswith('data:') or src.startswith('http'):
                return m.group(0)
            path = pathlib.Path(src).resolve()
            ext = path.suffix.lower().lstrip('.')
            if ext not in _IMAGE_EXTS:
                return m.group(0)
            if not any(path.is_relative_to(r) for r in _EMBED_ALLOWED_ROOTS):
                print(f'WARNING: image outside allowed paths, skipping embed: {src}')
                return m.group(0)
            if not path.exists():
                print(f'WARNING: image not found, skipping embed: {src}')
                return m.group(0)
            mime = _IMAGE_MIME[ext]
            data = base64.b64encode(path.read_bytes()).decode()
            return f'src={q}data:{mime};base64,{data}{q}'

        return re.sub(r"""\bsrc=([\"'])([^\"']*)\1""", src_replacer, tag)

    return re.sub(r'<img\b[^>]*>', img_replacer, html_str)


def build_html(data, assets):
    title = e(data.get('title', 'Document title'))
    subtitle = e(data.get('subtitle', ''))
    date = e(data.get('date', ''))
    sections = data.get('sections', [])
    sep = data.get('separator_title', '')

    font_css = f"""
@font-face {{ font-family: 'Inter'; font-weight: 400; font-style: normal;
  src: url('data:font/ttf;base64,{assets["inter_reg"]}') format('truetype'); }}
@font-face {{ font-family: 'Inter'; font-weight: 500; font-style: normal;
  src: url('data:font/ttf;base64,{assets["inter_med"]}') format('truetype'); }}
@font-face {{ font-family: 'Inter'; font-weight: 600; font-style: normal;
  src: url('data:font/ttf;base64,{assets["inter_sb"]}') format('truetype'); }}
@font-face {{ font-family: 'Inter'; font-weight: 700; font-style: normal;
  src: url('data:font/ttf;base64,{assets["inter_bold"]}') format('truetype'); }}
@font-face {{ font-family: 'Cormorant Garamond'; font-weight: 400; font-style: italic;
  src: url('data:font/ttf;base64,{assets["cormorant_it"]}') format('truetype'); }}
@font-face {{ font-family: 'Space Mono'; font-weight: 400; font-style: normal;
  src: url('data:font/ttf;base64,{assets["mono_reg"]}') format('truetype'); }}"""

    subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>' if subtitle else ''

    body_sections = ''
    for section in sections:
        heading_html = f'<h1>{e(section["heading"])}</h1>' if section.get('heading') else ''
        header_html = (
            f'<div class="page-header">'
            f'<img src="data:image/png;base64,{assets["logo_mark"]}" alt="Poetics"></div>'
        )
        section_html = embed_local_images(section.get('html', ''))
        body_sections += f'''
<div class="body-section">
  {header_html}
  {heading_html}
  {section_html}
</div>'''

    separator_html = ''
    if sep:
        separator_html = f'''
<div class="page-fixed separator">
  <div class="page-bg" style="background-image:url(\'data:image/jpeg;base64,{assets["section_bg"]}\')"></div>
  <div class="page-content">
    <h1>{e(sep)}</h1>
  </div>
</div>'''

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{font_css}
{assets["css"]}
</style>
</head>
<body>

<div class="page-fixed cover">
  <div class="page-bg" style="background-image:url('data:image/jpeg;base64,{assets["cover_bg"]}')"></div>
  <div class="page-content">
    <div class="cover-logo"><img src="data:image/png;base64,{assets["logo_wordmark"]}" alt="Poetics"></div>
    <div class="cover-middle">
      <div class="cover-title">{title}</div>
      {subtitle_html}
    </div>
    <div class="cover-date">{date}</div>
  </div>
</div>

{body_sections}
{separator_html}

</body>
</html>"""


# -- Playwright renderer -------------------------------------------------------

async def render_pdf(html_path, pdf_path, preview_path=None):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 816, 'height': 1056})
        await page.goto(pathlib.Path(html_path).as_uri())

        try:
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(500)
        except Exception:
            await page.wait_for_timeout(1500)

        font_loaded = await page.evaluate("document.fonts.check('16px \"Inter\"')")
        if not font_loaded:
            print('WARNING: Inter did not load — PDF will use fallback font.')

        if preview_path:
            await page.screenshot(
                path=preview_path,
                clip={'x': 0, 'y': 0, 'width': 816, 'height': 1056},
                full_page=False
            )
            print(f'Preview screenshot: {preview_path}')

        await page.pdf(
            path=pdf_path,
            format='Letter',
            print_background=True,
            display_header_footer=False,
            margin={'top': '0', 'bottom': '0.5in', 'left': '0', 'right': '0'}
        )
        await browser.close()

    # Page numbers from page 2 onward via reportlab overlay, if available.
    try:
        import io as _io
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.pagesizes import letter
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject

        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for i, pg in enumerate(reader.pages):
            writer.add_page(pg)
            if i == 0:
                continue

            buf = _io.BytesIO()
            c = rl_canvas.Canvas(buf, pagesize=letter)
            c.setFont('Helvetica', 9)
            c.setFillColorRGB(0.604, 0.604, 0.596)  # #9A9A98
            c.drawRightString(letter[0] - 36, 25, str(i + 1))
            c.save()
            buf.seek(0)

            overlay = PdfReader(buf).pages[0]
            ov_stream = overlay['/Contents'].get_object()
            ns = DecodedStreamObject()
            ns.set_data(ov_stream.get_data())
            ref = writer._add_object(ns)
            wp = writer.pages[i]
            ck = NameObject('/Contents')
            if ck in wp:
                existing = wp.raw_get(ck)
                if isinstance(existing, ArrayObject):
                    existing.append(ref)
                else:
                    wp[ck] = ArrayObject([existing, ref])
            else:
                wp[ck] = ArrayObject([ref])

        out = _io.BytesIO()
        writer.write(out)
        pathlib.Path(pdf_path).write_bytes(out.getvalue())
    except ImportError:
        pass  # reportlab/pypdf not installed — ship without page numbers rather than fail
    except (AttributeError, KeyError, TypeError, OSError) as ex:
        print(f'WARNING: could not add page numbers ({ex})')


# -- Entry point ----------------------------------------------------------------

def main():
    check_dependencies()

    if len(sys.argv) < 3:
        print('Usage: build-doc-pdf.py <content.json> <output.pdf>')
        print(__doc__)
        sys.exit(1)

    content_path = pathlib.Path(sys.argv[1])
    output_path = sys.argv[2]

    if not content_path.exists():
        print(f'ERROR: content file not found: {content_path}')
        sys.exit(1)

    with open(content_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as ex:
            print(f'ERROR: invalid JSON in {content_path}: {ex}')
            sys.exit(1)

    if not data.get('title'):
        print('ERROR: content JSON must include a "title" field')
        sys.exit(1)
    if not data.get('sections'):
        print('ERROR: content JSON must include at least one entry in "sections"')
        sys.exit(1)

    validate_section_html(data['sections'])

    root = find_kit_root()
    assets = load_assets(root)
    html = build_html(data, assets)

    stem = pathlib.Path(output_path).stem
    tmp_html = pathlib.Path('/tmp') / f'{stem}.tmp.html'
    tmp_html.write_text(html)

    preview_path = None
    if '--no-preview' not in sys.argv:
        preview_path = str(pathlib.Path('/tmp') / f'{stem}-preview.png')

    try:
        asyncio.run(render_pdf(str(tmp_html.resolve()), output_path, preview_path))
    finally:
        if tmp_html.exists():
            tmp_html.unlink()

    print(f'PDF saved: {output_path}')
    if preview_path and pathlib.Path(preview_path).exists():
        print(f'Cover preview: {preview_path}')


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError as ex:
        print(f'ERROR: {ex}')
        sys.exit(1)
    except Exception as ex:
        print(f'ERROR: unexpected failure — {ex}')
        raise
