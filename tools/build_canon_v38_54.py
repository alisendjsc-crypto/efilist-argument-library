#!/usr/bin/env python3
"""project_canon_v38_54.json -- MINOR canon bump, no release. V7 (seat l, 2026-10-04): the relief variant pilot
drafted (one relief-account variant on each of the seven pleasure-fork nodes, RV-7), drafted, not judged; R0319.

Adds to adversarial_map:
  relief_variants_pilot_V7   the draft: its files pinned, the nodes and anchors, the words, the validator run, the
                             builder's checks (the quote check among them) and controls, the source check, the pulls
                             gate2 is asked to read first; every value read from the builder's record at its md5
  berridge_check_V7          R0319 order 2: what was read at the source, with URLs, and what each record claims;
                             copied from the record, never retyped
  record_notes_V7            statements measured and corrected forward
and re-points next_recommended_session (gate2's round: the relief variant and RD-03 -> his word -> the next declared
pin).

Measured at run time, never typed: every md5, byte count, word count and check result. ccclxiv FIRST: v38_53
round-trips at this file's serialization, read at its md5 from the working tree or git history. Every top-level key
outside TOUCHED is asserted byte-identical; inside adversarial_map only the new keys are added. The served surfaces,
the design and its measurement, V6's checker, V5's redraft and the shapes files gate2's records pin are asserted at
their md5s. The gates it records run in their own process groups with TMPDIR in scratch.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): git mv v38_53 to v38_54, regenerate that record
with its own --write, then run this builder, which reads v38_53 from git history and overwrites v38_54.

  python3 tools/build_canon_v38_54.py [--out DIR]
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_53.json", "4bc14ae1a5fc6103df820900642f9728"
OUT = os.path.join(OUT_DIR, "project_canon_v38_54.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V7"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["relief_variants_pilot_V7", "berridge_check_V7", "record_notes_V7"]
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
KEPT = {"argument_shapes/shapes_redrafts_v0_1.json": "fc28cd12265e2712a9d610bbb2c1b69f",
        "argument_shapes/shapes_redrafts_record_v0_1.json": "ace5fb88886f7f7ce49a90658b590954",
        "argument_shapes/shapes_pilot_v0_1.json": "1f9c5da6166b538a90efa6dc7598124e",
        "argument_shapes/shapes_redrafts_judgments.json": "6f4974966c23920234f495cb20813d4c",
        "argument_shapes/shapes_pilot_judgments.json": "73503bccdd3ddf8b3a82f280181251d4",
        "adversarial_map_staging/r1/sp_reading_l6.py": "dc2525ef40fc5353a670484f511bd668"}
PILOT = {"staging": "response_variants/relief_variants_pilot_v0_1.json",
         "record": "response_variants/relief_variants_record_v0_1.json",
         "builder": "response_variants/build_relief_variants.py"}
VALIDATOR = "response_variants/response_variant_validator_v0_1.py"
KICKOFF = {"relay": "R0319", "md5": "bc1272c9aa8e2e5e82492673fdd7e94b"}
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
CL_REL = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
NEW_FILES = list(PILOT.values()) + ["tools/build_canon_v38_54.py", "README.md", "CHANGELOG.md"]

sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402


def md5b(b):
    return hashlib.md5(b).hexdigest()


def md5f(rel):
    return md5b(open(os.path.join(REPO, rel), "rb").read())


def pin(rel):
    return {"file": rel, "md5": md5f(rel), "bytes": os.path.getsize(os.path.join(REPO, rel))}


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


def kickoff_md5():
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) > 8 and f[1] == "SENT" and f[2] == KICKOFF["relay"]:
                assert f[8] == KICKOFF["md5"], "R0319: the index says %s" % f[8]
                return True
    return False


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_53 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in list(SERVED.items()) + list(KEPT.items()):
        assert md5f(rel) == m, "%s moved" % rel
    for blk in ("response_variants_design_V5", "shapes_redrafts_V5", "response_variants_build_V6"):
        for k, p in am[blk]["files"].items():
            assert md5f(p["file"]) == p["md5"], "%s's %s moved" % (blk, k)

    rec_raw = open(os.path.join(REPO, PILOT["record"]), "rb").read()
    rec = json.loads(rec_raw.decode("utf-8"))
    stg_raw = open(os.path.join(REPO, PILOT["staging"]), "rb").read()
    stg = json.loads(stg_raw.decode("utf-8"))
    assert rec["pins"]["staging"]["md5"] == md5b(stg_raw), "the record pins another staging file"
    assert rec["pins"]["canon"] == {"file": SRC_REL, "md5": SRC_MD5}, "the draft pins another canon"
    assert stg["meta"]["source_canon"] == {"file": SRC_REL, "md5": SRC_MD5}
    assert [v["variant_id"].split("/")[0] for v in stg["variants"]] == am["response_variants_rulings_V6"]["nodes_RV_7"]
    assert all(c["ok"] for c in rec["controls"]) and rec["controls"][0]["case"] == "C0"
    vr = rec["validator_run"]
    assert vr["verdict"] == "PASS" and vr["violation_count"] == 0 and vr["variants"] == 7
    kicked = kickoff_md5()

    scratch = tempfile.mkdtemp(prefix="canon_v38_54_")
    try:
        results = {}
        out = run([PILOT["builder"], "--check"], scratch)
        assert "matches the committed staging file and record" in out
        results["build_relief_variants --check"] = "GREEN: the staging file and record rebuilt byte for byte"
        out = run([VALIDATOR, PILOT["staging"]], scratch)
        tail = json.loads(out[out.rfind("\n{") + 1:])
        assert tail["verdict"] == "PASS" and tail["violation_count"] == 0 and tail["variants"] == 7
        results["response_variant_validator_v0_1 <staging>"] = (
            "GREEN: PASS, 0 violations, %d variants on %d nodes, all %d checks"
            % (tail["variants"], tail["nodes_with_variants"], len(vr["checks"])))
        out = run([VALIDATOR, "--self-test", "--check"], scratch)
        assert "reproduced byte for byte" in out
        results["response_variant_validator_v0_1 --self-test --check"] = "GREEN: the control record reproduced"
        out = run([VALIDATOR, "--embedded"], scratch)
        tail = json.loads(out[out.rfind("\n{") + 1:])
        assert tail["verdict"] == "PASS" and tail["variants"] == 0
        results["response_variant_validator_v0_1 --embedded"] = (
            "GREEN: PASS, %d variants in the corpus (the pilot is staging only)" % tail["variants"])
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    rows = rec["variants"]
    am["relief_variants_pilot_V7"] = {
        "state": ("DRAFTED, NOT JUDGED. gate2 judges it in its next round with RD-03 (R0317), drafter != judge (K258); "
                  "his word decides; the render waits for a declared pin, drawn by the design lane (RV-4); the game "
                  "leaves it out (RV-5). Staging only: not in the corpus, not served."),
        "kickoff": dict(KICKOFF, read_at_the_index=kicked),
        "files": {k: pin(v) for k, v in PILOT.items()},
        "type": stg["variants"][0]["type"],
        "label_rendered_by_the_page": rec["label_rendered_by_the_page"],
        "variant_coverage": stg["meta"]["variant_coverage"],
        "pins": {"corpus": stg["meta"]["source_corpus_md5"], "canon": stg["meta"]["source_canon"],
                 "objections_digest": stg["meta"]["source_corpus_objections_md5"]},
        "variants": [{"variant_id": r["variant_id"], "tier": r["tier"], "anchor": r["anchor"],
                      "razor_node": r["razor_node"], "text_words": r["text_words"], "text_md5": r["text_md5"],
                      "accounts_quoted": sorted({q["account"] for q in r["quotes"]}),
                      "his_words_in_text": r["his_words_in_text"]} for r in rows],
        "words": {k: rec["words"][k] for k in ("band", "min", "max", "total")},
        "how_drafted": ("each variant leads with the asymmetry of reliability his deprivation test establishes, gives "
                        "the relief thesis as his further inference, meets its node's sentence (the symmetric razor "
                        "head on at the three razor nodes), states the account at his strength (account [9]) and his "
                        "reason the library does not rest on it (account [0]), and ends on canon's open residual. "
                        "Attributed by role; the label is the type's; his words only as quotation."),
        "residual": rec["residual"],
        "validator_run": {"verdict": vr["verdict"], "violation_count": vr["violation_count"],
                          "variants": vr["variants"], "nodes_with_variants": vr["nodes_with_variants"],
                          "checks": vr["checks"]},
        "quote_check": {"rule": ("every double-quoted span in a variant's text and residual is an exact substring of an "
                                 "account its account_sources name, and every account named is quoted (the builder's "
                                 "quote-exact and sources-used; record_notes_V6 left this to V7's builder)"),
                        "quotes": sum(len(r["quotes"]) for r in rows),
                        "accounts_quoted": rec["source_check"]["accounts_quoted"],
                        "read_at_the_user_turns": rec["source_check"]},
        "builder_checks": rec["builder_checks"],
        "controls": [{k: c[k] for k in ("case", "mutation", "expect_red", "ok")} for c in rec["controls"]],
        "run_at_this_build": results,
        "pulls_for_gate2": rec["pulls_for_gate2"],
        "not_moved": rec["not_moved"]}

    am["berridge_check_V7"] = dict(rec["berridge_check"], copied_from="%s at %s" % (PILOT["record"], md5b(rec_raw)))

    cl_was = am["record_notes_V6"][-1]["record"]["md5"]
    cl_old_lines = pinned.bytes_at(REPO, CL_REL, cl_was).decode("utf-8").splitlines()
    cl_new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(cl_old_lines, cl_new_lines) if x != y]
    assert len(cl_old_lines) == len(cl_new_lines) and cl_diff == [('  "canon": "project_canon_v38_53.json"',
                                                                   '  "canon": "project_canon_v38_54.json"')], cl_diff
    found = {f["id"]: f for f in rec["found"]}
    am["record_notes_V7"] = [
        {"statement": ("neuroscience-positive-states#long: \"Dopamine encodes reward-prediction error\" ... the felt "
                       "positive \"is largely the experienced narrowing of a lack\""),
         "measured": found["F1"]["finding"]},
        {"statement": "R0290: two longs already run his mechanism locally",
         "measured": found["F2"]["finding"]},
        {"statement": "relief_view_for_the_variant: his ten accounts, verbatim, each with its turn md5",
         "measured": found["F3"]["finding"]},
        {"statement": "response_variants_build_V6 coverage: the pilot's seven nodes live in V7's builder",
         "measured": ("the builder reads the seven and their anchors from the design's measurement record at its md5 "
                      "and asserts them equal to nodes_RV_7; none is typed")},
        {"statement": "record_notes_V6 pins r1_collision_list_l7_v0_1.json at %s" % cl_was,
         "measured": ("the record names the canon file present, so this bump moved it by exactly one line, its "
                      "'canon' field (v38_53 to v38_54); regenerated by the tool's own --write"),
         "record": dict(pin(CL_REL), was=cl_was)}]

    d["canon_version"] = "38.54"
    d["canon_version_marker"] = "v38.54"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    kept_tail = nrs["session"][nrs["session"].index("V4 takes the one (a)"):]
    assert kept_tail.startswith("V4 takes the one (a) after the successor map's pin; the (d)s enter the map")
    nrs["session"] = (
        "The pin is v4.1.5. V7 drafted the relief variant: one relief-account variant on each of the seven pleasure-fork "
        "nodes (RV-7), from relief_view_for_the_variant, his accounts quoted verbatim and read at their user turns, the "
        "measured anchors, validator PASS 0, Berridge checked at the source; drafted, not judged "
        "(adversarial_map.relief_variants_pilot_V7). Next, in order: (1) gate2's round, drafter != judge (K258): the "
        "relief variant and the golden rule's third pass (R0317, RD-03); (2) his word; (3) the next declared pin session "
        "(safety_queue_L7, pin_queue_additions_R0292, the served-text repairs carried since L1 and LD3, the dopamine "
        "sentence V7 logged; the responseVariants render, RV-4, drawn by the design lane). " + kept_tail)
    nrs["V7_closed"] = {"state": "DRAFTED, NOT JUDGED (the relief variant pilot, seven nodes)",
                        "blocks": NEW_KEYS, "canon_writer_next": "gate2 (its next round), then seat l"}
    d["keyset_delta_ledger"]["v38_54_V7"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "V7 (seat l, 2026-10-04): the relief variant drafted on the seven fork nodes (RV-7) in response_variants/ "
        "(staging, %d-%d words each, his words only as quotation and read at their user turns); validator PASS 0; the "
        "builder's quote check and five controls; Berridge checked at the source (MEDLINE) and cited for the "
        "separability alone. Drafted, not judged. No pin." % (rec["words"]["min"], rec["words"]["max"]))

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
    print("project_canon_v38_54.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
