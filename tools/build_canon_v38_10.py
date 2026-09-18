#!/usr/bin/env python3
"""build_canon_v38_10.py -- derive project_canon_v38_10.json from v38_9 (MINOR).

ccclxiv: the SOURCE is round-tripped at the emitted serialization BEFORE anything is derived,
so a 350 KB reformat cannot hide a content change.
Asserts: top-level keyset unchanged at 41; invariants, schemas and hazard_map byte-identical.
Repo-relative; --out <dir>.
"""
import json, os, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_9.json")
DEST = os.path.join(OUT, "project_canon_v38_10.json")
DATE = "2026-09-17"          # OPERATOR-LOCAL (America/Phoenix). The sandbox clock reads UTC.
SESSION = "K348_terminal_successor_assembly_v1_1"

raw = open(SRC, "rb").read()
c = json.loads(raw.decode("utf-8"))
SER = dict(indent=2, ensure_ascii=False)
assert (json.dumps(c, **SER) + "\n").encode("utf-8") == raw, \
    "ccclxiv: source does not round-trip at the emitted serialization -- do not derive"
print("ccclxiv round-trip: v38_9 reproduces byte-for-byte at indent=2/ensure_ascii=False + NL")

FROZEN = {k: json.dumps(c[k], sort_keys=True, ensure_ascii=False)
          for k in ("invariants", "schemas", "hazard_map")}
KEYS_BEFORE = sorted(c.keys())

P = json.loads(open(os.path.join(_HERE, "k348_pins.json"), "rb").read().decode("utf-8"))
am = c["adversarial_map"]
RBR = P["rbr"]

am["entry_cap_ruling_K348"] = {
  "ruling": ("The node-level entry bound becomes 3 + 3*(variant loci on that node) -- the per-locus "
             "cap applied to variants exactly as it already applies to primaries. Josiah, K348 "
             "(%s). A node carrying NO variants keeps the Q1-ratified bound of 3 EXACTLY, which is "
             "the property the K345 amendment was written to preserve and this one preserves "
             "untouched." % DATE),
  "why_the_K345_form_had_to_move": (
    "The K345 bound, 3 + 1*(variant loci), was set when NO variant entry existed anywhere. It "
    "reserved a single slot per variant locus while the per-locus cap allows three, so the node "
    "bound and anti-inflation gate 5 disagree BY CONSTRUCTION wherever a variant locus legitimately "
    "opens: gate 5 says author the second continuation, and the node bound refuses to hold it. That "
    "is a contradiction between two ratified gates, not a budget question."),
  "where_it_surfaced": (
    "red-button-repugnant carries %d entries in the successor assembly -- 3 inherited from the "
    "frozen v1_0 and 3 from Phase F, %d of them at the one variant locus Phase F declared open -- "
    "against a K345 bound of %d. Every entry is legal per-locus and the node is illegal per-node."
    % (RBR["entries"], RBR["variant_loci"], RBR["bound_k345"])),
  "the_alternative_declined": (
    "Dropping one of the six on the merits, in the assembly only, was the other option put to "
    "Josiah, with the weakest of the six named: red-button-repugnant#archetypeVariants.sophisticate, "
    "the selective-debunking (a), whose answering locus already holds an (a) anchored on the same "
    "firmware passage. DECLINED. Dropping a sound entry to satisfy an arithmetic fixed before the "
    "thing it now constrains existed repairs the symptom, and the amendment is what stops the "
    "disagreement recurring at every future variant-bearing node."),
  "blast_radius_measured": (
    "Across the assembly's %d entries over %d nodes: %d node violates the K345 bound and %d violate "
    "the K348 bound. The heaviest node carries %d entries against a new bound of %d, and the "
    "heaviest locus carries 3 against a cap of 3, so the amendment buys headroom exactly where gate "
    "5 needs it and nowhere else. Measured in adversarial_map_staging/measure_k348_v0_1.json."
    % (P["entries"], P["nodes_total"], 1, 0, RBR["entries"], RBR["bound_k348"])),
  "implemented_at": "adv_map_validator_v0_5.py, check entry-cap-node. Design v0_4 section 11.3.",
  "delegation": ("Josiah delegated the FORM of the entry-cap amendment at K345 and ruled this form "
                 "at K348, presented with the measurement above and the alternative beside it."),
}

