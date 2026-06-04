# DIRECTIVE — v3.8 archetypeVariants render path (MAX, in-chat design + Cowork handoff)

**Session id:** `v3_8_render_path_archetype_toggle_s1`
**Class:** MAX (UX-design + render-code authoring; judgment-heavy). Produces a Cowork splice handout — the actual MB-file mutations route to Cowork, never spliced in-chat.
**Run AFTER:** K41a closed (the `CLAUDE.md` carry committed; `v3.8.x` pushed). Operates on the **`v3.8.x` backup-branch surfaces only**. Does NOT touch `main` / live `library.wuld.ink` (still v3.7.3) — the merge/deploy is the session AFTER this one.

## Why this session exists
The `archetypeVariants` **data** shipped to all surfaces at v3.8.0 (corpus) / v3.8.1 (jsx) but renders **invisible**: jsx has `REBUTTAL_STRENGTH`×0 and `archetypeVariants`×7 as data literals with **no `.archetypeVariants[` read path**; combined (×7) and index are the same — data only. The D5 in-place archetype toggle was never built. Until it is, the variant work is shipped-but-unseen. This session designs + authors the render path, then hands the splice to Cowork.

This is a **surface-render MINOR** (additive UI; zero invariant-block touch). Not MAJOR, no unseal. The v3.8 MAJOR bundle (suffering + variants + rename) closed at v3.8.0 — confirmed in `session_v3_8_major_cut_reconciliation_s1_state.json`.

## Deliverable (one)
A render-path **design spec + authored render code** (React fragment for jsx; vanilla-JS render fragment for combined/index) + a Cowork splice handout **`v3_8_render_path_cowork_handout_s1.md`** that **folds in the deferred residuals** (R1/R2 count fixes + R3 annotate note) in the same pass, since the render path re-touches those exact surfaces.

## Authoritative inputs (read; never full-view MB files)
- `ratified_variant_design_v1.json` — **D5** (in-place toggle: pills `sophisticate | defender | drifter | blended` on the response view, default = canonical short/med/long; NOT a separate tab, NOT hover/expand), **D1** (4 fixed slots, each optional — omit where nil), **D3** (variants live at `responses.archetypeVariants`), **D7** (additive; MUST NOT alter short/medium/long). Binding.
- `archetype_variant_scaffold_v1.json` — slot shape + `_variant_meta{variant_axis, grade_policy, build_status}`; per-slot `register` cue available for UI.
- corpus `efilist_argument_library_v3_8_0.json` — the 7 nodes' `responses.archetypeVariants` shape (single-body per slot; no depth tiering — confirm from char counts).
- `session_v3_8_major_cut_reconciliation_s1_state.json` — residual ledger (R1–R5), partition ruling, deferral.

## MANDATORY first step — render-surface recon (do before any design lock)
Locate the existing **response-render region** on each surface via `grep -n` (never `cat` / full-`view` MB files):
- jsx: the depth-toggle component that renders `responses.{short,medium,long}` (canon flags the stale chrome span ~L9325 — use as a starting hint, then grep the actual render function).
- combined.html / index.html: the vanilla-JS render function that emits the response body + the existing depth control.
Establish **how the current depth toggle renders a body** — the archetype toggle composes with it. Do not design before this is in hand.

## Design decisions to resolve + LOCK (recommend, then proceed)
- **DR1 — depth × archetype composition.** Variant slots are single-body (verify: no short/med/long tier). **Recommend:** pills are a peer control on the response view; selecting a pill **replaces** the canonical body with that archetype's variant body and the depth control reverts to / disables "canonical"; deselect restores depth. Default state = canonical, existing default depth. State the rule explicitly.
- **DR2 — pill visibility.** Pills render ONLY on nodes carrying `responses.archetypeVariants` (7 of 81); within those, ONLY authored slots (D1 omit-where-nil). No empty/disabled pills for omitted slots.
- **DR3 — register cue.** Pills labeled by archetype; decide whether to surface `_variant_meta`/per-slot `register` as a tooltip/subtitle. Recommend a lightweight cue, not a wall of meta.
- **DR4 — additivity guard (D7).** Canonical view reads `short/medium/long` verbatim; variants are display-only and never mutate the base. Assert in code + in the handout.
- **DR5 — objectionSubforms boundary.** `objectionSubforms` display surface stays **DEFERRED** (separate D5 sub-decision). This toggle is `archetypeVariants`-only. Do NOT build objectionSubforms UI here.
- **DR6 — narrow viewport.** Pills wrap/collapse gracefully on mobile. Decide the degradation.

## Then
- Author the render code, **one fragment per surface** (jsx React fragment; combined/index vanilla-JS fragment) — keep each bounded to dodge output-length cutoffs.
- Emit `v3_8_render_path_cowork_handout_s1.md` with grep-hint splice targets, **folding the deferred residuals**:
  - **R1** jsx: L7 docstring `75 objections / 229 pre-built` → `81 / 243`; retire the "4 archetype-conditional surfaces on violence-as-reductio" phrasing; L9473 badge `74` → `81`.
  - **R2** combined: `"78 objection"` ×4 (grep-hint L1541/1579/1640/2349) → classify chrome (→81) vs historical prose (hold); mirror on index.html.
  - **R3** add ONE registry-level `if_*` supersession note (do not rewrite the 16 dated `responses.if_*` provenance loci).
- Cut class **MINOR** (additive render + cosmetic chrome + provenance note; invariant subtree byte-identical).

## Gates (all pass before emitting the handout)
- **G1** render-surface recon complete; jsx/combined/index render regions located via grep-n.
- **G2** DR1–DR6 resolved + recorded with recommendations.
- **G3** render code authored per surface; reads `responses.archetypeVariants`; never mutates `short/medium/long` (D7 asserted).
- **G4** pills gated to authored slots only (D1); 7-node visibility correct; no empty pills.
- **G5** R1/R2/R3 folded into the same Cowork handout — no separate parity pass.
- **G6** cut class MINOR justified against bump rules; `objectionSubforms` confirmed deferred.

## Close
Emit render-code fragments (one file per surface) + `v3_8_render_path_cowork_handout_s1.md` + `session_v3_8_render_path_archetype_toggle_s1_state.json` (DR rulings, recon line-hints, folded-residual ledger, gate results, next = Cowork splice then variant-cut merge/deploy). Canon MINOR bump note. `present_files`. ≤3 sentences.

**Queued after this:** variant-cut **merge/deploy** session — Cowork splices the render path + folded residuals into `v3.8.x`, then merges `v3.8.x` → `main`, recomputes + re-attests the md5 set, rewrites `wuld.ink/library-about` (counts + md5), and deploys live. That is where v3.8 reaches production.
