#!/usr/bin/env python3
"""sweep_v4_1_0.py -- COWORK EXECUTION ORDER v4.1.0, the three subtractive repairs.

A LINE-INDEXED pass with a per-line anchor assertion, per the order's section 3: not
sed -i, not a global regex. Any failed assertion aborts before anything is written.

Differs from sweep_v4_0_1.py in one deliberate way: this NEVER mutates the tracked
originals. It reads the three surfaces and writes results to k344_drop/, so the base-md5
guard in the operator block still has an untouched base to guard, and so this can be run
as many times as it takes without a reset.

THE CUT IS THREE SURFACES. There is no build step: combined.html is a hand-assembled
superset carrying REBUTTAL_STRENGTH, which the JSX does not, and nothing regenerates any
surface from any other. All three carry the six spans BYTE-IDENTICALLY, verified, so one
replacement pair serves all three -- which is also what makes the cross-surface gate a
byte-equality check rather than a semantic one.

R3 carries FOUR spans, not the spec's three. The fourth is at
responses.archetypeVariants.defender and states the same unsourced ratio; the spec's own
scope note says a repair that leaves the node counting to ninety-nine against itself is
not a repair. Ratified by Josiah at K344.

ASCII-only source on purpose: every em dash is written \\u2014 so no encoding step between
here and the file can turn a constant into a different constant.
"""
import hashlib, io, json, os, sys
sys.dont_write_bytecode = True   # importing the validator must not litter __pycache__ into a served repo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, "k344_drop")

EMD = "—"

# --- section 0: the three surfaces and their base pins, verified at K344 --------------
SURFACES = {
    "efilist_argument_library_v4_0_0.json": ("6ee1f6f31e0f012db0d58cae4f912fcb", 1333912, 12342),
    "efilist_argument_library_v4_0_0.jsx":  ("b7dadfc39d988d643c408b3329ffcb54", 1273371,  8584),
    "combined.html":                        ("cee25a00b68ba036138d064c383d9a8b", 2982658, 12447),
}
JSONF = "efilist_argument_library_v4_0_0.json"
JSXF  = "efilist_argument_library_v4_0_0.jsx"
HTMLF = "combined.html"

# --- section 1: the six spans, with their line in each surface ------------------------
# (tag, {surface: 1-based line}, old, new)
EDITS = [
 ("R1", {JSONF: 1756, JSXF: 1744, HTMLF: 4595},
  "First, the empirical failure: behavioral genetics research consistently demonstrates that"
  " approximately 40-50% of the variance in subjective wellbeing is heritable. This means that"
  " roughly half of your capacity for happiness was determined at conception" + EMD + "before any"
  " 'choice' was possible. The remaining variance is split between environmental factors (which"
  " are largely unchosen" + EMD + "your birthplace, your family, your socioeconomic position, your"
  " era) and a modest contribution from intentional activity. The portion of wellbeing that is"
  " genuinely under voluntary control is the smallest slice of the pie.",
  "First, the empirical failure: behavioral genetics research consistently finds that 40-50% of"
  " the variance between people in subjective wellbeing tracks genetic variance. That is a"
  " population statistic, not a personal budget" + EMD + "it does not say that half of any given"
  " person's happiness was fixed at conception, and the correction is owed before anything is"
  " built on the number. What it does establish is enough: the differences in how well people"
  " fare are driven substantially by factors nobody selected. Nor is the remainder a reservoir"
  " of choice" + EMD + "the environmental share is itself largely unchosen (your birthplace, your"
  " family, your socioeconomic position, your era), and the voluntarist needs whatever is left"
  " over to be volitional, which no such study delivers."),

 ("R2", {JSONF: 581, JSXF: 569, HTMLF: 3420},
  "Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire pessimist"
  " tradition into a work that has never been substantively refuted" + EMD + "only dismissed with"
  " the exact social categorization you are deploying now.",
  "Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire pessimist"
  " tradition into a single sustained work" + EMD + "one far more often categorized than answered,"
  " in exactly the register you are using now."),

 ("R3a", {JSONF: 91, JSXF: 79, HTMLF: 2930},
  "Roughly one deployment in a hundred is a person actually worried about you. The rebuttal is"
  " built for the ninety-nine, and it names the one honestly rather than pretending it away.",
  "Genuine concern is the rare exception here, not the ordinary case. The rebuttal is built for"
  " the ordinary case, and it names the exception honestly rather than pretending it away."),

 ("R3b", {JSONF: 91, JSXF: 79, HTMLF: 2930},
  "The one-in-a-hundred who genuinely worries is making the argument-level case",
  "The one who genuinely worries is making the argument-level case"),

 ("R3c", {JSONF: 91, JSXF: 79, HTMLF: 2930},
  "The ninety-nine are doing neither; they have changed the subject.",
  "The rest are doing neither; they have changed the subject."),

 # the fourth R3 span -- archetypeVariants.defender, ratified at K344
 ("R3d", {JSONF: 94, JSXF: 82, HTMLF: 2933},
  "roughly one deployment in a hundred is genuine worry",
  "genuine worry is the rare exception"),
]

