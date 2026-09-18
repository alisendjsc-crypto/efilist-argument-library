#!/usr/bin/env python3
"""affordance_K352.py -- THE LEVEL-INDEPENDENT AFFORDANCE. A pin move on combined.html alone.

WHAT AND WHY. combined.html initialises `let responseLevel = "medium"` (L10278) and
window.__arglibRouteObj (L12412) never touches it, while 80 of the adversarial map's 98
`answered_by` references point at `#long` (re-derived this session against
adversarial_map_v1_3.json: long 80 / medium 11 / archetypeVariants.sophisticate 7). A reader
following a card anchor therefore lands four times in five on a depth that does not contain the
text the map says answers the objection. ccclxxiv is the master constraint: the gate is over UI
STATE, so it has a DEFAULT rather than a distribution and no corpus sweep can see it.

ONE MECHANISM, BOTH DIRECTIONS:
  outbound  a per-card [DISMANTLE] control rendered at EVERY responseLevel -- a control gated by
            the depth it exists to change cannot be found by the reader who needs it -- which
            forces `long` through setDepth() via the single card-anchor router.
  inbound   the anchor grammar gains an OPTIONAL depth suffix, `#obj-<id>@<short|medium|long>`.
            `@` is outside [A-Za-z0-9_-], so it cannot collide with any objection id, and a bare
            `#obj-<id>` keeps its exact K108 behaviour. Append-only, per canon v37.39.
            COPY LINK emits the suffix whenever the reader is not at the boot default, so the
            grammar ships with a producer rather than as an untested vocabulary.

NOT IN THIS CUT, deliberately: the default is NOT flipped to `long` (canon
`next.explicitly_NOT_recommended`; the depth ladder is a reading register and the default is
every visitor's first impression). The [NOTE] confidence coupling is NOT repaired. archetypeSel
is NOT touched (D7). No corpus byte moves on any surface, which is what makes
tools/xsurface_v4_1_0.py read IDENTICALLY before and after -- that identity is the mechanical
proof this cut touched no data.

METHOD. Line-indexed with a per-line anchor assertion, on the sweep_v4_1_0.py pattern: not sed,
not a global regex. Any failed assertion aborts before anything is written. NEVER mutates the
tracked original -- it reads combined.html and writes k352_drop/combined.html, so the operator
block still has an untouched base to guard and this can be re-run without a reset.

ASCII-only source on purpose.

  python3 tools/affordance_K352.py            # emit k352_drop/combined.html
"""
import hashlib, io, os, sys
sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, "k352_drop")
HTMLF = "combined.html"

BASE_MD5, BASE_BYTES, BASE_LINES = "72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770, 12446

# ---------------------------------------------------------------- section 1: the edits
# (tag, 1-based line, kind, expected-old, new)   kind: "R" replace that line, "I" insert after it
CSS_BLOCK = """
/* K352 -- the level-independent affordance. Rendered at EVERY responseLevel on purpose: a
   control gated by the depth it exists to change cannot be found by the reader who needs it.
   Sibling of .note-toggle in the response label, and styled off it. Hex literals here are
   3- or 6-digit DELIBERATELY: the eight 5-digit values above (#4a733, #c9033, #c5511, #33200
   and their high-contrast twins) are invalid CSS and are dropped by the parser, which is why
   the confidence badges render as bare coloured text. Measured at K352, logged, not repaired. */
.depth-jump {
  background: none; border: 1px solid #442222; color: #aa7777;
  font-family: inherit; font-size: 8px; padding: 2px 6px;
  cursor: pointer; letter-spacing: 1px; text-transform: uppercase;
  margin-left: 6px; vertical-align: middle; transition: all 0.15s ease;
}
.depth-jump:hover { border-color: #8b0000; color: #e0a0a0; }
.depth-jump[data-at="1"] { border-color: #8b0000; color: #e0a0a0; background: #2a0d0d; cursor: default; }
&.legible .depth-jump { font-size: 10px; padding: 4px 9px; }
&.high-contrast .depth-jump { background: #f5e8e8; border-color: #ddaaaa; color: #8b0000; }
&.high-contrast .depth-jump:hover { background: #e8d0d0; }
&.high-contrast .depth-jump[data-at="1"] { background: #8b0000; border-color: #8b0000; color: #ffffff; }""".rstrip("\n")

