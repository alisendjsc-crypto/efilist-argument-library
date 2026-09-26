# Honest-Residuals Register v0.5

**Status: WORKING, and derived from a drafted assembly.** 75 honest-residue (d) entries consolidated from `adversarial_map_v1_4.json` (cb61db5c), which carries L4's drafts of R1's FAILS. A seat that did not draft them judges them (K258); that judgment is recorded in canon, not here.
Contributing phases (by authorship): A (11), B1 (8), B2 (13), C (7), D (12), E (4), F (17), G (3). Contributing nothing: R.
Source corpus `04bf6482` / 82 nodes. Rebuild: `python3 build_register_v0_5.py`.

**Library-internal.** No corpus, ledger, index or `/combined` byte moves from this artifact.

---

## What moved from v0.4

- source is adversarial_map_v1_4.json, which carries L4's drafts of R1's 45 FAILS
- 35 tributaries added, each an R1 FAILS reclassified (a) -> (d) onto registered bedrock and filed on the facet of the registered (d) it reaches: HR-02 5, HR-03 9, HR-04 2, HR-05 6, HR-06 4, HR-11 1, HR-12 1, HR-14 7
- no bedrock added and no facet id minted; the class law forced none
- HR-11 conditions HR-02, HR-12 independent_of HR-10 and HR-14 independent_of HR-05 declared, because the new tributaries made each pair share a node; drafted by L4
- the birth-order check reads a reclassified tributary as adjudicated at L4, after G

Tributaries whose (d) is L4's reclassification of an R1 FAILS. `phase` is the phase that authored the move; `reclassified` names the R1 row and the registered (d) the line reaches. No bedrock and no facet id is added.

### Parity

Field for field, asserted before the write: every v0_4 bedrock keeps its name, alias, gloss, registration and birth certificate; relations gain exactly the three declared and lose none; every v0_4 tributary stands unchanged on its v0_4 facet; the only additions are the 35 reclassified tributaries. 7 of 15 bedrocks are byte-identical to v0_4. The v0_1 and v0_3 parity gates hold by transitivity: v0_4 held them, and no tributary they read has moved.

## What moved from v0.1 (carried from v0.4)

- source is adversarial_map_v1_2.json rather than six fragment files
- HR-14 added, with the three facets canon records plus the terminus that holds it open
- HR-05 registered_in repointed at canon: K345 folded it into terminal_stability_marker.honest_residuals, so v0_1's dangling-pointer finding is STALE and is dropped as a CORRECTION. Its novel-flag collision is untouched and stands
- the corpus pin moves to the post-cut corpus, on the grounds in corpus_span_ruling
- an adjacency the ratified four-kind vocabulary cannot express is recorded in the audit rather than declared as a relation that would misdescribe it
- K351: HR-15 added -- currency of obligation, consent versus constitutive relation. Ratified by Josiah at K350 on the structural ground: routing it into HR-06 would give HR-06 a tributary that dissolves HR-06's own question. Birth certificate care-ethics#note, which the same ratification reclassified (b) -> (d)
- K351: HR-06 gains depends_on HR-15, and HR-15 declares sibling_of HR-03. Both kinds were already in the ratified vocabulary, so no extension was needed

### The corpus span, ruled

ONE corpus is pinned, the post-cut one, and it is earned rather than asserted. The tributaries span two cuts by AUTHORSHIP: phases A through E were authored against the pre-cut corpus 6ee1f6f31e0f012db0d58cae4f912fcb, Phase R and Phase F against the post-cut corpus pinned above. A register is a namespace consolidation rather than a corpus-pinned adjudication, so carrying two pins would misdescribe it. What makes the single pin honest is the SOURCE: this file derives from adversarial_map_v1_2.json, which asserts every one of its anchors verbatim against the post-cut corpus before it will write. So every tributary here was authored against whichever cut its phase met and is VERIFIED against the one named above. The shipped v0_1 pins the pre-cut corpus for the same reason in reverse, and that is the field this file repairs.

