# adversarial_map_staging — the adversarial objection/rebuttal map (LIBRARY-INTERNAL, staged)

Home of the adversarial map program: for each of the 82 shipped v4.0.0 nodes, the strongest continuation a maximally competent hostile interlocutor deploys **against OUR text as written**, triaged into four disposition classes — the fidelity-ceiling mechanism inverted (overshoot promoted from exception to product). Commission: `adversarial_map_commission_relay_v1.md` (game-folder root, author-relayed). Design: the library K220 seat (Exchange 151, `K220_fold_relay_v1.md` `a49935a2`). Ratifications Q1–Q3 arrived RATIFIED AS STATED (ratify-by-transmission: the relay was pasted unedited).

**Contract.** Nothing in this directory is live, pinned, rendered, or canonical. The directory is **version-neutral** deliberately: (b)/(c) yields route to whichever future bundled cut ratifies them — no entry authorizes a byte; (b)/(c) yields are intake candidates routing through the normal staging → cold-grade → assembly chain. The map is LIBRARY-INTERNAL until a deliberate fold decision: own-surface shipping = an ordinary no-pin aux-wing fold runnable any session; any graft into `/combined` = a stance-layer change — Josiah + library-Claude ratify first, then a deliberate, isolated pin-move session. GitHub Pages serves these files raw at `library.wuld.ink/adversarial_map_staging/*` — unlinked and unindexed (the same class as `v4_staging/`).

## Contents

- `adversarial_map_design_v0_1.md` (`49514ec9`/7,722) — the design: entry schema, class law (a→c→b/d), the four anti-inflation gates (anchor rule · force floor · (a)-brevity ≤60 · regress stop), tier-descending phasing, staging, budgets, per-fold Cowork obligations, validator spec (§6).
- `adversarial_map_schema_v0_1.json` (`dacd818f`/3,143) — machine sibling; the ENTRY schema, id-closed against corpus `6ee1f6f3`/82.
- `adv_map_validator_v0_1.py` (`34fefb95`) — fragment/assembly validator implementing design §6. `--self-test` 24/24 (good fixture + 23 loud-fail cases); proven against the real corpus at K221 (one-per-class seed PASS + 9 bad mutations tripped). **Superseded by v0_2 but never mutated** — canon pins this blob and the K228–K231 receipts cite its output. Keep it on disk, keep it byte-identical.
- `adv_map_validator_v0_2.py` — the current validator. Every v0_1 check carried forward verbatim (the two agree ok-for-ok, fail-for-fail on all 16 shared checks against A+B1+B2+C), plus four additions. `--self-test` 36/36. Usage:
  `python3 adversarial_map_staging/adv_map_validator_v0_2.py <fragment.json> [...] --corpus efilist_argument_library_v4_0_0.json [--terminal] [--assembly]`

### What v0_2 adds

1. **Phase `E`.** v0_1's phase enum stopped at `D`, so a T1 fragment could not be validated at all.

2. **`objections-digest`** (hard when declared, skipped when absent). K332 root cause: four release relabels walked the corpus `version` field 4.0.0 → 4.0.4 while every objection stayed byte-identical. One content cut wore five whole-file md5s, and every fragment pinning `6ee1f6f3` failed `meta-corpus-pin` — which silently disabled **seven** downstream checks including `anchor-rule`, the program's core verbatim discipline. A whole-file md5 measures the envelope, not the text the anchors are cut from. Fragments may now also declare `source_corpus_objections_md5`, a digest over the objections array alone (`sort_keys=True`, so key reordering can't move it either). Get it from `--print-digest`. Corpus `6ee1f6f3` → objections digest **`0218f73b`**. New fragments should carry both pins: the whole-file md5 says *which file*, the digest says *which text*.

