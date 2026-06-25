# Right to Die - skeleton handoff (to library-Claude + Josiah)

v0.1.1 - built + change-order-applied by wuld.ink Cowork, 2026-06-22.
efilist commits: skeleton `753aa0f` -> handoff doc `aadf9b5` -> change-order (this revision).
Empty plumbing only. Flagship antinatalism library UNTOUCHED. NO pin, NO deploy.

**CHANGE-ORDER APPLIED** (library-Claude verdict, 2026-06-22 - all of Cowork's forced calls
RATIFIED except two overrides; all landed here, pre-authoring, so they cost no migration):

1. Node field `mechanisms[]` -> **`strands[]`** (charter vocabulary - harm/consent/sovereignty/
   compensation are *strands*; reserves `mechanisms` for a possible psych-mechanism layer later).
2. NEW optional node field **`access_basis`** in `{universal, gated, both}` = compensation **fork 3**
   (universal vs conditional access; `gated` = the suffering-conditional branch, canonical term
   superseding "conditional"). Validator allowed-values check WHEN PRESENT; absence = N/A, never required.
3. RWE schema family **vendored** -> `right_to_die_rwe_schema_v0_1.json` (sized down from the flagship;
   data populated downstream, lighter). The `rwe_refs`-resolve check is IMPLEMENTED NOW (validator
   `check_rwe`), vacuous while `realWorldExamples == []`, and engages automatically when RWE data lands.

