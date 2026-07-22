#!/usr/bin/env python3
"""build-deck.py - render a branded Poetics slide deck from a deck.json spec.

Runs standalone, no AI required:
    python3 build-deck.py <deck.json> <output.html|output.pdf|output.pptx>

The output format is chosen by the output file's extension:
  .html  - self-contained deck, zero external dependencies, opens in any
           browser, printable to PDF from there too. This is the primary
           deliverable — hand it to anyone, Claude or not.
  .pdf   - rendered via Playwright/Chromium from the same HTML.
  .pptx  - editable PowerPoint via python-pptx (styled but not pixel-identical
           to the HTML — python-pptx text boxes approximate the layout; treat
           the HTML/PDF as the source of visual truth, PPTX as the editable
           fallback for people who need to tweak slides in PowerPoint).

deck.json schema:
{
  "title": "Deck title",           // used for the HTML <title> and PPTX metadata
  "footer": "poeticsvr.com",       // optional; footer text on content slides
  "slides": [ ...one object per slide, see types below... ]
}

Slide types (all fields optional unless noted):

  {"type": "title", "title": "...", "subtitle": "...", "eyebrow": "..."}
      Cover. Big display bottom-left, optional mono eyebrow above the title.

  {"type": "statement", "text": "(required)", "eyebrow": "...", "credit": "..."}
      Centered mission-statement moment: small mono eyebrow, one large
      statement (emphasis markers shine here), optional small credit line.

  {"type": "section", "title": "(required)", "eyebrow": "..."}
      Section divider. Left-aligned display title with an automatic huge
      ghost numeral (01, 02, ...) counting section slides.

  {"type": "agenda", "title": "...", "items": ["...", ...]}
      Numbered index list with ghost numerals and hairline separators.
      Splits into two columns automatically when more than 4 items.

  {"type": "content", "title": "...", "bullets": ["...", ...], "eyebrow": "..."}
      Title + bullet list. Splits bullets into two columns when more than 5.

  {"type": "cards", "title": "...", "cards": [{"title": "...", "body": "..."}], "eyebrow": "..."}
      Grid of cards (2 across for 2/4 cards, 3 across for 3/5/6).

  {"type": "stats", "title": "...", "stats": [{"value": "1,500+", "label": "...", "sublabel": "..."}], "eyebrow": "..."}
      Big-number slide. 2-4 stats in one row, 5-6 in two rows of three.

  {"type": "split", "title": "...", "subtitle": "...", "items": [{"title": "...", "body": "..."}],
   "image": "/path/to/photo.jpg", "side": "right", "eyebrow": "..."}
      Editorial split: text column + rounded-corner image panel (the
      reference deck's "Station setup" pattern). "image" is a local path
      (allowlisted: /tmp or the brand-kit tree); without one, a quiet
      branded placeholder panel renders instead. "side" = image side.

  {"type": "timeline", "title": "...", "steps": [{"title": "...", "body": "..."}], "eyebrow": "..."}
      Horizontal numbered process (01 → 02 → 03) joined by a hairline.
      Best with 3-5 steps.

  {"type": "quote", "quote": "(required)", "attribution": "..."}
      Full-bleed serif pull quote with mono attribution.

  {"type": "closing", "title": "...", "cta": "...", "contact": "..."}
      Thank-you slide: contact line + CTA pill above a huge display title
      bottom-left (mirrors the reference deck's closing).

Every text field is treated as plain text and HTML-escaped automatically —
callers do not need to escape content themselves (unlike build-doc-pdf.py's
richer "html" field). Wrap 2-4 word phrases in *single asterisks* to render
them in the Cormorant Garamond italic "emphasis" voice per brand.md, e.g.
"A new way *to experience* art". Use it sparingly — once or twice per slide.
"""

import base64
import html as html_lib
import json
import pathlib
import re
import sys

KIT_ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = KIT_ROOT / "assets/fonts"
LOGOS = KIT_ROOT / "assets/logos"
BACKGROUNDS = KIT_ROOT / "assets/backgrounds"

ACCENT = "#0099FF"
CANVAS = "#06070F"          # deep blue-black, matching the Athens College deck
RAISED = "#111214"
TEXT_1 = "#F4F4F2"
TEXT_2 = "#9A9A98"


def e(text):
    return html_lib.escape(str(text or ""))


EMPH_RE = re.compile(r"\*([^*]+)\*")


