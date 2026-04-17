# MAP 1 — GENERATION LOG

Transparent audit trail for transition matrix generation.
Run against methodology v1.1 locked rules (Q1–Q6 user-decided).
**Revised 2026-04-16: post-audit-v1 corrections applied (see `map1_override_audit_v1.md`).**

---

## Summary statistics (post-audit-v1)

- Source nodes: 74
- Total edges (blended union): **869** (11.7 avg per node) — was 873 pre-audit
- Per-mode edge counts: Sophisticate 347 / Defender 262 / Drifter 370 — sophisticate was 351 pre-audit

### Convergence distribution (post-audit-v1)

| Convergence tier | Count | % of blended edges |
|---|---|---|
| ★★★ (all 3 modes agree) | 3 | 0.3% |
| ★★ (2 modes agree) | 104 | 12.0% |
| ★ (single mode) | 762 | 87.7% |

**Interpretation:** The predominantly single-mode distribution validates the three-mode architecture. If modes were redundant, we would see >50% three-mode convergence. The observed ~0.3% indicates that a Sophisticate, a Defender, and a Drifter attacking the same objection select substantially different successor nodes. This is the central strategic payoff of Map 1: different interlocutor types require different preparations. The audit-v1 edge removals did not materially shift the convergence character of the matrix.

---

## Disengagement assignments

Per-node heuristic per Q4 decision. HIGH = interlocutor often drops; LOW = interlocutor almost always continues.

### HIGH (7 nodes)

- `consent-incoherent` (T4)
- `cant-prove-nonexistence-better` (T4)
- `non-identity-problem` (T4)
- `bradley-no-subject` (T4)
- `boonin-critique` (T4)
- `performative-contradiction` (T4)
- `incommensurability` (T4)

### MEDIUM (59 nodes)

- `why-not-suicide` (T1)
- `consent-both-ways` (T2)
- `nihilism-label` (T2)
- `economy-population` (T3)
- `benatar-asymmetry-attack` (T4)
- `transhumanist-objection` (T4)
- `self-defeating` (T5)
- `imposing-values` (T5)
- `ai-fear` (T3)
- `natural-reproduce` (T1)
- `meaning-through-suffering` (T4)
- `free-will-defense` (T4)
- `procreative-liberty` (T4)
- `negative-util-aggregation` (T4)
- `western-philosophy` (T2)
- `antinatalism-misanthropic` (T1)
- `evolution-purpose` (T2)
- `future-solve` (T3)
- `extinction-culture` (T3)
- `playing-god` (T2)
- `policy-proposal` (T3)
- `next-person-cure-cancer` (T1)
- `pinker-better-world` (T3)
- `privileged-first-world` (T1)
- `selfish-lazy` (T1)
- `suffering-makes-human` (T2)
- `red-button-repugnant` (T5)
- `slippery-slope-eugenics` (T3)
- `adoption-instead` (T2)
- `bitter-childhood` (T1)
- `animals-reproduce` (T1)
- `overpopulation-addressed` (T3)
- `hedonic-contrast` (T4)
- `ableist-objection` (T3)
- `change-your-mind` (T1)
- `anthropic-principle` (T4)
- `meta-ethical-pluralism` (T5)
- `heat-death-futility` (T5)
- `happiness-is-choice` (T1)
- `cherry-picking-worst` (T2)
- `revealed-preference` (T4)
- `social-contract` (T3)
- `moral-progress` (T3)
- `contractualism-scanlon` (T4)
- `phenomenological-existentialism` (T4)
- `harman-benign-creation` (T4)
- `population-ethics-paradoxes` (T4)
- `moral-particularism` (T5)
- `marxist-materialist` (T3)
- `buddhist-objection` (T4)
- `virtue-ethics-flourishing` (T4)
- `neuroscience-positive-states` (T4)
- `epistemic-humility` (T4)
- `flow-states-csikszentmihalyi` (T4)
- `luxury-belief` (T2)
- `pragmatist-objection` (T4)
- `care-ethics` (T4)
- `rights-future-generations` (T3)
- `indigenous-philosophy` (T4)

### LOW (8 nodes)

- `life-gift` (T1)
- `just-depressed` (T1)
- `gods-plan` (T2)
- `just-edgy` (T1)
- `most-people-happy` (T2)
- `love-beauty-art` (T2)
- `speak-for-everyone` (T2)
- `survivor-testimony` (T2)

---

## Canonical sophisticate overrides (post-audit-v1)

Per Q5 decision: overrides applied at generation time based on academic-philosophy convention, NOT independently expert-validated. Each override edge is marked `canonical_override: true` in data and carries the user-facing disclosure note in-tool.

