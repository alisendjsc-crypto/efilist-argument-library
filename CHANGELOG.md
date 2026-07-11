# Changelog

All notable changes to the efilist argument library.

Versioning follows a PATCH/MINOR/MAJOR convention keyed on the **invariants subtree** (canon `invariants` block):

- **PATCH** — invariants subtree byte-identical to the prior release; content-advance + score-layer + prose re-cuts only. The structural taxonomy is unchanged.
- **MINOR** — invariants subtree mutated (counts shift, edges added, premises re-cut); corpus topology changes.
- **MAJOR** — schema-class break (RWE schema bump, score model re-architecture, surface-router redesign).

**Invariants anchor.** The v3.7 line ran on anchor `f6b94bf0cb3e6832dbdde0017b876e54` (subtree byte-identical across v3.7-stable → v3.7.3, which is why those were PATCH-class). **v3.8.0 mutated the subtree** — the new anchor is `8727787c5c0d4f8a08280b806db6fcc8` (method: `md5(json.dumps(invariants, sort_keys=True, ensure_ascii=False))`), held byte-identical across v3.8.0 → v3.8.3.

Per-release artifact integrity is canon-anchored in `archive_attestation.release_artifact_md5_set_per_release_manifest_*` and the `archive_attestation.v3_8_*` blocks. Headline counts are read from canon `invariants` (canon v37.3) and cross-verified against the corpus.

---

## [v4.0.0] — 2026-07-11

**MINOR** by the invariants convention (invariants subtree mutated — the first corpus-topology change since the v3.8.0 cut), released as the **v4.0.0 content cut**. Invariants anchor `c18693f413066e1916eb6281a376d2db` → `f5347636b5becaf25e4759b620090118` (the v3.8.0-era anchor predates the v3.9.12 graph-invariant resync; both prior states preserved in canon history).

### Added

- **`self-effacing-under-universalization`** — objection #82, Tier 5 / Meta-Objection, the Kantian universalizability charge ("even if true, 'do not procreate' cannot be universal law"). Full three-depth response triple, library-authored and cold-graded (long **89.8 A**, medium 88.1 A, short 86.0 B; unrounded means banded per the ratified convention). Mechanism web: **Category Error** (primary) + **Formal Logic Attack** — adjudicated EXISTING, mechanism #36 mint rejected; `mechanism_count` holds at 35. Dependency graph: one weak `benatars-asymmetry` link (the residue routes to the asymmetry cluster). Reciprocal disambiguation folded onto `self-defeating` (keywords + diagnosis pointer; the memetic and deontic forms now fence each other off explicitly).
- **Plain-language card** for the new objection (ROUTED register) and a per-node `register` field on all seven Tier-5 layman entries, per the ratified T5 register-dispositions sidecar — promoted this release from `v4_staging/` to the repo root as a durable canon call.
- **`layman_index_validator_v0_4.py`** — register-keyed T5 gate (defanged inherits the T4 hard defeat-vocabulary gate; routed exempt; unclassified register-tier nodes fail). `--warn-tiers` retires.

### Changed

