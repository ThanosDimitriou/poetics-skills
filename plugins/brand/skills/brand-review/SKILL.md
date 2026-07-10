---
name: brand-review
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill to review any asset against Poetics brand guidelines and get structured feedback
  with a compliance score. Trigger on: "review this", "check this against brand", "is this
  on-brand", "brand review", "brand check", "brand audit", "review my deck", "review this
  document", "review this social post". Accepts: screenshots, images, PPTX/DOCX/PDF files, URLs.

---

# Brand review

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

---

## Reference file

```bash
cat "${CLAUDE_PLUGIN_ROOT}/../../brand-kit/brand.md"
```

---

## Review format

**Brand compliance score: X/10**

**What's on-brand**
List what's correct. Be specific — name the element and why it passes.

**What needs fixing**
For each issue:
- Element: what it is
- Problem: what's wrong and what value was used
- Fix: exactly what it should be, citing the token/rule from `brand.md`
- Severity: Critical (breaks brand) or Minor (inconsistency)

**Summary**
One or two sentences: overall state, and the single most important fix.

---

## Scoring rules

- Start at 10. Deduct for each issue based on severity.
- Critical issues: -1.5 to -2 points each (wrong canvas/text colors, wrong fonts, logo misuse,
  a named film appearing anywhere, second accent color introduced).
- Minor issues: -0.5 to -1 point each (wrong font weight, spacing off, restraint violated —
  e.g. multiple mono annotations on one page).
- Never give a score without listing the issues that drove it.
- A score of 8+ means ship-ready with minor cleanup. Below 6 means needs rework.

**Always check for the hard rules first**, regardless of visual polish: no named/identifiable
films, one accent color only, voice register matches content type (narrator vs. inner voice).
