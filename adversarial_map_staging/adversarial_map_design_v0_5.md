# Adversarial Objection/Rebuttal Map — Design v0.2
*(v0.1: library seat, 2026-07-11 · answers `adversarial_map_commission_relay_v1.md` · Exchange 151 · DESIGN ONLY.*
*v0.2: wuld.ink Cowork, K345, 2026-09-17 — §9 added, amending §1 and §2 per the LOCI ruling. §0–§8 are v0.1 verbatim;*
*`adversarial_map_design_v0_1.md` stays on disk byte-identical as the record canon pins.)*

## 0. Contract restated in one line
For each of the 82 shipped nodes: the strongest continuation a maximally competent hostile interlocutor deploys **against our v4.0.0 text as written**, triaged into four disposition classes — the fidelity-ceiling mechanism inverted, overshoot promoted from exception to product.

## 1. Artifact schema

Machine skeleton in the sibling `adversarial_map_schema_v0_1.json`. Per entry:

```json
{
  "target_id": "<∈ corpus 6ee1f6f3 id set, n=82>",
  "target_locus": "short|medium|long|diagnosis|archetypeVariants.<slot>",   // <slot>: sophisticate|defender|drifter|blended -- see S9
  "target_anchor": "<≤15-word verbatim quote of the shipped clause the move engages>",
  "adversarial_move": "<40–150 words; the continuation at full strength>",
  "class": "a|b|c|d",
  "grounds": "<why this class; for (b): why the shipped text's best reading does not already meet it>",
  "routing": { "<class-shaped, see §2>" },
  "status": "mapped",
  "provenance": {"phase": "<A|B1|B2|C|D>", "date": "", "seat": ""}
}
```

Map-level meta: source-corpus pin (`6ee1f6f31e0f...` / 82 / tier split 13/17/14/31/7), register-law pointer, per-phase coverage arithmetic, class-count summary.

**Register of `adversarial_move`:** compressed analytic statement, not first-person performance. This is triage infrastructure, not a reader-facing asset; performance register (scholar-style) is a downstream vendoring decision if yields feed the game. Explicit dilemma structure encouraged; rhetoric banned.

**Coverage contract:** every node gets ≥1 entry — a confident (a) or (d) is itself the routing datum. Cap 3 entries/node; the contract is the *strongest* continuation, not all continuations.

> **Amended K345 (§9):** the cap's unit is now the **locus**, not the node — ≤3 per `(target_id, target_locus)`, with a node-level bound of `3 + (variant loci on that node)` so a node without variants keeps the ratified 3 exactly. And `coverage` is now two claims: `coverage` over the primary ladder, `variant_coverage` over `archetypeVariants`. **Read §9 before authoring against this section.**

## 2. Class law (adjudication order: a → c → b/d)

| class | test | routing shape | precedent |
|---|---|---|---|
| **(a) ALREADY-ANSWERED** | the move's best formulation is *met* (not merely addressable) by shipped prose somewhere in-corpus | `{"answered_by": ["node_id#depth", ...]}` | the 81-authoring null yield |
| **(c) NEW-NODE** | not a continuation of this node's dialectic at all — seed-1 individuation grounds: presupposition inversion, reader test, grading-object integrity | `{"intake_candidate": {"proposed_id","tier_guess","mechanism_guess","individuation_grounds"}}` | `self-effacing-under-universalization` |
| **(b) STRENGTHEN** | defeats the shipped prose (gap, equivocation, underpowered analogy) but not the position; a stronger text inside the node's identity meets it | `{"regen_candidate": {"axis_hit": ["c","r",...], "severity": "minor|headline"}}` | `contractualism-scanlon` B→A |
| **(d) HONEST-RESIDUE** | names bedrock — already-registered (solipsism dissolve-not-defeat; asymmetry-contingent amplifiers) or **new** bedrock the sweep surfaces | `{"residue": {"bedrock_name", "terminus_routing", "novel": bool}}` | solipsism |

> **Amended K346 (§10):** the selection criterion is ruled — an entry names the **strongest**
> continuation, not the most repairable — and §10.4 fixes what *strongest* means operationally, which
> is the part that inverts a phase's class distribution when it is left to practice. A fifth
> anti-inflation gate, the **stopping rule**, is added at §10.3. **Read §10 before authoring against
> this section.**

**(c) before (b)** because a move that beats the shipped prose *by being a different objection* is (c), not (b) — exactly the S4 flag's history.

