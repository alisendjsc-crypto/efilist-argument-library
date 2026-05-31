# efilist argument library

A structured taxonomy of objections to antinatalism. **81 objections across 5 tiers**, attached to **35 psychological mechanisms**, with **136 attested real-world deployments** mapped to four interlocutor archetypes — *sophisticate, defender, drifter, blended*.

This is taxonomic work, not advocacy. The objections are catalogued as live moves in real discourse, not strawmen and not specimens. The descriptive content stands as observation regardless of whether you share the suffering-priority axiom; the closing **coda** makes that axiom visible as a stake rather than a derivation. Read both.

---

## Open it (no download required)

The library is one self-contained HTML file. You do not have to clone or download anything to use it:

- **Live:** **[library.wuld.ink](https://library.wuld.ink)** — the deployed single-file build. Three surfaces behind an outer hash router:
  - [`library.wuld.ink/#/library`](https://library.wuld.ink/#/library) — the taxonomy + force-directed Map 1
  - [`library.wuld.ink/#/rwe`](https://library.wuld.ink/#/rwe) — the 136 attested real-world deployments
  - [`library.wuld.ink/#/coda`](https://library.wuld.ink/#/coda) — the closing artifact on the load-bearing axiom
- **From this repo, no clone:** open `combined.html` through a raw HTML proxy — e.g. `https://raw.githack.com/alisendjsc-crypto/efilist-argument-library/main/combined.html`. (The file is ~2.3 MB; small-file preview proxies may choke — `raw.githack` handles it.)
- **Offline:** download `combined.html` and open it directly in any modern browser. No build step, no server.

> Surface-level links only. Per-objection deep-link grammar inside `#/library` is **not yet resolved** against the router and is deliberately not published here. Use the three surface routes above.

---

## What it looks like

**Argument Flow — Map 1, the next-move predictor.** Pick a source objection; the map renders predicted successor moves across the selected archetype (here: *blended*), with convergence-tier and mode annotations.

![Argument Flow / Map 1](screenshots/argument-flow-map1.png)

**Real-world examples — attested in the wild.** Every catalogued move is grounded in an observed deployment, with provenance and a bounded (<15-word) quotation.

![Real-world examples surface](screenshots/real-world-examples.png)

Further views — the dependency graph, the mechanism web, an objection-detail deconstruction with RSI, and the surface chrome — are in [`screenshots/`](screenshots/) and walked through in [`instructions.md`](instructions.md). A standalone `rwe.html` packages the real-world-examples surface for direct viewing or downstream tooling.

> **Rendered-counter note (known lag at v3.8.3).** The static chrome in the dependency-graph and mechanism-web headers currently reads **78 objections / 245 dependencies** — the v3.7-line values. The v3.8.0 cut moved the canon-attested truth to **81 objections / 254 dependencies**, so the chrome now lags by the three nodes added in that cut. The correction is byte-neutral (`78`→`81`, `245`→`254`, equal digit-width) and is queued as an operator-elective chrome fix; the underlying data and graphs render all 81 objections correctly.

---

## The deliverable

The shippable artifact is a single file: **`combined.html`**. Library, real-world-examples table, and coda are absorbed into it behind the outer hash router. Works offline, no build step.

**Verbatim-artifact provenance (the integrity contract):**

| Field | Value |
|---|---|
| File | `combined.html` |
| Version tag | `v3.8.3` |
| md5 | `dbbbc6d1b993b20064ad0a6d9f27b051` |
| Size | `2,346,607` bytes |

That md5 is binding. The file ships **verbatim** — no regeneration, no whitespace cleanup, no key reordering. A drifted hash is a corrupted artifact (cross-platform line-ending conversion is the usual culprit; the repo's `.gitattributes` enforces LF).

The binding integrity source is the project canon's `archive_attestation` block (canon **v37.3**, `archive_attestation.v3_8_3`; invariants anchor `8727787c5c0d4f8a08280b806db6fcc8`, held byte-identical across the v3.8 line; gates G1–G6 + validator self-test/corpus PASS).

---

## Status

**Stable at v3.8.3** (canon v37.3 line). The prior "archived, no-successor" framing of the v3.7 line was **superseded by an operator-elective resumption**: the long-deferred **v3.8.0 structural cut** landed (+3 objections, +1 mechanism, topology re-derived), followed by three rebuttal-strengthening foldins.

- **v3.8.0 (MINOR)** — the structural cut. Invariants subtree mutated for the first time since v3.7-stable (anchor `f6b94bf0…` → `8727787c…`): **78 → 81 objections** (`eliminativism` T4, `solipsism` T4, `suffering-as-meaning` T2), **34 → 35 mechanisms** (`mech_Metaphysical_Deflation`), dependency graph 91→94 nodes / 245→254 links, mechanism web 112→116 / 133→140. Map 1 held at 78 nodes / 2,886 edges. RWE schema v1.6→v1.7; validator v1.6→v1.7.
- **v3.8.1 / .2 / .3 (PATCH)** — long-form strengthens of `violence-as-reductio` (→ 86.2 B), `negative-util-aggregation` (→ 84.0 B), and `joy-outweighs-harms` (→ 83.0 B), plus a batched index/combined score-layer parity reconciliation. Invariants byte-identical across all three (`8727787c…`).

The **deployment × grade danger quadrant remains empty**: the three highest-deployment objections — `violence-as-reductio` (27 RWE), `benatar-asymmetry-attack` (15), `ai-fear` (10) — are all B-band. Grade distribution (long, n=81): **A 36 / B 34 / C 11 / 0 ungraded**.

See [`CHANGELOG.md`](CHANGELOG.md) for per-release detail across the v3.7 and v3.8 lines.

---

## What's in the single file

`combined.html` carries three surfaces behind the hash router:

- **`#/library`** — the 81-objection taxonomy across 5 tiers, the 35 mechanism attributions, the dependency graph (**94 nodes** = 81 objections + 13 premises; **254 links**, 167 strong / 87 weak), the mechanism web (116 nodes, 140 links), and the force-directed Map 1 across the four archetypes (2,886 transition edges across 78 source-keys).
- **`#/rwe`** — the 136 attested real-world deployments (171 attachment edges), schema v1.7.
- **`#/coda`** — the closing artifact on the axiom this library does not derive.

The regenerable sources behind the single file — the authoritative corpus JSON, the denormalized JSX sibling, the canonical HTML source, the RWE schema (v1.7), and the v3′-strict + v1.7 validator — remain in the source tree and are **not deprecated**. See [`instructions.md`](instructions.md) for programmatic use and the per-file integrity set.

---

## Reading

Open the library, land on `#/library`, pick a tier 1 or tier 2 objection, read its responses, then follow a few archetype transitions outward. Open `#/coda` *after* — not before — the taxonomy feels familiar. Then return to the library with the coda's framing in mind.

For a longer guide — archetype semantics, the dependency graph, real-world-examples, programmatic use, integrity verification — see [`instructions.md`](instructions.md). For corpus-level numbers (transition counts, grade distribution, the deployment×grade danger quadrant, the RSI calculus), see [`STATISTICS.md`](STATISTICS.md).

---

## Cite

A `CITATION.cff` (CFF 1.2.0) is provided at repository root and enables GitHub's "Cite this repository" widget. BibTeX:

```bibtex
@misc{efilist_argument_library_2026,
  title   = {efilist argument library},
  author  = {Cooper, Josiah S.},
  year    = {2026},
  version = {3.8.3},
  url     = {https://github.com/alisendjsc-crypto/efilist-argument-library},
  note    = {Stable release, v3.8 line}
}
```

---

## License

- Corpus, JSX, schema, single-file HTML (`combined.html`), coda: **CC-BY-4.0**. Attribution required; no share-alike obligation.
- The v3′-strict + v1.7 validator (`v3prime_validator_v1_7.py`): **MIT**.

Attribution per `CITATION.cff`. Verbatim citation and adaptation both require attribution under CC-BY-4.0; the validator code is permissive.

> **Note on GitHub's "Unknown" license badge.** GitHub's license detector matches a single root `LICENSE` against canonical SPDX bodies. The current `LICENSE` is a human-worded CC-BY-4.0 *summary*, and the repo is content/code dual-licensed (`LICENSE` = CC-BY-4.0, `LICENSE-CODE` = MIT), neither of which GitHub auto-detects. To make the badge read **CC-BY-4.0**: replace the body of `LICENSE` with the verbatim canonical CC BY 4.0 legal text and move the custom attribution prose into a `NOTICE` file. This is an operator-elective cosmetic fix — the licensing of the work is unaffected and fully stated above.

---

## On the standpoint

The library does not derive the suffering-priority axiom from anything more basic and does not pretend to. The coda is the explicit account of that floor. The descriptive content — the taxonomy, the dependency graph, the mechanism attributions, the attested examples — stands as observation regardless of where you land on the axiom itself.

The library ends here. What remains is the act of standing on it.
