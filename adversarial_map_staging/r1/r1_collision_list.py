#!/usr/bin/env python3
"""r1_collision_list.py -- the collision rule adopted at L2, built (L3, 2026-09-25).

The rule, as canon records it (adversarial_map.a_vs_own_record_collision_finding_L2): every (a) whose
answered_by locus or same-node sibling carries a (b) or (d) is listed for reading, and the list must be
empty or ruled before any (a) card ships.

This lists every one of the map's (a) entries with:
  - its collisions: each (b)/(d) at an answering locus, and each (b)/(d) anywhere on its own node;
  - for reading only, each (b)/(d) elsewhere on an answering node (L2's law: contradictions hide there);
  - its R1 ruling (the latest row for it in R1_rulings.json) and, for a FAILS, the failure shape canon
    records as the seat's reading, which is what the drafting pass does with it;
  - its ship status: an (a) card may ship only on a HOLDS; a FAILS goes to the drafting pass by shape;
    an unruled (a) is blocked.

It exits 1 when the rule is broken: a collided (a) with no ruling, or a ruling whose referents moved
(the evidence file or the map no longer at the md5s the rulings file names). Ship status is a report,
not a failure: a blocked card is the rule working.

  python3 r1_collision_list.py                  # check and print the summary
  python3 r1_collision_list.py --emit <dir>     # also write r1_collision_list_v0_1.json and .md
  python3 r1_collision_list.py --self-test [--emit <path>]   # controls; the unmutated control runs first

Repo-relative. Writes nothing unless --emit is given. Deterministic.
"""
import copy, glob, hashlib, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"
NAME = "r1_collision_list_v0_1"


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def load(root, rel):
    return json.load(open(os.path.join(root, rel), encoding="utf-8"))


def shapes_from_canon(root):
    canons = sorted(glob.glob(os.path.join(root, "project_canon_v38_*.json")))
    if len(canons) != 1:
        raise SystemExit("REFUSED: expected exactly one project_canon_v38_*.json, found %d" % len(canons))
    am = json.load(open(canons[0], encoding="utf-8"))["adversarial_map"]
    keys = sorted(k for k in am if k.startswith("R1_progress_L") and "failure_shapes_seat_s_reading" in am[k])
    shapes = am[keys[-1]]["failure_shapes_seat_s_reading"] if keys else {}
    by_n = {}
    for shape, v in shapes.items():
        for n in v["entries"]:
            by_n[n] = shape
    return os.path.basename(canons[0]), by_n, {k: v["means"] for k, v in shapes.items()}


def build(root):
    """Return (fails, report). fails is a list of rule breaches; report is the full list."""
    doc = load(root, RULINGS)
    ev_rel, map_rel = doc["evidence"]["file"], doc["map"]["file"]
    fails = []
    if md5(os.path.join(root, ev_rel)) != doc["evidence"]["md5"]:
        fails.append("referent moved: %s is not at the md5 the rulings file names" % ev_rel)
    if md5(os.path.join(root, map_rel)) != doc["map"]["md5"]:
        fails.append("referent moved: %s is not at the md5 the rulings file names" % map_rel)
    ev = load(root, ev_rel)
    entries = load(root, map_rel)["entries"]
    last = {}
    for r in doc["rows"]:
        last[r["n"]] = r
    canon_file, shape_of, shape_means = shapes_from_canon(root)

    flags = {}
    for x in entries:
        if x["class"] in ("b", "d"):
            flags.setdefault(x["target_id"], []).append(x)

    def fl(x):
        return {"at": "%s#%s" % (x["target_id"], x["target_locus"]), "class": x["class"],
                "phase": x["provenance"]["phase"], "anchor": x["target_anchor"]}

    items = []
    for e in sorted(ev["entries"], key=lambda e: e["n"]):
        own = e["target_id"]
        refs = e["answered_by"]
        answering, elsewhere = [], []
        for ref in refs:
            node, _, locus = ref.partition("#")
            for x in flags.get(node, []):
                (answering if x["target_locus"] == locus else elsewhere).append(fl(x))
        own_node = [fl(x) for x in flags.get(own, [])]
        # an answering node that is the entry's own node is already counted under own_node
        answering = [a for a in answering if not a["at"].startswith(own + "#")]
        elsewhere = [a for a in elsewhere if not a["at"].startswith(own + "#")]
        uniq = lambda xs: [dict(t) for t in sorted({tuple(sorted(x.items())) for x in xs})]
        answering, elsewhere, own_node = uniq(answering), uniq(elsewhere), uniq(own_node)
        collided = bool(answering or own_node)
        r = last.get(e["n"])
        if r is None:
            status = "BLOCKED: unruled"
            if collided:
                fails.append("#%d %s#%s: collided and unruled" % (e["n"], own, e["target_locus"]))
        elif r["verdict"] == "HOLDS":
            status = "SHIP-ELIGIBLE: R1 HOLDS"
        else:
            status = "BLOCKED: R1 FAILS -> drafting pass (%s)" % shape_of.get(e["n"], "shape unrecorded")
        items.append({
            "n": e["n"], "target": "%s#%s" % (own, e["target_locus"]), "phase": e["phase"], "tier": e["tier"],
            "answered_by": refs, "collided": collided,
            "collisions": {"at_answering_locus": answering, "on_own_node": own_node},
            "for_reading_elsewhere_on_answering_nodes": elsewhere,
            "r1": None if r is None else {"row": r["row"], "verdict": r["verdict"], "basis": r["basis"],
                                          "reason": r["reason"], "stronger_continuation": r["stronger_continuation"]},
            "shape": shape_of.get(e["n"]) if r is not None and r["verdict"] == "FAILS" else None,
            "status": status})

    coll = [i for i in items if i["collided"]]
    count = lambda xs, v: sum(1 for i in xs if i["r1"] and i["r1"]["verdict"] == v)
    shapes = {}
    for i in items:
        if i["shape"]:
            shapes.setdefault(i["shape"], []).append(i["n"])
    report = {
        "artifact": NAME + ".json",
        "rule": "Every (a) whose answered_by locus or same-node sibling carries a (b) or (d) is listed for reading, "
                "and the list must be empty or ruled before any (a) card ships (canon "
                "adversarial_map.a_vs_own_record_collision_finding_L2, adopted at L2; built at L3).",
        "inputs": {"rulings": {"file": RULINGS, "md5": md5(os.path.join(root, RULINGS))},
                   "evidence": {"file": ev_rel, "md5": doc["evidence"]["md5"]},
                   "map": {"file": map_rel, "md5": doc["map"]["md5"]}, "canon": canon_file},
        "summary": {
            "a_entries": len(items), "ruled": sum(1 for i in items if i["r1"]),
            "collided": len(coll), "collided_ruled": sum(1 for i in coll if i["r1"]),
            "collided_HOLDS": count(coll, "HOLDS"), "collided_FAILS": count(coll, "FAILS"),
            "uncollided_HOLDS": count([i for i in items if not i["collided"]], "HOLDS"),
            "uncollided_FAILS": count([i for i in items if not i["collided"]], "FAILS"),
            "ship_eligible": sorted(i["n"] for i in items if i["status"].startswith("SHIP")),
            "blocked_by_shape": {k: sorted(v) for k, v in sorted(shapes.items())},
            "unruled": sorted(i["n"] for i in items if i["r1"] is None),
            "rule_broken": bool(fails)},
        "shape_means": shape_means,
        "items": items,
    }
    return fails, report