am["terminal_assembly_K348"] = {
  "artifact": "adversarial_map_staging/adversarial_map_v1_1.json",
  "md5": P["assembly_v1_1_md5"], "bytes": P["assembly_v1_1_bytes"],
  "landed": "K348 (%s, wuld.ink Cowork); NO PIN" % DATE,
  "state": ("MAPPED-COMPLETE, PRE-TRIAGE per ratification Q3. Every entry carries status 'mapped'; "
            "the lifecycle mapped -> queued -> ratified -> landed | rejected lives HERE, in canon, "
            "never in the artifact."),
  "coverage": ("%d/%d nodes at the primary ladder AND variant_coverage %s -- the first artifact in "
               "the programme to declare both, and per ccclxx a declared summary is gated against "
               "the scope of the file that declares it, which for a single-file assembly is the "
               "whole set." % (P["nodes"], P["nodes_total"], P["variant_coverage"])),
  "entries": P["entries"], "class_counts": P["class_counts"],
  "composition": ("%d entries inherited from the frozen v1_0 unchanged, %d superseded by Phase R "
                  "because the v4.1.0 cut destroyed their anchors (happiness-is-choice#long, "
                  "just-edgy#long, just-depressed#long), 4 from Phase R and 39 from Phase F."
                  % (P["inherited"], P["superseded"])),
  "why_v1_1_and_not_v2_0": (
    "79 of 82 nodes inherit their adjudication byte-for-byte, three re-adjudicate, the schema is "
    "unchanged and no inherited entry is re-classed. That is a revision of the same map over a "
    "re-cut corpus, not a re-mapping. The surface widens to 39 archetypeVariants loci the v1_0 "
    "claim was structurally unable to cover, and covered surface is an addition rather than a "
    "break. A v2_0 would mean the adjudications were re-done. update_protocol's MINOR/MAJOR rule "
    "governs CANON, not this artifact; the artifact states its own grounds in its meta."),
  "corpus_pin": ("POST-cut: %s, objections digest %s. The digest is taken from the validator's own "
                 "objections_digest rather than recomputed in the builder -- the K344 hazard, which "
                 "fired again on K347's first Phase F build." % (P["corpus_md5"], P["objections_digest"])),
  "anchors": ("All %d anchors asserted verbatim against the POST-cut corpus before the builder will "
              "write. This is the check the frozen v1_0 fails three ways against these bytes, and "
              "it is asserted rather than assumed." % P["entries"]),
  "validation": ("adv_map_validator_v0_5.py --assembly against the post-cut corpus: 23 checks, 0 "
                 "violations, 0 ADVISORIES. --assembly promotes every advisory to hard, so the "
                 "thirteen advisories v1_0 had to discharge are re-checked here against different "
                 "bytes rather than assumed to have stayed discharged."),
  "class_mix_gate": {
    "base_phases_A_to_E_a_or_d": "71/93 = %s" % P["base_rate"],
    "union": "105/133 = %s, exact two-sided p = %s" % (P["union_share"], P["union_p"]),
    "disjoint_R_and_F": "34/43 = %s, exact two-sided p = %s" % (P["new_share"], P["new_p"]),
    "which_one_counts": ("The DISJOINT figure. The union CONTAINS the base, so testing the union "
                         "against a rate computed from its own subset is not an independent test. "
                         "Both are reported and the artifact says which carries weight; ccclxviii "
                         "applies to a union as much as to a phase, and half of applying it is "
                         "knowing which number is the test."),
  },
  "controls": ("assembly_control_v0_1.json, %s / %d bytes: %d controls, all passing. The battery "
               "includes the predecessor's fate BOTH ways (v1_0 passes against its own pinned "
               "corpus and fails against the post-cut one on exactly anchor-rule x3 + "
               "meta-corpus-pin + objections-digest), nine mutations each naming the check it must "
               "trip, and a control that REMOVES an entry and proves coverage FAILS -- coverage is "
               "the claim this artifact exists to make and a coverage gate that cannot fail is "
               "decoration."
               % (P["assembly_control_md5"], P["assembly_control_bytes"], P["controls"])),
  "predecessor": ("adversarial_map_v1_0.json %s is NOT edited, NOT re-pinned and NOT re-run. It "
                  "stays byte-identical and stays pinned to the pre-cut corpus, recoverable at "
                  "git show 3e71546316285ef4fe3bd6d2da4ef1b5e4d6b50f:efilist_argument_library_v4_0_0.json. "
                  "Its own builder, build_assembly.py, also stays byte-identical, and this session "
                  "RE-DERIVED v1_0 from it against that corpus and got the same %d bytes before "
                  "writing a successor (ccclxiv, applied to an artifact rather than to a "
                  "serialization)." % (P["v1_0_md5"], 186406)),
  "fences": ("NO PIN. Zero corpus / jsx / combined / canon-invariant bytes. Cross-surface gate "
             "GREEN at %s at open and at close." % P["xsurface"]),
}

