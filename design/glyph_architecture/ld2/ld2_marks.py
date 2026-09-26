#!/usr/bin/env python3
"""ld2_marks.py -- the design lane's LD2 proposals as DATA, drawn from icons/gen_icons.py's own grids.

Design lane (seat l), 2026-09-26, America/Phoenix. Relay R0144. Nothing here is served: the sheet and the
prototypes read it. If Josiah picks a proposal, its data moves into icons/gen_icons.py, which stays the one
source of every served mark (law 12), and this file keeps only what he did not pick.

THE RULE (R0144): a motion earns its place only if it says its mark's own sentence, once. So each library
mark's one-shot below is written as its sentence first and its rects second; a verb that the sentence does
not contain is not used. Only opacity and transform move. Nothing loops.

Loading gen_icons.py runs it (it is a script): it is run in a throwaway directory, so its SVG/PNG outputs
never land in the repo, and its own asserts (pinned sigils.json, the silhouette law) run first.
"""
import contextlib, io, itertools, os, runpy, tempfile, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
GEN = os.path.join(REPO, 'icons', 'gen_icons.py')


def load_generator():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                ns = runpy.run_path(GEN, run_name='gen_icons')
        finally:
            os.chdir(cwd)
    return ns


G = load_generator()
ICONS, TIERS, TITLE, cells = G['ICONS'], G['TIERS'], G['TITLE'], G['cells']
ACC = G['ACC']
TIER_COLOUR = {1: '#ff3333', 2: '#ff6633', 3: '#cc9900', 4: '#6699cc', 5: '#a273d0'}   # flagship TIERS, measured
WINGS = ['right-to-die', 'abortion', 'transgenderism', 'anthropocentrism', 'veganism']


def lib(name):
    """A library mark as [x, y, w, h, role] rects, from the favicon grid."""
    return [[x, y, w, h, 'lit' if c == ACC else 'chrome'] for x, y, w, h, c in ICONS[name][1]]


def says(name):
    return ICONS[name][0].split(' — ')[1]


# ------------------------------------------------------------------------------------------------------
# A. THE LIBRARY MARKS SPEAK ONCE. (rect index, verb, delay s). Verbs, each a word the sentence uses:
#    fill  a block appears (opacity)             dx   an edge draws from its left end
#    dxm   an edge draws from its middle out     dy   an edge draws down from its top
#    dym   an edge grows from its middle out     stack  a rung is set down from above
#    n s e w  a part arrives from outside, from above / below / the right / the left
LIB_MOTION = {
    'libraries': ('its six cells fill in reading order, the lit one in its place',
                  [(0, 'fill', 0), (1, 'fill', .08), (2, 'fill', .16), (3, 'fill', .24), (4, 'fill', .32),
                   (5, 'fill', .40)]),
    'combined': ('the ladder stacks rung by rung from the shortest; the top rung, lit, is set last',
                 [(4, 'stack', 0), (3, 'stack', .1), (2, 'stack', .2), (1, 'stack', .3), (0, 'stack', .4)]),
    'right-to-die': ('the doorway draws, lintel then jambs; the lit step appears in the opening and does not move',
                     [(0, 'dx', 0), (1, 'dy', .25), (2, 'dy', .25), (3, 'fill', .6)]),
    'abortion': ('the stem grows and forks; both branches appear together',
                 [(0, 'dx', 0), (1, 'dym', .25), (2, 'fill', .5), (3, 'fill', .5)]),
    'transgenderism': ('both nodes appear together; the edge draws from its middle, outward both ways at once',
                       [(0, 'fill', 0), (2, 'fill', 0), (1, 'dxm', .25)]),
    'anthropocentrism': ('the four peers arrive together, each from outside; the centre stays empty',
                         [(0, 'n', 0), (1, 'w', 0), (2, 'e', 0), (3, 's', 0)]),
    'veganism': ('both nodes appear together; the boundary closes around them from all four sides at once',
                 [(4, 'fill', 0), (5, 'fill', 0), (0, 'n', .3), (1, 's', .3), (2, 'w', .3), (3, 'e', .3)]),
}
DUR = {'fill': .3, 'dx': .3, 'dxm': .35, 'dy': .3, 'dym': .3, 'stack': .3, 'n': .45, 's': .45, 'e': .45, 'w': .45}
for _n, (_s, _m) in LIB_MOTION.items():
    assert _n in ICONS and sorted(i for i, _, _ in _m) == list(range(len(ICONS[_n][1]))), (_n, 'every rect moves once')


