#!/usr/bin/env python3
"""project_canon_v38_46.json -- MINOR. gate2's second judgment of L7's successor map (R0245): the 18 rows L7 appended after
gate2's first judgment, map v1_8, register v0_9, the knock-on control, the controls_v1_7 change and the U-065 route. All 18
ACCEPT; the rest CONFIRM; R0244's condition is met. Judged, not ruled.

ccclxiv FIRST: v38_45 is round-tripped at the serialization this file emits BEFORE anything is derived; it is read at
its md5 from the working tree or git history, so this builder runs after the rename removes it. MINOR: keyset 42; one
adversarial_map subkey added. In-process: the rulings gate, the quote check, gate2's eight earlier judgment gates and the
new one GREEN (the new one with no committed base, so a rebuild after the commit writes the same bytes); the new gate's
control record all-as-expected and fresh; both of gate2's L7 readings reproduce.

  python3 tools/build_canon_v38_46.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_45.json", "725f2a4a7ed160179a37f2ea11965392"
OUT = os.path.join(OUT_DIR, "project_canon_v38_46.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "gate2", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["successor_redrafts_judgment_gate2"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

REC, GATE, CTL = R1 + "L7_successor_redrafts_judgments.json", R1 + "l7_redrafts_gate.py", R1 + "l7_redrafts_gate_control_v0_1.json"
READER, READING = R1 + "l7_redraft_reading.py", R1 + "l7_redraft_reading_v0_1.json"
READER1, READING1 = R1 + "l7_judgment_reading.py", R1 + "l7_judgment_reading_v0_1.json"
DRAFTS = R1 + "L7_successor_drafts.json"
EARLIER = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
           (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
           (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json"),
           (R1 + "pq_repair_judgments_gate.py", R1 + "PQ_repair_drafts_judgments.json"),
           (R1 + "pq_repair_redrafts_gate.py", R1 + "PQ_repair_redrafts_judgments.json"),
           (R1 + "sp_judgments_gate.py", R1 + "SP_drafts_judgments.json"),
           (R1 + "sp_redrafts_gate.py", R1 + "SP_redrafts_judgments.json"),
           (R1 + "l7_judgments_gate.py", R1 + "L7_successor_drafts_judgments.json")]
KICKOFF = {"relay": "R0245", "md5": "7ecc0659301d2bb21fee4e6dde7ee4dc"}


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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_45 does not round-trip"
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
    JG = mod(GATE, "l7rg")
    jfails, _ = JG.check(os.path.join(REPO, REC), REPO, None)
    assert not jfails, "L7 REDRAFTS GATE RED: %s" % jfails
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and c["all_as_expected"] and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["judgments_md5"] == f(REC)["md5"], "the control record is stale"
    for reader, reading in ((READER1, READING1), (READER, READING)):
        RD = mod(reader, os.path.basename(reader)[:-3] + "_b")
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
    assert tally == {"artifact": {"CONFIRM": 2}, "knock_on": {"STANDS": 6}, "measure": {"CONFIRM": 1},
                     "redraft": {"ACCEPT": 18}, "route": {"CONFIRM": 1}, "tool": {"CONFIRM": 1}}, tally
    assert rd["coverage"]["equal"] and not rd["derivation"]["failures"] and not rd["move_register"]["new_moves_with_history_wording"]


    am["successor_redrafts_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's second judgment of L7's successor map: all 18 redrafts ACCEPT; map v1_8, "
                  "register v0_9, the knock-on control and the controls_v1_7 change CONFIRM; the U-065 route CONFIRM with two "
                  "conditions for when it is built. R0244's condition is met. Nothing ships on a judgment.",
        "judge": "gate2, which drafted none of SM-52..SM-69, v1_8, v0_9, their builders or controls (K258); SM-69 carries "
                 "gate2's own U-045 lean (U2-032 records the pull)",
        "kickoff": KICKOFF,
        "answers": {"record": dict(f(R1 + "L7_successor_drafts_judgments.json"), file=R1 + "L7_successor_drafts_judgments.json"),
                    "canon_block": "adversarial_map.successor_drafts_judgment_gate2"},
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE, control=dict(
            f(CTL), file=CTL, result="%d of %d as expected, the unmutated control first; byte-identical under two forced "
                                     "hash seeds" % (len(c["controls"]), len(c["controls"])))),
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": {k: dict(v) for k, v in sorted(tally.items())},
        "reproduced": {"coverage": rd["coverage"]["equal"], "derivation": {k: rd["derivation"][k] for k in (
            "carried_byte_for_byte", "changed", "class_counts_v1_8")},
                       "history_wording_in_new_moves": len(rd["move_register"]["new_moves_with_history_wording"]),
                       "quotes_verbatim": "%d of %d" % (rd["quotes"]["verbatim"], rd["quotes"]["declared"]),
                       "bedrock_copies_hold": all(b["name_copied_equal"] and b["v0_8_files_the_source_there"]
                                                  and b["v0_9_files_the_entry_there"] for b in rd["bedrock"]),
                       "register": rd["register"], "validator_v0_7_assembly_on_v1_8": rd["validator"]["v0_7_assembly_on_v1_8"]},
        "knock_on": {"by_entry": rd["knock_on"]["newly_collided_by_lineage"],
                     "by_entry_and_class": rd["knock_on"]["by_lineage_and_class"],
                     "the_control": rd["knock_on"]["the_controls_record_lists"],
                     "correction": "U-064's count of 9 keyed by entry and missed six class changes; the control's 12 is "
                                   "right; the three not named in round one (#3, #4, #52) were read here and stand (U2-030)"},
        "u065_route_conditions": [r["carries"] for r in cur if r["kind"] == "route"][0],
        "r0244_condition": "met: all 18 redrafts accepted",
        "next": "His word on R0244's four asks; then L7 writes the R1 rows (#11, #22, #32, #50, and n=70 through the "
                "evidence addendum on U2-023's conditions) and closes. Canon passes back to L7.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.46"
    d["canon_version_marker"] = "v38.46"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.5. gate2 judged L7's 18 redrafts (adversarial_map.successor_redrafts_judgment_gate2): all "
                      "ACCEPT; v1_8 and register v0_9 CONFIRM; R0244's condition is met. Next: his word on R0244's four asks; "
                      "then L7 closes: the R1 rows he rules (#11, #22, #32, #50, and the new (a) at self-defeating#long through "
                      "the evidence addendum, on U2-023's two conditions), canon records his word, and the /adversarial/ tab "
                      "icon is wired if he does not object. Beside it: V2 drafts the pilot's shapes (R-V4); argue re-vendors "
                      "v4.1.5 (R0222). After: the next queue (successor_carries_L7_round2 and carries_L7), adversarial wing v2 "
                      "and /llms.txt, R2, the interconnection design, and the new-objection intake (R-V6) once the pilot is "
                      "judged.")
    nrs["judged_successor_redrafts_gate2"] = ("gate2 judged SM-52..SM-69 (record L7_successor_redrafts_judgments.json, gate "
                                              "l7_redrafts_gate.py): 18 ACCEPT; v1_8, v0_9, the knock-on control, the "
                                              "controls_v1_7 change and the U-065 route CONFIRM. Judged, not ruled.")
    d["keyset_delta_ledger"]["v38_46_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (successor_redrafts_judgment_gate2); "
        "next_recommended_session re-pointed; canon-meta; this note; one session_log_recent append. NO PIN. Every other "
        "top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): L7's 18 redrafts judged (R0245). Record %s: all ACCEPT (16 without the corpus-history wording, "
        "SM-55's hub condition as it stands, SM-69 pressing the diagnosis to HR-02); v1_8, v0_9, the knock-on control (12, "
        "which corrects gate2's own 9) and the controls_v1_7 change CONFIRM; the U-065 route CONFIRM with two conditions. "
        "R0244's condition met; canon back to L7." % (DATE, f(REC)["md5"][:8]))

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
    print("project_canon_v38_46.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s" % (f(REC)["md5"][:8], json.dumps(tally, sort_keys=True)))


if __name__ == "__main__":
    main()
