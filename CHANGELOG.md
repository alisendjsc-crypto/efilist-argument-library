# efilist_argument_library — v3.7 Stable Release

**Release tag:** v3.7-stable  
**Release date:** 2026-05-14  
**Cut session:** v3-7-cut  
**Canon at cut:** v24.1 (predecessor v24.0)

---

## What this is

A stable release marker for the v3.7 line of the efilist argument library — a structured taxonomy of objections to antinatalism with associated real-world examples, dependency mappings, and a force-directed visualization layer. The cut is **manifest-only**: zero artifact mutation. All six release artifacts are pre-existing, content-verified by md5, and attested against canon v24.0 invariants.

---

## Release artifact set

| Artifact | Size | md5 | Role |
|---|---|---|---|
| `efilist_argument_library_v3_7_post_cluster_insertion_inmendham.json` | 1,160,847 | `fb0e41ca1c0722e8615b1e7001e229ed` | Authoritative corpus |
| `efilist_argument_library_v3_7_post_surface_parity_jsx.jsx` | 1,107,006 | `be25b1432e7228db629b7122f85dec4d` | Denormalized React sibling |
| `index_v3_7_post_b3f2_surface_parity_html.html` | 1,687,795 | `39ea0cd42f137bbd3fdc86d6964ac91b` | Single-file HTML viewer |
| `real_world_examples_schema_v1_6.json` | 80,253 | `a5011ddba98cd98c5afc9c28cdc79752` | RWE schema (cut spec) |
| `coda_v3_7.html` | 11,040 | `e955812115e6aaf5bb1c445cd1c878c0` | Epistemic coda |
| `v3prime_validator_v1_6.py` | 21,816 | `f114d87c46a05891ac0077854200f000` | Validator (13/13 self-test PASS) |

Full sha256 set in `release_manifest_v3_7_stable.json`.

---

## Canonical counts (v3.7 stable)

- **78** objections across **5** tiers
- **34** psychological mechanisms (Map 1)
- **77** Map 1 nodes, **133** Map 2 (mechanism-objection) edges
- **91** dependency-graph nodes (13 premises + 78 objections), **245** links
- **9** foundational premises, **4** diagnostic premises
- **136** real-world example instances (multi-surface: corpus + JSX)
- **238** total pre-built responses (3 depth levels on most objections + archetype-conditional surfaces)
- **4** registered cross-cutting moves (3 defensive + 1 substantive position)

---

## Delta from v3.6.1 line

- **Objections:** 77 → 78 *(cluster-insertion-session-inmendham; T2 augmentation)*
- **Real-world examples:** 81 → 136 *(batch chain 8a–8j + inmendham cluster)*
- **Dependency-graph links:** 222 → 245 *(+23)*
- **Mechanism-objection edges:** 118 → 133 *(+15)*
- **JSX state:** registered_moves-only denormalization → registered_moves + realWorldExamples denormalization *(multi-surface RWE upgrade)*
- **HTML state:** chrome counters stale at 74/118/222 → refreshed to 78/77/133/245 *(byte-neutral splice)*
- **Arc closures:** `v3_7_surface_parity_arc` CLOSED at canon v23.1; `v3_7_cut_prep` absorbed at canon v24.0

---

## Pre-cut gate

- Validator self-test: **13/13 PASS** (`_overall_pass=true`)
- Round-trip JSON parse on corpus and canon: **PASS**
- Fingerprint capture on all six release artifacts: **complete**
- Canon invariant attestation: **100%** on cryptographic identity (md5/sha256)

---

## Documented residue (out of scope)

These are tracked as non-blocking and explicitly excluded from the cut per session prompt:

1. **`Q_canon_state_refresh_residue_invariant_drift` (LOW).** Canon `dep_graph_data_strong_link_count_v361` (159) + `dep_graph_data_weak_link_count_v361` (81) = 240, vs live corpus total link count 245. The v361-tagged scalars are locked-historic snapshots; the live corpus shows strong=161, weak=84 (sum=245, reconciled). The labeled invariants will be refreshed in a dedicated residue-invariant-refresh session.
2. **Canon corpus `size_bytes` record correction.** `cluster_insertion_session_inmendham_session_record.corpus_output_size_bytes` reads 1,157,942; live stat is 1,160,847 (+2905). md5 is identical → content integrity binding. Sub-md5 scalar bookkeeping correction deferred to residue session.
3. **15 active open questions** carry forward unchanged.

---

## What v3.7 stable *is not*

This is a release marker, not a project closure. It does not:

- Touch corpus, JSX, HTML, schema, validator, or coda content
- Resolve any of the 15 active open questions
- Close out the residue-invariant drift
- Adjudicate UI/affordance backlog
- Re-derive any field

It declares: *this six-artifact set, at these fingerprints, is the stable v3.7 release.*

---

## Next

Per canon v24.1 `next_recommended_session`:  
- **OPTION A:** `residue-invariant-refresh` (LOW priority; addresses arithmetic gap + size_bytes record + label-naming hygiene)  
- **OPTION B:** `closeout` (project archive; v3.7 stable as terminal release marker)

Operator selects.

---

*Author: Josiah S. Cooper (AnomicIndividual87) — License: free to use, distribute, and modify.*
