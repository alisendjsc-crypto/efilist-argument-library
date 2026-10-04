#!/usr/bin/env python3
"""project_canon_v38_52.json -- MINOR canon bump, no release. V5 (seat l, 2026-10-04): his word on R0314 recorded, the
golden rule's third pass drafted, and the responseVariants design drafted with its rulings for his word.

Adds to adversarial_map:
  his_words_V5                  his word on R0314 (gate2's three round-two asks), verbatim, and the asks it adopted,
                                copied from adversarial_map.shapes_redrafts_judgment_gate2.asks
  shapes_redrafts_V5            the golden rule's third pass (RD-03, answering RJ-001), in a new file; drafted, not judged
  response_variants_design_V5   the design (R0294's vehicle) and its measurement; rulings RV-1..RV-8 with leans, pending
                                his word
  record_notes_V5               statements measured and corrected forward
and re-points next_recommended_session (his word on the design -> the build and the relief variant -> gate2's next round
-> the next declared pin).

His word comes from tools/v38_52_his_words.json, cut byte-exact from the user turn by tools/extract_his_words_v38_52.py
and read here at its md5; this builder never needs the transcript to produce its bytes. Measured at run time, never
typed: every md5 and byte count. ccclxiv FIRST: v38_51 round-trips at this file's serialization, read at its md5 from the
working tree or git history. Every top-level key outside TOUCHED is asserted byte-identical; inside adversarial_map only
the new keys are added. Each ruling's lean is asserted present, word for word, in the design doc. The gates it records run
in their own process groups with TMPDIR in scratch.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): git mv v38_51 to v38_52, regenerate that record
with its own --write, then run this builder, which reads v38_51 from git history and overwrites v38_52.

  python3 tools/build_canon_v38_52.py [--out DIR]
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_51.json", "72efc067aab95b6db04e10db1caf5410"
OUT = os.path.join(OUT_DIR, "project_canon_v38_52.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V5"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["his_words_V5", "shapes_redrafts_V5", "response_variants_design_V5", "record_notes_V5"]
WORDS = ("tools/v38_52_his_words.json", "660d13821c69aa59e2e99b9f5747c20d")
EXTRACTOR = "tools/extract_his_words_v38_52.py"
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
SHAPES = {"redraft": "argument_shapes/shapes_redrafts_v0_2.json",
          "record": "argument_shapes/shapes_redrafts_record_v0_2.json",
          "builder": "argument_shapes/build_shapes_redrafts_v0_2.py"}
KEPT = {"argument_shapes/shapes_redrafts_v0_1.json": "fc28cd12265e2712a9d610bbb2c1b69f",
        "argument_shapes/shapes_redrafts_record_v0_1.json": "ace5fb88886f7f7ce49a90658b590954",
        "argument_shapes/shapes_pilot_v0_1.json": "1f9c5da6166b538a90efa6dc7598124e",
        "argument_shapes/shapes_redrafts_judgments.json": "6f4974966c23920234f495cb20813d4c",
        "argument_shapes/shapes_pilot_judgments.json": "73503bccdd3ddf8b3a82f280181251d4"}
DESIGN = {"doc": "design/variations/RESPONSE_VARIANTS_design_v0_1.md",
          "measure_script": "design/variations/measure_response_variants.py",
          "measure": "design/variations/measure_response_variants_v0_1.json"}
VARIATIONS_V0 = ("design/variations/VARIATIONS_design_v0_1.md", None)  # asserted unchanged against git HEAD
VALIDATOR = "argument_shapes/shape_validator_v0_1.py"
GATE2 = {"gate": "argument_shapes/shapes_redrafts_judgments_gate.py"}
RELAYS = {"R0313": "99120fe11c78028a46da4413423bc1a7", "R0314": "554a2eb6a8c697ec2e57c68a2f1a41d3",
          "R0315": "7dceab81f1757af658d01d54d297838f", "R0294": "56af368a4be20ab774dbf28837fadbdc"}
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
TRANSCRIPT = os.path.join(os.path.expanduser("~/.claude/projects"), "-home-josiahscooper-Projects-efilist-argument-library",
                          "f5e10266-5519-4820-8d43-cd27cfcfdcf0.jsonl")
CL_REL = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
SCHOLAR_REPO = os.path.expanduser("~/D/Argue the Argument")

# The rulings, each with the lean the design doc states (asserted present in the doc, whitespace collapsed).
RULINGS = [
    ("RV-1", "Where it lives: a new top-level key, not a key under responses.", "top-level."),
    ("RV-2", "Types: a closed set, or an open one.", "closed, with one type now, `relief-account`."),
    ("RV-3", "Labelling and attribution.",
     "the label is fixed per type and rendered by the page, never written per variant:"),
    ("RV-4", "The flagship toggle (a pin move).",
     "a closed disclosure at long depth, beside [NOTE] and under the note's own condition."),
    ("RV-5", "Does the game vendor it?", "not in the pilot."),
    ("RV-6", "The validator's checks.",
     "V1's pattern: a schema, a validator, and `--self-test` with one mutation per check, unmutated first."),
    ("RV-7", "The nodes: the six note 2 named, or the seven the crossref measures.", "the seven."),
    ("RV-8", "The open residual.", "carried on each variant, in the register's manner, and never registered as a bedrock."),
]
LABEL = "Another answer, not the library's chosen line: the author's relief account"
NEW_FILES = [WORDS[0], EXTRACTOR, SHAPES["redraft"], SHAPES["record"], SHAPES["builder"], DESIGN["doc"],
             DESIGN["measure_script"], DESIGN["measure"], "tools/build_canon_v38_52.py", "argument_shapes/README.md",
             "README.md", "CHANGELOG.md"]

sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402


def md5b(b):
    return hashlib.md5(b).hexdigest()


def md5f(rel):
    return md5b(open(os.path.join(REPO, rel), "rb").read())


def pin(rel):
    return {"file": rel, "md5": md5f(rel), "bytes": os.path.getsize(os.path.join(REPO, rel))}


def relay_md5s():
    got = {}
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) > 8 and f[1] == "SENT" and f[2] in RELAYS:
                got[f[2]] = f[8]
    return got


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
    return out


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_51 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in list(SERVED.items()) + list(KEPT.items()):
        assert md5f(rel) == m, "%s moved" % rel
    head_v0 = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + VARIATIONS_V0[0]], capture_output=True,
                             check=True).stdout
    assert open(os.path.join(REPO, VARIATIONS_V0[0]), "rb").read() == head_v0, "VARIATIONS v0_1 moved"

    W = json.loads(pinned.bytes_at(REPO, *WORDS).decode("utf-8"))
    e = W["excerpts"]["R0314_word"]
    assert md5b(e["text"].encode("utf-8")) == e["md5"] and e["whole_turn"] is True
    rmd5 = relay_md5s()
    for r, m in rmd5.items():
        assert m == RELAYS[r], "%s: the index says %s" % (r, m)
    for r, row in W["relays"].items():
        assert row["md5"] == RELAYS[r], r
    rel = lambda r: {"relay": r, "md5": RELAYS[r]}  # noqa: E731

    rec = json.loads(open(os.path.join(REPO, SHAPES["record"]), encoding="utf-8").read())
    assert rec["pins"]["redraft"]["md5"] == md5f(SHAPES["redraft"]), "the record pins another redraft file"
    assert rec["pins"]["his_words"]["md5"] == WORDS[1]
    meas = json.loads(open(os.path.join(REPO, DESIGN["measure"]), encoding="utf-8").read())
    doc = " ".join(open(os.path.join(REPO, DESIGN["doc"]), encoding="utf-8").read().split())
    for rid, _q, lean in RULINGS:
        assert ("**%s." % rid) in doc and lean in doc, "%s: the lean is not the doc's" % rid
    assert LABEL in doc

    scratch = tempfile.mkdtemp(prefix="canon_v38_52_")
    try:
        results = {}
        run([SHAPES["builder"], "--check"], scratch)
        results["build_shapes_redrafts_v0_2 --check"] = "GREEN"
        out = run([VALIDATOR, SHAPES["redraft"]], scratch)
        tail = json.loads(out[out.rfind("\n{") + 1:])
        assert tail["verdict"] == "PASS" and tail["violation_count"] == 0
        results["shape_validator_v0_1 shapes_redrafts_v0_2.json"] = "GREEN: PASS, %d shape, %d violations" % (
            tail["shapes"], tail["violation_count"])
        run([DESIGN["measure_script"], "--check"], scratch)
        results["measure_response_variants --check"] = "GREEN: the record and the doc's 8 figures"
        if os.path.exists(TRANSCRIPT):
            run([EXTRACTOR, "--check"], scratch)
        if os.path.isdir(os.path.join(SCHOLAR_REPO, ".git")):
            run([GATE2["gate"]], scratch)
            results["shapes_redrafts_judgments_gate (gate2's round two)"] = "GREEN: its pinned referents unmoved"
        else:
            print("note: the game's repository is absent; gate2's gate was not run (bytes unaffected)")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    g = am["shapes_redrafts_judgment_gate2"]
    am["his_words_V5"] = {
        "R0314": {
            "his_word": {"verbatim": e["text"],
                         "said": "%s UTC (America/Phoenix is UTC-7), V2b transcript line %d" % (e["turn"]["utc"],
                                                                                              e["turn"]["line"]),
                         "turn_md5": e["turn"]["turn_md5"], "whole_turn": True,
                         "answers_message": {"line": e["answers_message"]["line"],
                                             "text_md5": e["answers_message"]["text_md5"]}},
            "recorded_by": rel("R0315"),
            "answers": dict(rel("R0314"), seat="gate2 (V3b)"),
            "the_message_it_answers": ("V2b's message of %s UTC (line %d): yes to all three of gate2's asks, matching "
                                       "gate2's leans" % (e["answers_message"]["utc"], e["answers_message"]["line"])),
            "adopts": {"the_three_asks": [dict(a, adopted=True) for a in g["asks"]],
                       "from": "adversarial_map.shapes_redrafts_judgment_gate2.asks (gate2's asks and leans)"}},
        "read": ("the verbatim is the whole user turn named, pinned by the turn's md5, read at the user turn and not "
                 "at a search hit; %s at %s" % WORDS),
        "rule": "Quote his words; never paraphrase them."}
    r = rec["rows"][0]
    am["shapes_redrafts_V5"] = {
        "state": rec["state"],
        "files": {k: pin(v) for k, v in SHAPES.items()},
        "authority": rec["authority"],
        "supersession": rec["supersession"],
        "row": {"id": r["id"], "shape_id": r["shape_id"], "answers": r["answers"]["row"],
                "supersedes": r["supersedes"], "changed": r["changed"], "class": r["class"], "words": r["words"],
                "owed_met": r["owed_met"],
                "terminus": {"via": r["terminus"]["via"], "via_anchor": r["terminus"]["via_anchor"],
                             "register": r["terminus"]["bedrock"]["register"],
                             "copied_from": r["terminus"]["copied_from"]},
                "premise_sharers_read": r["premise_sharers_read"]},
        "validator_runs": rec["validator_runs"],
        "pulls": r["pulls"],
        "sources": ("the restatement rests on six records, each named with its URL and short verbatim excerpts in the "
                    "record (the SEP section 6 and bibliography; MEDLINE 11661183 and 11651921; Crossref for the 1993 "
                    "reprint chapter, the 1993 collection and the 1988 article); neither paper was read in full"),
        "after_round_three": rec["after_round_three"],
        "run_at_this_build": results,
        "not_moved": rec["not_moved"]}
    pf = meas["pleasure_fork"]
    am["response_variants_design_V5"] = {
        "state": "DRAFTED. The rulings wait for his word; nothing is built until he rules (R0315).",
        "charter": {"relay": rel("R0294"), "his_word": "adversarial_map.his_words_L8.R0294"},
        "files": {k: pin(v) for k, v in DESIGN.items()},
        "recommendation": ("A new top-level node key, responseVariants: typed alternative answers, each pinned to the "
                           "sentence of the long it varies, labelled as not the library's chosen line, behind a closed "
                           "disclosure at long depth; the RSI-graded long stays the default and keeps its grade. One "
                           "closed type to start, relief-account, on the fork nodes the crossref measures. Each variant "
                           "carries its open residual in the register's manner. The game leaves it out; the flagship "
                           "shows it in a declared pin after gate2 and his word."),
        "rulings": [{"id": rid, "ruling": q, "lean": lean, "state": "pending his word"} for rid, q, lean in RULINGS],
        "label_leaned": LABEL,
        "measured": {"fork_nodes": pf["fork_rows"], "of_secondary_conflicts": pf["secondary_conflict_rows"],
                     "note_2_names": pf["note_2_names"], "measured_not_in_note_2": pf["measured_not_in_note_2"],
                     "razor_nodes": meas["razor_nodes"], "game_keep": meas["game_embed"]["keep"],
                     "anchors": {n: v["anchor"] for n, v in meas["nodes"].items()},
                     "words": meas["words"]},
        "the_open_residual": {"source": "adversarial_map.relief_view_for_the_variant.the_open_residual",
                              "md5": meas["the_open_residual"]["md5"]},
        "on_his_word": ("the build on V1's pattern (schema, validator, --self-test control), then the relief variant "
                        "drafted by seat l from relief_view_for_the_variant, judged by gate2 (K258), then his word, then "
                        "the render in a declared pin"),
        "not_moved": "VARIATIONS_design_v0_1.md and its measurement; no corpus or served byte"}

    cl_old = g["collision_list_record_moved"]["md5"]
    old_lines = pinned.bytes_at(REPO, CL_REL, cl_old).decode("utf-8").splitlines()
    new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(old_lines, new_lines) if x != y]
    assert len(old_lines) == len(new_lines) and cl_diff == [('  "canon": "project_canon_v38_51.json"',
                                                             '  "canon": "project_canon_v38_52.json"')], cl_diff
    am["record_notes_V5"] = [
        {"statement": "R0294 and R0315: pilot the responseVariants design on 'the six pleasure-fork nodes'",
         "measured": ("the crossref's %d secondary-conflict rows carry the pleasure fork in %d: the six its note 2 "
                      "names, which his word adopted, and %s, which note 2's count missed. The design leans to all "
                      "seven (RV-7); his word decides." % (pf["secondary_conflict_rows"], pf["fork_count"],
                                                           ", ".join(pf["measured_not_in_note_2"])))},
        {"statement": "R0313: Hare 1975 'reprinted as chapter 10 of Essays on Bioethics, 1993, pp. 147-167, by Crossref'",
         "measured": ("right: the publisher's record (Crossref 10.1093/oso/9780198239833.003.0010) gives the chapter at "
                      "pp. 147-167. Crossref holds no record of the 1975 printing; its pages, 4(3): 201-222, are read "
                      "from the MEDLINE record (PMID 11661183) and the SEP's bibliography, and the third pass says so")},
        {"statement": ("RJ-008: the golden rule read as doing to others what we are glad was done to us is in none of "
                       "the six records"),
         "measured": ("no record read in V5 has it either; the third pass words the step as the SEP states it (glad to "
                      "exist, I prescribe my own creation; universalized, creating others relevantly like me, ceteris "
                      "paribus) and flags the change as a pull for gate2")},
        {"statement": "shapes_redrafts_judgment_gate2 pins r1_collision_list_l7_v0_1.json at %s" % cl_old,
         "measured": ("the record names the canon file present, so this bump moved it by exactly one line, its "
                      "'canon' field (v38_51 to v38_52); regenerated by the tool's own --write"),
         "record": dict(pin(CL_REL), was=cl_old)}]

    d["canon_version"] = "38.52"
    d["canon_version_marker"] = "v38.52"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = (
        "The pin is v4.1.5. V5 recorded his word on R0314 (gate2's three asks, adopted), drafted the golden rule's third "
        "pass in a new file (shapes_redrafts_v0_2.json; RD-03 answers RJ-001), and drafted the responseVariants design "
        "(R0294) with rulings RV-1..RV-8 and leans. Next, in order: (1) his word on the design's rulings; (2) the build on "
        "V1's pattern (schema, validator, --self-test control) and the relief variant, drafted by seat l from "
        "relief_view_for_the_variant; (3) gate2's next round: the relief variant and the golden rule's third pass, "
        "drafter != judge, then his word; (4) the next declared pin session (safety_queue_L7, pin_queue_additions_R0292, "
        "the served-text repairs carried since L1 and LD3; the responseVariants render once ruled and judged). V4 takes "
        "the one (a) after the successor map's pin; the (d)s enter the map at its next validator bump (many-peaks, "
        "heroism and soul-making now; the golden rule once gate2 accepts it); the (c) goes to the intake, "
        "love-from-the-void first, and the R-V6 self-objection batch (r_v6_adopted_V2b) follows the pilot's judgment.")
    nrs["V5_closed"] = {"state": ("RECORDED (his word on R0314) and DRAFTED (the golden rule's third pass; the "
                                  "responseVariants design, rulings pending his word)"), "blocks": NEW_KEYS,
                        "canon_writer_next": "seat l (his word on the design), then gate2 (its next round)"}
    d["keyset_delta_ledger"]["v38_52_V5"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "V5 (seat l, 2026-10-04): his word on R0314 recorded verbatim from the user turn (gate2's three asks adopted); "
        "the golden rule's third pass drafted in a new file (Hare's total as a limit, the shares held, the halt; Hare "
        "1975 added; route unchanged after reading the premise-sharers), validator PASS 0, for gate2's next round; the "
        "responseVariants design drafted with eight rulings and leans for his word; the pleasure fork measured at "
        "seven nodes. No pin.")

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-len(NEW_KEYS):] == NEW_KEYS and len(am) == len(am_before) + len(NEW_KEYS)
    assert json.loads(out.decode("utf-8")) == d
    for rel_ in NEW_FILES:
        assert os.path.exists(os.path.join(REPO, rel_)), rel_
    open(OUT, "wb").write(out)
    print("project_canon_v38_52.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
