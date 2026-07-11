#!/usr/bin/env python3
"""build-doc.py - render a branded Poetics document as .docx via python-docx.

Runs standalone, no AI required:
    python3 build-doc.py <content.json> <output.docx>

content.json schema is documented in schemas/doc-content-schema.md (identical
schema is shared with build-doc-pdf.py, so one payload renders to either
format).

-- Design compromise (read this before changing colors) -------------------
brand.md specifies a dark-canvas-only aesthetic. Word documents are read and
printed differently than web/PDF, so this renderer makes one pragmatic
trade-off, same one fabric (the Workable reference this was adapted from)
made: the COVER page is fully dark and on-brand (wordmark, glow background,
Inter display type). The BODY pages use a light, readable page with brand
headings, because a fully dark multi-page Word document prints and
screen-reads poorly and most Word themes fight a forced dark background.
If strict full-document dark-brand fidelity matters, render to PDF instead
(build-doc-pdf.py), which is the canonical branded document format.

-- Fonts --------------------------------------------------------------------
Poetics documents use Inter for display (headings) and body, plus Cormorant
Garamond italic for emphasis only (see brand.md). This renderer maps headings
and body to Inter automatically; any inline <em>/<i> text is set in Cormorant
Garamond italic, not just an italicized Inter, to match the brand's "signature
move" rule. True binary font embedding is not done here (Word requires
per-style obfuscated font parts); render to PDF for guaranteed embedding on
machines without these fonts installed.
"""

import json
import pathlib
import sys
from html.parser import HTMLParser


# -- Preflight checks ---------------------------------------------------------

def check_dependencies():
    """Ensure python-docx is importable; install it on a fresh sandbox if not."""
    import importlib
    import subprocess

    try:
        importlib.import_module("docx")
        return
    except ImportError:
        pass

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "python-docx", "--break-system-packages", "--quiet"],
    )
    if result.returncode != 0:
        # Older pip (pre-PEP 668) doesn't recognize --break-system-packages.
        subprocess.run([sys.executable, "-m", "pip", "install", "python-docx", "--quiet"], check=True)
    importlib.invalidate_caches()
    try:
        importlib.import_module("docx")
    except ImportError:
        sys.exit("error: python-docx is required but could not be installed")


check_dependencies()

from docx import Document  # noqa: E402
from docx.enum.section import WD_SECTION  # noqa: E402
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Emu, Inches, Pt, RGBColor  # noqa: E402


# -- Spec constants (from brand.md) --------------------------------------------

BODY_FONT = "Inter"
DISPLAY_FONT = "Inter"          # headlines use Inter (SemiBold), matching the deck aesthetic
ITALIC_FONT = "Cormorant Garamond"
FALLBACK_FONT = "Arial"
LINE = 1.3

PAGE_W_IN = 8.5
PAGE_H_IN = 11
MARGIN_SIDE_IN = 0.75
MARGIN_TB_IN = 0.75

ACCENT = "0099FF"
TEXT_ON_DARK = "F4F4F2"
TEXT_ON_DARK_SECONDARY = "9A9A98"
TEXT_ON_LIGHT = "17181A"       # near-black, for legibility on white body pages
TEXT_ON_LIGHT_SECONDARY = "5B5C5E"

# Type scale: (size_pt, bold, hex_color, display_font)
STYLES = {
    "title":    (40, True,  TEXT_ON_DARK, True),
    "subtitle": (16, False, TEXT_ON_DARK_SECONDARY, False),
    "date":     (11, False, TEXT_ON_DARK_SECONDARY, False),
    "h1":       (24, True,  ACCENT, True),
    "h2":       (17, True,  ACCENT, True),
    "h3":       (13, True,  TEXT_ON_LIGHT, True),
    "h4":       (12, True,  TEXT_ON_LIGHT, False),
    "h5":       (11, True,  TEXT_ON_LIGHT_SECONDARY, False),
    "h6":       (11, False, TEXT_ON_LIGHT_SECONDARY, False),
    "body":     (11, False, TEXT_ON_LIGHT, False),
}

HEADING_SPACE = {
    "h1": (24, 12), "h2": (20, 10), "h3": (16, 8),
    "h4": (14, 6), "h5": (14, 6), "h6": (14, 6),
}

