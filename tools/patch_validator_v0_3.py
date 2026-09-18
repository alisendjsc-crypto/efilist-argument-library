import os,sys,hashlib,re
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
E=REPO
SRC=os.path.join(REPO,"adversarial_map_staging","adv_map_validator_v0_2.py")
DEST=os.path.join(OUT,"adversarial_map_staging","adv_map_validator_v0_3.py")
src=open(SRC,"rb").read()
BASE="d775fbea1cd726690a49acf0914270c2"
got=hashlib.md5(src).hexdigest()
assert got==BASE, "BASE GUARD FAIL: %s != %s"%(got,BASE)
t=src.decode("utf-8")
assert "\r" not in t, "CR present"
PATCHES=[]
def P(name,old,new):
    PATCHES.append((name,old,new))

# 1 -- constants: variant locus grammar + phases
P("constants",
'''LOCI = ("short", "medium", "long", "diagnosis")
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E")''',
'''LOCI = ("short", "medium", "long", "diagnosis")
# K345 LOCI RULING (Josiah): the enum is EXTENDED to reach archetypeVariants.
# A target_locus is either a PRIMARY locus (the four above, unchanged) or a VARIANT
# locus spelled "archetypeVariants.<slot>". The dotted form is required so the entry
# names WHICH slot it engages -- 16 nodes carry 39 variants and they do not paraphrase
# one another. A variant locus is valid only where that slot exists on that node.
VARIANT_PREFIX = "archetypeVariants."
VARIANT_SLOTS = ("sophisticate", "defender", "drifter", "blended")
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E", "F", "R")''')

# 2 -- locus_text
P("locus_text",
'''def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    return node.get("responses", {}).get(locus, "")''',
'''def variant_slot(locus):
    """Slot name for a variant locus, else None. Pure string work -- no corpus needed."""
    if isinstance(locus, str) and locus.startswith(VARIANT_PREFIX):
        return locus[len(VARIANT_PREFIX):]
    return None


def locus_valid(node, locus):
    """A locus is valid if it is one of the four primaries, or a variant slot that
    EXISTS on this node. Primary loci are accepted unconditionally, exactly as v0_2
    accepted them: all 82 nodes carry all four, so tightening there would change
    passing behaviour for no measured gain."""
    if locus in LOCI:
        return True
    s = variant_slot(locus)
    if s is None or s not in VARIANT_SLOTS:
        return False
    return s in (node.get("responses", {}).get("archetypeVariants") or {})


def node_variant_slots(node):
    return [s for s in VARIANT_SLOTS
            if s in (node.get("responses", {}).get("archetypeVariants") or {})]


def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    s = variant_slot(locus)
    if s is not None:
        return (node.get("responses", {}).get("archetypeVariants") or {}).get(s, "")
    return node.get("responses", {}).get(locus, "")''')

# 3 -- target-locus + anchor-rule gate
P("target-locus/anchor-rule",
'''        note("target-locus", locus in LOCI, "%s: %r" % (tag, locus))
        anchor = e["target_anchor"]
        a_ok = isinstance(anchor, str) and anchor.strip() != "" and wc(anchor) <= 15
        if a_ok and in_ids and locus in LOCI:''',
'''        l_ok = in_ids and locus_valid(nodes[tid], locus)
        note("target-locus", l_ok, "%s: %r" % (tag, locus))
        anchor = e["target_anchor"]
        a_ok = isinstance(anchor, str) and anchor.strip() != "" and wc(anchor) <= 15
        if a_ok and in_ids and l_ok:''')

