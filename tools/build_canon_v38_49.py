#!/usr/bin/env python3
"""project_canon_v38_49.json -- MINOR canon bump, no release. V3 (gate2, 2026-10-03): the argument-shapes pilot judged.

Adds to adversarial_map:
  shapes_pilot_judgment_gate2   gate2's judgment of V2's ten shapes (5 ACCEPT, 2 AMEND, 3 REJECT), the three pulls, the
                                measures after judgment, what seat l owes, and the asks to his word with gate2's leans
and re-points next_recommended_session (his word on the asks; seat l's two redrafts, judged by gate2; then V4).

Everything is read from the judgment record and the reading record at the md5s their files carry; nothing is typed but
prose. ccclxiv FIRST: v38_48 round-trips at this file's serialization, read at its md5 from the working tree or git
history. Every top-level key outside TOUCHED is asserted byte-identical; inside adversarial_map only the new key is
added. When the game's repository is on the machine, the judgment gate, its self-test and the reading's --check run
first in their own process groups (TMPDIR in scratch) and must be GREEN; their output is not recorded, so the bytes
are the same either way.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): move v38_48 aside as v38_49, regenerate that
record with its own --write, then run this builder, which reads v38_48 from git history and overwrites v38_49.

  python3 tools/build_canon_v38_49.py [--out DIR]
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_48.json", "c971855b153a297f182503c342b3659c"
OUT = os.path.join(OUT_DIR, "project_canon_v38_49.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V3"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEY = "shapes_pilot_judgment_gate2"
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
FILES = {"record": "argument_shapes/shapes_pilot_judgments.json", "gate": "argument_shapes/shapes_judgments_gate.py",
         "control": "argument_shapes/shapes_judgments_gate_control_v0_1.json",
         "reading": "argument_shapes/shapes_judgment_reading.py",
         "reading_record": "argument_shapes/shapes_judgment_reading_v0_1.json"}
KICKOFF = {"relay": "R0297", "md5": "2a8a8ca2deea71aa39b1f12f30d7dc53"}
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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_48 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert NEW_KEY not in am
    for rel, m in SERVED.items():
        assert md5b(open(os.path.join(REPO, rel), "rb").read()) == m, "%s moved: no pin here" % rel

    if os.path.isdir(os.path.join(SCHOLAR_REPO, ".git")):
        scratch = tempfile.mkdtemp(prefix="v38_49_")
        try:
            for args in ([FILES["gate"]], [FILES["gate"], "--self-test"], [FILES["reading"], "--check"]):
                run(args, scratch)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    else:
        print("note: the game's repository is absent; the judgment gate was not run (bytes unaffected)")

    rec = json.loads(open(os.path.join(REPO, FILES["record"]), encoding="utf-8").read())
    rd = json.loads(open(os.path.join(REPO, FILES["reading_record"]), encoding="utf-8").read())
    assert rec["kickoff"] == KICKOFF
    rows = rec["rows"]
    shape_rows = [r for r in rows if r["kind"] == "shape"]
    by_id = {r["id"]: r for r in rows}

    def route(r):
        rt = r["route"]
        if not rt:
            return None
        if "via" in rt:
            return {"via": rt["via"], "bedrock": rt["bedrock"]["register"]}
        if "answered_by" in rt:
            return {"answered_by": [a["locus"] for a in rt["answered_by"]]}
        return rt

    verdicts = {r["shape_id"]: {"row": r["id"], "verdict": r["verdict"], "class_drafted": r["class_drafted"],
                                "class_judged": r["class_judged"], "belongs_to": r["belongs_to"], "route": route(r),
                                "reason": r["reason"]} for r in shape_rows}
    counts = {}
    for r in shape_rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    seq = by_id["SJ-023"]
    cl_old = am["record_notes_V2"][0]["record"]["md5"]
    old_lines = pinned.bytes_at(REPO, CL_REL, cl_old).decode("utf-8").splitlines()
    new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(old_lines, new_lines) if x != y]
    assert len(old_lines) == len(new_lines) and cl_diff == [('  "canon": "project_canon_v38_48.json"',
                                                             '  "canon": "project_canon_v38_49.json"')], cl_diff

    am[NEW_KEY] = {
        "state": "JUDGED, NOT RULED (V3, gate2, 2026-10-03). His word decides; nothing ships on a judgment.",
        "K258": "gate2 drafted none of the pilot, its measurement, its builder, the validator or its control.",
        "kickoff": KICKOFF,
        "files": {k: pin(v) for k, v in FILES.items()},
        "judged": rec["judged"],
        "counts": {"shapes": dict(sorted(counts.items())), "kept": rd["figures"]["judged"]["kept"],
                   "classes_judged": rd["figures"]["judged"]["classes"], "rows": len(rows)},
        "verdicts": verdicts,
        "pulls": {r["id"]: {"pull": r["pull"], "verdict": r["verdict"], "answer": r["answer"]}
                  for r in rows if r["kind"] == "pull"},
        "measures_after_judgment": {k: rd["figures"]["judged"][k] for k in (
            "a_cross_node", "routed_cross_node", "not_shipping_as_a_of_drafted", "not_shipping_as_a_of_kept",
            "words_kept", "per_node")},
        "measures_as_drafted_recomputed": {k: rd["figures"]["drafted"][k] for k in (
            "a_cross_node", "routed_cross_node", "not_shipping_as_a", "words")},
        "findings": [{"row": r["id"], "finding": r["finding"], "recommendation": r.get("recommendation")}
                     for r in rows if r["id"] in ("SJ-015", "SJ-016", "SJ-021")],
        "owed_to_seat_l": [{"row": r["id"], "shape_id": r["shape_id"], "owed": r["owed"]}
                           for r in shape_rows if r["owed"]],
        "carries": [{"row": r["id"], "carry": c} for r in shape_rows for c in r["carries"]],
        "asks": seq["asks"],
        "order": seq["order"],
        "collision_list_record_moved": dict(pin(CL_REL), was=cl_old, measured=(
            "the record names the canon file present, so this bump moved it by exactly one line, its 'canon' field "
            "(v38_48 to v38_49); regenerated by the tool's own --write")),
        "not_moved": "the pilot, its measurement, its builder, the validator, its control and the schema "
                     "(the gate pins them); the map validator; no corpus or served byte"}

    d["canon_version"] = "38.49"
    d["canon_version_marker"] = "v38.49"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = (
        "The pin is v4.1.5. V3 (gate2) judged the argument-shapes pilot: %d of 10 shapes kept (classes %s); three "
        "were other nodes' objections. Next, in order: (1) his word on the six asks in "
        "adversarial_map.shapes_pilot_judgment_gate2.asks; (2) seat l's two redrafts (SJ-003's statement, SJ-008's "
        "route) as new rows or a new file, judged by gate2; (3) the responseVariants design (R0294); (4) the relief "
        "variant, from relief_view_for_the_variant, judged by a seat that drafted none of it; (5) the next declared "
        "pin session (safety_queue_L7, pin_queue_additions_R0292, the served-text repairs carried since L1 and LD3). "
        "After his word: V4 puts the one (a) in the corpus after the successor map's pin; the (d)s enter the map at its "
        "next validator bump; the (c) opens the intake, love-from-the-void first." % (
            rd["figures"]["judged"]["kept"],
            " ".join("%s%d" % kv for kv in sorted(rd["figures"]["judged"]["classes"].items()))))
    nrs["V3_closed"] = {"state": "JUDGED, NOT RULED", "block": NEW_KEY, "canon_writer_next": "seat l"}
    d["keyset_delta_ledger"]["v38_49_V3"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % NEW_KEY)
    d["session_log_recent"].append(
        "V3 (gate2, 2026-10-03): the argument-shapes pilot judged (R0297): 5 ACCEPT, 2 AMEND, 3 REJECT. Three shapes were "
        "other nodes' scholar objections (gods-plan, extinction-culture, love-beauty-art); soul-making is (d) at HR-02, "
        "not (a); the golden rule owes Hare's weighed duty. One (a) remains, for V4. No pin.")

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
    print("project_canon_v38_49.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
