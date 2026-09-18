#!/usr/bin/env python3
"""
render_wing_v0_1.py -- K353. Render the Adversarial Map's OWN reader-facing surface.

WHAT THIS IS. An ordinary NO-PIN aux-wing fold, per canon
`adversarial_map.shipping_fork_disposition_verbatim`: an own-surface render is "runnable any
session"; only a /combined graft is a stance-layer change needing R4. Nothing here touches the
flagship, the corpus, the JSX or any map artifact. It READS four committed files and WRITES one.

WHAT IT SHIPS, AND THE LABEL THAT LICENSES IT. Exactly the pure-(d) nodes -- nodes every one of
whose entries in the terminal assembly is class (d). Per canon `class_asymmetry_ruling_K350`, the
open R1 question (strongest-vs-repairable) bites (a) and cannot touch (d), and the licence holds
ONLY under a label claiming TERMINUS rather than STRENGTH. Every heading, every link label and the
frame prose in this file are written to that constraint, and a control asserts no strength word
reaches the rendered page.

INSTRUMENTS ARE IMPORTED, NEVER REIMPLEMENTED (the K344 discipline): md5_bytes, objections_digest,
locus_text and variant_slot all come from the pinned validator module.

THE NORMALIZER, STATED BECAUSE A COUNT OVER FREE TEXT IS A COUNT OF A NORMALIZER (ccclxvi).
Bedrock identity is taken from honest_residuals_register_v0_4.json by (node, locus) lookup -- the
register's own HR-id namespace -- NOT from the entry's free-text routing.residue.bedrock_name.
The two disagree: 15 distinct name STRINGS over the ship set against 9 distinct registered
BEDROCKS. The register is the namespace; the strings are prose.

Run from the repo root or from this directory; paths resolve against the repo root either way.
Emits to <repo>/adversarial/index.html unless --out says otherwise.
"""
import io, os, sys, json, html, hashlib, importlib.util, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STG = os.path.join(ROOT, "adversarial_map_staging")

VALIDATOR = "adv_map_validator_v0_6.py"
ASSEMBLY = "adversarial_map_v1_3.json"
REGISTER = "honest_residuals_register_v0_4.json"
CORPUS = "efilist_argument_library_v4_0_0.json"

# base pins -- every input is gated before a byte is rendered
PINS = {
    ASSEMBLY:  ("681827419df72a16a7c6fe70df8fe77f", 269352),
    REGISTER:  ("d067729fafb51926bc9e845209417886", 44915),
    CORPUS:    ("04bf6482aa0374ee92a81c1d55ec41f8", 1334024),
    VALIDATOR: ("c002e93877b09d523daf786036af7a57", 59398),
}
OBJECTIONS_DIGEST = "2c5a083a31448dec0f1ce41e08ba5b04"

_spec = importlib.util.spec_from_file_location("advval", os.path.join(STG, VALIDATOR))
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

# ---------------------------------------------------------------- label constants
# THE TERMINUS LABEL. Register-sensitive and the author's; bound once here so a redline is one edit.
PAGE_TITLE = "Where the lines terminate"
SEC_LABEL = "WHERE THIS LINE TERMINATES"
MOVE_LABEL = "THE CONTINUATION"
TERMINUS_LABEL = "TERMINUS"
GROUNDS_LABEL = "WHY NO REWRITE CLOSES IT"
ANCHOR_LABEL = "AGAINST"

# the flagship's own strings, so the wing names its target in the target's words
DEPTH_LABEL = {"long": "FULL DISMANTLEMENT", "medium": "DECONSTRUCTION", "short": "PUNCH"}
LOCUS_SITE = {
    "long": "the FULL DISMANTLEMENT response",
    "medium": "the DECONSTRUCTION response",
    "short": "the PUNCH response",
    "diagnosis": "the CLINICAL DIAGNOSIS",
    "note": "the confidence note",
}