am["ccclxxi_hazard_K348"] = {
  "hazard": ("ccclxxi -- WHEN A RULING MOVES A GATE'S UNIT, EVERY OTHER INVARIANT STATED OVER THE "
             "OLD UNIT IS A CANDIDATE FOR THE SAME MOVE, AND NONE OF THEM FAILS UNTIL A FRAGMENT "
             "SET FINALLY CROSSES IT."),
  "instance": ("K345 moved the entry cap's unit from the NODE to the (node, locus). It did not move "
               "build_assembly.py's PARTITION invariant, which refuses to write if any node is "
               "claimed by two phases. Phase F authors variant loci on nodes A-E already cover, so "
               "at the successor assembly's fragment set that invariant fails %d ways BY "
               "CONSTRUCTION -- while the property it was protecting, that no two phases adjudicate "
               "the same text, is perfectly intact: %d loci are claimed by two phases."
               % (P["node_clashes"], P["locus_clashes"])),
  "why_it_survived": ("Every fold from A to E was a set in which the two formulations agree, "
                      "because A-E partition the 82 nodes between them. The formulations can only "
                      "disagree once a phase authors at a locus of a node another phase already "
                      "holds, which is what Phase F is. Three sessions passed between the ruling "
                      "that made the two forms different and the artifact that could tell them "
                      "apart."),
  "rule": ("On any ruling that changes a gate's unit, enumerate the other invariants stated over "
           "the old unit and rule each one explicitly -- migrate, keep, or record why it stays. "
           "Silence is what carries the old unit forward."),
  "lineage": ("ccclxx's family -- a check whose model of its own subject is stale -- but the stale "
              "model here is of the UNIT rather than of the instrument, and the trigger is a data "
              "set rather than an invocation."),
  "recorded_in": "design v0_4 section 11.4, and the assembly's own meta.partition_invariant.",
}

