#!/usr/bin/env python3
"""photo-library.py - the Poetics photo library for decks.

The photographs themselves stay on the owner's machine (this repo is public, and many
photographs show identifiable people). The repo keeps only an index:
brand-kit/photos/index.json, one entry per photograph with an id, what it shows, who is in
it, where it was taken and its shape. Decks refer to a photograph by id:

    "image": "photo:events-two-visitors-cinematic-11"

and build-deck.py resolves it against the library root:
    1. $POETICS_PHOTO_ROOT, if set
    2. "root" in index.json (default: the Poetics Website's own image folder)

Commands:
    python3 photo-library.py index [--root DIR]     rebuild index.json from the photos and the
                                                    website's alt text
    python3 photo-library.py list [--use USE]       print ids, shape and subject
    python3 photo-library.py sheet OUT.png [--use USE]
                                                    a captioned contact sheet, to choose from
USE is one of: cover, wide, portrait, people, team, any.
"""

import json
import os
import pathlib
import re
import sys

KIT = pathlib.Path(__file__).resolve().parent.parent
INDEX = KIT / "photos" / "index.json"
DEFAULT_ROOT = "~/Data/Projects/Poetics Website/src/assets/images"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def load_index():
    if not INDEX.exists():
        return {"root": DEFAULT_ROOT, "photos": []}
    return json.loads(INDEX.read_text(encoding="utf-8"))


def library_root(index=None):
    index = index or load_index()
    return pathlib.Path(os.environ.get("POETICS_PHOTO_ROOT") or index.get("root") or DEFAULT_ROOT).expanduser()


def resolve(photo_id):
    """The absolute path of a library photograph, or None."""
    index = load_index()
    for p in index.get("photos", []):
        if p["id"] == photo_id:
            path = library_root(index) / p["file"]
            return path if path.exists() else None
    return None


def website_alts(root: pathlib.Path):
    """Alt text the website already wrote, keyed by file name (from its .ts data and .md pages)."""
    src = root.parent.parent   # .../src/assets/images -> .../src
    alts = {}
    for f in list(src.rglob("*.ts")) + list(src.rglob("*.md")):
        if "node_modules" in f.parts:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Markdown front matter: "- src: ../path/file.jpg\n    alt: ..."
        for m in re.finditer(r"src:\s*\S*/([\w.-]+\.(?:jpe?g|png|webp))\s*\n\s*alt:\s*(.+)", text):
            alts.setdefault(m.group(1), m.group(2).strip().strip("'\""))
        # TypeScript: import name from '.../file.jpg' ... { src: name, alt: '...' }
        names = {m.group(1): m.group(2) for m in
                 re.finditer(r"import\s+(\w+)\s+from\s+'[^']*/([\w.-]+\.(?:jpe?g|png|webp))'", text)}
        for m in re.finditer(r"src:\s*(\w+),\s*alt:\s*'([^']+)'", text):
            if m.group(1) in names:
                alts.setdefault(names[m.group(1)], m.group(2))
    return alts


def describe(stem):
    words = re.sub(r"-\d+$", "", stem).split("-")
    return " ".join(words).capitalize() + "."


def build(root: pathlib.Path):
    from PIL import Image
    alts = website_alts(root)
    photos = []
    for f in sorted(root.rglob("*")):
        if f.suffix.lower() not in EXTS or "styleguide" in f.parts:
            continue
        with Image.open(f) as im:
            w, h = im.size
        rel = f.relative_to(root).as_posix()
        portrait = "portrait" in f.stem
        named = []
        if portrait:
            m = re.search(r"portrait-(.+?)-\d+$", f.stem)
            if m:
                named = [" ".join(x.capitalize() for x in m.group(1).split("-"))]
        shape = "portrait" if h > w * 1.05 else ("square" if abs(h - w) <= w * 0.05 else "landscape")
        uses = ["any"]
        if shape == "landscape" and w >= 1600:
            uses += ["cover", "wide"]
        if shape == "portrait":
            uses += ["portrait"]
        if portrait:
            uses = ["people"]
        team = any(k in f.stem for k in ("founders", "team"))
        if team:
            uses = ["team"]
        photos.append({
            "id": f.stem,
            "file": rel,
            "subject": alts.get(f.name) or describe(f.stem),
            "event": f.parent.name if f.parent != root else "",
            "people": ("Named person: " + ", ".join(named) + ". Use only on a page that names them.")
                      if named else ("The Poetics team. Use only when the user asks: decks leave the makers out."
                                     if team else "Visitors; not named."),
            "shape": shape,
            "size": [w, h],
            "use": uses,
            "focal": "top" if portrait else "center",
        })
    return photos


def pick(photos, use):
    return [p for p in photos if not use or use == "any" or use in p["use"]]


def sheet(photos, out, root):
    from PIL import Image, ImageDraw, ImageFont
    w, h, gap, cap, cols = 360, 240, 16, 52, 5
    rows = (len(photos) + cols - 1) // cols
    img = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * (h + cap) + (rows + 1) * gap), "#E5E8E3")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(str(KIT / "assets/fonts/InterTight-Variable.ttf"), 14)
    except Exception:
        font = ImageFont.load_default()
    for i, p in enumerate(photos):
        x, y = gap + (i % cols) * (w + gap), gap + (i // cols) * (h + cap + gap)
        try:
            with Image.open(root / p["file"]) as im:
                im = im.convert("RGB")
                im.thumbnail((w * 2, h * 2))
                r = max(w / im.width, h / im.height)
                im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
                left, top = (im.width - w) // 2, (im.height - h) // 2
                img.paste(im.crop((left, top, left + w, top + h)), (x, y))
        except Exception:
            pass
        draw.text((x, y + h + 6), p["id"][:48], fill="#121614", font=font)
        draw.text((x, y + h + 26), p["subject"][:52], fill="#5B625C", font=font)
    img.save(out)


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("index", "list", "sheet"):
        sys.exit(__doc__)
    use = args[args.index("--use") + 1] if "--use" in args else None
    index = load_index()
    if args[0] == "index":
        root = pathlib.Path(args[args.index("--root") + 1]).expanduser() if "--root" in args else library_root(index)
        if not root.exists():
            sys.exit(f"error: no photo library at {root} (set POETICS_PHOTO_ROOT or pass --root)")
        photos = build(root)
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        stored_root = DEFAULT_ROOT if root == pathlib.Path(DEFAULT_ROOT).expanduser() else str(root)
        INDEX.write_text(json.dumps({"root": stored_root, "photos": photos}, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
        print(f"Indexed {len(photos)} photographs from {root} -> {INDEX}")
    elif args[0] == "list":
        for p in pick(index["photos"], use):
            print(f'{p["id"]:<62} {p["shape"]:<9} {p["subject"]}')
    else:
        out = [a for a in args[1:] if not a.startswith("--") and a != use]
        if not out:
            sys.exit("usage: photo-library.py sheet OUT.png [--use USE]")
        sheet(pick(index["photos"], use), out[0], library_root(index))
        print(f"Wrote {out[0]}")


if __name__ == "__main__":
    main()
