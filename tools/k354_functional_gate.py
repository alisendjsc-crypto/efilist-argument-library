#!/usr/bin/env python3
"""k354_functional_gate.py -- the FUNCTIONAL gate on the note-and-confidence repair.

verify_K354.py proves the BYTES: that the changed set is exactly the declared loci and that no
corpus byte moved. It cannot prove that a reader can now open solipsism's note, and it cannot
prove that a repaired hex literal actually produces a border, because the thing that decides
that is the CSS parser rather than the file.

SO EVERY CLAIM HERE IS READ OFF A BINDING THE BROWSER DECLARES (ccclxxix):

  the [NOTE] control is found by its own onclick naming its node, never by DOM containment --
  the expanded body lives in a separate subtree (#results > .detail-panel), so a containment
  query is empty for every node, and an unscoped one answers a different question. K353 got
  this wrong in both directions before getting it right; the working form is inherited verbatim.

  the hex repair is read as getComputedStyle().borderTopWidth and .backgroundColor, NEVER as a
  string in the stylesheet. A 5-digit literal makes the whole declaration invalid, so the defect
  is the ABSENCE of a computed border -- exactly the thing a text scan cannot see and a text
  scan of the COMMENT documenting it reports backwards. Two sessions' scans matched that comment
  instead of the code.

  the note is proved reachable by CLICKING the control and requiring the note to become visible,
  not by the control's existence. An affordance that exists and does nothing is the defect one
  level up.

AND THE WHOLE BATTERY RUNS TWICE, against the BASE and against the CANDIDATE, with BOTH expected
values declared per check. A check whose base and candidate expectations are equal is an
invariant; a check where they differ is a repair, and its base run is its own failing control.
There is no check here that has not been shown to be capable of the other answer.

Every probe carries a boot witness (ccclxxvii): a fragment-only navigation is same-document, so
a hash-varying test reads the previous case's state as this case's verdict.

WHERE IT RUNS. The Cowork container, which carries Chromium and Playwright; the operator's VM
does not. Like k352_functional_gate.py and k353_wing_functional_gate.py it does not reproduce
from its committed location, and says so rather than leaving it to be discovered.
"""
import argparse, json, os, re, sys, threading, http.server, socketserver
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--cand", required=True)
ap.add_argument("--corpus", required=True)
ap.add_argument("--out", default="k354_functional_control_v0_1.json")
ap.add_argument("--shots", default="/home/claude/k354/shots")
A = ap.parse_args()
os.makedirs(A.shots, exist_ok=True)

CORPUS = json.load(open(A.corpus))["objections"]
GRADED = {o["id"]: o.get("confidence") for o in CORPUS if o.get("confidence")}
NOTED = sorted(o["id"] for o in CORPUS if o.get("note"))
LABEL = {"full": "FULL", "strong": "STRONG", "provisional": "PROVISIONAL"}

results, fails = [], []
def chk(name, base_want, cand_want, base_got, cand_got):
    ok = (base_got == base_want) and (cand_got == cand_want)
    kind = "INVARIANT" if base_want == cand_want else "REPAIR   "
    results.append({"check": name, "kind": kind.strip(), "ok": bool(ok),
                    "base_want": base_want, "base_got": base_got,
                    "cand_want": cand_want, "cand_got": cand_got})
    print(("  ok    " if ok else "  FAIL  ") + kind + "  " + name)
    if not ok:
        print("          base want %r got %r" % (base_want, base_got))
        print("          cand want %r got %r" % (cand_want, cand_got))
        fails.append(name)

class H(http.server.SimpleHTTPRequestHandler):
    """Mirrors the Pages routing: extensionless /combined."""
    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p == "/combined": p = "/combined.html"
        return os.path.join(self.server.root, p.lstrip("/"))
    def log_message(self, *a): pass

def serve(root):
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", 0), H)
    srv.root = root
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d" % srv.server_address[1]


