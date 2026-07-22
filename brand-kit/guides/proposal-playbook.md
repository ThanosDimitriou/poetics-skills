# Proposal playbook

How Poetics writes proposals, offers, and quotes to other companies — venues, museums, festivals,
schools, event spaces. This guide defines the document structures; `brand.md` defines the brand
and `schemas/doc-content-schema.md` defines the JSON payload both renderers consume. Like
everything in this kit, it is tool-agnostic: any AI assistant or person can follow it.

**Canonical output:** PDF via `scripts/build-doc-pdf.py` (full dark-brand fidelity). Produce
`.docx` via `scripts/build-doc.py` only if the client explicitly needs an editable file.

**File naming:** `Poetics-Proposal-<Client>-<YYYY-MM>.pdf` (or `Poetics-Quote-...` for quote
mode).

---

## The four modes

One skill, four document shapes. Pick by where the client is in the conversation:

| Mode | When | Length | Price appears |
|---|---|---|---|
| **pitch** | First contact, cold or early-stage — they haven't felt the product yet | 6–7 sections | Late, one figure, after the experience is sold |
| **offer** | Warm client ready to decide — scope is roughly agreed | 3 sections | Early-middle, one figure, with terms and a signature block |
| **tiered** | Budget or scale unknown — let them pick a size instead of saying no | 4 sections | Middle, one figure per tier, with a recommendation |
| **quote** | Fast follow-up to a warm or repeat client — "just send me the price" | 1 section | Immediately, one figure, reply-to-confirm |

If the mode isn't obvious from the request, ask once: "Is this a first pitch, a firm offer, a
tiered offer, or a quick quote?" A request for a "pitch deck" or "slides" is **not** this
playbook — that routes to decks.

### pitch — the cinematic proposal

Sells the feeling before the logistics. Sections, in order:

