#!/usr/bin/env python3
"""build-social.py - render Poetics feed posts and stories (Instagram, LinkedIn, TikTok) to PNG.

    python3 build-social.py deck.json [OUT_DIR] [--tile 360]

--tile sets the width of each slide in contact-sheet.png (default 270).

The social styles (see design-system.md, "Social feed styles"): three layouts, a few treatments.

  type    Type only. Solid ground (paper, paper-deep, dark, dark-deep, lens), big serif lines,
          a little grain. Optional "outline": an empty pill drawn as a line, with an optional line of text.
  photo   Full-bleed photograph, big serif lines on a soft dark shade at the bottom.
          "treatment": "natural" (default) or "duotone" (ink, lens blue and paper; grain on).
  framed  Light, airy: every photograph inside a pill or a lens frame. "arrangement":
            cover  lines on top, one big pill photograph below
            rows   three rows, a word over a pill-shaped photograph band   rows: [{t, photo, focal}]
            lens   one lens photograph (h: height), lines below, optional sub
            pair   two tall pills side by side, lines below                photos: [{photo, focal}]
            close  lines, an email link, a lens photograph below

deck.json:
  {"format": "post" | "story",          4:5 (1080 x 1350, default) or 9:16 (1080 x 1920, top and bottom 250px clear)
   "grain": true | false,               false turns the texture off everywhere
   "slides": [{"layout": "photo", "photo": "<library id or file path>", "focal": "50% 40%", "zoom": 1.1,
               "valign": "bottom" | "center" | "top", "scrim": true,
               "lines": [{"t": "Immersive cinema,", "max": 128}, {"t": "anywhere.", "max": 268}],
               "sub": "...", "link": "hello@poeticsvr.com"}, ...]}

Each line is sized to fill the 900px column, up to "max" (default 150), so a line never overflows.
Every render is checked: lines inside the 90px margins, clear of the wordmark (and, in a story, of the
app's interface), text not over a framed photograph. The copy is checked against guides/anti-slop.md's
rules (em dashes, exclamation marks, stock words). Problems print as PROBLEM / COPY lines; fix them.

Needs Playwright with Chrome (Claude Code; not claude.ai chat). Photographs: ids from photos/index.json
(see PHOTOS-SETUP.md), or a path to a file.
"""
import base64, html, importlib.util, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
spec = importlib.util.spec_from_file_location("photolib", HERE / "photo-library.py")
photolib = importlib.util.module_from_spec(spec); spec.loader.exec_module(photolib)

GROUNDS = {  # bg, ink, soft, accent (the one pressable thing: the email link), wordmark, dark?
    "paper":      dict(bg="#EFF0EC", ink="#121614", soft="#5B625C", accent="#16249C", mark="#121614", dark=False),
    "paper-deep": dict(bg="#E5E8E3", ink="#121614", soft="#5B625C", accent="#16249C", mark="#121614", dark=False),
    "dark":       dict(bg="#121614", ink="#F4F5F3", soft="#8A918B", accent="#8F9CFF", mark="#F4F5F3", dark=True),
    "dark-deep":  dict(bg="#1C211E", ink="#F4F5F3", soft="#8A918B", accent="#8F9CFF", mark="#F4F5F3", dark=True),
    "lens":       dict(bg="#16249C", ink="#EFF0EC", soft="rgba(239,240,236,.72)", accent="#EFF0EC", mark="#EFF0EC", dark=True),
}
INK, PAPER, LENS = (18, 22, 20), (239, 240, 236), (22, 36, 156)
MARGIN, COLUMN = 90, 900


GREEK = "U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF"


def font_face(family, weight, file, urange=None):
    data = base64.b64encode((KIT / "assets/fonts" / file).read_bytes()).decode()
    rng = f"unicode-range:{urange};" if urange else ""
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};font-display:block;{rng}"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}")


