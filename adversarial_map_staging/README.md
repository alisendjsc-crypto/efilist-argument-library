# adversarial_map_staging — the adversarial objection/rebuttal map (LIBRARY-INTERNAL, staged)

Home of the adversarial map program: for each of the 82 shipped v4.0.0 nodes, the strongest continuation a maximally competent hostile interlocutor deploys **against OUR text as written**, triaged into four disposition classes — the fidelity-ceiling mechanism inverted (overshoot promoted from exception to product). Commission: `adversarial_map_commission_relay_v1.md` (game-folder root, author-relayed). Design: the library K220 seat (Exchange 151, `K220_fold_relay_v1.md` `a49935a2`). Ratifications Q1–Q3 arrived RATIFIED AS STATED (ratify-by-transmission: the relay was pasted unedited).

**Contract.** Nothing in this directory is live, pinned, rendered, or canonical. The directory is **version-neutral** deliberately: (b)/(c) yields route to whichever future bundled cut ratifies them — no entry authorizes a byte; (b)/(c) yields are intake candidates routing through the normal staging → cold-grade → assembly chain. The map is LIBRARY-INTERNAL until a deliberate fold decision: own-surface shipping = an ordinary no-pin aux-wing fold runnable any session; any graft into `/combined` = a stance-layer change — Josiah + library-Claude ratify first, then a deliberate, isolated pin-move session. GitHub Pages serves these files raw at `library.wuld.ink/adversarial_map_staging/*` — unlinked and unindexed (the same class as `v4_staging/`).

## Contents

- `adversarial_map_design_v0_1.md` (`49514ec9`/7,722) — the design: entry schema, class law (a→c→b/d), the four anti-inflation gates (anchor rule · force floor · (a)-brevity ≤60 · regress stop), tier-descending phasing, staging, budgets, per-fold Cowork obligations, validator spec (§6).
- `adversarial_map_schema_v0_1.json` (`dacd818f`/3,143) — machine sibling; the ENTRY schema, id-closed against corpus `6ee1f6f3`/82.
- `adv_map_validator_v0_1.py` (`34fefb95`) — fragment/assembly validator implementing design §6. `--self-test` 24/24 (good fixture + 23 loud-fail cases); proven against the real corpus at K221 (one-per-class seed PASS + 9 bad mutations tripped). Usage:
  `python3 adversarial_map_staging/adv_map_validator_v0_1.py <fragment.json> [...] --corpus efilist_argument_library_v4_0_0.json [--terminal]`

## Container contract (fragments emit this shape; the schema pins the ENTRY, this README + the validator pin the CONTAINER)

```json
{ "meta": { "source_corpus": "efilist_argument_library_v4_0_0.json",
            "source_corpus_md5": "<full md5 of the corpus file — 6ee1f6f3…>",
            "class_counts": { "a": 0, "b": 0, "c": 0, "d": 0 },
            "coverage_distinct_ids": 0 },
  "entries": [ { "target_id": "…", "target_locus": "short|medium|long|diagnosis",
                 "target_anchor": "≤15-word verbatim substring at the locus",
                 "adversarial_move": "40–150 words (class a: ≤60)",
                 "class": "a|b|c|d", "grounds": "…",
                 "routing": { "<class-shaped — see the schema>" },
                 "status": "mapped",
                 "provenance": { "phase": "A|B1|B2|C|D", "date": "YYYY-MM-DD", "seat": "…" } } ] }
```

`class_counts` and `coverage_distinct_ids` are optional but validated against computed values when present. Canonical serialization: `json.dumps(indent=2, ensure_ascii=False)` + trailing newline (the validator's round-trip gate).

## Expected arrivals

`adv_map_phase{A|B1|B2|C|D}_v0_1.json` fragments — Phase A = T5 (n=7), carrying the ELECTED Map-1 curation rider for `self-effacing-under-universalization` (**transition-spec artifact ONLY**; the `combined.html` splice it implies is a separate, deliberate pin-move session — electing the rider authorized design, not a surface byte) → terminal `adversarial_map_v1_0.json` = the **mapped-complete (pre-triage)** state (Q3). Coverage law (Q1): every node ≥1 entry, ≤3 entries/node.

**Status lifecycle** (`mapped → queued → ratified → landed(version) | rejected(grounds)`) lives in `project_canon` (`adversarial_map` block), never in these artifacts — entries carry `status: "mapped"` only.

**One flag for Phase A:** the validator reads the schema's move band literally — 40–150 words all classes, class (a) additionally ≤60 (net 40–60 for (a)). If the 40-word floor proves too tight for confident (a) routing data, that is a one-line validator amend — flag it in the fragment's session state rather than padding moves.
