#!/usr/bin/env python3
"""frontdoor_K353.py -- route the front door to the Adversarial Map's own surface.

Line-indexed with a per-line anchor assertion before ANY mutation, on the affordance_K352.py
pattern: if an anchor has moved, nothing is written.

FOUR EDITS, and one of them is the reason this file exists rather than a sed.

The "Being built" blurb describes the map as "the strongest continuation a maximally competent
opponent would deploy". That was written when nothing shipped, and it is a STRENGTH claim. The
moment the front door links a reader-facing (d)-only surface, that sentence becomes the label on
it -- which is exactly what canon's class_asymmetry_ruling_K350 says the licence does not survive
("THE LABEL IS LOAD-BEARING and it is part of the ruling, not presentation"). Whether the map's
authors delivered strongest or most-repairable is R1, still open. So the blurb is REMOVED, not
relinked, and its replacement card claims disposition rather than force.

  python3 tools/frontdoor_K353.py [--out <path>]      # defaults to in-place at libraries/index.html
"""
import io, os, re, sys, hashlib, argparse, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join("libraries", "index.html")
BASE_MD5, BASE_BYTES, BASE_LINES = "6aa326f71bfe496ba727a2cf5281a179", 21065, 290

CARD = """      <div class="grouplbl">Instrument &mdash; <em>a hostile pass over the flagship&rsquo;s own text</em></div>
      <a class="lib-card adjacent" href="/adversarial/">
        <h2>The Adversarial Map</h2>
        <p>For each objection in the flagship, the next move an opponent makes <em>after</em> reading our rebuttal &mdash; sorted into four dispositions. One of the four is reader-facing so far: the 22 continuations that no rewrite of our text closes, and the 9 commitments they come to rest on instead.</p>
        <div class="lib-meta"><span class="lib-badge live">live</span> <span>21 of 82 nodes</span> <span>one disposition of four</span> <span class="lib-reg">attacks our own text</span></div>
      </a>"""

