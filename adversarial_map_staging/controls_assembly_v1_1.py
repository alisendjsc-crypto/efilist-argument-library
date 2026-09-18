#!/usr/bin/env python3
"""K348 controls for adversarial_map_v1_1.json.  A gate with no failing control is not a gate.

Five batteries:
  1. THE PREDECESSOR'S FATE, MEASURED.  v1_0 passes against its own pinned corpus and fails
     against the post-cut one, on exactly the checks the successor exists to repair.  The
     claim "v1_0 is frozen, not stale" is only worth anything if both halves are run.
  2. MUTATION BATTERY on v1_1.  Nine mutations, each naming the check it must trip.  One of
     them removes an entry and proves COVERAGE fails, because coverage is the claim this
     artifact exists to make and a coverage gate that cannot fail is decoration.
  3. THE BUILDER REFUSES.  The builder's own invariants are exercised by running it with
     the supersede set emptied: it must refuse, on anchors, rather than write.
  4. CLASS MIX, two-sided, against the A-E base rate -- ccclxviii applies to a union as much
     as to a phase.  Reported for the union AND for the disjoint new-only set, because the
     union CONTAINS the base and a test of a set against a rate computed from its own
     subset is not independent.  Saying so is the point.
  5. THE PARTITION INVARIANT, both units, computed rather than asserted.

Repo-relative.  --out <dir> writes the control record elsewhere.
"""
import os, sys, json, copy, math, tempfile, collections, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "assembly_control_v0_1.json")

sys.path.insert(0, STAGE)
import adv_map_validator_v0_5 as V

CORPUS_POST = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
CORPUS_PRE = os.environ.get("K348_CORPUS_PRE")     # git show 3e71546:efilist_argument_library_v4_0_0.json
V1_1 = os.path.join(MAP_DIR, "adversarial_map_v1_1.json")
V1_0 = os.path.join(STAGE, "adversarial_map_v1_0.json")

res = []
tmp = tempfile.mkdtemp(prefix="k348_ctl_")
base = json.loads(open(V1_1, "rb").read().decode("utf-8"))
corpus = json.loads(open(CORPUS_POST, "rb").read().decode("utf-8"))
nodes = {o["id"]: o for o in corpus["objections"]}


def run(path, corpus_path, assembly=True):
    return V.validate([path], corpus_path, assembly=assembly, out=lambda s: None)


