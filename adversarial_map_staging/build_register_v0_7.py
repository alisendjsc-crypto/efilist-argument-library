#!/usr/bin/env python3
"""honest_residuals_register_v0_7.json -- v0_6 plus #46's tributary (L4c, 2026-09-26).

Derived from v0_6 by one declared delta, then cross-checked against adversarial_map_v1_6.json, on the v0_6
method: every other bedrock and tributary is judged and must not move.
  i.   #46 (red-button-repugnant, defender slot), re-ruled FAILS on Josiah's word (R1-070) and reclassified to
       (d), joins HR-14 on the facet of the registered (d) its draft names (terminus-held-open, the node's own
       sophisticate slot), inserted in map order.
  ii.  Cross-check: every (d) in v1_6 is a tributary with the map's terminus_routing and novel flag; HR-14 is
       the only bedrock that moves, and only by that tributary; no adjacency pair is undeclared (the node
       already feeds HR-14, so no new pair can arise).

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, hashlib, itertools, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_7.json")
V0_6 = os.path.join(STAGE, "honest_residuals_register_v0_6.json")
V0_6_MD5 = "0689f46f18a4dbe8d40c9982a2ad06f9"
ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_6.json")
RELATION_KINDS = ("depends_on", "stronger_than", "sibling_of", "independent_of", "conditions")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main():
    fail = []
    raw = open(V0_6, "rb").read()
    assert md5b(raw) == V0_6_MD5, "BASE GUARD: register v0_6 is %s" % md5b(raw)
    v6 = json.loads(raw.decode("utf-8"))
    reg = json.loads(raw.decode("utf-8"))
    araw = open(ASSEMBLY, "rb").read()
    amap = json.loads(araw.decode("utf-8"))
    order = {(e["target_id"], e["target_locus"], e["target_anchor"]): i for i, e in enumerate(amap["entries"])}
    have = set()
    where = {}
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                k = (t["node"], t["locus"], t["anchor"])
                have.add(k)
                where[k] = (b["bedrock_id"], f)
    added = []
    for e in amap["entries"]:
        k = (e["target_id"], e["target_locus"], e["target_anchor"])
        am = e["provenance"].get("amended") or {}
        if e["class"] != "d" or k in have:
            continue
        if am.get("at") != "L4c":
            fail.append("%s#%s is a (d) the register lacks and L4c did not reclassify" % k[:2])
            continue
        src = (am["bedrock_from"].partition("#")[0], am["bedrock_from"].partition("#")[2], am["bedrock_from_anchor"])
        if src not in where:
            fail.append("%s#%s: bedrock_from is not a registered tributary" % k[:2])
            continue
        bid, facet = where[src]
        r = e["routing"]["residue"]
        facet["tributaries"].append({
            "phase": e["provenance"]["phase"], "node": k[0], "locus": k[1], "anchor": k[2], "novel": r["novel"],
            "terminus_routing": r["terminus_routing"],
            "reclassified": "from (a) at L4c under the R1 standard, row %s (superseding %s); through %s"
                            % (am["r1_row"], am["supersedes"], am["bedrock_from"])})
        added.append((bid, facet["facet_id"], k))
    if len(added) != 1:
        fail.append("expected exactly one new tributary (#46), found %d" % len(added))
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            ks = [(t["node"], t["locus"], t["anchor"]) for t in f["tributaries"]]
            base = [x for x in ks if x not in {a[2] for a in added}]
            if [order.get(x, -1) for x in base] != sorted(order.get(x, -1) for x in base):
                fail.append("%s/%s: v0_6's tributaries are not in map order" % (b["bedrock_id"], f["facet_id"]))
            f["tributaries"].sort(key=lambda t: order[(t["node"], t["locus"], t["anchor"])])
        b["tributary_count"] = sum(len(f["tributaries"]) for f in b["facets"])
    want = {}
    for e in amap["entries"]:
        if e["class"] == "d":
            r = e["routing"]["residue"]
            want[(e["target_id"], e["target_locus"], e["target_anchor"])] = (r["terminus_routing"], r["novel"])
    got = {(t["node"], t["locus"], t["anchor"]): (t["terminus_routing"], t["novel"])
           for b in reg["bedrocks"] for f in b["facets"] for t in f["tributaries"]}
    if got != want:
        fail.append("register and map disagree on %d tributaries" % len(set(got.items()) ^ set(want.items())))
    old = {b["bedrock_id"]: b for b in v6["bedrocks"]}
    moved = sorted(b["bedrock_id"] for b in reg["bedrocks"]
                   if json.dumps(b, sort_keys=True) != json.dumps(old[b["bedrock_id"]], sort_keys=True))
    if moved != sorted({a[0] for a in added}):
        fail.append("bedrocks that moved: %s" % moved)
    alias, cands, bynode, declared = {}, collections.defaultdict(set), collections.defaultdict(set), set()
    for b in reg["bedrocks"]:
        alias[b["bedrock_id"]] = [b["name"].lower()] + ([a.strip().lower() for a in re.split(r"[/]", b["alias"])]
                                                        if b["alias"] else [])
        for r in b["relations"]:
            declared.add(tuple(sorted((b["bedrock_id"], r["to"]))))
            if r["kind"] not in RELATION_KINDS:
                fail.append("%s declares kind %r" % (b["bedrock_id"], r["kind"]))
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                low = t["terminus_routing"].lower()
                for other, keys in alias.items():
                    if other != b["bedrock_id"] and (other.lower() in low or any(
                            k_ in low or k_.replace(" ", "-") in low for k_ in keys)):
                        cands[tuple(sorted((b["bedrock_id"], other)))].add("terminus names")
                bynode[t["node"]].add(b["bedrock_id"])
    for node, bids in bynode.items():
        for a, b_ in itertools.combinations(sorted(bids), 2):
            cands[(a, b_)].add("shared node %s" % node)
    for pair in sorted(set(cands) - declared):
        fail.append("UNDECLARED ADJACENCY: %s+%s" % pair)
    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1
    meta = dict(v6["meta"])
    meta["artifact"] = "honest_residuals_register_v0_7.json"
    meta["source"] = {"artifact": amap["meta"]["artifact"], "md5": md5b(araw), "entries": amap["meta"]["entries"]}
    meta["residue_entries"] = len(want)
    meta["status"] = ("WORKING, derived from v0_6 by one delta and cross-checked against adversarial_map_v1_6.json, "
                      "whose one re-ruled entry a seat that did not draft it judges (K258).")
    meta["phases_contributing"] = dict(collections.Counter(
        t["phase"] for b in reg["bedrocks"] for f in b["facets"] for t in f["tributaries"]))
    meta["changes_from_v0_6"] = [
        "#46 (red-button-repugnant, defender slot), re-ruled FAILS on Josiah's word (R1-070, on gate2's V-017), "
        "joins HR-14 on the terminus-held-open facet, beside the node's own sophisticate slot"]
    meta["parity_with_v0_6"] = ("Asserted before the write: HR-14 moved, by exactly that tributary, and no other "
                                "bedrock did; every (d) in adversarial_map_v1_6.json is a tributary here with the map's "
                                "terminus_routing and novel flag; no adjacency pair is undeclared.")
    meta["predecessor"] = {"artifact": "honest_residuals_register_v0_6.json", "md5": V0_6_MD5,
                           "note": "stays byte-identical on disk; v0_7 supersedes it, it is not edited"}
    adj = dict(meta["adjacency"])
    adj["candidates_derived"] = len(cands)
    adj["declared_relations"] = len(declared)
    adj["detected_and_declared"] = sorted("%s+%s" % p for p in sorted(set(cands) & declared))
    adj["declared_but_undetected"] = sorted("%s+%s" % p for p in sorted(declared - set(cands)))
    meta["adjacency"] = adj
    out = json.dumps({"meta": meta, "audit": v6["audit"], "bedrocks": reg["bedrocks"]}, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), md5b(b)))
    print("  added %s; %d (d)s cross-checked; adjacency %d candidates, 0 undeclared"
          % (["%s/%s %s#%s" % (a[0], a[1], a[2][0], a[2][1]) for a in added], len(want), len(cands)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
