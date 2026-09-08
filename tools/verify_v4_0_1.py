#!/usr/bin/env python3
"""verify_v4_0_1.py — post-mutation gate for the v4.0.1 sweep. Run from the repo root.

Stronger than the order's section-3 greps, and it exists because the video seat ran the
check I had not: the greps prove the named strings moved, they do NOT prove that nothing
ELSE moved. This diffs the working file against `git show HEAD:combined.html` line by line
and asserts the changed set is exactly the seven loci the order names.

  python3 tools/verify_v4_0_1.py          # before commit: HEAD is still the pre-sweep pin
"""
import hashlib, io, json, subprocess, sys

EXPECT_LINES = [1650, 1652, 1727, 1783, 1873, 2469, 10536]
BASE_MD5, NEW_MD5 = "e654eabd32fa95e5969d49e6eb15aa87", "9d13359e305c6caa3ae64759f3dcc0e6"
NEW_BYTES, LINES = 2963789, 12212
FROZEN = {10529: 43833, 10532: 52494, 10594: 1007967}
GONE = ["catalogs 81 ways", "close reading of all 81 entries",
        "<span>81</span> OBJECTIONS", "sole drag on 32 of 81"]
HELD = ["original 81 objections", "<span>35</span> MECHANISMS"]

fail = 0
def chk(name, cond, got=""):
    global fail
    if cond: print("  ok   " + name)
    else:    fail += 1; print("  FAIL " + name + ("  " + got if got else ""))

new = io.open("combined.html", encoding="utf-8", newline="").read()
b = new.encode("utf-8")
chk("md5 == %s" % NEW_MD5, hashlib.md5(b).hexdigest() == NEW_MD5, hashlib.md5(b).hexdigest())
chk("byte count == %d" % NEW_BYTES, len(b) == NEW_BYTES, str(len(b)))

base = subprocess.run(["git", "show", "HEAD:combined.html"], capture_output=True).stdout.decode("utf-8")
chk("HEAD is still the pre-sweep pin (run me BEFORE commit)",
    hashlib.md5(base.encode("utf-8")).hexdigest() == BASE_MD5)
B, N = base.splitlines(), new.splitlines()
chk("line count unchanged at %d" % LINES, len(B) == len(N) == LINES, "%d / %d" % (len(B), len(N)))
if len(B) == len(N):
    diff = [i + 1 for i, (x, y) in enumerate(zip(B, N)) if x != y]
    chk("EXACTLY the seven named loci differ, and nothing else",
        diff == EXPECT_LINES, repr(diff))

for s in GONE: chk("swept: %r gone" % s, new.count(s) == 0, str(new.count(s)))
for s in HELD: chk("held:  %r count 1" % s, new.count(s) == 1, str(new.count(s)))
for n, want in FROZEN.items():
    got = len(N[n - 1].encode("utf-8"))
    chk("mega-literal L%d byte-identical (%d)" % (n, want), got == want, str(got))

# the loop-closing check: chrome and prose only, no data moved
for ln, en, el, extra in ((10529, 117, 142, None), (10532, 95, 255, ("strong", 167, "weak", 88))):
    s = N[ln - 1]
    d = json.loads(s[s.find("{"):s.rfind("}") + 1])          # strict decode, not a text search
    chk("L%d graph literal %d nodes / %d links" % (ln, en, el),
        len(d.get("nodes", [])) == en and len(d.get("links", [])) == el,
        "%d / %d" % (len(d.get("nodes", [])), len(d.get("links", []))))
    if extra:
        k1, v1, k2, v2 = extra
        c = {}
        for x in d["links"]: c[x.get("strength")] = c.get(x.get("strength"), 0) + 1
        chk("L%d links %s=%d %s=%d" % (ln, k1, v1, k2, v2), c.get(k1) == v1 and c.get(k2) == v2, repr(c))

print("\nV4.0.1 GATE: " + ("RED — %d failure(s)" % fail if fail else "GREEN"))
sys.exit(1 if fail else 0)
