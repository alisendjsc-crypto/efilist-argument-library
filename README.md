# efilist argument library

A structured taxonomy of objections to antinatalism. 78 objections across 5 tiers, attached to 34 psychological mechanisms, with 136 attested real-world deployments mapped to four interlocutor archetypes — sophisticate, defender, drifter, blended.

This is taxonomic work, not advocacy. The objections are catalogued as live moves in real discourse, not strawmen and not specimens. The descriptive content stands as observation regardless of whether you share the suffering-priority axiom; the closing **coda** makes that axiom visible as a stake rather than a derivation. Read both.

---

## The deliverable

The shippable artifact is a single file: **`combined.html`**. Library, real-world-examples table, and coda are absorbed into it behind an outer hash router (`#/library`, `#/rwe`, `#/coda`). No build step, no server, works offline — open it directly in any modern browser.

**Verbatim-artifact provenance (the integrity contract):**

| Field | Value |
|---|---|
| File | `combined.html` |
| Version tag | `v3.7.1` |
| md5 | `dd2abd01a43c2f173c98aa1b8c88bcbb` |
| Size | `2,234,272` bytes |

That md5 is binding. The file ships **verbatim** — no regeneration, no whitespace cleanup, no key reordering. A drifted hash is a corrupted artifact (line-ending conversion on cross-platform pulls is the usual culprit; the repo's `.gitattributes` enforces LF).

<!-- TODO: screenshot -->

---

## Status

**Archived stable** at v3.7.1 (canon v27.x; `project_terminal_state: archived_v3_7_1_stable`). v3.7.1 is a PATCH over the v3.7 line — surface consolidation into the single-file distribution plus count/invariant reconciliation; corpus content is unchanged at 78 objections. No scheduled successor; no forcing function for v3.8. Future maintenance is operator-elective and topic-scoped.

If you find an objection missing or a mechanism mis-attached, that's a topic for a future operator-elective micro-session, not a patch to this release.

---

## What's in the single file

`combined.html` carries three surfaces behind the hash router:

- **`#/library`** — the 78-objection taxonomy across 5 tiers, the 34 mechanism attributions, the dependency graph (91 nodes — 78 objections + 13 premises; 245 links, 161 strong / 84 weak), and the force-directed Map 1 across the four archetypes.
- **`#/rwe`** — the 136 attested real-world deployments, schema v1.6.
- **`#/coda`** — the closing artifact on the axiom this library does not derive.

The regenerable sources behind the single file — the authoritative corpus JSON, the denormalized JSX sibling, the canonical HTML source, the RWE schema (v1.6), and the v3'-strict + v1.6 validator — remain in the source tree and are **not deprecated**. `release_manifest_v3_7_1.json` carries md5/sha256 for the full set.

---

## Reading

Open `combined.html`, land on `#/library`, pick a tier 1 or tier 2 objection, read its responses, then follow a few archetype transitions outward. Open `#/coda` *after* — not before — the taxonomy feels familiar. Then return to the library with the coda's framing in mind.

For a longer guide — archetype semantics, the dependency graph, real-world-examples, programmatic use, integrity verification — see [`instructions.md`](instructions.md).

---

## Cite

A `CITATION.cff` (CFF 1.2.0) is provided at repository root and enables GitHub's "Cite this repository" widget. BibTeX:

```bibtex
@misc{efilist_argument_library_2026,
  title   = {efilist argument library},
  author  = {Cooper, Josiah S.},
  year    = {2026},
  version = {3.7.1},
  url     = {https://github.com/alisendjsc-crypto/efilist-argument-library},
  note    = {Archived stable release}
}
```

---

## License

- Corpus, JSX, schema, single-file HTML (`combined.html`), coda: **CC-BY-4.0**. Attribution required; no share-alike obligation.
- The v3'-strict + v1.6 validator: **MIT**.

Attribution per `CITATION.cff`. Verbatim citation and adaptation both require attribution under CC-BY-4.0; the validator code is permissive.

---

## On the standpoint

The library does not derive the suffering-priority axiom from anything more basic and does not pretend to. The coda is the explicit account of that floor. The descriptive content — the taxonomy, the dependency graph, the mechanism attributions, the attested examples — stands as observation regardless of where you land on the axiom itself.

The library ends here. What remains is the act of standing on it.