TABLE_BORDER = "D8DADC"
TABLE_HEADER_BG = "F2F3F4"
CALLOUT_BG = "13161C"          # dark callout card, echoes the brand's raised-surface color
CALLOUT_TEXT = TEXT_ON_DARK

KIT_ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO_WORDMARK = KIT_ROOT / "assets/logos/wordmark-light.png"
LOGO_MARK = KIT_ROOT / "assets/logos/mark-light.png"


def _bg(slot, default_name):
    """Return a photo override from assets/backgrounds/photo/ if present, else the
    generated gradient. slot is e.g. 'doc-cover'; checks common image extensions."""
    photo_dir = KIT_ROOT / "assets/backgrounds/photo"
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        cand = photo_dir / f"{slot}{ext}"
        if cand.exists():
            return cand
    return KIT_ROOT / "assets/backgrounds" / default_name


COVER_BG_IMG = _bg("doc-cover", "doc-cover-bg.jpg")
SECTION_BG_IMG = _bg("doc-section", "doc-section-bg.jpg")

VOID_TAGS = {"br", "img", "hr"}
BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table", "div"}


# -- Low-level XML helpers ----------------------------------------------------

def _shade(element_pr, hex_fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    element_pr.append(shd)


def set_cell_bg(cell, hex_fill):
    _shade(cell._tc.get_or_add_tcPr(), hex_fill)


def set_table_borders(table, hex_color, sz=6):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), hex_color)
        borders.append(e)
    tblPr.append(borders)


def set_table_cell_margins(table, top, left=None, bottom=None, right=None):
    if left is None:
        left = bottom = right = top
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for edge, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:w"), str(int(val * 20)))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblPr.append(mar)


def pad_cell_paragraphs(cell, h_pt):
    for p in cell.paragraphs:
        p.paragraph_format.left_indent = Pt(h_pt)
        p.paragraph_format.right_indent = Pt(h_pt)


CONTENT_W_IN = PAGE_W_IN - 2 * MARGIN_SIDE_IN


def align_table_full_width(table):
    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.insert(0, tblW)
    tblW.set(qn("w:type"), "dxa")
    tblW.set(qn("w:w"), str(int(CONTENT_W_IN * 1440)))

    for old in tblPr.findall(qn("w:tblInd")):
        tblPr.remove(old)
    ind = OxmlElement("w:tblInd")
    ind.set(qn("w:w"), "0")
    ind.set(qn("w:type"), "dxa")
    jc = tblPr.find(qn("w:jc"))
    if jc is not None:
        jc.addnext(ind)
    else:
        tblW.addnext(ind)

    table.autofit = False
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")


def set_col_widths(table, widths_in):
    for i, w in enumerate(widths_in):
        table.columns[i].width = Inches(w)
        for cell in table.columns[i].cells:
            cell.width = Inches(w)


def set_theme_fonts(doc, typeface):
    import re
    theme_rt = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
    for rel in doc.part.rels.values():
        if rel.reltype != theme_rt:
            continue
        tp = rel.target_part
        try:
            blob = tp.blob.decode("utf-8")
        except Exception:
            return

        def _swap(block_tag, xml):
            return re.sub(
                rf'(<a:{block_tag}>\s*<a:latin typeface=")[^"]*(")',
                rf"\g<1>{typeface}\g<2>",
                xml,
                count=1,
                flags=re.S,
            )

        blob = _swap("majorFont", blob)
        blob = _swap("minorFont", blob)
        try:
            tp._blob = blob.encode("utf-8")
        except Exception:
            pass
        return


def add_font_fallback(doc, primary, alt=FALLBACK_FONT):
    font_rt = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable"
    for rel in doc.part.rels.values():
        if rel.reltype != font_rt:
            continue
        tp = rel.target_part
        try:
            blob = tp.blob.decode("utf-8")
        except Exception:
            return
        if f'w:name="{primary}"' in blob or "</w:fonts>" not in blob:
            return
        entry = (
            f'<w:font w:name="{primary}">'
            f'<w:altName w:val="{alt}"/>'
            f'<w:panose1 w:val="020B0604020202020204"/>'
            f'<w:charset w:val="00"/>'
            f'<w:family w:val="swiss"/>'
            f'<w:pitch w:val="variable"/>'
            f"</w:font>"
        )
        blob = blob.replace("</w:fonts>", entry + "</w:fonts>")
        try:
            tp._blob = blob.encode("utf-8")
        except Exception:
            pass
        return


