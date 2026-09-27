#!/usr/bin/env python3
"""project_canon_v38_44.json -- MINOR. gate2's judgment of L7's successor-map drafts (R0237): 51 rows over
adversarial_map_v1_7.json, validator v0_7 and register v0_8, and the knock-on the successor owed. 22 ACCEPT, 11 CONFIRM,
18 AMEND; both artifacts confirmed; nine newly collided (a)s stand. Judged, not ruled: L7 redrafts the 18, a seat that did
not draft them judges the redrafts, then his word.

ccclxiv FIRST: v38_43 is round-tripped at the serialization this file emits BEFORE anything is derived; it is read at
its md5 from the working tree or git history, so this builder runs after the rename removes it. MINOR: keyset 42; one
adversarial_map subkey added. In-process: the rulings gate, the quote check, gate2's seven earlier judgment gates and the
new one GREEN (the new one with no committed base, so a rebuild after the commit writes the same bytes); the new gate's
control record all-as-expected and fresh; the reading instrument reproduces its record.

  python3 tools/build_canon_v38_44.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_43.json", "68733040959dabe6f7b338e5e2e296af"
OUT = os.path.join(OUT_DIR, "project_canon_v38_44.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "gate2", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["successor_drafts_judgment_gate2"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

REC, GATE, CTL = R1 + "L7_successor_drafts_judgments.json", R1 + "l7_judgments_gate.py", R1 + "l7_judgments_gate_control_v0_1.json"
READER, READING = R1 + "l7_judgment_reading.py", R1 + "l7_judgment_reading_v0_1.json"
DRAFTS = R1 + "L7_successor_drafts.json"
EARLIER = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
           (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
           (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json"),
           (R1 + "pq_repair_judgments_gate.py", R1 + "PQ_repair_drafts_judgments.json"),
           (R1 + "pq_repair_redrafts_gate.py", R1 + "PQ_repair_redrafts_judgments.json"),
           (R1 + "sp_judgments_gate.py", R1 + "SP_drafts_judgments.json"),
           (R1 + "sp_redrafts_gate.py", R1 + "SP_redrafts_judgments.json")]
KICKOFF = {"relay": "R0237", "md5": "b0f7e81b55a0bc5da58574680e37b803"}


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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_43 does not round-trip"
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
    JG = mod(GATE, "l7jg")
    jfails, _ = JG.check(os.path.join(REPO, REC), REPO, None)
    assert not jfails, "L7 JUDGMENTS GATE RED: %s" % jfails
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and c["all_as_expected"] and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["judgments_md5"] == f(REC)["md5"], "the control record is stale"
    RD = mod(READER, "l7_judgment_reading_b")
    fresh = (json.dumps(RD.measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    assert fresh == open(os.path.join(REPO, READING), "rb").read(), "the reading record does not reproduce"
    rd = json.load(open(os.path.join(REPO, READING), encoding="utf-8"))

    # ---------------------------------------------------------------- the judgment, measured
    rec = json.load(open(os.path.join(REPO, REC), encoding="utf-8"))
    assert rec["kickoff"] == KICKOFF
    rows = rec["rows"]
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["id"] not in sup]
    of51 = collections.Counter(r["verdict"] for r in cur if r["kind"] in ("amend", "file", "stands", "carry", "relation"))
    arts = collections.Counter(r["verdict"] for r in cur if r["kind"] == "artifact")
    knock = collections.Counter(r["verdict"] for r in cur if r["kind"] == "knock_on")
    assert dict(of51) == {"ACCEPT": 22, "CONFIRM": 11, "AMEND": 18} and dict(arts) == {"CONFIRM": 2} \
        and dict(knock) == {"STANDS": 9}, (of51, arts, knock)
    amend = [r for r in cur if r.get("verdict") == "AMEND"]
    content = {"SM-08": "the move misstates the hub's condition (the typical floor clears a threshold of serious harm "
                        "imposed without consent only if the anti-imposition weight survives; the net-balance route is "
                        "left open)",
               "SM-45": "the move misstates its own anchor paragraph and passes over its diagnosis of stated preference "
                        "(the etiology inference the corpus forbids); the continuation must reach one named bedrock (lean "
                        "HR-02 by parity with SM-48)"}
    reg_only = sorted(r["row_id"] for r in amend if r["row_id"] not in content)
    assert len(reg_only) == 16 and sorted(content) == sorted(r["row_id"] for r in amend if r["row_id"] in content)
    holds = [{"row": r["row_id"], "target": r["target"]} for r in cur if r["kind"] == "amend" and r["r1"] == "HOLDS accepted"]
    dr = {x["id"]: x for x in json.load(open(os.path.join(REPO, DRAFTS), encoding="utf-8"))["rows"]}
    for h in holds:
        x = dr[h["row"]]
        h.update(n=x["entry"]["n"], supersedes=x["proposed_r1"]["supersedes"])
    assert sorted(h["n"] for h in holds) == [11, 22, 32, 50]
    assert [x["target"] for x in rd["new_a_without_r1"]] == ["self-defeating#long"]
    finds = {r["id"]: r["title"] for r in cur if r["kind"] == "finding"}

    am["successor_drafts_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's judgment of L7's successor-map drafts. Every class and terminus holds on the "
                  "v4.1.5 text; 18 rows owe a redraft (16 for corpus-history wording in their moves, SM-08 and SM-45 for "
                  "moves that misstate the text). Nothing ships on a judgment.",
        "judge": "gate2, which drafted none of the drafts record, v1_7, validator v0_7, register v0_8, their builders or the "
                 "measure (K258); it wrote X-033, X-034 and Z-033, which 13 of the rows cite as cause (U-067 records the pull)",
        "kickoff": KICKOFF,
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE, control=dict(
            f(CTL), file=CTL, result="%d of %d as expected, the unmutated control first; byte-identical under two forced "
                                     "hash seeds" % (len(c["controls"]), len(c["controls"])))),
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": {"of_the_51_rows": dict(sorted(of51.items())), "artifacts": dict(arts), "knock_on": dict(knock)},
        "reproduced": {"derivation": {k: rd["derivation"][k] for k in ("carried_byte_for_byte", "changed", "filed",
                                                                        "class_counts_v1_7")},
                       "quotes_verbatim": "%d of %d" % (rd["quotes"]["verbatim"], rd["quotes"]["declared"]),
                       "anchors_present": rd["anchors"]["all_present"], "bedrock_copies_hold": rd["bedrocks"]["all_hold"],
                       "validator_v0_7_assembly_on_v1_7": rd["validator"]["v0_7_assembly_on_v1_7"],
                       "adjacency_undeclared": rd["adjacency"]["undeclared_in_v0_8"]},
        "amend_owed": {"move_register_only": reg_only, "content": content,
                       "how": "one batch of superseding rows, each changing its move only (SM-45 may also change its "
                              "routing if its terminus changes); a seat that did not draft them judges them"},
        "proposed_r1_accepted": holds,
        "new_a_without_r1": {"target": "self-defeating#long", "row": "SM-27", "gate2_reading": "HOLDS",
                             "owed": "an R1 row after his word; the drafting seat decides how the R1 instruments admit an "
                                     "(a) the evidence file does not list (U-065)"},
        "knock_on": {"a_entries_in_v1_7": rd["knock_on"]["a_entries_in_v1_7"],
                     "newly_collided": [x["n"] for x in rd["knock_on"]["newly_collided"]],
                     "without_an_L7_row": [19, 68], "all_stand": True,
                     "owed_forward": "a successor's controls run the knock-on after the drafts are applied (U-064)"},
        "findings": finds,
        "safety_residuals_for_the_next_queue": [
            "revealed-preference#long: the preference for continued existence as the output of conditioning, compulsion "
            "and bias; classed sibling by L6's wide sweep, taken by no row (U-066)",
            "survivor-testimony#long and #diagnosis: the named bridge and the jump, the site-and-method detail SF-04 "
            "flagged; SW-07 removed only the death rate (U-066; gate2's lean: drop the site name)",
            "ai-fear#archetypeVariants.defender: 'The accelerationist grabbed the recommendation', to go with SM-30's (b)"],
        "asks_for_his_word": [
            {"ask": "Adopt this judgment: 22 ACCEPT and 11 CONFIRM now; the 18 AMENDs return to L7 for redraft.",
             "lean": "yes: every class and terminus holds on the v4.1.5 text; the AMENDs are wording (16) and two moves "
                     "that misstate the text"},
            {"ask": "Rule the four proposed HOLDS (#11 re-routed, #22, #32, #50) and the new (a) at self-defeating#long as "
                    "HOLDS; the R1 rows are appended after your word, as R1-070 was.",
             "lean": "yes: each answer now lives in the routed text, and each newly met (b) or (d) was read and does not "
                     "reach it"},
            {"ask": "Let the successor stand once a non-drafting seat accepts the 18 redrafts, conditional as 'yes to all' "
                    "was on SD-10.",
             "lean": "yes: the redrafts are narrow and measurable (the move only, but SM-45)"},
            {"ask": "Send the three safety residuals (U-066) to the next safety queue under your 2026-09-25 bar.",
             "lean": "yes for the revealed-preference sentence and the grabbed sentence; the bridge's name optional, "
                     "gate2's lean drop it"}],
        "next": "L7 appends the 18 superseding rows and rebuilds; a seat that did not draft them judges them; then his word "
                "on the asks and the R1 rows. Canon passes back to L7.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.44"
    d["canon_version_marker"] = "v38.44"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.5. gate2 judged L7's successor drafts (adversarial_map.successor_drafts_judgment_gate2): "
                      "22 ACCEPT, 11 CONFIRM, 18 AMEND. Next: L7 appends 18 superseding rows (16 change a move's "
                      "corpus-history wording only; SM-08 and SM-45 restate moves that misstate the text) and rebuilds; a "
                      "seat that did not draft them judges them; then his word on four asks, and the R1 rows it rules "
                      "(#11, #22, #32, #50 and the new (a) at self-defeating#long). Beside it: V2 drafts the pilot's shapes "
                      "(R-V4); argue re-vendors v4.1.5 (R0222). After: the next queue from carries_L7 and the three safety "
                      "residuals, adversarial wing v2 and /llms.txt, R2, the interconnection design, and the new-objection "
                      "intake (R-V6) once the pilot is judged.")
    nrs["judged_successor_drafts_gate2"] = ("gate2 judged the 51 rows (record L7_successor_drafts_judgments.json, gate "
                                            "l7_judgments_gate.py): 22 ACCEPT, 11 CONFIRM, 18 AMEND; validator v0_7 and "
                                            "register v0_8 confirmed; the nine newly collided (a)s stand. Judged, not ruled.")
    d["keyset_delta_ledger"]["v38_44_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (successor_drafts_judgment_gate2); "
        "next_recommended_session re-pointed; canon-meta; this note; one session_log_recent append. NO PIN. Every other "
        "top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): L7's successor drafts judged (R0237). Record %s: 22 ACCEPT, 11 CONFIRM, 18 AMEND (16 moves "
        "narrate the corpus's history; SM-08 and SM-45 misstate the text); validator v0_7 and register v0_8 CONFIRM; the "
        "knock-on the drafting seat did not run, measured here: nine (a)s newly collided, all stand. Four proposed HOLDS "
        "accepted; the new (a) at self-defeating#long read HOLDS. Canon back to L7." % (DATE, f(REC)["md5"][:8]))

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
    print("project_canon_v38_44.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: of the 51 %s | artifacts %s | knock-on %s" % (f(REC)["md5"][:8], dict(of51), dict(arts), dict(knock)))


if __name__ == "__main__":
    main()
