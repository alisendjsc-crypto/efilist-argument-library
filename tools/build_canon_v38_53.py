#!/usr/bin/env python3
"""project_canon_v38_53.json -- MINOR canon bump, no release. V6 (seat l, 2026-10-04): his word on R0316 recorded, the
responseVariants rulings RV-1..RV-8 adopted as leaned, and the build on V1's pattern (schema, validator, self-test
control) pinned.

Adds to adversarial_map:
  his_words_V6                    his word on R0316, verbatim from the user turn: the first sentence is the word; the
                                  whole turn is recorded as said with it
  response_variants_rulings_V6    RV-1..RV-8 ADOPTED as leaned, each ruling and lean copied from
                                  adversarial_map.response_variants_design_V5.rulings, the label from label_leaned
  response_variants_build_V6      response_variants/ pinned: schema, validator, self-test control, README; the
                                  self-test counts read from the control record
  record_notes_V6                 statements measured and corrected forward
and re-points next_recommended_session (V7 the relief variant -> gate2's next round -> his word -> the next declared pin).

His word comes from tools/v38_53_his_words.json, cut byte-exact from the user turn by tools/extract_his_words_v38_53.py
and read here at its md5; this builder never needs the transcript to produce its bytes. Measured at run time, never
typed: every md5, byte count and self-test count. ccclxiv FIRST: v38_52 round-trips at this file's serialization, read
at its md5 from the working tree or git history. Every top-level key outside TOUCHED is asserted byte-identical; inside
adversarial_map only the new keys are added. The design's files, V5's redraft and gate2's records are asserted at the
md5s canon already pins. The gates it records run in their own process groups with TMPDIR in scratch.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): git mv v38_52 to v38_53, regenerate that record
with its own --write, then run this builder, which reads v38_52 from git history and overwrites v38_53.

  python3 tools/build_canon_v38_53.py [--out DIR]
"""
import hashlib, importlib.util, json, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_52.json", "9697f796baacc7c54bd8212057f4e486"
OUT = os.path.join(OUT_DIR, "project_canon_v38_53.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V6"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["his_words_V6", "response_variants_rulings_V6", "response_variants_build_V6", "record_notes_V6"]
WORDS = ("tools/v38_53_his_words.json", "8956bfca39f1bd2e17a63d4760d00322")
EXTRACTOR = "tools/extract_his_words_v38_53.py"
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
KEPT = {"argument_shapes/shapes_redrafts_v0_1.json": "fc28cd12265e2712a9d610bbb2c1b69f",
        "argument_shapes/shapes_redrafts_record_v0_1.json": "ace5fb88886f7f7ce49a90658b590954",
        "argument_shapes/shapes_pilot_v0_1.json": "1f9c5da6166b538a90efa6dc7598124e",
        "argument_shapes/shapes_redrafts_judgments.json": "6f4974966c23920234f495cb20813d4c",
        "argument_shapes/shapes_pilot_judgments.json": "73503bccdd3ddf8b3a82f280181251d4",
        "adversarial_map_staging/r1/sp_reading_l6.py": "dc2525ef40fc5353a670484f511bd668",
        "argument_shapes/argument_shapes_schema_v0_1.json": "bef95b1dc2b9cb109760cd961d2da72b",
        "argument_shapes/shape_validator_v0_1.py": "64553b25b6db0ff67edeb87b89178297",
        "argument_shapes/shape_validator_control_v0_1.json": "64222600e415617bcd3ab8f7b8e453ef"}
BUILD = {"schema": "response_variants/response_variants_schema_v0_1.json",
         "validator": "response_variants/response_variant_validator_v0_1.py",
         "control": "response_variants/response_variant_validator_control_v0_1.json",
         "readme": "response_variants/README.md"}
RELAYS = {"R0316": "b37c0fb48c8d2473fb03da30bc644289", "R0318": "c6078a2d9c65fba129503092a8008a96",
          "R0294": "56af368a4be20ab774dbf28837fadbdc"}
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
TRANSCRIPT = os.path.join(os.path.expanduser("~/.claude/projects"), "-home-josiahscooper-Projects-efilist-argument-library",
                          "e013cfb0-df3e-4174-b2ea-e9c65822debb.jsonl")
CL_REL = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
CL_WAS = "90eb5e1688ca0200b859a0d4ab11f9d2"
MEASURE = "design/variations/measure_response_variants.py"
# One literal instance of each of gate2's nine EXIT patterns, to measure that L6's WIDE families contain them.
EXIT_SAMPLES = ["barriers to exit", "exit barriers", "trapped by them", "body vetoes the mind",
                "only 'exit' from existence is death", "graceful exit", "failure rate of suicide attempts",
                "It is a trap.", "recruited into the same firmware and then trapped"]
NEW_FILES = [WORDS[0], EXTRACTOR, "tools/build_canon_v38_53.py", "README.md", "CHANGELOG.md"] + list(BUILD.values())

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


def load_validator():
    spec = importlib.util.spec_from_file_location("response_variant_validator_v0_1",
                                                  os.path.join(REPO, BUILD["validator"]))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_52 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in list(SERVED.items()) + list(KEPT.items()):
        assert md5f(rel) == m, "%s moved" % rel
    dv5 = am["response_variants_design_V5"]
    for k, p in dv5["files"].items():
        assert md5f(p["file"]) == p["md5"], "the design's %s moved" % k
    for k, p in am["shapes_redrafts_V5"]["files"].items():
        assert md5f(p["file"]) == p["md5"], "V5's %s moved" % k

    W = json.loads(pinned.bytes_at(REPO, *WORDS).decode("utf-8"))
    e, whole = W["excerpts"]["R0316_word"], W["excerpts"]["R0316_whole_turn"]
    assert md5b(e["text"].encode("utf-8")) == e["md5"] and e["whole_turn"] is False and e["offsets"][0] == 0
    assert whole["whole_turn"] is True and whole["md5"] == whole["turn"]["turn_md5"] == e["turn"]["turn_md5"]
    assert whole["text"].startswith(e["text"])
    rmd5 = relay_md5s()
    for r, m in rmd5.items():
        assert m == RELAYS[r], "%s: the index says %s" % (r, m)
    for r, row in W["relays"].items():
        assert row["md5"] == RELAYS[r], r
    rel = lambda r: {"relay": r, "md5": RELAYS[r]}  # noqa: E731

    V = load_validator()
    schema = json.loads(open(os.path.join(REPO, BUILD["schema"]), encoding="utf-8").read())
    ctl = json.loads(open(os.path.join(REPO, BUILD["control"]), encoding="utf-8").read())
    cs = ctl["summary"]
    assert cs["as_expected"] == cs["cases"] and not cs["checks_never_turned_red"] and \
        cs["first_case_is_the_unmutated_control"] and cs["checks"] == len(V.CHECKS)
    assert schema["x-types"]["relief-account"]["label"] == dv5["label_leaned"]
    exit_in_wide = []
    for s, p in zip(EXIT_SAMPLES, V.EXIT):
        assert re.search(p, s), "sample %r does not match its EXIT pattern" % s
        exit_in_wide.append(bool(V.floor_hits(s)["floor-wide"]))

    scratch = tempfile.mkdtemp(prefix="canon_v38_53_")
    try:
        results = {}
        out = run([BUILD["validator"], "--self-test", "--check"], scratch)
        assert "reproduced byte for byte" in out
        results["response_variant_validator_v0_1 --self-test --check"] = (
            "GREEN: %d of %d cases as expected; %d of %d checks turned RED; the record reproduced byte for byte"
            % (cs["as_expected"], cs["cases"], cs["checks_turned_red_by_a_mutation"], cs["checks"]))
        out = run([BUILD["validator"], "--embedded"], scratch)
        tail = json.loads(out[out.rfind("\n{") + 1:])
        assert tail["verdict"] == "PASS" and tail["variants"] == 0
        results["response_variant_validator_v0_1 --embedded"] = "GREEN: PASS, %d variants in the corpus (%s)" % (
            tail["variants"], tail["variant_coverage"])
        run([MEASURE, "--check"], scratch)
        results["measure_response_variants --check"] = "GREEN: the design's measurement unmoved"
        if os.path.exists(TRANSCRIPT):
            run([EXTRACTOR, "--check"], scratch)
            results["extract_his_words_v38_53 --check"] = "GREEN: cut again from the user turn, byte-identical"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    am["his_words_V6"] = {
        "R0316": {
            "his_word": {"verbatim": e["text"],
                         "said": "%s UTC (America/Phoenix is UTC-7), V5 transcript line %d" % (e["turn"]["utc"],
                                                                                             e["turn"]["line"]),
                         "turn_md5": e["turn"]["turn_md5"], "whole_turn": False,
                         "offsets_in_turn": e["offsets"],
                         "answers_message": {"line": e["answers_message"]["line"],
                                             "text_md5": e["answers_message"]["text_md5"]}},
            "said_with_it": {"verbatim": whole["text"], "whole_turn": True, "turn_md5": whole["md5"],
                             "note": ("the rest of the turn leaves fresh-or-continue to the seat; V5 chose a fresh "
                                      "session and wrote V6's kickoff (R0318)")},
            "recorded_by": rel("R0318"),
            "answers": dict(rel("R0316"), seat="josiah (from V5)"),
            "the_message_it_answers": ("V5's message of %s UTC (line %d): adopt all eight leans of R0316, and V5 builds "
                                       "if he answers there" % (e["answers_message"]["utc"],
                                                                e["answers_message"]["line"])),
            "adopts": "RV-1..RV-8 as leaned: adversarial_map.response_variants_rulings_V6"},
        "read": ("cut at the user turn named, pinned by the turn's md5, read at the user turn and not at a search hit; "
                 "%s at %s" % WORDS),
        "rule": "Quote his words; never paraphrase them."}

    am["response_variants_rulings_V6"] = {
        "state": "RULED 2026-10-04 by his word (adversarial_map.his_words_V6.R0316); built at V6",
        "design": ("adversarial_map.response_variants_design_V5, left as recorded; the design doc and its measurement "
                   "stay byte-identical, and this block records the ruling"),
        "rulings": [{"id": r["id"], "ruling": r["ruling"], "lean": r["lean"], "state": "ADOPTED as leaned"}
                    for r in dv5["rulings"]],
        "copied_from": "adversarial_map.response_variants_design_V5.rulings (ruling and lean), and label_leaned",
        "label": dv5["label_leaned"],
        "attribution": schema["x-types"]["relief-account"]["whose_account"],
        "nodes_RV_7": dv5["measured"]["fork_nodes"],
        "type_table": schema["x-types"],
        "what_follows": ("V7 drafts the relief variant on the seven nodes; gate2 judges it with RD-03 (R0317); his word; "
                         "the render in the next declared pin, drawn by the design lane (RV-4). The game leaves it out "
                         "(RV-5).")}

    am["response_variants_build_V6"] = {
        "state": "BUILT. New files only, in response_variants/. Not served, not canon text; no corpus byte.",
        "files": {k: pin(v) for k, v in BUILD.items()},
        "pattern": "V1's argument_shapes/ (schema, validator, --self-test control), as RV-6 and R0318 order",
        "imports": ctl["imports"],
        "checks": list(V.CHECKS),
        "self_test": {"cases": cs["cases"], "as_expected": cs["as_expected"], "checks": cs["checks"],
                      "checks_turned_red_by_a_mutation": cs["checks_turned_red_by_a_mutation"],
                      "first_case_is_the_unmutated_control": cs["first_case_is_the_unmutated_control"],
                      "hash_seeds": "byte-identical under PYTHONHASHSEED 1 and 97"},
        "real_data_controls": ctl["real_data"],
        "modes": "staging files ({meta, variants}, pinning corpus and canon by md5); --embedded (the corpus's own list)",
        "run_at_this_build": results,
        "coverage": ("declared per file and gated against that file alone (ccclxx); the pilot's seven nodes live in V7's "
                     "builder, read from the design's measurement record at its md5, not in the validator"),
        "not_moved": ("the design v0_1 and its measurement; the shapes pilot, V2b's and V5's redrafts, gate2's records, "
                      "V1's files and sp_reading_l6.py, each asserted at its md5; no corpus or served byte")}

    cl_old_lines = pinned.bytes_at(REPO, CL_REL, CL_WAS).decode("utf-8").splitlines()
    cl_new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(cl_old_lines, cl_new_lines) if x != y]
    assert len(cl_old_lines) == len(cl_new_lines) and cl_diff == [('  "canon": "project_canon_v38_52.json"',
                                                                   '  "canon": "project_canon_v38_53.json"')], cl_diff
    info = ctl["his_accounts_for_the_drafter"]
    am["record_notes_V6"] = [
        {"statement": "RV-6: the floors include X-032's EXIT patterns and L6's WIDE families as two lists",
         "measured": ("one literal instance of each of gate2's %d EXIT patterns is also a WIDE hit in %d of %d, so an EXIT "
                      "phrase turns floor-exit and floor-wide RED together; the self-test expects exactly that pair. "
                      "Kept as two checks so a WIDE-only hit and an EXIT hit stay distinguishable"
                      % (len(V.EXIT), sum(exit_in_wide), len(EXIT_SAMPLES)))},
        {"statement": "RV-6's pro-life floor lists 'life is a gift'",
         "measured": ("that phrase is the life-gift node's own claim, so a variant on life-gift cannot repeat it in its "
                      "text or residual; the drafter names the claim another way. A floor is not a census, and this one "
                      "fires on mention as well as use")},
        {"statement": "design section 2: his words appear only as quotation, verbatim, from the canon paths a variant names",
         "measured": ("RV-6's list does not check it, and the validator holds to that list. V7's builder asserts every "
                      "quoted span in a variant's text is an exact substring of an account its account_sources name, "
                      "and gate2 checks the quotes with its own instrument")},
        {"statement": "his ten accounts in relief_view_for_the_variant, quoted under RV-6's text rules",
         "measured": ("%d of %d trip no floor and %d of %d are pure ASCII, so each can be quoted verbatim inside the "
                      "ASCII text (the control record lists them)"
                      % (sum(not a["floor_hits"] for a in info), len(info), sum(not a["non_ascii"] for a in info),
                         len(info)))},
        {"statement": "shapes_redrafts_V5 pins r1_collision_list_l7_v0_1.json at %s" % CL_WAS,
         "measured": ("the record names the canon file present, so this bump moved it by exactly one line, its "
                      "'canon' field (v38_52 to v38_53); regenerated by the tool's own --write"),
         "record": dict(pin(CL_REL), was=CL_WAS)}]

    d["canon_version"] = "38.53"
    d["canon_version_marker"] = "v38.53"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    kept_tail = nrs["session"][nrs["session"].index("V4 takes the one (a)"):]
    assert kept_tail.startswith("V4 takes the one (a) after the successor map's pin; the (d)s enter the map")
    nrs["session"] = (
        "The pin is v4.1.5. V6 recorded his word on R0316 (RV-1..RV-8 adopted as leaned) and built response_variants/ on "
        "V1's pattern (schema, validator, --self-test control). Next, in order: (1) V7, seat l at max: the relief variant "
        "on the seven nodes (RV-7) from relief_view_for_the_variant, his accounts quoted verbatim, the measured anchors, "
        "a builder with --check, validator PASS 0, Berridge checked before any text uses it; (2) gate2's next round: the "
        "relief variant and the golden rule's third pass (R0317), drafter != judge; (3) his word; (4) the next declared "
        "pin session (safety_queue_L7, pin_queue_additions_R0292, the served-text repairs carried since L1 and LD3; the "
        "responseVariants render, RV-4, drawn by the design lane). " + kept_tail)
    nrs["V6_closed"] = {"state": "RECORDED (his word on R0316) and BUILT (response_variants/: schema, validator, control)",
                        "blocks": NEW_KEYS, "canon_writer_next": "seat l (V7), then gate2 (its next round)"}
    d["keyset_delta_ledger"]["v38_53_V6"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "V6 (seat l, 2026-10-04): his word on R0316 recorded verbatim from the user turn (RV-1..RV-8 adopted as leaned); "
        "response_variants/ built on V1's pattern: the schema (one closed type, relief-account, its label copied from "
        "canon), the validator (RV-6's %d checks; EXIT and WIDE imported at their md5) and its self-test control (%d of "
        "%d, every check RED by a mutation, the seven measured anchors as a real-data control). No pin."
        % (cs["checks"], cs["as_expected"], cs["cases"]))

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
    print("project_canon_v38_53.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
