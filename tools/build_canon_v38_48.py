#!/usr/bin/env python3
"""project_canon_v38_48.json -- MINOR canon bump, no release. V2 (seat l, 2026-10-03): the words owed to canon since
R0274, recorded verbatim, and the argument-shapes pilot, drafted (gate2 judges it in V3).

Adds to adversarial_map:
  vault_v2_rulings_R0274        his word on the vault's six V2 recommendations (2026-10-02), and the six, verbatim
  his_words_L8                  his words behind R0292, R0294, R0295 and R0296, and what each adopted
  relief_view_for_the_variant   his own account of pleasure, verbatim, for the variant drafter; the open residual
  love_from_the_void_intake_V2  his pointer (R0296): his own argument for life, first item of the post-pilot intake
  r_v6_candidates_V2            the self-objection candidates: adopted, and waiting for his word (R0288 F5)
  pin_queue_additions_R0292     two phrases for the next declared pin's queue, neutral wording
  shapes_pilot_V2               the pilot: pins, classes, measures; drafted, not judged
  record_notes_V2               three relay statements corrected forward
and re-points next_recommended_session (V3; the responseVariants design; the relief variant; the next declared pin).

His words come from tools/v38_48_his_words.json, cut byte-exact from the user turns by
tools/extract_his_words_v38_48.py and read here at its md5; this builder never needs the transcripts. One sentence is
carried by md5 only (the resentment line; the repository is public). Measured at run time, never typed: every md5 and
byte count; each queued phrase is asserted to occur exactly once at its locus in the pinned corpus. ccclxiv FIRST:
v38_47 round-trips at this file's serialization, read at its md5 from the working tree or git history. Every top-level
key outside TOUCHED is asserted byte-identical; inside adversarial_map only the new keys are added. The gates it records
run in their own process groups with TMPDIR in scratch.

  python3 tools/build_canon_v38_48.py [--out DIR]
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_47.json", "6e0d89f3bf6bc043b88928862b6e0fbf"
OUT = os.path.join(OUT_DIR, "project_canon_v38_48.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V2"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["vault_v2_rulings_R0274", "his_words_L8", "relief_view_for_the_variant", "love_from_the_void_intake_V2",
            "r_v6_candidates_V2", "pin_queue_additions_R0292", "shapes_pilot_V2", "record_notes_V2"]
WORDS = ("tools/v38_48_his_words.json", "b50c63fb501a9dad1da95075437d53b3")
EXTRACTOR = "tools/extract_his_words_v38_48.py"
CORPUS = ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1")
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
SHAPES = {"pilot": "argument_shapes/shapes_pilot_v0_1.json", "measure": "argument_shapes/shapes_pilot_measure_v0_1.json",
          "builder": "argument_shapes/build_shapes_pilot.py", "validator": "argument_shapes/shape_validator_v0_1.py",
          "control": "argument_shapes/shape_validator_control_v0_1.json", "schema": "argument_shapes/argument_shapes_schema_v0_1.json"}
RELAYS = {"R0274": "vault_v2_rulings_adopted", "R0288": "library_feed_analysis_and_triage",
          "R0290": "l8_close_l7_landed_pleasure_account", "R0292": "his_word_on_r0290_and_parsimony_argument",
          "R0294": "relief_view_second_answer_and_response_variants", "R0295": "v2_kickoff_canon_v38_48_then_shapes_pilot",
          "R0296": "v2_addendum_love_from_the_void"}
RELAY_MD5 = {"R0274": "777efbe4f0a18b99600589d299afac89", "R0288": "5bb74ce27902b58658244622549ea376",
             "R0290": "48dd92e12395241dc96c087b546ecfb6", "R0292": "3a7b0bf16209afa70a0d8aec88524a42",
             "R0294": "56af368a4be20ab774dbf28837fadbdc", "R0295": "bc1a9af420aaa0b1658babc784bd5819",
             "R0296": "7cc84b67983028fefa70d5ff7826c754"}  # read from RELAY_INDEX.tsv at V2; re-asserted when present
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
QUEUE = [("joy-outweighs-harms", "long", "the false claim that all pleasure is relief"),
         ("neuroscience-positive-states", "long", "the cruder antinatalist")]
F5 = ["td-005 and pj-057, at negative-util-aggregation", "yr-029's forced exposure, at policy-proposal",
      "yr-036 and td-007, at antinatalism-misanthropic", "the 2026-10-03 \"crash out\" sentence"]

sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402


def md5b(b):
    return hashlib.md5(b).hexdigest()


def md5f(rel):
    return md5b(open(os.path.join(REPO, rel), "rb").read())


def pin(rel):
    return {"file": rel, "md5": md5f(rel), "bytes": os.path.getsize(os.path.join(REPO, rel))}


def relay_md5s():
    """The SENT row of each relay, from the append-only index (outside the repository). When the desk is present every
    md5 here must equal the index's; without it, the md5s committed above stand."""
    got = {}
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) > 8 and f[1] == "SENT" and f[2] in RELAYS:
                got[f[2]] = f[8]
    return got


