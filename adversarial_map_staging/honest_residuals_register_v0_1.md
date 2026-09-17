# Honest-Residuals Register v0.1

**Status: WORKING.** Derived from 26 honest-residue (d) entries across phases A, B1, B2, C, E.
Source corpus `6ee1f6f3` / 82 nodes. Rebuild: `python3 build_register.py [--with-draft-d] [--with-e]`.

**Library-internal.** No corpus, ledger, index or `/combined` byte moves from this artifact.
Not for publication until the map is terminal.

---

## Why the register is an input, not only an output

The design doc schedules this for terminal assembly: *(d)-novel items appended to the
honest-residuals register*. That is one phase too late, for a mechanical reason.

Every (d) entry carries a `novel` boolean. With no register, a phase author decides that
boolean **from memory of the preceding phases** — Phase D recalling what B2 registered three
phases back. That is not a discipline, it is a recall test, and it has been failed once: the
succession brief records N1 (moral realism / is-ought) as *"first registered at nihilism-label
(d, novel) in Phase D"*, when the shipped B2 fragment carries its birth certificate at
`phenomenological-existentialism` with `novel: true`, and B2's own `eliminativism` entry
already routes to it as *"already-surfaced (N1)"*. B2 precedes D.

The builder now refuses to write when a bedrock carries more than one birth certificate.
Fed a Phase D fragment that flags N1 novel, it aborts with `HR-04 claims this-program
registration but has 2 novel=true entries (need exactly 1)`.

Phase E was authored against this register. Both of its (d) entries were decided by lookup
rather than recall, reused registered bedrock strings, and introduced no new birth
certificate — which is what the register is for.

## What the free text was hiding

**22 distinct `bedrock_name` strings collapse to 12 actual bedrocks.** Nothing was wrong with
any individual entry; the fragmentation is what happens when a shared namespace is authored
one phase at a time with no shared list to write against.

| | |
|---|---|
| Residue entries | 26 |
| Distinct shipped `bedrock_name` strings | 22 |
| Actual bedrocks | 12 |
| Registered before this program | 8 |
| Registered **by** this program | 4 |

## Audit

**`dangling-registration-pointer` — HR-03.** HR-03 cites K224 bedrock 1, which is not present in canon's terminal_stability_marker.honest_residuals. 10 tributaries route to a registration that exists only in a session receipt. Fold it into canon or the pointer cannot be checked.

## Adjacency (F1 remedy)

Over-individuation — one bedrock wearing two ids — is the failure the birth-certificate
check cannot see. Two mechanical signals now narrow which pairs must be adjudicated: a
`terminus_routing` naming another bedrock, and a corpus node feeding two bedrocks.

| | |
|---|---|
| Possible pairs | 66 |
| Candidates derived by signal | 4 |
| Relations declared | 9 |
| **Declared but undetected by any signal** | **5** |

The last row is the honest part. `HR-04+HR-07` is a real dependency neither signal fires on:
their terminus routings never name each other and they share no tributary node. It surfaced
by hand during the D3 triage. **The signals are a floor on what must be adjudicated,
never a ceiling**, and an empty relations list is now an assertion of independence rather than
a default: the audit refuses to write while any detected pair goes undeclared.

## The register

| id | bedrock | trib | facets | registered in |
|---|---|---|---|---|
| `HR-01` | Global normative / epistemic skepticism | 1 | 1 | canon |
| `HR-02` | Asymmetry-contingency of the positive-states cluster | 2 | 2 | canon |
| `HR-03` | Impersonal vs person-affecting axiology *(K224 bedrock 1)* | 10 | 6 | K224 |
| `HR-04` | Moral realism / is-ought *(N1)* | 3 | 2 | **this program** |
| `HR-05` | Comparative vs non-comparative harm *(N2)* | 3 | 1 | **this program** |
| `HR-06` | Imposition wrong independent of harm *(N4 / bedrock-III)* | 1 | 1 | **this program** |
| `HR-07` | Normative error theory | 1 | 1 | **this program** |
| `HR-08` | Sub specie aeternitatis quietism | 1 | 1 | flagship_t5_register_dispositions_v0_1 |
| `HR-09` | Tolerance-weighting pluralism | 1 | 1 | flagship_t5_register_dispositions_v0_1 |
| `HR-10` | Radical holism / anti-theory | 1 | 1 | flagship_t5_register_dispositions_v0_1 |
| `HR-11` | Epistemic authority of the anti-extinction intuition | 1 | 1 | node |
| `HR-12` | Ex ante vs ex post locus of contractualist justification | 1 | 1 | node |

