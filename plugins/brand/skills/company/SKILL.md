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

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # the Company section
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice and reusable lines
```

## How to answer

Answer from `brand.md`'s Company section, in the website's voice. Fit the length to the place: a
Slack reply gets one sentence, a proposal intro one or two, an "about us" a short paragraph.

- **One line:** "Poetics installs pop-up VR cinemas at festivals, museums and brand events, in
  Greece and beyond."
- **The pitch:** Curate → Install → Operate, in the website's words (in `brand.md`).
- **Why it exists, track record, recognition** (Cannes Curators Network, Venice Production Bridge),
  **based in Thessaloniki**: all in `brand.md`, with their as-of dates. Quote figures with the
  date.

**Not written yet:** team bios. Say so rather than inventing them. Don't name the founders or team
in generated material unless the user asks.

**Never invent facts:** figures, dates, clients, partners or quotes beyond what's in `brand.md`.