def emph(text):
    """Escape text, then render *phrase* as Cormorant Garamond italic emphasis."""
    parts = []
    last = 0
    raw = str(text or "")
    for m in EMPH_RE.finditer(raw):
        parts.append(e(raw[last:m.start()]))
        parts.append(f'<em>{e(m.group(1))}</em>')
        last = m.end()
    parts.append(e(raw[last:]))
    return "".join(parts)


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def font_face_css():
    faces = [
        ("Inter", 300, "normal", "Inter-Light.ttf"),
        ("Inter", 400, "normal", "Inter-Regular.ttf"),
        ("Inter", 500, "normal", "Inter-Medium.ttf"),
        ("Inter", 600, "normal", "Inter-SemiBold.ttf"),
        ("Inter", 700, "normal", "Inter-Bold.ttf"),
        ("Cormorant Garamond", 400, "italic", "CormorantGaramond-Italic.ttf"),
        ("Space Mono", 400, "normal", "SpaceMono-Regular.ttf"),
    ]
    out = []
    for family, weight, style, filename in faces:
        path = FONTS / filename
        if not path.exists():
            continue
        out.append(
            f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
            f"font-style: {style}; src: url('data:font/ttf;base64,{b64(path)}') format('truetype'); }}"
        )
    return "\n".join(out)


DECK_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: %(canvas)s; }
body { font-family: 'Inter', sans-serif; color: %(text1)s; }
.slide {
  position: relative;
  width: 1920px; height: 1080px;
  overflow: hidden;
  background: %(canvas)s;
  background-size: cover;
  background-position: center;
  page-break-after: always;
  display: flex;
  flex-direction: column;
}
.slide + .slide { margin-top: 0; }
.slide-inner { position: relative; z-index: 1; flex: 1; display: flex; flex-direction: column; padding: 150px 120px 150px; }
.logo { position: absolute; top: 64px; left: 120px; z-index: 2; height: 26px; }

/* -- Shared header pattern: eyebrow above title, consistent anchor -- */
.eyebrow {
  font-family: 'Space Mono', monospace; font-size: 16px; letter-spacing: 0.16em;
  text-transform: uppercase; color: %(text2)s; margin-bottom: 26px;
}
h1.slide-title {
  font-family: 'Inter', sans-serif; font-weight: 600;
  font-size: 66px; line-height: 1.06; letter-spacing: -0.02em; color: %(text1)s;
  max-width: 1240px;
}
h1.slide-title.t-md { font-size: 56px; }
h1.slide-title.t-sm { font-size: 46px; max-width: 1400px; }
.slide-subtitle {
  font-family: 'Inter', sans-serif; font-weight: 300; font-size: 28px; line-height: 1.45;
  color: %(text2)s; margin-top: 22px; max-width: 980px;
}
em { font-family: 'Cormorant Garamond', serif; font-style: italic; color: inherit; }

/* -- Title (cover) -- */
.slide.title-slide .slide-inner { justify-content: flex-end; padding-bottom: 150px; }
.slide.title-slide h1.slide-title { font-size: 108px; line-height: 1.02; letter-spacing: -0.025em; max-width: 1500px; }
.slide.title-slide h1.slide-title.t-md { font-size: 88px; }
.slide.title-slide h1.slide-title.t-sm { font-size: 72px; }
.slide.title-slide .slide-subtitle { font-size: 30px; margin-top: 28px; }
.slide.title-slide .eyebrow { margin-bottom: 34px; }

/* -- Statement (centered mission moment) -- */
.slide.statement-slide .slide-inner { align-items: center; justify-content: center; text-align: center; }
.statement-text {
  font-family: 'Inter', sans-serif; font-weight: 500; font-size: 64px; line-height: 1.22;
  letter-spacing: -0.015em; color: %(text1)s; max-width: 1520px;
}
.statement-text.t-md { font-size: 54px; }
.statement-text.t-sm { font-size: 46px; }
.statement-credit {
  font-family: 'Inter', sans-serif; font-weight: 300; font-size: 22px;
  color: %(text2)s; margin-top: 44px;
}
.slide.statement-slide .eyebrow { margin-bottom: 40px; }

/* -- Section divider: asymmetric, huge ghost numeral -- */
.slide.section-slide .slide-inner { justify-content: flex-end; padding-bottom: 170px; }
.slide.section-slide h1.slide-title { font-size: 88px; max-width: 1400px; }
.ghost-numeral {
  position: absolute; top: 30px; right: 90px; z-index: 0;
  font-family: 'Inter', sans-serif; font-weight: 200; font-size: 460px; line-height: 1;
  letter-spacing: -0.03em; color: rgba(255,255,255,0.045);
  user-select: none;
}

/* -- Agenda: numbered index rows -- */
.agenda { margin-top: 64px; max-width: 1480px; }
.agenda.cols-2 { column-count: 2; column-gap: 110px; max-width: 1680px; }
.agenda-item {
  display: flex; align-items: baseline; gap: 34px;
  padding: 26px 4px; border-top: 1px solid rgba(255,255,255,0.10);
  break-inside: avoid;
}
.agenda-num {
  font-family: 'Space Mono', monospace; font-size: 18px; color: rgba(255,255,255,0.34);
  min-width: 44px;
}
.agenda-text { font-size: 31px; font-weight: 400; color: %(text1)s; line-height: 1.3; }

