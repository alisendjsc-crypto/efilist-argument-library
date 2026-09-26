#!/usr/bin/env python3
"""Build adversarial_map_v1_4.json -- R1's 45 FAILS, drafted (L4, 2026-09-25).

WHAT THIS BUILDER DOES, AND WHY IT IS NOT build_assembly_v1_3.py WITH A NEW LINE:
  i.   IT DOES NOT RE-ASSEMBLE FROM FRAGMENTS. It reads adversarial_map_v1_3.json, the map R1
       ruled, and applies the drafts in r1/R1_drafts_L4.json to it. Every fragment and v1_3
       stay byte-identical: R1_rulings.json and the R1 evidence file both pin v1_3, and every
       R1 gate reads it. The K338/K351 route (amend the ratified fragment in place) would move
       nine pinned files to change forty-one entries; this route moves none.
  ii.  EVERY FAILS ROW IS ACCOUNTED FOR, AND NO HOLDS ROW IS TOUCHED. The builder reads the
       current verdict of each of the 69 rows and refuses unless the drafts cover exactly the
       FAILS, once each. An entry the drafts leave alone must come out equal to its v1_3 self.
  iii. THE AMENDMENT RECORD RIDES IN provenance.amended. The validator's entry-keys check admits
       exactly the nine schema keys, and provenance is the entry's own history, so the record
       sits where a reader of the entry meets it and v0_6 validates the result unchanged. It
       names the R1 row, the standard, the shape, the prior class and routing, and any move
       edit (the cut text, so the original move is recoverable from the entry itself).
  iv.  A (d)'s BEDROCK IS COPIED, NOT TYPED. Each (d) draft names the registered (d) its line
       reaches (`bedrock_from`); the builder copies that entry's shipped bedrock_name verbatim
       and asserts the pinned register files it under the draft's HR-id and facet. Registered
       by lookup, as the K338 reclassifications were.
  v.   EVERY QUOTATION IS CHECKED. Each double-quoted span in a drafted grounds or
       terminus_routing must be declared in the draft's `quotes`, and every declared quote must
       be an exact substring of its source, checked by r1/r1_quote_check.py, the instrument the
       R1 rulings are checked with.
  vi.  THE VALIDATOR RUNS IN-PROCESS under --assembly and the build refuses on any violation or
       advisory. v0_6 is unchanged.

Repo-relative. --out <dir> to emit elsewhere. Deterministic: no set is iterated into the output.
"""
import collections, hashlib, io, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_4.json")

sys.path.insert(0, STAGE)
sys.path.insert(0, os.path.join(STAGE, "r1"))
import adv_map_validator_v0_6 as V   # noqa: E402
import r1_quote_check as Q           # noqa: E402

BASE = os.path.join(STAGE, "adversarial_map_v1_3.json")
BASE_MD5, BASE_BYTES = "681827419df72a16a7c6fe70df8fe77f", 269352
RULINGS = os.path.join(STAGE, "r1", "R1_rulings.json")
RULINGS_MD5 = "3f1dfad54021d7920576c7bd4840b62f"
EVIDENCE = os.path.join(STAGE, "r1", "R1_evidence_2026-09-19.json")
EVIDENCE_MD5 = "719b5ddb27680f32181a8a953c84b6c2"
REGISTER = os.path.join(STAGE, "honest_residuals_register_v0_4.json")
REGISTER_MD5 = "d067729fafb51926bc9e845209417886"
DRAFTS = os.path.join(STAGE, "r1", "R1_drafts_L4.json")
CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")

PHASES = ("A", "B1", "B2", "C", "D", "E", "R", "F", "G")
SHAPES = ("route_to_bedrock", "answer_flagged_b", "aggravation_s11_1", "aggravation_cross_node",
          "under_strength_move", "routed_answer_silent")