def shoot(pg, anchor_id, name):
    """Clip to the RESPONSE SECTION the anchor lives in, so the image is OF the subject.

    Two cuts of this were wrong and the control caught both. The first screenshotted the
    viewport at whatever scroll the probe left -- the page header, identical on both roots. The
    second scrolled and read getBoundingClientRect in the SAME evaluate, so the rect was read
    before the scroll had applied, and clipped a stale box; it also walked six parentElement
    hops to a container whose visible region is identical everywhere. The fix is to locate by a
    binding the artifact declares -- closest('.section'), the class the card's own markup uses --
    and to scroll and measure in separate round trips.
    """
    pg.evaluate("id => { const n = document.getElementById(id);"
                " if (n) (n.closest('.section') || n).scrollIntoView({block: 'center'}); }", anchor_id)
    pg.wait_for_timeout(350)
    box = pg.evaluate(
        """id => { const n = document.getElementById(id); if (!n) return null;
             const c = n.closest('.section') || n; const r = c.getBoundingClientRect();
             if (r.width < 40 || r.height < 40) return null;
             return {x: Math.max(0, r.x), y: Math.max(0, r.y),
                     width: Math.min(1380 - Math.max(0, r.x), r.width),
                     height: Math.min(2100 - Math.max(0, r.y), r.height)}; }""", anchor_id)
    path = os.path.join(A.shots, name)
    if box: pg.screenshot(path=path, clip=box)
    else:   pg.screenshot(path=path)
    import hashlib as _h
    return _h.md5(open(path, "rb").read()).hexdigest()

NOTE_BTN = ("id => [...document.querySelectorAll('.note-toggle')]"
            ".some(e => (e.getAttribute('onclick')||'').includes(\"toggleNote('\"+id+\"')\"))")

