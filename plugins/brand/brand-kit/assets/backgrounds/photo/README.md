# Photo backgrounds (drop-in)

The renderers use the generated gradient backgrounds (`../deck-bg-*.jpg`, `../doc-*-bg.jpg`) by
default. Drop real atmospheric photos here to use them instead — the kind of full-bleed, dark,
dramatically-lit imagery in the Athens College deck (a rim-lit figure in red/blue light, a warm
amber silhouette, a dark venue interior).

## How it works

Name a file to match the slot you want it to fill, and the renderers pick it up automatically:

| Filename (any of `.jpg .jpeg .png .webp`) | Used for |
|---|---|
| `deck-title.*` | Deck title + closing slides |
| `deck-default.*` | Deck content/section slides |
| `doc-cover.*` | Document/PDF cover page |
| `doc-section.*` | Document/PDF section-divider page |

If a matching file is present here, it overrides the generated gradient. If not, the gradient is
used. You can add just one (e.g. only `deck-title.jpg`) and leave the rest as gradients.

## What makes a good background photo

Per `brand.md`: full-bleed, graded **dark and cool**, treated as texture — never a bright or busy
image that fights the text. The text sits on top in white/gray, so:

- Keep the **left third dark** (headlines are left-aligned).
- Aim for a single dominant light source bleeding from a corner/edge, mostly shadow elsewhere.
- No text, logos, or busy detail baked into the image.
- Export at the slot's native size or larger: decks at **1920×1080**, doc cover/section at
  **1275×1650** (portrait). Larger is fine — the renderer covers-and-crops.

If you have raw photos that are too bright or not graded, tell Claude "grade these for Poetics
backgrounds" and it can darken/cool/crop them to fit before dropping them here.
