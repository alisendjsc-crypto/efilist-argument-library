#!/usr/bin/env python3
"""verify_K354.py -- THE RECONSTRUCTION GATE for the K354 note-and-confidence cut.

It answers one question the cutter cannot answer about itself: is the set of lines that moved
EXACTLY the set the cut declared? It does that by REBUILDING the candidate from the base's own
segments plus the declared new blocks and requiring byte equality, which is stronger than a diff
because a diff reports what changed while a reconstruction proves that nothing else did.

THREE DISCIPLINES, EACH WITH A REASON:

  THE BASE COMES FROM THE GIT BLOB, never from disk. `git rev-parse HEAD:combined.html` and
  `git show` are immune to a worktree that a half-run left dirty and to the eol filters that
  made WI-K343's first delta enumeration report six phantom changed files (ccclix / the
  autocrlf class). efilist forces eol=lf, so blob and worktree agree here -- which is a fact to
  assert, not to assume.

  THE NEW BLOCKS ARE LIFTED OUT OF THE CUTTER'S SOURCE BY ast, not retyped. A verifier that
  retypes the bytes it is verifying tests the typist. ast.literal_eval on the module's top-level
  string assignments means the two files cannot disagree about what was supposed to be written.
  The declared LOCI are pulled the same way, from the EDITS table's literal elements, and
  compared BOTH WAYS against this file's own segment plan.

  THE [NOTE] BUTTON'S MARKUP IS RE-EXTRACTED FROM THE BASE INDEPENDENTLY. Here a second
  implementation is the point rather than the hazard: the claim under test is "the control's
  markup is the base's own", so deriving it twice from the base and requiring agreement is a
  cross-check. It is three tokens of splitting, not a digest.

AND THE CORPUS IDENTITY, WHICH IS THE WHOLE LICENCE FOR THIS BEING A MECHANISM SESSION:
tools/xsurface_v4_1_0.py is run against the tracked tree AND against a scratch tree carrying the
candidate flagship beside the untouched corpus and JSX. Both must print the SAME canonical
serialization md5. That identity is the mechanical proof the cut touched no data, and it is what
lets the corpus `version` field stay 4.1.0 while the release label moves to v4.1.2.

  python3 tools/verify_K354.py
"""
import ast, hashlib, io, os, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, "k354_drop")
CUTTER = os.path.join(ROOT, "tools", "note_confidence_K354.py")
HTMLF, JSONF, JSXF = "combined.html", "efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx"

BASE_MD5, BASE_BYTES = "f095c0ce0e5a1d796d57fa5a5dd62f7d", 2985989
# the candidate is pinned by the cutter's OWN emitted binding, recomputed here rather than
# hand-copied -- a constant typed into two files is a constant that will disagree with itself.
CUT_PINS = "k354_cut_pins.json"
CORPUS_MD5 = "04bf6482aa0374ee92a81c1d55ec41f8"
JSX_MD5 = "b196548b6eb39065842d62292acca89f"
XSURFACE_GREEN = "6cd132ee5b8c7ca78ad0e095806f1c93"

# the segment plan, in 1-based base line numbers. Asserted against the cutter's own EDITS table.
PLAN_R = [378, 379, 380, 392, 401, 402, 403, 404, 420, 421, 422, 10559, 10564, 10583]
PLAN_D = [10560, 10561, 10562, 10563, 10565]
PLAN_I = [419]
PLAN_A = [10566]

HEX5 = re.compile(r"#[0-9a-fA-F]{5}\b")
HEX8 = re.compile(r"#[0-9a-fA-F]{8}\b")

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + str(got)) if got and not cond else ""))
    if not cond: fail += 1

def git(*a):
    return subprocess.check_output(["git", "-C", ROOT] + list(a))

def md5(b): return hashlib.md5(b).hexdigest()

print("VERIFY K354 -- reconstruction of the note-and-confidence cut\n")

# ---------------------------------------------------------------- 1. the base, from the blob
base_raw = git("show", "HEAD:" + HTMLF)
chk("base blob is the pin v4.1.1", (md5(base_raw), len(base_raw)) == (BASE_MD5, BASE_BYTES),
    "%s / %d" % (md5(base_raw), len(base_raw)))
disk_raw = io.open(os.path.join(ROOT, HTMLF), "rb").read()
chk("worktree == blob (eol=lf holds, ccclix)", disk_raw == base_raw)
chk("the tracked original was NOT mutated", md5(disk_raw) == BASE_MD5)

cand_raw = io.open(os.path.join(DROP, HTMLF), "rb").read()
import json as _json
PINS = _json.load(io.open(os.path.join(ROOT, "tools", CUT_PINS), encoding="utf-8"))
chk("the cut's declared BASE pin == the blob",
    (PINS["base"]["md5"], PINS["base"]["bytes"]) == (BASE_MD5, BASE_BYTES), PINS["base"])