/* -- Content bullets -- */
.bullets { list-style: none; margin-top: 58px; max-width: 1340px; }
.bullets.cols-2 { column-count: 2; column-gap: 100px; max-width: 1680px; }
.bullets li {
  font-size: 33px; line-height: 1.5; color: %(text1)s; font-weight: 300;
  padding-left: 44px; position: relative; margin-bottom: 34px;
  break-inside: avoid;
}
.bullets li::before {
  content: ''; position: absolute; left: 0; top: 17px; width: 7px; height: 7px;
  border-radius: 1px; background: %(accent)s;
}

/* -- Cards -- */
.cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 26px; margin-top: auto; margin-bottom: auto; }
.cards.cols-3 { grid-template-columns: repeat(3, 1fr); }
.card {
  background: rgba(17,18,20,0.72); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 42px 38px;
}
.card-dot {
  width: 7px; height: 7px; border-radius: 1px; background: rgba(255,255,255,0.5);
  margin-bottom: 22px;
}
.card-title { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 27px; color: %(text1)s; margin-bottom: 14px; }
.card-body { font-size: 21px; line-height: 1.55; color: %(text2)s; font-weight: 300; }

/* -- Stats: big numbers -- */
.stats { display: grid; gap: 30px 26px; margin-top: auto; margin-bottom: auto; max-width: 1680px; }
.stats.cols-2 { grid-template-columns: repeat(2, 1fr); }
.stats.cols-3 { grid-template-columns: repeat(3, 1fr); }
.stats.cols-4 { grid-template-columns: repeat(4, 1fr); }
.stat { border-top: 1px solid rgba(255,255,255,0.10); padding-top: 34px; }
.stat-value {
  font-family: 'Inter', sans-serif; font-weight: 300; font-size: 118px; line-height: 1;
  letter-spacing: -0.03em; color: %(accent)s;
}
.stats.cols-4 .stat-value { font-size: 96px; }
.stat-label { font-size: 25px; font-weight: 400; color: %(text1)s; margin-top: 18px; line-height: 1.35; }
.stat-sublabel { font-size: 19px; font-weight: 300; color: %(text2)s; margin-top: 8px; }

/* -- Split: text column + rounded image panel -- */
.split-wrap { display: flex; gap: 90px; margin-top: 26px; flex: 1; min-height: 0; align-items: stretch; }
.split-text { flex: 1.05; display: flex; flex-direction: column; }
.split-items { margin-top: 54px; display: flex; flex-direction: column; gap: 34px; }
.split-item { display: flex; gap: 26px; align-items: flex-start; }
.split-bar { width: 3px; border-radius: 2px; background: rgba(255,255,255,0.16); align-self: stretch; min-height: 58px; }
.split-item-title { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 28px; color: %(text1)s; }
.split-item-body { font-size: 22px; font-weight: 300; color: %(text2)s; margin-top: 6px; line-height: 1.45; }
.split-media { flex: 1; position: relative; border-radius: 20px; overflow: hidden; min-height: 0;
  border: 1px solid rgba(255,255,255,0.10); align-self: center; height: 680px; }
.split-media img { width: 100%%; height: 100%%; object-fit: cover; display: block; }
.split-placeholder {
  width: 100%%; height: 100%%; background:
    radial-gradient(closest-side at 78%% 22%%, rgba(0,153,255,0.16), transparent),
    %(raised)s;
  display: flex; align-items: center; justify-content: center;
}
.split-placeholder img { width: 110px; height: 110px; opacity: 0.28; object-fit: contain; }

/* -- Timeline: horizontal numbered process -- */
.timeline { display: flex; margin-top: auto; margin-bottom: auto; }
.tl-step { flex: 1; position: relative; padding: 0 44px 0 0; }
.tl-step:last-child { padding-right: 0; }
.tl-step::after {
  content: ''; position: absolute; top: 12px; left: 52px; right: 24px;
  border-top: 1px solid rgba(255,255,255,0.12);
}
.tl-step:last-child::after { right: 0; }
.tl-marker {
  display: inline-block;
  font-family: 'Space Mono', monospace; font-size: 18px; color: %(accent)s;
  line-height: 24px;
}
.tl-title { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 30px; color: %(text1)s; margin-top: 34px; }
.tl-body { font-size: 21px; font-weight: 300; color: %(text2)s; margin-top: 12px; line-height: 1.5; max-width: 400px; }

/* -- Quote -- */
.quote-slide .slide-inner { justify-content: center; align-items: flex-start; }
.quote-text {
  font-family: 'Cormorant Garamond', serif; font-style: italic; font-weight: 400;
  font-size: 60px; line-height: 1.38; color: %(text1)s; max-width: 1520px;
}
.quote-text.t-sm { font-size: 48px; }
.quote-attribution {
  font-family: 'Space Mono', monospace; font-size: 17px; letter-spacing: 0.12em;
  text-transform: uppercase; color: %(text2)s; margin-top: 48px;
}

