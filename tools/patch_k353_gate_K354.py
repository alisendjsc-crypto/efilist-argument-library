#!/usr/bin/env python3
"""patch_k353_gate_K354.py -- amend the wing's functional gate to the repaired flagship.

WHY THIS FILE EXISTS. k353_wing_functional_gate.py contains three checks that ASSERT THE DEFECT
this cut repairs: that solipsism's [NOTE] control is absent, that seven cards carry one, and
that the layer stands at 9 notes / 7 reachable. Run unchanged against the candidate they invert,
and NOTHING ELSE DOES -- all 22 wing links, the NULL, the care-ethics caveat and the boot-witness
control stay green. That inversion is the strongest evidence this session produces, because the
gate was written a session earlier by a seat with no knowledge of this cut, so it is captured as
`k354_prior_gate_inversion_v0_1.json` BEFORE anything here runs.

But a gate is not a record. The wuld primer says every future pin move owes this file a re-run,
so leaving it permanently three-red would hand the next session a landmine that reads exactly
like a regression. It is amended IN PLACE, on the K338/K351 amendment precedent, and its
pre-amendment bytes stay recoverable from git. Its landed K353 control artifact is NOT
overwritten -- the amended gate emits v0_2.

THE BASE COMES FROM THE GIT BLOB, not from disk, because this tool REPLACES THE FILE IT READS: a
disk base guard is true exactly once and false forever after (WI-K342). Every patch is asserted
to match exactly once before anything is written.

  python3 tools/patch_k353_gate_K354.py          # emit k354_drop/k353_wing_functional_gate.py
"""
import hashlib, io, os, subprocess, sys
sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, "k354_drop")
REL = "tools/k353_wing_functional_gate.py"
BASE_MD5 = "2628f870286489796e94386bf006511a"

AMEND = '''
AMENDED AT K354. Three checks here asserted the DEFECT rather than a property: that solipsism's
[NOTE] control is absent, that seven cards carry one, and that the layer stands at 9 notes / 7
reachable. K354 lifted the control out of `if (conf !== 'full')` so its condition equals its
container's, and all three inverted -- and nothing else in this file did. The pre-amendment run
against the repaired flagship is kept as k354_prior_gate_inversion_v0_1.json, 16 checks / 3
failed, and it is the cleanest evidence of the repair that exists. The three now assert the
repaired state, and this file's own control artifact moves to v0_2 so the K353 record stands.
'''

PATCHES = [
 ("docstring",
  "location, exactly as k352_functional_gate.py said of itself.\n\"\"\"",
  "location, exactly as k352_functional_gate.py said of itself.\n" + AMEND + "\"\"\""),

 ("out-default",
  'ap.add_argument("--out", default="k353_wing_functional_control_v0_1.json")',
  'ap.add_argument("--out", default="k354_wing_functional_control_v0_2.json")'),

 ("comment",
  "    # solipsism: the ship-set card whose own note NO link and NO click can reach",
  "    # solipsism: the ship-set card whose note K349 measured as unreachable by any reader and\n"
  "    # K354 repaired. It is in the wing's 21-node ship set, which is what made the repair this\n"
  "    # session's business rather than a carry: the wing points readers at that card."),

 ("check-solipsism",
  '    chk("solipsism: confidence:full suppresses its [NOTE] control, so its note is unreachable "\n'
  '        "(K349, logged not repaired -- pin-move work)", sol_btn is False, sol_btn)',
  '    chk("solipsism: its [NOTE] control is PRESENT -- the K349 finding, repaired at K354",\n'
  '        sol_btn is True, sol_btn)'),

 ("check-vacuity",
  '    chk("CONTROL the binding-scoped query is not vacuous: 7 cards DO carry a [NOTE] control",\n'
  '        any_btn == 7, any_btn)',
  '    chk("CONTROL the binding-scoped query is not vacuous: all 9 note-bearing cards carry one",\n'
  '        any_btn == 9, any_btn)'),

 ("check-gap",
  '    chk("and the gap is K349\'s exact figure: 9 notes rendered at `long`, 7 reachable",\n'
  '        n_notes == 9 and any_btn == 7, "%s notes / %s controls" % (n_notes, any_btn))',
  '    chk("and the gap K349 measured is CLOSED: 9 notes rendered at `long`, 9 reachable",\n'
  '        n_notes == 9 and any_btn == 9, "%s notes / %s controls" % (n_notes, any_btn))'),
]

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + str(got)) if got and not cond else ""))
    if not cond: fail += 1

raw = subprocess.check_output(["git", "-C", ROOT, "show", "HEAD:" + REL])
chk("base blob is the K353 gate", hashlib.md5(raw).hexdigest() == BASE_MD5, hashlib.md5(raw).hexdigest())
chk("base is CR-free", b"\r" not in raw)
if fail: sys.exit("ABORT: base is not the committed K353 gate -- nothing written")

txt = raw.decode("utf-8")
for tag, old, new in PATCHES:
    chk("%-16s matches exactly once" % tag, txt.count(old) == 1, txt.count(old))
if fail: sys.exit("ABORT: %d anchor(s) did not match exactly once -- nothing written" % fail)

out = txt
for tag, old, new in PATCHES:
    out = out.replace(old, new, 1)

chk("the three defect assertions are gone", out.count("any_btn == 7") == 0 and out.count("sol_btn is False") == 0)
chk("and the repaired ones are in", out.count("any_btn == 9") == 2 and out.count("sol_btn is True") == 1)
# A POSITIONAL line-by-line comparison is the wrong instrument here and the first cut used it:
# the docstring patch INSERTS lines, so every line after it shifts and compares unequal, and the
# check reported the whole file changed. Count changed REGIONS with difflib instead -- 6 patches,
# so at most 6 non-equal opcodes, and adjacent ones may merge.
import difflib
_ops = [o for o in difflib.SequenceMatcher(None, txt.split("\n"), out.split("\n")).get_opcodes()
        if o[0] != "equal"]
chk("changed REGIONS == the declared patch set", len(_ops) <= len(PATCHES), len(_ops))
chk("every changed region is small", all((o[2] - o[1]) <= 12 and (o[4] - o[3]) <= 16 for o in _ops),
    [(o[0], o[2] - o[1], o[4] - o[3]) for o in _ops])
chk("the wing's own checks are untouched",
    out.count("22 open-links in the live DOM") == 1 and out.count("NULL: the same links WITHOUT the suffix") == 1)
chk("result is ASCII and CR-free", "\r" not in out and all(ord(c) < 128 for c in out))
if fail: sys.exit("ABORT: %d failure(s) -- nothing written" % fail)

os.makedirs(DROP, exist_ok=True)
rb = out.encode("utf-8")
io.open(os.path.join(DROP, "k353_wing_functional_gate.py"), "wb").write(rb)
print("\n  WROTE %s" % os.path.join(DROP, "k353_wing_functional_gate.py"))
print("  %s  %s / %d  ->  %s / %d" % (REL, BASE_MD5, len(raw), hashlib.md5(rb).hexdigest(), len(rb)))
print("\nPATCH K353 GATE: GREEN")
