#!/usr/bin/env python3
"""honest_residuals_register_v0_6.json -- v0_5 plus exactly the deltas Josiah's word ruled (L4b, 2026-09-26).

v0_6 is DERIVED FROM v0_5 BY DECLARED DELTAS, then CROSS-CHECKED AGAINST THE MAP, rather than rebuilt from
scratch, because every other bedrock and tributary is already judged (gate2, J-046..J-048) and must not move:
  i.   J-052, on his word: the K349 pair is re-declared in the definitional direction. "A conditions B: A's
       resolution changes the FORCE of B's open question." The pair was stored as "HR-14 conditions HR-11",
       and its own note says HR-11's resolution moves HR-14. It now reads HR-11 conditions HR-14. Its note is
       carried verbatim, with one forward sentence. The substance does not move.
  ii.  The note on L4's own relation, HR-11 conditions HR-02, drops its "Same shape as HR-14 conditions HR-11."
       for the corrected name (J-046's carry).
  iii. J-050, on his word: three HR-06 tributaries (#25, #59, #62) take the terminus_routing adversarial_map_v1_5
       gives them, which names the path the line takes and the birth certificate as such.
Everything else must equal v0_5. The build then cross-checks the result against v1_5 (every (d) entry is a
tributary; the terminus_routing and novel flag on each are v1_5's) and re-runs the adjacency signals, which
must find no undeclared pair.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, hashlib, itertools, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_6.json")

V0_5 = os.path.join(STAGE, "honest_residuals_register_v0_5.json")
V0_5_MD5 = "0c29e3bd286ef9f5e6ddead7019f7ed3"
ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_5.json")
RELATION_KINDS = ("depends_on", "stronger_than", "sibling_of", "independent_of", "conditions")
FORWARD = (" Re-declared at L4b as HR-11 conditions HR-14, on Josiah's word (2026-09-26) adopting gate2's J-052: "
           "the definition runs from the bedrock whose resolution moves the other's force, and this note says that "
           "is HR-11. Stored on HR-14 until then; the substance is unchanged.")
OLD_TAIL = "Same shape as HR-14 conditions HR-11."
NEW_TAIL = "Same shape as HR-11 conditions HR-14, the K349 pair as re-declared on Josiah's word (J-052)."
ROUTING_FIX = (25, 59, 62)


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main():
    fail = []
    raw = open(V0_5, "rb").read()
    assert md5b(raw) == V0_5_MD5, "BASE GUARD: register v0_5 is %s" % md5b(raw)
    v5 = json.loads(raw.decode("utf-8"))
    reg = json.loads(raw.decode("utf-8"))
    araw = open(ASSEMBLY, "rb").read()
    amap = json.loads(araw.decode("utf-8"))
    B = {b["bedrock_id"]: b for b in reg["bedrocks"]}

    # ---- i. the K349 pair, re-declared
    h14 = [r for r in B["HR-14"]["relations"] if r["kind"] == "conditions" and r["to"] == "HR-11"]
    if len(h14) != 1:
        fail.append("HR-14 carries %d 'conditions HR-11' relations, expected exactly 1" % len(h14))
    else:
        B["HR-14"]["relations"] = [r for r in B["HR-14"]["relations"] if r is not h14[0]]
        B["HR-11"]["relations"].append({"kind": "conditions", "to": "HR-14", "note": h14[0]["note"] + FORWARD})
    # ---- ii. L4's note on HR-11 conditions HR-02
    h02 = [r for r in B["HR-11"]["relations"] if r["kind"] == "conditions" and r["to"] == "HR-02"]
    if len(h02) != 1 or h02[0]["note"].count(OLD_TAIL) != 1:
        fail.append("HR-11 conditions HR-02 is not the L4 relation with the old name in its note")
    else:
        h02[0]["note"] = h02[0]["note"].replace(OLD_TAIL, NEW_TAIL)
    # ---- iii. the three terminus_routing fixes, read from the map
    fixed = {}
    for e in amap["entries"]:
        rd = e["provenance"].get("redrafted")
        am = e["provenance"].get("amended")
        if rd and rd["kind"] == "terminus_routing" and am and am["r1_n"] in ROUTING_FIX:
            fixed[(e["target_id"], e["target_locus"], e["target_anchor"])] = e["routing"]["residue"]["terminus_routing"]
    if len(fixed) != len(ROUTING_FIX):
        fail.append("the map carries %d terminus_routing redrafts for %s" % (len(fixed), list(ROUTING_FIX)))
    hits = 0
    for f in B["HR-06"]["facets"]:
        for t in f["tributaries"]:
            k = (t["node"], t["locus"], t["anchor"])
            if k in fixed:
                t["terminus_routing"] = fixed[k]
                hits += 1
    if hits != len(ROUTING_FIX):
        fail.append("%d HR-06 tributaries matched the routing fixes, expected %d" % (hits, len(ROUTING_FIX)))

    # ---- cross-check against the map: every (d) is a tributary, with the map's routing and novel flag
    want = {}
    for e in amap["entries"]:
        if e["class"] == "d":
            r = e["routing"]["residue"]
            want[(e["target_id"], e["target_locus"], e["target_anchor"])] = (r["terminus_routing"], r["novel"])
    got = {}
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                got[(t["node"], t["locus"], t["anchor"])] = (t["terminus_routing"], t["novel"])
    if got != want:
        miss = sorted(set(want) ^ set(got))[:3]
        diff = sorted(k for k in set(want) & set(got) if want[k] != got[k])[:3]
        fail.append("register and map disagree: membership %s, fields %s" % (miss, diff))

    # ---- parity with v0_5: only the declared deltas moved
    old = {b["bedrock_id"]: b for b in v5["bedrocks"]}
    moved = sorted(bid for bid in B if json.dumps(B[bid], sort_keys=True) != json.dumps(old[bid], sort_keys=True))
    if moved != ["HR-06", "HR-11", "HR-14"]:
        fail.append("bedrocks that moved: %s; the declared deltas move HR-06, HR-11 and HR-14 only" % moved)
    for bid in moved:
        for k in ("name", "alias", "gloss", "registered_in", "birth_certificate", "tributary_count", "facet_count"):
            if B[bid][k] != old[bid][k]:
                fail.append("%s.%s moved" % (bid, k))
    six_old = [t for f in old["HR-06"]["facets"] for t in f["tributaries"]]
    six_new = [t for f in B["HR-06"]["facets"] for t in f["tributaries"]]
    changed6 = sum(1 for a, b in zip(six_old, six_new) if a != b)
    if len(six_old) != len(six_new) or changed6 != len(ROUTING_FIX) or B["HR-06"]["relations"] != old["HR-06"]["relations"]:
        fail.append("HR-06 moved outside its three tributaries' terminus_routing")

    # ---- adjacency: the two signals, and no undeclared pair
    alias = {}
    for b in reg["bedrocks"]:
        keys = [b["name"].lower()]
        if b["alias"]:
            keys += [a.strip().lower() for a in re.split(r"[/]", b["alias"])]
        alias[b["bedrock_id"]] = keys
    cands = collections.defaultdict(set)
    bynode = collections.defaultdict(set)
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                low = t["terminus_routing"].lower()
                for other, keys in alias.items():
                    if other != b["bedrock_id"] and (other.lower() in low or any(
                            k in low or k.replace(" ", "-") in low for k in keys)):
                        cands[tuple(sorted((b["bedrock_id"], other)))].add("terminus names")
                bynode[t["node"]].add(b["bedrock_id"])
    for node, bids in bynode.items():
        for a, b_ in itertools.combinations(sorted(bids), 2):
            cands[(a, b_)].add("shared node %s" % node)
    declared = set()
    for b in reg["bedrocks"]:
        for r in b["relations"]:
            declared.add(tuple(sorted((b["bedrock_id"], r["to"]))))
            if r["kind"] not in RELATION_KINDS:
                fail.append("%s declares kind %r" % (b["bedrock_id"], r["kind"]))
    for pair in sorted(set(cands) - declared):
        fail.append("UNDECLARED ADJACENCY: %s+%s" % pair)
    hand_only = sorted(declared - set(cands))

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1

    m5 = v5["meta"]
    meta = dict(m5)
    meta["artifact"] = "honest_residuals_register_v0_6.json"
    meta["source"] = {"artifact": amap["meta"]["artifact"], "md5": md5b(araw), "entries": amap["meta"]["entries"]}
    meta["status"] = ("WORKING, derived from v0_5 by the deltas Josiah's word ruled and cross-checked against "
                      "adversarial_map_v1_5.json, whose six redrafts a seat that did not draft them judges (K258).")
    meta["changes_from_v0_5"] = [
        "J-052: the K349 pair re-declared as HR-11 conditions HR-14 (it was stored on HR-14 pointing at HR-11); "
        "its note carried verbatim with one forward sentence; nothing substantive moves",
        "HR-11 conditions HR-02 (L4's relation): the note's reference to the K349 pair uses the corrected name",
        "J-050: #25, #59 and #62's tributaries on HR-06 name the path their line takes; the birth certificate is "
        "named as such",
    ]
    meta["parity_with_v0_5"] = ("Asserted before the write: HR-06, HR-11 and HR-14 moved and no other bedrock did; "
                                "HR-06 only in three tributaries' terminus_routing; HR-11 and HR-14 only in their "
                                "relations. Every (d) in adversarial_map_v1_5.json is a tributary here with the "
                                "map's terminus_routing and novel flag, and no adjacency pair is undeclared.")
    meta["predecessor"] = {"artifact": "honest_residuals_register_v0_5.json", "md5": V0_5_MD5,
                           "note": "stays byte-identical on disk; v0_6 supersedes it, it is not edited"}
    adj = dict(m5["adjacency"])
    adj["candidates_derived"] = len(cands)
    adj["declared_relations"] = len(declared)
    adj["detected_and_declared"] = sorted("%s+%s" % p for p in sorted(set(cands) & declared))
    adj["declared_but_undetected"] = sorted("%s+%s" % p for p in hand_only)
    adj["vocabulary_gap"] = dict(adj["vocabulary_gap"],
                                 status=("CLOSED at K349 by ratification; declared as a `conditions` relation, "
                                         "stored on HR-14 until L4b and on HR-11 since (J-052, Josiah's word)"))
    meta["adjacency"] = adj
    audit = list(v5["audit"]) + [dict(
        severity="relation-redeclared-J052", bedrock_id="HR-11+HR-14",
        detail=("The K349 pair was stored against its own definition (\"A conditions B: A's resolution changes the "
                "FORCE of B's open question\") as HR-14 conditions HR-11, while its note says HR-11's resolution "
                "moves HR-14. Found by gate2 (J-052) and re-declared on Josiah's word as HR-11 conditions HR-14. "
                "Canon's relation_vocabulary_K349.first_instance still reads the old name; canon records the "
                "correction forward rather than editing that block."))]
    doc = {"meta": meta, "audit": audit, "bedrocks": reg["bedrocks"]}
    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), md5b(b)))
    print("  moved: HR-06 (3 terminus_routing), HR-11 (+conditions HR-14, note), HR-14 (-conditions HR-11)")
    print("  adjacency: %d candidates, %d declared, 0 undeclared; map cross-check: %d (d)s, all equal"
          % (len(cands), len(declared), len(want)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