# words a terminus label may not use about what it ships. Gated in controls_wing_v0_1.py.
STRENGTH_WORDS = ("strongest", "the strongest", "best objection", "unanswerable", "refutes",
                  "defeats the library", "strongest possible")


def esc(s):
    """Escape for HTML text content. Gated: html.unescape(esc(s)) == s, for every string shipped."""
    return html.escape(s, quote=True)


def gate_inputs(out=print):
    bad = []
    for name, (m5, nb) in sorted(PINS.items()):
        p = os.path.join(STG, name) if name != CORPUS else os.path.join(ROOT, name)
        raw = io.open(p, "rb").read()
        got = (V.md5_bytes(raw), len(raw))
        ok = got == (m5, nb)
        out("  %-42s %s %s" % (name, "ok  " if ok else "FAIL", "%s / %d" % got))
        if not ok:
            bad.append(name)
    return bad


def load():
    asm = json.load(io.open(os.path.join(STG, ASSEMBLY), encoding="utf-8"))
    reg = json.load(io.open(os.path.join(STG, REGISTER), encoding="utf-8"))
    cor = json.load(io.open(os.path.join(ROOT, CORPUS), encoding="utf-8"))
    return asm, reg, cor


def ship_set(asm):
    """Pure-(d) nodes: every entry the assembly holds for that node is class (d)."""
    by = collections.OrderedDict()
    for e in asm["entries"]:
        by.setdefault(e["target_id"], []).append(e)
    return collections.OrderedDict(
        (k, v) for k, v in by.items() if all(x["class"] == "d" for x in v))


def register_index(reg):
    """(node, locus) -> (bedrock_id, bedrock, facet_id). The namespace, not the prose."""
    idx = {}
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                idx[(t["node"], t["locus"])] = (b["bedrock_id"], b, f["facet_id"])
    return idx


def link_for(node_id, locus):
    """The K352 inbound grammar, and only what it claims.

    #obj-<id>@<short|medium|long> forces the depth. There is NO @diagnosis and there should not
    be: the CLINICAL DIAGNOSIS section carries no responseLevel condition (combined.html L10554),
    so a bare anchor is already correct there and forcing a depth would be a claim about a gate
    that does not exist. #rwe- is not claimed by the suffix form at all.

    THE `note` LOCUS TAKES @long, AND THE FIRST CUT OF THIS FUNCTION GOT IT WRONG. `note` is not
    in the grammar, so the obvious fallthrough hands it the bare form -- and the bare form is
    exactly what fails there. The note DIV is emitted on `obj.note && responseLevel === 'long'`
    (combined.html L10584), so a bare link leaving a reader at the boot default renders no note
    element at all and no [NOTE] control beside it: the card would open with nothing of what the
    entry attacks anywhere on it. @long is the deepest form the grammar offers and the one the
    note depends on, so the note locus takes it and the surface states the remaining click.
    Caught by controls_wing_v0_1.py, not by reading.
    """
    if locus in ("short", "medium", "long"):
        return "/combined#obj-%s@%s" % (node_id, locus), True
    if locus == V.NOTE_LOCUS:
        return "/combined#obj-%s@long" % node_id, True
    return "/combined#obj-%s" % node_id, False


def build(asm, reg, cor):
    objs = {o["id"]: o for o in cor["objections"]}
    corpus_order = {o["id"]: i for i, o in enumerate(cor["objections"])}
    pure = ship_set(asm)
    idx = register_index(reg)

    rows = []
    for nid in sorted(pure, key=lambda k: corpus_order[k]):
        for e in sorted(pure[nid], key=lambda x: x["target_locus"]):
            key = (nid, e["target_locus"])
            if key not in idx:
                raise SystemExit("ABORT: %r has no register tributary -- the join is not total" % (key,))
            hid, bed, facet = idx[key]
            rows.append({
                "node": nid, "locus": e["target_locus"], "entry": e,
                "hid": hid, "bedrock": bed, "facet": facet,
                "obj": objs[nid], "ord": corpus_order[nid],
            })

    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault(r["hid"], []).append(r)
    # bedrocks by weight desc, then id asc -- the concentration IS the argument
    order = sorted(groups, key=lambda h: (-len(groups[h]), h))
    return rows, collections.OrderedDict((h, groups[h]) for h in order)


