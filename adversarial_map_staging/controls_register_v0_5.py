#!/usr/bin/env python3
"""controls_register_v0_5.py -- prove build_register_v0_5.py's new gates by failing them (L4).

Copies the staging tree to scratch, mutates one thing, runs the builder there, and requires the
refusal to name its own check. The unmutated control runs first and must reproduce the committed
register byte for byte.

  python3 controls_register_v0_5.py            # run, write register_control_v0_3.json
  python3 controls_register_v0_5.py --check    # run, compare with the committed record
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STAGE = "adversarial_map_staging"
RECORD = os.path.join(HERE, "register_control_v0_3.json")
BUILDER = "build_register_v0_5.py"
OUT = "honest_residuals_register_v0_5.json"
MAP = "adversarial_map_v1_4.json"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def scratch():
    d = tempfile.mkdtemp(prefix="l4_regcontrols_")
    shutil.copytree(os.path.join(REPO, STAGE), os.path.join(d, STAGE),
                    ignore=shutil.ignore_patterns("__pycache__", "*.tmp"))
    return d


def run(d):
    env = dict(os.environ, K348_REPO=d, PYTHONDONTWRITEBYTECODE="1")
    env.pop("K348_MAP_DIR", None)
    p = subprocess.run([sys.executable, os.path.join(d, STAGE, BUILDER)], env=env,
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def edit_map(d, fn):
    p = os.path.join(d, STAGE, MAP)
    doc = json.load(open(p, encoding="utf-8"))
    fn(doc["entries"])
    open(p, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def amended(entries, n):
    return [e for e in entries if e["provenance"].get("amended", {}).get("r1_n") == n][0]


def m_relation(d):
    p = os.path.join(d, STAGE, BUILDER)
    s = open(p, encoding="utf-8").read()
    i = s.index('    "HR-12": ("independent_of", "HR-10",')
    j = s.index('    "HR-14": ("independent_of", "HR-05",')
    open(p, "w", encoding="utf-8").write(s[:i] + s[j:])


def m_from(d):
    def f(es):
        amended(es, 10)["provenance"]["amended"]["bedrock_from"] = "life-gift#long"
    edit_map(d, f)


def m_novel(d):
    def f(es):
        amended(es, 44)["routing"]["residue"]["novel"] = True
    edit_map(d, f)


def m_old(d):
    def f(es):
        e = [x for x in es if x["target_id"] == "solipsism" and x["class"] == "d"][0]
        e["routing"]["residue"]["terminus_routing"] += " (moved)"
    edit_map(d, f)


def m_newbid(d):
    p = os.path.join(d, STAGE, BUILDER)
    s = open(p, encoding="utf-8").read()
    s = s.replace("BEDROCK_MAP = dict(W.BEDROCK_MAP)\n",
                  "BEDROCK_MAP = dict(W.BEDROCK_MAP)\n"
                  "BEDROCK_MAP['epistemic authority of the anti-extinction intuition (Moorean datum) versus "
                  "its evolutionary debunking'] = ('HR-16', 'moorean-datum-vs-debunking')\n", 1)
    open(p, "w", encoding="utf-8").write(s)


def m_base(d):
    p = os.path.join(d, STAGE, "honest_residuals_register_v0_4.json")
    b = open(p, "rb").read()
    open(p, "wb").write(b.replace(b"HR-01", b"HR-0l", 1))


CONTROLS = [
    ("C0 unmutated", None, None),
    ("C1 one added relation removed (HR-12 independent_of HR-10)", m_relation, "UNDECLARED ADJACENCY"),
    ("C2 an amended (d)'s bedrock_from points at another bedrock (#10)", m_from, "resolves to"),
    ("C3 a reclassified tributary claims novel=true (#44)", m_novel, "claims novel=true"),
    ("C4 a v0_4 tributary's text moves in the source map", m_old, "its v0_4 tributaries moved"),
    ("C5 a shipped name resolves to an unregistered bedrock", m_newbid, "not registered"),
    ("C6 the predecessor register moved by one byte", m_base, "BASE GUARD"),
]


def main():
    committed = open(os.path.join(REPO, STAGE, OUT), "rb").read()
    results, good = [], 0
    for name, mut, want in CONTROLS:
        d = scratch()
        try:
            if mut is not None:
                mut(d)
            rc, out = run(d)
            if mut is None:
                got = open(os.path.join(d, STAGE, OUT), "rb").read() if rc == 0 else b""
                ok = rc == 0 and got == committed
            else:
                ok = rc != 0 and want in out
        finally:
            shutil.rmtree(d)
        print("%-66s %s" % (name, "as expected" if ok else "UNEXPECTED (rc=%d)" % rc))
        results.append({"control": name, "expect": "writes the committed bytes" if mut is None
                        else "refuses, naming %r" % want, "as_expected": ok})
        good += ok
        if mut is None and not ok:
            print("CONTROLS: the unmutated control failed first; nothing after it means anything")
            return 1
    rec = {"artifact": "register_control_v0_3.json",
           "instrument": "adversarial_map_staging/controls_register_v0_5.py",
           "builder": "adversarial_map_staging/" + BUILDER,
           "register": {"file": "adversarial_map_staging/" + OUT, "md5": md5b(committed), "bytes": len(committed)},
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
