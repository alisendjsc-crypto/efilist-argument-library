#!/usr/bin/env python3
"""r1_collision_list_l7.py -- the collision list, read against the evidence each ruling names (L7, 2026-09-26).

WHY. r1_collision_list.py (cb3cd460, kept byte-identical) lists v1_3's 69 (a) entries with the LATEST R1 row for
each, whatever evidence that row was ruled on. From R1-071 on, rows re-rule #11, #22, #32 and #50 as they stand in
the successor map v1_8 and rule n=70, the (a) at self-defeating#long, which v1_3 does not hold (it is a (b) there).
Read on v1_3's routes, #11 would be reported against a route it no longer has (gate2, U2-023, condition 2).

WHAT. The same list, by the same code, twice:
  A. v1_3: R1's evidence and map, with only the rows ruled on R1's evidence (evidence_md5 == the evidence file's);
  B. the successor: the L7 addendum (R1_evidence_L7_addendum.json) and the map it pins (v1_8), with only the rows
     ruled on the addendum.
r1_collision_list.py is imported at its pinned bytes, never reimplemented; each part runs its build() in a scratch
root holding exactly that part's rulings, evidence, map and canon. A row naming neither evidence is a failure.
The rulings file is read at the md5 this file pins, so a later row cannot turn the check RED: a later ruling is a
new version of this list.

  python3 r1_collision_list_l7.py             # check and print both summaries; exits 1 when either part's rule breaks
  python3 r1_collision_list_l7.py --write     # also write r1_collision_list_l7_v0_1.json
  python3 r1_collision_list_l7.py --check     # rebuild; compare with the committed record byte for byte
  python3 r1_collision_list_l7.py --self-test [--emit <path>]   # controls; the unmutated control first

Repo-relative. Owns its scratch. Deterministic.
"""
import glob, hashlib, json, os, shutil, sys, tempfile, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

R = "adversarial_map_staging/r1"
RULINGS = (R + "/R1_rulings.json", "f7d02b16f6837e53033b3c7fb68332a9")
RCL = (R + "/r1_collision_list.py", "cb3cd460a6f72a47ac31232eb4287240")
ADDENDUM = (R + "/R1_evidence_L7_addendum.json", "ba55917f971520743773f0eb6fb518ea")
RECORD = os.path.join(HERE, "r1_collision_list_l7_v0_1.json")
RULE = "v0_2"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def load_rcl():
    src = pinned.bytes_at(REPO, *RCL).decode("utf-8")
    mod = types.ModuleType("r1_collision_list_pinned")
    mod.__file__ = os.path.join(REPO, RCL[0])
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def canon_path(root):
    cs = sorted(glob.glob(os.path.join(root, "project_canon_v38_*.json")))
    if len(cs) != 1:
        raise SystemExit("REFUSED: expected exactly one project_canon_v38_*.json in %s, found %d" % (root, len(cs)))
    return cs[0]


def part(K, tmp, name, header, rows, files, canon):
    """Run the pinned r1_collision_list.build() on a scratch root holding exactly these inputs."""
    d = os.path.join(tmp, name)
    for rel, b in files:
        os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
        open(os.path.join(d, rel), "wb").write(b)
    os.makedirs(os.path.join(d, R), exist_ok=True)
    open(os.path.join(d, RULINGS[0]), "w", encoding="utf-8").write(json.dumps(dict(header, rows=rows), ensure_ascii=False))
    shutil.copyfile(canon, os.path.join(d, os.path.basename(canon)))
    return K.build(d, RULE)


def build(root=REPO, rulings_bytes=None):
    K = load_rcl()
    fails = []
    rb = rulings_bytes if rulings_bytes is not None else pinned.bytes_at(REPO, *RULINGS)
    doc = json.loads(rb.decode("utf-8"))
    header = {k: v for k, v in doc.items() if k != "rows"}
    ev_md5 = doc["evidence"]["md5"]
    rd = lambda rel: open(os.path.join(root, rel), "rb").read()
    add_b = rd(ADDENDUM[0])
    if md5b(add_b) != ADDENDUM[1]:
        fails.append("referent moved: %s is %s, pinned %s" % (ADDENDUM[0], md5b(add_b), ADDENDUM[1]))
    add = json.loads(add_b.decode("utf-8"))
    rows_ev = [r for r in doc["rows"] if r["evidence_md5"] == ev_md5]
    rows_add = [r for r in doc["rows"] if r["evidence_md5"] == ADDENDUM[1]]
    other = [r["row"] for r in doc["rows"] if r["evidence_md5"] not in (ev_md5, ADDENDUM[1])]
    if other:
        fails.append("rows naming neither R1's evidence nor the addendum: %s" % ", ".join(other))
    canon = canon_path(root)
    tmp = tempfile.mkdtemp(prefix="r1coll_l7_")
    try:
        fa, ra = part(K, tmp, "v1_3", header, rows_ev,
                      [(doc["evidence"]["file"], rd(doc["evidence"]["file"])), (doc["map"]["file"], rd(doc["map"]["file"]))],
                      canon)
        mp = add["inputs"]["map"]
        hb = {"evidence": {"file": ADDENDUM[0], "md5": ADDENDUM[1]}, "map": {"file": mp["file"], "md5": mp["md5"]}}
        fb, rb2 = part(K, tmp, "successor", hb, rows_add, [(ADDENDUM[0], add_b), (mp["file"], rd(mp["file"]))], canon)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    fails += ["v1_3: " + f for f in fa] + ["successor: " + f for f in fb]
    rec = {
        "artifact": os.path.basename(RECORD),
        "instrument": R + "/r1_collision_list_l7.py",
        "rule": ra["rule"],
        "why": ("From R1-071 a row may be ruled on the L7 addendum (the successor v1_8) instead of R1's evidence (v1_3). "
                "Each part reads only the rows ruled on its own evidence (gate2 U2-023, condition 2)."),
        "inputs": {"rulings": {"file": RULINGS[0], "md5": md5b(rb)},
                   "r1_collision_list": {"file": RCL[0], "md5": RCL[1], "imported_at_pinned_bytes": True},
                   "addendum": {"file": ADDENDUM[0], "md5": ADDENDUM[1]}, "canon": os.path.basename(canon)},
        "rows": {"ruled_on_R1_evidence": len(rows_ev), "ruled_on_the_addendum": len(rows_add)},
        "v1_3": {"evidence": ra["inputs"]["evidence"], "map": ra["inputs"]["map"], "summary": ra["summary"]},
        "successor": {"evidence": rb2["inputs"]["evidence"], "map": rb2["inputs"]["map"], "summary": rb2["summary"],
                      "items": rb2["items"]},
    }
    return fails, rec


