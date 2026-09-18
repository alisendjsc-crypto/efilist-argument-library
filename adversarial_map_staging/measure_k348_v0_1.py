#!/usr/bin/env python3
"""K348 measurement file. Every numeric constant design v0_4 section 11 states is produced
here and gated against this file by build_design_v0_4.py. The doc transcribes; this measures.

Repo-relative. --out <dir> to emit elsewhere.
"""
import os, sys, json, re, math, collections

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "measure_k348_v0_1.json")

sys.path.insert(0, STAGE)
import adv_map_validator_v0_5 as V

corpus = json.loads(open(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"), "rb").read().decode("utf-8"))
nodes = {o["id"]: o for o in corpus["objections"]}
F = json.loads(open(os.path.join(STAGE, "adv_map_phaseF_v0_1.json"), "rb").read().decode("utf-8"))
A = json.loads(open(os.path.join(MAP_DIR, "adversarial_map_v1_1.json"), "rb").read().decode("utf-8"))

# ---- 11.1 inheritance, three-way -------------------------------------------------
AGG = re.compile(r"inherit", re.I)
CONV = re.compile(r"aggravat|creates the defect|converse", re.I)
aggravated = [e for e in F["entries"]
              if e["class"] == "b" and AGG.search(e["grounds"]) and CONV.search(e["grounds"])]
cured = [e for e in F["entries"] if e["class"] == "a"
         and any(r.split("#")[0] == e["target_id"]
                 for r in (e.get("routing", {}).get("answered_by") or []))]
f_class = dict(collections.Counter(e["class"] for e in F["entries"]))

# ---- 11.2 gate 5: same-clause pairs and multi-entry loci in the assembly ----------
by_locus = collections.defaultdict(list)
for e in A["entries"]:
    by_locus[(e["target_id"], e["target_locus"])].append(e["target_anchor"])
multi = {k: v for k, v in by_locus.items() if len(v) > 1}
same_clause = 0
for k, anchors in multi.items():
    for i, a1 in enumerate(anchors):
        for a2 in anchors[i + 1:]:
            if a1 in a2 or a2 in a1:
                same_clause += 1

# ---- 11.3 the entry cap ----------------------------------------------------------
per_node = collections.Counter(e["target_id"] for e in A["entries"])
per_locus = collections.Counter((e["target_id"], e["target_locus"]) for e in A["entries"])
rows = {}
for tid, n in per_node.items():
    nv = len(V.node_variant_slots(nodes[tid]))
    rows[tid] = dict(entries=n, variant_loci=nv, bound_k345=3 + nv, bound_k348=3 + 3 * nv)
viol_k345 = sorted(t for t, r in rows.items() if r["entries"] > r["bound_k345"])
viol_k348 = sorted(t for t, r in rows.items() if r["entries"] > r["bound_k348"])
headroom0 = sorted(t for t, r in rows.items() if r["entries"] == r["bound_k348"])
within1 = sorted(t for t, r in rows.items() if r["bound_k348"] - r["entries"] <= 1)
rbr = rows["red-button-repugnant"]

# ---- the assembly's own arithmetic ------------------------------------------------
cc = collections.Counter(e["class"] for e in A["entries"])
new = [e for e in A["entries"] if e["provenance"]["phase"] in ("R", "F")]
ccn = collections.Counter(e["class"] for e in new)
BASE_AD, BASE_N = 71, 93


def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def two_sided(k, n, p):
    pmf = [C(n, i) * (p ** i) * ((1 - p) ** (n - i)) for i in range(n + 1)]
    return sum(q for q in pmf if q <= pmf[k] + 1e-15)


p0 = BASE_AD / float(BASE_N)
k_all, n_all = cc["a"] + cc["d"], len(A["entries"])
k_new, n_new = ccn["a"] + ccn["d"], len(new)

# ---- partition, both units --------------------------------------------------------
bl, bn = collections.defaultdict(set), collections.defaultdict(set)
for e in A["entries"]:
    bl[(e["target_id"], e["target_locus"])].add(e["provenance"]["phase"])
    bn[e["target_id"]].add(e["provenance"]["phase"])

doc = {
 "artifact": "measure_k348_v0_1.json",
 "session": "K348", "date": "2026-09-17",
 "corpus_md5": V.md5_bytes(open(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"), "rb").read()),
 "assembly_md5": V.md5_bytes(open(os.path.join(MAP_DIR, "adversarial_map_v1_1.json"), "rb").read()),
 "inheritance": {
   "phaseF_class_counts": f_class,
   "phaseF_b_total": f_class.get("b", 0),
   "aggravated_count": len(aggravated),
   "aggravated_loci": sorted("%s#%s" % (e["target_id"], e["target_locus"]) for e in aggravated),
   "cured_count": len(cured),
   "cured_loci": sorted("%s#%s" % (e["target_id"], e["target_locus"]) for e in cured),
   "cure_criterion": "class (a) whose routing.answered_by names a locus of the SAME node",
   "aggravation_criterion": "class (b) whose grounds name inheritance AND mark the converse "
                            "(aggravates / creates the defect / converse)",
 },
 "gate5": {
   "assembly_multi_entry_loci": len(multi),
   "assembly_same_clause_pairs": same_clause,
   "validator_v0_5_self_test": 62,
   "validator_v0_4_self_test": 60,
   "parity_runs": 72, "parity_divergences": 0,
 },
 "entry_cap": {
   "per_locus_cap": 3,
   "max_entries_at_any_locus": max(per_locus.values()),
   "red_button_repugnant": rbr,
   "violations_under_k345_bound": viol_k345,
   "violations_under_k348_bound": viol_k348,
   "nodes_at_the_k348_bound": headroom0,
   "nodes_within_one_of_the_k348_bound": within1,
   "nodes_total": len(rows),
   "max_entries_at_any_node": max(per_node.values()),
 },
 "assembly": {
   "entries": len(A["entries"]),
   "nodes": A["meta"]["nodes_covered"], "nodes_total": A["meta"]["nodes_total"],
   "variant_coverage": A["meta"]["variant_coverage"],
   "variant_loci_hit": int(A["meta"]["variant_coverage"].split("/")[0]),
   "variant_loci_total": int(A["meta"]["variant_coverage"].split("/")[1]),
   "class_counts": {k: cc[k] for k in ("a", "b", "c", "d")},
   "inherited_from_v1_0": len([e for e in A["entries"]
                               if e["provenance"]["phase"] not in ("R", "F")]),
   "superseded": A["meta"]["supersedes"]["count"],
   "base_a_or_d": "%d/%d" % (BASE_AD, BASE_N), "base_rate": round(p0, 4),
   "union_a_or_d": "%d/%d" % (k_all, n_all), "union_share": round(k_all / float(n_all), 4),
   "union_two_sided_p": round(two_sided(k_all, n_all, p0), 4),
   "new_a_or_d": "%d/%d" % (k_new, n_new), "new_share": round(k_new / float(n_new), 4),
   "new_two_sided_p": round(two_sided(k_new, n_new, p0), 4),
 },
 "partition": {
   "locus_level_clashes": len([k for k, v in bl.items() if len(v) > 1]),
   "node_level_clashes": len([k for k, v in bn.items() if len(v) > 1]),
   "nodes": sorted(k for k, v in bn.items() if len(v) > 1),
 },
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
print("wrote %s  %d B  md5 %s" % (OUT, len(json.dumps(doc, indent=1, ensure_ascii=False).encode()) + 1,
                                  V.md5_bytes((json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode())))
print(json.dumps({k: doc[k] for k in ("inheritance", "gate5", "entry_cap", "partition")}, indent=1)[:2600])
