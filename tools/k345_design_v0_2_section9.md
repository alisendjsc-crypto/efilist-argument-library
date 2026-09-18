
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