def add_full_page_background(header, img_path):
    if not img_path.exists():
        return
    page_w = Emu(int(PAGE_W_IN * 914400))
    page_h = Emu(int(PAGE_H_IN * 914400))
    run = header.paragraphs[0].add_run()
    run.add_picture(str(img_path), width=page_w, height=page_h)
    drawing = run._r.find(qn("w:drawing"))
    inline = drawing.find(qn("wp:inline"))
    if inline is None:
        return
    anchor = OxmlElement("wp:anchor")
    for k, v in {
        "behindDoc": "1", "distT": "0", "distB": "0", "distL": "0", "distR": "0",
        "simplePos": "0", "locked": "0", "layoutInCell": "1",
        "allowOverlap": "1", "relativeHeight": "0",
    }.items():
        anchor.set(k, v)
    sp = OxmlElement("wp:simplePos")
    sp.set("x", "0")
    sp.set("y", "0")
    anchor.append(sp)
    for tag in ("wp:positionH", "wp:positionV"):
        pos = OxmlElement(tag)
        pos.set("relativeFrom", "page")
        off = OxmlElement("wp:posOffset")
        off.text = "0"
        pos.append(off)
        anchor.append(pos)
    for tag in ("wp:extent", "wp:effectExtent"):
        el = inline.find(qn(tag))
        if el is not None:
            anchor.append(el)
    anchor.append(OxmlElement("wp:wrapNone"))
    for tag in ("wp:docPr", "wp:cNvGraphicFramePr"):
        el = inline.find(qn(tag))
        if el is not None:
            anchor.append(el)
    graphic = inline.find(qn("a:graphic"))
    if graphic is not None:
        anchor.append(graphic)
    drawing.remove(inline)
    drawing.append(anchor)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    style_run(run, 9, False, TEXT_ON_LIGHT_SECONDARY)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)


