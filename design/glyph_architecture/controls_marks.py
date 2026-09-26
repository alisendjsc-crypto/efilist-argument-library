#!/usr/bin/env python3
"""controls_marks.py -- mutation controls for the front-door marks gate (design lane, 2026-09-25).

tools/icons_regen_check.py now also requires the three generated regions of site/libraries/index.html to
be byte for byte what icons/gen_icons.py draws from the pinned icons/sigils.json. A gate that has never
been seen to fail proves nothing, so each control below copies the inputs into a scratch root, applies ONE
mutation, runs the check against that root, and requires its exit code AND its own failure message. The
unmutated control runs first. Nothing in the repo is touched.

  python3 design/glyph_architecture/controls_marks.py    # writes controls_marks_v0_1.json beside itself
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["icons/gen_icons.py", "icons/sigils.json", "tools/icons_regen_check.py", "site/libraries/index.html"] + \
        sorted("site/" + f for f in os.listdir(os.path.join(REPO, "site")) if f.startswith("icon-") and f.endswith(".svg"))
PAGE = "site/libraries/index.html"
LADDER = "[[2, 1, 12, 2, 'lit'], [2, 4, 10, 2, 'chrome'], [2, 7, 8, 2, 'chrome'], [2, 10, 6, 2, 'chrome'], [2, 13, 4, 2, 'chrome']]"

def md5(b): return hashlib.md5(b).hexdigest()

def sub(path, old, new, count=1):
    def f(root):
        p = os.path.join(root, path); s = open(p, "rb").read()
        assert s.count(old) >= count, (path, old)
        open(p, "wb").write(s.replace(old, new, count))
    return f

def after_tiers(line):   # patch the scratch generator right after it loads the pinned grids
    return sub("icons/gen_icons.py", b"assert sorted(TIERS) == [1, 2, 3, 4, 5], sorted(TIERS)\n",
               b"assert sorted(TIERS) == [1, 2, 3, 4, 5], sorted(TIERS)\n" + line.encode() + b"\n")

CONTROLS = [
    ("C0 unmutated", None, [], 0, ["ICONS: 7 of 7", "MARKS: 3 of 3"]),
    ("C1 a pixel in the plate region changes role", sub(PAGE, b'<rect class="sg-lit" x="90"', b'<rect class="sg-c" x="90"'),
     [], 1, ["DIFF  marks-plate", "MARKS: RED -- 1 difference(s)"]),
    ("C2 a says-line in the rows region is edited", sub(PAGE, b"which stays standing", b"which stands"),
     [], 1, ["DIFF  marks-rows", "MARKS: RED -- 1 difference(s)"]),
    ("C3 the mini region's opening marker is gone", sub(PAGE, b"<!-- gen_icons.py:mini -->\n", b""),
     [], 1, ["DIFF  marks-mini", "markers not found in the page"]),
    ("C4 the rows region's opening marker appears twice",
     sub(PAGE, b"<!-- gen_icons.py:rows -->\n", b"<!-- gen_icons.py:rows -->\n<!-- gen_icons.py:rows -->\n"),
     [], 1, ["DIFF  marks-rows", "markers not found in the page"]),
    ("C5 one byte of the vendored sigils.json changes", sub("icons/sigils.json", b'"version":"1.0.0"', b'"version":"1.0.1"'),
     [], 1, ["ICONS: RED -- gen_icons.py refused to draw", "not the pinned copy"]),
    ("C6 a tier drawn as the flagship's ladder, top rung lit (L1a)", after_tiers("TIERS[4]['rects'] = " + LADDER),
     [], 1, ["ICONS: RED -- gen_icons.py refused to draw", "two marks share a silhouette"]),
    ("C7 the plate's mark changes under its labels", after_tiers("TIERS[3]['rects'][0][1] = 0"),
     [], 1, ["ICONS: RED -- gen_icons.py refused to draw", "plate labels"]),
    ("C8 a served favicon changes", sub("site/icon-veganism.svg", b"</svg>\n", b"</svg>\n\n"),
     [], 1, ["DIFF  veganism", "ICONS: RED -- 1 difference(s)"]),
    ("C9 --write-marks restores C1's page byte for byte",
     sub(PAGE, b'<rect class="sg-lit" x="90"', b'<rect class="sg-c" x="90"'),
     ["--write-marks"], 0, ["wrote  site/libraries/index.html", "MARKS: 3 of 3"]),
]

record = {"artifact": "controls_marks", "version": "0.1", "gate": "tools/icons_regen_check.py",
          "inputs": {f: md5(open(os.path.join(REPO, f), "rb").read()) for f in FILES}, "controls": []}
fails = 0
for name, mutate, flags, want_rc, want in CONTROLS:
    root = tempfile.mkdtemp(prefix="marks_ctl_")
    try:
        for f in FILES:
            os.makedirs(os.path.dirname(os.path.join(root, f)), exist_ok=True)
            shutil.copyfile(os.path.join(REPO, f), os.path.join(root, f))
        if mutate: mutate(root)
        run = subprocess.run([sys.executable, os.path.join(root, "tools/icons_regen_check.py"), root] + flags,
                             capture_output=True, text=True)
        text = run.stdout + run.stderr
        ok = run.returncode == want_rc and all(w in text for w in want)
        if name.startswith("C9"):   # the splice must restore the ORIGINAL page, not merely a passing one
            ok = ok and md5(open(os.path.join(root, PAGE), "rb").read()) == record["inputs"][PAGE]
    finally:
        shutil.rmtree(root)
    fails += not ok
    record["controls"].append({"control": name, "flags": flags, "want_rc": want_rc, "rc": run.returncode,
                               "want": want, "as_expected": ok})
    print("  %s  %s  (rc %d)" % ("ok  " if ok else "FAIL", name, run.returncode))
    if not ok: print(text)
record["summary"] = "%d of %d controls as expected" % (len(CONTROLS) - fails, len(CONTROLS))
open(os.path.join(HERE, "controls_marks_v0_1.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps(record, indent=1, sort_keys=True) + "\n")
print("CONTROLS: " + record["summary"])
sys.exit(1 if fails else 0)
