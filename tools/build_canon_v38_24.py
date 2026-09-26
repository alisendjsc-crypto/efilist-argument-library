#!/usr/bin/env python3
"""project_canon_v38_24.json -- MINOR. gate2: L4's drafts of R1's 45 FAILS, judged and not ruled.

ccclxiv FIRST: v38_23 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map one subkey is ADDED and
none moves. Every figure written here is computed from the committed files: the judgments gate runs
in-process and must be GREEN, its control record must be all-as-expected and name the committed
judgments file, and the reading instrument must be the one the record names. His words are carried
verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_23.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_24.json")
SRC_MD5 = "a743042662473f04e588c7ee10f4e111"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "gate2"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = {"R1_drafts_judgment_gate2"}

JUDG = "adversarial_map_staging/r1/R1_drafts_judgments.json"
GATE = "adversarial_map_staging/r1/r1_judgments_gate.py"
GATE_CTL = "adversarial_map_staging/r1/r1_judgments_gate_control_v0_1.json"
INSTR = "adversarial_map_staging/r1/r1_draft_dossiers.py"

KICKOFF = {"relay": "R0122", "md5": "f8be5b73e33f39192990d08c9d6dd987"}
HIS_PROCEED_L3 = "Proceed with your recommendations on all front's."
REC_L3 = ("The drafting pass (L4). Lean: a fresh session, starting from the worklist, with a different session "
          "judging the drafts.")


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def main():
    raw = open(SRC, "rb").read()
    assert hashlib.md5(raw).hexdigest() == SRC_MD5, "SRC GUARD: v38_23 moved"
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_23 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- the gate, in-process
    spec = importlib.util.spec_from_file_location("r1jg", os.path.join(REPO, GATE))
    G = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(G)
    fails, info = G.check(os.path.join(REPO, JUDG), REPO, G.committed_base())
    assert not fails, "JUDGMENTS GATE RED: %s" % fails
    ctl = json.load(open(os.path.join(REPO, GATE_CTL), encoding="utf-8"))
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["controls"][0]["control"] == "C0"
    assert ctl["judgments_md5"] == f(JUDG)["md5"] and ctl["gate_md5"] == f(GATE)["md5"], "control record is stale"
    jd = json.load(open(os.path.join(REPO, JUDG), encoding="utf-8"))
    assert jd["instrument"]["file"] == INSTR
    rows = jd["rows"]
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["id"] not in sup]
    drafts = [r for r in cur if r["kind"] == "draft"]
    rels = [r for r in cur if r["kind"] == "relation"]
    finds = [r for r in cur if r["kind"] == "finding"]
    verdicts = dict(collections.Counter(r["verdict"] for r in drafts))
    by_disp = collections.defaultdict(collections.Counter)
    for r in drafts:
        by_disp[r["drafted"]][r["verdict"]] += 1
    by_disp = {k: dict(v) for k, v in sorted(by_disp.items())}
    not_accepted = [{"n": r["n"], "row": r["id"], "r1_row": r["r1_row"], "target": r["target"],
                     "drafted": r["drafted"], "verdict": r["verdict"], "owed": r["owed"]}
                    for r in drafts if r["verdict"] != "ACCEPT"]
    assert len(drafts) == 45 and verdicts.get("ACCEPT", 0) + verdicts.get("AMEND", 0) + verdicts.get("REJECT", 0) == 45

    # ---------------------------------------------------------------- the block
    am["R1_drafts_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2 judged L4's drafts; Josiah's word decides. Nothing ships on a judgment, "
                  "and v1_4 is not edited: a drafting seat applies the AMEND and the REJECT in a successor map, and "
                  "a seat that did not draft it judges it (K258).",
        "judge": "gate2, a Code session that drafted none of L4's drafts, the drafts file or register v0_5 (K258)",
        "his_words_verbatim": HIS_PROCEED_L3,
        "the_recommendation_he_adopted": REC_L3,
        "kickoff": KICKOFF,
        "standard": "adversarial_map.R1_standard_ruling_L2; the record's header carries his words and the "
                    "recommendation he adopted, verbatim",
        "record": dict(f(JUDG), file=JUDG, gate=dict(f(GATE), file=GATE),
                       control=dict(f(GATE_CTL), file=GATE_CTL,
                                    result="%d of %d as expected, the unmutated control first"
                                           % (sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]))),
                       instrument=dict(f(INSTR), file=INSTR)),
        "judged": {k: v["md5"] for k, v in jd["judged"].items()},
        "verdicts": verdicts,
        "by_disposition": by_disp,
        "not_accepted": not_accepted,
        "relations": {r["relation"]: r["verdict"] for r in rels},
        "the_departure": "#45 goes to HR-02 intrinsic-value-of-existence rather than R1-017's HR-03, and the judge "
                         "accepts it: R1-017's own reason shows the tie-breaker does not reach existing beings, so the "
                         "line ends at the bare tie the node's own #medium (d) registers, with #47.",
        "findings": [{"row": r["id"], "title": r["title"], "whose": r["whose"]} for r in finds],
        "for_his_word": [
            {"ask": "Adopt the judgment: 43 drafts accepted, #14 amended, #58 rejected, the three relations accepted.",
             "recommendation": "yes; every verdict carries its reason and quotes, and the gate checks every quote "
                               "against its source"},
            {"ask": "#45's departure from R1-017 (HR-02, not HR-03).",
             "recommendation": "accept; a line cannot end at the bedrock of a premise its own ruling shows "
                               "inapplicable"},
            {"ask": "The new-prose reading (J-049): a move completion from the entry's own R1 row, forced by a "
                    "mandated trim and a ratified gate, is ruled record and not new prose.",
             "recommendation": "adopt; it keeps L2's 'no new prose' to what it guarded"},
            {"ask": "#58's redraft: the class-law run by a drafting seat.",
             "recommendation": "lean (b) at social-contract#long; (d) at HR-06 only if the burden-share distinction "
                               "fails"},
            {"ask": "The conditions direction (J-052): re-declare the K349 pair as HR-11 conditions HR-14.",
             "recommendation": "yes; the definition and the pair's own note already say so, and nothing substantive "
                               "moves"},
            {"ask": "Two conceded defects the new (d)s pass over (#6's phrase, #20's sentence) join pin_move_queue_L4.",
             "recommendation": "yes, when the queue next moves; it stays his to open"},
        ],
        "next": "His word. Then a drafting seat builds the successor map (v1_5) with the #14 amendment, the #58 "
                "redraft and the terminus_routing fixes at #25, #59 and #62, and #16's wording. A seat that did not "
                "draft it judges it. Then the 11 knock-on HOLDS are read against what survives. Then R2.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.24"
    d["canon_version_marker"] = "v38.24"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("Josiah's word on gate2's judgment (adversarial_map.R1_drafts_judgment_gate2; %s, %s). Then a "
                      "drafting seat (l) builds the successor map v1_5 from v1_4: #14 amended, #58 redrafted under "
                      "the class law, the terminus_routing wording at #25, #59 and #62, #16's wording. A seat that "
                      "did not draft it judges it (K258). Then the 11 knock-on HOLDS are read against what "
                      "survives. The pin-move queue (adversarial_map.pin_move_queue_L4) stays Josiah's to open. "
                      "Then R2, then the interconnection design." % (JUDG, f(JUDG)["md5"][:8]))
    nrs["judged_gate2"] = ("gate2 judged the 45 drafts: %s. Relations: %s. Judged is not ruled."
                           % (", ".join("%s %d" % kv for kv in sorted(verdicts.items())),
                              ", ".join("%s %s" % (r["relation"], r["verdict"]) for r in rels)))

    d["keyset_delta_ledger"]["v38_24_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (R1_drafts_judgment_gate2); "
        "next_recommended_session re-pointed (session rewritten; judged_gate2 added); canon-meta; this note; one "
        "session_log_recent append. NO PIN. invariants, schemas, hazard_map and flagship_sidecars asserted "
        "byte-identical, and every other top-level key too.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): L4's drafts of R1's 45 FAILS judged (R0122), under '%s'. %s: %s; relations %s; %d "
        "findings, six asks for his word with the seat's leans. #14 AMEND (its trimmed move never reaches HR-14); "
        "#58 REJECT (the new route answers only the instrumental form, and its fair-play answer lives in the "
        "grounds). #45's departure to HR-02 accepted. Judged, not ruled."
        % (DATE, HIS_PROCEED_L3, f(JUDG)["md5"][:8], ", ".join("%s %d" % kv for kv in sorted(verdicts.items())),
           ", ".join(r["verdict"] for r in rels), len(finds)))

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
    print("project_canon_v38_24.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  judgments %s: %s | relations %s | findings %d"
          % (f(JUDG)["md5"][:8], json.dumps(verdicts, sort_keys=True), [r["verdict"] for r in rels], len(finds)))


if __name__ == "__main__":
    main()