/* -- Closing: asymmetric thank-you (mirrors the reference deck) -- */
.slide.closing-slide .slide-inner { justify-content: flex-end; padding-bottom: 130px; }
.closing-contact {
  font-family: 'Inter', sans-serif; font-weight: 400; font-size: 26px;
  color: %(text1)s; margin-bottom: 46px;
}
.closing-contact span { text-decoration: underline; text-underline-offset: 6px;
  text-decoration-thickness: 1px; text-decoration-color: rgba(255,255,255,0.5); }
.slide.closing-slide h1.slide-title { font-size: 150px; line-height: 1; letter-spacing: -0.03em; max-width: none; }
.slide.closing-slide h1.slide-title.t-md { font-size: 110px; }
.slide.closing-slide h1.slide-title.t-sm { font-size: 84px; }
.cta {
  display: inline-block; font-family: 'Space Mono', monospace; margin-bottom: 46px;
  font-size: 17px; letter-spacing: 0.08em; text-transform: uppercase; color: %(accent)s;
  border: 1px solid rgba(0,153,255,0.4); border-radius: 26px; padding: 16px 36px;
  align-self: flex-start;
}

/* -- Footer: hairline rule, site left, slide counter right -- */
.footer-rule {
  position: absolute; bottom: 64px; left: 120px; right: 120px; z-index: 2;
  border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;
  display: flex; justify-content: space-between; align-items: baseline;
}
.footer-rule span {
  font-family: 'Space Mono', monospace; font-size: 14px; color: %(text2)s;
  letter-spacing: 0.04em;
}
.footer-rule .slide-no { color: rgba(255,255,255,0.30); }

