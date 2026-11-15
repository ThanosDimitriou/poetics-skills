# Poetics brand kit: handbook

How to get good work out of the Poetics brand kit: what to ask for, how to work with Claude on it,
what the rules are and why, and what to do when something looks off.

**Who this is for.** Anyone at Poetics who makes a deck, a proposal, a document, a social post or a
thumbnail, or who wants to check one. Part 9 is for whoever looks after the kit itself.

**What it is.** The kit is two things that travel together:

- **Knowledge:** the brand spec, the website's design system, the voice, and the rules for what
  never goes into anything (`brand-kit/brand.md`, `design-system.md`, `guides/`).
- **Skills and renderers:** instructions that tell Claude which of that to read for each job, and
  scripts that draw the result mechanically (decks, proposals, documents, social posts), so the
  look is the same whoever asks.

You don't operate any of it. You describe the job; Claude reads the right parts, asks what it
needs, writes the content and runs the renderer. Your part is the facts, the decisions and the
review.

Installing it is a separate page: [INSTALL.md](INSTALL.md).

---

## 1. The five-minute version

1. **Ask in plain words.** "Make a deck that introduces Poetics to a museum director." "Quote for
   [client] for [event], in Greek." "Instagram carousel for agencies and venues." The right skill
   starts by itself.
2. **Answer its questions.** For a deck it asks what the deck is for, who sees it and which photos.
   For a proposal it asks for the facts and **the price**. Give real answers; it won't guess.
3. **Look at what it made.** You get the file and an overview image of every page or slide. Open
   the overview first. Tell Claude what to change by page number: "page 4: shorter heading",
   "slide 3: a different photo".
4. **Fix what it flags.** Warnings about spacing, overflow or wording are real. Ask for them to be
   fixed in the content, not worked around.
5. **Check the facts and the photos yourself before it goes out.** Claude never invents a figure or
   a price, but it can't know whether the date is still right or whether someone agreed to be in
   a photo.

---

## 2. What to ask for

| You want | Say something like | You get | Skill |
|---|---|---|---|
| A deck to introduce Poetics | "Make a deck about Poetics for a festival director, presented live" | 16:9 HTML deck, PDF, overview image (PPTX on request) | brand-decks |
| A program of titles for one venue | "Curation deck for [venue], [occasion], 20 minutes a visitor. Titles: [list]" | Curation deck with facts checked against official sources | brand-decks |
| A price in front of a client | "Quote for [client], [event], [dates], 4 pods, €[price] excl. VAT, in Greek" | A4 quote sheet (PDF) | brand-proposals |
| A report, brief or one-pager | "One-pager for programmers on how a pop-up cinema works. PDF" | A4 PDF, or a Word file if it must be edited | brand-documents |
| An Instagram, LinkedIn or TikTok post or story | "Instagram carousel for agencies and venues, 6 slides, then a story version" | PNG slides at 4:5 or 9:16, plus a caption | brand-templates |
| A post or carousel, by hand | "Open the social studio" | A browser studio: all feed styles, drag to adjust, exports PNG, ZIP, PDF | brand-templates |
| A video thumbnail | "YouTube thumbnail for [video]" | 1920 × 1080 PNG from the thumbnail editor | brand-templates |
| A check of something | Attach it: "Review this against the brand" | A score out of 10, what passes, what to fix | brand-review |
| An answer | "Can I use the blue for a button?" "Does this sound like Poetics?" | Yes or no, the rule, the reason | brand-guidelines |
| Company boilerplate | "Write an about-us paragraph for a proposal intro" | Approved wording from the brand spec | company |
| Colors, fonts, logo rules | "What font do we use for headings?" | The exact spec | brand-identity |

You don't need to name the skill. The trigger words are in each skill's description, and the
plugin's routing rules send deck, proposal, document and social requests to these skills instead of
Claude's generic ones.

**Photos.** Decks, documents and social posts can use Poetics' own photographs by name (part 6).
If you don't have the photo library, send the files you want used.

---

## 3. How a good session goes

```
Brief → Claude's questions → draft (headings or copy) → render → look → fix → deliver
```

**Give the brief in one go.** What it is for, who sees it, the language, any dates or numbers you
want in it, the photos. The more of it you give up front, the fewer questions you get.

**Ask to see the outline first.** For a deck: "Show me the page headings before building." Changing
a heading is cheap; changing a rendered deck is slower.

