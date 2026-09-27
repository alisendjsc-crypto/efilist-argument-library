#!/usr/bin/env python3
"""project_canon_v38_40.json -- MINOR. gate2's second judgment of L6's X-032 safety pass (R0210): SD-10, which answers
Z-002 (SD-02's one dash). With it every row his word would ratify or admit has been judged, and his word on R0208, given
on the condition that gate2 accept SD-10, stands unconditional. It is recorded here as he gave it, read at source.

ccclxiv FIRST: v38_39 is round-tripped at the serialization this file emits BEFORE anything is derived; it is read at
its md5 from the working tree or git history, so this builder runs after the rename removes it. MINOR: keyset 42; one
adversarial_map subkey added. In-process: the rulings gate, the quote check, gate2's six earlier judgment gates and the
new one GREEN; L6's drafts gate GREEN; the new gate's control record all-as-expected; both of gate2's safety-pass readings
reproduce.

  python3 tools/build_canon_v38_40.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_39.json", "acc1caaca1eed507405c4e950f3c2059"
OUT = os.path.join(OUT_DIR, "project_canon_v38_40.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "gate2", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["safety_pass_redraft_judgment_gate2"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

REC, GATE, CTL = R1 + "SP_redrafts_judgments.json", R1 + "sp_redrafts_gate.py", R1 + "sp_redrafts_gate_control_v0_1.json"
READER, READING = R1 + "sp_redraft_reading.py", R1 + "sp_redraft_reading_v0_1.json"
READER1, READING1 = R1 + "sp_judgment_reading.py", R1 + "sp_judgment_reading_v0_1.json"
DRAFTS = R1 + "SP_drafts_L6.json"
DGATES = [R1 + "sp_drafts_gate_l6_v0_2.py", R1 + "sp_drafts_gate_l6.py"]   # L6's current gate, and the one gate2 judged
EARLIER = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
           (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
           (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json"),
           (R1 + "pq_repair_judgments_gate.py", R1 + "PQ_repair_drafts_judgments.json"),
           (R1 + "pq_repair_redrafts_gate.py", R1 + "PQ_repair_redrafts_judgments.json"),
           (R1 + "sp_judgments_gate.py", R1 + "SP_drafts_judgments.json")]
KICKOFF = {"relay": "R0210", "md5": "fe30b1b9f6e635974af8d5095e63dd48"}
ASKS = {"relay": "R0208", "md5": "669b6d2fe34acf872fa47f7c758a230c"}


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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_39 does not round-trip"
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
    drafts = json.load(open(os.path.join(REPO, DRAFTS), encoding="utf-8"))
    for i, dgate in enumerate(DGATES):
        DG = mod(dgate, "spdg%d" % i)
        dfails, _ = DG.check(drafts, DG.committed_base())
        assert not dfails, "%s RED: %s" % (dgate, dfails)
    JG = mod(GATE, "spjg")
    jfails, _ = JG.check(os.path.join(REPO, REC), REPO, JG.committed_base())
    assert not jfails, "SP JUDGMENTS GATE RED: %s" % jfails
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and c["all_as_expected"] and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["judgments_md5"] == f(REC)["md5"], "the control record is stale"
    for reader, reading in ((READER1, READING1), (READER, READING)):
        RD = mod(reader, os.path.basename(reader)[:-3])
        fresh = (json.dumps(RD.measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        assert fresh == open(os.path.join(REPO, reading), "rb").read(), "%s does not reproduce" % reading
    rd = json.load(open(os.path.join(REPO, READING), encoding="utf-8"))

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
    assert tally == {"knock_on": {"CONFIRM": 1}, "patch": {"CONFIRM": 1}, "redraft": {"ACCEPT": 1}}, tally
    assert rd["patch"] == {"x032_hits_after_every_row": 0, "rows_mixing_dash_styles": []} and rd["new_rows"] == ["SD-10"]
    dsup = {r.get("supersedes") for r in drafts["rows"] if r.get("supersedes")}
    dcur = [r for r in drafts["rows"] if r["id"] not in dsup]
    ratify = [r["id"] for r in dcur if r["kind"] == "draft" and r["status"] == "declared"]
    admit = [r["id"] for r in dcur if r["kind"] in ("companion", "widening")]
    assert len(ratify) == 9 and "SD-10" in ratify and "SD-02" not in ratify and len(admit) == 11, (ratify, admit)

    am["safety_pass_redraft_judgment_gate2"] = {
        "status": "JUDGED, AND HIS WORD STANDS. gate2's second judgment of the safety pass accepts SD-10, which meets the "
                  "one condition his word carried; every row it ratifies or admits has been judged.",
        "judge": "gate2, which drafted none of SD-10 (K258); the change is the one gate2's own Z-002 owed.",
        "kickoff": KICKOFF,
        "answers": {"record": dict(f(R1 + "SP_drafts_judgments.json"), file=R1 + "SP_drafts_judgments.json"),
                    "canon_block": "adversarial_map.safety_pass_judgment_gate2"},
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE, control=dict(
            f(CTL), file=CTL, result="%d of %d as expected, the unmutated control first; byte-identical under two "
                                     "forced hash seeds" % (len(c["controls"]), len(c["controls"])))),
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": tally,
        "sd10": "ACCEPT: SD-02's replacement with its one spaced em dash made unspaced, as the slot writes its others; "
                "nothing else moved (reading record, diff).",
        "the_text_his_word_ratifies": {"drafts": ratify, "companions_and_widening": admit,
                                           "drafts_record": dict(f(DRAFTS), file=DRAFTS)},
        "his_word": {
            "verbatim": "yes to all",
            "given": "2026-09-26, in chat to L6 (session local_e2a20571); 20:56 MST as L6 reports it",
            "answering": "R0208's five asks as L6 put them to him, each with both seats' lean yes, and conditional on gate2 "
                         "accepting SD-10",
            "asks": dict(ASKS, file="~/Downloads/Claude Code/relays/2026-09-26-gate2-L6-gate2-to-josiah-"
                                    "safety_pass_judged_five_asks-R0208.md"),
            "condition": "met: SD-10 ACCEPT (this record)",
            "read_at_source": "gate2 read his turn in L6's transcript before recording it (K392: a relay points to his "
                              "words, it does not replace them)",
            "what_it_covers": "(1) the nine rewrites, SD-10 standing in for SD-02; (2) SC-01..04; (3) the widening to "
                              "survivor-testimony, SW-01..06; (4) SW-07, the bridge's death rate dropped and its name kept "
                              "where the objection states itself, as R0208's lean; (5) survivor-testimony's mechanism "
                              "label left for the next pin that rebuilds the Mechanism Web",
            "recorded_by": "L6, in one ratification row at the pin; this block records it for the judgment it waited on",
        },
        "next": "L6's ratification row, then the v4.1.5 pin (a content cut), the labels, wuld-ink, and argue's re-vendor "
                "notice. Canon passes back to L6.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.40"
    d["canon_version_marker"] = "v38.40"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("L6: his word on the safety pass ('yes to all', R0208's five asks, unconditional now that SD-10 is "
                      "accepted) goes into one ratification row; then the v4.1.5 pin, a content cut, and the successor map, which also takes X-033's sibling "
                      "loci, PF-01..03, Z-033's honest-evaluation phrasing and SF-05's label. Then adversarial wing v2 and "
                      "/llms.txt, R2, and the interconnection design.")
    nrs["judged_safety_pass_redraft_gate2"] = ("gate2 judged SD-10: ACCEPT. Every row his word ratifies is judged; his word "
                                               "is recorded at adversarial_map.safety_pass_redraft_judgment_gate2.his_word.")
    d["keyset_delta_ledger"]["v38_40_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (safety_pass_redraft_judgment_gate2); "
        "next_recommended_session re-pointed; canon-meta; this note; one session_log_recent append. NO PIN. Every other "
        "top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): SD-10 judged (R0210). Record %s: ACCEPT, the one dash Z-002 owed; knock-on and patch CONFIRM. "
        "His word on R0208, 'yes to all' (20:56, to L6), was conditional on this row and now stands; L6 records the "
        "ratification row at the pin." % (DATE, f(REC)["md5"][:8]))

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
    print("project_canon_v38_40.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s" % (f(REC)["md5"][:8], json.dumps(tally, sort_keys=True)))


if __name__ == "__main__":
    main()