def write(doc, name):
    p = os.path.join(tmp, name)
    open(p, "w", encoding="utf-8", newline="\n").write(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return p


def mutation(name, mutate, expect_check):
    d = copy.deepcopy(base)
    mutate(d)
    ok, viol, _adv = run(write(d, "m_%s.json" % name), CORPUS_POST)
    tripped = any(v.startswith(expect_check + ":") for v in viol)
    good = tripped and not ok
    res.append((name, good, expect_check))
    print("%s . control [%s] expects FAIL on %s -> %s"
          % ("PASS" if good else "FAIL", name, expect_check, "tripped" if tripped else viol[:2]))


print("=== (1) THE PREDECESSOR'S FATE, BOTH HALVES ===")
if CORPUS_PRE and os.path.exists(CORPUS_PRE):
    ok0, v0, a0 = run(V1_0, CORPUS_PRE)
    good = ok0 and not v0 and not a0
    res.append(("v1_0-still-passes-against-its-own-pinned-corpus", good, "-"))
    print("%s . v1_0 vs PRE-cut corpus under --assembly: %d violations, %d advisories"
          % ("PASS" if good else "FAIL", len(v0), len(a0)))
else:
    print("SKIP . K348_CORPUS_PRE not set; the pre-cut half of the control did not run")
    res.append(("v1_0-still-passes-against-its-own-pinned-corpus", False, "-"))
okp, vp, _ap = run(V1_0, CORPUS_POST)
names = sorted({v.split(":")[0] for v in vp})
want = ["anchor-rule", "meta-corpus-pin", "objections-digest"]
good = (not okp) and names == want and len([v for v in vp if v.startswith("anchor-rule:")]) == 3
res.append(("v1_0-fails-post-cut-on-exactly-the-repaired-checks", good, "-"))
print("%s . v1_0 vs POST-cut corpus: %d violations over checks %s"
      % ("PASS" if good else "FAIL", len(vp), names))

print()
print("=== (2) MUTATION BATTERY on v1_1 ===")
ok, viol, adv = run(V1_1, CORPUS_POST)
good = ok and not viol and not adv
res.append(("v1_1-unmutated-passes-assembly-0-violations-0-advisories", good, "-"))
print("%s . v1_1 unmutated under --assembly: %d violations, %d advisories"
      % ("PASS" if good else "FAIL", len(viol), len(adv)))

# the node whose ONLY entry is at a primary locus -- removing it removes a node from coverage
solo = None
per_node = collections.Counter(e["target_id"] for e in base["entries"])
for e in base["entries"]:
    if per_node[e["target_id"]] == 1:
        solo = e
        break
assert solo is not None, "no single-entry node to remove -- rewrite this control"


def drop_solo(d):
    d["entries"] = [x for x in d["entries"]
                    if not (x["target_id"] == solo["target_id"]
                            and x["target_anchor"] == solo["target_anchor"])]
    d["meta"]["entries"] = len(d["entries"])
    d["meta"]["nodes_covered"] = d["meta"]["nodes_covered"] - 1
    d["meta"]["coverage_distinct_ids"] = d["meta"]["coverage_distinct_ids"] - 1
    cc = collections.Counter(x["class"] for x in d["entries"])
    d["meta"]["class_counts"] = {k: cc[k] for k in ("a", "b", "c", "d")}


mutation("remove-an-entry-breaks-COVERAGE", drop_solo, "coverage")

varent = [e for e in base["entries"] if V.variant_slot(e["target_locus"]) is not None]
solo_var = None
per_loc = collections.Counter((e["target_id"], e["target_locus"]) for e in base["entries"])
for e in varent:
    if per_loc[(e["target_id"], e["target_locus"])] == 1:
        solo_var = e
        break


def drop_variant(d):
    d["entries"] = [x for x in d["entries"]
                    if not (x["target_id"] == solo_var["target_id"]
                            and x["target_anchor"] == solo_var["target_anchor"])]
    d["meta"]["entries"] = len(d["entries"])
    cc = collections.Counter(x["class"] for x in d["entries"])
    d["meta"]["class_counts"] = {k: cc[k] for k in ("a", "b", "c", "d")}


mutation("remove-a-variant-entry-breaks-VARIANT-COVERAGE", drop_variant, "variant-coverage")

# restore one of the three superseded v1_0 entries, with its PRE-cut anchor
sup = base["meta"]["supersedes"]["entries"][0]
donor = [e for e in base["entries"] if e["target_id"] == sup["target_id"]][0]


def restore_superseded(d):
    e = copy.deepcopy(donor)
    e["target_locus"] = sup["target_locus"]
    e["target_anchor"] = sup["destroyed_anchor"]
    d["entries"].append(e)
    d["meta"]["entries"] = len(d["entries"])
    cc = collections.Counter(x["class"] for x in d["entries"])
    d["meta"]["class_counts"] = {k: cc[k] for k in ("a", "b", "c", "d")}


mutation("restoring-a-superseded-entry-breaks-ANCHOR-RULE", restore_superseded, "anchor-rule")

# a fourth entry at one locus -- the K345 per-locus cap, inside the K348 node bound
locus3 = [k for k, n in per_loc.items() if n == 3]
target_loc = locus3[0] if locus3 else (base["entries"][0]["target_id"], base["entries"][0]["target_locus"])


def fourth_at_locus(d):
    donor2 = [x for x in d["entries"]
              if (x["target_id"], x["target_locus"]) == target_loc][0]
    txt = V.locus_text(nodes[target_loc[0]], target_loc[1])
    words = txt.split()
    anchors = {x["target_anchor"] for x in d["entries"] if x["target_id"] == target_loc[0]}
    cand = next(" ".join(words[i:i + 5]) for i in range(len(words) - 5)
                if " ".join(words[i:i + 5]) in txt and " ".join(words[i:i + 5]) not in anchors)
    e = copy.deepcopy(donor2)
    e["target_anchor"] = cand
    d["entries"].append(e)
    d["meta"]["entries"] = len(d["entries"])
    cc = collections.Counter(x["class"] for x in d["entries"])
    d["meta"]["class_counts"] = {k: cc[k] for k in ("a", "b", "c", "d")}


mutation("fourth-entry-at-one-locus-breaks-ENTRY-CAP", fourth_at_locus, "entry-cap")

# a node with NO variant loci must still be capped at 3 EXACTLY -- the property the K348
# amendment was written to preserve, tested on the real artifact rather than on a fixture
novar = [tid for tid, n in per_node.items()
         if n == 3 and not V.node_variant_slots(nodes[tid])]
assert novar, "no 3-entry no-variant node in the assembly -- rewrite this control"
NV = sorted(novar)[0]


def fourth_at_novariant_node(d):
    donor3 = [x for x in d["entries"] if x["target_id"] == NV][0]
    used = {(x["target_locus"]) for x in d["entries"] if x["target_id"] == NV}
    loc = next(L for L in ("long", "medium", "short", "diagnosis") if L not in used)
    txt = V.locus_text(nodes[NV], loc)
    words = txt.split()
    e = copy.deepcopy(donor3)
    e["target_locus"] = loc
    e["target_anchor"] = " ".join(words[:6])
    d["entries"].append(e)
    d["meta"]["entries"] = len(d["entries"])
    cc = collections.Counter(x["class"] for x in d["entries"])
    d["meta"]["class_counts"] = {k: cc[k] for k in ("a", "b", "c", "d")}


mutation("no-variant-node-still-capped-at-3-breaks-ENTRY-CAP-NODE",
         fourth_at_novariant_node, "entry-cap-node")

mutation("wrong-corpus-pin-breaks-META-CORPUS-PIN",
         lambda d: d["meta"].__setitem__("source_corpus_md5", "0" * 32), "meta-corpus-pin")
mutation("wrong-objections-digest-breaks-OBJECTIONS-DIGEST",
         lambda d: d["meta"].__setitem__("source_corpus_objections_md5", "0" * 32),
         "objections-digest")
mutation("wrong-class-counts-breaks-META-SUMMARIES",
         lambda d: d["meta"]["class_counts"].__setitem__("a", d["meta"]["class_counts"]["a"] + 1),
         "meta-summaries")
mutation("wrong-variant-coverage-declaration-breaks-VARIANT-COVERAGE",
         lambda d: d["meta"].__setitem__("variant_coverage", "38/39"), "variant-coverage")

print()
print("=== (3) THE BUILDER REFUSES ===")
spec = importlib.util.spec_from_file_location("bld", os.path.join(STAGE, "build_assembly_v1_1.py"))
bld = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], "--out", tmp]
spec.loader.exec_module(bld)
bld.OUT = os.path.join(tmp, "refuse.json")
bld.SUPERSEDED = ()
rc = bld.main()
good = rc == 1 and not os.path.exists(bld.OUT)
res.append(("builder-refuses-when-the-supersede-set-is-emptied", good, "-"))
print("%s . builder with SUPERSEDED=() returned %d and wrote nothing"
      % ("PASS" if good else "FAIL", rc))