# 4 -- entry cap: per (id, locus) hard, per node scaled
P("entry-cap",
'''    for tid, tags in per_id.items():
        note("entry-cap", len(tags) <= 3, "%r has %d entries (cap 3)" % (tid, len(tags)))''',
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
             % (tid, len(tags), bound, bound - 3))''')

# 5 -- accumulate per_id_locus
P("accumulator",
'''        pairs.setdefault(key, []).append(tag)
        per_id.setdefault(e.get("target_id"), []).append(tag)''',
'''        pairs.setdefault(key, []).append(tag)
        per_id.setdefault(e.get("target_id"), []).append(tag)
        per_id_locus.setdefault((e.get("target_id"), e.get("target_locus")), []).append(tag)''')
P("accumulator-init",
'''    per_id = {}
    per_phase = {}''',
'''    per_id = {}
    per_id_locus = {}
    per_phase = {}''')

# 5b -- collect (path, meta) for the late variant-coverage gate
P("metas-init",
'''    all_entries = []
    for p in map_paths:''',
'''    all_entries = []
    metas = []
    for p in map_paths:''')
P("metas-append",
'''        for i, e in enumerate(doc["entries"]):
            tag = "%s[%d]" % (os.path.basename(p), i)
            all_entries.append((tag, e))''',
'''        metas.append((p, meta))
        for i, e in enumerate(doc["entries"]):
            tag = "%s[%d]" % (os.path.basename(p), i)
            all_entries.append((tag, e))''')

# 6 -- variant coverage: reported always, gated when declared
P("variant-coverage",
'''    covered = set(per_id) & ids
    missing = sorted(ids - covered)''',
'''    covered = set(per_id) & ids
    missing = sorted(ids - covered)
    # Variant coverage is REPORTED, never forced: Phase F is owed and a successor map
    # must be able to exist before it lands. When meta DECLARES the figure it is gated,
    # so the claim is checked even though completion is not compelled.
    var_loci_total = sorted((n["id"], VARIANT_PREFIX + s)
                            for n in corpus["objections"] for s in node_variant_slots(n))
    var_loci_hit = sorted(k for k in per_id_locus if variant_slot(k[1]) is not None)
    vc = "%d/%d" % (len(set(var_loci_hit)), len(var_loci_total))
    for p, meta in metas:
        if "variant_coverage" in meta:
            note("variant-coverage", meta["variant_coverage"] == vc,
                 "%s: declared %r vs computed %r" % (p, meta["variant_coverage"], vc))''')

# 7 -- report line
P("report",
'''    out("coverage: %d/%d corpus ids covered; per-phase %s" %''',
'''    out("variant-coverage: %s archetypeVariants loci carry >=1 entry" % vc)
    out("coverage: %d/%d corpus ids covered; per-phase %s" %''')

# 8 -- docstring version
P("docstring-version",
'''  meta-summaries         IF meta declares class_counts / coverage_distinct_ids, they must equal computed''',
'''  meta-summaries         IF meta declares class_counts / coverage_distinct_ids, they must equal computed
  variant-coverage       IF meta declares variant_coverage "<hit>/<total>", it must equal computed
  entry-cap              <=3 entries per (target_id, target_locus)          [K345: unit was the node]
  entry-cap-node         <=3 + (variant loci on that node) entries per node [K345: was a flat 3]

v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".
v0_2 IS RETAINED UNCHANGED beside this file: adversarial_map_v1_0.json's receipt names
it, and that receipt has to stay reproducible.''')

P("answered-by-variant",
  '                    if len(parts) != 2 or parts[0] not in ids or parts[1] not in LOCI:',
  '                    # K345: an (a) may route to a variant locus too. Same ruling, one step\n'
  '                    # over: leaving this at LOCI would let the enum extend while the routing\n'
  '                    # target stayed silently narrower than the thing it points at.\n'
  '                    if len(parts) != 2 or parts[0] not in ids \\\n'
  '                            or not locus_valid(nodes[parts[0]], parts[1]):')

CTRL = open(os.path.join(_HERE, "k345_validator_controls.txt"), encoding="utf-8").read()
P("k345-controls",
  "    passed = sum(1 for _n, g, _c in results if g)",
  CTRL + "    passed = sum(1 for _n, g, _c in results if g)")

for name,old,new in PATCHES:
    n=t.count(old)
    assert n==1, "PATCH %r matched %d times (want 1)"%(name,n)
    t=t.replace(old,new)
    print("  applied: %s"%name)
open(DEST,"wb").write(t.encode("utf-8"))
print("\nWROTE %s"%DEST)
print("  bytes %d  md5 %s"%(len(t.encode('utf-8')),hashlib.md5(t.encode('utf-8')).hexdigest()))
print("  source UNTOUCHED md5 %s"%hashlib.md5(open(SRC,'rb').read()).hexdigest())
