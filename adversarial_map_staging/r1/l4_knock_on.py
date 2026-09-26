#!/usr/bin/env python3
"""l4_knock_on.py -- what L4's drafts do to the (a) entries they did not touch (L4, 2026-09-25).

The collision rule (v0_2, canon adversarial_map.collision_rule_WIDENED_L3) lists every (a) whose
answering locus, own node, or an answering node's other slot carries a (b) or (d), and says the list
must be empty or ruled before any (a) card ships. R1's HOLDS were ruled against adversarial_map_v1_3.json.
The drafting pass turns (a)s into (d)s and (b)s ON THOSE SAME NODES, so an entry that held against v1_3
can meet a (b) or (d) in v1_4 that did not exist when it was ruled. This lists every such case. It rules
nothing: an entry listed here keeps its R1 verdict and is read again before its card ships.

The rule is re-applied here to a map other than the one r1_collision_list.py reads (that tool is pinned
to v1_3 through the rulings file). A re-implementation can disagree with the instrument (the K344 hazard),
so this one must first reproduce the committed v0_2 list's collided set on v1_3 exactly, or it refuses.

  python3 l4_knock_on.py            # measure, print, write l4_knock_on_v0_1.json
  python3 l4_knock_on.py --check    # measure, compare with the committed record

Repo-relative. Deterministic.
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
V1_3 = os.path.join(STAGE, "adversarial_map_v1_3.json")
V1_4 = os.path.join(STAGE, "adversarial_map_v1_4.json")
EVID = os.path.join(HERE, "R1_evidence_2026-09-19.json")
RULINGS = os.path.join(HERE, "R1_rulings.json")
LIST_V0_2 = os.path.join(HERE, "r1_collision_list_v0_2.json")
RECORD = os.path.join(HERE, "l4_knock_on_v0_1.json")


def load(p):
    return json.load(open(p, encoding="utf-8"))


def collisions(entries, a_entries):
    """(a) n -> the (b)/(d) entries the v0_2 rule sees for it, from `entries`."""
    flags = collections.defaultdict(list)
    for x in entries:
        if x["class"] in ("b", "d"):
            flags[x["target_id"]].append(x)
    out = {}
    for n, own, refs in a_entries:
        hits = []
        for ref in refs:
            node = ref.partition("#")[0]
            hits += [x for x in flags.get(node, []) if x["target_id"] != own]
        hits += flags.get(own, [])
        out[n] = hits
    return out


def tag(x):
    return "%s#%s" % (x["target_id"], x["target_locus"])


def measure():
    ev = load(EVID)["entries"]
    m3, m4 = load(V1_3)["entries"], load(V1_4)["entries"]
    last = {}
    for r in load(RULINGS)["rows"]:
        last[r["n"]] = r
    # 1. agreement with the instrument, on the map the instrument reads
    c3 = collisions(m3, [(e["n"], e["target_id"], e["answered_by"]) for e in ev])
    mine = sorted(n for n, h in c3.items() if h)
    theirs = sorted(i["n"] for i in load(LIST_V0_2)["items"] if i["collided"])
    if mine != theirs:
        sys.exit("REFUSED: this re-implementation collides %d entries on v1_3, the committed v0_2 list %d"
                 % (len(mine), len(theirs)))
    # 2. the (a)s left in v1_4, with the routing v1_4 gives them
    idx = {(x["target_id"], x["target_anchor"]): x for x in m4}
    left = []
    for e in ev:
        x = idx[(e["target_id"], e["target_anchor"])]
        if x["class"] == "a":
            left.append((e["n"], e["target_id"], x["routing"]["answered_by"]))
    c4 = collisions(m4, left)
    rows = []
    for n, own, refs in left:
        new = [x for x in c4[n] if "amended" in x["provenance"]]
        if not new:
            continue
        x = idx[[(e["target_id"], e["target_anchor"]) for e in ev if e["n"] == n][0]]
        rows.append({"n": n, "target": "%s#%s" % (own, x["target_locus"]), "r1_verdict": last[n]["verdict"],
                     "r1_row": last[n]["row"],
                     "new_collisions": sorted({"%s (%s, from #%d)" % (tag(y), y["class"],
                                                                      y["provenance"]["amended"]["r1_n"]) for y in new})})
    holds = [r for r in rows if r["r1_verdict"] == "HOLDS"]
    return {
        "artifact": "l4_knock_on_v0_1.json",
        "instrument": "adversarial_map_staging/r1/l4_knock_on.py",
        "rule": "collision rule v0_2, re-applied to adversarial_map_v1_4.json; agreement with the committed "
                "v0_2 list on v1_3 asserted first (%d collided, same set)" % len(mine),
        "what_it_means": ("An entry listed here met a (b) or (d) in v1_4 that did not exist when R1 ruled it on v1_3. "
                          "Its R1 verdict stands; the collision rule says it is read again before its card ships."),
        "a_entries_left_in_v1_4": len(left),
        "holds_newly_collided": [r["n"] for r in holds],
        "rows": rows,
    }


def main():
    rec = measure()
    s = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    for r in rec["rows"]:
        print("#%-3d %-52s %-5s %s" % (r["n"], r["target"], r["r1_verdict"], "; ".join(r["new_collisions"])))
    print("HOLDS newly collided by L4's drafts: %d (%s)" % (len(rec["holds_newly_collided"]),
                                                          ", ".join("#%d" % n for n in rec["holds_newly_collided"])))
    if "--check" in sys.argv:
        same = open(RECORD, encoding="utf-8").read() == s
        print("KNOCK-ON RECORD: %s" % ("matches the committed record" if same else "DIFFERS"))
        return 0 if same else 1
    open(RECORD, "w", encoding="utf-8").write(s)
    print("wrote %s" % os.path.basename(RECORD))
    return 0


if __name__ == "__main__":
    sys.exit(main())
