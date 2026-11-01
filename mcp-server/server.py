#!/usr/bin/env python3
"""Poetics brand MCP server.

Exposes the brand-kit/ portable core (brand.md, renderer scripts, schemas,
guides) as MCP resources, tools, and prompts, so any MCP-compatible client —
VS Code, Cursor, Windsurf, Claude Desktop, JetBrains, Claude Code — gets the
same auto-triggering/tool-calling behavior the Claude Code plugin has,
without being locked to Claude Code specifically.

This is a thin wrapper, same philosophy as plugins/brand: no brand knowledge
lives here. Every resource/tool reads or calls straight through to brand-kit/.

Run directly (stdio transport):
    python3 server.py

Requires: pip install "mcp[cli]"
"""

import json
import pathlib
import subprocess
import sys
import tempfile

from mcp.server.fastmcp import FastMCP

KIT = pathlib.Path(__file__).resolve().parent.parent / "brand-kit"
SCRIPTS = KIT / "scripts"

mcp = FastMCP("poetics-brand")


# -- Resources (read-only brand knowledge) -------------------------------------

@mcp.resource("brand://spec")
def brand_spec() -> str:
    """The Poetics brand spec: company facts, logo rules, voice summary, and the
    legacy visual spec the social templates still use. Decks, proposals and
    documents look the way brand://design-system says."""
    return (KIT / "brand.md").read_text()


@mcp.resource("brand://design-system")
def design_system() -> str:
    """How decks, proposals and documents look: the Poetics Website's design
    system (colour roles, type, spacing, shapes, the spacing guardrail)."""
    return (KIT / "design-system.md").read_text()


@mcp.resource("brand://guide/anti-slop")
def anti_slop_guide() -> str:
    """The deck rules and the patterns that make material read as machine-made."""
    return (KIT / "guides/anti-slop.md").read_text()


@mcp.resource("brand://schema/document")
def document_schema() -> str:
    """JSON content schema consumed by generate_branded_document."""
    return (KIT / "schemas/doc-content-schema.md").read_text()


@mcp.resource("brand://guide/voice")
def voice_guide() -> str:
    """The one voice guide (the website's voice), with reusable lines and before/after examples."""
    return (KIT / "guides/writing-on-brand-copy.md").read_text()


@mcp.resource("brand://guide/portability")
def portability_guide() -> str:
    """How to use brand-kit/ from tools other than an MCP-aware editor."""
    return (KIT / "guides/using-outside-claude-code.md").read_text()


# -- Tools (actions with side effects: they write files) -----------------------

def _run(script: str, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"{script} failed (exit {result.returncode}):\n{result.stdout}\n{result.stderr}"
        )
    return result.stdout.strip()


@mcp.tool()
def generate_branded_document(content: dict, output_path: str, format: str = "pdf") -> str:
    """Render a branded Poetics document. `content` must match the schema at
    brand://schema/document (title, subtitle, date, sections[], separator_title).

    Optional: theme ("light" default, "dark"), lang ("en" | "el"), cover_image
    (a local path or "photo:<id>"), confidential (default true). Documents
    follow brand://design-system: A4, off-white paper, Instrument Serif and Inter
    Tight, hairlines, "poeticsvr.com · Confidential" footers.

    format: "pdf" (the version to send, fonts embedded) or "docx" (editable in
    Word; needs Instrument Serif and Inter Tight installed). Proposals, offers
    and quotes are not documents: use generate_branded_deck with kind "proposal".

    Returns the absolute path to the generated file. Never invent content
    values not present in brand://spec (colors, logo, voice) — the renderer
    applies those automatically; you only supply the text content.
    """
    if format not in ("pdf", "docx"):
        raise ValueError('format must be "pdf" or "docx"')
    script = "build-doc-pdf.py" if format == "pdf" else "build-doc.py"

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(content, f)
        tmp_path = f.name
    try:
        _run(script, tmp_path, output_path)
    finally:
        pathlib.Path(tmp_path).unlink(missing_ok=True)
    return str(pathlib.Path(output_path).resolve())


