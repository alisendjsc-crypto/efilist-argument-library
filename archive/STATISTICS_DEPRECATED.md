# STATISTICS — efilist argument library

Corpus-level numbers, the transition calculus, the dependency and mechanism
topology, the real-world-example distributions, and the RSI scoring model.
**Figures current at v3.8.3 (canon v37.3).**

> **What this file is.** A *documentation* artifact reporting canon-attested
> figures with provenance. The corpus-scale, topology, and Map 1 numbers are read
> from canon's `invariants` block (v37.3). The grade matrix and deployment×grade
> quadrant in §7 are **computed this release** from `rebuttal_grading_ledger`
> (long depth) joined to the corpus `realWorldExamples` — they are no longer
> recompute-at-render references. The in-surface live STATS section specified in
> `corpus_statistics_spec.md` remains a deferred, harness-gated build.

---

## sampling_provenance — read first (structural caveat, not a footnote)

The real-world-example corpus is **diversified but opportunistic**. It was
harvested across five deliberately different surface classes — institutional
writing, lifestyle explainers, student journalism, primary social platforms,
niche forums — to avoid single-channel bias. It is **not a representative sample
of real-world objection frequency.** Every "share" or "deployment" figure below
is internal to the harvested set. A high deployment count means *"this move
shows up a lot in what was collected,"* never *"this is how often the move
occurs in the world."* The denominator for a true real-world rate does not
exist and is not claimed. This caveat governs every number in this document.

---

## 1. Corpus scale

| Dimension | Value | Source |
|---|---|---|
| Objections | **81** | canon `invariants.objection_count` |
| Tiers | **5** | canon `invariants.tier_count` |
| Psychological mechanisms | **35** | canon `invariants.mechanism_count` |
| Total responses | **243** | corpus `totalResponses` |
| Attested real-world deployments | **136** | corpus `len($.realWorldExamples)` |
| RWE → objection attachment edges | **171** | corpus `realWorldExamples[].attached_objections` |
| Interlocutor archetypes | **4** | sophisticate · defender · drifter · blended |
| Dependency-graph nodes | **94** | canon `invariants.dep_graph_data_node_count` |
| Dependency links | **254** | canon `invariants.dep_graph_data_link_count_v361` |
| Mechanism-web nodes | **116** | canon `invariants.map_graph_data_node_count` |
| Mechanism-web links | **140** | canon `invariants.map_graph_data_link_count` |
| Map 1 transition edges | **2,886** | canon `invariants.map1_edge_count_total` |
| Map 1 nodes | **78** | canon `invariants.map1_node_count` |

**The v3.8.0 cut.** v3.7 ran at 78 objections / 34 mechanisms (invariants anchor
`f6b94bf0…`). The **v3.8.0 structural cut** added three objections
(`eliminativism` T4, `solipsism` T4, `suffering-as-meaning` T2) and one mechanism
(`mech_Metaphysical_Deflation`), re-deriving the graphs: dependency 91→94 nodes /
245→254 links, mechanism web 112→116 / 133→140. The invariants subtree mutated
(new anchor `8727787c…`). **Map 1 was held at 78 nodes / 2,886 edges** — the three
new objections are not Map-1-represented, and `MAP1_TRANSITIONS` is byte-identical
across the cut.

---

## 2. Tier taxonomy

| Tier | Name | Register | Population |
|---|---|---|---|
| T1 | Emotional / Reflexive | reflexive, affect-driven, low deliberation | 13 |
| T2 | Folk Philosophical | inherited intuitions, unexamined commonplaces | 17 |
| T3 | Structural / Pragmatic | systems / consequences / feasibility framing | 14 |
| T4 | Genuine Philosophical | engaged, internally coherent, hardest to dismiss | 31 |
| T5 | Meta-Objection | objections to the framework / the project itself | 6 |

Tier is a property of the *objection*. It is orthogonal to dependency-link
strength. Per-tier populations are derived from `objections[].tier` at v3.8.3
(Σ = 81); the v3.8.0 cut placed two new T4 nodes (`eliminativism`, `solipsism`)
and one T2 node (`suffering-as-meaning`).

---

## 3. Map 1 — the transition calculus

Map 1 is a force-directed *next-move predictor*: from a selected source
objection it renders predicted successor objections within the selected
archetype's mode, annotated with convergence tier and mode rationale.