**Generation-time overrides: 15. Post-audit-v1 overrides retained: 10.**

Four edges were dropped entirely and one edge was retained but demoted from canonical-override status during audit-v1 (see `map1_override_audit_v1.md` for full reasoning). The dropped edges exhibited a "family-resemblance failure mode" in the generator heuristic — pairing source and target based on broad commitment-similarity rather than on specific argumentative trajectories documented in the literature.

### Retained canonical overrides (10)

### `benatar-asymmetry-attack`

- → `boonin-critique` (HIGH): Boonin's formal reconstruction is the canonical sophisticate escalation from any informal asymmetry attack. *(Audit-v1 note: Boonin is one of three parallel canonical responses alongside Bradley and Harman; HIGH weighting is defensible given that Bradley appears as a downstream MEDIUM move.)*

### `consent-incoherent`

- → `non-identity-problem` (HIGH): Parfit's non-identity problem is the canonical formal companion to consent-incoherence objections — they exploit the same metaphysical gap from different angles.

### `harman-benign-creation`

- → `population-ethics-paradoxes` (MEDIUM): Harman's permissibility argument naturally extends to population-ethics paradoxes (Mere Addition, Repugnant Conclusion).

### `boonin-critique`

- → `bradley-no-subject` (MEDIUM): Bradley's no-subject objection is the canonical complement to Boonin — both attack the evaluative status of non-existence states.

### `bradley-no-subject`

- → `incommensurability` (MEDIUM): Incommensurability is the canonical formal deepening of Bradley-style symmetry objections. *(Audit-v1 note: borderline; could reasonably be LOW.)*

### `non-identity-problem`

- → `harman-benign-creation` (MEDIUM): Harman's benign-creation argument is the standard move after non-identity — it attempts to salvage permissibility via outcome rather than harm attribution.

### `population-ethics-paradoxes`

- → `negative-util-aggregation` (HIGH): Mere Addition and repugnant conclusion naturally route to negative utilitarianism aggregation challenges — they're the paired pincer move.

### `meta-ethical-pluralism`

- → `moral-particularism` (MEDIUM): Particularism is the canonical meta-ethical companion — both attack systematic theorizing from different angles.

### `flow-states-csikszentmihalyi`

- → `hedonic-contrast` (MEDIUM): Flow and hedonic contrast are closely-linked empirical challenges to the zero-sum framework. *(Audit-v1 note: borderline; adjacent rather than canonical-paired.)*

### `neuroscience-positive-states`

- → `flow-states-csikszentmihalyi` (MEDIUM): Flow research and neuroscientific positive-state claims are the canonical paired empirical attack on zero-sum.

### Demoted from canonical-override status (1) — edge retained

### `contractualism-scanlon`

- → `harman-benign-creation` (HIGH): **No longer flagged as canonical override.** The generator's override rationale ("both argue creation is justified via outcome criteria") was philosophically confused — contractualism is specifically not outcome-based. However, the premise-matcher produces this edge independently at HIGH weight (shared_strong: 3 on consent-impossibility, empirical-tail-risk, proxy-gamble). The edge persists as an ordinary sophisticate edge; the `canonical_override` flag is now `false`.

### Dropped edges (4) — reasoning summarized

1. `virtue-ethics-flourishing` → `neuroscience-positive-states` (was MEDIUM): dropped. Neo-Aristotelian virtue ethics and positive-psych neuroscience come from disjoint traditions; virtue ethicists resist reducing *eudaimonia* to brain states.
2. `phenomenological-existentialism` → `performative-contradiction` (was MEDIUM): dropped. Performative contradiction lives in transcendental pragmatics (Apel/Habermas), not phenomenological existentialism.
3. `performative-contradiction` → `epistemic-humility` (was MEDIUM): dropped. Epistemic humility is a generic meta-posture, not a specific canonical target.
4. `buddhist-objection` → `indigenous-philosophy` (was LOW): dropped. Treating Buddhist metaphysics and Indigenous philosophies as interchangeable "non-Western alternatives" essentializes both and is not a canonical academic move.

See `map1_override_audit_v1.md` for full per-edge reasoning and recommended canonical alternatives.

---

## Two-mechanism disclosure edges

Nuclear retreat (T1→T5) and collapse (T4→T1) edges appearing in both Defender and Drifter modes per Q3 decision. Each carries the user-facing two-mechanism disclosure note.

**Total 2-mechanism edges: 44**