**Give facts, not adjectives.** "Six pods, one day, 250 screenings" gives Claude something to
write. "Make it impactful" gives it nothing, and you get stock phrases back.

**Review the overview, not the file.** Every render comes with an overview image of all pages.
Check it for: the right story in the right order, headings that read as plain sentences, photos
that fit, nothing cramped.

**Iterate by pointing.** "Slide 5: remove the subtitle." "Page 2: the figure should say 'as of
September 2026'." "Swap the photo on page 3 for one with an empty room."

**Know when to stop.** The rules in part 7 are strict on purpose. If Claude says it can't put
something in (a film's name, a price it wasn't given, an unlisted claim), the answer is to supply
the fact or leave the line out, not to argue it into the file.

---

## 4. Decks, proposals and documents

### Decks

Three variants. Claude asks which you need.

| Variant | For | Notes |
|---|---|---|
| Standard (16:9) | Introducing Poetics to a venue, partner, funder, or a talk | One idea a page. Presented live or sent |
| Curation (16:9) | The titles chosen for one venue | You give the titles. Claude never picks films |
| Proposal (A4) | A price or terms in front of a client | See below |

Tell it whether the deck is presented live or sent (sent decks need more on the page), and say
which photos. A deck gets its page headings as short plain sentences with a full stop.

### Proposals

Every proposal is an A4 quote sheet, built to `brand-kit/guides/proposal-playbook.md`. There are
four modes:

| Mode | Use it when |
|---|---|
| Quote | They only want the price |
| Offer | Scope is agreed and it is ready to sign (adds terms and signatures) |
| Tiered | Budget or size is unknown (several configurations) |
| Pitch | First contact, they haven't seen anything yet |

Things to have ready: client and addressee, the event or venue and dates, scope (pods, hours,
program), **the price**, terms, a proposal number, and the language. Most proposals are in Greek.

Rules that matter: one all-inclusive figure, excluding VAT, unless you ask for line items. **Claude
never guesses a price, date or term.** If one is missing the sheet is marked as a draft and
Claude tells you which figure to confirm. The footer carries the date and the scope disclaimer.

### Documents

Reports, briefs and one-pagers on A4. **PDF is the version to send** (fonts embedded, real pages).
Ask for Word only when someone has to edit it; it needs Instrument Serif and Inter Tight installed
to look as designed. If you give Claude source material (a link, a thread, pasted notes), it
extracts and structures the content first. If you attach an existing Word file it edits that
file instead of rebuilding it.

Figures get an as-of date. A price is set as a price, not a bullet.

---

## 5. Social posts and stories

Two ways to make social assets. Pick by the job.

| | Social studio | Renderer |
|---|---|---|
| What it is | An HTML page you open in a browser | A script Claude runs |
| Good for | Making or finishing a post by hand: drag, reframe, resize | A whole carousel planned and rendered by Claude |
| Output | PNG, a ZIP of all slides, a LinkedIn PDF, a project file | All slides, a contact sheet, checks |
| Look | The three feed layouts | The same three layouts, the same pixels |
| Needs | A browser, nothing else | Claude Code (Chrome and Playwright). Not claude.ai chat |

Both use the same deck JSON: ask Claude for a deck, open it in the studio, adjust by hand; or save
from the studio and have Claude render it. The studio is
`brand-kit/templates/social-carousel/editor.html` (4:5, 1:1, 9:16); the thumbnail editor is
`video-thumb/editor.html` (1920 × 1080). Both work offline by double-click.

**Using the studio:** pick a format and the wordmark rule at the top, or start from an example
carousel. For each slide choose a style, type the lines (each has its own size), add photos and
click one into the selected frame. Drag text to move it, drag a photo to reframe it, scroll to zoom.
The strip at the bottom adds, duplicates, deletes and reorders slides. Fix what Checks lists, then
export. Save project keeps everything, photos included, to carry on later.

### The three layouts

| Layout | Look | Use it for |
|---|---|---|
| **type** | A solid ground (paper, dark, or brand blue), big serif lines, a light grain | An idea, a question, a statement. "Why Poetics", the problem festivals face |
| **photo** | A full-bleed photograph, big serif lines on a soft shade. A duotone option | Ads and energy. The thing that should stop a scroll |
| **framed** | Light ground, every photograph in an oval or rounded frame | Proof and offers for agencies, venues and brands. The nearest to the website |