def render(rows, groups, asm, reg, cor):
    objs = {o["id"]: o for o in cor["objections"]}
    n_entries = len(rows)
    n_nodes = len({r["node"] for r in rows})
    n_floors = len(groups)
    n_mapped = asm["meta"]["nodes_total"]
    n_registered = len(reg["bedrocks"])

    P = []
    w = P.append
    w('<!doctype html>')
    w('<html lang="en">')
    w('<head>')
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w('<title>%s &middot; The Adversarial Map</title>' % esc(PAGE_TITLE))
    w('<meta name="description" content="The %d continuations of the argument library\'s own '
      'objections that no rewrite of its text closes, and the %d commitments they close against.">'
      % (n_entries, n_floors))
    w('<link rel="icon" href="/icon-libraries.svg">')
    w(STYLE)
    w(MODE_BOOT)
    w('<link rel="stylesheet" href="/wuld-layer.css">')
    w('<script src="/wuld-layer.js" defer></script>')
    w('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" '
      'href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?'
      'family=IBM+Plex+Mono:wght@300;400;500;700&display=swap" rel="stylesheet"></head>')
    w('<body>')
    w('<div class="wz-stage">')
    w('  <div class="wrap">')
    w('    <header class="site">')
    w('    <nav class="eyebrow wing-switcher" aria-label="Refusal Libraries">'
      '<a href="/libraries/">Refusal Libraries</a> <span aria-hidden="true">&middot;</span> '
      '<a href="/combined">Procreation &amp; Existence</a> <span aria-hidden="true">/</span> '
      '<a href="/right-to-die/combined">Right to Die</a> <span aria-hidden="true">/</span> '
      '<a href="/abortion/combined">Abortion</a> <span aria-hidden="true">/</span> '
      '<a href="/transgenderism/combined">Transgenderism</a> <span aria-hidden="true">/</span> '
      '<a href="/anthropocentrism/combined">Anthropocentrism</a> <span aria-hidden="true">/</span> '
      '<a href="/veganism/combined">Veganism</a> <span aria-hidden="true">&middot;</span> '
      '<span aria-current="page">Adversarial Map</span></nav>')
    w('    <h1>%s</h1>' % esc(PAGE_TITLE))
    w('    <div class="sub">%d continuations of this library\'s own objections that no rewrite of '
      'its text closes &mdash; and the %d commitments they close against instead.</div>'
      % (n_entries, n_floors))
    w('<div class="mode-toggle" role="group" aria-label="reading mode">')
    w('      <button id="mode-legible" type="button" aria-pressed="false" '
      'onclick="toggleModeAxis(\'legible\')">legible</button>')
    w('      <button id="mode-hc" type="button" aria-pressed="false" '
      'onclick="toggleModeAxis(\'high-contrast\')">high-contrast</button>')
    w('    </div>')
    w('    </header>')
    w('    <main>')
    w('      <div class="suite-rail"><div><b>%d</b><span>objections mapped</span></div>'
      '<div><b>%d</b><span>terminate here</span></div>'
      '<div><b>%d</b><span>continuations</span></div>'
      '<div><b>%d</b><span>floors named</span></div>'
      '<div><b>%d</b><span>floors in the register</span></div></div>'
      % (n_mapped, n_nodes, n_entries, n_floors, n_registered))

    # ---- the frame. This is the terminus label in prose and it is the only new reader-facing
    # text on the page; everything else is verbatim from the corpus, the assembly or the register.
    w('      <section class="frame">')
    w('        <p>The Adversarial Map is a hostile pass over this library&rsquo;s own text. For each '
      'of the flagship&rsquo;s %d objections it authors a <em>continuation</em> &mdash; the next move '
      'an opponent makes <em>after</em> reading our rebuttal &mdash; and sorts it into one of four '
      'dispositions: the corpus already answers it, the corpus needs a stronger text, it is really a '
      'new objection, or it reaches bedrock and stops.</p>' % n_mapped)
    w('        <p>Only the last disposition is on this page, and the reason is a question the map '
      'has not settled: whether a continuation was authored at full force or merely at the most '
      '<em>repairable</em> reading of our text. Until that is ruled, a card saying <em>we answer '
      'this</em> would claim more than the map has established. A card saying <em>this line '
      'terminates here</em> would not &mdash; a harder continuation reaches the same floor or a '
      'deeper one, and neither falsifies the claim. That asymmetry is the whole licence for this '
      'page, and it is why nothing else from the map is on it.</p>')
    w('        <p><strong>This is not a concession list.</strong> A disagreement that descends to a '
      'first commitment has not been won by whoever descended last; it has been <em>located</em>. '
      'What each card names is the floor both sides are standing on at the point the argument stops '
      'moving &mdash; and %d of these %d continuations come to rest on just two of them.</p>'
      % (len(list(groups.values())[0]) + len(list(groups.values())[1]), n_entries))
    w('        <p class="frame-not">Not here: the continuations the corpus answers, and the ones '
      'that show our text needs repair. Both wait on rulings of their own. Every quotation below is '
      'verbatim &mdash; from the objection card it attacks, or from the map entry that adjudicated '
      'it.</p>')
    w('      </section>')

    w('      <nav class="floorjump" aria-label="floors">')
    for hid, rs in groups.items():
        b = rs[0]["bedrock"]
        w('        <a href="#%s">%s <span>&times;%d</span></a>' % (esc(hid), esc(hid), len(rs)))
    w('      </nav>')

    for hid, rs in groups.items():
        b = rs[0]["bedrock"]
        w('      <section class="floor" id="%s">' % esc(hid))
        w('        <div class="floor-head">')
        w('          <div class="floor-id">%s <span class="floor-n">&times;%d</span></div>'
          % (esc(hid), len(rs)))
        w('          <h2>%s</h2>' % esc(b["name"]))
        if b.get("alias"):
            w('          <div class="floor-alias">also: %s</div>' % esc(b["alias"]))
        w('          <p class="floor-gloss">%s</p>' % esc(b["gloss"]))
        w('        </div>')
        for r in rs:
            w(card(r))
        w('      </section>')

    w('      <section class="colophon">')
    w('        <h2>What this page is made of</h2>')
    w('        <p>Every card is generated from three committed artifacts and nothing else: the '
      'terminal assembly <code>%s</code>, the residue register <code>%s</code>, and the corpus '
      '<code>%s</code>. The objection wording, the sentence each continuation attacks, the '
      'continuation itself and the adjudication are all verbatim; the floor a card is filed under '
      'is the register&rsquo;s identifier for it, not the free text in the entry.</p>'
      % (esc(ASSEMBLY), esc(REGISTER), esc(CORPUS)))
    w('        <p>The map covers all %d flagship objections. %d of them terminate: every '
      'continuation the map authored against them reaches a floor rather than a repair. The other '
      '%d carry at least one continuation of another disposition and are not on this page.</p>'
      % (n_mapped, n_nodes, n_mapped - n_nodes))
    w('        <p class="colophon-note">One link on this page lands a reader one step short. '
      '<code>care-ethics</code>&rsquo;s confidence note is reachable only through the card&rsquo;s '
      'own <code>[NOTE]</code> control, which no link form reaches; the card opens at full '
      'dismantlement and the note is one further click. Said here rather than papered over.</p>')
    w('      </section>')
    w('    </main>')
    w('    <footer style="margin-top:2rem;border-top:1px solid var(--line);padding-top:1rem">'
      '<div class="eyebrow" style="color:var(--faint)">The Adversarial Map &middot; one disposition '
      'of four &middot; <a href="/libraries/">The Refusal Libraries</a></div></footer>')
    w('  </div>')
    w('</div>')
    w('</body>')
    w('</html>')
    return "\n".join(P) + "\n"


