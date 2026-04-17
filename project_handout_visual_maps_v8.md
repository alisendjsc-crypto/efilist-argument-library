# PROJECT HANDOUT: EFIList Argument Library — v3.6.1 with Map 1 + Override Audit
## For continuation in a new Claude session

---

## PROJECT STATE

### What Exists (v3.6.1)
The EFIList Argument Library is now complete with all four maps:
- **74 objections** across 5 tiers, **222 pre-built responses** at 3 depth levels
- **Map 2 — Psychological Mechanism Web** (D3.js force-directed graph)
  - 34 canonical mechanism clusters, 74 objection nodes, 118 edges
- **Map 3 — Philosophical Dependency Graph** (D3.js stratified layout)
  - 13 premise nodes (9 foundational, 4 diagnostic), 74 objection nodes, 222 edges (post-audit)
  - Two-layer architecture, edge strength classification, review confidence system
- **Map 1 — Argument Flow Map (NEW in v3.6, audited in v3.6.1)** (D3.js radial/ego-centric layout)
  - Debate navigation tree: 74 source nodes, **869 blended-union edges** (was 873 pre-audit)
  - Three-mode architecture: Sophisticate / Defender / Drifter / Blended
  - Per-node disengagement probability indicator (7 HIGH / 59 MEDIUM / 8 LOW)
  - Convergence indicators (★★★ / ★★ / ★) on blended edges
  - Two-mechanism disclosure on 44 edges (nuclear retreat + collapse)
  - **10 canonical sophisticate overrides** flagged in-UI (was 15; 4 dropped and 1 demoted in audit-v1)
  - User-facing methodology panel (same pattern as Map 3)
- **Rebuttal Strength Index (RSI)** — 5-axis scoring on all 74 entries
- **Bidirectional cross-linking** across all four views
- **Features:** keyword search, tier filtering, 3 response depths, copy-to-clipboard, view switcher (LIBRARY | MECHANISM WEB | DEPENDENCY GRAPH | ARGUMENT FLOW)

### Files
| File | Version | Status |
|------|---------|--------|
| `index.html` (online) | v3.6 | Primary tool; D3 from CDN; ~1.22 MB |
| `efilist_argument_library_v34_offline.html` | v3.4 | **OUTDATED — no v3.5 or v3.6 updates** |
| `efilist_argument_library.json` | v3.4 | **OUTDATED** |
| `efilist_argument_library.jsx` | v3.4 (partial) | **OUTDATED — no RSI, no Map 1** |
| `README.md` | v3.5 | **Needs v3.6 update (Map 1 section)** |

### Architecture (v3.6)
Four integrated views sharing the OBJECTIONS array. D3 lazy-initializes each map only when the user switches. Cross-linking works in all directions.

**Data structures (script block):**
- `OBJECTIONS` — 74 entries
- `TIERS`, `DEP_FAMILY_COLORS`, `DEP_TIER_COLORS`, `MAP_TIER_COLORS`, `MAP_MECH_COLORS`
- `MAP_GRAPH_DATA` — Map 2 mechanism web data
- `DEP_GRAPH_DATA` — Map 3 dependency graph data (post-audit)
- `DEP_REVIEW_NOTES` — review confidence flags
- `REBUTTAL_STRENGTH` — RSI scores
- `MAP1_TRANSITIONS` (NEW) — 74 source nodes × 4 views (sophisticate/defender/drifter/blended) with rationale, weights, convergence, disclosure flags

**Map 1 functions:**
- `initMap1()` — lazy-init on first view switch
- `m1RenderSourceList()` — left-hand tier-grouped source node list with disengagement badges
- `m1SelectSource(id)` — click handler; updates graph + detail panel
- `m1SetMode(mode)` — toggles between blended/sophisticate/defender/drifter
- `m1RenderGraph()` — renders radial SVG: source at center, successors on arc
- `m1RenderDetail()` — right-hand panel with expandable edge cards, disclosure notes, jump buttons
- `toggleMap1Methodology()` — methodology panel toggle

---

## v3.6 SESSION CHANGELOG — MAP 1 BUILD

