#!/usr/bin/env python3
"""Pack the house layer: layer/src/ -> site/wuld-layer.{css,js}. Generative, self-checking.

    python3 layer/pack_layer.py           write site/wuld-layer.css and site/wuld-layer.js
    python3 layer/pack_layer.py --check   THE GATE: pack in memory, compare with site/ byte for
                                          byte, write nothing; exit 0 only if both are equal

Edit the parts in layer/src/, never the packed files: site/ is served as-is on push to main, and
every library page links both files. After an edit, run the packer, then --check (it must pass),
then commit the parts and the pack together. A commit that moves one without the other fails the
gate.

Lineage. Restored at WI-K410 (2026-09-26) from wuld-ink archive/measurement/k313c_packlayer.py
(filed at WI-K316, commit 43f0c7b), whose build/ folder was never committed anywhere. The parts
were split out of the served pack by that packer's own banners and re-packed byte for byte equal
(receipt: wuld-ink docs/ledger/2026-09-26-WI-K410.split.py). Two changes from K313c, both so the
parts alone determine the pack:
  - the JS's FURNITURE tail is a part (wuld-furniture.js), not bytes read back out of the
    previous pack, which made the old packer's output depend on its own last output;
  - --check compares with site/ itself, not with a golden copy parked in /tmp.
The joiners are unchanged: a fixed head, one banner per part except the JS's first, the tail with
no banner. So every byte of a pack is head, banner, part or tail, and verify() proves it.
"""
import sys, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'layer' / 'src'
SITE = ROOT / 'site'
BAR = b'=' * 94
def banner(n): return b'\n\n/* ' + BAR + b'\n   ' + n.encode() + b'\n   ' + BAR + b' */\n\n'
def md5(b): return hashlib.md5(b).hexdigest()

CSS_HEAD = (b'/* wuld-layer.css -- library.wuld.ink shared presentation + cosmetic layer.\n'
            b'   Concatenated by pack_layer.py. Edit the sources in build/, never this file. */\n')
CSS = ['wuld-type.css', 'wuld-bezel.css', 'wuld-vfx.css']
JS_HEAD = b'/* wuld-layer.js -- library.wuld.ink cosmetic + sound layer. */\n'
JS = ['wuld-vfx.js', 'wuld-sfx.js', 'wuld-fb.js', 'wuld-tour.js']
JS_TAIL = 'wuld-furniture.js'


def pack(head, names, first_banner, tail_name=None):
    out = bytearray(head); parts = []
    for k, n in enumerate(names):
        d = (SRC / n).read_bytes(); parts.append(d)
        out += (banner(n) if (k or first_banner) else b'') + d
    tail = (SRC / tail_name).read_bytes() if tail_name else b''
    out += tail
    return bytes(out), parts, tail


def verify(data, head, names, parts, first_banner, tail, label):
    """Every part present exactly once and in order; the pack is head + banners + parts + tail and
    nothing else. A packer that cannot account for every byte it emits is a second source of truth."""
    pos = 0
    for n, d in zip(names, parts):
        if not d:
            sys.exit('*** %s: %s is empty' % (label, n))
        i = data.find(d, pos)
        if i < 0: sys.exit('*** %s: %s missing from the pack' % (label, n))
        if data.count(d) != 1: sys.exit('*** %s: %s appears %d times' % (label, n, data.count(d)))
        pos = i + len(d)
    rebuilt = bytearray(head)
    for k, (n, d) in enumerate(zip(names, parts)):
        rebuilt += (banner(n) if (k or first_banner) else b'') + d
    rebuilt += tail
    if bytes(rebuilt) != data:
        sys.exit('*** %s: pack is not head + banners + parts + tail' % label)
    print('  %s: %d parts%s, in order, each once; every byte accounted for'
          % (label, len(parts), ' + tail' if tail else ''))


css, cp, _ = pack(CSS_HEAD, CSS, True)
js, jp, jt = pack(JS_HEAD, JS, False, JS_TAIL)
verify(css, CSS_HEAD, CSS, cp, True, b'', 'css')
verify(js, JS_HEAD, JS, jp, False, jt, 'js ')

if '--check' in sys.argv[1:]:
    bad = 0
    for name, data in (('wuld-layer.css', css), ('wuld-layer.js', js)):
        served = (SITE / name).read_bytes() if (SITE / name).exists() else b''
        ok = served == data
        bad += not ok
        print('  %-15s %s  pack %6d B %s   site %6d B %s'
              % (name, 'EQUAL' if ok else 'DIFF ', len(data), md5(data), len(served), md5(served)))
    if bad:
        sys.exit('*** GATE RED: %d of 2 packed files differ from site/. Run the packer, or restore '
                 'the part that moved.' % bad)
    print('  GATE GREEN: site/ is exactly the pack of layer/src/')
    sys.exit(0)

for name, data in (('wuld-layer.css', css), ('wuld-layer.js', js)):
    prev = (SITE / name).read_bytes() if (SITE / name).exists() else b''
    (SITE / name).write_bytes(data)
    print('  %-15s %6d B  (%+d)  md5=%s' % (name, len(data), len(data) - len(prev), md5(data)))