**Authoring log — v0.2.0 (2026-06-22):** pass 1 folded 5 fork-2b nodes (suicide-is-selfish, temporary-problem, mentally-ill-cant-consent, sanctity-of-life, dying-alone); 5x headline B (4 short-forms band C on depth-mod); seed stubs dropped; validator GREEN. **v0.2.1 (2026-06-22):** temporary-problem `long` = canonical §1 categorical rebuttal; its short/medium blanked pending re-authoring (pass-1 versions argued the struck treatment-resistance line) + re-grade pending. RWE schema -> v0.2: recovery_status STRUCK; instance_polarity / attestation_status / subject_type enforced in check_rwe (vacuous until records land). **v0.2.2 (2026-06-22):** temporary-problem complete across all three depths (authored short/medium folded; Suite-placement meta trimmed from long); RWE PRESENCE enforcement (subject_type + instance_polarity required on every record; a real-person record omitting subject_type now FAILs); the render honors markdown emphasis (*italic* / **bold**) + paragraph splitting. Re-graded 2026-06-22: long A / medium B / short B (headline A) against the authored content. **v0.3.0 (2026-06-22):** + coercion-of-the-vulnerable (tier 3, category third-party-harm, 6 coercion strand tags; cold-grade long/medium/short = 86.5/84.9/82.7 = B/B/B). 6 objections now. Open: anchor renames (coercion-of-the-vulnerable + dying-alone, pre-first-ship); the 'categorically-worse-error' counter is implicit -> a later strengthening pass. **v0.3.1 (2026-06-23):** + first RWE records (3 -> coercion-of-the-vulnerable): Farsoud (contested, subject-public-testimony, web-verified), MCS-housing (contested, public-record), Track-2 marginalization (objector-weaponized, public-record). instance_polarity 'contested' added (RWE schema v0.2.2); check_rwe LIVE = 0 violations. Ledger untouched. Pre-ship: add archive_url + swap to canonical OCC URLs (Coroner reports currently mirror / request-access). **v0.3.2 (2026-06-23):** coercion-of-the-vulnerable STRENGTHENED — categorical-worseness counter named + defeated (responses re-authored); re-graded r 0.82->0.87 / a 0.90->0.91, long geomean 0.877558 (B held — gap-closure under the 0.88 A-line, not a band bump). Anchor KEEP. Two residues conceded by design (eligibility-creep, safeguard-efficacy — honesty caps r). No RWE/schema/render touch. **v0.3.3 (2026-06-23):** + palliative-care-sufficiency (tier 3, category remedy-substitution, access_basis both; asymmetry-independent spine — autonomy-override / category-error / comparative-error, no Benatar). Cold-graded long/medium/short = 87.6/85.9/83.7 = B/B/B (boundary-safe; lands between suicide-is-selfish 87.5 and coercion 87.8). **7 objections now**; totalResponses 18->21; corpus 0.3.2->0.3.3. Last pre-ship anchor call: dying-alone RENAMED -> **assisting-is-complicity** (names the objector's load-bearing premise in X-is-Y form, sibling parity with suicide-is-selfish; subsumes the criminalize-demand + 'even being present' prongs) — 3-point swap (corpus id + ledger key + export anchor regenerated), zero residual `dying-alone` refs (prose 'dying alone' untouched). Both anchor calls now closed (coercion KEEP @ v0.3.2, this RENAME). Grade math independently re-derived (all 6 siblings reproduced to the decimal). Validator --self-test exit 0; export deterministic (7 objections); render-harness 7/7 (`#obj-assisting-is-complicity` resolves, `#obj-dying-alone` -> null). No RWE/schema/render-regen this session. **FIRST SHIP = GO** — next is the wuld.ink ship session (deploy + pin==live + search-index re-vendor + nav-strip splice + RWE archive_url/OCC-URL swap).

---

## 1. Vessel files

| File | Role / contract |
|---|---|
| `right_to_die_corpus_v0_1.json` | Corpus (v0.3.0). Sized-down flagship node shape. **6 objections (5 fork-2b + coercion-of-the-vulnerable); seed stubs dropped.** Single source of truth. |
| `combined.html` | Render surface. FETCHES the corpus at runtime (never inlines). tab(s) - tier filter (data-derived) - depth toggle (punch/deconstruct/dismantle) - keyword detection (over keywords[]+move_tags[]+trigger+diagnosis) - `access_basis` badge - markdown emphasis + paragraph rendering in responses - `#obj-<id>` deep-links. NO graph subsystem. |
| `right_to_die_grading_ledger.json` | RSI grades live HERE only. Empty. `band_thresholds` + `entry_shape_reference`. |
| `right_to_die_rwe_schema_v0_1.json` | Vendored RWE record schema (sized-down sibling of `real_world_examples_schema_v1_7.json`). Append-only `instance_id` anchors; `attached_objections[].objection_id` foreign-keyed to corpus ids; reverse slot = node `rwe_refs[]`. |
| `build_right_to_die_index.py` | Search-export generator. Deterministic, validator-gated. |
| `right-to-die-objections-index.json` | Generated export (regenerable). wuld.ink vendors on deploy. |
| `right_to_die_validator_v0_1.py` | `--self-test` = 25 synthetic fixtures + live seed leg. Pre-commit gate. |
| `HANDOFF.md` | This file. |

---

## 2. The forced calls - library-Claude ratification record

**RATIFIED as-built:** 2a RSI-in-ledger-only - 2b data-derived tier filter - 2c `totalEntries`
count guard - 2e export extends flagship (`library`+`surface_route`) - 2f gloss = `diagnosis` -
2g surface route `right-to-die/combined` (confirm production route at deploy) - 2h `_stub` exempt
from grading - 2i two seeds - 2j band-thresholds-in-ledger + cross-check (band the UNROUNDED
fraction; `rsi_pct` 1dp display-only) - `headline_grade_long` headline - committed seed export.

**OVERRIDDEN + applied this revision:** 2d `mechanisms`->`strands` (change-order 1); compensation
fork 3 -> `access_basis` field (change-order 2). **Forks 1-2 stay PROSE** - fork 1 (liberty->claim-
right) is a library-level framing stated ONCE in the framing/diagnosis layer, not a node toggle;
fork 2 (complicity 2a / obstruction 2b) is argument-internal.

---

## 3. Watch / still yours

- **Forks 2a/2b queryability - WATCH during authoring.** If you keep toggling 2a/2b per node, add a
  field THEN; don't pre-build. (Authoring pass 1 stands on fork **2b**, the obstruction-charge.)
- **RWE**: schema vendored + `check_rwe` live (vacuous now). Populate `corpus.realWorldExamples[]`
  downstream, lighter than the flagship; node `rwe_refs[]` are the reverse slots. Append-only
  `instance_id` anchors. Heavier flagship attestation fields are inheritable-from-parent per record.
- **Tier set + objection enumeration**: authored, not scaffolded (render follows the nodes present).
- **`mechanisms` (psych-mechanism layer)**: reserved by the rename, probably unused (smaller-by-design)
  - don't foreclose it.
- **Compensation forks, RWE attribution (Clayton/Inmendham), sovereignty framing** ("live free or die"
  = RWE color only, never load-bearing): per the charter residuals; settle at authoring.

---

## 4. Authoring mechanics

1. Add nodes to `corpus.objections[]`. Required per node:
   `id, tier, category, trigger, keywords[], move_tags[], diagnosis, responses{short,medium,long}, rwe_refs[]`
   (`sources[]` and `access_basis` optional). `diagnosis` = the gloss one-liner (also rendered).
   `move_tags[]` = granular dialectical move-tags (internal taxonomy, e.g. sovereignty-obstruction / claim-vs-license; renamable, NOT charter strands). Top-level `strands` reserves the four charter strands (harm/consent/sovereignty/compensation). [strands[]->move_tags[] covenant, 2026-06-24] `access_basis` in {universal,gated,both} where it applies.
2. `id`: kebab `^[a-z0-9][a-z0-9-]*$`, UNIQUE, **APPEND-ONLY** (permanent `#obj-<id>` anchor).
3. Bump `totalEntries` (= node count) and `totalResponses` (= non-empty response strings).
4. Grade into the LEDGER, not the node:
   `grades[id] = {graded:true, axes:{v,s,c,r,a}, short/medium/long:{rsi_pct,grade}, headline_grade_long}`.
   geomean is DERIVED from axes at regen (validator recomputes); NOT stored — never copy-forward (band-true discipline). Band the UNROUNDED fraction; `rsi_pct` 1dp display-only. Non-stub nodes must be in `grades` OR `ungraded[]`.
5. RWE (when authoring it): add records to `corpus.realWorldExamples[]` per `right_to_die_rwe_schema_v0_1.json`;
   set node `rwe_refs[]` to the `instance_id`s. `check_rwe` will then enforce both-direction resolution.
6. Regenerate the export:  `python3 build_right_to_die_index.py`
7. Gate before commit:  `python3 right_to_die_validator_v0_1.py --self-test`  -> must exit 0.
8. Drop the 2 `_stub` nodes when real content lands. Preview over HTTP (`python -m http.server` ->
   `combined.html`; it fetches the corpus, no `file://`).

---

## 5. Deploy / pin - DEFERRED

Not live. Authoring stays corpus-internal, no pin. First content-ship becomes a **wuld.ink session**:
deploy forces same-session pin==live + search-index regen + re-vendor of `right-to-die-objections-index.json`
(ccxxxvii cadence; the export's `surface_route` is what wuld.ink reads). **Nav-strip splice**
(`Harm & Autonomy | Anthropocentrism` above the flagship top row) stays deferred until >=1 sibling ships
authored content - a switcher with one destination is dead chrome.

---

## 6. Verification record (v0.1.1)

- `right_to_die_validator_v0_1.py --self-test` -> exit 0 (25/25 synthetic fixtures + 0 live violations).
- Export determinism: built twice, byte-identical (727 B); committed == fresh build; `schema_version:1`;
  export md5 UNCHANGED from v0.1 (`5858d370`) - the rename + `access_basis` do not touch the export.
- Render: `node --check` clean; pure-logic harness 13/13 vs the seed corpus, including strand-keyword
  legs (`harm`->tier-1, `sovereignty`->tier-3) proving `strands[]` is wired into keyword detection.
- Anchor uniqueness + anchor-safe regex; `check_rwe` referential integrity (vacuous at launch).
- Flagship UNTOUCHED: `git status` shows only the right-to-die folder.

MD5s at this revision:
`corpus 6a7d260a` - `ledger c6972036` - `rwe-schema c7b2e55d` - `build f45b504c` -
`validator 19f4844b` - `combined.html 8b29a3e6` - `export 5858d370`
