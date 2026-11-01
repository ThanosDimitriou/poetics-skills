#!/usr/bin/env python3
"""build-social-editors.py - build the two social editors from their sources.

    python3 build-social-editors.py

Reads templates/_src/ (social-post.html, video-thumb.html, social-common.js) and writes
templates/social-carousel/editor.html and templates/video-thumb/editor.html: single files that
work offline, by double-click, with the website's fonts (Instrument Serif, Inter Tight, Greek
included) and wordmark embedded. Edit the sources, then run this; never edit editor.html by hand.
"""

import base64
import importlib.util
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
SRC = KIT / "templates/_src"

spec = importlib.util.spec_from_file_location("build_deck", HERE / "build-deck.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)


def font_faces_js():
    faces = []
    for family, weight, filename, urange in bd.FONT_FACES:
        path = KIT / "assets/fonts" / filename
        if path.exists():
            uri = "data:font/woff2;base64," + base64.b64encode(path.read_bytes()).decode()
            faces.append([family, weight, uri, urange])
    return json.dumps(faces)


def build(src_name, out_rel):
    html = (SRC / src_name).read_text(encoding="utf-8")
    common = (SRC / "social-common.js").read_text(encoding="utf-8")
    wordmark = (KIT / "assets/logos/wordmark-mono.svg").read_text(encoding="utf-8").strip()
    html = (html.replace("/*COMMON_JS*/", common)
                .replace("/*FONT_FACES*/", font_faces_js())
                .replace("__WORDMARK_SVG__", json.dumps(wordmark))
                .replace("/*UI_FONTS*/", "/* Fonts load once, from the script below, for the canvas and this panel. */"))
    out = KIT / "templates" / out_rel
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    build("social-post.html", "social-carousel/editor.html")
    build("video-thumb.html", "video-thumb/editor.html")
