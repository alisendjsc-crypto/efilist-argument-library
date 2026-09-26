#!/usr/bin/env python3
"""controls_v1_5.py -- prove build_assembly_v1_5.py's and build_register_v0_6.py's gates by failing them (L4b).

Each control copies the staging tree, the corpus and the canon to scratch, mutates one thing, runs the
builder there with K348_REPO pointed at the copy, and requires the refusal to name its own check. Each
builder's unmutated control runs first and must reproduce the committed bytes.

  python3 controls_v1_5.py            # run, write controls_v1_5_v0_1.json
  python3 controls_v1_5.py --check    # run, compare with the committed record
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STAGE = "adversarial_map_staging"
RECORD = os.path.join(HERE, "controls_v1_5_v0_1.json")
MAP, REG = "adversarial_map_v1_5.json", "honest_residuals_register_v0_6.json"
REDRAFTS = os.path.join("r1", "R1_redrafts_v1_5.json")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def scratch():
    d = tempfile.mkdtemp(prefix="l4b_controls_")
    shutil.copytree(os.path.join(REPO, STAGE), os.path.join(d, STAGE),
                    ignore=shutil.ignore_patterns("__pycache__", "*.tmp"))
    for f in os.listdir(REPO):
        if f == "efilist_argument_library_v4_0_0.json" or re.match(r"project_canon_v38_\d+\.json$", f):
            shutil.copy2(os.path.join(REPO, f), os.path.join(d, f))
    # L4c: R1_rulings.json is append-only, and the builders pin it at 3f1dfad5; stage those bytes, so a
    # later row cannot turn an unmutated control RED. pinned.py reads them from git if the file grew.
    sys.path.insert(0, os.path.join(REPO, STAGE, "r1"))
    import pinned
    open(os.path.join(d, STAGE, "r1", "R1_rulings.json"), "wb").write(
        pinned.bytes_at(REPO, STAGE + "/r1/R1_rulings.json", "3f1dfad54021d7920576c7bd4840b62f"))
    return d


def run(d, builder):
    env = dict(os.environ, K348_REPO=d, PYTHONDONTWRITEBYTECODE="1")
    env.pop("K348_MAP_DIR", None)
    p = subprocess.run([sys.executable, os.path.join(d, STAGE, builder)], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def edit_json(d, rel, fn):
    p = os.path.join(d, STAGE, rel)
    doc = json.load(open(p, encoding="utf-8"))
    fn(doc)
    open(p, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def redraft(doc, n):
    return [x for x in doc["redrafts"] if x["n"] == n][0]


def c_wrong_row(d):
    edit_json(d, REDRAFTS, lambda doc: redraft(doc, 25).__setitem__("judgment_row", "J-014"))


def c_drop(d):
    edit_json(d, REDRAFTS, lambda doc: doc.__setitem__("redrafts", [x for x in doc["redrafts"] if x["n"] != 16]))


def c_completion(d):
    edit_json(d, REDRAFTS, lambda doc: redraft(doc, 14)["move_edit"].__setitem__(
        "completion", "A suffering-first view prefers whatever it likes."))


def c_misquote(d):
    def fn(doc):
        x = redraft(doc, 58)
        old = x["quotes"][1]["quote"]
        new = old.replace("existence itself", "existence alone")
        x["quotes"][1]["quote"] = new
        x["grounds"] = x["grounds"].replace(old, new)
    edit_json(d, REDRAFTS, fn)


def c_short_move(d):
    edit_json(d, REDRAFTS, lambda doc: redraft(doc, 58).__setitem__("move", "Fair play binds you. You free-ride."))


def c_base(rel):
    def fn(d):
        p = os.path.join(d, STAGE, rel)
        b = open(p, "rb").read()
        open(p, "wb").write(b.replace(b"mapped", b"Mapped", 1) if rel.startswith("adversarial") else
                            b.replace(b"HR-01", b"HR-0l", 1))
    return fn


def c_map_redraft_gone(d):
    def fn(doc):
        for e in doc["entries"]:
            rd = e["provenance"].get("redrafted")
            if rd and e["provenance"].get("amended", {}).get("r1_n") == 62:
                del e["provenance"]["redrafted"]
    edit_json(d, MAP, fn)


def c_map_other_routing(d):
    def fn(doc):
        e = [x for x in doc["entries"] if x["target_id"] == "solipsism" and x["class"] == "d"][0]
        e["routing"]["residue"]["terminus_routing"] += " (moved)"
    edit_json(d, MAP, fn)


CONTROLS = [
    ("A0 map builder, unmutated", "build_assembly_v1_5.py", None, MAP),
    ("A1 a redraft names another entry's judgment row (#25 -> J-014)", "build_assembly_v1_5.py", c_wrong_row, "does not name this entry"),
    ("A2 an owed fix left without a redraft (#16)", "build_assembly_v1_5.py", c_drop, "the rows that owe a fix"),
    ("A3 #14's completion is not its R1 row's line", "build_assembly_v1_5.py", c_completion, "not the R1 row's stronger line"),
    ("A4 a declared quotation altered (#58)", "build_assembly_v1_5.py", c_misquote, "NOT VERBATIM"),
    ("A5 #58's move under the 40-word floor", "build_assembly_v1_5.py", c_short_move, "move-band"),
    ("A6 v1_4 moved by one byte", "build_assembly_v1_5.py", c_base("adversarial_map_v1_4.json"), "BASE GUARD"),
    ("R0 register builder, unmutated", "build_register_v0_6.py", None, REG),
    ("R1 the map lost #62's routing redraft", "build_register_v0_6.py", c_map_redraft_gone, "the map carries"),
    ("R2 another (d)'s routing moved in the map", "build_register_v0_6.py", c_map_other_routing, "register and map disagree"),
    ("R3 register v0_5 moved by one byte", "build_register_v0_6.py", c_base("honest_residuals_register_v0_5.json"), "BASE GUARD"),
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
        print("%-66s %s" % (name, "as expected" if ok else "UNEXPECTED (rc=%d)" % rc))
        results.append({"control": name, "expect": ("writes the committed %s" % want) if mut is None
                        else "refuses, naming %r" % want, "as_expected": ok})
        good += ok
        if mut is None and not ok:
            print("CONTROLS: an unmutated control failed; nothing after it means anything")
            return 1
    rec = {"artifact": "controls_v1_5_v0_1.json", "instrument": "adversarial_map_staging/controls_v1_5.py",
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