am["validator_pin_v0_5"] = {
  "file": "adversarial_map_staging/adv_map_validator_v0_5.py",
  "md5": P["validator_v0_5_md5"], "bytes": P["validator_v0_5_bytes"],
  "self_test": "%d/%d (v0_4's 60 inherited, less the one control that asserted the superseded "
               "arithmetic, plus three written for the new bound)"
               % (P["self_test_v0_5"], P["self_test_v0_5"]),
  "derived_by": "tools/patch_validator_v0_5.py -- anchored single-occurrence replacement, "
                "base-guarded on v0_4. Four patches.",
  "v0_4_retained": ("adv_map_validator_v0_4.py stays BYTE-IDENTICAL at %s: canon pins it at "
                    "validator_pin_v0_4 and the Phase F receipt names it."
                    % "d7a049ee1161d3bc5de0d3fbff96bbf9"),
  "the_only_behavioural_change": ("entry-cap-node, per entry_cap_ruling_K348. Nothing else moves."),
  "controls": ("The K345 control that tripped at six is REPLACED rather than kept beside its "
               "successor: it asserted the superseded arithmetic and could only pass by being "
               "wrong. Its replacements: a 2-variant node clean at 9 and tripping at 10, and a "
               "control proving the per-LOCUS cap still binds inside the widened node bound -- four "
               "entries at one locus trip entry-cap while the node total is far under its bound."),
  "parity": ("v0_5 reproduces every v0_4 verdict across %d runs -- ten shipped artifacts plus two "
             "joint invocations, against BOTH the pre-cut and the post-cut corpus, in plain, "
             "--terminal and --assembly modes -- with %d divergences. The amended bound changes no "
             "verdict on anything already shipped; it changes the verdict on the assembly, which is "
             "the artifact it was ruled for." % (P["parity_runs"], P["parity_diffs"])),
}

am["design_pin_v0_4"] = {
  "file": "adversarial_map_staging/adversarial_map_design_v0_4.md",
  "md5": P["design_v0_4_md5"], "bytes": P["design_v0_4_bytes"],
  "adds": ("Section 11, amending sections 9 and 10. 11.1 inheritance cuts THREE ways, not one or "
           "two -- cure, aggravate, and fail-to-cure -- with the count measured across Phase F at "
           "20 cured against 2 aggravated. 11.2 gate 5 is a BICONDITIONAL in the design as well as "
           "in the code. 11.3 the K348 entry-cap ruling. 11.4 ccclxxi, the partition invariant's "
           "unit. 11.5 what the successor assembly is. A pointer is inserted into section 9 and "
           "into section 10 so a reader cannot author against superseded text by accident."),
  "v0_3_and_earlier_kept_byte_identical": ("eed4b2af42b1ad2235cf6a6a22974ea9, "
                                           "9083809f20328aee854b792260424425 and "
                                           "49514ec9d631c3fbdf2cbf227923dd1b -- canon pins them."),
  "gate": ("Every numeric constant in section 11 is bound once in build_design_v0_4.py and asserted "
           "against measure_k348_v0_1.json: 36 of 36 matched. AND the emitter then extracts every "
           "numeric token from the finished section and refuses to write if one is neither a bound "
           "constant nor an explicitly allowed literal -- 45 tokens, all accounted for. v0_3's "
           "docstring claimed that second half; its code asserted only that no placeholder "
           "survived. One mis-sourced binding was caught by writing the check: the gate-5 threshold "
           "'2' had been interpolated from the measured count of aggravated entries, which happens "
           "to be 2. It printed the right digit and asserted nothing. A rule constant has no "
           "measurement behind it and is now an allowed literal with the reason beside it."),
}

