# Poetics brand — Claude chat Skill

This is a **different distribution channel** from `plugins/brand/` (the Claude Code plugin) and
`mcp-server/` (the MCP server for IDEs). Those two assume a local git clone on disk. This one is
for **claude.ai and Claude Desktop chat**, which run Skills in a hosted, sandboxed environment
with no access to your local files — so everything the skill needs (spec, fonts, logos, renderer
scripts, templates) is bundled inside `poetics-brand/` itself.

## Installing

1. Download [`poetics-brand.zip`](poetics-brand.zip) from this folder (it's a zipped copy of the
   `poetics-brand/` directory next to this README).
2. In claude.ai or Claude Desktop: **Settings → Capabilities → Skills** → upload the zip.
3. Start a new conversation and ask something like *"what are Poetics's brand colors?"* or
   *"write a branded one-pager about X"* — the skill should trigger automatically.

If you change anything in `brand-kit/` (the portable core used by the other two paths) and want
the chat Skill to match, re-run the sync + zip step below and re-upload — this bundle is a copy,
not a live link, so it doesn't update itself.

## Keeping it in sync with brand-kit/

This bundle started as a straight copy of `brand-kit/`'s `brand.md`, `assets/`, `scripts/`,
`templates/`, `schemas/`, and the voice guide — with one consolidated `SKILL.md` replacing the
Claude Code plugin's per-capability `SKILL.md` + `GLOBAL_RULES.md` split (chat Skills work better
as a single upload than seven). To refresh it after editing `brand-kit/`:

```bash
cd claude-skills
rm -rf poetics-brand/assets poetics-brand/scripts poetics-brand/templates poetics-brand/schemas poetics-brand/guides
cp -R ../brand-kit/assets poetics-brand/assets
cp -R ../brand-kit/scripts poetics-brand/scripts
cp -R ../brand-kit/templates poetics-brand/templates
cp -R ../brand-kit/schemas poetics-brand/schemas
mkdir poetics-brand/guides
cp ../brand-kit/guides/{writing-on-brand-copy,proposal-playbook,deck-copy,anti-slop}.md poetics-brand/guides/
cp ../brand-kit/brand.md ../brand-kit/design-system.md poetics-brand/
find poetics-brand -name __pycache__ -prune -exec rm -rf {} +
rm -f poetics-brand.zip && zip -rq poetics-brand.zip poetics-brand -x "*.DS_Store" "*__pycache__*"
```

`../brand-kit` is a symlink to `plugins/brand/brand-kit`, the real folder. The photo index
(`brand-kit/photos/`) is left out on purpose: it points at photographs on the owner's machine,
which a hosted chat skill can't reach, so in claude.ai decks ask the user to upload photos.

(`SKILL.md` itself isn't touched by this sync — it's hand-written, not copied from `brand-kit/`;
update it manually if the routing logic or trigger phrases need to change.)

## What's verified vs. not

The bundled renderer scripts (`build-doc.py`, `build-doc-pdf.py`, `build-deck.py`) were tested
directly from this new location and produce identical output to `brand-kit/`'s copies — the
path-resolution logic is relative, so bundling didn't require any script changes.

What's **not** verified from this environment: actually uploading the zip to claude.ai/Claude
Desktop and confirming it triggers correctly in a live chat — that requires the claude.ai UI,
which isn't accessible from here. If it doesn't trigger or doesn't run scripts as expected once
uploaded, that's useful to report back.