def card(r):
    e, o = r["entry"], r["obj"]
    href, forced = link_for(r["node"], r["locus"])
    site = LOCUS_SITE[r["locus"]]
    L = []
    w = L.append
    w('        <article class="term" id="t-%s-%s">' % (esc(r["node"]), esc(r["locus"].replace(".", "-"))))
    w('          <div class="term-meta"><span class="tier">TIER %s</span>'
      '<span class="node">%s</span><span class="site">%s</span></div>'
      % (esc(str(o.get("tier", "?"))), esc(r["node"]), esc(site)))
    w('          <h3>&ldquo;%s&rdquo;</h3>' % esc(o.get("trigger") or r["node"]))
    w('          <div class="blk anchor"><span class="lbl">%s</span><p>&hellip;%s&hellip;</p></div>'
      % (ANCHOR_LABEL, esc(e["target_anchor"])))
    w('          <div class="blk move"><span class="lbl">%s</span><p>%s</p></div>'
      % (MOVE_LABEL, esc(e["adversarial_move"])))
    # The FACET, not the bedrock name. The floor heading two lines up already carries the
    # bedrock's id, name and gloss, so repeating the name here would put the same sentence on
    # all eight cards under HR-03 and tell a reader nothing about which of them they are
    # reading. The facet is what distinguishes them, and it is the register's own word for it.
    w('          <div class="blk term-floor"><span class="lbl">%s</span>'
      '<p><span class="hr">%s</span> %s</p></div>'
      % (TERMINUS_LABEL, esc(r["hid"]), esc(r["facet"])))
    routing = (e.get("routing", {}).get("residue", {}) or {}).get("terminus_routing", "")
    w('          <details class="adj"><summary>%s</summary><p>%s</p>%s</details>'
      % (GROUNDS_LABEL, esc(e["grounds"]),
         ('<p class="routing"><span class="rlbl">first registered</span> %s</p>' % esc(routing))
         if routing else ""))
    w('          <a class="open" href="%s">Open this objection %s <span aria-hidden="true">&rarr;</span></a>'
      % (esc(href), "at full dismantlement" if forced else "on the flagship"))
    w('        </article>')
    return "\n".join(L)


