# Anti-slop: what makes a deck read as AI-made, and what we do instead

Researched 2026-10-31 from the catalogs listed at the end. "Slop" is what you get when a model
fills in taste decisions nobody made. No single pattern proves anything; a cluster of them is what
an audience notices, and once noticed, it reads as "nobody spent time on this."

The cure is the same everywhere: make the decisions in advance (design-system.md does) and say the
specific thing. `build-deck.py` warns on the copy patterns marked ⚑.

---

## Poetics deck rules

These apply to every deck, whatever the variant. They come first; the catalogs below explain why.

1. **Say less.** Simple, direct wording. A heading is one short claim (12 words at most), a lead is
   one sentence, a row is one line. Cut every word that doesn't change the meaning. ⚑ (word limits
   per field)
2. **Give the eye room.** White space is the layout, not leftover space. A slide with less on it is
   better than a full one. When in doubt, split the slide or move detail to the speaker notes.
3. **No cheesy taglines.** No "where art meets technology", "step into", "like never before",
   "redefining", "the future of", "magical", "unforgettable", "a journey". Say the plain fact:
   "Pop-up VR cinemas for festivals, museums and brands." ⚑
4. **Few overlines.** The small line above a heading appears on a quarter of the slides at most,
   and only when it adds a fact: a date, an "as of", a document type. Never as decoration,
   never to repeat the heading. ⚑
5. **Not everything comes in threes.** Use the true count: two figures, four services, five
   steps. Three only when there are three. ⚑ (when most lists in a deck have exactly three)
6. **Leave the makers out.** Don't name whoever made the deck (founders, team members, "with love
   from"), unless the user asks. The company is Poetics. ⚑ (set `"allow_team_names": true` when asked)
7. **One email: hello@poeticsvr.com.** Never a personal address. The closing page offers that
   email and nothing else: one clear path. ⚑
8. **Every footer says "poeticsvr.com · Confidential".** That's the default; the renderer adds it.
   Turn it off only when asked (`"confidential": false`).
9. **Write like the website, not like a chatbot.** No "ready when you are", "as we understood it",
   "at a glance", "let's", "shall we", rhetorical questions as headings. Headings are short plain
   sentences with a full stop. See `deck-copy.md` for the voice and before/after examples. ⚑
10. **Ask before keeping filler.** Statement, section divider, agenda, full photo and gallery pages
   carry no information of their own; the user decides whether they stay.
11. **Room around everything.** 72px clear below the wordmark, nothing overlapping, nothing
   crowding the footer. Cramped chrome is the fastest way to look unfinished. ⚑ (`--check`)

---

## Visual patterns