### Session workflow
1. Read v5 handout, confirmed path: Map 1 debate navigation tree
2. Architecture chosen: **three modes (Sophisticate / Defender / Drifter) + blended default view**
3. Generation approach chosen: **rules-first methodology, user review, then algorithmic generation**
4. Weight system chosen: **3-tier categorical (HIGH / MEDIUM / LOW)**
5. Published methodology v1.0 with 6 open questions for user decision
6. User locked Q1-Q6 decisions (see `map1_methodology_v1_1_locked.md`)
7. Generator run over all 74 nodes — produced 354 sophisticate + 262 defender + 370 drifter + 873 blended-union edges
8. Spot-check on 5 diagnostic nodes confirmed philosophical coherence
9. Tightening pass: Sophisticate LOW threshold raised to require ≥1 strong OR ≥2 weak premises (dropped 3 marginal edges)
10. Integration patch applied to index.html — all structural audits pass
11. Runtime smoke test: 74 nodes × 4 modes = 296 render calls, zero failures

### Headline finding: convergence distribution
After generation, the distribution of blended edges by convergence tier:

| Convergence | Count | % |
|---|---|---|
| ★★★ (all 3 modes agree) | 3 | 0.3% |
| ★★ (2 modes agree) | 104 | 11.9% |
| ★ (single mode only) | 766 | 87.7% |

**87.7% single-mode distribution validates the three-mode architecture.** If modes were redundant, we would see majority ★★★ convergence. The observed result shows Sophisticate / Defender / Drifter select substantively different successors almost all the time. Collapsing to a single blended matrix would have destroyed ~88% of the predictive information. This is the empirical vindication of three-mode architecture.

### Q1-Q6 locked decisions

| # | Question | Decision |
|---|---|---|
| Q1 | Sophisticate tier-elevation bonus | APPROVED — sophisticates escalate, not regress |
| Q2 | Defender collapse T4→T1 boosted | APPROVED — defender losing argument regresses to ad hominem |
| Q3 | Nuclear retreat T1→T5 | In BOTH Defender and Drifter modes, with user-facing two-mechanism disclosure note |
| Q4 | Disengagement probability per node | APPROVED — 7 HIGH / 59 MEDIUM / 8 LOW |
| Q5 | Canonical sophisticate overrides | Applied at generation (15 total); audit-v1 subsequently dropped 4 and demoted 1 (10 retained). See `map1_override_audit_v1.md`. |
| Q6 | Convergence weighting | Separate indicator (★★★/★★/★), does not override mode-local weights; both displayed transparently |

---

## MAP 1 — FULL OPERATIONAL SPEC

### Three modes

**SOPHISTICATE** — Premise-pivot-driven. Pulls from Map 3. If response to A invokes Premise P, sophisticate next-move targets P. Favors tier-elevation (T1→T4), Genuine Philosophical + Meta-Objection categories. Suppresses tier-regression and Emotional/Reflexive pivots.

**DEFENDER** — Mechanism-retreat-driven. Pulls from Map 2. Same-mechanism retreat primary, same-mechType pivots secondary. Favors tier-lateral and tier-descending moves. Boosts T4→T1 collapse edges. Suppresses pivots to "genuine" mechType nodes.

**DRIFTER** — Tier-gravity-driven. Same-tier same-category strongest. One-tier adjacent medium. Multi-tier leaps dropped *except* T1→T5 nuclear retreat and T4→T1 collapse (preserved at LOW weight as rare-but-characteristic).

**BLENDED (default)** — Union of all three. Convergence indicated by star count. Mode-local weights preserved (a HIGH-weight single-mode edge is still HIGH; stars are separate signal).

### Weight buckets

- **HIGH** — High-confidence next-move. Sophisticate: ≥3 shared strong premises + tier-elevating + Genuine/Meta category. Defender: ≥2 shared mechanisms + tier-equal-or-descending + non-genuine mechType. Drifter: same-tier same-category.
- **MEDIUM** — Plausible next-move. Mid-confidence match.
- **LOW** — Possible but less likely next-move. Includes nuclear-retreat and collapse edges.

### Two-mechanism disclosure (nuclear retreat + collapse)

Nuclear retreat (T1→T5) and collapse (T4→T1) appear in both Defender and Drifter modes because two forces produce the same move: worldview-defense (Defender) and emotional exhaustion (Drifter). Each such edge carries a user-visible disclosure note explaining both readings.

### Canonical sophisticate overrides (10 retained after audit-v1)

For T4/T5 high-philosophy nodes where premise-matching under-predicts the textbook academic next-move, canonical overrides were applied at generation time (15 total). Audit-v1 then dropped 4 edges entirely (family-resemblance failure mode) and demoted 1 edge from override status while preserving it as an ordinary premise-matched edge.

**Retained (10):**

