# Changelog

All notable changes to the efilist argument library.

Versioning follows a PATCH/MINOR/MAJOR convention keyed on the **invariants subtree** (canon `invariants` block, anchor `f6b94bf0cb3e6832dbdde0017b876e54`):

- **PATCH** — invariants subtree byte-identical to the prior MINOR; content-advance + score-layer + prose re-cuts only. The structural taxonomy is unchanged.
- **MINOR** — invariants subtree mutated (counts shift, edges added, premises re-cut); corpus topology changes.
- **MAJOR** — schema-class break (RWE schema bump, score model re-architecture, surface-router redesign).

Per-release artifact integrity is canon-anchored in `archive_attestation.release_artifact_md5_set_per_release_manifest_*`. Headline counts cited here are read from canon `invariants` and cross-verified against the per-release manifests.

---

## [v3.7.5] — 2026-05-29

**PATCH.** `masochist-counterexample` suicide-coda excision (publish-gate ruling). Invariants subtree byte-identical to the v3.7 line (anchor `e1bf216e268dbcd0bc9fe7904537b82c`); corpus taxonomic content unchanged at 78 objections.

### Changed

- **`masochist-counterexample.responses.long`** — an unsourced editorial coda asserting a named forum participant's death by suicide was **excised** (single-line, length-only edit; −244 B per surface). Publish-gate ruling: the death claim did not clear the corpus's real-person sourcing bar (WHO / secondary-reporting standard) and carried public-surface sensitivity exposure. Node grade unchanged — **C** (RSI ≈80.0); the coda was non-axis-bearing.
- Propagated to all four surfaces: `efilist_argument_library_v3_7_5.json` (corpus, `04b2b6bf16de921f7ab8a7449b393f1a`), `combined.html` (`d8393d3b40bcabf3eceb993fc3e31cdc`), `index_v3_7_5.html` (`556bc1a39d0f5a5919bcaf14f3cdf4f4`), `efilist_argument_library_v3_7_5.jsx` (`da464f2713a29f2c5b3b2d51411996ef`). Mega-literals (`MAP1_TRANSITIONS`, `DEP_GRAPH_DATA`) byte-identical; all 78 nodes deep-equal corpus; coda residue 0.

### Attestation

- Validator `v3prime_validator_v1_6` PASS (rc 0; 136 records). Invariants subtree byte-identical `e1bf216e268dbcd0bc9fe7904537b82c` (G5 pre==post).
- Canon MAJOR bump v35.1 → v36.0 on published-contract md5-set revision; `release_artifact_md5_set_per_release_manifest_v3_7_5` + `harness_green_attestation_v3_7_5` ADDED. Project terminal state `archived_v3_7_4_stable` → `archived_v3_7_5_stable`.
- Project version classifier: **PATCH-class v3.7.5** (invariants unchanged); NOT v3.8.

---

## [v3.7.4] — 2026-05-29

**PATCH.** `masochist-counterexample` long-form strengthen + surface propagation. Invariants subtree byte-identical to the v3.7 line; corpus taxonomic content unchanged at 78 objections.

### Changed

- **`masochist-counterexample`** strengthened across all three response depths (`responses.short` / `medium` / `long`) plus `psychMechanism`; `sources` expanded 7 → 8. Single-node, style-preserving propagation to `combined.html`, the JSX sibling, and the index surface.
- Corpus advanced to `efilist_argument_library_v3_7_4.json` (`fc1a45a140c5b03339eecfd4f57bc97c`).

### Attestation

- Validator PASS; invariants subtree byte-identical `e1bf216e268dbcd0bc9fe7904537b82c`. Canon MAJOR bumps v33.4 → v34.0 (corpus/combined/jsx) → v35.0 (index divergent-carry resolved). Project terminal state → `archived_v3_7_4_stable`.
- **Note:** v3.7.4 was canon-attested but **staged-never-pushed** to this public repo (the repo remained at v3.7.3); it is superseded by v3.7.5 and published together here.
- Project version classifier: **PATCH-class v3.7.4**; NOT v3.8.

---

## [v3.7.3] — 2026-05-23

