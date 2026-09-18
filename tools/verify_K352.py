#!/usr/bin/env python3
"""verify_K352.py -- post-sweep gate for the level-independent affordance. Run from the repo root.

A DIFFERENT INSTRUMENT from the sweep's own assertions, which is the point: the sweep compares
against the file it read off disk; this reads the base from GIT BLOBS (`git rev-parse HEAD:<path>`)
and never trusts the worktree. Two instruments that fail differently is what a single check cannot
give you.

And it is stronger than the K344 verifier it descends from. verify_v4_1_0.py asserted "the changed
LINES are exactly the named loci", which only works when the line count is unchanged. This cut
INSERTS, so the gate instead RECONSTRUCTS: it re-applies the sweep's declared edit list to the git
base and asserts the result is byte-identical to the candidate. That proves the candidate IS the
base plus exactly these operations -- not merely that the operations are among the changes.

  python3 tools/verify_K352.py                # gate k352_drop against HEAD
  python3 tools/verify_K352.py --dir .        # gate the working tree (post Copy-Item)
"""
import argparse, hashlib, importlib.util, io, os, subprocess, sys
sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTMLF = "combined.html"
JSONF = "efilist_argument_library_v4_0_0.json"
JSXF  = "efilist_argument_library_v4_0_0.jsx"

BASE = ("72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770)      # the pin, v4.1.0
NEW  = ("f095c0ce0e5a1d796d57fa5a5dd62f7d", 2985989)      # the pin, v4.1.1
HELD_SURFACES = {JSONF: ("04bf6482aa0374ee92a81c1d55ec41f8", 1334024),
                 JSXF:  ("b196548b6eb39065842d62292acca89f", 1273483)}
XSURF = "6cd132ee5b8c7ca78ad0e095806f1c93"   # canonical-serialization md5, all three surfaces

# import the sweep's own edit list rather than re-typing it (ccclxii: never hand-type a value the
# machine also computes -- and a divergence between builder and gate is the failure this avoids)
_spec = importlib.util.spec_from_file_location("_sw", os.path.join(ROOT, "tools", "affordance_K352.py"))

ap = argparse.ArgumentParser(); ap.add_argument("--dir", default="k352_drop"); a = ap.parse_args()

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + got) if got and not cond else ""))
    if not cond: fail += 1

def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit("ABORT: git %s failed: %s" % (" ".join(args), r.stderr.decode()[:200]))
    return r.stdout

head = git("rev-parse", "--short", "HEAD").decode().strip()
print("VERIFY K352 -- candidate %s vs git HEAD %s\n" % (os.path.abspath(a.dir), head))

# --- 1. the base is still the base, git-to-git ----------------------------------------
blob = git("rev-parse", "HEAD:%s" % HTMLF).decode().strip()
base_bytes = git("cat-file", "blob", blob)
b5, bn = hashlib.md5(base_bytes).hexdigest(), len(base_bytes)
chk("%s: HEAD blob is still the v4.1.0 pin" % HTMLF, (b5, bn) == BASE, "%s / %d" % (b5, bn))

for p, (m, n) in HELD_SURFACES.items():
    bb = git("cat-file", "blob", git("rev-parse", "HEAD:%s" % p).decode().strip())
    chk("%s: HEAD blob UNMOVED (no corpus byte in this cut)" % p,
        (hashlib.md5(bb).hexdigest(), len(bb)) == (m, n))

# --- 2. the candidate is what the sweep said it was ------------------------------------
cand = io.open(os.path.join(ROOT, a.dir, HTMLF), "rb").read()
c5, cn = hashlib.md5(cand).hexdigest(), len(cand)
chk("%s: candidate md5 %s" % (HTMLF, NEW[0]), (c5, cn) == NEW, "%s / %d" % (c5, cn))
chk("%s: candidate is CR-free" % HTMLF, b"\r" not in cand)

# --- 3. RECONSTRUCTION: base + exactly the declared edits == candidate ------------------
sw = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(sw)      # the sweep re-runs its own gate on import; harmless
except SystemExit:
    pass