print()
print("=== (4) CLASS MIX vs THE A-E BASE RATE (ccclxviii) ===")
BASE = {"a": 39, "b": 21, "c": 1, "d": 32}
nb = sum(BASE.values())
p0 = (BASE["a"] + BASE["d"]) / float(nb)


def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def two_sided(k, n, p):
    pmf = [C(n, i) * (p ** i) * ((1 - p) ** (n - i)) for i in range(n + 1)]
    return sum(q for q in pmf if q <= pmf[k] + 1e-15)


cc = collections.Counter(e["class"] for e in base["entries"])
n_all = len(base["entries"])
k_all = cc["a"] + cc["d"]
p_all = two_sided(k_all, n_all, p0)
new = [e for e in base["entries"] if e["provenance"]["phase"] in ("R", "F")]
ccn = collections.Counter(e["class"] for e in new)
n_new = len(new)
k_new = ccn["a"] + ccn["d"]
p_new = two_sided(k_new, n_new, p0)
print("  base (v1_0, phases A-E) a+d = %d/%d = %.4f" % (BASE["a"] + BASE["d"], nb, p0))
print("  UNION      a+d = %d/%d = %.4f   exact two-sided p = %.4f" % (k_all, n_all, k_all / float(n_all), p_all))
print("  NEW ONLY   a+d = %d/%d = %.4f   exact two-sided p = %.4f" % (k_new, n_new, k_new / float(n_new), p_new))
print("  NOTE: the union CONTAINS the base, so the union test is not independent and is")
print("        reported for completeness. The disjoint R+F test is the one that carries weight.")
good = p_all >= 0.05 and p_new >= 0.05
res.append(("class-mix-consistent-with-prior-both-framings", good, "-"))
print("%s . both framings sit inside the prior" % ("PASS" if good else "FAIL"))