def lib_span(name):
    return max(d + DUR[v] for _, v, d in LIB_MOTION[name][1])


def glyph(rects, px, cls='sg', motion=None, moves=(), lit_class='sg-lit'):
    """One mark as inline SVG. motion: {rect index: (verb, delay)} adds m-<verb> and a --d delay;
    moves: rect indices that carry sg-m (the tier one-shots)."""
    motion = motion or {}
    out = []
    for i, (x, y, w, h, role) in enumerate(rects):
        c = (lit_class if role == 'lit' else 'sg-c') + (' sg-m' if i in moves else '')
        st = ''
        if i in motion:
            v, d = motion[i]
            c += ' m-' + v
            if d:
                st = ' style="--d:%gs"' % d
        out.append('<rect class="%s"%s x="%d" y="%d" width="%d" height="%d"/>' % (c, st, x, y, w, h))
    return ('<svg class="%s" viewBox="0 0 16 16" width="%d" height="%d" aria-hidden="true">%s</svg>'
            % (cls, px, px, ''.join(out)))


def lib_glyph(name, px, moving=True):
    m = {i: (v, d) for i, v, d in LIB_MOTION[name][1]} if moving else None
    return glyph(lib(name), px, motion=m)


def tier_glyph(t, px, moving=True, lit_class='sg-lit'):
    return glyph(TIERS[t]['rects'], px, moves=TIERS[t]['moves'] if moving else (), lit_class=lit_class)


# The motion CSS. GATE is the house layer's own (vfx tier, dark ground, motion allowed); the sheet passes its
# own selector for its demo panels. PLAY is the selector of an element that is saying its sentence now.
def motion_css(gate='html.wz-vfx:not(.wz-lightbg)', play='.play'):
    kf = '''@keyframes lm-fill{from{opacity:0}to{opacity:1}}
@keyframes lm-dx{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes lm-dy{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes lm-stack{from{opacity:0;transform:translateY(-3px)}to{opacity:1;transform:translateY(0)}}
@keyframes lm-n{from{opacity:0;transform:translateY(-2px)}to{opacity:1;transform:translateY(0)}}
@keyframes lm-s{from{opacity:0;transform:translateY(2px)}to{opacity:1;transform:translateY(0)}}
@keyframes lm-w{from{opacity:0;transform:translateX(-2px)}to{opacity:1;transform:translateX(0)}}
@keyframes lm-e{from{opacity:0;transform:translateX(2px)}to{opacity:1;transform:translateX(0)}}
.m-dx,.m-dxm,.m-dy,.m-dym{transform-box:fill-box}
.m-dx{transform-origin:0 50%}.m-dy{transform-origin:50% 0}.m-dxm,.m-dym{transform-origin:50% 50%}
'''
    kmap = {'fill': 'lm-fill', 'dx': 'lm-dx', 'dxm': 'lm-dx', 'dy': 'lm-dy', 'dym': 'lm-dy', 'stack': 'lm-stack',
            'n': 'lm-n', 's': 'lm-s', 'e': 'lm-e', 'w': 'lm-w'}
    rules = ','.join('%s %s .m-%s' % (gate, play, v) for v in DUR)
    per = ''.join('%s %s .m-%s{animation-name:%s;animation-duration:%gs}\n' % (gate, play, v, kmap[v], DUR[v])
                  for v in DUR)
    return (kf + '@media (prefers-reduced-motion:no-preference){\n'
            + rules + '{animation-timing-function:ease-out;animation-fill-mode:both;animation-delay:var(--d,0s)}\n'
            + per + '}\n')


# The tier one-shots, copied from the front door (argue S43's ag-sig-*), for anchor arrival (proposal D).
TIER_KF = '''@keyframes lib-sig-return{0%{transform:translateX(0)}45%{transform:translateX(3px)}100%{transform:translateX(0)}}
@keyframes lib-sig-handed{from{opacity:0;transform:translate(-5px,-5px)}to{opacity:1;transform:translate(0,0)}}
@keyframes lib-sig-rest{from{opacity:.35;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
@keyframes lib-sig-descend{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
@keyframes lib-sig-close{from{opacity:0;transform:scale(1.4)}to{opacity:1;transform:scale(1)}}
.t5 .sg-m{transform-box:view-box;transform-origin:8px 8px}
'''
TIER_ANIM = {1: 'lib-sig-return .7s ease-in-out', 2: 'lib-sig-handed .7s ease-out', 3: 'lib-sig-rest .6s ease-out',
             4: 'lib-sig-descend .7s ease-out', 5: 'lib-sig-close .7s ease-out'}