- `life-gift` → `self-defeating` (nuclear T1→T5)
- `just-depressed` → `self-defeating` (nuclear T1→T5)
- `why-not-suicide` → `self-defeating` (nuclear T1→T5)
- `benatar-asymmetry-attack` → `life-gift` (collapse T4→T1)
- `transhumanist-objection` → `life-gift` (collapse T4→T1)
- `natural-reproduce` → `self-defeating` (nuclear T1→T5)
- `just-edgy` → `self-defeating` (nuclear T1→T5)
- `meaning-through-suffering` → `life-gift` (collapse T4→T1)
- `free-will-defense` → `life-gift` (collapse T4→T1)
- `procreative-liberty` → `life-gift` (collapse T4→T1)
- `negative-util-aggregation` → `life-gift` (collapse T4→T1)
- `antinatalism-misanthropic` → `self-defeating` (nuclear T1→T5)
- `next-person-cure-cancer` → `self-defeating` (nuclear T1→T5)
- `next-person-cure-cancer` → `moral-particularism` (nuclear T1→T5)
- `next-person-cure-cancer` → `red-button-repugnant` (nuclear T1→T5)
- `next-person-cure-cancer` → `imposing-values` (nuclear T1→T5)
- `privileged-first-world` → `self-defeating` (nuclear T1→T5)
- `selfish-lazy` → `self-defeating` (nuclear T1→T5)
- `consent-incoherent` → `life-gift` (collapse T4→T1)
- `bitter-childhood` → `self-defeating` (nuclear T1→T5)
- `cant-prove-nonexistence-better` → `life-gift` (collapse T4→T1)
- `animals-reproduce` → `self-defeating` (nuclear T1→T5)
- `hedonic-contrast` → `life-gift` (collapse T4→T1)
- `change-your-mind` → `self-defeating` (nuclear T1→T5)
- `anthropic-principle` → `life-gift` (collapse T4→T1)
- `happiness-is-choice` → `self-defeating` (nuclear T1→T5)
- `revealed-preference` → `life-gift` (collapse T4→T1)
- `non-identity-problem` → `life-gift` (collapse T4→T1)
- `bradley-no-subject` → `life-gift` (collapse T4→T1)
- `contractualism-scanlon` → `life-gift` (collapse T4→T1)
- `phenomenological-existentialism` → `life-gift` (collapse T4→T1)
- `harman-benign-creation` → `life-gift` (collapse T4→T1)
- `population-ethics-paradoxes` → `life-gift` (collapse T4→T1)
- `boonin-critique` → `life-gift` (collapse T4→T1)
- `performative-contradiction` → `life-gift` (collapse T4→T1)
- `buddhist-objection` → `life-gift` (collapse T4→T1)
- `virtue-ethics-flourishing` → `life-gift` (collapse T4→T1)
- `neuroscience-positive-states` → `life-gift` (collapse T4→T1)
- `epistemic-humility` → `life-gift` (collapse T4→T1)
- `incommensurability` → `life-gift` (collapse T4→T1)
- `flow-states-csikszentmihalyi` → `life-gift` (collapse T4→T1)
- `pragmatist-objection` → `life-gift` (collapse T4→T1)
- `care-ethics` → `life-gift` (collapse T4→T1)
- `indigenous-philosophy` → `life-gift` (collapse T4→T1)

---

## Known limitations logged

1. **Canonical overrides not expert-validated.** Each override reflects generator judgment about academic-philosophy convention. Spot-checks recommended.
2. **Disengagement heuristic is coarse.** Three buckets (HIGH/MEDIUM/LOW) applied by rule; no empirical basis. Refinement possible with debate-transcript data.
3. **No empirical frequency calibration.** Weights are reasoned categorical judgments, not frequencies from observed debates. Percentages would imply false precision.
4. **Drifter-mode rhetorical-register matching via category field is a proxy.** True rhetorical register may be finer-grained than tier+category.
5. **Sophisticate mode under-predicts cross-framework moves.** Canonical overrides mitigate the highest-impact cases; others may remain under-predicted. Post-audit-v1, 10 overrides remain (was 15).
6. **Family-resemblance failure mode in canonical-override generation (discovered audit-v1).** The initial generator pass used a broad family-resemblance heuristic — pairing source and target based on commitment-similarity ("both challenge zero-sum," "both non-Western," "both continental") rather than on documented argumentative trajectories in the literature. Four of the 15 initial overrides exhibited this defect and were dropped. Future override passes must satisfy the test: *can the move be located in a specific paper, textbook, or recognized academic sequence?* If the only justification is structural resemblance, the edge is not canonical.
7. **Retained overrides have not had domain-expert review.** Audit-v1 was a spot-check against general philosophical knowledge, not a terminal validation. The 10 retained overrides should be passed to a trained ethicist before further expansion of the override set.
