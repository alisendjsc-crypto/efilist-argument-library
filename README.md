# efilist argument library

A structured taxonomy of objections to antinatalism. **81 objections across 5 tiers**, attached to **35 psychological mechanisms**, with **136 attested real-world deployments** mapped to four interlocutor archetypes — *sophisticate, defender, drifter, blended*.

This is taxonomic work, not advocacy. The objections are catalogued as live moves in real discourse, not strawmen and not specimens. The descriptive content stands as observation regardless of whether you share the suffering-priority axiom; the closing **coda** makes that axiom visible as a stake rather than a derivation. Read both.

This repository is also home to the **Refusal Suite** — a small, growing family of single-file argument libraries that carry the same method into adjacent domains: cold-graded objection taxonomies, an *optionality-only* register (each library defends a **right to**, and never argues that anyone **should**), and one shared charter. The efilist library is the flagship and by far the largest; its sibling wings are below.

---

## The Refusal Suite

Each library is a self-contained `combined.html` that renders from its own corpus, with every objection cold-graded on the RSI rubric and governed by [`refusal_suite_charter_v0_1.md`](refusal_suite_charter_v0_1.md). The flagship is the canonical, version-pinned artifact; the wings auto-deploy from this repository.

| Library | Defends | Objections | Status | Live |
|---|---|---|---|---|
| **efilist argument library** | the antinatalist conclusion | **81** | flagship · stable (v3.9.15) | [library.wuld.ink/combined](https://library.wuld.ink/combined) |
| **Right to Die** | the right to choose one's own death | 17 | live · set provisional-complete | [/right-to-die/combined](https://library.wuld.ink/right-to-die/combined) |
| **Anthropocentrism** | dissent from human-supremacy | 6 | live · set provisional-complete | [/anthropocentrism/combined](https://library.wuld.ink/anthropocentrism/combined) |
| **Transgenderism** | the right to gender self-determination | 3 | in build | [/transgenderism/combined](https://library.wuld.ink/transgenderism/combined) |
| **Abortion** | — | — | planned | — |
| **Veganism** | — | — | planned | — |

The wings share the flagship's discipline but not its scale — each answers the standing objections to a single optionality claim, tier-graded and charter-bound, in the same IBM-Plex-Mono "instrument" register. The suite groups its libraries by domain (*Procreation & Existence*, *Harm & Autonomy*) behind a wing-switcher. Object counts grow as objections are authored; the flagship remains the main work.

---

## Open it (no download required)

The flagship is one self-contained HTML file. You do not have to clone or download anything to use it:

- **Live:** **[library.wuld.ink](https://library.wuld.ink)** — the deployed single-file build. Three surfaces behind an outer hash router:
  - [`library.wuld.ink/#/library`](https://library.wuld.ink/#/library) — the taxonomy + force-directed Map 1
  - [`library.wuld.ink/#/rwe`](https://library.wuld.ink/#/rwe) — the 136 attested real-world deployments
  - [`library.wuld.ink/#/coda`](https://library.wuld.ink/#/coda) — the closing artifact on the load-bearing axiom
- **From this repo, no clone:** open `combined.html` through a raw HTML proxy — e.g. `https://raw.githack.com/alisendjsc-crypto/efilist-argument-library/main/combined.html`. (The file is ~2.9 MB; small-file preview proxies may choke — `raw.githack` handles it.)
- **Offline:** download `combined.html` and open it directly in any modern browser. No build step, no server.

> Surface-level links only. Per-objection deep-link grammar inside `#/library` is **not yet resolved** against the router and is deliberately not published here. Use the three surface routes above. The suite wings carry their own per-objection deep links (`…/<wing>/combined#obj-<id>`).

---

## What it looks like

**Argument Flow — Map 1, the next-move predictor.** Pick a source objection; the map renders predicted successor moves across the selected archetype (here: *blended*), with convergence-tier and mode annotations.

![Argument Flow / Map 1](screenshots/argument-flow-map1.png)

**Real-world examples — attested in the wild.** Every catalogued move is grounded in an observed deployment, with provenance and a bounded (<15-word) quotation.

![Real-world examples surface](screenshots/real-world-examples.png)

Further views — the dependency graph, the mechanism web, an objection-detail deconstruction with RSI, and the surface chrome — are in [`screenshots/`](screenshots/) and walked through in [`instructions.md`](instructions.md). A standalone `rwe.html` packages the real-world-examples surface for direct viewing or downstream tooling.

---

## The deliverable

The shippable artifact is a single file: **`combined.html`**. Library, real-world-examples table, and coda are absorbed into it behind the outer hash router. Works offline, no build step.

**Verbatim-artifact provenance (the integrity contract):**

| Field | Value |
|---|---|
| File | `combined.html` |
| Version (pin) | `v3.9.15` |
| md5 | `5f06815341b8f4ada1ea7830c0c65c72` |
| Size | `2,952,543` bytes |

That md5 is binding. The file ships **verbatim** — no regeneration, no whitespace cleanup, no key reordering. A drifted hash is a corrupted artifact (cross-platform line-ending conversion is the usual culprit; the repo's `.gitattributes` enforces LF). The served `/combined` is held byte-identical to the pin (**pin == live**); a deploy that moves the artifact forces a same-session re-pin.

The binding integrity source is the project canon's `archive_attestation` block (current line, canon **v37.39**) together with the wuld.ink pin tooling.

---

## Status

**Stable at v3.9.15** (canon v37.39 line). The corpus holds at the **v3.8.0 structural cut** — **81 objections / 5 tiers / 35 mechanisms**, the last change to the objection count. The v3.9 line is render, grading-surface, and suite-integration work layered on that corpus: the dependency-graph render-from-data correction, real-world-examples surfacing, per-objection RSI deconstruction, the reader-mode + collapsible-card chrome, and the **Refusal Suite wing-switcher** that ties the flagship to its siblings. See [`CHANGELOG.md`](CHANGELOG.md) for per-release detail.

The **deployment × grade danger quadrant remains empty**: the three highest-deployment objections — `violence-as-reductio` (27 RWE), `benatar-asymmetry-attack` (15), `ai-fear` (10) — are all B-band. Grade distribution (long, n=81): **A 36 / B 34 / C 11 / 0 ungraded**.

---

## What's in the single file

`combined.html` carries three surfaces behind the hash router:

- **`#/library`** — the 81-objection taxonomy across 5 tiers, the 35 mechanism attributions, the dependency graph (**94 nodes** = 81 objections + 13 premises; **254 links**, 167 strong / 87 weak), the mechanism web (116 nodes, 140 links), and the force-directed Map 1 across the four archetypes (2,886 transition edges across 78 source-keys).
- **`#/rwe`** — the 136 attested real-world deployments (171 attachment edges), schema v1.7.
- **`#/coda`** — the closing artifact on the axiom this library does not derive.

The regenerable sources behind the single file — the authoritative corpus JSON, the denormalized JSX sibling, the canonical HTML source, the RWE schema (v1.7), and the validator — remain in the source tree and are **not deprecated**. See [`instructions.md`](instructions.md) for programmatic use and the per-file integrity set.

---

## Repository structure

- **`combined.html`** + **`_redirects`** — the served flagship and its routing (`/` → `/combined`). The pinned artifact.
- **`efilist_argument_library_v3_8_0.json`** (corpus) · **`efilist_argument_library_v3_8_0.jsx`** (denormalized sibling) · **`rebuttal_grading_ledger.json`** · **`objections-index.json`** (generated export) · **`real_world_examples_schema_v1_7.json`** · **`build_objections_index.py`** — the regenerable flagship sources + tooling.
- **`refusal_suite_charter_v0_1.md`** — the shared charter governing every library in the suite.
- **`right-to-die/`** · **`anthropocentrism/`** · **`transgenderism/`** — the suite wings, each a self-contained set (corpus · grading ledger · objection index · `combined.html` · validator · builder).
- **`screenshots/`** — README imagery. **`project_canon_v37_39.json`** — the current canon record.
- **`archive/`** — historical session-state, canon-snapshot, variant, and audit records, retained for posterity (not part of the live build).

---

## Reading

Open the library, land on `#/library`, pick a tier 1 or tier 2 objection, read its responses, then follow a few archetype transitions outward. Open `#/coda` *after* — not before — the taxonomy feels familiar. Then return to the library with the coda's framing in mind.

For a longer guide — archetype semantics, the dependency graph, real-world-examples, programmatic use, integrity verification — see [`instructions.md`](instructions.md).

---

## Cite

A `CITATION.cff` (CFF 1.2.0) is provided at repository root and enables GitHub's "Cite this repository" widget. BibTeX:

```bibtex
@misc{efilist_argument_library_2026,
  title   = {efilist argument library},
  author  = {Cooper, Josiah S.},
  year    = {2026},
  version = {3.9.15},
  url     = {https://github.com/alisendjsc-crypto/efilist-argument-library},
  note    = {Stable release, v3.9 line; flagship of the Refusal Suite}
}
```

---

## License

- Corpus, JSX, schema, single-file HTML (`combined.html`), coda: **CC-BY-4.0**. Attribution required; no share-alike obligation.
- The validator code: **MIT**.

Attribution per `CITATION.cff`. Verbatim citation and adaptation both require attribution under CC-BY-4.0; the validator code is permissive.

> **Note on GitHub's "Unknown" license badge.** GitHub's license detector matches a single root `LICENSE` against canonical SPDX bodies. The current `LICENSE` is a human-worded CC-BY-4.0 *summary*, and the repo is content/code dual-licensed (`LICENSE` = CC-BY-4.0, `LICENSE-CODE` = MIT), neither of which GitHub auto-detects. To make the badge read **CC-BY-4.0**: replace the body of `LICENSE` with the verbatim canonical CC BY 4.0 legal text and move the custom attribution prose into a `NOTICE` file. This is an operator-elective cosmetic fix — the licensing of the work is unaffected and fully stated above.

---

## On the standpoint

The library does not derive the suffering-priority axiom from anything more basic and does not pretend to. The coda is the explicit account of that floor. The descriptive content — the taxonomy, the dependency graph, the mechanism attributions, the attested examples — stands as observation regardless of where you land on the axiom itself.

The library ends here. What remains is the act of standing on it.
