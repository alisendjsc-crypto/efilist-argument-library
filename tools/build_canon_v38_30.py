#!/usr/bin/env python3
"""project_canon_v38_30.json -- MINOR. L5, the declared pin session (R0150), phase 1: his word on gate2's v1_6
judgment (R0164); the pin-move queue with PQ-17 naming both sentences (W-004); every live instrument reads
the corpus at the md5 its record pins, rehearsed against an edited corpus.

ccclxiv FIRST: v38_29 is round-tripped at the serialization this file emits BEFORE anything is derived.
v38_29 is read at its md5 from the working tree or git history, so this builder still runs after the rename
convention removes the file (the law gate2's third stratum recorded).

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map three subkeys are ADDED and
none moves. In-process: the rulings gate, the quote check and gate2's three judgment gates must be GREEN;
the queue's sentences are measured on all three surfaces; every instrument's before and after md5 is read
from git and disk; the rehearsal record must be GREEN and cover exactly this queue's sentences.

  python3 tools/build_canon_v38_30.py                 # write project_canon_v38_30.json
  python3 tools/build_canon_v38_30.py --provisional   # the same, without the rehearsal (it reads this queue)
  python3 tools/build_canon_v38_30.py --out <dir>     # emit elsewhere

Repo-relative.
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
PROVISIONAL = "--provisional" in sys.argv
SRC_REL, SRC_MD5 = "project_canon_v38_29.json", "ca1a0bb75ee8fe56344104e35e011751"
OUT = os.path.join(OUT_DIR, "project_canon_v38_30.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L5", "2026-09-26"
BASE = "09289dd2c2f8b730fa7df73a84e349f8ad53983d"   # efilist HEAD when L5 opened
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["his_word_on_v1_6_judgment_R0164", "pin_move_queue_L5", "instruments_read_pinned_corpus_L5"]

S, R1 = "adversarial_map_staging/", "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, S, "r1"))
import pinned  # noqa: E402

CORPUS = "efilist_argument_library_v4_0_0.json"
PRE_PIN = "04bf6482aa0374ee92a81c1d55ec41f8"
SURFACES = {CORPUS: PRE_PIN, "efilist_argument_library_v4_0_0.jsx": "b196548b6eb39065842d62292acca89f",
            "site/combined.html": "006aa9833f7a8b103ad27a289ab22fa9"}   # the three at the pre-pin release, v4.1.2
JUDG3 = R1 + "R1_v1_6_judgments.json"
R0164 = {"relay": "R0164", "md5": "d677e708008341aaf9cf8892292730da", "from": "gate2", "to": "l"}
R0154 = {"relay": "R0154", "md5": "629edd7f2a5def402c0b52340507afce", "from": "gate2", "to": "josiah"}
R0150 = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2", "from": "gate2", "to": "l"}
HIS_WORD = "Go with your recommendations."
ANALOGY = ("Just as one violent actor does not represent environmentalism, an eliminationist adherent does not "
           "convert the consent-and-asymmetry argument into a suicide license.")

HELPER = R1 + "pinned.py"
INSTRUMENTS = [  # (file, what it reproduces or checks)
    (S + "build_assembly_v1_4.py", "map v1_4"),
    (S + "build_assembly_v1_5.py", "map v1_5"),
    (S + "build_assembly_v1_6.py", "map v1_6"),
    (S + "build_phaseF.py", "the Phase F fragment"),
    (S + "build_phaseF_register.py", "the Phase F defect register"),
    (S + "build_phaseR.py", "the Phase R fragment"),
    (S + "controls_assembly_v1_3.py", "map v1_2's reproduction (its farm now links the pinned corpus)"),
    (S + "controls_assembly_v1_4.py", "gate: v1_4's controls (stages the pinned corpus in scratch)"),
    (S + "controls_v1_5.py", "gate: v1_5's controls (stages the pinned corpus in scratch)"),
    (S + "controls_v1_6.py", "gate: v1_6's controls (stages the pinned corpus in scratch)"),
    (S + "controls_phaseF.py", "the Phase F class control"),
    (S + "controls_phaseF_proper.py", "the Phase F proper control"),
    (S + "measure_ccclxv_v0_1.py", "the ccclxv measurement"),
    (S + "measure_k348_v0_1.py", "the K348 measurement"),
    (S + "measure_k349.py", "the K349 measurement"),
    (R1 + "measure_r1_v0_1.py", "the R1 evidence"),
    (S + "render_wing_v0_1.py", "the served /adversarial/ page"),
    (R1 + "r1_quote_check.py", "gate: corpus: quotes resolve at the md5 the R1 evidence pins; Texts(corpus_md5=) names another"),
    (R1 + "r1_dossiers.py", "the R1 dossiers"),
    (R1 + "r1_draft_dossiers.py", "gate2's draft dossiers"),
    (R1 + "r1_knock_on_dossiers.py", "gate2's knock-on dossiers (also reads the rulings at 3f1dfad5, the md5 the v1_5 judgment pins)"),
]
LINEAGE = [S + "build_assembly_v1_1.py", S + "build_assembly_v1_2.py", S + "build_assembly_v1_3.py"]
FARM, REHEARSE, REHEARSAL = "tools/pinned_farm.py", "tools/rehearse_pin.py", "tools/pin_rehearsal_v0_1.json"
GATE2 = [  # gate2's three judgment gates and their controls: verified, never edited here
    (R1 + "r1_judgments_gate.py", "5837a2686b1762bca363dae9955a7880", R1 + "r1_judgments_gate_control_v0_5.json"),
    (R1 + "r1_v1_5_judgments_gate.py", "6fabef3b520c93c7e4a0b25e8865b78f", R1 + "r1_v1_5_judgments_gate_control_v0_3.json"),
    (R1 + "r1_v1_6_judgments_gate.py", "8631bdf248ca779edeb747fd02b9f870", R1 + "r1_v1_6_judgments_gate_control_v0_1.json"),
]


def md5b(b):
    return hashlib.md5(b).hexdigest()


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": md5b(b), "bytes": len(b)}


def at_base(rel):
    r = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (BASE, rel)], capture_output=True)
    assert r.returncode == 0, "%s is not in %s" % (rel, BASE[:7])
    return r.stdout


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def locus_text(corpus, locus):
    oid, loc = locus.split("#")
    o = next(x for x in corpus["objections"] if x["id"] == oid)
    r = o["responses"]
    if loc.startswith("archetypeVariants."):
        return r["archetypeVariants"][loc.split(".", 1)[1]]
    return r[loc] if loc in r else o[loc]


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_29 does not round-trip"
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
    texts = Q.Texts()
    assert texts.corpus_md5 == PRE_PIN
    q_ok, q_fail = Q.check(q_rows, texts)
    assert not q_fail and q_ok == len(q_rows), "QUOTE CHECK RED: %s" % q_fail
    g2 = []
    for i, (gate, want, ctl) in enumerate(GATE2):
        assert f(gate)["md5"] == want, "%s moved: gate2's gates are not this session's to edit" % gate
        rec_rel = (R1 + "R1_drafts_judgments.json", R1 + "R1_v1_5_judgments.json", JUDG3)[i]
        M = mod(gate, "g%d" % i)
        fl, _ = M.check(os.path.join(REPO, rec_rel), REPO, M.committed_base())
        assert not fl, "%s RED: %s" % (gate, fl)
        c = json.load(open(os.path.join(REPO, ctl), encoding="utf-8"))
        assert c["controls"][0]["control"] == "C0" and all(x["as_expected"] for x in c["controls"]), ctl
        g2.append(dict(f(gate), file=gate, control=dict(f(ctl), file=ctl, result="%d of %d as expected" % (
            len(c["controls"]), len(c["controls"])))))

    # ---------------------------------------------------------------- his word (R0164)
    j3 = json.load(open(os.path.join(REPO, JUDG3), encoding="utf-8"))
    assert f(JUDG3)["md5"] == "fa89adc9dcc8bef39795bc830efdc427"
    w004 = next(r for r in j3["rows"] if r["id"] == "W-004")
    w007 = next(r for r in j3["rows"] if r["id"] == "W-007")
    assert w004["verdict"] == "AMEND" and w004["row_id"] == "PQ-17"
    assert any(q["quote"] == ANALOGY for q in w004["quotes"]), "W-004 does not quote the analogy"
    am["his_word_on_v1_6_judgment_R0164"] = {
        "his_words_verbatim": HIS_WORD,
        "said": "2026-09-26 15:53 America/Phoenix, in chat to gate2",
        "answers": R0154,
        "relay": R0164,
        "adopts": [
            "gate2's judgment of v1_6 (%s %s): W-001 #46's (d) at HR-14, terminus-held-open, ACCEPT; W-002 register "
            "v0_7's delta ACCEPT; W-003 the knock-on measure (0 HOLDS) CONFIRM; W-005 the pin session's declaration "
            "CONFIRM; and the recommendations in findings W-006 (no change now for the pro tanto residual) and W-007 "
            "(the knock-on list carries every entry anchored inside a repaired sentence)." % (JUDG3, f(JUDG3)["md5"][:8]),
            "W-004: PQ-17 names both sentences of why-not-suicide's defender slot, the 'grabbed, not produced' "
            "sentence and the lone-actor analogy that follows it, which carries #4's map anchor.",
        ],
        "so": "W-004 and W-007 are ruled, no longer defaults. adversarial_map.R1_v1_6_judgment_gate2 stays as written "
              "(it says judged, not ruled, which was true when written). The corrected row is pin_move_queue_L5's "
              "PQ-17. Nothing else moves on this word: the pin move waits for his word on the drafted repairs, after "
              "gate2 judges them.",
    }

    # ---------------------------------------------------------------- the queue, PQ-17 corrected (W-004)
    corpus_pre = json.loads(pinned.bytes_at(REPO, CORPUS, PRE_PIN).decode("utf-8"))
    surf = {s: pinned.bytes_at(REPO, s, m).decode("utf-8") for s, m in SURFACES.items()}
    enc = lambda s: json.dumps(s, ensure_ascii=False)[1:-1]
    src = am["pin_move_queue_v1_6"]
    rows = []
    for r in src["rows"]:
        r2 = {}
        for k, v in r.items():
            if k == "sentence":
                r2["sentences"] = [v, ANALOGY] if r["id"] == "PQ-17" else [v]
            else:
                r2[k] = v
        if r["id"] == "PQ-17":
            r2["corrected"] = ("W-004 (%s), ruled on his word (R0164): v1_6's row named the first sentence only; "
                               "R1-024 conceded the second, the lone-actor analogy, by name, and it carries #4's own "
                               "map anchor ('%s'). The repair keeps that clause's claim, or #4 is re-judged against the "
                               "repaired text; #4 is on the knock-on list either way."
                               % (JUDG3, "an eliminationist adherent does not convert the consent-and-asymmetry "
                                         "argument into a suicide license"))
        text = locus_text(corpus_pre, r["locus"])
        pos = []
        for s in r2["sentences"]:
            assert text.count(s) == 1, (r["id"], "not once in its locus")
            for name, t in surf.items():
                assert t.count(enc(s)) == 1, (r["id"], name, t.count(enc(s)))
            pos.append(text.index(s))
        assert pos == sorted(pos), (r["id"], "sentences out of order")
        rows.append(r2)
    assert [r["id"] for r in rows] == ["PQ-%02d" % i for i in range(1, 18)]
    n_sent = sum(len(r["sentences"]) for r in rows)
    am["pin_move_queue_L5"] = {
        "whose": src["whose"],
        "declared": src["declared"],
        "supersedes": "adversarial_map.pin_move_queue_v1_6 (17 rows), which stays as recorded. The same 17 rows; each "
                      "names its sentences as a list, and PQ-17 names two (W-004, ruled at R0164).",
        "counts": dict(src["counts"], sentences=n_sent),
        "measured": "Each of the %d sentences occurs exactly once in its locus in the pre-pin corpus (%s) and exactly once "
                    "on each of the three surfaces at the pre-pin release (v4.1.2), in the JSON string encoding all three "
                    "share; PQ-17's two stand in the slot's order." % (n_sent, PRE_PIN[:8]),
        "rows": rows,
        "flow": src["flow"],
    }

    # ---------------------------------------------------------------- phase 1: the instruments
    inst = []
    for rel, what in INSTRUMENTS:
        was = md5b(at_base(rel))
        now = f(rel)
        assert was != now["md5"], "%s did not change" % rel
        inst.append(dict(file=rel, was=was, what=what, **now))
    helper_was = md5b(at_base(HELPER))
    assert helper_was != f(HELPER)["md5"]
    for rel in LINEAGE:
        assert md5b(at_base(rel)) == f(rel)["md5"], "%s must stay byte-identical" % rel
    block = {
        "law": "Every instrument that checks or reproduces a record reads the corpus at the md5 that record pins "
               "(meta.source_corpus_md5, %s for every map v1_1..v1_6, fragment, register and measurement), from git "
               "history once the pin moves the working corpus. tools/xsurface_v4_1_0.py alone reads the working "
               "surfaces: its job is to prove the three agree." % PRE_PIN[:8],
        "why": "R0150 phase 1. The pin session's repairs change the working corpus; as the instruments stood, a real "
               "three-surface edit turned five gates RED and made four measurement or control records drift with exit "
               "status 0, the worst case, because nothing says so.",
        "helper": dict(file=HELPER, was=helper_was, added="path_at(): the same lookup as bytes_at() for a reader that needs "
                       "a path; the committed blob is written under its own basename in a private temp directory "
                       "removed at exit", **f(HELPER)),
        "instruments": inst,
        "lineage_builders": {
            "files": LINEAGE,
            "kept": "byte-identical: each successor builder asserts its predecessor's md5, and tools/patch_assembly_v1_2.py "
                    "and _v1_3.py derive each builder from the one before by anchored patches (K348, K349, K351). "
                    "Editing one would break its own lineage.",
            "after_the_pin": dict(file=FARM, how="runs a script in a scratch root that links every top-level entry of the "
                                  "repo except the corpus, which it writes from git at the pinned md5, with K347_REPO "
                                  "and K348_REPO pointed at the root", **f(FARM)),
        },
        "judge_side": {"verified_not_edited": g2,
                       "note": "gate2's three judgment gates read the pinned corpus since 09289dd with their own inline "
                               "lookup; each is GREEN in-process here and its control record is all-as-expected."},
        "not_reproducing_at_base": {
            "build_assembly_v1_2.py": "Phase G was amended after v1_2 (K351); controls_assembly_v1_3.py reproduces v1_2 "
                                      "with the base fragment swapped in, and now links the pinned corpus into its farm",
            "controls_assembly_v1_1.py": "14 of 15 controls since a later change to its inputs",
            "controls_assembly_v1_2.py": "its record carries Cowork scratch paths (K351 found it; the record is a landed "
                                         "receipt, left alone)",
            "build_phaseG.py": "the Phase G fragment was amended (K351)",
            "build_measurement.py": "a grep count moved with the K360 site/ move",
            "r1/measure_r1_v0_1.py": "reproduces except the date it stamps on the evidence file",
            "build_assembly_v1_4.py and _v1_5.py standalone": "refuse on their R1_rulings BASE GUARD since R1-070 appended "
                                                              "a row; their controls stage the pinned rulings and reproduce",
        },
    }
    if PROVISIONAL:
        block["measured_before_L5"] = block["rehearsal"] = "PROVISIONAL BUILD: the rehearsal reads this queue."
    else:
        rec = json.load(open(os.path.join(REPO, REHEARSAL), encoding="utf-8"))
        v = rec["verdict"]
        assert v["GREEN"] is True, "the rehearsal is not GREEN"
        assert rec["queue_block"] == "pin_move_queue_L5"
        want = ["%s%s" % (r["id"], "" if i == 0 else "." + str(i + 1)) for r in rows for i in range(len(r["sentences"]))]
        assert rec["sentences"] == want, "the rehearsal did not edit exactly this queue's sentences"
        assert rec["base_commit"] == BASE
        sb = rec["SW_sweep_base"]
        moved = {k: x for k, x in sb.items() if not x["same"]}
        repro = lambda x: x["unmutated"]["rc"] == 0 and not x["unmutated"]["changed"]
        refused = sorted(k for k, x in moved.items() if repro(x) and x["edited"]["rc"] != 0)
        drifted = sorted(k for k, x in moved.items() if repro(x) and x["edited"]["rc"] == 0)
        already = sorted(k for k, x in moved.items() if not repro(x))
        block["measured_before_L5"] = {
            "what": "Every tracked Python file that names the corpus (%d, of which %d are skipped and named in the "
                    "record), run with no arguments in a scratch clone with the instruments as they were at %s, "
                    "unmutated and then with every queued sentence edited on all three surfaces (%s, SW_sweep_base)." % (
                        len(sb) + len(rec["SW_skipped"]), len(rec["SW_skipped"]), BASE[:7], REHEARSAL),
            "changed_outcome": len(moved),
            "refused_under_the_edit": refused,
            "drifted_with_exit_status_0": drifted,
            "already_not_reproducing_unmutated": already,
            "unchanged": len(sb) - len(moved),
            "also": "Three R1 readers take arguments and were rehearsed as outputs (outputs_C0_vs_C1): r1_quote_check "
                    "went RED (C2), r1_dossiers refused, r1_draft_dossiers drifted silently; r1_knock_on_dossiers "
                    "already refused at %s on #46, a HOLDS no more since R1-070." % BASE[:7],
        }
        block["rehearsal"] = dict(
            file=REHEARSAL, tool=dict(file=REHEARSE, **f(REHEARSE)), **f(REHEARSAL),
            edited="every sentence of pin_move_queue_L5 (%d) replaced by a placeholder on all three surfaces" % len(want),
            C0="unmutated: %d gates GREEN; 4 self-tests reproduce their committed control records"
               % len(rec["C0_unmutated"]["gates"]),
            C1="edited, instruments pinned: xsurface GREEN (the surfaces agree), %d gates GREEN, the same 4 self-tests "
               "reproduce, and %d instruments' outputs byte-identical to C0's" % (
                   len(rec["C1_edited_pinned"]["gates"]), len(rec["outputs_C0_vs_C1"])),
            C2="edited, instruments as they were at %s: RED at %s" % (BASE[:7], ", ".join(v["C2_red_with_unpinned_instruments"])),
            C3="the lineage builders v1_1 and v1_3 through %s on the edited corpus: each reproduces its committed map" % FARM,
            SW="%d scripts: %d with the same outcome edited as unmutated; differing only the lineage builders (%d) and "
               "scripts that did not reproduce unmutated (%d); unexplained 0" % (
                   len(rec["SW_sweep"]), len(v["SW_same_outcome_edited"]), len(v["SW_differs_lineage"]),
                   len(v["SW_differs_not_reproducing_unmutated"])),
        )
    am["instruments_read_pinned_corpus_L5"] = block

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.30"
    d["canon_version_marker"] = "v38.30"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("L5 continues (the declared pin session, R0150 %s): phase 2 drafts the repairs for "
                      "pin_move_queue_L5's 17 rows (%d sentences) with a knock-on list that carries every current HOLDS "
                      "routed to a repaired locus and every entry anchored inside a repaired sentence (W-007, ruled); "
                      "gate2 judges (K258); his word on the judged text; then the pin move. After it, a successor map "
                      "re-anchors and the six waiting (a)s are re-judged. Then adversarial wing v2 and /llms.txt "
                      "(adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design."
                      % (R0150["md5"][:8], n_sent))
    nrs["ruled_R0164"] = {"his_words_verbatim": HIS_WORD, "record": "adversarial_map.his_word_on_v1_6_judgment_R0164"}
    nrs["L5_phase_1"] = ("Every live instrument reads the corpus at the md5 its record pins; the lineage builders run "
                         "through tools/pinned_farm.py; rehearsed (tools/rehearse_pin.py). "
                         "adversarial_map.instruments_read_pinned_corpus_L5.")

    d["keyset_delta_ledger"]["v38_30_L5"] = (
        "MINOR. keyset UNCHANGED at 42. Three adversarial_map subkey additions (his_word_on_v1_6_judgment_R0164, "
        "pin_move_queue_L5, instruments_read_pinned_corpus_L5); next_recommended_session re-pointed (session rewritten; "
        "ruled_R0164 and L5_phase_1 added); canon-meta; this note; one session_log_recent append. NO PIN. invariants, "
        "schemas, hazard_map and flagship_sidecars asserted byte-identical, and every other top-level key too.")
    d["session_log_recent"].append(
        "L5 (%s; NO PIN): the declared pin session (R0150), phase 1. His word on gate2's v1_6 judgment recorded "
        "(R0164: '%s'), so W-004 and W-007 are ruled; PQ-17 names both sentences (pin_move_queue_L5, %d sentences). "
        "%d instruments read the corpus at the md5 their records pin; the three lineage builders stay byte-identical "
        "and run through tools/pinned_farm.py; rehearsed against an edit of every queued sentence. Next: the drafts."
        % (DATE, HIS_WORD, n_sent, len(inst)))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-3:] == ADDED and set(am) - set(am_before) == set(ADDED)
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_30.json  %s / %d%s" % (md5b(out), len(out), "  (PROVISIONAL)" if PROVISIONAL else ""))
    print("  queue: %d rows, %d sentences; instruments: %d; gate2's gates: %d verified" % (
        len(rows), n_sent, len(inst), len(g2)))


if __name__ == "__main__":
    main()
