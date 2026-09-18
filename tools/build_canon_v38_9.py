#!/usr/bin/env python3
"""build_canon_v38_9.py -- derive project_canon_v38_9.json from v38_8 (MINOR).

ccclxiv: the SOURCE is round-tripped at the emitted serialization BEFORE anything is derived,
so a 300 KB reformat cannot hide a content change.
Asserts: top-level keyset unchanged at 41; invariants, schemas and hazard_map byte-identical.
Repo-relative; --out <dir>.
"""
import json, os, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K347_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_8.json")
DEST = os.path.join(OUT, "project_canon_v38_9.json")
DATE = "2026-09-17"          # OPERATOR-LOCAL (America/Phoenix). The sandbox clock reads UTC.
SESSION = "K347_phase_F_proper_and_validator_v0_4"

raw = open(SRC, "rb").read()
c = json.loads(raw.decode("utf-8"))
SER = dict(indent=2, ensure_ascii=False)
assert (json.dumps(c, **SER) + "\n").encode("utf-8") == raw, \
    "ccclxiv: source does not round-trip at the emitted serialization -- do not derive"
print("ccclxiv round-trip: v38_8 reproduces byte-for-byte at indent=2/ensure_ascii=False + NL")

FROZEN = {k: json.dumps(c[k], sort_keys=True, ensure_ascii=False) for k in ("invariants", "schemas", "hazard_map")}
KEYS_BEFORE = sorted(c.keys())

# --- pins measured THIS session, bound once and printed from the binding (ccclxii) -------------
PINS = json.loads(open(os.path.join(_HERE, "k347_pins.json"), "rb").read().decode("utf-8"))
am = c["adversarial_map"]

BEDROCK = ("create-vs-destroy: whether an independently-motivated suffering-minimization layer "
           "grounds a positive case against existing beings")