1. **The experience** — open in the inner voice (short italic beat: *"You sit down. The lights
   dim."*), then narrate what one visitor feels and what that does for the venue. No specs yet.
2. **What we do** — the three verbs as stacked callouts: Curate, Install, Operate (use the
   canonical copy from `brand.md`'s Company section).
3. **A program for [venue]** — themes matched to their exhibition/occasion. Describe by theme and
   feeling only; state explicitly that titles come later in curation (never name films).
4. **The engagement** — one specs table: venue, dates, pods, capacity, footprint, staffing, what
   the venue must provide (power, a corner of quiet).
5. **Investment** — the single all-inclusive figure (see Pricing below), add-on lines, validity.
6. **Next steps** — three concrete steps to opening day, plus an invitation to come sit in a pod.
   End with the contact line.

### offer — the commercial proposal

Compact and procurement-ready. Sections, in order:

1. **Overview** — a short summary paragraph, then a `callout-2col`: "Engagement at a glance"
   (venue, dates, pods, capacity, footprint) beside "What's included" (curation, install,
   operation, hygiene, strike). Close with the validity note.
2. **Scope & investment** — a scope table describing what each element covers (no per-line
   prices), then the single all-inclusive price callout, then an optional add-ons table.
3. **Timeline & terms** — a when/what timeline table, terms bullets, and the acceptance callout
   with signature lines for both parties.

### tiered — the configuration offer

Three sizes, one recommendation. Sections, in order:

1. **The idea** — two or three paragraphs: what the installation is, what Poetics handles, why
   the offer comes in configurations.
2. **Configurations** — one comparison table, tiers as columns (established names: **Chamber /
   Gallery / Forum** — small / recommended / large), rows for pods, duration, sessions/day,
   footprint, program size, operators, and price. Follow with a callout: "Our recommendation:
   [tier]" and one honest sentence of reasoning specific to their space and audience.
3. **Included in every configuration** — bullets for the always-included services, then add-ons.
4. **Terms & acceptance** — terms bullets, then a reply-to-confirm callout: "Reply naming your
   configuration and we'll send the confirmation paperwork."

### quote — the quick quotation

Cover page + one section. For clients who already know the product:

1. Single section headed **Quotation** — one context sentence referencing the prior conversation,
   a compact engagement summary table (dates, pods, duration), the price callout, validity and
   payment terms as two or three bullets, and a reply-to-confirm line.

Subtitle carries a quotation number (see Conventions).

---

## Pricing rules

- **One all-inclusive figure is the default** — per proposal, or per tier in tiered mode. Render
  it as a callout: title `€ X — all-inclusive`, body listing what it covers (curation, delivery,
  installation, operation, hygiene, strike) and `Excludes VAT.`
- **No line-item price breakdowns** unless the user explicitly asks for an itemized quote (e.g.
  procurement demands it). The scope table describes the work; the callout carries the number.
- **Add-ons may carry their own prices** (additional weeks, evening-event coverage) — they are
  separate decisions, listed in their own small table.
- **Never invent a price.** The user must supply every figure. If a figure isn't confirmed yet,
  render an explicit placeholder (`€ [TBC]`) and say so when delivering the document — never a
  realistic-looking guess.
- Always note `excl. VAT` wherever a figure appears.

---

## Conventions

- **Cover:** title names the venue or the experience ("Immersive cinema at [venue]", "A cinema of
  one"), sentence case. Subtitle carries the document type: "Proposal & quotation · Nº YYYY-NNN"
  (offer/quote) or "A proposal for [client]" (pitch). Date field: "Month YYYY · Prepared by
  Poetics for [client]" — or just "Month YYYY · Poetics" for pitch mode.
- **Numbering:** offers and quotes get `Nº YYYY-NNN`; ask the user for the next number rather
  than inventing a sequence.
- **Validity:** default 30 days, "dates are held on a first-confirmed basis." Confirm with the
  user if unstated.
- **Terms** (offer/tiered/quote): payment split and invoice terms (ask; don't assume), insurance
  note, cancellation policy, what the venue provides (standard power; no network dependency for
  playback). Only state terms the user has confirmed are real.
- **Acceptance:** offer mode gets signature lines for both parties inside a callout; tiered and
  quote modes close reply-to-confirm; pitch mode closes with next steps instead.
- **Contact line:** name · Poetics · email · poeticsvr.com, as the last paragraph.
- **Theme:** dark is canonical. If the proposal will be printed or the client's procurement
  process wants a conventional document, set `"theme": "light"` in the content JSON — white body
  pages, dark cover kept (see `brand.md`, Light / print variant). Same content payload either
  way; nothing else changes.

---

## Voice

Everything in `brand.md`'s Voice & tone section applies, plus:

- The inner voice (serif italic, second person) belongs in **pitch mode's opening** and, at most,
  one or two 2–4 word emphasis phrases per page elsewhere. Offer, tiered, and quote modes are
  narrator-voice documents — factual, scannable, no flourish.
- Sell by what the visitor feels and what the venue's team never has to do. Never hype, never
  superlatives, never "immersive revolution."
- Never name or visually identify a film — describe programs by theme only, and in pitch mode say
  outright that titles come later in curation. It reads as confidence, not evasion.
- State what Poetics handles as flat fact (delivery, cabling, operators, hygiene, strike). The
  quiet completeness of the list is the pitch.

---

## Reusable payload snippets

The price callout — use the elevated `price-callout` block (not a generic `callout`): the price
is the single most-scanned element in a proposal, and it should read as the page's focal point,
not another card among cards:

```json
"<div class=\"price-callout\"><div class=\"price-value\">€ 18,600</div><div class=\"price-note\">All-inclusive</div><div class=\"price-body\">Curation, licensing coordination, delivery, installation, operation for all open hours, hygiene protocol and consumables, and strike. Excludes VAT.</div></div>"
```

For tiered mode, mark the recommended column with `class="recommended"` on its `<th>` and `<td>`
cells so it's visually obvious before a client reads a single row:

```json
"<table><tr><th>Configuration</th><th class=\"recommended\">Gallery (recommended)</th><th>Forum</th></tr><tr><td>Price</td><td class=\"recommended\" style=\"text-align:right;white-space:nowrap\">€ 18,600</td><td style=\"text-align:right;white-space:nowrap\">€ 32,400</td></tr></table>"
```

The at-a-glance pair (offer mode, section 1):

```json
"<div class=\"callout-2col\"><div class=\"callout\"><div class=\"callout-title\">Engagement at a glance</div><div class=\"callout-body\">Venue: …<br>Dates: …<br>Pods: …<br>Capacity: …<br>Footprint: …</div></div><div class=\"callout\"><div class=\"callout-title\">What's included</div><div class=\"callout-body\">Program curation matched to your theme<br>Delivery, cabling, and installation<br>Trained operators for all open hours<br>Hygiene protocol and consumables<br>De-installation and strike</div></div></div>"
```

The acceptance block (offer mode):

```json
"<div class=\"callout\"><div class=\"callout-title\">Acceptance</div><div class=\"callout-body\">To confirm, countersign below and return this page — or simply reply to the covering email and we'll take it from there.<br><br>For Poetics: ______________________&nbsp;&nbsp;&nbsp;&nbsp;Date: ____________<br><br>For [client]: ______________________&nbsp;&nbsp;&nbsp;&nbsp;Date: ____________</div></div>"
```

A testimonial or the pitch-mode opening line — use `pull-quote`, not italic body text, so it reads
as a deliberate beat rather than an aside:

```json
"<div class=\"pull-quote\"><div class=\"pull-quote-text\">It was my first VR experience, and it was overwhelming. In seconds, you're transported into a world that feels real, yet beautifully dreamlike.</div><div class=\"pull-quote-attribution\">Marina Spanou, Songwriter &amp; Performer</div></div>"
```

Traction numbers (pitch mode's "why this works," or any report's "at a glance" figures) — use
`stat-row`, not a bullet list, whenever a number is the point:

```json
"<div class=\"stat-row\"><div class=\"stat\"><div class=\"stat-value\">1,500+</div><div class=\"stat-label\">screenings delivered</div></div><div class=\"stat\"><div class=\"stat-value\">96%</div><div class=\"stat-label\">of viewers recommend</div></div></div>"
```

Right-aligned price cells in tables need `style="text-align:right;white-space:nowrap"` so figures
don't wrap.

---

## Working from provided text

When the user supplies their own text (paste, file, notes) instead of describing the document,
determine intent first — verbatim or raw material — and ask once if unclear:

- **Verbatim** — keep their wording. Map it onto the chosen mode's section structure and the
  standard furniture (price callout, tables, acceptance close); escape it; change nothing but
  obvious typos. If something the mode requires is missing (price, validity, acceptance), flag
  the gap and ask — don't write it for them unasked.
- **Raw material** — mine it for the facts (client, occasion, scale, dates, figures, terms),
  then write the document in the brand voice following the mode's structure, exactly as if those
  facts had come from the interview below. The pricing rules above still hold: figures come only
  from the user's material or their answers.

---

## What to ask before generating

One question at a time; skip anything already given:

| Missing | Ask |
|---|---|
| Mode | "First pitch, firm offer, tiered offer, or quick quote?" |
| Client & venue | "Who's it for — which venue/space?" |
| Occasion | "What's the occasion — exhibition, festival, event? Any theme?" |
| Scale & dates | "How many pods, how long, and when?" |
| **The price(s)** | "What's the all-inclusive figure?" (or per-tier figures) — never guess |
| Terms | "Payment terms and validity — use 50/50 and 30 days, or something else?" |
| Number | Offer/quote modes: "What proposal number should this carry?" |
