#!/usr/bin/env python3
"""r1_rulings_gate.py -- the gate beside R1_rulings.json (L2, 2026-09-25).

R1_rulings.json is APPEND-ONLY: a row is never edited or removed, and a correction is a new row
whose `supersedes` names the row it replaces. This gate checks, and exits 1 on any failure:

  1. every row names a real entry: its `n` exists in the evidence file, and its `target` and
     `phase` are that entry's;
  2. every verdict is HOLDS or FAILS; a FAILS carries its stronger-continuation line, and a HOLDS
     carries none;
  3. no entry is ruled twice without a row that supersedes the first (per entry, each later row
     supersedes the row before it, and nothing else);
  4. the evidence file is still at the md5 every row names, and the map it was measured from is
     still at the md5 the evidence records;
  5. append-only: every row of the committed base (git HEAD's copy, or --base) is still present,
     unchanged and in order, and the header is unchanged.

  python3 r1_rulings_gate.py                 # the repo's files; base = git HEAD's copy
  python3 r1_rulings_gate.py --self-test     # mutation controls; the unmutated control runs first
  python3 r1_rulings_gate.py --self-test --emit <path>   # also write the control record

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/R1_rulings.json"
ROW_KEYS = {"row", "n", "target", "phase", "block", "verdict", "reason", "stronger_continuation", "basis",
            "map_record", "note_not_ruled", "ruled_by", "seat", "date", "evidence_md5", "supersedes"}


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def committed_base():
    try:
        return subprocess.run(["git", "-C", REPO, "show", "HEAD:" + REL], capture_output=True,
                              check=True).stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def check(rulings_path, repo_dir, base_text):
    """Return (list of failure lines, list of info lines)."""
    fails, info = [], []
    doc = json.load(open(rulings_path, encoding="utf-8"))
    rows = doc.get("rows")
    if not isinstance(rows, list) or not rows:
        return ["structure: no rows"], info
    ev_path = os.path.join(repo_dir, doc["evidence"]["file"])
    map_path = os.path.join(repo_dir, doc["map"]["file"])
    ev = json.load(open(ev_path, encoding="utf-8"))
    by_n = {e["n"]: e for e in ev["entries"]}

    # 4 -- the referents have not moved
    ev_md5, map_md5 = md5(ev_path), md5(map_path)
    if ev_md5 != doc["evidence"]["md5"]:
        fails.append("evidence md5: file is %s, header names %s" % (ev_md5, doc["evidence"]["md5"]))
    if map_md5 != doc["map"]["md5"] or map_md5 != ev["inputs"]["map_md5"]:
        fails.append("map md5: file is %s, header names %s, evidence records %s"
                     % (map_md5, doc["map"]["md5"], ev["inputs"]["map_md5"]))

    seen_ids, chains = set(), {}
    for i, r in enumerate(rows, 1):
        rid = r.get("row", "?")
        if set(r) != ROW_KEYS:
            fails.append("%s: keys differ from the schema (%s)" % (rid, sorted(set(r) ^ ROW_KEYS)))
            continue
        if rid != "R1-%03d" % i:
            fails.append("%s: row ids must run R1-001, R1-002, ... in file order (expected R1-%03d)" % (rid, i))
        if rid in seen_ids:
            fails.append("%s: duplicate row id" % rid)
        seen_ids.add(rid)
        # 1
        e = by_n.get(r["n"])
        if e is None:
            fails.append("%s: n=%s names no evidence entry" % (rid, r["n"]))
        else:
            tgt = e["target_id"] + "#" + e["target_locus"]
            if r["target"] != tgt:
                fails.append("%s: target %s != evidence #%s %s" % (rid, r["target"], r["n"], tgt))
            if r["phase"] != e["phase"]:
                fails.append("%s: phase %s != evidence #%s phase %s" % (rid, r["phase"], r["n"], e["phase"]))
        # 2
        if r["verdict"] not in ("HOLDS", "FAILS"):
            fails.append("%s: verdict %r is not HOLDS or FAILS" % (rid, r["verdict"]))
        elif r["verdict"] == "FAILS" and not (isinstance(r["stronger_continuation"], str)
                                              and r["stronger_continuation"].strip()):
            fails.append("%s: FAILS without its stronger-continuation line" % rid)
        elif r["verdict"] == "HOLDS" and r["stronger_continuation"] is not None:
            fails.append("%s: HOLDS carries a stronger-continuation line" % rid)
        if not (isinstance(r["ruled_by"], dict) and str(r["ruled_by"].get("josiah_verbatim", "")).strip()):
            fails.append("%s: ruled_by carries no verbatim words" % rid)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        # 4, per row
        if r["evidence_md5"] != ev_md5:
            fails.append("%s: names evidence md5 %s, file is %s" % (rid, r["evidence_md5"], ev_md5))
        # 3
        prev = chains.get(r["n"])
        if prev is None:
            if r["supersedes"] is not None:
                fails.append("%s: supersedes %s, but it is the first row for #%s" % (rid, r["supersedes"], r["n"]))
        elif r["supersedes"] != prev:
            fails.append("%s: #%s ruled twice without superseding %s" % (rid, r["n"], prev))
        chains[r["n"]] = rid

    # 5 -- append-only against the committed base
    if base_text is None:
        info.append("append-only: SKIPPED -- no committed base yet (first landing); vacuous, not a pass")
    else:
        base = json.loads(base_text)
        bh = {k: v for k, v in base.items() if k != "rows"}
        ch = {k: v for k, v in doc.items() if k != "rows"}
        if bh != ch:
            fails.append("append-only: the header differs from the committed base")
        brows = base["rows"]
        if rows[:len(brows)] != brows:
            bad = next((b["row"] for b, c in zip(brows, rows) if b != c), "a removed row")
            fails.append("append-only: committed row %s was edited or removed" % bad)
        info.append("append-only: %d committed rows intact, %d appended" % (len(brows), len(rows) - len(brows))
                    if not any(f.startswith("append-only") for f in fails) else "append-only: BROKEN")
    ruled = sorted(chains)
    info.append("rows %d | entries ruled %d | current verdicts: HOLDS %d, FAILS %d" % (
        len(rows), len(ruled),
        sum(1 for n in ruled if [r for r in rows if r["n"] == n][-1]["verdict"] == "HOLDS"),
        sum(1 for n in ruled if [r for r in rows if r["n"] == n][-1]["verdict"] == "FAILS")))
    return fails, info


def run(rulings_path, repo_dir, base_text):
    fails, info = check(rulings_path, repo_dir, base_text)
    return (1 if fails else 0), fails, info


# ------------------------------------------------------------------ controls
def self_test(emit=None):
    real = os.path.join(REPO, REL)
    doc0 = json.load(open(real, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="r1gate_")
    results = []
    try:
        def stage(mut_doc=None, mut_ev=None, mut_map=None, base=None):
            d = os.path.join(tmp, "c%d" % len(results))
            os.makedirs(os.path.join(d, "adversarial_map_staging", "r1"))
            for key, mut in (("evidence", mut_ev), ("map", mut_map)):
                src = os.path.join(REPO, doc0[key]["file"])
                dst = os.path.join(d, doc0[key]["file"])
                shutil.copyfile(src, dst)
                if mut:
                    b = open(dst, "rb").read()
                    open(dst, "wb").write(b[:-1] + (b"\n" if b[-1:] != b"\n" else b" "))
            p = os.path.join(d, REL)
            json.dump(mut_doc if mut_doc is not None else doc0, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            # base defaults to the staged document itself, so each control isolates its own check;
            # the append-only controls pass the original explicitly
            return p, d, json.dumps(base if base is not None else (mut_doc if mut_doc is not None else doc0),
                                    ensure_ascii=False)

        def mut(fn):
            d = copy.deepcopy(doc0); fn(d); return d

        r0 = doc0["rows"][0]
        fails_row = next(r for r in doc0["rows"] if r["verdict"] == "FAILS")
        extra = dict(copy.deepcopy(r0), row="R1-%03d" % (len(doc0["rows"]) + 1))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "a row names n=999", dict(mut_doc=mut(lambda d: d["rows"][0].update(n=999))), 1, "names no evidence entry"),
            ("C2", "a row's target names the wrong locus", dict(mut_doc=mut(lambda d: d["rows"][0].update(target=d["rows"][0]["target"].split("#")[0] + "#short"))), 1, "!= evidence"),
            ("C3", "a verdict reads MAYBE", dict(mut_doc=mut(lambda d: d["rows"][0].update(verdict="MAYBE"))), 1, "is not HOLDS or FAILS"),
            ("C4", "a FAILS row loses its stronger line", dict(mut_doc=mut(lambda d: next(r for r in d["rows"] if r["row"] == fails_row["row"]).update(stronger_continuation=None))), 1, "FAILS without its stronger-continuation line"),
            ("C5", "an entry ruled twice, no supersedes", dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=None))), base=doc0), 1, "ruled twice without superseding"),
            ("C6", "the evidence file moves by one byte", dict(mut_ev=True), 1, "evidence md5"),
            ("C7", "the map file moves by one byte", dict(mut_map=True), 1, "map md5"),
            ("C8", "a committed row is edited in place", dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C9", "a committed row is removed", dict(mut_doc=mut(lambda d: d["rows"].pop(0)), base=doc0), 1, "was edited or removed"),
            ("C10", "a correction row supersedes properly", dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=r0["row"]))), base=doc0), 0, None),
        ]
        ok_all = True
        for cid, what, kw, want_rc, want_msg in controls:
            p, d, base = stage(**kw)
            rc, fails, _ = run(p, d, base)
            matched = (want_msg is None and not fails) or (want_msg is not None and any(want_msg in f for f in fails))
            good = rc == want_rc and matched
            if cid == "C0" and not good:
                print("C0 (unmutated) is not GREEN -- no mutation result below could mean anything")
                return 1
            ok_all &= good
            results.append({"control": cid, "mutation": what, "expected_rc": want_rc,
                            "expected_message": want_msg, "rc": rc, "as_expected": good,
                            "failure_lines": fails[:3]})
            print("%-4s %-40s rc=%d %s" % (cid, what, rc, "as expected" if good else "UNEXPECTED: %s" % fails))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELF-TEST: %d of %d controls as expected" % (sum(r["as_expected"] for r in results), len(results)))
    if emit:
        rec = {"artifact": os.path.basename(emit), "gate": "adversarial_map_staging/r1/r1_rulings_gate.py",
               "gate_md5": md5(os.path.abspath(__file__)), "rulings_md5": md5(real),
               "rule": "C0, the unmutated control, runs first and must be GREEN; each mutation must go RED with "
                       "its own failure line; C10, a proper correction row, must stay GREEN.",
               "controls": results}
        open(emit, "w", encoding="utf-8").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    return 0 if ok_all else 1


def main():
    if "--self-test" in sys.argv:
        emit = sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None
        sys.exit(self_test(emit))
    base_text = committed_base()
    if "--base" in sys.argv:
        base_text = open(sys.argv[sys.argv.index("--base") + 1], encoding="utf-8").read()
    rc, fails, info = run(os.path.join(REPO, REL), REPO, base_text)
    for line in info:
        print("  " + line)
    for line in fails:
        print("  FAIL " + line)
    print("R1 RULINGS GATE: %s" % ("GREEN" if rc == 0 else "RED"))
    sys.exit(rc)


if __name__ == "__main__":
    main()