def add_hyperlink(paragraph, url, runs_fmt_text):
    """Links use the accent color, per brand.md ('interactive states, links')."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    for text, fmt in runs_fmt_text:
        font = ITALIC_FONT if fmt.get("italic") else BODY_FONT
        r = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        rFonts = OxmlElement("w:rFonts")
        for attr in ("w:ascii", "w:hAnsi", "w:cs"):
            rFonts.set(qn(attr), font)
        rPr.append(rFonts)
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(STYLES["body"][0] * 2)))
        rPr.append(sz)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), ACCENT)
        rPr.append(color)
        if fmt.get("bold"):
            rPr.append(OxmlElement("w:b"))
        if fmt.get("italic"):
            rPr.append(OxmlElement("w:i"))
        r.append(rPr)
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = text
        r.append(t)
        hyperlink.append(r)
    paragraph._p.append(hyperlink)


# -- Run / paragraph styling --------------------------------------------------

def style_run(run, size_pt, bold, hex_color, italic=False, display=False):
    """Picks the font by role: italic -> Cormorant Garamond (brand's emphasis
    voice), display -> Inter SemiBold (headings), else Inter (body)."""
    font = ITALIC_FONT if italic else (DISPLAY_FONT if display else BODY_FONT)
    run.font.name = font
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(attr), font)
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(hex_color)


def new_paragraph(container, space_before=None, space_after=None, line=LINE):
    p = container.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = line
    if space_before is not None:
        pf.space_before = Pt(space_before)
    if space_after is not None:
        pf.space_after = Pt(space_after)
    return p


HEADING_STYLE_NAMES = {
    "h1": "Heading 1", "h2": "Heading 2", "h3": "Heading 3",
    "h4": "Heading 4", "h5": "Heading 5", "h6": "Heading 6",
}


def add_heading(container, level, text):
    size, bold, color, display = STYLES[level]
    before, after = HEADING_SPACE[level]
    p = new_paragraph(container, space_before=before, space_after=after)
    style_name = HEADING_STYLE_NAMES.get(level)
    if style_name:
        try:
            p.style = style_name
        except KeyError:
            pass
    p.paragraph_format.keep_with_next = True
    style_run(p.add_run(text), size, bold, color, display=display)
    return p


# -- HTML subset parsing ------------------------------------------------------

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "root", "attrs": {}, "children": []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "children": []}
        self.stack[-1]["children"].append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1]["children"].append({"tag": tag, "attrs": dict(attrs), "children": []})

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]["children"].append(data)


def parse_html(raw):
    tb = TreeBuilder()
    tb.feed(raw or "")
    return tb.root["children"]


def has_class(node, name):
    return name in (node.get("attrs", {}).get("class", "").split())


# -- Inline rendering ---------------------------------------------------------

def collect_inline_segments(children, fmt):
    segs = []
    for ch in children:
        if isinstance(ch, str):
            text = ch.replace("\n", " ")
            if text:
                segs.append(("text", text, dict(fmt)))
            continue
        tag = ch["tag"]
        if tag == "br":
            segs.append(("break", None, None))
        elif tag in ("strong", "b"):
            segs.extend(collect_inline_segments(ch["children"], {**fmt, "bold": True}))
        elif tag in ("em", "i"):
            segs.extend(collect_inline_segments(ch["children"], {**fmt, "italic": True}))
        elif tag == "a":
            url = ch["attrs"].get("href", "")
            inner = collect_inline_segments(ch["children"], fmt)
            link_runs = [(t, f) for kind, t, f in inner if kind == "text"]
            if url and link_runs:
                segs.append(("link", url, link_runs))
            else:
                segs.extend(inner)
        else:
            segs.extend(collect_inline_segments(ch["children"], fmt))
    return segs


def render_inline(paragraph, children, base_size, base_color):
    for kind, val, fmt in collect_inline_segments(children, {}):
        if kind == "break":
            paragraph.add_run().add_break()
        elif kind == "text":
            run = paragraph.add_run(val)
            style_run(run, base_size, fmt.get("bold", False), base_color, fmt.get("italic", False))
        elif kind == "link":
            add_hyperlink(paragraph, val, fmt)


# -- Block rendering ----------------------------------------------------------

def render_blocks(container, nodes):
    for node in nodes:
        if isinstance(node, str):
            if node.strip():
                p = new_paragraph(container, space_after=12)
                style_run(p.add_run(node.strip()), STYLES["body"][0], False, STYLES["body"][2])
            continue
        render_block(container, node)


def render_block(container, node):
    tag = node["tag"]
    if tag in ("h2", "h3", "h4", "h5", "h6"):
        add_heading(container, tag, inline_text(node["children"]))
    elif tag == "p":
        p = new_paragraph(container, space_after=12)
        render_inline(p, node["children"], STYLES["body"][0], STYLES["body"][2])
    elif tag in ("ul", "ol"):
        style_name = "List Number" if tag == "ol" else "List Bullet"
        for li in node["children"]:
            if isinstance(li, dict) and li["tag"] == "li":
                p = container.add_paragraph(style=style_name)
                p.paragraph_format.line_spacing = LINE
                p.paragraph_format.space_after = Pt(6)
                render_inline(p, li["children"], STYLES["body"][0], STYLES["body"][2])
    elif tag == "img":
        render_image(container, node)
    elif tag == "table":
        render_table(container, node)
    elif tag == "div":
        if has_class(node, "callout-2col"):
            render_callout_2col(container, node)
        elif has_class(node, "callout"):
            render_callout(container, node["children"])
        else:
            render_blocks(container, node["children"])


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
CONTENT_WIDTH = Inches(6.5)


def render_image(container, node):
    src = node.get("attrs", {}).get("src", "")
    if not src or src.startswith(("http", "data:")):
        return
    path = pathlib.Path(src)
    if path.suffix.lower() not in IMAGE_EXTS or not path.exists():
        return
    p = new_paragraph(container, space_after=12)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    try:
        from docx.image.exceptions import UnrecognizedImageError
        try:
            p.add_run().add_picture(str(path), width=CONTENT_WIDTH)
        except UnrecognizedImageError:
            return
    except Exception:
        return


def inline_text(children):
    return "".join(t for kind, t, _ in collect_inline_segments(children, {}) if kind == "text").strip()


def iter_rows(table_node):
    rows = []

    def walk(n):
        for ch in n.get("children", []):
            if isinstance(ch, dict):
                if ch["tag"] == "tr":
                    rows.append(ch)
                else:
                    walk(ch)
    walk(table_node)
    return rows


def render_table(container, table_node):
    rows = iter_rows(table_node)
    if not rows:
        return
    matrix = []
    header_flags = []
    for tr in rows:
        cells = [c for c in tr["children"] if isinstance(c, dict) and c["tag"] in ("td", "th")]
        matrix.append(cells)
        header_flags.append(any(c["tag"] == "th" for c in cells))
    ncols = max((len(r) for r in matrix), default=0)
    if ncols == 0:
        return

    table = container.add_table(rows=len(matrix), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    align_table_full_width(table)
    set_col_widths(table, [CONTENT_W_IN / ncols] * ncols)
    set_table_borders(table, TABLE_BORDER, sz=6)
    set_table_cell_margins(table, 5)

    for ri, cells in enumerate(matrix):
        is_header = header_flags[ri]
        for ci in range(ncols):
            cell = table.cell(ri, ci)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            if is_header:
                set_cell_bg(cell, TABLE_HEADER_BG)
            else:
                set_cell_bg(cell, "FFFFFF")
            node = cells[ci] if ci < len(cells) else None
            render_cell(cell, node, bold=is_header)
    new_paragraph(container, space_after=4)


def render_cell(cell, node, bold=False):
    cell.paragraphs[0].text = ""
    if node is None:
        return
    block_children = [c for c in node["children"] if isinstance(c, dict) and c["tag"] in BLOCK_TAGS]
    if block_children:
        for c in node["children"]:
            if isinstance(c, dict) and c["tag"] in BLOCK_TAGS:
                render_block(cell, c)
    else:
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = LINE
        size, _, color, _ = STYLES["body"]
        segs = collect_inline_segments(node["children"], {"bold": bold})
        if not segs:
            return
        for kind, val, fmt in segs:
            if kind == "break":
                p.add_run().add_break()
            elif kind == "text":
                style_run(p.add_run(val), size, fmt.get("bold", False), color, fmt.get("italic", False))
            elif kind == "link":
                add_hyperlink(p, val, fmt)


CALLOUT_PAD_V = 19
CALLOUT_PAD_H = 18


def render_callout(container, children):
    table = container.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    align_table_full_width(table)
    set_col_widths(table, [CONTENT_W_IN])
    set_table_cell_margins(table, CALLOUT_PAD_V, 0, CALLOUT_PAD_V, 0)
    cell = table.cell(0, 0)
    fill_callout_cell(cell, children)
    pad_cell_paragraphs(cell, CALLOUT_PAD_H)
    new_paragraph(container, space_after=4)
    return table


def fill_callout_cell(cell, src):
    set_cell_bg(cell, CALLOUT_BG)
    cell.paragraphs[0].text = ""
    first_done = False
    for ch in src:
        if isinstance(ch, dict) and ch["tag"] == "div" and has_class(ch, "callout-title"):
            p = cell.paragraphs[0] if not first_done else cell.add_paragraph()
            p.paragraph_format.line_spacing = LINE
            p.paragraph_format.space_after = Pt(6)
            style_run(p.add_run(inline_text(ch["children"])), 11, True, CALLOUT_TEXT)
            first_done = True
        elif isinstance(ch, dict) and ch["tag"] == "div" and has_class(ch, "callout-body"):
            p = cell.paragraphs[0] if not first_done else cell.add_paragraph()
            p.paragraph_format.line_spacing = LINE
            render_inline(p, ch["children"], 11, CALLOUT_TEXT)
            first_done = True
        elif isinstance(ch, dict) and ch["tag"] in BLOCK_TAGS:
            render_block(cell, ch)
            first_done = True
        elif isinstance(ch, str) and ch.strip():
            p = cell.paragraphs[0] if not first_done else cell.add_paragraph()
            p.paragraph_format.line_spacing = LINE
            style_run(p.add_run(ch.strip()), 11, False, CALLOUT_TEXT)
            first_done = True


def render_callout_2col(container, node):
    callouts = [c for c in node["children"] if isinstance(c, dict) and c["tag"] == "div" and has_class(c, "callout")]
    if not callouts:
        render_blocks(container, node["children"])
        return
    gap_in = 0.2
    box_in = (CONTENT_W_IN - gap_in) / 2
    table = container.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    align_table_full_width(table)
    set_col_widths(table, [box_in, gap_in, box_in])
    set_table_cell_margins(table, CALLOUT_PAD_V, 0, CALLOUT_PAD_V, 0)
    fill_callout_cell(table.cell(0, 0), callouts[0]["children"])
    pad_cell_paragraphs(table.cell(0, 0), CALLOUT_PAD_H)
    if len(callouts) > 1:
        fill_callout_cell(table.cell(0, 2), callouts[1]["children"])
        pad_cell_paragraphs(table.cell(0, 2), CALLOUT_PAD_H)
    table.cell(0, 1).paragraphs[0].text = ""
    new_paragraph(container, space_after=4)


# -- Page builders ------------------------------------------------------------

def build_cover(doc, title, subtitle, date):
    sec = doc.sections[0]
    sec.page_width = Inches(PAGE_W_IN)
    sec.page_height = Inches(PAGE_H_IN)
    sec.top_margin = Inches(0.9)
    sec.bottom_margin = Inches(0.75)
    sec.left_margin = Inches(MARGIN_SIDE_IN)
    sec.right_margin = Inches(MARGIN_SIDE_IN)

    if COVER_BG_IMG.exists():
        add_full_page_background(sec.header, COVER_BG_IMG)

    logo_p = doc.add_paragraph()
    logo_p.paragraph_format.space_after = Pt(0)
    if LOGO_WORDMARK.exists():
        logo_p.add_run().add_picture(str(LOGO_WORDMARK), height=Pt(20))

    for _ in range(12):
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(0)
        sp.paragraph_format.line_spacing = 1.0
        style_run(sp.add_run(""), 18, False, TEXT_ON_DARK)

    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_after = Pt(12)
    title_p.paragraph_format.line_spacing = 1.05
    style_run(title_p.add_run(title), *STYLES["title"])

    if subtitle:
        sub_p = doc.add_paragraph()
        sub_p.paragraph_format.space_after = Pt(8)
        style_run(sub_p.add_run(subtitle), *STYLES["subtitle"])

    if date:
        date_p = doc.add_paragraph()
        date_p.paragraph_format.space_before = Pt(24)
        style_run(date_p.add_run(date), *STYLES["date"])


def start_body_section(doc):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.page_width = Inches(PAGE_W_IN)
    sec.page_height = Inches(PAGE_H_IN)
    sec.top_margin = Inches(MARGIN_TB_IN)
    sec.bottom_margin = Inches(MARGIN_TB_IN)
    sec.left_margin = Inches(MARGIN_SIDE_IN)
    sec.right_margin = Inches(MARGIN_SIDE_IN)

    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:start"), "1")
    sec._sectPr.append(pg)

    header = sec.header
    header.is_linked_to_previous = False
    if LOGO_MARK.exists():
        mark_p = header.paragraphs[0]
        mark_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        mark_p.add_run().add_picture(str(LOGO_MARK), height=Pt(16))

    footer = sec.footer
    footer.is_linked_to_previous = False
    add_page_number(footer.paragraphs[0])
    return sec


def add_section_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    run._r.append(br)


def build_separator(doc, title):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.page_width = Inches(PAGE_W_IN)
    sec.page_height = Inches(PAGE_H_IN)
    sec.top_margin = Inches(MARGIN_TB_IN)
    sec.bottom_margin = Inches(MARGIN_TB_IN)
    sec.left_margin = Inches(MARGIN_SIDE_IN)
    sec.right_margin = Inches(MARGIN_SIDE_IN)

    header = sec.header
    header.is_linked_to_previous = False
    if SECTION_BG_IMG.exists():
        add_full_page_background(header, SECTION_BG_IMG)

    for _ in range(16):
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(0)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(24)
    style_run(p.add_run(title), 24, True, TEXT_ON_DARK, display=True)


# -- Main ---------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        sys.exit("usage: build-doc.py <content.json> <output.docx>")
    content_path, out_path = sys.argv[1], sys.argv[2]
    with open(content_path, encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Untitled")
    subtitle = data.get("subtitle", "")
    date = data.get("date", "")
    sections = data.get("sections", []) or []
    separator_title = data.get("separator_title", "")

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(STYLES["body"][0])
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    set_theme_fonts(doc, FALLBACK_FONT)
    add_font_fallback(doc, BODY_FONT)
    add_font_fallback(doc, DISPLAY_FONT)
    add_font_fallback(doc, ITALIC_FONT, alt="Georgia")

    build_cover(doc, title, subtitle, date)
    start_body_section(doc)

    for i, section in enumerate(sections):
        if i > 0:
            add_section_page_break(doc)
        heading = section.get("heading", "")
        if heading:
            add_heading(doc, "h1", heading)
        render_blocks(doc, parse_html(section.get("html", "")))

    if separator_title:
        build_separator(doc, separator_title)

    doc.save(out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