- **`contractualism-scanlon`** responses regenerated wholesale against the strongest modern ex-ante / hypothetical-consent form (Frick engine, Kumar type-standpoint, the proxy-consent analogy battery). Identity fields byte-locked; sources gain Frick, Kumar, and the Reibetanz/Otsuka ex-post critiques. Ledger row superseded under regeneration discipline: headline **B → A** (long 90.6 A / medium 88.9 A / short 86.8 B). The plain-language card is re-mirrored to the regenerated short (the K202 reveal no longer serves a stale mirror).
- Counts across all four surfaces: corpus **81 → 82** objections (tier split 13/17/14/31/**7**, 246 responses), mechanism web **116 → 117** nodes / **140 → 142** links, dependency graph **94 → 95** nodes / **254 → 255** links (167 strong / 88 weak), grading ledger 82 rows, objections-index + flagship layman index 82 entries (layman `schema_version` → `layman_index_v0_3`, `source_index_pin` rotated).
- `combined.html` **v3.9.16 → v4.0.0** (`6dfeb5d4`/2,955,840 → `e654eabd32fa95e5969d49e6eb15aa87`/2,963,752). Canon **v37.40 → v38.0** (MAJOR: invariant block revised). Corpus/JSX filenames minted at `_v4_0_0`, v3_8_0 pair archived.

---

## [v3.8.3] — 2026-05-30

**PATCH** over v3.8.0. `joy-outweighs-harms` long-form strengthen + the batched index/combined surface-parity reconciliation. Invariants subtree byte-identical (anchor `8727787c…`); corpus taxonomic content unchanged at 81 objections.

### Changed

- **`joy-outweighs-harms.responses.long`** re-authored 3,184 → 8,159 chars. The old soundness floor was an etiology-masquerading-as-axiology equivocation (suffering-as-deterrent wielded against a commensurability claim); the new architecture concedes the hedonic scale and a net-positive aggregate, then wins on the **separateness of persons / the unit-switch** — "outweighs" is true of the ensemble and false as a justification to the one who bears the bad. Ledger axes → `{v0.87, s0.83, c0.83, r0.82, a0.80}`. `long.rsi_pct` **76.6 → 83.0**; `long.grade` **C → B**; `headline_grade_long` C → B.
- **Derive-at-render lift (VAR/masochist posture).** This node stores only the long tuple; medium/short are derived at render. The long lift therefore re-derives the displayed shorter tiers: **medium 75.0 D → 81.3 C, short 72.8 D → 79.2 C** — every tier rises, both shorter tiers cross D→C, and the short/medium **prose is byte-identical** (no authoring).
- **`combined.html`** `REBUTTAL_STRENGTH['joy-outweighs-harms']` base axes → `{v0.87, s0.83, c0.83, r0.82, a0.80}` (renders long 83.0 B / medium 81.3 C / short 79.2 C via `depthModifiedRSI`).
- **`rebuttal_grading_ledger`** refreshed for the joy axes overwrite + `depths_note`.

### Changed — batched index surface-parity (the deferred MINOR, executed here)

The index score layer had lagged the ledger since the v3.8.1/.2 foldins (a deliberate accumulate-then-batch deferral). All three were reconciled in one pass:

- **`violence-as-reductio`** index `REBUTTAL_STRENGTH` `{v0.86,s0.82,c0.84,r0.84,a0.83}` (83.8) → `{v0.87,s0.85,c0.87,r0.86,a0.86}` (**86.2 B**) — matches ledger/combined.
- **`negative-util-aggregation`** index `{v0.85,s0.80,c0.85,r0.75,a0.75}` (79.9) → `{v0.86,s0.83,c0.86,r0.82,a0.83}` (**84.0 B**).
- **`joy-outweighs-harms`** index → `{v0.87,s0.83,c0.83,r0.82,a0.80}` (**83.0 B**).
- After this pass, **index == combined == ledger** for all three nodes. No fourth node touched.

### Attestation

- Canon **v37.2 → v37.3 MINOR** (additive `archive_attestation.v3_8_3`; invariants subtree byte-identical, anchor `8727787c…` held pre==post; 81/35/5 unchanged).
- Gates **G1–G6 PASS** (long md5 `7d2ac7b2…` in corpus/jsx/index/combined; short/medium byte-stable; combined renders 83.0/81.3/79.2; index `REBUTTAL_STRENGTH` == ledger for the 3; corpus/jsx/combined parse clean @81; canon v37.3 MINOR). Validator **v1.7 self-test green** (exit 0, `_overall_pass: true`); **corpus `verdict: PASS`** (zero blocking violations).
- Project version classifier: **PATCH-class v3.8.3** (invariants byte-identical to v3.8.0).

### Per-file integrity contract (current working set)

| Artifact | File (local frozen base) | md5 | Size |
|---|---|---|---|
| single-file | `combined.html` ← `combined_v3_8_0.html` | `dbbbc6d1b993b20064ad0a6d9f27b051` | 2,346,607 |
| corpus JSON | `efilist_argument_library_v3_8_0.json` | `36febc9a80e9ffb8af5f5425a3cdad90` | 1,261,374 |
| JSX | `efilist_argument_library_v3_8_0.jsx` | `133945446fbafa12039ae3599c056448` | 1,202,078 |
| index HTML | `index_v3_8_0.html` | `84ad36b948923974ec6eff21a056325d` | 1,800,126 |
| coda | `coda_v3_7.html` | `654f56cf29d9a808fc870dda4c98b3cc` | 11,040 |
| validator | `v3prime_validator_v1_7.py` | `2cfb638d9a95aec20cd890a22e3b9263` | 22,322 |
| RWE schema | `real_world_examples_schema_v1_7.json` | `13ca1171725b8652dffc04b864692d40` | 80,202 |
| grading ledger | `rebuttal_grading_ledger_v3_8_0.json` | `a09946844ec9a2a967b8f965d1cae3d8` | 41,879 |

> Filenames carry a **frozen `_v3_8_0` base** (the MAJOR-cut marker); content advances in place through v3.8.1/.2/.3. The release is identified by git tag, not the filename. See the push handoff for repo-naming options.

---

## [v3.8.2] — 2026-05-30

**PATCH** over v3.8.0. `negative-util-aggregation` long-form strengthen. Invariants subtree byte-identical (anchor `8727787c…`).

### Changed

- **`negative-util-aggregation.responses.long`** re-authored 1,958 → 7,276 chars. Retired the consent-bolt-on (category error) + feasibility-dodge; installed a clean three-conjunct fork + begs-question diagnosis + de-idealization ledger move + layer-1/layer-2 split + an owned maximizing-NU concession. Ledger axes → `{v0.86, s0.83, c0.86, r0.82, a0.83}`; `long.rsi_pct` **79.9 → 84.0**; `long.grade` **C → B**; `headline_grade_long` B. Short 76.2 C / medium 78.3 C held byte-stable.
- **`combined.html`** `REBUTTAL_STRENGTH['negative-util-aggregation']` → `{v0.86,s0.83,c0.86,r0.82,a0.83}` (84.0 B).

### Attestation

- Canon **v37.1 → v37.2 MINOR**; invariants byte-identical (`8727787c…`). Surface-mutation gates 7/7 PASS.

---

## [v3.8.1] — 2026-05-30

**PATCH** over v3.8.0. `violence-as-reductio` long-form strengthen + jsx node-parity closure. Invariants subtree byte-identical (anchor `8727787c…`).

### Changed

- **`violence-as-reductio.responses.long`** strengthened on the NU-centrality seam, 11,795 → 16,595 chars. Regraded **83.8 → 86.2 B** (+2.4). Ledger short/medium deterministic backfill (80.1 C / 82.2 B) + `depths_note`.
- **`combined.html`** `REBUTTAL_STRENGTH['violence-as-reductio']` base axes → `{v0.87,s0.85,c0.87,r0.86,a0.86}`.

### Fixed

- **JSX node-parity closed.** The JSX `OBJECTIONS` array was regenerated from corpus to **81 nodes** with **7 `archetypeVariants`** propagated; the legacy `if_*` archetype keys were retired in favor of `responses.archetypeVariants`. JSX data parity with the corpus is now complete (the React *component* render path remains v3.7-era — see Known limitations).

### Attestation

- Canon **v37.0 → v37.1 MINOR**; invariants byte-identical (`8727787c…`). Gates 7/7 PASS.

---

## [v3.8.0] — 2026-05-30

**MINOR** (3.7 → 3.8). The structural cut the v3.7 line deferred. **The invariants subtree was mutated** — anchor `f6b94bf0…` → `8727787c…`. This is the first topology change since v3.7-stable, executed as one atomic phase-1 MAJOR cut (canon **v36.1 → v37.0**; deep-diff = 15 intended changes, historical records byte-identical).

### Added — taxonomy

- **+3 objections (78 → 81):**
  - `eliminativism` (**T4**) — eliminativism / illusionism about phenomenal valence ("suffering isn't really *bad* / it's just chemicals") deployed to dissolve the harm premise.
  - `solipsism` (**T4**) — only one's own mind is certain, so others' suffering can't ground the harm claim.
  - `suffering-as-meaning` (**T2**) — suffering confers meaning / growth, so it is not a harm to be prevented.
- **+1 mechanism (34 → 35):** `mech_Metaphysical_Deflation` (genuine-engagement type), minted from the `eliminativism` node.

### Changed — topology & schema

- **Dependency graph** 91 → **94 nodes** (81 objections + 13 premises) / 245 → **254 links** (161 → **167 strong** / 84 → **87 weak**).
- **Mechanism web** 112 → **116 nodes** (35 mechanisms + 81 objections) / 133 → **140 links**.
- **Map 1 held at 78 nodes / 2,886 edges** — the 3 new objections are not Map-1-represented; `MAP1_TRANSITIONS` is byte-identical.
- **`if_*` archetype keys retired → `responses.archetypeVariants`** (7 archetypeVariants side-cars spliced across corpus/jsx/combined/index).
- **`refutationalVariants` → `objectionSubforms`** (renamed across all four surfaces).
- **RWE schema v1.6 → v1.7** (`real_world_examples_schema_v1_7.json`); **validator v1.6 → v1.7** (`v3prime_validator_v1_7.py`).
- `totalEntries` 78 → **81**; `totalResponses` 238 → **243**.

### Unchanged

- 5 tiers; 13 premises (9 foundational + 4 diagnostic); 136 attested real-world deployments / 171 attachment edges (the 3 new objections carry no deployments yet — 78/81 objections are attested in the wild).

### Attestation

- Canon **v36.1 → v37.0 MAJOR** (one atomic cut). New invariants anchor `8727787c…`. Base surfaces were `index_v3_7_6.html` / `combined_v3_7_6.html`.

> **Note on v3.7.4 → v3.7.6.** Between the published v3.7.3 and the v3.8.0 cut, the v3.7 line continued with operator-elective content-advance micro-releases (v3.7.4–v3.7.6, benatar short/medium refinements) that were not separately tagged in this public repo; they are folded into the v3.8.0 base. The v3.8.0 cut supersedes them.

---

## [v3.7.3] — 2026-05-23

**PATCH.** `benatar-asymmetry-attack` long-form strengthen + ledger sync re-cut. Invariants subtree byte-identical to v3.7-stable (anchor `f6b94bf0cb3e6832dbdde0017b876e54`); corpus taxonomic content unchanged at 78 objections.

### Changed

- **`benatar-asymmetry-attack.responses.long`** strengthened from 4904ch single-paragraph to 8205ch four-paragraph treatment. Ledger axes re-cut to `{v0.88, s0.81, c0.80, r0.78, a0.84}`. `long.rsi_pct` 78.3 → 82.13; `long.grade` **C → B**; `headline_grade_long` C → B. Short/medium forms held verbatim per v28.2 cold-grade convention.
- **Danger quadrant** (deployment × grade): with the `benatar-asymmetry-attack` regrade, the corpus's two highest-deployment objections (`violence-as-reductio` cleared at v3.7.2, `benatar-asymmetry-attack` cleared here) are both B-band. No nodes remain in the danger quadrant; empty at v3.7.3.
- **`combined.html`** re-synced to v3.7.3 corpus (md5 `29f9d5c0d4befac52dae4ca88ea4211f`, size 2,243,165).
- **`rebuttal_grading_ledger.json`** refreshed for benatar axes overwrite (md5 `9b0b291fe4818587e3d724a7d6daf017`).

### Added

- **`rwe.html`** — fourth view-tab artifact (stats view). Sidecar; not wired into the in-app hash router.
- **`v3_7_cut_invariants.json`**, **`corpus_statistics_spec.md`**, **`sort_feature_spec.md`**.

### Attestation

- Harness `invariant_derivation_harness_v1` GREEN (exit 0). Surface-mutation gates 9/9 PASS. Canon v29.0 → v30.0. Project terminal state → `archived_v3_7_3_stable`. PATCH-class; NOT v3.8.

---

## [v3.7.2] — 2026-05-17

**PATCH.** Content-advance re-cut + publication reconciliation. Structural invariants byte-identical to v3.7 line; 78 objections.

- **`violence-as-reductio.responses.long`** strengthened (11,795 chars). Regraded **C(≈0.805) → B(≈0.838)**. The single most-deployed objection (27 RWE) cleared the danger quadrant.
- **`benatar-asymmetry-attack.responses.long`** strengthened (4904 chars). Blind re-grade C78.3 → C80.7 — band unchanged at v3.7.2 (cleared at v3.7.3).
- **Rendered-counter chrome** corrected from pre-sweep `74 / 222` to canon-attested `78 objections / 245 dependencies` (length-preserving, byte-neutral).
- **Pre-cut ledger sync**: four formerly-ungraded nodes entered `/grades`; ungraded 4 → 0. All 78/78 graded.

---

## [v3.7.1] — 2026-05-14

**MINOR-bookkeeping reconciliation** over v3.7-stable: 77→78 objection-count reconciliation. Single-file `combined.html` shipped (md5 `dd2abd01…`) absorbing library + RWE + coda behind the outer hash router. Public tag `v3.7.1`.

---

## [v3.7-stable] — initial publication

**MINOR.** Authoritative corpus published: 78 objections / 5 tiers / 34 mechanisms / 13 premises (9 foundational + 4 diagnostic) / 91 dependency-graph nodes / 245 dependency links (161 strong / 84 weak) / 112 mechanism-web nodes / 133 mechanism-web links / 2,886 Map 1 transition edges / 136 attested real-world deployments. RWE schema v1.6. Validator v1.6.

---

## Provenance

v3.8.x entries are constructed from canon v37.3's `archive_attestation.v3_8_*` blocks, the `rebuttal_grading_ledger`, and direct corpus/canon-invariant reads (objection/mechanism set-diffs against the v3.7 baseline). v3.7.x entries are carried from the prior changelog (canon v33.0 attestation). Where summaries cite axis tuples, RSI percentages, or md5/byte deltas, those numbers are canon-attested at the release moment they describe.
