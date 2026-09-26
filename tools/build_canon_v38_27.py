#!/usr/bin/env python3
"""project_canon_v38_27.json -- MINOR. R1-070: #46 re-ruled FAILS on Josiah's word, superseding R1-011;
the two judgment gates read an append-only record at the bytes they pin.

ccclxiv FIRST: v38_26 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map two subkeys are ADDED and
none moves. Every figure written here is computed from the committed files: the rulings gate, the quote
check and both judgment gates run in-process and must be GREEN; the four newest control records must be
all-as-expected and name the files they pin; every current FAILS must carry exactly one failure shape.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, copy, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_26.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_27.json")
SRC_MD5 = "1a54981b2f41b8e53621f37aebd94b2e"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "gate2"
DATE = "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = {"R1_070_rerule_gate2", "R1_progress_L3_after_R1_070"}

R1 = "adversarial_map_staging/r1/"
RULINGS = R1 + "R1_rulings.json"
RULINGS_PINNED = "3f1dfad54021d7920576c7bd4840b62f"
RGATE, RGATE_CTL = R1 + "r1_rulings_gate.py", R1 + "r1_rulings_gate_control_v0_3.json"
QCHECK = R1 + "r1_quote_check.py"
COLL, COLL_CTL = R1 + "r1_collision_list.py", R1 + "r1_collision_list_control_v0_3.json"
GATE1, GATE1_CTL, REC1 = R1 + "r1_judgments_gate.py", R1 + "r1_judgments_gate_control_v0_4.json", R1 + "R1_drafts_judgments.json"
GATE2, GATE2_CTL, REC2 = (R1 + "r1_v1_5_judgments_gate.py", R1 + "r1_v1_5_judgments_gate_control_v0_2.json",
                          R1 + "R1_v1_5_judgments.json")
GATE1_FROM, GATE2_FROM = "8b27cb997795c39c667c8841b3b6bcc5", "8572ae88d91e8eaaa51b8cdff88bacce"

HIS_WORD = "Proceed with all of your recommendations."
L4_COMMIT = "46b6f65"


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def control(rel, tool_rel, tool_key, pinned_key, pinned_rel):
    c = json.load(open(os.path.join(REPO, rel), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and all(x["as_expected"] for x in c["controls"]), rel
    assert c[tool_key] == f(tool_rel)["md5"] and c[pinned_key] == f(pinned_rel)["md5"], "%s is stale" % rel
    return dict(f(rel), file=rel, result="%d of %d as expected, the unmutated control first" % (
        len(c["controls"]), len(c["controls"])))


def main():
    raw = open(SRC, "rb").read()
    assert hashlib.md5(raw).hexdigest() == SRC_MD5, "SRC GUARD: v38_26 moved"
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_26 does not round-trip"
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
    for rel, rec_rel, name in ((GATE1, REC1, "g1"), (GATE2, REC2, "g2")):
        M = mod(rel, name)
        fl, info = M.check(os.path.join(REPO, rec_rel), REPO, M.committed_base())
        assert not fl, "%s RED: %s" % (rel, fl)
        assert any(x.startswith("pin rulings:") and "appended row" in x for x in info), "%s: rulings not grown?" % rel
    ctl = {"rulings_gate": control(RGATE_CTL, RGATE, "gate_md5", "rulings_md5", RULINGS),
           "collision_list": control(COLL_CTL, COLL, "tool_md5", "rulings_md5", RULINGS),
           "first_judgments_gate": control(GATE1_CTL, GATE1, "gate_md5", "judgments_md5", REC1),
           "second_judgments_gate": control(GATE2_CTL, GATE2, "gate_md5", "judgments_md5", REC2)}

    # ---------------------------------------------------------------- the row, and R1's totals after it
    rows = json.load(open(os.path.join(REPO, RULINGS), encoding="utf-8"))["rows"]
    new = rows[-1]
    assert (new["row"], new["n"], new["verdict"], new["supersedes"]) == ("R1-070", 46, "FAILS", "R1-011")
    assert new["ruled_by"]["josiah_verbatim"] == HIS_WORD and L4_COMMIT in new["ruled_by"]["on"]
    old = next(r for r in rows if r["row"] == "R1-011")
    assert (old["n"], old["verdict"], old["target"]) == (46, "HOLDS", new["target"])
    sup = {r["supersedes"] for r in rows if r.get("supersedes")}
    cur = {r["n"]: r for r in rows if r["row"] not in sup}
    assert len(cur) == 69 and len(rows) == 70
    tot = collections.Counter(r["verdict"] for r in cur.values())
    by_block = collections.defaultdict(collections.Counter)
    for r in cur.values():
        by_block[r["block"]][r["verdict"]] += 1
    by_block = {"block_%d" % k: dict(sorted(v.items())) for k, v in sorted(by_block.items())}
    assert dict(tot) == {"HOLDS": 23, "FAILS": 46}
    assert by_block == {"block_1": {"FAILS": 17, "HOLDS": 13}, "block_2": {"FAILS": 29, "HOLDS": 10}}

    shapes = copy.deepcopy(am["R1_progress_L3"]["failure_shapes_seat_s_reading"])
    assert 46 not in [n for v in shapes.values() for n in v["entries"]]
    shapes["route_to_bedrock"]["entries"].append(46)
    shaped = [n for v in shapes.values() for n in v["entries"]]
    fails_now = sorted(n for n, r in cur.items() if r["verdict"] == "FAILS")
    assert sorted(shaped) == fails_now and len(shaped) == len(set(shaped)), "every FAILS needs exactly one shape"
    j45 = next(r for r in json.load(open(os.path.join(REPO, REC1), encoding="utf-8"))["rows"]
               if r["kind"] == "draft" and r.get("n") == 45)
    assert (j45["id"], j45["verdict"]) == ("J-031", "ACCEPT")

    # ---------------------------------------------------------------- the blocks
    am["R1_070_rerule_gate2"] = {
        "status": "RULED. R1-070 supersedes R1-011: #46 FAILS. The disposition is not ruled: a drafting seat drafts "
                  "it, and a seat that did not draft it judges it (K258).",
        "his_words_verbatim": HIS_WORD,
        "on": "gate2's lean on #46 as R0142 presented it (row V-017 of %s): re-rule R1-011 FAILS, then a (d) at "
              "HR-14. The L4 session put it to him in chat, relayed his words to gate2 verbatim and recorded them in "
              "efilist %s's message, %s. The judgment the lean rests on (R0142's first ask) is adopted with it. "
              "R0142's third ask, queueing why-not-suicide's defender framing beside PQ-08, was not put to him; the "
              "L4 session queues it marked as gate2's lean." % (REC2, L4_COMMIT, DATE),
        "row": {"row": new["row"], "supersedes": new["supersedes"], "n": new["n"], "target": new["target"],
                "verdict": new["verdict"], "basis": new["basis"], "seat": new["seat"],
                "failure_shape_seat_s_reading": "route_to_bedrock"},
        "why": "The defender move says the recoil still has an object, the pro tanto worth of the lives the button "
               "ends. R1-011 held because the long's second horn answered it. L4's drafts, accepted by gate2 (%s), "
               "made #45 a (d) at that answering locus, which records the long's dismissal of the pro-existence "
               "recoil as cutting both ways and ending at a tie under HR-02. So the map now records, where the answer "
               "lives, that the recoil's object is not removed, which is what the answer needed (the L2 standard)."
               % j45["id"],
        "rulings": dict(f(RULINGS), file=RULINGS, rows=len(rows), entries_ruled=len(cur),
                        pinned_by_both_judgments=RULINGS_PINNED),
        "judgment_gates_read_pinned_bytes": {
            "law": "A judgment is checked against the bytes it judged. When a record it pins is append-only and "
                   "grows, the gate reads the pinned bytes back from git history, requires the growth to be "
                   "appended rows only (header unchanged, the pinned rows a prefix), and reads every judged "
                   "artifact at its pinned bytes, never at a later state.",
            "why_it_is_load_bearing": "Withhold the history and the second gate goes RED twice: on the pin, and on "
                                      "V-017, which names R1-011 as #46's current HOLDS. It was, when judged; R1-070, "
                                      "which the judgment itself led to, would otherwise convict the judgment of an "
                                      "error it did not make. Measured before this commit, not recorded as a control.",
            "append_only": {GATE1: [RULINGS], GATE2: [RULINGS, REC1]},
            "first_gate": dict(f(GATE1), file=GATE1, was=GATE1_FROM, control=ctl["first_judgments_gate"]),
            "second_gate": dict(f(GATE2), file=GATE2, was=GATE2_FROM, control=ctl["second_judgments_gate"]),
            "controls_added": "first gate C12 (the rulings grow by one row: GREEN) and C13 (a committed rulings row "
                              "edited: RED); second gate C13 and C15 (the rulings, and the first judgment record, "
                              "grow by one row: GREEN) and C14 (a committed rulings row edited: RED)",
            "not_used": "L4c's adversarial_map_staging/r1/pinned.py does the same lookup for L4's instruments; the "
                        "judge's gates carry their own copy, so a drafting seat's instrument change cannot move them",
        },
        "controls_regenerated_after_the_append": {
            "rulings_gate": ctl["rulings_gate"],
            "collision_list": ctl["collision_list"],
            "note": "L3's law: a control record that names the rulings md5 is regenerated when the rows change. "
                    "Only rulings_md5 and one row number in a failure line moved; the v0_2 records stay as committed.",
        },
        "next": "The L4 session drafts #46's (d) as v1_6 (lean HR-14, terminus-held-open; the alternative is HR-02 "
                "with #45 and #47), re-runs the knock-on measure against it, and sends it to gate2 to judge.",
    }
    am["R1_progress_L3_after_R1_070"] = {
        "status": "R1 stays COMPLETE: 69 of 69 entries ruled, in 70 rows. One entry's ruling moved.",
        "totals": dict(sorted(tot.items())),
        "by_block": by_block,
        "moved": {"n": 46, "from": "R1-011 HOLDS", "to": "R1-070 FAILS"},
        "failure_shapes_seat_s_reading": shapes,
        "shape_note_R1_070": "#46 joins route_to_bedrock under that shape's own definition: the (d) it routes to is "
                             "at the answering locus. The (d) is #45's, made by L4's drafting pass after R1 ruled "
                             "#46, so this is the first FAILS whose bedrock the map recorded after the ruling. The "
                             "other shapes and their entries are R1_progress_L3's, unchanged.",
        "read_by": "adversarial_map_staging/r1/r1_collision_list.py, which reads the newest R1_progress_L* block "
                   "that carries failure shapes. Without this block it lists #46 as blocked with its shape "
                   "unrecorded and leaves it out of its blocked count.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.27"
    d["canon_version_marker"] = "v38.27"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The L4 session (seat l) drafts #46's (d) under R1-070 (adversarial_map.R1_070_rerule_gate2) "
                      "as v1_6, lean HR-14, re-runs the knock-on measure against it, and a seat that did not draft it "
                      "(gate2) judges it (K258). The pin session (adversarial_map.pin_move_queue_v1_5, 16 rows, plus "
                      "the why-not-suicide defender framing the L4 session queues as gate2's lean) is his to declare "
                      "and does not wait on #46. Then R2, then the interconnection design.")
    nrs["rerule_R1_070_gate2"] = ("#46 re-ruled FAILS on his word ('%s'); R1: 69 of 69, HOLDS %d, FAILS %d. The two "
                                  "judgment gates now read the rulings at the bytes they judged."
                                  % (HIS_WORD, tot["HOLDS"], tot["FAILS"]))

    d["keyset_delta_ledger"]["v38_27_gate2"] = (
        "MINOR. keyset UNCHANGED at 42. Two adversarial_map subkey additions (R1_070_rerule_gate2, "
        "R1_progress_L3_after_R1_070); next_recommended_session re-pointed (session rewritten; rerule_R1_070_gate2 "
        "added); canon-meta; this note; one session_log_recent append. NO PIN. invariants, schemas, hazard_map and "
        "flagship_sidecars asserted byte-identical, and every other top-level key too.")
    d["session_log_recent"].append(
        "gate2 (%s; NO PIN): R1-070 appended to R1_rulings.json (%s), superseding R1-011: #46 FAILS, on '%s' (relayed "
        "by the L4 session, recorded at %s). R1 69 of 69: HOLDS %d, FAILS %d. Both judgment gates read an "
        "append-only record at its pinned bytes (first gate %s, second %s); four control records regenerated."
        % (DATE, f(RULINGS)["md5"][:8], HIS_WORD, L4_COMMIT, tot["HOLDS"], tot["FAILS"], f(GATE1)["md5"][:8],
           f(GATE2)["md5"][:8]))

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
    print("project_canon_v38_27.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  rulings %s: %d rows, HOLDS %d, FAILS %d | %s" % (f(RULINGS)["md5"][:8], len(rows), tot["HOLDS"],
                                                             tot["FAILS"], json.dumps(by_block, sort_keys=True)))


if __name__ == "__main__":
    main()
