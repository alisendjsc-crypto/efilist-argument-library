# Honest-Residuals Register v0.2

**Status: WORKING, and derived from a terminal artifact.** 39 honest-residue (d) entries consolidated from `adversarial_map_v1_1.json` (e9e5abf8), which is the successor assembly.
Contributing phases: A (6), B1 (5), B2 (12), C (3), D (4), E (2), F (7). Contributing nothing: R.
Source corpus `04bf6482` / 82 nodes. Rebuild: `python3 build_register_v0_2.py`.

**Library-internal.** No corpus, ledger, index or `/combined` byte moves from this artifact.

---

## What moved from v0.1

- source is adversarial_map_v1_1.json rather than six fragment files
- HR-14 added, with the three facets canon records plus the terminus that holds it open
- HR-05 registered_in repointed at canon: K345 folded it into terminal_stability_marker.honest_residuals, so v0_1's dangling-pointer finding is STALE and is dropped as a CORRECTION. Its novel-flag collision is untouched and stands
- the corpus pin moves to the post-cut corpus, on the grounds in corpus_span_ruling
- an adjacency the ratified four-kind vocabulary cannot express is recorded in the audit rather than declared as a relation that would misdescribe it

### The corpus span, ruled

ONE corpus is pinned, the post-cut one, and it is earned rather than asserted. The tributaries span two cuts by AUTHORSHIP: phases A through E were authored against the pre-cut corpus 6ee1f6f31e0f012db0d58cae4f912fcb, Phase R and Phase F against the post-cut corpus pinned above. A register is a namespace consolidation rather than a corpus-pinned adjudication, so carrying two pins would misdescribe it. What makes the single pin honest is the SOURCE: this file derives from adversarial_map_v1_1.json, which asserts every one of its anchors verbatim against the post-cut corpus before it will write. So every tributary here was authored against whichever cut its phase met and is VERIFIED against the one named above. The shipped v0_1 pins the pre-cut corpus for the same reason in reverse, and that is the field this file repairs.

### Parity

Restricted to phases ['A', 'B1', 'B2', 'C', 'D', 'E'], every bedrock's name, alias, gloss, registered_in, relations and facet tributaries equal v0_1's, except HR-05.registered_in, which this file deliberately moves. Tributaries inside a facet are compared as a sorted multiset because their ORDER moved from fragment-internal to corpus order when the source became the corpus-ordered assembly; the bedrocks whose facet order that actually re-sequenced are listed below. The build refuses to write on any difference of content.

---

## Audit

- **[novel-flag-collision] `HR-05`** — HR-05 was registered before this program (canon:terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm) but 1 fragment entry/ies flag it novel=true: [('B2', 'harman-benign-creation')]. A bedrock has one birth certificate.
- **[adjacency-vocabulary-gap] `HR-14+HR-11`** — HR-11 is the epistemic authority of the anti-extinction intuition against its evolutionary debunking. red-button-repugnant's own (a) answers the sophisticate variant by naming the survival firmware the framework already identifies, which is HR-11's subject matter, and the same node's sophisticate (d) is HR-14's birth certificate. Neither bedrock entails the other and both questions arise independently, so none of depends_on / stronger_than / sibling_of / independent_of states the relation: HR-11's resolution does not create or dissolve HR-14's question, it changes HR-14's FORCE. A fifth kind -- conditions -- would say it. Naming the gap rather than declaring a relation that misdescribes it, because the vocabulary is ratified and extending it is Josiah's.

### Adjacency

7 candidates derived from the two signals, 13 relations declared, 6 declared beyond what the signals detect.

Adjacency candidates are derived from two signals: a terminus_routing naming another bedrock, and a corpus node feeding two bedrocks. They are a FLOOR on what must be adjudicated, never a ceiling -- HR-04+HR-07 fires on neither and was found by hand, and so is HR-14+HR-11. An empty relations list is an assertion of independence rather than a default.

**Vocabulary gap — `HR-14+HR-11`:** HR-11 is the epistemic authority of the anti-extinction intuition against its evolutionary debunking. red-button-repugnant's own (a) answers the sophisticate variant by naming the survival firmware the framework already identifies, which is HR-11's subject matter, and the same node's sophisticate (d) is HR-14's birth certificate. Neither bedrock entails the other and both questions arise independently, so none of depends_on / stronger_than / sibling_of / independent_of states the relation: HR-11's resolution does not create or dissolve HR-14's question, it changes HR-14's FORCE. A fifth kind -- conditions -- would say it. Naming the gap rather than declaring a relation that misdescribes it, because the vocabulary is ratified and extending it is Josiah's.

---

## Bedrocks

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

**Tributaries (4 across 3 facets):**

- **impersonal-comparison-reading** — `self-effacing-under-universalization` (A)
- **intrinsic-value-of-existence** — `red-button-repugnant` (A)
- **merely-possible-beneficiary** — `joy-outweighs-harms` (D), `suffering-as-meaning` (D)

### HR-03 — Impersonal vs person-affecting axiology

*Alias:* `K224 bedrock 1`

Whether value and standing are seated in a standpoint-bearing individual or assessable impersonally. The corpus's universal conclusion needs the impersonal reading; the objector needs the person-affecting one. Neither side derives the other.

*Registered in:* `canon:terminal_stability_marker.honest_residuals.impersonal_vs_person_affecting`

**Tributaries (13 across 6 facets):**

