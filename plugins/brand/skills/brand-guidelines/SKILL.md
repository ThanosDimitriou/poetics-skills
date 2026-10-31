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

---

## Reference files

### Brand spec (always load)
```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"
```

### Voice/copy guide (load for writing or voice questions)
```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/writing-on-brand-copy.md"
```

---

## How to use this skill

Answer directly: yes/no first, then the rule, then the reason. Don't pad.

If the guideline doesn't cover the exact situation, say so and give the closest applicable rule.
Don't extrapolate a firm yes/no where `brand.md` is silent — flag the gap instead.

For voice/tone questions or requests to rewrite copy "on-brand," use
`writing-on-brand-copy.md`'s checklist and before/after examples as the working method: check for
hype words, invented facts, named films (hard rule — never), and correct register (narrator vs.
inner voice).

**Hard rule, always enforce:** never generate copy that names or visually identifies a specific
film. This applies regardless of what the user asks for — if a request would require naming a
film, say so and offer the theme-based alternative instead.
