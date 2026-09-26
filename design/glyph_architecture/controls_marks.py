#!/usr/bin/env python3
"""controls_marks.py -- mutation controls for the front-door marks gate (design lane, 2026-09-25).

tools/icons_regen_check.py now also requires the generated regions of site/libraries/index.html to
be byte for byte what icons/gen_icons.py draws from the pinned icons/sigils.json. A gate that has never
been seen to fail proves nothing, so each control below copies the inputs into a scratch root, applies ONE
mutation, runs the check against that root, and requires its exit code AND its own failure message. The
unmutated control runs first. Nothing in the repo is touched.

  python3 design/glyph_architecture/controls_marks.py    # writes controls_marks_v0_3.json beside itself (v0_2 on main)

v0_2 (LD2, 2026-09-26): the gate now checks six pages against the manifest gen_icons.py writes (the front
door and the five wings). C10 is retargeted at the abortion card's mark as it is now drawn (it carries its
one-shot), and C12-C19 prove each new way a page can drift: a wing's title mark, a plate's part name, one
page's copy of the shared stylesheet, a region planted on the wrong page, a missing template, a wing grid
changed under its plate's labels, a one-shot that moves a rect twice, and a missing page. A want item that
starts with "re:" is a regular expression. v0_1 is LD1's record and stays as it was.

v0_3 (the flagship package, branch design/marks-flagship; lands only with a declared pin move): the flagship is
the seventh page, and C20 proves its own stylesheet cannot drift. v0_2 stays main's record.
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
WINGS = ["right-to-die", "abortion", "transgenderism", "anthropocentrism", "veganism"]
FILES = ["icons/gen_icons.py", "icons/sigils.json", "tools/icons_regen_check.py", "site/libraries/index.html"] + \
        ["site/%s/combined.html" % w for w in WINGS] + ["site/combined.html"] + \
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

def gone(path):
    def f(root): os.remove(os.path.join(root, path))
    return f

def W(w): return "site/%s/combined.html" % w

CONTROLS = [
    ("C0 unmutated", None, [], 0, ["ICONS: 7 of 7", "MARKS: 41 of 41 regions on 7 pages"]),
    ("C1 a pixel in the plate region changes role", sub(PAGE, b'<rect class="sg-lit" x="90"', b'<rect class="sg-c" x="90"'),
     [], 1, ["re:DIFF  libraries +marks-plate ", "MARKS: RED -- 1 difference(s)"]),
    ("C2 a says-line in the rows region is edited", sub(PAGE, b"which stays standing", b"which stands"),
     [], 1, ["re:DIFF  libraries +marks-rows ", "MARKS: RED -- 1 difference(s)"]),
    ("C3 the mini region's opening marker is gone", sub(PAGE, b"<!-- gen_icons.py:mini -->\n", b""),
     [], 1, ["re:DIFF  libraries +marks-mini +markers not found in the page"]),
    ("C4 the rows region's opening marker appears twice",
     sub(PAGE, b"<!-- gen_icons.py:rows -->\n", b"<!-- gen_icons.py:rows -->\n<!-- gen_icons.py:rows -->\n"),
     [], 1, ["re:DIFF  libraries +marks-rows +markers not found in the page"]),
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
     ["--write-marks"], 0, ["wrote  site/libraries/index.html", "MARKS: 41 of 41"]),
    ("C10 a library's mark on its card changes",
     sub(PAGE, b'<rect class="sg-lit m-fill" style="--d:0.5s" x="10" y="11"', b'<rect class="sg-c m-fill" style="--d:0.5s" x="10" y="11"'),
     [], 1, ["re:DIFF  libraries +marks-lib-abortion ", "MARKS: RED -- 1 difference(s)"]),
    ("C11 the page carries a region the generator does not draw",
     sub(PAGE, b"    </aside>\n", b"<!-- gen_icons.py:ghost -->\n<!-- /gen_icons.py:ghost -->\n    </aside>\n"),
     [], 1, ["re:DIFF  libraries +marks-ghost +not drawn by gen_icons.py", "MARKS: RED -- 1 difference(s)"]),
    ("C12 a wing's title mark changes (the step goes dark)",
     sub(W("right-to-die"), b'<rect class="sg-lit m-fill" style="--d:0.6s"', b'<rect class="sg-c m-fill" style="--d:0.6s"'),
     [], 1, ["re:DIFF  right-to-die +marks-lib-right-to-die ", "MARKS: RED -- 1 difference(s)"]),
    ("C13 a plate's part name is edited on its page", sub(W("abortion"), b">lit &#183; a branch<", b">lit &#183; the branch<"),
     [], 1, ["re:DIFF  abortion +marks-plate-abortion ", "MARKS: RED -- 1 difference(s)"]),
    ("C14 one page's copy of the shared motion stylesheet drifts",
     sub(W("transgenderism"), b"animation-name:lm-fill;animation-duration:0.3s", b"animation-name:lm-fill;animation-duration:0.4s"),
     [], 1, ["re:DIFF  transgenderism +marks-lm-css ", "re:SAME  veganism +marks-lm-css ", "MARKS: RED -- 1 difference(s)"]),
    ("C15 a region drawn for another page is planted on a wing",
     sub(W("anthropocentrism"), b"</body>", b"<!-- gen_icons.py:plate-veganism -->\n<!-- /gen_icons.py:plate-veganism -->\n</body>"),
     [], 1, ["re:DIFF  anthropocentrism +marks-plate-veganism +drawn, but not for this page", "MARKS: RED -- 1 difference(s)"]),
    ("C16 a wing page loses its tier-mark template's markers",
     sub(W("veganism"), b"<!-- gen_icons.py:tier-marks -->\n", b""),
     [], 1, ["re:DIFF  veganism +marks-tier-marks +markers not found in the page"]),
    ("C17 a wing's grid changes under its plate's labels",
     sub("icons/gen_icons.py", b"R(1,6,4,4), R(5,7,6,2), R(11,6,4,4, ACC)", b"R(1,6,4,4), R(5,7,6,1), R(11,6,4,4, ACC)"),
     [], 1, ["ICONS: RED -- gen_icons.py refused to draw", "plate labels"]),
    ("C18 a one-shot moves one rect twice and leaves one still",
     sub("icons/gen_icons.py", b"[(0, 'fill', 0), (2, 'fill', 0), (1, 'dxm', .25)]", b"[(0, 'fill', 0), (0, 'fill', 0), (1, 'dxm', .25)]"),
     [], 1, ["ICONS: RED -- gen_icons.py refused to draw", "every rect moves exactly once"]),
    ("C19 a wing page is missing", gone(W("abortion")),
     [], 1, ["re:DIFF  site/abortion/combined.html +the page is missing", "MARKS: RED -- 1 difference(s)"]),
    ("C20 the flagship's copy of its marks stylesheet drifts (every tier lit in crimson)",
     sub("site/combined.html", b".sg-c{fill:#e8e4dd}.sg-lit{fill:var(--lit,#ef3a58)}", b".sg-c{fill:#e8e4dd}.sg-lit{fill:#ef3a58}"),
     [], 1, ["re:DIFF  combined.html +marks-flag-css ", "MARKS: RED -- 1 difference(s)"]),
]

record = {"artifact": "controls_marks", "version": "0.3", "gate": "tools/icons_regen_check.py",
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
        ok = run.returncode == want_rc and all(re.search(w[3:], text) if w.startswith("re:") else w in text for w in want)
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
open(os.path.join(HERE, "controls_marks_v0_3.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps(record, indent=1, sort_keys=True) + "\n")
print("CONTROLS: " + record["summary"])
sys.exit(1 if fails else 0)