3. **`b1-bradley-bar` / `b1-hedonic-crossref`** (advisory; hard under `--assembly`). Phase B1 predates both carry-forward constraints. **K224 bars routing an (a) into `bradley-no-subject#long` for a comparative-harm move** — because bradley answers such moves by asserting non-comparative wronging, which is itself unsettled bedrock (`HR-05`), so the route treats a bedrock commitment as a settled answer. K229 scopes that bar to comparative-harm moves. K230 calls the cross-ref the hedonic-contrast route leans on broken. Neither predicate is machine-decidable — *"is this a comparative-harm move"* is an editorial judgment — but **whether it was adjudicated** is. An (a)-entry routing into a constrained locus clears by naming the constraint in its `grounds` with a token, matched as a **prefix** so the suffix can name the disposition the ruling actually reached:

   | routing target | token prefix | canonical suffixes |
   |---|---|---|
   | `bradley-no-subject#long` | `[K229-` | `[K229-comparative]` (bar bites) / `[K229-not-comparative]` (bar clears) |
   | `transhumanist-objection#long` | `[K230-crossref` | `[K230-crossref-repaired]` / `[K230-crossref-not-load-bearing]` |

   The token asserts the ruling was **made**, not that it came out clean; the prose carries the reasoning. Prefix matching exists so an author is never forced to attest a disposition the ruling did not reach — an entry adjudicated *not* comparative-harm would otherwise have to claim a repair that never happened. These fire on exactly the five B1 entries the succession brief names — `free-will-defense`, `procreative-liberty`, `consent-incoherent`, `non-identity-problem` (bradley) and `hedonic-contrast` (transhumanist). That is the point: the debt is standing and stays visible on every run until it is paid. `non-identity-problem` is the likeliest breach, since it *is* the no-worse-off-baseline problem.

4. **`move-ascii`** (advisory; hard under `--assembly`). The move gate has always read *40–150 words, ASCII, no standalone dash tokens*. v0_1 mechanized the word band and neither of the others. Mechanizing ASCII now **registers a live breach rather than inventing one**: eight Phase A moves carry U+2014, and zero moves in B1, B2, C or D do. Phase A predates the discipline.

### Severity model

| label | meaning |
|---|---|
| `PASS` / `FAIL` | hard check. Any `FAIL` sets exit 1. |
| `WARN` | advisory. Reported on every run, never sets exit 1 on its own. |
| `--assembly` | promotes every advisory to hard and implies `--terminal`. **The assembly step into `adversarial_map_v1_0.json` must run with it.** |

Advisories exist so a constraint ratified *after* an artifact shipped stays loudly visible without retroactively failing four ratified fragments. `--assembly` is the one moment the debt must be paid rather than displayed.

- `adv_map_phaseD_v0_1.json` — Phase D, T2, n=17, 10a / 3b / 0c / 4d, K231's fragment verbatim. `session_K231_state.json` is its authoring receipt: it carries the per-entry routing, the four carry-forward checks (all PASS — notably CF4, the `nihilism-label` watch on the act/omission-default-under-skepticism overclaim, cleared at origin) and six open questions.
- `adv_map_phaseE_v0_1.json` — **Phase E, T1, n=13. The tier-descending sweep is complete: every one of the 82 nodes now carries at least one entry.** 5a / 5b / 1c / 2d. Built by `build_phaseE.py`, which verifies every anchor verbatim at its named locus, every word band, the entry cap, id×anchor uniqueness, ASCII purity and the absence of standalone dash tokens *before* writing, and refuses to write on any failure. First fragment to carry `source_corpus_objections_md5`.

  **It carries the program's first (c).** Zero (c) across the previous 69 nodes had two readings — the corpus is individuation-complete, or the bar is too high. It was the bar, and the cause is procedural: every phase adjudicated node-against-node, which leaves a *corpus-level* objection nowhere to land. `diagnosis-not-refutation` (tier guess 5, presupposition-inversion) is the objection that the rebuttals commit the genetic fallacy they convict the objector of. Measured before it was ruled: 26 of 82 nodes deploy diagnostic vocabulary inside their responses; the rule forbidding it appears in exactly 2 (`just-depressed#long`, `life-gift#long`); T5 holds nothing method-level.

