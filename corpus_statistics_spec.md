# corpus_statistics_spec.md

**Session:** rebuttal_strengthening_worklist_and_stats_sort_scoping_session
**Project:** efilist_argument_library · v3.7 line · **Date:** 2026-05-16
**Status:** SCOPING ONLY. No surface built. Terminus sealed. This document
specifies a future content-mutating STATS section build; it does not author one.

---

## Decision gate — RESOLVED

Operator was silent at session open. **Default taken: corpus-internal
deployment share.** The deployment statistic is `(RWE instances attached to
objection) / (total RWE attachment edges)`, labelled in the surface as a share
*within the harvested corpus*, never as a real-world frequency. The rejected
alternative ("theorized rate of deployment %") manufactures a denominator that
does not exist and reproduces the pretty-number-over-substance failure that
triggered the grading work in the first place. If a later operator overrides to
the theorized framing, the number must render semi-hidden by default and carry a
prominent epistemic-health warning inline.

---

## Hard rule (non-negotiable, applies to every figure)

Every statistic is **computed from canonical data at render time, never
hand-authored**. No figure is stored as a literal in the surface. This is the
single rule that prevents the stats section from drifting against the corpus the
way the stale `~0.10/0.05` depth-modifier comment drifted against the
0.12/0.05 code. If a number cannot be derived from `objections`,
`realWorldExamples`, or the RSI layer at render, it does not go in the section.

## Mandatory disclaimer header (`sampling_provenance`)

The section opens with a first-class, non-collapsible caveat block stating: the
real-world example corpus is **diversified but opportunistic** (institutional /
lifestyle / student-journalism / primary-platform / niche surfaces), is **not a
representative sample of real-world objection frequency**, and every share below
is internal to the harvested set. This header is structural, not a footnote.

---

## Metric list

Each metric below names its canonical source and the render-time computation.

1. **Deployment share (per objection).**
   `count(realWorldExamples[].attached_objections[].objection_id == obj.id)` /
   `total attachment edges`. Source: `realWorldExamples`. Current totals for
   reference: 136 RWE records, 171 attachment edges. Sortable (see
   `sort_feature_spec.md`).

2. **Grade distribution by tier.**
   Join RSI headline grade (long) onto `obj.tier`. Source: RSI layer +
   `objections[].tier`. Current long-depth matrix (reference, recompute at
   render): tier1 A6/B5/C2; tier2 A4/B7/C3; tier3 A5/B8 (+1 ungraded);
   tier4 A7/B14/C7; tier5 A4/B2. 4 nodes ungraded — render them as an explicit
   `UNGRADED` cell, never silently dropped or counted as a grade.

3. **Tier population.** `count(objections by tier)`. Source: `objections`.

4. **Archetype-signal distribution.**
   `count(realWorldExamples[].archetype_signal_observed)`. Source:
   `realWorldExamples`. Current global (reference): sophisticate 72,
   not-applicable 38, defender 15, drifter 6, blended 5. The `not-applicable`
   share (~28%) must be displayed, not hidden — it is a corpus-health signal,
   not noise.

5. **Mechanism fan-out.** Per `psychMechanism`, the count of objections
   carrying it. Source: `objections[].psychMechanism`. Surfaces which
   mechanisms are load-bearing vs singletons.

6. **Deployment × grade danger-quadrant — PUSH THIS.**
   The 2-D view: x = deployment share, y = headline grade (long), highlighting
   the high-deployment ∩ (C-grade OR ungraded) region. This is the one
   statistic the project currently lacks and most needs — it is the only view
   that makes "a weak rebuttal that is heavily deployed in the wild" legible at
   a glance. Reference state: **benatar-asymmetry-attack** (C78.3 @ 15 RWE) is
   the active alarm; **violence-as-reductio** (UNGRADED @ 27 RWE, highest
   deployment) is the latent alarm that grading will either light up or clear;
   life-gift (C @ 4 RWE) and ai-fear (B @ 10 RWE) are not in the quadrant.
   Render ungraded high-deployment nodes in a distinct "pending-grade" state
   inside the quadrant so the grading backlog is visible as risk, not absence.

---

## Build status & dependency

Buildable as a surface-only section analogous to the RSI `REBUTTAL_STRENGTH`
precedent (a render-layer construct, not a corpus field). It depends on the
RSI-corpus denormalization fork only insofar as grade-by-tier and the
danger-quadrant read RSI: if RSI stays surface-only, the stats section computes
from the same surface const the existing RSI render uses; if RSI is later
backfilled into the corpus, the section reads the corpus field instead. Either
way the hard render-compute rule holds. This section is a v3.8-class
content-mutating, harness-gated build — not a patch, not in scope here.
