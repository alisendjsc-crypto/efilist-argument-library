"""K348 -- derive adv_map_validator_v0_5.py from v0_4 by anchored, single-occurrence
replacement.  v0_4 stays byte-identical on disk: canon pins it at validator_pin_v0_4 and
the Phase F receipt names it.

v0_5 makes ONE ruled change and nothing else.

THE RULING (Josiah, K348).  The K345 node bound `3 + (variant loci)` was set when no
variant entry existed anywhere.  It reserved ONE slot per variant locus on top of the
primary allowance, while the per-locus cap lets any locus -- primary or variant -- carry
three.  So the bound and anti-inflation gate 5 disagree BY CONSTRUCTION wherever a variant
locus legitimately opens: gate 5 says author the second continuation, and the node bound
refuses to hold it.  Phase F met exactly that at `red-button-repugnant`, which is legal
per-locus and illegal per-node.  The bound becomes `3 + 3 x (variant loci)` -- the
per-locus cap applied to variants as it already is to primaries.  A node carrying NO
variants still keeps the Q1-ratified bound of 3 EXACTLY, which is the property the K345
amendment was written to preserve and this one preserves unchanged.

MEASURED BLAST RADIUS: across the 133-entry projected assembly, the amended bound changes
the verdict at exactly one node (red-button-repugnant, 6 entries) and at no other; zero
nodes are within reach of the new bound.  Josiah delegated the FORM of the entry-cap
amendment at K345 and ruled this one at K348.

Repo-relative: resolves the repo from its own location.  --out <dir> to emit elsewhere.
"""
import os, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_4.py")
DEST = os.path.join(OUT, "adversarial_map_staging", "adv_map_validator_v0_5.py")

BASE = "d7a049ee1161d3bc5de0d3fbff96bbf9"
src = open(SRC, "rb").read()
got = hashlib.md5(src).hexdigest()
assert got == BASE, "BASE GUARD FAIL: %s != %s" % (got, BASE)
t = src.decode("utf-8")
assert "\r" not in t, "CR present in v0_4"

PATCHES = []
def P(name, old, new):
    PATCHES.append((name, old, new))

# 1 -- docstring: the check list states the bound, so it moves with the bound
P("doc-checklist",
'''  entry-cap-node         <=3 + (variant loci on that node) entries per node [K345: was a flat 3]''',
'''  entry-cap-node         <=3 + 3*(variant loci on that node) entries per node
                         [K348: was 3 + 1*(variant loci); K345: was a flat 3]''')

# 2 -- docstring: version note
P("doc-version",
'''v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".''',
'''v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".
v0_5 (K348): the node bound becomes 3 + 3*(variant loci).  The K345 form reserved ONE
slot per variant locus while the per-locus cap allows three, so the node bound and
anti-inflation gate 5 disagreed by construction wherever a variant locus legitimately
opened -- gate 5 asks for the second continuation and the node bound refused to hold it.
A node with NO variants still keeps the ratified bound of 3 EXACTLY.  Ruled by Josiah at
K348 on a measurement: across the 133-entry successor assembly the amended bound changes
the verdict at one node and no other.  v0_4 IS RETAINED UNCHANGED beside this file:
canon pins it at validator_pin_v0_4 and the Phase F receipt names it.''')

