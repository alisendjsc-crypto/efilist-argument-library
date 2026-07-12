# Adversarial Objection/Rebuttal Map — Design v0.1
*(Library seat, 2026-07-11 · answers `adversarial_map_commission_relay_v1.md` · Exchange 151 candidate · DESIGN ONLY — zero map entries authored here)*

## 0. Contract restated in one line
For each of the 82 shipped nodes: the strongest continuation a maximally competent hostile interlocutor deploys **against our v4.0.0 text as written**, triaged into four disposition classes — the fidelity-ceiling mechanism inverted, overshoot promoted from exception to product.

## 1. Artifact schema

Machine skeleton in the sibling `adversarial_map_schema_v0_1.json`. Per entry:

```json
{
  "target_id": "<∈ corpus 6ee1f6f3 id set, n=82>",
  "target_locus": "short|medium|long|diagnosis",
  "target_anchor": "<≤15-word verbatim quote of the shipped clause the move engages>",
  "adversarial_move": "<40–150 words; the continuation at full strength>",
  "class": "a|b|c|d",
  "grounds": "<why this class; for (b): why the shipped text's best reading does not already meet it>",
  "routing": { "<class-shaped, see §2>" },
  "status": "mapped",
  "provenance": {"phase": "<A|B1|B2|C|D>", "date": "", "seat": ""}
}
```

Map-level meta: source-corpus pin (`6ee1f6f31e0f...` / 82 / tier split 13/17/14/31/7), register-law pointer, per-phase coverage arithmetic, class-count summary.

**Register of `adversarial_move`:** compressed analytic statement, not first-person performance. This is triage infrastructure, not a reader-facing asset; performance register (scholar-style) is a downstream vendoring decision if yields feed the game. Explicit dilemma structure encouraged; rhetoric banned.

**Coverage contract:** every node gets ≥1 entry — a confident (a) or (d) is itself the routing datum. Cap 3 entries/node; the contract is the *strongest* continuation, not all continuations.

## 2. Class law (adjudication order: a → c → b/d)

| class | test | routing shape | precedent |
|---|---|---|---|
| **(a) ALREADY-ANSWERED** | the move's best formulation is *met* (not merely addressable) by shipped prose somewhere in-corpus | `{"answered_by": ["node_id#depth", ...]}` | the 81-authoring null yield |
| **(c) NEW-NODE** | not a continuation of this node's dialectic at all — seed-1 individuation grounds: presupposition inversion, reader test, grading-object integrity | `{"intake_candidate": {"proposed_id","tier_guess","mechanism_guess","individuation_grounds"}}` | `self-effacing-under-universalization` |
| **(b) STRENGTHEN** | defeats the shipped prose (gap, equivocation, underpowered analogy) but not the position; a stronger text inside the node's identity meets it | `{"regen_candidate": {"axis_hit": ["c","r",...], "severity": "minor|headline"}}` | `contractualism-scanlon` B→A |
| **(d) HONEST-RESIDUE** | names bedrock — already-registered (solipsism dissolve-not-defeat; asymmetry-contingent amplifiers) or **new** bedrock the sweep surfaces | `{"residue": {"bedrock_name", "terminus_routing", "novel": bool}}` | solipsism |

**(c) before (b)** because a move that beats the shipped prose *by being a different objection* is (c), not (b) — exactly the S4 flag's history.

