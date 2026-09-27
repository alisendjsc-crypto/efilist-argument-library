# V0: variations of objections and rebuttals (design v0_1)

**Seat l, V0, 2026-09-26. Drafted, then ruled the same evening (§11).** Built on R0194 (LD3's kickoff) and R0197 (its addendum:
his go, and his words on new objections). Worktree branch `design/variations`, cut from efilist `70d224c`.
No corpus, canon or served byte moved. **Every count below** comes from `measure_variations.py`, which
writes `measure_variations_v0_1.json` (byte-identical under three hash seeds; `--check` recomputes).
`check_design_counts.py` gates each count in this text against that record.

*Amended the same evening, before any ruling, after argue's R0203 answered §6's questions. The changes:
§3 (the register a shape is written in; scoring), F3 and §6 (argue's answers; which archetype slots are in
flux).*

---

## 0. Recommendation

1. **The game can go deeper now, with no library work.** In each register it shows one fixed line per
   objection (82), and the right card is always the objection's own card. The game carries, or can
   vendor, much more that it never shows: 277 trigger phrasings, 47 real-world quote-objection pairs
   that fit exactly, 39 archetype answers (embedded, read 0 times), and 50 wing objections. That work is
   argue's (§6).
2. **The strongest replay lever already exists: the adversarial map is the flagship's retreat lattice.**
   Its 29 (a) entries push an objection further and route it to where the library answers it (20 of their
   40 targets are another objection's card). Its 76 (d) entries end at named bedrock. The game's ROUTE THE
   RETREAT drill plays exactly this shape, today on anthropocentrism's 12 edges. **Lean: yes, after the
   successor map, on his word.** It changes L1a's "public to read, never promoted" (R-V5).
3. **The library authors argument shapes first, as ruled, but the schema has to be built.** The field
   R0194 counted on records how *defenders refuse* one objection. It does not hold the objection's other
   shapes (F1). A shape ships only where the library already answers it, and it names the answering
   sentence. Pilot: 6 nodes, about 18 shapes, about 1,620 words (§5).
4. **New objections come through an intake that runs after the pilot is judged.** It is triaged by the
   map's own class law. Most finds will be shapes of existing objections, not new nodes (§7).

---

## 1. What the measurement changed

R0194's figures, re-measured on v4.1.4 (corpus `f3d88311`), all hold:
- 82 objections, 3 depths on every node;
- 3.38 phrasings and 9.13 keywords per node;
- archetype variants on 16 nodes, 39 slots (sophisticate 13, defender 12, drifter 7, blended 7);
- one `objectionSubforms` node carrying 4 units;
- 136 real-world instances over 78 nodes;
- 2,886 Map 1 edges.

One reading of those figures does not hold (F1). The other findings are new.

- **F1. `objectionSubforms` is the defender's side, not the objector's.**
  - All 4 of its definitions open *"Position-holder..."*.
  - Its 4 anchors are refutation-of-deployment instances.
  - The RWE schema's key for it reads "canonical refutational variant".
  - It was `refutationalVariants` until the v3.8 rename, which was ratified on 2026-05-29 as "an
    attack-decomposition / objection sub-form layer ... NOT an archetype variant".
  - It is not rendered: the string occurs once in `combined.html` and once in the JSX, and both times it
    is only the data key.

  So "schema exists, 1 of 82" does not hold for what R0194 described, *"the same objection, a different
  argument shape"*. That kind has no schema. **Cost:** one build session (V1), plus a render inside a pin.
- **F2. What goes stale is 82 fixed pairs.**
  - PLAIN, the default, shows `layman_trigger`; SCHOLAR shows the scholar line. Each is one line per node.
  - The card faces are fixed lines too.
  - `play()` scores a pick right only when the card's id equals the objection's.

  New wording for the same pair delays memorising it; it does not prevent it. A variation that lasts
  changes *which card is right*, or *whether any card is*.
- **F3. The game holds variation it never shows.** See recommendation 1. The embed keeps `responses`
  whole, so all 39 archetype answers are in the page, and the code reads them 0 times. But 9 of the 16
  nodes that carry them are in flux, and 5 slots are named by pending repairs. One of those,
  red-button-repugnant's sophisticate slot, is inside L6's safety pass right now (§6).
- **F4. Attested shapes are thin wherever the text is stable.**
  - Real-world deployments that do not fit the trigger exactly: 54 attachments over 33 nodes.
  - 28 of those sit on the 13 nodes whose text is in flux (named by X-032/033/034 or PF-01..07).
  - Of the 69 stable nodes, only `meaning-through-suffering` has two.

  So pilot shapes will be sourced mostly from published work, with real-world instances where they exist.
- **F5. A routing that names only a locus is too weak to ship.** All 40 of the map's (a) routing targets
  name a locus, never a sentence. R1 failed 46 of its 69 (a) entries. A shape's routing makes the same
  kind of claim, so it names the answering sentence (at most 15 words, verbatim). That also lets a reader
  see where the answer is.
- **F6. A game-only layer written by the library already exists.** The scholar layer (82 lines, 9,152
  words) is canon-pinned as a "GAME-side asset, NOT a library line", and no map reads it. Shapes should not
  follow that model: a shape makes a claim about the library's own text.

---

## 2. The kinds, named for what they vary

| kind | the same objection, a different... | side | in the data | in the game | next |
|---|---|---|---|---|---|
| Surfaces | wording | objector | 277 phrasings; 82 layman; 82 scholar; 47 exact-fit quote pairs | 82 per register | argue, now |
| Voices | interlocutor | answer | `archetypeVariants`: 16 nodes, 39 | embedded, never read | argue, now |
| **Shapes** | **argument** | objector | **none** | none | **V1 to V4; the first kind the library authors** |
| Rejoinders | the push that follows the answer | objector | map v1_6: 29 (a), 76 (d) | anthropocentrism only (12 edges) | his word, after the successor map |
| Refusals | the defender's answer | answer | `objectionSubforms`: 1 node, 4 | not embedded | leave as is; grows only with evidence |
| New objections | (a new node) | objector | map (c): 1, `diagnosis-not-refutation` | none | intake, after the pilot |

Shapes and rejoinders need the same change in the game: a prompt whose right card is **another**
objection's card. One engine change serves both.

---

## 3. The shape schema (V1 builds it)

`argumentShapes` is a list at the top level of a node, beside `objectionSubforms`. It does **not** go
under `responses`: the game embeds `responses` whole, so a key placed there would ride into `/argue/` at
the next re-vendor without the argue seat choosing to take it.

```
{
  "shape_id":    "<node-id>/<slug>",
  "label":       "<3-6 words>",
  "statement":   "<the objection in this shape, in the objector's voice; 30-70 words; ASCII; no dash tokens>",
  "differs_by":  "<one sentence: the premise or move that makes this a different argument>",
  "attested_by": ["<rwe instance_id>" or {"citation": "<author, title, year, locator>"}],
  "answered_by": [{"locus": "<node-id>#<short|medium|long|archetypeVariants.slot>",
                   "anchor": "<at most 15 words, verbatim at that locus>"}],
  "provenance":  {"phase": "<new letter>", "date": "YYYY-MM-DD", "seat": "..."}
}
```

The 30-70 word band sits between the layman lines (49-71 words) and the scholar lines (96-120). It is long
enough to carry an argument and short enough to deal as a prompt.

- **One register per shape.** The game shows the layman line in PLAIN and the scholar line in SCHOLAR, and
  the corpus trigger only as a fallback (R0203). So a shape's `statement` is written plain, and the game
  shows it in both registers. A scholar form would be a later, optional field, like the scholar layer.
- **No new grading.** An (a) shape is answered by text the ledger already grades, so the game scores it at
  the answering (id, depth) cell. The grade-the-argument drill keeps to each node's own objection, because
  RSI was graded against that objection and not against the shape.

**Triage is the map's class law, unchanged (a, then c, then b/d):**
- **(a)** the library already answers the shape. It ships.
- **(b)** the library answers it badly. It goes to the regen queue, not the corpus.
- **(d)** it ends at bedrock. It becomes a map entry, shown on `/adversarial/`.
- **(c)** it is not this objection at all. It goes to the intake.

**The corpus carries (a) shapes only.** The game therefore never deals a shape the library cannot answer.
What the library cannot answer stays where he ruled it lives: in the public map.

---

## 4. How the map, the validators and gate2 cover a shape

What anything must carry to be judged, read from validator v0_6:
- a locus the validator can name: `short`, `medium`, `long`, `diagnosis`, plus `archetypeVariants.<slot>`
  and `note`, existence-gated;
- an anchor of at most 15 words, verbatim at that locus;
- a render site that readers actually reach (K345; `ccclxxii`);
- a word band (moves 40-150; class (a) at most 60);
- entry caps (3 per locus; a node's cap is 3 + 3 x its variant loci);
- a PHASES letter;
- coverage declared per file.

Shapes are fitted to that:
- **A shape validator (new, V1).** It sits beside the map validator and imports its locus functions, so
  the anchor rule is the same code. It checks:
  - ids resolve;
  - every `answered_by` locus exists (existence-gated);
  - every anchor is verbatim and at most 15 words;
  - the statement's band and ASCII;
  - every `attested_by` instance exists and is attached to this node;
  - at most 3 shapes per node in the pilot;
  - `shape_coverage` is declared per file.
- **The map validator's successor.** `argumentShapes.<shape_id>` becomes an existence-gated locus, as
  archetype variants became one at K345. The adversarial read can then test each shipped statement for
  strength: a shape stated weaker than people actually make it is a straw man, and so a (b) against our
  own text. The node cap extends to cover shape loci, and PHASES gains a letter.
- **gate2, for each shape** (K258: never the seat that drafted it):
  - The routing HOLDS or FAILS, by R1's method: read every (b) and (d) at the answering locus and at its
    siblings, and run the collision list.
  - The statement is the strongest form of that shape (K346).
  - The shape differs from the node's trigger, layman line and scholar line. If it does not, it is a
    surface, not a shape.
  - The source really makes the move (the quote check).
- **The render (a pin).** Each flagship card gets a closed disclosure, "Other shapes (n)". Each shape
  links to its answering card with the anchored sentence marked. The design lane draws it. Whether readers
  reach it is measured on the data, not the code (`ccclxxii`).
- **Safety.** His 2026-09-25 bar binds every shape, and the game's Article 1 binds every card. The pilot
  stays off the suicide and violence nodes, which are in flux anyway.

---

## 5. The pilot

**The rule, applied by the script:**
1. Drop the 13 nodes that a pending pin-queue finding names.
2. For each tier, take the stable node that the three Next Move characters reach most often (Map 1
   in-degree).
3. Add the stable node with the most attested non-exact deployments.

| node | tier | why | Map 1 in-degree | attested non-exact | what it tests |
|---|---|---|---|---|---|
| `life-gift` | 1 | top of T1 | 60 | 0 | the opener players meet first; 5 strong premises to split shapes on |
| `joy-outweighs-harms` | 2 | top of T2 and of the game | 109 | 0 | the node the game deals most; 7 strong premises, tied for the most |
| `future-solve` | 3 | top of T3 | 28 | 0 | a pragmatic objection; carries a sophisticate slot, so a routing can land on a variant locus |
| `free-will-defense` | 4 | top of T4 | 46 | 0 | a theistic, technical shape set |
| `meta-ethical-pluralism` | 5 | top of T5 | 44 | 1 (Harris) | a meta-objection |
| `meaning-through-suffering` | 4 | most attested | 36 | 2 (Peterson) | the real-world path: shapes seeded from instances |

About 3 shapes per node, so about 18 in all. The pilot measures four things:
- **the share of shapes whose right card is another objection's.** The map's prior is 20 of 40;
- **the FAILS rate,** against R1's 46 of 69;
- **words per shape;**
- **the bar for "a different shape".**

`masochist-counterexample` is the second-most-reached node (in-degree 106). The one-per-tier rule leaves
it out, so it opens the scale-up.

---

## 6. What the game can do now (argue's call, no library work)

1. **Opening lines.** The 277 trigger phrasings run 1 to 17 words (mean 4.6). They are cue-length, not
   prompt-length, so they fit as the opponent's opening words in front of the PLAIN or SCHOLAR line, or
   in a fast round.
2. **"Heard in the wild."** There are 47 quote-and-node pairs, over 30 nodes, where a real deployment fits
   its objection exactly.
   - They need `realWorldExamples` in a new data block.
   - Across all 136 instances, 1 quote is verbatim-verified and 4 are speaker-attributed but unverified.
     The rest carry no status. Show the library's attribution and source, and never the word "verified".
   - The non-exact attachments are shapes, not surfaces. They belong to §3.
3. **Voice-matched answers.** When the opponent is the sophisticate, the defender or the drifter and the
   node has that slot, the reveal shows it: 16 nodes, 39 texts, already embedded. Argue ranks this first
   (R0203). **Caveat, measured:**
   - Only 7 of the 16 nodes are stable (13 slots). The other 9 carry 26 slots.
   - Pending repairs name 5 slots: red-button-repugnant's sophisticate (X-032, L6's safety pass, now);
     ai-fear's defender, both of slippery-slope-eugenics' slots, and bitter-childhood's defender (X-033,
     the next pin).
   - **Lean:** show the 7 stable nodes' slots first. Hold red-button-repugnant's sophisticate slot until the
     v4.1.5 re-vendor: on screen today it would show the framing the safety pass is cutting.
