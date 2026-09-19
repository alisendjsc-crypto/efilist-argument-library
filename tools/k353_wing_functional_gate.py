#!/usr/bin/env python3
"""k353_wing_functional_gate.py -- the FUNCTIONAL gate on the Adversarial Map's own surface.

controls_wing_v0_1.py proves the BYTES: that every fragment matches the grammar EXTRACTED from
combined.html, that every id is real, that no @diagnosis is emitted. None of that proves a
reader who clicks actually lands at the locus. This serves both surfaces from a local server
that mirrors the Pages routing (/combined -> combined.html, /adversarial/ -> the wing), drives
real Chromium, and asserts the end-to-end claim for EVERY link the wing emits.

It runs the SUFFIX-STRIPPED form as a NULL for every @long claim: "the wing's links land the
reader at full dismantlement" is a claim about a before-state, and a before-state is measured
(ccclxvi).

Every probe carries a BOOT WITNESS (ccclxxvii): a fragment-only navigation is SAME-DOCUMENT, so
a hash-varying test reads the previous case's state as this case's verdict. about:blank between
probes is what makes each one a real boot, and a failing control proves the witness can fire.

WHERE IT RUNS. The Cowork container, which carries Chromium and Playwright; the operator's local
VM does not. So this is the one tool in this cut that does not reproduce from its committed
location, exactly as k352_functional_gate.py said of itself.

AMENDED AT K354. Three checks here asserted the DEFECT rather than a property: that solipsism's
[NOTE] control is absent, that seven cards carry one, and that the layer stands at 9 notes / 7
reachable. K354 lifted the control out of `if (conf !== 'full')` so its condition equals its
container's, and all three inverted -- and nothing else in this file did. The pre-amendment run
against the repaired flagship is kept as k354_prior_gate_inversion_v0_1.json, 16 checks / 3
failed, and it is the cleanest evidence of the repair that exists. The three now assert the
repaired state, and this file's own control artifact moves to v0_2 so the K353 record stands.
"""
import json, re, sys, threading, http.server, socketserver, functools, os, argparse
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--root", default="/mnt/user-data/uploads/efilist-argument-library")
ap.add_argument("--out", default="k354_wing_functional_control_v0_2.json")
ap.add_argument("--shots", default="/home/claude/k353/shots")
A = ap.parse_args()
ROOT = A.root

results, fails = [], []
def chk(name, cond, got=""):
    results.append({"check": name, "ok": bool(cond), "detail": str(got)[:300]})
    print(("  ok    " if cond else "  FAIL  ") + name + (("   " + str(got)[:220]) if not cond else ""))
    if not cond: fails.append(name)

class H(http.server.SimpleHTTPRequestHandler):
    """Mirrors the Pages routing this wing's links assume: extensionless /combined, and
    /adversarial/ served as a directory index."""
    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p in ("/combined", "/combined.html"): return os.path.join(ROOT, "combined.html")
        if p in ("/adversarial", "/adversarial/", "/adversarial/index.html"):
            return os.path.join(ROOT, "adversarial", "index.html")
        return os.path.join(ROOT, p.lstrip("/"))
    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), H)
PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:%d" % PORT
print("serving %s at %s" % (ROOT, BASE))

def probe(pg, url):
    errs = []
    try: pg.evaluate("() => { window.__preNav = 1; }")
    except Exception: pass
    pg.goto("about:blank")
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(900)
    if pg.evaluate("() => typeof window.__preNav !== 'undefined'"):
        raise AssertionError("ccclxxvii: same-document navigation -- the initialiser did NOT re-run")
    return errs

