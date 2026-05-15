# efilist argument library

A structured taxonomy of objections to antinatalism. 78 objections across 5 tiers, attached to 34 psychological mechanisms, with 136 attested real-world deployments mapped to four interlocutor archetypes — sophisticate, defender, drifter, blended.

This is taxonomic work, not advocacy. The objections are catalogued as live moves in real discourse, not strawmen and not specimens. The descriptive content stands as observation regardless of whether you share the suffering-priority axiom; the closing **coda** makes that axiom visible as a stake rather than a derivation. Read both.

---

## Status

**Archived stable** at canon v26.x. v3.7 is the stable release; no scheduled successor; no forcing function for v3.8. Future maintenance is operator-elective and topic-scoped. The substrate is md5-locked.

If you find an objection missing or a mechanism mis-attached, that's a topic for a future micro-session, not a patch to this release.

---

## What's here

```
corpus/                              authoritative corpus + JSX sibling
viewer/                              single-file HTML viewer (no build step)
coda/                                closing artifact — on the axiom this library does not derive
schema/                              real-world-examples schema (v1.6)
validator/                           v3'-strict + v1.6 attestation validator
process/                             archive-state canon + closeout session record
release_manifest_v3_7_stable.json    md5/sha256 attestation
CHANGELOG.md                         release notes
LICENSE                              CC-BY-4.0 (content)
LICENSE-CODE                         MIT (validator)
instructions.md                      usage guide — viewer, archetypes, programmatic use, integrity
.gitattributes                       LF preservation across cross-platform pushes
```

Filenames preserve their session-of-origin suffixes (`_v3_7_post_*`, `_v1_6`, etc.). The rename window opens at v3.8, not v3.7 — the suffixes are part of the audit trail.

---

## Reading

The viewer at `viewer/index_v3_7_post_b3f2_surface_parity_html.html` is a single-file SPA. Open it directly — no build step, no server, works offline. From there, the coda is reachable via the in-app link or at `coda/coda_v3_7.html`.

The structured form lives in `corpus/efilist_argument_library_v3_7_post_cluster_insertion_inmendham.json`. The schema describing the real-world-examples table is in `schema/`. The validator at `validator/v3prime_validator_v1_6.py` exercises v3'-strict + v1.6 attestation rules and passes self-test at 13/13.

The dependency graph (91 nodes, 245 links: 161 strong / 84 weak) anchors each objection to 13 premises — 9 foundational, 4 diagnostic. The objection space across the four archetypes is rendered as a force-directed map embedded in the viewer.

For a longer guide — archetype semantics, suggested reading order, programmatic use, integrity verification — see [`instructions.md`](instructions.md).

---

## Cite

`CITATION.cff` is forthcoming in a follow-up session. Until then, cite the repository and the `v3.7.0` tag:

```bibtex
@misc{efilist_argument_library_2026,
  title   = {efilist argument library},
  author  = {Cooper, Josiah S.},
  year    = {2026},
  version = {3.7.0},
  url     = {https://github.com/alisendjsc-crypto/efilist-argument-library},
  note    = {Archived stable release}
}
```

---

## License

- Corpus, JSX, schema, viewer HTML, coda: **CC-BY-4.0**. Attribution required; no share-alike obligation.
- `validator/v3prime_validator_v1_6.py`: **MIT**.

Attribution per `CITATION.cff` once authored. Verbatim citation and adaptation both require attribution under CC-BY-4.0; the validator code is permissive.

---

## On the standpoint

The library does not derive the suffering-priority axiom from anything more basic and does not pretend to. The coda is the explicit account of that floor. The descriptive content — the taxonomy, the dependency graph, the mechanism attributions, the attested examples — stands as observation regardless of where you land on the axiom itself.

The library ends here. What remains is the act of standing on it.
