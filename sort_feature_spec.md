# sort_feature_spec.md

**Session:** rebuttal_strengthening_worklist_and_stats_sort_scoping_session
**Project:** efilist_argument_library · v3.7 line · **Date:** 2026-05-16
**Status:** SCOPING ONLY. No UI built. Terminus sealed. Companion to
`corpus_statistics_spec.md`; kept as a separate file per close protocol.

---

## Feature

A tier-list sort control: toggle the objection ordering between the existing
default and **"most → least deployed"** (descending deployment count). Surface
chrome only — it reorders presentation, it touches no canonical content.

## Data dependency

Requires a per-objection deployment-count map at the render layer:
`deployment[obj.id] = count(realWorldExamples[].attached_objections[].objection_id == obj.id)`.

This is the same derivation the stats section's metric (1) uses — compute it
once at render and share it. **Precedent: RSI.** `REBUTTAL_STRENGTH` already
established the pattern of a surface-only const driving display logic without a
corresponding corpus field; the deployment map follows that precedent exactly.
It must be computed at render, never hand-authored, for the same anti-drift
reason. Reference distribution (recompute at render): violence-as-reductio 27,
benatar-asymmetry-attack 15, ai-fear 10, why-not-suicide 7,
antinatalism-misanthropic 6, slippery-slope-eugenics 5, life-gift 4,
non-identity-problem 4.

## Independence from the percentage decision

The sort feature is **fully specifiable and buildable even if the deployment
percentage is hidden**. Sorting needs only the ordinal count, not a displayed
share. Build paths:

- **Percentage visible** (current default decision): sort control sits next to
  the visible share; the share doubles as the sort key's surfaced value.
- **Percentage semi-hidden** (override branch): the sort still works on the
  underlying count; the control reorders the list without ever rendering the
  number. Optionally expose only ranks (1st, 2nd, …) instead of shares.

Spec the control as decision-independent: it ships in either branch.

## Behaviour

- Toggle, not a one-way action: default order ⇄ deployment-descending.
- Ungraded high-deployment nodes (e.g. violence-as-reductio at 27) sort by
  deployment normally; deployment is grade-independent, so no special-casing.
- Ties broken by stable secondary key (existing default order) so the sort is
  deterministic.

## Build status

v3.8-class surface-only chrome. Content-mutating to the surface artifact only
(no corpus/JSX/canon write), harness-gated like any terminus-reopening surface
edit. Lowest-complexity item in the post-archive queue; specs feed it directly.
Not in scope this session.