with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={"width": 1280, "height": 2000})
    pg = ctx.new_page()
    perr = []
    pg.on("pageerror", lambda e: perr.append(str(e)[:200]))
    # external hosts are blocked so the verdict is about the artifacts, not the network
    pg.route(re.compile(r"^https?://(?!127\.0\.0\.1)"), lambda r: r.abort())

    # ---------------------------------------------------------------- the wing itself
    probe(pg, BASE + "/adversarial/")
    chk("the wing loads with no page error", not perr, perr)
    n_terms = pg.eval_on_selector_all(".term", "e => e.length")
    n_floors = pg.eval_on_selector_all(".floor", "e => e.length")
    chk("22 termination cards render", n_terms == 22, n_terms)
    chk("9 floor sections render", n_floors == 9, n_floors)
    hrefs = pg.eval_on_selector_all("a.open", "es => es.map(e => e.getAttribute('href'))")
    chk("22 open-links in the live DOM", len(hrefs) == 22, len(hrefs))
    jump = pg.eval_on_selector_all(".floorjump a", "es => es.map(e => e.getAttribute('href'))")
    chk("every floor-jump anchor resolves to a section on the page",
        all(pg.eval_on_selector_all(h, "e => e.length") == 1 for h in jump), jump)
    os.makedirs(A.shots, exist_ok=True)
    pg.screenshot(path=os.path.join(A.shots, "wing_top.png"))
    pg.evaluate("() => document.querySelector('.floor').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(A.shots, "wing_cards.png"))
    pg.evaluate("() => document.documentElement.setAttribute('data-mode','legible')")
    pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(A.shots, "wing_legible.png"))

    # ---------------------------------------------------------------- every emitted link
    ok_long, ok_bare, bad = 0, 0, []
    for h in hrefs:
        frag = h.split("#", 1)[1]
        want_long = frag.endswith("@long")
        nid = re.match(r"obj-([A-Za-z0-9_-]+)", frag).group(1)
        perr.clear()
        probe(pg, BASE + h)
        lvl = pg.evaluate("() => (typeof responseLevel !== 'undefined') ? responseLevel : null")
        # No `||` fallback: the card element IS `obj-<id>`, verified in the DOM. A fallback
        # here would let the check pass on a different element and call it the same finding.
        open_card = pg.evaluate(
            "id => { var el = document.getElementById('obj-'+id);"
            " return !!(el && el.offsetParent !== null); }", nid)
        if want_long:
            good = (lvl == "long") and open_card and not perr
            ok_long += good
        else:
            good = open_card and not perr
            ok_bare += good
        if not good:
            bad.append({"href": h, "level": lvl, "card_visible": open_card, "errors": list(perr)})
    chk("every @long link lands the reader at FULL DISMANTLEMENT with the card open",
        ok_long == 21, "%d/21 -- %s" % (ok_long, bad))
    chk("the one bare link (the diagnosis locus) opens its card",
        ok_bare == 1, "%d/1" % ok_bare)
    chk("no page error on any of the 22 landings", not bad, bad)

    # ---------------------------------------------------------------- the NULL (before-state)
    nulls = []
    for h in [x for x in hrefs if x.endswith("@long")][:4]:
        probe(pg, BASE + h.replace("@long", ""))
        nulls.append(pg.evaluate("() => responseLevel"))
    chk("NULL: the same links WITHOUT the suffix leave the reader at the boot default",
        set(nulls) == {"medium"}, nulls)
    chk("CONTROL so the suffix is what does the work, measured rather than asserted",
        ok_long == 21 and set(nulls) == {"medium"})

    # ---------------------------------------------------------------- the care-ethics caveat
    probe(pg, BASE + "/combined#obj-care-ethics@long")
    # SCOPED to the card. A document-wide `.note-toggle` query is not a fact about this node:
    # at responseLevel `long` EVERY conf!=full node with a note emits one, so the bare selector
    # answers "does any card anywhere have a note control", which is not the question. The first
    # cut asked it that way in both directions and its own solipsism control convicted it.
    # SCOPE BY THE FLAGSHIP'S OWN BINDING, not by DOM containment. Two cuts of this check were
    # wrong in two different ways. A document-wide `.note-toggle` query answers "does ANY card
    # have a note control" -- at `long`, seven do -- which is not the question. Scoping to
    # `#obj-care-ethics .note-toggle` is wrong the other way: the expanded body lives in a
    # SEPARATE subtree (#results > .detail-panel), so that selector is empty for every node and
    # would have reported the note unreachable everywhere. The toggle's own onclick names its
    # node, so that is what identifies it.
    def note_btn(nid):
        return pg.evaluate("id => [...document.querySelectorAll('.note-toggle')]"
                           ".some(e => (e.getAttribute('onclick')||'').includes(\"toggleNote('\"+id+\"')\"))", nid)
    has_note_btn = note_btn("care-ethics")
    note_hidden = pg.evaluate(
        "() => { var n = document.getElementById('note-care-ethics');"
        " return n ? (n.offsetParent === null || getComputedStyle(n).display === 'none') : null; }")
    chk("care-ethics: the [NOTE] control IS present after landing, so 'one further click' is true",
        has_note_btn is True, has_note_btn)
    chk("care-ethics: and the note is still closed until that click, so the caveat is not idle",
        note_hidden is True, note_hidden)
    pg.screenshot(path=os.path.join(A.shots, "flagship_care_ethics_long.png"))

    # solipsism: the ship-set card whose note K349 measured as unreachable by any reader and
    # K354 repaired. It is in the wing's 21-node ship set, which is what made the repair this
    # session's business rather than a carry: the wing points readers at that card.
    probe(pg, BASE + "/combined#obj-solipsism@long")
    sol_btn = note_btn("solipsism")
    any_btn = pg.evaluate("() => document.querySelectorAll('.note-toggle').length")
    n_notes = pg.evaluate("() => Object.keys(window).length && "
                          "document.querySelectorAll('.confidence-note').length")
    chk("solipsism: its [NOTE] control is PRESENT -- the K349 finding, repaired at K354",
        sol_btn is True, sol_btn)
    chk("CONTROL the binding-scoped query is not vacuous: all 9 note-bearing cards carry one",
        any_btn == 9, any_btn)
    chk("and the gap K349 measured is CLOSED: 9 notes rendered at `long`, 9 reachable",
        n_notes == 9 and any_btn == 9, "%s notes / %s controls" % (n_notes, any_btn))

    # ---------------------------------------------------------------- the witness's own control
    pg.goto(BASE + "/combined", wait_until="load"); pg.wait_for_timeout(700)
    pg.evaluate("() => { window.__preNav = 1; }")
    pg.goto(BASE + "/combined#obj-life-gift@long", wait_until="load"); pg.wait_for_timeout(500)
    survived = pg.evaluate("() => typeof window.__preNav !== 'undefined'")
    chk("CONTROL the boot witness CAN fire: without the reset it survives a hash-only nav",
        survived is True, survived)
    br.close()

srv.shutdown()
payload = {"artifact": os.path.basename(A.out), "checks": len(results), "failed": len(fails),
           "failures": fails, "results": results}
open(A.out, "w").write(json.dumps(payload, indent=1, sort_keys=True) + "\n")
print("\n  %d checks, %d failed -> %s" % (len(results), len(fails), A.out))
sys.exit(1 if fails else 0)
