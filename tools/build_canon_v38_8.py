#!/usr/bin/env python3
"""
build_canon_v38_8.py -- v38.7 -> v38.8, MINOR. Keyset UNCHANGED at 41.

ccclxiv: the round-trip of the SOURCE is asserted before anything is derived, so a serialization
mismatch cannot present as a 300 KB reformat with the content buried in it.
"""
import json, os, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_7.json")
raw = open(SRC, "rb").read()
assert hashlib.md5(raw).hexdigest() == "a27c5635b3b51d475061fac990c7122e", "canon v38.7 base guard FAILED"
d = json.loads(raw.decode("utf-8"))
SER = lambda o: (json.dumps(o, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
assert SER(d) == raw, "ccclxiv: v38.7 does not round-trip at the serialization about to be used"
print("ccclxiv round-trip of v38.7: PASS")

FROZEN = {k: json.dumps(d[k], sort_keys=True) for k in ("invariants", "schemas", "hazard_map")}
KEYS_BEFORE = list(d.keys())
am = d["adversarial_map"]

am["ccclxv_ruling_K346"] = {
 "ruling": "STRONGEST. An entry names the strongest continuation a maximally competent hostile interlocutor deploys against our text as written, per design section 0. The most-repairable-defect reading is REJECTED. Josiah + the library seat, K346 (2026-09-18); reversible by Josiah.",
 "the_finding_that_prompted_it_does_not_survive_its_null": "WI-K336 registered ccclxv on the claim that A-E practised repairable while section 0 asks for strongest, evidenced by three of Phase R's four anchors landing on clauses the v4.1.0 cut never touched. That overlap was published without a null. The four re-adjudicated loci have changed-word fractions summing to 0.2264, so the EXPECTED number of Phase R anchors in cut-touched text under uniform placement is 0.2264 of 4; observed is 1. Cut-touched text is OVER-represented. ccclxvi, committed one section from where ccclxvi was registered.",
 "direct_tests_against_the_frozen_map": "If authors continued while repairable material lasted, multi-entry nodes would be (b)-enriched. (b) share is 0.1053 in multi-entry nodes against 0.2568 in single-entry nodes -- depleted; permutation null against the enrichment direction, N=20000, p=0.9657. The (b)-heaviness belongs to Phase R's repair brief: v1_0's (b) share is 0.2258, Phase R's is 0.75. Move-length medians run (d) 119 > (b) 103 > (a) 51, which is strongest-first authoring, not repair-first.",
 "disposition": "ccclxv STANDS as a hazard about written gates being silent about which of two readings is meant. Its worked example -- that A-E practised repairable -- is STRUCK. Recorded as a correction, not restamped.",
 "evidence": {"file": "adversarial_map_staging/measure_ccclxv_v0_1.json", "md5": "8772c80cbc6908a2ebce7faaf502b844",
              "generator": "adversarial_map_staging/measure_ccclxv_v0_1.py", "reproducible_under_forced_hash_seeds": True}
}
am["stopping_rule_gate5_K346"] = {
 "gate": "Anti-inflation gate 5, design v0_3 section 10.3. Author the strongest continuation and adjudicate it; then answer one question and RECORD the answer -- is there a second continuation at this locus that engages a different clause and would not be met by the same reply? If yes, author it to the cap. If no, the locus is closed and the fragment declares it closed.",
 "why": "A-E authored 1.1341 entries per node against a cap of 3, with `long` taking 77 of 93 anchors, and nothing written says when a locus is done. That is ccclxi's shape with evidence, and it is the real gap the ccclxv finding was reaching for: the unwritten norm was a STOPPING rule, not a selection criterion.",
 "form": "Declared per-locus in fragment meta; reported every run, gated when declared, on the pattern section 9.4.3 set for variant_coverage. OWED: the gate itself lands at validator v0_4."
}
am["operationalisation_hazard_ccclxviii_K346"] = {
 "hazard": "ccclxviii -- AN OPERATIONALISATION OF A RATIFIED CRITERION CAN SATISFY EVERY WRITTEN GATE AND STILL INVERT THE RESULT.",
 "instance": "K346 ruled strongest-not-repairable and then operationalised `strongest` as strongest-against-what-this-locus-uniquely-says. For a register variant that filter selects against (a) BY CONSTRUCTION, because what a variant uniquely says is exactly the part its primary ladder does not already answer. The defect register returned (b) on all 39 entries. Against the A-E base rate for (a)-or-(d) of 0.7634, drawing zero across 38 loci is a 1.62e-24 event. A seeded sorted-pool sample of four loci re-adjudicated under the plain reading flips 3 of 4 to (a).",
 "rule": "`Strongest` means strongest against the text as a reader meets it -- the whole locus, including everything it inherits from its node -- never strongest against the locus's distinctive content. For a variant the strongest continuation is usually the one its primary ladder already answers, and that (a) is the routing datum the map exists to produce.",
 "detection_rule": "A class distribution that departs from its own base rate is an INSTRUMENT READING before it is a finding. Compute the phase's class mix against the prior before writing a receipt over it.",
 "lineage": "ccclxv's substitution one level out, committed by the session that ruled on ccclxv. Phase R found the (a) at n=1 and said not to generalise; the generalisation that mattered was the opposite one."
}
am["phaseF_defect_register_K346"] = {
 "file": "adversarial_map_staging/adv_map_phaseF_defect_register_v0_1.json",
 "md5": "5c9da93b0217013ac898449e20cbfe24", "bytes": 90881,
 "state": "DEFECT REGISTER, NOT AN ADJUDICATION. 39 verified internal defects across 38 of the 39 archetypeVariants loci. Validator v0_3: PASS, 0 violations, 0 advisories.",
 "no_coverage_claim": "variant_coverage is DELIBERATELY NOT DECLARED. 38 of 39 loci carry an entry, but declaring coverage would assert adjudication the artifact has not performed, which is 82/82 in a new file.",
 "control": {"file": "adversarial_map_staging/phaseF_class_control_v0_1.json", "md5": "146e11956686b657d59a863522964c4f",
             "generator": "adversarial_map_staging/controls_phaseF.py", "mutation_controls": "11 of 11 behaved"},
 "findings_independent_of_class": [
  "ORIGIN-DEBUNKING SPLIT: life-gift#long, indigenous-philosophy#long, love-beauty-art#long and nihilism-label#long each rule that inferring a belief's falsity from its evolutionary or psychological cause is a genetic fallacy; red-button#archetypeVariants.sophisticate, why-not-suicide#long and bitter-childhood#archetypeVariants.defender deploy that inference as a load-bearing move. No locus adjudicates between them.",
  "The just-depressed depressive-realism contradiction logged at K345 REACHES A SECOND NODE: most-people-happy#archetypeVariants.sophisticate leans on depressive realism as its defeater, which just-depressed#archetypeVariants.sophisticate says a sophisticate reaching for it would be cherry-picking. The K345 record scopes the contradiction to just-depressed's own loci and so understates its extent.",
  "REGISTER RETRACTION, 6 instances: drifter-register slots open with a reassurance that a higher-register locus in the same corpus withdraws. An artifact of the archetype FEATURE rather than of any node -- the register split creates a surface on which the corpus tells two readers different things, and nothing checks across registers.",
  "BLENDED TRIAGE UNDER-ENUMERATION, 6 of the 7 blended slots ship an exhaustive-sounding two-branch routing rule that omits at least one strand their own node names.",
  "CIRCULAR ROUTE: slippery-slope-eugenics#archetypeVariants.sophisticate routes its conceded coercion-floor residue to violence-as-reductio, whose sophisticate slot disclaims anchor-specific entailment and routes it back by name. Neither node adjudicates it.",
  "ACT/OMISSION: the corpus carries the creation-versus-intervention cut as a dissolution of the wild-animal dilemma and never defends it as the contested asymmetry it is."],
 "phase_F_proper_still_OWED": "The class-law adjudication of the 39 variant loci re-opens from the plain reading in section 10.4. The register is an input to it, not a substitute for it."
}
am["design_pin_v0_3"] = {
 "file": "adversarial_map_staging/adversarial_map_design_v0_3.md", "md5": "eed4b2af42b1ad2235cf6a6a22974ea9", "bytes": 21170,
 "adds": "Section 10, amending section 2: the ccclxv ruling, anti-inflation gate 5 (the stopping rule), ccclxviii, the archetype-weighting ruling, and the two-lane RWE note. A pointer is inserted into section 2 so a reader cannot author against the old text by accident.",
 "v0_2_and_v0_1_kept_byte_identical": "9083809f20328aee854b792260424425 and 49514ec9d631c3fbdf2cbf227923dd1b -- canon pins them and the Phase A-R receipts cite them.",
 "gate": "Every numeric constant in section 10 is bound once in build_design_v0_3.py, asserted against the measurement file that produced it, and interpolated from the binding: 25 of 25 matched. A number absent from the table cannot appear in the section."
}
am["archetype_weighting_ruling_K346"] = {
 "ruling": "AUTHOR EVENLY ACROSS LOCI. One entry per locus is the floor; further entries are allocated by the stopping rule, never by slot frequency. Josiah, K346. Ruled after measurement rather than taken as a default.",
 "why_observed_deployment_is_the_wrong_weight": "The 0.7347 sophisticate share over 98 applicable instances is VENUE-BOUND, not a property of deployment. Sophisticate share by public_reach: niche_or_pseudonymous 0.417, high_reach_intellectual 0.929, named_specialist 1.0; register heterogeneity permutation p = 0.0. The frame is concentrated and scholarly by design, 62 distinct publications over 98 instances.",
 "two_further_grounds": "Design section 0 is a COMPETENCE contract (a maximally competent hostile interlocutor); frequency is a different axis and importing it would be ccclxv's substitution in a new place. And defect density runs OPPOSITE to deployment -- the drifter and blended variants are the shortest, least-attended text in the feature, so a map hunting for weakness should not spend its budget where the corpus was most careful.",
 "evidence": {"file": "adversarial_map_staging/measure_archetype_v0_1.json", "md5": "307222a62f4e4749bd9fc461131a6172",
              "generator": "adversarial_map_staging/measure_archetype_v0_1.py",
              "control": "The script reproduces canon's stored 72/15/6/5 over 98 applicable instances exactly before any cross-tab is computed."}
}
am["rwe_two_lane_collection_K346"] = {
 "correction_by_Josiah_K346": "The realWorldExamples panel was built for NOTABLE sources -- citable, archive-backed, attestable -- which is the right build for its first two purposes: defeating the straw-man charge, and cataloguing the scope and depth of the subject. Notable sources select for sophisticates, because people writing for publication perform competence. Sweeping social platforms was never an exclusion from the PROGRAMME: the mundane everyday-interaction data is WANTED, and it is exactly what the argument-flow prediction system needs.",
 "consequence": "The panel's archetype mix is LANE ONE's mix. The venue measurement at measure_archetype_v0_1.json describes the collection frame, not deployment in the world, and the defender, drifter and blended archetypes live in the lane that has not been collected.",
 "adds_to_the_K345b_collection_spec": "A SECOND LANE with its own schema, whose purpose is the archetype and prediction layers rather than citability: volume and thread structure carry the weight, byline attestation carries less. The K345b constraint stands unchanged for lane one -- threaded, sequentially numbered, single-attachment instances are what the prediction aim needs -- and lane two is where they can be obtained at volume.",
 "not_a_finding_about_skill": "K345b's verdict is untouched: the clean single-attachment test is n=17, p=0.37, no defensible signal. This entry is a collection instruction."
}

d["next_recommended_session"] = {
 "action": "PHASE F PROPER -- the class-law adjudication of the 39 archetypeVariants loci, re-opened from the plain reading of `strongest` fixed at design v0_3 section 10.4. adv_map_phaseF_defect_register_v0_1.json is an INPUT (39 verified defects with repairs stated), not a substitute: its class column is not a class-law verdict and it makes no coverage claim.",
 "first_move": "For each locus ask the plain question -- what is the strongest continuation against this text as a reader meets it, including everything the locus inherits from its node -- and run a -> c -> b/d on THAT. Expect (a) to be common: the control at phaseF_class_control_v0_1.json flips 3 of 4 sampled loci to (a), and an (a) at a variant locus is the routing datum the map exists to produce.",
 "gates": [
  "Compute the phase's class mix against the A-E base rate BEFORE writing any receipt over it (ccclxviii). A distribution far from the prior is an instrument reading.",
  "Declare the per-locus stopping rule (gate 5, design v0_3 section 10.3); validator v0_4 is owed to gate it.",
  "adversarial_map_v1_0.json stays byte-identical at c4989e98b042e2f787a82df3f11ecdad and is not re-pinned.",
  "The terminal successor assembly is NOT built until Phase F proper lands.",
  "`note` (9 nodes, 544 words, rendered) is still IN SCOPE and unadjudicated."],
 "then": "The terminal successor assembly: Phase R + the 78 inherited entries + Phase F, pinned to 04bf6482, declaring BOTH coverage and variant_coverage. Then the sixteen v4.1.0 enrichment items, happiness-is-choice#medium, and the just-depressed depressive-realism contradiction -- whose extent K346 found wider than logged.",
 "not_this_session": "diagnosis-not-refutation, the single (c), and the v5.0.0 intake cut. Unchanged since v38.3: it belongs to a session that begins fresh. gods-plan and western-philosophy stay HELD for it.",
 "also_read_first": "adversarial_map.operationalisation_hazard_ccclxviii_K346 before authoring a single entry, and adversarial_map.phaseF_defect_register_K346.findings_independent_of_class -- four corpus-level patterns that a per-locus map cannot see and that survive the class error entirely."
}
d["canon_version"] = "38.8"
d["canon_version_marker"] = "v38.8"
d["last_updated"] = "2026-09-18"
d["last_updated_by_session"] = "K346_phaseF_defect_register_and_ccclxv_ruling"
d["keyset_delta_ledger"]["v38_8_note"] = (
 "v38.7 -> v38.8 MINOR (K346_phaseF_defect_register_and_ccclxv_ruling, 2026-09-18): keyset UNCHANGED at 41. "
 "Seven additions INSIDE adversarial_map (ccclxv_ruling_K346, stopping_rule_gate5_K346, "
 "operationalisation_hazard_ccclxviii_K346, phaseF_defect_register_K346, design_pin_v0_3, "
 "archetype_weighting_ruling_K346, rwe_two_lane_collection_K346) and a replacement of next_recommended_session. "
 "invariants, schemas and hazard_map asserted byte-identical by the builder, and the SOURCE was round-tripped at "
 "the emitted serialization before anything was derived (ccclxiv). NO PIN; no corpus, JSX, flagship or frozen-map byte moved.")

assert list(d.keys()) == KEYS_BEFORE, "top-level keyset moved"
assert len(KEYS_BEFORE) == 41, len(KEYS_BEFORE)
for k, v in FROZEN.items():
    assert json.dumps(d[k], sort_keys=True) == v, "%s is not byte-identical" % k
b = SER(d)
p = os.path.join(OUT, "project_canon_v38_8.json")
open(p, "wb").write(b)
print("keyset held at %d; invariants/schemas/hazard_map byte-identical" % len(KEYS_BEFORE))
print("%s  %s  %d bytes" % (os.path.basename(p), hashlib.md5(b).hexdigest(), len(b)))