# (tag, line, kind, old, new) -- kind R replace line, I insert after line,
# S replace a unique substring WITHIN that line, D delete the run old..new inclusive
EDITS = [
 ("F1-nav", 224, "S",
  '<a href="/veganism/combined">Veganism</a></nav>',
  '<a href="/veganism/combined">Veganism</a> <span aria-hidden="true">&middot;</span> '
  '<a href="/adversarial/">Adversarial Map</a></nav>'),

 ("F2-sub", 226, "R",
  '    <div class="sub">Five argument libraries and a flagship-adjacent module, under one roof.</div>',
  '    <div class="sub">Five argument libraries and a flagship-adjacent module, under one roof '
  '&mdash; and a hostile map of the flagship&rsquo;s own text.</div>'),

 ("F3-card", 267, "I", '      </a>', CARD),

 ("F4-soon-intro", 271, "R",
  '        <p>Neither is announced and neither has a date. They are named here because both are built on this corpus, and a reader who finds them later should know where they came from.</p>',
  '        <p>Not announced, and it has no date. It is named here because it is built on this '
  'corpus, and a reader who finds it later should know where it came from.</p>'),

 ("F5-drop-map-blurb", 273, "D", '          <div class="soon-item">', 277),
]

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("   " + str(got)[:220]) if got and not cond else ""))
    if not cond: fail += 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, TARGET))
    a = ap.parse_args()
    src = os.path.join(ROOT, TARGET)
    # THE BASE COMES FROM THE GIT BLOB, not from disk, because this tool REPLACES the file it
    # reads. A disk base guard is true exactly once and false forever after, so the first cut
    # of this file could not be re-run to reproduce its own output -- the defect K351 registered
    # against amend_phaseG and repaired the same way. Disk is used only as a fallback, and only
    # when it still matches the pin.
    raw = None
    try:
        blob = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + TARGET.replace(os.sep, "/")],
                              capture_output=True)
        if blob.returncode == 0 and hashlib.md5(blob.stdout).hexdigest() == BASE_MD5:
            raw, whence = blob.stdout, "git blob HEAD:%s" % TARGET.replace(os.sep, "/")
    except Exception:
        pass
    if raw is None:
        raw, whence = io.open(src, "rb").read(), "disk"
    b5, bn = hashlib.md5(raw).hexdigest(), len(raw)
    print("FRONTDOOR K353 -- %s\n  base from: %s" % (src, whence))
    chk("base is the committed front door", (b5, bn) == (BASE_MD5, BASE_BYTES), "%s / %d" % (b5, bn))
    chk("base is CR-free", b"\r" not in raw)
    if fail: sys.exit("ABORT: base is not the expected front door -- nothing written")

    lines = raw.decode("utf-8").split("\n")
    chk("base line count", len(lines) == BASE_LINES + 1, str(len(lines)))

    for tag, ln, kind, old, new in EDITS:
        got = lines[ln - 1]
        if kind == "R":
            chk("%-18s L%-4d anchor" % (tag, ln), got == old, "\n    want %r\n    got  %r" % (old, got))
        elif kind == "I":
            chk("%-18s L%-4d anchor" % (tag, ln), got == old, "got %r" % got)
        elif kind == "S":
            chk("%-18s L%-4d substring unique" % (tag, ln), got.count(old) == 1, "count %d" % got.count(old))
        elif kind == "D":
            chk("%-18s L%-4d run start" % (tag, ln), got == old, "got %r" % got)
            run = "\n".join(lines[ln - 1:new])
            chk("%-18s run names the map blurb" % tag, "<h3>The Adversarial Map</h3>" in run)
            chk("%-18s run does NOT reach the card game" % tag, "Argue the Argument" not in run)
            chk("%-18s run closes cleanly" % tag, lines[new - 1] == "          </div>", lines[new - 1])
        else:
            sys.exit("ABORT: unknown kind %r" % kind)
    if fail: sys.exit("ABORT: %d anchor assertion(s) failed -- nothing written" % fail)

    out = list(lines)
    for tag, ln, kind, old, new in sorted(EDITS, key=lambda e: -e[1]):
        if kind == "R":   out[ln - 1] = new
        elif kind == "I": out.insert(ln, new)
        elif kind == "S": out[ln - 1] = out[ln - 1].replace(old, new)
        elif kind == "D": del out[ln - 1:new]

    res = "\n".join(out); rb = res.encode("utf-8")

    HELD = [('<a class="lib-card flagship" href="/combined">', 1),
            ('<a class="lib-card" href="/right-to-die/combined">', 1),
            ('<a class="lib-card adjacent" href="/veganism/combined">', 1),
            ('<h3>Argue the Argument</h3>', 1),
            ('<section class="soon" aria-labelledby="soon-h">', 1),
            ('<b>132</b><span>objections</span>', 1)]
    GONE = ['<h3>The Adversarial Map</h3>',
            'the strongest continuation a maximally competent opponent would deploy',
            'Neither is announced and neither has a date']
    NEW = [('href="/adversarial/"', 2), ('<h2>The Adversarial Map</h2>', 1),
           ('one disposition of four', 1), ('attacks our own text', 1)]
    for s, n in HELD: chk("held x%d %r" % (n, s[:46]), res.count(s) == n, res.count(s))
    for s in GONE:    chk("gone   %r" % s[:46], res.count(s) == 0, res.count(s))
    for s, n in NEW:  chk("new  x%d %r" % (n, s[:46]), res.count(s) == n, res.count(s))
    chk("the soon-grid still holds exactly one item", res.count('<div class="soon-item">') == 1,
        res.count('<div class="soon-item">'))
    chk("no strength claim survives on the front door about the map",
        not re.search(r"strongest[^<]{0,80}(continuation|objection)", res))
    chk("result is CR-free", b"\r" not in rb)
    chk("result ends with exactly one newline", rb.endswith(b"\n") and not rb.endswith(b"\n\n"))
    chk("div balance is unchanged by the net edit",
        res.count("<div") - res.count("</div>") == lines.count("<div") - lines.count("</div>")
        or (res.count("<div") - res.count("</div>")) == 0,
        "%d vs %d" % (res.count("<div") - res.count("</div>"), 0))
    if fail: sys.exit("ABORT: %d failure(s) -- nothing written" % fail)

    io.open(a.out, "wb").write(rb)
    print("\n  WROTE %s" % a.out)
    print("  %s / %d  ->  %s / %d  (%+d bytes, %+d lines)"
          % (BASE_MD5, BASE_BYTES, hashlib.md5(rb).hexdigest(), len(rb),
             len(rb) - BASE_BYTES, len(out) - len(lines)))
    print("\nFRONTDOOR GATE: GREEN")

if __name__ == "__main__":
    main()
