#!/usr/bin/env python3
"""project_canon_v38_33.json -- MINOR. L5, the declared pin session (R0150): the corrections gate2's judgment owed
(PD-02, PD-03, PD-08 -> PD-19, PD-20, PD-21), PC-05 reworded to name the reply rather than the man (X-034's safe
wording, PC-06), the drafts gate and patch tool readied for phase 5 (ratification rows; the corpus version), and a
housekeeping finding: the phase-1 rehearsal's first run swept itself and orphaned a recursion that filled the shared
/tmp, since killed, cleaned and fixed at the source. Drafted, not judged.

ccclxiv FIRST: v38_32 is round-tripped at the serialization this file emits BEFORE anything is derived; it is read
at its md5 from the working tree or git history, so this builder runs after the rename removes it.

  python3 tools/build_canon_v38_33.py [--out DIR]
Repo-relative.
"""
import hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_32.json", "459747d7a06311a937035efe77600927"
OUT = os.path.join(OUT_DIR, "project_canon_v38_33.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L5", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = ["pin_repair_redrafts_L5"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

RECORD, GATE, KNOCK = R1 + "PQ_repair_drafts_L5.json", R1 + "pin_repair_drafts_gate_v0_2.py", R1 + "PQ_knock_on_L5_v0_2.json"
GATE_V01, PATCH_V01 = R1 + "pin_repair_drafts_gate.py", "tools/pin_patch_l5.py"   # judged; byte-identical
CTL = R1 + "pin_repair_drafts_gate_control_v0_2.json"
JUDG = (R1 + "PQ_repair_drafts_judgments.json", "2ed68a7cf7f83b8d61a977f0aad0b08e")
PATCH, REHEARSE = "tools/pin_patch_l5_v0_2.py", "tools/rehearse_pin.py"
R0178 = {"relay": "R0178", "md5": "4f2f362dc7b56e8ec7bcff6f6a56e98b", "from": "gate2", "to": "josiah"}
ANSWERS = {"PD-19": ("PD-02", "X-002"), "PD-20": ("PD-03", "X-003"), "PD-21": ("PD-08", "X-008"),
           "PC-06": ("PC-05", "X-034")}
GATE2 = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
         (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
         (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json")]


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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_32 does not round-trip"
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
    assert f(JUDG[0])["md5"] == JUDG[1], "gate2's judgment record moved"
    judg = json.load(open(os.path.join(REPO, JUDG[0]), encoding="utf-8"))
    jrows = {r["id"]: r for r in judg["rows"]}
    assert f(GATE_V01)["md5"] == "6556c41c51d9a609fb35857e8e294577" and f(PATCH_V01)["md5"] == "092b9adc7cfbac33ed0f99d2b6170bb5"
    DG = mod(GATE, "pqg")
    rec = json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
    dfails, dnotes = DG.check(rec, DG.committed_base())
    assert not dfails, "DRAFTS GATE RED: %s" % dfails
    canonical = {n.split(" set:")[0]: n.rsplit(" ", 1)[1] for n in dnotes if "agree at canonical" in n}
    appended = [n for n in dnotes if "committed rows intact" in n]
    c = json.load(open(os.path.join(REPO, CTL), encoding="utf-8"))
    assert c["controls"][0]["control"] == "C0" and all(x["as_expected"] for x in c["controls"])
    assert c["gate_md5"] == f(GATE)["md5"] and c["record_md5"] == f(RECORD)["md5"], "the control record is stale"
    ko = DG.knock_on_record(rec)
    assert (json.dumps(ko, indent=1, ensure_ascii=False) + "\n").encode("utf-8") == open(
        os.path.join(REPO, KNOCK), "rb").read(), "the knock-on record does not reproduce"

    # ---------------------------------------------------------------- the corrections, measured
    by = {r["id"]: r for r in rec["rows"]}
    corr = []
    for new, (old, x) in ANSWERS.items():
        r = by[new]
        assert r["supersedes"] == old, (new, r["supersedes"])
        j = jrows[x]
        assert j.get("row_id", old) == old, (new, x, j.get("row_id"))
        corr.append({"row": new, "supersedes": old, "answers": x, "verdict_answered": j.get("verdict") or j["kind"],
                     "owed": j.get("owed") or j.get("recommendation"), "how": r["how"], "words": r["words"]})
    am["pin_repair_redrafts_L5"] = {
        "status": "DRAFTED, NOT JUDGED. gate2 judges the four rows below (K258); then his word (R0178's four asks); "
                  "then the pin move.",
        "answers": dict(file=JUDG[0], md5=JUDG[1], canon_block="adversarial_map.pin_repair_drafts_judgment_gate2"),
        "corrections": corr,
        "record": dict(f(RECORD), file=RECORD, appended=appended[0] if appended else None,
                       gate=dict(f(GATE), file=GATE, control=dict(f(CTL), file=CTL, result="%d of %d as expected, the "
                                 "unmutated control first" % (len(c["controls"]), len(c["controls"]))),
                                 changed="v0_2, a new file: G10 (a ratification row names only current drafts and "
                                         "companions and covers every queue sentence once, with his words and the relay "
                                         "and judgment it answers); the patch simulation's temp directory removes itself; "
                                         "control C7 aims at a current row; the patch is read through the v0_2 tool"),
                       judged_v0_1_kept=dict(gate=dict(f(GATE_V01), file=GATE_V01), patch=dict(f(PATCH_V01), file=PATCH_V01),
                                             why="gate2's judgment gate pins both at the md5s it judged; a new version is a "
                                                 "new file (the lineage law), and v0_1 still gates the grown record GREEN")),
        "knock_on": dict(f(KNOCK), file=KNOCK, note="v0_1 (phase 2) kept; v0_2 carries the corrected text beside the old"),
        "patch": dict(f(PATCH), file=PATCH, changed="a new file over v0_1's patch: --set ratified reads the newest current "
                      "ratification row; --corpus-version moves the corpus JSON's content-cut version (K335) and nothing "
                      "else",
                      patched_canonical_md5={"declared": canonical["declared"], "with_companions": canonical["all"]}),
        "housekeeping": {
            "what": "The phase-1 rehearsal's first run swept every script that names the corpus, itself included, and the "
                    "sweep's timeout killed only the direct child: its grandchildren went on rehearsing, recursively, in "
                    "orphaned clones under /tmp, and the older instruments each run leaked a scratch directory. The shared "
                    "16 GB /tmp filled at about 17:45; the drafts gate's own patch simulation leaked too.",
            "done": "The orphaned process tree was killed by PID (the shell's own ancestry excluded); 74 orphaned "
                    "rehearsal clones, 78 patch-simulation directories and 2,417 leaked instrument directories, all owned "
                    "by this seat and in use by no process, were removed; /tmp went from 100% to 35%.",
            "fixed": dict(f(REHEARSE), file=REHEARSE, how="every subprocess runs with TMPDIR inside the run's scratch; a "
                          "swept script that times out is killed with its whole process group; the tool skips itself. "
                          "Its phase-1 record, tools/pin_rehearsal_v0_1.json, is a receipt of that run and does not move."),
            "law": "A tool that runs other tools must own their scratch and their process group: a timeout that kills "
                   "one process of a tree orphans the rest.",
        },
        "lean_on_R0178_ask_4": "Agree with gate2: do not hold this pin for the six survival-as-barrier passages (X-032). "
                               "Open a short safety pass over them once the pin closes: keep the argument that the "
                               "drive to survive is a drive, not proof that a life is good; cut only the framing that "
                               "casts a wish to die as the mind's rational verdict and the drive as what blocks it. One "
                               "of the six is social-contract#long's exit sentence, which follows PD-16; PD-16 makes it "
                               "no worse.",
        "for_his_word": R0178,
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.33"
    d["canon_version_marker"] = "v38.33"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("gate2 judges L5's four correction rows (PD-19, PD-20, PD-21, PC-06; "
                      "adversarial_map.pin_repair_redrafts_L5); then his word on R0178's asks; then L5's phase 5, the "
                      "pin move. Then the safety pass over the six loci gate2 found (X-032), a successor map that "
                      "re-anchors, re-judges the six waiting (a)s and files the sibling loci (X-033) and PF-01..03 as (b)s, "
                      "adversarial wing v2 and /llms.txt (adversarial_map.reader_aid_backlog_L4c), R2, and the "
                      "interconnection design.")
    nrs["L5_corrections"] = ("PD-02, PD-03, PD-08 corrected as owed (PD-19, PD-20, PD-21); PC-05 reworded to name the "
                             "reply (PC-06). adversarial_map.pin_repair_redrafts_L5.")
    d["keyset_delta_ledger"]["v38_33_L5"] = (
        "MINOR. keyset UNCHANGED at 42. One adversarial_map subkey addition (pin_repair_redrafts_L5); "
        "next_recommended_session re-pointed (session rewritten; L5_corrections added); canon-meta; this note; one "
        "session_log_recent append. NO PIN. Every other top-level key asserted byte-identical.")
    d["session_log_recent"].append(
        "L5 (%s; NO PIN): the corrections gate2 owed, appended (%s): PD-19 (X-002), PD-20 (X-003), PD-21 (X-008), and "
        "PC-06 naming the reply (X-034). Patch GREEN at %s (with companions %s). A runaway rehearsal recursion that "
        "filled /tmp was killed, cleaned and fixed at the source. Relayed to gate2." % (
            DATE, f(RECORD)["md5"][:8], canonical["declared"][:8], canonical["all"][:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-1:] == ADDED and set(am) - set(am_before) == set(ADDED)
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_33.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  corrections %s; canonical %s / %s" % ([x["row"] for x in corr], canonical["declared"][:8],
                                                 canonical["all"][:8]))


if __name__ == "__main__":
    main()
