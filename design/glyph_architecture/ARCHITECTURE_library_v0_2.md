# Glyph and sigil architecture — library edition, v0.2

*Design lane (seat `l`), session LD2, 2026-09-26, America/Phoenix. Branch `design/marks`; the flagship's half
on `design/marks-flagship`. Kickoff: relay R0144 (drafted by LD1a on his instruction). v0.1 (LD1/LD1a) stays
as it was; this file supersedes it where they differ, and says so.*

**Status key.** **RULED** = Josiah's words, quoted. **BUILT** = on `design/marks`, measured, shown to him.
**PACKAGE** = on `design/marks-flagship`, built and measured, landing only in a pin move he declares.
**v0** = drawn, not built. *The seat's reading* marks what is this seat's and not his.

---

## 0. Recommendation first

1. **Merge `design/marks` on his word.** It moves served bytes on the front door and the five wing pages only:
   no pin, no canon.
2. **The flagship package lands in its own pin move, after the corpus-repair pin session he has already
   declared (R0150).** The seat's reading: that session's receipts are about corpus bytes on three surfaces;
   a design change to the same file in the same move would mix two kinds of diff. The package is rebased onto
   the repaired flagship when that session closes.
3. **E stays drawings** until the /adversarial/ page shows a second disposition (relay R0159 to the content
   sessions, who own that page).
4. **His POV/blur line goes to the wuld-ink lane** (relay R0160). It starts from a finding: the live
   peripheral blur renders nothing (§9).
5. **F, the Adversarial Map's own mark, is RULED and built** on the front door (§7b). Its page's tab icon is the
   content lane's to wire, in the adversarial wing v2 session.

---

## 1. What he has ruled (verbatim)

- His brief for this lane, as R0144 records it: *"I love the new additions. If you think you can further
  implement glyphs, sigils, and symbols with subtle animations across the library--without feeling random and
  meaningless--it could really enhance the site's intrigue and visual factor. Draft a new isolated session
  (isolated from the meat and potatoes of the normal library sessions) with your recommended next aesthetic
  steps."*
- His TO DO lines this lane owns (R0144): *"Make glyphs and sigils across site more intricate and elaborate to
  add to sites visual factor, flare, and flow."* and *"Theorize how these glyphs, sigils, and symbols could be
  further implemented across the site, in a meaningful way, that would enhance the site's aesthetic and
  intrigue--elevating it from the plain text--and button interface."*
- The launch: *"go, launch it"* (as relayed by the launching session).
- **On the LD2 design sheet's four rulings, 2026-09-26:** *"Go with your recommendations on all of the
  above."* That adopted: build A, B and D on the wings now; stage D on the flagship as a pin package, lit in
  the flagship's own tier colours; build C on Right to Die first; keep E as drawings, offered to the content
  sessions; send his POV/blur line to its own session in the wuld-ink lane.
- **On F, the Adversarial Map's mark (added by relay R0153 from the L4 session):** *"I'm liking it. Approved as
  is."* The seat read that reply as a yes to both questions it answered: F as drawn, and the built work going
  live. His TO DO line it answers, verbatim (canon `adversarial_map.reader_aid_backlog_L4c`, priority 1 of the
  order he adopted): *"Adversarial part of library has no unique favicon icon (fix)"*.
- Everything v0.1 §1 records stands.

---

## 2. Corrections (measured; each supersedes what it names)

1. **v0.1's law 8 was false.** It said tier marks are flagship-only because "none of the four wing corpora,
   and not the Veganism module, carries a tier field". Every one of them tiers every objection: Right to Die
   2/8/7 at tiers 2/3/4; Abortion 4/3 at 3/4; Transgenderism 11/1 at 3/4; Anthropocentrism 1/2/3 at 2/3/4;
   Veganism 2/4/1/1 at 1/2/3/4. The four wings' corpora call the tier map an "inherited tier-methodology
   FRAME"; the values on the nodes are authored. Every wing page already printed "tier N" on each card and had
   a Tier filter. So the tier marks now sit beside those words (§4, D).
2. **R0144 said each wing's `build_<wing>_index.py` reads its page.** They read only the corpus JSON
   (measured: every `open()` in the five builders). Their "output unchanged" check therefore cannot see a page
   edit; it was run and passes, and the page gate is `tools/icons_regen_check.py` plus
   `measure_wings.mjs`.