---

## Audit

- **[novel-flag-collision] `HR-05`** — HR-05 was registered before this program (canon:terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm) but 1 fragment entry/ies flag it novel=true: [('B2', 'harman-benign-creation')]. A bedrock has one birth certificate.
- **[adjacency-vocabulary-gap-CLOSED] `HR-14+HR-11`** — RESOLVED at K349: Josiah ratified a fifth relation kind, `conditions`, and HR-14+HR-11 is declared under it. The v0_2 statement of the gap is preserved verbatim below. HR-11 is the epistemic authority of the anti-extinction intuition against its evolutionary debunking. red-button-repugnant's own (a) answers the sophisticate variant by naming the survival firmware the framework already identifies, which is HR-11's subject matter, and the same node's sophisticate (d) is HR-14's birth certificate. Neither bedrock entails the other and both questions arise independently, so none of depends_on / stronger_than / sibling_of / independent_of states the relation: HR-11's resolution does not create or dissolve HR-14's question, it changes HR-14's FORCE. A fifth kind -- conditions -- would say it. Naming the gap rather than declaring a relation that misdescribes it, because the vocabulary is ratified and extending it is Josiah's.
- **[relations-drafted-L4] `HR-11+HR-02, HR-12+HR-10, HR-14+HR-05`** — Three relations are declared because three pairs came to share a tributary node when L4 reclassified R1's FAILS, and the adjacency gate refuses an undeclared pair. They are the drafting seat's, inside the ratified vocabulary, and are judged with the drafts (K258).

### Adjacency

14 candidates derived from the two signals, 19 relations declared, 5 declared beyond what the signals detect; 3 added at L4 (HR-02+HR-11, HR-05+HR-14, HR-10+HR-12).

Adjacency candidates are derived from two signals: a terminus_routing naming another bedrock, and a corpus node feeding two bedrocks. They are a FLOOR on what must be adjudicated, never a ceiling -- HR-04+HR-07 fires on neither and was found by hand, and so is HR-14+HR-11. An empty relations list is an assertion of independence rather than a default.

**Vocabulary gap — `HR-14+HR-11`:** HR-11 is the epistemic authority of the anti-extinction intuition against its evolutionary debunking. red-button-repugnant's own (a) answers the sophisticate variant by naming the survival firmware the framework already identifies, which is HR-11's subject matter, and the same node's sophisticate (d) is HR-14's birth certificate. Neither bedrock entails the other and both questions arise independently, so none of depends_on / stronger_than / sibling_of / independent_of states the relation: HR-11's resolution does not create or dissolve HR-14's question, it changes HR-14's FORCE. A fifth kind -- conditions -- would say it. Naming the gap rather than declaring a relation that misdescribes it, because the vocabulary is ratified and extending it is Josiah's.

---

## Bedrocks

A tributary marked `→L4` is an R1 FAILS that L4 reclassified (a) → (d); its phase is the phase that authored the move.

### HR-01 — Global normative / epistemic skepticism

Skepticism deep enough to dissolve all warrant dissolves the harm premise and the procreative license alike. The corpus defeats solipsism only as a LICENSE, never as metaphysics.

*Registered in:* `canon:terminal_stability_marker.honest_residuals.solipsism_global_skeptic`

**Tributaries (1 across 1 facet):**

- **dissolution-of-all-warrant** — `solipsism` (B2)

### HR-02 — Asymmetry-contingency of the positive-states cluster

The positive-states rebuttals run Benatar's asymmetry as the load-bearing spine and grant the hedonic premise arguendo. Reject the asymmetry and the spine goes with it. Ceiling: high-B by design.

*Registered in:* `canon:terminal_stability_marker.honest_residuals.asymmetry_dependent_amplifiers`

**Relations:**

