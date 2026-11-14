# Poetics brand rules

For anything branding-related — documents, decks, social assets, "is this on-brand" questions,
or writing copy for Poetics — read `brand-kit/brand.md` first. It's the single source of truth
for colors, typography, logo rules, voice/tone, and company facts. Never invent brand values not
present in that file.

To generate a branded document, PDF, or deck, don't hand-build the styling — run the renderer
scripts in `brand-kit/scripts/` (`build-doc.py`, `build-doc-pdf.py`, `build-deck.py`), which apply
the brand mechanically from structured content you provide. See `brand-kit/schemas/` for the
content format each script expects.

For social carousels or video thumbnails, open the self-contained editors in
`brand-kit/templates/*/editor.html` directly in a browser. For a finished feed carousel or story
(type, photo or framed style), write a deck JSON from `brand-kit/templates/social-styles/examples/`
and run `brand-kit/scripts/build-social.py`; read "Social feed styles" in `brand-kit/design-system.md` first.

For richer tool-calling (not just this file's static context), this repo also has an MCP server
at `mcp-server/` — see its README to connect it.
