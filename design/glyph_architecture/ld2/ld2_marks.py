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


# A and B were built (2026-09-26, on Josiah's word "Go with your recommendations on all of the above."): their
# data now lives in icons/gen_icons.py, the one source, and is read from there. Only E (drawings, not built)
# is defined here.
LIB_MOTION, DUR, PLATES = G['LIB_MOTION'], G['LIB_DUR'], G['PLATES']
_KF = G['LIB_KF']


def lib_span(name):
    return max(d + DUR[v] for _, v, d in LIB_MOTION[name][1])


def glyph(rects, px, cls='sg', motion=None, moves=(), lit_class='sg-lit'):
    """The generator's own drawing (cls and lit_class kept for the sheet's call sites; both are the defaults)."""
    assert cls == 'sg' and lit_class == 'sg-lit'
    return G['glyph'](rects, px, moves=moves, motion=motion)


def lib_glyph(name, px, moving=True):
    return glyph(lib(name), px, motion=G['moving'](name) if moving else None)


def tier_glyph(t, px, moving=True, lit_class='sg-lit'):
    return glyph(TIERS[t]['rects'], px, moves=TIERS[t]['moves'] if moving else (), lit_class=lit_class)


def motion_css(gate='html.wz-vfx:not(.wz-lightbg)', play='.play'):
    """The generator's library-mark motion with the sheet's own gate and trigger (the pages use the generator's)."""
    css = G['lm_css']
    body = css[css.index('@keyframes lm-fill'):css.index('@media')]
    rules = ','.join('%s %s .m-%s' % (gate, play, v) for v in DUR)
    per = ''.join('%s %s .m-%s{animation-name:%s;animation-duration:%gs}\n' % (gate, play, v, _KF[v], DUR[v]) for v in DUR)
    return (body + '@media (prefers-reduced-motion:no-preference){\n' + rules
            + '{animation-timing-function:ease-out;animation-fill-mode:both;animation-delay:var(--d,0s)}\n' + per + '}\n')


TIER_KF = G['wing_css'][G['wing_css'].index('@keyframes lib-sig-return'):G['wing_css'].index('@media')]
TIER_ANIM = G['TIER_ANIM']


def tier_arrival_css(gate='html.wz-vfx:not(.wz-lightbg)', play='.obj.flash'):
    return (TIER_KF + '@media (prefers-reduced-motion:no-preference){\n'
            + ''.join('%s %s .t%d .sg-m{animation:%s .2s both}\n' % (gate, play, t, a) for t, a in TIER_ANIM.items())
            + '}\n')


def plate(name, **_):
    """The wing's plate as the generator draws it (just the SVG, for the sheet)."""
    f = G['wing_plate'](name)
    return f[f.index('<svg'):f.index('</svg>') + 6]


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