print()
print("=== (5) THE PARTITION INVARIANT, BOTH UNITS ===")
by_locus, by_node = collections.defaultdict(set), collections.defaultdict(set)
for e in base["entries"]:
    by_locus[(e["target_id"], e["target_locus"])].add(e["provenance"]["phase"])
    by_node[e["target_id"]].add(e["provenance"]["phase"])
loc_clash = [k for k, v in by_locus.items() if len(v) > 1]
node_clash = sorted(k for k, v in by_node.items() if len(v) > 1)
declared = base["meta"]["partition_invariant"]["nodes_carrying_more_than_one_phase"]
good = not loc_clash and node_clash == sorted(declared) and len(node_clash) == 16
res.append(("partition-holds-at-the-locus-and-fails-at-the-node-as-declared", good, "-"))
print("%s . locus-level clashes %d ; node-level clashes %d (declared %d)"
      % ("PASS" if good else "FAIL", len(loc_clash), len(node_clash), len(declared)))

passed = sum(1 for _n, g, _c in res if g)
rec = {"artifact": "assembly_control_v0_1.json",
       "of": "adversarial_map_v1_1.json",
       "session": "K348", "date": "2026-09-17",
       "validator": "adv_map_validator_v0_5.py",
       "controls": passed, "controls_total": len(res),
       "all_pass": passed == len(res),
       "results": [{"name": n, "pass": g, "expects": c} for n, g, c in res],
       "class_mix": {"base_a_or_d": "%d/%d" % (BASE["a"] + BASE["d"], nb),
                     "base_rate": round(p0, 4),
                     "union_a_or_d": "%d/%d" % (k_all, n_all),
                     "union_two_sided_p": round(p_all, 6),
                     "new_only_a_or_d": "%d/%d" % (k_new, n_new),
                     "new_only_two_sided_p": round(p_new, 6),
                     "independence_note": ("the union contains the base, so only the disjoint "
                                           "R+F figure is an independent test of the prior")},
       "partition": {"locus_level_clashes": len(loc_clash),
                     "node_level_clashes": len(node_clash),
                     "nodes": node_clash},
       "single_entry_node_removed_in_the_coverage_control": solo["target_id"],
       "no_variant_node_used_for_the_bound_control": NV}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
print()
print(json.dumps({"controls": len(res), "passed": passed, "all_pass": passed == len(res)}, indent=1))
print("wrote %s" % OUT)
sys.exit(0 if passed == len(res) else 1)