| Pattern | Why it reads as slop | Poetics instead |
| --- | --- | --- |
| Dark canvas with glowing accents, radial halos, soft spotlights | The default "premium tech" look | Paper and ink, light by default. No glows, no gradients |
| Purple-to-blue or cyan-on-dark palettes, gradient text | The AI palette | Seven fixed roles. Blue only on things you can press |
| Cards around everything ("cardocalypse"), nested cards, shadows on cards | Container instead of content | Space and 1px hairlines. No boxes, no card shadows |
| Identical icon + heading + text card grids | Every point gets equal weight, nothing leads | Ruled rows or columns on hairlines, under a heading that makes the claim |
| Icon tile above every heading, decorative icons | Ornament standing in for an idea | No decorative icons. A photograph, or nothing |
| Thick accent bar on one side of a block; colour bars under titles | Lazy emphasis, multiplies colours | Never. Hairlines structure, they don't decorate |
| Small all-caps letterspaced label above every heading | The most common AI eyebrow | An overline only when it adds a fact (a date, who it's for). Sentence case, no tracking |
| Italic serif flourish tacked onto a sans headline | The AI "editorial" shortcut | One display face, upright. No italic emphasis voice |
| Dashboard row of hero metrics, all equal weight | Invites invented round numbers; no claim | A heading that states the claim, then up to three real figures that prove it |
| Tiny numbered labels with no real sequence | Fake structure | Numerals only for a real order (agenda, timeline steps) |
| Everything centred | No reading line | Left-aligned. Nothing centred |
| Same spacing everywhere | Nothing groups | One scale, and the same relationship always gets the same gap |
| Oversized radii on everything | Generic softness | Three radii: pill, lens 48px, small 18px, each with a job |
| Cream or beige "warm" default background | The default warm palette | `paper` #F4F5F3, a cool tinted neutral |
| Pure #000 / #FFF | No designed palette | Tinted ink and paper |
| Glassmorphism, frosted panels | Decoration | None |
| Default fonts (Inter, Roboto, Arial) | Every product looks alike | Instrument Serif for display. (Inter Tight is the website's text face: kept, but always under a serif display) |
| Repeated identical slide layouts | Copy-paste rhythm | Never three of the same layout in a row (the renderer warns) |
| Bouncy or elastic motion, builds and reveals | Fussy | Nothing moves. Slides change at once |
| Placeholder art: blobs, circles, empty icon squares | Looks unfinished | An empty frame renders only in drafts, and the renderer warns |

## Copy patterns

| Pattern | Example | Poetics instead |
| --- | --- | --- |
| ⚑ Em dashes everywhere | "Immersive — and unforgettable" | A colon, comma, full stop or parentheses |
| ⚑ Stock vocabulary | delve, seamless, elevate, unlock, leverage, empower, pivotal, vibrant, tapestry, testament, cutting-edge, world-class, game-changing, robust, harness | The concrete thing: what the visitor sees, what the venue doesn't have to do |
| ⚑ "Not X, but Y" / "not just X, it's Y" / "more than just" | "It's not just VR, it's a journey" | Say Y. Use the contrast only when X was a real belief someone holds |
| ⚑ Copula avoidance | "serves as", "stands as", "boasts" | is, has |
| Rule of three, everywhere | "immersive, intuitive and impactful" | Two or four when that's the true count. Three only when there are three |
| ⚑ Exclamation marks, emoji | "Book now! 🚀" | Neither |
| ⚑ Title Case Headings | "Why Venues Choose Us" | Sentence case |
| Topic headings | "Pricing" | A claim: "One figure covers everything" (the titles test, below) |
| Heading and subheading that repeat each other | "Our team / The people behind Poetics" | Cut one, or make the second add a fact |
| Restating summaries | "In summary...", a recap slide of the last three slides | End on the ask, not a recap |
| Generic CTAs | "Learn more" | "Get in touch", "Book a call": what actually happens |
| Inflated significance | "a testament to", "a pivotal moment" | The fact, with its number and date |
| Vague attribution | "experts agree", "studies show" | Name the source or drop the claim |
| Invented numbers, quotes, names | "Trusted by 100+ venues" | Never invent. Unknowns are written as `[PLACEHOLDER]` and stay out of the deck until confirmed |
| Hedges and chat residue | "it's important to note", "here's an overview" | Delete |

## The process causes, and the fixes

1. **No point of view per slide.** Write the one sentence the audience should remember before
   picking a layout. That sentence is the heading.
2. **Vague style instructions** ("modern and clean"). Use the tokens and slide types, not adjectives.
3. **Filling space.** A slide with less on it is fine. Split instead of shrinking type.
4. **Accepting the first default.** Each fix only moves a model to its next default, so the rules
   live in the renderer and the design system, not in a prompt.

---

## What to remove from the current Figma deck

From "Poetics - Proposal template" (Figma, reviewed 2026-10-31):

- Glow and blur atmospheric backgrounds on the cover and content slides.
- Bordered, translucent cards on "What we offer", "A new landscape" and "Unique because"
  (cards around everything, identical grids).
- Letterspaced capital eyebrows: "POETICS IS ON A MISSION TO", "INTRODUCING".
- Empty or icon tiles above "Arts / Education / Entertainment" and the pricing models.
- Side accent bars beside each figure on "Poetics in numbers", and six equal-weight metrics with no
  claim in the heading.
- Centred statement and product-intro slides.
- Topic headings ("What we offer", "Curation", "Pricing models") where a claim would carry the slide.
- Title-case labels ("Flat-Fee") and a heart symbol in the credit line.
- A "We are here" chip on the timeline: kept as an idea (it's information), drawn as an ink rule on
  the current step instead of a badge.

`templates/decks/standard.json` is that deck rebuilt without them.

---

## Sources

- Penn State, Michael Alley, assertion-evidence research: writing.engr.psu.edu/research.html
- Plus AI, "How to make AI-generated slides that don't look like AI slop": plusai.com/blog/how-to-make-ai-slides-that-dont-look-like-ai-slop
- Impeccable, slop catalog: impeccable.style/slop
- pixelslop, AI slop pattern catalog: cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md
- 925 Studios, "AI slop fonts and gradients": 925studios.co/blog/ai-slop-design-tells
- Adrian Krebs, "Scoring 500 Show HN pages for AI design patterns": adriankrebs.ch/blog/design-slop/
- Wikipedia, "Signs of AI writing": en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Anthropic, pptx skill (design anti-patterns, QA loop): github.com/anthropics/skills/tree/main/skills/pptx
- zarazhangrui/frontend-slides (anti-slop, density modes, fixed stage): github.com/zarazhangrui/frontend-slides
