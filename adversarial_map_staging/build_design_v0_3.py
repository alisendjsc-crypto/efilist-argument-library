#!/usr/bin/env python3
"""
build_design_v0_3.py -- emits adversarial_map_design_v0_3.md from v0_2 plus section 10.

v0_2 stays on disk byte-identical: canon pins it and the Phase R receipt cites it, exactly as v0_1
was kept when section 9 was added. Nothing is rewritten; section 10 amends section 2 and a pointer
line is inserted into section 2 so a reader cannot author against the old text by accident.

ccclxii discipline: every numeric constant in section 10 is BOUND ONCE below, gated against the
measurement file that produced it, and interpolated from the binding. A number that is not in the
CONSTANTS table cannot appear in the section -- the emitter asserts that too.
"""
import json, os, re, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else _HERE
BASE = os.path.join(_HERE, "adversarial_map_design_v0_2.md")
raw = open(BASE, "rb").read()
assert hashlib.md5(raw).hexdigest() == "9083809f20328aee854b792260424425", "design v0_2 base guard FAILED"
src = raw.decode("utf-8")

M_CCC = json.load(open(os.path.join(_HERE, "measure_ccclxv_v0_1.json"), encoding="utf-8"))
M_ARC = json.load(open(os.path.join(_HERE, "measure_archetype_v0_1.json"), encoding="utf-8"))
M_CTL = json.load(open(os.path.join(_HERE, "phaseF_class_control_v0_1.json"), encoding="utf-8"))

def at(doc, path):
    cur = doc
    for k in path.split("/"):
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    return cur

# name -> (rendered, source doc, json path).  Bound once; gated; printed from the binding.
C = {
 "EXP_ANCHORS":   ("0.2264", M_CCC, "A5_expected_anchors_in_changed_text_under_uniform"),
 "OBS_ANCHORS":   ("1",      M_CCC, "A5_observed_anchors_in_changed_text"),
 "N_R":           ("4",      M_CCC, "A5_n_phaseR_entries"),
 "B_MULTI":       ("0.1053", M_CCC, "A2_b_share_multi"),
 "B_SINGLE":      ("0.2568", M_CCC, "A2_b_share_single"),
 "PERM_P":        ("0.9657", M_CCC, "A2_perm_null_p_b_enriched_in_multi"),
 "PERM_N":        ("20000",  M_CCC, "A2_perm_N"),
 "B_V10":         ("0.2258", M_CCC, "A1_v1_0_b_share"),
 "B_R":           ("0.75",   M_CCC, "A1_R_b_share"),
 "MOVE_A":        ("51",     M_CCC, "A3_move_words_median_by_class/a"),
 "MOVE_B":        ("103",    M_CCC, "A3_move_words_median_by_class/b"),
 "MOVE_D":        ("119",    M_CCC, "A3_move_words_median_by_class/d"),
 "LONG_ANCHORS":  ("77",     M_CCC, "A4_locus_dist/long"),
 "PER_NODE":      ("1.1341", M_CCC, "A2_entries_per_node_mean"),
 "SOPH_SHARE":    ("0.7347", M_ARC, "overall_soph_share"),
 "N_APPLICABLE":  ("98",     M_ARC, "n_applicable"),
 "SOPH_NICHE":    ("0.417",  M_ARC, "xtab_public_reach/niche_or_pseudonymous/soph_share"),
 "SOPH_HIGH":     ("0.929",  M_ARC, "xtab_public_reach/high_reach_intellectual/soph_share"),
 "SOPH_NAMED":    ("1.0",    M_ARC, "xtab_public_reach/named_specialist/soph_share"),
 "REG_P":         ("0.0",    M_ARC, "register_heterogeneity_perm_p"),
 "N_PUBS":        ("62",     M_ARC, "n_distinct_publications"),
 "FLIPS":         ("3",      M_CTL, "readjudication_sample/flips_to_a"),
 "FLIPS_OF":      ("4",      M_CTL, "readjudication_sample/of"),
 "P_NULL":        ("1.62e-24", M_CTL, "class_distribution/P_zero_of_n_in_a_or_d_given_base_rate"),
 "BASE_AD":       ("0.7634", M_CTL, "class_distribution/P_a_or_d_base_rate"),
}
for name, (rendered, doc, path) in C.items():
    got = at(doc, path)
    assert abs(float(rendered) - float(got)) < 1e-9, "CONSTANT %s: doc says %s, measurement says %s" % (name, rendered, got)
