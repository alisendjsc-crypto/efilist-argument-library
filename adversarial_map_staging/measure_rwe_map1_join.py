"""K345a: recompute every figure canon's CORPUS_IS_REACTIVE_ONLY_K345 entry cites, and
assert the canon text agrees. The entry quotes; this file measures. Run with no args to
gate the committed canon: python adversarial_map_staging/measure_rwe_map1_join.py"""
import sys, os, json, re
from collections import Counter, defaultdict
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)

def load_map1(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    i = t.find("var MAP1_TRANSITIONS = ") + len("var MAP1_TRANSITIONS = ")
    depth = 0; j = i
    while True:
        if t[j] == "{": depth += 1
        elif t[j] == "}":
            depth -= 1
            if depth == 0: break
        j += 1
    return json.loads(t[i:j + 1])

d = json.load(open(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"), encoding="utf-8"))
M = load_map1(os.path.join(REPO, "combined.html"))
rwe = d["realWorldExamples"]; ids = [n["id"] for n in d["objections"]]
m = {}
m["nodes"] = len(ids)
m["rwe_instances"] = len(rwe)
att = set()
for r in rwe:
    for a in r.get("attached_objections", []): att.add(a["objection_id"])
m["rwe_nodes_covered"] = len(att & set(ids))
m["map1_sources"] = len(M)
m["map1_edges"] = sum(len(a) for v in M.values() for k, a in v.items() if k != "source_meta")
m["map1_branches"] = len({k for v in M.values() for k in v if k != "source_meta"})
m["map1_observed_fields"] = sorted({f for v in M.values() for k, a in v.items() if k != "source_meta"
                                    for e in a for f in e if re.search(r"observ|empiric|freq|count|seen|attest", f, re.I)})
dis = Counter(v["source_meta"].get("disengagement_probability") for v in M.values() if "source_meta" in v)
m["disengagement"] = dict(dis)
arch = Counter(r.get("archetype_signal_observed") for r in rwe)
m["archetype_observed"] = {k: arch[k] for k in ("sophisticate", "defender", "drifter", "blended")}
m["archetype_not_applicable"] = arch.get("not-applicable", 0)
m["archetype_applicable"] = sum(m["archetype_observed"].values())
slots = Counter()
for n in d["objections"]:
    for s in (n["responses"].get("archetypeVariants") or {}): slots[s] += 1
m["archetype_authored"] = dict(slots)
th = defaultdict(list)
for idx, r in enumerate(rwe):
    if r.get("thread_id"): th[r["thread_id"]].append((idx, r))
multi = {k: v for k, v in th.items() if len(v) > 1}
m["threads"] = len(th); m["threads_multi"] = len(multi)
m["instances_in_multi"] = sum(len(v) for v in multi.values())
SEQ = re.compile(r"-(\d{3})$")
m["threads_multi_numbered"] = sum(1 for v in multi.values() if all(SEQ.search(r["instance_id"]) for _, r in v))
pairs = []
for tid, items in multi.items():
    numbered = all(SEQ.search(r["instance_id"]) for _, r in items)
    seq = sorted(items, key=lambda p: (int(SEQ.search(p[1]["instance_id"]).group(1)) if numbered else p[0]))
    nodes = [[a["objection_id"] for a in r.get("attached_objections", [])] for _, r in seq]
    for a, b in zip(nodes, nodes[1:]):
        for x in a:
            for y in b:
                if x != y: pairs.append((x, y))
m["ordered_pairs"] = len(pairs); m["ordered_pairs_distinct"] = len(set(pairs))
hit = 0
for x, y in set(pairs):
    tg = {e["target"] for k, a in M.get(x, {}).items() if k != "source_meta" for e in a}
    if y in tg: hit += 1
m["pairs_map1_contains"] = hit
m["nodes_no_rwe"] = sorted(set(ids) - att)
m["nodes_absent_map1"] = sorted(set(ids) - set(M))
m["uncovered_sets_identical"] = m["nodes_no_rwe"] == m["nodes_absent_map1"]
print(json.dumps(m, indent=1, ensure_ascii=False))

canon = [f for f in os.listdir(REPO) if re.match(r"project_canon_v38_\d+\.json$", f)]
if not canon: sys.exit(0)
c = json.load(open(os.path.join(REPO, sorted(canon)[-1]), encoding="utf-8"))
txt = c["open_questions"]["active"].get("CORPUS_IS_REACTIVE_ONLY_K345", "")
CLAIMS = [("136 instances", m["rwe_instances"]), ("78 of the 82", m["rwe_nodes_covered"]),
          ("2,886 edges", m["map1_edges"]), ("78 source nodes", m["map1_sources"]),
          ("4 \narchetype branches", m["map1_branches"]), ("15 threads", m["threads"]),
          ("11 with more than", m["threads_multi"]), ("51 instances", m["instances_in_multi"]),
          ("57 ordered", m["ordered_pairs"]), ("53 distinct", m["ordered_pairs_distinct"]),
          ("23 are edges", m["pairs_map1_contains"]), ("sophisticate 72", m["archetype_observed"]["sophisticate"]),
          ("defender 15", m["archetype_observed"]["defender"]), ("drifter 6", m["archetype_observed"]["drifter"]),
          ("blended 5", m["archetype_observed"]["blended"]), ("98 applicable", m["archetype_applicable"]),
          ("38 not-applicable", m["archetype_not_applicable"]),
          ("sophisticate 13", m["archetype_authored"]["sophisticate"]), ("defender 12", m["archetype_authored"]["defender"]),
          ("LOW 10", m["disengagement"].get("LOW")), ("MEDIUM 61", m["disengagement"].get("MEDIUM"))]
flat = " ".join(txt.split())
bad = 0
for needle, measured in CLAIMS:
    n = " ".join(needle.split())
    nums = re.findall(r"\d[\d,]*", n)
    ok = (n in flat) and any(x.replace(",", "") == str(measured) for x in nums)
    if not ok: bad += 1; print("CANON MISMATCH: %r vs measured %s" % (n, measured))
assert m["map1_observed_fields"] == [], "MAP1 now HAS an observed field -- the canon entry is out of date"
print("\n%s: %d of %d canon figures matched measurement" % ("FAIL" if bad else "CANON AGREES WITH MEASUREMENT", len(CLAIMS) - bad, len(CLAIMS)))
sys.exit(1 if bad else 0)