1. `benatar-asymmetry-attack` → `boonin-critique` (HIGH)
2. `consent-incoherent` → `non-identity-problem` (HIGH)
3. `harman-benign-creation` → `population-ethics-paradoxes` (MEDIUM)
4. `boonin-critique` → `bradley-no-subject` (MEDIUM)
5. `bradley-no-subject` → `incommensurability` (MEDIUM) *(borderline)*
6. `non-identity-problem` → `harman-benign-creation` (MEDIUM)
7. `population-ethics-paradoxes` → `negative-util-aggregation` (HIGH)
8. `meta-ethical-pluralism` → `moral-particularism` (MEDIUM)
9. `flow-states-csikszentmihalyi` → `hedonic-contrast` (MEDIUM) *(borderline)*
10. `neuroscience-positive-states` → `flow-states-csikszentmihalyi` (MEDIUM)

**Demoted from canonical-override status but edge preserved (1):**

- `contractualism-scanlon` → `harman-benign-creation` (HIGH): original override rationale was philosophically confused ("both outcome-based" — wrong for Scanlonian contractualism). Edge survives via premise-matcher's independent HIGH-weight classification.

**Dropped entirely (4):**

- `virtue-ethics-flourishing` → `neuroscience-positive-states` (was MEDIUM)
- `phenomenological-existentialism` → `performative-contradiction` (was MEDIUM)
- `performative-contradiction` → `epistemic-humility` (was MEDIUM)
- `buddhist-objection` → `indigenous-philosophy` (was LOW)

All 10 retained overrides are flagged `canonical_override: true` in data and carry the in-UI "not independently expert-validated" disclosure. Full per-edge audit reasoning in `map1_override_audit_v1.md`.

### Disengagement probability

Per-node badge (HIGH / MEDIUM / LOW) indicating how often the objection dead-ends:

**HIGH (7):** `performative-contradiction`, `consent-incoherent`, `bradley-no-subject`, `non-identity-problem`, `incommensurability`, `boonin-critique`, `cant-prove-nonexistence-better`

**LOW (8):** T1/T2 nodes driven by TMT or Optimism Bias (emotional investment keeps interlocutor engaged): `life-gift`, `just-depressed`, `most-people-happy`, `gods-plan`, `just-edgy`, `survivor-testimony`, `extinction-culture`, `pinker-better-world`

**MEDIUM (59):** all others

---

## ACTIVE TASKS (v3.6)

