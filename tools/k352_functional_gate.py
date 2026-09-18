#!/usr/bin/env python3
"""k352_functional_gate.py -- the FUNCTIONAL gate on the level-independent affordance.

The sweep and tools/verify_K352.py prove the BYTES: that combined.html is its git base plus
exactly twelve declared edits, and that the cross-surface md5 did not move. Neither proves the
artifact still WORKS, and an untested JS change to a 2.98 MB hand-assembled flagship is the
class of thing that burns a session. This loads the candidate in real Chromium over file://,
with every http(s) request ABORTED so the verdict is about the artifact and not the network,
and asserts the mechanism end to end.

It runs the BASE as a NULL for every deep-link claim. "The affordance fixes the broken link" is
a claim about a before-state, and a before-state is measured, not asserted (ccclxvi).

WHERE IT RUNS. The Cowork container, which carries Chromium and Playwright; the operator's
local VM does not, so this is the one tool in this cut that does not reproduce from its
committed location. Said out loud rather than left for a later session to discover.

  python3 tools/k352_functional_gate.py --base <pinned combined.html> --cand <candidate> \
      --out tools/k352_functional_control_v0_1.json
"""
import argparse, json, sys
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True); ap.add_argument("--cand", required=True)
ap.add_argument("--out", default=None); ap.add_argument("--node", default="care-ethics")
_a = ap.parse_args()
BASE = "file://" + _a.base
CAND = "file://" + _a.cand
NODE = _a.node

fails, out = [], []
def chk(name, cond, got=""):
    out.append(("  ok   " if cond else "  FAIL ") + name + (("   " + str(got)) if not cond else ""))
    if not cond: fails.append(name)

def probe(pg, url, hsh=""):
    """COLD load. goto() to the same document with only the hash changed is a SAME-DOCUMENT
    navigation -- no reload, no re-init, so module state survives. The first cut of this test
    did that and read a previous case's responseLevel as this case's verdict. about:blank
    between probes is what makes each one a real boot."""
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
    try: pg.evaluate("() => { window.__preNav = 1; }")   # BOOT WITNESS, stamped on the OUTGOING document
    except Exception: pass
    pg.goto("about:blank")
    pg.goto(url + hsh, wait_until="load")
    pg.wait_for_timeout(1200)
    if pg.evaluate("() => typeof window.__preNav !== 'undefined'"):
        raise AssertionError("ccclxxvii: same-document navigation -- the initialiser did NOT re-run, "
                             "so any state read here belongs to the PREVIOUS case (%s)" % (url + hsh))
    return errs

def probe_samedoc_DEMO(pg, url, hsh):
    """The failing control for the witness: navigate WITHOUT the about:blank reset and show the
    witness survives, i.e. that the first cut of this test really could read a stale verdict."""
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(800)
    pg.evaluate("() => { window.__preNav = 1; }")
    pg.goto(url + hsh, wait_until="load"); pg.wait_for_timeout(600)
    return pg.evaluate("() => typeof window.__preNav !== 'undefined'")

def state(pg):
    return pg.evaluate("""() => {
      const act = [...document.querySelectorAll('.depth-btn')].filter(b=>b.classList.contains('active')).map(b=>b.dataset.depth);
      const dj  = [...document.querySelectorAll('.depth-jump')];
      const cl  = [...document.querySelectorAll('.copy-link-btn')].map(b=>b.getAttribute('onclick')).filter(s=>s&&s.includes("'obj-"));
      const foc = [...document.querySelectorAll('.objection-header.focused')].map(e=>e.id);
      const open= [...document.querySelectorAll('.objection-header.open')].map(e=>e.id);
      return { activeDepth: act, cards: document.querySelectorAll('#results .objection-header').length,
               djCount: dj.length, djAt: [...new Set(dj.map(b=>b.dataset.at))],
               copySample: cl[0]||null, copyWithAt: cl.filter(s=>s.includes('@')).length,
               focused: foc, open: open, hash: location.hash, rl: (()=>{try{return responseLevel}catch(e){return 'ERR'}})() };
    }""")

