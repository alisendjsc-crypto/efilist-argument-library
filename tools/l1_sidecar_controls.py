#!/usr/bin/env python3
"""l1_sidecar_controls.py -- the controls that prove the sidecar half of tools/xsurface_v4_1_0.py can
fail, and fails for the right reason. L1 (2026-09-25).

Each control copies the three surfaces and both sidecars into a fresh scratch tree, writes a stand-in
canon holding only `flagship_sidecars.pins` for the scratch sidecars (the gate reads nothing else from
canon), applies one mutation, runs the gate with --dir on that tree, and requires BOTH the exit code
AND the exact set of FAIL lines it names. A control that fails for a different reason than the one it
was built for is a failed control. The unmutated control runs first and must be GREEN with every path
resolved inside the scratch tree, so no later RED can come from a broken harness.

  python3 tools/l1_sidecar_controls.py     # -> tools/l1_sidecar_control_v0_1.json; exit 1 on any deviation
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GATE = os.path.join(HERE, "xsurface_v4_1_0.py")
OUT = os.path.join(HERE, "l1_sidecar_control_v0_1.json")
MGD, M1 = "sidecars/map_graph_data.json", "sidecars/map1_transitions.json"
COPY = ("efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx",
        "site/combined.html", MGD, M1)
CANON = "project_canon_v0_control.json"


def fresh():
    d = tempfile.mkdtemp(prefix="l1_ctl_")
    for rel in COPY:
        os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
        shutil.copyfile(os.path.join(REPO, rel), os.path.join(d, rel))
    pins = {}
    for rel in (MGD, M1):
        b = open(os.path.join(d, rel), "rb").read()
        pins[rel] = {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}
    json.dump({"flagship_sidecars": {"pins": pins}}, open(os.path.join(d, CANON), "w"))
    return d


def edit(d, rel, fn):
    p = os.path.join(d, rel)
    b = fn(open(p, "rb").read())
    open(p, "wb").write(b)


def resave(fn):
    """Parse the sidecar, mutate it, re-serialize it exactly as the generator does."""
    def go(b):
        x = json.loads(b.decode("utf-8")); fn(x)
        return (json.dumps(x, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return go


def once(old, new):
    def go(b):
        assert b.count(old) >= 1, old
        return b.replace(old, new, 1)
    return go


def in_literal(name, old, new):
    """Replace the first `old` that lies INSIDE the flagship's `var name = ...;` literal, nowhere else."""
    def go(b):
        s = b.decode("utf-8")
        i = s.index("var %s = " % name)
        j = s.index(old, i)
        k = s.index("\nvar ", i + 1)
        assert j < k, "%r is not inside %s" % (old, name)
        return (s[:j] + new + s[j + len(old):]).encode("utf-8")
    return go


def drop_last_link(x): x["data"]["links"].pop()
def flip_weight(x):
    e = x["data"][next(iter(x["data"]))]["sophisticate"][0]
    e["weight"] = "LOW" if e["weight"] != "LOW" else "HIGH"


PIN_M1 = lambda d: json.load(open(os.path.join(d, CANON)))["flagship_sidecars"]["pins"][M1]["md5"]