4. **The advanced sets.** 50 wing objections: right-to-die 17, transgenderism 12, veganism 8, abortion 7,
   anthropocentrism 6. They open in Article 10's order.

Already in use, so not listed above: the three depths (the reveal, and grade-the-argument) and Map 1
(Next Move, and Call the Next Move).

**Argue answered before it was asked (R0203, measured at game `c5b60e6`):**
- The embed keeps `id, tier, category, trigger, keywords, responses, diagnosis`. A new corpus key needs a
  line in KEEP, plus gates.
- Each card answers exactly one objection. Scoring is by (id, depth) ledger cell. Map 1's edges are by id.
- Tier drives the badge, the decoys (one never-asked card per tier in the hand) and the register exits.
- Argue agrees that the library authors the variations and the game re-vendors them.

**Still open for argue's build, when shapes or rejoinders reach it:**
- the engine change for a prompt whose right card is another objection's;
- the hand must hold that card, which can sit in another tier;
- a shape keeps its own node's tier and its place in the Map 1 walk;
- how often each node is dealt over argue's seeded walks, to check the in-degree proxy §5 uses.

---

## 7. The new-objection intake

His words, verbatim (R0197): *"For the deferred "new objections"--I'm always open and curious to see
what's out there I haven't heard before. So far I've heard almost every objection in the library before.
The academic objections are a little more particular, but there are also a lot of academics who've made
similar calls I believe and don't have much to add--though--there's always new material coming out."*