**Edge distribution across the 78 source-keys** (unchanged since v3.7.2 —
topology untouched by the v3.8 score-layer foldins, and the v3.8.0 cut held Map 1
at 78):

| Archetype | Edges |
|---|---|
| sophisticate | 675 |
| defender | 526 |
| drifter | 390 |
| blended | 1,295 |
| **total** | **2,886** |

**Blended mode-count distribution:** `{1: 1,010 · 2: 274 · 3: 11}` (Σ = 1,295).
**Two-mechanism disclosure true-counts:** `defender 5 · drifter 42 · blended 45`.
(Source: canon `invariants.map1_*`.)

Behavioral content lives in each edge's `rationale` (or `mode_rationales` for
blended edges). The map is the artifact; the numbers above are its shape.

---

## 4. Dependency graph

**94 nodes** = 81 objections + **13 premises**. Premise split: **9 foundational +
4 diagnostic** (unchanged across the v3.8.0 cut). **254 links**, partitioned
**167 strong** (load-bearing) / **87 weak** (softer / invoked) — canon
`invariants.dep_graph_data_strong|weak_link_count_post_cluster_insertion`.

Premise families (surface legend): Axiological · Consent · Metaphysical ·
Empirical · Structural · Diagnostic (Psychological) · Diagnostic
(Characterization). The foundational spine includes Consent Impossibility,
Benatar's Asymmetry, the Proxy Gamble, Empirical Tail-Risk, Suffering-as-
Deterrent, Convergent Architecture, Alogical Isness, Contextus Claudit, and the
zero-line premise; the four diagnostic frameworks include Optimism Bias, Labor
Sine Fructu, Terror Management Theory, and Depressive Realism. Per-premise
strong/weak counts: recompute from `premiseDependencyMatrix`.

---

## 5. Mechanism web

**116 nodes** = 35 mechanisms + 81 objections. **140 links** (canon
`invariants.map_graph_data_*`). The v3.8.0 cut added `mech_Metaphysical_Deflation`
(35th mechanism), minted from the `eliminativism` node. Mechanism-type taxonomy
(surface legend): Psychological Defense · Cognitive Bias · Rhetorical Fallacy ·
Structural Deflection · Genuine Engagement. Node size scales by connection count —
load-bearing mechanisms (e.g. Terror Management Theory, Optimism Bias) carry many
objection edges; singletons carry one.

---

## 6. Real-world examples

| Metric | Value | Source / status |
|---|---|---|
| Attested deployments | **136** | corpus `len($.realWorldExamples)` |
| Attachment edges (RWE → objection) | **171** | corpus, computed at v3.8.3 |
| Objections with ≥1 deployment | **78 / 81** | computed — the 3 v3.8.0-cut nodes carry no deployments yet |
| First-commitment instances | **15** | canon invariant |

**Archetype-signal distribution** (unchanged — the RWE corpus did not change in
the v3.8 line): sophisticate 72 · not-applicable 38 · defender 15 · drifter 6 ·
blended 5. The ~28% `not-applicable` share is a **corpus-health signal** — many
harvested deployments do not legibly read as any single archetype — and is
reported, not hidden.

The three objections added in the v3.8.0 cut (`eliminativism`, `solipsism`,
`suffering-as-meaning`) are **catalogued but not yet attested in the wild** — they
carry zero real-world deployments. This is a corpus-honesty signal, not a defect:
they were added on taxonomic grounds, and the harvest has not (yet) caught them in
live discourse.

Each record enforces a **<15-word quotation bound** at the schema level plus
required provenance fields. Schema: `real_world_examples_schema_v1_7.json`
(`spec_version: 1.7`).

---

## 7. Rebuttal strength — the RSI calculus

Responses render at three depths — **PUNCH**, **DECONSTRUCT**, **DISMANTLE** —
each with an in-app `RSI METHODOLOGY` panel.

**The model:**

- Each rebuttal carries a raw 5-axis tuple `REBUTTAL_STRENGTH {v, s, c, r, a}`.
- This raw tuple persists in **`index.html`** (with `combined.html` as its derived
  superset). It is **not** in the corpus JSON or JSX — those are the
  non-score-bearing taxonomic spine by canonized design (2-artifact
  score-layering, canon v28.1).
- `RSI`, the percentage, and the letter grade-band are **derived at render** by
  `computeRSI` → `rsiGrade`, with `depthModifiedRSI` applying the depth modifier.
  The grade bands are **A ≥ 0.88 · B ≥ 0.82 · C ≥ 0.76 · D < 0.76**.