am["phaseF_proper_K347"] = {
  "artifact": "adversarial_map_staging/adv_map_phaseF_v0_1.json",
  "md5": PINS["phaseF_md5"], "bytes": PINS["phaseF_bytes"],
  "landed": "K347 (%s, wuld.ink Cowork); NO PIN" % DATE,
  "scope": ("38 of the 39 archetypeVariants loci over 16 nodes, 39 entries. Phase R holds the 39th, "
            "just-depressed#archetypeVariants.defender. Validator v0_4 PASS, 22 checks, 0 violations, "
            "0 advisories; the whole variant surface reports variant_coverage 39/39 when Phase F and "
            "Phase R are validated together, which is the successor-map fragment set."),
  "reading_applied": ("ccclxviii, the plain reading: strongest against the text AS A READER MEETS IT, the "
                      "whole locus including everything it inherits from its node. The K346 register was "
                      "used as an INPUT and each of its entries was read only AFTER an independent "
                      "continuation had been formed at that locus, so its frame could not be inherited."),
  "class_counts": PINS["class_counts"],
  "class_mix_gate": {
    "base_phases_A_to_E_a_or_d": "71/93 = 0.7634",
    "observed_a_or_d": "%d/%d = %s" % (PINS["a_or_d"], PINS["entries"], PINS["a_or_d_share"]),
    "exact_two_sided_binomial_p": PINS["binomial_p"],
    "verdict": ("CONSISTENT with its own base rate, so the receipt is not written over an instrument "
                "reading. Stated in both directions on purpose: knowing K346 drew zero (a) is not a "
                "licence to rubber-stamp (a), and a lazy (a) is worse than a lazy (b) because it asserts "
                "the corpus answers something it may not and terminates a locus with no regen candidate "
                "and no residue. For contrast, the K346 register's 0-of-39 has p = 3.83e-25 at this prior."),
    "within_total_split": ("(a) rises to 0.667 from a base of 0.419 and (d) falls to 0.179 from 0.344. That "
                           "is what design section 10.4 predicts for loci that re-present an argument their "
                           "primary ladder already answers: the (a) is the routing datum the map exists to "
                           "produce. Zero (c), continuing the whole-program pattern."),
  },
  "evidence_discipline": ("All 26 (a) entries name an answering locus AND carry a verbatim snippet from it, "
                         "asserted against the corpus programmatically rather than quoted: 26 of 26 in "
                         "phaseF_proper_control_v0_1.json. Four (a) entries route to a VARIANT locus, "
                         "exercising the K345 answered_by grammar for the first time."),
  "findings": {
    "new_bedrock_is_an_artifact_of_the_routing_graph": (
      "why-not-suicide, ai-fear, antinatalism-misanthropic and wild-animal-suffering-consistency all route "
      "the positive-eliminationist charge to red-button-repugnant, and benatar-asymmetry-attack routes "
      "create-vs-destroy to nodes that route it there. red-button-repugnant's sophisticate slot holds it "
      "open BY RULING. So the charge is answered in no locus: it is relocated until it reaches the one node "
      "whose disposition is to leave it standing, and the routing manufactures the appearance of an answer "
      "no locus supplies. Registered as HR-14 below. A per-locus map can only see this by reading the graph, "
      "which is why four phases did not."),
    "inheritance_cuts_both_ways": (
      "Design section 10.4 states one direction, that the whole-node reading cures a locus-local defect, and "
      "it does: next-person-cure-cancer#archetypeVariants.sophisticate aims a deprivation argument past its "
      "target and #long frames the same refusal on consent, so the move is met and the entry is (a). It also "
      "AGGRAVATES. just-depressed#archetypeVariants.sophisticate disavows depressive realism while #short and "
      "#medium assert it as evidence, so what the locus inherits makes a correct text false-in-context; "
      "violence-as-reductio#archetypeVariants.drifter asserts an incompatibility between caring about "
      "suffering and causing harm that its own #long surrenders. Two of the six (b) entries exist only "
      "because of what the locus inherits. OWED: design section 11 should state both directions."),
    "entailment_standard_is_the_clusters_shared_exposure": (
      "ai-fear, violence-as-reductio, slippery-slope-eugenics and why-not-suicide all answer a recklessness "
      "or facilitation charge by demanding premise-to-action entailment, and none argues that entailment is "
      "the right test for such a charge. Registered ONCE, as a headline regen candidate at "
      "ai-fear#archetypeVariants.defender, rather than four times; the other three loci are met on the terms "
      "their own moves take."),
    "drifter_and_blended_were_not_the_soft_targets_predicted": (
      "Design section 10.5 declined to weight effort to observed deployment partly on the ground that drifter "
      "and blended are the shortest, least-attended text. Authored evenly, they returned 3 of the 6 (b) "
      "entries from 14 of 38 loci against 13 sophisticate loci returning 1. A count rather than a finding, "
      "and it runs opposite to the stated expectation; the even-authoring ruling is what surfaced it."),
  },
  "forward_constraint_for_the_assembly": (
    "red-button-repugnant carries 3 entries in the frozen v1_0 and 3 in Phase F, against a node bound of "
    "3 + 2 variant loci = 5. Any successor assembly inheriting v1_0's three primary entries verbatim stands "
    "at 6 and trips entry-cap-node. Flagged now rather than discovered at assembly: the bound is a K345 "
    "amendment Josiah delegated, so either it is revisited or one of the six is dropped on the merits."),
  "fences": ("NO PIN. Zero corpus / jsx / combined / canon-invariant / adversarial_map_v1_0 bytes. "
             "Cross-surface gate GREEN at %s at open and at close. The frozen v1_0 stays pinned to the "
             "pre-cut corpus and is neither re-run nor re-pinned." % PINS["xsurface"]),
}

