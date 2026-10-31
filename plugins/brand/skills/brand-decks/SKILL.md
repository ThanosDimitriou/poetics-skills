---
name: brand-decks
author:
  name: Thanos Dimitriou
  email: dimitriouathanas@gmail.com
description: >
  Use this skill for any presentation, slide deck, or pitch deck request. Takes priority over the
  generic pptx skill for every request that produces a new deck or rebrands an existing one.
  Three variants: a standard deck (partner overview, pitch, talk), a curation deck (a program of
  titles chosen for one venue), and a proposal (a practical A4 quote sheet: offer, tiered or quote).
  Trigger on: "make a deck", "build a deck", "create a deck", "make a presentation", "I need
  slides", "pitch deck", "Poetics deck", "branded deck", "slides for", "presentation about", "make
  a ppt", "PowerPoint", "curation deck", "program deck", "proposal deck", "offer deck", "quote
  slides". This applies even when the user mentions an existing .pptx, .pdf or Figma deck as input:
  the output is always a fresh Poetics deck, so this skill owns the workflow.
---

# Brand decks

Read `${CLAUDE_PLUGIN_ROOT}/GLOBAL_RULES.md` first.

## Reference files

```bash
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/design-system.md"      # the visual system
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/deck-copy.md"   # how to write: the website's voice
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/guides/anti-slop.md"   # the deck rules, what never to do
cat "${CLAUDE_PLUGIN_ROOT}/brand-kit/brand.md"              # company facts, logo rules
```

For proposals, also read `brand-kit/guides/proposal-playbook.md` (modes, pricing rules).

---

## 1. The question tree (every time the skill is called)

Run this before writing anything. Use AskUserQuestion. **Skip any question the request already
answers**, and never ask more than four at once. Recommend an option when you can (first, marked
"Recommended").

```
Q1  What is the deck for?
    ├─ Introduce Poetics to someone (venue, partner, funder, a talk)  → STANDARD (16:9)
    ├─ Show the titles we chose for one venue                          → CURATION (16:9)
    └─ Put a price or terms in front of a client                       → PROPOSAL (A4, practical)
                                                                         └─ Q1b  Where are they?
                                                                            ├─ First contact, haven't seen it   → pitch
                                                                            ├─ Scope agreed, ready to sign      → offer
                                                                            ├─ Budget or size unknown           → tiered
                                                                            └─ Just want the price              → quote
```

Then the variant's must-haves (ask only for what's missing):

- **Standard:** who it's for, presented live or sent.
- **Curation:** venue, occasion, audience, dates, minutes per visitor, languages, and the titles
  (never pick films yourself).
- **Proposal:** the playbook's checklist: client, venue, dates, pods, **the price** (never guess
  it), payment terms, proposal number, and the language (most proposals are in Greek: `"lang": "el"`).

Then, for every deck with photographs (not proposals), ask:

```
Q2  Which photographs?
    ├─ Ours: pick from the Poetics photo library            (Recommended)
    ├─ Yours: you'll send the files
    └─ Mixed: ours, plus some you'll send
```

For "ours", show the library sheet so the user can see what's there:
`python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/photo-library.py" sheet /tmp/photos.png --use cover`
(uses: cover, wide, portrait, people, any). Refer to library photos by id: `"image":
"photo:events-two-visitors-cinematic-11"`. Portraits of named people only go on a page that names
them; team photos only when asked. Curation stills never come from the library (see the audit
round).

### Only if the brief is unclear: the audience questions

Ask these when you can't tell who the deck is for or what it must achieve. Not otherwise.

- **Who will see it?** Museum or gallery · Festival · Brand or agency · School or university ·
  Funder or investor · A repeat client
- **How will they see it?** Presented live · Sent to read · Both
- **What should they do after the last page?** Write to us · Confirm dates · Approve a program ·
  Sign
- **What do they already know about Poetics?** Nothing · Saw it at an event · Worked with us

Use the answers to **suggest** additions and removals, then let the user decide:

