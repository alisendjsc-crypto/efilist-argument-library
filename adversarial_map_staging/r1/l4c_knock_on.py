#!/usr/bin/env python3
"""l4c_knock_on.py -- what #46's (d) in v1_6 does to the (a) entries it did not touch (L4c, 2026-09-26).

l4_knock_on.py measured v1_4 against v1_3. This measures v1_6 against v1_5 with the SAME collision
function, imported rather than re-implemented (the K344 hazard), after first requiring that
l4_knock_on.measure() still reproduces its committed record byte for byte. It lists every (a) left in
v1_6 whose collision set gained an entry that v1_5 did not have. It rules nothing: a listed entry keeps
its R1 verdict and is read again (the judge's knock-on reading) before its card ships.

  python3 l4c_knock_on.py            # measure, print, write l4c_knock_on_v0_1.json
  python3 l4c_knock_on.py --check    # measure, compare with the committed record
  python3 l4c_knock_on.py --self-test  # a probe (a) routed into #46's node must see exactly #46's new (d)

Repo-relative. Deterministic.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
REPO = os.path.dirname(STAGE)
sys.path.insert(0, HERE)
import l4_knock_on as K   # noqa: E402
import pinned             # noqa: E402

V1_5 = os.path.join(STAGE, "adversarial_map_v1_5.json")
V1_6 = os.path.join(STAGE, "adversarial_map_v1_6.json")
RULINGS_MD5 = "d829437e938a8b9dded5cb8cbaa26b74"
RECORD = os.path.join(HERE, "l4c_knock_on_v0_1.json")


def key(x):
    return (x["target_id"], x["target_locus"], x["target_anchor"], x["class"])


def measure():
    prior = json.dumps(K.measure(), indent=2, ensure_ascii=False) + "\n"
    if prior != open(K.RECORD, encoding="utf-8").read():
        sys.exit("REFUSED: l4_knock_on.measure() no longer reproduces l4_knock_on_v0_1.json")
    ev = K.load(K.EVID)["entries"]
    m5, m6 = K.load(V1_5)["entries"], K.load(V1_6)["entries"]
    rul = json.loads(pinned.bytes_at(REPO, "adversarial_map_staging/r1/R1_rulings.json", RULINGS_MD5)
                     .decode("utf-8"))["rows"]
    sup = {r["supersedes"] for r in rul if r.get("supersedes")}
    cur = {r["n"]: r for r in rul if r["row"] not in sup}
    i5 = {(x["target_id"], x["target_anchor"]): x for x in m5}
    i6 = {(x["target_id"], x["target_anchor"]): x for x in m6}
    left = []
    for e in ev:
        k = (e["target_id"], e["target_anchor"])
        if i6[k]["class"] == "a":
            if i5[k]["class"] != "a" or i5[k]["routing"] != i6[k]["routing"]:
                sys.exit("REFUSED: #%d is an (a) in v1_6 whose v1_5 class or routing differs" % e["n"])
            left.append((e["n"], e["target_id"], i6[k]["routing"]["answered_by"]))
    c5, c6 = K.collisions(m5, left), K.collisions(m6, left)
    rows = []
    for n, own, _refs in left:
        before = {key(y) for y in c5[n]}
        new = {key(x): x for x in c6[n] if key(x) not in before}
        if not new:
            continue
        x = i6[[(e["target_id"], e["target_anchor"]) for e in ev if e["n"] == n][0]]
        rows.append({"n": n, "target": "%s#%s" % (own, x["target_locus"]), "r1_verdict": cur[n]["verdict"],
                     "r1_row": cur[n]["row"],
                     "new_collisions": sorted("%s (%s, from #%d)" % (K.tag(y), y["class"], y["provenance"]["amended"]["r1_n"])
                                              for y in new.values())})
    raw5, raw6 = open(V1_5, "rb").read(), open(V1_6, "rb").read()
    return {
        "artifact": "l4c_knock_on_v0_1.json",
        "instrument": "adversarial_map_staging/r1/l4c_knock_on.py",
        "rule": "collision rule v0_2, l4_knock_on.collisions imported; l4_knock_on.measure() reproduced its "
                "committed record first",
        "maps": {"before": {"file": "adversarial_map_staging/adversarial_map_v1_5.json", "md5": hashlib.md5(raw5).hexdigest()},
                 "after": {"file": "adversarial_map_staging/adversarial_map_v1_6.json", "md5": hashlib.md5(raw6).hexdigest()}},
        "rulings_md5": RULINGS_MD5,
        "what_it_means": ("An entry listed here met a (b) or (d) in v1_6 that v1_5 did not have. Its R1 verdict "
                          "stands; the collision rule says it is read again before its card ships."),
        "a_entries_left_in_v1_6": len(left),
        "holds_newly_collided": [r["n"] for r in rows if r["r1_verdict"] == "HOLDS"],
        "rows": rows,
    }


def self_test():
    """The measure found nothing; prove it can find something. A probe (a) routed to red-button-repugnant#long
    must gain exactly one collision between v1_5 and v1_6: #46's (d)."""
    m5, m6 = K.load(V1_5)["entries"], K.load(V1_6)["entries"]
    d46 = [x for x in m6 if x["provenance"].get("amended", {}).get("at") == "L4c"]
    probe = [(0, "probe-node", ["red-button-repugnant#long"])]
    c5, c6 = K.collisions(m5, probe), K.collisions(m6, probe)
    new = {key(x) for x in c6[0]} - {key(y) for y in c5[0]}
    ok = len(d46) == 1 and new == {key(d46[0])}
    print("SELF-TEST: a probe (a) routed to red-button-repugnant#long gains %s: %s"
          % (sorted(new), "PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv:
        return self_test()
    rec = measure()
    s = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    for r in rec["rows"]:
        print("#%-3d %-52s %-5s %s" % (r["n"], r["target"], r["r1_verdict"], "; ".join(r["new_collisions"])))
    print("(a) entries left in v1_6: %d; HOLDS newly collided by #46's (d): %d (%s)"
          % (rec["a_entries_left_in_v1_6"], len(rec["holds_newly_collided"]),
             ", ".join("#%d" % n for n in rec["holds_newly_collided"]) or "none"))
    if "--check" in sys.argv:
        same = open(RECORD, encoding="utf-8").read() == s
        print("KNOCK-ON RECORD: %s" % ("matches the committed record" if same else "DIFFERS"))
        return 0 if same else 1
    open(RECORD, "w", encoding="utf-8").write(s)
    print("wrote %s" % os.path.basename(RECORD))
    return 0


if __name__ == "__main__":
    sys.exit(main())