# --- section 1b: the corpus version field. JSON-ONLY -- the jsx and the flagship carry
# no "version": "4.0.x" string at all, verified, so there is no cross-surface question.
#
# THE FIELD NAMES THE CONTENT CUT, NOT THE RELEASE. It is not stale at 4.0.0 and this is
# not a relabel. Commit e922e6c restored it to 4.0.0 after the v4.0.1-v4.0.4 release
# relabels had walked it to 4.0.4 while the content stayed byte-identical: "one content
# version wore five hashes and every Adversarial Map fragment, the scholar register and
# canon, all of which pin 6ee1f6f3, failed validation against HEAD." v4.1.0 is the first
# genuine content cut since K219, so it is the first bump that rule licenses.
# The objections digest is independent of this field -- it is computed over `objections`
# only, and the validator's own `label churn survives` self-test sets version to 4.0.4 to
# prove it -- so the digest moves here because the RESPONSES moved, nothing else.
# `generated` is NOT touched: it dates an authoring run, and no run happened today.
VERSION_EDIT = (JSONF, 3, '"version": "4.0.0"', '"version": "4.1.0"')

# --- section 2: strings that must SURVIVE, untouched, in all three surfaces ------------
HELD = [
    "Second, the neurochemical reality",                    # follows R1 in the same response
    "Terror Management Theory formalized them empirically", # precedes R2
    "; they have changed the subject.",                     # R3c's kept tail
    "Hold the honest remainder:",                           # R3d's kept head
    "and that person gets met in good faith",               # R3d's kept tail
]

# --- section 3: strings that must be GONE from all three surfaces ----------------------
GONE = [old for _t, _l, old, _n in EDITS] + [
    "roughly half of your capacity for happiness was determined at conception",
    "has never been substantively refuted",
    "Roughly one deployment in a hundred is a person actually worried about you",
]

# --- word-count invariants, stated in advance (K342: only a count catches a change in
# meaning that is internally consistent) ----------------------------------------------
WORDS = {
    ("happiness-is-choice", "long"):    (555, 589),
    ("just-edgy", "long"):              (220, 220),
    ("just-depressed", "long"):         (979, 978),
    ("just-depressed", "defender"):     (347, 344),
}

fail = []
def need(cond, msg):
    if not cond:
        fail.append(msg)
        print("  ABORT " + msg)
    return cond