STYLE = """<style>
:root{
  --bg:#0b0b0c; --panel:#101012; --fg:#d8d4cc; --dim:#7a766e; --faint:#4a4742;
  --accent:#c41e3a; --line:#23211f; --stub:#b8902a;
  --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{font-size:16px}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--mono);
  line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:60rem;margin:0 auto;padding:1.5rem 1.25rem 4rem}
header.site{border-bottom:1px solid var(--line);padding-bottom:1rem;margin-bottom:1rem}
.eyebrow{font-size:.7rem;letter-spacing:.18em;color:var(--dim);text-transform:uppercase}
h1{font-size:1.6rem;margin:.3rem 0 .15rem;letter-spacing:.02em}
.sub{color:var(--dim);font-size:.85rem;max-width:46rem}
.wing-switcher a{color:var(--dim);text-decoration:none;border-bottom:1px solid transparent}
.wing-switcher a:hover{color:var(--accent);border-bottom-color:var(--accent)}
.wing-switcher [aria-current="page"]{color:var(--fg)}
.mode-toggle{display:flex;gap:.25rem;margin:.6rem 0 0;flex-wrap:wrap}
.mode-toggle button{background:none;border:1px solid var(--line);color:var(--dim);font:inherit;
  font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;padding:.25rem .5rem;cursor:pointer;
  border-radius:2px}
.mode-toggle button.active{color:var(--fg);border-color:var(--accent)}
.mode-toggle button:focus-visible{outline:1px solid var(--accent);outline-offset:2px}
.suite-rail{display:flex;flex-wrap:wrap;gap:0;border:1px solid var(--line);margin:1rem 0 0}
.suite-rail div{flex:1 1 8rem;padding:.55rem .8rem;border-right:1px solid var(--line)}
.suite-rail div:last-child{border-right:none}
.suite-rail b{display:block;font-size:1.15rem;font-weight:500;color:var(--fg);
  font-variant-numeric:tabular-nums;line-height:1.2}
.suite-rail span{font-size:.55rem;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
@media (max-width:520px){ .suite-rail div{flex:1 1 45%;border-bottom:1px solid var(--line)} }
.frame{max-width:46rem;margin:1.3rem 0 1.6rem}
.frame p{font-size:.86rem;color:var(--dim);line-height:1.65;margin:.7rem 0}
.frame strong{color:var(--fg);font-weight:500}
.frame em{font-style:normal;color:var(--fg)}
.frame .frame-not{border-left:2px solid var(--line);padding-left:.8rem;color:var(--faint);
  font-size:.8rem}
.floorjump{display:flex;flex-wrap:wrap;gap:.3rem;margin:0 0 2rem;padding:.7rem;
  border:1px solid var(--line);background:var(--panel);border-radius:3px}
.floorjump a{font-size:.64rem;letter-spacing:.1em;color:var(--dim);border:1px solid var(--line);
  padding:.2rem .5rem;border-radius:2px}
.floorjump a:hover{color:var(--fg);border-color:var(--accent);text-decoration:none}
.floorjump a span{color:var(--faint)}
.floor{margin:0 0 2.6rem;scroll-margin-top:1rem}
.floor-head{border-top:1px solid var(--accent);padding-top:.7rem;margin-bottom:1rem}
.floor-id{font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
.floor-id .floor-n{color:var(--faint);margin-left:.4rem}
.floor-head h2{font-size:1.18rem;margin:.25rem 0 .3rem;font-weight:600;line-height:1.35}
.floor-alias{font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.floor-gloss{font-size:.82rem;color:var(--dim);line-height:1.6;margin:.45rem 0 0;max-width:46rem}
.term{border:1px solid var(--line);border-left:2px solid var(--faint);background:var(--panel);
  padding:1rem 1.1rem;margin:0 0 1rem;border-radius:3px;scroll-margin-top:1rem}
.term-meta{display:flex;gap:.45rem;flex-wrap:wrap;align-items:center;font-size:.58rem;
  letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.term-meta>span+span::before{content:"\\00b7";color:var(--faint);margin-right:.45rem}
.term-meta .tier{color:var(--dim)}
.term-meta .node{color:var(--dim)}
.term h3{font-size:1rem;margin:.35rem 0 .6rem;font-weight:600;line-height:1.4;color:var(--fg)}
.blk{margin:.55rem 0}
.blk .lbl{display:block;font-size:.58rem;letter-spacing:.15em;text-transform:uppercase;
  color:var(--faint);margin-bottom:.2rem}
.blk p{margin:0;font-size:.84rem;line-height:1.6}
.blk.anchor{padding-left:.7rem;border-left:1px solid var(--line)}
.blk.anchor p{color:var(--dim);font-style:italic}
.blk.move{background:#000;border:1px solid var(--line);border-radius:2px;padding:.6rem .75rem}
.blk.move .lbl{color:var(--accent)}
.blk.term-floor{padding-left:.7rem;border-left:2px solid var(--stub)}
.blk.term-floor .lbl{color:var(--stub)}
.blk.term-floor p{color:var(--fg);font-size:.8rem}
.blk.term-floor .hr{color:var(--stub);letter-spacing:.06em}
.adj .routing{color:var(--faint);font-size:.72rem;margin-top:.45rem}
.adj .routing .rlbl{color:var(--faint);letter-spacing:.14em;text-transform:uppercase;font-size:.58rem;display:block;margin-bottom:.15rem}
.adj{margin:.6rem 0 0}
.adj>summary{cursor:pointer;list-style:none;color:var(--dim);font-size:.58rem;letter-spacing:.15em;
  text-transform:uppercase;padding:.15rem 0;display:inline-block}
.adj>summary::-webkit-details-marker{display:none}
.adj>summary::after{content:" [+]";color:var(--faint)}
.adj[open]>summary::after{content:" [-]"}
.adj>summary:focus-visible{outline:1px solid var(--accent);outline-offset:2px}
.adj p{margin:.35rem 0 0;font-size:.78rem;color:var(--dim);line-height:1.6;padding-left:.7rem;
  border-left:1px solid var(--line)}
.open{display:inline-block;margin-top:.7rem;font-size:.66rem;letter-spacing:.1em;
  text-transform:uppercase;border:1px solid var(--line);padding:.3rem .6rem;border-radius:2px;
  color:var(--dim)}
.open:hover{color:var(--fg);border-color:var(--accent);text-decoration:none}
.colophon{border-top:1px solid var(--line);margin-top:2.4rem;padding-top:1.1rem;max-width:46rem}
.colophon h2{font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);
  margin:0 0 .5rem;font-weight:400}
.colophon p{font-size:.78rem;color:var(--faint);line-height:1.6;margin:.5rem 0}
.colophon code{color:var(--dim);font-size:.74rem}
.colophon .colophon-note{border-left:2px solid var(--stub);padding-left:.8rem}
[data-mode="legible"]{
  --bg:#f5efe6;--panel:#ebe3d4;--fg:#1a1816;--dim:#5f5a50;--faint:#8a8275;
  --accent:#a91930;--line:#d7ccb9;--stub:#876820;font-size:17px;
}
[data-mode="high-contrast"]{
  --bg:#000;--panel:#000;--fg:#fff;--dim:#d2d2d2;--faint:#a6a6a6;
  --accent:#ff4060;--line:#fff;--stub:#ffd400;
}
[data-mode="both"]{
  --bg:#fff;--panel:#fff;--fg:#000;--dim:#333;--faint:#555;
  --accent:#c00028;--line:#000;--stub:#7a5b00;font-size:17px;
}
[data-mode="high-contrast"] :focus-visible,[data-mode="both"] :focus-visible{
  outline:2px solid #ffeb3b;outline-offset:2px}
[data-mode="legible"] .blk.move{background:#fffdf9}
[data-mode="both"] .blk.move{background:#fff}
[data-mode="legible"] body,[data-mode="both"] body{font-family:'Georgia','Times New Roman',serif}
[data-mode="legible"] .eyebrow,[data-mode="both"] .eyebrow,
[data-mode="legible"] .mode-toggle button,[data-mode="both"] .mode-toggle button,
[data-mode="legible"] .lbl,[data-mode="both"] .lbl,
[data-mode="legible"] .term-meta,[data-mode="both"] .term-meta,
[data-mode="legible"] .floor-id,[data-mode="both"] .floor-id,
[data-mode="legible"] .open,[data-mode="both"] .open,
[data-mode="legible"] .floorjump a,[data-mode="both"] .floorjump a,
[data-mode="legible"] .adj>summary,[data-mode="both"] .adj>summary,
[data-mode="legible"] .suite-rail span,[data-mode="both"] .suite-rail span,
[data-mode="legible"] .colophon h2,[data-mode="both"] .colophon h2{font-family:var(--mono)}
</style>"""

