#!/usr/bin/env python3
"""check_design_counts.py -- V0 (seat l, 2026-09-26): every count in VARIATIONS_design_v0_1.md, gated.

measure_variations.py re-derives the counts; this proves the design QUOTES them. Each claim below is a
phrase of the design with its numbers filled in from measure_variations_v0_1.json, never typed: the
phrase must occur in the design (whitespace-normalised). A number edited in the prose without the
measurement, or a measurement that moved under the prose, turns this RED.

  python3 design/variations/check_design_counts.py              # GREEN n/n, or RED with each miss
  python3 design/variations/check_design_counts.py --self-test  # the unmutated run first, then 3 mutations
Pure ASCII source.
"""
import copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.join(HERE, "VARIATIONS_design_v0_1.md")
RECORD = os.path.join(HERE, "measure_variations_v0_1.json")


def n(x):
    return "{:,}".format(x) if isinstance(x, int) and abs(x) >= 1000 else str(x)


def claims(J):
    c, rw, am, av, g = J["corpus"], J["realWorldExamples"], J["adversarial_map_v1_6"], J["archetypeVariants"], J["game"]
    est, sub, pil = J["cost"]["estimate"], J["objectionSubforms"], J["pilot"]
    lay, sch = J["surfaces"]["layman_trigger_words"], g["scholar_layer"]["words"]
    wings = J["wings"]["objections_by_wing"]
    pn = {x["id"]: x for x in pil["nodes"]}
    top = dict(J["map1"]["top10_in_degree"])
    fx = av["in_flux"]
    assert fx["slots_named_by_the_live_safety_pass_X032"] == [["red-button-repugnant", "sophisticate"]]
    assert fx["slots_on_stable_nodes"] + fx["slots_on_in_flux_nodes"] == av["slots"]
    v = J["validator_v0_6"]
    band = re.match(r"adversarial_move (\d+)-(\d+) words; class \(a\) additionally <=(\d+)", v["move_band"]).groups()
    assert v["entry_cap_locus"] == "<=3 entries per (target_id, target_locus)"
    assert re.match(r"<=3 \+ 3\*\(variant loci on that node\)", v["entry_cap_node"])
    assert sub["rwe_schema_calls_it_a_refutational_variant"] is True
    assert c["depths_on_every_node"] is True and g["code_reads"]["archetypeVariants"] == 0
    assert pil["eligible_with_2plus_attested_nonexact"] == ["meaning-through-suffering"]
    assert am["a_routing_targets_locus_only_no_anchor"] == am["a_routing_targets"]
    assert J["corpus"]["strong_premise_max_nodes"].count("joy-outweighs-harms") == 1 and len(J["corpus"]["strong_premise_max_nodes"]) >= 2
    L = [
        "In each register it shows one fixed line per objection (%s)" % J["surfaces"]["shown_per_register"],
        "%s trigger phrasings, %s real-world quote-objection pairs that fit exactly, %s archetype answers (embedded, read %s times), and %s wing objections"
        % (c["trigger_phrasings_total"], rw["short_quote_node_pairs_deploys_against_exact_fit"], av["slots"],
           g["code_reads"]["archetypeVariants"], J["wings"]["total"]),
        "Its %s (a) entries" % am["class_counts"]["a"],
        "(%s of their %s targets are another objection's card)" % (am["a_routing_targets_on_another_node"], am["a_routing_targets"]),
        "Its %s (d) entries end at named bedrock" % am["class_counts"]["d"],
        "today on anthropocentrism's %s edges" % J["retreat_lattice"]["anthropocentrism"]["retreat_edges"],
        "Pilot: %s nodes, about %s shapes, about %s words" % (J["plan_constants"]["pilot_nodes"], est["pilot_shapes"], n(est["pilot_words"])),
        "%s objections, 3 depths on every node" % c["objections"],
        "%s phrasings and %s keywords per node" % (c["trigger_phrasings"]["mean"], c["keywords_per_node"]["mean"]),
        "archetype variants on %s nodes, %s slots (sophisticate %s, defender %s, drifter %s, blended %s)"
        % (av["nodes"], av["slots"], av["by_slot"]["sophisticate"], av["by_slot"]["defender"], av["by_slot"]["drifter"], av["by_slot"]["blended"]),
        "one `objectionSubforms` node carrying %s units" % sub["units"],
        "%s real-world instances over %s nodes" % (rw["instances"], rw["nodes_attached"]),
        "%s Map 1 edges" % n(J["map1"]["edge_counts"]["total"]),
        "All %s of its definitions open" % sub["definitions_opening_Position-holder"],
        "Its %s anchors are refutation-of-deployment instances" % sub["corpus_anchor_polarity"]["refutation-of-deployment"],
        "the string occurs %s in `combined.html` and %s in the JSX"
        % ({1: "once"}[sub["occurrences_in_combined_html"]], {1: "once"}[sub["occurrences_in_jsx"]]),
        "%s attachments over %s nodes" % (rw["deploys_against_nonexact_attachments"], rw["deploys_against_nonexact_nodes"]),
        "%s of those sit on the %s nodes whose text is in flux"
        % (pil["rwe_concentration"]["nonexact_attachments_on_in_flux_nodes"], len(pil["in_flux"])),
        "Of the %s stable nodes, only `meaning-through-suffering` has two" % pil["eligible"],
        "All %s of the map's (a) routing targets" % am["a_routing_targets"],
        "R1 failed %s of its %s (a) entries" % (J["r1"]["verdicts"]["FAILS"], J["r1"]["entries_ruled"]),
        "The scholar layer (%s lines, %s words)" % (g["scholar_layer"]["nodes"], n(sch["total"])),
        "| %s phrasings; %s layman; %s scholar; %s exact-fit quote pairs | %s per register |"
        % (c["trigger_phrasings_total"], J["surfaces"]["shown_per_register"], g["scholar_layer"]["nodes"],
           rw["short_quote_node_pairs_deploys_against_exact_fit"], J["surfaces"]["shown_per_register"]),
        "`archetypeVariants`: %s nodes, %s |" % (av["nodes"], av["slots"]),
        "map v1_6: %s (a), %s (d) | anthropocentrism only (%s edges)"
        % (am["class_counts"]["a"], am["class_counts"]["d"], J["retreat_lattice"]["anthropocentrism"]["retreat_edges"]),
        "`objectionSubforms`: %s node, %s |" % (len(sub["nodes"]), sub["units"]),
        "map (c): %s, `%s`" % (am["class_counts"]["c"], am["c_entries"][0][1]),
        "the layman lines (%s-%s words) and the scholar lines (%s-%s)" % (lay["min"], lay["max"], sch["min"], sch["max"]),
        "entry caps (3 per locus; a node's cap is 3 + 3 x its variant loci)",
        "a word band (moves %s-%s; class (a) at most %s)" % band,
        "Drop the %s nodes that a pending pin-queue finding names" % len(pil["in_flux"]),
    ]
    for nid, label in (("life-gift", "top of T1"), ("joy-outweighs-harms", "top of T2 and of the game"),
                       ("future-solve", "top of T3"), ("free-will-defense", "top of T4"),
                       ("meta-ethical-pluralism", "top of T5"), ("meaning-through-suffering", "most attested")):
        x = pn[nid]
        L.append("| `%s` | %s | %s | %s | %s" % (nid, x["tier"], label, x["map1_in_degree"], len(x["attested_nonexact"])))
    L += [
        "%s strong premises to split shapes on" % pn["life-gift"]["strong_premises"],
        "%s strong premises, tied for the most" % pn["joy-outweighs-harms"]["strong_premises"],
        "carries a %s slot" % {("sophisticate",): "sophisticate"}[tuple(pn["future-solve"]["variant_slots"])],
        "About %s shapes per node, so about %s in all" % (J["plan_constants"]["shapes_per_node"], est["pilot_shapes"]),
        "The map's prior is %s of %s" % (am["a_routing_targets_on_another_node"], am["a_routing_targets"]),
        "against R1's %s of %s" % (J["r1"]["verdicts"]["FAILS"], J["r1"]["entries_ruled"]),
        "`masochist-counterexample` is the second-most-reached node (in-degree %s)" % top["masochist-counterexample"],
        "The %s trigger phrasings run %s to %s words (mean %s)"
        % (c["trigger_phrasings_total"], c["trigger_phrasing_words"]["min"], c["trigger_phrasing_words"]["max"],
           round(c["trigger_phrasing_words"]["mean"], 1)),
        "There are %s quote-and-node pairs, over %s nodes"
        % (rw["short_quote_node_pairs_deploys_against_exact_fit"], rw["short_quote_node_pairs_deploys_against_exact_fit_nodes"]),
        "Across all %s instances, %s quote is verbatim-verified and %s are speaker-attributed"
        % (rw["instances"], rw["short_quote_attestation_status"]["verbatim_verified"],
           rw["short_quote_attestation_status"]["speaker_attributed_unverified"]),
        "%s nodes, %s texts, already embedded" % (av["nodes"], av["slots"]),
        "%s wing objections: right-to-die %s, transgenderism %s, veganism %s, abortion %s, anthropocentrism %s"
        % (J["wings"]["total"], wings["right-to-die"], wings["transgenderism"], wings["veganism"], wings["abortion"],
           wings["anthropocentrism"]),
        "| ~%s |" % n(est["pilot_words"]),
        "| the full corpus: %s shapes | l, then gate2 | ~%s + ~%s | ~%s |"
        % (est["full_shapes"], est["full_drafting_sessions"], est["full_judging_sessions"], n(est["full_words"])),
        "the archetype variants run to %s words and the scholar layer to %s"
        % (n(J["cost"]["existing_layer_totals_words"]["archetypeVariants"]), n(J["cost"]["existing_layer_totals_words"]["scholar_layer"])),
        "corpus `%s`, JSX `%s`, `combined.html` `%s`, layman index `%s`" % tuple(J["pins"][k][:8] for k in ("corpus", "jsx", "combined", "layman")),
        "Map 1 `%s`, map v1_6 `%s`, validator v0_6 `%s`, R1 rulings `%s`" % tuple(J["pins"][k][:8] for k in ("map1", "advmap", "validator", "rulings")),
        "commit `%s`, `inject_data.py` `%s`, `index.html` `%s`, scholar v1.1" % tuple(J["pins_argue"][k][:8] for k in ("commit", "inject_data", "index")),
        "`%s`." % J["pins_argue"]["scholar"][:8],
        "(corpus `%s`)" % J["pins"]["corpus"][:8],
        "But %s of the %s nodes that carry them are in flux, and %s slots are named by pending repairs"
        % (fx["nodes"], av["nodes"], len(fx["slots_named_by_pending_findings"])),
        "Only %s of the %s nodes are stable (%s slots). The other %s carry %s slots."
        % (fx["stable_nodes"], av["nodes"], fx["slots_on_stable_nodes"], fx["nodes"], fx["slots_on_in_flux_nodes"]),
        "Pending repairs name %s slots: red-button-repugnant's sophisticate (X-032" % len(fx["slots_named_by_pending_findings"]),
        "show the %s stable nodes' slots first" % fx["stable_nodes"],
    ]
    return L