3. **R0144 said the house layer's sources exist nowhere.** The packer does:
   `wuld-ink/archive/measurement/k313c_packlayer.py`. The served CSS splits by its banners into its three
   parts and re-packs byte for byte (measured); the JS carries the same markers (§9).

---

## 3. The grammar, and the motion vocabulary (adopted; law 13 is new)

The grammar is v0.1 §2, unchanged: 16×16, crispEdges, `#0a0a0a` ground, chrome `#e8e4dd`, exactly one lit
element, nodes / edges / grounds / brackets, how a thing is **built**, never what it is **about**.

**The motion vocabulary** (`icons/gen_icons.py`, `LIB_MOTION`): every one-shot is written as its mark's
sentence first and its rects second, and uses only these verbs:

| verb | what moves | used by |
|---|---|---|
| `fill` | a block appears (opacity) | the index's cells, the doorway's step, the branches, the nodes |
| `dx` / `dxm` | an edge draws from its left end / from its middle both ways (scaleX) | the lintel, the stem; the undirected edge |
| `dy` / `dym` | an edge draws down from its top / from its middle both ways (scaleY) | the jambs; the fork |
| `stack` | a rung is set down from above | the flagship's ladder |
| `n` `s` `e` `w` | a part arrives from outside | the four peers; the boundary's four sides |

The same verb means the same thing wherever it appears: "arrives from outside" is both the peers gathering
around an empty centre and the boundary closing around two nodes, because both marks are about what
surrounds what. Opacity and transform only; 0.45–0.9 s; nothing loops; the house gate decides.

---

## 4. What is built (BUILT, on `design/marks`)

| | what it says | where | motion | pin |
|---|---|---|---|---|
| **A** | each library mark builds itself the way its sentence says | front door: the title's on arrival, each card's the first time the card is seen, again on hover; each wing's title once as the page opens | its one-shot, once | no |
| **B** | this page is this library | each wing's title carries its mark; its About tab draws the mark large on its pixel grid, parts named ("edge · the lintel", "the opening", "lit · the step"; the peers' centre is named "empty") | the title's one-shot (A) | no |
| **D** (wings) | how an objection is built, before a word of it | beside "tier N" on every card and every tier filter, crimson | a link straight to one card plays that card's tier one-shot once | no |
| **C** (Right to Die) | where you are | a spine in the left margin: one node per objection the filter shows, the lit node the one being read | none; it changes as you scroll | no |

**The one-shots, as built** (`LIB_MOTION`):

| mark | its sentence | the one-shot |
|---|---|---|
| the index | six cells, an index | its six cells fill in reading order, the lit one in its place |
| the flagship | the five-tier ladder | the ladder stacks rung by rung from the shortest; the top rung, lit, is set last |
| Right to Die | a doorway standing open | the doorway draws, lintel then jambs; the lit step appears in the opening and does not move |
| Abortion | a stem that forks; both branches present | the stem grows and forks; both branches appear together |
| Transgenderism | two nodes, one edge, no arrowhead either way | both nodes appear together; the edge draws from its middle, outward both ways at once |
| Anthropocentrism | four peers around an empty centre | the four peers arrive together, each from outside; the centre stays empty |
| Veganism | a boundary enclosing more than one | both nodes appear together; the boundary closes around them from all four sides at once |

**How it is generated.** `icons/gen_icons.py` draws every mark and writes `marks-pages.json`, naming the regions
each page must carry. 19 regions, 37 placements on 6 pages: the front door's 11 (the seven `lib-<name>` marks
now carry their one-shots; the key's rows stay still) plus `lm-css`; each wing's `lib-<wing>`,
`plate-<wing>`, `lm-css`, `wing-css` and `tier-marks` (a `<template>` its own render code clones). The
stylesheets that move the marks are generated too, so a duration cannot drift between six copies. A page's
own code only says "now": it puts `.play` on an element for `--lm-span`, which the generator sets.

**The gate.** `tools/icons_regen_check.py` checks every page in the manifest byte for byte: a missing region, a
changed byte, and a region drawn for a different page are each a difference. 7 of 7 favicons; 37 of 37
regions. **Controls:** `controls_marks.py` v0_2, 20 of 20 as expected, the unmutated control first, the record
byte-identical under two hash seeds. New: C12 a wing's title mark, C13 a plate's part name, C14 one page's copy
of the shared stylesheet, C15 a region planted on the wrong page, C16 a missing template, C17 a wing grid
changed under its plate's labels, C18 a one-shot that moves a rect twice, C19 a missing page. C10 was
retargeted: the abortion card's mark now carries its one-shot, so LD1's mutation string would have hit the
key's still copy instead.