am["validator_pin_v0_4"] = {
  "file": "adversarial_map_staging/adv_map_validator_v0_4.py",
  "md5": PINS["v0_4_md5"], "bytes": PINS["v0_4_bytes"],
  "self_test": "60/60 (v0_3's 50 inherited, plus 10 written for the two checks v0_4 adds)",
  "derived_by": "tools/patch_validator_v0_4.py -- anchored single-occurrence replacement, base-guarded on v0_3",
  "v0_3_retained": ("adv_map_validator_v0_3.py stays BYTE-IDENTICAL at %s: the Phase F defect register's "
                    "receipt names it, and canon pins it at validator_pin_v0_3." % PINS["v0_3_md5"]),
  "checks_added": {
    "stopping-rule": ("Anti-inflation gate 5, design v0_3 section 10.3, made checkable. A fragment may declare "
                      "locus_closure, a per-locus record of the stopping decision, gated when declared on the "
                      "section 9.4.3 pattern. The declared key set must equal the loci THAT FILE carries "
                      "entries for, both ways; values are closed|open; and open <-> >=2 entries is a "
                      "BICONDITIONAL, because the declaration records the answer to 'is there a second "
                      "continuation here'. Two entries at one locus may not sit on the same clause, which is "
                      "the minimal mechanisation of 'engages a different clause': neither anchor may be a "
                      "substring of the other. Measured across all nine pre-existing artifacts, that "
                      "sub-check finds 0 same-clause pairs over 13 multi-entry loci, so it is confirmatory "
                      "rather than a repair, and it is scoped inside the declaration so no frozen receipt "
                      "can be disturbed by it."),
    "variant-coverage (amended)": ("ccclxx. A per-file declaration is now gated against THAT FILE's own "
                                   "variant loci, as class_counts and coverage_distinct_ids already were. "
                                   "The all-loaded-files figure is still reported."),
  },
  "parity": ("v0_4 reproduces every v0_3 verdict on all nine pre-existing artifacts against both the pre-cut "
             "and the post-cut corpus, --assembly included, with one intended exception: Phase R loaded "
             "TOGETHER with the K346 register, which v0_3 fails and v0_4 passes. That exception is the "
             "ccclxx defect, live on shipped bytes."),
  "scope_note": ("The session prompt asked for ONE check. The second was taken deliberately: shipping a "
                 "variant_coverage declaration known to break under a legitimate invocation would be cccli, "
                 "the failure the one-check instruction exists to prevent."),
}

am["ccclxx_hazard_K347"] = {
  "hazard": ("ccclxx -- A PER-FILE DECLARATION GATED AGAINST A GLOBALLY-COMPUTED VALUE IS "
             "INVOCATION-DEPENDENT: the same bytes pass or fail by how many sibling files the run loads."),
  "instance": ("variant_coverage is declared in a fragment's own meta but was compared against the hit-count "
               "summed over every loaded file. Phase F truthfully declares 38/39 and passes alone; loaded "
               "beside Phase R the computed figure is 39/39 and both files fail. This is not hypothetical: "
               "Phase R and the K346 defect register, both already shipped, fail together under v0_3 today, "
               "and nothing had ever run them together."),
  "why_it_survived": ("The sibling summaries class_counts and coverage_distinct_ids were already computed "
                      "per file. variant_coverage was the only declared summary gated against a global "
                      "figure, so the inconsistency was invisible to any single-fragment run, and every "
                      "fold from A to E was a single-fragment run."),
  "rule": ("Gate a declared summary against the scope of the thing that declares it. If a figure is a "
           "set-level claim, it belongs in a set-level artifact, not in a member's meta."),
  "lineage": ("ccclxix's family: the check was sound and its model of its own instrument was not. Found by "
              "trying to DECLARE the value at scale rather than by reading the code."),
  "control": ("phaseF_proper_control_v0_1.json carries it both ways -- v0_4 passes solo and joint, v0_3 "
              "passes solo and fails joint. A fix with no failing control on the old code is cosmetic."),
}

