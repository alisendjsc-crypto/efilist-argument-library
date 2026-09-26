#!/usr/bin/env python3
"""Build adversarial_map_v1_5.json -- the fixes gate2's judgment owed, on Josiah's word (L4b, 2026-09-26).

WHAT THIS BUILDER DOES:
  i.   It reads adversarial_map_v1_4.json, L4's drafts as gate2 judged them, and applies
       r1/R1_redrafts_v1_5.json. v1_4 and the judgment record stay byte-identical: the judgment pins
       v1_4, and a judged file is superseded, never edited.
  ii.  EVERY REDRAFT ANSWERS A JUDGMENT ROW, AND EVERY OWED ROW IS ANSWERED. A redraft names its row in
       R1_drafts_judgments.json; the row must be an AMEND or REJECT, or an ACCEPT that owes wording. The
       build refuses if any such row has no redraft, or if a redraft touches an entry no row names.
  iii. THE RECORD RIDES IN provenance.redrafted, beside L4's provenance.amended: the judgment row, what
       kind of fix, the prior class, routing and move where they moved, and the base map's md5.
  iv.  Every double-quoted span in a redrafted grounds or terminus_routing is declared and checked
       verbatim with r1/r1_quote_check.py; a move completion must be its R1 row's stronger line,
       asserted as a substring of that row.
  v.   The validator v0_6 runs in-process under --assembly; the build refuses on any violation or
       advisory.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, hashlib, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_5.json")

sys.path.insert(0, STAGE)
sys.path.insert(0, os.path.join(STAGE, "r1"))
import adv_map_validator_v0_6 as V   # noqa: E402
import r1_quote_check as Q           # noqa: E402

BASE = os.path.join(STAGE, "adversarial_map_v1_4.json")
BASE_MD5, BASE_BYTES = "cb61db5cdade98234d69d222b372f515", 333184
JUDGMENTS = os.path.join(STAGE, "r1", "R1_drafts_judgments.json")
JUDGMENTS_MD5 = "fcfe31c7252b9cc49265214aaff09161"
RULINGS = os.path.join(STAGE, "r1", "R1_rulings.json")
RULINGS_MD5 = "3f1dfad54021d7920576c7bd4840b62f"
REDRAFTS = os.path.join(STAGE, "r1", "R1_redrafts_v1_5.json")
CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
PHASES = ("A", "B1", "B2", "C", "D", "E", "R", "F", "G")
KINDS = ("amend_move", "reclass_to_b", "terminus_routing", "grounds_wording")
BY = "library seat, Code (L4, continuing on Josiah's word); drafter under K258, judges nothing"
DATE = "2026-09-26"
UNDER = "Josiah's word on gate2's judgment (canon adversarial_map.R1_drafts_judgment_gate2)"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main():
    fail = []
    raw = open(BASE, "rb").read()
    assert md5b(raw) == BASE_MD5 and len(raw) == BASE_BYTES, "BASE GUARD: v1_4 moved (%s)" % md5b(raw)
    for p, want in ((JUDGMENTS, JUDGMENTS_MD5), (RULINGS, RULINGS_MD5)):
        got = md5b(open(p, "rb").read())
        assert got == want, "BASE GUARD: %s is %s, pinned %s" % (os.path.basename(p), got, want)
    base = json.loads(raw.decode("utf-8"))
    craw = open(CORPUS, "rb").read()
    assert md5b(craw) == base["meta"]["source_corpus_md5"], "corpus is not the one v1_4 pins"
    corpus = json.loads(craw.decode("utf-8"))
    rraw = open(REDRAFTS, "rb").read()
    rd = json.loads(rraw.decode("utf-8"))
    jrows = {r["id"]: r for r in json.load(open(JUDGMENTS, encoding="utf-8"))["rows"]}
    stronger = {}
    for r in json.load(open(RULINGS, encoding="utf-8"))["rows"]:
        stronger[r["n"]] = r["stronger_continuation"]

    # --- completeness: every draft row that owes a fix has exactly one redraft, and nothing else does
    owing = sorted(r["id"] for r in jrows.values() if r.get("kind") == "draft"
                   and (r["verdict"] in ("AMEND", "REJECT") or r.get("owed")))
    named = [x["judgment_row"] for x in rd["redrafts"]]
    if sorted(named) != owing or len(set(named)) != len(named):
        fail.append("redrafts answer %s; the rows that owe a fix are %s" % (sorted(named), owing))

    idx = {}
    for i, e in enumerate(base["entries"]):
        am = e["provenance"].get("amended")
        if am:
            idx[am["r1_n"]] = i
    entries = [json.loads(json.dumps(e)) for e in base["entries"]]
    texts = Q.Texts()
    quotes_all, changed, record = [], {}, []
    for x in sorted(rd["redrafts"], key=lambda x: x["n"]):
        n, tag = x["n"], "#%d" % x["n"]
        jr = jrows.get(x["judgment_row"])
        if jr is None or jr.get("n") != n:
            fail.append("%s: judgment row %s does not name this entry" % (tag, x["judgment_row"]))
            continue
        if x["kind"] not in KINDS:
            fail.append("%s: kind %r" % (tag, x["kind"]))
            continue
        i = idx.get(n)
        if i is None:
            fail.append("%s: no amended entry in v1_4" % tag)
            continue
        e = entries[i]
        frm, fields = {}, []
        if x["kind"] == "amend_move":
            me = x["move_edit"]
            if me["completion"].rstrip(".")[1:] not in stronger.get(n, ""):
                fail.append("%s: the completion is not the R1 row's stronger line" % tag)
            frm["adversarial_move"] = e["adversarial_move"]
            e["adversarial_move"] = e["adversarial_move"] + " " + me["completion"]
            e["grounds"] = x["grounds"]
            fields += ["adversarial_move", "grounds"]
        elif x["kind"] == "reclass_to_b":
            if jr["verdict"] != "REJECT":
                fail.append("%s: a reclassification answers a %s, not a REJECT" % (tag, jr["verdict"]))
            frm.update({"class": e["class"], "routing": e["routing"], "adversarial_move": e["adversarial_move"]})
            e["class"] = "b"
            e["routing"] = {"regen_candidate": x["regen_candidate"]}
            e["adversarial_move"] = x["move"]
            e["grounds"] = x["grounds"]
            fields += ["adversarial_move", "class", "grounds", "routing"]
        elif x["kind"] == "terminus_routing":
            if e["class"] != "d":
                fail.append("%s: terminus_routing on a class %s entry" % (tag, e["class"]))
                continue
            frm["routing"] = json.loads(json.dumps(e["routing"]))
            e["routing"]["residue"]["terminus_routing"] = x["terminus_routing"]
            fields += ["routing"]
        elif x["kind"] == "grounds_wording":
            e["grounds"] = x["grounds"]
            fields += ["grounds"]
        declared = [qq["quote"] for qq in x.get("quotes", [])]
        for fld in ("grounds", "terminus_routing"):
            for span in re.findall(r'"([^"]+)"', x.get(fld, "")):
                if span not in declared:
                    fail.append("%s: undeclared quotation in %s: %r" % (tag, fld, span[:60]))
        quotes_all += [dict(qq, tag=tag) for qq in x.get("quotes", [])]
        e["provenance"] = dict(e["provenance"], redrafted={
            "at": "L4b", "date": DATE, "by": BY, "under": UNDER, "judgment_row": x["judgment_row"],
            "judgment_verdict": jr["verdict"], "kind": x["kind"], "fields_changed": sorted(fields),
            "from": frm, "base": {"artifact": "adversarial_map_v1_4.json", "md5": BASE_MD5}})
        changed[i] = n
        record.append({"n": n, "judgment_row": x["judgment_row"], "verdict": jr["verdict"], "kind": x["kind"],
                       "class_after": e["class"], "target": "%s#%s" % (e["target_id"], e["target_locus"])})

    _ok, qfails = Q.check(quotes_all, texts)
    fail += ["quote " + f for f in qfails]
    for i, e in enumerate(entries):
        if i not in changed and e != base["entries"][i]:
            fail.append("entry %d moved without a redraft" % i)
    nodes = {o["id"]: o for o in corpus["objections"]}
    for pq in rd["pin_move_queue_additions"]:
        node, _, locus = pq["locus"].partition("#")
        if pq["anchor"] not in (V.locus_text(nodes[node], locus) or ""):
            fail.append("%s: anchor not verbatim at %s" % (pq["id"], pq["locus"]))
    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1

    m4 = base["meta"]
    cc = dict(collections.Counter(e["class"] for e in entries))
    per_phase = {ph: dict(collections.Counter(
        e["class"] for e in entries if e["provenance"]["phase"] == ph)) for ph in PHASES}
    tiers = {o["id"]: o["tier"] for o in corpus["objections"]}
    per_tier = {}
    for t in sorted(set(tiers.values())):
        sub = [e for e in entries if tiers[e["target_id"]] == t]
        per_tier["T%d" % t] = {"nodes": len(set(e["target_id"] for e in sub)), "entries": len(sub),
                               **dict(collections.Counter(e["class"] for e in sub))}
    meta = {}
    for k, v in m4.items():
        meta[k] = v
        if k == "r1_amendments":
            meta["r1_redrafts"] = {
                "what": ("The fixes gate2's judgment of v1_4 owed, applied on Josiah's word: %d entries. "
                         "v1_4's other %d entries are byte-identical here." % (len(record), len(entries) - len(record))),
                "his_words_verbatim": rd["his_word"]["verbatim"],
                "answered": rd["his_word"]["answered"],
                "judgment": {"file": "adversarial_map_staging/r1/R1_drafts_judgments.json", "md5": JUDGMENTS_MD5},
                "as_written": ("L4's redrafts. A seat that did not draft them judges them (K258); the judgment is "
                               "recorded in canon and the judgment record, never here."),
                "redrafts": {"file": "adversarial_map_staging/r1/R1_redrafts_v1_5.json", "md5": md5b(rraw),
                             "bytes": len(rraw)},
                "where_each_record_lives": "provenance.redrafted, beside L4's provenance.amended",
                "rows": record,
            }
    meta["artifact"] = "adversarial_map_v1_5.json"
    meta["assembled"] = "2026-09-26, efilist Code seat, L4b (the judged drafts, fixed)"
    meta["successor_to"] = {
        "artifact": "adversarial_map_v1_4.json", "md5": BASE_MD5, "bytes": BASE_BYTES,
        "and_before_it": m4["successor_to"]["artifact"] + " " + m4["successor_to"]["md5"] + " (the map R1 ruled), and "
                         + m4["successor_to"]["and_before_it"],
        "v1_4_is_not_replaced": "v1_4 stays byte-identical on disk: gate2's judgment record pins it.",
        "why_v1_5": "The six fixes the judgment owed, on one ratified standard; no entry added, removed or re-anchored.",
        "frozen_predecessor": m4["successor_to"]["frozen_predecessor"],
    }
    meta["class_counts"] = cc
    meta["per_phase"] = per_phase
    meta["per_tier"] = per_tier
    meta["siblings"] = dict(m4["siblings"], predecessor="adversarial_map_v1_4.json",
                            register="honest_residuals_register_v0_6.json", redrafts="r1/R1_redrafts_v1_5.json")
    meta["fences"] = m4["fences"].replace("honest_residuals_register_v0_5.json", "honest_residuals_register_v0_6.json")
    doc = {"meta": meta, "entries": entries}
    out = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    open(tmp, "wb").write(out)
    lines = []
    passed, viol, adv = V.validate([tmp], CORPUS, assembly=True, out=lines.append)
    if not passed or viol or adv:
        print("REFUSING TO WRITE -- validator v0_6 --assembly: %d violation(s), %d advisory(ies)" % (len(viol), len(adv)))
        for v in (viol + adv)[:20]:
            print("  " + v)
        os.remove(tmp)
        return 1
    os.replace(tmp, OUT)
    checks = [l_ for l_ in lines if l_.startswith(("PASS", "FAIL", "WARN"))]
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), md5b(out)))
    print("  redrafted %d | class %s | quotes %d verbatim | validator v0_6 --assembly: %d checks, all PASS"
          % (len(record), json.dumps(cc, sort_keys=True), len(quotes_all), len(checks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
