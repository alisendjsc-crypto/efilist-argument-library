# Using the efilist argument library

A short utility guide. The README is the door; this file is the room.

---

## Open it

The whole library is one file: **`combined.html`**. You can use it three ways without cloning the repo:

- **Live:** [`library.wuld.ink`](https://library.wuld.ink) — the deployed single-file build.
- **Raw proxy (repo, no clone):** `https://raw.githack.com/alisendjsc-crypto/efilist-argument-library/main/combined.html`.
- **Offline:** download `combined.html`, open it in any modern browser — no server, no build step.

Three surfaces live behind an outer hash router:

- `#/library` — the taxonomy, mechanism web, dependency graph, and force-directed Map 1
- `#/rwe` — the real-world-examples table
- `#/coda` — the closing artifact on the load-bearing axiom

You can deep-link to any of the three **surfaces** by appending its hash route. Per-objection deep-linking *inside* `#/library` is not a published address form — the outer hash router consumes the hash for surface selection first, so a bare `#<objection-id>` is not guaranteed to resolve. Surface-level routes only until that grammar is resolved against the router.

---

## The surface chrome

`combined.html` opens on `LIBRARY` (tabs: `LIBRARY` / `EXAMPLES` / `CODA`) with a typography selector (`STANDARD` / `LEGIBLE` / `HIGH-CONTRAST` / `BOTH`). Within `#/library` there are four views: `LIBRARY`, `MECHANISM WEB`, `DEPENDENCY GRAPH`, `ARGUMENT FLOW`. Objection responses render at three depths — `PUNCH`, `DECONSTRUCT`, `DISMANTLE` — with an `RSI METHODOLOGY` panel explaining the strength index. See [`screenshots/`](screenshots/) for each view.

> **Rendered-counter caveat (resolved in v3.7.2; held at v3.7.3).** The static header chrome in the `DEPENDENCY GRAPH` and `MECHANISM WEB` views previously showed a pre-sweep `74 objections` / `222 dependencies`. The v3.7.2 re-cut corrected it (byte-neutral, length-preserving): the headers now read **78 objections / 245 dependencies**, matching canon-attested truth (**78 objections, 245 dependencies, 91 dependency-graph nodes**). v3.7.3 is PATCH-class; the chrome is unchanged.

---

## The four archetypes

Map 1 renders the objection space across four interlocutor modes:

- **sophisticate** — pivots via shared premises and shared mechanisms.
- **defender** — surfaces mechanism with two-mechanism disclosure.
- **drifter** — moves by pattern, often across mechanisms.
- **blended** — composite mode with per-mode rationales and convergence-tier accounting.

Edge distribution across the **78 source-keys** (v3.7.3 attestation; unchanged from v3.7.2 — score-layer + prose re-cut, topology untouched): **675 sophisticate, 526 defender, 390 drifter, 1,295 blended — 2,886 total.** Blended mode-count distribution (successors disclosed per blended edge): {1: 1,010, 2: 274, 3: 11}. Two-mechanism disclosure true-counts: defender 5, drifter 42, blended 45.

The behavioral content lives in each edge's `rationale` field (or `mode_rationales` for blended edges). Each edge walks the specific move from one objection to the next within that archetype's mode. The patterns are easier to see than to summarize — work the map.

---

## The dependency graph

**91 nodes**: 78 objections + 13 premises (9 foundational, 4 diagnostic). **245 links**, of which **161 are strong** (load-bearing) and **84 are weak** (softer relevance).

Strong vs. weak is a separate axis from tier. An objection's tier categorizes the objection itself; a link's strength is a property of how tightly that objection depends on the premise (or another objection) at the other end of the link.

The mechanism web is a separate view: **112 nodes** (34 mechanisms + 78 objections), **133 links**.

---

## Real-world examples

`#/rwe` carries **136 attested real-world deployments** of objections in live discourse — institutional writing, lifestyle explainers, student journalism, social platforms, niche forums. They are evidence that the catalogued moves occur in the wild, not constructed illustrations.

**Schema:** `real_world_examples_schema_v1_6.json` (`spec_id: real_world_examples_schema_v1`, `spec_version: 1.6`). The authoritative store is the corpus JSON at JSON-path `$.realWorldExamples`; per-objection indices and the JSX embedding are derived views.

Each example record carries, among other fields:

- `instance_id` — unique, pattern-recommended identifier
- `attached_objections` — which catalogued objection(s) the deployment instantiates (≥1)
- `source_url`, `source_title`, `source_byline`, `source_publication`, `source_date`, `accessed_date`, `archive_url` — provenance and decay-resistance
- `short_quote_under_15_words` + `paraphrased_summary` — bounded excerpt plus a paraphrase (the under-15-word cap is a schema-enforced quotation discipline)
- `rhetorical_move_observed`, `instance_polarity`, `frame_inversion`, `layer_skepticism` — what the move *does*
- `speaker_type`, `archetype_signal_observed`, `archetype_signal_rationale` — which interlocutor archetype the source reads as, and why
- `corpus_decay_risk`, `short_quote_attestation_status`, `verbatim_recovery_status` — integrity / link-rot tracking

The schema's `validation_rules` block is what the validator exercises against the table; the under-15-word quotation bound and required-provenance fields are enforced there, not by convention.

A standalone view of the real-world-examples table also ships as `rwe.html` (sidecar; new at v3.7.3) — the same 136-deployment surface as `#/rwe` inside the single-file router, packaged for direct viewing or downstream tooling. Not wired into the outer hash router; open directly.

---

## A reading order

The library doesn't enforce a path. If you want one:

1. Open the library. On `#/library`, pick a tier 1 or tier 2 objection. Read the responses.
2. Follow a few archetype transitions outward. Notice how the four modes pivot differently from the same starting node.
3. Cross to `#/rwe` and find a deployment attached to that objection. See the move in the wild.
4. Open `#/coda` *after* — not before — the taxonomy feels familiar. The coda makes the load-bearing axiom explicit.
5. Return to the library with the coda's framing in mind.

---

## Programmatic use

The regenerable sources behind the single file are not deprecated:

- **Corpus:** `efilist_argument_library_v3_7_3.json`.
  Top-level keys: `version`, `generated`, `totalEntries`, `totalResponses`, `tiers`, `objections`, `dependencyGraph`, `premiseDependencyMatrix`, `premises`, `realWorldExamples`, `registered_moves`, `features`. `totalEntries` 78, `totalResponses` 238.
- **RWE schema:** `real_world_examples_schema_v1_6.json`.
- **Validator:** `v3prime_validator_v1_6.py`. Confirm integrity:
  ```
  python3 v3prime_validator_v1_6.py --self-test
  ```
  Expect `13/13 PASS` and `_overall_pass: true`.

The denormalized React sibling `efilist_argument_library_v3_7_3.jsx` carries `registered_moves` and `realWorldExamples` as top-level constants for tooling that prefers JSX over JSON ingestion. Content is byte-identical to the corpus JSON's corresponding fields.

### Where the score lives (architecture — read this before tooling against grades)

The rebuttal-strength score layer is **canonized as a 2-artifact model** (canon v28.1):

- **Taxonomic spine — `corpus JSON` + `JSX`.** Objection identity, tier, category, mechanism-links, `dependencyGraph`, prose. **Non-score-bearing by design.** Low churn. The score tuple is **not** in the corpus or the JSX, and denormalizing it into them is canonically rejected.
- **Score layer — `index.html`** (with `combined.html` as its derived superset bundle). The raw `REBUTTAL_STRENGTH` 5-tuple `{v, s, c, r, a}` persists **here only**. `RSI` / percentage / grade-band are **never persisted anywhere** — they are derived at render by `computeRSI` / `rsiGrade` / `depthModifiedRSI`.

Practical consequence: do not expect a grade field in the corpus JSON or JSX — they don't carry one and that is intentional, not an omission. If you need scores programmatically, project them from the `index.html` score layer at point of demand (a derived `scores.json`), not from the spine. `combined.html` regenerates as the superset of `index.html`. The ledger that tracked grade consistency (`rebuttal_grading_ledger`) reached `LEDGER_INCONSISTENT` and was **resolved at canon v28.2**; a v3.7.2 pre-cut ledger-sync brought all **78/78** into `/grades` (ungraded → 0, fully consistent with the `index.html` score layer). The v3.7.3 ledger sync re-cut applied the `benatar-asymmetry-attack` axes overwrite (long.rsi_pct 78.3 → 82.13, long.grade C → B). The open-questions active set is empty.

See [`STATISTICS.md`](STATISTICS.md) for the RSI calculus described at the level the canon attests it, and for corpus-level distributions.

---

## Verifying integrity

The binding integrity source is the project canon's `archive_attestation` block. The single-file contract:

```
md5sum combined.html        # -> 29f9d5c0d4befac52dae4ca88ea4211f
stat -c %s combined.html    # -> 2243165
```

`release_manifest_v3_7_1.json` in this repo is a **reconstructed** manifest: it carries the invariant attestation (node/edge/distribution counts), not the md5/sha256 set. Treat the canon-anchored md5 above as authoritative for the single-file contract. A size/hash mismatch usually means line-ending conversion on a cross-platform pull; the repo's `.gitattributes` enforces LF — if you've sidestepped it, restore from the `v3.7.3` release tag.

v3.7.3 per-file integrity set (the published contract; canon v30.0 `archive_attestation.release_artifact_md5_set_per_release_manifest_v3_7_3`):

| Artifact | File | md5 |
|---|---|---|
| single-file | `combined.html` | `29f9d5c0d4befac52dae4ca88ea4211f` |
| corpus JSON | `efilist_argument_library_v3_7_3.json` | `af2befa16e7e23b6c73104e529d5f653` |
| JSX | `efilist_argument_library_v3_7_3.jsx` | `2f25960ad66bf9539a79a3e6dcc6d73a` |
| index HTML | `index_v3_7_3.html` | `eb73fb6f456ce43d9cf44e2be264f55d` |
| coda | `coda_v3_7.html` | `654f56cf29d9a808fc870dda4c98b3cc` |
| validator | `v3prime_validator_v1_6.py` | `f114d87c46a05891ac0077854200f000` |
| RWE schema | `real_world_examples_schema_v1_6.json` | `a5011ddba98cd98c5afc9c28cdc79752` |
| grading ledger | `rebuttal_grading_ledger.json` | `9b0b291fe4818587e3d724a7d6daf017` |

---

## Reporting

Archived stable at v3.7.3 (canon v30.0 line). No maintenance cadence. Open an issue if something seems off, but expect resolution only via an operator-elective follow-up session — not a patch release.
