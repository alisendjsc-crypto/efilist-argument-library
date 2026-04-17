# Argument Library

**An interactive objection-map and next-move predictor for antinatalist / efilist / negative-utilitarian debate.**

Version 3.6.1 — April 2026

---

## What this is

A single-file web application (`index.html`, ~1.2 MB, no build step, no dependencies beyond CDN D3) that catalogues the objections real interlocutors raise against antinatalist arguments and predicts, given the objection you are *currently* facing, which objection is most likely to come next.

It is not a persuasion tool. It is a terrain map. You still have to walk the terrain.

The tool exists because most antinatalist debate — online and off — cycles through a small set of predictable moves and never reaches the parts of the position where the argument is actually load-bearing. Knowing which move is coming lets you either short-circuit the loop or decide, honestly, that the conversation is not going to go anywhere worth going.

---

## What's new in 3.6.1

- **HIGH CONTRAST and LEGIBILITY rendering fixed in Argument Flow (Map 1).** Previous builds flipped the outer shell to a cream palette when HIGH CONTRAST was enabled but left the inner Map 1 panels dark, producing an unreadable hybrid. D3 node strokes also rendered invisibly against the flipped background. Both are now covered by explicit `body.high-contrast .m1-*` and `body.legible .m1-*` override rules (≈85 lines of CSS).
- **Version strings bumped** across title, header, and in-UI methodology references.
- **Audit-v1 state embedded.** The `MAP1_TRANSITIONS` dataset reflects the manual pass completed in the v3.5 audit: four canonical overrides dropped (virtue-ethics, phenomenological-existentialism, performative-contradiction, buddhist-objection), one demoted (contractualism-scanlon → harman), ten retained. See `map1_override_audit_v1.md` for full justifications.

---

## Architecture

**74 objection nodes** across five tiers:

- **T1 — Emotional / Reflexive.** First-contact objections. "That's depressing." "You're just unhappy." "Have you tried therapy?"
- **T2 — Folk Philosophical.** The sophomore layer. Appeals to nature, consent handwaves, "but think of the people who enjoy life," the asymmetry denied without engaging Benatar.
- **T3 — Structural / Pragmatic.** "If it's so bad why don't you kill yourself," extinction-as-catastrophe framings, the is-ought slide, population-ethics gestures without the math.
- **T4 — Genuine Philosophical.** Where the argument actually lives. Non-identity, Boonin's critique of the asymmetry, Bradley on comparativism, Harman on counterfactuals, the negative-utilitarian aggregation problem, incommensurability.
- **T5 — Meta-Objection.** "You're just an edgelord." "This is performative." Moves that refuse the object-level.

**13 premise nodes** with **222 dependency edges** feeding a separate dependency-graph view.

**~869 blended edges** in the Argument Flow map, distributed across three interlocutor modes:

- **Sophisticate** (~347 edges) — the philosophy-literate opponent who moves from T2→T4 quickly.
- **Defender** (~262 edges) — emotionally invested in natalism, cycles T1/T2/T5.
- **Drifter** (~370 edges) — drifts across tiers without commitment, often lands in T3.

Convergence ratings on transitions: **★★★ ~0.3%** (near-certain next move), **★★ ~12%** (likely), **★ ~87.7%** (plausible). The asymmetry is honest about what we can and can't predict.

**Ten retained canonical overrides** (high-signal transitions that the premise-matcher alone would miss or misweight):

1. `benatar-asymmetry-attack → boonin-critique` (HIGH)
2. `consent-incoherent → non-identity-problem` (HIGH)
3. `bradley → incommensurability` (MEDIUM)
4. `non-identity → harman` (MEDIUM)
5. `population-ethics → negative-util-aggregation` (HIGH)
6. `meta-ethical-pluralism → moral-particularism` (MEDIUM)
7. `flow-states → hedonic-contrast` (MEDIUM)
8. `neuroscience-positive-states → flow-states` (MEDIUM)
9. `harman → population-ethics` (HIGH)
10. `boonin → bradley` (MEDIUM)

Borderline MEDIUMs flagged for future review: `bradley→incommensurability`, `flow-states→hedonic-contrast`.

---

## Views

Five tabs across the top:

- **LIBRARY** — browse all 74 objections by tier, with steelman, response, and references.
- **MECHANISM WEB** — force-directed graph showing how objection classes cluster and share mechanisms.
- **DEPENDENCY GRAPH** — the 13 premises and their 222 dependency edges. Where the argument rests.
- **ARGUMENT FLOW (Map 1)** — the predictor. Pick the objection you're facing, get ranked next-move candidates by mode.
- **METHODOLOGY** — how the transitions were generated, scored, and audited.

---

## Legibility modes

Toggle via the controls bar:

- **STANDARD** — default dark theme.
- **LEGIBILITY** — Georgia serif, 16px base, 1.8 line-height. For extended reading.
- **HIGH CONTRAST** — cream/beige palette, dark text, high-visibility borders. For low-vision use and for print-like reading.
- **LEGIBILITY + HIGH CONTRAST** — stack both.

All four modes now render correctly across all five views, including Map 1.

---

## How to use

Open `index.html` in any modern browser. No server, no build, no install. The file is self-contained except for two CDN imports (D3 v7 and a web font); it degrades gracefully offline if those fail.

For debate preparation, the intended workflow is:

1. Start in **LIBRARY**. Read the tier your interlocutor tends to operate in.
2. When you hit a specific objection in-conversation, switch to **ARGUMENT FLOW**, select the source objection, pick the mode that matches your interlocutor's style, and read the top three predicted next moves.
3. Have your responses to those ready *before* you make your next statement. Most debates are lost in the gap between being right and being prepared.

---

## Methodology and honest limits

The transition weights were generated by a premise-matcher (shared-premise overlap between objection nodes, weighted by tier distance and mode) and then manually audited against the canonical literature. The audit dropped overrides that reflected the author's philosophical preferences rather than actual observed interlocutor behavior. It retained overrides where the premise-matcher demonstrably misses a high-frequency move (e.g. sophisticates jumping from Benatar's asymmetry attack straight to Boonin's critique rather than to the weaker folk rebuttals the matcher ranks higher).

**This tool does not argue the antinatalist case.** It maps the objection landscape. The `steelman` field on each objection is written to be genuinely strong — if it reads as weak, the author considers that a bug.

**The 87.7% single-star convergence figure is load-bearing.** Most moves in most debates are plausible rather than predictable. The tool's value is in the 12% of two-star transitions and the handful of three-stars, not in a false claim of total predictability.

---

## Files in this repository

- `index.html` — the application (v3.6.1, 3742 lines).
- `map1_transitions.json` — raw transition data, post-audit-v1.
- `map1_methodology_v1_1_locked.md` — scoring rubric and generation methodology.
- `map1_override_audit_v1.md` — audit trail for the ten retained and five removed/demoted canonical overrides.
- `map1_generation_log.md` — chronological log of dataset generation.
- `project_handout_visual_maps_v8.md` — design notes for the visual-map system.
- `README.md` — this file.

---

## License and attribution

Author-controlled. If you cite or adapt, reference the version number and the audit iteration (currently v3.6.1 / audit-v1). Pull requests welcome on the transition dataset if you have observational data on real debates; pull requests welcome on the methodology if you can demonstrate a flaw in the premise-matcher's scoring.

Domain-expert review of the ten retained canonical overrides remains open. If you have published work on any of the flagged transitions, the author would like to hear from you.