# 3 -- the bound itself, and the comment that states its reasoning
P("node-bound",
'''    # K345: the cap's unit moves from the NODE to the LOCUS, because the locus is the
    # unit the anchor engages. A node with no archetypeVariants keeps the ratified
    # bound of 3 EXACTLY; a node with variants gets one more slot per variant locus,
    # so the gate extends in proportion to the text rather than being loosened flat.
    for (tid, locus), tags in per_id_locus.items():
        note("entry-cap", len(tags) <= 3,
             "%r#%s has %d entries (cap 3 per locus)" % (tid, locus, len(tags)))
    for tid, tags in per_id.items():
        bound = 3 + (len(node_variant_slots(nodes[tid])) if tid in nodes else 0)
        note("entry-cap-node", len(tags) <= bound,
             "%r has %d entries (node bound %d = 3 + %d variant loci)"
             % (tid, len(tags), bound, bound - 3))''',
'''    # K345: the cap's unit moves from the NODE to the LOCUS, because the locus is the
    # unit the anchor engages. A node with no archetypeVariants keeps the ratified
    # bound of 3 EXACTLY.
    # K348 (Josiah): the node bound scales by the per-locus cap, not by one slot per
    # locus. The K345 form was set when NO variant entry existed; it reserved a single
    # slot per variant locus while the per-locus cap allows three, so the node bound and
    # anti-inflation gate 5 contradicted each other wherever a variant locus legitimately
    # opened. The bound now applies the per-locus cap to variants exactly as it already
    # applies to primaries, and a node with no variants is untouched at 3.
    for (tid, locus), tags in per_id_locus.items():
        note("entry-cap", len(tags) <= 3,
             "%r#%s has %d entries (cap 3 per locus)" % (tid, locus, len(tags)))
    for tid, tags in per_id.items():
        nvar = len(node_variant_slots(nodes[tid])) if tid in nodes else 0
        bound = 3 + 3 * nvar
        note("entry-cap-node", len(tags) <= bound,
             "%r has %d entries (node bound %d = 3 + 3*%d variant loci)"
             % (tid, len(tags), bound, nvar))''')

# 4 -- the controls. A gate with no failing control is not a gate, and a control that
#      asserts a SUPERSEDED arithmetic would pass only by being wrong, so the K345
#      trips-at-6 case is REPLACED rather than kept beside its successor.
P("self-test-node-bound-cases",
'''    # 8. the node bound SCALES: node-y carries 2 variant slots, so 5 is clean and 6 trips
    five = [_entry(target_id="node-y", target_anchor=a) for a in
            ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over")] + [
           vent("sophisticate", "carrying its own distinct commitment"),
           vent("defender", "naming the bad faith")]
    clean("k345-entry-cap-node-scales-to-5", five)
    case("k345-entry-cap-node-trips-at-6",
         five + [_entry(target_id="node-y", target_locus="medium", target_anchor="medium text y")],
         "entry-cap-node")''',
'''    # 8. the node bound SCALES: node-y carries 2 variant slots. Under the K348 form the
    #    bound is 3 + 3*2 = 9, so five is clean, nine is clean, and the tenth trips. The
    #    K345 control that tripped at SIX is not kept beside these: it asserted the
    #    superseded arithmetic and could only pass by being wrong.
    five = [_entry(target_id="node-y", target_anchor=a) for a in
            ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over")] + [
           vent("sophisticate", "carrying its own distinct commitment"),
           vent("defender", "naming the bad faith")]
    clean("k345-entry-cap-node-scales-to-5", five)
    nine = ([_entry(target_id="node-y", target_locus="long", target_anchor=a) for a in
             ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over")]
            + [_entry(target_id="node-y", target_locus="medium", target_anchor=a) for a in
               ("medium text y four", "text y four five", "y four five six")]
            + [vent("sophisticate", a) for a in
               ("sophisticate variant for node", "carrying its own distinct commitment",
                "epsilon zeta")])
    clean("k348-entry-cap-node-scales-to-9", nine)
    case("k348-entry-cap-node-trips-at-10",
         nine + [vent("defender", "naming the bad faith")], "entry-cap-node")
    # 8a. the per-LOCUS cap still binds INSIDE the widened node bound: four entries at one
    #     locus trip entry-cap even though the node total (4) is far under the bound (9).
    #     Widening the node bound must not loosen the gate the locus ruling installed.
    case("k348-per-locus-cap-binds-inside-the-node-bound",
         [_entry(target_id="node-y", target_locus="long", target_anchor=a) for a in
          ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over",
           "fox jumps over the")], "entry-cap")''')

for name, old, new in PATCHES:
    n = t.count(old)
    assert n == 1, "ANCHOR %s occurs %d times, expected 1" % (name, n)
    t = t.replace(old, new)

out_b = t.encode("utf-8")
assert b"\r" not in out_b, "CR in output"
assert all(c < 128 for c in out_b), "non-ASCII byte in output"
os.makedirs(os.path.dirname(DEST), exist_ok=True)
open(DEST, "wb").write(out_b)
print("wrote %s  md5 %s  bytes %d  patches %d"
      % (DEST, hashlib.md5(out_b).hexdigest(), len(out_b), len(PATCHES)))