### TASK A: Manual validation of canonical overrides (Priority: Medium)
**Status: Audit-v1 completed 2026-04-16.** First-pass review dropped 4 edges (family-resemblance failure mode), demoted 1 edge from override status while preserving as ordinary premise-matched edge, retained 10. Audit document: `map1_override_audit_v1.md`.
**Remaining:** Domain-expert (trained ethicist) review of the 10 retained overrides. Two are borderline at MEDIUM (#5 `bradley-no-subject → incommensurability`; #9 `flow-states-csikszentmihalyi → hedonic-contrast`) and could reasonably demote to LOW. One (#1 `benatar-asymmetry-attack → boonin-critique` HIGH) could be strengthened by acknowledging parallel canonical responses (Bradley, Harman) in the rationale.

### TASK B: Disengagement heuristic refinement (Priority: Low)
Current HIGH/MEDIUM/LOW assignment is rule-based, not empirically calibrated. If debate-transcript data becomes available, refine assignments.

### TASK C: Spot-check non-trivial subset of blended edges (Priority: Medium)
Full validation of 869 blended edges is impractical. A structured 10% spot-check (~87 edges) distributed across tiers would surface systematic errors.

### TASK D: Offline HTML + JSON + JSX update to v3.6.1 (Priority: Medium)
All three distribution files are currently v3.4 and don't include v3.5 content edits, RSI system, Map 1, OR audit-v1 corrections. Full regen needed.

### TASK E: README update to v3.6.1 (Priority: Medium)
Add Map 1 section to README, note override audit, update screenshots, update live-link documentation. GitHub About box also still advertises v3.4.

### TASK F: Updated screenshots (Priority: Low)
Screenshots need v3.6.1 — Map 1 view, disengagement badges, convergence stars, disclosure notes.

---

## FUTURE DIRECTION

### Unified Home / Landing Page
Still deferred. Lower priority than refinement tasks above.

### Map 1 refinement passes
Once the tool has live use, transition predictions can be refined from actual debate data. Areas most likely to need correction:
- Sophisticate mode: cross-framework moves not covered by canonical overrides
- Drifter mode: register-matching within tier (category field is a proxy)
- Disengagement probability: coarse 3-bucket heuristic
- **Override additions (any future pass)** must satisfy the audit-v1 test: *can the source→target move be located in a specific paper, textbook, or recognized academic sequence?* Family-resemblance justifications ("both challenge X," "both resist Y") do not qualify.

---

## KEY PHILOSOPHICAL FRAMEWORKS (for reference)

Unchanged from v3.5. See v5 handout for full list. Core additions in Map 1 methodology:
- **Convergent Architecture** — tracked structurally in transition matrix; ★★★ edges reflect cross-mode convergence, which is a meta-version of convergent foundations.
- **Two-mechanism disclosure** — the insight that distinct generative forces (worldview-defense vs. emotional exhaustion) can produce identical rhetorical moves.

---

## AESTHETIC PARAMETERS

Unchanged from v3.5 plus:
- Map 1 edge colors: HIGH red (#c55), MEDIUM amber (#cc9900), LOW grey dashed (#666)
- Stars: gold (#cc9900)
- Two-mechanism/canonical disclosure bg: dark amber (#1a1408) with gold left-border

---

## USER CONTEXT

Unchanged. Author: Josiah S. Cooper (AnomicIndividual87).

---

## SESSION NOTES FOR AI

- v3.6.1 HTML is standalone, ~1.22 MB
- MAP1_TRANSITIONS is inserted after DEP_REVIEW_NOTES in script block
- Map 1 functions are prefixed `m1*` or `initMap1`/`toggleMap1Methodology`
- Map 1 uses radial layout (source at center, successors on arc), NOT force-directed like Maps 2/3
- Full structural audit passed pre-audit-v1: HTML balance, JS braces 4828/4828, parens 0/0, all four views present, all four switcher buttons wired, MAP1_TRANSITIONS parses with 74 sources, zero dangling edges, runtime 74×4 = 296 render calls all successful
- Post-audit-v1: MAP1_TRANSITIONS edge counts reduced by 4 (blended 873→869, sophisticate 351→347). Structural audit re-run on patched HTML confirmed clean.
- Recommended next steps: domain-expert review of 10 retained overrides (Task A residual), (C) blended edge spot-check, (D) offline file regeneration to v3.6.1, (E) README update to v3.6.1

---

## CHANGES LOG

- **v3.0 → v3.1:** +8 academic entries, zero-sum + suffering-deterrence addenda
- **v3.1 → v3.2:** +14 entries gap analysis, confidence system
- **v3.2 → v3.3:** +Map 2 (Mechanism Web)
- **v3.3 → v3.4:** +Map 3 (Dependency Graph)
- **v3.4 → v3.5:** Content review (14 edits), +RSI system, gladiator-war gloss, bug check
- **v3.5 → v3.6:** +Map 1 (Argument Flow Map). Three-mode architecture (Sophisticate/Defender/Drifter) with Blended default view. 873 blended-union edges generated from Maps 2+3+tier-gravity per v1.1 locked methodology. Convergence indicators (★★★/★★/★). Two-mechanism disclosure edges (44 total) for nuclear retreat and collapse. 15 canonical sophisticate overrides with in-UI disclosure. Per-node disengagement probability (7 HIGH / 59 MEDIUM / 8 LOW). Full Map 1 methodology panel. Runtime smoke test: 74 nodes × 4 modes = 296 render calls, zero failures. Structural audit clean.
- **v3.6 → v3.6.1:** Map 1 canonical-override audit v1. First-pass review of the 15 generation-time overrides identified a "family-resemblance failure mode" in the generator heuristic (pairing by commitment-similarity rather than documented argumentative trajectories). Four edges dropped entirely (`virtue-ethics-flourishing → neuroscience-positive-states`, `phenomenological-existentialism → performative-contradiction`, `performative-contradiction → epistemic-humility`, `buddhist-objection → indigenous-philosophy`). One edge demoted from override status but preserved as ordinary premise-matched edge (`contractualism-scanlon → harman-benign-creation` — premise-matcher independently produces it at HIGH). 10 overrides retained. Blended 873→869, sophisticate 351→347. Convergence distribution ~unchanged (87.7% single-mode preserved). Audit document: `map1_override_audit_v1.md`. Known Limitations section of `map1_generation_log.md` gained two entries (family-resemblance mode; retained-overrides-need-domain-expert-review).

---

*Upload `index.html` (v3.6.1) + this document at the start of a new chat to resume. Audit document `map1_override_audit_v1.md` and generation log `map1_generation_log.md` provide reasoning context if override-related work is resumed.*