**Anti-inflation gates** (the ceiling's discipline substitute, since the bound is removed):
1. **Anchor rule** — no entry without `target_anchor`; the move must engage a clause we actually shipped, killing mechanism-generic counters. *(K345: "shipped" means rendered to a reader. `archetypeVariants` and `note` render; `objectionSubforms` does not — §9.2, §9.4.)*
2. **Force floor** — `grounds` must state why the shipped text's *best reading* fails; a move met on charitable reading is (a).
3. **(a)-brevity cap** — ≤60 words of move-statement; (a) entries are routing data, not essays.
4. **Regress stop** — one round only: the opponent's next move after *our* answer; no counter-counter chains. Depth-2 dialectic is the card game's job, fed by (a) edges.

## 3. Phasing — recommendation: tier-descending, mechanism-adjacent within phase

| phase | scope | n | seats | expected yield profile |
|---|---|---|---|---|
| **A (pilot)** | T5 | 7 | 0.5–0.7 | calibrates all four classes; the defanged trio (heat-death, meta-ethical-pluralism, particularism) are natural (d) exemplars; routed quartet stress-tests (a)/(b) boundary |
| **B1 / B2** | T4 | 31 | 1 + 1 (15/16 split) | the (b)/(c) core — where the sophisticated counters live |
| **C** | T3 + T2 | 31 | 1–1.5 | shifts toward (a) routing data — game material; cheaper per node |
| **D** | T1 | 13 | 0.5 (fold into C's second seat if budget holds) | near-pure (a); fast |

**Total: 4–5 authoring seats** + per-phase Cowork micro-folds + one terminal assembly fold.

**Why not mechanism-clustered as primary axis:** clustering generates counters against the *mechanism class*, diluting the against-OUR-text contract — the anchor rule exists precisely because that drift is the failure mode. Mechanism adjacency survives as *secondary ordering within phases*: shared-structure counters (one flawed move reused across nodes) get caught and cross-referenced without becoming the unit of analysis. Tier-descending front-loads the intake-relevant discoveries and matches the scholar program's demonstrated density gradient.

**Pilot-first** per program precedent (S1 → S4). Phase A additionally carries the parked **Map-1 curation elective for node 82** as a rider — the pilot reads that node's full dialectic anyway; marginal cost near zero. DEP_GRAPH inert-counter strip stays parked, unbundled.

## 4. Staging home
`adversarial_map_staging/` at repo root — **version-neutral** deliberately: (b)/(c) yields route to whichever future bundled cut ratifies them (v4.1/v5 scoping is downstream); naming the dir by target version would presume the target. Contents: `adv_map_phase{A|B1|B2|C|D}_v0_1.json` fragments + terminal `adversarial_map_v1_0.json` assembly. Map is LIBRARY-INTERNAL: no deploy, no combined/ledger/index bytes, until a deliberate fold decision.

## 5. Status lifecycle for (b)/(c) yields
`mapped → queued (Josiah triage) → ratified → landed(version) | rejected(grounds)`. The map records `mapped` only; everything downstream lives in canon agenda + the normal staging → cold-grade → assembly chain. No entry authorizes a byte.

## 6. Cowork owes per fold
- **Per phase:** collect fragment → validator run → md5/byte pin → coordination-doc exchange log → git commit. **First fold only:** canon MINOR adding the `adversarial_map` block (keyset delta logged).
- **Terminal:** assembly build (fragments partition the 82, id-preferring dedupe — scholar pattern), class-count summary into canon, extraction of the (b)/(c) queue as a v-cut scoping input, (d)-novel items appended to the honest-residuals register.
- **Never:** corpus/ledger/index/combined touches from this program.

**Validator spec** (`adv_map_validator_v0_1.py`, Cowork implements — mechanical): target_id ∈ 82 ∧ id×anchor unique; per-phase union arithmetic → 82/82 at terminal; class ∈ {a,b,c,d} with class-shaped routing (schema in the JSON sibling); anchor ≤15 words ∧ verbatim-in-corpus check (substring against the target node's shipped text — the anchor rule made programmatic); move band 40–150; status enum; serialization round-trip.

## 7. Open questions (Josiah)
1. Cap 3 entries/node — ratify or amend?
2. Phase-A rider (Map-1 curation of node 82) — elect now or keep parked?
3. Terminal artifact name `adversarial_map_v1_0.json` — or reserve `v1_0` for post-triage state?

## 8. Sequencing executed this seat
R1 + R2 authored and assembled first (warm-up claim honored — re-entering ceiling discipline before designing its inversion): `scholar-objections_v1_1.json` (82/82, md5 `20999eb9`) + micro-fragment delta. Design above is the hand-back; Phase A opens on ratification.

---

## 9. The LOCI ruling (K345, 2026-09-17) — amends §1 and §2

`adversarial_map_design_v0_1.md` stays on disk byte-identical; canon pins it and the Phase A–E
receipts cite it. This section is the amendment, and it exists because the alternative was a third
arc of silence (`ccclxi`).

### 9.1 What was wrong

The validator's `LOCI` enum was `("short","medium","long","diagnosis")`. `responses.archetypeVariants`
is not in it, so `target_locus` could not name a variant and `anchor-rule` could not reach one.
**`coverage: 82/82 nodes, 93 entries` was true of what the map could see, and silent about the rest.**
Nothing ever failed, because nothing ever looked.

### 9.2 What was measured before the ruling

Against the post-cut corpus `04bf6482aa0374ee92a81c1d55ec41f8`:

| class of text | rendered? | nodes | units | words |
|---|---|---|---|---|
| the four primary loci | yes | 82 | 328 | 67,427 |
| `responses.archetypeVariants` | **yes** — per-card archetype toggle (v3.8 D5); the selected slot also substitutes for the response level on copy | 16 | 39 | 10,069 |
| `note` | **yes** — toggle, `responseLevel === 'long'` only | 9 | 9 | 544 |
| `objectionSubforms` | **no** — data only, no render site on either surface | 1 | 4 | 646 |

Variant slots: `sophisticate` 13, `defender` 12, `drifter` 7, `blended` 7. By tier: T1 7, T2 2, T3 4,
T4 2, T5 1 — concentrated in T1, which is where Phase E worked and found nothing there because it
could not look.

### 9.3 The case that archetype variants are "just register" was tested and it is false

The defensible version of leaving the enum alone was that variants are register re-castings of an
already-adjudicated response, so adjudicating the response adjudicates them. **Measured, with controls:**
content-token novelty of each variant against its own node's four primary loci, compared against a
known register-compression of the same content and against unrelated text.

| | n | median novelty |
|---|---|---|
| CONTROL, floor — `short` vs `medium`+`long`+`diagnosis` (a known compression of the same content) | 16 | **0.293** |
| CONTROL, floor — `medium` vs `long`+`diagnosis` | 16 | **0.498** |
| **TREATMENT — each variant vs its own node's four loci** | **39** | **0.591** |
| CONTROL, ceiling — each variant vs an *unrelated* node's four loci | 39 | **0.855** |

Variants sit above both register-compression floors and well below the unrelated ceiling: not
paraphrase, not unrelated — **adjacent new argument on the same target**, which is what the map exists
to triage. The textual evidence agrees and is less arguable than the arithmetic: **27 of 39 variants
name another slot explicitly and hand work to it** — *"The defender slot handled the actor; this slot
handles the framework"*; *"it is the sophisticate's question, answered in that slot, not this one"*.
The slots partition the dialectical labour. They do not restate one another.

> **Amended K348 (§11.3):** the node-level entry bound in item 2 below is superseded. It is now
> `3 + 3×(variant loci on that node)` — the per-locus cap applied to variants as it already is to
> primaries — because the one-slot-per-locus form contradicts anti-inflation gate 5 wherever a
> variant locus legitimately opens. A node with no variants is unchanged at 3. **Read §11.3 before
> using the bound in item 2.**

### 9.4 The ruling

**EXTEND.** Josiah, K345.

1. **`target_locus` grammar.** A locus is either one of the four primaries, unchanged, or the dotted
   form `archetypeVariants.<slot>` with `<slot>` in `{sophisticate, defender, drifter, blended}`. A
   variant locus is valid only where that slot exists on that node. `answered_by` refs take the same
   grammar, for the same reason: an enum that extends while its routing target stays narrower is the
   original defect one step over.
2. **The entry cap moves from the node to the locus.** `<=3` entries per `(target_id, target_locus)`,
   because the locus is the unit the anchor engages. A second, node-level bound holds at
   `3 + (variant loci on that node)`, so **a node carrying no variants keeps the ratified bound of 3
   exactly** and the gate extends in proportion to the text rather than being loosened flat. This
   amends a Q1-ratified gate; Josiah delegated the form of the amendment at K345.
3. **`coverage` is now two claims, and both are stated.** `coverage: 82/82` continues to mean the
   primary ladder. `variant_coverage: <hit>/<total>` is reported on every run and gated whenever a
   fragment declares it. Completion is **not** forced by the gate, because Phase F is owed and a
   successor map has to be able to exist before it lands. A map that cannot say what it has not done
   is how `82/82` became misleading in the first place.
4. **`note` is IN SCOPE and unadjudicated.** 9 nodes, 544 words, rendered. It is editorial apparatus
   rather than rebuttal prose, and at least one instance (`care-ethics`) is a published concession
   that the node's own response is underpowered. That is an attack surface of an unusual kind. It is
   **not** added to the enum here, because its shape is not a response and the anchor rule assumes one.
   Named as owed, with grounds, rather than left silent.
5. **`objectionSubforms` is OUT OF SCOPE, on measured grounds.** 1 node, 646 words, and **no render
   site on either shipped surface** — grep finds exactly one occurrence in `combined.html` and one in
   the JSX, and both are the data key. The map's contract is the strongest continuation against text
   we shipped *to a reader*. Unrendered data is not that. If it is ever surfaced, this line is the
   record that its scope was decided rather than overlooked.

### 9.5 Phase F, opened

39 variant loci across 16 nodes. Tier-descending within the phase, as §3. The frozen
`adversarial_map_v1_0.json` is **not re-run and not re-pinned**; it gains a scope note in canon saying
what its coverage claim covered. Its bytes do not move.


---

## 10. The ccclxv ruling, the stopping rule, and what "strongest" means operationally (K346, 2026-09-18) — amends §2

`adversarial_map_design_v0_2.md` stays on disk byte-identical; canon pins it and the Phase R receipt
cites it. This section is the amendment, on the same terms §9 was.

### 10.1 The ruling

**STRONGEST.** Phase F and every phase after it author the strongest continuation a maximally
competent hostile interlocutor deploys against our text as written, exactly as §0 says. The
most-repairable-defect reading is **rejected**. Josiah + the library seat, K346; reversible by Josiah.

### 10.2 The finding that prompted the ruling does not survive its own null, and that is recorded rather than quietly dropped

WI-K336 registered `ccclxv` on the claim that phases A–E practised *repairable* while §0 asks for
*strongest*. Its evidence was that three of Phase R's four anchors land on clauses the v4.1.0 cut
never touched. **That overlap was published without a null.** The four re-adjudicated loci had
changed-word fractions summing to 0.2264, so under uniform anchor placement the *expected*
number of Phase R anchors landing in cut-touched text is 0.2264 of 4. Observed:
1 of 4. Cut-touched text is **over**-represented, not walked past. This is `ccclxvi`
committed one section away from where `ccclxvi` was registered.

Two further tests, both against the frozen `adversarial_map_v1_0.json`:

- If authors kept going while repairable material lasted, multi-entry nodes should be (b)-enriched.
  (b) share is **0.1053 in multi-entry nodes against 0.2568 in single-entry nodes** —
  depleted. Permutation null against the enrichment direction, N=20000: **p = 0.9657**.
- The (b)-heaviness belongs to Phase R's repair brief, not to A–E: v1_0's (b) share is **0.2258**,
  Phase R's is **0.75**.
- Move length by class runs (d) **119** > (b) **103** > (a) **51** median words. The
  longest, most-developed moves are the bedrock ones, which is the signature of strongest-first
  authoring.

The practised criterion was not *repairable*. `ccclxv` stands as a hazard about gates being silent,
and its worked example is struck.

### 10.3 What was actually unwritten: the stopping rule, not the selection criterion

A–E authored **1.1341 entries per node against a cap of 3**, with `long` taking 77 of
93 anchors. Nothing written says when a locus is *done*. That is `ccclxi`'s shape with evidence, and
it is the real gap the ccclxv finding was reaching for.

> **Amended K348 (§11):** `open` ⇔ ≥2 entries is a **biconditional** — a locus carrying two entries
> cannot declare itself closed (§11.2) — and §10.4's inheritance principle runs in three directions,
> not one (§11.1). **Read §11 before authoring against this section.**

**Anti-inflation gate 5 — the stopping rule.** Author the strongest continuation and adjudicate it.
Then answer one question and record the answer: *is there a second continuation at this locus that
engages a different clause and would not be met by the same reply?* If yes, author it, to the cap. If
no, the locus is closed and the fragment declares it closed. The stop becomes an auditable claim
rather than a silence. Declared per-locus in fragment meta, gated when declared, on the pattern §9.4.3
set for `variant_coverage`. The gate itself is owed at validator v0_4.

### 10.4 ccclxviii — an operationalisation can satisfy every written gate and still invert the result

K346 ruled §10.1 and then operationalised "strongest" as *strongest against what this locus uniquely
says*. For a register variant that filter selects against (a) **by construction**, because what a
variant uniquely says is precisely the part its primary ladder does not already answer. The resulting
defect register returned (b) on all 39 entries. Against the A–E base rate for (a)-or-(d) of
**0.7634**, drawing zero is a **1.62e-24** event. A seeded, sorted-pool sample of four loci
re-adjudicated under the plain reading flips **3 of 4** to (a).

**The rule.** *Strongest* means strongest against the text as a reader meets it — the whole locus,
including everything it inherits from its node — never strongest against the locus's distinctive
content. For a variant the strongest continuation is usually the one its primary ladder already
answers, and that (a) is the routing datum the map exists to produce. Phase R found exactly this at
n=1 and said not to generalise; the generalisation that mattered was the opposite one.

And the detection rule, which is the transferable part: **a class distribution that departs from its
own base rate is an instrument reading before it is a finding.** Compute the phase's class mix
against the prior before writing a receipt over it.

### 10.5 Archetype weighting for Phase F: author evenly across loci — ruled, not defaulted

Observed `archetype_signal_observed` runs sophisticate **0.7347** over **98**
applicable real-world instances, against a near-even authored distribution. Effort is **not** weighted
to it. Measured grounds:

- The signal is venue-bound. Sophisticate share by `public_reach`: niche or pseudonymous
  **0.417**, high-reach intellectual **0.929**, named specialist **1.0**.
  Register heterogeneity, permutation p = **0.0**.
- The frame is concentrated and scholarly by design: **62** distinct publications over
  98 instances.
- §0 is a **competence** contract ("a maximally competent hostile interlocutor"). Frequency is a
  different axis, and importing it would be `ccclxv`'s substitution in a new place.
- Defect density runs opposite to deployment: the drifter and blended variants are the shortest and
  least-attended text in the feature, and a map hunting for weakness should not spend its budget where
  the corpus was most careful.

One entry per locus is the floor; further entries are allocated by §10.3's stopping rule, never by
slot frequency.

### 10.6 The archetype signal is a collection-frame diagnostic, and the frame has two lanes (Josiah, K346)

The `realWorldExamples` panel was built for **notable** sources — citable, archive-backed, attestable —
which is the right build for its first two purposes: defeating the straw-man charge, and cataloguing
the scope and depth of the subject. Notable sources select for sophisticates, because people writing
for publication perform competence. **The mundane everyday-interaction lane is wanted and simply has
not been collected.** It is not excluded from the programme; it is the lane the prediction aim needs,
and it is where the defender, drifter and blended archetypes actually live.

So the panel's archetype mix is lane one's mix, and the venue measurement above is a description of
lane one rather than of deployment. This adds to the K345b collection spec: a **second lane**, with its
own schema, where volume and thread structure carry the weight and byline attestation carries less, and
whose purpose is the archetype and prediction layers rather than citability.


---

## 11. Inheritance cuts three ways, the stopping rule as a biconditional, and the entry-cap ruling (K348, 2026-09-17) — amends §9 and §10

`adversarial_map_design_v0_3.md` stays on disk byte-identical; canon pins it at `design_pin_v0_3`
and the Phase F receipt cites it. This section is the amendment, on the same terms §§9 and 10 were.

### 11.1 Inheritance cuts BOTH ways — and the honest count is three

§10.4 states one direction: the whole-node reading CURES a locus-local defect, because the strongest
continuation against a variant is usually the one its primary ladder already answers. Phase F bears
that out at scale — **20 of its 26 (a) entries are answered by a locus of the variant's OWN
node**, which is inheritance curing, measured rather than asserted. `next-person-cure-cancer#archetypeVariants.sophisticate`
is the clean worked example: the variant aims a deprivation argument past its target, the node's
`#long` frames the same refusal on consent, and the move is met.

**It also AGGRAVATES, and §10.4 does not say so.** Two of Phase F's 6 (b) entries exist only
because of what the locus inherits:

- `just-depressed#archetypeVariants.sophisticate` disavows depressive realism while the node's
  `#short` and `#medium` assert it as evidence. The sophisticate text is **correct standing alone**
  and is made false-in-context by its own node.
- `violence-as-reductio#archetypeVariants.drifter` asserts an incompatibility between caring about
  suffering and causing harm that the node's own `#long` surrenders when it concedes the bridge is
  held by founders.

**And the third way is the one neither direction names: inheritance can simply FAIL to cure.** The
remaining (b) entries are locus-local defects that survive the whole-node reading — the node has no
answer to supply, or supplies one the locus contradicts. `bitter-childhood#archetypeVariants.defender`
is the shape: no locus in the corpus meets the move, because the corpus's own rule condemns it.

**The rule.** Read the whole node before classing a variant, and record WHICH of the three the node
did — cured, aggravated, or failed to cure. A grounds field that says only "not locus-local" has not
said which, and the difference decides the class: cured is (a), aggravated is (b) and the repair is
at the NODE rather than at the locus, failed-to-cure is (b) and the repair is at the locus. Counted
across Phase F: **20 cured, 2 aggravated**, the rest failed to cure.

### 11.2 Anti-inflation gate 5 is a BICONDITIONAL, and §10.3 reads one-directional

§10.3 states the stopping rule as a question to answer and record: *is there a second continuation at
this locus that engages a different clause and would not be met by the same reply?* The prose reads
as though only an `open` declaration carries an obligation. It does not.

**`open` ⇔ ≥2 entries.** The declaration records the ANSWER to that question, so a locus
carrying two entries has answered *yes* and cannot also declare itself closed, exactly as a locus
carrying one and declaring `open` has not discharged the claim it made. The first cut of the gate at
validator v0_4 asserted only the forward direction, and a mutation declaring the open locus `closed`
did not trip it — **a failing control convicted the gate's author**, which is the whole reason the
control exists.

The minimal mechanisation of *engages a different clause*: two entries at one locus may not have one
anchor a substring of the other. Measured across the successor assembly, **0 same-clause
pairs over 7 multi-entry loci**, so the sub-check is confirmatory rather than a repair,
and it is scoped inside the declaration so no frozen receipt can be disturbed by it.

### 11.3 The node entry cap scales by the per-locus cap, not by one slot per locus (Josiah, K348)

§9.4 item 2 set a second, node-level bound at `3 + (variant loci on that node)`. That was written
when **no variant entry existed anywhere**, and it reserved a single slot per variant locus while the
per-locus cap allows 3. So the node bound and gate 5 disagree BY CONSTRUCTION wherever a variant
locus legitimately opens: §11.2 says author the second continuation, and the node bound refuses to
hold it.

`red-button-repugnant` is where the disagreement surfaced. It carries 6 entries in the
successor assembly — three inherited from the frozen v1_0 and three from Phase F, 2 of them at
one variant locus gate 5 declared open — against a §9.4 bound of 5. Every one is legal
per-locus and the node is illegal per-node.

**THE RULING (Josiah, K348).** The node bound becomes `3 + 3×(variant loci on that node)`:
the per-locus cap applied to variants exactly as it already applies to primaries. **A node carrying
no variants still keeps the Q1-ratified bound of 3 exactly**, which is the property the §9.4
amendment was written to preserve and this one preserves untouched.

The alternative on the table was dropping one of the 6 on the merits, in the assembly only. It
was declined: the bound and gate 5 are in structural disagreement, and dropping a sound entry to
satisfy an arithmetic fixed before the thing it now constrains existed repairs the symptom.

Blast radius, measured across the assembly's 133 entries over 82 nodes: **1 node
violates the old bound and 0 violate the new one**. The heaviest node in the corpus carries
6 entries and the heaviest locus carries 3, so the amendment buys headroom where
gate 5 needs it and nowhere else. Implemented at validator v0_5, whose self-test runs 62 cases
against v0_4's 60, and which reproduces every v0_4 verdict across 72 runs over every
shipped artifact and both corpora with 0 divergences.

### 11.4 The partition invariant belongs to the LOCUS too, and that was invisible until a fragment set crossed it

v1_0's builder refused to write unless the fragments PARTITIONED the corpus: no node claimed by two
phases. That invariant is sound for phases A–E, which carve the 82 nodes between them. Phase F
authors variant loci on nodes A–E already cover, so at the successor assembly's fragment set the
node-level form fails **16 ways by construction** — while the property it was actually
protecting, that no two phases adjudicate the same text, is perfectly intact: **0 loci
are claimed by two phases**.

This is the same unit migration §9.4 made for the entry cap, one layer over, and it has the same
cause: an invariant written when the locus did not exist as a unit states itself over the node
because the node was the only unit there was. The general form is worth carrying: **when a ruling
moves a gate's unit, every OTHER invariant stated over the old unit is a candidate for the same move,
and nothing fails until a fragment set finally crosses it.** The successor assembly states the
migrated invariant in its own meta, with the 16 nodes listed, so the next reader meets the
fact rather than rediscovering it.

### 11.5 What the successor assembly is

`adversarial_map_v1_1.json`: 133 entries covering all 82 nodes at the primary ladder and
all 39 of 39 archetypeVariants loci, classes 66a / 27b / 1c / 39d,
pinned to the post-cut corpus. 90 entries are inherited from v1_0 unchanged and 3 are superseded by
Phase R because the v4.1.0 cut destroyed their anchors. It is a **revision**, not a re-mapping, which
is why it is v1_1: the schema is unchanged and no inherited entry is re-classed.

Class mix against the A–E base rate of 0.7634, per §10.4's detection rule: the union runs
0.7895 (two-sided p = 0.5408) and the disjoint R+F set runs 0.7907 (p = 0.8575). Both sit
inside the prior. **The union figure is reported and does not carry weight**: the union CONTAINS the
base, so testing it against a rate computed from its own subset is not an independent test. Saying
which of two figures is the real one is part of the gate.

## 12. The `note` layer, the reachability finding, and the fifth relation kind (K349, 2026-09-17) — amends §9, §10 and §11

`adversarial_map_design_v0_4.md` stays on disk byte-identical; canon pins it at `design_pin_v0_4`
and the v1_2 receipt cites it. This section is the amendment, on the terms §§10 and 11 were.

### 12.1 `note` is a map target, NARROWLY (Josiah, K349 — delegated to the build seat)

K345 named `note` IN SCOPE and never discharged its own reservation: the shape is not a
response and the anchor rule assumes one. The reservation was real and the disposition was put
to Josiah with the classification already measured, because a scope question deserves the
`ccclxviii` discipline as much as a class distribution does — decide what the population looks
like before deciding what to do with it.

Of the 9 notes, **3 are authoring apparatus** — sibling taxonomy, build-pass
provenance (*"first taxonomically committed in session 4h-alt … across 6 source-vehicles in
build-pass batches 1 and 3"*), a ratification-delta line (*"inclusion bumps the ratified delta
78->80 to 78->81"*), and a TIER NOTE addressed to a future editor. **1 is a legitimate
scope qualifier**, checked against its own `#long` rather than assumed. The remaining
**5 carry a claim or a concession the corpus would have to defend**, and those are
Phase G.

**The ruling is NARROW because the class law does not survive the other 4.**
"The strongest continuation a maximally competent hostile interlocutor deploys against our text"
is malformed against a build-accounting line. Authoring against all 9 would have
produced 9 entries and four of them would have been inflation, which is the `82/82`
problem in a new artifact — and the kickoff named that risk in advance. `note_coverage` is
therefore **5/9**, declared and deliberately partial: a phase that cannot say what it has
not done is how a coverage claim becomes misleading.

Josiah delegated 0a to this seat rather than ruling it. That is recorded as a delegation, not as
a ruling, because the difference matters to whoever reads this next.

### 12.2 THE FINDING: `note` is not an independent field. It is a dependent of `confidence`.

`combined.html` emits the `[NOTE]` button INSIDE `if (conf !== 'full')`, where
`conf = obj.confidence || 'full'`, and `toggleNote` has exactly one caller — that button. So a
note on a node graded `full`, or ungraded, has its `<div>` emitted at `display:none` with
nothing in the artifact able to reveal it.

**2 of the 9 notes are structurally unreachable by any reader: 195
of 544 words, 35.8% of the layer.** They are the two longest. One of them is
`solipsism`, whose note is the text that *explains* its `confidence:full` — and that value is
exactly what suppresses the button that would let anyone read the explanation.

So the CSS class name `confidence-note` was never the misnomer; the FIELD name `note` is. The
layer is architecturally a confidence disclosure, which is also why 6 of the
9 note-bearing nodes already carry a (d) in the successor assembly against
35 of 82 corpus-wide — the corpus puts a note where it knows it is on hard ground.

### 12.3 `confidence` is OUT as a map target and IN as a regen candidate (Josiah, K349)

It carries no corpus text, so the anchor rule has nothing to bite on and it cannot be a map
entry. It is ruled explicitly rather than by silence, and on different grounds from
`objectionSubforms`, which K345 ruled out for having **no render site at all**. `confidence` has
one, and the handoff's premise that "no text reaches the reader" is false: the badge emits the
literal strings STRONG and PROVISIONAL for 7 nodes.

What is filed instead is a regen candidate with three legs, each measured:

1. `full` renders **identically to absent**. 11 nodes were affirmatively graded `full`
   and 64 were never graded, and a reader cannot tell them apart.
2. `provisional` renders as a 70% opacity band on the long response with **no label**,
   which a reader cannot interpret and a screen reader cannot convey at all.
3. The grade silently controls whether a node's note is reachable — §12.2. A field documented
   nowhere as a visibility control is one.

### 12.4 Apparatus cannot satisfy coverage (K349 ruling, made explicitly)

`coverage` keyed on `target_id` alone, so a node whose only entry sat at `#note` would have
counted as covered. `coverage` is the claim that every node's ARGUMENT was adjudicated, and a
note is apparatus attached to a node, not the node's argument. It is now restricted to argued
loci in the validator, and stated POSITIVELY in the assembly builder — v1_1 computed primary
coverage as "not a variant locus", which a new locus kind walks straight into.

That is `ccclxxi` a second time in three sessions, and it was found by READING the builder rather
than trusting that the K348 migration had covered it. **Measured blast radius: zero.** No shipped
artifact carries a note entry, so no verdict moves; what changes is what the NEXT phase can claim.

### 12.5 The fifth relation kind: `conditions` (Josiah, K349)

> **A conditions B**: A's resolution changes the FORCE of B's open question without creating or
> dissolving it. B stays askable either way; what moves is how much turns on the answer.

HR-14+HR-11 is its first instance and the reason it was ratified: K348 recorded that pair in the
register's AUDIT rather than declaring it, because none of `depends_on / stronger_than /
sibling_of / independent_of` states it. The register is rebuilt at v0_3 with the relation
declared — and with the vocabulary made an **enforced allowlist** rather than the five-line
comment it had been.

The same pass found that `build_register.py`'s own comment claims *"the audit below refuses to
write if any mechanically-derived adjacency candidate is undeclared."* It did not. It appended an
audit line and wrote anyway. The claim was true by luck — the undeclared set has always been
empty — and it is a gate now. That is `cccli` in its purest form, and one more instance of it
discharged.

### 12.6 `ccclxxii` — A RENDER SITE IS NOT REACHABILITY, AND THE DIFFERENCE IS DATA-DEPENDENT

Two scope audits have now asked *does this field have a render site?* and treated the answer as
settling whether readers meet the text. K345 ruled `objectionSubforms` OUT because it has none.
This session came within one ruling of treating `note` as uniformly rendered because it has one.

**A render site can be nested inside a condition on a DIFFERENT field, so whether text reaches a
reader is a fact about the DATA, not about the code.** The predicate was being evaluated
statically when it is data-dependent, and the error is silent in both directions: it over-counts
a field whose gate is usually closed and under-counts one whose gate is usually open.

The rule: to establish that shipped text reaches a reader, find the render site, **enumerate every
condition gating it, and evaluate those conditions over the actual corpus** — then report the
count, not the existence. `ccclviii`'s family (measure the state you think you measured), narrowed
to the specific case where the instrument is a static read of a dynamic predicate.

### 12.7 What was run

Validator v0_6, self-test **78/78** against v0_5's 62, and v0_6
reproduces **every** v0_5 verdict across **66 runs** over the shipped artifacts, both
corpora and all three modes, with **0 divergences**. `adversarial_map_v1_2.json` carries
138 entries against v1_1's 133, 82/82 primary, 39/39 variant, 5/9
note, and passes `--assembly` at 0 violations and 0 advisories. Phase G's class mix is
3(a)/2(b) — a+d 3/5 = 0.6 against the A–E prior of 0.7634,
exact two-sided p = 0.3389; zero (d) against a prior of 0.3441, p = 0.1722.

**Both p-values are stated with their power, because at n=5 the gate is nearly
unfalsifiable and saying it passed without saying that would be the flattery version of a
control.** The structural reason for zero (d) is measured rather than argued: 6 of
the 5 authored nodes already carry a (d) at a primary locus on the very bedrock a note
entry would route to, so a second one would restate a registered residue rather than route a new
one. Entry-cap headroom on every note-bearing node was checked before authoring — minimum
2 — so the node bound was NOT extended and no ruling was owed.

**46 controls across three batteries, all passing**: 23 on Phase G and the patch,
16 on the assembly, 7 on the register. Two of them had to be repaired before they
earned the name — one displayed a violation it had not matched on, and one refused for the
harness's reason rather than the guard's.
