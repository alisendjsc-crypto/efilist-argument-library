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