chk("candidate md5 and bytes RECOMPUTED == the cut's declared binding",
    (md5(cand_raw), len(cand_raw)) == (PINS["candidate"]["md5"], PINS["candidate"]["bytes"]),
    "%s / %d vs %s" % (md5(cand_raw), len(cand_raw), PINS["candidate"]))
if fail: sys.exit("ABORT: inputs are not what this gate was written against")

L = base_raw.decode("utf-8").split("\n")
cand = cand_raw.decode("utf-8")

# ---------------------------------------------------------------- 2. the cutter's declarations
csrc = io.open(CUTTER, encoding="utf-8").read()
tree = ast.parse(csrc)
K = {}
for node in tree.body:
    if not isinstance(node, ast.Assign) or len(node.targets) != 1: continue
    tgt = node.targets[0]
    if isinstance(tgt, ast.Name):
        try: K[tgt.id] = ast.literal_eval(node.value)
        except Exception: pass
    elif isinstance(tgt, ast.Tuple) and isinstance(node.value, ast.Tuple):
        # BASE_MD5, BASE_BYTES, BASE_LINES = "...", n, n -- a tuple target, which a Name-only
        # walk skips silently. Found by this gate aborting on a constant it had declared it
        # would read: the locator was the NODE SHAPE, and the shape was assumed (ccclxxix).
        for nm, val in zip(tgt.elts, node.value.elts):
            if isinstance(nm, ast.Name):
                try: K[nm.id] = ast.literal_eval(val)
                except Exception: pass
for name in ("CSS_FULL", "CSS_STRONG", "CSS_PROV", "CSS_TOGGLE", "CSS_CMT_401", "CSS_CMT_402",
             "CSS_CMT_403", "CSS_CMT_404", "CSS_HC_NEW", "CSS_HC_STRONG", "CSS_HC_PROV",
             "CSS_PROV_RESP", "JS_HEAD", "JS_RESPBOX", "INTRODUCED_HEX8"):
    chk("cutter declares %s" % name, name in K)
chk("cutter's declared base md5 == the blob", K.get("BASE_MD5") == BASE_MD5, K.get("BASE_MD5"))
chk("cutter's declared base bytes == the blob", K.get("BASE_BYTES") == BASE_BYTES, K.get("BASE_BYTES"))
if fail: sys.exit("ABORT: could not read the cutter's declarations")

# the declared loci, from the EDITS table's literal elements
loci = {"R": [], "D": [], "I": [], "A": []}
for node in tree.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "EDITS":
        for elt in node.value.elts:
            tag, ln, kind = [ast.literal_eval(x) for x in elt.elts[:3]]
            loci[kind].append(ln)
chk("declared R loci == the plan", sorted(loci["R"]) == sorted(PLAN_R), sorted(loci["R"]))
chk("declared D loci == the plan", sorted(loci["D"]) == sorted(PLAN_D), sorted(loci["D"]))
chk("declared I loci == the plan", sorted(loci["I"]) == sorted(PLAN_I), sorted(loci["I"]))
chk("declared A loci == the plan", sorted(loci["A"]) == sorted(PLAN_A), sorted(loci["A"]))
chk("no locus is declared twice",
    len(loci["R"] + loci["D"] + loci["I"] + loci["A"]) == len(set(loci["R"] + loci["D"] + loci["I"] + loci["A"])))
if fail: sys.exit("ABORT: the cut's declared loci and this gate's plan disagree")

# ---------------------------------------------------------------- 3. the [NOTE] markup, re-derived
BTN = L[10565 - 1].split("(hasNote ? ", 1)[1].rsplit(" : '');", 1)[0]
JS_NOTE = "            badges += " + BTN + ";"
chk("the control's markup survives verbatim, once", cand.count(BTN) == 1, cand.count(BTN))
chk("base emitted it once too", base_raw.decode("utf-8").count(BTN) == 1)

# ---------------------------------------------------------------- 4. THE RECONSTRUCTION
rebuilt = (
    L[0:377]
    + [K["CSS_FULL"], K["CSS_STRONG"], K["CSS_PROV"]]          # 378-380
    + L[380:391]                                                # 381-391
    + [K["CSS_TOGGLE"]]                                         # 392
    + L[392:400]                                                # 393-400
    + [K["CSS_CMT_401"], K["CSS_CMT_402"], K["CSS_CMT_403"], K["CSS_CMT_404"]]
    + L[404:419]                                                # 405-419
    + [K["CSS_HC_NEW"]]                                        # inserted after 419
    + [K["CSS_HC_STRONG"], K["CSS_HC_PROV"], K["CSS_PROV_RESP"]]
    + L[422:10558]                                              # 423-10558
    + [K["JS_HEAD"], JS_NOTE]                                   # 10559 ; 10560-63 gone ; 10564
    + L[10565:10582]                                            # 10566-10582 (10565 deleted)
    + [K["JS_RESPBOX"]]                                         # 10583
    + L[10583:]                                                 # 10584-end
)
rebuilt_txt = "\n".join(rebuilt)
chk("RECONSTRUCTION: base segments + declared blocks == candidate, byte for byte",
    rebuilt_txt.encode("utf-8") == cand_raw)
