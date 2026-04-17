# MAP 1 — CANONICAL OVERRIDE AUDIT v1
## Post-generation review of the 15 canonical sophisticate overrides

Audit conducted per Active Task A in the v3.6 handout. The 15 overrides were applied at generation time without independent expert validation (per Q5 of methodology v1.1). This document records a structured review against academic-philosophy convention, identifies corrections, and names a generator heuristic that should be constrained in future override passes.

---

## Epistemic status of this audit

The reviewer is not an academic philosopher. The review is a spot-check against general knowledge of the relevant philosophical literatures (Benatar critique corpus, population ethics, non-identity problem literature, contractualism, virtue ethics, phenomenology, performative-contradiction arguments, comparative philosophy, positive psychology). Corrections reflect judgments about what a trained ethicist would recognize as canonical, not a comprehensive paper-by-paper literature audit. A later review by a domain specialist could resurface dropped edges or flag retained ones; this audit is a first-pass filter, not a terminal validation.

The burden of proof is asymmetric. These overrides were algorithmically generated without validation, so the relevant question is whether each is canonical *enough* to bear the label. For the five edges dropped below, the answer is: probably not.

---

## Summary of outcomes

| Action | Count | Edges |
|---|---|---|
| **Retained as canonical override** | 10 | #1, #2, #3, #4, #5, #6, #11, #12, #14, #15 |
| **Retained but demoted from canonical-override status** | 1 | #7 (kept as ordinary premise-matched edge) |
| **Dropped entirely** | 4 | #8, #9, #10, #13 |

Net: 15 canonical overrides → **10 canonical overrides**; 5 edges materially revised (1 demoted, 4 removed).

---

## Family-resemblance failure mode