DISPOSITIONS = ("a_to_d", "a_to_b", "reroute_a", "trim_waits", "waits")
MOVE_EDITS = ("trim", "trim_and_complete", "reauthor")
AMENDED_BY = "library seat, Code (L4); drafter under K258, judges nothing"
AMENDED_DATE = "2026-09-25"
STANDARD = "adversarial_map.R1_standard_ruling_L2"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def canon_shapes():
    """n -> failure shape, from canon's R1_progress_L3 (the seat's reading, as ruled)."""
    names = sorted(f for f in os.listdir(REPO) if re.match(r"project_canon_v38_\d+\.json$", f))
    if len(names) != 1:
        sys.exit("REFUSED: expected exactly one project_canon_v38_*.json, found %d" % len(names))
    c = json.load(io.open(os.path.join(REPO, names[0]), encoding="utf-8"))
    fs = c["adversarial_map"]["R1_progress_L3"]["failure_shapes_seat_s_reading"]
    out = {}
    for shape, v in fs.items():
        for n in v["entries"]:
            out[n] = shape
    return out


def main():
    fail = []
    raw = open(BASE, "rb").read()
    assert md5b(raw) == BASE_MD5 and len(raw) == BASE_BYTES, "BASE GUARD: v1_3 moved (%s)" % md5b(raw)
    for p, want in ((RULINGS, RULINGS_MD5), (EVIDENCE, EVIDENCE_MD5), (REGISTER, REGISTER_MD5)):
        got = md5b(open(p, "rb").read())
        assert got == want, "BASE GUARD: %s is %s, pinned %s" % (os.path.basename(p), got, want)
    base = json.loads(raw.decode("utf-8"))
    craw = open(CORPUS, "rb").read()
    assert md5b(craw) == base["meta"]["source_corpus_md5"], "corpus is not the one v1_3 pins"
    corpus = json.loads(craw.decode("utf-8"))
    nodes = {o["id"]: o for o in corpus["objections"]}
    draws = open(DRAFTS, "rb").read()
    drafts_doc = json.loads(draws.decode("utf-8"))
    drafts = drafts_doc["drafts"]

    # --- the rows: the CURRENT verdict per entry (a later row supersedes an earlier one)
    rows = json.load(open(RULINGS, encoding="utf-8"))["rows"]
    by_row = {r["row"]: r for r in rows}
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    current = {}
    for r in rows:
        if r["row"] not in superseded:
            if r["n"] in current:
                fail.append("two current rows for #%d" % r["n"])
            current[r["n"]] = r
    fails_n = sorted(n for n, r in current.items() if r["verdict"] == "FAILS")
    holds_n = sorted(n for n, r in current.items() if r["verdict"] == "HOLDS")
    ev = {e["n"]: e for e in json.load(open(EVIDENCE, encoding="utf-8"))["entries"]}
    shapes = canon_shapes()

    # --- the partition: drafts cover exactly the FAILS, once each
    dn = [x["n"] for x in drafts]
    if sorted(dn) != fails_n or len(set(dn)) != len(dn):
        fail.append("drafts cover %s; the FAILS are %s" % (sorted(dn), fails_n))
    if set(dn) & set(holds_n):
        fail.append("a draft touches a HOLDS row: %s" % sorted(set(dn) & set(holds_n)))
    if sorted(shapes) != fails_n:
        fail.append("canon's failure shapes cover %d entries, the FAILS are %d" % (len(shapes), len(fails_n)))

    idx = {(e["target_id"], e["target_anchor"]): i for i, e in enumerate(base["entries"])}
    entries = [json.loads(json.dumps(e)) for e in base["entries"]]
    reg = json.load(open(REGISTER, encoding="utf-8"))
    reg_row = {}
    for b in reg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                reg_row[(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], f["facet_id"])

    texts = Q.Texts()
    quotes_all = []
    changed = {}
    record = []
    for x in sorted(drafts, key=lambda x: x["n"]):
        n = x["n"]
        tag = "#%d" % n
        r = current.get(n)
        if r is None or r["row"] != x["row"] or r["verdict"] != "FAILS":
            fail.append("%s: row %s is not the current FAILS row" % (tag, x["row"]))
            continue
        disp = x["disposition"]
        if disp not in DISPOSITIONS:
            fail.append("%s: disposition %r" % (tag, disp))
            continue
        e_ev = ev[n]
        i = idx.get((e_ev["target_id"], e_ev["target_anchor"]))
        if i is None:
            fail.append("%s: no v1_3 entry at %s / %r" % (tag, e_ev["target_id"], e_ev["target_anchor"]))
            continue
        e = entries[i]
        if "%s#%s" % (e["target_id"], e["target_locus"]) != r["target"] or e["class"] != "a":
            fail.append("%s: the v1_3 entry is %s#%s class %s, the row says %s"
                        % (tag, e["target_id"], e["target_locus"], e["class"], r["target"]))
            continue
        shape = shapes.get(n)
        if shape not in SHAPES:
            fail.append("%s: shape %r" % (tag, shape))
        if disp == "waits":
            extra = sorted(set(x) - {"n", "row", "disposition", "waits_on", "for_the_judge"})
            if extra:
                fail.append("%s: a waiting entry carries edit fields %s" % (tag, extra))
            record.append(dict(n=n, row=x["row"], target=r["target"], shape=shape, disposition=disp,
                               class_after="a", entry_changed=False, waits_on=x["waits_on"]))
            continue

        before = json.loads(json.dumps(e))
        frm = {"class": e["class"], "routing": before["routing"]}
        fields = []
        # --- the move
        me = x.get("move_edit")
        if me:
            if me["kind"] not in MOVE_EDITS:
                fail.append("%s: move_edit kind %r" % (tag, me["kind"]))
                continue
            mv = e["adversarial_move"]
            if me["kind"] == "reauthor":
                new_mv = me["move"]
            else:
                if mv.count(me["cut"]) != 1:
                    fail.append("%s: the cut does not occur exactly once in the v1_3 move" % tag)
                    continue
                new_mv = mv.replace(me["cut"], "", 1)
                if me["kind"] == "trim_and_complete":
                    new_mv = new_mv + " " + me["completion"]
            frm["adversarial_move"] = mv
            e["adversarial_move"] = new_mv
            fields.append("adversarial_move")
        elif disp == "trim_waits":
            fail.append("%s: trim_waits with no move_edit" % tag)
        # --- class, routing, grounds
        if disp == "a_to_d":
            src = x["bedrock_from"]
            node, _, locus = src.partition("#")
            ds = [y for y in base["entries"] if y["target_id"] == node and y["target_locus"] == locus
                  and y["class"] == "d"]
            if len(ds) != 1:
                fail.append("%s: bedrock_from %s names %d (d) entries in v1_3" % (tag, src, len(ds)))
                continue
            got = reg_row.get((node, locus, ds[0]["target_anchor"]))
            if got != (x["hr"], x["facet"]):
                fail.append("%s: the register files %s under %s, the draft says %s/%s"
                            % (tag, src, got, x["hr"], x["facet"]))
            e["class"] = "d"
            e["routing"] = {"residue": {"bedrock_name": ds[0]["routing"]["residue"]["bedrock_name"],
                                        "terminus_routing": x["terminus_routing"], "novel": False}}
            e["grounds"] = x["grounds"]
            fields += ["class", "grounds", "routing"]
        elif disp == "a_to_b":
            e["class"] = "b"
            e["routing"] = {"regen_candidate": x["regen_candidate"]}
            e["grounds"] = x["grounds"]
            fields += ["class", "grounds", "routing"]
        elif disp == "reroute_a":
            e["routing"] = {"answered_by": list(x["answered_by"])}
            e["grounds"] = x["grounds"]
            fields += ["grounds", "routing"]
        # --- quotations: declared, and verbatim
        declared = [qq["quote"] for qq in x.get("quotes", [])]
        for fld in ("grounds", "terminus_routing"):
            for span in re.findall(r'"([^"]+)"', x.get(fld, "")):
                if span not in declared:
                    fail.append("%s: undeclared quotation in %s: %r" % (tag, fld, span[:60]))
        for qq in x.get("quotes", []):
            quotes_all.append(dict(qq, tag=tag))
        # --- the record
        am = {"at": "L4", "date": AMENDED_DATE, "by": AMENDED_BY, "under": STANDARD,
              "r1_row": x["row"], "r1_n": n, "shape": shape, "disposition": disp,
              "fields_changed": sorted(fields), "from": frm}
        if disp == "a_to_d":
            am["bedrock_from"] = x["bedrock_from"]
        if me:
            am["move_edit"] = {k: v for k, v in me.items() if k != "move"}
        am["base"] = {"artifact": "adversarial_map_v1_3.json", "md5": BASE_MD5}
        e["provenance"] = dict(e["provenance"], amended=am)
        changed[i] = n
        rw = dict(n=n, row=x["row"], target=r["target"], shape=shape, disposition=disp,
                  class_after=e["class"], entry_changed=True)
        if disp == "trim_waits":
            rw["waits_on"] = x["waits_on"]
        record.append(rw)

    ok, qfails = Q.check(quotes_all, texts)
    fail += ["quote " + f for f in qfails]
    # untouched entries are their v1_3 selves
    for i, e in enumerate(entries):
        if i not in changed and e != base["entries"][i]:
            fail.append("entry %d moved without a draft" % i)
    # queue anchors are verbatim where they say
    for pq in drafts_doc["pin_move_queue"]:
        node, _, locus = pq["locus"].partition("#")
        if pq["anchor"] not in (V.locus_text(nodes[node], locus) or ""):
            fail.append("%s: anchor not verbatim at %s" % (pq["id"], pq["locus"]))
        if pq.get("repair_src"):
            _ok, f2 = Q.check([{"src": pq["repair_src"], "quote": pq["repair"], "tag": pq["id"]}], texts)
            fail += ["queue " + f for f in f2]

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1

    # --- meta: v1_3's, carried, with the computed fields recomputed
    m3 = base["meta"]
    cc = dict(collections.Counter(e["class"] for e in entries))
    per_phase = {ph: dict(collections.Counter(
        e["class"] for e in entries if e["provenance"]["phase"] == ph)) for ph in PHASES}
    tiers = {o["id"]: o["tier"] for o in corpus["objections"]}
    per_tier = {}
    for t in sorted(set(tiers.values())):
        sub = [e for e in entries if tiers[e["target_id"]] == t]
        per_tier["T%d" % t] = {"nodes": len(set(e["target_id"] for e in sub)), "entries": len(sub),
                               **dict(collections.Counter(e["class"] for e in sub))}
    by_disp = dict(collections.Counter(rw["disposition"] for rw in record))
    moved = [rw for rw in record if rw["entry_changed"]]
    meta = {}
    for k, v in m3.items():
        meta[k] = v
        if k == "state":
            meta["r1_amendments"] = {
                "what": ("R1's 45 FAILS, disposed of by a drafting pass under the standard Josiah "
                         "adopted at L2 (canon %s) and the reading rules of R1_rules_L3. %d entries "
                         "change; %d wait on a (b) repair with no byte moved." %
                         (STANDARD, len(moved), len(record) - len(moved))),
                "his_words_verbatim": drafts_doc["standard"]["his_words_verbatim"],
                "the_recommendation_he_adopted": drafts_doc["standard"]["the_recommendation_he_adopted"],
                "as_written": ("L4's drafts. A seat that did not draft them judges them (K258, the gate2 "
                               "role); whether they are judged, and how, is recorded in canon, never here."),
                "by_disposition": by_disp,
                "entries_changed": len(moved),
                "entries_waiting_unchanged": len(record) - len(moved),
                "where_each_record_lives": ("provenance.amended on every changed entry: the R1 row, the "
                                            "standard, the shape, the prior class and routing, and any move "
                                            "edit with the text it cut. provenance is the entry's history and "
                                            "the validator's nine-key check admits no tenth key, so v0_6 "
                                            "validates this file unchanged."),
                "drafts": {"file": "adversarial_map_staging/r1/R1_drafts_L4.json", "md5": md5b(draws),
                           "bytes": len(draws)},
                "rulings": {"file": "adversarial_map_staging/r1/R1_rulings.json", "md5": RULINGS_MD5},
                "rows": record,
            }
    meta["artifact"] = "adversarial_map_v1_4.json"
    meta["assembled"] = "2026-09-25, efilist Code seat, L4 (drafting pass)"
    meta["successor_to"] = {
        "artifact": "adversarial_map_v1_3.json", "md5": BASE_MD5, "bytes": BASE_BYTES,
        "and_before_it": ("adversarial_map_v1_2.json (e4bef3cac882aa079951ba7ec1a9d11e), v1_1 "
                          "(e9e5abf820e3f7a687e2b84443883ade) and v1_0 (FROZEN, c4989e98b042e2f787a82df3f11ecdad)"),
        "v1_3_is_not_replaced": ("v1_3 stays byte-identical on disk: it is the map R1 ruled, and "
                                 "R1_rulings.json, the R1 evidence file and every R1 gate pin it."),
        "why_v1_4_and_not_v2_0": ("Every one of v1_3's 138 entries is here in the same order; none is "
                                  "added, removed or re-anchored, and the schema's key set is unchanged. "
                                  "%d entries change disposition or text under one ratified standard, "
                                  "each tied to the R1 row that ruled it; the other %d are byte-identical "
                                  "to v1_3. The kickoff names this file v1_4; a v2_0 would mean the "
                                  "mapping itself was redone rather than R1 applied to it." % (len(moved), len(entries) - len(moved))),
        "frozen_predecessor": m3["successor_to"]["frozen_predecessor"],
    }
    meta["class_counts"] = cc
    meta["per_phase"] = per_phase
    meta["per_tier"] = per_tier
    meta["validation"] = ("validator v0_6 under --assembly against the post-cut corpus, in-process at "
                          "build: 0 violations AND 0 advisories, or this file is not written.")
    meta["fences"] = ("Nothing here authorizes a byte. The drafts are unjudged. (b) and (c) yields are "
                      "intake candidates routing through staging -> cold-grade -> assembly inside a declared "
                      "content cut; corpus repairs the drafts need are queued for a pin move Josiah opens "
                      "(R1_drafts_L4.json pin_move_queue). (d) termini route to "
                      "honest_residuals_register_v0_5.json.")
    meta["siblings"] = dict(m3["siblings"], predecessor="adversarial_map_v1_3.json",
                            register="honest_residuals_register_v0_5.json",
                            drafts="r1/R1_drafts_L4.json")
    doc = {"meta": meta, "entries": entries}
    out = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    open(tmp, "wb").write(out)

    lines = []
    passed, viol, adv = V.validate([tmp], CORPUS, assembly=True, out=lines.append)
    if not passed or viol or adv:
        print("REFUSING TO WRITE -- validator v0_6 --assembly: %d violation(s), %d advisory(ies)"
              % (len(viol), len(adv)))
        for v in (viol + adv)[:20]:
            print("  " + v)
        os.remove(tmp)
        return 1
    os.replace(tmp, OUT)
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), md5b(out)))
    print("  entries %d | changed %d | waiting unchanged %d | class %s"
          % (len(entries), len(moved), len(record) - len(moved), json.dumps(cc, sort_keys=True)))
    print("  by disposition %s" % json.dumps(by_disp, sort_keys=True))
    checks = [l_ for l_ in lines if l_.startswith(("PASS", "FAIL", "WARN"))]
    print("  quotes checked %d, all verbatim | validator v0_6 --assembly: %d checks, all PASS"
          % (len(quotes_all), len(checks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