MODE_BOOT = """<script>
/* Reading-mode bootstrap, pre-paint, no FOUC. Ported byte-for-byte in behaviour from
   libraries/index.html: same storage key, same four modes, same two independent axes, and
   deliberately NO prefers-color-scheme branch (WI-K321b: it opened a wing in serif-on-cream
   for any reader whose OS is light while the flagship opened in mono-on-black beside it). */
(function(){
  var KEY="wuld:libmode",ALLOWED=["standard","legible","high-contrast","both"];
  function resolve(){
    var s=null; try{s=localStorage.getItem(KEY);}catch(e){}
    if(s&&ALLOWED.indexOf(s)!==-1) return s;
    return "standard";
  }
  function sync(mode){
    var l=(mode==="legible"||mode==="both"), h=(mode==="high-contrast"||mode==="both");
    var bl=document.getElementById("mode-legible"), bh=document.getElementById("mode-hc");
    if(bl){ bl.classList.toggle("active",l); bl.setAttribute("aria-pressed",String(l)); }
    if(bh){ bh.classList.toggle("active",h); bh.setAttribute("aria-pressed",String(h)); }
  }
  document.documentElement.setAttribute("data-mode", resolve());
  window.setMode=function(mode){
    if(ALLOWED.indexOf(mode)===-1) mode="standard";
    document.documentElement.setAttribute("data-mode", mode);
    try{ localStorage.setItem(KEY,mode); }catch(e){}
    sync(mode);
  };
  window.toggleModeAxis=function(axis){
    var m=document.documentElement.getAttribute("data-mode")||"standard";
    var l=(m==="legible"||m==="both"), h=(m==="high-contrast"||m==="both");
    if(axis==="legible") l=!l; else if(axis==="high-contrast") h=!h;
    window.setMode(l&&h ? "both" : l ? "legible" : h ? "high-contrast" : "standard");
  };
  document.addEventListener("DOMContentLoaded", function(){
    sync(document.documentElement.getAttribute("data-mode")||"standard");
  });
})();
</script>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "adversarial", "index.html"))
    ap.add_argument("--no-gate", action="store_true",
                    help="skip the input pin gate (controls only; never for a ship build)")
    a = ap.parse_args()

    print("render_wing_v0_1 -- repo root %s" % ROOT)
    print("INPUT GATE")
    bad = gate_inputs()
    if bad and not a.no_gate:
        sys.exit("ABORT: %d input(s) off their pin -- nothing rendered" % len(bad))

    asm, reg, cor = load()
    dg = V.objections_digest(cor)
    print("  objections digest                          %s %s" % ("ok  " if dg == OBJECTIONS_DIGEST else "FAIL", dg))
    if dg != OBJECTIONS_DIGEST and not a.no_gate:
        sys.exit("ABORT: objections digest off its pin")

    rows, groups = build(asm, reg, cor)
    print("SHIP SET  %d entries / %d nodes / %d floors"
          % (len(rows), len({r['node'] for r in rows}), len(groups)))
    for hid, rs in groups.items():
        print("    %-6s x%-3d %s" % (hid, len(rs), rs[0]["bedrock"]["name"][:64]))

    # --- anchor rule, re-run at SHIP time against the live corpus ------------------------
    objs = {o["id"]: o for o in cor["objections"]}
    bad_anchor = [(r["node"], r["locus"]) for r in rows
                  if r["entry"]["target_anchor"] not in V.locus_text(objs[r["node"]], r["locus"])]
    print("  anchor rule at ship time                   %s %d/%d verbatim"
          % ("ok  " if not bad_anchor else "FAIL", len(rows) - len(bad_anchor), len(rows)))
    if bad_anchor:
        sys.exit("ABORT: anchors not verbatim: %r" % bad_anchor)

    out = render(rows, groups, asm, reg, cor)
    rb = out.encode("utf-8")
    d = os.path.dirname(os.path.abspath(a.out))
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(a.out, "wb").write(rb)
    print("\n  WROTE %s" % a.out)
    print("  %s / %d bytes / %d lines" % (V.md5_bytes(rb), len(rb), out.count("\n")))


if __name__ == "__main__":
    main()
