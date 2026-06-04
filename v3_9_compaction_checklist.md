# v3.9 Compaction Checklist - operator-side (Claude.ai Library project panel)
Session: v3_9_0_scoping_cowork (K58, 2026-06-03)

## FINDING THAT CHANGES THE PLAN
The handout said removed files are safe because *git history retains them*. **FALSE for the per-node files.**
Only 93 files were ever committed to the efilist repo. ZERO matches for `regrade_*`, `*_long_v3_8_*`,
per-node `*_foldin*` docs, `session_v3_7_*`, `v3_8_phase0*`, `_v3_7_5_salvage_log.json`. Downloads: also none.
Those files exist ONLY in the project knowledge panel. Deleting them there = the drafts are gone.

## Your fork (pick one before deleting)
- **(a) Archive-then-delete (recommended):** in the panel, open each remove-list file -> download/copy into
  the repo root -> run the K58 PS block (it stages an `archive/v3_8_per_node/` folder if present) -> THEN delete
  from the panel. Cost: ~10-20 min of clicking. Preserves the authored drafts the handout assumed were preserved.
- **(b) Delete outright:** defensible - every fold's RESULT is already in corpus + ledger + canon attestations;
  the standalone drafts are working scratch. You lose the drafts' prose history. Faster.

## Remove from panel (per handout patterns)
- `regrade_*` (v3.8.1-13 per-node regrades)
- `*_long_v3_8_*` (per-node long drafts)
- per-node `*_foldin*` docs (NOT pending_foldin_manifest.json - that stays)
- `session_v3_7_*`, `v3_8_phase0*`, `_v3_7_5_salvage_log.json`, other pre-v3.8 session-state/salvage

## Keep in panel (handout list, repo-verified)
| file | repo bytes | note |
|---|---|---|
| project_canon_v37_20.json | ~209K | NEW this session - upload, replaces v37_19 per update_protocol |
| efilist_argument_library_v3_8_0.json | 1,302,369 | corpus |
| efilist_argument_library_v3_8_0.jsx | 1,245,444 | |
| combined.html | 2,391,247 | see lever below |
| rebuttal_grading_ledger.json | 42,750 | |
| v3prime_validator_v1_7.py | 22,322 | |
| pending_foldin_manifest.json | 40,451 | |
| backward_gap_audit_v3_8_14.json | NOT IN REPO | panel-only keep-file: download -> commit it too |
| v3_8_23 artifacts | ~10K | findings + state |
| v3_9 artifacts (4) | ~95K | inventory, triage, rwe schema, state - upload after commit |

## Capacity math (honest version)
Cowork cannot see the panel, so reclaimed-% is yours to read off the project settings page after deletion.
Structure of the estimate: the keep-set is ~5.35 MB and is DOMINATED by three artifacts (corpus + jsx +
combined = ~4.94 MB). The per-node remove-set is historically ~3-40 KB per file - removing it frees a real
but MODEST share. **The big lever, if ~83% does not drop enough: combined.html (2.39 MB) is reproducible
from the repo and live at library.wuld.ink/combined.html - it does not have to live in the panel.** The
handout lists it keep; treat un-mounting it as the escalation step, ratified by Library-Claude, not a default.
Record: pre-% (~83) -> post-% = ____ in v3_9_0_scoping_cowork_state.json on next touch.

## Repo hygiene bundled into the K58 PS block
- 5 files are STAGED FOR DELETION in the efilist index (`git rm --cached` state): sort_feature_spec.md,
  stats_render.py, v3_7_cut_invariants.json, v3_8_23_coherence_audit_findings.json, v3prime_validator_v1_7.py.
  The marker's audit_ref must resolve in-repo and the validator is repo-critical -> the block UNSTAGES them
  (working copies untouched). If un-tracking was deliberate, say so and we re-do it deliberately.
- Stray `.k58_wtest` write-probe (sandbox cannot unlink) - block deletes it.
- push_v3_8_19/21/22.ps1 remain untracked litter - delete or keep at your convenience.
