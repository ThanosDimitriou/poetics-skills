# Installing the Poetics brand kit

One repo, five ways to use it. Pick the section for whichever tool you actually work in — you
don't need to do all five.

**Important distinction if you use Claude:** "Claude Code" (Path A, the CLI/IDE tool) and
"claude.ai / Claude Desktop chat" (Path E) are two separate products with two separate skill
mechanisms. Installing Path A does **not** make anything show up in a claude.ai or Claude Desktop
chat conversation — that needs Path E specifically. This trips people up, so it's called out here
twice.

---

## 0. Get the repo (needed for every path)

```bash
git clone https://github.com/ThanosDimitriou/poetics-skills.git
cd poetics-skills
```

Or, one line that also runs the Claude Desktop/Windsurf installer in the same breath:

```bash
npx degit ThanosDimitriou/poetics-skills poetics-skills && cd poetics-skills && bash mcp-server/install.sh
```

(`degit` is a standard public npm tool for pulling a repo without its git history — not something
we publish or maintain. Since it drops the `.git` folder, you won't be able to `git pull` later to
get brand updates; use the plain `git clone` above if you'll want to update in place.)

**For Claude Code, VS Code, or Cursor: that's it — skip straight to verifying below.** This repo
ships committed config (`.claude/settings.json`, `.mcp.json`, `.vscode/mcp.json`,
`.cursor/mcp.json`) that those tools auto-discover the moment you open the folder. No install
command to run, nothing to paste into a settings file.

---

## Path A — Claude Code (zero commands)

**This is the `claude` CLI / IDE integration — not claude.ai or the Claude Desktop chat window.**
If you want it in a regular chat conversation instead, skip to Path E.

Open this repo in Claude Code. The `brand` plugin is already registered and enabled via the
committed `.claude/settings.json` — confirm with:

```bash
claude plugin list
```

You should see `brand@poetics` listed as enabled. Then just ask naturally — *"make a Poetics deck
about X"*, *"write a branded one-pager"*, *"is this on-brand?"*

*(If you're adding this repo to Claude Code from somewhere other than a local clone — e.g. as a
marketplace source for a different project — the manual equivalent is:*
`claude plugin marketplace add ThanosDimitriou/poetics-skills && claude plugin install brand@poetics`*.)*

---

## Path B — VS Code or Cursor (zero commands)

Open this repo's folder in the editor. It auto-detects the MCP server from the committed
`.vscode/mcp.json` / `.cursor/mcp.json`. You may see a one-time prompt asking to trust/allow the
workspace's MCP server — approve it.

One dependency needs installing once per machine:
```bash
python3 -m pip install -r mcp-server/requirements.txt
```
(needs Python 3.10+; see [`mcp-server/README.md`](mcp-server/README.md) if your default `python3`
is older)

**Verify:** ask *"what are Poetics's brand colors?"* — it should answer with real hex values via
the MCP server, not generic ones.

---

## Path C — Claude Desktop or Windsurf (one command)

These don't have a "project folder" concept to auto-discover config from, so they need:

```bash
bash mcp-server/install.sh
```

This finds a Python 3.10+ interpreter, installs the one dependency, and safely registers the
server in whichever of the two it finds on your machine (backs up existing config first, never
touches other MCP servers you have configured, safe to re-run). Restart the editor afterward.

For any other MCP-compatible tool (JetBrains AI Assistant, etc.), see the manual config shape in
[`mcp-server/README.md`](mcp-server/README.md).

---

## Path D — ChatGPT, Gemini, or no AI tool at all

Nothing to install beyond the repo itself. Everything lives in `brand-kit/`.

**To generate a document or PDF by hand:**
1. Read `brand-kit/brand.md` (the brand rules) and `brand-kit/schemas/doc-content-schema.md` (the
   content format).
2. Write a `content.json` file matching that schema.
3. Run:
   ```bash
   python3 brand-kit/scripts/build-doc-pdf.py content.json output.pdf
   ```
   (First run installs its own dependencies automatically — takes a minute, once only.)

**With ChatGPT/Gemini instead of writing the JSON by hand:**
1. Paste `brand-kit/brand.md` into the tool's project/custom instructions.
2. Ask it to draft content matching `brand-kit/schemas/doc-content-schema.md`.
3. Save its output as `content.json` and run the same command as above.

**For a social carousel or video thumbnail:** open the file directly in a browser — no server,
no install:
```
brand-kit/templates/social-carousel/editor.html
brand-kit/templates/video-thumb/editor.html
```

Full details: [`brand-kit/guides/using-outside-claude-code.md`](brand-kit/guides/using-outside-claude-code.md).

---

## Path E — claude.ai or Claude Desktop **chat** (one upload)

Separate from Path A. Claude Code plugin skills assume a local git clone; claude.ai/Claude
Desktop's chat **Skills** feature (Settings → Capabilities → Skills) runs in a hosted sandbox with
no access to your files, so it needs a self-contained bundle instead.

1. Download [`claude-skills/poetics-brand.zip`](claude-skills/poetics-brand.zip) from this repo
   (either clone the repo and grab the file, or download it directly from GitHub).
2. In claude.ai or Claude Desktop: **Settings → Capabilities → Skills** → upload the zip.
3. Start a new conversation and ask *"what are Poetics's brand colors?"* — it should trigger.

Details, and how to re-sync the bundle after editing `brand-kit/`:
[`claude-skills/README.md`](claude-skills/README.md).

**Not covered:** ChatGPT and Gemini don't have an equivalent private-skill-upload mechanism —
real tool-calling there would require hosting the renderer scripts as a public web API plus a
Custom GPT Action / Gemini Extension, a bigger and different project than packaging a skill. Path
D (pasting `brand.md` into custom instructions) is the practical option for those tools today.

---

## After installing: updating the brand

Paths A–D need no reinstalling when the brand changes — edit
[`brand-kit/brand.md`](brand-kit/brand.md) directly, commit, push, and every one of them reads the
file fresh each time it runs.

**Path E is the one exception.** The chat Skill bundle is a snapshot, not a live link to
`brand-kit/` — re-sync and re-upload it after brand changes (steps in
[`claude-skills/README.md`](claude-skills/README.md)).
