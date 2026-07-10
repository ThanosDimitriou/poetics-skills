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

Python **3.10+** (the `mcp` SDK requires it — if your default `python3` is older, point the
config at a newer interpreter, e.g. a Homebrew Python).

```bash
python3 -m pip install -r requirements.txt
```

The renderer scripts it calls into (`brand-kit/scripts/*.py`) self-install their own dependencies
(`python-docx`, `python-pptx`, `playwright` + a one-time Chromium download for PDF export) the
first time they run.

## Running it directly

```bash
python3 mcp-server/server.py
```

This starts a stdio MCP server — it's meant to be launched by an editor/client, not run
standalone in a terminal for interactive use (it just sits there waiting for MCP messages on
stdin/stdout, which is correct).

## Installing in each client

All of these register the same command:

```
command: python3   (or the full path to a 3.10+ interpreter)
args:    ["<absolute-path-to-this-repo>/mcp-server/server.py"]
```

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "poetics-brand": {
      "command": "python3",
      "args": ["/absolute/path/to/Poetics Skills/mcp-server/server.py"]
    }
  }
}
```

Restart Claude Desktop.

### Claude Code

From within this repo:

```bash
claude mcp add poetics-brand -- python3 "$(pwd)/mcp-server/server.py"
```

Or add a project-scoped `.mcp.json` at the repo root (see the example below) so it's shared with
anyone who clones the repo.

### VS Code (MCP support in Copilot Chat / Claude extensions)

Add to `.vscode/mcp.json` in this repo (or your user settings):

```json
{
  "servers": {
    "poetics-brand": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-server/server.py"]
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "poetics-brand": {
      "command": "python3",
      "args": ["/absolute/path/to/Poetics Skills/mcp-server/server.py"]
    }
  }
}
```

### Windsurf / JetBrains AI Assistant

Same shape as Cursor's config, in whichever file that client uses for MCP server definitions —
consult that tool's MCP docs; the `command`/`args` pair above is universal.

## Verifying it works

Once connected, ask the assistant in that editor something like *"what are Poetics's brand
colors?"* — it should read the `brand://spec` resource and answer from it, or *"generate a test
Poetics one-pager PDF"* — it should call `generate_branded_document`.