**Measured** (Chromium 153, Firefox 155):

| check | result |
|---|---|
| wings: 5 pages × 6 widths (360–1440) × 4 reading modes × 2 engines | **240 runs, 0 with horizontal overflow on either tab**; the title's mark, one tier mark per card and per filter, and the plate, right on every run |
| wings: WCAG AA over the plate's part names, its caption and the tier lines | **min 5.37:1**, none below 4.5 |
| wings: the motion gate (title), 5 cases × 2 wings × 2 engines | **20 of 20**: moves only at vfx + dark + motion allowed, once |
| wings: anchor arrival | **6 of 6**: the linked card's tier mark plays once; no other card's moves; none under reduced motion or on a light ground |
| Right to Die's spine | **2 of 2**: 17 nodes for 17 cards; lit 0 at the top, 5 at the sixth card, 16 at the end; follows the keyword filter; hidden on About and at 390 px; page ink on a light ground |
| front door (with F) | **80 of 80** layouts without overflow, AA min 5.06, all 8 named marks, LD1's tier motion 12 of 12, **A 12 of 12** (cards below the fold wait until seen; hover replays; the key's rows never move) |
| errors | **0** page or console errors |
| xsurface | GREEN; the flagship untouched (`006aa983` / 2,987,411) |

**Cost, over the wire (gzip -9):** front door +1.3 KB with F (10.1 → 11.4 KB); Right to Die +3.4 KB (with the spine);
Abortion, Transgenderism, Anthropocentrism, Veganism +2.4–2.5 KB each. Raw: +4.7 KB and +10.3–13.5 KB.

---

## 5. Where the build departs from R0144 (the seat's calls, each with its reason)

1. **Abortion's branches appear together.** R0144 had the lit branch appear last. That stages a choice ending
   on one branch; the mark says *both branches present*, and the wing defends an option.
2. **Right to Die's step appears in place** and never moves toward or through the doorway: nothing depicts an
   act (R0108 law 4).
3. **The spine takes the page's ink on a light ground.** A mark keeps its `#0a0a0a` ground because it must be
   the same object as the tab icon (law 10); the spine is furniture of one page, and a black rail on the cream
   page read heavier than the text it indexes.
4. **Phones get no spine.** There is no margin, the layer's chin owns the bottom edge, and a strip at the top
   would cost reading space on every scroll; the count line already says where the list stands.
5. **The plates scale down on phones** (0.50 at 360 px, measured, so the 13 px part names render at about 6.5 px): the drawing
   stays whole and its caption carries the sentence. Zoom restores the names.
6. **The front door's key says what changed:** every library sorts its objections on the same five tiers; each
   card's mark builds itself once where effects are on, the way its line says.
7. **The flagship's marks are lit from its own `TIERS` table** (`--lit` on each tile), so no colour is copied into
   the generator; a tile keeps the dark-ground colour in every mode because its ground never changes.

---

## 6. Laws for any library use

v0.1 §6's laws 1–12 stand, except **law 8, which is withdrawn** (§2.1): tier marks go wherever a tier's words
are already on the page, and nowhere else. Added:

13. **A motion says its mark's own sentence, once.** If the sentence cannot be written, the mark does not move.
    Verbs come from §3's vocabulary, and a verb means the same thing on every mark.
14. **One source for motion, too.** The generator writes the stylesheet a mark's motion needs, and the page
    only says "now". A page never carries a hand copy of a duration.
15. **A mark keeps its ground; furniture takes the page's ink.** Anything drawn in the grammar that is not the
    same object as a tab icon (the spine, a divider) follows the reading mode.

---

## 7. The flagship package (PACKAGE, on `design/marks-flagship`, `7bf5b35`)

- Every tier badge (82) and tier filter (5) carries its tier's mark beside the words, the game's badge form,
  lit in the tier's own colour from the page's `TIERS`. A shared link to one objection (K108's `#obj-<id>`,
  which adds `.focused`) plays that badge's mark once. The ladder sits beside ARGUMENT LIBRARY and says its
  sentence once.