**Grade distribution by tier** (long depth, computed at v3.8.3 from
`rebuttal_grading_ledger` joined to `objections[].tier`):

| Tier | A | B | C | D | Ungraded |
|---|---|---|---|---|---|
| T1 | 9 | 2 | 2 | — | — |
| T2 | 8 | 5 | 4 | — | — |
| T3 | 8 | 6 | — | — | — |
| T4 | 7 | 19 | 5 | — | — |
| T5 | 4 | 2 | — | — | — |
| **Total** | **36** | **34** | **11** | **0** | **0** |

**All 81/81 graded; zero D-band; zero ungraded.** The three v3.8 long-form
strengthens lifted their nodes out of the C floor: `violence-as-reductio`
86.2 B, `negative-util-aggregation` 84.0 B, `joy-outweighs-harms` 83.0 B. The
remaining 11 C-band nodes are all C (none D); the current floor is
`flow-states-csikszentmihalyi` at 78.1 C.

**Deployment × grade — the danger quadrant** (the analytical view the project
most needs: a weak rebuttal that is heavily deployed in the wild):

| Objection | Grade | Deployments |
|---|---|---|
| `violence-as-reductio` | **B** (86.2) | 27 (highest) |
| `benatar-asymmetry-attack` | **B** (82.1) | 15 |
| `ai-fear` | **B** | 10 |
| `why-not-suicide` | **A** | 7 |
| `transhumanist-objection` | C | 5 |
| `life-gift` | C | 4 |

**The danger quadrant is empty at v3.8.3.** No objection with high deployment
(≥ 8 RWE) sits below B-band — the three most-deployed nodes are all B. The C-band
nodes that remain are all low-deployment (≤ 5). This does not foreclose future
re-entry (a new attested deployment shifting a C node into high-RWE territory, or a
cold-regrade reverting a band could re-populate it); it states the current corpus
position.

---

## 8. How the project was built (the discipline)

The library is built under a set of canonized engineering invariants worth
stating, because they explain why the numbers above are trustworthy:

- **2-artifact score-layering (canon v28.1).** The taxonomic spine (corpus + JSX)
  is low-churn and score-free; the high-churn score overlay lives only in
  `index.html` (with `combined.html` as its derived superset). The v3.8 foldins
  exercised exactly this firewall: prose + score changes touched index/combined,
  the corpus/jsx spine carried only the prose.
- **Invariants-anchor versioning.** Every release is classed against the
  `invariants` subtree md5 (`md5(json.dumps(invariants, sort_keys=True,
  ensure_ascii=False))`). v3.7.x held `f6b94bf0…` (PATCH-class); v3.8.0 mutated it
  to `8727787c…` (MINOR — the topology changed); v3.8.1/.2/.3 held `8727787c…`
  byte-identical (PATCH-class).
- **<15-word quotation discipline.** Schema-enforced on every real-world example —
  not a convention, a validation rule (`real_world_examples_schema_v1_7.json`).
- **Compute-at-render, never hand-author.** No derived figure (RSI, share, band)
  is stored as a literal in the shipped artifact. The grade matrix in §7 is
  computed from the ledger for *this document*, not asserted as a frozen render.
- **Validator gate.** `v3prime_validator_v1_7.py --self-test` is green
  (`_overall_pass: true`); the corpus returns `verdict: PASS` (zero blocking
  violations) at v3.8.3.

---

## Provenance & honest limits

Headline counts (81 / 5 / 35 / 243 / 136 / 171 / 94 / 254 / 167-87 / 116 / 140 /
2,886) are read from the canon **invariants** block at **canon v37.3**. The grade
matrix and deployment×grade quadrant (§7) and the attachment-edge / objections-
with-deployments figures (§6) were **computed at v3.8.3** from the live corpus and
`rebuttal_grading_ledger` — they are exact for this release, not recompute-at-
render references. Per-premise dependency splits and any per-edge Map 1 rationale
content remain render-bound; recompute against `premiseDependencyMatrix` and the
`MAP1_TRANSITIONS` literal for those.

The in-surface STATS section (`corpus_statistics_spec.md`) — with live computed
metrics and the interactive danger quadrant — remains a deferred, harness-gated,
terminus-reopening build. It is not this file and is not scheduled.