CONTROLS = [
    ("C0 unmutated", None, []),
    ("C1 one link dropped from the MAP_GRAPH_DATA sidecar",
     lambda d: edit(d, MGD, resave(drop_last_link)),
     ["%s data == the flagship's MAP_GRAPH_DATA" % MGD, "%s data_md5 describes its own data" % MGD,
      "%s is byte for byte what" % MGD, "%s == its canon pin" % MGD]),
    ("C2 one Map 1 weight flipped in the sidecar",
     lambda d: edit(d, M1, resave(flip_weight)),
     ["%s data == the flagship's MAP1_TRANSITIONS" % M1, "%s data_md5 describes its own data" % M1,
      "%s is byte for byte what" % M1, "%s == its canon pin" % M1]),
    ("C3 whitespace only: one space before the sidecar's final newline (same JSON)",
     lambda d: edit(d, MGD, lambda b: b[:-2] + b" }\n" if b.endswith(b"}\n") else b + b"?"),
     ["%s is byte for byte what" % MGD, "%s == its canon pin" % MGD]),
    ("C4 one character of a mechanism label changed inside the flagship's MAP_GRAPH_DATA",
     lambda d: edit(d, "site/combined.html",
                    in_literal("MAP_GRAPH_DATA", '"label":"Terror Management Theory"',
                               '"label":"Terror Management Theorx"')),
     ["%s data == the flagship's MAP_GRAPH_DATA" % MGD, "%s is byte for byte what" % MGD]),
    ("C5 one word of Map 1's served caveat changed in the flagship",
     lambda d: edit(d, "site/combined.html",
                    once(b"not measured frequencies;", b"not measured frequency;")),
     ["%s is byte for byte what" % M1]),
    ("C6 one hex digit of the Map 1 canon pin changed",
     lambda d: edit(d, CANON, lambda b: b.replace(PIN_M1(d).encode(),
                                                  (("0" if PIN_M1(d)[0] != "0" else "1") + PIN_M1(d)[1:]).encode())),
     ["%s == its canon pin" % M1]),
    ("C7 a second canon file beside the first",
     lambda d: shutil.copyfile(os.path.join(d, CANON), os.path.join(d, "project_canon_v0_control2.json")),
     ["exactly one project_canon_v*.json", "%s == its canon pin" % MGD, "%s == its canon pin" % M1]),
    ("C8 the MAP_GRAPH_DATA sidecar absent from --dir resolves to the repo's own copy",
     lambda d: os.remove(os.path.join(d, MGD)), []),
]


def fails(out):
    return [l[len("  FAIL "):] for l in out.splitlines() if l.startswith("  FAIL ")]


def main():
    rows, bad = [], 0
    for name, mutate, expect in CONTROLS:
        d = fresh()
        try:
            if mutate:
                mutate(d)
            r = subprocess.run([sys.executable, GATE, "--dir", d], capture_output=True, text=True)
            out = r.stdout + r.stderr
            got = fails(out)
            matched = sorted(e for e in expect if any(g.startswith(e) for g in got))
            stray = [g for g in got if not any(g.startswith(e) for e in expect)]
            paths = re.findall(r"^  (?:canon|sidecar)  +(.*)$", r.stdout, flags=re.M)
            inside = [p.startswith(d + os.sep) for p in paths]
            if name.startswith("C8"):     # the sidecar falls back to the repo's copy; canon stays in scratch
                where_ok = inside == [True, False, True] and paths[1] == os.path.join(REPO, MGD)
            elif name.startswith("C7"):   # two canon files: none is chosen
                where_ok = len(paths) == 3 and paths[0] == "?" and all(inside[1:])
            else:
                where_ok = len(paths) == 3 and all(inside)
            ok = (r.returncode == (1 if expect else 0) and matched == sorted(expect) and not stray
                  and where_ok and r.stdout.rstrip().endswith("GREEN" if not expect else "failure(s)"))
        finally:
            shutil.rmtree(d)
        bad += not ok
        rows.append({"control": name, "expected_rc": 1 if expect else 0, "rc": r.returncode,
                     "expected_fails": expect, "observed_fails": [g.split("  ")[0] for g in got],
                     "paths_resolved_as_intended": where_ok,
                     "verdict": "AS EXPECTED" if ok else "DEVIATION"})
        print("%-11s %s  rc=%d  fails=%d  %s" % ("AS EXPECTED" if ok else "DEVIATION", name[:3], r.returncode,
                                                 len(got), name[3:]))
    rec = {"artifact": "l1_sidecar_control_v0_1",
           "gate": {"path": "tools/xsurface_v4_1_0.py",
                    "md5": hashlib.md5(open(GATE, "rb").read()).hexdigest()},
           "method": ("Each control copies the three surfaces and both sidecars into a fresh scratch tree, "
                      "writes a stand-in canon holding only flagship_sidecars.pins, applies one mutation, "
                      "runs the gate with --dir, and requires the exit code, the exact set of FAIL lines "
                      "and the resolved paths. C0 runs first."),
           "controls": rows,
           "summary": "%d of %d as expected" % (len(rows) - bad, len(rows))}
    open(OUT, "w", encoding="utf-8").write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    print(rec["summary"])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
