# Brand plugin

Makes Poetics's brand accessible and enforceable across the team. Anyone can ask brand questions,
generate branded documents/decks/social assets, and get work reviewed against the brand, without
routing through a designer for every deliverable.

**Owner:** Thanos Dimitriou (dimitriouathanas@gmail.com)

This plugin is a thin Claude Code wrapper — the actual brand knowledge lives in `brand-kit/` at
the repo root, not inside this plugin. See `../../brand-kit/brand.md` for the spec itself and
`../../brand-kit/guides/using-outside-claude-code.md` for using it without Claude Code.

## Skills

| Skill | What it does |
|---|---|
| brand-identity | Source of truth for visual identity: colors, typography, logo, spacing |
| brand-guidelines | Answers "can I do X?" questions, plus voice/tone guidance |
| brand-documents | Branded Word and PDF documents, rendered by bundled scripts |
| brand-decks | Branded presentations as self-contained HTML with PDF/PPTX export |
| brand-templates | Social carousels and video thumbnails via self-contained HTML editors |
| brand-review | Reviews any asset against the brand, returns a structured compliance score |
| company | "What is Poetics" boilerplate for decks/docs/proposal intros |

Skill routing and output rules live in `GLOBAL_RULES.md`.

## Updating the brand

Edit `../../brand-kit/brand.md` directly and save. No build step, no sync, no approval workflow —
every skill reads the file fresh each time it runs.