**PATCH.** `benatar-asymmetry-attack` long-form strengthen + ledger sync re-cut. Invariants subtree byte-identical to v3.7-stable (anchor `f6b94bf0cb3e6832dbdde0017b876e54`); corpus taxonomic content unchanged at 78 objections.

### Changed

- **`benatar-asymmetry-attack.responses.long`** strengthened from 4904ch single-paragraph to 8205ch four-paragraph treatment. Ledger axes re-cut to `{v0.88, s0.81, c0.80, r0.78, a0.84}`. `long.rsi_pct` 78.3 → 82.13; `long.grade` **C → B**; `headline_grade_long` C → B. Short/medium forms held verbatim per v28.2 cold-grade convention (presentation byte-identical → prior snapshot retained).
- **Danger quadrant** (deployment × grade): with `benatar-asymmetry-attack` regrade, the second-highest-deployment node clears the weak-rebuttal alarm. The corpus's two highest-deployment objections (`violence-as-reductio` cleared at v3.7.2, `benatar-asymmetry-attack` cleared here) are now both B-band. No nodes remain in the danger quadrant; the analytical view that originally motivated the score axis is empty at v3.7.3.
- **`combined.html`** re-synced to v3.7.3 corpus (md5 `29f9d5c0d4befac52dae4ca88ea4211f`, size 2,243,165). The v3.7.2-era combined.html (md5 `2accf16a...`, size 2,236,312) is superseded; the prior coherence-note flag on benatar long-form para-1-only divergence is now closed.
- **`rebuttal_grading_ledger.json`** refreshed for benatar axes overwrite (md5 `9b0b291fe4818587e3d724a7d6daf017`, size 29,874).

### Added

- **`rwe.html`** — fourth view-tab artifact (stats view, sampling-provenance disclosure). Shipped here as a sidecar; not yet wired into the in-app outer hash router. Operator-elective `_redirects` shortcut to `/rwe.html` is a separate decision.
- **`v3_7_cut_invariants.json`** — terminal-cut invariants snapshot for downstream verification and citation.
- **`corpus_statistics_spec.md`** — methodology spec for `STATISTICS.md` numbers + deferred in-surface STATS section.
- **`sort_feature_spec.md`** — documentation of the sort/filter UI scoping.

### Unchanged (carried v3.7.2-verified)

- `coda_v3_7.html` (md5 `654f56cf...`, 11,040 B)
- `v3prime_validator_v1_6.py` (md5 `f114d87c...`, 21,816 B)
- `real_world_examples_schema_v1_6.json` (md5 `a5011ddb...`, 80,253 B)

### Attestation

- Harness `invariant_derivation_harness_v1` GREEN (exit 0; `derived == canon == manifest`).
- Surface-mutation hard gates 9/9 PASS (S2 atomic batch, single-script pattern).
- S3 canon MAJOR bump v29.0 → v30.0 on `archive_attestation` public-contract revision; `release_artifact_md5_set_per_release_manifest_v3_7_3` ADDED (8 artifacts).
- Project terminal state: `archived_v3_7_2_stable` → `archived_v3_7_3_stable`.
- Project version classifier: **PATCH-class v3.7.3** (mirrors v28.4→v29.0 MAJOR-canon / PATCH-project pattern); NOT v3.8.

### Per-file integrity contract (canon `release_artifact_md5_set_per_release_manifest_v3_7_3`)

| Artifact | File | md5 | Size |
|---|---|---|---|
| corpus JSON | `efilist_argument_library_v3_7_3.json` | `af2befa16e7e23b6c73104e529d5f653` | 1,169,378 |
| JSX | `efilist_argument_library_v3_7_3.jsx` | `2f25960ad66bf9539a79a3e6dcc6d73a` | 1,115,535 |
| index HTML | `index_v3_7_3.html` | `eb73fb6f456ce43d9cf44e2be264f55d` | 1,696,684 |
| single-file | `combined.html` | `29f9d5c0d4befac52dae4ca88ea4211f` | 2,243,165 |
| coda | `coda_v3_7.html` | `654f56cf29d9a808fc870dda4c98b3cc` | 11,040 |
| validator | `v3prime_validator_v1_6.py` | `f114d87c46a05891ac0077854200f000` | 21,816 |
| RWE schema | `real_world_examples_schema_v1_6.json` | `a5011ddba98cd98c5afc9c28cdc79752` | 80,253 |
| grading ledger | `rebuttal_grading_ledger.json` | `9b0b291fe4818587e3d724a7d6daf017` | 29,874 |

