#!/usr/bin/env python3
"""note_confidence_K354.py -- THE NOTE AND THE CONFIDENCE LAYER. A pin move on combined.html alone.

WHAT AND WHY. Three defects in one region, all of them mechanism rather than stance.

  1  THE [NOTE] CONTROL IS GATED ON A FIELD ITS CONTAINER IGNORES. The note <div> is emitted on
     `obj.note && responseLevel === 'long'` with no confidence condition; the [NOTE] button that
     reveals it sits inside `if (conf !== 'full')`, and toggleNote has exactly one caller. So the
     container is emitted for 9 nodes and the control for 7. Measured: violence-as-reductio
     (106w, ungraded) and solipsism (89w, confidence:full) are STRUCTURALLY UNREACHABLE by any
     reader -- 195 of 544 words, 35.8% of the layer, and the two longest. solipsism is the
     reductio: its note is the text that EXPLAINS its confidence:full, and that value is exactly
     what suppresses the button. K352 ruled the flagship wrong and the JSX right on the
     flagship's OWN internal inconsistency; this is that repair.

  2  THE UNGRADED ARE SILENTLY UPGRADED. `const conf = obj.confidence || 'full'` defaults the 64
     never-graded objections to the top grade, so a missing badge meant either "graded full" (11)
     or "never graded" (64) and a reader could not tell them apart. The badge now reads
     obj.confidence DIRECTLY: 18 cards carry a grade, 64 carry none, and absence means UNGRADED.
     `full` renders FULL. Ruled by Josiah at K354 on this seat's stated recommendation.

  3  SIX CONFIDENCE DECLARATIONS HAVE BEEN INVALID CSS SINCE THEY WERE WRITTEN. Eleven 5-digit
     hex literals -- 3-digit colour plus 2 alpha digits, intending the 8-digit form. Five-digit
     hex is invalid and the WHOLE declaration is dropped, so the badges have rendered as bare
     coloured text with no border and no background in all three modes, and .note-toggle has
     rendered as browser-default button chrome rather than as [DISMANTLE]'s sibling. WI-K343
     logged this and counted EIGHT; the count is ELEVEN over SIX declarations. The three it
     missed are .confidence-full's pair (dead code until defect 2 is repaired -- this cut makes
     it live, which is why it rides) and .note-toggle's #33200 (the border of the very control
     defect 1 puts on two more cards). A naive grep returns 15: four of those are inside K352's
     own COMMENT documenting the bug, which is ccclxxix's marker trap and is why this tool
     counts DECLARATIONS and gates the result at zero.

  .note-toggle's border resolves to #332 rather than the literal expansion #33332200, which is a
  fully transparent border and no repair anyone would recognise. The artifact declares the
  answer: K352's .depth-jump comment says it is "sibling of .note-toggle ... and styled off it"
  and uses a visible dim #442222.

  .provisional-response is REMOVED, rule and class emission both -- an unlabelled 70% opacity
  band on one node, invisible to a screen reader, a contrast cost, and a restatement of the
  PROVISIONAL badge that renders in the section label directly above the same box. Subtraction,
  not redesign, and nothing is left dangling as a future locator trap.

  A high-contrast rule for .confidence-full is ADDED because the ruling requires it: #4a7 on the
  high-contrast light ground is about 2.5:1, so shipping FULL without it would introduce an
  accessibility defect in the session that exists to remove one.

NOT IN THIS CUT, deliberately: no corpus byte on any surface, so tools/xsurface_v4_1_0.py reads
IDENTICALLY before and after -- that identity is the mechanical proof this touched no data. The
note CONTAINER is not touched (it was always right). responseLevel's default is NOT flipped
(canon `next.explicitly_NOT_recommended`). setDepth, the K352 affordance, the anchor grammar,
archetypeSel and toggleNote are all asserted byte-identical.

METHOD. Line-indexed with a per-line anchor assertion before any mutation, on the
affordance_K352.py pattern: not sed, not a global regex. NEVER mutates the tracked original --
it reads combined.html and writes k354_drop/combined.html, so the operator block still has an
untouched base to guard and this is re-runnable without a reset.

THE [NOTE] BUTTON'S MARKUP IS NOT RETYPED. It is EXTRACTED from the base's own line 10565 and
re-emitted byte-for-byte, so this cut provably changes the control's CONDITION and not the
control. Asserted.

ASCII-only source on purpose.

  python3 tools/note_confidence_K354.py       # emit k354_drop/combined.html
"""
import hashlib, io, os, re, sys
sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, "k354_drop")
HTMLF = "combined.html"

