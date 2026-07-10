---
name: company
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for general questions about Poetics as a company — what we do, who we serve,
  business model, or an "about us" blurb for a document/deck/proposal intro. Trigger on: "what is
  Poetics", "what does Poetics do", "about Poetics", "company overview", "elevator pitch", "who
  are Poetics's customers", or any context where "tell me about Poetics" is implied. Do NOT
  trigger for visual identity questions (use brand-identity) or voice/tone questions (use
  brand-guidelines).
---

# Company

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

---

## Reference file

The "Company" section of the brand spec has the factual boilerplate:

```bash
cat "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/brand.md"
```

---

## How to use this skill

Lead with the three-verb pitch (Curate → Install → Operate) and adapt length/register to the
audience — a Slack reply needs one sentence, a proposal intro needs a paragraph.

**What's covered:** what Poetics does, the three-verb pitch, where they're based, who they serve
(B2B: museums, galleries, festivals, schools, event spaces), and social/site links.

**What's not covered yet** (flagged in `brand.md`'s "Open questions" section): a fuller
"about us"/company story and team bios. If asked for these, say the source content doesn't exist
yet rather than inventing a narrative — this is explicitly called out as an open item for Thanos
to supply.

**Never invent facts** — stats, dates, team bios, or customer names beyond what's in `brand.md`.