| Audience | Suggest adding | Suggest removing |
| --- | --- | --- |
| Museum or gallery | How we choose programs (E2), the room and footprint, a portrait of a cultural figure (V2) | Pricing models, software |
| Festival | Figures (P1), throughput per hour, gallery of past festivals (S4) | Long company story |
| Brand or agency | Audience figures, brand events (E4), visitor quotes | Curation detail |
| School or university | The education strand, age ratings, hygiene and supervision | Roadmap, software |
| Funder or investor | Figures, what comes next (T1), software (S1), recognition | Operations detail |
| Repeat client | Only what's new: program, dates, price | Introduction, statement, gallery, visitors |
| Sent to read | `density: "reading"`, short paragraphs (E5) where needed | Pages that only work spoken |
| Proposal, any client | Only what decides the deal: scope, capacity, price, terms | Intro and closing pages, photographs, figures |

Confidential material (roadmap, franchise, streaming platform status, internal tools, pricing
models) only goes into a deck when the user includes it.

### Filler pages: always ask

Filler pages carry no information of their own: **O3 Statement, N1 Section divider, N2 Agenda,
S3 Full photo, S4 Gallery**. The renderer lists them after every render. Before delivering, ask
(AskUserQuestion, multiSelect) which to keep, naming each one with its page number and content
("2 · O3 · You give us the room."). Remove the rest. Never add filler to a proposal.

---

## 2. Storyline: headings only

List every page as its template code plus its heading, and show the list to the user before
rendering:

```
O2  Immersive cinema, anywhere.
E3  What we take care of.
P1  What we have done so far.
S1  We run it ourselves.
C1  Tell us about your space.
```

Read the headings in order: together they should tell the whole story. Write them the way the
website does (`guides/deck-copy.md`): a short plain sentence with a full stop, "we" and "you",
what happens rather than how it feels. Reuse the website's own lines where they fit.

---

## 3. Page templates

Every page is one of these. Build by reusing them; pick by the **shape of the content**.

| Category | Code | Template | Use it when the content is… |
| --- | --- | --- | --- |
| **Open** | O1 | Cover | The title and one line, no photo to hand |
| | O2 | Cover with photo | The title, with a real event photograph (preferred) |
| | O3 | Statement *(filler)* | One sentence that matters |
| **Navigate** | N1 | Section divider *(filler)* | A new part, in decks over ~12 pages |
| | N2 | Agenda *(filler)* | A long deck's real order |
| **Explain** | E1 | Claim and rows | A heading with 2–5 short lines |
| | E2 | Claim and terms | Labels with values: brief, specs, terms |
| | E3 | Claim and columns | 2–4 parallel things of equal weight |
| | E4 | Claim and photo columns | 2–4 parallel things, each with a photograph |
| | E5 | Text | A few short paragraphs (mostly proposals) |
| **Prove** | P1 | Figures | 1–4 real numbers, with an as-of date |
| | P2 | Comparison table | Tiers, a program, add-ons |
| **Show** | S1 | Text and photo | A few lines and one photograph |
| | S2 | Photo with claim | The photograph is the evidence |
| | S3 | Full photo *(filler)* | A pause: one photograph, no words |
| | S4 | Gallery *(filler)* | 2–8 photographs showing range |
| **Voices** | V1 | Quote | One person's words |
| | V2 | Portraits | 2–5 named people who were there |
| **Time** | T1 | Steps | Real steps in order (`now` marks today) |
| **Close** | C1 | Closing | One path: write to hello@poeticsvr.com |
| **Deal** | D1 | Price | One all-inclusive figure, what it covers, validity |
| | D2 | Acceptance | Signature blocks |
| | D3 | Quote sheet | The practical proposal page: to, heading, intro, scope, capacity, price |
| **Program** | W1 | Title card | Curation only: one work, still, synopsis, facts |
| **Document** | A1 | Stacked page | A4 only: two or three templates on one page |

See them all: `build-deck.py templates/decks/catalog.json /tmp/catalog.html --sheet` →
`/tmp/catalog-sheet.png`. **When you're unsure which template fits a page**, show the sheet or the
candidates and ask with AskUserQuestion: two to four options, each "code · name: why", your
recommendation first.

---

## 4. The three variants

Starters (full examples) in `${CLAUDE_PLUGIN_ROOT}/brand-kit/templates/decks/`. Copy one,
then rewrite it for the brief. Curation and proposal starters ship with `"draft": true`
(placeholders show highlighted); remove `draft` for the version that goes out.