def render_md(rep):
    s = rep["summary"]
    L = ["# R1 collision list v0_1: the drafting pass's worklist", "",
         "Generated by `adversarial_map_staging/r1/r1_collision_list.py` from the rulings file `%s`, the evidence "
         "file and the map it names, and `%s`. Do not edit; regenerate." % (rep["inputs"]["rulings"]["md5"][:8],
                                                                           rep["inputs"]["canon"]), "",
         "**The rule:** %s" % rep["rule"], "",
         "- (a) entries: %d; ruled: %d; unruled: %d" % (s["a_entries"], s["ruled"], len(s["unruled"])),
         "- collided: %d (ruled %d: HOLDS %d, FAILS %d); not collided: HOLDS %d, FAILS %d"
         % (s["collided"], s["collided_ruled"], s["collided_HOLDS"], s["collided_FAILS"], s["uncollided_HOLDS"],
            s["uncollided_FAILS"]),
         "- ship-eligible (R1 HOLDS): %d; blocked (R1 FAILS): %d" % (
             len(s["ship_eligible"]), sum(len(v) for v in s["blocked_by_shape"].values())),
         "- rule broken: %s" % ("YES" if s["rule_broken"] else "no"), ""]
    by_n = {i["n"]: i for i in rep["items"]}

    def flags_md(i):
        out = []
        for x in i["collisions"]["at_answering_locus"]:
            out.append("  - collision at the answering locus: (%s) `%s` [%s] \"%s\"" % (x["class"], x["at"], x["phase"], x["anchor"]))
        for x in i["collisions"]["on_own_node"]:
            out.append("  - collision on its own node: (%s) `%s` [%s] \"%s\"" % (x["class"], x["at"], x["phase"], x["anchor"]))
        for x in i["for_reading_elsewhere_on_answering_nodes"]:
            out.append("  - for reading (answering node, other slot): (%s) `%s` [%s]" % (x["class"], x["at"], x["phase"]))
        return out

    L += ["## Blocked: R1 FAILS, by failure shape (the seat's reading)", ""]
    for shape, ns in s["blocked_by_shape"].items():
        L += ["### %s (%d)" % (shape, len(ns)), "", rep["shape_means"].get(shape, ""), ""]
        for n in ns:
            i = by_n[n]
            L += ["- **#%d `%s`** [%s, %s] -> %s  (%s, basis %s)" % (
                n, i["target"], i["phase"], i["tier"], ", ".join("`%s`" % a for a in i["answered_by"]),
                i["r1"]["row"], i["r1"]["basis"]),
                  "  - why it failed: %s" % i["r1"]["reason"],
                  "  - stronger line: %s" % i["r1"]["stronger_continuation"]]
            L += flags_md(i)
        L.append("")
    L += ["## Ship-eligible: R1 HOLDS", ""]
    for n in s["ship_eligible"]:
        i = by_n[n]
        L.append("- #%d `%s` [%s] -> %s  (%s)%s" % (
            n, i["target"], i["phase"], ", ".join("`%s`" % a for a in i["answered_by"]), i["r1"]["row"],
            "  **collided, ruled HOLDS**" if i["collided"] else ""))
        if i["collided"]:
            L += flags_md(i)
    if s["unruled"]:
        L += ["", "## Unruled", ""] + ["- #%d `%s`" % (n, by_n[n]["target"]) for n in s["unruled"]]
    L.append("")
    return "\n".join(L)


