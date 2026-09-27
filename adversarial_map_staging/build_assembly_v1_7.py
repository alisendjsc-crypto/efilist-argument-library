#!/usr/bin/env python3
"""Build adversarial_map_v1_7.json -- the successor map over the v4.1.3 and v4.1.5 cuts (L7, 2026-09-26, R0223).

  i.   It reads the ruled map v1_6 (frozen: never edited, never re-pinned) and applies r1/L7_successor_drafts.json.
       v1_6 stays byte-identical. The successor is pinned to the corpus it reads, 7b6e65e5 (v4.1.5).
  ii.  COVERAGE IS CHECKED AGAINST THE MEASURE, NOT ASSUMED. r1/l7_measure_v0_1.json lists every anchor that moved
       or went, every anchor left at a moved locus, every (a) routed to a moved locus and every passage quoting a
       repaired sentence. Each must have exactly one row; an entry whose anchor went must have its anchor set; a
       passage whose quoted words are gone from the locus must have that field rewritten. The six waiting (a)s (v1_6
       (a)s whose current R1 row is FAILS) must each have a re-judgment row.
  iii. AUTHORITY: a row names a v1_6 entry by index, target and anchor, and all three must agree. A (d)'s
       bedrock_name ("@from") is copied from the registered (d) its row names by locus AND anchor, and register v0_7
       must file that (d) under the HR-id and facet the row claims (L4's law).
  iv.  QUOTES: every declared quotation is checked verbatim at its source (corpus: the v4.1.5 locus; v1_6: any field
       of any v1_6 entry at that locus), and every double-quoted span in a changed or filed field must be declared.
  v.   Every entry no row changes carries over byte for byte. A changed entry records its prior values in
       provenance.successor_L7; a filed entry is phase H. The validator v0_7 runs in-process under --assembly
       against the v4.1.5 corpus; the build refuses on any violation or advisory.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import collections, copy, hashlib, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_7.json")

sys.path.insert(0, STAGE)
sys.path.insert(0, os.path.join(STAGE, "r1"))
import adv_map_validator_v0_7 as V   # noqa: E402  -- import the instrument, never reimplement it
import pinned                        # noqa: E402

S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
PIN = {
    "base": (S + "/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "drafts": (R + "/L7_successor_drafts.json", "fd9267f853a5a09fe5aa3972b16fa2a7"),
    "measure": (R + "/l7_measure_v0_1.json", "4d98b4a3b5c3a57ef62543001ba7ff64"),
    "register": (S + "/honest_residuals_register_v0_7.json", "bcbff23113f3fb0135d5fd5b3e2630d5"),
    "rulings": (R + "/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74"),
    "evidence": (R + "/R1_evidence_2026-09-19.json", "719b5ddb27680f32181a8a953c84b6c2"),
}
VALIDATOR_MD5 = "8a74dcc452338f127ec03e078090c2ed"
CORPUS = "efilist_argument_library_v4_0_0.json"
CORPUS_PIN = "7b6e65e531018fecb37baf2a4fedd6d1"
PHASES = ("A", "B1", "B2", "C", "D", "E", "R", "F", "G", "H")
FIELDS = ("class", "target_anchor", "adversarial_move", "grounds", "routing")
BY = "library seat, Code (L7, on Josiah's word to LD3); drafter under K258, judges nothing"
DATE = "2026-09-26"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def main():
    fail = []
    vraw = open(os.path.join(STAGE, "adv_map_validator_v0_7.py"), "rb").read()
    assert md5b(vraw) == VALIDATOR_MD5, "VALIDATOR GUARD: v0_7 is %s" % md5b(vraw)
    raw = {}
    for k, (rel, m) in PIN.items():
        try:
            raw[k] = pinned.bytes_at(REPO, rel, m)
        except LookupError as err:
            print("BASE GUARD: %s" % err)
            return 1
    base = json.loads(raw["base"].decode("utf-8"))
    drafts = json.loads(raw["drafts"].decode("utf-8"))
    measure = json.loads(raw["measure"].decode("utf-8"))
    register = json.loads(raw["register"].decode("utf-8"))
    rulings = json.loads(raw["rulings"].decode("utf-8"))["rows"]
    evidence = json.loads(raw["evidence"].decode("utf-8"))["entries"]
    cpath = pinned.path_at(REPO, CORPUS, CORPUS_PIN)
    corpus = json.loads(open(cpath, "rb").read().decode("utf-8"))
    nodes = {o["id"]: o for o in corpus["objections"]}
    if measure["pinned"]["map"]["md5"] != PIN["base"][1] or measure["pinned"]["corpus_post"]["md5"] != CORPUS_PIN:
        fail.append("MEASURE: the record does not measure v1_6 against 7b6e65e5")

    sup = {r["supersedes"] for r in drafts["rows"] if r.get("supersedes")}
    rows = [r for r in drafts["rows"] if r["id"] not in sup]
    entries = [copy.deepcopy(e) for e in base["entries"]]
    ev = {(e["target_id"], e["target_locus"], e["target_anchor"]): e["n"] for e in evidence}
    rsup = {r["supersedes"] for r in rulings if r.get("supersedes")}
    current = {r["n"]: r for r in rulings if r["row"] not in rsup}
    trib = {}
    for b in register["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                trib[(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], f["facet_id"])

    # ---- authority: every entry-naming row names a real v1_6 entry, once ----
    by_entry = collections.defaultdict(list)
    for r in rows:
        if r["kind"] in ("amend", "stands"):
            x = r["entry"]
            i = x["i"]
            e = base["entries"][i] if 0 <= i < len(base["entries"]) else None
            if e is None or "%s#%s" % (e["target_id"], e["target_locus"]) != x["target"] \
                    or e["target_anchor"] != x["anchor"]:
                fail.append("%s: entry %d is not %s / %r in v1_6" % (r["id"], i, x["target"], x["anchor"][:40]))
                continue
            if x.get("n") != ev.get((e["target_id"], e["target_locus"], e["target_anchor"])):
                fail.append("%s: entry %d's #n is not %r" % (r["id"], i, x.get("n")))
            by_entry[i].append(r)
    for i, rs in by_entry.items():
        if len(rs) != 1:
            fail.append("entry %d has %d rows: %s" % (i, len(rs), [r["id"] for r in rs]))

    # ---- coverage, against the measure ----
    def row_for(i):
        return (by_entry.get(i) or [None])[0]
    for x in measure["entries"]:
        r = row_for(x["i"])
        if x["status"] == "gone":
            if r is None or r["kind"] != "amend" or "target_anchor" not in r.get("set", {}):
                fail.append("COVERAGE: entry %d's anchor is gone and no row sets a new one" % x["i"])
        elif x["status"] == "moved" or x.get("survives_outside"):
            if r is None:
                fail.append("COVERAGE: entry %d (%s at a moved locus) has no row" % (x["i"], x["status"]))
    for x in measure["routes"]:
        if row_for(x["i"]) is None:
            fail.append("COVERAGE: entry %d routes to moved %s and has no row" % (x["i"], x["answered_by"]))
    fieldmap = {"adversarial_move": "adversarial_move", "grounds": "grounds",
                "bedrock_name": "routing", "terminus_routing": "routing"}
    for x in measure["quotes"]:
        r = row_for(x["i"])
        if r is None:
            fail.append("COVERAGE: entry %d quotes %s and has no row" % (x["i"], x["quotes_from"]))
        elif x["still_verbatim_post"] < x["shingles"] and fieldmap[x["field"]] not in r.get("set", {}):
            fail.append("COVERAGE: entry %d's %s quotes words gone from %s, and its row does not rewrite it"
                        % (x["i"], x["field"], x["quotes_from"]))
    for i, e in enumerate(base["entries"]):
        n = ev.get((e["target_id"], e["target_locus"], e["target_anchor"]))
        if e["class"] == "a" and n in current and current[n]["verdict"] == "FAILS":
            r = row_for(i)
            if r is None or r["disposition"] != "rejudge_waiting":
                fail.append("COVERAGE: waiting (a) #%d (entry %d) has no re-judgment row" % (n, i))

    # ---- bedrock_from: copied, never typed ----
    def resolve_from(r, routing):
        bf = r.get("bedrock_from")
        rs = routing.get("residue") if isinstance(routing, dict) else None
        if not rs or rs.get("bedrock_name") != "@from":
            return routing
        if not bf:
            fail.append("%s: '@from' with no bedrock_from" % r["id"])
            return routing
        node, _, loc = bf["locus"].partition("#")
        src = [y for y in base["entries"] if y["target_id"] == node and y["target_locus"] == loc
               and y["target_anchor"] == bf["anchor"] and y["class"] == "d"]
        if len(src) != 1:
            fail.append("%s: bedrock_from names %d (d)s in v1_6" % (r["id"], len(src)))
            return routing
        if trib.get((node, loc, bf["anchor"])) != (bf["hr"], bf["facet"]):
            fail.append("%s: register v0_7 does not file bedrock_from under %s/%s" % (r["id"], bf["hr"], bf["facet"]))
        out = copy.deepcopy(routing)
        out["residue"]["bedrock_name"] = src[0]["routing"]["residue"]["bedrock_name"]
        return out

    # ---- quotes ----
    def pool(src):
        kind, _, rest = src.partition(":")
        node, _, loc = rest.partition("#")
        if kind == "corpus":
            if node not in nodes or not V.locus_valid(nodes[node], loc) and loc not in ("trigger",):
                raise KeyError("no corpus locus %s" % rest)
            return [V.locus_text(nodes[node], loc) if loc != "trigger" else nodes[node].get("trigger", "")]
        if kind == "v1_6":
            xs = [y for y in base["entries"] if y["target_id"] == node and y["target_locus"] == loc]
            if not xs:
                raise KeyError("no v1_6 entry at %s" % rest)
            return [s for y in xs for s in strings({k: y[k] for k in FIELDS})]
        raise KeyError("unknown source kind %r" % kind)
    nq = 0
    for r in rows:
        declared = []
        for q in r.get("quotes", []):
            nq += 1
            try:
                ok = any(q["quote"] in t for t in pool(q["src"]))
            except KeyError as err:
                fail.append("%s: quote source %s -- %s" % (r["id"], q["src"], err))
                continue
            if not ok:
                fail.append("%s: NOT VERBATIM at %s: %r" % (r["id"], q["src"], q["quote"][:80]))
            declared.append(q["quote"])
        changed = dict(r.get("set", {}))
        changed.update(r.get("new_entry", {}))
        for fld in ("adversarial_move", "grounds", "routing"):
            for s in strings(changed.get(fld, "")):
                for span in re.findall(r'"([^"]+)"', s):
                    if span not in declared:
                        fail.append("%s: undeclared quotation in %s: %r" % (r["id"], fld, span[:60]))

    # ---- apply ----
    changed_i, record = {}, []
    for r in rows:
        if r["kind"] == "amend":
            i = r["entry"]["i"]
            e = entries[i]
            new = dict(r["set"])
            if "routing" in new:
                new["routing"] = resolve_from(r, new["routing"])
            frm = {k: copy.deepcopy(e[k]) for k in new if k in FIELDS}
            unknown = [k for k in new if k not in FIELDS]
            if unknown:
                fail.append("%s: sets unknown fields %s" % (r["id"], unknown))
            for k in FIELDS:
                if k in new:
                    e[k] = new[k]
            sl = {"at": "L7", "date": DATE, "by": BY, "row": r["id"], "disposition": r["disposition"],
                  "cause": r["cause"], "fields_changed": [k for k in FIELDS if k in new], "from": frm,
                  "base": {"artifact": "adversarial_map_v1_6.json", "md5": PIN["base"][1]}}
            if r.get("bedrock_from"):
                sl["bedrock_from"] = r["bedrock_from"]
            if r.get("proposed_r1"):
                sl["proposed_r1"] = r["proposed_r1"]
            e["provenance"] = dict(e["provenance"], successor_L7=sl)
            changed_i[i] = r["id"]
            record.append({"row": r["id"], "i": i, "target": r["entry"]["target"], "disposition": r["disposition"],
                           "class": "%s -> %s" % (frm.get("class", e["class"]), e["class"])})
    filed = []
    for r in rows:
        if r["kind"] == "file":
            ne = dict(r["new_entry"])
            ne["routing"] = resolve_from(r, ne["routing"])
            e = {"target_id": ne["target_id"], "target_locus": ne["target_locus"], "target_anchor": ne["target_anchor"],
                 "adversarial_move": ne["adversarial_move"], "class": ne["class"], "grounds": ne["grounds"],
                 "routing": ne["routing"], "status": "mapped",
                 "provenance": {"phase": "H", "date": DATE, "seat": BY,
                                "filed": {"row": r["id"], "findings": r.get("finding", []), "cause": r["cause"]}}}
            if r.get("bedrock_from"):
                e["provenance"]["filed"]["bedrock_from"] = r["bedrock_from"]
            if r.get("source"):
                e["provenance"]["filed"]["source"] = r["source"]
            filed.append(e)
            record.append({"row": r["id"], "i": len(entries) + len(filed) - 1,
                           "target": "%s#%s" % (e["target_id"], e["target_locus"]),
                           "disposition": r["disposition"], "class": "new -> %s" % e["class"]})
    entries += filed
    for i, e in enumerate(base["entries"]):
        if i not in changed_i and entries[i] != e:
            fail.append("entry %d moved without a row" % i)
    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1

    # ---- meta ----
    m6 = base["meta"]
    cc = dict(collections.Counter(e["class"] for e in entries))
    per_phase = {ph: dict(collections.Counter(e["class"] for e in entries if e["provenance"]["phase"] == ph))
                 for ph in PHASES}
    tiers = {o["id"]: o["tier"] for o in corpus["objections"]}
    per_tier = {}
    for t in sorted(set(tiers.values())):
        sub = [e for e in entries if tiers[e["target_id"]] == t]
        per_tier["T%d" % t] = {"nodes": len(set(e["target_id"] for e in sub)), "entries": len(sub),
                               **dict(collections.Counter(e["class"] for e in sub))}
    prim = collections.Counter(e["target_locus"] for e in entries if e["target_locus"] in V.LOCI)
    var = [e for e in entries if V.variant_slot(e["target_locus"])]
    notes = [e for e in entries if e["target_locus"] == V.NOTE_LOCUS]
    kinds = collections.Counter((r["kind"], r["disposition"]) for r in rows)
    proposals = [{"row": r["id"], "n": r["entry"]["n"], "target": r["entry"]["target"], **r["proposed_r1"]}
                 for r in rows if r.get("proposed_r1")]
    meta = {}
    for k, v in m6.items():
        meta[k] = v
        if k == "r1_rerulings":
            meta["l7_successor"] = {
                "what": ("The successor over the v4.1.3 (L5) and v4.1.5 (L6) content cuts. The ruled map v1_6 is frozen "
                         "and stays pinned to 04bf6482; this file reads 7b6e65e5. Every entry the measure touched was read; "
                         "every change names its cause; the rest carry byte for byte."),
                "his_word": drafts["his_word"],
                "drafts": {"file": PIN["drafts"][0], "md5": PIN["drafts"][1], "rows": len(rows)},
                "measure": {"file": PIN["measure"][0], "md5": PIN["measure"][1]},
                "by_kind": {"%s/%s" % k: v for k, v in sorted(kinds.items())},
                "entries_changed": len(changed_i), "entries_filed": len(filed),
                "entries_carried_byte_for_byte": len(base["entries"]) - len(changed_i),
                "proposed_r1_rows": proposals,
                "as_written": ("L7's drafts. A seat that did not draft them judges them (K258, the gate2 role); whether "
                               "they are judged, and how, is recorded in canon, never here. No R1 row is written by this "
                               "file: a proposed verdict waits for gate2's judgment and his word."),
                "rows": record}
    meta["artifact"] = "adversarial_map_v1_7.json"
    meta["assembled"] = "2026-09-26, efilist Code seat, L7 (the successor map over the v4.1.3 and v4.1.5 cuts)"
    meta["successor_to"] = dict(m6["successor_to"], artifact="adversarial_map_v1_6.json", md5=PIN["base"][1],
                                bytes=len(raw["base"]),
                                and_before_it="adversarial_map_v1_5.json 0df413ed655a5373468c218832854bbe, and before it "
                                              + m6["successor_to"]["and_before_it"],
                                why_v1_7=("A revision of the same map over a re-cut corpus, as v1_1 was over v4.1.0: the "
                                          "entries the two cuts reached are re-read and, where their text moved, "
                                          "adjudicated afresh; findings of the two pin sessions are filed; the schema is "
                                          "unchanged."))
    for k in ("why_v1_6", "v1_5_is_not_replaced"):
        meta["successor_to"].pop(k, None)
    meta["successor_to"]["v1_6_is_not_replaced"] = ("v1_6 stays byte-identical on disk and stays pinned to 04bf6482: "
                                                    "gate2's v1_6 judgment and the pin-session records pin it.")
    meta["source_corpus_md5"] = CORPUS_PIN
    meta["source_corpus_objections_md5"] = V.objections_digest(corpus)
    meta["corpus_note"] = ("v4.1.5, the corpus after the L5 cut (v4.1.3, 23 rows) and the L6 cut (v4.1.5, 20 rows); "
                           "v4.1.4 moved page design only. The digest is the validator's own objections_digest (K344).")
    meta["entries"] = len(entries)
    meta["nodes_covered"] = len(set(e["target_id"] for e in entries if e["target_locus"] != V.NOTE_LOCUS))
    meta["coverage_distinct_ids"] = len(set(e["target_id"] for e in entries))
    meta["variant_coverage"] = "%d/%d" % (len({(e["target_id"], e["target_locus"]) for e in var}),
                                          sum(len(V.node_variant_slots(o)) for o in corpus["objections"]))
    meta["note_coverage"] = "%d/%d" % (len({(e["target_id"], e["target_locus"]) for e in notes}),
                                       sum(1 for o in corpus["objections"] if V.node_has_note(o)))
    meta["class_counts"] = cc
    meta["per_phase"] = per_phase
    meta["per_tier"] = per_tier
    meta["locus_distribution"] = {"primary": dict(sorted(prim.items())), "variant_entries": len(var),
                                  "variant_loci_carrying_entries": len({(e["target_id"], e["target_locus"]) for e in var}),
                                  "note_entries": len(notes),
                                  "note_loci_carrying_entries": len({(e["target_id"], e["target_locus"]) for e in notes}),
                                  "shape_entries": 0}
    meta["entry_caps"] = dict(m6["entry_caps"], per_node=(
        "<=3 + 3*(variant loci) + 3*(argumentShapes loci) on that node. K348 (Josiah) for variants; extended to "
        "shape loci at validator v0_7 (L7), one locus kind over. The corpus carries no shapes yet, so no node's "
        "bound moves here."))
    meta["validation"] = ("validator v0_7 under --assembly against the v4.1.5 corpus, in-process at build: 0 violations "
                          "AND 0 advisories, or this file is not written.")
    meta["siblings"] = dict(m6["siblings"], predecessor="adversarial_map_v1_6.json",
                            register="honest_residuals_register_v0_8.json", drafts="r1/L7_successor_drafts.json",
                            measure="r1/l7_measure_v0_1.json")
    meta["fences"] = m6["fences"].replace("honest_residuals_register_v0_7.json", "honest_residuals_register_v0_8.json")
    out = (json.dumps({"meta": meta, "entries": entries}, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    open(tmp, "wb").write(out)
    lines = []
    passed, viol, adv = V.validate([tmp], cpath, assembly=True, out=lines.append)
    if not passed or viol or adv:
        print("REFUSING TO WRITE -- validator v0_7 --assembly: %d violation(s), %d advisory(ies)" % (len(viol), len(adv)))
        for v in (viol + adv)[:30]:
            print("  " + v)
        os.remove(tmp)
        return 1
    os.replace(tmp, OUT)
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), md5b(out)))
    print("  changed %d, filed %d, carried %d | class %s | quotes %d verbatim | validator v0_7 --assembly: %d checks, all PASS"
          % (len(changed_i), len(filed), len(base["entries"]) - len(changed_i), json.dumps(cc, sort_keys=True), nq,
             len([l_ for l_ in lines if l_.startswith(("PASS", "FAIL", "WARN"))])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
