# Using the efilist argument library

A short utility guide. The README is the door; this file is the room. **Current at v3.8.3.**

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

You can deep-link to any of the three **surfaces** by appending its hash route. Per-objection deep-linking *inside* `#/library` is not a published address form — the outer hash router consumes the hash for surface selection first.

---

## The surface chrome

`combined.html` opens on `LIBRARY` (tabs: `LIBRARY` / `EXAMPLES` / `CODA`) with a typography selector (`STANDARD` / `LEGIBLE` / `HIGH-CONTRAST` / `BOTH`). Within `#/library` there are four views: `LIBRARY`, `MECHANISM WEB`, `DEPENDENCY GRAPH`, `ARGUMENT FLOW`. Objection responses render at three depths — `PUNCH`, `DECONSTRUCT`, `DISMANTLE` — with an `RSI METHODOLOGY` panel explaining the strength index.

> **Rendered-counter caveat (known lag at v3.8.3).** The static header chrome in the `DEPENDENCY GRAPH` and `MECHANISM WEB` views currently reads **78 objections / 245 dependencies** — the v3.7-line values. The v3.8.0 cut moved canon truth to **81 objections / 254 dependencies**; the chrome lags by the three nodes added in that cut. The fix is byte-neutral (equal digit-width) and is queued as an operator-elective chrome correction; the data and graphs render all 81 objections correctly.

---

## The four archetypes

Map 1 renders the objection space across four interlocutor modes:

- **sophisticate** — pivots via shared premises and shared mechanisms.
- **defender** — surfaces mechanism with two-mechanism disclosure.
- **drifter** — moves by pattern, often across mechanisms.
- **blended** — composite mode with per-mode rationales and convergence-tier accounting.

Edge distribution across the **78 source-keys** (unchanged since v3.7.2; the v3.8.0 cut held Map 1 at 78 nodes): **675 sophisticate, 526 defender, 390 drifter, 1,295 blended — 2,886 total.** Blended mode-count distribution: {1: 1,010, 2: 274, 3: 11}. Two-mechanism disclosure true-counts: defender 5, drifter 42, blended 45.

The behavioral content lives in each edge's `rationale` field (or `mode_rationales` for blended edges). Work the map — the patterns are easier to see than to summarize.

---

## The dependency graph

**94 nodes**: 81 objections + 13 premises (9 foundational, 4 diagnostic). **254 links**, of which **167 are strong** (load-bearing) and **87 are weak** (softer relevance).

Strong vs. weak is a separate axis from tier. An objection's tier categorizes the objection itself; a link's strength is a property of how tightly that objection depends on the premise (or another objection) at the other end.

The mechanism web is a separate view: **116 nodes** (35 mechanisms + 81 objections), **140 links**.

---

## Real-world examples

`#/rwe` carries **136 attested real-world deployments** (171 attachment edges) of objections in live discourse — institutional writing, lifestyle explainers, student journalism, social platforms, niche forums. They are evidence that the catalogued moves occur in the wild, not constructed illustrations. **78 of the 81 objections** carry at least one deployment; the three added in the v3.8.0 cut (`eliminativism`, `solipsism`, `suffering-as-meaning`) are catalogued but not yet attested.

**Schema:** `real_world_examples_schema_v1_7.json` (`spec_id: real_world_examples_schema_v1`, `spec_version: 1.7`). The authoritative store is the corpus JSON at JSON-path `$.realWorldExamples`; per-objection indices and the JSX embedding are derived views.

Each record carries `instance_id`, `attached_objections` (≥1, each with `objection_id` + attachment rationale), full provenance (`source_url`, `source_date`, `accessed_date`, `archive_url`, decay-risk / recovery-status tracking), a `short_quote_under_15_words` + `paraphrased_summary`, and move-characterization fields (`rhetorical_move_observed`, `instance_polarity`, `archetype_signal_observed`). The schema's `validation_rules` block is what the validator exercises; the under-15-word bound and required-provenance fields are enforced there, not by convention.

A standalone view of the table also ships as `rwe.html` (sidecar) — the same surface as `#/rwe`, packaged for direct viewing. Not wired into the outer hash router; open directly.

---

## A reading order

1. Open the library. On `#/library`, pick a tier 1 or tier 2 objection. Read the responses.
2. Follow a few archetype transitions outward. Notice how the four modes pivot differently from the same starting node.
3. Cross to `#/rwe` and find a deployment attached to that objection. See the move in the wild.
4. Open `#/coda` *after* — not before — the taxonomy feels familiar.
5. Return to the library with the coda's framing in mind.

---

## Programmatic use

The regenerable sources behind the single file are not deprecated:

