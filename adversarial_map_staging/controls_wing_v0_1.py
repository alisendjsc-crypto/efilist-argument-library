#!/usr/bin/env python3
"""
controls_wing_v0_1.py -- K353. The control battery for the Adversarial Map's own surface.

EVERY GATE HERE HAS A FAILING CONTROL, because a gate that cannot be shown to fail for its own
reason is decoration (K348/K349, and WI-K343's standing lesson: the checks that merely restate a
stronger check are where the false alarms accumulate). The strong gate is the renderer's own
input pin + ship-time anchor rule; everything below either adds a claim those cannot make, or
carries a mutation that trips it.

The link-grammar gate is deliberately NOT written from memory: the regex is EXTRACTED from
combined.html at run time, so a future pin that narrows the grammar breaks this battery rather
than silently shipping links the flagship no longer accepts.

  python3 adversarial_map_staging/controls_wing_v0_1.py --out adversarial_map_staging/wing_control_v0_1.json
"""
import io, os, re, sys, json, html, argparse, importlib.util, collections, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location("wing", os.path.join(HERE, "render_wing_v0_1.py"))
WING = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(WING)
V = WING.V

PAGE = os.path.join(ROOT, "adversarial", "index.html")
FLAG = os.path.join(ROOT, "combined.html")

results = []
fails = []