@mcp.tool()
def generate_branded_deck(deck: dict, output_path: str) -> str:
    """Render a Poetics slide deck in the website's design system
    (brand-kit/design-system.md). `deck` is {kind, format?, theme?, density?,
    title, footer?, confidential?, number?, date?, disclaimer?, slides[]}.
    Proposals default to A4 portrait (.html/.pdf only), with the creation date
    and a scope disclaimer in every footer. kind is "standard",
    "curation" (the only kind that may name films, via "work" slides) or
    "proposal" (with "mode": pitch | offer | tiered | quote). Slide types:
    cover, statement, section, agenda, content, terms, columns, stats, split,
    timeline, quote, people, gallery, media, table, price, work, acceptance,
    closing. A slide may name a page template instead: {"template": "E3"}
    (O1-O3 open, N1-N2 navigate, E1-E4 explain, P1-P2 prove, S1-S4 show,
    V1-V2 voices, T1 steps, C1 closing (email only), D1-D2 deal, W1 title
    card, E5 text, A1 stacked A4 page with "sections").
    See build-deck.py's docstring for every field, and
    brand-kit/templates/decks/ for a starter of each kind.

    Output format is chosen by output_path's extension: .html (a presenter
    that scales to any screen; arrow keys, F, N for notes, T for theme), .pdf
    (rendered from the same HTML via headless Chromium), or .pptx (editable
    approximation with speaker notes).

    Write in the website's voice (brand-kit/guides/deck-copy.md): short plain
    headings with a full stop, no em dashes. Items holding a [PLACEHOLDER]
    are dropped unless "draft": true.

    Returns the absolute path to the generated file.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(deck, f)
        tmp_path = f.name
    try:
        _run("build-deck.py", tmp_path, output_path)
    finally:
        pathlib.Path(tmp_path).unlink(missing_ok=True)
    return str(pathlib.Path(output_path).resolve())


@mcp.tool()
def get_logo_path(variant: str = "wordmark", background: str = "dark") -> str:
    """Return the absolute path to the correct Poetics logo file for a given
    background. variant: "wordmark" (horizontal lockup) or "mark" (standalone
    square pill). background: the color of the surface the logo will sit ON
    ("dark" or "light") — the tool picks the correctly-contrasting logo color
    automatically (light logo on dark backgrounds, dark logo on light ones),
    so you never have to reason about the light/dark naming convention
    yourself.
    """
    if variant not in ("wordmark", "mark"):
        raise ValueError('variant must be "wordmark" or "mark"')
    if background not in ("dark", "light"):
        raise ValueError('background must be "dark" or "light"')
    logo_color = "light" if background == "dark" else "dark"
    path = KIT / "assets/logos" / f"{variant}-{logo_color}.svg"
    if not path.exists():
        path = path.with_suffix(".png")
    if not path.exists():
        raise FileNotFoundError(f"No logo asset found for {variant}/{background}")
    return str(path.resolve())


@mcp.tool()
def get_social_template_path(template: str) -> str:
    """Return the absolute path to a self-contained HTML social asset editor.
    template: "social-carousel" (1080x1350 carousel slides) or "video-thumb"
    (1920x1080 video thumbnails). Open the returned path in a browser — it's
    a local file, no server needed. The user fills the form and exports a PNG
    themselves; this tool cannot complete that interactive step for them.
    """
    if template not in ("social-carousel", "video-thumb"):
        raise ValueError('template must be "social-carousel" or "video-thumb"')
    path = KIT / "templates" / template / "editor.html"
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return str(path.resolve())


# -- Prompts (reusable prompt templates) ----------------------------------------

@mcp.prompt()
def review_against_brand(asset_description: str) -> str:
    """Build a brand-compliance review prompt for a described asset, using the
    same rubric as the Claude Code brand-review skill: score from 10, deduct
    for critical (-1.5 to -2) vs minor (-0.5 to -1) issues, cite specific
    values from brand.md for every deduction."""
    spec = (KIT / "brand.md").read_text()
    system = (KIT / "design-system.md").read_text()
    slop = (KIT / "guides/anti-slop.md").read_text()
    return f"""Read the Poetics brand spec, the design system (decks, proposals and
documents look like this; social templates still use brand.md's legacy spec), and
the deck rules:

{spec}

---

{system}

---

{slop}

---

Review the following asset against them. Produce:

**Brand compliance score: X/10**

**What's on-brand** — list what's correct, name the element and why it passes.

**What needs fixing** — for each issue: Element / Problem (what's wrong and what
value was used) / Fix (exactly what it should be, citing the token or rule) /
Severity (Critical: -1.5 to -2pts, e.g. the old dark look on a deck or document,
wrong fonts, a second accent colour, logo misuse, a named film outside a curation
deck, an invented figure; Minor: -0.5 to -1pt, e.g. a deck-rule break, spacing,
a voice slip).

**Summary** — one or two sentences: overall state, single most important fix.

Always check the hard rules first regardless of visual polish: no named or
visually identifiable films (except a curation deck), nothing invented, one
accent colour only on what can be pressed, the website's voice (plain, no em
dashes, no stock phrases).

Asset to review:
{asset_description}"""


@mcp.prompt()
def write_on_brand_copy(topic: str) -> str:
    """Build a prompt for drafting on-brand Poetics copy about a given topic,
    grounded in brand.md's voice/tone rules and the writing guide's
    before/after examples."""
    spec = (KIT / "brand.md").read_text()
    guide = (KIT / "guides/writing-on-brand-copy.md").read_text()
    return f"""Read this Poetics brand spec:

{spec}

---

And this voice/copy guide:

{guide}

---

Write copy about: {topic}

Write in the website's voice exactly as the guide describes: plain, concrete,
"we" and "you", short sentences, what happens rather than how it feels, no em
dashes, no hype. Keep the hard rules: no invented facts, no named films."""


if __name__ == "__main__":
    mcp.run()
