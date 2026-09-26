#!/usr/bin/env python3
"""project_canon_v38_21.json -- MINOR. L3, second commit: the collision rule adopted at L2 is BUILT, so the
drafting pass starts from a machine-made list.

ccclxiv FIRST: v38_20 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map one subkey is ADDED and
none moves. Every count is computed here: the collision rule runs in-process and must be GREEN, the
committed list must be byte-identical to a fresh render, and the control record must name this tool and
this rulings file. His words are carried verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import hashlib, json, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
R1 = os.path.join(REPO, "adversarial_map_staging", "r1")
sys.path.insert(0, R1)
import r1_collision_list as C

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_20.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_21.json")
SRC_MD5 = "969cfd66f71136a76d2a62caae348896"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L3_build"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
TOOL = "adversarial_map_staging/r1/r1_collision_list.py"
LIST_JSON = "adversarial_map_staging/r1/r1_collision_list_v0_1.json"
LIST_MD = "adversarial_map_staging/r1/r1_collision_list_v0_1.md"
CONTROL = "adversarial_map_staging/r1/r1_collision_list_control_v0_1.json"
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"

# Josiah, in chat, 2026-09-25. Verbatim, typo included.
HIS_RULING = "Go with your recommendations on all of the above. Proceed as you wish."
HIS_FOCUS = ("The relays can be deferred for later since it's mostly aesthetic work or prioritized on your "
             "reecommendations. Focus on the substance for now.")
# The words he adopted the rule with at L2, as canon v38_19 records them (a_vs_own_record_collision_finding_L2).
HIS_L2 = "Go with your recommendations on all of the above."

UNCOLLIDED_FAILS_WHY = {
    22: "the seat's reading alone: the routed locus is silent on determinism",
    35: "the entry's own grounds, and a (d) on a third node, natural-reproduce#diagnosis",
    39: "a (d) on the answering node's other slot, slippery-slope-eugenics#short",
    40: "the seat's reading alone: the move stops short of its payload",
    58: "the seat's reading alone: the routed loci answer the version the move set aside",
    63: "the corpus's own text: the routed long concedes the move's premise",
}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_20.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_20 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    fails, rep = C.build(REPO)
    assert not fails, "the collision rule is RED: %s" % fails
    with tempfile.TemporaryDirectory() as t:
        C.emit(rep, t)
        for rel in (LIST_JSON, LIST_MD):
            fresh = open(os.path.join(t, os.path.basename(rel)), "rb").read()
            assert fresh == open(os.path.join(REPO, rel), "rb").read(), "%s is not what the tool renders" % rel
    ctl = json.load(open(os.path.join(REPO, CONTROL), encoding="utf-8"))
    assert ctl["controls"][0]["control"] == "C0" and all(c["as_expected"] for c in ctl["controls"])
    assert ctl["tool_md5"] == f(TOOL)["md5"], "the control record ran against another tool"
    assert ctl["rulings_md5"] == f(RULINGS)["md5"], "the control record ran against another rulings file"
    s = rep["summary"]
    items = rep["items"]
    assert s["a_entries"] == 69 and s["ruled"] == 69 and not s["unruled"], "R1 is not complete"
    unc_fails = sorted(i["n"] for i in items if not i["collided"] and i["r1"]["verdict"] == "FAILS")
    assert unc_fails == sorted(UNCOLLIDED_FAILS_WHY), unc_fails
    widen = sorted(i["n"] for i in items if not i["collided"] and i["for_reading_elsewhere_on_answering_nodes"])
    widen_fails = sorted(n for n in widen if n in unc_fails)
    n_fails = sum(len(v) for v in s["blocked_by_shape"].values())

    # ---------------------------------------------------------------- adversarial_map: one addition
    am["collision_rule_BUILT_L3"] = {
        "rule": "Every (a) whose answered_by locus or same-node sibling carries a (b) or (d) is listed for "
                "reading, and the list must be empty or ruled before any (a) card ships.",
        "adopted": "L2, his words '%s' (a_vs_own_record_collision_finding_L2: 'A build item, not a ruling "
                   "session's.')" % HIS_L2,
        "built_on_his_words_verbatim": {"ruling_both_L3_batches": HIS_RULING, "mid_session": HIS_FOCUS},
        "tool": dict(f(TOOL), file=TOOL,
                     exits_1_when="a collided (a) has no ruling, or the evidence file or the map is no longer at "
                                  "the md5 the rulings file names",
                     reports="each (a)'s collisions at its answering loci and on its own node, flags elsewhere on "
                             "its answering nodes for reading, its R1 row, its failure shape, and its ship status"),
        "list": {"json": dict(f(LIST_JSON), file=LIST_JSON), "md": dict(f(LIST_MD), file=LIST_MD),
                 "what_it_is": "The drafting pass's worklist: the 45 FAILS grouped by failure shape, each with "
                               "why it failed, the stronger line and its collisions; then the 24 HOLDS.",
                 "reproducible_under_forced_hash_seeds": True},
        "controls": dict(f(CONTROL), file=CONTROL,
                         result="%d of %d as expected, the unmutated control first"
                                % (sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]))),
        "counts": {"a_entries": s["a_entries"], "collided": s["collided"],
                   "collided_HOLDS": s["collided_HOLDS"], "collided_FAILS": s["collided_FAILS"],
                   "not_collided_HOLDS": s["uncollided_HOLDS"], "not_collided_FAILS": s["uncollided_FAILS"],
                   "ship_eligible": len(s["ship_eligible"]), "blocked": n_fails,
                   "blocked_by_shape": {k: len(v) for k, v in s["blocked_by_shape"].items()}},
        "finding_necessary_not_sufficient": (
            "The rule catches %d of the %d FAILS. The other %d were found only by reading: %s. %d collided entries "
            "held: the collision was read and found not to bear on the move. So the list is where reading "
            "starts, never where it stops."
            % (s["collided_FAILS"], n_fails, len(unc_fails),
               "; ".join("#%d (%s)" % (n, UNCOLLIDED_FAILS_WHY[n]) for n in unc_fails), s["collided_HOLDS"])),
        "lean_unruled": (
            "Widen the collision set to (b)/(d) on an answering node's other slots, L2's law made mechanical: it "
            "would add %d entries to the reading list (%s), %d of which failed (%s). The seat's lean, not a "
            "ruling; the adopted rule is built as adopted."
            % (len(widen), ", ".join("#%d" % n for n in widen), len(widen_fails),
               ", ".join("#%d" % n for n in widen_fails) or "none")),
        "validator_untouched": "adv_map_validator_v0_6.py is unchanged. The rule lives beside R1 because it reads "
                               "R1's rulings, which the map validator does not.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.21"
    d["canon_version_marker"] = "v38.21"
    d["last_updated_by_session"] = SESSION

    nrs = d["next_recommended_session"]
    nrs["session"] = ("L4: the drafting pass over the %d FAILS, starting from %s (grouped by failure shape; "
                      "method_L3 says what each shape gets), judged by a seat that did not draft it (the gate2 "
                      "role, K258). Then R2." % (n_fails, LIST_MD))
    nrs["build_done_L3"] = ("The validator-rule build recommended at L2 and L3 is done: "
                            "adversarial_map.collision_rule_BUILT_L3.")
    nrs["carried_L3_build"] = ("Relays deferred on his word ('%s'): R0104 and R0107 un-acked, no close relay, no "
                               "desk snapshot of the efilist CLAUDE.md for L3 yet. Waiting in seat l's queue, "
                               "unread: R0108 (argue to l, 'glyph_sigil_architecture_v1'), which the argue seat "
                               "says carries his request that the game's tier sigils and HUD marks come to the "
                               "library." % HIS_FOCUS)

    d["keyset_delta_ledger"]["v38_21_L3_build"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (collision_rule_BUILT_L3); "
        "next_recommended_session re-pointed (session rewritten; build_done_L3, carried_L3_build added); "
        "canon-meta; this note; one session_log_recent append. NO PIN: combined.html, corpus, jsx, the R1 "
        "evidence file, the rulings and the map untouched. invariants, schemas, hazard_map and flagship_sidecars "
        "asserted byte-identical, and every other top-level key too.")

    d["session_log_recent"].append(
        "L3_build (%s; NO PIN): THE COLLISION RULE ADOPTED AT L2 IS BUILT, on his words '%s' and '%s'. %s lists "
        "all %d (a) entries: %d collided (HOLDS %d, FAILS %d), %d not; %d ship-eligible on R1 HOLDS, %d blocked "
        "for the drafting pass by shape. It catches %d of the %d FAILS; %d were found only by reading (#%s). "
        "Controls %d of %d. The drafting pass starts from %s."
        % (DATE, HIS_RULING, HIS_FOCUS, TOOL, s["a_entries"], s["collided"], s["collided_HOLDS"],
           s["collided_FAILS"], s["a_entries"] - s["collided"], len(s["ship_eligible"]), n_fails,
           s["collided_FAILS"], n_fails, len(unc_fails), ", #".join(str(n) for n in unc_fails),
           sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]), LIST_MD))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == {"collision_rule_BUILT_L3"}
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_21.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset 42 held; adversarial_map +1; collided %d (HOLDS %d, FAILS %d); not collided %d"
          % (s["collided"], s["collided_HOLDS"], s["collided_FAILS"], s["a_entries"] - s["collided"]))
    print("  FAILS caught %d of %d; found only by reading: %s" % (s["collided_FAILS"], n_fails, unc_fails))
    print("  widening would add %s (failed among them: %s)" % (widen, widen_fails))


if __name__ == "__main__":
    main()
