#!/usr/bin/env python3
"""Build adversarial_map_v1_6.json -- #46 re-ruled FAILS and reclassified (L4c, 2026-09-26).

  i.   It reads adversarial_map_v1_5.json (gate2 judged it; its record pins it) and applies
       r1/R1_redrafts_v1_6.json. v1_5 stays byte-identical.
  ii.  AUTHORITY IS CHECKED, NOT ASSUMED. The entry's current row in R1_rulings.json must be FAILS and must
       supersede a HOLDS row; gate2's knock-on row the redraft names must read REOPENS for the same entry.
  iii. The (d)'s bedrock_name is copied from the registered (d) the redraft names by locus AND anchor (two
       (d)s now share red-button-repugnant's sophisticate slot), and register v0_6 must file that (d) under the
       HR-id and facet the redraft claims.
  iv.  The record rides in provenance.amended (this entry had none: R1 held it until now), naming the new R1
       row, the one it supersedes, the knock-on row, and the prior class and routing. Its failure shape is read
       from canon's newest R1_progress_L* block by r1_collision_list.shapes_from_canon, the instrument that
       lists the collisions, so the two cannot disagree (gate2's note on R1-070).
  v.   Quotations declared and checked with r1/r1_quote_check.py; the validator v0_6 runs in-process under
       --assembly; the build refuses on any violation or advisory.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, hashlib, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_6.json")

sys.path.insert(0, STAGE)
sys.path.insert(0, os.path.join(STAGE, "r1"))
import adv_map_validator_v0_6 as V   # noqa: E402
import r1_quote_check as Q           # noqa: E402
import r1_collision_list as CL       # noqa: E402

BASE = os.path.join(STAGE, "adversarial_map_v1_5.json")
BASE_MD5, BASE_BYTES = "0df413ed655a5373468c218832854bbe", 342742
RULINGS = os.path.join(STAGE, "r1", "R1_rulings.json")
RULINGS_MD5 = "d829437e938a8b9dded5cb8cbaa26b74"
KNOCK = os.path.join(STAGE, "r1", "R1_v1_5_judgments.json")
KNOCK_MD5 = "291e80fd27b4a8928129daca52929bd8"
REGISTER = os.path.join(STAGE, "honest_residuals_register_v0_6.json")
REGISTER_MD5 = "0689f46f18a4dbe8d40c9982a2ad06f9"
REDRAFTS = os.path.join(STAGE, "r1", "R1_redrafts_v1_6.json")
EVIDENCE = os.path.join(STAGE, "r1", "R1_evidence_2026-09-19.json")
CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
PHASES = ("A", "B1", "B2", "C", "D", "E", "R", "F", "G")
BY = "library seat, Code (L4c, on Josiah's word); drafter under K258, judges nothing"
DATE = "2026-09-26"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main():
    fail = []
    raw = open(BASE, "rb").read()
    assert md5b(raw) == BASE_MD5 and len(raw) == BASE_BYTES, "BASE GUARD: v1_5 moved (%s)" % md5b(raw)
    for p, want in ((RULINGS, RULINGS_MD5), (KNOCK, KNOCK_MD5), (REGISTER, REGISTER_MD5)):
        got = md5b(open(p, "rb").read())
        assert got == want, "BASE GUARD: %s is %s, pinned %s" % (os.path.basename(p), got, want)
    base = json.loads(raw.decode("utf-8"))
    craw = open(CORPUS, "rb").read()
    assert md5b(craw) == base["meta"]["source_corpus_md5"], "corpus is not the one v1_5 pins"
    corpus = json.loads(craw.decode("utf-8"))
    rraw = open(REDRAFTS, "rb").read()
    rd = json.loads(rraw.decode("utf-8"))
    rows = json.load(open(RULINGS, encoding="utf-8"))["rows"]
    by_row = {r["row"]: r for r in rows}
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    current = {r["n"]: r for r in rows if r["row"] not in superseded}
    knock = {r["id"]: r for r in json.load(open(KNOCK, encoding="utf-8"))["rows"]}
    _canon, shape_of, _means = CL.shapes_from_canon(REPO)
    ev = {e["n"]: e for e in json.load(open(EVIDENCE, encoding="utf-8"))["entries"]}
    reg_row = {}
    for b in json.load(open(REGISTER, encoding="utf-8"))["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                reg_row[(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], f["facet_id"])

    idx = {(e["target_id"], e["target_anchor"]): i for i, e in enumerate(base["entries"])}
    entries = [json.loads(json.dumps(e)) for e in base["entries"]]
    texts = Q.Texts()
    quotes_all, changed, record = [], {}, []
    for x in rd["redrafts"]:
        n, tag = x["n"], "#%d" % x["n"]
        r = current.get(n)
        if r is None or r["verdict"] != "FAILS" or not r.get("supersedes") \
                or by_row.get(r["supersedes"], {}).get("verdict") != "HOLDS":
            fail.append("%s: its current R1 row is not a FAILS superseding a HOLDS" % tag)
            continue
        k = knock.get(x["knock_on_row"])
        if k is None or k.get("n") != n or k.get("verdict") != "REOPENS":
            fail.append("%s: knock-on row %s does not reopen this entry" % (tag, x["knock_on_row"]))
            continue
        i = idx.get((ev[n]["target_id"], ev[n]["target_anchor"]))
        if i is None:
            fail.append("%s: no v1_5 entry" % tag)
            continue
        e = entries[i]
        if e["class"] != "a" or "amended" in e["provenance"]:
            fail.append("%s: the v1_5 entry is not an untouched (a)" % tag)
            continue
        if n not in shape_of:
            fail.append("%s: canon's newest R1_progress block gives it no failure shape" % tag)
            continue
        node, _, locus = x["bedrock_from"].partition("#")
        src = [y for y in base["entries"] if y["target_id"] == node and y["target_locus"] == locus
               and y["target_anchor"] == x["bedrock_from_anchor"] and y["class"] == "d"]
        if len(src) != 1:
            fail.append("%s: bedrock_from names %d (d)s" % (tag, len(src)))
            continue
        if reg_row.get((node, locus, x["bedrock_from_anchor"])) != (x["hr"], x["facet"]):
            fail.append("%s: the register does not file bedrock_from under %s/%s" % (tag, x["hr"], x["facet"]))
        frm = {"class": e["class"], "routing": e["routing"]}
        e["class"] = "d"
        e["routing"] = {"residue": {"bedrock_name": src[0]["routing"]["residue"]["bedrock_name"],
                                    "terminus_routing": x["terminus_routing"], "novel": False}}
        e["grounds"] = x["grounds"]
        declared = [q["quote"] for q in x["quotes"]]
        for fld in ("grounds", "terminus_routing"):
            for span in re.findall(r'"([^"]+)"', x[fld]):
                if span not in declared:
                    fail.append("%s: undeclared quotation in %s: %r" % (tag, fld, span[:60]))
        quotes_all += [dict(q, tag=tag) for q in x["quotes"]]
        e["provenance"] = dict(e["provenance"], amended={
            "at": "L4c", "date": DATE, "by": BY, "under": "adversarial_map.R1_standard_ruling_L2",
            "r1_row": r["row"], "r1_n": n, "supersedes": r["supersedes"], "knock_on_row": x["knock_on_row"],
            "shape": shape_of[n], "disposition": x["disposition"],
            "fields_changed": ["class", "grounds", "routing"], "from": frm,
            "bedrock_from": x["bedrock_from"], "bedrock_from_anchor": x["bedrock_from_anchor"],
            "base": {"artifact": "adversarial_map_v1_5.json", "md5": BASE_MD5}})
        changed[i] = n
        record.append({"n": n, "r1_row": r["row"], "supersedes": r["supersedes"], "knock_on_row": x["knock_on_row"],
                       "class_after": "d", "terminus": "%s %s" % (x["hr"], x["facet"]),
                       "target": "%s#%s" % (e["target_id"], e["target_locus"])})
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

    m5 = base["meta"]
    cc = dict(collections.Counter(e["class"] for e in entries))
    per_phase = {ph: dict(collections.Counter(e["class"] for e in entries if e["provenance"]["phase"] == ph))
                 for ph in PHASES}
    tiers = {o["id"]: o["tier"] for o in corpus["objections"]}
    per_tier = {}
    for t in sorted(set(tiers.values())):
        sub = [e for e in entries if tiers[e["target_id"]] == t]
        per_tier["T%d" % t] = {"nodes": len(set(e["target_id"] for e in sub)), "entries": len(sub),
                               **dict(collections.Counter(e["class"] for e in sub))}
    meta = {}
    for k, v in m5.items():
        meta[k] = v
        if k == "r1_redrafts":
            meta["r1_rerulings"] = {
                "what": "An entry R1 held, re-ruled FAILS after gate2's knock-on reading, reclassified under the class law.",
                "his_words_verbatim": rd["his_word"]["verbatim"], "answered": rd["his_word"]["answered"],
                "redrafts": {"file": "adversarial_map_staging/r1/R1_redrafts_v1_6.json", "md5": md5b(rraw), "bytes": len(rraw)},
                "rulings": {"file": "adversarial_map_staging/r1/R1_rulings.json", "md5": RULINGS_MD5},
                "knock_on": {"file": "adversarial_map_staging/r1/R1_v1_5_judgments.json", "md5": KNOCK_MD5},
                "as_written": "L4c's draft; a seat that did not draft it judges it (K258), recorded in canon, never here.",
                "rows": record}
    meta["artifact"] = "adversarial_map_v1_6.json"
    meta["assembled"] = "2026-09-26, efilist Code seat, L4c (#46 re-ruled and reclassified)"
    meta["successor_to"] = dict(m5["successor_to"], artifact="adversarial_map_v1_5.json", md5=BASE_MD5, bytes=BASE_BYTES,
                                and_before_it="adversarial_map_v1_4.json cb61db5cdade98234d69d222b372f515, and before it "
                                              + m5["successor_to"]["and_before_it"],
                                why_v1_6="One entry re-ruled on his word and reclassified; nothing else moves.")
    meta["successor_to"].pop("why_v1_5", None)
    meta["successor_to"].pop("v1_4_is_not_replaced", None)
    meta["successor_to"]["v1_5_is_not_replaced"] = "v1_5 stays byte-identical on disk: gate2's v1_5 judgment pins it."
    meta["class_counts"] = cc
    meta["per_phase"] = per_phase
    meta["per_tier"] = per_tier
    meta["siblings"] = dict(m5["siblings"], predecessor="adversarial_map_v1_5.json",
                            register="honest_residuals_register_v0_7.json", redrafts="r1/R1_redrafts_v1_6.json")
    meta["fences"] = m5["fences"].replace("honest_residuals_register_v0_6.json", "honest_residuals_register_v0_7.json")
    out = (json.dumps({"meta": meta, "entries": entries}, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
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
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), md5b(out)))
    print("  re-ruled and reclassified %d | class %s | quotes %d verbatim | validator v0_6 --assembly: %d checks, all PASS"
          % (len(record), json.dumps(cc, sort_keys=True), len(quotes_all),
             len([l_ for l_ in lines if l_.startswith(("PASS", "FAIL", "WARN"))])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
