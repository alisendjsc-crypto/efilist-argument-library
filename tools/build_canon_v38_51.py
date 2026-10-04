#!/usr/bin/env python3
"""project_canon_v38_51.json -- MINOR canon bump, no release. V3b (gate2, 2026-10-04): V2b's two redrafts judged.

Adds to adversarial_map:
  shapes_redrafts_judgment_gate2   gate2's round-two judgment of the two redrafts (soul-making ACCEPT, the golden rule
                                   AMEND), the scheme, the sources, the three pulls, the record's third note, the
                                   forward correction of round one's Hare source read, what seat l owes, and the asks
                                   to his word with gate2's leans
and re-points next_recommended_session (his word on the asks; the golden rule's third round; then the order V2b set).

Everything is read from the judgment record at the md5 its file carries; nothing is typed but prose. ccclxiv FIRST:
v38_50 round-trips at this file's serialization, read at its md5 from the working tree or git history. Every
top-level key outside TOUCHED is asserted byte-identical; inside adversarial_map only the new key is added. When the
game's repository is on the machine, the round-two gate and its self-test run first in their own process groups
(TMPDIR in scratch) and must be GREEN; their output is not recorded, so the bytes are the same either way.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): git mv v38_50 to v38_51, regenerate that
record with its own --write, then run this builder, which reads v38_50 from git history and overwrites v38_51.

  python3 tools/build_canon_v38_51.py [--out DIR]
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_50.json", "98302afdf29af8ed3149111843d717ab"
OUT = os.path.join(OUT_DIR, "project_canon_v38_51.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V3b"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEY = "shapes_redrafts_judgment_gate2"
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
FILES = {"record": "argument_shapes/shapes_redrafts_judgments.json",
         "gate": "argument_shapes/shapes_redrafts_judgments_gate.py",
         "control": "argument_shapes/shapes_redrafts_judgments_gate_control_v0_1.json"}
KICKOFF = {"relay": "R0311", "md5": "95ae9542298d5162efb407780e82d2ff"}
CL_REL = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
SCHOLAR_REPO = os.path.expanduser("~/D/Argue the Argument")

sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402


def md5b(b):
    return hashlib.md5(b).hexdigest()


def pin(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"file": rel, "md5": md5b(b), "bytes": len(b)}


def run(args, scratch):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
    p = subprocess.Popen([sys.executable] + args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, env=env, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        raise
    assert p.returncode == 0, "%s: rc %d\n%s" % (" ".join(args), p.returncode, out[-2000:])


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_50 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert NEW_KEY not in am
    for rel, m in SERVED.items():
        assert md5b(open(os.path.join(REPO, rel), "rb").read()) == m, "%s moved: no pin here" % rel

    if os.path.isdir(os.path.join(SCHOLAR_REPO, ".git")):
        scratch = tempfile.mkdtemp(prefix="v38_51_")
        try:
            for args in ([FILES["gate"]], [FILES["gate"], "--self-test"]):
                run(args, scratch)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    else:
        print("note: the game's repository is absent; the round-two gate was not run (bytes unaffected)")

    rec = json.loads(open(os.path.join(REPO, FILES["record"]), encoding="utf-8").read())
    assert rec["kickoff"] == KICKOFF
    rows = rec["rows"]
    by_id = {r["id"]: r for r in rows}
    shape_rows = [r for r in rows if r["kind"] == "shape"]

    def route(r):
        rt = r["route"]
        if not rt:
            return None
        if "via" in rt:
            return {"via": rt["via"], "bedrock": rt["bedrock"]["register"]}
        if "answered_by" in rt:
            return {"answered_by": [a["locus"] for a in rt["answered_by"]]}
        return rt

    verdicts = {r["shape_id"]: {"row": r["id"], "redraft": r["redraft"], "answers": r["answers"],
                                "verdict": r["verdict"], "class_drafted": r["class_drafted"],
                                "class_judged": r["class_judged"], "route": route(r), "reason": r["reason"]}
                for r in shape_rows}
    counts = {}
    for r in shape_rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    seq = by_id["RJ-011"]
    cl_old = am["record_notes_V2b"][3]["record"]["md5"]
    old_lines = pinned.bytes_at(REPO, CL_REL, cl_old).decode("utf-8").splitlines()
    new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(old_lines, new_lines) if x != y]
    assert len(old_lines) == len(new_lines) and cl_diff == [('  "canon": "project_canon_v38_50.json"',
                                                             '  "canon": "project_canon_v38_51.json"')], cl_diff

    am[NEW_KEY] = {
        "state": "JUDGED, NOT RULED (V3b, gate2, 2026-10-04). His word decides; nothing ships on a judgment.",
        "K258": "gate2 drafted none of the redrafts, their record, their builder, the his-words extractor or canon v38.50.",
        "kickoff": KICKOFF,
        "files": {k: pin(v) for k, v in FILES.items()},
        "judged": rec["judged"],
        "counts": {"redrafts": dict(sorted(counts.items())), "rows": len(rows)},
        "verdicts": verdicts,
        "scheme": {"row": "RJ-003", "verdict": by_id["RJ-003"]["verdict"], "finding": by_id["RJ-003"]["finding"],
                   "validator_runs": {k.split(".", 1)[1]: v for k, v in by_id["RJ-003"]["figures"].items()}},
        "sources": {"row": "RJ-004", "verdict": by_id["RJ-004"]["verdict"], "finding": by_id["RJ-004"]["finding"],
                    "checked": by_id["RJ-004"]["checked"]},
        "pulls": {r["id"]: {"pull": r["pull_text"], "verdict": r["verdict"], "answer": r["answer"]}
                  for r in rows if r["kind"] == "pull"},
        "note": {"row": "RJ-008", "on": by_id["RJ-008"]["measure"], "verdict": by_id["RJ-008"]["verdict"],
                 "finding": by_id["RJ-008"]["finding"]},
        "round_one_corrected_forward": {"row": "RJ-009", "corrects": ["SJ-003 (reads.source)", "SJ-018 (Hare clause)"],
                                        "finding": by_id["RJ-009"]["finding"]},
        "safety": {"row": "RJ-010", "verdict": by_id["RJ-010"]["verdict"]},
        "owed_to_seat_l": [{"row": r["id"], "shape_id": r["shape_id"], "owed": r["owed"]}
                           for r in shape_rows if r["owed"]],
        "asks": seq["asks"],
        "order": seq["order"],
        "collision_list_record_moved": dict(pin(CL_REL), was=cl_old, measured=(
            "the record names the canon file present, so this bump moved it by exactly one line, its 'canon' field "
            "(v38_50 to v38_51); regenerated by the tool's own --write")),
        "not_moved": ("the redrafts, their record and builder, the pilot, gate2's round-one record, gate and reading, "
                      "the validator and its control, the schema; no corpus or served byte")}

    d["canon_version"] = "38.51"
    d["canon_version_marker"] = "v38.51"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = (
        "The pin is v4.1.5. V3b (gate2) judged V2b's two redrafts: soul-making ACCEPT as (d) at HR-02; the golden rule "
        "AMEND (Hare's total stated as a limit on the duty, with his halt and the held distribution; Hare 1975 added). "
        "Next, in order: (1) his word on the three asks in adversarial_map.%s.asks; (2) the responseVariants design "
        "(R0294), in whose seat-l session, on his word, the golden rule's third redraft is drafted in a new file "
        "(shapes_redrafts_v0_2.json), judged in gate2's next round; (3) the relief variant, drafted from "
        "relief_view_for_the_variant and judged by a seat that drafted none of it; (4) the next declared pin session "
        "(safety_queue_L7, pin_queue_additions_R0292, the served-text repairs carried since L1 and LD3). V4 takes the "
        "one (a) after the successor map's pin; the (d)s enter the map at its next validator bump (many-peaks, heroism "
        "and soul-making now; the golden rule once round three accepts it); the (c) goes to the intake, "
        "love-from-the-void first, and the R-V6 self-objection batch (r_v6_adopted_V2b) follows the pilot's judgment."
        % NEW_KEY)
    nrs["V3b_closed"] = {"state": "JUDGED, NOT RULED", "block": NEW_KEY, "canon_writer_next": "seat l"}
    d["keyset_delta_ledger"]["v38_51_V3b"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % NEW_KEY)
    d["session_log_recent"].append(
        "V3b (gate2, 2026-10-04): V2b's two redrafts judged (R0311): soul-making ACCEPT as (d) at HR-02; the golden rule "
        "AMEND, because its total is stated as the duty's trigger, which his L3 reading meets at joy-outweighs-harms, "
        "and without Hare's halt; Hare 1975 to be added to its attestation. Round one's Hare source read corrected "
        "forward. No pin.")

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-1] == NEW_KEY and len(am) == len(am_before) + 1
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_51.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