BASE_MD5, BASE_BYTES, BASE_LINES = "f095c0ce0e5a1d796d57fa5a5dd62f7d", 2985989, 12482

HEX5 = re.compile(r"#[0-9a-fA-F]{5}\b")
HEX8 = re.compile(r"#[0-9a-fA-F]{8}\b")

# ---------------------------------------------------------------- section 1: the new blocks
CSS_FULL = ".confidence-full { color: #4a7; border: 1px solid #44aa7733; background: #44aa7711; }"
CSS_STRONG = ".confidence-strong { color: #c90; border: 1px solid #cc990033; background: #cc990011; }"
CSS_PROV = ".confidence-provisional { color: #c55; border: 1px solid #cc555533; background: #cc555511; }"
CSS_TOGGLE = "  background: none; border: 1px solid #332; color: #996;"

# K352's comment said "logged, not repaired" and named four of the literals inline. Both claims
# are false after this cut, and the inline literals are the marker a scan keeps matching, so the
# four comment lines are rewritten 1:1 -- same line count, no shift.
CSS_CMT_401 = "   Sibling of .note-toggle in the response label, and styled off it. Hex literals here are"
CSS_CMT_402 = "   3- or 6-digit DELIBERATELY. The 5-digit values that stood above were REPAIRED at K354 to"
CSS_CMT_403 = "   the 8-digit form their author intended: eleven literals over SIX declarations, not the"
CSS_CMT_404 = "   eight K352 counted -- .confidence-full and .note-toggle were the two it missed. */"

# K354, ccclxxx: in HIGH CONTRAST the badges take the repaired BORDER and NO FILL. The dark-mode
# fills are dark tints; composited over the high-contrast LIGHT ground they darken it under dark
# text, and repairing the invalid background therefore LOWERS contrast -- measured, STRONG falls
# 4.16:1 -> 3.84:1, i.e. the badge is less legible repaired than it was broken. The invalid
# declaration was DROPPED, so everything downstream was computed against its absence; repairing
# it is an ADDITION to the cascade rather than a restoration of intent. `background: none` keeps
# the high-contrast ground exactly as the reader has always seen it, repairs the border, and
# regresses nothing. The authored colours are untouched.
CSS_HC_STRONG = "&.high-contrast .confidence-badge.confidence-strong { color: #960; border-color: #99660044; background: none; }"
CSS_HC_PROV = "&.high-contrast .confidence-badge.confidence-provisional { color: #a33; border-color: #aa333344; background: none; }"
# K354: two high-contrast rules this cut REQUIRES rather than chooses. FULL never rendered
# before, so it never needed one -- #4a7 is about 2.5:1 on the high-contrast light ground, and
# shipping it without this would introduce an accessibility defect in the session that exists to
# remove one (#174 measures 4.75:1). .note-toggle never had one either: its #996 measures 2.51:1
# there, under even the 3:1 floor for a UI component, while its [DISMANTLE] sibling -- which
# K352 says is "styled off it" -- has had one since K352. Making the button legible on two more
# cards while leaving it illegible in the accessibility mode is not a repair. #5c5520 on #f5f3e8
# measures 6.81:1, and the gate computes all of these from the browser rather than trusting them.
CSS_HC_NEW = (
"&.high-contrast .confidence-badge.confidence-full { color: #174; border-color: #11774444; background: none; }\n"
"&.high-contrast .note-toggle { background: #f5f3e8; border-color: #ccc8a8; color: #5c5520; }"
)

