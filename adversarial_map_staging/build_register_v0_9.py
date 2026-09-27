#!/usr/bin/env python3
"""honest_residuals_register_v0_9.json -- v0_8 carried to adversarial_map_v1_8.json (L7, 2026-09-26, R0243).

Derived from v0_8 by the one delta the redrafts make, then cross-checked against v1_8 on the v0_6..v0_8 method:
  i.   A (d) whose routing a redraft changed (provenance.redrafted_L7 with routing in fields_changed) leaves its old
       facet and joins the facet of the registered (d) its row copied its bedrock from (bedrock_from, by locus AND
       anchor), in map order; its terminus_routing follows the map, and the move is recorded in `moved_at_L7`.
  ii.  Nothing else moves: the bedrocks that moved are exactly the one the tributary left and the one it joined; every
       (d) in v1_8 is a tributary with the map's terminus_routing and novel flag; no adjacency pair is undeclared.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, copy, hashlib, itertools, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_9.json")
V0_8 = os.path.join(STAGE, "honest_residuals_register_v0_8.json")
V0_8_MD5 = "8f6d38886b95033600752a5be052bd99"
ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_8.json")
RELATION_KINDS = ("depends_on", "stronger_than", "sibling_of", "independent_of", "conditions")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main():
    fail = []
    raw = open(V0_8, "rb").read()
    assert md5b(raw) == V0_8_MD5, "BASE GUARD: register v0_8 is %s" % md5b(raw)
    v8 = json.loads(raw.decode("utf-8"))
    reg = copy.deepcopy(v8)
    araw = open(ASSEMBLY, "rb").read()
    amap = json.loads(araw.decode("utf-8"))
    order = {(e["target_id"], e["target_locus"], e["target_anchor"]): i for i, e in enumerate(amap["entries"])}
    where = {}
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                where[(t["node"], t["locus"], t["anchor"])] = (b, f, t)
    touched, changes = set(), []
    for e in amap["entries"]:
        rd = e["provenance"].get("redrafted_L7")
        if not rd or "routing" not in rd["fields_changed"]:
            continue
        k = (e["target_id"], e["target_locus"], e["target_anchor"])
        if e["class"] != "d" or k not in where:
            fail.append("%s#%s: a redrafted routing on an entry the register does not hold as a (d)" % k[:2])
            continue
        bf = rd.get("bedrock_from")
        src = (bf["locus"].partition("#")[0], bf["locus"].partition("#")[2], bf["anchor"]) if bf else None
        if src not in where:
            fail.append("%s#%s: bedrock_from is not a registered tributary" % k[:2])
            continue
        nb, nf, _t = where[src]
        if (nb["bedrock_id"], nf["facet_id"]) != (bf["hr"], bf["facet"]):
            fail.append("%s#%s: bedrock_from is filed under %s/%s, not %s/%s"
                        % (k[0], k[1], nb["bedrock_id"], nf["facet_id"], bf["hr"], bf["facet"]))
            continue
        ob, of, t = where[k]
        r = e["routing"]["residue"]
        before = {"bedrock": ob["bedrock_id"], "facet": of["facet_id"], "terminus_routing": t["terminus_routing"]}
        of["tributaries"].remove(t)
        t = dict(t, terminus_routing=r["terminus_routing"], novel=r["novel"])
        t["moved_at_L7"] = {"row": rd["row"], "supersedes": rd["supersedes"], "answers": rd["answers"], "from": before}
        nf["tributaries"].append(t)
        where[k] = (nb, nf, t)
        touched |= {ob["bedrock_id"], nb["bedrock_id"]}
        changes.append("%s/%s -> %s/%s %s#%s (%s, answering %s)" % (before["bedrock"], before["facet"], nb["bedrock_id"],
                                                                    nf["facet_id"], k[0], k[1], rd["row"], rd["answers"]))
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            f["tributaries"].sort(key=lambda t: order.get((t["node"], t["locus"], t["anchor"]), 10 ** 6))
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
    old = {b["bedrock_id"]: b for b in v8["bedrocks"]}
    moved = sorted(b["bedrock_id"] for b in reg["bedrocks"]
                   if json.dumps(b, sort_keys=True) != json.dumps(old[b["bedrock_id"]], sort_keys=True))
    if moved != sorted(touched):
        fail.append("bedrocks that moved %s are not the ones the redrafts reach %s" % (moved, sorted(touched)))
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
        fail.append("UNDECLARED ADJACENCY: %s+%s (%s)" % (pair[0], pair[1], sorted(cands[pair])))
    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1
    meta = dict(v8["meta"])
    meta["artifact"] = "honest_residuals_register_v0_9.json"
    meta["source"] = {"artifact": amap["meta"]["artifact"], "md5": md5b(araw), "entries": amap["meta"]["entries"]}
    meta["source_corpus_md5"] = amap["meta"]["source_corpus_md5"]
    meta["source_corpus_objections_md5"] = amap["meta"]["source_corpus_objections_md5"]
    meta["residue_entries"] = len(want)
    meta["status"] = ("WORKING, derived from v0_8 by the redrafts' one delta and cross-checked against "
                      "adversarial_map_v1_8.json, whose redrafts a seat that did not draft them judges (K258).")
    meta["phases_contributing"] = dict(collections.Counter(
        t["phase"] for b in reg["bedrocks"] for f in b["facets"] for t in f["tributaries"]))
    meta["changes_from_v0_8"] = changes
    meta["parity_with_v0_8"] = ("Asserted before the write: the bedrocks that moved are exactly the ones the redrafted "
                                "tributary left and joined (%s); every (d) in adversarial_map_v1_8.json is a tributary here "
                                "with the map's terminus_routing and novel flag; no adjacency pair is undeclared."
                                % ", ".join(sorted(touched)))
    meta["predecessor"] = {"artifact": "honest_residuals_register_v0_8.json", "md5": V0_8_MD5,
                           "note": "stays byte-identical on disk; v0_9 supersedes it, it is not edited"}
    adj = dict(meta["adjacency"])
    adj["candidates_derived"] = len(cands)
    adj["declared_relations"] = len(declared)
    adj["detected_and_declared"] = sorted("%s+%s" % p for p in sorted(set(cands) & declared))
    adj["declared_but_undetected"] = sorted("%s+%s" % p for p in sorted(declared - set(cands)))
    meta["adjacency"] = adj
    out = json.dumps({"meta": meta, "audit": v8["audit"], "bedrocks": reg["bedrocks"]}, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), md5b(b)))
    print("  %d change(s); %d (d)s cross-checked; bedrocks moved %s; adjacency %d candidates, 0 undeclared"
          % (len(changes), len(want), moved, len(cands)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
