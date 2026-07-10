# Poetics brand MCP server

Exposes `brand-kit/` (the portable brand core — spec, renderer scripts, schemas, guides) as an
[MCP](https://modelcontextprotocol.io) server, so any MCP-compatible editor or CLI gets the same
auto-triggering / tool-calling behavior the Claude Code plugin has — without being locked to
Claude Code. VS Code, Cursor, Windsurf, JetBrains, and Claude Desktop all support connecting to
MCP servers.

Same philosophy as `plugins/brand`: this file carries no brand knowledge itself. Every
resource/tool reads or calls straight through to `brand-kit/`. Edit `brand-kit/brand.md` and every
client, Claude Code plugin or MCP, picks it up immediately.

## What it exposes

**Resources** (read-only context):
- `brand://spec` — the full brand.md
- `brand://schema/document` — the JSON schema for `generate_branded_document`
- `brand://guide/voice` — voice/tone checklist and examples
- `brand://guide/portability` — using brand-kit outside any AI tool

**Tools** (actions):
- `generate_branded_document(content, output_path, format)` — writes a branded `.pdf` or `.docx`
- `generate_branded_deck(deck, output_path)` — writes a branded `.html`, `.pdf`, or `.pptx` deck
- `get_logo_path(variant, background)` — resolves the correct logo file for a given background
- `get_social_template_path(template)` — path to the carousel / video-thumb HTML editor

**Prompts** (reusable templates):
- `review_against_brand(asset_description)` — brand-compliance review, same rubric as the
  Claude Code `brand-review` skill
- `write_on_brand_copy(topic)` — on-brand copy drafting, grounded in the voice guide

## Requirements

Python **3.10+** for the server itself (the `mcp` SDK requires it — if your default `python3` is
older, the installer below finds a newer one automatically). The renderer scripts it calls into
(`brand-kit/scripts/*.py`) self-install their own dependencies (`python-docx`, `python-pptx`,
`playwright` + a one-time Chromium download for PDF export) the first time they run.

## Installing

**VS Code, Cursor, and Claude Code need zero setup.** This repo ships workspace-scoped MCP config
(`.vscode/mcp.json`, `.cursor/mcp.json`, `.mcp.json`) that those tools auto-discover the moment
you open the folder — the same trick as `.claude/settings.json` auto-enabling the Claude Code
plugin. Just clone the repo and open it.

**Claude Desktop and Windsurf** don't have a "workspace" concept to auto-discover config from, so
they need one command:

```bash
bash mcp-server/install.sh
```

This finds a Python 3.10+ interpreter, installs the SDK, and merges the `poetics-brand` entry into
whichever of those two it finds installed on your machine — safely: it only ever touches its own
entry, backs up the existing config first, and is a no-op if already configured (safe to re-run).
It never removes or overwrites any other MCP server you already have configured.

Restart whichever editor it configured to pick up the new server.

### Anything else (JetBrains AI Assistant, etc.)

`install.sh` only automates the two global-config tools above. For anything else, register the
server manually using this shape (wherever that tool defines MCP servers):

```json
{
  "command": "python3",
  "args": ["/absolute/path/to/poetics-skills/mcp-server/server.py"]
}
```

## Verifying it works

Once connected, ask the assistant in that editor something like *"what are Poetics's brand
colors?"* — it should read the `brand://spec` resource and answer from it, or *"generate a test
Poetics one-pager PDF"* — it should call `generate_branded_document`.

## Running it directly (debugging only)

```bash
python3 mcp-server/server.py
```

Starts a stdio MCP server — meant to be launched by an editor/client, not run interactively (it
just sits waiting for MCP messages on stdin/stdout, which is correct).
