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

---

## Reference file

The full visual identity spec: colors, typography, logo, spacing, voice/tone, company facts.

```bash
cat "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/brand.md"
```

---

## How to use this skill

Answer the question using only what's in `brand.md`. If a section hasn't been populated (see its
"Open questions" section), say so — do not invent values.

When sharing color values, include both hex and the usage note from the spec. When sharing type
specs, include family, weight, and role together — a partial answer causes more problems than it
solves.

If the question touches the accent color, mention the open discrepancy noted in `brand.md`
("Open questions for Thanos" #1) rather than stating `#0099FF` as unconditionally final.
