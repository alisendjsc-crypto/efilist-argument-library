#!/usr/bin/env python3
"""project_canon_v38_32.json -- MINOR. gate2's fourth judgment: the declared pin session's drafted repairs for
pin_move_queue_L5 (18 sentences), its five proposed companions, its seven findings and the knock-on (R0175).

ccclxiv FIRST: v38_31 is round-tripped at the serialization this file emits BEFORE anything is derived. v38_31 is
read at its md5 from the working tree or git history, so this builder runs after the rename removes it.

MINOR: keyset held at 42; every top-level key this build does not name byte-identical; inside adversarial_map one
subkey is ADDED and none moves. In-process: the rulings gate, the quote check, gate2's three earlier judgment gates
and the new one GREEN; the drafts gate GREEN (its patch simulation included) with its control record all-as-expected;
the new gate's control record all-as-expected and naming the gate and record it pins; the reading record reproduces.

  python3 tools/build_canon_v38_32.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_31.json", "58a729987e9c223d1ca3e3741c96ecce"
OUT = os.path.join(OUT_DIR, "project_canon_v38_32.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "gate2", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["pin_repair_drafts_judgment_gate2"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

REC, GATE, CTL = R1 + "PQ_repair_drafts_judgments.json", R1 + "pq_repair_judgments_gate.py", \
    R1 + "pq_repair_judgments_gate_control_v0_1.json"
READER, READING = R1 + "pq_judgment_reading.py", R1 + "pq_judgment_reading_v0_1.json"
DRAFTS, DGATE, DCTL = R1 + "PQ_repair_drafts_L5.json", R1 + "pin_repair_drafts_gate.py", \
    R1 + "pin_repair_drafts_gate_control_v0_1.json"
EARLIER = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
           (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
           (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json")]
KICKOFF = {"relay": "R0175", "md5": "43a09b54db5ac68e4dab24616b8cf710"}
R0150 = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2"}


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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_31 does not round-trip"
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
    DG = mod(DGATE, "pqg")
    drafts = json.load(open(os.path.join(REPO, DRAFTS), encoding="utf-8"))
    dfails, _ = DG.check(drafts, DG.committed_base())
    assert not dfails, "DRAFTS GATE RED: %s" % dfails
    dc = json.load(open(os.path.join(REPO, DCTL), encoding="utf-8"))
    assert dc["controls"][0]["control"] == "C0" and all(x["as_expected"] for x in dc["controls"])
    JG = mod(GATE, "pqjg")
    jfails, _ = JG.check(os.path.join(REPO, REC), REPO, JG.committed_base())
    assert not jfails, "JUDGMENTS GATE RED: %s" % jfails
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and c["all_as_expected"] and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["judgments_md5"] == f(REC)["md5"], "the control record is stale"
    RD = mod(READER, "pqrd")
    fresh = (json.dumps(RD.measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    assert fresh == open(os.path.join(REPO, READING), "rb").read(), "the reading record does not reproduce"
    reading = json.loads(fresh.decode("utf-8"))

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
    assert tally == {"companion": {"ACCEPT": 5}, "draft": {"ACCEPT": 15, "AMEND": 3},
                     "finding_review": {"CONFIRM": 7}, "knock_on": {"CONFIRM": 1}}, tally
    amends = [{"judgment": r["id"], "draft": r["row_id"], "locus": r["locus"], "owed": r["owed"]}
              for r in cur if r["kind"] == "draft" and r["verdict"] == "AMEND"]
    accepted = [r["row_id"] for r in cur if r["kind"] == "draft" and r["verdict"] == "ACCEPT"]
    comps = [{"judgment": r["id"], "companion": r["row_id"], "verdict": r["verdict"], "lean": r["lean"]}
             for r in cur if r["kind"] == "companion"]
    reviews = {r["row_id"]: r["verdict"] for r in cur if r["kind"] == "finding_review"}
    ko = next(r for r in cur if r["kind"] == "knock_on")
    finds = [{"judgment": r["id"], "title": r["title"], "whose": r["whose"], "recommendation": r["recommendation"]}
             for r in cur if r["kind"] == "finding"]
    ex = reading["exit_framing"]
    assert ex["pre_equals_post"] and len(ex["loci"]) == 6 and len(ex["nodes"]) == 5, ex["loci"]
    sib = {s["defect"]: s["loci"] for s in reading["sibling_loci"]}
    kn = reading["knock_on_independent"]
    assert kn["anchor_inside_matches_record"] and kn["answer_routes_here_matches_record"]

    # ---------------------------------------------------------------- the block
    am["pin_repair_drafts_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's fourth judgment; Josiah's word decides. Nothing is served on a judgment.",
        "judge": "gate2, a Code session that drafted none of the drafts record, its gate, the patch tool or the knock-on "
                 "record (K258). PD-17 and PD-18 carry out gate2's own lean (V-023) and finding (W-004); X-035 "
                 "records the pull.",
        "his_words_it_applies": [{"verbatim": w["verbatim"], "said": w["said"], "recorded": w["recorded"]}
                                 for w in rec["his_word"]],
        "kickoff": KICKOFF,
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE, control=dict(
            f(CTL), file=CTL, result="%d of %d as expected, the unmutated control first; byte-identical under two "
                                     "forced hash seeds" % (len(c["controls"]), len(c["controls"])))),
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": tally,
        "drafts_accepted": accepted,
        "drafts_amended": amends,
        "companions": comps,
        "l5_findings": reviews,
        "knock_on": {"claim": ko["claim"], "verdict": ko["verdict"],
                     "reproduced": "gate2's own instrument, at the pinned bytes: the same sets as the drafts' "
                                   "knock-on record; the patch changes exactly the %d repaired loci, and in each only "
                                   "the rows' sentences" % reading["confinement"]["repaired_loci"],
                     "also": "a fourteenth entry, the (b) at benatar-asymmetry-attack#long, is anchored inside PD-02's "
                             "sentence and again in the paragraph's last sentence, which stays; it does not move and is "
                             "re-judged there at the successor map"},
        "safety": {"bar": "his words of 2026-09-25, verbatim in the record's his_word",
                   "drafts": "PD-08, PC-02, PD-15, PD-17 and PD-18 touch suicide and killing; none encourages "
                             "self-harm, suicide or homicide, and none turns pro-life. PD-08's AMEND is about "
                             "attribution and keeps every safety property the draft has.",
                   "outside_the_queue": {"finding": "X-032", "loci": ex["loci"], "patterns": ex["patterns"],
                                         "reading": "the survival drive, or the taboo against suicide, framed as a "
                                                    "barrier on an exit; the argument is anti-pro-life and stays, the "
                                                    "framing is what his bar puts in question (the seat's reading, "
                                                    "not his words)"}},
        "sibling_loci": {"finding": "X-033", "loci": sib},
        "gate2_findings": finds,
        "for_his_word": [
            {"ask": "Ratify the drafted sentences for the pin move, as judged: the fifteen accepted, and PD-02, PD-03 "
                    "and PD-08 once L5's superseding rows make the owed changes and gate2 accepts them.",
             "lean_L5": "yes, as gate2 leaves them",
             "lean_gate2": "yes; and give the word now, on the condition that gate2 accepts the three, so the pin "
                           "does not wait on you twice. Each owed change is narrow and named (X-002, X-003, X-008)."},
            {"ask": "Admit the five companion sentences PC-01..PC-05 into this pin.",
             "lean_L5": "yes",
             "lean_gate2": "yes, all five: each is accepted, and each keeps its row's paragraph or a waiting (a) from "
                           "contradicting the repair. PC-05 names Bradley: check a source first, or reword it to name "
                           "the reply rather than the man (X-034)."},
            {"ask": "Leave the slot- and paragraph-scale repairs for a later queue.",
             "lean_L5": "yes; PF-01, PF-02 and PF-03, each filed and judged as its own (b) at the successor map first",
             "lean_gate2": "yes, and put the sibling loci of X-033 in the same queue: after this pin, three nodes say "
                           "both things until it lands"},
            {"ask": "The six loci that frame the survival drive as a barrier to exit (X-032).",
             "lean_L5": "not yet seen; gate2 raised it",
             "lean_gate2": "do not hold this pin for it; open a short safety pass over the six as soon as this pin "
                           "closes, not at the successor map: the library seat drafts, gate2 judges, your word, then a "
                           "pin. Keep the anti-pro-life argument; cut only the framing."},
        ],
        "next": "L5 appends superseding rows for PD-02, PD-03 and PD-08 that make the owed changes, re-runs its gate and "
                "the patch, and relays them; gate2 judges the three (rows superseding X-002, X-003 and X-008). Then his "
                "word, which L5 records in canon with ratified rows, and phase 5: tools/pin_patch_l5.py --apply --set "
                "ratified (R0150 %s). LD3 (R0170) follows L5's pin." % R0150["md5"][:8],
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.32"
    d["canon_version_marker"] = "v38.32"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("L5 (the declared pin session, R0150 %s) appends the three owed redrafts (PD-02, PD-03, PD-08; "
                      "adversarial_map.pin_repair_drafts_judgment_gate2); gate2 judges them; his word ratifies the judged "
                      "text and admits the companions; L5's phase 5 moves the pin. Then the safety pass over the six loci "
                      "gate2 found (X-032), a successor map that re-anchors and re-judges the six waiting (a)s and files "
                      "the sibling loci (X-033) and PF-01..03 as (b)s, adversarial wing v2 and /llms.txt "
                      "(adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design." % R0150["md5"][:8])
    nrs["judged_pin_repair_drafts_gate2"] = (
        "gate2 judged L5's drafts: %s. Judged is not ruled."
        % "; ".join("%s %s" % (k, ", ".join("%s %d" % kv for kv in v.items())) for k, v in tally.items()))

    d["keyset_delta_ledger"]["v38_32_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (pin_repair_drafts_judgment_gate2); "
        "next_recommended_session re-pointed (session rewritten; judged_pin_repair_drafts_gate2 added); canon-meta; this "
        "note; one session_log_recent append. NO PIN. Every other top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): L5's drafts judged (R0175). Record %s: 15 drafts ACCEPT; PD-02, PD-03 and PD-08 AMEND "
        "(a consent threshold the paragraph gives the rival; a clause that claims more than the fence; the second layer "
        "named as some efilists'); companions ACCEPT, lean admit; L5's seven findings CONFIRM; knock-on CONFIRM, the five "
        "HOLDS stand. Found: six loci that frame the survival drive as a barrier to exit (a safety question for him) "
        "and the pin's defects at sibling loci. Judged, not ruled." % (DATE, f(REC)["md5"][:8]))

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
    print("project_canon_v38_32.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s" % (f(REC)["md5"][:8], json.dumps(tally, sort_keys=True)))


if __name__ == "__main__":
    main()
