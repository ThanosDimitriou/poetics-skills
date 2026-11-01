---
name: brand-guidelines
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for "can I do X?" brand questions, rules and do's/don'ts, and guidance on
  applying the Poetics brand correctly — including voice and tone. Trigger on: "is this
  on-brand", "can I use this color for", "what font should I use for", "brand guidelines",
  "brand rules", "how should I style", "does Poetics sound like this", "write this on-brand",
  "make this sound like Poetics".

---

# Brand guidelines

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"   # the voice, for everything
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/anti-slop.md"               # what never to do
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"                  # visual rules (decks, documents)
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"                          # company, logo, legacy social spec
```

## How to answer

Yes or no first, then the rule, then the reason. Don't pad. If the guidelines don't cover the
exact situation, say so and give the closest rule; don't invent a firm answer.

**Visual questions:** decks, proposals and documents follow `design-system.md` (one accent, the
lens blue, only on what can be pressed; space and hairlines, never boxes or shadows; no gradients;
the spacing guardrail). The social templates still use `brand.md`'s legacy spec.

**Copy and "make this sound like Poetics":** rewrite in the website's voice using
`writing-on-brand-copy.md`: plain, concrete, "we" and "you", short sentences, what happens
rather than how it feels, no em dashes, no hype, sentence case. Check the rewrite against
`anti-slop.md` before giving it back. Reuse the website's approved lines where they fit.

## Hard rules, always

- Never name or visually identify a specific film, except in a curation deck made for one venue.
  If a request needs a film named anywhere else, say so and offer the theme-based version.
- Never invent a figure, date, quote, name or price. Mark unknowns as `[PLACEHOLDER]`.
- The only email is hello@poeticsvr.com; don't name the people who made the material unless asked.
- Confidential items (pricing amounts, franchise model, roadmap dates, streaming platform status,
  internal tooling, survey methodology) stay out unless the user includes them.
