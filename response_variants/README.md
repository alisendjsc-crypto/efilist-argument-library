# response_variants/ — another answer, labelled as not the library's chosen line

**Ruled 2026-10-04.** Josiah's word, said to seat l (V5) at the user turn and recorded verbatim in canon
`adversarial_map.his_words_V6`: *"Proceed with your recommendations on all of the above."* It adopts RV-1..RV-8 of
the responseVariants design (`design/variations/RESPONSE_VARIANTS_design_v0_1.md`) as leaned; the rulings are in canon
`adversarial_map.response_variants_rulings_V6`. Built by V6 (seat l).

**Not served, not canon.** Nothing here is under `site/`, and no corpus byte carries a `responseVariants` key yet. A
variant reaches the flagship only in a declared pin, after a seat that did not draft it judges it and he rules (RV-4).
The game does not vendor it (RV-5).

| file | what it is |
|---|---|
| `response_variants_schema_v0_1.json` | The contract (design section 2): a top-level `responseVariants` list on a node, never under `responses` (RV-1). Each entry: `variant_id`, `type`, `varies` {locus, anchor}, `text`, `residual` {where_both_stop, concedes {library, account}, status}, `account_sources`, `provenance`. The closed type table (RV-2) holds one type, `relief-account`, with its fixed label and "the library's author" (RV-3); the label is copied from canon's `label_leaned`. A staging file is `{meta, variants}`. |
| `response_variant_validator_v0_1.py` | RV-6's checks, exactly the design's list: ids, the closed type, one variant per (node, type), the long's anchor (at most 15 words, verbatim, unique), the 120-300-word ASCII text, the open residual, the no-win floor, his safety bar as floors (gate2's EXIT and L6's WIDE, imported from `adversarial_map_staging/r1/sp_reading_l6.py` at its md5; the design's pro-life list), `account_sources` resolving to his verbatim words in the canon the file pins, and coverage declared per file. Two modes: staging files, and `--embedded` (the corpus's own list; none today). |
| `response_variant_validator_control_v0_1.json` | The `--self-test` record: the unmutated control first, one mutation per check, every check turned RED, real-data controls on the corpus and canon at their pins (the seven measured anchors), byte-identical under two hash seeds. It also lists his ten accounts against the floors and the ASCII rule, for the drafter. |

Run before and after any touch:

```
python3 response_variants/response_variant_validator_v0_1.py --self-test --check
python3 response_variants/response_variant_validator_v0_1.py --embedded
python3 response_variants/response_variant_validator_v0_1.py <fragment.json>
```

A floor is not a census: gate2 still reads every variant against his bar. The pilot's seven nodes (RV-7) live in the
relief variant's builder, read from the design's measurement record at its md5, not in the validator.
