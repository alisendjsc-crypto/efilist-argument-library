# argument_shapes/ -- the same objection, a different argument (V1)

Seat l, V1, 2026-09-26. **Not served** (`site/` is the served tree) and **not canon**. V2 (2026-10-03)
drafted the pilot: 10 shapes over the six R-V4 nodes. gate2 judged it in V3 (2026-10-03): 5 ACCEPT, 2 AMEND,
3 REJECT; judged, not ruled. Then, on his word, V4 puts the (a) shapes in the corpus and renders them on the
flagship.

Built from the variations design v0_1, sections 3 and 4 (`design/variations/VARIATIONS_design_v0_1.md`,
md5 `fcf6f6fe`). His word on its six rulings: *"Go with your leans on all of the rulings."* That word is
recorded in canon v38.42, `adversarial_map.variations_rulings_V0`.

## Files

| file | what it is |
|---|---|
| `argument_shapes_schema_v0_1.json` | The contract, as a JSON Schema. It covers a staging file (`{meta, shapes}`) and the shape object that a corpus node carries in its top-level `argumentShapes` list. |
| `shape_validator_v0_1.py` | The validator: 18 checks. It runs over staging files, or over the corpus's own shapes with `--embedded`. |
| `shape_validator_control_v0_1.json` | The self-test record: 59 cases, the unmutated control first, and every one of the 18 checks turned RED by a mutation. It is byte-identical under two hash seeds. |
| `shapes_pilot_v0_1.json` | The pilot (V2): 10 shapes, `bound_for: "staging"`, phase S, pinned to corpus `7b6e65e5`. Classes a2 b2 c1 d5. Validator PASS, 0 violations. |
| `shapes_pilot_measure_v0_1.json` | The pilot's measurement (design section 5): the cross-node share, the classes against R1, words per shape, the bar for a different shape, each (d)'s bedrock copied from the map and register, the collision check with the drafter's reading, the dropped candidates. |
| `build_shapes_pilot.py` | Builds both from the shapes it holds; `--check` reproduces them byte for byte. |
| `shapes_pilot_judgments.json` | gate2's judgment (V3): 23 rows, append-only. Each shape read four ways (the routing by R1's method, the strongest form, a shape and not a surface, the source makes the move) plus its class; the three pulls; the measurement. Every quote verbatim at pinned bytes. |
| `shapes_judgments_gate.py` | The gate on that record: pins, coverage, routes, quotes, figures, append-only history. `--self-test` runs `shapes_judgments_gate_control_v0_1.json` (16 cases, the unmutated record first). |
| `shapes_judgment_reading.py` | gate2's reading instrument: every figure the record states, recomputed from the judged artifacts at their md5s, into `shapes_judgment_reading_v0_1.json`; `--check` reproduces it. Needs the game's repository (the scholar lines). |

## The rules it enforces

- **Where a shape lives:** `argumentShapes` is a top-level node key, beside `objectionSubforms` (R-V1).
  It is never under `responses`, because the game embeds `responses` whole.
- **What the corpus may carry:** class (a) shapes only (R-V2). A staging file may hold (a), (b), (c) and (d)
  shapes, and must say which class each one is. A file with `meta.bound_for: "corpus"` fails on anything
  that is not (a).
- **The answer:** every (a) and (b) shape names at least one answering locus as `<node-id>#<locus>`, with
  an anchor. The anchor is at most 15 words and verbatim at that locus (F5: a routing names the answering
  sentence, not only its locus).
- **The same code as the map:** loci are checked by map validator v0_6's `locus_valid`, loaded at its
  pinned md5 `c002e938`. So `archetypeVariants.<slot>` and `note` are existence-gated exactly as they are
  on the map. v0_6 has no anchor function: it computes its anchor rule inline. `anchor_ok()` restates that
  one expression over v0_6's own `locus_text` and `wc`.
- **Attestation:** each `attested_by` item is either a `realWorldExamples` `instance_id` attached to *this*
  node, or `{"citation": "author, title, year, locator"}`.
- **The statement:** 30-70 words, ASCII, and no standalone dash token (v0_6's `DASH_TOKEN_RE`).
- **The label:** 3-6 words.
- **The cap:** at most 3 shapes per node, across every file loaded together.
- **Coverage:** `meta.shape_coverage` is required, and it is gated against its own file alone (ccclxx).
- **Provenance:** the phase is `S`, a new letter kept disjoint from the map's PHASES.
- **The corpus pin:** a staging file pins its corpus by whole-file md5 (`meta.source_corpus_md5`), and
  optionally by the objections digest. The validator reads the corpus at that md5 through
  `adversarial_map_staging/r1/pinned.py`, so a later pin cannot turn a true file RED.

## Run it

```bash
python3 argument_shapes/shape_validator_v0_1.py --self-test --check
```

```bash
python3 argument_shapes/shape_validator_v0_1.py --embedded
```

```bash
python3 argument_shapes/shape_validator_v0_1.py <fragment.json> [...]
```

`--embedded` passes on today's corpus with 0 shapes: it proves the key is absent, nothing more.
`--self-test --write` regenerates the record. Do that only after a deliberate change to the validator,
and never to make a check pass.

## Not done here, on purpose

- **The map validator is not bumped.** `argumentShapes.<shape_id>` becomes an existence-gated map locus at
  the successor map's validator bump (R0194's sequence). Until then, the map cannot hold an adversarial
  entry against a shape.
- **Some checks are gate2's, not the machine's.** The validator cannot tell whether a shape is really a
  different argument from the trigger, the layman line and the scholar line, or whether its statement is
  the strongest form (K346). Nor can it tell whether the source really makes the move. Those are gate2's
  reads in V3 (design section 4).
- **The "one sentence" in `differs_by` is not machine-checked.** The validator checks only that it is a
  non-empty ASCII string.