CSS_PROV_RESP = (
"/* K354 -- the provisional opacity band is GONE, the rule and the class emission both. It was a\n"
"   70% dim on the one provisional node's long response: unlabelled, conveying nothing to a\n"
"   screen reader, costing contrast, and restating the PROVISIONAL badge that renders in the\n"
"   section label directly above the same box. Subtraction, not redesign; nothing dangles. */"
)

JS_HEAD = (
"          /* K354 -- the badge reads obj.confidence DIRECTLY. What stood here defaulted a\n"
"             missing grade to the top one, so the 64 NEVER-GRADED objections were silently\n"
"             upgraded and the 11 affirmatively graded ones hidden among them; absence of a\n"
"             badge now means UNGRADED, which is true. An unknown value still renders nothing. */\n"
"          const _confLabel = obj.confidence === 'full' ? 'FULL'\n"
"            : obj.confidence === 'strong' ? 'STRONG'\n"
"            : obj.confidence === 'provisional' ? 'PROVISIONAL' : '';\n"
"          let badges = '';\n"
"          if (_confLabel) {\n"
"            badges += '<span class=\"confidence-badge confidence-' + obj.confidence + '\">' + _confLabel + '</span>';\n"
"          }\n"
"          /* K354 -- the [NOTE] control is LIFTED OUT of the confidence branch so its condition\n"
"             equals the note container's below: 9 containers, 9 controls. It was gated on a\n"
"             field its own container ignores, and toggleNote has exactly one caller, so\n"
"             solipsism's note -- the text that explains its own confidence grade -- was\n"
"             suppressed by the very value it explains. The button's markup below is the base's\n"
"             own, carried over unchanged: this repairs the CONDITION, not the control. */\n"
"          if (obj.note && responseLevel === 'long') {"
)
JS_RESPBOX = '        ${archetypePills(obj)}${rweBlock(obj)}<div class="response-box">${_bodyText}</div>'

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + got) if got and not cond else ""))
    if not cond: fail += 1

src = os.path.join(ROOT, HTMLF)
raw = io.open(src, "rb").read()
b5, bn = hashlib.md5(raw).hexdigest(), len(raw)
print("NOTE + CONFIDENCE K354 -- %s" % src)
chk("base is the pin v4.1.1", (b5, bn) == (BASE_MD5, BASE_BYTES), "%s / %d" % (b5, bn))
chk("base is CR-free", b"\r" not in raw)
if fail: sys.exit("ABORT: base is not the expected pin -- nothing written")

base_text = raw.decode("utf-8")
lines = base_text.split("\n")
chk("base line count", len(lines) == BASE_LINES + 1, str(len(lines)))
if fail: sys.exit("ABORT: base shape -- nothing written")

# --- the [NOTE] button's markup, EXTRACTED from the base rather than retyped -----------
L10565 = lines[10565 - 1]
try:
    BTN = L10565.split("(hasNote ? ", 1)[1].rsplit(" : '');", 1)[0]
except IndexError:
    BTN = ""
chk("button markup extracted from the base", BTN.startswith("'<button class=\"note-toggle\"")
    and BTN.endswith("[NOTE]</button>'"), repr(BTN[:60]))
if fail: sys.exit("ABORT: could not extract the control from the base -- nothing written")
JS_NOTE = "            badges += " + BTN + ";"

