# Installing the Poetics brand kit

For anyone at Poetics who wants Claude (or another AI tool) to make on-brand decks, proposals,
documents and social assets. Pick the one path for the tool you work in.

| You work in | Path | Effort |
| --- | --- | --- |
| **Claude Code**: the `claude` terminal app, its IDE extensions, or the Code tab of the Claude desktop app | [A](#path-a--claude-code-recommended) | Two commands |
| VS Code or Cursor with another AI assistant | [B](#path-b--vs-code-or-cursor) | Clone and open |
| Claude Desktop chat (MCP) or Windsurf | [C](#path-c--claude-desktop-chat-mcp-or-windsurf) | One script |
| ChatGPT, Gemini, or no AI tool | [D](#path-d--chatgpt-gemini-or-by-hand) | Run the scripts yourself |
| **claude.ai** or the Claude Desktop chat window, using Skills | [E](#path-e--claudeai-chat-skills) | One upload |

**Claude Code and claude.ai chat are separate products.** Installing Path A does not make anything
appear in a claude.ai conversation, and Path E does nothing in Claude Code.

---

## What you can ask for

- **"Make a deck about…"**: a 16:9 deck in the website's design system. It asks a few questions
  first (what it's for, who will see it, which photos) and shows the page headings before
  building.
- **"Write a proposal / an offer / a quote for…"**: a practical A4 quote sheet (scope, capacity,
  price, date and scope disclaimer in the footer), in Greek or English. It asks for the price and
  never guesses one.
- **"Curated program for [venue]"**: a curation deck of the titles you choose, with facts and
  links checked against official sources.
- **"Write a one-pager / report / brief"**, **"social carousel"**, **"is this on-brand?"**,
  **"what are our colors?"**

You get an HTML file, a PDF, and an overview image of every page to review.

---

## Path A — Claude Code (recommended)

Works in the terminal, the IDE extensions and the Claude desktop app's Code tab: they share the
same plugins.

**1. Install the plugin** (once per computer):

```bash
claude plugin marketplace add ThanosDimitriou/poetics-skills
```

```bash
claude plugin install brand@poetics
```

Start a new Claude Code session and ask for a deck or a proposal. `claude plugin list` should show
`brand@poetics` as enabled.

**2. Install what PDFs need** (once per computer): Python 3, Google Chrome, and two Python
packages. The renderer uses your Chrome to make PDFs and page previews.

```bash
python3 -m pip install --user playwright pillow
```

**3. Optional: the photo library.** Decks can use Poetics' own photographs by name. They live in
the website project, not in this repo (it's public, and the photos show real people). If you have
a copy of the Poetics Website repo, point the kit at its image folder, for example:

```bash
echo 'export POETICS_PHOTO_ROOT="$HOME/Data/Projects/Poetics Website/src/assets/images"' >> ~/.zshrc
```

Without it, the skill simply asks you to send the photos you want.

### Getting updates

The installed plugin is a copy. When the kit changes, update it:

```bash
claude plugin marketplace update poetics
```

```bash
claude plugin install brand@poetics
```

(Or run `/plugin` inside Claude Code and update from there.) Then start a new session.

### "Unrecognized keys" or the plugin won't install

Your Claude Code is older than the plugin's manifest (the title "Brand kit - Poetics" and the icon
need a recent version). Update it, then install again:

```bash
claude update
```

### "command not found: claude"

Claude Code is installed, but your terminal doesn't know where. It usually lives in
`~/.local/bin`; add that folder to your PATH and open a new terminal tab:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

If that doesn't help, Claude Code isn't installed yet: see
[claude.com/claude-code](https://claude.com/claude-code).

### Working on the kit itself

Clone the repo and open it in Claude Code. The committed `.claude/settings.json` turns the plugin
on for that folder.

```bash
git clone https://github.com/ThanosDimitriou/poetics-skills.git
```

The real files live in `plugins/brand/brand-kit/`; `brand-kit/` at the repo root links to the same
folder.

---

## Path B — VS Code or Cursor

Clone the repo (above) and open the folder. The editor detects the bundled MCP server from
`.vscode/mcp.json` or `.cursor/mcp.json`; approve it when asked. Install its one dependency once:

```bash
python3 -m pip install -r mcp-server/requirements.txt
```

Needs Python 3.10+ (see [`mcp-server/README.md`](mcp-server/README.md) if yours is older). Check
it works by asking *"what are Poetics's brand colors?"*: the answer should include real hex values.

---

## Path C — Claude Desktop chat (MCP) or Windsurf

Clone the repo, then run the installer. It finds Python 3.10+, installs the dependency, and adds
the server to Claude Desktop or Windsurf without touching your other servers (it backs up your
config first, and is safe to re-run). Restart the app afterwards.

```bash
bash mcp-server/install.sh
```

Other MCP tools (JetBrains AI Assistant, etc.): see the manual config in
[`mcp-server/README.md`](mcp-server/README.md).

---

## Path D — ChatGPT, Gemini, or by hand

Clone the repo. Everything is in `brand-kit/`, and the scripts run from any terminal.

**Decks and proposals:** copy a starter from `brand-kit/templates/decks/` (`standard.json`,
`curation.json`, `quote.json`, `proposal.json`), edit it (every field is described at the top of
`brand-kit/scripts/build-deck.py`), then:

```bash
python3 brand-kit/scripts/build-deck.py my-deck.json my-deck.pdf
```

Add `--sheet` with an `.html` output to get a preview image of every page and a layout check.
Read `brand-kit/design-system.md` and `brand-kit/guides/deck-copy.md` for how decks look and
are written.

**Documents (one-pagers, reports):** write a `content.json` matching
`brand-kit/schemas/doc-content-schema.md`, then:

```bash
python3 brand-kit/scripts/build-doc-pdf.py content.json output.pdf
```

**With ChatGPT or Gemini:** paste `brand-kit/brand.md` and `brand-kit/guides/deck-copy.md` into
the tool's instructions, ask it to write the JSON, save it, and run the command yourself.

**Social carousel or video thumbnail:** open the editor in a browser, no install:
`brand-kit/templates/social-carousel/editor.html` or `brand-kit/templates/video-thumb/editor.html`.

More: [`brand-kit/guides/using-outside-claude-code.md`](brand-kit/guides/using-outside-claude-code.md).

---

## Path E — claude.ai chat (Skills)

claude.ai and the Claude Desktop chat window run Skills in a hosted sandbox with no access to your
files, so they use a self-contained bundle.

1. Download [`claude-skills/poetics-brand.zip`](claude-skills/poetics-brand.zip) from this repo.
2. In claude.ai or Claude Desktop: **Settings → Capabilities → Skills** → upload the zip.
3. Start a new conversation and ask *"make a Poetics deck about…"* or *"write a proposal for…"*.

Each person uploads it once. In chat, the photo library isn't available: attach the photos you
want to the conversation. When the kit changes, download the new zip and upload it again (it's a
snapshot, not a live link). How the bundle is rebuilt: [`claude-skills/README.md`](claude-skills/README.md).

---

## When the brand changes

| Path | What to do |
| --- | --- |
| A (Claude Code plugin) | Update the plugin (see "Getting updates") |
| B, C, D (cloned repo) | `git pull` in your copy of the repo |
| E (claude.ai) | Upload the new zip |