- Generated regions `lib-combined`, `lm-css`, `flag-css`, `tier-marks`: 41 of 41 regions on 7 pages.
  `controls_marks.py` writes v0_3 on that branch: 21 of 21 (C20: the flagship's stylesheet cannot drift).
- Measured: 48 layout runs (6 widths × 4 modes × 2 engines), no overflow, every badge and filter marked once
  and lit in its tier's colour; the title's one-shot only where the gate is open, 14 of 14; arrival 4 of 4.
- xsurface GREEN (no corpus literal touched); `build_map_sidecars.py --check` unchanged. Package flagship
  `acff9d814949ad1793199aea2f13103e` / 2,996,290 B.
- **What its pin move will also owe** (none done): the front door's "pinned v4.1.2" badge; README's pin
  table; a CHANGELOG release entry; the canon's pin record (a canon bump, the pin session's); wuld-ink's pin
  constants via `tools/library-pin.py` and its search-index regeneration (the objection re-vendor is a no-op by
  identity, since no objection byte moves); the live read-back of `/combined` by bytes and by render; xsurface,
  `build_map_sidecars.py --check`, `icons_regen_check.py` and `controls_marks.py` re-run at the pin.
- **Sequencing:** the corpus-repair pin session (R0150) will change `site/combined.html` first. The package is
  then rebased onto the repaired flagship, re-gated and re-measured before its own pin move.

---

## 7b. F: the Adversarial Map's own mark (RULED; BUILT on the front door)

- **Its sentence, from his words for the page** (*"a mirror library to object to even my OWN beliefs"*, canon
  `audience_and_purpose_ruling_L1a`): **the flagship's ladder faces its own reflection across a mirror.** The
  flagship's five rungs, halved, on the left; their reflection on the right; the mirror between them is the lit
  element, because the mirror is what the page is. It supersedes v0.1 §7.1's "if the Adversarial Map is to carry
  a mark, it needs one drawn" and LD1a's lean to leave it bare.
- **Its one-shot:** the ladder appears, the mirror draws down between, and the reflection appears across it
  (`fill`, `dy`, `fill`; 0.85 s).
- **Checks:** no silhouette shared with any of the 16 other marks (7 library, 5 tier, 4 v0 dispositions); its
  nearest is the flagship's own ladder at IoU 0.35. It reads at 16 px in a tab (shown to him).
- **Built:** `icons/gen_icons.py` draws it as the eighth favicon, `site/icon-adversarial.svg`
  (`afa3a69f79d6aec862d4a75d82419205`, 1,176 B), and as `lib-adversarial` on the front door's Adversarial Map
  card; the key lists it under "The libraries, and the map". 8 of 8 favicons, 38 of 38 regions;
  `controls_marks.py` 21 of 21 (C20: the icon cannot go missing unnoticed); front door re-measured, v0_4.
- **Not built, and not this lane's:** its page's tab. `/adversarial/` is rendered by the content lane's
  `render_wing_v0_1.py`; it changes the page's `<link rel="icon">` to `/icon-adversarial.svg` (and may put
  `lib-adversarial` beside its title) in the adversarial wing v2 session, after the pin session. Relayed with
  the md5.

---

## 8. E: outcome glyphs, v0 (drawings; offered to the content sessions in R0159)

The Adversarial Map sorts every continuation four ways. One layout for all four: the continuation is the node on
top, the corpus is the row of three below, and **the lit element is where the continuation stops**.

| | disposition | the drawing says |
|---|---|---|
| (a) | the corpus already answers it | routed: its edge reaches a node in the corpus, and that node is lit |
| (b) | the corpus needs a stronger text | short: its edge stops before the corpus; the lit end is where our text runs out |
| (c) | it is really a new objection | new: it has no edge into the corpus, so it stays lit where it stands |
| (d) | it reaches bedrock and stops | bedrock: its edge passes the corpus and stops on the lit ground |

All four pass the silhouette law; the nearest live mark is T4 to (a) at IoU 0.50, under the 0.54 already
between T2 and T5. R0108's "met" is drawn as T5's silhouette, and the collision law refuses it; the map has no
"defanged". **Lean, given to the content sessions:** place none until two dispositions are reader-facing; a
family teaches a distinction only when two of its members are in view. Grids: `ld2/ld2_marks.py`, `DISP`.

---

## 9. His POV / peripheral-blur line (sent to the wuld-ink lane in R0160)

