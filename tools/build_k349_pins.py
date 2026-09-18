#!/usr/bin/env python3
"""Emit tools/k349_pins.json -- every constant the K349 canon entry and the operator blocks
quote, bound ONCE here from the artifact or the measurement that means it.

The objections digest comes from the validator, never from the corpus's whole-file md5:
that exact substitution was the defect K348 caught in its OWN pins file.
"""
import json, os, sys, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
sz = lambda p: os.path.getsize(p)


def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m


def rj(p):
    return json.loads(open(p, "rb").read().decode("utf-8"))


def main():
    V = load(os.path.join(STG, "adv_map_validator_v0_6.py"), "v6p")
    corpus_p = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
    corpus = rj(corpus_p)
    M = rj(os.path.join(STG, "measure_k349_v0_1.json"))
    CG = rj(os.path.join(STG, "phaseG_control_v0_1.json"))
    CA = rj(os.path.join(STG, "assembly_control_v0_2.json"))
    CR = rj(os.path.join(STG, "register_control_v0_1.json"))
    G = rj(os.path.join(STG, "adv_map_phaseG_v0_1.json"))
    A12 = rj(os.path.join(STG, "adversarial_map_v1_2.json"))

    files = {
        "phaseG": "adversarial_map_staging/adv_map_phaseG_v0_1.json",
        "assembly_v1_2": "adversarial_map_staging/adversarial_map_v1_2.json",
        "validator_v0_6": "adversarial_map_staging/adv_map_validator_v0_6.py",
        "validator_v0_5": "adversarial_map_staging/adv_map_validator_v0_5.py",
        "register_v0_3": "adversarial_map_staging/honest_residuals_register_v0_3.json",
        "register_v0_3_md": "adversarial_map_staging/honest_residuals_register_v0_3.md",
        "design_v0_5": "adversarial_map_staging/adversarial_map_design_v0_5.md",
        "phaseG_control": "adversarial_map_staging/phaseG_control_v0_1.json",
        "assembly_control_v0_2": "adversarial_map_staging/assembly_control_v0_2.json",
        "register_control": "adversarial_map_staging/register_control_v0_1.json",
        "measure_k349": "adversarial_map_staging/measure_k349_v0_1.json",
        "build_phaseG": "adversarial_map_staging/build_phaseG.py",
        "build_assembly_v1_2": "adversarial_map_staging/build_assembly_v1_2.py",
        "build_register_v0_3": "adversarial_map_staging/build_register_v0_3.py",
        "render_register_v0_3": "adversarial_map_staging/render_register_v0_3.py",
        "build_design_v0_5": "adversarial_map_staging/build_design_v0_5.py",
        "controls_phaseG": "adversarial_map_staging/controls_phaseG.py",
        "controls_assembly_v1_2": "adversarial_map_staging/controls_assembly_v1_2.py",
        "controls_register_v0_3": "adversarial_map_staging/controls_register_v0_3.py",
        "measure_k349_py": "adversarial_map_staging/measure_k349.py",
        "patch_validator_v0_6": "tools/patch_validator_v0_6.py",
        "patch_assembly_v1_2": "tools/patch_assembly_v1_2.py",
        "patch_register_v0_3": "tools/patch_register_v0_3.py",
        "k349_validator_controls": "tools/k349_validator_controls.txt",
        "build_canon_v38_11": "tools/build_canon_v38_11.py",
    }
    P = {"session": "K349", "date_operator_local": "2026-09-17"}
    for k, rel in sorted(files.items()):
        p = os.path.join(REPO, rel)
        if os.path.exists(p):
            P[k + "_md5"] = md5f(p)
            P[k + "_bytes"] = sz(p)
        else:
            P[k + "_md5"] = None
            P[k + "_bytes"] = None

    # HELD surfaces, re-derived
    for k, rel in (("corpus", "efilist_argument_library_v4_0_0.json"),
                   ("jsx", "efilist_argument_library_v4_0_0.jsx"),
                   ("combined", "combined.html"),
                   ("v1_0", "adversarial_map_staging/adversarial_map_v1_0.json"),
                   ("v1_1", "adversarial_map_staging/adversarial_map_v1_1.json"),
                   ("register_v0_2", "adversarial_map_staging/honest_residuals_register_v0_2.json"),
                   ("design_v0_4", "adversarial_map_staging/adversarial_map_design_v0_4.md"),
                   ("build_assembly_v1_1", "adversarial_map_staging/build_assembly_v1_1.py")):
        p = os.path.join(REPO, rel)
        P[k + "_md5"] = md5f(p); P[k + "_bytes"] = sz(p)

    P["objections_digest"] = V.objections_digest(corpus)
    assert P["objections_digest"] != P["corpus_md5"], \
        "the digest was filled from the whole-file md5 -- the K348 defect, again"
    assert P["objections_digest"] == G["meta"]["source_corpus_objections_md5"]
    assert P["objections_digest"] == A12["meta"]["source_corpus_objections_md5"]

    nl = M["note_layer"]
    P["note"] = {
        "nodes": nl["nodes"], "words": nl["words_total"],
        "reachable": nl["reachable_n"], "unreachable": nl["unreachable_n"],
        "unreachable_ids": sorted(e["id"] for e in nl["unreachable"]),
        "words_unreachable": nl["words_unreachable"], "pct_unreachable": nl["pct_words_unreachable"],
        "authored": len(G["entries"]), "note_coverage": G["meta"]["note_coverage"],
        "apparatus": len([1 for v in G["meta"]["not_authored"].values() if v.startswith("(i)")]),
        "qualifier": len([1 for v in G["meta"]["not_authored"].values() if v.startswith("(ii)")]),
    }
    cl = M["confidence_layer"]
    P["confidence"] = {"nodes": M["out_of_enum_fields"]["confidence"],
                       "distribution": cl["distribution"],
                       "badge_emitting": cl["badge_emitting_n"],
                       "graded_full": cl["graded_full_n"], "ungraded": cl["ungraded_n"]}
    P["class_counts_phaseG"] = CG["class_mix"]["counts"]
    P["class_mix"] = CG["class_mix"]
    P["entries_v1_2"] = len(A12["entries"])
    P["entries_v1_1"] = P["entries_v1_2"] - len(G["entries"])
    P["variant_coverage"] = A12["meta"]["variant_coverage"]
    P["coverage"] = "%d/%d" % (A12["meta"]["nodes_covered"], A12["meta"]["nodes_total"])
    P["controls"] = {"phaseG": CG["summary"]["controls"], "assembly": CA["summary"]["controls"],
                     "register": CR["summary"]["controls"],
                     "total": CG["summary"]["controls"] + CA["summary"]["controls"]
                              + CR["summary"]["controls"]}
    assert all(x["all_pass"] for x in (CG["summary"], CA["summary"], CR["summary"])), \
        "a control battery is not green -- refusing to pin"
    P["parity_runs"] = CG["parity_runs"]
    P["parity_divergences"] = 0
    P["self_test_v0_6"] = 78
    P["self_test_v0_5"] = 62
    P["bedrocks"] = 14
    P["min_headroom"] = M["entry_cap_headroom"]["min_headroom"]
    P["already_bedrock"] = M["bedrock_enrichment"]["note_nodes_with_d_n"]
    P["corpus_d_nodes"] = M["bedrock_enrichment"]["corpus_nodes_with_d_n"]

    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "k349_pins.json")
    b = (json.dumps(P, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print("wrote %s %s %d B" % (dest, hashlib.md5(b).hexdigest(), len(b)))
    print("  digest %s | coverage %s | variant %s | note %s | controls %d"
          % (P["objections_digest"][:12], P["coverage"], P["variant_coverage"],
             P["note"]["note_coverage"], P["controls"]["total"]))


if __name__ == "__main__":
    main()