def tier_arrival_css(gate='html.wz-vfx:not(.wz-lightbg)', play='.obj.flash'):
    return (TIER_KF + '@media (prefers-reduced-motion:no-preference){\n'
            + ''.join('%s %s .t%d .sg-m{animation:%s .2s both}\n' % (gate, play, t, a) for t, a in TIER_ANIM.items())
            + '}\n')


# ------------------------------------------------------------------------------------------------------
# B. THE PLATES: each wing's mark drawn large on its pixel grid, its parts named in the grammar's words and
#    its own sentence's. (label, side, anchor cell x, anchor cell y). Side L/R/T/B runs a leader to that gutter;
#    'in' writes the label inside the mark, centred on the anchor. Every label is placed for THIS grid, so a
#    changed grid stops the build (the front door's plate does the same).
PLATES = {
    'right-to-die': [('edge · the lintel', 'R', 14, 3), ('edge · a jamb', 'L', 2, 8),
                     ('the opening', 'R', 10, 8), ('lit · the step', 'R', 9, 13.5)],
    'abortion': [('edge · the stem', 'L', 1, 8), ('edge · the fork', 'L', 8, 4),
                 ('node · a branch', 'R', 14, 4), ('lit · a branch', 'R', 14, 13)],
    'transgenderism': [('node', 'L', 1, 8), ('lit · node', 'R', 15, 8),
                       ('edge · no arrowhead either way', 'B', 8, 9)],
    'anthropocentrism': [('node · a peer', 'T', 8, 1), ('node · a peer', 'L', 1, 8),
                         ('lit · a peer', 'R', 15, 8), ('node · a peer', 'B', 8, 15),
                         ('empty', 'in', 8, 8)],
    'veganism': [('edge · the boundary', 'R', 15, 4), ('node', 'L', 4, 8.5), ('lit · node', 'R', 12, 8.5)],
}
PLATE_GRID = {n: lib(n) for n in PLATES}      # asserted below against the favicon grids, so labels cannot drift
assert PLATE_GRID['right-to-die'] == [[2, 2, 12, 2, 'chrome'], [2, 4, 2, 11, 'chrome'], [12, 4, 2, 11, 'chrome'],
                                      [7, 12, 2, 3, 'lit']], 'plate labels: right-to-die'
assert PLATE_GRID['anthropocentrism'] == [[6, 1, 4, 4, 'chrome'], [1, 6, 4, 4, 'chrome'], [11, 6, 4, 4, 'lit'],
                                          [6, 11, 4, 4, 'chrome']], 'plate labels: anthropocentrism'


def plate(name, C=15, gut=150, tb=34):
    """The mark at C px per cell on its grid, leaders under the parts, labels in the gutters. Returns SVG."""
    N = 16 * C
    W, H = N + 2 * gut, N + 2 * tb
    ox, oy = gut, tb
    grid = ''.join('M%d.5 %dV%dM%d %d.5H%d' % (ox + k * C, oy, oy + N, ox, oy + k * C, ox + N) for k in range(1, 16))
    parts = ''.join('<rect class="%s" x="%d" y="%d" width="%d" height="%d"/>' % (
        'sg-lit' if r == 'lit' else 'sg-c', ox + x * C, oy + y * C, w * C, h * C) for x, y, w, h, r in lib(name))
    leads, labels = [], []
    for text, side, ax, ay in PLATES[name]:
        px, py = ox + ax * C, oy + ay * C
        if side == 'R':
            leads.append((px, round(py), ox + N + 8 - px, 1)); labels.append((ox + N + 12, round(py) + 4, 'start', text))
        elif side == 'L':
            leads.append((ox - 8, round(py), px - ox + 8, 1)); labels.append((ox - 12, round(py) + 4, 'end', text))
        elif side == 'T':
            leads.append((round(px), oy - 8, 1, py - oy + 8)); labels.append((round(px), oy - 13, 'middle', text))
        elif side == 'B':
            leads.append((round(px), py, 1, oy + N + 8 - py)); labels.append((round(px), oy + N + 22, 'middle', text))
        else:
            labels.append((round(px), round(py) + 4, 'middle', text))
    lead = ''.join('<rect class="pl-lead" x="%d" y="%d" width="%d" height="%d"/>' % r for r in leads)
    lab = ''.join('<text class="pl-lbl" x="%d" y="%d" text-anchor="%s">%s</text>' % (x, y, a, html.escape(t))
                  for x, y, a, t in labels)
    return ('<svg class="mk-plate-svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{a}">'
            '<rect class="pl-ground" x="{ox}" y="{oy}" width="{N}" height="{N}"/>'
            '<path class="pl-grid" d="{g}"/>{lead}{parts}{lab}</svg>').format(
        W=W, H=H, ox=ox, oy=oy, N=N, g=grid, lead=lead, parts=parts, lab=lab,
        a=html.escape('%s’s mark, enlarged: %s.' % (TITLE[name], says(name))))