FONTS = "".join([  # Latin and Greek: the same families as the decks
    font_face("Instrument Serif", 400, "InstrumentSerif-Regular-latin.woff2"),
    font_face("Instrument Serif", 400, "NotoSerifDisplay-w70-greek.woff2", GREEK),
    font_face("Inter Tight", 400, "InterTight-400-latin.woff2"),
    font_face("Inter Tight", 400, "InterTight-400-greek.woff2", GREEK),
    font_face("Inter Tight", 500, "InterTight-500-latin.woff2"),
    font_face("Inter Tight", 500, "InterTight-500-greek.woff2", GREEK),
])
WORDMARK = (KIT / "assets/logos/wordmark-mono.svg").read_text().replace('width="148" height="20"', 'width="100%" height="100%"')


def photo_uri(ref):
    p = pathlib.Path(ref).expanduser()
    if ("/" in ref or "." in ref) and p.exists():
        return p.resolve().as_uri()
    found = photolib.resolve(ref)
    if not found:
        sys.exit(f"photo not found: {ref} (an id from photos/index.json, or a file path; see PHOTOS-SETUP.md)")
    return found.as_uri()


def esc(s): return html.escape(s or "")


# ---- copy check: the same rules as the editors and guides/anti-slop.md -------------------------------
SLOP = ["journey", "seamless", "unforgettable", "magical", "magic", "cutting-edge", "revolutionary", "revolutionize",
        "solution", "leverage", "unlock", "next-generation", "elevate", "game-changing", "delve", "empower",
        "world-class", "bespoke", "hassle-free", "step into", "like never before", "redefin", "reimagin",
        "the future of", "immerse yourself", "dive into", "ready when you are", "let's", "shall we", "breathtaking",
        "beyond imagination"]


def copy_issues(text):
    out, low = [], text.lower()
    if "—" in text: out.append("an em dash (use a colon, comma or full stop)")
    if "!" in text: out.append("an exclamation mark")
    if re.search(r"\*[^*]+\*", text): out.append("*asterisks* (there are no italics)")
    if re.search(r"\b[A-Z]{4,}\b", re.sub(r"\b(VR|AR|XR|TIF|LBVR)\b", "", text)): out.append("capitals (use sentence case)")
    if re.search("[\U0001F300-\U0001FAFF☀-➿]", text): out.append("an emoji")
    hit = next((w for w in SLOP if w in low), None)
    if hit: out.append(f'"{hit}" reads as stock copy')
    return out


def slide_texts(s):
    t = [l["t"] for l in s.get("lines", [])] + [s.get("sub", ""), s.get("link", "")]
    t += [r["t"] for r in s.get("rows", [])] + [(s.get("outline") or {}).get("text", "")]
    return [x for x in t if x]


# ---- texture -----------------------------------------------------------------------------------------
NOISE = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='360' height='360'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 {c}  0 0 0 0 {c}  0 0 0 0 {c}  0 0 0 {a} 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")


def grain(dark, strong=False):
    c, a, blend, op = (1, .9, "screen", .12 if strong else .06) if dark else (0, 1.1, "multiply", .08)
    return (f'<div class="grain" style="background-image:url(&quot;{NOISE.format(c=c, a=a)}&quot;);'
            f'mix-blend-mode:{blend};opacity:{op}"></div>')


def duo_filter():
    t = lambda i: " ".join(f"{c[i] / 255:.4f}" for c in (INK, LENS, PAPER))
    return ('<svg width="0" height="0" style="position:absolute"><filter id="duo" color-interpolation-filters="sRGB">'
            '<feColorMatrix type="matrix" values=".2126 .7152 .0722 0 0 .2126 .7152 .0722 0 0 .2126 .7152 .0722 0 0 0 0 0 1 0"/>'
            f'<feComponentTransfer><feFuncR type="table" tableValues="{t(0)}"/><feFuncG type="table" tableValues="{t(1)}"/>'
            f'<feFuncB type="table" tableValues="{t(2)}"/></feComponentTransfer></filter></svg>')


