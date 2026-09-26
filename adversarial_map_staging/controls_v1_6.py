#!/usr/bin/env python3
"""controls_v1_6.py -- prove build_assembly_v1_6.py's and build_register_v0_7.py's gates by failing them (L4c).

Each control copies the staging tree, the corpus and the canon to scratch, mutates one thing, runs the
builder there with K348_REPO pointed at the copy, and requires the refusal to name its own check. Each
builder's unmutated control runs first and must reproduce the committed bytes.

  python3 controls_v1_6.py            # run, write controls_v1_6_v0_1.json
  python3 controls_v1_6.py --check    # run, compare with the committed record
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STAGE = "adversarial_map_staging"
RECORD = os.path.join(HERE, "controls_v1_6_v0_1.json")
MAP, REG = "adversarial_map_v1_6.json", "honest_residuals_register_v0_7.json"
REDRAFTS = os.path.join("r1", "R1_redrafts_v1_6.json")
RULINGS_PIN = "d829437e938a8b9dded5cb8cbaa26b74"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def scratch():
    d = tempfile.mkdtemp(prefix="l4c_controls_")
    shutil.copytree(os.path.join(REPO, STAGE), os.path.join(d, STAGE),
                    ignore=shutil.ignore_patterns("__pycache__", "*.tmp"))
    for f in os.listdir(REPO):
        if f == "efilist_argument_library_v4_0_0.json" or re.match(r"project_canon_v38_\d+\.json$", f):
            shutil.copy2(os.path.join(REPO, f), os.path.join(d, f))
    # R1_rulings.json is append-only, and build_assembly_v1_6.py pins it at RULINGS_PIN; stage those bytes, so a
    # later row cannot turn an unmutated control RED. pinned.py reads them from git if the file grew.
    sys.path.insert(0, os.path.join(REPO, STAGE, "r1"))
    import pinned
    open(os.path.join(d, STAGE, "r1", "R1_rulings.json"), "wb").write(
        pinned.bytes_at(REPO, STAGE + "/r1/R1_rulings.json", RULINGS_PIN))
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


def rd0(doc):
    return doc["redrafts"][0]


def c_knock(d):
    edit_json(d, REDRAFTS, lambda doc: rd0(doc).__setitem__("knock_on_row", "V-001"))


def c_anchor(d):
    edit_json(d, REDRAFTS, lambda doc: rd0(doc).__setitem__("bedrock_from_anchor", "not an anchor anywhere"))


def c_hr(d):
    edit_json(d, REDRAFTS, lambda doc: rd0(doc).__setitem__("hr", "HR-02"))


def c_misquote(d):
    def fn(doc):
        x = rd0(doc)
        old = x["quotes"][1]["quote"]
        new = old.replace("undebunked", "debunked")
        x["quotes"][1]["quote"] = new
        x["grounds"] = x["grounds"].replace(old, new)
    edit_json(d, REDRAFTS, fn)


def c_held(d):
    edit_json(d, REDRAFTS, lambda doc: rd0(doc).__setitem__("n", 3))


def c_base(rel):
    def fn(d):
        p = os.path.join(d, STAGE, rel)
        b = open(p, "rb").read()
        open(p, "wb").write(b.replace(b"mapped", b"Mapped", 1) if rel.startswith("adversarial") else
                            b.replace(b"HR-01", b"HR-0l", 1))
    return fn


def c_map_routing(d):
    def fn(doc):
        # an inherited (d): #46's own tributary is derived from the map, so moving it moves both sides
        e = [x for x in doc["entries"] if x["class"] == "d"
             and x["provenance"].get("amended", {}).get("at") != "L4c"][0]
        e["routing"]["residue"]["terminus_routing"] += " (moved)"
    edit_json(d, MAP, fn)


def c_shape(d):
    p = [os.path.join(d, f) for f in sorted(os.listdir(d)) if re.match(r"project_canon_v38_\d+\.json$", f)][0]
    doc = json.load(open(p, encoding="utf-8"))
    am = doc["adversarial_map"]
    k = sorted(k for k in am if k.startswith("R1_progress_L") and "failure_shapes_seat_s_reading" in am[k])[-1]
    for v in am[k]["failure_shapes_seat_s_reading"].values():
        v["entries"] = [n for n in v["entries"] if n != 46]
    open(p, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


CONTROLS = [
    ("A0 map builder, unmutated", "build_assembly_v1_6.py", None, MAP),
    ("A1 the knock-on row does not reopen #46 (V-001)", "build_assembly_v1_6.py", c_knock, "does not reopen this entry"),
    ("A2 bedrock_from's anchor names no (d)", "build_assembly_v1_6.py", c_anchor, "bedrock_from names 0"),
    ("A3 the draft claims HR-02", "build_assembly_v1_6.py", c_hr, "the register does not file bedrock_from"),
    ("A4 a declared quotation altered", "build_assembly_v1_6.py", c_misquote, "NOT VERBATIM"),
    ("A5 a draft for an entry R1 still holds (#3)", "build_assembly_v1_6.py", c_held, "not a FAILS superseding a HOLDS"),
    ("A6 v1_5 moved by one byte", "build_assembly_v1_6.py", c_base("adversarial_map_v1_5.json"), "BASE GUARD"),
    ("A7 canon's newest R1_progress block gives #46 no shape", "build_assembly_v1_6.py", c_shape,
     "gives it no failure shape"),
    ("R0 register builder, unmutated", "build_register_v0_7.py", None, REG),
    ("R1 an inherited (d)'s routing moved in the map", "build_register_v0_7.py", c_map_routing, "register and map disagree"),
    ("R2 register v0_6 moved by one byte", "build_register_v0_7.py", c_base("honest_residuals_register_v0_6.json"), "BASE GUARD"),
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
    rec = {"artifact": "controls_v1_6_v0_1.json", "instrument": "adversarial_map_staging/controls_v1_6.py",
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
