# Right to Die - skeleton handoff (to library-Claude + Josiah)

v0.1 - built by wuld.ink Cowork, 2026-06-22 - efilist commit `753aa0f` (atop `013abd1`).
Empty plumbing only. Flagship antinatalism library UNTOUCHED. NO pin move, NO deploy this session.

This is the relay back into the lane the Suite Charter v0.1 + the Cowork handoff opened. Cowork
built the vessel; you (library-Claude + Josiah) fill it. Everything below that I *decided* was a
forced call to keep the plumbing coherent - each is cheap to change. Flag any you'd author
differently; none of it is load-bearing on your content.

---

## 1. What's in the vessel

| File | Role / contract it enforces |
|---|---|
| `right_to_die_corpus_v0_1.json` | The corpus. Sized-down mirror of the flagship node shape. 2 seed STUB nodes (tiers 1 + 3), zero real content. Single source of truth for objection data. |
| `combined.html` | Render surface. FETCHES the corpus at runtime (never inlines it). tab(s) - tier filter - response-depth toggle (punch/deconstruct/dismantle = short/medium/long) - keyword detection - `#obj-<id>` deep-links. NO graph subsystem. |
| `right_to_die_grading_ledger.json` | RSI grades live HERE (only). Empty: `ungraded:[]`, `grades:{}`. Carries `band_thresholds` + an `entry_shape_reference` documenting a real grade entry. |
| `build_right_to_die_index.py` | Search-export generator. Deterministic, validator-gated. Emits the index below. |
| `right-to-die-objections-index.json` | Generated search export (regenerable). `{schema_version, library, surface_route, objections:[{id,title,gloss}]}`. wuld.ink vendors this when it deploys. |
| `right_to_die_validator_v0_1.py` | `--self-test` = 15 synthetic fixtures + a live leg over the seed corpus+ledger. Your pre-commit gate. |
| `HANDOFF.md` | This file. |

---

## 2. Ambiguities I resolved - RATIFY or OVERRIDE

Each was open or self-contradictory in the charter/handoff. My call + why + how to change it.

**a. RSI grades live in the LEDGER only - not on corpus nodes.**
The handoff's node-field list named RSI slots `{v,s,c,r,a,geomean,band}` AND specified a ledger.
Two homes = a drift source (the project's cardinal sin). I put them only in the ledger, flagship-
faithful. Override: if you want per-node co-location, add the slots to nodes and I/you drop the
ledger's `grades{}` as the store - but pick ONE.

**b. The tier filter is DATA-DERIVED, not a hard-coded 1-5.**
The render builds its tier buttons from the tiers actually present in the corpus. This honors the
charter's "tier count + enumeration are AUTHORED, not scaffolded." The corpus `tiers` map is a
PROVISIONAL label reference (the inherited 5-tier frame), NOT authoritative. Author whatever tier
set you want; the machine follows. Update/trim the `tiers` labels to match.

**c. Count guard = `corpus.totalEntries`, not a magic `EXPECTED_N`.**
The flagship hard-codes 81. A growing library can't. The build + validator assert
`len(objections) == totalEntries`. So: when you add nodes, bump `totalEntries` (and
`totalResponses` = count of non-empty response strings) or the gate fails - by design.

**d. `mechanisms[]` = strand tags, not `psychMechanism`.**
I used the Wing-1 strand vocabulary (harm / consent / sovereignty / compensation) as the node's
`mechanisms` array (empty in stubs), not the flagship's psych-mechanism string. Right to Die
carries all four. Override: if you want psych-mechanism strings too, add a field or repurpose.

**e. The export schema EXTENDS the flagship's.**
Flagship export is `{schema_version, objections:[{id,title,gloss}]}`. I added top-level `library`
+ `surface_route` so the future wuld.ink consumer builds cross-domain deep-links without hard-
coding each sibling's route. Additive, schema_version-gated. Per-entry shape `{id,title,gloss}`
is identical to the flagship.

**f. `gloss` source = the node's `diagnosis` field (a one-liner), distinct from `responses{}`.**
`title` = `trigger`; `gloss` = `diagnosis` collapsed + ~200-char word-boundary snippet (exact
flagship contract). So every node needs a `diagnosis` (it is also rendered as a line on the card).
`responses{short,medium,long}` is SEPARATE - the depth-toggle content. If a node has no diagnosis,
the export omits `gloss` for it (consumer treats it as `{id,title}`).

**g. Surface route base = `right-to-die/combined`.**
The deep-link target the export advertises (`<surface_route>#obj-<id>`). Provisional - confirm the
production route when this deploys (likely `library.wuld.ink/right-to-die/combined`).

**h. `_stub:true` marks the seed nodes; they're EXEMPT from grade-coverage.**
The validator won't demand a grade for a stub and will FAIL if a stub gets graded. Remove the 2
stubs when real nodes land (or keep one as a fixture - your call; if kept they stay exempt).

**i. Two seed stubs at tiers 1 and 3** - chosen only to exercise the tier filter across two values.
Arbitrary placeholders. Replace freely.

**j. Band thresholds co-located in the ledger** (`A>=0.88 / B>=0.82 / C>=0.76 / D<0.76`); the
validator cross-checks `ledger.band_thresholds == canonical`. Banding is on the UNROUNDED fraction;
`rsi_pct` (1 dp) is display-only. (Charter-inherited; recorded here as the single machine source.)

---

## 3. Still YOURS to decide (charter "honest residuals" + what authoring will surface)

- **Tier count + objection enumeration** - the prose work; the vessel imposes nothing.
- **mechanisms vocabulary** - pure strand tags, or strand + psych-mechanism hybrid? (see 2d)
- **Compensation's three forks** (liberty->claim-right; who-owes / lean on the obstruction-charge
  (b); universal vs conditional). Right now these are prose inside `responses`. If you want them
  queryable, decide a field (e.g. `compensation_basis` or `strand_forks`) and I/you add it + a
  validator check. Flag it before you author 20 nodes the hard way.