# ---- slides ------------------------------------------------------------------------------------------
def build(deck):
    story = deck.get("format") == "story"
    H = 1920 if story else 1350
    mark_top, txt_bottom, txt_top = (270, 300, 440) if story else (84, 120, 190)
    oy = 230 if story else 0                      # framed content starts 72px below the wordmark
    shift = (H - 1350) // 2 if story else 0       # an explicit "top" is written for the 4:5 canvas
    grain_on = deck.get("grain", True)

    css = FONTS + f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#777}}
.slide{{position:relative;width:1080px;height:{H}px;overflow:hidden;font-family:'Inter Tight',sans-serif;font-weight:400}}
.bg{{position:absolute;inset:0;background-size:cover;background-repeat:no-repeat}}
.scrim{{position:absolute;inset:0}}
.scrim.bottom{{background:linear-gradient(to top,rgba(8,10,9,.80) 0%,rgba(8,10,9,.55) 30%,rgba(8,10,9,.12) 58%,rgba(8,10,9,0) 70%)}}
.scrim.top{{background:linear-gradient(to bottom,rgba(8,10,9,.80) 0%,rgba(8,10,9,.55) 30%,rgba(8,10,9,.12) 58%,rgba(8,10,9,0) 70%)}}
.scrim.center{{background:rgba(8,10,9,.42)}}
.scrim.top-only{{background:linear-gradient(to bottom,rgba(8,10,9,.86) 0%,rgba(8,10,9,.66) 10%,rgba(8,10,9,.28) 20%,rgba(8,10,9,0) 32%)}}
.grain{{position:absolute;inset:0;pointer-events:none}}
.mark{{position:absolute;left:{MARGIN}px;top:{mark_top}px;width:{36 * 148 / 20:.0f}px;height:36px}}
.txt{{position:absolute;left:{MARGIN}px;right:{MARGIN}px;display:flex;flex-direction:column}}
.txt.bottom{{bottom:{txt_bottom}px}} .txt.top{{top:{txt_top}px}} .txt.center{{top:0;bottom:0;justify-content:center}}
.blk{{position:absolute;left:{MARGIN}px;width:{COLUMN}px;display:flex;flex-direction:column}}
.ln{{display:block;font-family:'Instrument Serif',Georgia,serif;letter-spacing:-0.035em;white-space:nowrap;
  width:max-content;line-height:.92}}
.ln + .ln{{margin-top:-.04em}}
.sub{{font-size:34px;line-height:1.3;margin-top:34px}}
.link{{font-family:'Instrument Serif',Georgia,serif;font-size:68px;letter-spacing:-0.02em;margin-top:40px}}
.fr{{position:absolute;left:0;top:{oy}px;width:1080px;height:1350px}}
.fr .sub{{margin-top:26px}} .fr .link{{margin-top:30px}}
.ph{{position:absolute;background-size:cover;background-repeat:no-repeat}}
.outline{{position:absolute;left:{MARGIN}px;width:{COLUMN}px;display:flex;align-items:center;justify-content:center;
  text-align:center;border-style:solid;border-width:3px}}