**Anti-inflation gates** (the ceiling's discipline substitute, since the bound is removed):
1. **Anchor rule** — no entry without `target_anchor`; the move must engage a clause we actually shipped, killing mechanism-generic counters.
2. **Force floor** — `grounds` must state why the shipped text's *best reading* fails; a move met on charitable reading is (a).
3. **(a)-brevity cap** — ≤60 words of move-statement; (a) entries are routing data, not essays.
4. **Regress stop** — one round only: the opponent's next move after *our* answer; no counter-counter chains. Depth-2 dialectic is the card game's job, fed by (a) edges.

## 3. Phasing — recommendation: tier-descending, mechanism-adjacent within phase

| phase | scope | n | seats | expected yield profile |
|---|---|---|---|---|
| **A (pilot)** | T5 | 7 | 0.5–0.7 | calibrates all four classes; the defanged trio (heat-death, meta-ethical-pluralism, particularism) are natural (d) exemplars; routed quartet stress-tests (a)/(b) boundary |
| **B1 / B2** | T4 | 31 | 1 + 1 (15/16 split) | the (b)/(c) core — where the sophisticated counters live |
| **C** | T3 + T2 | 31 | 1–1.5 | shifts toward (a) routing data — game material; cheaper per node |
| **D** | T1 | 13 | 0.5 (fold into C's second seat if budget holds) | near-pure (a); fast |

**Total: 4–5 authoring seats** + per-phase Cowork micro-folds + one terminal assembly fold.

**Why not mechanism-clustered as primary axis:** clustering generates counters against the *mechanism class*, diluting the against-OUR-text contract — the anchor rule exists precisely because that drift is the failure mode. Mechanism adjacency survives as *secondary ordering within phases*: shared-structure counters (one flawed move reused across nodes) get caught and cross-referenced without becoming the unit of analysis. Tier-descending front-loads the intake-relevant discoveries and matches the scholar program's demonstrated density gradient.

**Pilot-first** per program precedent (S1 → S4). Phase A additionally carries the parked **Map-1 curation elective for node 82** as a rider — the pilot reads that node's full dialectic anyway; marginal cost near zero. DEP_GRAPH inert-counter strip stays parked, unbundled.

## 4. Staging home
`adversarial_map_staging/` at repo root — **version-neutral** deliberately: (b)/(c) yields route to whichever future bundled cut ratifies them (v4.1/v5 scoping is downstream); naming the dir by target version would presume the target. Contents: `adv_map_phase{A|B1|B2|C|D}_v0_1.json` fragments + terminal `adversarial_map_v1_0.json` assembly. Map is LIBRARY-INTERNAL: no deploy, no combined/ledger/index bytes, until a deliberate fold decision.

## 5. Status lifecycle for (b)/(c) yields
`mapped → queued (Josiah triage) → ratified → landed(version) | rejected(grounds)`. The map records `mapped` only; everything downstream lives in canon agenda + the normal staging → cold-grade → assembly chain. No entry authorizes a byte.

## 6. Cowork owes per fold
- **Per phase:** collect fragment → validator run → md5/byte pin → coordination-doc exchange log → git commit. **First fold only:** canon MINOR adding the `adversarial_map` block (keyset delta logged).
- **Terminal:** assembly build (fragments partition the 82, id-preferring dedupe — scholar pattern), class-count summary into canon, extraction of the (b)/(c) queue as a v-cut scoping input, (d)-novel items appended to the honest-residuals register.
- **Never:** corpus/ledger/index/combined touches from this program.

**Validator spec** (`adv_map_validator_v0_1.py`, Cowork implements — mechanical): target_id ∈ 82 ∧ id×anchor unique; per-phase union arithmetic → 82/82 at terminal; class ∈ {a,b,c,d} with class-shaped routing (schema in the JSON sibling); anchor ≤15 words ∧ verbatim-in-corpus check (substring against the target node's shipped text — the anchor rule made programmatic); move band 40–150; status enum; serialization round-trip.

## 7. Open questions (Josiah)
1. Cap 3 entries/node — ratify or amend?
2. Phase-A rider (Map-1 curation of node 82) — elect now or keep parked?
3. Terminal artifact name `adversarial_map_v1_0.json` — or reserve `v1_0` for post-triage state?

## 8. Sequencing executed this seat
R1 + R2 authored and assembled first (warm-up claim honored — re-entering ceiling discipline before designing its inversion): `scholar-objections_v1_1.json` (82/82, md5 `20999eb9`) + micro-fragment delta. Design above is the hand-back; Phase A opens on ratification.
