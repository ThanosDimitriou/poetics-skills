---
name: brand-identity
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for any question about Poetics's visual identity specs. Trigger on: "brand
  colors", "Poetics colors", "what font does Poetics use", "Poetics typography", "logo rules",
  "logo variants", "brand specs", "design tokens", "visual identity", "spacing scale",
  "brand identity", or any request for raw brand specification data.

---

# Brand identity

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"   # how everything looks
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"           # logo rules, company, social canvas specs
```

## How to answer

**One system for everything:** decks, proposals, documents and social assets all follow
`design-system.md` (the website's system). Logo files and social sizes are in `brand.md`.

The current system in one breath: seven colour roles in light and dark (paper `#EFF0EC`, ink
`#121614`, ink-soft `#5B625C`, lens `#16249C` only on what can be pressed; dark theme values in
the file), Instrument Serif 400 for display and Inter Tight 400/500 for text, three radii (pill,
lens, small), one spacing scale, the single-colour wordmark. Read the file for anything more
precise than that.

- **Colours:** give the hex and the role ("lens `#16249C`: links, buttons and the one action;
  never decoration"). Mention the dark-theme value when it matters.
- **Type:** family, weight, size token and role together. A partial answer causes more problems
  than it solves.
- **Logo:** the rules in `brand.md` apply to everything; decks and documents use
  `assets/logos/wordmark-mono.svg` painted in ink.
- If something isn't specified, say so. Never invent a value.