am["honest_residuals_register_pin_v0_2"] = {
  "file": "adversarial_map_staging/honest_residuals_register_v0_2.json",
  "md5": P["register_v0_2_md5"], "bytes": P["register_v0_2_bytes"],
  "companion": "honest_residuals_register_v0_2.md %s" % P["register_v0_2_md_md5"],
  "landed": "K348 (%s); NO PIN" % DATE,
  "basis": ("DERIVED FROM THE ASSEMBLY, not from fragments: all 39 (d) entries of "
            "adversarial_map_v1_1.json, consolidated into 14 bedrocks over 25 distinct shipped "
            "bedrock names. Phase R contributes no residue and the file says so rather than "
            "omitting it."),
  "corpus_span_ruled": (
    "ONE corpus is pinned, the post-cut one, and the single pin is EARNED rather than asserted. The "
    "tributaries span two cuts by AUTHORSHIP -- A through E against the pre-cut corpus, R and F "
    "against the post-cut one -- and a register is a namespace consolidation rather than a "
    "corpus-pinned adjudication, so carrying two pins would misdescribe it. What makes the single "
    "pin honest is the source: the assembly asserts every one of its anchors verbatim against the "
    "post-cut corpus before it will write, so every tributary here is authored against whichever "
    "cut its phase met and VERIFIED against the one named."),
  "HR_14_added": ("With the three facets recorded at terminal_stability_marker.honest_residuals."
                  "create_vs_destroy_positive_case plus the terminus that holds the question open. "
                  "All four tributaries carry the SAME shipped bedrock_name, so BEDROCK_MAP -- keyed "
                  "on that string alone -- cannot separate the facets; FACET_BY_NODE does it, keyed "
                  "on (bedrock_id, node), and refuses to write if a tributary moves node."),
  "HR_05_pointer_now_resolves": (
    "v0_1's audit records HR-05 as registered at 'K224:carry-forward-bar', a session receipt rather "
    "than canon, and fires a dangling-registration-pointer finding on it. K345 folded HR-05 into "
    "terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm, so the pointer "
    "HAS a canon home and the finding is STALE. registered_in is repointed and the finding is "
    "dropped as a CORRECTION. HR-05's NOVEL-FLAG COLLISION is untouched and stands: it is a real "
    "defect."),
  "adjacency": ("Two new pairs fire on the shared-tributary-node signal, HR-14+HR-02 at "
                "red-button-repugnant and HR-14+HR-03 at slippery-slope-eugenics, and both are "
                "adjudicated independent_of with grounds. A third, HR-14+HR-11, fires on neither "
                "signal and is recorded in the AUDIT rather than declared, because the ratified "
                "four-kind vocabulary cannot state it: HR-11's resolution neither creates nor "
                "dissolves HR-14's question, it changes HR-14's FORCE. A fifth kind -- conditions -- "
                "would say it, and extending a ratified vocabulary is Josiah's, not a build call."),
  "parity_gate": ("Restricted to the phases v0_1 read, every bedrock's name, alias, gloss, "
                  "registered_in, relations and facet tributaries must equal v0_1's or the build "
                  "refuses. The one deliberate exception is HR-05.registered_in. Tributaries inside "
                  "a facet are compared as a sorted multiset because their ORDER moved from "
                  "fragment-internal to corpus order when the source became the corpus-ordered "
                  "assembly; that re-sequencing is recorded, not hidden."),
}

am["honest_residuals_register_pin"]["SUPERSEDED_K348"] = (
  "Superseded by honest_residuals_register_pin_v0_2. AND THIS RECORD WAS STALE IN THREE PLACES, "
  "found by rebuilding the artifact rather than by reading anything. (1) The md5 above, %s, is the "
  "K334 build; the file on disk is %s, rebuilt afterwards when D and E were folded in, and nothing "
  "re-derived the pin. (2) 'basis: phases A, B1, B2, C, E only -- the Phase D draft is deliberately "
  "excluded' is false of the shipped bytes: they reproduce only under --with-d --with-e. (3) The "
  "shipped file pins the PRE-cut corpus 6ee1f6f31e0f012db0d58cae4f912fcb -- it reproduces today in "
  "every byte EXCEPT that field, which is the whole of the difference. v0_1's bytes are left "
  "untouched; the corrections live here. ccclxii's family one level out: there a receipt was a "
  "claim about a run that nothing checked, here a pin is a claim about an ARTIFACT that nothing "
  "re-derived, and it went stale by the artifact moving rather than by the claim being copied."
  % (P["register_v0_1_canon_pin_stale"], P["register_v0_1_md5_on_disk"]))

