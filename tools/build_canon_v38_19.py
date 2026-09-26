#!/usr/bin/env python3
"""project_canon_v38_19.json -- MINOR. L2: R1 ruled for 40 of the 69 (a) entries, and the standard that
decides what a FAILS becomes.

ccclxiv FIRST: v38_18 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map three subkeys are ADDED
and none moves. Every count is computed here from the rulings file, the evidence file and the map
(ccclxii), and the rulings gate is run in-process and must be GREEN. His words are carried verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
R1 = os.path.join(REPO, "adversarial_map_staging", "r1")
sys.path.insert(0, R1)
import r1_rulings_gate as G

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_18.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_19.json")
SRC_MD5 = "1da05cb8de285d0263cc724110044f4c"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L2_R1"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"
GATE = "adversarial_map_staging/r1/r1_rulings_gate.py"
CONTROL = "adversarial_map_staging/r1/r1_rulings_gate_control_v0_1.json"

# Josiah, in chat, 2026-09-25. Verbatim.
HIS_BLOCK1 = "Go with your recommendations on all of the above and proceed as you wish."   # on the Block 1 sample
HIS_BLOCK2 = "Go with your recommendations on all of the above."   # on Phase A, the other 18 of F, and the standard
# His words as the L2 kickoff quotes them (relay R0091, drafted by L1a). Verbatim from that relay.
HIS_HORIZON = ("I do want the adversarial's continuations and responses to be inter-connected eventually, "
               "but we want to do it well and right.")
R0091_MD5 = "9cf73a848974fdcb6a1cd23babac6d80"
# The seat's recommendation he adopted with HIS_BLOCK2, verbatim from the L2 message he answered.
STANDARD_REC = ("No. Reclassify those entries as (d), routed to the registered bedrock. They then ship under "
                "\"where this line terminates\" (already approved at K350), with no new prose. Entries whose "
                "answer carries a (b) wait for that repair.")
STANDARD_WHY = ("K350's class-asymmetry ruling already implies it, and it keeps every card claiming only what "
                "the map has established.")

# The seat's reading, not his words: what each FAILS is, and so what the standard sends it to.
SHAPES = {
    "route_to_bedrock": [60, 20, 16, 15, 8, 9, 10, 31, 33, 12, 13, 44, 45, 61, 47],
    "answer_flagged_b": [67, 1, 11, 32, 48],
    "aggravation_s11_1": [5],
    "under_strength_move": [40],
}
SHAPE_MEANS = {
    "route_to_bedrock": "The answer routed to is one the map itself records as ending at registered bedrock "
                        "(HR-03, HR-05, HR-06, HR-14, or a (d) at the answering locus). Under the standard: "
                        "reclassify to (d), routed to that bedrock; ships under the terminus label with no new prose.",
    "answer_flagged_b": "The answer's load-bearing sentence carries a (b) the map already holds. Under the standard: "
                        "waits on that repair; a (d) instead if the repair itself ends at bedrock.",
    "aggravation_s11_1": "The node's own text concedes the move's premise (design section 11.1, aggravation): a (b) "
                         "repair at the slot.",
    "under_strength_move": "The move stops short of its own payload; re-author it at full strength, then re-judge. "
                           "The one FAILS that rests on the seat's reading alone.",
}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_18.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_18 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    fails, info = G.check(os.path.join(REPO, RULINGS), REPO, G.committed_base())
    assert not fails, "the rulings gate is RED: %s" % fails
    ctl = json.load(open(os.path.join(REPO, CONTROL), encoding="utf-8"))
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["controls"][0]["control"] == "C0"
    assert ctl["gate_md5"] == f(GATE)["md5"], "the control record ran against another gate"
    assert ctl["rulings_md5"] == f(RULINGS)["md5"], "the control record ran against another rulings file"
    doc = json.load(open(os.path.join(REPO, RULINGS), encoding="utf-8"))
    ev = json.load(open(os.path.join(REPO, doc["evidence"]["file"]), encoding="utf-8"))
    mp = json.load(open(os.path.join(REPO, doc["map"]["file"]), encoding="utf-8"))["entries"]
    rows = doc["rows"]
    last = {}
    for r in rows:
        last[r["n"]] = r
    by_n = {e["n"]: e for e in ev["entries"]}
    held = sorted(n for n, r in last.items() if r["verdict"] == "HOLDS")
    failed = sorted(n for n, r in last.items() if r["verdict"] == "FAILS")
    carried = sorted(n for n in by_n if n not in last)
    assert len(held) + len(failed) + len(carried) == len(by_n) == 69
    assert sorted(sum(SHAPES.values(), [])) == failed, "the failure shapes do not partition the FAILS"
    seat_only = sorted(n for n in failed if last[n]["basis"] == "seat-reading")
    assert seat_only == SHAPES["under_strength_move"], seat_only

    def tally(pred):
        out = {}
        for n, e in sorted(by_n.items()):
            if not pred(e):
                continue
            p = out.setdefault(e["phase"], {"entries": 0, "HOLDS": 0, "FAILS": 0, "carried": 0})
            p["entries"] += 1
            p["carried" if n in carried else last[n]["verdict"]] += 1
        tot = {k: sum(p[k] for p in out.values()) for k in ("entries", "HOLDS", "FAILS", "carried")}
        return dict(sorted(out.items()), total=tot)
    block1 = tally(lambda e: e["phase"] in ("F", "G", "R"))
    block2 = tally(lambda e: e["phase"] not in ("F", "G", "R"))

    # the mechanical screen reported to Josiah: (a) entries with a (b)/(d) at an answering or own locus
    flagged = {}
    for x in mp:
        if x["class"] in ("b", "d"):
            flagged.setdefault(x["target_id"] + "#" + x["target_locus"], []).append(x)
    hub = "benatar-asymmetry-attack#long"
    screen = {"block_1": 0, "block_2": 0, "via_" + hub: 0}
    for e in ev["entries"]:
        own = e["target_id"] + "#" + e["target_locus"]
        refs = e["answered_by"] + [own]
        if any(r in flagged for r in refs):
            screen["block_1" if e["phase"] in ("F", "G", "R") else "block_2"] += 1
        if hub in e["answered_by"]:
            screen["via_" + hub] += 1
    carried_by_phase = {}
    for n in carried:
        carried_by_phase.setdefault(by_n[n]["phase"], []).append(n)
    carried_line = " · ".join("%s %s" % (ph, " ".join("#%d" % n for n in ns))
                              for ph, ns in sorted(carried_by_phase.items()))

    # ---------------------------------------------------------------- adversarial_map: three additions
    am["R1_progress_L2"] = {
        "status": "%d of %d ruled (HOLDS %d, FAILS %d); %d carried. Block 1 fully read; Block 2 read through Phase A."
                  % (len(last), len(by_n), len(held), len(failed), len(carried)),
        "his_words_verbatim": {"on_the_block_1_sample": HIS_BLOCK1,
                               "on_phase_A_the_other_18_of_F_and_the_standard": HIS_BLOCK2},
        "his_words_on_where_this_leads_verbatim": HIS_HORIZON,
        "source_of_that_quotation": "the L2 kickoff, relay R0091 (md5 %s), drafted by L1a on his words" % R0091_MD5,
        "rulings": dict(f(RULINGS), file=RULINGS, rows=len(rows),
                        law="Append-only; a correction is a new row that supersedes. The evidence file's ruling "
                            "slots stay null on purpose: its builder rewrites them on every run (K351)."),
        "gate": dict(f(GATE), file=GATE, controls="%d of %d as expected, the unmutated control first"
                     % (sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"])),
                     control_record=dict(f(CONTROL), file=CONTROL,
                                         reproducible_under_forced_hash_seeds=True)),
        "block_1_under_the_K346_ruling": block1,
        "block_2_before_it": block2,
        "held": held,
        "failed": failed,
        "carried": carried_line,
        "failed_resting_on_the_seat_s_reading_alone": seat_only,
        "failure_shapes_seat_s_reading": {k: {"entries": v, "means": SHAPE_MEANS[k]} for k, v in SHAPES.items()},
        "correction_carried_forward": (
            "L1 told Josiah (R0084 and in chat) that the record shows Phases A-E aimed at the most repairable "
            "reading. ccclxv_ruling_K346 had STRUCK that finding against its null; L2 said so in its first "
            "message. The two-block method stands on the narrower ground that A-E predate the explicit "
            "'strongest' ruling, and no FAILS here rests on the struck claim."),
        "detection_rule_ccclxviii_applied": (
            "The result departs sharply from the kickoff's expectation that most A-E entries would hold. Read "
            "as an instrument first: %d of the %d FAILS rest on the map's own (b)/(d) entries or canon records "
            "rather than the seat's reading; Block 1's sample was built from the hardest cases, but the 18 read "
            "after it split 9-9, so the rate is not a sampling artifact; and the one judgment the instrument "
            "adds -- an answer that ends at registered bedrock does not meet a move that presses that bedrock "
            "-- was put to Josiah as a ruling and adopted (R1_standard_ruling_L2)."
            % (len(failed) - len(seat_only), len(failed))),
        "ruled_is_not_shipped": "Nothing reached /adversarial/ or /combined. The evidence file, the map, the corpus "
                                "and the pin are untouched.",
    }
    am["R1_standard_ruling_L2"] = {
        "question": ("May an (a) say WE ANSWER THIS when the answer it routes to is one the map itself records as "
                     "ending at bedrock, or as flawed?"),
        "his_words_verbatim": HIS_BLOCK2,
        "the_recommendation_he_adopted": STANDARD_REC,
        "its_stated_reason": STANDARD_WHY,
        "grounded_in": "class_asymmetry_ruling_K350 (an (a) claims WE ANSWER THIS; a (d) claims only that a line "
                       "terminates at named bedrock) and terminus_label_pin_K353 (the label's strings).",
        "who_executes": "A drafting seat reclassifies or repairs; a seat that did not draft judges the result "
                        "(K258). L2 judged and drafted nothing.",
        "reach": "Binds the %d FAILS ruled here and every (a) ruled after it, the %d carried included."
                 % (len(failed), len(carried)),
    }
    am["a_vs_own_record_collision_finding_L2"] = {
        "finding": ("The map contradicts itself. In %d of the %d FAILS an (a) routes WE ANSWER THIS to an answer "
                    "the map's own entries (a (b) or (d) at the answering locus, at a sibling slot of the same "
                    "node, or in the answering text itself) or canon records (HR-14, the K338 withdrawal, the "
                    "K350 routing constraint) already record as ending at bedrock or as flawed."
                    % (len(failed) - len(seat_only), len(failed))),
        "two_mechanisms": {
            "phase_A": "Written at K222, before B1, B2, F, the K338 withdrawal and the K350 constraint found "
                       "bedrock at the loci it routes to. The later map learned what the early (a)s never absorbed.",
            "phase_F": "One slot of a node classed (d), and the node's other slots classed (a) and routed to the "
                       "argument that (d) says ends at bedrock: benatar-asymmetry-attack, antinatalism-misanthropic, "
                       "ai-fear, why-not-suicide.",
        },
        "mechanical_screen": ("(a) entries with a (b) or (d) at an answering locus or at their own locus: %d of %d "
                              "in Block 1, %d of %d in Block 2; %d of the 69 route through %s. It over-flags a hub "
                              "and misses sibling-slot conflicts (#60, #16 were found at siblings). A reading list, "
                              "not a verdict."
                              % (screen["block_1"], block1["total"]["entries"], screen["block_2"],
                                 block2["total"]["entries"], screen["via_" + hub], hub)),
        "recommendation_adopted": ("A build session adds a validator rule: every (a) whose answered_by locus or "
                                   "same-node sibling carries a (b) or (d) is listed for reading, and the list must "
                                   "be empty or ruled before any (a) card ships. A build item, not a ruling "
                                   "session's."),
        "his_words_verbatim": HIS_BLOCK2,
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.19"
    d["canon_version_marker"] = "v38.19"
    d["last_updated_by_session"] = SESSION

    nrs = d["next_recommended_session"]
    nrs["session"] = ("L3: R1 Block 2, phases B1-E (%d entries), read one by one with the L2 collision check in "
                      "every dossier; then the drafting-seat pass on the %d FAILS under R1_standard_ruling_L2, "
                      "judged by a seat that did not draft it; then R2." % (len(carried), len(failed)))
    nrs["method_L2"] = ("Phase A failed entries, so by R1_method_ruling_L1a's decision rule the rest of Block 2 is "
                        "read entry by entry. Before judging each, list every (b) or (d) on its answering loci and on "
                        "its own node's other slots, and every canon record on those loci (HR-14, K338, K350). An (a) "
                        "whose answer the map itself records as ending at bedrock, or as flawed, does not hold "
                        "(R1_standard_ruling_L2).")
    nrs["carried_L2"] = carried_line
    nrs["after_R1_L2"] = ("Re-authoring for the FAILS (a drafting session, then a non-drafting judge); the "
                          "validator rule in a_vs_own_record_collision_finding_L2 (a build session); R2, may a (b) be "
                          "reader-facing and under what label, with a recommendation already at "
                          "interconnection_design_K350.b_class_reader_facing_OPEN_R2; then the interconnection build, "
                          "a design Josiah ratifies before a byte ships -- in his words, as R0091 quotes them: '%s'"
                          % HIS_HORIZON)

    d["keyset_delta_ledger"]["v38_19_L2"] = (
        "MINOR. keyset UNCHANGED at 42. Three adversarial_map subkey additions (R1_progress_L2, "
        "R1_standard_ruling_L2, a_vs_own_record_collision_finding_L2); next_recommended_session re-pointed "
        "(session rewritten; method_L2, carried_L2, after_R1_L2 added); canon-meta; this note; one "
        "session_log_recent append. NO PIN: combined.html, corpus, jsx, the R1 evidence file and the map "
        "untouched. invariants, schemas, hazard_map and flagship_sidecars asserted byte-identical, and every "
        "other top-level key too.")

    d["session_log_recent"].append(
        "L2_R1 (%s; NO PIN): R1 RULED FOR %d OF %d (a) ENTRIES, in his words '%s' (the Block 1 sample) and '%s' "
        "(Phase A, the other 18 of F, and the standard). Block 1 fully read, %d: HOLDS %d, FAILS %d. Block 2 "
        "Phase A, %d: HOLDS %d, FAILS %d. Carried: %d (B1-E). %d of the %d FAILS are contradicted by the map's "
        "own records; #%s rests on the seat's reading alone. STANDARD RULED: an (a) may not say WE ANSWER THIS "
        "where the map records its answer as ending at bedrock or as flawed; such entries become (d)s under the "
        "terminus label or wait on their (b) repair. Rulings in %s (append-only; gate %s, controls %d of %d). "
        "L1's struck A-E premise corrected forward in L2's first message."
        % (DATE, len(last), len(by_n), HIS_BLOCK1, HIS_BLOCK2,
           block1["total"]["entries"], block1["total"]["HOLDS"], block1["total"]["FAILS"],
           block2["A"]["entries"], block2["A"]["HOLDS"], block2["A"]["FAILS"], len(carried),
           len(failed) - len(seat_only), len(failed), ", #".join(str(n) for n in seat_only),
           RULINGS, GATE, sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"])))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == {"R1_progress_L2", "R1_standard_ruling_L2",
                                        "a_vs_own_record_collision_finding_L2"}
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_19.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset 42 held; adversarial_map +3; ruled %d (HOLDS %d, FAILS %d), carried %d"
          % (len(last), len(held), len(failed), len(carried)))
    print("  block 1: %s" % json.dumps(block1["total"]))
    print("  block 2: %s" % json.dumps(block2["total"]))
    print("  screen: %s" % json.dumps(screen))
    print("  carried: %s" % carried_line)


if __name__ == "__main__":
    main()