- `depends_on` → `HR-03` — lives on HR-03's IMPERSONAL horn: the asymmetry is an impersonal-value claim, so the amplifier cluster is contingent on that horn being taken

**Tributaries (9 across 3 facets):**

- **impersonal-comparison-reading** — `self-effacing-under-universalization` (A)
- **intrinsic-value-of-existence** — `red-button-repugnant` (A→L4), `red-button-repugnant#medium` (A), `red-button-repugnant#archetypeVariants.sophisticate` (F→L4)
- **merely-possible-beneficiary** — `joy-outweighs-harms` (D), `privileged-first-world#archetypeVariants.defender` (F→L4), `suffering-makes-human` (D→L4), `survivor-testimony` (D→L4), `suffering-as-meaning` (D)

### HR-03 — Impersonal vs person-affecting axiology

*Alias:* `K224 bedrock 1`

Whether value and standing are seated in a standpoint-bearing individual or assessable impersonally. The corpus's universal conclusion needs the impersonal reading; the objector needs the person-affecting one. Neither side derives the other.

*Registered in:* `canon:terminal_stability_marker.honest_residuals.impersonal_vs_person_affecting`

**Tributaries (22 across 6 facets):**

- **absence-asymmetry** — `epistemic-humility` (B2)
- **aggregation-vs-iteration** — `population-ethics-paradoxes` (B2)
- **metaethical-locus** — `benatar-asymmetry-attack` (B1), `benatar-asymmetry-attack#archetypeVariants.defender` (F→L4)
- **relational-holist-seat-of-standing** — `care-ethics` (B2), `indigenous-philosophy` (B2)
- **unfacetted** — `love-beauty-art` (D), `extinction-culture` (C), `privileged-first-world` (E→L4), `slippery-slope-eugenics#short` (C), `marxist-materialist` (C)
- **value-requires-a-valuer** — `benatar-asymmetry-attack#archetypeVariants.blended` (F→L4), `benatar-asymmetry-attack#archetypeVariants.drifter` (F→L4), `benatar-asymmetry-attack#archetypeVariants.sophisticate` (F), `meaning-through-suffering` (B1→L4), `antinatalism-misanthropic#archetypeVariants.blended` (F→L4), `antinatalism-misanthropic#archetypeVariants.drifter` (F→L4), `antinatalism-misanthropic#archetypeVariants.sophisticate` (F), `anthropic-principle` (B1→L4), `performative-contradiction` (B2), `pragmatist-objection` (B2), `rights-future-generations` (C→L4)

### HR-04 — Moral realism / is-ought

*Alias:* `N1`

Whether suffering's disvalue is stance-independent. The corpus refuses to derive an ought from a fact, then requires an ought it does not derive either.

*Registered in:* `this-program`
  ·  *Birth certificate:* `phenomenological-existentialism#long` (phase B2)

**Relations:**

- `sibling_of` → `HR-01` — both dissolve verdicts, HR-01 by voiding all warrant and HR-04 by denying the ought is derivable; neither entails the other

**Tributaries (5 across 2 facets):**

- **conserved-property-under-redescription** — `eliminativism` (B2), `eliminativism#note` (G→L4)
- **stance-independence-of-disvalue** — `natural-reproduce#diagnosis` (E), `evolution-purpose#short` (D→L4), `phenomenological-existentialism` (B2)

### HR-05 — Comparative vs non-comparative harm

*Alias:* `N2`

Whether creation can wrong a being for whom no worse-off baseline exists.

*Registered in:* `canon:terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm`
  ·  *Birth certificate:* `harman-benign-creation#long` (phase B2)

**Relations:**

- `depends_on` → `HR-03` — lives on HR-03's PERSON-AFFECTING horn: go impersonal and the worse-off-baseline question does not arise, because no person needs a baseline

**Tributaries (12 across 1 facet):**