- **Corpus:** `efilist_argument_library_v3_8_0.json`.
  Top-level keys: `version`, `generated`, `totalEntries`, `totalResponses`, `tiers`, `features`, `objections`, `dependencyGraph`, `premiseDependencyMatrix`, `premises`, `realWorldExamples`, `registered_moves`. `totalEntries` **81**, `totalResponses` **243**.
- **RWE schema:** `real_world_examples_schema_v1_7.json`.
- **Validator:** `v3prime_validator_v1_7.py`. Confirm integrity:
  ```
  python3 v3prime_validator_v1_7.py --self-test          # -> _overall_pass: true (exit 0)
  python3 v3prime_validator_v1_7.py efilist_argument_library_v3_8_0.json   # -> verdict: PASS
  ```

> **Filename scheme (v3.8 line).** The corpus / JSX / index filenames carry a **frozen `_v3_8_0` base** — the marker of the v3.8.0 MAJOR cut. Content advances in place through v3.8.1/.2/.3; the release is identified by the git tag (`v3.8.3`), not the filename. `combined.html`, `rebuttal_grading_ledger.json`, and `coda_v3_7.html` keep bare / `_v3_7` names as before.

The denormalized React sibling `efilist_argument_library_v3_8_0.jsx` carries `registered_moves` and `realWorldExamples` as top-level constants. Content is byte-identical to the corpus JSON's corresponding fields. (The React *component* render path is still v3.7-era — it renders short/medium/long only, with no `archetypeVariants` render path; the data parity is complete, the component refresh is deferred.)

### Where the score lives (architecture — read this before tooling against grades)

The rebuttal-strength score layer is **canonized as a 2-artifact model** (canon v28.1):

- **Taxonomic spine — `corpus JSON` + `JSX`.** Objection identity, tier, category, mechanism-links, `dependencyGraph`, prose. **Non-score-bearing by design.** The score tuple is **not** in the corpus or JSX.
- **Score layer — `index.html`** (with `combined.html` as its derived superset). The raw `REBUTTAL_STRENGTH` 5-tuple `{v, s, c, r, a}` persists **here only**. `RSI` / percentage / grade-band are **never persisted** — derived at render by `computeRSI` / `rsiGrade` / `depthModifiedRSI` (bands A ≥ 0.88 · B ≥ 0.82 · C ≥ 0.76 · D < 0.76).

Practical consequence: do not expect a grade field in the corpus JSON or JSX. If you need scores programmatically, project them from the `index.html` score layer. The grade-consistency ledger (`rebuttal_grading_ledger`) is fully consistent with the index score layer at v3.8.3: all **81/81 graded**, ungraded → 0. The v3.8.1/.2/.3 foldins applied the `violence-as-reductio` (→86.2 B), `negative-util-aggregation` (→84.0 B), and `joy-outweighs-harms` (→83.0 B) axes overwrites, and v3.8.3 reconciled the index score layer to the ledger for all three (index == combined == ledger).

See [`STATISTICS.md`](STATISTICS.md) for the RSI calculus and corpus-level distributions.

---

## Verifying integrity

The binding integrity source is the project canon's `archive_attestation` block (canon v37.3, `archive_attestation.v3_8_3`). The single-file contract:

```
md5sum combined.html        # -> dbbbc6d1b993b20064ad0a6d9f27b051
stat -c %s combined.html    # -> 2346607
```

A size/hash mismatch usually means line-ending conversion on a cross-platform pull; the repo's `.gitattributes` enforces LF — restore from the `v3.8.3` release tag if you've sidestepped it.

v3.8.3 per-file integrity set (`archive_attestation.v3_8_3.published_contract_md5`):

| Artifact | File | md5 |
|---|---|---|
| single-file | `combined.html` | `dbbbc6d1b993b20064ad0a6d9f27b051` |
| corpus JSON | `efilist_argument_library_v3_8_0.json` | `36febc9a80e9ffb8af5f5425a3cdad90` |
| JSX | `efilist_argument_library_v3_8_0.jsx` | `133945446fbafa12039ae3599c056448` |
| index HTML | `index_v3_8_0.html` | `84ad36b948923974ec6eff21a056325d` |
| coda | `coda_v3_7.html` | `654f56cf29d9a808fc870dda4c98b3cc` |
| validator | `v3prime_validator_v1_7.py` | `2cfb638d9a95aec20cd890a22e3b9263` |
| RWE schema | `real_world_examples_schema_v1_7.json` | `13ca1171725b8652dffc04b864692d40` |
| grading ledger | `rebuttal_grading_ledger_v3_8_0.json` | `a09946844ec9a2a967b8f965d1cae3d8` |

---

## Reporting

Stable at v3.8.3 (canon v37.3 line). The v3.8 line has an open operator-elective strengthening queue (the current grade floor is `flow-states-csikszentmihalyi`, 78.1 C). Open an issue if something seems off; resolution is via operator-elective follow-up, not a maintenance cadence.
