# efilist argument library

A structured taxonomy of objections to antinatalism. **81 objections across 5 tiers**, attached to **35 psychological mechanisms**, with **136 attested real-world deployments** mapped to four interlocutor archetypes — *sophisticate, defender, drifter, blended*.

This is taxonomic work, not advocacy. The objections are catalogued as live moves in real discourse, not strawmen and not specimens. The descriptive content stands as observation regardless of whether you share the suffering-priority axiom; the closing **coda** makes that axiom visible as a stake rather than a derivation. Read both.

This repository is also home to the **Refusal Suite** — a small, growing family of single-file argument libraries that carry the same method into adjacent domains: cold-graded objection taxonomies, an *optionality-only* register for the wings (each defends a **right to** and never argues anyone **should** — the one licensed exception is abortion's single advisory claim), and one shared charter. The efilist library is the flagship and by far the largest; its four sibling wings, plus a flagship-adjacent veganism module, are below.

---

## The Refusal Suite

Each library is a self-contained `combined.html` that renders from its own corpus, with every objection cold-graded on the RSI rubric and governed by [`refusal_suite_charter_v0_1.md`](refusal_suite_charter_v0_1.md). The flagship is the canonical, version-pinned artifact; the wings auto-deploy from this repository.

| Library | Defends | Objections | Status | Live |
|---|---|---|---|---|
| **efilist argument library** | the antinatalist conclusion | **81** | flagship · pinned v3.9.16 | [library.wuld.ink/combined](https://library.wuld.ink/combined) |
| **Right to Die** | the right to choose one's own death | 17 | provisional-complete (v0.3.19) | [/right-to-die/combined](https://library.wuld.ink/right-to-die/combined) |
| **Abortion** | the right to end a pregnancy | 7 | complete (v0.1.6) · two-layer: optionality + one advisory claim | [/abortion/combined](https://library.wuld.ink/abortion/combined) |
| **Transgenderism** | the right to gender self-determination | 12 | complete (v0.1.11) | [/transgenderism/combined](https://library.wuld.ink/transgenderism/combined) |
| **Anthropocentrism** | dissent from human-supremacy | 6 | provisional-complete (v0.1.7) | [/anthropocentrism/combined](https://library.wuld.ink/anthropocentrism/combined) |
| **Veganism** | the positive case for veganism | 8 | complete (v0.2.1) · flagship-adjacent module | [/veganism/combined](https://library.wuld.ink/veganism/combined) |

The wings share the flagship's discipline but not its scale — each answers the standing objections to a single claim, tier-graded and charter-bound, in the same IBM-Plex-Mono "instrument" register. All are now built out. Every surface — flagship and wings — carries a **plain-language reading** alongside its scholar view (a `plain / scholar` toggle on the wings; a per-objection `plain` reveal on the flagship). The suite groups its libraries by domain (*Procreation & Existence*, *Harm & Autonomy*) behind a wing-switcher, and an umbrella front door lists all six surfaces at **[library.wuld.ink/libraries](https://library.wuld.ink/libraries)**.

---

## Open it (no download required)

The flagship is one self-contained HTML file. You do not have to clone or download anything to use it:

- **Live:** **[library.wuld.ink](https://library.wuld.ink)** now opens the umbrella front door; the flagship single-file build is at **[library.wuld.ink/combined](https://library.wuld.ink/combined)**, with three surfaces behind its top-nav router:
  - **library** — the taxonomy + force-directed Map 1
  - **examples** — the 136 attested real-world deployments
  - **coda** — the closing artifact on the load-bearing axiom
- **From this repo, no clone:** open `combined.html` through a raw HTML proxy — e.g. `https://raw.githack.com/alisendjsc-crypto/efilist-argument-library/main/combined.html`. (The file is ~2.9 MB; small-file preview proxies may choke — `raw.githack` handles it.)
- **Offline:** download `combined.html` and open it directly in any modern browser. No build step, no server.

> The flagship carries per-objection deep links (a copy-link on each card; `…/combined#obj-<id>`), and each suite wing carries its own (`…/<wing>/combined#obj-<id>`).

---

## What it looks like

**Argument Flow — Map 1, the next-move predictor.** Pick a source objection; the map renders predicted successor moves across the selected archetype (here: *blended*), with convergence-tier and mode annotations.

![Argument Flow / Map 1](screenshots/argument-flow-map1.png)

**Real-world examples — attested in the wild.** Every catalogued move is grounded in an observed deployment, with provenance and a bounded (<15-word) quotation.

![Real-world examples surface](screenshots/real-world-examples.png)

Further views — the dependency graph, the mechanism web, an objection-detail deconstruction with RSI, and the surface chrome — are in [`screenshots/`](screenshots/) and walked through in [`instructions.md`](instructions.md). A standalone `rwe.html` packages the real-world-examples surface for direct viewing or downstream tooling.

---

## The deliverable

The shippable artifact is a single file: **`combined.html`**. Library, real-world-examples table, and coda are absorbed into it behind the top-nav router. Works offline, no build step.

**Verbatim-artifact provenance (the integrity contract):**

| Field | Value |
|---|---|
| File | `combined.html` |
| Version (pin) | `v3.9.16` |
| md5 | `6dfeb5d4bb625fbb061b1cf0432f48ca` |
| Size | `2,955,840` bytes |

That md5 is binding. The file ships **verbatim** — no regeneration, no whitespace cleanup, no key reordering. A drifted hash is a corrupted artifact (cross-platform line-ending conversion is the usual culprit; the repo's `.gitattributes` enforces LF). The served `/combined` is held byte-identical to the pin (**pin == live**); a deploy that moves the artifact forces a same-session re-pin.

The binding integrity source is the project canon's `archive_attestation` block (current line, canon **v37.40**) together with the wuld.ink pin tooling.

---

## Status

**Stable at v3.9.16** (canon v37.40 line). The corpus holds at the **v3.8.0 structural cut** — **81 objections / 5 tiers / 35 mechanisms**, the last change to the objection count. The v3.9 line is render, grading-surface, and suite-integration work layered on that corpus: the dependency-graph render-from-data correction, real-world-examples surfacing, per-objection RSI deconstruction, the reader-mode + collapsible-card chrome, and the **Refusal Suite wing-switcher** that ties the flagship to its siblings. See [`CHANGELOG.md`](CHANGELOG.md) for per-release detail.

The **deployment × grade danger quadrant remains empty**: the three highest-deployment objections — `violence-as-reductio` (27 RWE), `benatar-asymmetry-attack` (15), `ai-fear` (10) — are all B-band. Grade distribution (long, n=81): **A 36 / B 34 / C 11 / 0 ungraded**.

---

## What's in the single file

`combined.html` carries three surfaces behind its top-nav router:

- **library** — the 81-objection taxonomy across 5 tiers, the 35 mechanism attributions, the dependency graph (**94 nodes** = 81 objections + 13 premises; **254 links**, 167 strong / 87 weak), the mechanism web (116 nodes, 140 links), and the force-directed Map 1 across the four archetypes (2,886 transition edges across 78 source-keys).
- **examples** — the 136 attested real-world deployments (171 attachment edges), schema v1.7.
- **coda** — the closing artifact on the axiom this library does not derive.

The regenerable sources behind the single file — the authoritative corpus JSON, the denormalized JSX sibling, the canonical HTML source, the RWE schema (v1.7), and the validator — remain in the source tree and are **not deprecated**. See [`instructions.md`](instructions.md) for programmatic use and the per-file integrity set.

---

## Repository structure

- **`combined.html`** + **`_redirects`** — the served flagship and its routing (`/` → `/libraries/`; `/combined` serves the flagship). The pinned artifact.
- **`efilist_argument_library_v3_8_0.json`** (corpus) · **`efilist_argument_library_v3_8_0.jsx`** (denormalized sibling) · **`rebuttal_grading_ledger.json`** · **`objections-index.json`** (generated export) · **`real_world_examples_schema_v1_7.json`** · **`build_objections_index.py`** — the regenerable flagship sources + tooling.
- **`refusal_suite_charter_v0_1.md`** — the shared charter governing every library in the suite.
- **`right-to-die/`** · **`abortion/`** · **`transgenderism/`** · **`anthropocentrism/`** — the four suite wings, each a self-contained set (corpus · grading ledger · objection index · `combined.html` · validator · builder · plain-language layman index). **`veganism/`** — the flagship-adjacent module (same set; a positive case, not an optionality wing). **`libraries/`** — the umbrella front door served at `/libraries`; **`flagship-layman-index.json`** + **`layman_index_validator_v0_*.py`** — the flagship plain-language mirror and its validators.
- **`screenshots/`** — README imagery. **`project_canon_v37_40.json`** — the current canon record.
- **`archive/`** — historical session-state, canon-snapshot, variant, and audit records, retained for posterity (not part of the live build).

---

## Reading

Open the flagship, land on its **library** view, pick a tier 1 or tier 2 objection, read its responses, then follow a few archetype transitions outward. Open the **coda** *after* — not before — the taxonomy feels familiar. Then return to the library with the coda's framing in mind.

For a longer guide — archetype semantics, the dependency graph, real-world-examples, programmatic use, integrity verification — see [`instructions.md`](instructions.md).

---

## Cite

A `CITATION.cff` (CFF 1.2.0) is provided at repository root and enables GitHub's "Cite this repository" widget. BibTeX:

```bibtex
@misc{efilist_argument_library_2026,
  title   = {efilist argument library},
  author  = {Cooper, Josiah S.},
  year    = {2026},
  version = {3.9.16},
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
