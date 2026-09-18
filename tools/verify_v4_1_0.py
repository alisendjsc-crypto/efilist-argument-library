#!/usr/bin/env python3
"""verify_v4_1_0.py -- post-sweep gate for the v4.1.0 cut. Run from the repo root.

This exists for the reason verify_v4_0_1.py existed, in its author's words: "the greps
prove the named strings moved, they do NOT prove that nothing ELSE moved." It reads the
base from GIT, not from disk -- a different instrument from the sweep's own section 2,
which compares against the in-memory pre-edit copy. Two instruments that fail differently
is the point; agreeing for the same wrong reason is what a single check cannot rule out.

Identity is asserted git-to-git by BLOB SHA (`git rev-parse HEAD:<path>`), never by piping
a blob through the shell -- ccclix: PowerShell's `>` re-encodes, and a hash of a redirect
describes the redirect.

  python3 tools/verify_v4_1_0.py                 # gate k344_drop against HEAD
  python3 tools/verify_v4_1_0.py --dir .         # gate the working tree (post Move-Item)
"""
import argparse, hashlib, io, os, subprocess, sys

JSONF = "efilist_argument_library_v4_0_0.json"
JSXF  = "efilist_argument_library_v4_0_0.jsx"
HTMLF = "combined.html"

# Base pins -- what HEAD must still be when this runs. If HEAD has already moved past the
# cut, this gate is meaningless and says so rather than passing vacuously.
BASE = {
    JSONF: ("6ee1f6f31e0f012db0d58cae4f912fcb", 1333912),
    JSXF:  ("b7dadfc39d988d643c408b3329ffcb54", 1273371),
    HTMLF: ("cee25a00b68ba036138d064c383d9a8b", 2982658),
}
NEW = {
    JSONF: ("04bf6482aa0374ee92a81c1d55ec41f8", 1334024),
    JSXF:  ("b196548b6eb39065842d62292acca89f", 1273483),
    HTMLF: ("72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770),
}
LOCI = {JSONF: [3, 91, 94, 581, 1756], JSXF: [79, 82, 569, 1744], HTMLF: [2930, 2933, 3420, 4595]}

GONE = [
    "roughly half of your capacity for happiness was determined at conception",
    "has never been substantively refuted",
    "Roughly one deployment in a hundred is a person actually worried about you",
    "The one-in-a-hundred who genuinely worries is making the argument-level case",
    "The ninety-nine are doing neither; they have changed the subject.",
    "roughly one deployment in a hundred is genuine worry",
    "the smallest slice of the pie",
]
HELD = [
    "Second, the neurochemical reality",
    "Terror Management Theory formalized them empirically",
    "; they have changed the subject.",
    "Hold the honest remainder:",
    "and that person gets met in good faith",
]

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default="k344_drop")
a = ap.parse_args()

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + got) if got and not cond else ""))
    if not cond: fail += 1

def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ABORT: git %s failed: %s" % (" ".join(args), r.stderr.decode()[:200]))
    return r.stdout

print("VERIFY v4.1.0 -- candidate %s vs git HEAD %s\n"
      % (os.path.abspath(a.dir), git("rev-parse", "--short", "HEAD").decode().strip()))

for p in (JSONF, JSXF, HTMLF):
    # --- the base is still the base, proven git-to-git ---------------------------------
    head_blob = git("rev-parse", "HEAD:%s" % p).decode().strip()
    base_bytes = git("cat-file", "blob", head_blob)
    b5, bn = hashlib.md5(base_bytes).hexdigest(), len(base_bytes)
    chk("%s: HEAD blob is still the pre-cut base" % p, (b5, bn) == BASE[p], "%s / %d" % (b5, bn))

    # --- the candidate is what the sweep said it was -----------------------------------
    cand = io.open(os.path.join(a.dir, p), encoding="utf-8", newline="").read()
    cb = cand.encode("utf-8")
    c5, cn = hashlib.md5(cb).hexdigest(), len(cb)
    chk("%s: candidate md5 %s" % (p, NEW[p][0]), (c5, cn) == NEW[p], "%s / %d" % (c5, cn))
    chk("%s: candidate is CR-free" % p, b"\r" not in cb)

    # --- the changed set is EXACTLY the named loci, and nothing else -------------------
    B = base_bytes.decode("utf-8").split("\n")
    N = cand.split("\n")
    chk("%s: line count unchanged at %d" % (p, len(B)), len(B) == len(N), "%d -> %d" % (len(B), len(N)))
    if len(B) == len(N):
        diff = [i + 1 for i, (x, y) in enumerate(zip(B, N)) if x != y]
        chk("%s: EXACTLY the named loci differ, nothing else" % p, diff == LOCI[p], repr(diff))

    # --- GONE / HELD -------------------------------------------------------------------
    for s in GONE:
        chk("%s: gone %r" % (p, s[:40]), cand.count(s) == 0, str(cand.count(s)))
    for s in HELD:
        chk("%s: held %r x1" % (p, s[:40]), cand.count(s) == 1, str(cand.count(s)))
    print()

# --- the flagship is the pin: say so out loud ------------------------------------------
print("  PIN: %s  %s -> %s  (%+d bytes)"
      % (HTMLF, BASE[HTMLF][0], NEW[HTMLF][0], NEW[HTMLF][1] - BASE[HTMLF][1]))
print("\nVERIFY GATE: " + ("RED -- %d failure(s)" % fail if fail else "GREEN"))
sys.exit(1 if fail else 0)