"""

    def lines(ls, color=""):
        return "".join(
            f'<span class="ln" data-max="{l.get("max", l.get("size", 150))}" style="font-size:100px;{color}">{esc(l["t"])}</span>'
            for l in ls)

    def framed_photo(pid, focal, x, y, w, h, radius, bg):
        return (f'<div class="ph" style=\'left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{radius}px;'
                f'background-color:{bg};background-image:url("{photo_uri(pid)}");background-position:{focal or "50% 50%"}\'></div>')

    def slide(s, i):
        L = s["layout"]
        g = GROUNDS[s.get("ground", "dark" if L == "photo" else "paper")]
        ink = f'color:{g["ink"]};'
        mark = WORDMARK.replace('fill="#121614"', f'fill="{g["mark"]}"')
        want_grain = s.get("grain", L == "type" or (L == "photo" and s.get("treatment") == "duotone"))
        tex = grain(g["dark"], s.get("ground") == "lens" or L == "photo") if (grain_on and want_grain) else ""
        body, extras = "", ""
        if L == "photo":
            focal = s.get("focal", "50% 50%")
            filt = "filter:contrast(1.15) url(#duo);" if s.get("treatment") == "duotone" else ""
            body += (f'<div class="bg" style=\'background-image:url("{photo_uri(s["photo"])}");background-position:{focal};'
                     f'transform:scale({s.get("zoom", 1)});transform-origin:{focal};{filt}\'></div>')
            valign = s.get("valign", "bottom")
            if s.get("lines") and s.get("scrim", True):
                body += f'<div class="scrim {valign}"></div>'
            else:
                body += '<div class="scrim top-only"></div>'
            sub = f'<div class="sub" style="color:rgba(244,245,243,.78)">{esc(s["sub"])}</div>' if s.get("sub") else ""
            link = f'<div class="link" style="color:{g["accent"]}">{esc(s["link"])}</div>' if s.get("link") else ""
            if s.get("lines"):
                body += f'<div class="txt {valign}">{lines(s["lines"], ink)}{sub}{link}</div>'
        elif L == "type":
            valign = s.get("valign", "top")
            sub_c = "rgba(244,245,243,.78)" if g["dark"] and s.get("ground") != "lens" else g["soft"]
            sub = f'<div class="sub" style="color:{sub_c}">{esc(s["sub"])}</div>' if s.get("sub") else ""
            link = f'<div class="link" style="color:{g["accent"]}">{esc(s["link"])}</div>' if s.get("link") else ""
            if "top" in s:
                body += f'<div class="blk" style="top:{s["top"] + shift}px">{lines(s["lines"], ink)}{sub}{link}</div>'
            else:
                body += f'<div class="txt {valign}">{lines(s["lines"], ink)}{sub}{link}</div>'
            o = s.get("outline")
            if o:
                oh = o.get("h", 380)
                inner = f'<span style="font-size:36px;color:{g["soft"]}">{esc(o["text"])}</span>' if o.get("text") else ""
                body += (f'<div class="outline" style="bottom:{o.get("bottom", txt_bottom + 30)}px;height:{oh}px;'
                         f'border-radius:{oh / 2}px;border-color:{g["ink"]}">{inner}</div>')
        elif L == "framed":
            a, bgc = s["arrangement"], "#E5E8E3"
            sub = f'<div class="sub" style="color:{g["soft"]}">{esc(s["sub"])}</div>' if s.get("sub") else ""
            link = f'<div class="link" style="color:{g["accent"]}">{esc(s["link"])}</div>' if s.get("link") else ""
            if a == "cover":
                body += f'<div class="blk" style="top:192px">{lines(s["lines"], ink)}</div>'
                body += framed_photo(s["photo"], s.get("focal"), 90, 690, 900, 570, 285, bgc)
            elif a == "rows":
                y = 192
                for r in s["rows"]:
                    body += f'<div class="blk" style="top:{y}px">{lines([{"t": r["t"], "max": 170}], ink)}</div>'
                    body += framed_photo(r["photo"], r.get("focal"), 90, y + 168, 900, 160, 80, bgc)
                    y += 357
            elif a == "lens":
                h = s.get("h", 700)
                body += framed_photo(s["photo"], s.get("focal"), 90, 192, 900, h, 48, bgc)
                body += f'<div class="blk" style="top:{192 + h + 44}px">{lines(s["lines"], ink)}{sub}</div>'
            elif a == "pair":
                for k, p in enumerate(s["photos"]):
                    body += framed_photo(p["photo"], p.get("focal"), 90 + k * 470, 192, 430, 560, 215, bgc)
                body += f'<div class="blk" style="top:800px">{lines(s["lines"], ink)}</div>'
            elif a == "close":
                body += f'<div class="blk" style="top:192px">{lines(s["lines"], ink)}{link}</div>'
                body += framed_photo(s["photo"], s.get("focal"), 90, 700, 900, 560, 48, bgc)
            else:
                sys.exit(f"slide {i}: unknown framed arrangement {a!r}")
            body = f'<div class="fr">{body}</div>'
        else:
            sys.exit(f"slide {i}: unknown layout {L!r} (type, photo, framed)")
        return f'<section class="slide" id="s{i}" style="background:{g["bg"]}">{body}{tex}<div class="mark">{mark}</div></section>'

    slides = deck["slides"]
    page = (f"<!doctype html><meta charset=utf-8><style>{css}</style><body>{duo_filter()}"
            + "".join(slide(s, i) for i, s in enumerate(slides, 1)) + "</body>")
    return page, slides, story, H


CHECK_JS = """([id, story, safeTop, safeBottom]) => { const out = [], sl = document.getElementById(id).getBoundingClientRect();
  const texts = [...document.querySelectorAll('#'+id+' .ln, #'+id+' .link, #'+id+' .sub')];
  const phs = [...document.querySelectorAll('#'+id+' .ph')].map(p => p.getBoundingClientRect());
  texts.forEach(e => { const r = e.getBoundingClientRect(), name = e.textContent;
    if (r.left - sl.left < 89 || r.right - sl.left > 991) out.push('outside the margins: ' + name);
    if (r.top - sl.top < safeTop) out.push((story ? 'in the top 250px: ' : 'too close to the wordmark: ') + name);
    if (r.bottom - sl.top > safeBottom) out.push((story ? 'in the bottom 250px: ' : 'too close to the foot: ') + name);
    phs.forEach(q => { if (r.left < q.right && r.right > q.left && r.top < q.bottom - 4 && r.bottom > q.top + 4)
      out.push('over a photograph: ' + name); }); });
  return out; }"""


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); return 0
    tile = None                                   # --tile N: width of each slide in contact-sheet.png
    if "--tile" in args:
        k = args.index("--tile"); tile = int(args[k + 1]); del args[k:k + 2]
    src = pathlib.Path(args[0]).resolve()
    out = pathlib.Path(args[1]).resolve() if len(args) > 1 else src.parent
    deck = json.loads(src.read_text())
    page, slides, story, H = build(deck)
    out.mkdir(parents=True, exist_ok=True)
    html_path = out / "_social.html"
    html_path.write_text(page, encoding="utf-8")
    problems = 0
    for i, s in enumerate(slides, 1):
        for t in slide_texts(s):
            for msg in copy_issues(t):
                print(f"COPY slide {i}: {msg}: {t}"); problems += 1

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="chrome")
        except Exception:
            b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": H})
        pg.goto(html_path.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(1500)
        pg.evaluate("""() => document.querySelectorAll('.ln').forEach(e => {
            e.style.fontSize = '100px'; const w = e.getBoundingClientRect().width;
            e.style.fontSize = Math.min(+e.dataset.max, 100 * 900 / w) + 'px'; })""")
        names = []
        for i, s in enumerate(slides, 1):
            bad = pg.evaluate(CHECK_JS, [f"s{i}", story, 250 if story else 156, 1670 if story else 1262])
            name = f"{i:02d}-{s.get('arrangement') or s['layout']}.png"
            pg.locator(f"#s{i}").screenshot(path=str(out / name))
            names.append(name)
            problems += len(bad)
            print(name, "ok" if not bad else "PROBLEM " + "; ".join(bad))
        # contact sheet: all slides side by side, for a quick look
        w = tile or (252 if story else 270); h = round(w * (16 / 9 if story else 5 / 4))
        cols = min(3 if tile and tile >= 340 else 4, len(names)); rows = -(-len(names) // cols)
        tiles = "".join(f'<img src="{(out / n).as_uri()}" style="width:{w}px;height:{h}px;margin:0 10px 10px 0">' for n in names)
        sheet = out / "_sheet.html"
        sheet.write_text(f'<body style="margin:0;background:#1e1e1e;padding:10px 0 0 10px;width:{cols * (w + 10) + 10}px">{tiles}</body>')
        pg2 = b.new_page(viewport={"width": cols * (w + 10) + 10, "height": rows * (h + 10) + 10})
        pg2.goto(sheet.as_uri()); pg2.wait_for_timeout(500)
        pg2.screenshot(path=str(out / "contact-sheet.png")); sheet.unlink()
        b.close()
    html_path.unlink()
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
