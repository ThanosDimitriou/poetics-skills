# Proposal playbook

How Poetics writes proposals, offers and quotes to other companies: venues, museums, festivals,
brands, agencies, schools. Every proposal is a **practical A4 document** built with the deck
renderer's proposal variant, modelled on the proposals Poetics already sends (one page that says
who it's for, what's in scope and what it costs). `design-system.md` defines how it looks,
`guides/deck-copy.md` how it's written. Like everything in this kit, it is tool-agnostic.

**Renderer:** `scripts/build-deck.py` with `"kind": "proposal"` (A4 portrait by default).
**Starters:** `templates/decks/quote.json` (one page) and `templates/decks/proposal.json` (offer).
**Output:** PDF (real A4 pages), plus the HTML if useful. No .docx or .pptx.
**File naming:** `Poetics-Proposal-<Client>-<YYYY-MM>.pdf`, or `Poetics-Quote-...` for quotes.

---

## The shape

No cover, no closing page, no photographs, no filler. The first page is the **quote sheet (D3)**:

1. **To:** the client (`"to"`); "Προς:" in Greek.
2. **Heading:** what it is, in one line: "VR cinema at TIF." "Immersive cinema at [venue]."
3. **Intro:** one sentence on what the proposal covers.
4. **Scope:** ruled rows, each a short bold line with an optional detail and sub-items
   (`"scope": [{"title", "text", "items": [...]}]`). Numbers written the team's way:
   "Δέκα (10) VR pods".
5. **Capacity:** one line, if known ("Up to 3,000 screenings.").
6. **Price:** the single figure, its basis (excl. VAT), validity.

Every page's footer carries the date (`"date"`, today by default) and the scope disclaimer
(`"disclaimer"`; default "Any change in scope requires an adjusted quotation.", or the client's
own wording, e.g. extra hours, branding and printing as separate add-ons). Greek proposals set
`"lang": "el"`; the renderer then writes its own labels in Greek. Keep the team's terms of art
(scope, pods, licensing, onboarding) as they write them.

---

## The four modes

Pick by where the client is in the conversation. If unclear, ask once.

| Mode | When | Pages |
| --- | --- | --- |
| **quote** | "Just send the price", repeat or warm client | 1: D3 |
| **offer** | Scope agreed, ready to sign | 2: D3 · A1 (E2 terms + D2 acceptance) |
| **tiered** | Budget or size unknown: let them pick | 2: A1 (E5 one paragraph + P2 tiers) · A1 (E2 terms + D2 acceptance) |
| **pitch** | First contact, they haven't seen it | 2–3: A1 (E5 what we propose + E3 what we take care of) · D3 · A1 (E2 terms) |

- **Tiered:** tiers as table columns (Chamber / Gallery / Forum: small, recommended, large), rows
  for pods, days, sessions a day, footprint, program size, operators, price. Mark the one you'd
  pick with `"highlight"` and `"highlight_label": "Recommended"`, and say why in the table's
  `"note"`, in one honest sentence about their space.
- **Pitch:** a pitch that needs photographs, visitors and a story is a **standard deck**, not a
  proposal. The pitch proposal stays practical.

---

## Pricing rules

- **One all-inclusive figure is the default**, per proposal or per tier. The quote sheet sets it
  large; its basis says "excl. VAT" (Greek: "Χωρίς ΦΠΑ").
- **No line-item prices** unless the user asks for an itemized quote (procurement sometimes does).
  The scope says what's included; the figure carries the price.
- **Add-ons may carry their own prices** (an extra week, an evening event), in a small P2 table
  after the price.
- **Never invent a price.** Every figure comes from the user. If one isn't confirmed, the document
  is a draft (`"draft": true`, the price shows as a highlighted `€ [AMOUNT]`), and you say so when
  delivering it. Never a plausible-looking guess.

---

## Conventions

- **Numbering:** offers and quotes carry `"number": "YYYY-NNN"` (shown in every footer as Nº).
  Ask the user for the next number; never invent a sequence.
- **Validity:** 30 days by default, "Dates are held for whoever confirms first." Confirm if
  unstated.
- **Terms** (offer, tiered, and on request for quotes): payment split, cancellation, what the
  client provides (the space, standard power, access the day before). Only terms the user has
  confirmed are real.
- **Acceptance:** offers and tiered offers end with signature blocks (D2); quotes end with the
  price (the client replies by email).
- **Contact:** the footer and hello@poeticsvr.com. No personal names unless the user asks.

---

## Voice

The website's voice (`guides/deck-copy.md`): plain, concrete, first person plural, short
sentences, active verbs. A proposal is narrator-voice throughout: state what Poetics handles as
flat fact (delivery, cabling, operators, hygiene, pack-down). The quiet completeness of the list
is the pitch. No hype, no superlatives, no "immersive revolution". Never name or show a film:
describe a program by theme, and say titles come with curation.

---

## Working from provided text

When the user supplies their own text (an earlier proposal, notes, an email), ask once if unclear:
**verbatim** or **raw material**?

- **Verbatim:** keep their wording; map it onto the quote sheet (to, heading, intro, scope rows,
  capacity, price, date, disclaimer). Change nothing but obvious typos. If something is missing
  (price, validity, acceptance for an offer), flag it and ask.
- **Raw material:** take the facts (client, event, scope, dates, figures, terms) and write it in
  the website's voice, as if they came from the questions below. Figures still come only from
  their material or their answers.

---

## What to ask before generating

One question at a time; skip anything already given:

| Missing | Ask |
| --- | --- |
| Mode | "Just the price, a firm offer, sizes to choose from, or a first pitch?" |
| Client | "Who is it for, and who should it be addressed to?" |
| Event or venue | "Which event or space, and when?" |
| Scope | "How many pods, how many days and hours, how many titles, what else is included?" |
| **The price** | "What's the all-inclusive figure, excl. VAT?" (or one per size). Never guess |
| Terms | "Payment terms and validity: 50/50 and 30 days, or something else?" |
| Number | Offers and quotes: "What number should this carry?" |
| Language | "Greek or English?" |