Reviewing the suspect cluster revealed a non-random pattern. Four of the five problematic edges (#8, #9, #10, #13) share a structural defect: the generator appears to have used a **broad family-resemblance heuristic** — "both challenge zero-sum," "both are non-Western," "both are continental," "both resist systematic ethical theorizing" — where academic philosophy actually tracks much finer argumentative lineages. The heuristic is not wrong in principle (philosophical neighbors do sometimes share commitments), but it collapses distinctions that matter for predicting actual discursive moves.

Examples of the failure mode:

- **"Both non-Western"** (#13): Treats Buddhist metaphysics and Indigenous philosophies as interchangeable, ignoring that each tradition has internal canonical moves that do not pass through the other.
- **"Both challenge zero-sum"** (#8): Pairs Neo-Aristotelian virtue ethics with positive-psych neuroscience, ignoring that virtue ethicists explicitly resist reducing *eudaimonia* to brain states.
- **"Both continental"** (#9): Pairs phenomenological existentialism with performative-contradiction arguments, ignoring that the latter live in transcendental pragmatics (Apel/Habermas), a distinct continental subtradition.

Edge #10's defect is related but distinct: the generator substituted a generic meta-philosophical posture ("epistemic humility") for a specific canonical philosophical target, when what's wanted is a recognized academic move (fallibilism, burden-shifting, tighter proof structure).

**Heuristic shift for any future override passes:** canonical overrides should be grounded in specific argumentative trajectories in the literature, not in topological similarity between philosophical commitments. If the only justification for an edge is that the source and target "feel like they belong together," it does not meet the canonical-override bar.

This finding is logged as a new known limitation in `map1_generation_log.md`.

---

## Retained as canonical override (10)

### #1 `benatar-asymmetry-attack` → `boonin-critique` (HIGH) — **RETAINED with note**

Defensible, though with a caveat the rationale should acknowledge: Boonin is *a* canonical response to Benatar's asymmetry, not *the* sole canonical response. The textbook attacks come from Boonin, Bradley ("Benatar and the Logic of Betterness," 2010), and Harman ("Critical Study of *Better Never to Have Been*," 2009). Weighting Boonin HIGH is defensible; Bradley appears as a downstream MEDIUM move (#4), which is a coherent dialectical structure. No data change, but the override rationale could be tightened in a future pass to acknowledge the multi-pronged academic response.

### #2 `consent-incoherent` → `non-identity-problem` (HIGH) — **RETAINED**

Shiffrin's consent-based antinatalism and Parfit's non-identity problem are tightly paired — both exploit the metaphysical gap of pre-existence, and Parfit's *Reasons and Persons* (1984) is the formal framework any trained philosopher would reach for. HIGH is appropriate.

### #3 `harman-benign-creation` → `population-ethics-paradoxes` (MEDIUM) — **RETAINED**

Harman's 2004 "Can We Harm and Benefit in Creating?" does naturally adjoin Parfit's population-ethics paradoxes, though "naturally extends" overstates slightly — Harman's trajectory is more about defending permissibility than engaging the Repugnant Conclusion directly. MEDIUM is the right weight; raising it would be overreach.

### #4 `boonin-critique` → `bradley-no-subject` (MEDIUM) — **RETAINED**

Both attack the evaluative status of non-existence states. Natural companions in the Benatar critique literature.

### #5 `bradley-no-subject` → `incommensurability` (MEDIUM) — **RETAINED (borderline)**

Incommensurability literature (Chang, Raz) is primarily about practical reasoning; applying it to existence/non-existence comparison is a coherent move but not textbook-canonical. Keeping at MEDIUM; could reasonably be LOW in a future pass.

### #6 `non-identity-problem` → `harman-benign-creation` (MEDIUM) — **RETAINED**

Harman is often situated as a response to non-identity puzzles. Canonical.

### #11 `population-ethics-paradoxes` → `negative-util-aggregation` (HIGH) — **RETAINED**

Parfit's Repugnant Conclusion and NU's aggregation problems are tightly paired — Arrhenius's population-ethics corpus explicitly links them. HIGH is right.

### #12 `meta-ethical-pluralism` → `moral-particularism` (MEDIUM) — **RETAINED**

Dancy's particularism and meta-ethical pluralism are not identical (particularism is specifically about non-codifiability), but both push against monistic systematic theorizing. Natural allies at MEDIUM.

### #14 `flow-states-csikszentmihalyi` → `hedonic-contrast` (MEDIUM) — **RETAINED (borderline)**

Both from positive psychology but addressing different questions (optimal experience vs. baseline adaptation). Adjacent rather than canonical-paired. MEDIUM is slightly generous but defensible.

### #15 `neuroscience-positive-states` → `flow-states-csikszentmihalyi` (MEDIUM) — **RETAINED**

Canonical pairing within positive psychology (Seligman, Csikszentmihalyi).

---

## Retained but demoted from canonical-override status (1)

### #7 `contractualism-scanlon` → `harman-benign-creation` — **EDGE PRESERVED, OVERRIDE FLAG REMOVED**

The generator's rationale for marking this as a canonical override — "both argue creation is justified via outcome criteria" — is straightforwardly wrong. Scanlonian contractualism (Scanlon, *What We Owe to Each Other*, 1998) is specifically *not* outcome-based; it is about justifiability to persons. Harman's benign creation is closer to outcome-oriented reasoning. The stated rationale conflates two distinct meta-ethical structures.

There is a defensible version of this edge — contractualism famously struggles with non-existent persons who cannot be party to a contract, which creates a structural analogy with non-identity-adjacent moves like Harman's — but that is not what the generator reasoned from, and we should not patch the rationale to save the override.

**However**, the premise-matcher independently produces this edge at HIGH weight through legitimate shared-premise detection: `shared_strong: 3` on the premises (consent-impossibility, empirical-tail-risk, proxy-gamble). The edge therefore survives as an ordinary sophisticate edge without needing the canonical-override designation.

**Action**: In both the sophisticate-mode and blended-view entries for this edge, flip `canonical_override: true → false`. Replace the confused override rationale with the premise-matching rationale (already present in `blended.mode_rationales.sophisticate`). Remove the `override_rationale` field from the sophisticate entry.

---

## Dropped entirely (4)

For each of these, the premise-matcher produced `shared_strong: 0, shared_any: 0, raw_score: -1`. The edges exist in the data *only* because of the canonical override. Removing the override means removing the edge.

### #8 `virtue-ethics-flourishing` → `neuroscience-positive-states` — **DROPPED**

Not canonical. Neo-Aristotelian virtue ethics (MacIntyre, Foot, Hursthouse) and positive-psych neuroscience (Seligman et al.) come from disjoint traditions. A virtue ethicist defending *eudaimonia* against reduction to brain states is performing a canonical virtue-ethics move; *making* that reduction is what they are defending against. Pairing them as a "canonical two-front attack" inverts the dialectic.

Canonical sophisticate escalations from virtue ethics: other eudaimonist positions (MacIntyre's *After Virtue*, Foot's *Natural Goodness*), perfectionism (Hurka), Hursthouse's treatment of applied ethics. If a high-quality canonical override for this source node is desired, one of those targets would be more defensible.

### #9 `phenomenological-existentialism` → `performative-contradiction` — **DROPPED**

Performative-contradiction arguments (Apel, Habermas) live in transcendental pragmatics — a distinct continental subtradition from phenomenological existentialism (Heidegger, Sartre, Merleau-Ponty). There is a conversational connection in the EFIList context (thrownness as a response to "you performatively contradict by existing"), but this is not a canonical literature pairing. A more canonical escalation from phenomenological existentialism would target Camus's absurdism, Sartre's bad faith, or Heideggerian being-toward-death.

### #10 `performative-contradiction` → `epistemic-humility` — **DROPPED**

"Epistemic humility" is a general meta-philosophical posture, not a specific philosophical position of the kind that performative-contradiction arguments canonically route to when deflected. The canonical next-moves are: reformulation (tighter proof structure), fallibilist retreat, or burden-shifting arguments. This edge substitutes a generic concession for a specific canonical target.

### #13 `buddhist-objection` → `indigenous-philosophy` — **DROPPED**

The stated rationale — "Buddhist and Indigenous ontologies are often deployed in tandem as non-Western alternatives" — is the clearest case of the family-resemblance failure mode. Buddhist philosophy has a highly developed metaphysics of suffering (*dukkha*, *anātman*, *pratītyasamutpāda*) with direct bearing on antinatalist arguments. "Indigenous philosophy" is a cover term for dozens of distinct traditions — Māori, Lakota, Andean, Akan, Diné, and others — each with different metaphysical commitments. Treating them as interchangeable *non-Western-alternative* units essentializes both.

Canonical sophisticate moves from a Buddhist objection: other schools of Buddhist thought (Madhyamaka, Yogācāra, Theravāda positions), comparative philosophy explicitly engaging Buddhism (Garfield, Siderits), or Schopenhauer (whose engagement with Buddhism is a well-trodden bridge to Western pessimism and antinatalism). Any of these would be more defensible candidates than `indigenous-philosophy`.

---

## Changes to propagate

### `map1_transitions.json`

- **#7**: In `contractualism-scanlon.sophisticate` and `contractualism-scanlon.blended` entries for target `harman-benign-creation`: flip `canonical_override: true → false`; rewrite the `rationale` field in the sophisticate entry to the premise-matching text (mirroring the `shared_strong: 3` form); remove the `override_rationale` field from the sophisticate entry.
- **#8, #9, #10, #13**: Remove the target-edge from both the `sophisticate` and `blended` arrays of the respective source node.

### `map1_generation_log.md`

- Update summary: "Total overrides applied: 15" → "Total overrides applied: 10 (after v1 audit; originally 15, 4 dropped, 1 demoted to non-override)"
- Remove #7, #8, #9, #10, #13 from the override list.
- Add this audit document as a Known Limitation entry with pointer to `map1_override_audit_v1.md`.
- Update per-mode and blended edge counts (-4 edges in sophisticate, -4 in blended).

### `project_handout_visual_maps_v7.md`

- Update "15 canonical sophisticate overrides" to "10 canonical sophisticate overrides" in all occurrences.
- Update Active Task A status to note the audit occurred and what remains (the remaining 10 still have not had independent domain-expert validation).
- Add version note: next version is v3.6.1 or v3.7 (user's call).

### `index.html`

- `MAP1_TRANSITIONS` data block: apply the JSON changes above.
- Methodology panel text: if it states "15 canonical overrides," update to "10 canonical overrides (after v1 audit)."
- Convergence-distribution stats: edge counts shift slightly (blended 873 → 869; sophisticate 351 → 347; ★ count -8 since each dropped edge was in both soph + blended).

---

## Residual risk

Even after this audit, the 10 retained overrides have not been independently validated by a trained ethicist. The audit is a spot-check against general philosophical knowledge. In particular:

1. **#5 and #14 are borderline** — defensible but slightly generous at MEDIUM. A philosopher might argue for LOW.
2. **#1 could be strengthened** by acknowledging in the rationale that Bradley and Harman are parallel canonical responses (not just Boonin).
3. **The heuristic "sophisticate mode under-predicts cross-framework moves"** (from the generation log's Known Limitations §5) is now partly mitigated by the 10 retained overrides, but the heuristic's empirical frequency — how often does cross-framework movement actually happen in sophisticated debates — remains uncalibrated.

Future passes should prioritize domain-expert validation over expansion. The temptation to add more canonical overrides should be resisted until the existing 10 have passed formal review.

---

## Process recommendation for future override passes

Based on the family-resemblance failure mode finding:

Before marking any edge as a canonical override, require an answer to this test question: **"Can I point to a specific paper, textbook, or recognized academic sequence where this exact source-to-target move is the conventional next-step?"**

If the answer is "because they share a commitment" or "because both resist X" or "because they're both non-Y" — *not* canonical. Demote to ordinary premise-matched edge (if premise support exists) or drop.

If the answer is "Scanlon responds to X with Y in *What We Owe to Each Other*, Chapter Z" or "the standard move after Parfit's non-identity argument is Harman's benign-creation paper" — canonical.

---

*Audit v1 conducted 2026-04-16. Supersedes no prior audit. Next review: after live tool use surfaces cases where retained overrides under- or over-predict actual discursive moves, OR after domain-expert review, whichever comes first.*