def emit(rep, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, NAME + ".json"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, NAME + ".md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(rep))


# ------------------------------------------------------------------ controls
def self_test(emit_path=None):
    tmp = tempfile.mkdtemp(prefix="r1coll_")
    doc0 = load(REPO, RULINGS)
    results = []
    try:
        def stage(name, mutate):
            d = os.path.join(tmp, name)
            for rel in (RULINGS, doc0["evidence"]["file"], doc0["map"]["file"]):
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(REPO, rel), os.path.join(d, rel))
            for c in glob.glob(os.path.join(REPO, "project_canon_v38_*.json")):
                shutil.copyfile(c, os.path.join(d, os.path.basename(c)))
            mutate(d)
            return d

        def drop_rows_for(n):
            def m(d):
                p = os.path.join(d, RULINGS)
                doc = json.load(open(p, encoding="utf-8"))
                doc["rows"] = [r for r in doc["rows"] if r["n"] != n]
                json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            return m

        def append_byte(rel):
            def m(d):
                open(os.path.join(d, rel), "ab").write(b" ")
            return m

        _, rep0 = build(REPO)
        collided = [i["n"] for i in rep0["items"] if i["collided"]]
        clean = [i["n"] for i in rep0["items"] if not i["collided"]]
        controls = [
            ("C0", "unmutated", lambda d: None, 0),
            ("C1", "a collided (a) loses its ruling (#%d)" % collided[0], drop_rows_for(collided[0]), 1),
            ("C2", "the map moves one byte", append_byte(doc0["map"]["file"]), 1),
            ("C3", "the evidence file moves one byte", append_byte(doc0["evidence"]["file"]), 1),
            ("C4", "an uncollided (a) loses its ruling (#%d): blocked, not a breach" % clean[0],
             drop_rows_for(clean[0]), 0),
        ]
        for cid, what, mut, want in controls:
            d = stage(cid, mut)
            fails, rep = build(d)
            got = 1 if fails else 0
            extra = ""
            if cid == "C4":
                ok4 = clean[0] in rep["summary"]["unruled"] and got == 0
                extra = " (blocked as unruled: %s)" % ok4
                got = 0 if ok4 else 1
            results.append({"control": cid, "what": what, "rc": 1 if fails else 0, "expected_rc": want,
                            "as_expected": got == want, "fail_lines": fails[:3]})
            print("%-3s %-62s rc=%d %s%s" % (cid, what, 1 if fails else 0,
                                             "as expected" if got == want else "UNEXPECTED", extra))
            if cid == "C0" and got != want:
                print("SELF-TEST: the unmutated control failed first; nothing after it means anything")
                return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    good = sum(r["as_expected"] for r in results)
    print("SELF-TEST: %d of %d controls as expected" % (good, len(results)))
    if emit_path:
        rec = {"artifact": os.path.basename(emit_path),
               "tool": "adversarial_map_staging/r1/r1_collision_list.py",
               "tool_md5": md5(os.path.abspath(__file__)),
               "rulings_md5": md5(os.path.join(REPO, RULINGS)),
               "rule": "C0, the unmutated control, runs first and must be GREEN; C1-C3 must go RED; C4 must stay "
                       "GREEN with the entry reported as blocked (unruled).",
               "controls": results}
        with open(emit_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    return 0 if good == len(results) else 1


def main():
    a = sys.argv[1:]
    if a[:1] == ["--self-test"]:
        return self_test(a[a.index("--emit") + 1] if "--emit" in a else None)
    fails, rep = build(REPO)
    s = rep["summary"]
    for f_ in fails:
        print("FAIL", f_)
    print("(a) entries %d | ruled %d | collided %d (HOLDS %d, FAILS %d) | ship-eligible %d | blocked %d | unruled %d"
          % (s["a_entries"], s["ruled"], s["collided"], s["collided_HOLDS"], s["collided_FAILS"],
             len(s["ship_eligible"]), sum(len(v) for v in s["blocked_by_shape"].values()), len(s["unruled"])))
    print("blocked by shape: %s" % json.dumps({k: len(v) for k, v in s["blocked_by_shape"].items()}))
    if "--emit" in a:
        emit(rep, a[a.index("--emit") + 1])
        print("wrote %s.json and %s.md" % (NAME, NAME))
    print("COLLISION RULE: %s" % ("GREEN" if not fails else "RED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