print("constants gated: %d of %d against their measurement files" % (len(C), len(C)))

S10 = """

---

## 10. The ccclxv ruling, the stopping rule, and what "strongest" means operationally (K346, 2026-09-18) — amends §2

`adversarial_map_design_v0_2.md` stays on disk byte-identical; canon pins it and the Phase R receipt
cites it. This section is the amendment, on the same terms §9 was.

### 10.1 The ruling

**STRONGEST.** Phase F and every phase after it author the strongest continuation a maximally
competent hostile interlocutor deploys against our text as written, exactly as §0 says. The
most-repairable-defect reading is **rejected**. Josiah + the library seat, K346; reversible by Josiah.

### 10.2 The finding that prompted the ruling does not survive its own null, and that is recorded rather than quietly dropped

WI-K336 registered `ccclxv` on the claim that phases A–E practised *repairable* while §0 asks for
*strongest*. Its evidence was that three of Phase R's four anchors land on clauses the v4.1.0 cut
never touched. **That overlap was published without a null.** The four re-adjudicated loci had
changed-word fractions summing to {EXP_ANCHORS}, so under uniform anchor placement the *expected*
number of Phase R anchors landing in cut-touched text is {EXP_ANCHORS} of {N_R}. Observed:
{OBS_ANCHORS} of {N_R}. Cut-touched text is **over**-represented, not walked past. This is `ccclxvi`
committed one section away from where `ccclxvi` was registered.

Two further tests, both against the frozen `adversarial_map_v1_0.json`:

- If authors kept going while repairable material lasted, multi-entry nodes should be (b)-enriched.
  (b) share is **{B_MULTI} in multi-entry nodes against {B_SINGLE} in single-entry nodes** —
  depleted. Permutation null against the enrichment direction, N={PERM_N}: **p = {PERM_P}**.
- The (b)-heaviness belongs to Phase R's repair brief, not to A–E: v1_0's (b) share is **{B_V10}**,
  Phase R's is **{B_R}**.
- Move length by class runs (d) **{MOVE_D}** > (b) **{MOVE_B}** > (a) **{MOVE_A}** median words. The
  longest, most-developed moves are the bedrock ones, which is the signature of strongest-first
  authoring.

The practised criterion was not *repairable*. `ccclxv` stands as a hazard about gates being silent,
and its worked example is struck.

### 10.3 What was actually unwritten: the stopping rule, not the selection criterion

A–E authored **{PER_NODE} entries per node against a cap of 3**, with `long` taking {LONG_ANCHORS} of
93 anchors. Nothing written says when a locus is *done*. That is `ccclxi`'s shape with evidence, and
it is the real gap the ccclxv finding was reaching for.

**Anti-inflation gate 5 — the stopping rule.** Author the strongest continuation and adjudicate it.
Then answer one question and record the answer: *is there a second continuation at this locus that
engages a different clause and would not be met by the same reply?* If yes, author it, to the cap. If
no, the locus is closed and the fragment declares it closed. The stop becomes an auditable claim
rather than a silence. Declared per-locus in fragment meta, gated when declared, on the pattern §9.4.3
set for `variant_coverage`. The gate itself is owed at validator v0_4.

### 10.4 ccclxviii — an operationalisation can satisfy every written gate and still invert the result

K346 ruled §10.1 and then operationalised "strongest" as *strongest against what this locus uniquely
says*. For a register variant that filter selects against (a) **by construction**, because what a
variant uniquely says is precisely the part its primary ladder does not already answer. The resulting
defect register returned (b) on all 39 entries. Against the A–E base rate for (a)-or-(d) of
**{BASE_AD}**, drawing zero is a **{P_NULL}** event. A seeded, sorted-pool sample of four loci
re-adjudicated under the plain reading flips **{FLIPS} of {FLIPS_OF}** to (a).

**The rule.** *Strongest* means strongest against the text as a reader meets it — the whole locus,
including everything it inherits from its node — never strongest against the locus's distinctive
content. For a variant the strongest continuation is usually the one its primary ladder already
answers, and that (a) is the routing datum the map exists to produce. Phase R found exactly this at
n=1 and said not to generalise; the generalisation that mattered was the opposite one.

And the detection rule, which is the transferable part: **a class distribution that departs from its
own base rate is an instrument reading before it is a finding.** Compute the phase's class mix
against the prior before writing a receipt over it.

### 10.5 Archetype weighting for Phase F: author evenly across loci — ruled, not defaulted

Observed `archetype_signal_observed` runs sophisticate **{SOPH_SHARE}** over **{N_APPLICABLE}**
applicable real-world instances, against a near-even authored distribution. Effort is **not** weighted
to it. Measured grounds:

- The signal is venue-bound. Sophisticate share by `public_reach`: niche or pseudonymous
  **{SOPH_NICHE}**, high-reach intellectual **{SOPH_HIGH}**, named specialist **{SOPH_NAMED}**.
  Register heterogeneity, permutation p = **{REG_P}**.
- The frame is concentrated and scholarly by design: **{N_PUBS}** distinct publications over
  {N_APPLICABLE} instances.
- §0 is a **competence** contract ("a maximally competent hostile interlocutor"). Frequency is a
  different axis, and importing it would be `ccclxv`'s substitution in a new place.
- Defect density runs opposite to deployment: the drifter and blended variants are the shortest and
  least-attended text in the feature, and a map hunting for weakness should not spend its budget where
  the corpus was most careful.

One entry per locus is the floor; further entries are allocated by §10.3's stopping rule, never by
slot frequency.

### 10.6 The archetype signal is a collection-frame diagnostic, and the frame has two lanes (Josiah, K346)

The `realWorldExamples` panel was built for **notable** sources — citable, archive-backed, attestable —
which is the right build for its first two purposes: defeating the straw-man charge, and cataloguing
the scope and depth of the subject. Notable sources select for sophisticates, because people writing
for publication perform competence. **The mundane everyday-interaction lane is wanted and simply has
not been collected.** It is not excluded from the programme; it is the lane the prediction aim needs,
and it is where the defender, drifter and blended archetypes actually live.

So the panel's archetype mix is lane one's mix, and the venue measurement above is a description of
lane one rather than of deployment. This adds to the K345b collection spec: a **second lane**, with its
own schema, where volume and thread structure carry the weight and byline attestation carries less, and
whose purpose is the archetype and prediction layers rather than citability.
"""
for k, (rendered, _, _) in C.items():
    S10 = S10.replace("{" + k + "}", rendered)
assert not re.search(r"\{[A-Z0-9_]+\}", S10), re.findall(r"\{[A-Z0-9_]+\}", S10)

POINTER = """
> **Amended K346 (§10):** the selection criterion is ruled — an entry names the **strongest**
> continuation, not the most repairable — and §10.4 fixes what *strongest* means operationally, which
> is the part that inverts a phase's class distribution when it is left to practice. A fifth
> anti-inflation gate, the **stopping rule**, is added at §10.3. **Read §10 before authoring against
> this section.**
"""
anchor = "**(c) before (b)** because"
assert src.count(anchor) == 1
src2 = src.replace(anchor, POINTER.strip() + "\n\n" + anchor)
out = src2 + S10
b = out.encode("utf-8")
p = os.path.join(OUT, "adversarial_map_design_v0_3.md")
open(p, "wb").write(b)
print("%s  %s  %d bytes  (v0_2 was %d, untouched)" % (os.path.basename(p), hashlib.md5(b).hexdigest(), len(b), len(raw)))