chk("line 10566 was asserted and left alone", L[10566 - 1] == "          }" and cand.count("\n          }\n") >= 1)

# ---------------------------------------------------------------- 5. independent invariants
HELD = [
    ('let responseLevel = "medium";', 1),                 # the default is NOT flipped
    ("function setDepth(depth) {", 1),
    ('class="depth-jump"', 1),                            # K352's affordance, untouched
    ("(?:@(short|medium|long))?", 1),                     # K352's anchor grammar, untouched
    ("__arglibRouteObj(pk, pd)", 1),
    ("function toggleNote(id) {", 1),                     # the one caller's callee
    ("let archetypeSel = {};", 1),                        # D7
    # THE RULING: the note CONTAINER was always right and is not touched.
    ("${obj.note && responseLevel === 'long' ? '<div class=\"confidence-note\" id=\"note-' + obj.id + '\">' + obj.note + '</div>' : ''}", 1),
    ('class="note-toggle"', 1),                           # still exactly one emission site
]
GONE = ["const conf = obj.confidence || 'full';", "if (conf !== 'full') {",
        "const hasNote = obj.note && responseLevel === 'long';", "provisional-response"]
for s, n in HELD: chk("held x%d %r" % (n, s[:50]), cand.count(s) == n, cand.count(s))
for s in GONE:    chk("gone   %r" % s[:50], cand.count(s) == 0, cand.count(s))

b5, c5 = len(HEX5.findall(base_raw.decode("utf-8"))), len(HEX5.findall(cand))
chk("5-digit hex: base 15 (non-vacuity)", b5 == 15, b5)
chk("5-digit hex: candidate 0", c5 == 0, c5)
d8 = sorted(set(HEX8.findall(cand)) - set(HEX8.findall(base_raw.decode("utf-8"))))
chk("8-digit hex introduced == the declared set", d8 == sorted(set(K["INTRODUCED_HEX8"])), d8)
chk("the cut's hex census agrees with this gate's", (PINS["hex5"]["base"], PINS["hex5"]["candidate"]) == (b5, c5), PINS["hex5"])
chk("candidate is CR-free", b"\r" not in cand_raw)
chk("candidate ends with exactly one newline", cand_raw.endswith(b"\n") and not cand_raw.endswith(b"\n\n"))

# ---------------------------------------------------------------- 6. no corpus byte, anywhere
cj = git("show", "HEAD:" + JSONF); cx = git("show", "HEAD:" + JSXF)
chk("corpus JSON blob unmoved", md5(cj) == CORPUS_MD5, md5(cj))
chk("JSX blob unmoved", md5(cx) == JSX_MD5, md5(cx))
chk("corpus `version` field still names the 4.1.0 CONTENT CUT", b'"version": "4.1.0"' in cj)

# ---------------------------------------------------------------- 7. the cross-surface identity
def xsurface(d):
    out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "xsurface_v4_1_0.py"), "--dir", d],
                         cwd=ROOT, capture_output=True, text=True)
    m = re.findall(r"\b([0-9a-f]{32})\b", out.stdout)
    return out.returncode, (m[-1] if m else ""), out.stdout

tmp = tempfile.mkdtemp(prefix="k354_x_")
try:
    io.open(os.path.join(tmp, HTMLF), "wb").write(cand_raw)
    io.open(os.path.join(tmp, JSONF), "wb").write(cj)
    io.open(os.path.join(tmp, JSXF), "wb").write(cx)
    rc0, h0, o0 = xsurface(ROOT)
    rc1, h1, o1 = xsurface(tmp)
    chk("xsurface GREEN on the tracked tree", rc0 == 0 and h0 == XSURFACE_GREEN, "%d %s" % (rc0, h0))
    chk("xsurface GREEN on the candidate tree", rc1 == 0 and h1 == XSURFACE_GREEN, "%d %s" % (rc1, h1))
    chk("THE IDENTITY: before == after == %s" % XSURFACE_GREEN, h0 == h1 == XSURFACE_GREEN)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
if fail: sys.exit("VERIFY K354: %d FAILURE(S)" % fail)
print("VERIFY K354: GREEN -- the changed set is EXACTLY the declared loci, and no corpus byte moved.")
