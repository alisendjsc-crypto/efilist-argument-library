#!/usr/bin/env python3
"""project_canon_v38_38.json -- MINOR. gate2's judgment of L6's X-032 safety pass (R0207): nine drafts, four proposed
companions, seven proposed widening rows, ten findings and the knock-on.

ccclxiv FIRST: v38_37 is round-tripped at the serialization this file emits BEFORE anything is derived; it is read at
its md5 from the working tree or git history, so this builder runs after the rename removes it.

MINOR: keyset held at 42; every top-level key this build does not name byte-identical; inside adversarial_map one
subkey is ADDED and none moves. In-process: the rulings gate, the quote check, gate2's five earlier judgment gates and
the new one GREEN; L6's drafts gate GREEN; the new gate's control record all-as-expected and naming the gate and record
it pins; gate2's reading record reproduces.

  python3 tools/build_canon_v38_38.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_37.json", "39295a2d9199c1b391700107e521009d"
OUT = os.path.join(OUT_DIR, "project_canon_v38_38.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "gate2", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["safety_pass_judgment_gate2"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

REC, GATE, CTL = R1 + "SP_drafts_judgments.json", R1 + "sp_judgments_gate.py", R1 + "sp_judgments_gate_control_v0_1.json"
READER, READING = R1 + "sp_judgment_reading.py", R1 + "sp_judgment_reading_v0_1.json"
DRAFTS, DGATE = R1 + "SP_drafts_L6.json", R1 + "sp_drafts_gate_l6.py"
EARLIER = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
           (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
           (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json"),
           (R1 + "pq_repair_judgments_gate.py", R1 + "PQ_repair_drafts_judgments.json"),
           (R1 + "pq_repair_redrafts_gate.py", R1 + "PQ_repair_redrafts_judgments.json")]
KICKOFF = {"relay": "R0207", "md5": "7948020d5dbcfaf2cc52af02ed1f44a1"}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_37 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- every gate, in-process
    G = mod(R1 + "r1_rulings_gate.py", "r1rg")
    fails, _ = G.check(os.path.join(REPO, R1 + "R1_rulings.json"), REPO, G.committed_base())
    assert not fails, "RULINGS GATE RED: %s" % fails
    Q = mod(R1 + "r1_quote_check.py", "r1qc")
    q_rows = Q.rulings_quotes()
    q_ok, q_fail = Q.check(q_rows, Q.Texts())
    assert not q_fail and q_ok == len(q_rows), "QUOTE CHECK RED: %s" % q_fail
    for i, (gate, rec_rel) in enumerate(EARLIER):
        M = mod(gate, "g%d" % i)
        fl, _ = M.check(os.path.join(REPO, rec_rel), REPO, M.committed_base())
        assert not fl, "%s RED: %s" % (gate, fl)
    DG = mod(DGATE, "spdg")
    drafts = json.load(open(os.path.join(REPO, DRAFTS), encoding="utf-8"))
    dfails, _ = DG.check(drafts, DG.committed_base())
    assert not dfails, "L6 DRAFTS GATE RED: %s" % dfails
    JG = mod(GATE, "spjg")
    jfails, _ = JG.check(os.path.join(REPO, REC), REPO, JG.committed_base())
    assert not jfails, "SP JUDGMENTS GATE RED: %s" % jfails
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and c["all_as_expected"] and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["judgments_md5"] == f(REC)["md5"], "the control record is stale"
    RD = mod(READER, "sprd")
    fresh = (json.dumps(RD.measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    assert fresh == open(os.path.join(REPO, READING), "rb").read(), "the reading record does not reproduce"
    rd = json.loads(fresh.decode("utf-8"))

    # ---------------------------------------------------------------- the judgment, measured
    rec = json.load(open(os.path.join(REPO, REC), encoding="utf-8"))
    assert rec["kickoff"] == KICKOFF
    rows = rec["rows"]
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["id"] not in sup]
    tally = collections.defaultdict(collections.Counter)
    for r in cur:
        if r["kind"] != "finding":
            tally[r["kind"]][r["verdict"]] += 1
    tally = {k: dict(sorted(v.items())) for k, v in sorted(tally.items())}
    assert tally == {"companion": {"ACCEPT": 4}, "draft": {"ACCEPT": 8, "AMEND": 1}, "finding_review": {"CONFIRM": 10},
                     "knock_on": {"CONFIRM": 1}, "widening": {"ACCEPT": 7}}, tally
    amends = [{"judgment": r["id"], "row": r["row_id"], "locus": r["locus"], "owed": r["owed"]}
              for r in cur if r.get("verdict") == "AMEND"]
    leans = {r["row_id"]: r["lean"] for r in cur if r["kind"] in ("companion", "widening")}
    finds = [{"judgment": r["id"], "title": r["title"], "whose": r["whose"], "recommendation": r["recommendation"]}
             for r in cur if r["kind"] == "finding"]
    assert rd["exit_patterns"]["after_every_row"]["hits"] == 0 and rd["dashes"]["rows_bringing_the_other_style"] == ["SD-02"]

    # ---------------------------------------------------------------- the block
    am["safety_pass_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's judgment of L6's X-032 safety pass. His word decides the companions and the "
                  "widening, which go past the six; nothing is served on a judgment.",
        "judge": "gate2, which drafted none of the pass (K258). X-032 and its lean are gate2's own, and the drafts carry "
                 "them out; Z-035 records the pull and the two alternatives tested on the text.",
        "kickoff": KICKOFF,
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE, control=dict(
            f(CTL), file=CTL, result="%d of %d as expected, the unmutated control first; byte-identical under two "
                                     "forced hash seeds" % (len(c["controls"]), len(c["controls"])))),
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": tally,
        "amend": amends,
        "leans": leans,
        "measured": {"x032_patterns": "%d hits at the six before; %d after every row" % (
            rd["exit_patterns"]["before"]["hits"], rd["exit_patterns"]["after_every_row"]["hits"]),
            "dashes": "one row brings the other em-dash style into its slot: SD-02",
            "honest_evaluation_phrasing_after": sorted({h["locus"] for h in rd["honest_evaluation_phrasing"]["after_every_row"]}),
            "knock_on": "#3 and #56 stand; #44's anchor survives; #47's moves"},
        "findings": finds,
        "for_his_word": [
            {"ask": "Ratify SD-01..09 for the v4.1.5 pin: eight as judged, and SD-02 once L6's superseding row makes the "
                    "owed dash change and gate2 accepts it.",
             "lean_L6": "yes",
             "lean_gate2": "yes; and give the word now, on the condition that gate2 accepts SD-02's one-character fix, "
                           "so the pin does not wait on you twice"},
            {"ask": "Admit the four companions at revealed-preference (SC-01..04).",
             "lean_L6": "yes", "lean_gate2": "yes: the same framing one slot away, and SC-01..03 are the map's own repair"},
            {"ask": "Widen the pass to survivor-testimony (SW-01..06).",
             "lean_L6": "yes",
             "lean_gate2": "yes: its long read a survivor's recovery as bias, the most dangerous passage the sweep found"},
            {"ask": "Take SW-07: the lethality rate for a named site goes; the bridge's name stays where the objection "
                    "states itself.",
             "lean_L6": "yes", "lean_gate2": "yes; removing the name too is yours to ask for, and the seat's lean is to keep it"},
            {"ask": "Carry survivor-testimony's mechanism label (SF-05) to the next pin that regenerates the Mechanism "
                    "Web sidecar.",
             "lean_L6": "yes", "lean_gate2": "yes"},
        ],
        "next": "L6 appends a superseding row for SD-02 (the slot's unspaced em dash) and relays it; gate2 judges that one "
                "row. His word, which L6 records with one ratification row naming exactly what he ratifies and admits; "
                "then the v4.1.5 pin (a content cut) with tools/pin_patch_l6.py --apply --set ratified, a re-vendor notice "
                "to argue, and the successor map. Canon writing passes back to L6.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.38"
    d["canon_version_marker"] = "v38.38"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("L6 (the X-032 safety pass) appends SD-02's owed dash fix; gate2 judges it; his word on the five asks "
                      "(adversarial_map.safety_pass_judgment_gate2.for_his_word); then the v4.1.5 pin, a content cut, and "
                      "the successor map, which also takes X-033's sibling loci, PF-01..03, Z-033's honest-evaluation "
                      "phrasing and SF-05's label. Then adversarial wing v2 and /llms.txt, R2, and the interconnection "
                      "design.")
    nrs["judged_safety_pass_gate2"] = (
        "gate2 judged the X-032 safety pass: %s. Judged is not ruled."
        % "; ".join("%s %s" % (k, ", ".join("%s %d" % kv for kv in v.items())) for k, v in tally.items()))

    d["keyset_delta_ledger"]["v38_38_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (safety_pass_judgment_gate2); "
        "next_recommended_session re-pointed (session rewritten; judged_safety_pass_gate2 added); canon-meta; this note; "
        "one session_log_recent append. NO PIN. Every other top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): L6's X-032 safety pass judged (R0207). Record %s: SD-01, SD-03..09 ACCEPT; SD-02 AMEND (the "
        "slot's unspaced em dash); SC-01..04 and SW-01..07 ACCEPT, lean admit; SF-01..10 CONFIRM; knock-on CONFIRM. "
        "Found: X-032's own patterns were a floor (the framing stood at six more slots); the honest-evaluation phrasing "
        "survives at boonin-critique, about procreation intuitions, for the successor map. Judged, not ruled."
        % (DATE, f(REC)["md5"][:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-1:] == ADDED and set(am) - set(am_before) == set(ADDED)
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"
    open(OUT, "wb").write(out)
    print("project_canon_v38_38.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s" % (f(REC)["md5"][:8], json.dumps(tally, sort_keys=True)))


if __name__ == "__main__":
    main()