def measure(root, tag):
    """Every number this gate reports, read once per root."""
    srv, BASE = serve(root)
    m = {"pageerrors": []}
    try:
        with sync_playwright() as p:
            br = p.chromium.launch()
            ctx = br.new_context(viewport={"width": 1400, "height": 2200})
            pg = ctx.new_page()
            pg.on("pageerror", lambda e: m["pageerrors"].append(str(e)[:200]))
            pg.route(re.compile(r"^https?://(?!127\.0\.0\.1)"), lambda r: r.abort())

            def probe(url):
                try: pg.evaluate("() => { window.__preNav = 1; }")
                except Exception: pass
                pg.goto("about:blank")
                pg.goto(url, wait_until="load")
                pg.wait_for_timeout(900)
                if pg.evaluate("() => typeof window.__preNav !== 'undefined'"):
                    raise AssertionError("ccclxxvii: same-document nav -- the initialiser did NOT re-run")

            # ---- boot default and the K352 affordance, at the boot level
            probe(BASE + "/combined")
            m["boot_level"] = pg.evaluate("() => responseLevel")
            m["dismantle_at_boot"] = pg.evaluate("() => document.querySelectorAll('.depth-jump').length")

            # ---- everything else at full dismantlement, via the module's own accessor
            pg.evaluate("() => setDepth('long')"); pg.wait_for_timeout(600)
            m["level"] = pg.evaluate("() => responseLevel")
            m["notes"] = pg.evaluate("() => document.querySelectorAll('.confidence-note').length")
            m["controls"] = pg.evaluate("() => document.querySelectorAll('.note-toggle').length")
            m["badges"] = pg.evaluate("() => document.querySelectorAll('.confidence-badge').length")
            m["badge_labels"] = pg.evaluate(
                "() => { const c = {}; document.querySelectorAll('.confidence-badge')"
                ".forEach(e => c[e.textContent.trim()] = (c[e.textContent.trim()]||0)+1); return c; }")
            m["cards"] = pg.evaluate("() => document.querySelectorAll('.objection-card, .result-card, .card').length")
            m["prov_band"] = pg.evaluate("() => document.querySelectorAll('.provisional-response').length")
            # the control exists, per node, located by its own onclick
            for nid in NOTED:
                m["btn:" + nid] = pg.evaluate(NOTE_BTN, nid)
            # the badge each graded node actually shows, located by the note/badge's own card
            m["badge_by_node"] = pg.evaluate(
                """() => { const out = {};
                     document.querySelectorAll('.confidence-badge').forEach(b => {
                       let n = b.parentElement, id = null;
                       while (n && !id) {
                         const t = n.querySelector && n.querySelector('.note-toggle');
                         if (t) { const mm = (t.getAttribute('onclick')||'').match(/toggleNote\\('([^']+)'\\)/); if (mm) id = mm[1]; }
                         if (!id && n.id && n.id.indexOf('note-') === 0) id = n.id.slice(5);
                         n = n.parentElement;
                       }
                       if (id) out[id] = b.textContent.trim();
                     }); return out; }""")

            # ---- computed style: the hex repair, read from the browser not the stylesheet
            def cs(sel, props):
                return pg.evaluate(
                    "a => { const e = document.querySelector(a[0]); if (!e) return null;"
                    " const s = getComputedStyle(e); const o = {}; a[1].forEach(p => o[p] = s[p]); return o; }",
                    [sel, props])
            m["css_strong"] = cs(".confidence-badge.confidence-strong", ["borderTopWidth", "borderTopStyle", "backgroundColor"])
            m["css_prov"]   = cs(".confidence-badge.confidence-provisional", ["borderTopWidth", "backgroundColor"])
            m["css_full"]   = cs(".confidence-badge.confidence-full", ["borderTopWidth", "backgroundColor"])
            m["css_toggle"] = cs(".note-toggle", ["borderTopWidth", "borderTopStyle", "borderTopColor"])
            m["prov_opacity"] = pg.evaluate(
                "() => { const n = document.getElementById('note-indigenous-philosophy');"
                " if (!n) return null; const b = n.parentElement.querySelector('.response-box');"
                " return b ? getComputedStyle(b).opacity : null; }")

            # ---- the K352 grammar still routes -- AND it is what opens the card. Every
            # measurement below needs an EXPANDED panel: the detail panel is collapsed until a
            # card is opened, so a clip box read off a collapsed section is empty and a
            # screenshot silently falls back to the viewport. That is how two cuts of the shot
            # came out byte-identical between the roots.
            probe(BASE + "/combined#obj-solipsism@long")
            m["deeplink_level"] = pg.evaluate("() => responseLevel")

            # ---- the note is REACHABLE, not merely controlled: click it
            m["solipsism_visible_before"] = pg.evaluate(
                "() => { const n = document.getElementById('note-solipsism');"
                " return n ? (getComputedStyle(n).display !== 'none') : null; }")
            m["shot_before"] = shoot(pg, "note-solipsism", "%s_solipsism_before.png" % tag)
            clicked = pg.evaluate(
                """() => { const t = [...document.querySelectorAll('.note-toggle')]
                      .find(e => (e.getAttribute('onclick')||'').includes("toggleNote('solipsism')"));
                     if (!t) return 'no-control'; t.click(); return 'clicked'; }""")
            pg.wait_for_timeout(250)
            m["solipsism_click"] = clicked
            m["solipsism_visible_after"] = pg.evaluate(
                "() => { const n = document.getElementById('note-solipsism');"
                " return n ? (getComputedStyle(n).display !== 'none') : null; }")
            m["shot_solipsism"] = shoot(pg, "note-solipsism", "%s_solipsism_long.png" % tag)

            # ---- high contrast: the mode the FULL badge never needed until this cut
            pg.evaluate("() => document.body.classList.add('high-contrast')")
            pg.wait_for_timeout(300)
            m["hc_full"] = cs(".confidence-badge.confidence-full", ["color", "borderTopWidth"])
            m["hc_strong"] = cs(".confidence-badge.confidence-strong", ["color", "borderTopWidth"])
            m["shot_hc"] = shoot(pg, "note-solipsism", "%s_hc_badges.png" % tag)
            def swatch(sel):
                return pg.evaluate(
                    "a => { const e = document.querySelector(a); if (!e) return null;"
                    " const s = getComputedStyle(e);"
                    " return {color: s.color, bg: s.backgroundColor, ground: (" + EFF_BG + ")(e.parentElement)}; }",
                    sel)
            m["hc_sw_note"]   = swatch(".note-toggle")
            m["hc_sw_full"]   = swatch(".confidence-badge.confidence-full")
            m["hc_sw_strong"] = swatch(".confidence-badge.confidence-strong")
            m["hc_sw_prov"]   = swatch(".confidence-badge.confidence-provisional")
            pg.evaluate("() => document.body.classList.remove('high-contrast')")

            # ---- the boot witness's own failing control
            pg.goto(BASE + "/combined", wait_until="load"); pg.wait_for_timeout(600)
            pg.evaluate("() => { window.__preNav = 1; }")
            pg.goto(BASE + "/combined#obj-life-gift@long", wait_until="load"); pg.wait_for_timeout(400)
            m["witness_survives_hash_only"] = pg.evaluate("() => typeof window.__preNav !== 'undefined'")
            br.close()
    finally:
        srv.shutdown()
    return m