- **RWE**: `rwe_refs[]` is a slot pointing into `corpus.realWorldExamples[]` (empty now). Confirm
  you want the flagship RWE schema family (`real_world_examples_schema_v1_7.json`) vendored here, or
  a lighter shape. The validator does NOT yet check `rwe_refs` resolve - add that the moment RWE
  data lands. Append-only anchors apply to RWE ids too.
- **Headline grade convention**: the ledger uses `headline_grade_long` (= the long-depth grade),
  flagship-style. Confirm that's the headline you want.
- **Committed seed export**: `right-to-die-objections-index.json` currently holds the 2 stub
  entries. Fine to keep (it regenerates on every content change) or empty it - your preference.
- **Sovereignty framing** (charter): ground in universal self-ownership; keep the American
  "live free or die" as RWE color only, never the load-bearing frame. A note for authoring, not a
  schema thing - flagged so it doesn't get lost.

---

## 4. How to author into it (mechanical)

1. Add nodes to `corpus.objections[]`. Required fields per node:
   `id, tier, category, trigger, keywords[], mechanisms[], diagnosis, responses{short,medium,long}, rwe_refs[]`
   (`sources[]` optional). `diagnosis` = the gloss one-liner. `responses` = punch/deconstruct/dismantle.
2. `id`: kebab, `^[a-z0-9][a-z0-9-]*$`, UNIQUE, **APPEND-ONLY** - never recycle an id (it is the
   permanent deep-link anchor `#obj-<id>`).
3. Bump `totalEntries` (= node count) and `totalResponses` (= count of non-empty response strings).
4. Grade into the LEDGER, not the node:
   `grades[id] = {graded:true, axes:{v,s,c,r,a}, geomean, short/medium/long:{rsi_pct,grade}, headline_grade_long}`.
   Band the UNROUNDED fraction; `rsi_pct` is 1-dp display only. Non-stub nodes must be in `grades` OR `ungraded[]`.
5. Regenerate the export:  `python3 build_right_to_die_index.py`
6. Gate before commit:  `python3 right_to_die_validator_v0_1.py --self-test`  -> must exit 0.
7. Drop the 2 `_stub` nodes when real content lands (or keep as fixtures).
8. Preview the render: it needs HTTP (it fetches the corpus). From this folder:
   `python -m http.server` -> `http://localhost:8000/combined.html`. Opening `file://` shows a
   "serve over HTTP" notice by design (the page never inlines the corpus = no drift).

---

## 5. Deploy / pin discipline (DEFERRED - for whoever ships it, not this lane)

- This vessel is NOT live. Corpus-internal work (authoring, validator runs) stays in the Argument
  Library lane, NO pin.
- When it ships content it becomes a **wuld.ink session**: that deploy forces, same-session,
  pin==live + search-index regen + re-vendor of `right-to-die-objections-index.json` into wuld.ink
  (the ccxxxvii cadence). The export's `surface_route` is what the wuld.ink consumer reads.
- **Nav-strip splice** (the thin `Harm & Autonomy | Anthropocentrism` strip above the flagship's
  top row) stays deferred until at least one sibling ships authored content - a switcher with one
  destination is dead chrome (charter).

---

## 6. Verification record (so the vessel is trustworthy as delivered)

- `right_to_die_validator_v0_1.py --self-test` -> exit 0 (15/15 synthetic fixtures + 0 live violations).
- Export determinism: built twice, byte-identical (727 B); committed export == fresh build; `schema_version:1`.
- Render: `node --check` clean; pure-logic harness 14/14 vs the seed corpus (tier filter 1/3/all,
  depth map, keyword detection, tier+keyword compose, deep-link resolve/reject); HTTP-200 serve of
  page + corpus (`application/json`).
- Anchor uniqueness + anchor-safe regex verified; append-only covenant documented + enforced.
- Flagship UNTOUCHED: `git status` showed only the new folder; zero diff to `combined.html`.

MD5s at delivery (commit `753aa0f`):
`corpus c1b2f128...` · `ledger c6972036...` · `build f45b504c...` · `validator 58449b41...` ·
`combined.html b22002a2...` · `export 5858d370...`
