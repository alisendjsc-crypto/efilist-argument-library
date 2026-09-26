# Glyph and sigil architecture — library edition, v0.1

*Design lane (seat `l`), 2026-09-25/26, America/Phoenix. Branch `design/sigils`. The front door was shown to
Josiah, revised on his notes of 2026-09-26 (§1), and approved: *"I like it."* Answers relay R0111 (the kickoff)
and R0108 (argue's architecture v1, md5 `ee1f57f6`), with R0107.*

**Status key.** **RULED** = Josiah's words, quoted. **BUILT** = on this branch, measured, waiting for his look.
**THEORY** = proposed, not drawn, not started. **PIN** = touches `site/combined.html`, so it is a declared
pin-move session he opens and ratifies. Anything marked *the seat's reading* is this seat's, not his.

---

## 0. Recommendation first

1. **The front door as built goes live.** It moves served bytes on `/libraries` only, no pin, no canon.
2. **Done on his note:** each library's own mark beside its name on the page, and the libraries first in the
   side panel (§4).
3. **First flagship use, when a pin move is declared:** the tier mark on each tier filter button and each
   objection's tier badge, in the game's badge form (§7.2).
4. **First new family:** outcome glyphs (routed / defanged / met). **Not** move glyphs yet: the move-tag
   vocabulary is too scattered to draw (§8.2, measured).

---

## 1. What he has ruled (verbatim; nothing here is paraphrased as his)

- The sigil sheet: *"I like them."* (R0107, R0108 §0.)
- The build and the motion, in the game: *"It all looks good. Approved as is."* (R0108 §0.)
- The HUD retrofit, in the game: *"Very good. I am liking all of them."* (R0108 §0.) Game-only; not adopted here.
- His brief, which R0108 records *"verbatim in substance"* rather than verbatim, with two quoted fragments:
  *"so it also helps make the page look more interesting"* and *"currently there's only words and no real image
  foundation besides the webs, graphs, and flows"*.
- This lane: *"Proceed with your recommendations on all front's. DO you think a sigil  / design architecture
  session would be warranted in its own isolated session while the meat of the library presses on?"* (R0111.)
- Tier sigils in `icons/gen_icons.py`, in principle: L1a recorded it (canon v38.18); his words there were
  *"Going with your recommendations on all of the above."*
- Pedagogy, standing: the audience must *"crawl and scramble to develop its own rational understanding"*.
- **On the preview, 2026-09-26:** *"Show me  a quick preview image, so I can look at it before it goes live."*
  Then: *"Thank you. It looks good. Something missing are each wing's individual favicon icon. They all have
  one. Feel free to place a marker for each of them and an explanation somewhere in the side panel if you
  deem."* Then: *"Do you think the order should be reversed, so it shows the wing's icons on top first?"* (the
  seat's answer: yes). Then, on the result: *"It's looking good, less plain, more intriguing. I like it."*

**Ruled:** the front door as built (§4), by his "I like it" on the preview. **Not yet ruled:** every THEORY item.

---

## 2. The grammar (adopted from the library, not invented)

| rule | value |
|---|---|
| grid | 16×16, `crispEdges`; no curves, no anti-aliasing, no gradients |
| ground | `#0a0a0a`, the favicons' own; **it travels with the mark into every reading mode** (§6) |
| chrome | `#e8e4dd` |
| lit | exactly one element, library crimson `#ef3a58` |
| vocabulary | nodes (blocks), edges (thin lines), grounds (a long bar underneath), brackets (corners) |
| meaning | how an objection is **built**, never what it is **about** |

Two families on the site:
1. **Library marks** — the seven favicons (front door, flagship, five wings). They name a library.
2. **Tier marks** — the five, drawn by the argue seat. They describe how an objection of that tier is built.
   **Flagship only** (§6, law 8).

---

## 3. One source, and its gate (BUILT)

- **Data.** `icons/sigils.json` is byte for byte argue `ed9286f:design/tier_sigils_v0/sigils.json`
  (md5 `1e7e99bd628e65bb10d246f859eefe64`, 1,715 B), the copy R0108 names. Measured: its five tier grids are
  identical to R0107's `6fb26e1` copy (`b97acd2b`); `ed9286f` only adds the game's HUD grids, unused here.
- **Generator.** `icons/gen_icons.py` still draws the seven favicons, byte-identical (7 of 7). It now also
  refuses any `sigils.json` but the pinned bytes, re-asserts the grids (in bounds, no overlap, one lit), and
  writes the front door's eleven regions: `mini` (the five at 1×), `rows` (each at 2× with its label and the
  sentence of what its shape says, both from `sigils.json`), `plate` (T3 drawn large, three parts named),
  `libs` (the seven library marks with what each shape says: the words after the dash in each favicon's own
  description) and `lib-<name>` ×7 (each library's mark beside its name on the page).
- **Collision law, mechanised.** L1a warned that a ladder with its top rung lit *is* the flagship's favicon.
  The generator now refuses to draw if any two marks, across both families, share a silhouette. Measured on
  the drawn set: no collision; the closest tier-to-favicon pair is T1 and Veganism at IoU 0.36; the closest
  pair of tiers is T2 and T5 at 0.54.
- **Gate.** `tools/icons_regen_check.py` (L1's check, extended) requires the favicons **and** every
  generated region of `site/libraries/index.html` to be byte for byte what the generator draws. The region
  list is whatever the generator draws, and a marker in the page it does not draw is a difference too.
  `--write-marks` splices them in. A refused draw prints its own reason as a RED.
- **Controls.** `controls_marks.py` → `controls_marks_v0_1.json`: **12 of 12 as expected**, the unmutated
  control first; each mutation RED with its own message. C6 draws a tier as the flagship's ladder and is
  refused; C9 proves the splice restores the original page byte for byte; C10 changes a card's mark; C11
  plants a region the generator does not draw. The record
  reproduces byte-identically under two forced hash seeds. It pins the page's md5, so regenerate it after
  any change to the page.

---

## 4. The front-door key (BUILT)

**What a reader sees.**
- **Beside every name.** The page title carries the index's own mark; each library's card carries its mark
  beside the title, the same drawing as the icon in its browser tab. The Adversarial Map has no mark of its
  own (its tab borrows the front door's), so its card has none.
- **The rail.** The "5 tiers" figure carries the five tier marks at actual size. They link to the key.
- **The side panel, "Reading the marks."** One line: two kinds of mark share one grammar, and neither pictures a
  topic. Then **the libraries first** (his note): the seven library marks, each with what its shape says. Then
  **the five tiers**: one line on tiers, the plate (T3 at 15×, its pixel grid showing, `lit` / `edge` / `node`
  labelled) and its caption, the sentence that names all five parts and says where to look, the five rows, and a
  link into the flagship.
- **Where.** At 72rem and wider, a 19rem column beside the libraries. It stays in view while you scroll, but
  **only when it fits the window whole**; at 1,506 px it now fits none of the windows tested. Narrower, it sits
  after the libraries, the two sections side by side on tablets.
- **Motion.** The game's five one-shots, copied: opacity and transform only, no loop. They play once, in
  order (T1 → T5, a quarter-second apart), the first time the tier rows are seen. Hovering a row plays its mark
  again. The rail's marks and the library marks never move. The gate is the house layer's own: **the vfx display tier, a dark
  ground, and motion allowed**. The layer gates its glow and its sound the same way; its comment says why:
  *"one power button should mean one thing."* Reduced motion, a light reading mode, and the cosmetic or off
  tiers are all still.

**Measured (Playwright, Chromium 153 and Firefox 155; `measure_front_door.mjs`, record `measure_front_door_v0_2.json`
for this page; `v0_1` is the record of the first build, shown on 2026-09-25).**

| check | result |
|---|---|
| horizontal overflow, 10 widths (360–1920) × 4 reading modes × 2 engines | **0 of 80** (display tier cosmetic; see §9 for the vfx pan) |
| WCAG AA, all 44 text items in the side panel and rail, every run | **min 5.06:1** |
| the seven marks beside names (title + six cards), every run | **7 of 7** |
| page errors or console errors | **0** |
| motion gate, 6 cases × 2 engines | **12 of 12**: moves only at vfx + dark + motion allowed, the first time the tier rows are seen; stops after; hover replays |
| sticky | the panel is 1,506 px and fits none of 1440×900, 1440×1100, 1920×1080, so it stays put |
| favicons / regions / controls | 7 of 7 · 11 of 11 · 12 of 12 |
| xsurface | GREEN, flagship `006aa983` / 2,987,411 untouched |

**Cost.** `site/libraries/index.html` 21,304 → 43,308 B raw; gzip 6,404 → 10,383 B (+4.0 KB over the wire).
Inline marks are 12,928 B raw of that. No new files are served.

---

## 5. Where the build departs from R0108's recommendation (the seat's calls, each with its reason)

1. **The link goes to `/combined`, not to a tier section.** The flagship has no tier anchor, and its router
   promotes any bare hash to the real-world-examples view: `/combined#tierFilters` lands on `#/rwe/tierFilters`.
2. **Sticky only when it fits.** A sticky column taller than the window hides its own foot. A short check
   decides, on load, resize, font load and reading-mode change.
3. **No separate strip after the intro.** The five marks live in the rail's "5 tiers" cell at every width:
   no added height, and the figure sits beside its marks.
4. **The motion gate is the house's**, not "VFX only" alone (the reason is in §4).
5. **The plate is one real mark, not a specimen.** No single mark holds all five parts, and composing one
   would draw a sixth mark that is not a tier. T3 carries three parts; the key sentence names the other two,
   and T4 and T5 show them.
6. **The ground travels with the mark.** Crimson as R0108 recommended, and the `#0a0a0a` tile in every mode,
   so on a cream page a mark is still the same object as the icon in the tab.
7. **The rows play in sequence**, so the marks assemble one after another rather than all at once.
8. **The T-numbers are not crimson.** One lit element per row: the eye should land on the mark.
9. **Both families in one panel, libraries first** (his note, 2026-09-26). The reader meets the library cards
   first, so the panel explains those marks first; the tier marks are one level deeper, inside the flagship.
   The plate stays with the tiers it belongs to: a wing's mark drawn large would put one topic above the others
   on the front door.

---

## 6. Laws for any library use

R0108 §4's seven laws are adopted as written: structure not subject; beside the words, never instead of
them; one lit element; the register reaches the marks (T4 drawn and animated standing, nothing breaks);
motion teaches once and stops; the legend teaches how to read and never hands over a conclusion; one source.

Added by this lane:

8. **Tier marks are flagship-only.** Measured: none of the four wing corpora, and not the Veganism module,
   carries a tier field. A tier mark on a wing page would claim a structure the wing does not have. This
   corrects R0108 §6.1, which puts them on "every objection header in each library".
9. **No two marks share a silhouette.** Gated in `gen_icons.py`; any new family must pass it before it is
   drawn anywhere.
10. **The ground travels with the mark**, into every reading mode.
11. **Motion follows the house gate**: vfx tier, dark ground, motion allowed.
12. **Generated, never pasted.** A page carries a mark only between a generator's markers, and a gate checks
    it byte for byte.

---

## 7. THEORY: further use across the site (ordered by value to a reader against cost)

1. **Library marks on the front-door cards.** *No pin.* **BUILT 2026-09-26 on his note** (§4). If the
   Adversarial Map is to carry a mark, it needs one drawn: a new mark, his to approve.
2. **Tier marks in the flagship.** *PIN.* On the five tier filter buttons and on every objection's tier
   badge, in the game's form: mark plus "T#", never instead of it. **A ruling it needs:** the lit element in
   the flagship's existing tier colours, or in crimson. **Lean: tier colour in the flagship**, whose tiers are
   already colour-coded, as the game's badges are; crimson on the front door, which speaks the house voice.
3. **A tier anchor in the flagship.** *PIN.* A route such as `#/library/tier-4`, so the front door can link to
   a tier and not only to the page.
4. **The Mechanism Web and Dependency Graph, node shapes by tier.** *PIN.* The site's only imagery and the
   marks become one language; the key's rows become the graphs' legend.
5. **Section dividers from the grammar** (a ground line with one lit node). Static and cheap. The flagship is
   a PIN; the wings are their own files and their own lane's.
6. **Anchor arrival.** *PIN.* A deep link to an objection plays that objection's tier one-shot once.
7. **Wing headers carry their library mark.** No pin; the wings' lane.

---

## 8. THEORY: new families for visual learners (each needs his approval before it is drawn)

1. **Outcome glyphs** — routed (the node leaves along an edge), defanged (it stays and its lit core goes dark),
   met (held in brackets). They teach the dissolve-versus-defeat distinction, which R0108 §7.1 reports argue's
   status doc calling the single best educational payload. **Lean: the first new family.**
2. **Move glyphs — measured, and not ready.** `move_tags` exist only in the four wing corpora: none in the
   flagship, none in Veganism. 326 tags, 212 distinct; the twelve most frequent cover 29%; only three recur
   in two or more wings (`anti-conscription`, `burden-inversion`, `parity`). Three of R0108's five example
   tags (`scope-misfire`, `standard-correction`, `remedy-mismatch`) occur nowhere. A move family needs a
   controlled vocabulary first, and that is corpus work for the library seat, not drawing.
3. **Depth glyphs** (PUNCH / DECONSTRUCT / DISMANTLE). **Collision warning:** R0108 draws them as "the same
   ladder as the flagship favicon's five bars", which is L1a's hazard exactly. The generator would refuse an
   identical silhouette, but a one-, two- and three-rung ladder still reads as the flagship's. **Lean:** draw
   depth as edges cut along one chain, not as rungs.
4. **Mechanism marks, by rule.** Measured as R0108 says: `mechType` rhetorical 12, structural 10, genuine 6,
   defense 5, cognitive 2 (35). Derive the 35 from type and objection count; never hand-draw them.
5. **A "how to read an objection" strip**: build → move → outcome, a mark and a line each, one play in view.
   It waits on families 1 and 2.

---

## 9. Findings, logged and not repaired

- **The house layer overflows by 6 px during its first-visit tour** at the vfx tier, in Chromium only: the
  stage is panned `translate(6px, 3.6px)`. In one run of the instrument, the untouched page did it in 23 of
  24 Chromium cases and this branch in 0 of 24; an earlier run caught 3 on the branch, so it is timing, not
  layout. Firefox: none. `wuld-layer.css/js` are shared and outside this lane.
- **The flagship has no link target for a tier** (§5.1), and any bare hash opens the RWE view.
- **R0108 §6.1** would put tier marks on wing headers; the wings have no tiers (law 8).
- **R0108 §7.2**'s example tags are mostly absent from the corpora (§8.2).
- **The README's `icons/` line** now under-describes `gen_icons.py`. It shares a line with the canon filename
  that L4 bumps tonight, so it is updated at merge, not on this branch.

---

## 10. Where everything is

| file | md5 | what |
|---|---|---|
| `icons/sigils.json` | `1e7e99bd` | the argue grids, vendored byte for byte (`ed9286f`) |
| `icons/gen_icons.py` | `ae22c4c4` | draws both families and the page's 11 regions; refuses unpinned data and shared silhouettes |
| `tools/icons_regen_check.py` | `a3b5ef51` | the gate: 7 favicons + every front-door region; `--write-marks` |
| `site/libraries/index.html` | `8a7f4160` | the front door, with the marks beside every name and the side panel |
| `design/glyph_architecture/controls_marks.py` | `f1e07284` | the 12 mutation controls |
| `design/glyph_architecture/controls_marks_v0_1.json` | `d076176e` | their record (it pins the page md5) |
| `design/glyph_architecture/measure_front_door.mjs` | `7e88e381` | the browser measurement, both engines |
| `design/glyph_architecture/measure_front_door_v0_2.json` | `43d443df` | its record for this page (§4) |
| `design/glyph_architecture/measure_front_door_v0_1.json` | `4eb0b483` | its record for the first build, and §9's pan count |
| this file | — | the architecture, ruled vs THEORY |

Sources outside this repo: argue `ed9286f` `design/tier_sigils_v0/` (`ARCHITECTURE.md` `fa9a1f19`, byte-identical
to R0108's frozen body; `gen_sigils.py`; `sheet.svg/.png`, the sheet he approved).
