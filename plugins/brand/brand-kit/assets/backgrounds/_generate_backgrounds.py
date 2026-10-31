#!/usr/bin/env python3
"""Regenerate the cinematic gradient backgrounds for docs and decks.

Produces deep blue-black fields with soft multi-color light bleeding from the
edges — evoking the Athens College deck's atmospheric lighting (cool blue,
faint warm/violet counterpoints) without needing photographic assets. Real
photo backgrounds, when available, go in ../backgrounds/photo/ and override
these per the renderer logic.

Run:  python3 _generate_backgrounds.py
Requires only Pillow.
"""
from PIL import Image, ImageFilter

CANVAS = (6, 7, 15)          # #06070F deep blue-black (matches the deck)

# Glow palette — cool-dominant, with faint warm/violet counterpoints, all low-intensity.
# Kept deliberately muted: in the reference deck color is a whisper in the dark, most of
# the frame stays deep blue-black. Text areas must remain legible, so glows sit in corners.
BLUE = (10, 70, 150)
CYAN = (20, 95, 145)
VIOLET = (55, 30, 95)
WARM = (110, 55, 35)

def make_bg(path, w, h, orbs, base=CANVAS):
    """orbs: list of (cx_frac, cy_frac, radius_frac, color, intensity 0..1).

    Built at low resolution and upscaled with blur for smooth, cheap gradients.
    """
    scale = 6
    lw, lh = max(1, w // scale), max(1, h // scale)
    img = Image.new("RGB", (lw, lh), base)
    px = img.load()
    for cxf, cyf, rf, color, inten in orbs:
        cx, cy, r = cxf * lw, cyf * lh, rf * max(lw, lh)
        r2 = r * r
        for y in range(lh):
            dy = y - cy
            for x in range(lw):
                dx = x - cx
                d2 = dx * dx + dy * dy
                if d2 >= r2:
                    continue
                # smooth falloff (cosine-like via squared term)
                t = (1.0 - (d2 / r2)) ** 2 * inten
                r0, g0, b0 = px[x, y]
                px[x, y] = (
                    min(255, int(r0 + (color[0] - r0) * t)),
                    min(255, int(g0 + (color[1] - g0) * t)),
                    min(255, int(b0 + (color[2] - b0) * t)),
                )
    img = img.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(max(w, h) / 140))
    img.save(path, quality=90)
    print("wrote", path, img.size)


# Document cover — portrait 8.5x11 @150dpi. Cool blue upper-right, faint violet lower-left.
make_bg("doc-cover-bg.jpg", 1275, 1650, [
    (0.88, 0.08, 0.50, BLUE, 0.32),
    (0.92, 0.06, 0.24, CYAN, 0.26),
    (0.05, 0.94, 0.36, VIOLET, 0.16),
])

# Document section divider — quieter, single cool glow lower-right.
make_bg("doc-section-bg.jpg", 1275, 1650, [
    (0.90, 0.90, 0.46, BLUE, 0.24),
    (0.10, 0.12, 0.30, VIOLET, 0.12),
])

# Deck default content slide — 16:9, cool glow drifting from the far right corner.
make_bg("deck-bg-default.jpg", 1920, 1080, [
    (0.94, 0.12, 0.46, BLUE, 0.26),
    (0.97, 0.16, 0.24, CYAN, 0.22),
    (0.03, 0.94, 0.34, VIOLET, 0.12),
])

# Deck title slide — most atmospheric, but left half stays dark for the headline.
# Cool blue from the right + a faint warm counterpoint, echoing the reference title lighting.
make_bg("deck-bg-title.jpg", 1920, 1080, [
    (0.90, 0.24, 0.52, BLUE, 0.34),
    (0.95, 0.16, 0.26, CYAN, 0.28),
    (0.70, 0.52, 0.30, WARM, 0.16),
    (0.10, 0.90, 0.34, VIOLET, 0.16),
])