- **no-worse-off-baseline** — `life-gift` (E), `consent-both-ways` (D→L4), `imposing-values#short` (A→L4), `most-people-happy` (D→L4), `procreative-liberty` (B1), `speak-for-everyone` (D→L4), `consent-incoherent` (B1→L4), `cherry-picking-worst#short` (D→L4), `cherry-picking-worst#archetypeVariants.sophisticate` (F), `non-identity-problem` (B1), `harman-benign-creation` (B2), `incommensurability` (B2)

### HR-06 — Imposition wrong independent of harm

*Alias:* `N4 / bedrock-III`

Whether imposing an unrefusable condition on a non-antecedent subject is wrong whatever the harm ledger says.

*Registered in:* `this-program`
  ·  *Birth certificate:* `boonin-critique#short` (phase B2)

**Relations:**

- `depends_on` → `HR-03` — same person-affecting horn as HR-05: wronging without harm still requires a subject to be wronged
- `stronger_than` → `HR-05` — D4 ruling: HR-06 survives HR-05's resolution in either direction, since a wrong independent of harm needs no comparison to establish
- `depends_on` → `HR-15` — HR-15: HR-06 asks whether unauthorized imposition wrongs absent harm, which presupposes that authorization is the currency. Resolve HR-15 in care ethics' favour and HR-06's question does not arise; resolve it against and HR-06 is untouched. Same declared shape as HR-05 depends_on HR-03.

**Tributaries (5 across 1 facet):**

- **unrefusable-condition-on-non-antecedent-subject** — `masochist-counterexample` (D→L4), `moral-progress` (C→L4), `boonin-critique#short` (B2), `boonin-critique#note` (G→L4), `buddhist-objection` (B2→L4)

### HR-07 — Normative error theory

Categorical bindingness denied while the aversion datum is granted. Nothing in the corpus compels an error theorist who concedes that suffering is aversive.

*Registered in:* `this-program`
  ·  *Birth certificate:* `meta-ethical-pluralism#long` (phase A)

**Relations:**

- `depends_on` → `HR-04` — D3 finding: error theory is a stance WITHIN the HR-04 dispute that additionally denies categorical bindingness, a further question surviving either answer to HR-04. NOT detected by the adjacency signals; found by hand

**Tributaries (1 across 1 facet):**

- **categorical-bindingness-denial** — `meta-ethical-pluralism` (A)

### HR-08 — Sub specie aeternitatis quietism

The axiological-nihilist exit taken at the cosmic register: no verdict survives the view from nowhere, the corpus's included.

*Registered in:* `flagship_t5_register_dispositions_v0_1:heat-death-futility(defanged)`

**Relations:**

- `sibling_of` → `HR-01` — verdict dissolution at the cosmic register rather than by voiding warrant

**Tributaries (1 across 1 facet):**

- **cosmic-register-exit** — `heat-death-futility#medium` (A)

### HR-09 — Tolerance-weighting pluralism

A lexical priority placed above suffering-minimization. The corpus asserts the priority rather than deriving it.

*Registered in:* `flagship_t5_register_dispositions_v0_1:meta-ethical-pluralism(defanged)`

**Relations:**

- `independent_of` → `HR-07` — co-located at meta-ethical-pluralism, which is why the shared-node signal fires, but the claims are distinct and near-opposed: HR-07 denies that anything binds categorically, HR-09 asserts a competing value with lexical priority. Sharing a tributary node is a fact about where they surfaced, not about what they claim

**Tributaries (1 across 1 facet):**

- **lexical-priority-above-suffering-minimization** — `meta-ethical-pluralism#medium` (A)

### HR-10 — Radical holism / anti-theory

Refusal of invariant verdicts as such. Dissolves the corpus's universal conclusion and the objector's counter-verdict symmetrically.

*Registered in:* `flagship_t5_register_dispositions_v0_1:moral-particularism(defanged)`

**Relations:**

- `sibling_of` → `HR-01` — verdict dissolution by refusing invariant verdicts rather than by voiding warrant