# --------------------------------------------------------------------------------------------
# Colour expectations are DERIVED FROM THE DECLARED HEX, never typed. The first cut of this gate
# hand-wrote "rgba(204, 153, 0, 0.2)" for a background whose literal ends 11, not 33 -- the
# border alpha, transposed onto the fill -- and hand-wrote a UA default border colour it had
# guessed. Four of its six failures were that, and the artifact was right every time. ccclxii
# is usually read as "bind the constant"; its sharper form is "never hand-type a value the
# machine also computes", and a browser computes all of these.
def rgba(s):
    v = [float(x) for x in re.findall(r"[\d.]+", s or "")]
    if len(v) < 3: return None
    if len(v) == 3: v.append(1.0)
    return (int(v[0]), int(v[1]), int(v[2]), round(v[3], 3))

def from_hex(h):
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h) + "ff"
    if len(h) == 6: h += "ff"
    r, g, b, a = (int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
    return (r, g, b, round(a / 255.0, 3))

TRANSPARENT = (0, 0, 0, 0.0)

# --------------------------------------------------------------------------------------------
# WCAG contrast, computed from what the BROWSER reports rather than from the stylesheet. The
# effective background is found by walking ancestors until one is not transparent, and a badge's
# own translucent fill is composited over it -- a ratio taken against a guessed ground is a
# claim about the guess.
EFF_BG = """el => { let n = el, out = 'rgb(255,255,255)';
    while (n) { const b = getComputedStyle(n).backgroundColor;
      const m = b.match(/[\\d.]+/g);
      if (m && (m.length < 4 || parseFloat(m[3]) > 0.9)) { out = b; break; }
      n = n.parentElement; }
    return out; }"""

def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def lum(rgb):
    return 0.2126 * _lin(rgb[0]) + 0.7152 * _lin(rgb[1]) + 0.0722 * _lin(rgb[2])

def over(fg, bg):
    """composite fg (with alpha) over bg"""
    a = fg[3]
    return tuple(int(round(fg[i] * a + bg[i] * (1 - a))) for i in range(3))

def contrast(text_rgba, own_bg_rgba, ground_rgba):
    ground = ground_rgba[:3]
    bg = over(own_bg_rgba, ground) if own_bg_rgba and own_bg_rgba[3] > 0 else ground
    txt = over(text_rgba, bg) if text_rgba[3] < 1 else text_rgba[:3]
    hi, lo = max(lum(txt), lum(bg)), min(lum(txt), lum(bg))
    return round((hi + 0.05) / (lo + 0.05), 2)



def fill(mm, key):   return rgba((mm.get(key) or {}).get("backgroundColor")) if mm.get(key) else None
def bwidth(mm, key): return (mm.get(key) or {}).get("borderTopWidth") if mm.get(key) else None
def bstyle(mm, key): return (mm.get(key) or {}).get("borderTopStyle") if mm.get(key) else None

print("K354 FUNCTIONAL GATE -- every check run against BOTH roots\n")
B = measure(A.base, "base")
C = measure(A.cand, "cand")

# ---------------------------------------------------------------- THE REPAIR
chk("9 notes render at full dismantlement", 9, 9, B["notes"], C["notes"])
chk("the [NOTE] control's count EQUALS the container's -- the whole ruling", 7, 9, B["controls"], C["controls"])
for nid in NOTED:
    want_base = GRADED.get(nid) not in (None, "full")
    chk("[NOTE] control present: %s" % nid, want_base, True, B["btn:" + nid], C["btn:" + nid])
chk("solipsism's note starts CLOSED on both -- the repair opens nothing by itself",
    False, False, B["solipsism_visible_before"], C["solipsism_visible_before"])
chk("solipsism: the control can be clicked at all", "no-control", "clicked",
    B["solipsism_click"], C["solipsism_click"])
chk("solipsism's note becomes VISIBLE -- reachable, not merely controlled", False, True,
    B["solipsism_visible_after"], C["solipsism_visible_after"])

# ---------------------------------------------------------------- THE CONFIDENCE RENDER
chk("badge count: 7 graded-and-shown -> all 18 affirmative grades", 7, 18, B["badges"], C["badges"])
chk("badge labels by grade", {"STRONG": 6, "PROVISIONAL": 1},
    {"FULL": 11, "STRONG": 6, "PROVISIONAL": 1}, B["badge_labels"], C["badge_labels"])
joined = {k: v for k, v in C["badge_by_node"].items() if k in GRADED}
chk("every badge found on a note-bearing card names that node's own corpus grade",
    {k: LABEL[GRADED[k]] for k in B["badge_by_node"] if k in GRADED},
    {k: LABEL[GRADED[k]] for k in NOTED if k in GRADED},
    {k: v for k, v in B["badge_by_node"].items() if k in GRADED}, joined)

# ---------------------------------------------------------------- THE HEX REPAIR, COMPUTED
chk("STRONG badge: invalid CSS dropped the border -> repaired to 1px solid",
    ("0px", "none"), ("1px", "solid"),
    (bwidth(B, "css_strong"), bstyle(B, "css_strong")), (bwidth(C, "css_strong"), bstyle(C, "css_strong")))
chk("STRONG badge fill: transparent -> the declared #cc990011",
    TRANSPARENT, from_hex("#cc990011"), fill(B, "css_strong"), fill(C, "css_strong"))
chk("PROVISIONAL badge: 0px -> 1px, and transparent -> the declared #cc555511",
    ("0px", TRANSPARENT), ("1px", from_hex("#cc555511")),
    (bwidth(B, "css_prov"), fill(B, "css_prov")), (bwidth(C, "css_prov"), fill(C, "css_prov")))
chk("FULL badge: it does not exist on the base at all, and is styled on the candidate",
    None, ("1px", from_hex("#44aa7711")),
    B["css_full"], (bwidth(C, "css_full"), fill(C, "css_full")))
chk("[NOTE] button: browser-default 2px outset chrome -> the 1px dim border [DISMANTLE] is styled off",
    ("2px", "outset"), ("1px", "solid"),
    (bwidth(B, "css_toggle"), bstyle(B, "css_toggle")), (bwidth(C, "css_toggle"), bstyle(C, "css_toggle")))
chk("[NOTE] button border colour is the declared #332",
    None, from_hex("#332"), None, rgba(C["css_toggle"]["borderTopColor"]))
chk("high-contrast FULL badge is dark on the light ground (the rule this ruling required)",
    None, (from_hex("#174")[:3], "1px"),
    B["hc_full"], (rgba(C["hc_full"]["color"])[:3], C["hc_full"]["borderTopWidth"]))
chk("high-contrast STRONG badge gains its border too",
    (from_hex("#960")[:3], "0px"), (from_hex("#960")[:3], "1px"),
    (rgba(B["hc_strong"]["color"])[:3], B["hc_strong"]["borderTopWidth"]),
    (rgba(C["hc_strong"]["color"])[:3], C["hc_strong"]["borderTopWidth"]))

# ---------------------------------------------------------------- THE PROVISIONAL BAND
chk("the unlabelled opacity band is gone from the DOM", 1, 0, B["prov_band"], C["prov_band"])
chk("and the provisional node's response body is at full opacity", "0.7", "1",
    B["prov_opacity"], C["prov_opacity"])

# ---------------------------------------------------------------- NOTHING ELSE MOVED
chk("the boot default is still medium -- NOT flipped", "medium", "medium", B["boot_level"], C["boot_level"])
chk("K352's [DISMANTLE] still renders on every card at the boot level", 82, 82,
    B["dismantle_at_boot"], C["dismantle_at_boot"])
chk("K352's anchor grammar still forces long", "long", "long", B["deeplink_level"], C["deeplink_level"])
chk("setDepth('long') reached long", "long", "long", B["level"], C["level"])
chk("no page error on either surface", [], [], B["pageerrors"], C["pageerrors"])
chk("CONTROL the boot witness CAN fire: without the reset it survives a hash-only nav",
    True, True, B["witness_survives_hash_only"], C["witness_survives_hash_only"])
chk("CONTROL the screenshots are OF the subject: the two roots' images must DIFFER",
    True, True, B["shot_solipsism"] != C["shot_solipsism"], B["shot_hc"] != C["shot_hc"])

# ---------------------------------------------------------------- HIGH-CONTRAST LEGIBILITY
def ratio_of(mm, key):
    sw = mm.get(key)
    if not sw: return None
    return contrast(rgba(sw["color"]), rgba(sw["bg"]), rgba(sw["ground"]))

r_note_b, r_note_c = ratio_of(B, "hc_sw_note"), ratio_of(C, "hc_sw_note")
r_full_c = ratio_of(C, "hc_sw_full")
r_strong_b, r_strong_c = ratio_of(B, "hc_sw_strong"), ratio_of(C, "hc_sw_strong")
r_prov_b, r_prov_c = ratio_of(B, "hc_sw_prov"), ratio_of(C, "hc_sw_prov")
chk("high-contrast [NOTE]: under the 3:1 UI floor -> over the 4.5:1 text floor  (%s -> %s)"
    % (r_note_b, r_note_c), True, True, r_note_b is not None and r_note_b < 3.0,
    r_note_c is not None and r_note_c >= 4.5)
chk("high-contrast [FULL] clears 4.5:1, which is why #174 rather than #4a7  (%s)" % r_full_c,
    None, True, B.get("hc_sw_full"), r_full_c is not None and r_full_c >= 4.5)
# ccclxxx: a repaired declaration is an ADDITION to the cascade. The first cut restored the
# dark-mode fills in high contrast too, and the composite darkened the ground under dark text:
# STRONG measured 4.16 -> 3.84, LESS legible repaired than broken. `background: none` in high
# contrast is why these two are now >= their base values rather than below them.
chk("NO high-contrast regression: STRONG  (%s -> %s)" % (r_strong_b, r_strong_c),
    True, True, r_strong_b is not None, r_strong_c is not None and r_strong_c >= r_strong_b)
chk("NO high-contrast regression: PROVISIONAL  (%s -> %s)" % (r_prov_b, r_prov_c),
    True, True, r_prov_b is not None, r_prov_c is not None and r_prov_c >= r_prov_b)
results.append({"check": "LOGGED not repaired: the high-contrast STRONG badge measures %s:1, "
                         "under 4.5 for 8px text. Pre-existing, UNCHANGED by this cut, an "
                         "authored colour, and a register call rather than a build one."
                         % r_strong_c,
                "kind": "LOGGED", "ok": True, "base_want": r_strong_b, "base_got": r_strong_b,
                "cand_want": r_strong_c, "cand_got": r_strong_c})
print("  LOG      high-contrast STRONG %s -> %s ; PROVISIONAL %s -> %s ; FULL (new) %s ; NOTE %s -> %s"
      % (r_strong_b, r_strong_c, r_prov_b, r_prov_c, r_full_c, r_note_b, r_note_c))

repairs = sum(1 for r in results if r["kind"] == "REPAIR")
payload = {"artifact": os.path.basename(A.out), "checks": len(results), "failed": len(fails),
           "repairs": repairs, "invariants": len(results) - repairs,
           "contrast_high_contrast": {"note": [r_note_b, r_note_c], "full": [None, r_full_c],
                                      "strong": [r_strong_b, r_strong_c],
                                      "provisional": [r_prov_b, r_prov_c]},
           "failures": fails, "results": results}
open(A.out, "w").write(json.dumps(payload, indent=1, sort_keys=True) + "\n")
print("\n  %d checks (%d repairs with a failing base control, %d invariants), %d failed -> %s"
      % (len(results), repairs, len(results) - repairs, len(fails), A.out))
sys.exit(1 if fails else 0)
