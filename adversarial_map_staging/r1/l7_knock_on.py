#!/usr/bin/env python3
"""l7_knock_on.py -- the knock-on as a build control for the successor map (L7, 2026-09-26; gate2's U-064).

gate2's recommendation at U-064, adopted: "a successor's controls run the knock-on after the drafts apply, and a stands
row reads every newly collided entry." L7 measured before drafting; this measures after. For every (a) in the
successor (adversarial_map_v1_8.json) it computes the (b)/(d)s the collision rule v0_2 sees for it (l4_knock_on.collisions,
imported at its pinned bytes, as gate2's reading imports it), subtracts those it saw in v1_6, and lists every (a) that
gained one. Each must be READ: by a gate2 `knock_on` row naming its entry (L7_successor_drafts_judgments.json, pinned),
or by an L7 row naming it. An unread newly collided (a) fails the check.

  python3 l7_knock_on.py            # write l7_knock_on_v0_1.json
  python3 l7_knock_on.py --check    # recompute; compare with the committed record byte for byte
  python3 l7_knock_on.py --self-test [--emit <path>]   # the unmutated control first, then a read removed

Repo-relative. Writes only its record. Reads everything at a pin. Deterministic.
"""
import copy, hashlib, json, os, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
RECORD = os.path.join(HERE, "l7_knock_on_v0_1.json")
PIN = {
    "v1_6": (S + "/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "successor": (S + "/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827"),
    "judgment": (R + "/L7_successor_drafts_judgments.json", "bd3b4e89f25e7f874f5aa553b998fe0d"),
    "drafts": (R + "/L7_successor_drafts.json", "370e7d02457314e10d6211f95d5ae8c0"),
    "tool": (R + "/l4_knock_on.py", "66022fa8e9ba7ad3ff26e42aee5b0b1c"),
}


def md5b(b):
    return hashlib.md5(b).hexdigest()


def load_inputs():
    raw = {k: pinned.bytes_at(REPO, rel, m) for k, (rel, m) in PIN.items()}
    tool = types.ModuleType("l4_knock_on_pinned")
    tool.__file__ = os.path.join(REPO, PIN["tool"][0])
    exec(compile(raw.pop("tool").decode("utf-8"), tool.__file__, "exec"), tool.__dict__)
    return {k: json.loads(v.decode("utf-8")) for k, v in raw.items()}, tool


def key(x):
    return (x["target_id"], x["target_locus"], x["target_anchor"])


def measure(inp, K):
    fail = []
    e6, e8 = inp["v1_6"]["entries"], inp["successor"]["entries"]
    i6 = {key(x): j for j, x in enumerate(e6)}
    i8 = {key(x): j for j, x in enumerate(e8)}
    reads = {}
    for r in inp["judgment"]["rows"]:
        if r.get("kind") == "knock_on":
            reads.setdefault(r["i"], []).append(r["id"])
    sup = {r["supersedes"] for r in inp["drafts"]["rows"] if r.get("supersedes")}
    rows = [r for r in inp["drafts"]["rows"] if r["id"] not in sup]
    own = {}
    for r in rows:
        if r.get("entry"):
            own.setdefault(r["entry"]["i"], []).append(r["id"])
    out, n_a = [], 0
    for i, x in enumerate(e8):
        if x["class"] != "a":
            continue
        n_a += 1
        c8 = {i8[key(y)] for y in K.collisions(e8, [(i, x["target_id"], x["routing"]["answered_by"])])[i]}
        before = set()
        j6 = i6.get(key(x))
        if j6 is None and "successor_L7" in x["provenance"]:
            j6 = i if i < len(e6) else None
        if j6 is not None and e6[j6]["class"] == "a":
            c6 = K.collisions(e6, [(j6, e6[j6]["target_id"], e6[j6]["routing"]["answered_by"])])[j6]
            before = {i8[key(y)] for y in c6 if key(y) in i8}
        new = sorted(c8 - before)
        if not new:
            continue
        read_by = sorted(reads.get(i, [])) + sorted(own.get(i, []))
        item = {"i": i, "target": "%s#%s" % (x["target_id"], x["target_locus"]), "anchor": x["target_anchor"],
                "new_collisions": [{"i": j, "at": "%s#%s" % (e8[j]["target_id"], e8[j]["target_locus"]),
                                    "class": e8[j]["class"]} for j in new],
                "read_by": read_by}
        out.append(item)
        if not read_by:
            fail.append("UNREAD: (a) %d %s gained %d collision(s) and no row reads it" % (i, item["target"], len(new)))
    return fail, {"a_entries": n_a, "newly_collided": out}


def build(inp, K):
    fail, m = measure(inp, K)
    if fail:
        return fail, None
    rec = {"artifact": "l7_knock_on_v0_1.json", "instrument": R + "/l7_knock_on.py",
           "adopts": "gate2's U-064: a successor's controls run the knock-on after the drafts apply",
           "rule": "collision rule v0_2, l4_knock_on.collisions at its pinned bytes, the successor against v1_6",
           "pinned": {k: {"file": rel, "md5": md5} for k, (rel, md5) in PIN.items()},
           "a_entries_in_successor": m["a_entries"], "newly_collided": len(m["newly_collided"]),
           "read_by_gate2": sum(1 for x in m["newly_collided"] if any(r.startswith("U-") for r in x["read_by"])),
           "items": m["newly_collided"]}
    return [], rec


def serialize(rec):
    return json.dumps(rec, indent=2, ensure_ascii=False) + "\n"


def self_test(emit=None):
    base, K = load_inputs()
    results = []

    def run(name, mut, expect):
        inp = copy.deepcopy(base)
        if mut:
            mut(inp)
        fail, rec = build(inp, K)
        ok = (not fail and serialize(rec) == open(RECORD, encoding="utf-8").read()) if expect is None \
            else any(expect in f for f in fail)
        results.append({"control": name, "expect": "reproduces the committed record" if expect is None
                        else "refuses, naming %r" % expect, "as_expected": ok})
        print("%-64s %s" % (name, "as expected" if ok else "UNEXPECTED"))
        return ok

    def drop_read(i):
        def m(inp):
            inp["judgment"]["rows"] = [r for r in inp["judgment"]["rows"] if not (r.get("kind") == "knock_on" and r["i"] == i)]
        return m

    def new_flag(inp):
        # a (b) filed at the answering locus of an (a) no row reads: entry 63, next-person-cure-cancer#long -> #medium
        e = copy.deepcopy([x for x in inp["successor"]["entries"] if x["class"] == "b"][0])
        e.update(target_id="next-person-cure-cancer", target_locus="medium", target_anchor="a control anchor")
        inp["successor"]["entries"].append(e)

    if not run("C0 unmutated: reproduces the committed record", None, None):
        print("SELF-TEST: the unmutated control failed; nothing after it means anything")
        return 1
    run("C1 gate2's read of #19 removed (U-059)", drop_read(30), "UNREAD: (a) 30")
    run("C2 gate2's read of #68 removed (U-062)", drop_read(136), "UNREAD: (a) 136")
    run("C3 a new (b) at an unread (a)'s answering locus (entry 63)", new_flag, "UNREAD: (a) 63")
    good = sum(1 for r in results if r["as_expected"])
    rec = {"artifact": os.path.basename(emit) if emit else "l7_knock_on_control_v0_1.json",
           "instrument": R + "/l7_knock_on.py --self-test",
           "record": {"file": R + "/l7_knock_on_v0_1.json", "md5": md5b(open(RECORD, "rb").read())},
           "result": "%d of %d controls as expected, the unmutated first" % (good, len(results)), "controls": results}
    if emit:
        open(emit, "w", encoding="utf-8").write(serialize(rec))
    print("SELF-TEST: %d of %d controls as expected" % (good, len(results)))
    return 0 if good == len(results) else 1


def main():
    if "--self-test" in sys.argv:
        return self_test(sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None)
    inp, K = load_inputs()
    fail, rec = build(inp, K)
    if fail:
        print("REFUSED -- %d failure(s):" % len(fail))
        for f in fail:
            print("  " + f)
        return 1
    s = serialize(rec)
    if "--check" in sys.argv:
        same = open(RECORD, encoding="utf-8").read() == s
        print("KNOCK-ON RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        return 0 if same else 1
    open(RECORD, "w", encoding="utf-8").write(s)
    print("WROTE %s  %d B  md5 %s" % (os.path.basename(RECORD), len(s.encode("utf-8")), md5b(s.encode("utf-8"))))
    print("  (a)s %d | newly collided %d | read by gate2 %d" % (rec["a_entries_in_successor"], rec["newly_collided"],
                                                              rec["read_by_gate2"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
