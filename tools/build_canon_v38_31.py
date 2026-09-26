#!/usr/bin/env python3
"""project_canon_v38_31.json -- MINOR. L5, the declared pin session (R0150), phase 2: the drafted repairs for
pin_move_queue_L5 (17 rows, 18 sentences), five proposed companion sentences, seven findings, and the knock-on
list; drafted, not judged.

ccclxiv FIRST: v38_30 is round-tripped at the serialization this file emits BEFORE anything is derived. v38_30
is read at its md5 from the working tree or git history, so this builder runs after the rename removes it.

MINOR: keyset held at 42; every top-level key this build does not name byte-identical; inside adversarial_map
one subkey is ADDED and none moves. In-process: the rulings gate, the quote check and gate2's three judgment gates
GREEN; the drafts gate GREEN (its patch simulation included); its control record all-as-expected and naming the
record and gate it pins; the knock-on record reproduces.

  python3 tools/build_canon_v38_31.py [--out DIR]
Repo-relative.
"""
import collections, hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_30.json", "c1af1fb5f2bc5c7a265e7a8901818ef2"
OUT = os.path.join(OUT_DIR, "project_canon_v38_31.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L5", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["pin_repair_drafts_L5"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

RECORD, GATE, CTL, KNOCK = (R1 + "PQ_repair_drafts_L5.json", R1 + "pin_repair_drafts_gate.py",
                            R1 + "pin_repair_drafts_gate_control_v0_1.json", R1 + "PQ_knock_on_L5_v0_1.json")
BUILDER, DOSSIERS, PATCH = R1 + "build_PQ_repair_drafts_L5.py", R1 + "pq_dossiers.py", "tools/pin_patch_l5.py"
GATE2 = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
         (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
         (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json")]
R0150 = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2"}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_30 does not round-trip"
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
    for i, (gate, rec_rel) in enumerate(GATE2):
        M = mod(gate, "g%d" % i)
        fl, _ = M.check(os.path.join(REPO, rec_rel), REPO, M.committed_base())
        assert not fl, "%s RED: %s" % (gate, fl)
    DG = mod(GATE, "pqg")
    rec = json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
    dfails, dnotes = DG.check(rec, DG.committed_base())
    assert not dfails, "DRAFTS GATE RED: %s" % dfails
    canonical = {}
    for n in dnotes:
        if "agree at canonical" in n:
            canonical[n.split(" set:")[0]] = n.rsplit(" ", 1)[1]
    assert set(canonical) == {"declared", "all"}
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["record_md5"] == f(RECORD)["md5"], "the control record is stale"
    ko = DG.knock_on_record(rec)
    assert (json.dumps(ko, indent=1, ensure_ascii=False) + "\n").encode("utf-8") == open(
        os.path.join(REPO, KNOCK), "rb").read(), "the knock-on record does not reproduce"

    # ---------------------------------------------------------------- the drafts, measured
    rows = rec["rows"]
    drafts = [r for r in rows if r["kind"] == "draft"]
    comps = [r for r in rows if r["kind"] == "companion"]
    finds = [r for r in rows if r["kind"] == "finding"]
    kinds = collections.Counter(r["kind"] for r in ko["rows"])
    holds = [r for r in ko["rows"] if r["kind"] == "answer_routes_here" and r["verdict"] == "HOLDS"]
    waits = [r for r in ko["rows"] if r["kind"] == "answer_routes_here" and r["verdict"] == "FAILS"]
    am["pin_repair_drafts_L5"] = {
        "status": "DRAFTED, NOT JUDGED. gate2 judges (K258); his word on the judged text ratifies; then the pin move "
                  "(R0150 phases 3, 4, 5).",
        "drafter": "L5, the declared pin session (seat l, Code). It judges none of this.",
        "record": dict(f(RECORD), file=RECORD,
                       gate=dict(f(GATE), file=GATE, control=dict(f(CTL), file=CTL, result="%d of %d as expected, the "
                                 "unmutated control first" % (len(c["controls"]), len(c["controls"])))),
                       builder=dict(f(BUILDER), file=BUILDER, note="emits the first rows only; the record is "
                                    "append-only once committed")),
        "instruments": {"dossiers": dict(f(DOSSIERS), file=DOSSIERS),
                        "patch": dict(f(PATCH), file=PATCH, note="builds the three-surface patch by whole-locus "
                                      "replacement; phase 5 applies the ratified set with the same code")},
        "drafts": {"rows": len(drafts), "sentences_of_the_queue": len(drafts),
                   "words": {"current": sum(r["words"]["current"] for r in drafts),
                             "replacement": sum(r["words"]["replacement"] for r in drafts),
                             "delta": sum(r["words"]["delta"] for r in drafts)},
                   "patched_canonical_md5": canonical["declared"]},
        "companions": {"rows": [{"id": r["id"], "completes": r["pq"], "locus": r["locus"], "serves": r["serves"]}
                                for r in comps],
                       "words_delta": sum(r["words"]["delta"] for r in comps),
                       "patched_canonical_md5_with_them": canonical["all"],
                       "why": "W-004's reasoning, which he ruled on at R0164: a queue row that names one sentence while "
                              "the conceded text continues into the next leaves the conceded text standing. Each "
                              "companion is one sentence without which its row's repair would contradict its own "
                              "paragraph, or (PC-01) the locus a waiting (a) actually routes to.",
                       "status": "proposed: each needs his word to enter the queue"},
        "findings": [{"id": r["id"], "title": r["title"]} for r in finds],
        "knock_on": {"record": dict(f(KNOCK), file=KNOCK), "counts": dict(sorted(kinds.items())),
                     "holds_routed_to_repaired_loci": sorted(r["n"] for r in holds),
                     "waiting_fails_routed_to_repaired_loci": sorted(r["n"] for r in waits),
                     "reading": "PF-07: all five HOLDS stand on text the repairs do not touch (the seat's reading)."},
        "for_his_word": [
            {"ask": "After gate2's judgment: ratify the 18 drafted sentences (as judged) for the pin move.",
             "recommendation": "yes, as gate2 leaves them"},
            {"ask": "Admit the five companion sentences PC-01..PC-05 into this pin.",
             "recommendation": "yes; without them PQ-09 and PQ-13 contradict their own paragraphs, PQ-08's reassurance "
                               "keeps a flat 'never', and #50 cannot pass because its answer routes to the medium"},
            {"ask": "Leave the slot- and paragraph-scale repairs (PF-01 #1's defender slot, PF-02 #48's safeguard "
                    "paragraph, PF-03 bitter-childhood's clearer-sight sentences) for a later queue.",
             "recommendation": "yes; each should be filed and judged as its own (b) at the successor map first"},
        ],
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.31"
    d["canon_version_marker"] = "v38.31"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("gate2 judges L5's drafts (adversarial_map.pin_repair_drafts_L5): 18 sentences, 5 proposed "
                      "companions, 7 findings and the knock-on list; then his word on the judged text; then L5's "
                      "phase 5, the pin move (R0150 %s). After it, a successor map re-anchors and the six waiting (a)s "
                      "are re-judged. Then adversarial wing v2 and /llms.txt (adversarial_map.reader_aid_backlog_L4c), "
                      "R2, and the interconnection design." % R0150["md5"][:8])
    nrs["L5_phase_2"] = ("Drafted, not judged: %d sentences (+%d words), %d companions proposed, %d findings. The "
                         "patch builds GREEN under xsurface for both sets. adversarial_map.pin_repair_drafts_L5."
                         % (len(drafts), sum(r["words"]["delta"] for r in drafts), len(comps), len(finds)))

    d["keyset_delta_ledger"]["v38_31_L5"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (pin_repair_drafts_L5); "
        "next_recommended_session re-pointed (session rewritten; L5_phase_2 added); canon-meta; this note; one "
        "session_log_recent append. NO PIN. Every other top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "L5 (%s; NO PIN): phase 2. The repairs for pin_move_queue_L5 drafted (%s): %d sentences, +%d words; the patch "
        "builds GREEN under xsurface at canonical %s (with the five proposed companions, %s). %d findings: #1, #48 "
        "and #50 need more than this queue. Relayed to gate2 for judgment." % (
            DATE, f(RECORD)["md5"][:8], len(drafts), sum(r["words"]["delta"] for r in drafts),
            canonical["declared"][:8], canonical["all"][:8], len(finds)))

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
    print("project_canon_v38_31.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  drafts %d, companions %d, findings %d; canonical %s / %s" % (
        len(drafts), len(comps), len(finds), canonical["declared"][:8], canonical["all"][:8]))


if __name__ == "__main__":
    main()