lines = base_bytes.decode("utf-8").split("\n")
for tag, ln, kind, old, new in sw.EDITS:
    chk("reconstruct: %-16s L%-6d anchor holds in the GIT BASE" % (tag, ln), lines[ln - 1] == old)
out = list(lines)
for tag, ln, kind, old, new in sorted(sw.EDITS, key=lambda e: -e[1]):
    if kind == "R": out[ln - 1] = new
    else:           out.insert(ln, new)
rb = "\n".join(out).encode("utf-8")
chk("RECONSTRUCTION: git base + exactly the %d declared edits == candidate, byte for byte"
    % len(sw.EDITS), rb == cand, hashlib.md5(rb).hexdigest())

# --- 4. the data did not move: the cross-surface gate must read IDENTICALLY -------------
import tempfile, shutil
tmp = tempfile.mkdtemp()
shutil.copy(os.path.join(ROOT, a.dir, HTMLF), os.path.join(tmp, HTMLF))
for p in HELD_SURFACES: shutil.copy(os.path.join(ROOT, p), os.path.join(tmp, p))
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "xsurface_v4_1_0.py"), "--dir", tmp],
                   capture_output=True, cwd=ROOT)
xo = r.stdout.decode()
shutil.rmtree(tmp, ignore_errors=True)
chk("x-surface gate GREEN on the candidate", r.returncode == 0)
chk("x-surface md5 IDENTICAL to the base at %s -- the mechanical proof this cut touched NO DATA"
    % XSURF, xo.count(XSURF) == 3, repr([l.strip() for l in xo.splitlines() if "canon" in l]))

# --- 5. the register invariants -------------------------------------------------------
c = cand.decode("utf-8")
chk("the default is NOT flipped", c.count('let responseLevel = "medium";') == 1)
chk("boot still calls setDepth('medium')", c.count("  setDepth('medium');") == 1)
chk("the [NOTE] confidence coupling is UNTOUCHED (queued, not repaired)",
    c.count("if (conf !== 'full') {") == 1 and
    c.count("const hasNote = obj.note && responseLevel === 'long';") == 1)
chk("archetypeSel untouched (D7)", c.count("let archetypeSel = {};") == 1)
chk("exactly one card-anchor router", c.count("window.__arglibRouteObj = function") == 1)
# the comment in CSS_BLOCK NAMES the eight invalid literals it declines to repeat, so scan the
# DECLARATIONS only -- the first cut of this check scanned the comment too and convicted the gate
# rather than the bytes, which is the third time this session a check's model of its own subject
# was the thing that was wrong.
_re = __import__("re")
_decls = _re.sub(r"/\*.*?\*/", "", sw.CSS_BLOCK, flags=_re.S)
_hex = _re.findall(r"#([0-9a-fA-F]+)\b", _decls)
chk("no 5-digit hex in this cut's CSS declarations (%d literals, all 3- or 6-digit)" % len(_hex),
    _hex and all(len(t) in (3, 6) for t in _hex), repr([t for t in _hex if len(t) not in (3, 6)]))
# assert the DECLARATION LINES survive verbatim, not the literals -- this cut's comment names
# four of them, so a raw occurrence count is 2 and says nothing. (The reconstruction check above
# already implies this; it is restated because a receipt a reader can check by eye is worth a line.)
for _l in [".confidence-full { color: #4a7; border: 1px solid #4a733; background: #4a711; }",
           ".confidence-strong { color: #c90; border: 1px solid #c9033; background: #c9011; }",
           ".confidence-provisional { color: #c55; border: 1px solid #c5533; background: #c5511; }",
           "  background: none; border: 1px solid #33200; color: #996;"]:
    chk("pre-existing invalid-hex line survives verbatim: %r" % _l[:44], c.count(_l) == 1, str(c.count(_l)))

print("\n  PIN: %s  %s / %d  ->  %s / %d  (%+d bytes)"
      % (HTMLF, BASE[0], BASE[1], NEW[0], NEW[1], NEW[1] - BASE[1]))
print("\nVERIFY K352: " + ("RED -- %d failure(s)" % fail if fail else "GREEN"))
sys.exit(1 if fail else 0)