**Tributaries (1 across 1 facet):**

- **refusal-of-invariant-verdicts** — `moral-particularism` (A)

### HR-11 — Epistemic authority of the anti-extinction intuition

Moorean datum versus its evolutionary debunking. The node registers the dispute rather than settling it.

*Registered in:* `node:negative-util-aggregation(evolved-attachment-not-truth-tracking)`

**Relations:**

- `conditions` → `HR-02` — L4, drafted: co-located at red-button-repugnant, where #44 reaches HR-11 and the (d) at #medium, with #45 and #47, sits on HR-02's intrinsic-value-of-existence facet. That (d) states the dispute HR-11 names -- 'The firmware genealogy cannot break the tie' -- and HR-11's own tributary cross-refers to this node's Moorean retreat, so the pair was adjacent before any signal could see it. HR-11's resolution changes the FORCE of HR-02's open question through that facet without creating or dissolving it: if the debunking succeeds, the staked value of existence loses the intuition that makes it more than a stake, and the question whether the positive-states rebuttals survive rejecting the asymmetry stays askable either way. Same shape as HR-14 conditions HR-11.

**Tributaries (2 across 1 facet):**

- **moorean-datum-vs-debunking** — `negative-util-aggregation` (B1), `red-button-repugnant` (A→L4)

### HR-12 — Ex ante vs ex post locus of contractualist justification

Prospects or outcomes as the justificand, type-standpoints as bearers. A live internal dispute the node registers.

*Registered in:* `node:contractualism-scanlon(live-internal-dispute)`

**Relations:**

- `independent_of` → `HR-10` — L4, drafted: co-located at moral-particularism, where the Phase A (d) is HR-10 and #61 reaches HR-12 through contractualism-scanlon. HR-10 refuses invariant verdicts as such; HR-12 asks which standpoint, prospects or outcomes, contractualist justification is indexed to. The particularist's refusal arises whichever index wins, and the index question arises inside contractualism with no particularism at all. Sharing a node is a fact about where #61 surfaced, not about what either bedrock claims.

**Tributaries (2 across 1 facet):**

- **ex-ante-vs-ex-post-justificand** — `contractualism-scanlon` (B1), `moral-particularism` (A→L4)

### HR-13 — Agent-neutral reasons grounding

*Alias:* `N1-reasons`

Whether suffering's disvalue generates a reason binding a procreator who is simply indifferent to the future subject. Affirming that the cosmos has no telos and no agent-neutral values is what strips such reasons of a source; the corpus asserts the relation binds rather than showing it does.

*Registered in:* `this-program`
  ·  *Birth certificate:* `nihilism-label#long` (phase D)

**Relations:**

- `depends_on` → `HR-04` — presupposes the HR-04 question: only once suffering's disvalue is stance-independent does it become askable whether that disvalue generates reasons binding an agent who is simply indifferent. A realist about value can deny agent-neutral reasons (the Humean position), so HR-13 survives either answer to HR-04
- `independent_of` → `HR-07` — adjacent but distinct: HR-07 denies that anything binds categorically, HR-13 asks whether what binds is agent-NEUTRAL. Agent-relative categorical reasons satisfy HR-07 and fail HR-13

**Tributaries (1 across 1 facet):**

- **binding-an-indifferent-agent** — `nihilism-label` (D)

### HR-14 — Create vs destroy: a positive case against existing beings

*Alias:* `K347 bedrock`

Whether an independently-motivated suffering-minimization layer grounds a positive case against beings who already exist. The corpus answers the ENTAILMENT question -- the antinatalist core does not entail the negative-utilitarian superstructure -- and leaves the MOTIVATION question open by ruling. Four nodes route the charge to red-button-repugnant, whose sophisticate slot states that holding it open rather than pretending it closed is that node's terminus, so the charge is answered in no locus: it is relocated until it reaches the one node whose disposition is to leave it standing. This bedrock is an artifact of the ROUTING GRAPH rather than of any text, which is why four per-locus phases could not see it.