@media print {
  html, body { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  .slide { break-after: page; }
}
""" % {"canvas": CANVAS, "raised": RAISED, "text1": TEXT_1, "text2": TEXT_2, "accent": ACCENT}


_MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}


def slide_background_uri(slot: str, default_name: str) -> str:
    """Photo override from assets/backgrounds/photo/<slot>.* if present, else the gradient."""
    photo_dir = BACKGROUNDS / "photo"
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        cand = photo_dir / f"{slot}{ext}"
        if cand.exists():
            return f"data:{_MIME[ext]};base64,{b64(cand)}"
    path = BACKGROUNDS / default_name
    if path.exists():
        return f"data:image/jpeg;base64,{b64(path)}"
    return ""


def _load_brand_assets():
    import importlib.util as _ilu
    _ba_path = pathlib.Path(__file__).parent / "_brand_assets.py"
    _ba_spec = _ilu.spec_from_file_location("_brand_assets", _ba_path)
    _ba = _ilu.module_from_spec(_ba_spec)
    _ba_spec.loader.exec_module(_ba)
    return _ba


def resolve_slide_image(src: str) -> str:
    """Resolve a slide's local image path to a data URI via the shared allowlist
    (/tmp and the brand-kit tree). Returns '' if not resolvable."""
    if not src:
        return ""
    if src.startswith("data:image/"):
        return src
    ba = _load_brand_assets()
    return ba.resolve_local_image(src, ba.make_allowed_roots(__file__))


def strip_markers(text) -> str:
    return EMPH_RE.sub(r"\1", str(text or ""))


def size_class(text, md_at: int, sm_at: int) -> str:
    """Adaptive display sizing: long lines step down so they never crowd the
    slide. Thresholds are character counts of the marker-stripped text."""
    n = len(strip_markers(text))
    if n > sm_at:
        return " t-sm"
    if n > md_at:
        return " t-md"
    return ""


def _eyebrow(slide) -> str:
    return f'<div class="eyebrow">{e(slide.get("eyebrow", ""))}</div>' if slide.get("eyebrow") else ""


def _header(slide, md_at=52, sm_at=88) -> str:
    """Shared eyebrow + adaptive title header for content-family slides."""
    title = slide.get("title", "")
    if not title and not slide.get("eyebrow"):
        return ""
    return f'{_eyebrow(slide)}<h1 class="slide-title{size_class(title, md_at, sm_at)}">{emph(title)}</h1>'


def render_slide(slide: dict, logo_uri: str, mark_uri: str, footer_text: str,
                 index: int, total: int, section_no: int) -> str:
    stype = slide.get("type", "content")
    if stype in ("title", "statement", "section", "closing"):
        bg_uri = slide_background_uri("deck-title", "deck-bg-title.jpg")
    else:
        bg_uri = slide_background_uri("deck-default", "deck-bg-default.jpg")
    bg_style = f"background-image:url('{bg_uri}');" if bg_uri else ""

    logo_html = f'<img class="logo" src="{logo_uri}" alt="Poetics">' if logo_uri and stype != "section" else ""
    footer_html = (
        f'<div class="footer-rule"><span>{e(footer_text)}</span>'
        f'<span class="slide-no">{index:02d} / {total:02d}</span></div>'
        if footer_text and stype not in ("title", "closing") else ""
    )

    if stype == "title":
        body = f'''
    <div class="slide-inner">
      {_eyebrow(slide)}
      <h1 class="slide-title{size_class(slide.get("title",""), 34, 58)}">{emph(slide.get("title", ""))}</h1>
      {f'<div class="slide-subtitle">{emph(slide.get("subtitle", ""))}</div>' if slide.get("subtitle") else ""}
    </div>'''
        cls = "title-slide"

    elif stype == "statement":
        text = slide.get("text", "") or slide.get("title", "")
        body = f'''
    <div class="slide-inner">
      {_eyebrow(slide)}
      <div class="statement-text{size_class(text, 90, 160)}">{emph(text)}</div>
      {f'<div class="statement-credit">{emph(slide.get("credit", ""))}</div>' if slide.get("credit") else ""}
    </div>'''
        cls = "statement-slide"

    elif stype == "section":
        body = f'''
    <div class="ghost-numeral">{section_no:02d}</div>
    <div class="slide-inner">
      {_eyebrow(slide)}
      <h1 class="slide-title{size_class(slide.get("title",""), 40, 70)}">{emph(slide.get("title", ""))}</h1>
    </div>'''
        cls = "section-slide"

    elif stype == "agenda":
        items = slide.get("items", [])
        cols = " cols-2" if len(items) > 4 else ""
        rows = "".join(
            f'<div class="agenda-item"><span class="agenda-num">{i + 1:02d}</span>'
            f'<span class="agenda-text">{emph(it)}</span></div>'
            for i, it in enumerate(items)
        )
        body = f'''
    <div class="slide-inner">
      {_header(slide)}
      <div class="agenda{cols}">{rows}</div>
    </div>'''
        cls = "agenda-slide"

    elif stype == "content":
        items = slide.get("bullets", [])
        cols = " cols-2" if len(items) > 5 else ""
        bullets = "".join(f'<li>{emph(b)}</li>' for b in items)
        body = f'''
    <div class="slide-inner">
      {_header(slide)}
      <ul class="bullets{cols}">{bullets}</ul>
    </div>'''
        cls = "content-slide"

    elif stype == "cards":
        cards = slide.get("cards", [])
        cols = " cols-3" if len(cards) in (3, 5, 6) else ""
        card_html = "".join(
            f'<div class="card"><div class="card-dot"></div>'
            f'<div class="card-title">{e(c.get("title",""))}</div>'
            f'<div class="card-body">{emph(c.get("body",""))}</div></div>'
            for c in cards
        )
        body = f'''
    <div class="slide-inner">
      {_header(slide)}
      <div class="cards{cols}">{card_html}</div>
    </div>'''
        cls = "cards-slide"

    elif stype == "stats":
        stats = slide.get("stats", [])
        n = len(stats)
        cols = " cols-2" if n <= 2 else (" cols-4" if n == 4 else " cols-3")
        stat_html = "".join(
            f'<div class="stat"><div class="stat-value">{e(s.get("value",""))}</div>'
            f'<div class="stat-label">{emph(s.get("label",""))}</div>'
            + (f'<div class="stat-sublabel">{emph(s.get("sublabel",""))}</div>' if s.get("sublabel") else "")
            + '</div>'
            for s in stats
        )
        body = f'''
    <div class="slide-inner">
      {_header(slide)}
      <div class="stats{cols}">{stat_html}</div>
    </div>'''
        cls = "stats-slide"

    elif stype == "split":
        items = slide.get("items", [])
        item_html = "".join(
            f'<div class="split-item"><div class="split-bar"></div><div>'
            f'<div class="split-item-title">{e(it.get("title",""))}</div>'
            + (f'<div class="split-item-body">{emph(it.get("body",""))}</div>' if it.get("body") else "")
            + '</div></div>'
            for it in items
        )
        img_uri = resolve_slide_image(slide.get("image", ""))
        if img_uri:
            media = f'<img src="{img_uri}" alt="">'
        else:
            ph_logo = f'<img src="{mark_uri}" alt="">' if mark_uri else ""
            media = f'<div class="split-placeholder">{ph_logo}</div>'
        text_col = f'''<div class="split-text">
        {_header(slide, md_at=34, sm_at=60)}
        {f'<div class="slide-subtitle">{emph(slide.get("subtitle", ""))}</div>' if slide.get("subtitle") else ""}
        <div class="split-items">{item_html}</div>
      </div>'''
        media_col = f'<div class="split-media">{media}</div>'
        cols = (media_col + text_col) if slide.get("side") == "left" else (text_col + media_col)
        body = f'''
    <div class="slide-inner">
      <div class="split-wrap">{cols}</div>
    </div>'''
        cls = "split-slide"

    elif stype == "timeline":
        steps = slide.get("steps", [])
        step_html = "".join(
            f'<div class="tl-step"><span class="tl-marker">{i + 1:02d}</span>'
            f'<div class="tl-title">{e(st.get("title",""))}</div>'
            + (f'<div class="tl-body">{emph(st.get("body",""))}</div>' if st.get("body") else "")
            + '</div>'
            for i, st in enumerate(steps)
        )
        body = f'''
    <div class="slide-inner">
      {_header(slide)}
      <div class="timeline">{step_html}</div>
    </div>'''
        cls = "timeline-slide"

    elif stype == "quote":
        qtext = slide.get("quote", "")
        qcls = " t-sm" if len(strip_markers(qtext)) > 180 else ""
        body = f'''
    <div class="slide-inner">
      <div class="quote-text{qcls}">&ldquo;{emph(qtext)}&rdquo;</div>
      {f'<div class="quote-attribution">{e(slide.get("attribution",""))}</div>' if slide.get("attribution") else ""}
    </div>'''
        cls = "quote-slide"

    elif stype == "closing":
        contact = slide.get("contact", "")
        contact_html = (
            f'<div class="closing-contact"><span>{emph(contact)}</span></div>' if contact else ""
        )
        cta_html = f'<div class="cta">{e(slide.get("cta",""))}</div>' if slide.get("cta") else ""
        body = f'''
    <div class="slide-inner">
      {contact_html}
      {cta_html}
      <h1 class="slide-title{size_class(slide.get("title",""), 16, 30)}">{emph(slide.get("title", ""))}</h1>
    </div>'''
        cls = "closing-slide"

    else:
        body = f'<div class="slide-inner">{_header(slide)}</div>'
        cls = "content-slide"

    return f'<section class="slide {cls}" style="{bg_style}">{logo_html}{body}{footer_html}</section>'


def build_html(deck: dict) -> str:
    title = e(deck.get("title", "Poetics deck"))
    footer_text = deck.get("footer", "poeticsvr.com")
    logo_path = LOGOS / "wordmark-light.png"
    logo_uri = f"data:image/png;base64,{b64(logo_path)}" if logo_path.exists() else ""
    mark_path = LOGOS / "mark-light.png"
    mark_uri = f"data:image/png;base64,{b64(mark_path)}" if mark_path.exists() else ""

    slides = deck.get("slides", [])
    total = len(slides)
    parts = []
    section_no = 0
    for i, s in enumerate(slides):
        if s.get("type") == "section":
            section_no += 1
        parts.append(render_slide(s, logo_uri, mark_uri, footer_text, i + 1, total, section_no))
    slides_html = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{font_face_css()}
{DECK_CSS}
</style>
</head>
<body>
{slides_html}
</body>
</html>"""


# -- PDF export (Playwright) ---------------------------------------------------

def export_pdf(html_path: pathlib.Path, pdf_path: str):
    import asyncio

    async def _run():
        import os as _os
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                channel=_os.environ.get("POETICS_BROWSER_CHANNEL") or None)
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            await page.goto(html_path.as_uri())
            try:
                await page.evaluate("document.fonts.ready")
                await page.wait_for_timeout(400)
            except Exception:
                await page.wait_for_timeout(1200)
            await page.pdf(
                path=pdf_path,
                width="1920px", height="1080px",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            )
            await browser.close()

    asyncio.run(_run())


