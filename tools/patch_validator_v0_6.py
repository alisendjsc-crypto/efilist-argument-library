#!/usr/bin/env python3
"""K349: derive adv_map_validator_v0_6.py from v0_5 by ANCHORED single-occurrence patches.

v0_5 is left byte-identical -- canon pins it and the v1_1 receipt names it.
Every anchor is asserted to occur EXACTLY once before substitution; a zero or a
duplicate aborts. Reads binary, decodes UTF-8 explicitly, consults no locale (ccclx).
"""
import os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_5.py")
V0_5_MD5 = "713da227ec4457eaf644996ef352ff20"

PATCHES = []
def P(tag, old, new):
    PATCHES.append((tag, old, new))

# ---- P1: the docstring check list ------------------------------------------------
P("docstring-checks",
"""  variant-coverage       IF meta declares variant_coverage "<hit>/<total>", it must equal THAT FILE's
                         own variant loci over the corpus total   [K347/ccclxx: was all loaded files]
""",
"""  variant-coverage       IF meta declares variant_coverage "<hit>/<total>", it must equal THAT FILE's
                         own variant loci over the corpus total   [K347/ccclxx: was all loaded files]
  note-coverage          NEW (K349) -- IF meta declares note_coverage "<hit>/<total>", it must equal
                         THAT FILE's own note loci over the corpus total. Per-file for the same
                         ccclxx reason variant-coverage is; note loci NEVER fold into variant_coverage
""")

# ---- P2: the locus enum and the phase enum ---------------------------------------
P("loci-constants",
'''VARIANT_PREFIX = "archetypeVariants."
VARIANT_SLOTS = ("sophisticate", "defender", "drifter", "blended")
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E", "F", "R")
''',
'''VARIANT_PREFIX = "archetypeVariants."
VARIANT_SLOTS = ("sophisticate", "defender", "drifter", "blended")
# K349 NOTE RULING (Josiah, delegated to this seat): `note` is a map target, NARROWLY --
# authored only where the note makes or concedes a claim the corpus would have to defend.
# It is a TOP-LEVEL node key, not `responses.note`, and it is NOT added to LOCI: the four
# primaries are accepted unconditionally because all 82 nodes carry all four, while only
# 9 carry a note. Putting `note` in LOCI would let a target_locus of "note" validate on a
# node that has none, and locus_text would hand the anchor rule an empty string -- the
# exact routing defect the K345 both-ways proof was written to catch. So it is
# EXISTENCE-GATED, like a variant slot.
NOTE_LOCUS = "note"
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E", "F", "R", "G")
''')

# ---- P3: locus_valid -------------------------------------------------------------
P("locus-valid",
'''    if locus in LOCI:
        return True
    s = variant_slot(locus)
''',
'''    if locus in LOCI:
        return True
    if locus == NOTE_LOCUS:
        return isinstance(node.get(NOTE_LOCUS), str) and node[NOTE_LOCUS].strip() != ""
    s = variant_slot(locus)
''')

# ---- P4: locus_text --------------------------------------------------------------
P("locus-text",
'''def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
''',
'''def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    if locus == NOTE_LOCUS:
        # TOP-LEVEL key. Reading it out of `responses` would return "" on every node and
        # make anchor-rule vacuously unsatisfiable rather than loudly wrong.
        return node.get(NOTE_LOCUS, "")
''')

# ---- P5: note_loci helper --------------------------------------------------------
P("note-loci-helper",
'''def node_variant_slots(node):
    return [s for s in VARIANT_SLOTS
            if s in (node.get("responses", {}).get("archetypeVariants") or {})]
''',
'''def node_variant_slots(node):
    return [s for s in VARIANT_SLOTS
            if s in (node.get("responses", {}).get("archetypeVariants") or {})]


def node_has_note(node):
    return isinstance(node.get(NOTE_LOCUS), str) and node[NOTE_LOCUS].strip() != ""
''')

# ---- P6: coverage excludes note loci, + the note-coverage check -------------------
P("coverage-and-note-coverage",
'''    covered = set(per_id) & ids
    missing = sorted(ids - covered)
''',
'''    # K349 RULING, made explicitly rather than carried by silence (ccclxxi). `coverage`
    # is the claim that every node's ARGUMENT was adjudicated. A note is apparatus
    # attached to a node, not the node's argument, so a node whose ONLY entry sits at
    # `#note` is not covered. Blast radius measured at the ruling: 0 -- every node in the
    # successor assembly carries a primary entry, and v1_0 and v1_1 hold no note entries
    # at all, so no shipped verdict moves. The alternative, leaving `coverage` keyed on
    # target_id alone, would have let a future phase satisfy 82/82 with apparatus.
    argued = set(tid for (tid, locus) in per_id_locus if locus != NOTE_LOCUS)
    covered = argued & ids
    missing = sorted(ids - covered)
''')