BADGE_BLOCK = (
"          /* K352: the level-independent affordance. Rendered at EVERY responseLevel -- a\n"
"             control gated by the depth it exists to change cannot be found by the reader who\n"
"             needs it. Routes through the single card-anchor router, which reaches setDepth();\n"
"             there is no parallel render path here, and archetypeSel is never touched (D7). */\n"
"          var _atLong = responseLevel === 'long';\n"
"          var _djLabel = _atLong ? 'Already at full dismantlement' : 'Open this objection at full dismantlement';\n"
"          badges += '<button class=\"depth-jump\" data-at=\"' + (_atLong ? '1' : '0') + '\" aria-label=\"' + _djLabel +\n"
"            '\" title=\"' + _djLabel + '\" onclick=\"event.stopPropagation(); __arglibRouteObj(\\'' + obj.id + '\\', \\'long\\')\">[DISMANTLE]</button>';\n"
"          return badges;"
)

ROUTER_BLOCK = (
"  /* K352: the level-independent affordance. This router never touched responseLevel, so a\n"
"     #obj-<id> deep link landed every reader on the medium default while 80 of the map's 98\n"
"     answer targets sit at long. setDepth() is the ONLY path -- it syncs the .depth-btn active\n"
"     class and calls render() itself, so exactly one render happens here either way. */\n"
"  if ((depth === 'short' || depth === 'medium' || depth === 'long') && typeof setDepth === 'function') setDepth(depth);\n"
"  else render();"
)

PENDING_BLOCK = (
"    var pk = window.__arglib.pendingObjAnchor, pd = window.__arglib.pendingObjDepth || null;\n"
"    window.__arglib.pendingObjAnchor = null; window.__arglib.pendingObjDepth = null;"
)

EDITS = [
 ("E1-css", 397, "I",
  ".note-toggle:hover { border-color: #996; color: #cc9; }",
  CSS_BLOCK),

 ("E2-covenant", 2786, "R",
  "      /* K108 card anchors: #obj-<key> / #rwe-<instance_id> -- carve out BEFORE the legacy promote (append-only covenant, canon v37.39) */",
  "      /* K108 card anchors: #obj-<key> / #rwe-<instance_id> -- carve out BEFORE the legacy promote (append-only covenant, canon v37.39)\n"
  "         K352 extends the OBJ form only, append-only: #obj-<key>@<short|medium|long> forces the depth. `@` is outside the id vocabulary\n"
  "         [A-Za-z0-9_-] so it cannot collide with any id; a bare #obj-<key> is byte-identical in behaviour; #rwe-<id>@... is NOT claimed\n"
  "         and still falls through to the legacy promote exactly as before. */"),

 ("E3-regex", 2787, "R",
  "      var cardm = /^(obj|rwe)-([A-Za-z0-9_-]+)$/.exec(raw);",
  "      var cardm = /^(obj|rwe)-([A-Za-z0-9_-]+)(?:@(short|medium|long))?$/.exec(raw);"),

 ("E4-rwe-guard", 2788, "R",
  "      if (cardm && cardm[1] === 'rwe') {",
  "      if (cardm && cardm[1] === 'rwe' && !cardm[3]) {"),

 ("E5-route-call", 2797, "R",
  "        if (typeof window.__arglibRouteObj === 'function') window.__arglibRouteObj(cardm[2]);",
  "        if (typeof window.__arglibRouteObj === 'function') window.__arglibRouteObj(cardm[2], cardm[3]);"),

 ("E6-pending-set", 2798, "R",
  "        else window.__arglib.pendingObjAnchor = cardm[2];",
  "        else { window.__arglib.pendingObjAnchor = cardm[2]; window.__arglib.pendingObjDepth = cardm[3] || null; }"),

 ("E7-badge", 10551, "R",
  "          return badges;",
  BADGE_BLOCK),

 ("E8-copylink", 10576, "R",
  "        <button class=\"copy-btn\" id=\"copy-${obj.id}\" onclick=\"event.stopPropagation(); copyResponse('${obj.id}')\">COPY RESPONSE</button><button class=\"copy-btn copy-link-btn\" onclick=\"event.stopPropagation(); copyCardLink('obj-${obj.id}', this)\">COPY LINK</button>",
  "        <button class=\"copy-btn\" id=\"copy-${obj.id}\" onclick=\"event.stopPropagation(); copyResponse('${obj.id}')\">COPY RESPONSE</button><button class=\"copy-btn copy-link-btn\" onclick=\"event.stopPropagation(); copyCardLink('obj-${obj.id}${responseLevel === 'medium' ? '' : '@' + responseLevel}', this)\">COPY LINK</button>"),

 ("E9-router-sig", 12412, "R",
  "window.__arglibRouteObj = function(key) {",
  "window.__arglibRouteObj = function(key, depth) {"),

 ("E10-router-depth", 12415, "R",
  "  render();",
  ROUTER_BLOCK),

 ("E11-pending-read", 12439, "R",
  "    var pk = window.__arglib.pendingObjAnchor; window.__arglib.pendingObjAnchor = null;",
  PENDING_BLOCK),

 ("E12-pending-call", 12440, "R",
  "    window.__arglibRouteObj(pk);",
  "    window.__arglibRouteObj(pk, pd);"),
]

