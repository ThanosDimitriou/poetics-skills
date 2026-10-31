# Using this brand kit outside Claude Code

Everything in `brand-kit/` is plain files — markdown, images, font files, and Python scripts.
None of it requires Claude or Claude Code. This guide covers using it with ChatGPT, Gemini, or by
hand.

## The short version

1. Give an AI tool `brand.md` as context (paste it, or upload it if the tool supports files).
2. Ask it to produce content — not a styled document, just structured content matching the
   relevant schema (`schemas/doc-content-schema.md` for docs/PDFs, or the `deck.json` /
   carousel-editor shape for decks/social).
3. Run the matching script yourself from a terminal. **The script applies the brand, not the
   AI.** This is the point of the split: no matter which assistant wrote the content, the output
   file is identically on-brand, because styling is mechanical, not AI-generated.

## ChatGPT (Projects / Custom GPT instructions)

1. Create a Project (or Custom GPT).
2. Paste the full contents of `brand.md` into the Project/GPT instructions, or upload it as a
   knowledge file if the plan supports file uploads.
3. Optionally upload the logo files from `assets/logos/` so ChatGPT can reference them when
   describing layout (it can't embed them into a script's output directly, but it can reason
   about placement).
4. When asking for a document: "Write the content for a one-pager about X. Structure it to match
   this schema exactly: [paste `schemas/doc-content-schema.md`]." Save what it gives you as
   `content.json`.
5. Run: `python3 scripts/build-doc-pdf.py content.json output.pdf`

## Gemini (Gems)

Same pattern: put `brand.md` in the Gem's instructions, ask for schema-matching JSON output, run
the renderer script yourself.

## No AI at all

Everything here works by hand too:

- Read `brand.md` for the colors/fonts/voice rules directly.
- Write a `content.json` file yourself following `schemas/doc-content-schema.md`.
- Run the script from a terminal: `python3 scripts/build-doc.py content.json output.docx`.
- For social assets, open `templates/social-carousel/editor.html` or
  `templates/video-thumb/editor.html` directly in a browser (double-click the file) — no server,
  no upload, just fill in the form and click export.

## What you lose without Claude Code

Only convenience: automatic skill-triggering ("make a Poetics deck" firing the right tool),
routing over the plugin's generic pptx/docx/pdf handling, and the content-extraction step that
reads a source document/URL for you. The actual brand fidelity — colors, fonts, logo, layout — is
identical either way, because it's enforced by the scripts, not by whichever AI wrote the content.

## Requirements

- Python 3 with `pip` access (scripts self-install their dependencies on first run:
  `python-docx`, `python-pptx`, `playwright` + a one-time ~110MB Chromium download for PDF
  export).
- A modern browser for the HTML templates (any current Chrome, Safari, Firefox, Edge).