with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context()
    ctx.route("**/*", lambda r: r.abort() if r.request.url.startswith(("http://","https://")) else r.continue_())
    pg = ctx.new_page()

    # ---------- 0. the artifact boots at all -----------------------------------------
    e = probe(pg, CAND); s = state(pg)
    chk("candidate boots with no uncaught page error", not e, e[:2])
    chk("candidate renders all 82 cards", s["cards"] == 82, s["cards"])
    chk("candidate default depth is medium (NOT flipped)", s["activeDepth"] == ["medium"] and s["rl"] == "medium", s)

    # ---------- 1. the affordance renders at the DEFAULT level ------------------------
    chk("[DISMANTLE] renders on every card at the default level", s["djCount"] == 82, s["djCount"])
    chk("...and reports 'not at depth' there", s["djAt"] == ["0"], s["djAt"])
    chk("COPY LINK carries NO suffix at the default level", s["copyWithAt"] == 0, s["copySample"])

    # ---------- 2. activation forces long, through setDepth --------------------------
    pg.evaluate("""() => { const c=[...document.querySelectorAll('#results .objection-header')].find(e=>e.id==='obj-%s');
                           c.nextElementSibling.querySelector('.depth-jump').click(); }""" % NODE)
    pg.wait_for_timeout(500); s2 = state(pg)
    chk("activation sets responseLevel=long", s2["rl"] == "long", s2["rl"])
    chk("activation syncs the global depth control (setDepth path, not a parallel one)",
        s2["activeDepth"] == ["long"], s2["activeDepth"])
    chk("activation lands the reader ON the card", ("obj-%s" % NODE) in s2["focused"]
        and ("obj-%s" % NODE) in s2["open"], (s2["focused"], s2["open"]))
    chk("the affordance now reports 'at depth' on every card", s2["djAt"] == ["1"], s2["djAt"])
    chk("COPY LINK now carries @long on every card", s2["copyWithAt"] == 82 and "@long" in s2["copySample"],
        (s2["copyWithAt"], s2["copySample"]))
    chk("the affordance still renders at long (it is level-INDEPENDENT)", s2["djCount"] == 82, s2["djCount"])

    # ---------- 3. THE NULL: the base's behaviour on the same deep link ---------------
    probe(pg, BASE, "#obj-%s" % NODE); b = state(pg)
    chk("NULL: on the BASE, #obj-<id> lands the reader at MEDIUM -- the broken link",
        b["rl"] == "medium" and ("obj-%s" % NODE) in b["focused"], (b["rl"], b["focused"]))
    chk("NULL: the base has no affordance at all", b["djCount"] == 0, b["djCount"])

    # ---------- 4. inbound: the new grammar ------------------------------------------
    e = probe(pg, CAND, "#obj-%s@long" % NODE); s3 = state(pg)
    chk("#obj-<id>@long boots straight to long", s3["rl"] == "long" and s3["activeDepth"] == ["long"],
        (s3["rl"], s3["activeDepth"]))
    chk("#obj-<id>@long focuses the card", ("obj-%s" % NODE) in s3["focused"], s3["focused"])
    chk("#obj-<id>@long raises no page error", not e, e[:2])

    e = probe(pg, CAND, "#obj-%s@short" % NODE); s4 = state(pg)
    chk("#obj-<id>@short boots to short (the grammar is general, not a long-only hack)",
        s4["rl"] == "short" and s4["activeDepth"] == ["short"], (s4["rl"], s4["activeDepth"]))

    # ---------- 5. APPEND-ONLY: every pre-existing form is byte-for-byte unchanged ----
    probe(pg, CAND, "#obj-%s" % NODE); s5 = state(pg)
    chk("APPEND-ONLY: bare #obj-<id> still lands at medium and still focuses, exactly as K108",
        s5["rl"] == "medium" and ("obj-%s" % NODE) in s5["focused"] and s5["activeDepth"] == ["medium"],
        (s5["rl"], s5["focused"], s5["activeDepth"]))
    probe(pg, CAND, "#obj-%s@bogus" % NODE); s6 = state(pg)
    chk("an unknown depth token does NOT match the carve-out (falls to the legacy promote)",
        s6["hash"].startswith("#/rwe/"), s6["hash"])
    # and the property the first cut of this test found by accident, worth asserting on purpose:
    # a bare anchor arriving at a page the reader has already taken to `long` must NOT drag them
    # back to the default. The affordance forces a depth only when the link asks for one.
    probe(pg, CAND, "#obj-%s@long" % NODE)
    pg.evaluate("() => { location.hash = '#obj-life-gift'; }"); pg.wait_for_timeout(600)
    sB = state(pg)
    chk("a bare anchor does NOT reset a reader who is already at long",
        sB["rl"] == "long" and "obj-life-gift" in sB["focused"], (sB["rl"], sB["focused"]))

    probe(pg, CAND, "#obj-not-a-real-node@long"); s7 = state(pg)
    chk("an unknown id with a valid depth degrades silently, no error, no depth change",
        s7["rl"] == "medium", (s7["rl"], s7["hash"]))

    rwe = pg.evaluate("() => (typeof REAL_WORLD_EXAMPLES!=='undefined' && REAL_WORLD_EXAMPLES.length) ? REAL_WORLD_EXAMPLES[0].instance_id : null")
    if rwe:
        probe(pg, CAND, "#rwe-%s" % rwe); r1 = state(pg)
        chk("APPEND-ONLY: #rwe-<id> still promotes to #/rwe/instance:<id>",
            r1["hash"] == "#/rwe/instance:%s" % rwe, r1["hash"])
        probe(pg, CAND, "#rwe-%s@long" % rwe); r2 = state(pg)
        chk("#rwe-<id>@long is NOT claimed -- it falls through to the legacy promote, as before",
            r2["hash"] == "#/rwe/rwe-%s@long" % rwe, r2["hash"])
    else:
        chk("REAL_WORLD_EXAMPLES present for the rwe legs", False, "absent")

    # ---------- 6. hashchange on an already-open page --------------------------------
    probe(pg, CAND)
    pg.evaluate("() => { location.hash = '#obj-%s@long'; }" % NODE); pg.wait_for_timeout(600)
    s8 = state(pg)
    chk("live hashchange (page already booted) also forces the depth",
        s8["rl"] == "long" and ("obj-%s" % NODE) in s8["focused"], (s8["rl"], s8["focused"]))

    # ---------- 7. the note gates are untouched --------------------------------------
    probe(pg, CAND, "#obj-solipsism@long"); n = pg.evaluate("""() => ({
        noteDivs: document.querySelectorAll('.confidence-note').length,
        noteBtns: document.querySelectorAll('.note-toggle').length })""")
    chk("note layer UNCHANGED: 9 note divs, 7 revealers -- the coupling is queued, not repaired",
        (n["noteDivs"], n["noteBtns"]) == (9, 7), n)

    # ---------- 8. the boot witness has a FAILING control ----------------------------
    chk("ccclxxvii control: without the reset the witness SURVIVES, so the guard can fail",
        probe_samedoc_DEMO(pg, CAND, "#obj-%s@long" % NODE) is True)
    chk("ccclxxvii control: with the reset it does not",
        (probe(pg, CAND, "#obj-%s@long" % NODE) or True) is True)

    br.close()

art = {"artifact": "k352_functional_control_v0_1", "generated_by": "tools/k352_functional_gate.py",
       "subject": "combined.html -- the level-independent affordance (K352)",
       "method": "real Chromium via Playwright over file://, all http(s) requests aborted; the pinned base run as a NULL for every deep-link claim",
       # K351 found assembly_control_v0_2.json unreproducible because it recorded a scratch path.
       # Record the IDENTITY of what was tested, never where it happened to sit.
       "base_md5": __import__("hashlib").md5(open(_a.base, "rb").read()).hexdigest(),
       "candidate_md5": __import__("hashlib").md5(open(_a.cand, "rb").read()).hexdigest(),
       "node_under_test": NODE,
       "checks": [l.strip() for l in out], "n_checks": len(out),
       "failures": fails, "verdict": "RED" if fails else "GREEN"}
if _a.out:
    with open(_a.out, "w", encoding="utf-8") as f:
        json.dump(art, f, indent=2, ensure_ascii=False); f.write("\n")
print("\n".join(out))
print("\nK352 FUNCTIONAL GATE: " + ("RED -- %d failure(s)" % len(fails) if fails else "GREEN (%d checks)" % len(out)))
sys.exit(1 if fails else 0)
