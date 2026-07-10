# Installing the Poetics brand kit

One repo, three ways to use it. Pick the section for whichever tool you actually work in — you
don't need to do all three. If you're not sure, start with **Path A**; it's the fastest and
works everywhere.

---

## 0. Get the repo (needed for every path)

```bash
git clone https://github.com/ThanosDimitriou/poetics-skills.git
cd poetics-skills
```

You need **Python 3.10+** on your machine for Path C (MCP server); Paths A and B work with any
Python 3. Check your version:

```bash
python3 --version
```

If it's older than 3.10 and you want Path C, install a newer one (e.g. `brew install python@3.11`
on macOS) — you'll point the MCP config at that interpreter instead of the system default.

---

## Path A — No AI tool, or any AI tool that isn't Claude Code (ChatGPT, Gemini, etc.)

Nothing to install beyond the repo itself. Everything lives in `brand-kit/`.

**To generate a document or PDF by hand:**
1. Read `brand-kit/brand.md` (the brand rules) and `brand-kit/schemas/doc-content-schema.md` (the
   content format).
2. Write a `content.json` file matching that schema.
3. Run:
   ```bash
   python3 brand-kit/scripts/build-doc-pdf.py content.json output.pdf
   ```
   (First run installs its own dependencies automatically — `python-docx`/`playwright` etc. — this
   takes a minute the first time only.)

**To generate one with ChatGPT/Gemini instead of writing the JSON by hand:**
1. Paste `brand-kit/brand.md` into the tool's project instructions / custom instructions.
2. Ask it to draft content matching `brand-kit/schemas/doc-content-schema.md`.
3. Save its output as `content.json` and run the same command as above.

**For a social carousel or video thumbnail:** just open the file directly in a browser —
no server, no install:
```
brand-kit/templates/social-carousel/editor.html
brand-kit/templates/video-thumb/editor.html
```

Full details: [`brand-kit/guides/using-outside-claude-code.md`](brand-kit/guides/using-outside-claude-code.md).

---

## Path B — Claude Code

1. In Claude Code, from anywhere:
   ```
   /plugin marketplace add /path/to/poetics-skills
   ```
   (or use the repo URL if you cloned it — either a local path or the GitHub URL works)
2. Install the plugin when prompted, or run:
   ```
   /plugin install brand
   ```
3. Done. Just ask naturally — *"make a Poetics deck about X"*, *"write a branded one-pager"*,
   *"is this on-brand?"* — the right skill triggers automatically.

**Verify it worked:** ask *"what are Poetics's brand colors?"* — it should answer with real hex
values, not generic ones.

---

## Path C — VS Code, Cursor, Windsurf, JetBrains, or Claude Desktop (via MCP)

1. Install the MCP server's one dependency:
   ```bash
   python3 -m pip install -r mcp-server/requirements.txt
   ```
   (use your 3.10+ interpreter if your default `python3` is older — e.g.
   `python3.11 -m pip install -r mcp-server/requirements.txt`)

2. Add the server to your editor's MCP config. The shape is the same everywhere — only the file
   location differs:

   | Editor | Config file |
   |---|---|
   | Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) |
   | Claude Code | already auto-discovered via `.mcp.json` in this repo, or run `claude mcp add poetics-brand -- python3 "$(pwd)/mcp-server/server.py"` |
   | VS Code | `.vscode/mcp.json` |
   | Cursor | `.cursor/mcp.json` |
   | Windsurf / JetBrains | wherever that tool defines MCP servers — same `command`/`args` shape |

   Config content (adjust the path to where you cloned the repo):
   ```json
   {
     "mcpServers": {
       "poetics-brand": {
         "command": "python3",
         "args": ["/path/to/poetics-skills/mcp-server/server.py"]
       }
     }
   }
   ```
   (VS Code's `mcp.json` uses a top-level `"servers"` key instead of `"mcpServers"` — see
   [`mcp-server/README.md`](mcp-server/README.md) for the exact per-editor syntax.)

3. Restart the editor (or reload its MCP connections if it supports that without a restart).

**Verify it worked:** ask the assistant in that editor *"what are Poetics's brand colors?"* or
*"generate a test Poetics PDF"* — it should read the brand resource / call the generation tool.

Full details, including what each tool/resource/prompt does: [`mcp-server/README.md`](mcp-server/README.md).

---

## Lightweight fallback (no install, partial awareness)

Two files in this repo give Cursor and GitHub Copilot static awareness of the brand — no
tool-calling, just "read `brand.md` before answering branding questions." These work automatically
the moment you open the repo in either tool, no setup needed: `.cursorrules` and
`.github/copilot-instructions.md`. Use Path C instead if you want real tool-calling (actually
generating files, not just answering questions) in those editors.

---

## After installing: updating the brand

None of the paths above need to be reinstalled when the brand changes. Edit
[`brand-kit/brand.md`](brand-kit/brand.md) directly, commit, push — every path reads that file
fresh each time it runs.