def chk(name, cond, got=""):
    results.append({"check": name, "ok": bool(cond), "detail": str(got)[:400]})
    print(("  ok    " if cond else "  FAIL  ") + name + (("   " + str(got)[:200]) if not cond else ""))
    if not cond:
        fails.append(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "wing_control_v0_1.json"))
    a = ap.parse_args()

    page = io.open(PAGE, encoding="utf-8").read()
    praw = io.open(PAGE, "rb").read()
    asm, reg, cor = WING.load()
    objs = {o["id"]: o for o in cor["objections"]}
    rows, groups = WING.build(asm, reg, cor)
    pure = WING.ship_set(asm)

    print("WING CONTROLS -- page %s / %d bytes" % (V.md5_bytes(praw), len(praw)))

    # ---------------------------------------------------------------- 1 ship-set closure
    all_by = collections.defaultdict(list)
    for e in asm["entries"]:
        all_by[e["target_id"]].append(e)
    expect_nodes = {k for k, v in all_by.items() if all(x["class"] == "d" for x in v)}
    got_nodes = {r["node"] for r in rows}
    chk("ship set == pure-(d) nodes, both directions",
        expect_nodes == got_nodes, "missing %s extra %s"
        % (sorted(expect_nodes - got_nodes), sorted(got_nodes - expect_nodes)))
    chk("every rendered entry is class (d)", all(r["entry"]["class"] == "d" for r in rows))
    chk("every pure-(d) ENTRY is rendered, not just every node",
        len(rows) == sum(len(v) for v in pure.values()),
        "%d rendered vs %d in the pure set" % (len(rows), sum(len(v) for v in pure.values())))

    # FAILING CONTROL: a node with one (a) must not qualify
    mixed = [k for k, v in all_by.items()
             if any(x["class"] == "d" for x in v) and any(x["class"] != "d" for x in v)]
    chk("CONTROL a mixed-class node exists to be excluded", len(mixed) > 0, len(mixed))
    chk("CONTROL no mixed-class node reached the page",
        not (set(mixed) & got_nodes), sorted(set(mixed) & got_nodes))

    # ---------------------------------------------------------------- 2 link grammar, EXTRACTED
    flag = io.open(FLAG, encoding="utf-8").read()
    m = re.search(r"var cardm = /\^(\(obj\|rwe\)[^/]*)/\.exec\(raw\);", flag)
    chk("the flagship's card-anchor regex was EXTRACTED, not retyped", m is not None)
    if not m:
        return finish(a.out)
    grammar = re.compile("^" + m.group(1) + "$")
    hrefs = re.findall(r'<a class="open" href="([^"]+)"', page)
    chk("one open-link per rendered entry", len(hrefs) == len(rows), "%d vs %d" % (len(hrefs), len(rows)))
    frags = [h.split("#", 1)[1] for h in hrefs if "#" in h]
    chk("every open-link carries a fragment", len(frags) == len(hrefs))
    bad = [f for f in frags if not grammar.match(f)]
    chk("every fragment matches the flagship's own grammar", not bad, bad)
    # FAILING CONTROL: forms the grammar must reject
    chk("CONTROL grammar rejects @diagnosis", not grammar.match("obj-natural-reproduce@diagnosis"))
    chk("CONTROL grammar rejects @note", not grammar.match("obj-care-ethics@note"))
    chk("CONTROL grammar rejects an empty suffix", not grammar.match("obj-life-gift@"))
    chk("CONTROL grammar accepts the bare form", bool(grammar.match("obj-life-gift")))

    chk("no @diagnosis or @note is emitted anywhere on the page",
        "@diagnosis" not in page and "@note" not in page)
    ids = [grammar.match(f).group(2) for f in frags]
    chk("every linked id is a real objection", all(i in objs for i in ids),
        sorted(set(i for i in ids if i not in objs)))
    depths = [grammar.match(f).group(3) for f in frags]
    chk("only 'long' or no depth is ever forced", set(depths) <= {"long", None}, sorted(set(map(str, depths))))
    # the locus decides the form, and the diagnosis locus takes the bare one
    formed = {(r["node"], r["locus"]): WING.link_for(r["node"], r["locus"])[0] for r in rows}
    chk("the diagnosis locus takes the BARE form",
        formed[("natural-reproduce", "diagnosis")] == "/combined#obj-natural-reproduce",
        formed.get(("natural-reproduce", "diagnosis")))
    chk("the note locus is linked at @long, not at @note",
        formed[("care-ethics", "note")] == "/combined#obj-care-ethics@long",
        formed.get(("care-ethics", "note")))

    # ---------------------------------------------------------------- 3 verbatim + escaping
    shipped = []
    for r in rows:
        shipped += [r["entry"]["target_anchor"], r["entry"]["adversarial_move"],
                    r["entry"]["grounds"], r["bedrock"]["name"],
                    (r["entry"]["routing"]["residue"] or {}).get("terminus_routing") or "",
                    objs[r["node"]].get("trigger") or r["node"]]
    for g in groups.values():
        shipped += [g[0]["bedrock"]["name"], g[0]["bedrock"]["gloss"]]
    shipped = [s for s in shipped if s]
    missing = [s[:60] for s in shipped if WING.esc(s) not in page]
    chk("every shipped string appears ESCAPED and verbatim on the page", not missing, missing)
    rt = [s[:60] for s in shipped if html.unescape(WING.esc(s)) != s]
    chk("escaping round-trips for every shipped string", not rt, rt)
    # FAILING CONTROL: a string that is NOT on the page must be reported missing
    chk("CONTROL a string not in the corpus is absent",
        WING.esc("this sentence is not in the corpus") not in page)

    # ---------------------------------------------------------------- 4 anchor rule, independently
    bad_anchor = [(r["node"], r["locus"]) for r in rows
                  if r["entry"]["target_anchor"] not in V.locus_text(objs[r["node"]], r["locus"])]
    chk("anchor rule: every AGAINST quote is verbatim at its own locus", not bad_anchor, bad_anchor)
    # FAILING CONTROL: the same quote read at the WRONG locus must not be found
    ctl = [r for r in rows if r["locus"] == "long"][0]
    chk("CONTROL the same quote is NOT found at a different locus",
        ctl["entry"]["target_anchor"] not in V.locus_text(objs[ctl["node"]], "short"))

    # ---------------------------------------------------------------- 5 the terminus label
    # scope: the page MINUS every verbatim span, i.e. only the text this repo authored.
    chrome = page
    for s in sorted(set(shipped), key=len, reverse=True):
        chrome = chrome.replace(WING.esc(s), " ")
    hits = [w for w in WING.STRENGTH_WORDS if w in chrome.lower()]
    chk("no strength claim in the page's OWN text (verbatim spans excluded)", not hits, hits)
    chk("CONTROL the scoping is not vacuous: verbatim spans really were removed",
        len(chrome) < len(page) * 0.55, "%d of %d chars remain" % (len(chrome), len(page)))
    chk("the terminus label is present", WING.SEC_LABEL or WING.PAGE_TITLE in page)
    chk("the page says what it does NOT claim", "would claim more than the map has established" in page)
    chk("'this line terminates here' is stated", "this line terminates here" in page)
    # FAILING CONTROL: the strength scan can fire
    chk("CONTROL the strength scan fires on a planted word",
        any(w in (chrome + " strongest").lower() for w in WING.STRENGTH_WORDS))

    # ---------------------------------------------------------------- 6 the normalizer
    idx = WING.register_index(reg)
    free = {r["entry"]["routing"]["residue"]["bedrock_name"] for r in rows}
    regd = {r["bedrock"]["name"] for r in rows}
    chk("the register join is TOTAL over the ship set",
        all((r["node"], r["locus"]) in idx for r in rows))
    chk("the normalizer choice is not vacuous: free text and register disagree",
        len(free) != len(regd), "free %d vs register %d" % (len(free), len(regd)))
    chk("the register namespace is the smaller one, as claimed",
        len(regd) < len(free), "free %d vs register %d" % (len(free), len(regd)))
    chk("floors named on the page are a strict subset of the register",
        len(groups) < len(reg["bedrocks"]), "%d of %d" % (len(groups), len(reg["bedrocks"])))

    # ---------------------------------------------------------------- 7 the frame's own figure
    top2 = sum(len(v) for v in list(groups.values())[:2])
    chk("the 'two floors' figure on the page is the MEASURED one",
        ("%d of these %d continuations" % (top2, len(rows))) in page,
        "expected '%d of these %d'" % (top2, len(rows)))
    chk("CONTROL that figure is not the trivial one", top2 != len(rows) and top2 > len(rows) // 2, top2)

    # ---------------------------------------------------------------- 8 care-ethics, twice
    ce = [r for r in rows if r["node"] == "care-ethics"]
    facets_on_page = [r for r in rows if ('<span class="hr">%s</span> %s' % (r["hid"], r["facet"])) in page]
    chk("every card names its FACET rather than repeating the floor's name",
        len(facets_on_page) == len(rows), "%d/%d" % (len(facets_on_page), len(rows)))
    hr03 = [r for r in rows if r["hid"] == "HR-03"]
    chk("CONTROL that distinction is not idle: the largest floor spans several facets",
        len({r["facet"] for r in hr03}) > 1, sorted({r["facet"] for r in hr03}))
    chk("care-ethics is on the page twice, at two different floors",
        len(ce) == 2 and len({r["hid"] for r in ce}) == 2,
        [(r["locus"], r["hid"]) for r in ce])
    chk("the one-click-short caveat is stated rather than papered over",
        "one further click" in page and "care-ethics" in page)
    # and the caveat is TRUE: the [NOTE] button is emitted for this node
    ceo = objs["care-ethics"]
    chk("the caveat is true: care-ethics is confidence!=full and has a note, so [NOTE] renders",
        ceo.get("confidence") not in (None, "full") and bool(ceo.get("note")),
        "%s / note=%s" % (ceo.get("confidence"), bool(ceo.get("note"))))

    # ---------------------------------------------------------------- 9 no archetype gate
    # The slot lookup is IMPORTED. The first cut read a TOP-LEVEL "archetypeVariants" key, which
    # no objection has -- they live at responses.archetypeVariants -- so the gate returned a
    # reassuring zero for the wrong reason and its own control convicted it. Reimplementing a
    # lookup the validator already publishes is how that happens.
    stranded = [r["node"] for r in rows if V.node_variant_slots(objs[r["node"]])]
    chk("not one shipped node carries archetypeVariants, so no card sits behind an archetype pill",
        not stranded, stranded)
    corpus_variant_nodes = sum(1 for o in cor["objections"] if V.node_variant_slots(o))
    chk("CONTROL archetypeVariants exist elsewhere in the corpus, so this is a fact not an absence",
        corpus_variant_nodes > 0, corpus_variant_nodes)
    chk("CONTROL the slot lookup is the validator's, not a local re-read of a top-level key",
        sum(1 for o in cor["objections"] if o.get("archetypeVariants")) == 0
        and corpus_variant_nodes > 0,
        "top-level %d / validator %d"
        % (sum(1 for o in cor["objections"] if o.get("archetypeVariants")), corpus_variant_nodes))

    # ---------------------------------------------------------------- 10 determinism
    outs = []
    for seed in ("0", "1"):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "index.html")
            env = dict(os.environ, PYTHONHASHSEED=seed)
            r = subprocess.run([sys.executable, os.path.join(HERE, "render_wing_v0_1.py"), "--out", p],
                               cwd=ROOT, env=env, capture_output=True, text=True)
            outs.append((r.returncode, V.md5_bytes(io.open(p, "rb").read()) if r.returncode == 0 else r.stderr[-200:]))
    chk("reproduces byte-identically under two forced PYTHONHASHSEED values",
        outs[0] == outs[1] and outs[0][0] == 0, outs)
    chk("and reproduces the COMMITTED page", outs[0][1] == V.md5_bytes(praw), outs[0][1])
    # and from the staging directory, not only from the repo root
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "index.html")
        r = subprocess.run([sys.executable, "render_wing_v0_1.py", "--out", p],
                           cwd=HERE, capture_output=True, text=True)
        got = V.md5_bytes(io.open(p, "rb").read()) if r.returncode == 0 else r.stderr[-200:]
    chk("reproduces when run from its COMMITTED location, not only from the repo root",
        got == V.md5_bytes(praw), got)

    # ---------------------------------------------------------------- 11 nothing else moved
    held = {
        "combined.html": "f095c0ce0e5a1d796d57fa5a5dd62f7d",
        "efilist_argument_library_v4_0_0.json": "04bf6482aa0374ee92a81c1d55ec41f8",
        "efilist_argument_library_v4_0_0.jsx": "b196548b6eb39065842d62292acca89f",
        "adversarial_map_staging/adversarial_map_v1_0.json": "c4989e98b042e2f787a82df3f11ecdad",
        "adversarial_map_staging/adversarial_map_v1_1.json": "e9e5abf820e3f7a687e2b84443883ade",
        "adversarial_map_staging/adversarial_map_v1_2.json": "e4bef3cac882aa079951ba7ec1a9d11e",
        "adversarial_map_staging/adversarial_map_v1_3.json": "681827419df72a16a7c6fe70df8fe77f",
        "adversarial_map_staging/honest_residuals_register_v0_4.json": "d067729fafb51926bc9e845209417886",
        "adversarial_map_staging/adv_map_validator_v0_6.py": "c002e93877b09d523daf786036af7a57",
    }
    moved = [k for k, h in sorted(held.items())
             if V.md5_bytes(io.open(os.path.join(ROOT, k), "rb").read()) != h]
    chk("no flagship / corpus / jsx / map / register byte moved", not moved, moved)

    # ---------------------------------------------------------------- 12 page hygiene
    chk("page is valid UTF-8 and ends with exactly one newline",
        praw.endswith(b"\n") and not praw.endswith(b"\n\n"))
    chk("page is CR-free", b"\r" not in praw)
    chk("no unresolved template placeholder", "%s" not in page and "%d" not in page)
    chk("the shared presentation layer is linked, never inlined",
        '<link rel="stylesheet" href="/wuld-layer.css">' in page
        and '<script src="/wuld-layer.js" defer></script>' in page)
    # Scan for the MECHANISM, not for the token. The first cut matched the source comment that
    # explains why the branch is absent -- the marker rather than the defect, and the third time
    # this family has fired in this arc (WI-K343 met it twice in one session).
    pcs_rule = re.search(r"@media[^{]*prefers-color-scheme", page) or \
        re.search(r"matchMedia\s*\(\s*[\"'][^\"']*prefers-color-scheme", page)
    chk("no prefers-color-scheme BRANCH (WI-K321b) -- rule/matchMedia, not the word",
        pcs_rule is None, pcs_rule.group(0) if pcs_rule else "")
    chk("CONTROL that scan fires on a real rule",
        re.search(r"@media[^{]*prefers-color-scheme",
                  page + "@media (prefers-color-scheme: light){}") is not None)
    chk("CONTROL and it does NOT fire on prose naming the feature",
        re.search(r"@media[^{]*prefers-color-scheme", "NO prefers-color-scheme branch here") is None)

    finish(a.out)


def finish(out):
    payload = {
        "artifact": "wing_control_v0_1.json",
        "subject": "adversarial/index.html -- the Adversarial Map's own reader-facing surface",
        "checks": len(results),
        "failed": len(fails),
        "failures": fails,
        "results": results,
    }
    io.open(out, "w", encoding="utf-8").write(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    print("\n  %d checks, %d failed -> %s" % (len(results), len(fails), out))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