def check_playwright():
    import importlib
    import subprocess
    import os as _os
    try:
        importlib.import_module("playwright")
    except ImportError:
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "playwright"])
        if r.returncode != 0:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "playwright"], check=True)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            exe = pw.chromium.executable_path
        if not (exe and _os.path.exists(exe)):
            raise RuntimeError
    except Exception:
        import importlib.util as _ilu
        _ba_path = pathlib.Path(__file__).parent / "_brand_assets.py"
        _ba_spec = _ilu.spec_from_file_location("_brand_assets", _ba_path)
        _ba = _ilu.module_from_spec(_ba_spec)
        _ba_spec.loader.exec_module(_ba)
        channel = _ba.pick_browser_channel()
        if channel:
            # System Chrome/Edge renders identically — skip the 110 MB download
            # (which also fails outright on networks that block the Playwright CDN).
            _os.environ.setdefault("POETICS_BROWSER_CHANNEL", channel)
            print(f"Bundled Chromium not installed — using system browser (channel: {channel}).",
                  file=sys.stderr)
        else:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


# -- PPTX export (python-pptx) -------------------------------------------------

def export_pptx(deck: dict, out_path: str):
    import subprocess
    import importlib
    try:
        importlib.import_module("pptx")
    except ImportError:
        r = subprocess.run([sys.executable, "-m", "pip", "install", "python-pptx", "--break-system-packages", "--quiet"])
        if r.returncode != 0:
            subprocess.run([sys.executable, "-m", "pip", "install", "python-pptx", "--quiet"], check=True)

    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    def rgb(hexstr):
        hexstr = hexstr.lstrip("#")
        return RGBColor(int(hexstr[0:2], 16), int(hexstr[2:4], 16), int(hexstr[4:6], 16))

    prs = Presentation()
    prs.slide_width = Emu(12192000)   # 13.333in, 16:9
    prs.slide_height = Emu(6858000)   # 7.5in
    blank = prs.slide_layouts[6]

    def strip_emphasis(text):
        return EMPH_RE.sub(r"\1", text or "")

    def add_text(slide, x, y, w, h, text, *, font="Inter", size=18, bold=False,
                 italic=False, color=TEXT_1, align=None, space_after=None):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.italic = italic
        p.font.color.rgb = rgb(color)
        if align is not None:
            p.alignment = align
        if space_after is not None:
            p.space_after = Pt(space_after)
        return box

    for s in deck.get("slides", []):
        slide = prs.slides.add_slide(blank)
        bg = slide.background
        bg.fill.solid()
        bg.fill.fore_color.rgb = rgb(CANVAS)

        stype = s.get("type", "content")
        title_text = strip_emphasis(s.get("title", "") or s.get("quote", "") or s.get("text", ""))

        if stype == "statement":
            add_text(slide, 1.2, 2.6, 10.9, 2.4, strip_emphasis(s.get("text", "") or s.get("title", "")),
                     size=32, bold=False, align=PP_ALIGN.CENTER)
            if s.get("credit"):
                add_text(slide, 1.2, 5.2, 10.9, 0.6, strip_emphasis(s["credit"]),
                         size=13, color=TEXT_2, align=PP_ALIGN.CENTER)
            continue

        if stype == "quote":
            add_text(slide, 0.8, 2.4, 11.7, 2.6, f'“{title_text}”',
                     font="Cormorant Garamond", size=32, italic=True)
            if s.get("attribution"):
                add_text(slide, 0.8, 5.4, 10.0, 0.6, s["attribution"].upper(),
                         font="Space Mono", size=12, color=TEXT_2)
            continue

        if stype == "closing":
            if s.get("contact"):
                add_text(slide, 0.8, 3.4, 10.0, 0.6, strip_emphasis(s["contact"]), size=16)
            if s.get("cta"):
                add_text(slide, 0.8, 4.1, 6.0, 0.6, s["cta"].upper(),
                         font="Space Mono", size=13, color=ACCENT)
            add_text(slide, 0.8, 4.9, 12.0, 1.8, title_text, size=64, bold=True)
            continue

        # Title-at-top family (title, section, agenda, content, cards, stats, split, timeline).
        add_text(slide, 0.8, 0.7, 11.7, 1.8, title_text,
                 size=48 if stype in ("title", "section") else 34, bold=True)
        if stype == "title" and s.get("subtitle"):
            add_text(slide, 0.8, 2.2, 10.5, 0.9, strip_emphasis(s["subtitle"]), size=18, color=TEXT_2)

        if stype == "agenda" and s.get("items"):
            body = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(4.7))
            btf = body.text_frame
            btf.word_wrap = True
            for i, it in enumerate(s["items"]):
                bp = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
                bp.text = f"{i + 1:02d}   {strip_emphasis(it)}"
                bp.font.name = "Inter"
                bp.font.size = Pt(18)
                bp.font.color.rgb = rgb(TEXT_1)
                bp.space_after = Pt(12)
        elif stype == "content" and s.get("bullets"):
            body = slide.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(11.5), Inches(4.5))
            btf = body.text_frame
            btf.word_wrap = True
            for i, b in enumerate(s["bullets"]):
                bp = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
                bp.text = f"—  {strip_emphasis(b)}"
                bp.font.name = "Inter"
                bp.font.size = Pt(18)
                bp.font.color.rgb = rgb(TEXT_1)
                bp.space_after = Pt(10)
        elif stype == "cards" and s.get("cards"):
            cards = s["cards"]
            n = len(cards)
            col_w = 11.5 / max(n, 1)
            for i, c in enumerate(cards):
                box = slide.shapes.add_textbox(Inches(0.8 + col_w * i), Inches(2.6),
                                               Inches(col_w - 0.2), Inches(3.5))
                ctf = box.text_frame
                ctf.word_wrap = True
                cp = ctf.paragraphs[0]
                cp.text = strip_emphasis(c.get("title", ""))
                cp.font.name = "Inter"
                cp.font.bold = True
                cp.font.size = Pt(16)
                cp.font.color.rgb = rgb(TEXT_1)
                bp = ctf.add_paragraph()
                bp.text = strip_emphasis(c.get("body", ""))
                bp.font.name = "Inter"
                bp.font.size = Pt(13)
                bp.font.color.rgb = rgb(TEXT_2)
        elif stype == "stats" and s.get("stats"):
            stats = s["stats"]
            n = len(stats)
            col_w = 11.5 / max(n, 1)
            for i, st in enumerate(stats):
                box = slide.shapes.add_textbox(Inches(0.8 + col_w * i), Inches(2.8),
                                               Inches(col_w - 0.2), Inches(3.0))
                ctf = box.text_frame
                ctf.word_wrap = True
                vp = ctf.paragraphs[0]
                vp.text = st.get("value", "")
                vp.font.name = "Inter"
                vp.font.size = Pt(54)
                vp.font.color.rgb = rgb(ACCENT)
                lp = ctf.add_paragraph()
                lp.text = strip_emphasis(st.get("label", ""))
                lp.font.name = "Inter"
                lp.font.size = Pt(15)
                lp.font.color.rgb = rgb(TEXT_1)
                if st.get("sublabel"):
                    sp = ctf.add_paragraph()
                    sp.text = strip_emphasis(st["sublabel"])
                    sp.font.name = "Inter"
                    sp.font.size = Pt(12)
                    sp.font.color.rgb = rgb(TEXT_2)
        elif stype == "split":
            if s.get("subtitle"):
                add_text(slide, 0.8, 1.9, 6.2, 0.8, strip_emphasis(s["subtitle"]), size=15, color=TEXT_2)
            body = slide.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(6.2), Inches(4.2))
            btf = body.text_frame
            btf.word_wrap = True
            for i, it in enumerate(s.get("items", [])):
                tp = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
                tp.text = strip_emphasis(it.get("title", ""))
                tp.font.name = "Inter"
                tp.font.bold = True
                tp.font.size = Pt(17)
                tp.font.color.rgb = rgb(TEXT_1)
                if it.get("body"):
                    bp = btf.add_paragraph()
                    bp.text = strip_emphasis(it["body"])
                    bp.font.name = "Inter"
                    bp.font.size = Pt(13)
                    bp.font.color.rgb = rgb(TEXT_2)
                    bp.space_after = Pt(10)
            img_uri = resolve_slide_image(s.get("image", ""))
            if img_uri.startswith("data:image/"):
                import io as _io
                raw = base64.b64decode(img_uri.split(",", 1)[1])
                try:
                    slide.shapes.add_picture(_io.BytesIO(raw), Inches(7.4), Inches(1.6),
                                             width=Inches(5.1))
                except Exception:
                    pass
        elif stype == "timeline" and s.get("steps"):
            steps = s["steps"]
            n = len(steps)
            col_w = 11.5 / max(n, 1)
            for i, st in enumerate(steps):
                box = slide.shapes.add_textbox(Inches(0.8 + col_w * i), Inches(2.8),
                                               Inches(col_w - 0.3), Inches(3.2))
                ctf = box.text_frame
                ctf.word_wrap = True
                mp = ctf.paragraphs[0]
                mp.text = f"{i + 1:02d}"
                mp.font.name = "Space Mono"
                mp.font.size = Pt(13)
                mp.font.color.rgb = rgb(ACCENT)
                tp = ctf.add_paragraph()
                tp.text = strip_emphasis(st.get("title", ""))
                tp.font.name = "Inter"
                tp.font.bold = True
                tp.font.size = Pt(17)
                tp.font.color.rgb = rgb(TEXT_1)
                if st.get("body"):
                    bp = ctf.add_paragraph()
                    bp.text = strip_emphasis(st["body"])
                    bp.font.name = "Inter"
                    bp.font.size = Pt(13)
                    bp.font.color.rgb = rgb(TEXT_2)

    prs.save(out_path)


# -- Entry point -----------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        sys.exit("usage: build-deck.py <deck.json> <output.html|output.pdf|output.pptx>")
    deck_path, out_path = sys.argv[1], sys.argv[2]
    with open(deck_path, encoding="utf-8") as f:
        deck = json.load(f)

    out = pathlib.Path(out_path)
    ext = out.suffix.lower()

    html = build_html(deck)

    if ext == ".html":
        out.write_text(html, encoding="utf-8")
        print(f"Wrote {out_path}")
    elif ext == ".pdf":
        check_playwright()
        tmp_html = pathlib.Path("/tmp") / f"{out.stem}.tmp.html"
        tmp_html.write_text(html, encoding="utf-8")
        try:
            export_pdf(tmp_html.resolve(), out_path)
        finally:
            tmp_html.unlink(missing_ok=True)
        print(f"Wrote {out_path}")
    elif ext == ".pptx":
        export_pptx(deck, out_path)
        print(f"Wrote {out_path}")
    else:
        sys.exit(f"error: unsupported output extension '{ext}' (use .html, .pdf, or .pptx)")


if __name__ == "__main__":
    main()