- `honest_residuals_register_v0_1.json` / `.md` — the (d) consolidation the design doc schedules for terminal assembly. **It is an INPUT to phase authoring, not only an output.** Every (d) carries a `novel` boolean; with no register a phase author decides it from memory of preceding phases, which is a recall test rather than a discipline, and it has been failed once (the succession brief records N1 as first registered in Phase D; the shipped B2 fragment carries its birth certificate at `phenomenological-existentialism` with `novel: true`, and B2 precedes D). 26 (d) entries, **22 distinct free-text bedrock names collapsing to 12 actual bedrocks**. Phase E was authored against it and both its (d) entries were decided by lookup, introducing no new birth certificate.

  Two audits. The **birth-certificate** check refuses to write when a bedrock carries more than one `novel: true` — under-individuation. The **adjacency** check derives candidate pairs from two signals (a `terminus_routing` naming another bedrock; a corpus node feeding two bedrocks), cutting 66 possible pairs to 4, and refuses to write while any detected pair goes undeclared — so an empty `relations` list is an assertion of independence, never a default. The signals are a **floor on what must be adjudicated, never a ceiling**: `HR-04`+`HR-07` is a real dependency neither fires on, found by hand.

- `build_register.py` / `render_register.py` — run from this directory: `python3 build_register.py [--with-d] [--with-e]` then `python3 render_register.py`. Everything is derived except `BEDROCK_MAP` and `RELATIONS`, which are the editorial acts, and both are audited against the fragments before writing.

### Decision artifacts and evidence

- `adversarial_map_assembly_rulings_v0_1.json` / `.md` — all five assembly decisions of the succession brief §2.5, ruled. **The K224 bar reads as a PROHIBITION, not a licence**: routing an (a) into `bradley-no-subject#long` for a comparative-harm move is barred, because bradley answers such moves by *asserting* non-comparative wronging, which is unsettled bedrock (`HR-05`). Adjudicating B1's five carry-forward entries against it gives **2 breaches** (`procreative-liberty`, `non-identity-problem` — proposed to reclassify (a)→(d)) and 3 clears. Proposed, never applied: those fragments are ratified and are not rewritten without a ruling.

- `adversarial_map_regen_queue_v0_1.json` / `.md` — the v-cut scoping input. **21 (b) + 1 (c) across 21 nodes, 26% of the corpus.** Version class ruled as a split: **v4.1.0** for the 19 enrichment regens (v3.9 was opened as the enrichment line), **v5.0.0** for the node intake (v4.0.0 was MAJOR *because* it was intake, 81→82 renumbered). Split rather than bundled so nineteen prose corrections are not hostage to the single most contestable item in the program; the ordering was measured, not assumed, by scanning every (b)'s grounds for intake-coupling.

- `process_ledger_v0_1.md` — the discrete-notes surface: **eight failure shapes, not a list of incidents.** The hazard registry in wuld-ink's `CLAUDE.md` is the record of authority and numbers things in the order they went wrong, which is the right record and the wrong teacher — the next failure never arrives wearing the last one's costume. `claude_md_hazard_registry_snapshot.txt` carries the cited headlines so `build_ledger.py` can verify every numeral without reaching across repos.

- `calibration_phaseD_rederivation_v0_1.json` — **superseded as a selection, retained as evidence.** The wuld-ink re-derivation of Phase D (4a/12b/0c/1d). Deliberately named so it cannot be globbed as a phase fragment. Kept because the locus finding above has no evidence without it: had it landed it would have produced **nine fabricated regen candidates**, taking the v4.1.0 cut from 21 (b) to 30 and its corpus footprint from 26% to 37%.

## Container contract (fragments emit this shape; the schema pins the ENTRY, this README + the validator pin the CONTAINER)