- **Scope (K345a):** scholarly and published work, including new material from 2024 to 2026. No mining of
  social media.
- **Screen before anything counts as new:**
  1. Find the nearest of the 82 by trigger, keywords, layman line, scholar line and diagnosis.
  2. Then read it.
- **Triage by the map's class law:**
  - Most finds are shapes of existing objections, and go to §3.
  - A (c) must name its individuation grounds (presupposition inversion, reader test, grading-object
    integrity). It then joins `diagnosis-not-refutation` in the v5.0.0 intake.
- **What he gets:** a short reading sheet of what he has not heard, each with its source. Not a bulk list.
- **The session:** its own, with fan-out ON, because it is many independent reads. It runs after gate2
  judges the pilot, so the novelty bar is set on about 18 shapes before a sweep produces hundreds.

---

## 8. Costs

| step | who | sessions | words |
|---|---|---|---|
| V1: the schema and the shape validator (new files only) | l | 1 | none |
| the map validator's shape locus | rides the successor map's validator bump (R0194's sequence) | 0 extra | none |
| V2: pilot draft, 6 nodes | l | 1 | ~1,620 |
| V3: judge | gate2 | 1 | none |
| his word, then V4: the pin and the render | l + design lane | 1 | none |
| the game build | argue | 1-2 | none |
| the intake sweep | l, fan-out | 1 | a reading sheet |
| the full corpus: 246 shapes | l, then gate2 | ~8 + ~8 | ~22,140 |

For scale: the archetype variants run to 10,242 words and the scholar layer to 9,152. The pin (V4) waits
its turn behind L6's v4.1.5 and the successor map's pin. V1 and V2 touch no served byte, so they can run
at any time.

---

## 9. Rulings (his), with leans

- **R-V1.** Build `argumentShapes` as a new key, and leave `objectionSubforms` as ratified.
  *Lean: yes.* A rename would touch served text and the RWE schema's key, and no reader gains from it.
- **R-V2.** Ship only (a) shapes. Send (b), (d) and (c) to the regen queue, the map and the intake.
  *Lean: yes.* The game never deals a shape the library cannot answer, and what the library cannot answer
  stays public in the map.
- **R-V3.** Shapes render on the flagship card (a pin), and the game re-vendors them from the corpus.
  *Lean: yes.* A game-only layer repeats the scholar precedent, which no map reads.
- **R-V4.** The pilot is the six nodes in §5. *Lean: as listed.*
- **R-V5.** The game may play the map's retreats in ROUTE THE RETREAT. *Lean: yes, after the successor map
  lands, (a) entries first.* The (d) entries are the "where our answers stop" question argue has already
  put to him, so this is one ruling, and it is his alone because it changes L1a.
- **R-V6.** The intake runs after the pilot is judged, over scholarly work including 2024 to 2026.
  *Lean: yes.*

---

## 10. Record

- **Pins, all in the measurement record:**
  - efilist: corpus `f3d88311`, JSX `518c62f4`, `combined.html` `ed040cad`, layman index `7a1f0881`,
    Map 1 `1b059c49`, map v1_6 `7a69bc9f`, validator v0_6 `c002e938`, R1 rulings `d829437e`;
  - game: commit `a801c556`, `inject_data.py` `a740d363`, `index.html` `c3dc6fc4`, scholar v1.1
    `20999eb9`.
- **The game was read through `git show` at that commit, never its working tree.** A live argue session
  holds uncommitted edits there.
- **V0 wrote only under `design/variations/`,** in its own worktree beside L6.

---

## 11. His ruling (2026-09-26)

His words, verbatim, in the V0 session: *"Go with your leans on all of the rulings."*

That adopts §9 as leaned:
- **R-V1.** `argumentShapes` is a new top-level key. `objectionSubforms` stays as ratified.
- **R-V2.** The corpus carries (a) shapes only. (b) goes to the regen queue, (d) to the map, (c) to the
  intake.
- **R-V3.** Shapes render on the flagship card in a pin. The game re-vendors them from the corpus.
- **R-V4.** The pilot is `life-gift`, `joy-outweighs-harms`, `future-solve`, `free-will-defense`,
  `meta-ethical-pluralism` and `meaning-through-suffering`.
- **R-V5.** The game may play the map's retreats in ROUTE THE RETREAT, after the successor map lands,
  (a) entries first. The (d) entries fall under the same ruling. For the game, this changes L1a's "public
  to read, never promoted".
- **R-V6.** The intake runs after the pilot is judged, over scholarly and published work including 2024
  to 2026.

**Not ruled by this word:** §6's lean on voice-matched answers (show the 7 stable nodes' slots first; hold
red-button-repugnant's sophisticate slot until the v4.1.5 re-vendor). That option is argue's to put to
him. The lean goes to argue as the library's.

**What follows, in order:**
1. The canon records R-V1 to R-V6, and R-V5's change to L1a, at its next bump. L6 holds the canon now;
   the record is relayed to seat l.
2. V1 builds the schema and the shape validator (new files only). The map validator's shape locus rides
   the successor map's bump.
3. V2: l drafts the pilot. V3: gate2 judges it. Then his word. V4: the pin and the render, after L6's
   v4.1.5 and the successor map's pin.
4. The intake, after V3.
5. Argue: the "now" list is theirs to build; the map's retreats come after the successor map.
