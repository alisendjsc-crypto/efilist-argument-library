#!/usr/bin/env python3
"""project_canon_v38_20.json -- MINOR. L3: R1 COMPLETE. The 29 (a) entries L2 carried (phases B1-E) are ruled,
so all 69 are; the three reading rules they were ruled under are recorded; and what a drafting seat does next.

ccclxiv FIRST: v38_19 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map three subkeys are ADDED
and none moves. Every count is computed here from the rulings file, the evidence file and the map
(ccclxii); the rulings gate and the quote checker are run in-process and must be GREEN; the control
record must name this gate and this rulings file. His words are carried verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
R1 = os.path.join(REPO, "adversarial_map_staging", "r1")
sys.path.insert(0, R1)
import r1_rulings_gate as G
import r1_quote_check as Q

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_19.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_20.json")
SRC_MD5 = "e7f625232563f6876ceaa9f26aec9378"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L3_R1"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"
GATE = "adversarial_map_staging/r1/r1_rulings_gate.py"
CONTROL = "adversarial_map_staging/r1/r1_rulings_gate_control_v0_2.json"
CONTROL_V01 = "adversarial_map_staging/r1/r1_rulings_gate_control_v0_1.json"
CONTROL_V01_MD5 = "93871579c41ed7c8d3e93b6cace1f0e8"
DOSSIERS = "adversarial_map_staging/r1/r1_dossiers.py"
QUOTES = "adversarial_map_staging/r1/r1_quote_check.py"
KICKOFF = {"relay": "R0104", "md5": None}   # filled from the relay index below if present

# Josiah, in chat, 2026-09-25, answering both L3 batches and the three rules stated with them. Verbatim.
HIS_L3 = "Go with your recommendations on all of the above. Proceed as you wish."
# His words as the L2 kickoff quotes them (relay R0091). Verbatim; carried forward from v38_19.
HIS_HORIZON = ("I do want the adversarial's continuations and responses to be inter-connected eventually, "
               "but we want to do it well and right.")

# The three rules as the seat presented them in chat before he ruled (markdown stripped). Verbatim.
HUB_RULE = ("Sixteen entries route to benatar-asymmetry-attack#long. One of those is FAILS only when its move "
            "presses what the hub's own flags record. Those flags are the contested impersonal core (HR-03) and "
            "the suffering-load premise the hub never establishes. If the hub meets the move without resting on "
            "either, it holds. Routing to a flagged hub is not by itself a fail.")
K350_RULE = ("Where a move is normative consent-scepticism, the route through consent-incoherent is barred, and "
             "the entry then holds only if its other route meets the move. #59 is barred. #22, #54 and #58 are "
             "not, so their route is read on its merits.")
JOY_RULE = ("It covers routes into joy-outweighs-harms#long. That locus's own (d) concedes one case: when the "
            "person bearing the harms also gets the goods, the argument falls back on the asymmetry (HR-02). So a "
            "move about others' goods is met there, and a move about the created person's own goods ends at "
            "HR-02. On that reading #49 holds, and #43 and #64 fail.")

L2_ROWS = 40          # rows R1-001..R1-040, ruled at L2
L3_N = [21, 22, 26, 42, 53, 54, 62, 7, 14, 17, 52, 58, 59, 65,          # batch 1: B1, B2, C
        6, 23, 25, 34, 35, 43, 49, 57, 63, 64, 2, 37, 39, 50, 51]       # batch 2: D, E

# The seat's reading, not his words: what each FAILS is, and so what the drafting pass does with it.
SHAPES = {
    "route_to_bedrock": [60, 20, 16, 15, 8, 9, 10, 31, 33, 12, 13, 44, 45, 61, 47,            # L2
                         21, 54, 14, 17, 59, 65, 6, 23, 34, 35, 43, 57, 64, 2, 39],           # L3
    "answer_flagged_b": [67, 1, 11, 32, 48, 42, 62, 7, 50],
    "aggravation_s11_1": [5],
    "aggravation_cross_node": [63],
    "under_strength_move": [40],
    "routed_answer_silent": [22, 58, 25],
}
SHAPE_MEANS = {
    "route_to_bedrock": "The answer routed to is one the map itself records as ending at registered bedrock "
                        "(HR-02, HR-03, HR-04, HR-05, HR-06, HR-11, HR-14, or a (d) at the answering locus or a "
                        "sibling slot). Under the standard: reclassify to (d), routed to that bedrock; ships under "
                        "the terminus label with no new prose.",
    "answer_flagged_b": "The answer's load-bearing sentence carries a (b) the map already holds (at the answering "
                        "locus, or a sibling slot's (b) whose rule convicts it). Under the standard: waits on that "
                        "repair; a (d) instead if the repair itself ends at bedrock.",
    "aggravation_s11_1": "The node's own text concedes the move's premise (design section 11.1, aggravation): a (b) "
                         "repair at the slot.",
    "aggravation_cross_node": "NEW at L3. The node the entry routes to concedes the move's premise in its own "
                              "words (#63: economy-population#long calls the aging-care problem real, against "
                              "the target's 'not by individual people'). A (b) repair at the target sentence.",
    "under_strength_move": "The move stops short of its own payload; re-author it at full strength, then re-judge.",
    "routed_answer_silent": "NEW at L3. The routed locus does not engage the move: the answer the grounds describe "
                            "is argued in the grounds, or lives elsewhere, not in the routed text (L2's #47 basis). "
                            "The drafting seat re-routes to a locus that answers, repairs the target, or re-authors; "
                            "then a non-drafting seat judges.",
}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def relay_md5(rid):
    idx = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
    if not os.path.exists(idx):
        return None
    for line in open(idx, encoding="utf-8"):
        cols = line.rstrip("\n").split("\t")
        if len(cols) > 8 and cols[1] == "SENT" and cols[2] == rid:
            return cols[8]
    return None


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_19.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_19 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    fails, info = G.check(os.path.join(REPO, RULINGS), REPO, G.committed_base())
    assert not fails, "the rulings gate is RED: %s" % fails
    texts = Q.Texts()
    q_rows = Q.rulings_quotes()
    q_ok, q_fail = Q.check(q_rows, texts)
    assert not q_fail, "the quote check is RED: %s" % q_fail
    ctl = json.load(open(os.path.join(REPO, CONTROL), encoding="utf-8"))
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["controls"][0]["control"] == "C0"
    assert ctl["gate_md5"] == f(GATE)["md5"], "the control record ran against another gate"
    assert ctl["rulings_md5"] == f(RULINGS)["md5"], "the control record ran against another rulings file"
    assert f(CONTROL_V01)["md5"] == CONTROL_V01_MD5, "L2's control record moved"
    doc = json.load(open(os.path.join(REPO, RULINGS), encoding="utf-8"))
    ev = json.load(open(os.path.join(REPO, doc["evidence"]["file"]), encoding="utf-8"))
    mp = json.load(open(os.path.join(REPO, doc["map"]["file"]), encoding="utf-8"))["entries"]
    rows = doc["rows"]
    assert len(rows) == 69 and [r["n"] for r in rows[L2_ROWS:]] == L3_N, "L3's rows are not R1-041..R1-069 as ruled"
    assert all(r["ruled_by"]["josiah_verbatim"] == HIS_L3 for r in rows[L2_ROWS:]), "his words differ on a row"
    last = {}
    for r in rows:
        last[r["n"]] = r
    by_n = {e["n"]: e for e in ev["entries"]}
    held = sorted(n for n, r in last.items() if r["verdict"] == "HOLDS")
    failed = sorted(n for n, r in last.items() if r["verdict"] == "FAILS")
    carried = sorted(n for n in by_n if n not in last)
    assert not carried and len(held) + len(failed) == len(by_n) == 69, "R1 is not complete"
    assert sorted(sum(SHAPES.values(), [])) == failed, "the failure shapes do not partition the FAILS"
    l3_held = sorted(n for n in L3_N if last[n]["verdict"] == "HOLDS")
    l3_failed = sorted(n for n in L3_N if last[n]["verdict"] == "FAILS")
    seat_only = sorted(n for n in failed if last[n]["basis"] == "seat-reading")
    corpus_only = sorted(n for n in failed if last[n]["basis"] == "corpus-record")
    assert seat_only == [22, 40, 58], seat_only
    assert corpus_only == [63], corpus_only
    partly_seat = [25, 50, 54]
    assert all(last[n]["basis"] == "map-record" and "seat's reading" in last[n]["reason"] for n in partly_seat)

    def tally(pred, only=None):
        out = {}
        for n, e in sorted(by_n.items()):
            if not pred(e) or (only is not None and n not in only):
                continue
            p = out.setdefault(e["phase"], {"entries": 0, "HOLDS": 0, "FAILS": 0})
            p["entries"] += 1
            p[last[n]["verdict"]] += 1
        tot = {k: sum(p[k] for p in out.values()) for k in ("entries", "HOLDS", "FAILS")}
        return dict(sorted(out.items()), total=tot)
    block1 = tally(lambda e: e["phase"] in ("F", "G", "R"))
    block2 = tally(lambda e: e["phase"] not in ("F", "G", "R"))
    ruled_l3 = tally(lambda e: True, only=set(L3_N))
    total = tally(lambda e: True)

    # the hub, and the mechanical screen, over L3's 29
    hub = "benatar-asymmetry-attack#long"
    hub_l3 = [n for n in L3_N if hub in by_n[n]["answered_by"]]
    hub_failed = sorted(n for n in hub_l3 if last[n]["verdict"] == "FAILS")
    hub_held = sorted(n for n in hub_l3 if last[n]["verdict"] == "HOLDS")
    flagged = {}
    for x in mp:
        if x["class"] in ("b", "d"):
            flagged.setdefault(x["target_id"] + "#" + x["target_locus"], []).append(x)
    screened = sorted(n for n in L3_N if any(r in flagged for r in
                      by_n[n]["answered_by"] + [by_n[n]["target_id"] + "#" + by_n[n]["target_locus"]]))
    screen_failed = sorted(n for n in screened if last[n]["verdict"] == "FAILS")
    l3_map_record = sorted(n for n in l3_failed if last[n]["basis"] == "map-record")
    k350_barred = [59]
    k350_open = [22, 54, 58]
    kick_md5 = relay_md5(KICKOFF["relay"])

    # ---------------------------------------------------------------- adversarial_map: three additions
    am["R1_progress_L3"] = {
        "status": "R1 COMPLETE: %d of %d ruled (HOLDS %d, FAILS %d). L3 ruled the %d L2 carried (HOLDS %d, FAILS %d)."
                  % (len(last), len(by_n), len(held), len(failed), len(L3_N), len(l3_held), len(l3_failed)),
        "his_words_verbatim": HIS_L3,
        "on": "both L3 batches as presented (Batch 1: B1, B2, C, 14 entries; Batch 2: D, E, 15 entries) and the "
              "three reading rules stated with them (R1_rules_L3), in chat, 2026-09-25",
        "kickoff": {"relay": KICKOFF["relay"], "md5": kick_md5},
        "rulings": dict(f(RULINGS), file=RULINGS, rows=len(rows), rows_L3="R1-041..R1-069",
                        law="Append-only; a correction is a new row that supersedes. The evidence file's ruling "
                            "slots stay null on purpose: its builder rewrites them on every run (K351)."),
        "gate": dict(f(GATE), file=GATE, unchanged_since_L2=True,
                     controls="%d of %d as expected, the unmutated control first"
                              % (sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"])),
                     control_record_v0_2=dict(f(CONTROL), file=CONTROL,
                                              reproducible_under_forced_hash_seeds=True),
                     control_record_v0_1="unchanged, %s, as L2 left it" % CONTROL_V01_MD5),
        "instruments": {
            "dossiers": dict(f(DOSSIERS), file=DOSSIERS,
                             does="One markdown dossier per entry: node frame, anchor, move, grounds, the target "
                                  "locus and every answering locus in full, every map entry on the target node and "
                                  "each answering node (each (a) with its R1 ruling), every other (a) spending the "
                                  "same answer, the register bedrocks and canon records on the route (K224/K338, "
                                  "K350, the transhumanist ban, HR-14), and the mechanical screen. Judges nothing.",
                             reproducible_under_forced_hash_seeds=True),
            "quote_check": dict(f(QUOTES), file=QUOTES,
                                does="Asserts every quoted sentence is an exact substring of the corpus locus, map "
                                     "entry, canon path or register bedrock it names; --rulings checks every "
                                     "map_record quote in R1_rulings.json; --self-test runs 8 controls, the "
                                     "unmutated control first.",
                                rulings_quotes_verbatim="%d of %d" % (q_ok, len(q_rows))),
            "why": "L2's dossier builder and quote checker lived in scratch, so its method could not be reproduced "
                   "from the repo (R0104, step 1).",
            "sheets": "Two reading sheets presented, not committed; every quotation on them checked verbatim with "
                      "the committed checker: 83 of 83 (Batch 1) and 96 of 96 (Batch 2).",
        },
        "by_block": {"block_1_F_G_R": block1, "block_2_A_to_E": block2, "all_69": total["total"]},
        "ruled_at_L3": ruled_l3,
        "held": held,
        "failed": failed,
        "held_L3": l3_held,
        "failed_L3": l3_failed,
        "failed_resting_on_the_seat_s_reading_alone": seat_only,
        "failed_resting_partly_on_the_seat_s_reading": partly_seat,
        "failed_resting_on_the_corpus_s_own_text_not_a_map_entry": corpus_only,
        "failure_shapes_seat_s_reading": {k: {"entries": v, "means": SHAPE_MEANS[k]} for k, v in SHAPES.items()},
        "hub_rule_applied": {"routed_to": hub, "entries_L3": len(hub_l3), "FAILS": hub_failed, "HOLDS": hub_held},
        "k350_rule_applied": {"barred": k350_barred, "not_barred_read_on_merits": k350_open},
        "detection_rule_ccclxviii_applied": (
            "L3 failed %d of %d against L2's 22 of 40, so the rate was read as an instrument first. %d of L3's %d "
            "FAILS rest on map records (3 of them partly on the seat's reading: #25, #50, #54), #63 on the "
            "corpus's own text, and #22 and #58 on the seat's reading alone. Phases B1-E were written before the "
            "F, G, K338, K347 and K350 records that now flag their answers, and L2's own screen had marked %d of "
            "these %d entries as collisions before any was read (%d of those failed). Where the flagged point was "
            "only the objector's next move, the seat held, as L2 did at #30 and #36: #26, #49, #52."
            % (len(l3_failed), len(L3_N), len(l3_map_record), len(l3_failed), len(screened), len(L3_N),
               len(screen_failed))),
        "ruled_is_not_shipped": "Nothing reached /adversarial/ or /combined. The evidence file, the map, the corpus "
                                "and the pin are untouched.",
    }
    am["R1_rules_L3"] = {
        "his_words_verbatim": HIS_L3,
        "hub_rule": {"the_recommendation_he_adopted": HUB_RULE,
                     "why": "Sixteen of the 29 route to one flagged hub; without a stated rule the sixteen verdicts "
                            "swing on mood (R0104)."},
        "k350_rule": {"the_recommendation_he_adopted": K350_RULE,
                      "rests_on": "routing_constraint_consent_incoherent_K350; L2's #13 and #61 set the precedent."},
        "joy_outweighs_reading": {"the_recommendation_he_adopted": JOY_RULE,
                                  "rests_on": "the Phase D (d) at joy-outweighs-harms#long, which calls the "
                                              "dilemma decisive against the naive aggregator and concedes the "
                                              "intrapersonal horn relocates to the asymmetry (HR-02)."},
        "source": "the L3 chat messages that presented Batch 1 and Batch 2, 2026-09-25 (markdown stripped)",
    }
    am["R1_findings_L3"] = {
        "hr05_risk_frame": "HR-05's risk-without-an-antecedent-subject facet, registered by the (d) at "
                           "cherry-picking-worst#archetypeVariants.sophisticate, ended #23, #34 and #57: the "
                           "proxy-gamble frame the corpus leans on is the thing that (d) records as contested. #6 "
                           "met HR-05's other face, the stake symmetry registered at life-gift#long.",
        "moves_that_carry_their_own_answer": "The move field of #7, #14 and #62 contains a rebuttal as well as the "
                                             "objection, so a card would print the answer inside the objection "
                                             "(L2 found the same at #1). A drafting item whatever the verdict.",
        "grounds_describe_text_the_route_lacks": "#25 (the grounds say the hub grants suffering-mutability; the "
                                                 "hub never discusses it), #22 (act-structure is claimed of a "
                                                 "locus silent on determinism), #58 (the fair-play answer lives in "
                                                 "the grounds, not the routed loci). L2's #47 is the same shape.",
        "gate5_second_clauses_logged_not_ruled": "#53 (the long's own third point, pressed impersonally, is L2's "
                                                 "#10), #51 (the naturalistic-fallacy clause, open to the boomerang "
                                                 "registered at natural-reproduce#diagnosis), #52 (the grounds call "
                                                 "the total-utilitarian variant 'met arguendo' at the hub, which "
                                                 "the hub's own (d)s contradict). L2's #27 and #3 stand beside them.",
        "his_words_verbatim": HIS_L3,
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.20"
    d["canon_version_marker"] = "v38.20"
    d["last_updated_by_session"] = SESSION

    nrs = d["next_recommended_session"]
    nrs["session"] = ("A short build session first, then L4. BUILD (no pin): the validator rule adopted at L2 "
                      "(a_vs_own_record_collision_finding_L2) -- list every (a) whose answered_by locus or "
                      "same-node sibling carries a (b) or (d), plus the R1 verdict beside each, so the drafting "
                      "pass starts from a machine-made list. L4: the drafting pass over the %d FAILS by shape "
                      "(method_L3), judged by a seat that did not draft it (the gate2 role, K258). Then R2."
                      % len(failed))
    nrs["method_L3"] = {k: {"entries": v, "does": SHAPE_MEANS[k]} for k, v in SHAPES.items()}
    nrs["carried_L3"] = ("R1 carries nothing: 69 of 69 ruled. Carried beside it: the gate-5 second clauses "
                         "(R1_findings_L3; L2's #27 and #3); the moves that carry their own answer (#1, #7, #14, "
                         "#62); L1a's carries (ruling 1's rest, the two served-text repairs, readme_paths_gate.py's "
                         "curl.exe, instructions.md's stale counts); the unverified Boonin lead (a 2012 article or a "
                         "book; check a source before any repair).")
    nrs["after_R1_L3"] = ("R2, may a (b) be reader-facing and under what label, with a recommendation already at "
                          "interconnection_design_K350.b_class_reader_facing_OPEN_R2; then the interconnection "
                          "build, a design Josiah ratifies before a byte ships -- in his words, as R0091 quotes "
                          "them: '%s'" % HIS_HORIZON)

    d["keyset_delta_ledger"]["v38_20_L3"] = (
        "MINOR. keyset UNCHANGED at 42. Three adversarial_map subkey additions (R1_progress_L3, R1_rules_L3, "
        "R1_findings_L3); next_recommended_session re-pointed (session rewritten; method_L3, carried_L3, "
        "after_R1_L3 added); canon-meta; this note; one session_log_recent append. NO PIN: combined.html, "
        "corpus, jsx, the R1 evidence file and the map untouched. invariants, schemas, hazard_map and "
        "flagship_sidecars asserted byte-identical, and every other top-level key too.")

    d["session_log_recent"].append(
        "L3_R1 (%s; NO PIN): R1 COMPLETE, %d OF %d (a) ENTRIES RULED: HOLDS %d, FAILS %d. L3 ruled the %d L2 "
        "carried (B1-E) in his words '%s' -- HOLDS %d (#%s), FAILS %d -- under three reading rules he adopted "
        "with them (the hub rule, the K350 rule, the joy-outweighs reading). %d of L3's FAILS rest on map "
        "records; #63 on the corpus's own text; #22 and #58 on the seat's reading alone. Two new failure "
        "shapes: routed answer silent (#22, #25, #58) and cross-node aggravation (#63). Reading instruments "
        "committed: %s and %s. Rulings %s (gate %s, controls v0_2 %d of %d). Next: the validator-rule build, then "
        "the drafting pass over the %d FAILS, judged by a seat that did not draft."
        % (DATE, len(last), len(by_n), len(held), len(failed), len(L3_N), HIS_L3, len(l3_held),
           ", #".join(str(n) for n in l3_held), len(l3_failed), len(l3_map_record), DOSSIERS, QUOTES, RULINGS,
           GATE, sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]), len(failed)))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == {"R1_progress_L3", "R1_rules_L3", "R1_findings_L3"}
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_20.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset 42 held; adversarial_map +3; R1 %d of %d (HOLDS %d, FAILS %d); L3 %d (HOLDS %d, FAILS %d)"
          % (len(last), len(by_n), len(held), len(failed), len(L3_N), len(l3_held), len(l3_failed)))
    print("  block 1: %s" % json.dumps(block1["total"]))
    print("  block 2: %s" % json.dumps(block2["total"]))
    print("  hub (L3): %d routed, FAILS %s, HOLDS %s" % (len(hub_l3), hub_failed, hub_held))
    print("  screen (L3): %d of %d flagged, %d of those failed" % (len(screened), len(L3_N), len(screen_failed)))
    print("  quotes: rulings %d of %d verbatim; kickoff %s md5 %s" % (q_ok, len(q_rows), KICKOFF["relay"], kick_md5))


if __name__ == "__main__":
    main()
