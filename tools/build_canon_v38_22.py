#!/usr/bin/env python3
"""project_canon_v38_22.json -- MINOR. L3, third commit: on Josiah's word the collision rule is WIDENED (v0_2), the
drafting pass and a parallel design lane are set up, and the next session is re-pointed.

ccclxiv FIRST: v38_21 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map one subkey is ADDED and
none moves. The widened rule runs in-process and must be GREEN; the committed v0_2 list must equal a
fresh render; v0_1 must still reproduce from the same tool; the control record must name this tool and
this rulings file. His words are carried verbatim, typos included.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import hashlib, json, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
R1 = os.path.join(REPO, "adversarial_map_staging", "r1")
sys.path.insert(0, R1)
import r1_collision_list as C

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_21.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_22.json")
SRC_MD5 = "53379874833efe74c588a5b241dfa30f"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L3_widen"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
TOOL = "adversarial_map_staging/r1/r1_collision_list.py"
V02_JSON = "adversarial_map_staging/r1/r1_collision_list_v0_2.json"
V02_MD = "adversarial_map_staging/r1/r1_collision_list_v0_2.md"
V01_JSON = "adversarial_map_staging/r1/r1_collision_list_v0_1.json"
V01_MD = "adversarial_map_staging/r1/r1_collision_list_v0_1.md"
V01_MD5 = {"json": "4ca417f18c47530099282d9d86947e70", "md": "0f849e4126c77a9ecc0d549ecb3f918d"}
CONTROL = "adversarial_map_staging/r1/r1_collision_list_control_v0_2.json"
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"

# Josiah, in chat, 2026-09-25, one message. Verbatim, typos and spacing included.
HIS_PROCEED = "Proceed with your recommendations on all front's."
HIS_QUESTION = ("DO you think a sigil  / design architecture session would be warranted in its own isolated session "
                "while the meat of the library presses on?")
# The seat's recommendations he answered, verbatim from the L3 message he replied to (markdown stripped).
REC_WIDEN = ("Widen the automatic check to cover the other slots of the node an answer routes to. Lean: yes. It would "
             "have caught #39 and #58 as well, both failures, at the cost of two more entries to read.")
REC_L4 = ("The drafting pass (L4). Lean: a fresh session, starting from the worklist, with a different session "
          "judging the drafts.")
REC_R2 = "R2, then the interconnection design. Lean: after L4."
REC_BOOKKEEPING = ("Lean: clear all of it in about a minute at the start of the next library session, or now if you "
                   "give the word.")
READ_ONLY = [22, 35, 40, 63]


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_21.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_21 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    fails, rep = C.build(REPO, "v0_2")
    assert not fails, "the widened collision rule is RED: %s" % fails
    fails1, rep1 = C.build(REPO, "v0_1")
    assert not fails1
    with tempfile.TemporaryDirectory() as t:
        C.emit(rep, t)
        for rel in (V02_JSON, V02_MD):
            fresh = open(os.path.join(t, os.path.basename(rel)), "rb").read()
            assert fresh == open(os.path.join(REPO, rel), "rb").read(), "%s is not what the tool renders" % rel
    assert f(V01_JSON)["md5"] == V01_MD5["json"] and f(V01_MD)["md5"] == V01_MD5["md"], "the v0_1 list moved"
    ctl = json.load(open(os.path.join(REPO, CONTROL), encoding="utf-8"))
    assert ctl["controls"][0]["control"] == "C0" and all(c["as_expected"] for c in ctl["controls"])
    assert ctl["tool_md5"] == f(TOOL)["md5"], "the control record ran against another tool"
    assert ctl["rulings_md5"] == f(RULINGS)["md5"], "the control record ran against another rulings file"
    s, s1 = rep["summary"], rep1["summary"]
    items = rep["items"]
    c1 = {i["n"] for i in rep1["items"] if i["collided"]}
    added = sorted(i["n"] for i in items if i["collided"] and i["n"] not in c1)
    assert added == [39, 58], added
    read_only = sorted(i["n"] for i in items if not i["collided"] and i["r1"]["verdict"] == "FAILS")
    assert read_only == READ_ONLY, read_only
    n_fails = sum(len(v) for v in s["blocked_by_shape"].values())

    # ---------------------------------------------------------------- adversarial_map: one addition
    am["collision_rule_WIDENED_L3"] = {
        "his_words_verbatim": HIS_PROCEED,
        "the_recommendation_he_adopted": REC_WIDEN,
        "rule_v0_2": C.RULE_TEXT["v0_2"],
        "tool": dict(f(TOOL), file=TOOL, default_rule="v0_2",
                     v0_1_still_reproduces="--rule v0_1 re-renders the committed v0_1 list byte for byte except the "
                                           "canon filename it names (v38_20 then, the current canon now), whose "
                                           "failure shapes are unchanged"),
        "list_v0_2": {"json": dict(f(V02_JSON), file=V02_JSON), "md": dict(f(V02_MD), file=V02_MD),
                      "reproducible_under_forced_hash_seeds": True},
        "list_v0_1": "kept as committed, %s / %s; not superseded in place" % (V01_MD5["json"][:8], V01_MD5["md"][:8]),
        "controls": dict(f(CONTROL), file=CONTROL,
                         result="%d of %d as expected, the unmutated control first; C5 proves the widening "
                                "reaches an entry v0_1 does not"
                                % (sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]))),
        "counts_v0_2": {"collided": s["collided"], "collided_HOLDS": s["collided_HOLDS"],
                        "collided_FAILS": s["collided_FAILS"], "not_collided_HOLDS": s["uncollided_HOLDS"],
                        "not_collided_FAILS": s["uncollided_FAILS"]},
        "counts_v0_1": {"collided": s1["collided"], "collided_FAILS": s1["collided_FAILS"]},
        "what_the_widening_added": "#39 and #58, both FAILS; no HOLDS were added to the reading list.",
        "found_only_by_reading": "%d of the %d FAILS: %s. A mechanical rule cannot reach a silent route (#22), a "
                                 "record on a third node (#35), a stopped-short move (#40) or a concession in plain "
                                 "corpus text (#63); reading stays mandatory."
                                 % (len(read_only), n_fails, ", ".join("#%d" % n for n in read_only)),
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.22"
    d["canon_version_marker"] = "v38.22"
    d["last_updated_by_session"] = SESSION

    nrs = d["next_recommended_session"]
    nrs["session"] = ("L4: the drafting pass over the %d FAILS, starting from %s (grouped by failure shape; "
                      "method_L3 says what each shape gets), judged by a seat that did not draft it (the gate2 role, "
                      "K258). In parallel and isolated: the design lane (parallel_lane_design_L3). Then R2, then the "
                      "interconnection design." % (n_fails, V02_MD))
    nrs["ruled_L3_close"] = {
        "his_words_verbatim": HIS_PROCEED,
        "adopted": {"widen_the_check": REC_WIDEN, "drafting_pass": REC_L4, "r2": REC_R2,
                    "deferred_bookkeeping": REC_BOOKKEEPING},
    }
    nrs["parallel_lane_design_L3"] = {
        "his_question_verbatim": HIS_QUESTION,
        "the_seat_s_answer": ("Yes: its own session, now, in parallel with L4, isolated in its own git worktree on "
                              "its own branch. It shares nothing with the drafting pass but the repository, the canon "
                              "file and the served tree; so it bumps no canon, touches nothing under "
                              "adversarial_map_staging/ and never touches site/combined.html (any flagship use is a "
                              "declared pin move); /libraries deploys on push to main, so it shows him a preview and "
                              "merges on his word."),
        "acted_on": "his standing default that the seat's recommendations proceed unless he says otherwise, and "
                    "'%s'" % HIS_PROCEED,
        "inputs": "R0108 (argue to l, glyph_sigil_architecture_v1) and R0107; the grids in argue's "
                  "design/tier_sigils_v0/sigils.json at argue 6fb26e1 (md5 b97acd2b), copied from the file, never "
                  "from a render; L1a's note that a full ladder with its top rung lit is pixel-identical to the "
                  "flagship favicon.",
    }
    nrs["carried_L3_build"] = ("Cleared at L3's close: R0104 and R0107 acked; the close relay and the desk snapshot "
                               "follow this commit. R0108 goes to the design lane unread by L3.")

    d["keyset_delta_ledger"]["v38_22_L3_widen"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (collision_rule_WIDENED_L3); "
        "next_recommended_session re-pointed (session rewritten; ruled_L3_close and parallel_lane_design_L3 added; "
        "carried_L3_build updated); canon-meta; this note; one session_log_recent append. NO PIN. invariants, "
        "schemas, hazard_map and flagship_sidecars asserted byte-identical, and every other top-level key too.")

    d["session_log_recent"].append(
        "L3_widen (%s; NO PIN): on his words '%s' the collision rule is WIDENED to an answering node's other slots "
        "(v0_2): %d collided (HOLDS %d, FAILS %d), adding #39 and #58; it now catches %d of the %d FAILS, and %s "
        "were found only by reading. v0_1 kept. His question, verbatim: '%s' The seat's answer: yes, an isolated "
        "parallel design lane (worktree, no canon bump, no pin, merge on his word). L4, the drafting pass, starts "
        "from %s."
        % (DATE, HIS_PROCEED, s["collided"], s["collided_HOLDS"], s["collided_FAILS"], s["collided_FAILS"], n_fails,
           ", ".join("#%d" % n for n in read_only), HIS_QUESTION, V02_MD))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == {"collision_rule_WIDENED_L3"}
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_22.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  v0_2: collided %d (HOLDS %d, FAILS %d); added %s; read-only FAILS %s"
          % (s["collided"], s["collided_HOLDS"], s["collided_FAILS"], added, read_only))


if __name__ == "__main__":
    main()