- **absence-asymmetry** — `epistemic-humility` (B2)
- **aggregation-vs-iteration** — `population-ethics-paradoxes` (B2)
- **metaethical-locus** — `benatar-asymmetry-attack` (B1)
- **relational-holist-seat-of-standing** — `care-ethics` (B2), `indigenous-philosophy` (B2)
- **unfacetted** — `love-beauty-art` (D), `extinction-culture` (C), `slippery-slope-eugenics` (C), `marxist-materialist` (C)
- **value-requires-a-valuer** — `benatar-asymmetry-attack` (F), `antinatalism-misanthropic` (F), `performative-contradiction` (B2), `pragmatist-objection` (B2)

### HR-04 — Moral realism / is-ought

*Alias:* `N1`

Whether suffering's disvalue is stance-independent. The corpus refuses to derive an ought from a fact, then requires an ought it does not derive either.

*Registered in:* `this-program`
  ·  *Birth certificate:* `phenomenological-existentialism#long` (phase B2)

**Relations:**

- `sibling_of` → `HR-01` — both dissolve verdicts, HR-01 by voiding all warrant and HR-04 by denying the ought is derivable; neither entails the other

**Tributaries (3 across 2 facets):**

- **conserved-property-under-redescription** — `eliminativism` (B2)
- **stance-independence-of-disvalue** — `natural-reproduce` (E), `phenomenological-existentialism` (B2)

### HR-05 — Comparative vs non-comparative harm

*Alias:* `N2`

Whether creation can wrong a being for whom no worse-off baseline exists.

*Registered in:* `canon:terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm`
  ·  *Birth certificate:* `harman-benign-creation#long` (phase B2)

**Relations:**

- `depends_on` → `HR-03` — lives on HR-03's PERSON-AFFECTING horn: go impersonal and the worse-off-baseline question does not arise, because no person needs a baseline

**Tributaries (6 across 1 facet):**

- **no-worse-off-baseline** — `life-gift` (E), `procreative-liberty` (B1), `cherry-picking-worst` (F), `non-identity-problem` (B1), `harman-benign-creation` (B2), `incommensurability` (B2)

### HR-06 — Imposition wrong independent of harm

*Alias:* `N4 / bedrock-III`

Whether imposing an unrefusable condition on a non-antecedent subject is wrong whatever the harm ledger says.

*Registered in:* `this-program`
  ·  *Birth certificate:* `boonin-critique#short` (phase B2)

**Relations:**

- `depends_on` → `HR-03` — same person-affecting horn as HR-05: wronging without harm still requires a subject to be wronged
- `stronger_than` → `HR-05` — D4 ruling: HR-06 survives HR-05's resolution in either direction, since a wrong independent of harm needs no comparison to establish

**Tributaries (1 across 1 facet):**

- **unrefusable-condition-on-non-antecedent-subject** — `boonin-critique` (B2)

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

- **cosmic-register-exit** — `heat-death-futility` (A)

### HR-09 — Tolerance-weighting pluralism

A lexical priority placed above suffering-minimization. The corpus asserts the priority rather than deriving it.

*Registered in:* `flagship_t5_register_dispositions_v0_1:meta-ethical-pluralism(defanged)`

**Relations:**

- `independent_of` → `HR-07` — co-located at meta-ethical-pluralism, which is why the shared-node signal fires, but the claims are distinct and near-opposed: HR-07 denies that anything binds categorically, HR-09 asserts a competing value with lexical priority. Sharing a tributary node is a fact about where they surfaced, not about what they claim

**Tributaries (1 across 1 facet):**

- **lexical-priority-above-suffering-minimization** — `meta-ethical-pluralism` (A)

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

**Tributaries (1 across 1 facet):**

- **moorean-datum-vs-debunking** — `negative-util-aggregation` (B1)

### HR-12 — Ex ante vs ex post locus of contractualist justification

Prospects or outcomes as the justificand, type-standpoints as bearers. A live internal dispute the node registers.

*Registered in:* `node:contractualism-scanlon(live-internal-dispute)`

**Tributaries (1 across 1 facet):**

- **ex-ante-vs-ex-post-justificand** — `contractualism-scanlon` (B1)

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

- `independent_of` → `HR-02` — co-located at red-button-repugnant, which is why the shared-node signal fires, and the co-location is a fact about where they surfaced rather than about what they claim. HR-02 asks whether the positive-states cluster survives rejecting Benatar's asymmetry; HR-14 asks whether suffering-minimization grounds a positive case against beings who already exist. HR-14's question arises on either answer to HR-02. An intrinsic-value-of-existence verdict would change the LEDGER HR-14 is weighed on without dissolving the question, which is a different thing from a dependency
- `independent_of` → `HR-03` — co-located at slippery-slope-eugenics. HR-03 disputes whether value and standing are seated in a standpoint-bearing individual or assessable impersonally, and every one of its facets turns on merely-possible persons or on a valuerless world. HR-14 concerns beings who ALREADY HAVE standpoints and baselines -- it is the one residue in the register whose subjects are actual -- so the axiology dispute does not reach it and it arises on either horn

**Tributaries (4 across 4 facets):**

- **coercion-floor** — `slippery-slope-eugenics` (F)
- **positive-case-for-cessation** — `why-not-suicide` (F)
- **successor-preference** — `ai-fear` (F)
- **terminus-held-open** — `red-button-repugnant` (F)