### `HR-01` Global normative / epistemic skepticism

Skepticism deep enough to dissolve all warrant dissolves the harm premise and the procreative license alike. The corpus defeats solipsism only as a LICENSE, never as metaphysics.

**Registered before this program:** `canon:terminal_stability_marker.honest_residuals.solipsism_global_skeptic`.

**Tributaries (1 across 1 facet):**

- **dissolution-of-all-warrant** — `solipsism` (B2)

### `HR-02` Asymmetry-contingency of the positive-states cluster

The positive-states rebuttals run Benatar's asymmetry as the load-bearing spine and grant the hedonic premise arguendo. Reject the asymmetry and the spine goes with it. Ceiling: high-B by design.

**Registered before this program:** `canon:terminal_stability_marker.honest_residuals.asymmetry_dependent_amplifiers`.

**Relations:**

- `depends_on` → `HR-03` — lives on HR-03's IMPERSONAL horn: the asymmetry is an impersonal-value claim, so the amplifier cluster is contingent on that horn being taken

**Tributaries (2 across 2 facets):**

- **impersonal-comparison-reading** — `self-effacing-under-universalization` (A)
- **intrinsic-value-of-existence** — `red-button-repugnant` (A)

### `HR-03` Impersonal vs person-affecting axiology — *K224 bedrock 1*

Whether value and standing are seated in a standpoint-bearing individual or assessable impersonally. The corpus's universal conclusion needs the impersonal reading; the objector needs the person-affecting one. Neither side derives the other.

**Registered before this program:** `K224:bedrock-1`.

**Tributaries (10 across 6 facets):**

- **absence-asymmetry** — `epistemic-humility` (B2)
- **aggregation-vs-iteration** — `population-ethics-paradoxes` (B2)
- **metaethical-locus** — `benatar-asymmetry-attack` (B1)
- **relational-holist-seat-of-standing** — `care-ethics` (B2), `indigenous-philosophy` (B2)
- **unfacetted** — `extinction-culture` (C), `slippery-slope-eugenics` (C), `marxist-materialist` (C)
- **value-requires-a-valuer** — `performative-contradiction` (B2), `pragmatist-objection` (B2)

### `HR-04` Moral realism / is-ought — *N1*

Whether suffering's disvalue is stance-independent. The corpus refuses to derive an ought from a fact, then requires an ought it does not derive either.

**Birth certificate:** phase B2, `phenomenological-existentialism#long`.

**Relations:**

- `sibling_of` → `HR-01` — both dissolve verdicts, HR-01 by voiding all warrant and HR-04 by denying the ought is derivable; neither entails the other

**Tributaries (3 across 2 facets):**

- **conserved-property-under-redescription** — `eliminativism` (B2)
- **stance-independence-of-disvalue** — `phenomenological-existentialism` (B2), `natural-reproduce` (E)

### `HR-05` Comparative vs non-comparative harm — *N2*

Whether creation can wrong a being for whom no worse-off baseline exists.

**Birth certificate:** phase B2, `harman-benign-creation#long`.

**Relations:**

- `depends_on` → `HR-03` — lives on HR-03's PERSON-AFFECTING horn: go impersonal and the worse-off-baseline question does not arise, because no person needs a baseline

**Tributaries (3 across 1 facet):**

