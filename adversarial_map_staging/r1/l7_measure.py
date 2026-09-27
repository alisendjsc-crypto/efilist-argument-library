#!/usr/bin/env python3
"""l7_measure.py -- where every entry of the ruled map v1_6 stands in the v4.1.5 text (L7, 2026-09-26, R0223 order 1).

The ruled map v1_6 is pinned to corpus 04bf6482 (the text before v4.1.3). Two cuts have since moved text under it:
v4.1.3 (L5: the 23 rows PR-01 ratified) and v4.1.5 (L6: the 20 rows SR-01 ratified). v4.1.4 moved page design only.
The successor map is pinned to 7b6e65e5 (v4.1.5), so before a word of it is drafted this measures, for every entry:

  1. THE CHAIN. The landed rows ARE the whole difference: PR-01's rows applied to 04bf6482's objections give
     f3d88311's objections exactly, and SR-01's rows applied to those give 7b6e65e5's. Anything else that moved
     between the cuts would be text no knock-on record looked at, so this is asserted before anything is classified.
  2. EVERY ANCHOR (138 of 138). Where the anchor lies in the pre-cut locus, against the landed rows' spans mapped
     into pre-cut coordinates and widened to their sentences (sentence_bounds, imported from sp_dossiers_l6.py):
       unchanged  the locus did not move; or an occurrence of the anchor lies outside every repaired sentence and
                  the anchor is still verbatim (gate2's fifth-stratum law: it survives, and is read where it survives)
       moved      every occurrence lies inside a repaired sentence, and the anchor string is still in the v4.1.5
                  locus (W-007, ruled at R0164: a repair moves every anchor inside its sentence)
       gone       the anchor is no longer verbatim in the v4.1.5 locus
  3. EVERY ROUTED ANSWER. Each (a) whose answered_by names a locus either cut moved, with its current R1 row.
  4. EVERY QUOTING PASSAGE. Map text that carries six or more consecutive words of a repaired sentence (the
     knock-on records' shingle, over the move and the grounds, and here also over a (d)'s bedrock_name and
     terminus_routing), with whether those words are still in the v4.1.5 locus.
  5. AGREEMENT WITH THE INPUTS. Both knock-on records (PQ_knock_on_L5_v0_2.json, SP_knock_on_L6_v0_2.json) are read
     at the md5s canon names, never re-derived by hand: every row of each must be reproduced by 2-4, or this refuses.
     What 2-4 find beyond them is listed with the row that caused it, never dropped.

Everything is read at a pin (pinned.py): the map, the three corpora, both drafts records, both knock-on records,
the R1 rulings, the R1 evidence (#n for R1's entries) and the two modules imported. Nothing else is read.

  python3 l7_measure.py             # write l7_measure_v0_1.json
  python3 l7_measure.py --check     # recompute; compare with the committed record byte for byte
  python3 l7_measure.py --self-test # controls, the unmutated first; --emit <path> writes their record

Repo-relative. Writes only its record (or --emit's path). Deterministic: file order throughout, sort where a set is
listed. It spawns nothing and writes no temp file.
"""
import copy, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = os.path.join(HERE, "l7_measure_v0_1.json")
S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
CORPUS = "efilist_argument_library_v4_0_0.json"
PIN = {
    "map": (S + "/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "corpus_pre": (CORPUS, "04bf6482aa0374ee92a81c1d55ec41f8"),
    "corpus_mid": (CORPUS, "f3d88311ea98f8333aebbecb67766351"),
    "corpus_post": (CORPUS, "7b6e65e531018fecb37baf2a4fedd6d1"),
    "drafts_L5": (R + "/PQ_repair_drafts_L5.json", "8c57223e8f9170cb8303bcc4b9d982c4"),
    "drafts_L6": (R + "/SP_drafts_L6.json", "e493f8cdcf74aa3ad7982e1e906cffde"),
    "knock_on_L5": (R + "/PQ_knock_on_L5_v0_2.json", "2cde775ee82cd16b0e5cdb88820bd130"),
    "knock_on_L6": (R + "/SP_knock_on_L6_v0_2.json", "013319b88335e3b6ce6bc8dd9ac709a4"),
    "rulings": (R + "/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74"),
    "evidence": (R + "/R1_evidence_2026-09-19.json", "719b5ddb27680f32181a8a953c84b6c2"),
}
MODS = {
    "validator": (S + "/adv_map_validator_v0_6.py", "c002e93877b09d523daf786036af7a57"),
    "sp_dossiers": (R + "/sp_dossiers_l6.py", None),   # md5 filled at load from the committed blob; see load_mod
}
CUTS = (("L5", "v4.1.3", "drafts_L5", "PR-01", "corpus_pre", "corpus_mid"),
        ("L6", "v4.1.5", "drafts_L6", "SR-01", "corpus_mid", "corpus_post"))
SHINGLE = 6


def md5b(b):
    return hashlib.md5(b).hexdigest()


def load_inputs():
    raw = {k: pinned.bytes_at(REPO, rel, m) for k, (rel, m) in PIN.items()}
    return {k: json.loads(b.decode("utf-8")) for k, b in raw.items()}


def load_mod(key):
    rel, want = MODS[key]
    b = open(os.path.join(REPO, rel), "rb").read()
    if want is not None:
        assert md5b(b) == want, "MODULE GUARD: %s is %s, pinned %s" % (rel, md5b(b), want)
    spec = importlib.util.spec_from_file_location("l7_" + key, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, md5b(b)


V, _V_MD5 = load_mod("validator")
SPD, SPD_MD5 = load_mod("sp_dossiers")
sentence_bounds, shingles = SPD.sentence_bounds, SPD.shingles


def get_locus(node, locus):
    return V.locus_text(node, locus)


def set_locus(node, locus, text):
    if locus in ("diagnosis", "note"):
        node[locus] = text
    elif locus.startswith("archetypeVariants."):
        node["responses"]["archetypeVariants"][locus.split(".", 1)[1]] = text
    else:
        node["responses"][locus] = text


def landed_rows(inp, cut):
    _tag, _ver, dkey, rid, _a, _b = cut
    rows = inp[dkey]["rows"]
    rat = [r for r in rows if r["id"] == rid]
    assert len(rat) == 1 and rat[0]["kind"] == "ratification", "%s: no single ratification row %s" % (dkey, rid)
    by = {r["id"]: r for r in rows}
    return [by[i] for i in rat[0]["rows"]]


def back(l5_edits, p, is_end):
    """A v4.1.3 position mapped to pre-cut coordinates through the L5 edits at its locus ((start, end, delta) in
    pre-cut coordinates). A position inside an L5 replacement widens to that replacement's pre-cut start or end."""
    shift = 0
    for ci, cj, dl in sorted(l5_edits):
        m0, m1 = ci + shift, cj + shift + dl
        if p <= m0:
            break
        if p < m1:
            return cj if is_end else ci
        shift += dl
    return p - shift


def measure(inp):
    fail = []
    nodes = {k: {o["id"]: o for o in inp[k]["objections"]} for k in ("corpus_pre", "corpus_mid", "corpus_post")}

    # ---- 1. the chain -------------------------------------------------------------------------------------------
    chain = {}
    work = copy.deepcopy(inp["corpus_pre"]["objections"])
    wby = {o["id"]: o for o in work}
    for cut in CUTS:
        tag, ver, dkey, rid, a, b = cut
        rows = landed_rows(inp, cut)
        for r in rows:
            node, _, loc = r["locus"].partition("#")
            t = get_locus(wby[node], loc)
            if t.count(r["current"]) != 1:
                fail.append("CHAIN: %s %s: its current text occurs %d times at %s"
                            % (tag, r["id"], t.count(r["current"]), r["locus"]))
                continue
            i = t.index(r["current"])
            set_locus(wby[node], loc, t[:i] + r["replacement"] + t[i + len(r["current"]):])
        same = json.dumps(work, sort_keys=True, ensure_ascii=False) == \
            json.dumps(inp[b]["objections"], sort_keys=True, ensure_ascii=False)
        chain[tag] = {"cut": ver, "ratification": rid, "rows": len(rows),
                      "loci": len({r["locus"] for r in rows}), "objections_equal": same}
        if not same:
            fail.append("CHAIN: %s's %d rows applied to %s do not give %s's objections" % (tag, len(rows), a, b))

    # ---- the landed spans, in PRE-CUT coordinates ------------------------------------------------------------------
    # An L5 row's current text is pre-cut text. An L6 row's is v4.1.3 text: it is mapped back through the L5 edits at
    # its locus, and a span that reaches into an L5 replacement widens to that replacement's pre-cut span.
    edits, l5 = {}, {}
    for cut in CUTS:
        tag, _v, _d, _r, a, _b = cut
        for r in landed_rows(inp, cut):
            node, _, loc = r["locus"].partition("#")
            t = get_locus(nodes[a][node], loc)
            if t.count(r["current"]) != 1:
                fail.append("SPAN: %s %s: its current text occurs %d times in %s at %s"
                            % (tag, r["id"], t.count(r["current"]), a, r["locus"]))
                continue
            i = t.index(r["current"])
            j = i + len(r["current"])
            if tag == "L5":
                l5.setdefault(r["locus"], []).append((i, j, len(r["replacement"]) - len(r["current"])))
                i0, j0 = i, j
            else:
                i0, j0 = back(l5.get(r["locus"], []), i, False), back(l5.get(r["locus"], []), j, True)
            edits.setdefault(r["locus"], []).append((tag, r["id"], i0, j0))

    pre, post = nodes["corpus_pre"], nodes["corpus_post"]

    def sentences_of(locus):
        """Pre-cut (start, end, cut, row) spans and their widened sentences at a changed locus."""
        node, _, loc = locus.partition("#")
        t0 = get_locus(pre[node], loc)
        out = []
        for tag, rid, i0, j0 in edits.get(locus, []):
            b0, b1 = sentence_bounds(t0, i0, j0)
            out.append({"cut": tag, "row": rid, "span": (i0, j0), "sentence": (b0, b1)})
        return t0, out

    # ---- 2. every anchor ----------------------------------------------------------------------------------------
    ev = {(e["target_id"], e["target_locus"], e["target_anchor"]): e["n"] for e in inp["evidence"]["entries"]}
    rrows = inp["rulings"]["rows"]
    sup = {r["supersedes"] for r in rrows if r.get("supersedes")}
    current = {r["n"]: r for r in rrows if r["row"] not in sup}
    entries = inp["map"]["entries"]
    per_entry, status_n = [], {}
    for idx, e in enumerate(entries):
        tid, loc, a = e["target_id"], e["target_locus"], e["target_anchor"]
        locus = "%s#%s" % (tid, loc)
        n = ev.get((tid, loc, a))
        t0, t2 = get_locus(pre[tid], loc), get_locus(post[tid], loc)
        if a not in t0:
            fail.append("ANCHOR: entry %d (%s) is not verbatim in the pre-cut locus the map pins" % (idx, locus))
            continue
        row = {"i": idx, "n": n, "target": locus, "class": e["class"], "anchor": a}
        if t0 == t2:
            row["status"] = "unchanged"
        else:
            _t, sp = sentences_of(locus)
            occ, k = [], t0.find(a)
            while k != -1:
                occ.append(k)
                k = t0.find(a, k + 1)
            where = []
            for p in occ:
                q = p + len(a)
                span = sorted({s["row"] for s in sp if p < s["span"][1] and q > s["span"][0]})
                sent = sorted({s["row"] for s in sp if p < s["sentence"][1] and q > s["sentence"][0]} - set(span))
                where.append({"at": p, "inside_span": span, "inside_sentence": sent})
            now = t2.count(a)
            outside = [w for w in where if not w["inside_span"] and not w["inside_sentence"]]
            if now == 0:
                row["status"] = "gone"
            elif outside:
                row["status"] = "unchanged"
                row["survives_outside"] = True
            else:
                row["status"] = "moved"
            row["locus_changed_by"] = sorted({"%s %s" % (s["cut"], s["row"]) for s in sp})
            row["occurrences_pre"] = where
            row["occurrences_post"] = now
        status_n[row["status"]] = status_n.get(row["status"], 0) + 1
        per_entry.append(row)

    changed_loci = sorted(edits)

    # ---- 3. every routed answer ---------------------------------------------------------------------------------
    routes = []
    for idx, e in enumerate(entries):
        if e["class"] != "a":
            continue
        n = ev.get((e["target_id"], e["target_locus"], e["target_anchor"]))
        for ref in e["routing"]["answered_by"]:
            if ref in edits:
                ru = current.get(n)
                routes.append({"i": idx, "n": n, "target": "%s#%s" % (e["target_id"], e["target_locus"]),
                               "anchor": e["target_anchor"], "answered_by": ref,
                               "rows": ["%s %s" % (x[0], x[1]) for x in edits[ref]],
                               "ruling_row": ru["row"] if ru else None, "verdict": ru["verdict"] if ru else None})

    # ---- 4. every quoting passage -------------------------------------------------------------------------------
    quotes = []
    for locus in changed_loci:
        t0, sp = sentences_of(locus)
        node, _, loc = locus.partition("#")
        t2 = get_locus(post[node], loc)
        for s in sp:
            text = t0[s["sentence"][0]:s["sentence"][1]]
            sh = shingles(text, SHINGLE)
            for idx, e in enumerate(entries):
                fields = [("adversarial_move", e["adversarial_move"]), ("grounds", e["grounds"])]
                rs = e["routing"].get("residue")
                if rs:
                    fields += [("bedrock_name", rs["bedrock_name"]), ("terminus_routing", rs["terminus_routing"])]
                for fld, val in fields:
                    hit = sorted(x for x in sh if x in val)
                    if hit:
                        quotes.append({"i": idx, "n": ev.get((e["target_id"], e["target_locus"], e["target_anchor"])),
                                       "target": "%s#%s" % (e["target_id"], e["target_locus"]), "class": e["class"],
                                       "field": fld, "quotes_from": locus, "row": "%s %s" % (s["cut"], s["row"]),
                                       "shingles": len(hit), "first": hit[0],
                                       "still_verbatim_post": [x in t2 for x in hit].count(True)})

    # ---- 5. agreement with the two knock-on records --------------------------------------------------------------
    matched = {"routes": set(), "quotes": set(), "anchors": set()}
    by_target_anchor = {}
    for r in per_entry:
        by_target_anchor.setdefault((r["target"], r["anchor"]), []).append(r)
    pq_locus = {}
    for r in inp["drafts_L5"]["rows"]:
        if r.get("locus"):
            pq_locus.setdefault(r.get("pq") or r["id"], r["locus"])
            pq_locus.setdefault(r["id"], r["locus"])
    agree = []
    for key, rec in (("L5", inp["knock_on_L5"]), ("L6", inp["knock_on_L6"])):
        for k, kr in enumerate(rec["rows"]):
            ok, why = False, ""
            if kr["kind"] in ("anchor_inside", "anchor_meets_repair"):
                hits = by_target_anchor.get((kr["locus"], kr["anchor"]), [])
                ok = len(hits) == 1 and hits[0]["status"] in ("moved", "gone")
                if ok and kr["kind"] == "anchor_meets_repair":
                    ok = (hits[0]["status"] == "moved") == bool(kr["survives_the_repair"])
                if ok:
                    matched["anchors"].add(hits[0]["i"])
                why = "the entry at %s is %s" % (kr["locus"], [h["status"] for h in hits] or "absent")
            elif kr["kind"] == "answer_routes_here":
                hits = [x for x in routes if x["target"] == kr["target"] and x["anchor"] == kr["anchor"]
                        and x["answered_by"] == kr["locus"]]
                ok = len(hits) == 1 and hits[0]["verdict"] == kr["verdict"] and hits[0]["ruling_row"] == kr["ruling_row"]
                if ok:
                    matched["routes"].add((hits[0]["i"], hits[0]["answered_by"]))
                why = "%d routed answer(s) found" % len(hits)
            elif kr["kind"] == "quoted_in_map":
                loc_k = kr.get("locus") or pq_locus.get(kr["pq"])
                hits = [x for x in quotes if x["target"] == kr["target"] and x["field"] == kr["field"]
                        and x["quotes_from"] == loc_k and kr["shingle"] in entries[x["i"]][kr["field"]]]
                ok = bool(hits)
                if ok:
                    for x in hits:
                        matched["quotes"].add((x["i"], x["field"], x["quotes_from"]))
                why = "%d quoting passage(s) found" % len(hits)
            agree.append({"record": key, "row": k, "kind": kr["kind"], "reproduced": ok})
            if not ok:
                fail.append("AGREEMENT: knock-on %s row %d (%s at %s) not reproduced: %s"
                            % (key, k, kr["kind"], kr.get("locus") or kr.get("target"), why))
    beyond = {
        "anchors": [{"i": r["i"], "target": r["target"], "status": r["status"], "rows": r["locus_changed_by"]}
                    for r in per_entry if r["status"] in ("moved", "gone") and r["i"] not in matched["anchors"]],
        "routes": [{"i": x["i"], "n": x["n"], "target": x["target"], "answered_by": x["answered_by"], "rows": x["rows"]}
                   for x in routes if (x["i"], x["answered_by"]) not in matched["routes"]],
        "quotes": [{"i": x["i"], "n": x["n"], "target": x["target"], "field": x["field"], "quotes_from": x["quotes_from"],
                    "row": x["row"]} for x in quotes if (x["i"], x["field"], x["quotes_from"]) not in matched["quotes"]],
    }
    survives = [{"i": r["i"], "target": r["target"], "rows": r["locus_changed_by"]}
                for r in per_entry if r.get("survives_outside")]
    return fail, {
        "chain": chain, "changed_loci": changed_loci, "status_counts": dict(sorted(status_n.items())),
        "entries": per_entry, "routes": routes, "quotes": quotes,
        "agreement": {"rows": len(agree), "reproduced": sum(1 for x in agree if x["reproduced"]),
                      "by_record": {k: sum(1 for x in agree if x["record"] == k) for k in ("L5", "L6")}},
        "beyond_the_knock_on_records": beyond, "survives_outside_a_repaired_sentence": survives}


def build(inp):
    fail, m = measure(inp)
    if fail:
        return fail, None
    rec = {
        "artifact": "l7_measure_v0_1.json",
        "instrument": R + "/l7_measure.py",
        "session": "L7 (R0223 order 1), seat l, Code; measures only, drafts nothing",
        "pinned": {k: {"file": rel, "md5": md5} for k, (rel, md5) in PIN.items()},
        "modules": {"validator": {"file": MODS["validator"][0], "md5": MODS["validator"][1]},
                    "sp_dossiers": {"file": MODS["sp_dossiers"][0], "md5": SPD_MD5,
                                    "uses": "sentence_bounds, shingles (the L6 knock-on's own functions)"}},
        "classes": {"unchanged": "the locus did not move, or an occurrence lies outside every repaired sentence and "
                                 "is still verbatim (gate2, fifth stratum)",
                    "moved": "every occurrence lies inside a repaired sentence; the anchor string is still in the "
                             "v4.1.5 locus (W-007)",
                    "gone": "the anchor is no longer verbatim in the v4.1.5 locus"},
        "shingle_words": SHINGLE,
    }
    rec.update(m)
    return [], rec


def serialize(rec):
    return json.dumps(rec, indent=2, ensure_ascii=False) + "\n"


def self_test(emit=None):
    base = load_inputs()
    results = []

    def run(name, mutate, expect):
        inp = copy.deepcopy(base)
        if mutate:
            mutate(inp)
        fail, rec = build(inp)
        if expect is None:
            ok = not fail and serialize(rec) == open(RECORD, encoding="utf-8").read()
        else:
            ok = any(expect in f for f in fail)
        results.append({"control": name, "expect": "reproduces the committed record" if expect is None
                        else "refuses, naming %r" % expect, "as_expected": ok})
        print("%-70s %s" % (name, "as expected" if ok else "UNEXPECTED"))
        return ok

    def drop_row(cut_rid, row_id):
        def m(inp):
            for k in ("drafts_L5", "drafts_L6"):
                for r in inp[k]["rows"]:
                    if r["id"] == cut_rid:
                        r["rows"] = [x for x in r["rows"] if x != row_id]
        return m

    def knock_anchor(inp):
        r = [x for x in inp["knock_on_L6"]["rows"] if x["kind"] == "anchor_meets_repair"][0]
        r["anchor"] = r["anchor"][:-1] + "X"

    def knock_verdict(inp):
        r = [x for x in inp["knock_on_L5"]["rows"] if x["kind"] == "answer_routes_here"][0]
        r["verdict"] = "HOLDS" if r["verdict"] == "FAILS" else "FAILS"

    def knock_survives(inp):
        r = [x for x in inp["knock_on_L6"]["rows"] if x["kind"] == "anchor_meets_repair"][0]
        r["survives_the_repair"] = not r["survives_the_repair"]

    def map_anchor(inp):
        inp["map"]["entries"][0]["target_anchor"] = "an anchor that is nowhere in the locus"

    def post_moved(inp):
        o = [x for x in inp["corpus_post"]["objections"] if x["id"] == "life-gift"][0]
        o["responses"]["short"] = o["responses"]["short"] + " A sentence no row landed."

    def quote_gone(inp):
        r = [x for x in inp["knock_on_L5"]["rows"] if x["kind"] == "quoted_in_map"][0]
        r["shingle"] = "six words that no map passage carries"

    ok = run("C0 unmutated: reproduces the committed record", None, None)
    if not ok:
        print("SELF-TEST: the unmutated control failed; nothing after it means anything")
        return 1
    run("C1 a landed L6 row dropped from SR-01 (SD-07)", drop_row("SR-01", "SD-07"), "CHAIN: L6")
    run("C2 a landed L5 row dropped from PR-01 (PD-16)", drop_row("PR-01", "PD-16"), "CHAIN: L5")
    run("C3 text moved in v4.1.5 that no row landed", post_moved, "CHAIN: L6")
    run("C4 a knock-on anchor altered by one character", knock_anchor, "AGREEMENT: knock-on L6")
    run("C5 a knock-on verdict flipped", knock_verdict, "AGREEMENT: knock-on L5")
    run("C6 a knock-on 'survives the repair' flipped", knock_survives, "AGREEMENT: knock-on L6")
    run("C7 a knock-on shingle no passage carries", quote_gone, "AGREEMENT: knock-on L5")
    run("C8 a map anchor absent from the pre-cut locus", map_anchor, "ANCHOR: entry 0")
    good = sum(1 for r in results if r["as_expected"])
    rec = {"artifact": os.path.basename(emit) if emit else "l7_measure_control_v0_1.json",
           "instrument": R + "/l7_measure.py --self-test",
           "record": {"file": R + "/l7_measure_v0_1.json", "md5": md5b(open(RECORD, "rb").read())},
           "result": "%d of %d controls as expected, the unmutated first" % (good, len(results)),
           "controls": results}
    if emit:
        open(emit, "w", encoding="utf-8").write(serialize(rec))
    print("SELF-TEST: %d of %d controls as expected" % (good, len(results)))
    return 0 if good == len(results) else 1


def main():
    if "--self-test" in sys.argv:
        emit = sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None
        return self_test(emit)
    fail, rec = build(load_inputs())
    if fail:
        print("REFUSED -- %d failure(s):" % len(fail))
        for f in fail:
            print("  " + f)
        return 1
    s = serialize(rec)
    if "--check" in sys.argv:
        same = open(RECORD, encoding="utf-8").read() == s
        print("MEASURE RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        return 0 if same else 1
    open(RECORD, "w", encoding="utf-8").write(s)
    print("WROTE %s  %d B  md5 %s" % (os.path.basename(RECORD), len(s.encode("utf-8")), md5b(s.encode("utf-8"))))
    print("  chain %s | status %s | routed answers %d | quoting passages %d | knock-on rows reproduced %d of %d"
          % ({k: v["objections_equal"] for k, v in rec["chain"].items()}, rec["status_counts"], len(rec["routes"]),
             len(rec["quotes"]), rec["agreement"]["reproduced"], rec["agreement"]["rows"]))
    b = rec["beyond_the_knock_on_records"]
    print("  beyond the knock-on records: anchors %d, routes %d, quotes %d; survives outside a repaired sentence %d"
          % (len(b["anchors"]), len(b["routes"]), len(b["quotes"]), len(rec["survives_outside_a_repaired_sentence"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