# ---------------------------------------------------------------- section 2: invariants
# strings that must be BYTE-IDENTICAL in the result -- the things this cut must not disturb
HELD = [
    ('let responseLevel = "medium";', 1),                  # the default is NOT flipped
    ("  setDepth('medium');", 1),                          # boot still syncs to medium
    ('<button class="depth-btn active" data-depth="short" onclick="setDepth(\'short\')">PUNCH</button>', 1),
    ("function setDepth(depth) {", 1),                     # the only depth path, unchanged
    ("  responseLevel = depth;", 1),
    ("const hasNote = obj.note && responseLevel === 'long';", 1),   # note gates untouched
    ("if (conf !== 'full') {", 1),
    ("let archetypeSel = {};", 1),
    ("init();", 1),
]
# strings that must NOT survive
GONE = [
    "window.__arglibRouteObj = function(key) {",
    "/^(obj|rwe)-([A-Za-z0-9_-]+)$/",
    "copyCardLink('obj-${obj.id}', this)",
]
# strings that must APPEAR exactly once
NEW = [
    ("class=\"depth-jump\"", 1),
    ("\n.depth-jump {", 1),          # line-anchored: the bare substring also matches the two nested rules
    ("(?:@(short|medium|long))?", 1),
    ("pendingObjDepth", 3),
    ("__arglibRouteObj(cardm[2], cardm[3])", 1),
    ("__arglibRouteObj(pk, pd)", 1),
    ("window.__arglibRouteObj = function(key, depth) {", 1),
]

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + got) if got and not cond else ""))
    if not cond: fail += 1

src = os.path.join(ROOT, HTMLF)
raw = io.open(src, "rb").read()
b5, bn = hashlib.md5(raw).hexdigest(), len(raw)
print("AFFORDANCE K352 -- %s" % src)
chk("base is the pin v4.1.0", (b5, bn) == (BASE_MD5, BASE_BYTES), "%s / %d" % (b5, bn))
chk("base is CR-free", b"\r" not in raw)
if fail: sys.exit("ABORT: base is not the expected pin -- nothing written")

lines = raw.decode("utf-8").split("\n")
chk("base line count", len(lines) == BASE_LINES + 1, str(len(lines)))   # trailing newline -> one empty tail

# --- per-line anchor assertion, before ANY mutation -----------------------------------
for tag, ln, kind, old, new in EDITS:
    got = lines[ln - 1]
    chk("%-16s L%-6d anchor" % (tag, ln), got == old, "\n        want %r\n        got  %r" % (old, got))
if fail: sys.exit("ABORT: %d anchor assertion(s) failed -- nothing written" % fail)

# --- apply, descending so earlier line numbers stay valid ------------------------------
out = list(lines)
for tag, ln, kind, old, new in sorted(EDITS, key=lambda e: -e[1]):
    if kind == "R":   out[ln - 1] = new
    elif kind == "I": out.insert(ln, new)
    else:             sys.exit("ABORT: unknown kind %r" % kind)

res = "\n".join(out)
rb = res.encode("utf-8")

for s, n in HELD: chk("held x%d %r" % (n, s[:52]), res.count(s) == n, str(res.count(s)))
for s in GONE:    chk("gone   %r" % s[:52], res.count(s) == 0, str(res.count(s)))
for s, n in NEW:  chk("new  x%d %r" % (n, s[:52]), res.count(s) == n, str(res.count(s)))
chk("result is CR-free", b"\r" not in rb)
chk("result ends with exactly one newline", rb.endswith(b"\n") and not rb.endswith(b"\n\n"))
chk("result is pure ASCII outside the base's own non-ASCII",
    all(ord(c) < 128 for e in EDITS for c in e[4]))

if fail: sys.exit("ABORT: %d failure(s) -- nothing written" % fail)

os.makedirs(DROP, exist_ok=True)
io.open(os.path.join(DROP, HTMLF), "wb").write(rb)
print("\n  WROTE %s" % os.path.join(DROP, HTMLF))
print("  PIN: %s  %s / %d  ->  %s / %d  (%+d bytes, %+d lines)"
      % (HTMLF, BASE_MD5, BASE_BYTES, hashlib.md5(rb).hexdigest(), len(rb),
         len(rb) - BASE_BYTES, len(out) - len(lines)))
print("\nAFFORDANCE GATE: GREEN")
