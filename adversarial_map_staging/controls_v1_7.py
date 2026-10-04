#!/usr/bin/env python3
"""controls_v1_7.py -- prove build_assembly_v1_7.py's and build_register_v0_8.py's gates by failing them (L7).

Each control copies the staging tree, the corpus (at the md5 the successor pins) and the canon to scratch, mutates one
thing, runs the builder there with K348_REPO pointed at the copy, and requires the refusal to name its own check. Each
builder's unmutated control runs first and must reproduce the committed bytes.

The assembly builder pins its drafts record and the measure by md5, so a control that mutates either also re-pins it
in the scratch copy of the builder: otherwise every such control would stop at the base guard and prove nothing about
the check behind it. The committed builder is never touched.

  python3 controls_v1_7.py            # run, write controls_v1_7_v0_1.json
  python3 controls_v1_7.py --check    # run, compare with the committed record
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STAGE = "adversarial_map_staging"
RECORD = os.path.join(HERE, "controls_v1_7_v0_1.json")
MAP, REG = "adversarial_map_v1_7.json", "honest_residuals_register_v0_8.json"
DRAFTS = os.path.join("r1", "L7_successor_drafts.json")
BUILDER = "build_assembly_v1_7.py"
CORPUS_PIN = "7b6e65e531018fecb37baf2a4fedd6d1"
DRAFTS_PIN = "fd9267f853a5a09fe5aa3972b16fa2a7"   # the bytes build_assembly_v1_7.py pins
RULINGS = os.path.join("r1", "R1_rulings.json")
RULINGS_PIN = "d829437e938a8b9dded5cb8cbaa26b74"  # the bytes build_assembly_v1_7.py pins


def md5b(b):
    return hashlib.md5(b).hexdigest()


def scratch():
    d = tempfile.mkdtemp(prefix="l7_controls_")
    shutil.copytree(os.path.join(REPO, STAGE), os.path.join(d, STAGE),
                    ignore=shutil.ignore_patterns("__pycache__", "*.tmp"))
    for f in os.listdir(REPO):
        if re.match(r"project_canon_v38_\d+\.json$", f):
            shutil.copy2(os.path.join(REPO, f), os.path.join(d, f))
    sys.path.insert(0, os.path.join(REPO, STAGE, "r1"))
    import pinned
    open(os.path.join(d, "efilist_argument_library_v4_0_0.json"), "wb").write(
        pinned.bytes_at(REPO, "efilist_argument_library_v4_0_0.json", CORPUS_PIN))
    # L7, second round: the drafts record is append-only and build_assembly_v1_7.py pins it at DRAFTS_PIN. Stage those
    # bytes, so a later row cannot turn an unmutated control RED (the L4c law for R1_rulings.json); pinned.py reads
    # them from git once the file has grown.
    open(os.path.join(d, STAGE, DRAFTS), "wb").write(pinned.bytes_at(REPO, STAGE + "/r1/L7_successor_drafts.json",
                                                                    DRAFTS_PIN))
    # L7 close: the same for R1_rulings.json, which grows from R1-071 (a rehearsal with four rows appended turned A0
    # RED: the scratch copy has no git history to read the pinned bytes back from).
    open(os.path.join(d, STAGE, RULINGS), "wb").write(pinned.bytes_at(REPO, STAGE + "/r1/R1_rulings.json", RULINGS_PIN))
    return d


def run(d, builder):
    env = dict(os.environ, K348_REPO=d, PYTHONDONTWRITEBYTECODE="1")
    env.pop("K348_MAP_DIR", None)
    p = subprocess.run([sys.executable, os.path.join(d, STAGE, builder)], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def repin(d, rel):
    """Re-pin a mutated input in the scratch copy of the assembly builder."""
    p = os.path.join(d, STAGE, rel)
    new = md5b(open(p, "rb").read())
    bp = os.path.join(d, STAGE, BUILDER)
    src = open(bp, encoding="utf-8").read()
    line = [l for l in src.splitlines() if ("/" + os.path.basename(rel) + '"') in l and "(" in l][0]
    old = re.search(r'"([0-9a-f]{32})"', line).group(1)
    open(bp, "w", encoding="utf-8").write(src.replace(old, new, 1))
    return old, new


def edit_json(d, rel, fn):
    p = os.path.join(d, STAGE, rel)
    doc = json.load(open(p, encoding="utf-8"))
    fn(doc)
    open(p, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def drafts_edit(fn):
    def m(d):
        edit_json(d, DRAFTS, fn)
        repin(d, DRAFTS)
    return m


def row(doc, pred):
    return [r for r in doc["rows"] if pred(r)][0]


def drop(pred):
    return lambda doc: doc["rows"].remove(row(doc, pred))


def at(i):
    return lambda r: (r.get("entry") or {}).get("i") == i


def c_unset_grounds(doc):
    row(doc, at(5))["set"].pop("grounds")


def c_wrong_anchor(doc):
    row(doc, at(4))["entry"]["anchor"] = "not the anchor of entry 4"


def c_misquote(doc):
    r = row(doc, at(9))
    q = r["quotes"][0]["quote"]
    r["quotes"][0]["quote"] = q.replace("already", "alrady")
    r["set"]["grounds"] = r["set"]["grounds"].replace(q, r["quotes"][0]["quote"])


def c_undeclared(doc):
    r = row(doc, at(12))
    r["set"]["grounds"] += ' It adds "a quotation nobody declared".'


def c_wrong_facet(doc):
    row(doc, at(51))["bedrock_from"]["facet"] = "metaethical-locus"


def c_twice(doc):
    doc["rows"].append(dict(row(doc, at(4)), id="SM-99"))


def c_dash(doc):
    r = row(doc, lambda r: r["kind"] == "file")
    r["new_entry"]["adversarial_move"] = r["new_entry"]["adversarial_move"].replace(". ", " — ", 1)


def c_base(rel):
    def fn(d):
        p = os.path.join(d, STAGE, rel)
        b = open(p, "rb").read()
        open(p, "wb").write(b.replace(b"mapped", b"Mapped", 1) if rel.startswith("adversarial") else
                            b.replace(b"HR-01", b"HR-0l", 1))
    return fn


def c_map_routing(d):
    def fn(doc):
        e = [x for x in doc["entries"] if x["class"] == "d" and "successor_L7" not in x["provenance"]
             and "filed" not in x["provenance"]][0]
        e["routing"]["residue"]["terminus_routing"] += " (moved)"
    edit_json(d, MAP, fn)


def c_no_relation(d):
    edit_json(d, DRAFTS, drop(lambda r: r["kind"] == "relation"))
    new = md5b(open(os.path.join(d, STAGE, DRAFTS), "rb").read())
    edit_json(d, MAP, lambda doc: doc["meta"]["l7_successor"]["drafts"].__setitem__("md5", new))


CONTROLS = [
    ("A0 map builder, unmutated", BUILDER, None, MAP),
    ("A1 a gone anchor loses its row (entry 2)", BUILDER, drafts_edit(drop(at(2))),
     "COVERAGE: entry 2's anchor is gone"),
    ("A2 a routed HOLDS loses its read (#24, entry 39)", BUILDER, drafts_edit(drop(at(39))),
     "COVERAGE: entry 39 routes to moved"),
    ("A3 a stale quotation left unrewritten (#3's grounds)", BUILDER, drafts_edit(c_unset_grounds),
     "COVERAGE: entry 5's grounds quotes words gone"),
    ("A4 a waiting (a) loses its re-judgment (#48)", BUILDER, drafts_edit(drop(at(80))),
     "COVERAGE: waiting (a) #48"),
    ("A5 a row names an anchor its entry does not carry", BUILDER, drafts_edit(c_wrong_anchor), "is not"),
    ("A6 a declared quotation altered by one letter", BUILDER, drafts_edit(c_misquote), "NOT VERBATIM"),
    ("A7 an undeclared quotation in changed grounds", BUILDER, drafts_edit(c_undeclared), "undeclared quotation"),
    ("A8 bedrock_from claims a facet the register does not file", BUILDER, drafts_edit(c_wrong_facet),
     "register v0_7 does not file bedrock_from"),
    ("A9 two rows for one entry", BUILDER, drafts_edit(c_twice), "has 2 rows"),
    ("A10 a filed move carrying a dash token (the validator, in-process)", BUILDER, drafts_edit(c_dash),
     "validator v0_7 --assembly"),
    ("A11 v1_6 moved by one byte", BUILDER, c_base("adversarial_map_v1_6.json"), "BASE GUARD"),
    ("R0 register builder, unmutated", "build_register_v0_8.py", None, REG),
    ("R1 an inherited (d)'s routing moved in the map", "build_register_v0_8.py", c_map_routing,
     "register and map disagree"),
    ("R2 the drafted relation removed", "build_register_v0_8.py", c_no_relation, "UNDECLARED ADJACENCY: HR-02+HR-06"),
    ("R3 register v0_7 moved by one byte", "build_register_v0_8.py", c_base("honest_residuals_register_v0_7.json"),
     "BASE GUARD"),
]


def main():
    results, good = [], 0
    for name, builder, mut, want in CONTROLS:
        d = scratch()
        try:
            if mut is not None:
                mut(d)
            rc, out = run(d, builder)
            if mut is None:
                committed = open(os.path.join(REPO, STAGE, want), "rb").read()
                got = open(os.path.join(d, STAGE, want), "rb").read() if rc == 0 else b""
                ok = rc == 0 and got == committed
            else:
                ok = rc != 0 and want in out
        finally:
            shutil.rmtree(d)
        print("%-72s %s" % (name, "as expected" if ok else "UNEXPECTED (rc=%d)" % rc))
        if not ok:
            print("    " + "\n    ".join(out.strip().splitlines()[-4:]))
        results.append({"control": name, "expect": ("writes the committed %s" % want) if mut is None
                        else "refuses, naming %r" % want, "as_expected": ok})
        good += ok
        if mut is None and not ok:
            print("CONTROLS: an unmutated control failed; nothing after it means anything")
            return 1
    rec = {"artifact": "controls_v1_7_v0_1.json", "instrument": "adversarial_map_staging/controls_v1_7.py",
           "map": {"file": "adversarial_map_staging/" + MAP, "md5": md5b(open(os.path.join(HERE, MAP), "rb").read())},
           "register": {"file": "adversarial_map_staging/" + REG, "md5": md5b(open(os.path.join(HERE, REG), "rb").read())},
           "result": "%d of %d controls as expected, each builder's unmutated control first" % (good, len(CONTROLS)),
           "controls": results}
    s = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        same = open(RECORD, encoding="utf-8").read() == s
        print("CONTROL RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        return 0 if (same and good == len(CONTROLS)) else 1
    open(RECORD, "w", encoding="utf-8").write(s)
    print("CONTROLS: %d of %d as expected; wrote %s" % (good, len(CONTROLS), os.path.basename(RECORD)))
    return 0 if good == len(CONTROLS) else 1


if __name__ == "__main__":
    sys.exit(main())
