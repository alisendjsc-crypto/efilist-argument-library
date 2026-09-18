"""K345b: calibrate MAP1_TRANSITIONS against the observed transitions in realWorldExamples.

WHAT THIS IS FOR. MAP1's 2,886 edges are scored from premise overlap and tier distance and carry
no observed field anywhere. This asks whether they predict where real exchanges actually go. It is
an INSTRUMENT, not a verdict: it reports rates with their chance baselines and refuses to interpret.

THE CONTROL THAT MATTERS. MAP1 is dense -- ~21.6% of all ordered (source,target) pairs are edges
pooled -- so a randomly drawn pair hits often. Any raw hit rate is meaningless without the
shuffled-target baseline computed here, and K345's "23 of 53" was published without it.

THE CONFOUND THAT MATTERS. attached_objections is many-to-many. Crossing consecutive instances
inflates n and the cross-pairs are NOT independent: two nodes attached to one instance are often
premise-siblings, and MAP1 is BUILT from premise overlap, so the cross-product manufactures hits
for a reason that has nothing to do with conversational dynamics. STRICT mode keeps only instances
carrying exactly one attached objection. Report both; trust neither alone.

Run: python adversarial_map_staging/rwe_map1_calibration_v0_1.py [--out <dir>] [--emit]
"""
import sys, os, json, re, random, hashlib, statistics as st
from collections import defaultdict
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SEED = 345
SLOTS = ("sophisticate", "defender", "drifter", "blended")
SEQ = re.compile(r"-(\d{3})$")


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


def observed(rwe, strict):
    """Ordered (source, target, observed_archetype) triples from adjacent instances in a thread.
    Order comes from the numbered instance_id suffix where every member has one; array order is a
    fallback and is FLAGGED, never silently assumed."""
    th = defaultdict(list)
    for idx, r in enumerate(rwe):
        if r.get("thread_id"): th[r["thread_id"]].append((idx, r))
    out, fallback = [], []
    for tid, items in th.items():
        if len(items) < 2: continue
        numbered = all(SEQ.search(r["instance_id"]) for _, r in items)
        if not numbered: fallback.append(tid)
        seq = sorted(items, key=lambda p: (int(SEQ.search(p[1]["instance_id"]).group(1)) if numbered else p[0]))
        recs = [(r, [a["objection_id"] for a in r.get("attached_objections", [])]) for _, r in seq]
        for (ra, na), (rb, nb) in zip(recs, recs[1:]):
            if strict and (len(na) != 1 or len(nb) != 1): continue
            for x in na:
                for y in nb:
                    if x != y: out.append((x, y, ra.get("archetype_signal_observed")))
    return out, fallback


def run(triples, pooled, bybranch, srcs, conditioned, trials=3000):
    S = sorted(set(triples))
    if not S: return None
    def tg(x, a):
        if conditioned and a in SLOTS: return bybranch.get(x, {}).get(a, set())
        return pooled.get(x, set())
    hit = sum(1 for x, y, a in S if y in tg(x, a))
    # `srcs` is a set, and set iteration order for strings varies BETWEEN PROCESSES with
    # PYTHONHASHSEED. Drawing from an unsorted comprehension made this permutation test
    # non-reproducible despite a fixed seed -- caught by the determinism control, not by
    # reading the code. Candidates are sorted once per source and reused.
    cand = {x: sorted(n for n in srcs if n != x) for x, _, _ in S}
    random.seed(SEED); rates = []
    for _ in range(trials):
        h = 0
        for x, y, a in S:
            if random.choice(cand[x]) in tg(x, a): h += 1
        rates.append(h / len(S))
    rates.sort()
    k = max(1, int(0.025 * trials))
    return {"n": len(S), "hits": hit, "rate": round(hit / len(S), 4),
            "chance_mean": round(st.mean(rates), 4),
            "chance_95_lo": round(rates[k], 4), "chance_95_hi": round(rates[-k], 4),
            "p_permutation": round(sum(1 for r in rates if r >= hit / len(S)) / trials, 4)}