- The layer already has both pieces: §5 THE CAMERA (a pan, `--wz-pan: 6px`, bounded by the lip, "10.7 px at
  1440") and §6 PERIPHERAL BLUR (two masked strips, `--wz-soft-w: 34%`, opacity driven from the cursor).
- **FOUND: the blur renders nothing today.** Live, both engines, the strips exist and follow the cursor, and
  `backdrop-filter` computes to `none`, because `--wz-soft-blur` is declared nowhere: not in the served CSS or
  JS, not in any page, not in the archived K313c test file. So "increase peripheral blurring" starts by
  declaring the value and proving a pixel delta.
- **The sources are recoverable:** the served CSS splits into `wuld-type.css`, `wuld-bezel.css` and
  `wuld-vfx.css` and re-packs byte for byte with `wuld-ink/archive/measurement/k313c_packlayer.py`'s banners;
  the JS has `wuld-vfx.js` then banners for `wuld-sfx.js`, `wuld-fb.js`, `wuld-tour.js`, then its tail.
- This lane did not touch the packed file.

---

## 10. Findings, logged and not repaired

- The live peripheral blur is inert (§9); reported to the lane that owns the layer.
- LD1's finding stands: at the vfx tier the layer's first-visit tour can pan the stage 6 px in Chromium. Every
  layout run here was at the cosmetic tier for that reason.
- A wing plate's part names render at about 6.5 px on a 360 px phone (§5.5). A second, narrow drawing would fix it at
  about 1.6 KB per wing; not done.
- An instrument flake, fixed: sampling the front door's title after page load missed its one-shot once in
  Firefox (it had already ended). `measure_front_door.mjs` now counts animation starts from before the page runs.
  `measure_wings.mjs` samples the same way and passed 20 of 20 twice; it was not changed, so its record still
  matches its code.
- The flagship's high-contrast axis is its light ground; the house gate reads the ground itself
  (`wz-lightbg`), so the package needed no special case. Measured in all four modes.

---

## 11. Where everything is

| file | md5 | what |
|---|---|---|
| `icons/gen_icons.py` | `b69a4f46` | every mark, the one-shots, the plates, the stylesheets, the manifest |
| `site/icon-adversarial.svg` | `afa3a69f` | F, the Adversarial Map's favicon (its page wires it later) |
| `icons/sigils.json` | `1e7e99bd` | argue's tier grids, vendored (unchanged) |
| `tools/icons_regen_check.py` | `4a073a4f` | the gate: 7 favicons + every page in the manifest; `--write-marks` |
| `site/libraries/index.html` | `f57480e0` | the front door (with F on the map's card) |
| `site/right-to-die/combined.html` | `41b2a071` | with the spine |
| `site/abortion/combined.html` | `d5a551d8` | |
| `site/transgenderism/combined.html` | `51b48ccc` | |
| `site/anthropocentrism/combined.html` | `7b39591d` | |
| `site/veganism/combined.html` | `e0a89fa0` | |
| `design/glyph_architecture/controls_marks.py` | `9367d60e` | 21 controls |
| `design/glyph_architecture/controls_marks_v0_2.json` | `c17709f8` | their record (pins the six pages' md5s; regenerate after any page change) |
| `design/glyph_architecture/measure_wings.mjs` | `8d2dc91d` | the wings, both engines |
| `design/glyph_architecture/measure_wings_v0_1.json` | `de5bd013` | its record |
| `design/glyph_architecture/measure_front_door.mjs` | `25b790a3` | the front door, both engines (§2b is A; it counts the title's animation starts from before the page runs) |
| `design/glyph_architecture/measure_front_door_v0_4.json` | `a4508cef` | its record for the front door with F (v0_3: the build before F) |
| `design/glyph_architecture/ld2/` | | the design sheet and preview instruments: `ld2_marks.py` (E's grids; reads the generator for the rest), `build_ld2.py` (prototypes on scratch copies, costs, the sheet, the preview), `shoot_ld2.mjs`, `gif_ld2.mjs`, `preview_ld2.mjs` |
| `design/marks-flagship` | `7bf5b35` | the package: flagship `acff9d81`, generator `2c7de4cb`, controls v0_3 `6cad40ba`, `measure_flagship_v0_1.json` `ce8f34c9` |
| relays | | R0144 (the kickoff), R0153 (F, from L4c), R0159 (E, to the content sessions), R0160 (the layer's depth, to the wuld-ink lane), R0161 (the flagship package, FYI for R0150) |