# ---------------------------------------------------------------- section 2: the edits
# (tag, 1-based line, kind, expected-old, new)  kind: R replace, D delete, I insert after
EDITS = [
 ("C1-full",        378, "R", ".confidence-full { color: #4a7; border: 1px solid #4a733; background: #4a711; }", CSS_FULL),
 ("C2-strong",      379, "R", ".confidence-strong { color: #c90; border: 1px solid #c9033; background: #c9011; }", CSS_STRONG),
 ("C3-prov",        380, "R", ".confidence-provisional { color: #c55; border: 1px solid #c5533; background: #c5511; }", CSS_PROV),
 ("C4-toggle",      392, "R", "  background: none; border: 1px solid #33200; color: #996;", CSS_TOGGLE),
 ("C5-cmt401",      401, "R", "   Sibling of .note-toggle in the response label, and styled off it. Hex literals here are", CSS_CMT_401),
 ("C6-cmt402",      402, "R", "   3- or 6-digit DELIBERATELY: the eight 5-digit values above (#4a733, #c9033, #c5511, #33200", CSS_CMT_402),
 ("C7-cmt403",      403, "R", "   and their high-contrast twins) are invalid CSS and are dropped by the parser, which is why", CSS_CMT_403),
 ("C8-cmt404",      404, "R", "   the confidence badges render as bare coloured text. Measured at K352, logged, not repaired. */", CSS_CMT_404),
 ("C9-hcfull",      419, "I", "&.high-contrast .confidence-note { background: #ede8df; border-color: #cca; color: #665; }", CSS_HC_NEW),
 ("C10-hcstrong",   420, "R", "&.high-contrast .confidence-badge.confidence-strong { color: #960; border-color: #96044; background: #96011; }", CSS_HC_STRONG),
 ("C11-hcprov",     421, "R", "&.high-contrast .confidence-badge.confidence-provisional { color: #a33; border-color: #a3344; background: #a3311; }", CSS_HC_PROV),
 ("C12-provresp",   422, "R", ".provisional-response { opacity: 0.7; }", CSS_PROV_RESP),
 ("J1-head",      10559, "R", "          const conf = obj.confidence || 'full';", JS_HEAD),
 ("J2-del",       10560, "D", "          let badges = '';", None),
 ("J3-del",       10561, "D", "          if (conf !== 'full') {", None),
 ("J4-del",       10562, "D", "            const label = conf === 'strong' ? 'STRONG' : 'PROVISIONAL';", None),
 ("J5-del",       10563, "D", "            const hasNote = obj.note && responseLevel === 'long';", None),
 ("J6-note",      10564, "R", "            badges += '<span class=\"confidence-badge confidence-' + conf + '\">' + label + '</span>' +", JS_NOTE),
 ("J7-del",       10565, "D", L10565, None),
 ("J8-close",     10566, "A", "          }", None),
 ("J9-respbox",   10583, "R", "        ${archetypePills(obj)}${rweBlock(obj)}<div class=\"response-box ${(obj.confidence === 'provisional' && responseLevel === 'long') ? 'provisional-response' : ''}\">${_bodyText}</div>", JS_RESPBOX),
]

# ---------------------------------------------------------------- section 3: invariants
HELD = [
    ('let responseLevel = "medium";', 1),
    ("function setDepth(depth) {", 1),
    ("  responseLevel = depth;", 1),
    ('class="depth-jump"', 1),
    ("(?:@(short|medium|long))?", 1),
    ("__arglibRouteObj(pk, pd)", 1),
    ("function toggleNote(id) {", 1),
    ("let archetypeSel = {};", 1),
    ("\n.confidence-note {", 1),   # line-anchored: the bare substring also matches the two nested rules
    ('.confidence-note.visible { display: block; }', 1),
    # THE RULING: the note CONTAINER is not touched.
    ("${obj.note && responseLevel === 'long' ? '<div class=\"confidence-note\" id=\"note-' + obj.id + '\">' + obj.note + '</div>' : ''}", 1),
    ('class="note-toggle"', 1),
    ("init();", 1),
]
GONE = [
    "const conf = obj.confidence || 'full';",
    "if (conf !== 'full') {",
    "const hasNote = obj.note && responseLevel === 'long';",
    "provisional-response",
]
NEW = [
    ("_confLabel", 3),
    ("obj.confidence === 'full' ? 'FULL'", 1),
    ('<div class="response-box">', 1),
    ("\n.confidence-full {", 1),
    ("confidence-badge.confidence-full", 1),
    ("&.high-contrast .note-toggle {", 1),
]
INTRODUCED_HEX8 = ["#44aa7733", "#44aa7711", "#cc990033", "#cc990011", "#cc555533",
                   "#cc555511", "#99660044", "#aa333344", "#11774444"]