**Standard** (`standard.json`): 16:9, speaker density. Films described by theme only.

**Curation** (`curation.json`): 16:9, reading density. The one place films are named (W1).

**Proposal** (`proposal.json`, `quote.json`): a **practical document**, modelled on the proposals
Poetics already sends. A4 portrait, reading density, **no cover and no closing page**: the first
page is the D3 quote sheet (to, heading, one intro sentence, the scope as ruled rows with
sub-items, capacity, the price). Every footer carries the disclaimer ("Any change in scope requires
an adjusted quotation.", or the client-specific wording in `"disclaimer"`) and the date
(`"date"`, today by default). `"lang": "el"` writes the footer, labels and signature lines in Greek.
Keep the client's own terms of art (scope, pods, licensing) as the team writes them. Modes:

- **quote** (1 page): D3. As `quote.json`.
- **offer** (2 pages): D3 · A1 (E2 terms + D2 acceptance). As `proposal.json`.
- **tiered** (2 pages): A1 (E5 one paragraph + P2 tiers with `highlight` and
  `highlight_label: "Recommended"`) · A1 (E2 terms + D2 acceptance).
- **pitch** (2–3 pages): A1 (E5 what we propose + E3 what we take care of) · D3 · A1 (E2 terms).
  A pitch that needs photographs and a story is a standard deck, not a proposal.

---

## 5. Curation: research, then the audit round

Curation decks name real works, so every fact and link must be true.

1. **Research.** For each title the user names, find the official sources: the distributor's
   catalog page, the studio's page, the festival's selection page. Take facts only from these
   (title, creator, year, length, format, languages, distributor) and record each in `sources`
   with its URL. Use a still from the official press kit or distributor page, with an
   `image_credit` saying where it came from, and an official page or trailer as the `link`.
   Never use a Poetics library photo as a film still. Anything you can't find stays a
   `[PLACEHOLDER]`.
2. **Audit round** (a separate pass, after the deck is drafted): open every source again and
   compare it with what the slide says. Fix any mismatch; mark each source `"checked": true` only
   after confirming it. Then run:
   `python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/audit-deck.py" deck.json`
   It checks every link answers, every image resolves and is large enough, every title card has
   checked sources and a credit, and no placeholder is left. It writes `deck-audit.md`.
3. **Report** the audit table to the user with the deck. A deck with a failed audit is a draft:
   say what failed.

Proposals and standard decks that cite outside facts (press, awards, partners) get the same audit.

---

## 6. Rules for every deck

- **Say less.** Short plain sentences, website voice (`deck-copy.md`). No cheesy taglines, no
  chatty phrases ("ready when you are", "as we understood it", "let's").
- **White space.** Fewer things per page. Split rather than fill.
- **Few overlines** (a quarter of the pages at most, only to add a fact). **True counts**, not
  threes. **No makers' names** unless asked. **Email: hello@poeticsvr.com**, only.
- **Footer on every page: poeticsvr.com · Confidential.**
- **Closing (C1): one path, the email.** No buttons, no second option.
- **Spacing guardrail.** Nothing within 72px below the wordmark, nothing overlapping, nothing
  crowding the footer. `--check` fails a deck that breaks it; fix it before delivering.
- Light theme (off-white, never #FFFFFF) by default; no em dashes, exclamation marks or emoji;
  never invent a fact, figure, quote or price; never name a film outside a curation deck.

The renderer warns on all of these. Fix every warning or say why it stays.

---

## 7. Render, look, deliver

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-deck.py" deck.json deck.html --sheet
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-deck.py" deck.json deck.pdf
python3 "${CLAUDE_PLUGIN_ROOT}/brand-kit/scripts/build-deck.py" deck.json deck.pptx   # 16:9 only
```

`--sheet` writes a PNG per page, a captioned `deck-sheet.png`, reports overflow, spacing and
overlap problems, and lists filler pages. **Look at the images** before delivering. Fix content, not CSS: fewer words, fewer rows,
split the page, another template. Re-render after every fix.

Deliver HTML + PDF + the sheet. A 16:9 HTML deck is a presenter (arrows, F fullscreen, N notes,
T theme); an A4 HTML is a scrolling document. PPTX only for 16:9 decks someone must edit. Say
what's still a placeholder.