am["next"] = (
  "THE SUCCESSOR MAP'S TERMINAL ASSEMBLY, now unblocked: Phase F has landed, so the successor map's "
  "fragment set is Phase R (4 entries) + Phase F (39 entries) plus whatever of the frozen v1_0's 93 entries "
  "are inherited. Its FIRST arithmetic is the red-button-repugnant node bound recorded at "
  "phaseF_proper_K347.forward_constraint_for_the_assembly: 3 inherited + 3 new against a bound of 5. Before "
  "the assembly, two cheaper items that the assembly will otherwise carry: design section 11, stating that "
  "inheritance cuts BOTH ways and fixing gate 5's biconditional in the design as well as the code; and "
  "honest_residuals_register v0_2, which must add Phase F and Phase R to FRAGS and PHASE_ORDER, add HR-14 to "
  "BEDROCK_MAP with its three facets, declare any adjacency the audit detects, and rule on the register "
  "spanning two corpus cuts (A-C pin the pre-cut corpus, F and R the post-cut one). Then the sixteen v4.1.0 "
  "enrichment items plus happiness-is-choice#medium, and only then the v5.0.0 intake cut.")

tsm = c["terminal_stability_marker"]["honest_residuals"]
tsm["create_vs_destroy_positive_case"] = {
  "register_id": "HR-14",
  "alias": "K347 bedrock",
  "claim": ("Whether an independently-motivated suffering-minimization layer grounds a positive case against "
            "existing beings. The corpus answers the ENTAILMENT question -- the antinatalist core does not "
            "entail the negative-utilitarian superstructure, demonstrated at violence-as-reductio and "
            "why-not-suicide -- and leaves the MOTIVATION question open by ruling."),
  "why_it_is_bedrock": ("Four nodes route the charge to red-button-repugnant, whose sophisticate slot states "
                        "that holding it open rather than pretending it closed is that node's terminus. No "
                        "locus in the corpus closes it, so the routing graph is load-bearing for an answer "
                        "that does not exist anywhere."),
  "birth_certificate": {"phase": "F", "node": "red-button-repugnant",
                        "locus": "archetypeVariants.sophisticate", "session": "K347"},
  "facets": {
    "positive-case-for-cessation": "why-not-suicide#archetypeVariants.sophisticate (self-application route)",
    "successor-preference": "ai-fear#archetypeVariants.sophisticate (a non-suffering successor preferred over the incumbent)",
    "coercion-floor": ("slippery-slope-eugenics#archetypeVariants.sophisticate -- and this facet is additionally "
                       "stranded by the slippery-slope-eugenics / violence-as-reductio MUTUAL route, the circular "
                       "route logged at K346: each names the other as owner."),
  },
  "owed": ("honest_residuals_register_v0_1.json is NOT yet rebuilt to carry HR-14; the register's whole purpose "
           "is that a phase author decides novel: true|false by lookup rather than from memory, so v0_2 is owed "
           "before the next authoring phase. Recorded here so the pointer is checkable in the meantime."),
}

am_next_top = {
  "action": ("THE SUCCESSOR MAP TERMINAL ASSEMBLY, or the two cheaper items ahead of it (design section 11; "
             "honest_residuals_register v0_2). Phase F proper has landed and the archetypeVariants surface is "
             "adjudicated 39/39 across Phase R + Phase F."),
  "first_move": ("Do NOT begin by assembling. Read phaseF_proper_K347.forward_constraint_for_the_assembly and "
                 "settle the red-button-repugnant node bound first: 3 inherited entries from the frozen v1_0 "
                 "plus 3 from Phase F against a bound of 3 + 2 variant loci = 5. The bound is a K345 amendment "
                 "Josiah delegated, so it is revisited or one of the six is dropped on the merits. An assembly "
                 "that discovers this at its own gate will have already spent the session."),
  "then": ("Validate the fragment set with adv_map_validator_v0_4.py, whose stopping-rule and per-file "
           "variant-coverage checks are new; run the cross-surface gate before and after; and remember that "
           "coverage: 82/82 is a claim about a (map, corpus) PAIR, so the successor map pins the POST-cut "
           "corpus and the frozen v1_0 keeps the pre-cut one."),
  "fences": "NO PIN unless the session's declared subject is a pin move. The frozen v1_0's bytes do not move.",
}
c["next_recommended_session"] = am_next_top