am["terminal_artifact_pin"]["successor_K348"] = (
  "SUPERSEDED BY adversarial_map_v1_1.json (terminal_assembly_K348), which pins the post-cut "
  "corpus, inherits %d of these 93 entries unchanged, takes Phase R's re-adjudication of the three "
  "whose anchors the cut destroyed, and adds Phase F's 39. THIS RECORD AND THIS ARTIFACT DO NOT "
  "MOVE. v1_0 was re-derived from its own untouched builder against the pre-cut corpus this session "
  "and came back byte-identical, which is what licensed writing a successor." % P["inherited"])

hr = c["terminal_stability_marker"]["honest_residuals"]
hr["create_vs_destroy_positive_case"]["owed"] = (
  "DISCHARGED at K348. honest_residuals_register_v0_2.json carries HR-14 with its three facets plus "
  "the terminus that holds the question open, derived from the successor assembly. See "
  "adversarial_map.honest_residuals_register_pin_v0_2.")
hr["register_pointer"] = (
  "This block records the TERMINAL residuals. The working consolidation of everything the "
  "Adversarial Map has surfaced lives at adversarial_map_staging/honest_residuals_register_v0_2.json "
  "(14 bedrocks, HR-01..HR-14) and is library-internal. HR-01 and HR-02 above are its two pre-map "
  "entries; HR-03, HR-05 and HR-14 are landed here; the rest stay in the register. v0_1 is "
  "superseded and its canon record was stale in three places -- see "
  "adversarial_map.honest_residuals_register_pin.SUPERSEDED_K348.")

am["next"] = (
  "THE TERMINAL SUCCESSOR ASSEMBLY IS LANDED, so the map's next move is a CHOICE rather than a debt. "
  "The cheapest real item is `note`: 9 nodes, 544 words, RENDERED behind a toggle at "
  "responseLevel==='long', IN SCOPE since K345 and still unadjudicated. It is the last unadjudicated "
  "rendered text class and the natural PHASE G, and it needs a ruling first, because its shape is not "
  "a response and the anchor rule assumes one -- at least one instance (care-ethics) is a published "
  "concession that the node's own response is underpowered, which is an attack surface of an unusual "
  "kind. After that, or instead of it: the sixteen v4.1.0 enrichment items plus "
  "happiness-is-choice#medium and the depressive-realism contradiction, which K347 adjudicated at "
  "just-depressed#archetypeVariants.sophisticate as a headline (b) and did NOT repair -- and which "
  "design v0_4 section 11.1 now classes as an AGGRAVATION, meaning the repair belongs at the node "
  "rather than at the locus. Then the v5.0.0 intake cut and its single (c). NOT owed: a register "
  "rebuild (v0_2 landed), a design section (v0_4 landed), or any re-run of the frozen v1_0.")

c["next_recommended_session"] = {
  "title": "PHASE G (`note`) -- ruling first, or the v4.1.0 enrichment items",
  "why": ("The successor assembly is the terminal artifact the programme was building toward and it "
          "is landed at 82/82 primary and 39/39 variant. Nothing structural is owed. `note` is the "
          "only rendered text class the map has never covered, and it is blocked on a RULING rather "
          "than on a build: the anchor rule assumes a response and a note is not one."),
  "read_first": ("adversarial_map_design_v0_4.md sections 9, 10 and 11 -- 11.1's three-way "
                 "inheritance rule changes how a variant or a note is classed, and 11.3's bound is "
                 "the arithmetic any further authoring runs against. Then "
                 "loci_enum_ruling_K345.note_IN_SCOPE_unadjudicated, which states the shape problem."),
  "fences": "NO PIN unless the session's declared subject is a pin move. The frozen v1_0's bytes do "
            "not move, and neither do v0_2/v0_3/v0_4 of the design or v0_1..v0_4 of the validator.",
}

