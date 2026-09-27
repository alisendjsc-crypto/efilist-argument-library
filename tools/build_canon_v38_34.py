#!/usr/bin/env python3
"""project_canon_v38_34.json -- MINOR. gate2's second judgment of the pin session's repairs: the four correction rows
(PD-19, PD-20, PD-21, PC-06) that answer its first judgment (R0179), the knock-on after them, and the phase-5 patch
tool against the judged one. With it, the text his word would ratify is complete.

ccclxiv FIRST: v38_33 is round-tripped at the serialization this file emits BEFORE anything is derived; it is read at
its md5 from the working tree or git history, so this builder runs after the rename removes it.

MINOR: keyset held at 42; every top-level key this build does not name byte-identical; inside adversarial_map one
subkey is ADDED and none moves. In-process: the rulings gate, the quote check, gate2's four earlier judgment gates and
the new one GREEN; the pin session's drafts gates v0_1 and v0_2 GREEN; both of gate2's reading records reproduce;
both of gate2's pq control records all-as-expected and naming the gate and record they pin.

  python3 tools/build_canon_v38_34.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_33.json", "3a9415fccf78fe08acfb19814692f8ed"
OUT = os.path.join(OUT_DIR, "project_canon_v38_34.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "gate2", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["pin_repair_redrafts_judgment_gate2"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

REC, GATE, CTL = (R1 + "PQ_repair_redrafts_judgments.json", R1 + "pq_repair_redrafts_gate.py",
                  R1 + "pq_repair_redrafts_gate_control_v0_1.json")
READER, READING = R1 + "pq_redraft_reading.py", R1 + "pq_redraft_reading_v0_1.json"
REC1, GATE1, CTL1 = (R1 + "PQ_repair_drafts_judgments.json", R1 + "pq_repair_judgments_gate.py",
                     R1 + "pq_repair_judgments_gate_control_v0_1.json")
READER1, READING1 = R1 + "pq_judgment_reading.py", R1 + "pq_judgment_reading_v0_1.json"
DRAFTS = R1 + "PQ_repair_drafts_L5.json"
DGATES = [R1 + "pin_repair_drafts_gate.py", R1 + "pin_repair_drafts_gate_v0_2.py"]
EARLIER = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
           (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
           (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json"),
           (GATE1, REC1)]
KICKOFF = {"relay": "R0179", "md5": "c4bf691a144554f6d04014ce141d739e"}
R0150 = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2"}
R0178 = {"relay": "R0178", "md5": "4f2f362dc7b56e8ec7bcff6f6a56e98b"}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def control(ctl_rel, gate_rel, rec_rel):
    c = json.load(open(os.path.join(REPO, ctl_rel), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and c["all_as_expected"] and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(gate_rel)["md5"] and c["judgments_md5"] == f(rec_rel)["md5"], "%s is stale" % ctl_rel
    return dict(f(ctl_rel), file=ctl_rel, result="%d of %d as expected, the unmutated control first; byte-identical "
                                                 "under two forced hash seeds" % (len(c["controls"]), len(c["controls"])))


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_33 does not round-trip"
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
    for i, rel in enumerate(DGATES):
        DG = mod(rel, "dg%d" % i)
        dfails, _ = DG.check(drafts, DG.committed_base())
        assert not dfails, "%s RED: %s" % (rel, dfails)
    JG = mod(GATE, "pqrg")
    jfails, _ = JG.check(os.path.join(REPO, REC), REPO, JG.committed_base())
    assert not jfails, "REDRAFTS GATE RED: %s" % jfails
    ctl = {"first": control(CTL1, GATE1, REC1), "second": control(CTL, GATE, REC)}
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
    assert tally == {"companion_redraft": {"ACCEPT": 1}, "knock_on": {"CONFIRM": 1}, "patch": {"CONFIRM": 1},
                     "redraft": {"ACCEPT": 3}}, tally
    corrections = [{"judgment": r["id"], "row": r["row_id"], "replaces": r["replaces"], "answers": r["answers"],
                    "verdict": r["verdict"], **({"lean": r["lean"]} if "lean" in r else {})}
                   for r in cur if r["kind"] in ("redraft", "companion_redraft")]
    dsup = {r.get("supersedes") for r in drafts["rows"] if r.get("supersedes")}
    dcur = [r for r in drafts["rows"] if r["id"] not in dsup]
    ratifiable = [r["id"] for r in dcur if r["kind"] == "draft" and r["status"] == "declared"]
    admissible = [r["id"] for r in dcur if r["kind"] == "companion"]
    assert len(ratifiable) == 18 and admissible == ["PC-01", "PC-02", "PC-03", "PC-04", "PC-06"], (ratifiable, admissible)
    eq = rd["patch_equivalence"]

    # ---------------------------------------------------------------- the block
    am["pin_repair_redrafts_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's second judgment of the pin session's repairs; with it every sentence his "
                  "word would ratify has been judged. Josiah's word decides; nothing is served on a judgment.",
        "judge": "gate2, which drafted none of the correction rows (K258). The four carry out gate2's own owed changes "
                 "and PC-06 uses its own wording; Y-007 records the pull and how each row was read against its whole "
                 "paragraph or slot.",
        "kickoff": KICKOFF,
        "answers": {"record": dict(f(REC1), file=REC1), "canon_block": "adversarial_map.pin_repair_drafts_judgment_gate2"},
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE, control=ctl["second"]),
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": tally,
        "corrections": corrections,
        "knock_on": "CONFIRM: the corrections keep every current text; 13 anchors move and 10 answers route, the "
                    "first judgment's sets and the knock-on record v0_2's; the five HOLDS stand.",
        "patch": {"verdict": "CONFIRM", "byte_identical_between_v0_1_and_v0_2": True,
                  "surfaces_declared": eq["declared"]["surfaces"], "surfaces_all": eq["all"]["surfaces"],
                  "note": "v0_2 adds only the ratified selection and the corpus content-cut field; phase 5 applies the "
                          "text judged here"},
        "the_text_his_word_would_ratify": {
            "drafts": ratifiable,
            "companions": admissible,
            "why_these": "the current rows of the drafts record: the fifteen drafts the first judgment accepted, the "
                         "three corrections accepted here in place of PD-02, PD-03 and PD-08, and the five companions "
                         "with PC-06 in place of PC-05",
            "drafts_record": dict(f(DRAFTS), file=DRAFTS),
        },
        "for_his_word": [
            {"ask": "Ratify the eighteen drafted sentences, as judged, for the pin move: %s." % ", ".join(ratifiable),
             "lean_L5": "yes", "lean_gate2": "yes; every one is now accepted"},
            {"ask": "Admit the five companion sentences: %s." % ", ".join(admissible),
             "lean_L5": "yes",
             "lean_gate2": "yes; each keeps its row's paragraph or a waiting (a) from contradicting the repair, and "
                           "PC-06 names the reply, not the man"},
            {"ask": "Leave the slot- and paragraph-scale repairs for a later queue: PF-01..PF-03, the sibling "
                    "passages of X-033, and the Bradley closing line of X-034.",
             "lean_L5": "yes", "lean_gate2": "yes, each filed as its own (b) at the successor map first"},
            {"ask": "The six passages that frame the survival drive as a barrier to exit (X-032).",
             "lean_L5": "agrees with gate2",
             "lean_gate2": "do not hold the pin; open a short safety pass over the six as soon as it closes. Keep the "
                           "anti-pro-life argument; cut only the framing."},
        ],
        "supersedes_asks": "%s's four asks (%s), now with every correction judged and both seats' leans agreeing"
                           % (R0178["relay"], R0178["md5"][:8]),
        "next": "His word, relayed to seat l. L5 appends one ratification row naming exactly the rows he ratifies "
                "(pin_repair_drafts_gate_v0_2.py G10 checks it), records his word in canon, and runs phase 5: "
                "tools/pin_patch_l5_v0_2.py --apply --set ratified (R0150 %s). Then LD3 (R0170)." % R0150["md5"][:8],
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.34"
    d["canon_version_marker"] = "v38.34"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("His word on the judged text (adversarial_map.pin_repair_redrafts_judgment_gate2.for_his_word), "
                      "relayed to seat l; then L5's phase 5, the pin move (R0150 %s), with one ratification row naming "
                      "exactly what he ratifies. Then the safety pass over the six loci gate2 found (X-032), a successor "
                      "map that re-anchors, re-judges the six waiting (a)s and files the sibling loci (X-033) and "
                      "PF-01..03 as (b)s, adversarial wing v2 and /llms.txt (adversarial_map.reader_aid_backlog_L4c), "
                      "R2, and the interconnection design." % R0150["md5"][:8])
    nrs["judged_pin_repair_redrafts_gate2"] = (
        "gate2 judged L5's corrections: %s. Every sentence his word would ratify is judged. Judged is not ruled."
        % "; ".join("%s %s" % (k, ", ".join("%s %d" % kv for kv in v.items())) for k, v in tally.items()))

    d["keyset_delta_ledger"]["v38_34_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (pin_repair_redrafts_judgment_gate2); "
        "next_recommended_session re-pointed (session rewritten; judged_pin_repair_redrafts_gate2 added); canon-meta; "
        "this note; one session_log_recent append. NO PIN. Every other top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): L5's corrections judged (R0179). Record %s: PD-19, PD-20, PD-21 and PC-06 ACCEPT, each "
        "making the change its first-judgment row owed; the knock-on unchanged and the five HOLDS standing; the phase-5 "
        "patch tool builds the judged tool's bytes. Every sentence his word would ratify is judged; both seats' leans "
        "agree on all four asks. Judged, not ruled." % (DATE, f(REC)["md5"][:8]))

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
    print("project_canon_v38_34.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s" % (f(REC)["md5"][:8], json.dumps(tally, sort_keys=True)))


if __name__ == "__main__":
    main()