```json
{ "meta": { "source_corpus": "efilist_argument_library_v4_0_0.json",
            "source_corpus_md5": "<full md5 of the corpus file — 6ee1f6f3…>",
            "source_corpus_objections_md5": "<v0_2, optional-but-preferred — 0218f73b…>",
            "class_counts": { "a": 0, "b": 0, "c": 0, "d": 0 },
            "coverage_distinct_ids": 0 },
  "entries": [ { "target_id": "…", "target_locus": "short|medium|long|diagnosis",
                 "target_anchor": "≤15-word verbatim substring at the locus",
                 "adversarial_move": "40–150 words (class a: ≤60)",
                 "class": "a|b|c|d", "grounds": "…",
                 "routing": { "<class-shaped — see the schema>" },
                 "status": "mapped",
                 "provenance": { "phase": "A|B1|B2|C|D|E", "date": "YYYY-MM-DD", "seat": "…" } } ] }
```

`class_counts`, `coverage_distinct_ids` and `source_corpus_objections_md5` are optional but validated against computed values when present. Canonical serialization: `json.dumps(indent=2, ensure_ascii=False)` + trailing newline (the validator's round-trip gate).

## Expected arrivals

**ALL SIX PHASES HAVE LANDED. The map is mapped-complete: 82/82 nodes, 93 entries, validator v0_2 terminal run 0 violations.**

Phase D is **K231's fragment, landed verbatim** (md5 `8d41db905561c4e32df33d41b4874bd5`, 36,701 B, authored 2026-07-17, 10a/3b/0c/4d) together with its authoring receipt `session_K231_state.json`. It was recovered on 2026-09-17 from the K231 chat's download cards, where it had been sitting undownloaded the whole time — which is why every disk, `archive/` and Release search came back empty.

**The calibration control paid for itself.** A wuld-ink re-derivation of the same 17 T2 nodes existed (4a/12b/0c/1d) and was within an hour of being folded. Diffing the pair against each other, rather than either against the corpus, found a defect no gate in this program can see:

- **Class agreement 5/17. Anchor agreement 0/17.** The two never engaged the same text.
- K231 targeted `long` 15 times; the re-derivation targeted `medium` 11 times. The long response is the corpus's most defended prose and `medium` is a condensation, so attacking `medium` finds gaps far more easily — which is the whole of 12b against 3b.
- **Eight of the re-derivation's twelve (b) entries never consider the long form at all.** The force floor says an entry is (a) if the *best reading of the shipped text* survives, and for a node shipping three depths that reading includes `long`.

**Locus discipline is now a program norm with numbers behind it: 77 of the map's 93 entries target `long`** (B1 16/16, B2 15/16, D 15/17, E 12/13; Phase A's 6 `medium` predate the norm). **Author against the deepest locus that addresses the objection, or state in the grounds why a shallower one was chosen.** The anchor rule permits any locus and says nothing about depth, so a phase can drift shallow without tripping a single check while its class distribution moves sharply. That is invisible to the validator and was invisible to five phases of review.

Note the re-plan recorded in K230's receipt but never propagated until canon v38.2: C delivered T3 only against a plan of T3+T2, so D = T2 (n=17) and E = T1 (n=13).

`adv_map_phase{A|B1|B2|C|D|E}_v0_1.json` fragments — Phase A = T5 (n=7), carrying the ELECTED Map-1 curation rider for `self-effacing-under-universalization` (**transition-spec artifact ONLY**; the `combined.html` splice it implies is a separate, deliberate pin-move session — electing the rider authorized design, not a surface byte) → terminal `adversarial_map_v1_0.json` = the **mapped-complete (pre-triage)** state (Q3). Coverage law (Q1): every node ≥1 entry, ≤3 entries/node.

**Status lifecycle** (`mapped → queued → ratified → landed(version) | rejected(grounds)`) lives in `project_canon` (`adversarial_map` block), never in these artifacts — entries carry `status: "mapped"` only.

**One flag for Phase A:** the validator reads the schema's move band literally — 40–150 words all classes, class (a) additionally ≤60 (net 40–60 for (a)). If the 40-word floor proves too tight for confident (a) routing data, that is a one-line validator amend — flag it in the fragment's session state rather than padding moves.
