#!/usr/bin/env python3
"""controls_assembly_v1_4.py -- prove build_assembly_v1_4.py's gates by failing them (L4).

Each control copies the inputs to a scratch tree, mutates exactly one thing, runs the builder
there with K348_REPO pointed at the copy, and requires the refusal to name ITS OWN check (a
non-zero exit is not enough: a builder that dies for the wrong reason proves nothing). The
unmutated control runs first and must write a file byte-identical to the committed
adversarial_map_v1_4.json; if it does not, nothing after it means anything.

  python3 controls_assembly_v1_4.py            # run, print, write assembly_control_v0_4.json
  python3 controls_assembly_v1_4.py --check    # run, print, compare with the committed record

Repo-relative. Writes only the control record (and scratch it removes).
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STAGE = "adversarial_map_staging"
RECORD = os.path.join(HERE, "assembly_control_v0_4.json")
BUILDER = "build_assembly_v1_4.py"
MAP = "adversarial_map_v1_4.json"
DRAFTS = os.path.join("r1", "R1_drafts_L4.json")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def scratch():
    d = tempfile.mkdtemp(prefix="l4_controls_")
    shutil.copytree(os.path.join(REPO, STAGE), os.path.join(d, STAGE),
                    ignore=shutil.ignore_patterns("__pycache__", "*.tmp"))
    for f in os.listdir(REPO):
        if f == "efilist_argument_library_v4_0_0.json" or re.match(r"project_canon_v38_\d+\.json$", f):
            shutil.copy2(os.path.join(REPO, f), os.path.join(d, f))
    return d


def run(d):
    env = dict(os.environ, K348_REPO=d, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, os.path.join(d, STAGE, BUILDER)], env=env,
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def edit_drafts(d, fn):
    p = os.path.join(d, STAGE, DRAFTS)
    doc = json.load(open(p, encoding="utf-8"))
    fn(doc)
    open(p, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def draft(doc, n):
    return [x for x in doc["drafts"] if x["n"] == n][0]


def m_holds(doc):
    doc["drafts"].append({"n": 3, "row": "R1-023", "disposition": "waits", "waits_on": [],
                          "for_the_judge": None})


def m_drop(doc):
    doc["drafts"] = [x for x in doc["drafts"] if x["n"] != 65]


def m_quote(doc):
    x = draft(doc, 8)
    qq = x["quotes"][0]["quote"]
    x["quotes"][0]["quote"] = qq[:-2] + "X" + qq[-1]
    x["grounds"] = x["grounds"].replace(qq, x["quotes"][0]["quote"])


def m_undeclared(doc):
    x = draft(doc, 9)
    x["grounds"] += ' It is "decisive".'


def m_hr(doc):
    draft(doc, 10)["hr"] = "HR-04"


def m_cut(doc):
    draft(doc, 14)["move_edit"]["cut"] = ", which the asymmetry forbids"


def m_floor(doc):
    me = draft(doc, 62)["move_edit"]
    me["completion"] = "That is all."


def m_bedrock(doc):
    draft(doc, 21)["bedrock_from"] = "meaning-through-suffering#long"


def m_waits(doc):
    draft(doc, 11)["grounds"] = "moved"


def m_base(d):
    p = os.path.join(d, STAGE, "adversarial_map_v1_3.json")
    b = bytearray(open(p, "rb").read())
    i = b.index(b"mapped")
    b[i] = ord("M")
    open(p, "wb").write(bytes(b))


CONTROLS = [
    ("C0 unmutated", None, None),
    ("C1 a draft for a HOLDS row (#3)", m_holds, "drafts cover"),
    ("C2 a FAILS row left without a draft (#65)", m_drop, "drafts cover"),
    ("C3 one character changed in a declared quotation (#8)", m_quote, "NOT VERBATIM"),
    ("C4 an undeclared quotation in grounds (#9)", m_undeclared, "undeclared quotation"),
    ("C5 a (d) draft claims the wrong bedrock (#10 -> HR-04)", m_hr, "the register files"),
    ("C6 a cut that is not in the move (#14)", m_cut, "does not occur exactly once"),
    ("C7 a completion that leaves a move under the 40-word floor (#62)", m_floor, "move-band"),
    ("C8 bedrock_from names a locus with no (d) (#21)", m_bedrock, "(d) entries in v1_3"),
    ("C9 a waiting entry carries an edit field (#11)", m_waits, "a waiting entry carries edit fields"),
    ("C10 the base map moved by one byte", "base", "BASE GUARD"),
]


def main():
    committed = open(os.path.join(REPO, STAGE, MAP), "rb").read()
    results, good = [], 0
    for name, mut, want in CONTROLS:
        d = scratch()
        try:
            if mut == "base":
                m_base(d)
            elif mut is not None:
                edit_drafts(d, mut)
            rc, out = run(d)
            if mut is None:
                got = open(os.path.join(d, STAGE, MAP), "rb").read() if rc == 0 else b""
                ok = rc == 0 and got == committed
                seen = "wrote %s, %s the committed file" % (md5b(got)[:8], "equal to" if got == committed else "NOT equal to")
            else:
                ok = rc != 0 and want in out
                seen = "refused, naming its own check" if ok else "rc=%d; expected %r in the refusal" % (rc, want)
        finally:
            shutil.rmtree(d)
        print("%-66s %s" % (name, "as expected" if ok else "UNEXPECTED: " + seen))
        results.append({"control": name, "expect": "writes the committed bytes" if mut is None
                        else "refuses, naming %r" % want, "as_expected": ok})
        good += ok
        if mut is None and not ok:
            print("CONTROLS: the unmutated control failed first; nothing after it means anything")
            return 1
    rec = {"artifact": "assembly_control_v0_4.json",
           "instrument": "adversarial_map_staging/controls_assembly_v1_4.py",
           "builder": "adversarial_map_staging/" + BUILDER,
           "map": {"file": "adversarial_map_staging/" + MAP, "md5": md5b(committed), "bytes": len(committed)},
           "result": "%d of %d controls as expected, the unmutated control first" % (good, len(CONTROLS)),
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