def serialize(rec):
    return json.dumps(rec, indent=1, ensure_ascii=False) + "\n"


def report(fails, rec):
    for key in ("v1_3", "successor"):
        s = rec[key]["summary"]
        print("%-9s (a) %d | ruled %d | collided %d (HOLDS %d, FAILS %d) | ship-eligible %d | blocked %d | unruled %d"
              % (key, s["a_entries"], s["ruled"], s["collided"], s["collided_HOLDS"], s["collided_FAILS"],
                 len(s["ship_eligible"]), sum(len(v) for v in s["blocked_by_shape"].values()), len(s["unruled"])))
    for f in fails:
        print("  FAIL " + f)


def self_test(emit=None):
    results = []
    tmp = tempfile.mkdtemp(prefix="r1coll_l7_st_")
    try:
        rb = pinned.bytes_at(REPO, *RULINGS)
        doc = json.loads(rb.decode("utf-8"))

        def with_rows(fn):
            d = json.loads(rb.decode("utf-8"))
            fn(d)
            return json.dumps(d, ensure_ascii=False).encode("utf-8")

        def staged(mut_rel=None):
            d = os.path.join(tmp, "c%d" % len(results))
            add = json.loads(open(os.path.join(REPO, ADDENDUM[0]), "rb").read())
            for rel in (doc["evidence"]["file"], doc["map"]["file"], ADDENDUM[0], add["inputs"]["map"]["file"]):
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                b = open(os.path.join(REPO, rel), "rb").read()
                if rel == mut_rel:
                    b = b[:-1] + (b"\n" if b[-1:] != b"\n" else b" ")
                open(os.path.join(d, rel), "wb").write(b)
            shutil.copyfile(canon_path(REPO), os.path.join(d, os.path.basename(canon_path(REPO))))
            return d

        add_rows = [r for r in doc["rows"] if r["evidence_md5"] == ADDENDUM[1]]
        first_add = add_rows[0]["row"] if add_rows else None
        controls = [
            ("C0", "unmutated: reproduces the committed record", None, None, None),
            ("C1", "the first row ruled on the addendum removed", None,
             with_rows(lambda d: d["rows"].remove(next(r for r in d["rows"] if r["row"] == first_add))), "successor: #"),
            ("C2", "a row names neither evidence", None,
             with_rows(lambda d: d["rows"][-1].update(evidence_md5="0" * 32)), "naming neither"),
            ("C3", "the addendum moves by one byte", ADDENDUM[0], None, "referent moved: " + ADDENDUM[0]),
            ("C4", "the successor map moves by one byte", "adversarial_map_staging/adversarial_map_v1_8.json", None,
             "successor: referent moved"),
            ("C5", "v1_3 moves by one byte", "adversarial_map_staging/adversarial_map_v1_3.json", None,
             "v1_3: referent moved"),
        ]
        ok_all = True
        for cid, what, mut_rel, mut_rows, want in controls:
            root = staged(mut_rel)
            fails, rec = build(root, mut_rows)
            if want is None:
                good = not fails and serialize(rec) == open(RECORD, encoding="utf-8").read()
            else:
                good = any(want in f for f in fails)
            results.append({"control": cid, "mutation": what, "expected": "reproduces the record" if want is None
                            else "refuses, naming %r" % want, "as_expected": good, "failure_lines": fails[:3]})
            print("%-4s %-52s %s" % (cid, what, "as expected" if good else "UNEXPECTED: %s" % fails[:3]))
            if cid == "C0" and not good:
                print("SELF-TEST: the unmutated control failed; nothing after it means anything")
                return 1
            ok_all &= good
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    good = sum(r["as_expected"] for r in results)
    print("SELF-TEST: %d of %d controls as expected" % (good, len(results)))
    if emit:
        rec = {"artifact": os.path.basename(emit), "instrument": R + "/r1_collision_list_l7.py --self-test",
               "record": {"file": R + "/" + os.path.basename(RECORD), "md5": md5b(open(RECORD, "rb").read())},
               "result": "%d of %d controls as expected, the unmutated first" % (good, len(results)),
               "controls": results}
        open(emit, "w", encoding="utf-8").write(serialize(rec))
    return 0 if ok_all else 1


def main():
    if "--self-test" in sys.argv:
        return self_test(sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None)
    fails, rec = build()
    report(fails, rec)
    s = serialize(rec)
    if "--check" in sys.argv:
        same = open(RECORD, encoding="utf-8").read() == s
        print("COLLISION LIST L7: record %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        return 0 if (same and not fails) else 1
    if "--write" in sys.argv:
        open(RECORD, "w", encoding="utf-8").write(s)
        print("WROTE %s  md5 %s" % (os.path.basename(RECORD), md5b(s.encode("utf-8"))))
    print("COLLISION LIST L7: %s" % ("GREEN" if not fails else "RED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