def read(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8", newline="").read()

print("K344 v4.1.0 SWEEP -- 3 surfaces, 6 spans, 18 span-replacements, 12 text loci + 1 version locus\n")

# ===== 0. preconditions ===============================================================
base = {}
for p, (m5, nb, nl) in SURFACES.items():
    s = read(p); b = s.encode("utf-8")
    got5, gotb, gotl = hashlib.md5(b).hexdigest(), len(b), len(s.split("\n"))
    need(got5 == m5, "0.md5 %s: %s != %s" % (p, got5, m5))
    need(gotb == nb, "0.bytes %s: %d != %d" % (p, gotb, nb))
    need(gotl == nl, "0.lines %s: %d != %d" % (p, gotl, nl))
    need("\r" not in s, "0.cr %s: carriage returns present" % p)
    base[p] = s
    print("  0 %-38s md5 %s  %9d B  %6d lines  CR-free" % (p, got5, gotb, gotl))
if fail: sys.exit("\nPRECONDITIONS FAILED -- nothing written\n")

# ===== 1. per-line anchor assertions, then the edits ==================================
print()
work = dict(base)
touched = {p: set() for p in SURFACES}
for tag, loci, old, new in EDITS:
    need(old != new, "1.%s: old == new" % tag)
    for p, ln in loci.items():
        s = work[p]
        L = s.split("\n")
        need(len(L) >= ln, "1.%s %s: file has no line %d" % (tag, p, ln))
        if fail: break
        line = L[ln - 1]
        c_line, c_file = line.count(old), s.count(old)
        need(c_line == 1, "1.%s %s L%d: anchor occurs %dx on the line, expected 1" % (tag, p, ln, c_line))
        need(c_file == 1, "1.%s %s: anchor occurs %dx in the file, expected 1" % (tag, p, c_file))
        need(new not in s, "1.%s %s: replacement text ALREADY present -- sweep already run?" % (tag, p))
        if fail: break
        L[ln - 1] = line.replace(old, new, 1)
        work[p] = "\n".join(L)
        touched[p].add(ln)
    if fail: break
    print("  1 %-4s json L%-5d jsx L%-5d html L%-5d  %+d chars" %
          (tag, loci[JSONF], loci[JSXF], loci[HTMLF], len(new) - len(old)))

# the version locus
if not fail:
    p, ln, old, new = VERSION_EDIT
    L = work[p].split("\n")
    need(L[ln - 1].count(old) == 1, "1.VER %s L%d: %r not on the line exactly once" % (p, ln, old))
    need(work[p].count(old) == 1, "1.VER %s: %r occurs %dx in the file" % (p, old, work[p].count(old)))
    if not fail:
        L[ln - 1] = L[ln - 1].replace(old, new, 1)
        work[p] = "\n".join(L)
        touched[p].add(ln)
        print("  1 VER  json L%-5d  %s -> %s" % (ln, old, new))
if fail: sys.exit("\nEDIT PHASE FAILED -- nothing written\n")

# ===== 2. the changed-line set is EXACTLY the named loci ==============================
print()
EXPECT = {JSONF: sorted({1756, 581, 91, 94, 3}), JSXF: sorted({1744, 569, 79, 82}),
          HTMLF: sorted({4595, 3420, 2930, 2933})}
for p in SURFACES:
    B, N = base[p].split("\n"), work[p].split("\n")
    need(len(B) == len(N), "2.%s: line count moved %d -> %d" % (p, len(B), len(N)))
    if fail: continue
    diff = sorted(i + 1 for i, (x, y) in enumerate(zip(B, N)) if x != y)
    need(diff == EXPECT[p], "2.%s: changed lines %r != named %r" % (p, diff, EXPECT[p]))
    need(sorted(touched[p]) == EXPECT[p], "2.%s: touched %r != named %r" % (p, sorted(touched[p]), EXPECT[p]))
    print("  2 %-38s changed lines %s -- exactly the named loci" % (p, diff))

# ===== 3. GONE / HELD / NEW, on the new text ==========================================
print()
for p in SURFACES:
    s = work[p]
    for g in GONE:
        need(s.count(g) == 0, "3.GONE %s: %r still present %dx" % (p, g[:46], s.count(g)))
    for h in HELD:
        need(s.count(h) == 1, "3.HELD %s: %r count %d, expected 1" % (p, h[:46], s.count(h)))
    for tag, _l, _o, new in EDITS:
        need(s.count(new) == 1, "3.NEW %s %s: count %d, expected 1" % (p, tag, s.count(new)))
print("  3 GONE %d strings x3 surfaces | HELD %d x3 | NEW %d x3" % (len(GONE), len(HELD), len(EDITS)))

# ===== 4. cross-surface gate -- the check that did not exist before ===================
# For every span: new present exactly once in all three, old absent from all three, and
# the three surfaces agree on the repaired passage BYTE FOR BYTE.
print()
for tag, loci, old, new in EDITS:
    got = {}
    for p in SURFACES:
        L = work[p].split("\n")
        line = L[loci[p] - 1]
        i = line.find(new)
        need(i >= 0, "4.%s %s: repaired span not on its own line" % (tag, p))
        if i >= 0:
            got[p] = line[i:i + len(new)]
    vals = set(got.values())
    need(len(vals) == 1, "4.%s: the three surfaces DISAGREE on the repaired passage" % tag)
    need(vals == {new} if vals else False, "4.%s: surface text != intended replacement" % tag)
print("  4 cross-surface: %d spans x 3 surfaces agree byte-for-byte" % len(EDITS))

# ===== 5. the JSON still parses, and changed exactly where it should ==================
print()
b_doc = json.loads(base[JSONF])
n_doc = json.loads(work[JSONF])
def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, path + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, path + (i,))
    else:
        yield path, x