c["session_log_recent"].append(
  "%s (%s, wuld.ink Cowork; NO PIN) [MINOR v38.8->v38.9]: PHASE F PROPER, and the archetypeVariants surface "
  "is adjudicated. 38 loci over 16 nodes, 39 entries, validator v0_4 PASS 22 checks 0 violations 0 advisories; "
  "with Phase R the set reports variant_coverage 39/39. Class mix a26/b6/d7, a+d = %s against the A-E base rate "
  "of 0.7634, exact two-sided binomial p = %s -- CONSISTENT, so the receipt is not written over an instrument "
  "reading, and the gate was stated in both directions because knowing K346 drew zero (a) is not a licence to "
  "rubber-stamp (a). All 26 (a) entries carry a verbatim snippet from their answering locus, asserted against "
  "the corpus. NEW BEDROCK HR-14, and it is an artifact of the ROUTING GRAPH rather than of any one text: four "
  "nodes route the positive-eliminationist charge to red-button-repugnant, whose sophisticate slot holds it "
  "open by ruling, so the charge is answered in no locus. SECOND FINDING: inheritance cuts BOTH ways -- design "
  "10.4 says the whole-node reading cures a locus-local defect, and it does, but it also AGGRAVATES, and two "
  "of the six (b) entries exist only because of what the locus inherits. VALIDATOR v0_4: gate 5 made checkable "
  "with open <-> >=2 entries as a biconditional, and ccclxx, a per-file declaration gated against a global "
  "figure -- Phase R and the K346 register, both shipped, fail together under v0_3 today. 23/23 controls; "
  "everything reproduces byte-identically under two forced PYTHONHASHSEEDs."
  % (SESSION, DATE, PINS["a_or_d_share"], PINS["binomial_p"]))

c["keyset_delta_ledger"]["v38_9_note"] = (
  "v38.8 -> v38.9 MINOR (%s, %s): keyset UNCHANGED at 41. Four additions INSIDE adversarial_map "
  "(phaseF_proper_K347, validator_pin_v0_4, ccclxx_hazard_K347) plus a replacement of adversarial_map.next; "
  "one addition inside terminal_stability_marker.honest_residuals (create_vs_destroy_positive_case = HR-14, "
  "the first new bedrock since HR-13); a replacement of next_recommended_session; one session_log_recent "
  "append. invariants, schemas and hazard_map asserted byte-identical, which is what would have forced MAJOR."
  % (SESSION, DATE))

c["canon_version"] = "38.9"
c["canon_version_marker"] = "v38.9"
c["last_updated"] = DATE
c["last_updated_by_session"] = SESSION

# --- gates ------------------------------------------------------------------------------------
assert sorted(c.keys()) == KEYS_BEFORE, "top-level keyset moved: %r" % (
    set(c.keys()) ^ set(KEYS_BEFORE),)
assert len(c.keys()) == 41, "keyset is %d, expected 41" % len(c.keys())
for k, v in FROZEN.items():
    assert json.dumps(c[k], sort_keys=True, ensure_ascii=False) == v, \
        "%s MOVED -- this would be a MAJOR bump, not MINOR" % k
print("keyset 41 unchanged; invariants / schemas / hazard_map byte-identical -> MINOR")

out = (json.dumps(c, **SER) + "\n").encode("utf-8")
os.makedirs(OUT, exist_ok=True)
open(DEST, "wb").write(out)
print("wrote %s  md5 %s  bytes %d" % (DEST, hashlib.md5(out).hexdigest(), len(out)))