- **no-worse-off-baseline** — `harman-benign-creation` (B2), `incommensurability` (B2), `life-gift` (E)

### `HR-06` Imposition wrong independent of harm — *N4 / bedrock-III*

Whether imposing an unrefusable condition on a non-antecedent subject is wrong whatever the harm ledger says.

**Birth certificate:** phase B2, `boonin-critique#short`.

**Relations:**

- `depends_on` → `HR-03` — same person-affecting horn as HR-05: wronging without harm still requires a subject to be wronged
- `stronger_than` → `HR-05` — D4 ruling: HR-06 survives HR-05's resolution in either direction, since a wrong independent of harm needs no comparison to establish

**Tributaries (1 across 1 facet):**

- **unrefusable-condition-on-non-antecedent-subject** — `boonin-critique` (B2)

### `HR-07` Normative error theory

Categorical bindingness denied while the aversion datum is granted. Nothing in the corpus compels an error theorist who concedes that suffering is aversive.

**Birth certificate:** phase A, `meta-ethical-pluralism#long`.

**Relations:**

- `depends_on` → `HR-04` — D3 finding: error theory is a stance WITHIN the HR-04 dispute that additionally denies categorical bindingness, a further question surviving either answer to HR-04. NOT detected by the adjacency signals; found by hand

**Tributaries (1 across 1 facet):**

- **categorical-bindingness-denial** — `meta-ethical-pluralism` (A)

### `HR-08` Sub specie aeternitatis quietism

The axiological-nihilist exit taken at the cosmic register: no verdict survives the view from nowhere, the corpus's included.

**Registered before this program:** `flagship_t5_register_dispositions_v0_1:heat-death-futility(defanged)`.

**Relations:**

- `sibling_of` → `HR-01` — verdict dissolution at the cosmic register rather than by voiding warrant

**Tributaries (1 across 1 facet):**

- **cosmic-register-exit** — `heat-death-futility` (A)

### `HR-09` Tolerance-weighting pluralism

A lexical priority placed above suffering-minimization. The corpus asserts the priority rather than deriving it.

**Registered before this program:** `flagship_t5_register_dispositions_v0_1:meta-ethical-pluralism(defanged)`.

**Relations:**

- `independent_of` → `HR-07` — co-located at meta-ethical-pluralism, which is why the shared-node signal fires, but the claims are distinct and near-opposed: HR-07 denies that anything binds categorically, HR-09 asserts a competing value with lexical priority. Sharing a tributary node is a fact about where they surfaced, not about what they claim

**Tributaries (1 across 1 facet):**

- **lexical-priority-above-suffering-minimization** — `meta-ethical-pluralism` (A)

### `HR-10` Radical holism / anti-theory

Refusal of invariant verdicts as such. Dissolves the corpus's universal conclusion and the objector's counter-verdict symmetrically.

**Registered before this program:** `flagship_t5_register_dispositions_v0_1:moral-particularism(defanged)`.

**Relations:**

- `sibling_of` → `HR-01` — verdict dissolution by refusing invariant verdicts rather than by voiding warrant

**Tributaries (1 across 1 facet):**

- **refusal-of-invariant-verdicts** — `moral-particularism` (A)

### `HR-11` Epistemic authority of the anti-extinction intuition

Moorean datum versus its evolutionary debunking. The node registers the dispute rather than settling it.

**Registered before this program:** `node:negative-util-aggregation(evolved-attachment-not-truth-tracking)`.

**Tributaries (1 across 1 facet):**

- **moorean-datum-vs-debunking** — `negative-util-aggregation` (B1)

### `HR-12` Ex ante vs ex post locus of contractualist justification

Prospects or outcomes as the justificand, type-standpoints as bearers. A live internal dispute the node registers.

**Registered before this program:** `node:contractualism-scanlon(live-internal-dispute)`.

**Tributaries (1 across 1 facet):**

- **ex-ante-vs-ex-post-justificand** — `contractualism-scanlon` (B1)

