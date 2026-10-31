# Brand plugin

Makes Poetics's brand accessible and enforceable across the team. Anyone can ask brand questions,
generate branded documents/decks/social assets, and get work reviewed against the brand, without
routing through a designer for every deliverable.

**Owner:** Thanos Dimitriou (dimitriouathanas@gmail.com)

The brand knowledge lives in `brand-kit/` inside this plugin, so an installed copy carries it.
The repo root's `brand-kit` is a symlink to it. See `brand-kit/brand.md` for the spec and
`brand-kit/guides/using-outside-claude-code.md` for using it without Claude Code.

## Skills

| Skill | What it does |
|---|---|
| brand-identity | Source of truth for visual identity: colors, typography, logo, spacing |
| brand-guidelines | Answers "can I do X?" questions, plus voice/tone guidance |
| brand-documents | Branded Word and PDF documents, rendered by bundled scripts |
| brand-proposals | Proposals, offers and quotes: practical A4 quote sheets (quote / offer / tiered / pitch) per `brand-kit/guides/proposal-playbook.md`, rendered by the deck renderer |
| brand-decks | Decks in the website's design system: standard, curation and proposal variants, as an HTML presenter with PDF/PPTX export |
| brand-templates | Social carousels and video thumbnails via self-contained HTML editors |
| brand-review | Reviews any asset against the brand, returns a structured compliance score |
| company | "What is Poetics" boilerplate for decks/docs/proposal intros |

Skill routing and output rules live in `GLOBAL_RULES.md`.

## Updating the brand

Edit `brand-kit/brand.md` directly and save. No build step, no sync, no approval workflow —
every skill reads the file fresh each time it runs.