def run(args, scratch, ok_rc=(0,)):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
    p = subprocess.Popen([sys.executable] + args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, env=env, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        raise
    assert p.returncode in ok_rc, "%s: rc %d\n%s" % (" ".join(args), p.returncode, out[-2000:])
    return out


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_47 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in SERVED.items():
        assert md5f(rel) == m, "%s moved: no pin here" % rel

    W = json.loads(pinned.bytes_at(REPO, *WORDS).decode("utf-8"))
    X = W["excerpts"]

    def q(key):
        e = X[key]
        assert "text" in e and md5b(e["text"].encode("utf-8")) == e["md5"], key
        return {"verbatim": e["text"], "said": "%s UTC (America/Phoenix is UTC-7), %s transcript line %d" % (
            e["turn"]["utc"], e["turn"]["transcript"], e["turn"]["line"]), "turn_md5": e["turn"]["turn_md5"],
            "relay": e["relay"]}

    rmd5 = relay_md5s()
    for r, m in rmd5.items():
        assert m == RELAY_MD5[r], "%s: the index says %s" % (r, m)
    relays = {r: {"topic": t, "md5": RELAY_MD5[r]} for r, t in RELAYS.items()}

    corpus = json.loads(pinned.bytes_at(REPO, *CORPUS).decode("utf-8"))
    O = {o["id"]: o for o in corpus["objections"]}
    for node, locus, phrase in QUEUE:
        text = O[node]["responses"][locus]
        assert text.count(phrase) == 1, "%s#%s: %r occurs %d times" % (node, locus, phrase, text.count(phrase))

    meas = json.loads(open(os.path.join(REPO, SHAPES["measure"]), encoding="utf-8").read())
    assert meas["pins"]["pilot"]["md5"] == md5f(SHAPES["pilot"]), "the measurement pins another pilot"
    scratch = tempfile.mkdtemp(prefix="canon_v38_48_")
    try:
        results = {}
        for name, args in [("shape_validator_v0_1 --self-test --check", [SHAPES["validator"], "--self-test", "--check"]),
                           ("shape_validator_v0_1 shapes_pilot_v0_1.json", [SHAPES["validator"], SHAPES["pilot"]]),
                           ("build_shapes_pilot --check", [SHAPES["builder"], "--check"])]:
            out = run(args, scratch)
            results[name] = "GREEN"
            if name.endswith(".json"):
                tail = json.loads(out[out.rfind("\n{") + 1:])
                assert tail["verdict"] == "PASS" and tail["violation_count"] == 0
                results[name] = "GREEN: PASS, %d shapes, %d violations" % (tail["shapes"], tail["violation_count"])
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    rec6 = W["recommendations_R0274"]
    am["vault_v2_rulings_R0274"] = {
        "his_word": q("R0274_word"),
        "whole_message": {"note": "~/Documents/Obsidian Vault/raw/notes/2026-10-02-library-crossref-rulings-and-pleasure.md",
                          "note_md5": "58121d1f5b930d2e22fd3d61154bd322", "message_md5": X["R0274_word"]["turn"]["turn_md5"],
                          "read": "at the user turn (vault V2 transcript), not at a search hit; the note's message_md5 equals the turn's"},
        "the_six_adopted": {"verbatim": rec6["items"], "from": {"file": rec6["file"], "md5": rec6["md5"], "lines": rec6["lines"]},
                            "whose": rec6["whose"]},
        "status": {"1": "standing: the crossref's conflicts (7 primary, 33 secondary) are a queue for his rulings; L changes nothing in them on its own",
                   "2": "the relief view goes beside the concession on six entries; vehicle superseded by R0294 (responseVariants, designed after this pilot); the concession stays",
                   "3": "pj-016, pj-127, yr-017: R-V6 self-objection candidates after the pilot (r_v6_candidates_V2)",
                   "4": "love-from-the-void, pro-exposure-to-horror, waking-up-here-again, the-judgment: variations-intake candidates after the pilot is judged; love-from-the-void first (R0296)",
                   "5": "standing: at every pin move the vault regenerates its mirror; the pin session's close relays one line to code",
                   "6": "carried out by the vault: the Facebook ingest (kickoff R0277, close R0280), reported to seat l at R0281: 5 of 38 silent entries changed, context only, no library change"},
        "relay": relays["R0274"]}
    am["his_words_L8"] = {
        "R0292": {"his_word": q("R0292_word"), "with_it": [q("R0292_keep_to_it"), q("R0292_open_disagreement")],
                  "adopts": ["two phrases go to the next declared pin's queue for neutral wording (pin_queue_additions_R0292)",
                             "R0274 item 2's variant is drafted from his own account, after this pilot; drafter != judge, then his word (vehicle: see R0294)",
                             "his resentment line joins the R-V6 self-objection candidates, his 2026-10-03 framing beside it, adversarial side only (r_v6_candidates_V2)",
                             "withdrawn, no action: R0288 F2 ('matters absolutely' stays) and F3 (the descriptions of antinatalists stay)"],
                  "relay": relays["R0292"]},
        "R0294": {"his_word": q("R0294_word"),
                  "adopts": ["the vehicle for alternative rebuttals is a per-node responseVariants locus, not RWE: typed variants, labelled as not the library's chosen line, behind a toggle at long depth; the RSI-graded answer stays the default. The variations lane designs it after this pilot and pilots it on the six pleasure-fork nodes, his relief account first; a note is the fallback for a single node only",
                             "the pleasure disagreement is registered as an open residual, in the honest-residuals register's manner, never as a win"],
                  "supersedes": "R0292's item 2 on the vehicle only", "relay": relays["R0294"]},
        "R0295": {"his_word": q("R0295_word"), "produced": "R0295 (this session's kickoff) and its addendum R0296", "relay": relays["R0295"]},
        "R0296": {"his_word": q("R0296_pointer"), "relay": relays["R0296"]},
        "rule": "Quote his words; never paraphrase them. Each verbatim above is an exact slice of the user turn named, pinned by the turn's md5."}
    am["relief_view_for_the_variant"] = {
        "for": "the relief variant's drafter (next_recommended_session item 3), drafter != judge, then his word",
        "his_accounts_verbatim": [q("R0274_pleasure_account"), q("R0290_not_a_mirror"), q("R0290_numbers_game"),
                                  q("R0290_relief_account"), q("R0292_argument"), q("R0294_account"),
                                  q("R0294_alternative"), q("R0294_relief_thesis_noted"),
                                  q("R0295_parsimony_and_deprivation_test"), q("R0296_concession")],
        "the_open_residual": ("Where both sides stop, by his words and the seat's: whether a deficit's constant co-presence "
                              "shows that every good is that deficit shrinking. Neither side claims proof; his words: "
                              "\"I admit the gap\" and \"I concede that i reliability doesn't prove the point\". The variant "
                              "states his view as an alternative the library chose not to rest on, never as a correction, and "
                              "registers the disagreement as open."),
        "drafting_notes": {"whose": "the seats', not his (R0292, R0295 addendum)",
                           "points": ["carry his parsimony move and his base-state evidence at full strength",
                                      "lead with the asymmetry of reliability his deprivation test establishes (suffering can be guaranteed by removing inputs; pleasure cannot be guaranteed by adding them), then the relief thesis as his further inference, then the open residual",
                                      "name the objection the variant must meet: the introspection that reports hunger as bad also reports eating as good",
                                      "Berridge's liking/wanting dissociation was cited from memory at L8 and is unverified: check the source before any text uses it"]},
        "existing_corpus_uses": "masochist-counterexample and neuroscience-positive-states#short already run his mechanism locally (R0290)"}
    am["love_from_the_void_intake_V2"] = {
        "his_pointer": q("R0296_pointer"),
        "what": ("his 'Esoteric Argumentation For Life [Hypothetical-Conjecture]' (vault wiki/concepts/love-from-the-void.md; "
                 "pt-037, pt-030, em-009; short version pt-023): an argument FOR continued life, from an unknown, possible good "
                 "grounded in autogenesis, modal rather than technological. Read the vault notes (authorship: josiah only) before "
                 "quoting any of them."),
        "placement": ("The FIRST item of the post-pilot variations intake (R0274 item 4), after the pilot is judged, on the "
                      "adversarial side only, as his self-objection (L1a: earning trust by openly challenging his own beliefs)."),
        "lean": "it may be a future-solve shape or a new (c); the intake decides by the map's class law",
        "reserved_move": ("its modal move, that a good able to make up for suffering is not impossible, so waiting for it is "
                          "not illogical, is reserved for the intake; no pilot shape uses it (asserted by build_shapes_pilot.py)"),
        "nearest_loci": "future-solve (which answers the technological 'future will fix it' and the proxy gamble, not a modal 'not impossible'); the no-compensation lines of life-gift and joy-outweighs-harms, which it contradicts",
        "safety": ("It argues for life, so it lives on the adversarial side as his self-objection. It never enters the harness "
                   "or the flagship's answering voice (his 2026-09-25 bar: never pro-life)."),
        "attestation": "his pt/em texts are his own writing; whether they count as attested (published, checkable) or self-attested is for the intake to settle with his word; do not cite them as published until the venue is checked",
        "corrects_forward": "R0288 F6 said love-from-the-void 'sits beside red-button'; wrong (R0296): it is an argument for continued life",
        "relay": relays["R0296"]}
    am["r_v6_candidates_V2"] = {
        "adopted": [{"items": ["pj-016", "pj-127", "yr-017"], "by": "R0274 item 3, his word of 2026-10-02"},
                    {"items": ["his resentment line (R0290)"], "by": "R0292 item 3, his word of 2026-10-03",
                     "carried_by_md5_only": {k: X["R0290_resentment_line"][k] for k in ("md5", "offsets", "turn", "words", "text_withheld")},
                     "with": "his 2026-10-03 framing quoted beside it, when the intake drafts it"}],
        "waiting_for_his_word": {"items": F5, "from": "R0288 F5", "lean": ("add them, with his word; any text near violence goes in "
                                 "with his 2026-10-03 gloss quoted beside it, never the 2014 lines alone; the pilot keeps off "
                                 "the suicide and violence nodes"), "asked": "in V2's close to josiah"},
        "where": "the new-objection intake (R-V6), after the pilot is judged; adversarial side only, never the flagship's voice"}
    am["pin_queue_additions_R0292"] = {
        "phrases": [{"locus": "%s#%s" % (n, l), "phrase": p, "occurs_at_locus": 1} for n, l, p in QUEUE],
        "lean_adopted": "neutral wording, e.g. 'a stronger claim the argument does not need'; the argument wins downstream either way",
        "rides": "the next declared pin session, with safety_queue_L7 and the carried served-text repairs; no pin of its own",
        "corpus": dict(zip(("file", "md5"), CORPUS))}
    m = meas["measures"]
    am["shapes_pilot_V2"] = {
        "state": "DRAFTED, NOT JUDGED. gate2 judges it in V3 (K258: never the seat that drafted it).",
        "files": {k: pin(v) for k, v in SHAPES.items()},
        "counts": meas["counts"], "validator_run": meas["validator_run"],
        "measures": {"right_card_another_objections": m["right_card_another_objections"],
                     "classes_against_R1": m["classes_against_R1"], "words_per_shape": m["words_per_shape"],
                     "bar_for_a_different_shape": m["bar_for_a_different_shape"]},
        "attestation": meas["attestation"],
        "routes_after_judgment": "(a) to the corpus in V4, on his word, after the successor map's pin; (b) to the regen queue; (d) to the map; (c) to the intake (R-V2)",
        "not_bumped": "the map validator; argumentShapes.<shape_id> becomes a map locus at the successor map's next validator bump",
        "run_at_this_build": results}
    cl_rel = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
    cl_old = am["successor_rulings_L7"]["instruments"]["collision_list_l7"]["record"]["md5"]
    old_lines = pinned.bytes_at(REPO, cl_rel, cl_old).decode("utf-8").splitlines()
    new_lines = open(os.path.join(REPO, cl_rel), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(old_lines, new_lines) if x != y]
    assert len(old_lines) == len(new_lines) and cl_diff == [('  "canon": "project_canon_v38_47.json"',
                                                             '  "canon": "project_canon_v38_48.json"')], cl_diff
    am["record_notes_V2"] = [
        {"statement": "successor_rulings_L7 pins r1_collision_list_l7_v0_1.json at %s" % cl_old,
         "measured": ("the record names the canon file of its run, so this bump moved it by exactly one line, its "
                      "'canon' field (v38_47 to v38_48); no row, verdict or count moved. Regenerated by the tool's own "
                      "--write so that --check stays a live gate. The record names a canon file, so every canon bump "
                      "moves it the same way; its next version should not. The instrument stays byte-identical."),
         "record": dict(pin(cl_rel), was=cl_old)},
        {"statement": "R0290 quoted his answer to R0288 as four paragraphs and said his 'Proceed on the previous \"yes to all\"' came the next turn",
         "measured": "it sits inside the same turn (L8 transcript line 337, 20:02 MST), between the third and fourth paragraphs; R0290's quote omits it without a mark",
         "verbatim": q("R0290_proceed_line")},
        {"statement": "R0295: ruling 6, 'the Facebook re-run, done at R0281'",
         "measured": "both true in part: the vault ran it under kickoff R0277 and closed it at R0280; R0281 is its report to seat l"},
        {"statement": "R0288 F6: love-from-the-void 'sits beside red-button'",
         "measured": "corrected by R0296: it is an argument for continued life (love_from_the_void_intake_V2)"}]

    d["canon_version"] = "38.48"
    d["canon_version_marker"] = "v38.48"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = (
        "The pin is v4.1.5. V2 recorded the words owed since R0274 and drafted the argument-shapes pilot (%d shapes over "
        "%d nodes; classes %s). Next, in order: (1) V3, gate2 judges the pilot, drafter != judge, then his word; "
        "(2) the responseVariants design (R0294), a small variations-lane session; (3) the relief variant, drafted from his "
        "words in relief_view_for_the_variant, judged by a seat that drafted none of it; (4) the next declared pin session, "
        "whose queue holds safety_queue_L7, the two phrases of pin_queue_additions_R0292 and the served-text repairs carried "
        "since L1 and LD3. After the pilot is judged: the variations intake, love-from-the-void first, then the R-V6 "
        "self-objection batch." % (meas["counts"]["shapes"], meas["counts"]["nodes"],
                                   " ".join("%s%d" % (k, v) for k, v in meas["counts"]["classes"].items())))
    nrs["V2_closed"] = {"state": "DRAFTED (the pilot) and RECORDED (the owed words)", "blocks": NEW_KEYS}
    d["keyset_delta_ledger"]["v38_48_V2"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "V2 (2026-10-03): his words owed since R0274 recorded verbatim from the user turns (R0274's six V2 rulings; R0292; "
        "R0294; R0295; R0296's pointer to love-from-the-void, now the post-pilot intake's first item); the argument-shapes "
        "pilot drafted on the six R-V4 nodes, validator PASS 0, for gate2 (V3). No pin.")

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-len(NEW_KEYS):] == NEW_KEYS and len(am) == len(am_before) + len(NEW_KEYS)
    assert not any(k.startswith("R1_progress_L") for k in NEW_KEYS)
    assert X["R0290_resentment_line"].get("text") is None and "text" not in am["r_v6_candidates_V2"]["adopted"][1]["carried_by_md5_only"]
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_48.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