c["session_log_recent"].append(
  "%s (%s, wuld.ink Cowork; NO PIN) [MINOR v38.9->v38.10]: THE TERMINAL SUCCESSOR ASSEMBLY. "
  "adversarial_map_v1_1.json, %d entries over %d/%d nodes at the primary ladder AND variant_coverage "
  "%s -- the first artifact in the programme to declare both -- classes a%d/b%d/c%d/d%d, pinned to "
  "the post-cut corpus, validator v0_5 --assembly 23 checks 0 violations 0 ADVISORIES, %d controls "
  "all passing. %d entries inherit from the frozen v1_0 unchanged and 3 are superseded by Phase R; "
  "all %d anchors are asserted verbatim against the post-cut corpus rather than assumed. RULING "
  "(Josiah): the node entry bound becomes 3 + 3*(variant loci), because the K345 form reserved one "
  "slot per variant locus while the per-locus cap allows three, so the bound and gate 5 contradicted "
  "each other wherever a variant locus legitimately opened. ccclxxi: when a ruling moves a gate's "
  "unit, every other invariant over the old unit is a candidate for the same move and none of them "
  "fails until a fragment set crosses it -- v1_0's node-level PARTITION invariant fails %d ways by "
  "construction at this fragment set while the property it protects is intact at %d locus-level "
  "clashes. Register v0_2 derived from the assembly, which settles the two-corpus span by earning a "
  "single pin. Design v0_4 section 11. AND CANON'S OWN RECORD OF THE v0_1 REGISTER WAS STALE IN "
  "THREE PLACES, found by rebuilding the artifact: wrong md5, wrong basis, and a pre-cut corpus pin."
  % (SESSION, DATE, P["entries"], P["nodes"], P["nodes_total"], P["variant_coverage"],
     P["class_counts"]["a"], P["class_counts"]["b"], P["class_counts"]["c"], P["class_counts"]["d"],
     P["controls"], P["inherited"], P["entries"], P["node_clashes"], P["locus_clashes"]))

c["keyset_delta_ledger"]["v38_10_note"] = (
  "v38.9 -> v38.10 MINOR (%s, %s): keyset UNCHANGED at 41. Six additions INSIDE adversarial_map "
  "(entry_cap_ruling_K348, terminal_assembly_K348, ccclxxi_hazard_K348, validator_pin_v0_5, "
  "design_pin_v0_4, honest_residuals_register_pin_v0_2), a replacement of adversarial_map.next, and "
  "two CORRECTIONS to existing records: honest_residuals_register_pin gains SUPERSEDED_K348 naming "
  "three stale facts in itself, and terminal_artifact_pin gains successor_K348. Inside "
  "terminal_stability_marker.honest_residuals: create_vs_destroy_positive_case.owed discharged and "
  "register_pointer rewritten for 14 bedrocks. A replacement of next_recommended_session; one "
  "session_log_recent append. invariants, schemas and hazard_map asserted byte-identical, which is "
  "what would have forced MAJOR." % (SESSION, DATE))

c["canon_version"] = "38.10"
c["canon_version_marker"] = "v38.10"
c["last_updated"] = DATE
c["last_updated_by_session"] = SESSION

assert sorted(c.keys()) == KEYS_BEFORE, "top-level keyset moved: %r" % (set(c.keys()) ^ set(KEYS_BEFORE),)
assert len(c.keys()) == 41, "keyset is %d, expected 41" % len(c.keys())
for k, v in FROZEN.items():
    assert json.dumps(c[k], sort_keys=True, ensure_ascii=False) == v, \
        "%s MOVED -- this would be a MAJOR bump, not MINOR" % k
print("keyset 41 unchanged; invariants / schemas / hazard_map byte-identical -> MINOR")

out = (json.dumps(c, **SER) + "\n").encode("utf-8")
os.makedirs(OUT, exist_ok=True)
open(DEST, "wb").write(out)
print("wrote %s  md5 %s  bytes %d" % (DEST, hashlib.md5(out).hexdigest(), len(out)))