*Registered in:* `this-program`
  ·  *Birth certificate:* `red-button-repugnant#archetypeVariants.sophisticate` (phase F)

**Relations:**

- `conditions` → `HR-11` — K349, Josiah: the first instance of the fifth kind. HR-11 is the epistemic authority of the anti-extinction intuition against its evolutionary debunking. If the debunking succeeds, HR-14's question -- whether the positive-eliminationist charge is answered anywhere in the corpus -- stays exactly as open, but far less turns on it, because the intuition generating the charge's rhetorical force loses its standing. If the debunking fails, HR-14's openness is a live scandal rather than a curiosity. Neither bedrock entails the other and both arise independently, so none of the four ratified kinds states it; what moves is FORCE, not existence.
- `independent_of` → `HR-02` — co-located at red-button-repugnant, which is why the shared-node signal fires, and the co-location is a fact about where they surfaced rather than about what they claim. HR-02 asks whether the positive-states cluster survives rejecting Benatar's asymmetry; HR-14 asks whether suffering-minimization grounds a positive case against beings who already exist. HR-14's question arises on either answer to HR-02. An intrinsic-value-of-existence verdict would change the LEDGER HR-14 is weighed on without dissolving the question, which is a different thing from a dependency
- `independent_of` → `HR-03` — co-located at slippery-slope-eugenics. HR-03 disputes whether value and standing are seated in a standpoint-bearing individual or assessable impersonally, and every one of its facets turns on merely-possible persons or on a valuerless world. HR-14 concerns beings who ALREADY HAVE standpoints and baselines -- it is the one residue in the register whose subjects are actual -- so the axiology dispute does not reach it and it arises on either horn
- `independent_of` → `HR-05` — L4, drafted: co-located at imposing-values, whose #short takes the creation symmetry (#13, HR-05) and whose #medium the terminal-outcome clause (#12, HR-14). HR-05 asks whether creation can wrong a being with no worse-off baseline; HR-14 concerns beings who already exist and have baselines. Neither resolution touches the other's question, the same ground on which HR-14 is already declared independent_of HR-03.

**Tributaries (11 across 4 facets):**

- **coercion-floor** — `slippery-slope-eugenics#archetypeVariants.sophisticate` (F)
- **positive-case-for-cessation** — `why-not-suicide` (E→L4), `why-not-suicide#archetypeVariants.sophisticate` (F), `violence-as-reductio#archetypeVariants.sophisticate` (F→L4)
- **successor-preference** — `ai-fear#short` (C→L4), `ai-fear#archetypeVariants.blended` (F→L4), `ai-fear#archetypeVariants.drifter` (F→L4), `ai-fear#archetypeVariants.sophisticate` (F)
- **terminus-held-open** — `imposing-values#medium` (A→L4), `violence-as-reductio` (C→L4), `red-button-repugnant#archetypeVariants.sophisticate` (F)

### HR-15 — Currency of obligation: consent versus constitutive relation

*Alias:* `rival-occupant`

Whether obligation is denominated in authorization by the obligated party, or constituted by the relation the parties stand in. The corpus's consent architecture presupposes the first; a developed relational ethics denies it, and nothing in-corpus derives either.

*Registered in:* `this-program`
  ·  *Birth certificate:* `care-ethics#note` (phase G)

**Relations:**

- `sibling_of` → `HR-03` — HR-03: both concern where the moral primitive is seated, neither derives the other. HR-03 is the seat of STANDING (what bears value); HR-15 is the currency of OBLIGATION (what makes a demand binding). They come apart both ways -- a relational holist can hold consent is the currency for impositions on individuals, and a natural-duties theorist denies consent-as-currency with no relational axiology at all.

**Tributaries (1 across 1 facet):**

- **unchosen-relations-bind-without-authorization** — `care-ethics#note` (G)