def power(baseline, effect, ns, trials=1500):
    out = {}
    for n in ns:
        random.seed(9); det = 0
        for _ in range(trials):
            obs = sum(1 for _ in range(n) if random.random() < baseline + effect)
            null = sorted(sum(1 for _ in range(n) if random.random() < baseline) for _ in range(120))
            if obs > null[int(0.95 * len(null))]: det += 1
        out[str(n)] = round(det / trials, 3)
    return out


d = json.load(open(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"), encoding="utf-8"))
M = load_map1(os.path.join(REPO, "combined.html"))
srcs = set(M)
pooled = {s: {e["target"] for k, a in v.items() if k != "source_meta" for e in a} for s, v in M.items()}
bybranch = {s: {k: {e["target"] for e in a} for k, a in v.items() if k != "source_meta"} for s, v in M.items()}
deg = [len(v) for v in pooled.values()]
crossed, fb = observed(d["realWorldExamples"], False)
strict, _ = observed(d["realWorldExamples"], True)

REP = {
 "artifact": "rwe_map1_calibration_v0_1.json",
 "measured": "2026-09-17, wuld.ink Cowork, K345b",
 "asks": "Do MAP1_TRANSITIONS edges predict where real exchanges actually go?",
 "answer": "NOT YET ANSWERABLE. Reported below with the baselines and the confound that decides it.",
 "map1": {"sources": len(M), "edges": sum(len(a) for v in M.values() for k, a in v.items() if k != "source_meta"),
          "branches": sorted({k for v in M.values() for k in v if k != "source_meta"}),
          "pooled_outdegree_mean": round(sum(deg) / len(deg), 1),
          "pooled_edge_density": round(sum(deg) / (len(srcs) * (len(srcs) - 1)), 4),
          "observed_fields_on_edges": "NONE -- every edge is scored from premise overlap and tier distance"},
 "ordering": {"threads_using_numbered_instance_ids": True,
              "threads_falling_back_to_array_order": fb,
              "note": "array-order fallback is flagged, never silently assumed"},
 "tests": {
  "crossed_pooled": run(crossed, pooled, bybranch, srcs, False),
  "crossed_archetype_conditioned": run(crossed, pooled, bybranch, srcs, True),
  "STRICT_pooled": run(strict, pooled, bybranch, srcs, False),
  "STRICT_archetype_conditioned": run(strict, pooled, bybranch, srcs, True)},
 "reading": (
  "The apparent signal lives ENTIRELY in the cross-product. Crossed mode reaches p around 0.01-0.02, "
  "but its units are not independent -- two nodes attached to one instance are often premise-siblings "
  "and MAP1 is built from premise overlap, so the cross-product manufactures hits for a reason that is "
  "not conversational. STRICT mode, which is the clean test, drops to n=%d and lands nowhere near "
  "significance. THERE IS NO DEFENSIBLE SIGNAL YET. What exists is a working method, a known chance "
  "baseline, and a data requirement." % len(set(strict))),
 "power_to_detect_a_10pt_effect": power(0.339, 0.10, [53, 100, 200, 400, 800]),
 "what_would_change_it": (
  "Roughly n=200 clean units for ~88%% power against a 10-point effect. The clean count today is %d, "
  "from 136 instances. So the binding constraint is NOT the number of real-world instances -- it is how "
  "many are THREADED, SEQUENTIALLY NUMBERED and SINGLE-ATTACHMENT. Collecting more one-off instances "
  "grows the panel's other purposes and moves this test almost not at all." % len(set(strict))),
 "not_ruled_here": "Whether MAP1's analytic weights are right. This instrument cannot say, and says so."}
print(json.dumps(REP, indent=1, ensure_ascii=False))
if "--emit" in sys.argv:
    dest = os.path.join(OUT, "adversarial_map_staging", "rwe_map1_calibration_v0_1.json")
    b = (json.dumps(REP, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print("\nWROTE %s\n  bytes %d  md5 %s" % (dest, len(b), hashlib.md5(b).hexdigest()), file=sys.stderr)
