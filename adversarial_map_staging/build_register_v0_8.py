#!/usr/bin/env python3
"""honest_residuals_register_v0_8.json -- v0_7 carried to the successor map v1_7 (L7, 2026-09-26, R0223).

Derived from v0_7 by the deltas the successor's rows make, then cross-checked against adversarial_map_v1_7.json, on
the v0_6/v0_7 method: every bedrock and tributary the rows do not reach is judged and must not move.
  i.   A (d) that v1_7 re-anchored or re-routed (provenance.successor_L7 on a v1_6 (d)) keeps its tributary; the
       tributary's anchor and terminus_routing follow the map, and the change is recorded in `revised_at_L7`.
  ii.  A (d) new in v1_7 (an entry reclassified to (d) at L7, or a (d) filed at L7) joins the facet of the registered
       (d) its row copied its bedrock from (bedrock_from, by locus AND anchor), in map order. A reclassified tributary
       keeps the phase that authored its move and carries `reclassified`; a filed one is phase H and carries `filed`.
  iii. No (d) leaves the register: v1_7 turns no v1_6 (d) into another class, and the build refuses if one does.
  iv.  Relations: the drafts record's `relation` rows are appended, and their notes' quotations are declared.
  v.   Cross-check: every (d) in v1_7 is a tributary here with the map's terminus_routing and novel flag; the bedrocks
       that moved are exactly those the rows reach; no adjacency pair is undeclared.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, copy, hashlib, itertools, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_8.json")
V0_7 = os.path.join(STAGE, "honest_residuals_register_v0_7.json")
V0_7_MD5 = "bcbff23113f3fb0135d5fd5b3e2630d5"
ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_7.json")
BASE_MAP = os.path.join(STAGE, "adversarial_map_v1_6.json")
BASE_MAP_MD5 = "7a69bc9fd197047c3cf7cecdb37a44ed"
DRAFTS = os.path.join(STAGE, "r1", "L7_successor_drafts.json")
RELATION_KINDS = ("depends_on", "stronger_than", "sibling_of", "independent_of", "conditions")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main():
    fail = []
    raw = open(V0_7, "rb").read()
    assert md5b(raw) == V0_7_MD5, "BASE GUARD: register v0_7 is %s" % md5b(raw)
    braw = open(BASE_MAP, "rb").read()
    assert md5b(braw) == BASE_MAP_MD5, "BASE GUARD: map v1_6 is %s" % md5b(braw)
    v7 = json.loads(raw.decode("utf-8"))
    reg = copy.deepcopy(v7)
    araw = open(ASSEMBLY, "rb").read()
    amap = json.loads(araw.decode("utf-8"))
    base = json.loads(braw.decode("utf-8"))
    draws = open(DRAFTS, "rb").read()
    if md5b(draws) != amap["meta"]["l7_successor"]["drafts"]["md5"]:
        fail.append("the drafts record is not the one the map names")
    drafts = json.loads(draws.decode("utf-8"))
    order = {(e["target_id"], e["target_locus"], e["target_anchor"]): i for i, e in enumerate(amap["entries"])}
    where = {}
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                where[(t["node"], t["locus"], t["anchor"])] = (b, f, t)
    was_d = {(e["target_id"], e["target_locus"], e["target_anchor"]) for e in base["entries"] if e["class"] == "d"}
    touched, changes = set(), []
    for i, e in enumerate(amap["entries"]):
        pv = e["provenance"]
        sl, fl = pv.get("successor_L7"), pv.get("filed")
        if not sl and not fl:
            continue
        k = (e["target_id"], e["target_locus"], e["target_anchor"])
        if sl:
            old = (k[0], k[1], sl["from"].get("target_anchor", k[2]))
            if old in was_d and e["class"] != "d":
                fail.append("%s#%s: a v1_6 (d) left the register's class" % k[:2])
                continue
        if e["class"] != "d":
            continue
        r = e["routing"]["residue"]
        if sl and old in was_d:
            if old not in where:
                fail.append("%s#%s: v1_6 (d) not in register v0_7" % k[:2])
                continue
            b, f, t = where[old]
            before = {x: t[x] for x in ("anchor", "terminus_routing", "novel")}
            after = {"anchor": k[2], "terminus_routing": r["terminus_routing"], "novel": r["novel"]}
            if before != after:
                t.update(after)
                t["revised_at_L7"] = {"row": sl["row"], "disposition": sl["disposition"],
                                      "fields": sorted(x for x in before if before[x] != after[x]),
                                      "from": {x: before[x] for x in before if before[x] != after[x]}}
                touched.add(b["bedrock_id"])
                changes.append("%s/%s %s#%s: %s (%s, %s)" % (b["bedrock_id"], f["facet_id"], k[0], k[1],
                                                               "+".join(t["revised_at_L7"]["fields"]), sl["row"],
                                                               sl["disposition"]))
            continue
        bf = (sl or fl).get("bedrock_from")
        if not bf:
            fail.append("%s#%s: a new (d) with no bedrock_from" % k[:2])
            continue
        src = (bf["locus"].partition("#")[0], bf["locus"].partition("#")[2], bf["anchor"])
        if src not in where:
            fail.append("%s#%s: bedrock_from is not a registered tributary" % k[:2])
            continue
        b, f, _t = where[src]
        if (b["bedrock_id"], f["facet_id"]) != (bf["hr"], bf["facet"]):
            fail.append("%s#%s: bedrock_from is filed under %s/%s, not %s/%s"
                        % (k[0], k[1], b["bedrock_id"], f["facet_id"], bf["hr"], bf["facet"]))
            continue
        t = {"phase": pv["phase"], "node": k[0], "locus": k[1], "anchor": k[2], "novel": r["novel"],
             "terminus_routing": r["terminus_routing"]}
        if sl:
            t["reclassified"] = ("from (%s) at L7, row %s (%s), after %s; through %s"
                                 % (sl["from"].get("class", "?"), sl["row"], sl["disposition"],
                                    ", ".join(sl["cause"].get("rows") or []) or "no landed row", bf["locus"]))
        else:
            t["filed"] = "at L7, row %s, from %s; through %s" % (fl["row"], ", ".join(fl["findings"]), bf["locus"])
        f["tributaries"].append(t)
        where[k] = (b, f, t)
        touched.add(b["bedrock_id"])
        changes.append("%s/%s %s#%s: joins (%s)" % (b["bedrock_id"], f["facet_id"], k[0], k[1], (sl or fl)["row"]))
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            f["tributaries"].sort(key=lambda t: order.get((t["node"], t["locus"], t["anchor"]), 10 ** 6))
        b["tributary_count"] = sum(len(f["tributaries"]) for f in b["facets"])
    # ---- relations drafted at L7 ----
    ids = {b["bedrock_id"]: b for b in reg["bedrocks"]}
    relations = []
    for row in drafts["rows"]:
        if row["kind"] != "relation":
            continue
        rel = row["relation"]
        declared = [q["quote"] for q in row.get("quotes", [])]
        for span in re.findall(r'"([^"]+)"', rel["note"]):
            if span not in declared:
                fail.append("%s: undeclared quotation in the relation note: %r" % (row["id"], span[:60]))
        if rel["kind"] not in RELATION_KINDS or rel["from"] not in ids or rel["to"] not in ids:
            fail.append("%s: relation %s %s %s is not well formed" % (row["id"], rel["from"], rel["kind"], rel["to"]))
            continue
        ids[rel["from"]]["relations"].append({"kind": rel["kind"], "to": rel["to"], "note": rel["note"]})
        touched.add(rel["from"])
        relations.append("%s %s %s (%s)" % (rel["from"], rel["kind"], rel["to"], row["id"]))
    # ---- cross-check against the map ----
    want = {}
    for e in amap["entries"]:
        if e["class"] == "d":
            r = e["routing"]["residue"]
            want[(e["target_id"], e["target_locus"], e["target_anchor"])] = (r["terminus_routing"], r["novel"])
    got = {(t["node"], t["locus"], t["anchor"]): (t["terminus_routing"], t["novel"])
           for b in reg["bedrocks"] for f in b["facets"] for t in f["tributaries"]}
    if got != want:
        fail.append("register and map disagree on %d tributaries" % len(set(got.items()) ^ set(want.items())))
    old = {b["bedrock_id"]: b for b in v7["bedrocks"]}
    moved = sorted(b["bedrock_id"] for b in reg["bedrocks"]
                   if json.dumps(b, sort_keys=True) != json.dumps(old[b["bedrock_id"]], sort_keys=True))
    if moved != sorted(touched):
        fail.append("bedrocks that moved %s are not the ones the rows reach %s" % (moved, sorted(touched)))
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
    meta = dict(v7["meta"])
    meta["artifact"] = "honest_residuals_register_v0_8.json"
    meta["source"] = {"artifact": amap["meta"]["artifact"], "md5": md5b(araw), "entries": amap["meta"]["entries"]}
    meta["source_corpus_md5"] = amap["meta"]["source_corpus_md5"]
    meta["source_corpus_objections_md5"] = amap["meta"]["source_corpus_objections_md5"]
    meta["residue_entries"] = len(want)
    meta["status"] = ("WORKING, derived from v0_7 by the successor's deltas and cross-checked against "
                      "adversarial_map_v1_7.json, whose drafts a seat that did not draft them judges (K258).")
    meta["phases_contributing"] = dict(collections.Counter(
        t["phase"] for b in reg["bedrocks"] for f in b["facets"] for t in f["tributaries"]))
    meta["changes_from_v0_7"] = changes + ["relation drafted: %s" % x for x in relations]
    meta["parity_with_v0_7"] = ("Asserted before the write: the bedrocks that moved are exactly those the successor's rows "
                                "reach (%s); every (d) in adversarial_map_v1_7.json is a tributary here with the map's "
                                "terminus_routing and novel flag; no (d) left; no adjacency pair is undeclared."
                                % ", ".join(sorted(touched)))
    meta["predecessor"] = {"artifact": "honest_residuals_register_v0_7.json", "md5": V0_7_MD5,
                           "note": "stays byte-identical on disk; v0_8 supersedes it, it is not edited"}
    adj = dict(meta["adjacency"])
    adj["candidates_derived"] = len(cands)
    adj["declared_relations"] = len(declared)
    adj["detected_and_declared"] = sorted("%s+%s" % p for p in sorted(set(cands) & declared))
    adj["declared_but_undetected"] = sorted("%s+%s" % p for p in sorted(declared - set(cands)))
    adj["added_at_L7"] = sorted("%s+%s" % tuple(sorted((r.split()[0], r.split()[2]))) for r in relations)
    meta["adjacency"] = adj
    out = json.dumps({"meta": meta, "audit": v7["audit"], "bedrocks": reg["bedrocks"]}, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), md5b(b)))
    print("  %d change(s), %d relation(s) drafted; %d (d)s cross-checked; bedrocks moved %s; adjacency %d candidates, "
          "0 undeclared" % (len(changes), len(relations), len(want), moved, len(cands)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