# --- per-line anchor assertion, before ANY mutation -----------------------------------
for tag, ln, kind, old, new in EDITS:
    got = lines[ln - 1]
    chk("%-14s L%-6d anchor" % (tag, ln), got == old, "\n        want %r\n        got  %r" % (old, got))
if fail: sys.exit("ABORT: %d anchor assertion(s) failed -- nothing written" % fail)

# --- apply, descending so earlier line numbers stay valid ------------------------------
out = list(lines)
for tag, ln, kind, old, new in sorted(EDITS, key=lambda e: -e[1]):
    if kind == "R":   out[ln - 1] = new
    elif kind == "D": del out[ln - 1]
    elif kind == "I": out.insert(ln, new)
    elif kind == "A": pass          # asserted above, deliberately unmutated
    else:             sys.exit("ABORT: unknown kind %r" % kind)

res = "\n".join(out)
rb = res.encode("utf-8")

for s, n in HELD: chk("held x%d %r" % (n, s[:54]), res.count(s) == n, str(res.count(s)))
for s in GONE:    chk("gone   %r" % s[:54], res.count(s) == 0, str(res.count(s)))
for s, n in NEW:  chk("new  x%d %r" % (n, s[:54]), res.count(s) == n, str(res.count(s)))

# the locator-proof hex gate: count LITERALS, not names, and require the base to be non-zero so
# the check is proved non-vacuous in both directions (ccclxxix).
b5c, r5c = len(HEX5.findall(base_text)), len(HEX5.findall(res))
chk("base carries 5-digit hex (non-vacuity)", b5c == 15, str(b5c))
chk("result carries ZERO 5-digit hex", r5c == 0, str(r5c))
d8 = sorted(set(HEX8.findall(res)) - set(HEX8.findall(base_text)))
chk("8-digit hex introduced is exactly the declared set", d8 == sorted(set(INTRODUCED_HEX8)), repr(d8))

chk("the control's markup is the base's, byte-for-byte", BTN in res and res.count(BTN) == 1)
chk("result is CR-free", b"\r" not in rb)
chk("result ends with exactly one newline", rb.endswith(b"\n") and not rb.endswith(b"\n\n"))
chk("every emitted byte is ASCII",
    all(ord(c) < 128 for e in EDITS if e[4] for c in e[4]))

if fail: sys.exit("ABORT: %d failure(s) -- nothing written" % fail)

os.makedirs(DROP, exist_ok=True)
io.open(os.path.join(DROP, HTMLF), "wb").write(rb)
# ONE binding for every constant this cut produces. verify_K354.py RECOMPUTES each and asserts
# against it, and the operator block gates the same values -- so no hash is ever hand-typed
# twice (ccclxii).
import json as _json
io.open(os.path.join(ROOT, "tools", "k354_cut_pins.json"), "w", newline="\n").write(_json.dumps({
    "base": {"md5": BASE_MD5, "bytes": BASE_BYTES, "lines": BASE_LINES},
    "candidate": {"md5": hashlib.md5(rb).hexdigest(), "bytes": len(rb), "lines": len(out) - 1},
    "delta": {"bytes": len(rb) - BASE_BYTES, "lines": len(out) - len(lines)},
    "hex5": {"base": b5c, "candidate": r5c},
    "hex8_introduced": sorted(set(INTRODUCED_HEX8)),
}, indent=1, sort_keys=True) + "\n")
print("\n  WROTE %s" % os.path.join(DROP, HTMLF))
print("  PIN: %s  %s / %d  ->  %s / %d  (%+d bytes, %+d lines)"
      % (HTMLF, BASE_MD5, BASE_BYTES, hashlib.md5(rb).hexdigest(), len(rb),
         len(rb) - BASE_BYTES, len(out) - len(lines)))
print("\nNOTE + CONFIDENCE GATE: GREEN")
