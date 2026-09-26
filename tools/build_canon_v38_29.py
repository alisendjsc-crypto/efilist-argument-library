#!/usr/bin/env python3
"""project_canon_v38_29.json -- MINOR. gate2's third judgment: v1_6's #46 (d), register v0_7's delta, the
knock-on measure, PQ-17 and the pin session's declaration; and the judgment gates read a pinned corpus.

ccclxiv FIRST: v38_28 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map one subkey is ADDED and
none moves. Every figure written here is computed from the committed files: the rulings gate, the quote
check and all three judgment gates run in-process and must be GREEN; the reading instrument must
reproduce its committed record; the three newest control records must be all-as-expected and name the
files they pin.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_28.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_29.json")
SRC_MD5 = "d9d0c23a9e47bd1cc38f69a378c2198f"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "gate2"
DATE = "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = {"R1_v1_6_judgment_gate2"}

R1 = "adversarial_map_staging/r1/"
RULINGS = R1 + "R1_rulings.json"
RGATE, QCHECK = R1 + "r1_rulings_gate.py", R1 + "r1_quote_check.py"
REC1, GATE1, CTL1, WAS1 = (R1 + "R1_drafts_judgments.json", R1 + "r1_judgments_gate.py",
                           R1 + "r1_judgments_gate_control_v0_5.json", "0e1cbc42118625f7a6bac0065018b326")
REC2, GATE2, CTL2, WAS2 = (R1 + "R1_v1_5_judgments.json", R1 + "r1_v1_5_judgments_gate.py",
                           R1 + "r1_v1_5_judgments_gate_control_v0_3.json", "f5a732f4b87cb5910d549eaa7fd59ae4")
REC3, GATE3, CTL3 = R1 + "R1_v1_6_judgments.json", R1 + "r1_v1_6_judgments_gate.py", R1 + "r1_v1_6_judgments_gate_control_v0_1.json"
READER, READING = R1 + "r1_v1_6_reading.py", R1 + "r1_v1_6_reading_v0_1.json"
KICKOFF = {"relay": "R0151", "md5": "45459ed3787b4c5c0d656bd09fce9a9a"}
PIN_KICKOFF = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2"}


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
    assert c["controls"][0]["control"] == "C0" and all(x["as_expected"] for x in c["controls"]), ctl_rel
    assert c["gate_md5"] == f(gate_rel)["md5"] and c["judgments_md5"] == f(rec_rel)["md5"], "%s is stale" % ctl_rel
    return dict(f(ctl_rel), file=ctl_rel, result="%d of %d as expected, the unmutated control first" % (
        len(c["controls"]), len(c["controls"])))


def main():
    raw = open(SRC, "rb").read()
    assert hashlib.md5(raw).hexdigest() == SRC_MD5, "SRC GUARD: v38_28 moved"
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_28 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- every gate, in-process
    G = mod(RGATE, "r1rg")
    fails, _ = G.check(os.path.join(REPO, RULINGS), REPO, G.committed_base())
    assert not fails, "RULINGS GATE RED: %s" % fails
    Q = mod(QCHECK, "r1qc")
    q_rows = Q.rulings_quotes()
    q_ok, q_fail = Q.check(q_rows, Q.Texts())
    assert not q_fail and q_ok == len(q_rows), "QUOTE CHECK RED: %s" % q_fail
    for rel, rec_rel, name in ((GATE1, REC1, "g1"), (GATE2, REC2, "g2"), (GATE3, REC3, "g3")):
        M = mod(rel, name)
        fl, _ = M.check(os.path.join(REPO, rec_rel), REPO, M.committed_base())
        assert not fl, "%s RED: %s" % (rel, fl)
    RD = mod(READER, "r1rd")
    fresh = (json.dumps(RD.measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    assert fresh == open(os.path.join(REPO, READING), "rb").read(), "the reading record does not reproduce"
    ctl = {"first": control(CTL1, GATE1, REC1), "second": control(CTL2, GATE2, REC2),
           "third": control(CTL3, GATE3, REC3)}

    # ---------------------------------------------------------------- the judgment, measured
    rec = json.load(open(os.path.join(REPO, REC3), encoding="utf-8"))
    assert rec["kickoff"] == KICKOFF
    rows = rec["rows"]
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["id"] not in sup]
    by_kind = collections.defaultdict(collections.Counter)
    for r in cur:
        if r["kind"] != "finding":
            by_kind[r["kind"]][r["verdict"]] += 1
    by_kind = {k: dict(v) for k, v in sorted(by_kind.items())}
    assert by_kind == {"declaration": {"CONFIRM": 1}, "measure": {"CONFIRM": 1}, "queue_row": {"AMEND": 1},
                       "redraft": {"ACCEPT": 1}, "register": {"ACCEPT": 1}}, by_kind
    pq = next(r for r in cur if r["kind"] == "queue_row")
    reading = json.loads(fresh.decode("utf-8"))
    assert reading["pq17"]["lone_actor_sentence_per_surface"] == {"corpus": 1, "jsx": 1, "combined": 1}
    assert reading["knock_on_independent"]["a_on_or_routed_to_node"] == []

    # ---------------------------------------------------------------- the block
    am["R1_v1_6_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's third judgment; Josiah's word decides.",
        "judge": "gate2, a Code session that drafted none of v1_6, the redrafts file, register v0_7 or the queue "
                 "(K258). #46's disposition was gate2's own lean (V-017); W-006 records the pull and how W-001 "
                 "answers it.",
        "his_words_it_follows": [w["verbatim"] for w in rec["his_word"]],
        "kickoff": KICKOFF,
        "record": dict(f(REC3), file=REC3, gate=dict(f(GATE3), file=GATE3), control=ctl["third"],
                       instrument=dict(f(READER), file=READER, record=dict(f(READING), file=READING))),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": by_kind,
        "n46": "ACCEPT. The move, anchor and status are v1_5's; the card's own continuation (a third horn, "
               "existence carrying weight without overriding content) needs a positive case against beings who "
               "exist, which is what HR-14 holds open. HR-02 was tested and fails on the register's own text: its "
               "gloss scopes it to the asymmetry, which does not reach the lives the button ends.",
        "register_v0_7": "ACCEPT: exactly one tributary added (#46, HR-14 terminus-held-open); nothing else moved.",
        "knock_on": "CONFIRM: 0 HOLDS newly collided, reproduced without the instrument (no (a) on or routed to "
                    "red-button-repugnant among v1_6's 29).",
        "pq17": {"verdict": "AMEND", "owed": pq["owed"],
                 "why": "R1-024 conceded the lone-actor analogy by name, and the analogy is the sentence after the "
                        "one PQ-17 names; it carries #4's own map anchor."},
        "declaration": "CONFIRM: his words to gate2 verbatim, R0150 named by id and md5; his words to the L4 "
                       "session recorded as that session reports them.",
        "findings": [{"row": r["id"], "title": r["title"], "whose": r["whose"]} for r in cur if r["kind"] == "finding"],
        "judgment_gates_read_pinned_corpus": {
            "law": "Every judgment gate reads corpus: at the md5 its judged map pins (meta.source_corpus_md5), "
                   "from git history once the working corpus moves. If those bytes cannot be recovered, a corpus "
                   "quote fails; it never floats with the working corpus.",
            "why": "R0150's phase 1: the declared pin session changes the corpus, and the first two judgment "
                   "records quote it 12 and 8 times. Any quote of a repaired sentence would otherwise go RED.",
            "rehearsed": "In a scratch clone, one quoted corpus span per record was replaced in the working corpus. "
                         "The committed gates went RED (NOT VERBATIM at J-003 and at V-002); the new gates stayed "
                         "GREEN. Measured before this commit, and recorded as controls in each gate's self-test "
                         "(a simulated pin GREEN; the same with git history withheld RED).",
            "first_gate": dict(f(GATE1), file=GATE1, was=WAS1, control=ctl["first"]),
            "second_gate": dict(f(GATE2), file=GATE2, was=WAS2, control=ctl["second"]),
            "third_gate": "written with it: corpus: from map_v1_6's pin, canon: from the pinned v38.28, which the "
                          "rename convention removes at this bump and git history keeps",
            "not_done_here": "The L-lane instruments (the assembly builders and controls, the dossier "
                             "instruments, r1_quote_check's corpus: source) are the pin session's phase 1.",
        },
        "for_his_word": [
            {"ask": "Adopt this judgment: #46's (d) at HR-14, register v0_7's delta and the knock-on measure "
                    "accepted or confirmed, and the declaration confirmed.",
             "recommendation": "yes; each verdict carries its reason, the gate checks every quotation at the bytes "
                               "judged, and the reading instrument reproduces every figure"},
            {"ask": "PQ-17 names both sentences of the why-not-suicide defender slot: the 'grabbed, not produced' "
                    "sentence and the lone-actor analogy after it (W-004).",
             "recommendation": "yes; R1-024 conceded the analogy by name, so repairing the other sentence alone "
                               "would leave the conceded text standing. The pin session, a drafting seat, makes the "
                               "correction in its first canon bump."},
        ],
        "next": "gate2 launches the declared pin session (R0150) now that this judgment has landed, so the window "
                "his words name is clear. The session carries W-004's AMEND and W-007's recommendation as defaults. "
                "His word on this judgment can come at any time, and the pin session records it in its next canon "
                "bump.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.29"
    d["canon_version_marker"] = "v38.29"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The declared pin session (seat l, kickoff R0150 %s), launched by gate2 once this judgment "
                      "lands: phase 1 pins the corpus in the L-lane instruments; phase 2 drafts all 17 queue rows' "
                      "repairs, with PQ-17 naming both sentences (adversarial_map.R1_v1_6_judgment_gate2, W-004) and "
                      "a knock-on list that includes every entry anchored inside a repaired sentence (W-007); gate2 "
                      "judges; his word; then the pin move. After it, a successor map re-anchors and the six waiting "
                      "(a)s are re-judged. Then adversarial wing v2 and /llms.txt "
                      "(adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design." % PIN_KICKOFF["md5"][:8])
    nrs["judged_v1_6_gate2"] = ("gate2 judged v1_6: %s. Judged is not ruled."
                                % "; ".join("%s %s" % (k, ", ".join("%s %d" % kv for kv in sorted(v.items())))
                                            for k, v in by_kind.items()))

    d["keyset_delta_ledger"]["v38_29_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (R1_v1_6_judgment_gate2); "
        "next_recommended_session re-pointed (session rewritten; judged_v1_6_gate2 added); canon-meta; this note; one "
        "session_log_recent append. NO PIN. invariants, schemas, hazard_map and flagship_sidecars asserted "
        "byte-identical, and every other top-level key too.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): v1_6 judged (R0151). Record %s: #46's (d) at HR-14 ACCEPT; register v0_7 ACCEPT; "
        "knock-on 0 CONFIRM; PQ-17 AMEND (name the lone-actor analogy too; it carries #4's anchor); declaration "
        "CONFIRM. The three judgment gates read the corpus at the md5 their judged map pins, rehearsed against a "
        "changed corpus. Judged, not ruled. Next: gate2 launches the declared pin session (R0150)."
        % (DATE, f(REC3)["md5"][:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == ADDED
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_29.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s" % (f(REC3)["md5"][:8], json.dumps(by_kind, sort_keys=True)))


if __name__ == "__main__":
    main()