# ------------------------------------------------------------------------------------------------------
# E. THE DISPOSITION GLYPHS, v0 (drawings only; nothing is built). The Adversarial Map sorts every
#    continuation four ways. One layout for all four: the continuation is the node at the top, the corpus is
#    the row of three below, and THE LIT ELEMENT IS WHERE THE CONTINUATION STOPS.
_C, _ROW = [6, 1, 4, 4], [[1, 9, 4, 4], [6, 9, 4, 4], [11, 9, 4, 4]]
DISP = {
    'a': ('the corpus already answers it',
          'routed: its edge reaches a node in the corpus, and that node is lit',
          [_C + ['chrome'], [7, 5, 2, 4, 'chrome'], _ROW[0] + ['chrome'], _ROW[1] + ['lit'], _ROW[2] + ['chrome']]),
    'b': ('the corpus needs a stronger text',
          'short: its edge stops before the corpus; the lit end is where our text runs out',
          [_C + ['chrome'], [7, 5, 2, 2, 'lit'], _ROW[0] + ['chrome'], _ROW[1] + ['chrome'], _ROW[2] + ['chrome']]),
    'c': ('it is really a new objection',
          'new: it has no edge into the corpus, so it stays lit where it stands',
          [_C + ['lit'], _ROW[0] + ['chrome'], _ROW[1] + ['chrome'], _ROW[2] + ['chrome']]),
    'd': ('it reaches bedrock and stops',
          'bedrock: its edge passes the corpus and stops on the lit ground',
          [_C + ['chrome'], [7, 5, 2, 9, 'chrome'], _ROW[0] + ['chrome'], _ROW[2] + ['chrome'], [1, 14, 14, 2, 'lit']]),
}


def silhouettes():
    """Every mark's cell set, both families plus the v0 dispositions; asserts the silhouette law."""
    s = {('library', n): cells(lib(n)) for n in ICONS}
    s.update({('tier', t): cells(v['rects']) for t, v in TIERS.items()})
    for k, (_, _, r) in DISP.items():
        assert [x[4] for x in r].count('lit') == 1, ('one lit element', k)
        s[('disposition', k)] = cells(r)
    assert len(set(s.values())) == len(s), 'two marks share a silhouette'
    return s


def closest_pairs(s, fam_a, fam_b, k=3):
    iou = lambda a, b: len(a & b) / len(a | b)
    pairs = [(iou(s[p], s[q]), p, q) for p, q in itertools.combinations(s, 2)
             if {p[0], q[0]} == {fam_a, fam_b} or (fam_a == fam_b == p[0] == q[0])]
    return sorted(pairs, reverse=True)[:k]


if __name__ == '__main__':
    s = silhouettes()
    print('silhouette law: %d marks, no two share a silhouette' % len(s))
    base = closest_pairs({k: v for k, v in s.items() if k[0] != 'disposition'}, 'library', 'tier', 1) + \
        closest_pairs(s, 'tier', 'tier', 1)
    print('closest existing pairs:', ', '.join('%s-%s %.2f' % (p[1], q[1], v) for v, p, q in base))
    for fam in ('library', 'tier'):
        v, p, q = closest_pairs(s, 'disposition', fam, 1)[0]
        print('closest disposition-%s pair: %s / %s  IoU %.2f' % (fam, p, q, v))
    for n in LIB_MOTION:
        print('%-17s %.2fs  %s' % (n, lib_span(n), LIB_MOTION[n][0]))