P("note-coverage-check",
'''    out("corpus: whole-file %s  objections-digest %s" % (cmd5[:12], odig[:12]))
    out("variant-coverage: %s archetypeVariants loci carry >=1 entry" % vc)
''',
'''    # K349: note_coverage is declared BY A FILE and gated against THAT FILE, for the same
    # reason variant_coverage is (ccclxx). Note loci are counted here and NOWHERE else --
    # they do not fold into variant_coverage, which is a claim about archetypeVariants.
    note_loci_total = sorted((n["id"], NOTE_LOCUS) for n in corpus["objections"]
                             if node_has_note(n))
    note_loci_hit = sorted(k for k in per_id_locus if k[1] == NOTE_LOCUS)
    nc = "%d/%d" % (len(set(note_loci_hit)), len(note_loci_total))
    for p, meta in metas:
        if "note_coverage" in meta:
            own = set()
            for e in file_entries.get(p, []):
                if isinstance(e, dict) and e.get("target_locus") == NOTE_LOCUS:
                    own.add((e.get("target_id"), NOTE_LOCUS))
            own_nc = "%d/%d" % (len(own), len(note_loci_total))
            note("note-coverage", meta["note_coverage"] == own_nc,
                 "%s: declared %r vs this file's %r (all loaded files: %s)"
                 % (p, meta["note_coverage"], own_nc, nc))
    out("corpus: whole-file %s  objections-digest %s" % (cmd5[:12], odig[:12]))
    out("variant-coverage: %s archetypeVariants loci carry >=1 entry" % vc)
    out("note-coverage: %s note loci carry >=1 entry" % nc)
''')

# ---- P7: header version line -----------------------------------------------------
P("header-version",
'''v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".''',
'''v0_6 (K349): target_locus reaches the top-level `note` key, EXISTENCE-GATED, for the
             narrow Phase G ruling; `coverage` is restricted to argued loci so apparatus
             cannot satisfy 82/82; note_coverage added, per-file per ccclxx; PHASES += G.
v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".''')

# ---- P9: the K349 control battery, carried in a sidecar --------------------------
# The battery is Python source containing triple-quoted strings, so it lives in
# tools/k349_validator_controls.txt rather than inline -- the K345 precedent.
def _load_battery():
    sp = os.path.join(HERE, "k349_validator_controls.txt")
    raw = open(sp, "rb").read().decode("utf-8")
    a = raw.split("===K349-OLD===\n", 1)[1]
    old, rest = a.split("===K349-NEW===\n", 1)
    new = rest.split("===K349-END===", 1)[0]
    return old.rstrip("\n"), new.rstrip("\n")

_b_old, _b_new = _load_battery()
P("k349-battery", _b_old, _b_new)


# ---- P10: name BOTH coverage quantities ------------------------------------------
# The K349 coverage ruling made `coverage_distinct_ids` mean two different things
# depending on where it is read. In meta it is gated against the distinct target_ids a
# FILE touches, at any locus; in the run summary it reports `covered`, which is what
# --terminal gates and which now excludes note-only nodes. Those were near-synonyms
# before the ruling and are not any more, so both are named rather than left to collide
# (ccclxxi: an invariant stated over the old unit is ruled explicitly, never by silence).
# Additive to the OUTPUT only -- no gate reads it, and no shipped artifact's verdict moves.
P("summary-names-both",
  '''                    "coverage_distinct_ids": len(covered), "terminal": terminal,''',
  '''                    "coverage_distinct_ids": len(covered),
                    "coverage_ids_touched": len(set(per_id) & ids), "terminal": terminal,''')


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == V0_5_MD5, "base v0_5 md5 %s != expected %s" % (got, V0_5_MD5)
    txt = raw.decode("utf-8")
    for tag, old, new in PATCHES:
        n = txt.count(old)
        assert n == 1, "anchor %r occurs %d times, expected exactly 1" % (tag, n)
        txt = txt.replace(old, new, 1)
        print("  patched %s" % tag)
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "adversarial_map_staging", "adv_map_validator_v0_6.py")
    out = txt.encode("utf-8")
    open(dest, "wb").write(out)
    print("wrote %s  %s  %d B" % (dest, hashlib.md5(out).hexdigest(), len(out)))
    # the base must be untouched by this run
    assert hashlib.md5(open(SRC, "rb").read()).hexdigest() == V0_5_MD5, "v0_5 was mutated"
    print("  v0_5 byte-identical: OK")

if __name__ == "__main__":
    main()