bl, nl_ = dict(leaves(b_doc)), dict(leaves(n_doc))
need(set(bl) == set(nl_), "5.json: leaf SET moved (keys added or removed)")
moved = sorted(k for k in bl if bl[k] != nl_.get(k))
byid = {o["id"]: i for i, o in enumerate(b_doc["objections"])}
WANT = sorted([("version",)] + [
    ("objections", byid["happiness-is-choice"], "responses", "long"),
    ("objections", byid["just-edgy"], "responses", "long"),
    ("objections", byid["just-depressed"], "responses", "long"),
    ("objections", byid["just-depressed"], "responses", "archetypeVariants", "defender"),
])
need(moved == WANT, "5.json: moved leaves %r != %r" % (moved, WANT))
print("  5 json parses; exactly %d leaves moved, and they are the named ones" % len(moved))

# ===== 6. word-count invariants, stated in advance ====================================
print()
def wc(doc, nid, locus):
    r = doc["objections"][byid[nid]]["responses"]
    return len((r["archetypeVariants"]["defender"] if locus == "defender" else r[locus]).split())
for (nid, locus), (w0, w1) in WORDS.items():
    g0, g1 = wc(b_doc, nid, locus), wc(n_doc, nid, locus)
    need(g0 == w0, "6.%s/%s: BASE word count %d != declared %d" % (nid, locus, g0, w0))
    need(g1 == w1, "6.%s/%s: NEW word count %d != declared %d" % (nid, locus, g1, w1))
    print("  6 %-22s %-9s %4d -> %4d (%+d)" % (nid, locus, g0, g1, g1 - g0))

# ===== 7. anchor destruction is the receipt ===========================================
print()
MAP = os.path.join(ROOT, "adversarial_map_staging", "adversarial_map_v1_0.json")
m = json.load(io.open(MAP, encoding="utf-8"))
# Resolve the locus with the VALIDATOR'S OWN function, imported rather than reimplemented:
# `diagnosis` does not live under `responses`, and a second implementation of the lookup is
# a second chance to disagree with the very gate this check stands in for. (My first pass
# reimplemented it, read "" for the two diagnosis-locus entries, and reported 88 of 93
# holding -- the harness describing itself, ccclviii.)
sys.path.insert(0, os.path.join(ROOT, "adversarial_map_staging"))
from adv_map_validator_v0_2 import locus_text
def node_text(doc, nid, locus):
    return locus_text(doc["objections"][byid[nid]], locus)
broke, held = [], []
for e in m["entries"]:
    tid, loc, anc = e["target_id"], e["target_locus"], e["target_anchor"]
    if not need(tid in byid, "7.anchor: target_id %r not in corpus" % tid): continue
    was = anc in node_text(b_doc, tid, loc)
    now = anc in node_text(n_doc, tid, loc)
    need(was, "7.anchor %s#%s did not match even BEFORE the cut" % (tid, loc))
    if was and not now: broke.append((tid, loc))
    elif was and now:   held.append((tid, loc))
WANT_BROKE = sorted([("happiness-is-choice", "long"), ("just-edgy", "long"), ("just-depressed", "long")])
need(sorted(broke) == WANT_BROKE, "7: anchors broken %r != the three intended %r" % (sorted(broke), WANT_BROKE))
need(len(held) == len(m["entries"]) - 3, "7: %d anchors held, expected %d" % (len(held), len(m["entries"]) - 3))
print("  7 anchors: %d of %d hold; exactly the 3 intended break -- the repair's receipt" % (len(held), len(m["entries"])))

if fail:
    sys.exit("\nSWEEP FAILED (%d) -- NOTHING WRITTEN\n" % len(fail))

# ===== write ==========================================================================
os.makedirs(DROP, exist_ok=True)
print("\n  --- results (k344_drop/) ---")
for p in SURFACES:
    b = work[p].encode("utf-8")
    io.open(os.path.join(DROP, p), "w", encoding="utf-8", newline="").write(work[p])
    print("  %-38s new_md5 %s  %9d B  (%+d)" %
          (p, hashlib.md5(b).hexdigest(), len(b), len(b) - SURFACES[p][1]))
print("\nSWEEP GREEN -- originals untouched, base guards still valid.")
