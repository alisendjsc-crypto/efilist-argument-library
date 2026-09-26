#!/usr/bin/env python3
"""project_canon_v38_26.json -- MINOR. gate2's second judgment: v1_5's redrafts, register v0_6, the
first gate's change, and the eleven knocked-on HOLDS. Judged, not ruled.

ccclxiv FIRST: v38_25 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map one subkey is ADDED and
none moves. Every figure written here is computed from the committed files: both judgment gates run
in-process and must be GREEN, both newest control records must be all-as-expected and name the
committed files, and the reading instrument must be the one the record names.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_25.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_26.json")
SRC_MD5 = "72f474c22ee4b9d670dd3edbbcb0d062"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "gate2"
DATE = "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = {"R1_v1_5_judgment_gate2"}

REC = "adversarial_map_staging/r1/R1_v1_5_judgments.json"
GATE = "adversarial_map_staging/r1/r1_v1_5_judgments_gate.py"
GATE_CTL = "adversarial_map_staging/r1/r1_v1_5_judgments_gate_control_v0_1.json"
INSTR = "adversarial_map_staging/r1/r1_knock_on_dossiers.py"
GATE1 = "adversarial_map_staging/r1/r1_judgments_gate.py"
GATE1_CTL = "adversarial_map_staging/r1/r1_judgments_gate_control_v0_3.json"
REC1 = "adversarial_map_staging/r1/R1_drafts_judgments.json"

KICKOFF = {"relay": "R0136", "md5": "12237481725827051e07186398e0250b"}
HIS_WORD_L4B = "Go with the recommendations on all of the above and for Gate 2's seat. Continue with my word."


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def gate_module(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    raw = open(SRC, "rb").read()
    assert hashlib.md5(raw).hexdigest() == SRC_MD5, "SRC GUARD: v38_25 moved"
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_25 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- both gates, in-process
    G = gate_module(GATE, "r1v15g")
    fails, _ = G.check(os.path.join(REPO, REC), REPO, G.committed_base())
    assert not fails, "v1_5 JUDGMENTS GATE RED: %s" % fails
    G1 = gate_module(GATE1, "r1jg")
    fails1, _ = G1.check(os.path.join(REPO, REC1), REPO, G1.committed_base())
    assert not fails1, "FIRST JUDGMENTS GATE RED: %s" % fails1
    for ctl_rel, gate_rel, rec_rel, key in ((GATE_CTL, GATE, REC, "judgments_md5"), (GATE1_CTL, GATE1, REC1, "judgments_md5")):
        ctl = json.load(open(os.path.join(REPO, ctl_rel), encoding="utf-8"))
        assert ctl["controls"][0]["control"] == "C0" and all(c["as_expected"] for c in ctl["controls"]), ctl_rel
        assert ctl["gate_md5"] == f(gate_rel)["md5"] and ctl[key] == f(rec_rel)["md5"], "%s is stale" % ctl_rel
    rec = json.load(open(os.path.join(REPO, REC), encoding="utf-8"))
    assert rec["instrument"]["file"] == INSTR and rec["his_word"]["verbatim"] == HIS_WORD_L4B
    rows = rec["rows"]
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["id"] not in sup]
    by_kind = collections.defaultdict(collections.Counter)
    for r in cur:
        if r["kind"] != "finding":
            by_kind[r["kind"]][r["verdict"]] += 1
    by_kind = {k: dict(v) for k, v in sorted(by_kind.items())}
    reopened = [{"n": r["n"], "row": r["id"], "r1_row": r["r1_row"], "target": r["target"], "lean": r["lean"]}
                for r in cur if r["kind"] == "knock_on" and r["verdict"] == "REOPENS"]
    stands = [r["n"] for r in cur if r["kind"] == "knock_on" and r["verdict"] == "STANDS"]
    assert by_kind["redraft"] == {"ACCEPT": 6} and by_kind["register"] == {"ACCEPT": 3}
    assert len(reopened) + len(stands) == 11

    # ---------------------------------------------------------------- the block
    am["R1_v1_5_judgment_gate2"] = {
        "status": "JUDGED, NOT RULED. gate2's second judgment; Josiah's word decides. The REOPENS is a lean for his "
                  "re-ruling of an R1 row, not a ruling.",
        "judge": "gate2, a Code session that drafted none of v1_5, the redrafts file or register v0_6 (K258)",
        "his_word_it_follows": HIS_WORD_L4B,
        "kickoff": KICKOFF,
        "record": dict(f(REC), file=REC, gate=dict(f(GATE), file=GATE),
                       control=dict(f(GATE_CTL), file=GATE_CTL,
                                    result="%d of %d as expected, the unmutated control first" % (
                                        sum(c["as_expected"] for c in json.load(open(os.path.join(REPO, GATE_CTL),
                                                                                     encoding="utf-8"))["controls"]),
                                        len(json.load(open(os.path.join(REPO, GATE_CTL), encoding="utf-8"))["controls"]))),
                       instrument=dict(f(INSTR), file=INSTR)),
        "judged": {k: v["md5"] for k, v in rec["judged"].items()},
        "verdicts": by_kind,
        "the_redrafts": "all six accepted: #14's move now reaches HR-14's successor-preference facet from R1-049's own "
                        "line; #58 is a (b) at social-contract#long whose burden-share repair needs no bedrock premise "
                        "(the corpus has no fair-play discussion anywhere, measured); #25, #59 and #62 name the path "
                        "their line takes; #16 names its passage",
        "register_v0_6": "all three declared deltas accepted, and nothing else moved (diffed field by field)",
        "the_first_gate": {"verdict": "CONFIRM", "change": "a2a20f22 -> f0460624 (L4b)",
                           "why": "register: quotations must resolve against the register the record judged; the "
                                  "original gate went RED on exactly J-046 and J-052 once v0_6 made the corrections "
                                  "those rows asked for, and on nothing else",
                           "docstring": dict(f(GATE1), file=GATE1, control=dict(f(GATE1_CTL), file=GATE1_CTL),
                                             note="point 5 brought into line with the change; logic unchanged")},
        "knock_on": {"stands": stands, "reopens": reopened},
        "findings": [{"row": r["id"], "title": r["title"], "whose": r["whose"]} for r in cur if r["kind"] == "finding"],
        "for_his_word": [
            {"ask": "Adopt this judgment: the six redrafts, register v0_6 and the gate change accepted; ten knocked-on "
                    "HOLDS stand.",
             "recommendation": "yes; each verdict carries its reason, and the gate checks every quotation"},
            {"ask": "Re-rule #46 (R1-011) FAILS.",
             "recommendation": "yes; the new (d) at its answering locus records that the recoil its answer had to "
                               "empty still stands, so the card cannot say WE ANSWER THIS. Then a drafting seat runs "
                               "the class law (lean (d) at HR-14, terminus-held-open) and a non-drafting seat judges it"},
            {"ask": "Queue why-not-suicide's defender-slot framing ('grabbed, not produced') beside PQ-08.",
             "recommendation": "yes, when the queue next moves; it is the conceded misfit R1-024 accepted, and it "
                               "stays his to open"},
        ],
        "next": "His word. If #46 is re-ruled, a drafting seat builds the successor with its disposition and re-runs "
                "the knock-on measure; a seat that did not draft it judges it. The 16-row pin session does not depend "
                "on #46 and can be declared on his word.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.26"
    d["canon_version_marker"] = "v38.26"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("Josiah's word on gate2's second judgment (adversarial_map.R1_v1_5_judgment_gate2; %s, %s): the "
                      "six redrafts, register v0_6 and the first gate's change accepted; ten knocked-on HOLDS stand; "
                      "#46 reopens with a lean to re-rule it FAILS. Then a drafting seat (l) builds the successor with "
                      "#46's disposition, re-measures the knock-on, and a seat that did not draft it judges it (K258). "
                      "The pin session (adversarial_map.pin_move_queue_v1_5, 16 rows) is his to declare and does not "
                      "wait on #46. Then R2, then the interconnection design." % (REC, f(REC)["md5"][:8]))
    nrs["judged_v1_5_gate2"] = ("gate2 judged v1_5: %s. Knock-on: %d stand, #%s reopens. Judged is not ruled."
                                % ("; ".join("%s %s" % (k, ", ".join("%s %d" % kv for kv in sorted(v.items())))
                                             for k, v in by_kind.items() if k != "knock_on"),
                                   len(stands), ", #".join(str(x["n"]) for x in reopened)))

    d["keyset_delta_ledger"]["v38_26_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (R1_v1_5_judgment_gate2); "
        "next_recommended_session re-pointed (session rewritten; judged_v1_5_gate2 added); canon-meta; this note; one "
        "session_log_recent append. NO PIN. invariants, schemas, hazard_map and flagship_sidecars asserted "
        "byte-identical, and every other top-level key too.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): v1_5 judged (R0136), under '%s'. Record %s: six redrafts ACCEPT, register v0_6's three "
        "deltas ACCEPT, the first gate's change CONFIRM (its docstring brought into line). Knock-on: %d HOLDS stand; "
        "#46 REOPENS (the new (d) at its answering locus records the recoil its answer had to empty as standing; lean "
        "re-rule FAILS, then (d) HR-14). Judged, not ruled."
        % (DATE, HIS_WORD_L4B, f(REC)["md5"][:8], len(stands)))

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
    print("project_canon_v38_26.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  record %s: %s | stands %s | reopens %s" % (f(REC)["md5"][:8], json.dumps(by_kind, sort_keys=True),
                                                        stands, [x["n"] for x in reopened]))


if __name__ == "__main__":
    main()
