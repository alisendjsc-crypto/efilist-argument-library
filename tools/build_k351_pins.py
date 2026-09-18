#!/usr/bin/env python3
"""Emit tools/k351_pins.json -- every constant the K351 canon entry, the stratum and the
operator blocks quote, bound ONCE here from the artifact or the measurement that means it.

ccclxii, mechanised: a receipt is a claim about a run, and an unbound constant is a claim
nothing checks. Every hex string a block or a document quotes this session is read out of
this file or gated against it.

The objections digest comes from the VALIDATOR, never from the corpus's whole-file md5 --
that exact substitution was the defect K348 caught in its own pins file.
"""
import json, os, sys, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "tools", "k351_pins.json")
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
sz = os.path.getsize
rj = lambda p: json.loads(open(p, "rb").read().decode("utf-8"))

# (key stem, path relative to the repo). Everything this session writes or holds.
NEW = [
    ("phaseG", "adversarial_map_staging/adv_map_phaseG_v0_1.json"),
    ("assembly_v1_3", "adversarial_map_staging/adversarial_map_v1_3.json"),
    ("build_assembly_v1_3", "adversarial_map_staging/build_assembly_v1_3.py"),
    ("register_v0_4", "adversarial_map_staging/honest_residuals_register_v0_4.json"),
    ("register_v0_4_md", "adversarial_map_staging/honest_residuals_register_v0_4.md"),
    ("build_register_v0_4", "adversarial_map_staging/build_register_v0_4.py"),
    ("render_register_v0_4", "adversarial_map_staging/render_register_v0_4.py"),
    ("controls_assembly_v1_3", "adversarial_map_staging/controls_assembly_v1_3.py"),
    ("assembly_control_v0_3", "adversarial_map_staging/assembly_control_v0_3.json"),
    ("controls_register_v0_4", "adversarial_map_staging/controls_register_v0_4.py"),
    ("register_control_v0_2", "adversarial_map_staging/register_control_v0_2.json"),
    ("amend_phaseG", "tools/amend_phaseG_K351.py"),
    ("patch_assembly_v1_3", "tools/patch_assembly_v1_3.py"),
    ("patch_register_v0_4", "tools/patch_register_v0_4.py"),
    ("build_canon_v38_13", "tools/build_canon_v38_13.py"),
    ("verify_k351", "tools/verify_k351.py"),
    ("k351_verification", "tools/k351_verification.json"),
    # This file pins its OWN BUILDER so that every constant an operator block quotes is
    # traceable to a measurement. It cannot pin itself; that md5 is measured by the
    # constants check directly. The gap was found by running the check, not by reading.
    ("build_k351_pins", "tools/build_k351_pins.py"),
    ("canon_v38_13", "project_canon_v38_13.json"),
]
HELD = [
    ("combined", "combined.html"),
    ("corpus", "efilist_argument_library_v4_0_0.json"),
    ("jsx", "efilist_argument_library_v4_0_0.jsx"),
    ("canon_v38_12", "project_canon_v38_12.json"),
    ("assembly_v1_0", "adversarial_map_staging/adversarial_map_v1_0.json"),
    ("assembly_v1_1", "adversarial_map_staging/adversarial_map_v1_1.json"),
    ("assembly_v1_2", "adversarial_map_staging/adversarial_map_v1_2.json"),
    ("build_assembly_v1_2", "adversarial_map_staging/build_assembly_v1_2.py"),
    ("register_v0_3", "adversarial_map_staging/honest_residuals_register_v0_3.json"),
    ("build_register_v0_3", "adversarial_map_staging/build_register_v0_3.py"),
    ("validator_v0_6", "adversarial_map_staging/adv_map_validator_v0_6.py"),
]


def main():
    spec = importlib.util.spec_from_file_location(
        "v6p", os.path.join(STG, "adv_map_validator_v0_6.py"))
    V = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(V)

    p = {}
    for stem, rel in NEW + HELD:
        f = os.path.join(REPO, rel)
        p[stem + "_md5"] = md5f(f)
        p[stem + "_bytes"] = sz(f)

    corpus = rj(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"))
    p["objections_digest"] = V.objections_digest(corpus)
    p["objections"] = len(corpus["objections"])

    a = rj(os.path.join(STG, "adversarial_map_v1_3.json"))
    prev = rj(os.path.join(STG, "adversarial_map_v1_2.json"))
    p["assembly_entries"] = a["meta"]["entries"]
    p["assembly_class_counts"] = a["meta"]["class_counts"]
    p["assembly_class_counts_prev"] = prev["meta"]["class_counts"]
    p["coverage"] = "%d/%d" % (a["meta"]["nodes_covered"], a["meta"]["nodes_total"])
    p["variant_coverage"] = a["meta"]["variant_coverage"]
    p["note_coverage"] = a["meta"]["note_coverage"]

    r = rj(os.path.join(STG, "honest_residuals_register_v0_4.json"))
    p["bedrocks"] = r["meta"]["bedrocks"]
    p["residue_entries"] = r["meta"]["residue_entries"]
    p["undeclared_adjacencies"] = sum(
        1 for x in r["audit"] if x["severity"] == "undeclared-adjacency")

    # care-ethics: the cap the kickoff warned about, and the one that actually bound.
    node = next(o for o in corpus["objections"] if o["id"] == "care-ethics")
    nvar = len(V.node_variant_slots(node))
    p["care_ethics"] = {
        "entries": sum(1 for e in a["entries"] if e["target_id"] == "care-ethics"),
        "variant_loci": nvar, "node_bound": 3 + 3 * nvar,
        "long_locus_owner_phase": next(e["provenance"]["phase"] for e in a["entries"]
                                       if e["target_id"] == "care-ethics"
                                       and e["target_locus"] == "long"),
        "binding_constraint": "the PARTITION invariant, not entry-cap-node",
    }

    # unqueued (b): the queue builder reads the A-E fragments only.
    AE = {"A", "B1", "B2", "C", "D", "E"}
    def unq(doc):
        return sorted("%s#%s [%s]" % (e["target_id"], e["target_locus"], e["provenance"]["phase"])
                      for e in doc["entries"]
                      if e["class"] == "b" and e["provenance"]["phase"] not in AE)
    p["unqueued_b_before"] = len(unq(prev))
    p["unqueued_b_after"] = len(unq(a))
    p["unqueued_b_entries"] = unq(a)

    cA = rj(os.path.join(STG, "assembly_control_v0_3.json"))
    cR = rj(os.path.join(STG, "register_control_v0_2.json"))
    vK = rj(os.path.join(REPO, "tools", "k351_verification.json"))
    p["controls"] = {"assembly": cA["summary"], "register": cR["summary"],
                     "verification": vK["summary"],
                     "total": (cA["summary"]["controls"] + cR["summary"]["controls"]
                               + vK["summary"]["checks"]),
                     "total_passed": (cA["summary"]["passed"] + cR["summary"]["passed"]
                                      + vK["summary"]["passed"])}
    p["base_ref"] = "649fdbc288611fa6ea420e95055d810264301a06"
    p["phaseG_base_blob_md5"] = "d7cd18eb0467f38d8ecd4694776dd885"
    p["date_operator_local"] = "2026-09-18"

    out = json.dumps(p, indent=2, ensure_ascii=True, sort_keys=True) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), hashlib.md5(b).hexdigest()))
    print("  %d pinned paths; controls %d/%d"
          % (len(NEW) + len(HELD), p["controls"]["total_passed"], p["controls"]["total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
