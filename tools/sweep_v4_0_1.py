#!/usr/bin/env python3
"""sweep_v4_0_1.py — COWORK EXECUTION ORDER v4.0.1, section 1: the seven display-string loci.

A LINE-INDEXED pass with a per-line anchor assertion, as the order requires: not sed -i,
not a global regex. Any failed assertion aborts before anything is written.

Phase 1 only — `combined.html`. The version re-stamp (section 4a) is phase 2, because every
one of its surfaces needs the NEW md5, which does not exist until this file is written.
"""
import hashlib, io, sys

SRC = "combined.html"
PIN_MD5, PIN_BYTES, PIN_LINES = "e654eabd32fa95e5969d49e6eb15aa87", 2963752, 12212
FROZEN = {10529: 43833, 10532: 52494, 10594: 1007967}   # order section 0.4

# (n, 1-based line, anchor that must be present, replacement)
EDITS = [
    (1, 1727,  "<span>81</span> OBJECTIONS",       "<span>82</span> OBJECTIONS"),
    (2, 1727,  "<span>140</span> CONNECTIONS",     "<span>142</span> CONNECTIONS"),
    (3, 2469,  "catalogs 81 ways",                 "catalogs 82 ways"),
    (4, 1650,  "close reading of all 81 entries",  "close reading of all 82 entries"),
    (5, 1783,  "close reading of all 81 entries",  "close reading of all 82 entries"),
    (6, 1873,  "close reading of all 81 entries",  "close reading of all 82 entries"),
    # section 1 #7, the OPTIONAL UPGRADE, taken. Both figures were recomputed from
    # rebuttal_grading_ledger.json before splicing: robustness is the sole weakest axis on
    # 31 of 82 and ties for weakest on 34 more. The anchor is widened by one leading "and "
    # so the clause reads grammatically; the order's own anchor is asserted separately below.
    (7, 1652,  "and the sole drag on 32 of 81 nodes",
               "the sole weakest axis on 31 of 82 nodes and tying for weakest on 34 more"),
    (8, 10536, "stored sum 245 vs 254 links",      "stored sum 245 vs 255 links"),
]
# section 2 — must still be present, and untouched, afterwards
HELD = ["original 81 objections", "<span>35</span> MECHANISMS"]
# section 3 — post-edit greps, all must be 0
GONE = ["catalogs 81 ways", "close reading of all 81 entries",
        "<span>81</span> OBJECTIONS", "sole drag on 32 of 81"]

raw = io.open(SRC, encoding="utf-8", newline="").read()

# --- section 0 preconditions ---------------------------------------------------------
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
if md5 != PIN_MD5:
    sys.exit("ABORT 0.2: md5 %s != %s — every line number is keyed to that file" % (md5, PIN_MD5))
if len(raw.encode("utf-8")) != PIN_BYTES:
    sys.exit("ABORT 0.2: byte count %d != %d" % (len(raw.encode("utf-8")), PIN_BYTES))
lines = raw.splitlines(keepends=True)
if len(lines) != PIN_LINES:
    sys.exit("ABORT 0.3: %d lines != %d" % (len(lines), PIN_LINES))
for n, want in FROZEN.items():
    got = len(lines[n - 1].rstrip("\n").encode("utf-8"))
    if got != want:
        sys.exit("ABORT 0.4: L%d is %d bytes, recorded %d" % (n, got, want))
print("0 · preconditions MET — md5, %d bytes, %d lines, 3 mega-literals" % (PIN_BYTES, PIN_LINES))

# --- section 1 edits, asserted per line ----------------------------------------------
if lines[1651].count("the sole drag on 32 of 81 nodes") != 1:      # the order's own anchor
    sys.exit("ABORT 1.7: the order's anchor is not on L1652 exactly once")
for n, ln, anchor, repl in EDITS:
    L = lines[ln - 1]
    c = L.count(anchor)
    if c != 1:
        sys.exit("ABORT 1.%d: anchor %r occurs %d× on L%d, expected 1" % (n, anchor, c, ln))
    lines[ln - 1] = L.replace(anchor, repl, 1)
    print("  1.%d L%-6d ok" % (n, ln))

out = "".join(lines)

# --- section 3 post-edit verification, on the NEW text -------------------------------
for s in GONE:
    if out.count(s) != 0:
        sys.exit("ABORT 3: %r still present %d×" % (s, out.count(s)))
for s in HELD:
    if out.count(s) != 1:
        sys.exit("ABORT 3: held %r count %d, expected 1" % (s, out.count(s)))
new_lines = out.splitlines(keepends=True)
if len(new_lines) != PIN_LINES:
    sys.exit("ABORT 3: line count moved to %d" % len(new_lines))
for n, want in FROZEN.items():
    got = len(new_lines[n - 1].rstrip("\n").encode("utf-8"))
    if got != want:
        sys.exit("ABORT 3: mega-literal L%d moved %d -> %d" % (n, want, got))
print("3 · post-edit verification PASSED — 4 gone, 2 held, line count and 3 literals frozen")

io.open(SRC, "w", encoding="utf-8", newline="").write(out)
b = out.encode("utf-8")
print("\nnew_md5:        %s" % hashlib.md5(b).hexdigest())
print("new_byte_count: %d" % len(b))