Things to know:

- **One layout per post.** A photo carousel may have a type slide between its photos. A framed
  carousel stays framed.
- **Pinned or neighbouring posts get different layouts**, so their covers don't read as one post.
- **Say less.** One to three lines a slide, one short line under at most, no footers, no slide
  counts. Big words beat small ones.
- **Stories** use the same decks with `"format": "story"` (1080 × 1920). The top 270px and bottom
  380px are kept clear of Instagram's own interface and an ad's button.
- **Slide 2 is a second cover.** Instagram shows a carousel again from slide 2, so make it work
  alone.
- **LinkedIn:** add `--pdf` and post `slides.pdf` as a document post.
- **Captions** repeat the essential slide text and the email, and end with three to five CamelCase
  hashtags (#ImmersiveCinema).

### How to ask

> Instagram carousel to promote Poetics to agencies and venues. Framed style, 6 slides, one
> idea each. Then the story version. Use the photo library.

Claude drafts the copy first, shows it to you, renders, and gives you the overview image. The
quickest route to a good post is to react to the copy before it is drawn.

### The deck file (for anyone running it by hand)

The renderer reads a JSON deck. Start from an example in
`brand-kit/templates/social-styles/examples/` (`photo-post.json`, `framed-post.json`,
`type-post.json`, and `styles.json`, which has one slide of each look). Each has a picture next to
it (`photo-post.jpg` and so on): open it to see what the result should look like. The examples use
only photographs without people.

```bash
python3 brand-kit/scripts/build-social.py my-deck.json out
```

| Field | Where | Values |
|---|---|---|
| `format` | deck | `"post"` (4:5, default) or `"story"` (9:16) |
| `grain` | deck | `false` turns the texture off everywhere |
| `layout` | slide | `"type"`, `"photo"`, `"framed"` |
| `ground` | slide | `paper`, `paper-deep`, `dark`, `dark-deep`, `lens` (type slides; photo slides are dark) |
| `treatment` | photo slide | `"natural"` (default) or `"duotone"` |
| `arrangement` | framed slide | `cover`, `rows`, `lens`, `pair`, `close` |
| `photo`, `focal`, `zoom` | photo and framed | a photo id or path; `"50% 40%"`; `1.15` |
| `lines` | most slides | `[{"t": "Immersive cinema,", "max": 128}]`. Each line fills the column up to `max` |
| `sub`, `link` | most slides | one short line; the email address (`hello@poeticsvr.com`) |
| `valign`, `top` | type and photo | `top`, `center`, `bottom`; or a pixel offset |
| `outline` | type slide | `{"text": "…", "h": 380, "bottom": 150}`: an empty oval drawn as a line |
| `rows`, `photos`, `h` | framed | the rows of `rows`, the two photos of `pair`, the photo height of `lens` |

The renderer prints `ok` or `PROBLEM` for every slide (outside the margins, too close to the
wordmark, in a story's top 270px or bottom 380px, text over a framed photograph) and `COPY` for wording
(an em dash, an exclamation mark, a stock phrase, capitals). It exits with an error if anything is
flagged. The copy check reads English; for Greek posts, read the wording yourself.

### Before a post runs as an ad

- **Consent.** A photograph with people you can recognize needs their agreement for advertising,
  not just for the event. Prefer blurred people, objects and empty rooms for paid posts.
- **Event names.** A photo from a named event (TEDxAUTH, a festival) may need the organiser's
  agreement to appear in an ad.
- **No film names or stills**, ever, outside a curation deck.
- **Stats carry a date.** "5,000+ screenings" is true as of a date; keep that date in the post or
  the caption, and update it when the number changes.
- **Button and link.** Pick the button for the goal (Learn more, Contact us) and send people to
  poeticsvr.com.

---

## 6. The photo library

Poetics' own photographs are listed in `brand-kit/photos/index.json`: what each shows, who is in
it, its shape and its uses. The files themselves stay on your machine, not in the repo (it is
public and the photos show real people).

- **Use by name.** Decks use `"photo:<id>"`; social decks use the id. Ask Claude to show the
  library sheet so you can see what is there.
- **Set up.** The files default to the website's image folder; `POETICS_PHOTO_ROOT` points
  elsewhere. Colleagues without the website project get a zip and a setup prompt:
  [PHOTOS-SETUP.md](PHOTOS-SETUP.md).
- **No library?** Send the photos you want used.
- **Missing photo.** A deck shows an empty frame and warns; the social renderer stops and tells
  you which id wasn't found.

---

## 7. The rules in one page

**Voice.** Plain, concrete, "we" and "you". Short sentences. Say what happens, not how it should
feel. Headings are short plain sentences with a full stop. Sentence case. American spelling
("program", "organization").

| Not this | This |
|---|---|
| Unforgettable immersive journeys! | We install a cinema in your venue in a day. |
| Step into the future of storytelling | Each pod is one seat: a swivel chair, a headset and headphones. |
| Elevate your event, seamlessly. | Trained operators run every session. |

No em dashes, no exclamation marks, no emoji, no italics, no stock words (journey, seamless,
unlock, elevate, unforgettable and the rest in `guides/anti-slop.md`). "True counts, not threes":
if there are four reasons, write four.

**Hard rules, for everything.**

- **Never name or show a specific film**, except in a curation deck made for one venue. Describe a
  program by theme: arts, education, entertainment.
- **Never invent** a figure, date, quote, name, partner or price. An unknown becomes a capitalised
  bracket, `[ATTENDANCE]`, and the item is dropped or the document is marked a draft.
- **Confidential until cleared:** pricing amounts, the franchise model, roadmap dates (other than
  the December festival), the streaming platform's status, internal tooling, survey methodology.
- **One email address:** hello@poeticsvr.com (no personal addresses; don't name who made the
  material unless asked).
- **Stats carry an as-of date.**

**Look.** Off-white paper and ink, light by default, with a dark set. Instrument Serif for display,
Inter Tight for text. The wordmark top-left with space below it. One accent, the lens blue, used
on what can be pressed. Space and hairlines instead of boxes and shadows. Photographs in rounded
frames. Details: `brand-kit/design-system.md`.

**The social feed relaxes four rules**, in those forms only: a soft shade under type on a
full-bleed photograph, a brand-blue ground, a light grain, and a duotone photograph. Everything
else (tokens, fonts, wordmark, voice, the content rules) still applies.

---

## 8. When something looks off

| What you see | What to do |
|---|---|
| Claude didn't use the brand skill | Say what you want in the brand's words: "a Poetics deck", "a branded one-pager", "a Poetics Instagram carousel". Check the plugin is on (`claude plugin list` shows `brand@poetics`) and start a new session |
| The look is the old one (dark, different fonts) | You have an old copy. Update the plugin (INSTALL.md, "Getting updates") |
| "Photo not found" | The id is wrong or the library isn't set up (part 6). Send the photo instead |
| Fonts look wrong in Word | Install Instrument Serif and Inter Tight, or send the PDF |
| A page is flagged for overflow or spacing | Ask Claude to shorten the content. Don't ask it to shrink the type |
| `COPY` or a copy warning | Say the plain fact instead. The warning names the phrase |
| Greek text looks off | Greek is supported; if something is wrong, tell Claude the slide and the line |
| It asks a question you already answered | Say it again in one line; skip nothing you want kept |
| You're in claude.ai chat and can't render posts | Ask for the copy (or a deck JSON) and make it in the social studio |
| Claude refuses a film name or a price | By design. Supply the fact, or leave it out |

If you can't tell whether something is allowed, ask: "Is this on-brand: [the thing]?" The
guidelines skill answers yes or no, then the rule, then the reason.

---

## 9. For whoever looks after the kit

### How it fits together

```
brand-kit/                      the knowledge and the renderers (plugins/brand/brand-kit/)
  brand.md                      company facts, logo rules, voice summary, social sizes
  design-system.md              how everything looks (the website's system)
  guides/                       voice, deck copy, anti-slop, proposal playbook
  scripts/                      build-deck.py, build-doc-pdf.py, build-doc.py,
                                build-social.py, build-social-editors.py, photo-library.py
  templates/                    deck starters, the two editors, social-styles/examples
  photos/index.json             the photo library index
plugins/brand/skills/           one skill per job (decks, proposals, documents, templates,
                                review, guidelines, identity, company)
plugins/brand/GLOBAL_RULES.md   routing and the rules every skill reads first
claude-skills/                  the self-contained bundle for claude.ai chat
mcp-server/                     the same knowledge for other tools
```

The repo root's `brand-kit` is a link to `plugins/brand/brand-kit`.

### Change something, then check it

| You want to change | Edit | Then |
|---|---|---|
| A brand fact, a voice rule | `brand.md` or `guides/` | Ask Claude a question that depends on it |
| How decks, documents or posts look | `design-system.md` and the renderer script | Render the examples and read the overview |
| A social style | `scripts/build-social.py` | Render all four decks in `templates/social-styles/examples/`; every slide should print `ok` |
| The two editors | `templates/_src/`, then `python3 brand-kit/scripts/build-social-editors.py` | Never edit `editor.html` by hand |
| When a skill triggers | The `description` in its `SKILL.md` | Try the phrases in a new session |
| The photo library | The website's image folder, then `photo-library.py index` | Send colleagues a new zip |

Keep `design-system.md` and the renderers in step: where the two disagree, the website's design
system wins, and `design-system.md` is updated to match. Brand questions the spec marks as
open stay open until someone with the answer settles them; don't let Claude pick.

### Releasing a change

1. Commit the change. Bump the version in `plugins/brand/.claude-plugin/plugin.json` and
   `marketplace.json` (the plugin is at 0.5.1).
2. Colleagues on Claude Code update: `claude plugin marketplace update poetics`, then
   `claude plugin install brand@poetics`, then a new session.
3. Colleagues using a cloned repo: `git pull`.
4. claude.ai chat users: rebuild the bundle (steps in `claude-skills/README.md`) and have them
   upload the new zip. The bundle is a snapshot; chat can read the new rules but can't run the
   social renderer.

### Adding a social style

Add a layout or treatment in `build-social.py`, add a slide to `examples/styles.json`, describe it
in `design-system.md` ("Social feed styles") including which rule it relaxes and why, update the
table in the `brand-templates` skill, and render every example. Keep the number of looks small:
three layouts with a few treatments is easier to use than many templates.

### Keeping it honest

- Every claim in a template or example comes from the website or `brand.md`. If a fact changes
  (a count, a date), change it at the source first.
- Check examples render cleanly after any change to fonts, tokens or the wordmark.
- Retire things in the open: the old dark look is retired and `git log` has it.

---

## 10. Prompts to copy

**Decks**
- "Make a deck that introduces Poetics to a museum director. Presented live. Use our photo library."
- "Curation deck for [venue], for [occasion], [N] visitors, [N] minutes each, in English and
  Greek. Titles: [list]. Check the facts against official sources."
- "Same deck, but for a brand agency and shorter: eight pages."

**Proposals**
- "Quote for [client] for [event] on [dates]: [N] pods, [N] hours a day, €[price] excl. VAT,
  50% on booking. In Greek."
- "Tiered proposal for [client]: we don't know the audience size yet."

**Documents**
- "One-pager for festival programmers on how a pop-up immersive cinema works. PDF."
- "Turn this thread into a two-page brief." (paste or link it)

**Social**
- "Instagram carousel promoting Poetics to agencies and venues. Framed style. Six slides. Then a
  story version."
- "A philosophical carousel about why we're called Poetics. Type layout, no photographs on the
  cover. It will be pinned next to our photo post, so make the cover look different."
- "Story version of this post." (give the deck or the folder)

**Checks and answers**
- "Review this deck against the brand." (attach it)
- "Is this on-brand: blue as the background of an Instagram slide?"
- "Rewrite this paragraph in the Poetics voice: [paste]."
- "What are our brand colors, and when do we use the blue?"

---

## Glossary

| Word | Meaning |
|---|---|
| **Aperture** | The shape language of the system: every photograph and module is a form taken from the pill in the wordmark's O |
| **Pill, lens** | Two of the three rounded shapes: a fully rounded oval, and a rounded rectangle for photos |
| **Ground** | The background color of a slide |
| **Treatment** | How a photograph is processed: natural, or duotone (ink, blue and paper) |
| **Shade** | The soft dark gradient under type on a full-bleed photograph |
| **Grain** | A light film texture over a slide |
| **As-of date** | The date a statistic was true, shown with the number |
| **Overview image** | The picture of every page or slide that comes with a render |
| **Skill** | A set of instructions Claude follows for one job, loaded when your request matches |
| **Plugin** | The installed package of skills and the brand kit |
| **Renderer** | The script that draws a deck, document or post from content |