def norm(s):
    return re.sub(r"\s+", " ", s)


def check(J, doc):
    text = norm(doc)
    L = claims(J)
    miss = [x for x in L if norm(x) not in text]
    return len(L), miss


def main(argv):
    J = json.load(open(RECORD, encoding="utf-8"))
    doc = open(DESIGN, encoding="utf-8").read()
    if "--self-test" in argv:
        total, miss = check(J, doc)
        assert not miss, "unmutated control is RED: %s" % miss[:3]
        results = [("C0 unmutated", True)]
        J1 = copy.deepcopy(J); J1["corpus"]["trigger_phrasings_total"] += 1
        results.append(("C1 record: trigger_phrasings_total +1", bool(check(J1, doc)[1])))
        results.append(("C2 design: '1,620' -> '1,630'", bool(check(J, doc.replace("1,620", "1,630"))[1])))
        J3 = copy.deepcopy(J); J3["pilot"]["nodes"][1]["map1_in_degree"] = 108
        results.append(("C3 record: joy in-degree 109 -> 108", bool(check(J3, doc)[1])))
        for name, ok in results:
            print("%s  %s" % ("ok " if ok else "BAD", name))
        good = all(ok for _, ok in results)
        print("self-test %d/%d" % (sum(ok for _, ok in results), len(results)))
        return 0 if good else 1
    total, miss = check(J, doc)
    if miss:
        print("RED: %d of %d claims not found in the design:" % (len(miss), total))
        for x in miss:
            print("  - " + x)
        return 1
    print("GREEN: %d of %d claims in the design match measure_variations_v0_1.json" % (total, total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
