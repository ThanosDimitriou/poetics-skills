#!/usr/bin/env python3
"""audit-deck.py - check a deck's links, images and sources before it goes out.

    python3 audit-deck.py <deck.json> [--offline]

Writes <deck>-audit.md beside the deck and exits 1 if anything fails. Checks:

  links    every URL in the deck (title-card links, sources, anything starting with http)
           answers with HTTP 2xx/3xx; --offline skips this
  images   every image resolves (library ids and paths) and is large enough for its place
  sources  every curation title card (W1/work) lists sources, each with a URL, and every
           source is marked "checked": true by the person or agent who opened it and
           confirmed the fact; every still has an image_credit
  text     no [PLACEHOLDER] left (unless the deck is a draft)

A script can only confirm that a link answers. Whether the page says what the slide says is the
audit round in the deck skill: open each source, compare it with the fact, then set
"checked": true (or fix the slide).
"""

import importlib.util
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
URL_RE = re.compile(r"https?://[^\s\"'<>]+")
PH_RE = re.compile(r"\[[A-Z][A-Z0-9 _/&+.'’\-]*(?::[^\]]*)?\]")


def load_builder():
    spec = importlib.util.spec_from_file_location("build_deck", HERE / "build-deck.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pages(deck):
    """Every slide, with A1 sections flattened, as (label, slide)."""
    for k, s in enumerate(deck.get("slides", []), 1):
        yield f"page {k}", s
        for j, sec in enumerate(s.get("sections") or [], 1):
            yield f"page {k}.{j}", sec


def strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from strings(x)


def check_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Poetics deck audit)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.status < 400, f"{r.status}" + (f" → {r.url}" if r.url != url else "")
        except urllib.error.HTTPError as err:
            if method == "HEAD" and err.code in (403, 405, 501):
                continue
            return False, f"HTTP {err.code}"
        except Exception as err:   # DNS, timeout, TLS
            if method == "HEAD":
                continue
            return False, type(err).__name__
    return False, "no answer"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    deck_path = pathlib.Path(args[0]).resolve()
    deck = json.loads(deck_path.read_text(encoding="utf-8"))
    offline = "--offline" in sys.argv
    bd = load_builder()
    bd._ALLOWED_EXTRA.append(deck_path.parent)
    rows, failed = [], 0

    def add(check, where, ok, detail):
        nonlocal failed
        failed += 0 if ok else 1
        rows.append((check, where, "ok" if ok else "FAIL", detail))

    seen = set()
    for where, s in pages(deck):
        s = bd.resolve_template(s, where)
        stype = s.get("type")
        # links
        for text in strings({k: v for k, v in s.items() if k != "notes"}):
            for url in URL_RE.findall(text):
                if url in seen or offline:
                    continue
                seen.add(url)
                ok, detail = check_url(url)
                add("link", where, ok, f"{url} ({detail})")
        # images
        imgs = [s.get("image")] + [im if isinstance(im, str) else (im or {}).get("src") for im in s.get("images") or []]
        imgs += [c.get("image") for c in (s.get("columns") or s.get("people") or []) if isinstance(c, dict)]
        for src in [i for i in imgs if i]:
            uri = bd.resolve_image(src)
            if not uri:
                add("image", where, False, f"{src} not found")
                continue
            try:
                import base64
                import io
                from PIL import Image
                w, h = Image.open(io.BytesIO(base64.b64decode(uri.split(",", 1)[1]))).size
                need = 1600 if stype in ("cover", "media", "work") else 900
                add("image", where, w >= need, f"{src} {w}×{h}" + ("" if w >= need else f" (needs {need}px wide)"))
            except Exception as err:
                add("image", where, False, f"{src} unreadable ({type(err).__name__})")
        # sources on curation title cards
        if stype == "work":
            title = s.get("title", "?")
            srcs = s.get("sources") or []
            if not srcs:
                add("sources", where, False, f"{title}: no sources")
            for src in srcs:
                url, fact = src.get("url", ""), src.get("fact", "?")
                if not URL_RE.match(url or ""):
                    add("sources", where, False, f"{title}: '{fact}' has no URL")
                elif not src.get("checked"):
                    add("sources", where, False, f"{title}: '{fact}' not checked against {url}")
                else:
                    add("sources", where, True, f"{title}: '{fact}' checked ({url})")
            if s.get("image") and not s.get("image_credit"):
                add("sources", where, False, f"{title}: still has no image_credit")
            elif s.get("image_credit"):
                add("sources", where, not PH_RE.search(s["image_credit"]), f"{title}: credit '{s['image_credit']}'")
        # placeholders
        if not deck.get("draft"):
            for text in strings(s):
                for m in PH_RE.findall(text):
                    add("text", where, False, f"placeholder left: {m}")

    out = deck_path.with_name(deck_path.stem + "-audit.md")
    lines = [f"# Audit: {deck.get('title', deck_path.name)}", "",
             f"{len(rows) - failed} passed, {failed} failed" + (" (links not checked: --offline)" if offline else ""), "",
             "| Check | Where | Result | Detail |", "| --- | --- | --- | --- |"]
    lines += [f"| {c} | {w} | {r} | {d.replace('|', '/')} |" for c, w, r, d in rows]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}: {len(rows) - failed} passed, {failed} failed")
    for c, w, r, d in rows:
        if r == "FAIL":
            print(f"  - {w} [{c}] {d}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
