# Poetics Skills

On-brand document, presentation, and social asset generation for the Poetics team — backed by a
single branding spec that updates everything downstream when it changes.

**New here? Start with [`INSTALL.md`](INSTALL.md)** — step-by-step setup for whichever tool you
actually use (no AI, ChatGPT/Gemini, Claude Code, or VS Code/Cursor/Windsurf/JetBrains/Claude
Desktop via MCP).

Structurally inspired by Workable's internal Claude plugin marketplace ("fabric") — not included
in this repo, since it's marked internal-only in its own source. This repo is a much smaller,
leaner version of that pattern, built specifically for Poetics.

## Three ways to use this

### 1. Any AI tool, or by hand — `brand-kit/`

`brand-kit/` is the portable core: the brand spec, logo/font assets, and Python renderer scripts.
Nothing in it is Claude-specific. Point ChatGPT, Gemini, or any other tool at `brand-kit/brand.md`
as context, or skip AI entirely and run the scripts yourself. See
[`brand-kit/guides/using-outside-claude-code.md`](brand-kit/guides/using-outside-claude-code.md).

```
brand-kit/
├── brand.md              ← the single spec: colors, type, logo, voice/tone, company facts
├── assets/                 logos, self-hosted font files, generated glow backgrounds
├── scripts/                 build-doc.py / build-doc-pdf.py / build-deck.py — run these directly
├── templates/               self-contained HTML editors for social carousels & video thumbnails
├── schemas/                 the JSON content schema the scripts consume
└── guides/                  voice/tone guide, and the "outside Claude Code" guide
```

### 2. Claude Code — `plugins/brand`

A thin wrapper around the same `brand-kit/` files, packaged as a Claude Code plugin: skills
auto-trigger on natural requests ("make a Poetics deck," "write a branded doc," "is this
on-brand?") and take priority over Claude's generic `pptx`/`docx`/`pdf` skills.

**Zero-command install:** the marketplace registration and plugin install are committed in
`.claude/settings.json` — just `git clone` and open the repo in Claude Code, it's already active.
Confirm with `claude plugin list`.

### 3. Any MCP-compatible editor/CLI — `mcp-server/`

VS Code, Cursor, Windsurf, JetBrains, and Claude Desktop all support connecting to
[MCP](https://modelcontextprotocol.io) servers. `mcp-server/` wraps `brand-kit/` as MCP
resources/tools/prompts, so those tools get the same auto-triggering and tool-calling behavior as
the Claude Code plugin, without being locked to Claude Code.

**VS Code and Cursor:** zero-command — `.vscode/mcp.json` and `.cursor/mcp.json` are committed and
auto-discovered on opening the folder.
**Claude Desktop and Windsurf:** one command — `bash mcp-server/install.sh` (no project-folder
concept for those to auto-discover config from, so it safely merges the entry into their global
config for you).
See [`mcp-server/README.md`](mcp-server/README.md) for details and any other client.

Lighter-weight, config-only awareness (no tool-calling, just pointing the AI at `brand.md`) is
also wired up via `.cursorrules` and `.github/copilot-instructions.md` for editors that read
those files but don't yet support MCP.

## Updating the brand

Edit [`brand-kit/brand.md`](brand-kit/brand.md) directly and save. There's no build step, no
sync process, and no approval workflow — every skill and script reads the file fresh each time it
runs. If you're not sure what's safe to change, the file's own "Open questions" section flags
anything still unresolved.

## Repo layout

```
brand-kit/            portable brand core (see above) — works with or without Claude
marketplace.json       Claude Code marketplace manifest
.claude-plugin/         mirror consumed by Claude Code
.claude/settings.json   commits the plugin as pre-installed for anyone who clones the repo
plugins/brand/           the thin Claude Code skill wrapper
mcp-server/              MCP server wrapper + install.sh for Claude Desktop/Windsurf
.mcp.json, .vscode/mcp.json, .cursor/mcp.json   committed MCP config, auto-discovered on open
.cursorrules             lightweight brand pointer for Cursor
.github/copilot-instructions.md   lightweight brand pointer for GitHub Copilot
fabric-master/           Workable's reference marketplace (untouched, for inspiration only)
```

## Status

Built 2026-07-10. Real logo masters (SVG + PNG, light/dark variants) and the document/deck/social
renderers are aligned to the Athens College deck aesthetic: deep blue-black canvas, Inter display
type with occasional Cormorant italic accents, and cinematic gradient backgrounds (with a drop-in
folder at `brand-kit/assets/backgrounds/photo/` for real photos).

Remaining open items are in `brand.md`'s "Open questions for Thanos" section: the accent color
(ember vs. electric blue — currently electric blue `#0099FF` pending confirmation) and a fuller
About/company story. Real background photos from the deck can be dropped in whenever available.
