#!/usr/bin/env python3
"""restamp_v4_0_1.py — COWORK EXECUTION ORDER section 4a, phase 2.

Runs AFTER sweep_v4_0_1.py: every surface here needs the new md5, which does not exist
until combined.html is written. Each edit asserts its anchor and aborts the whole pass on
any failure.

TWO of the order's named targets are NOT re-stamped, deliberately:
  * rebuttal_grading_ledger.json has no version field (keys: artifact, status, method,
    rubric_ref, ungraded, grades, archetype_variant_grades). Nothing to stamp.
  * the .jsx's only "4.0.0" is a HISTORICAL provenance line — "v4.0.0 cut folded at K219
    (2026-07-11)" — which is true. Stamping it to 4.0.1 would make a true sentence false,
    which is the L1722 error class this order exists to avoid. Reported, not forced.
"""
import hashlib, io, json, sys

NEW_MD5 = hashlib.md5(io.open("combined.html", encoding="utf-8", newline="").read().encode("utf-8")).hexdigest()
NEW_BYTES = len(io.open("combined.html", encoding="utf-8", newline="").read().encode("utf-8"))
OLD_MD5, OLD_BYTES = "e654eabd32fa95e5969d49e6eb15aa87", "2,963,752"
NB = "{:,}".format(NEW_BYTES)
print("stamping v4.0.1 · md5 %s · %s bytes" % (NEW_MD5, NB))

def edit(path, subs, line_hints=()):
    s = io.open(path, encoding="utf-8", newline="").read()
    for old, new in subs:
        n = s.count(old)
        if n != 1:
            sys.exit("ABORT %s: anchor %r occurs %d×, expected 1" % (path, old[:60], n))
        s = s.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("  ok %s (%d edit%s)" % (path, len(subs), "" if len(subs) == 1 else "s"))

# --- README: pin table + the stale grade line -----------------------------------------
edit("README.md", [
    ("| Version (pin) | `v4.0.0` |", "| Version (pin) | `v4.0.1` |"),
    ("| md5 | `%s` |" % OLD_MD5,
     "| md5 | `%s` |" % NEW_MD5),
    ("| Size | `%s` bytes |" % OLD_BYTES, "| Size | `%s` bytes |" % NB),
    ("Grade distribution (long, n=81): **A 36 / B 34 / C 11 / 0 ungraded**",
     "Grade distribution (long, n=82): **A 28 / B 53 / C 1 / 0 ungraded**"),
])

# --- libraries front door -------------------------------------------------------------
edit("libraries_index.html", [("<span>pinned v4.0.0</span>", "<span>pinned v4.0.1</span>")])

# --- corpus version field (filename stays frozen, per convention) ----------------------
p = "efilist_argument_library_v4_0_0.json"
raw = io.open(p, encoding="utf-8", newline="").read()
d = json.loads(raw)
if d.get("version") != "4.0.0":
    sys.exit("ABORT corpus: version is %r, expected '4.0.0'" % d.get("version"))
n = raw.count('"version": "4.0.0"')
if n != 1:
    sys.exit("ABORT corpus: '\"version\": \"4.0.0\"' occurs %d×, expected 1" % n)
io.open(p, "w", encoding="utf-8", newline="").write(raw.replace('"version": "4.0.0"', '"version": "4.0.1"', 1))
print("  ok %s (version field only; bytes otherwise untouched)" % p)
print("\nDONE — README, libraries/index.html, corpus. CHANGELOG entry is written separately.")