---

## [v3.7.2] — 2026-05-17

**PATCH.** Content-advance re-cut + publication reconciliation. Structural invariants byte-identical to v3.7 line; corpus taxonomic content unchanged at 78 objections.

### Changed

- **`violence-as-reductio.responses.long`** strengthened (11,795 chars). Regraded **C(≈0.805) → B(≈0.838)**. The corpus's single most-deployed objection (27 RWE) cleared the danger quadrant.
- **`benatar-asymmetry-attack.responses.long`** strengthened (4904 chars). Blind re-grade moved C78.3 → C80.7 — materially harder to a hostile reader but band unchanged and quadrant not cleared at v3.7.2. (Cleared at v3.7.3.)
- **Rendered-counter chrome** in `DEPENDENCY GRAPH` and `MECHANISM WEB` headers corrected from pre-sweep `74 objections / 222 dependencies` to canon-attested `78 objections / 245 dependencies` (length-preserving, byte-neutral).
- **Pre-cut ledger sync** brought `rebuttal_grading_ledger.json` fully consistent. Four formerly-ungraded nodes (`violence-as-reductio`, `masochist-counterexample`, `joy-outweighs-harms`, `wild-animal-suffering-consistency`) entered `/grades`. Ungraded count: 4 → 0. All 78/78 graded corpus-wide.

### Attestation

- Harness GREEN; project terminal state `archived_v3_7_1_stable` → `archived_v3_7_2_stable`. Canon line: v29.0.

---

## [v3.7.1] — 2026-05-14

**PATCH.** Two changes — both non-topology-affecting:

### Attestation correction (canon-side bookkeeping)

The v3.7-stable canon attestation of `map1_node_count = 77` was defective against the v3.7-stable shipped literal, which had carried 78 nodes from initial publication. The v27.0 invariant snapshot re-certified the attestation to **78**, matching the shipped count. **Invariants subtree bytes unchanged** — the literal was correct all along; this was a canon-side bookkeeping fix, not a topology change. This is why v3.7.1 is PATCH-class (per the legend at the top of this file) and not MINOR.

### Single-file packaging (new artifact)

Single-file `combined.html` shipped (md5 `dd2abd01...`, 2,234,272 B) absorbing library + RWE + coda behind the outer hash router. First combined-file deliverable in the project; the prior v3.7.0 nested-folder publication plan was superseded. Public tag `v3.7.1` (Branch A).

---

## [v3.7-stable] — initial publication

**MINOR.** Authoritative corpus published: **78 objections** / 5 tiers / 34 mechanisms / 13 premises (9 foundational + 4 diagnostic) / 91 dependency-graph nodes / 245 dependency links (161 strong / 84 weak) / 112 mechanism-web nodes / 133 mechanism-web links / 2,886 Map 1 transition edges / 136 attested real-world deployments. RWE schema v1.6. Validator v1.6 (`v3prime_validator_v1_6.py`, 13/13 PASS).

> **Bookkeeping footnote.** The canon attestation at v3.7-stable publication time incorrectly claimed `map1_node_count = 77` against a shipped literal that already carried 78. The attestation was re-certified to 78 in v3.7.1 (PATCH). The corpus has carried 78 from initial publication; the 77→78 entry in v3.7.1 reflects the canon's record of the count, not a change to the corpus itself. Project history prior to v3.7-stable saw the corpus grow incrementally through the mid-70s on its way to 78; that history sits below the v3.7 release floor and is not detailed here.

---

## Provenance

This changelog is constructed verbatim from canon v33.0's `archive_attestation.attestation_summary` plus per-release `release_artifact_md5_set_per_release_manifest_v3_7_*` blocks and harness-green attestations. Where summaries cite specific axis tuples, RSI percentages, or md5/byte deltas, those numbers are canon-attested at the release moment they describe; later releases may carry refinements to the same fields.
