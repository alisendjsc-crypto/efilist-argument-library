#!/usr/bin/env python3
"""project_canon_v38_50.json -- MINOR canon bump, no release. V2b (seat l, 2026-10-03): his words on R0298 and R0308
recorded, his private statements by md5 only, and the two redrafts gate2's V3 judgment owed, drafted.

Adds to adversarial_map:
  his_words_V2b            his word on R0298 (F5's candidates; the resentment line md5-only) and on R0308 (the six asks;
                           V2's hand-off), verbatim, and what each adopted
  r_v6_adopted_V2b         R0288 F5's four candidates moved to adopted, the gloss rule with them, and the July line added
                           on the seat's lean (reversible), carried by md5 only
  private_statements_V2    his private statements of 2026-10-03 (R0300, R0302, R0304, and the rest of his 22:51 MST
                           turn), by turn and md5 only; no library change follows from them
  shapes_redrafts_V2b      SJ-003's statement and SJ-008's route, redrafted in a new file; drafted, not judged
  record_notes_V2b         four statements measured and corrected forward
and re-points next_recommended_session (gate2 round two; the responseVariants design; the relief variant; the next
declared pin).

His words come from tools/v38_50_his_words.json, cut byte-exact from the user turns by tools/extract_his_words_v38_50.py
and read here at its md5; this builder never needs the transcripts to produce its bytes. Measured at run time, never
typed: every md5 and byte count. ccclxiv FIRST: v38_49 round-trips at this file's serialization, read at its md5 from the
working tree or git history. Every top-level key outside TOUCHED is asserted byte-identical; inside adversarial_map only
the new keys are added. The gates it records run in their own process groups with TMPDIR in scratch. When the
transcript is on the machine, a leak check reads each private statement at its offsets and asserts that no run of seven
of its words occurs in anything this session writes; its output is not recorded, so the bytes are the same either way.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): move v38_49 aside as v38_50, regenerate that
record with its own --write, then run this builder, which reads v38_49 from git history and overwrites v38_50.

  python3 tools/build_canon_v38_50.py [--out DIR]
"""
import hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_49.json", "31186ff0c1939ba7292e908dfbb7ff4c"
OUT = os.path.join(OUT_DIR, "project_canon_v38_50.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V2b"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["his_words_V2b", "r_v6_adopted_V2b", "private_statements_V2", "shapes_redrafts_V2b", "record_notes_V2b"]
WORDS = ("tools/v38_50_his_words.json", "6f2d0c5e060de228cabe9b6bcc357890")
EXTRACTOR = "tools/extract_his_words_v38_50.py"
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
SHAPES = {"redrafts": "argument_shapes/shapes_redrafts_v0_1.json",
          "record": "argument_shapes/shapes_redrafts_record_v0_1.json",
          "builder": "argument_shapes/build_shapes_redrafts.py"}
REDRAFTS_RECORD_MD5 = "ace5fb88886f7f7ce49a90658b590954"
JUDGMENT = {"gate": "argument_shapes/shapes_judgments_gate.py", "reading": "argument_shapes/shapes_judgment_reading.py"}
VALIDATOR = "argument_shapes/shape_validator_v0_1.py"
RELAYS = {"R0299": "486c96f8be874784ab96dcdfd7191986", "R0300": "0ec1a18764a3f630093164d540cc5266",
          "R0302": "a28d2312361286e5f23d7a001e4b0e1b", "R0304": "16f4b671ccc7b8cd9e79b309decd4eb0",
          "R0307": "774b204484f0c8a28bf05bfba537c62c", "R0308": "f4112683a046d2bfc5b3811194929211",
          "R0309": "75d347417326463ac27baba0fbc514ea"}  # read from RELAY_INDEX.tsv at V2b; re-asserted when present
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
TRANSCRIPT = os.path.join(os.path.expanduser("~/.claude/projects"), "-home-josiahscooper-Projects-efilist-argument-library",
                          "b664995c-43f2-4ec1-877b-d18b71cb68d8.jsonl")
CL_REL = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
SCHOLAR_REPO = os.path.expanduser("~/D/Argue the Argument")
PRIVATE = ["R0300_gloss", "R0302_followup", "R0304_third_followup", "R0309_statement_2251"]
NEW_FILES = [WORDS[0], EXTRACTOR, SHAPES["redrafts"], SHAPES["record"], SHAPES["builder"], "tools/build_canon_v38_50.py",
             "argument_shapes/README.md", "README.md", "CHANGELOG.md"]

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


def shingles(text, n=7):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def leak_check(X, new_text):
    """Each private statement, read at its offsets in the transcript: no run of seven of its words may occur in the new
    canon content or in any file this session writes. Skipped (and said) when the transcript is absent."""
    if not os.path.exists(TRANSCRIPT):
        print("note: the transcript is absent; the leak check was not run (bytes unaffected)")
        return
    human = {}
    for line in open(TRANSCRIPT, encoding="utf-8"):
        o = json.loads(line)
        c = (o.get("message") or {}).get("content")
        if o.get("type") == "user" and isinstance(c, list):
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if o.get("type") == "user" and isinstance(c, str) and c.strip():
            human[md5b(c.encode("utf-8"))] = c
    hay = shingles(new_text)
    for k in PRIVATE:
        e = X[k]
        t = human[e["turn"]["turn_md5"]][e["offsets"][0]:e["offsets"][1]]
        assert md5b(t.encode("utf-8")) == e["md5"], k
        hit = shingles(t) & hay
        assert not hit, "LEAK: %s shares %d seven-word runs with what this session writes" % (k, len(hit))
    print("leak check: %d private statements, no seven-word run in anything written" % len(PRIVATE))


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_49 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in SERVED.items():
        assert md5f(rel) == m, "%s moved: no pin here" % rel

    W = json.loads(pinned.bytes_at(REPO, *WORDS).decode("utf-8"))
    X = W["excerpts"]
    for k in PRIVATE:
        assert "text" not in X[k] and X[k].get("text_withheld"), k

    def q(key):
        e = X[key]
        assert "text" in e and md5b(e["text"].encode("utf-8")) == e["md5"], key
        return {"verbatim": e["text"], "said": "%s UTC (America/Phoenix is UTC-7), V2 transcript line %d" % (
            e["turn"]["utc"], e["turn"]["line"]), "turn_md5": e["turn"]["turn_md5"],
            "answers_message": {"line": e["answers_message"]["line"], "text_md5": e["answers_message"]["text_md5"]}}

    def by_md5(key):
        e = X[key]
        return {"turn": {"transcript": "V2 (%s)" % W["transcript"]["V2"], "line": e["turn"]["line"],
                         "utc": e["turn"]["utc"], "turn_md5": e["turn"]["turn_md5"]},
                "offsets": e["offsets"], "md5": e["md5"], "words": e["words"],
                "whole_turn": bool(e.get("whole_turn")), "text_withheld": e["text_withheld"]}

    rmd5 = relay_md5s()
    for r, m in rmd5.items():
        assert m == RELAYS[r], "%s: the index says %s" % (r, m)
    for r, row in W["relays"].items():
        assert row["md5"] == RELAYS[r], r
    rel = lambda r: {"relay": r, "md5": RELAYS[r]}  # noqa: E731

    rec = json.loads(open(os.path.join(REPO, SHAPES["record"]), encoding="utf-8").read())
    assert md5f(SHAPES["record"]) == REDRAFTS_RECORD_MD5, "the redrafts record moved"
    assert rec["pins"]["redrafts"]["md5"] == md5f(SHAPES["redrafts"]), "the record pins another redrafts file"
    assert rec["pins"]["his_words"]["md5"] == WORDS[1]

    scratch = tempfile.mkdtemp(prefix="canon_v38_50_")
    try:
        results = {}
        out = run([SHAPES["builder"], "--check"], scratch)
        results["build_shapes_redrafts --check"] = "GREEN"
        out = run([VALIDATOR, SHAPES["redrafts"]], scratch)
        tail = json.loads(out[out.rfind("\n{") + 1:])
        assert tail["verdict"] == "PASS" and tail["violation_count"] == 0
        results["shape_validator_v0_1 shapes_redrafts_v0_1.json"] = "GREEN: PASS, %d shapes, %d violations" % (
            tail["shapes"], tail["violation_count"])
        if os.path.exists(TRANSCRIPT):
            run([EXTRACTOR, "--check"], scratch)
        if os.path.isdir(os.path.join(SCHOLAR_REPO, ".git")):
            for args in ([JUDGMENT["gate"]], [JUDGMENT["gate"], "--self-test"], [JUDGMENT["reading"], "--check"]):
                run(args, scratch)
        else:
            print("note: the game's repository is absent; gate2's judgment gate was not run (bytes unaffected)")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    g = am["shapes_pilot_judgment_gate2"]
    rv6 = am["r_v6_candidates_V2"]
    am["his_words_V2b"] = {
        "R0298": {"his_word": q("R0298_word"), "recorded_by": rel("R0299"),
                  "adopts": ["V3: gate2 judges the pilot (done; adversarial_map.shapes_pilot_judgment_gate2)",
                             "R0288 F5's four candidates join the R-V6 self-objection batch, with the gloss rule "
                             "(r_v6_adopted_V2b)",
                             "the resentment line stays in canon by md5 only, as r_v6_candidates_V2 carries it"]},
        "R0308": {"his_word": q("R0308_word"), "recorded_by": rel("R0309"),
                  "answers": dict(rel("R0308"), seat="gate2 (V3)"),
                  "the_message_it_answers": ("V2's message of %s UTC (line %d): adopt all six asks, its lean "
                                             "matching gate2's on each, then hand the two redrafts and canon v38.50 to "
                                             "a fresh seat-l session" % (X["R0308_word"]["answers_message"]["utc"],
                                                                         X["R0308_word"]["answers_message"]["line"])),
                  "adopts": {"the_six_asks": [dict(a, adopted=True) for a in g["asks"]],
                             "from": "adversarial_map.shapes_pilot_judgment_gate2.asks (gate2's asks and leans)",
                             "the_hand_off": "a fresh seat-l session (V2b) drafts SJ-003's statement and SJ-008's "
                                             "route and writes canon v38.50 (shapes_redrafts_V2b)"},
                  "the_same_turn": "the rest of the turn is private (private_statements_V2)"},
        "read": ("each verbatim is an exact slice of the user turn named, pinned by the turn's md5, read at the user "
                 "turn and not at a search hit; %s at %s" % WORDS),
        "rule": "Quote his words; never paraphrase them."}
    am["r_v6_adopted_V2b"] = {
        "moved_to_adopted": {"items": rv6["waiting_for_his_word"]["items"],
                             "from": "adversarial_map.r_v6_candidates_V2.waiting_for_his_word (R0288 F5)",
                             "by": "his word on R0298 (his_words_V2b.R0298)"},
        "the_rule_adopted_with_them": {"lean": rv6["waiting_for_his_word"]["lean"],
                                       "from": "adversarial_map.r_v6_candidates_V2.waiting_for_his_word.lean"},
        "his_gloss": {"key": "R0300_gloss", "carried_by_md5_only": by_md5("R0300_gloss"), "relay": rel("R0300"),
                      "use": "quoted beside the lines it glosses when the intake drafts them, with his word"},
        "added_on_the_seats_lean": {
            "what": "his July 2026 line in the vault (fb-2026-07, body line 25), beside the 2026-10-03 sentence, "
                    "under the same gloss",
            "lean": "V2's (R0300), standing under his default rule; reversible by his word",
            "carried_by_md5_only": W["july_line"]},
        "the_batch_now": ["pj-016, pj-127, yr-017 (R0274 item 3)", "the resentment line (R0292 item 3)",
                          "R0288 F5's four (R0298)", "the July line (the seat's lean)"],
        "where": rv6["where"],
        "the_bar": "his 2026-09-25 safety bar binds every entry, in his words at "
                   "adversarial_map.safety_pass_LANDED_L6.the_bar.his_words_verbatim"}
    am["private_statements_V2"] = {
        "rule": ("His private statements are recorded here by turn and md5 only. The texts live in the relays named, "
                 "on the operator's desk, and never enter this public repository as text (R0309's law). Each relay's "
                 "quotation was asserted equal to its turn."),
        "statements": [dict(by_md5(k), key=k, relay=rel(r)) for k, r in
                       (("R0300_gloss", "R0300"), ("R0302_followup", "R0302"), ("R0304_third_followup", "R0304"),
                        ("R0309_statement_2251", "R0309"))],
        "the_22_51_turn": "the statement is the turn up to his word on R0308, which closes it (his_words_V2b.R0308)",
        "library_change": "none; the R-V6 intake and the relief and metaethics forks read them, with his word, "
                          "before any text quotes them"}
    rows = rec["rows"]
    am["shapes_redrafts_V2b"] = {
        "state": rec["state"],
        "files": {k: pin(v) for k, v in SHAPES.items()},
        "authority": rec["authority"],
        "supersession": rec["supersession"],
        "rows": [{"id": r["id"], "shape_id": r["shape_id"], "answers": r["answers"]["row"],
                  "changed": r["changed"], "class": r["class"], "words": r["words"],
                  "terminus": {"via": r["terminus"]["via"], "via_anchor": r["terminus"]["via_anchor"],
                               "register": r["terminus"]["bedrock"]["register"],
                               "copied_from": r["terminus"]["copied_from"]}} for r in rows],
        "validator_runs": rec["validator_runs"],
        "pulls": {r["id"]: r["pulls"] for r in rows if r.get("pulls")},
        "sources": ("RD-01's Hare restatement rests on six records, each named with its URL and short verbatim "
                    "excerpts in the record; neither the article nor its reprint was read in full"),
        "after_round_two": rec["after_round_two"],
        "run_at_this_build": results,
        "not_moved": rec["not_moved"]}
    cl_old = g["collision_list_record_moved"]["md5"]
    old_lines = pinned.bytes_at(REPO, CL_REL, cl_old).decode("utf-8").splitlines()
    new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(old_lines, new_lines) if x != y]
    assert len(old_lines) == len(new_lines) and cl_diff == [('  "canon": "project_canon_v38_49.json"',
                                                             '  "canon": "project_canon_v38_50.json"')], cl_diff
    r0304 = W["relays"]["R0304"]
    am["record_notes_V2b"] = [
        {"statement": "R0304 gives its turn md5 as `md5`",
         "measured": ("a placeholder left unfilled; measured at the user turn, the turn's md5 is %s (R0309 carried its "
                      "first eight characters). The quotation itself equals the turn byte for byte." % (
                          X["R0304_third_followup"]["turn"]["turn_md5"])),
         "relay": dict(rel("R0304"), as_printed=r0304["turn_md5_as_printed"])},
        {"statement": "R0300 places the July line at fb-2026-07 'L25'",
         "measured": ("right in the vault's own numbering, which counts from the line after the front matter "
                      "(claude/tools/grep_sources.py); it is file line %d. The words R0300 quotes occur once more, "
                      "at file line %d." % (W["july_line"]["line"], W["july_line"]["also_at"][0]["line"]))},
        {"statement": "the pilot's attestation note for Hare 1988: 'a secondary summary of its thesis: we can harm "
                      "possible people by preventing them from becoming actual'",
         "measured": ("in the records this seat read, those words are the publisher's description of Essays on "
                      "Bioethics (1993), the collection that reprints the article as chapter 5. The article's own "
                      "opening, in the reprint's record, says that the possible person's interests have to be "
                      "considered. The redraft's harm clause rests on the collection's description; its weighed duty "
                      "rests on the opening and on the indexer's abstract (shapes_redrafts_V2b.sources)")},
        {"statement": "shapes_pilot_judgment_gate2 pins r1_collision_list_l7_v0_1.json at %s" % cl_old,
         "measured": ("the record names the canon file present, so this bump moved it by exactly one line, its "
                      "'canon' field (v38_49 to v38_50); regenerated by the tool's own --write"),
         "record": dict(pin(CL_REL), was=cl_old)}]

    d["canon_version"] = "38.50"
    d["canon_version_marker"] = "v38.50"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = (
        "The pin is v4.1.5. V2b drafted the two redrafts gate2's V3 judgment owed (SJ-003's statement, SJ-008's route) "
        "in a new file, and recorded his words on R0298 and R0308. Next, in order: (1) gate2 round two judges the two "
        "redrafts only (argument_shapes/shapes_redrafts_v0_1.json and its record), drafter != judge, then his word; "
        "(2) the responseVariants design (R0294); (3) the relief variant, drafted from relief_view_for_the_variant and "
        "judged by a seat that drafted none of it; (4) the next declared pin session (safety_queue_L7, "
        "pin_queue_additions_R0292, the served-text repairs carried since L1 and LD3). V4 takes the one (a) after the "
        "successor map's pin; the (d)s enter the map at its next validator bump (many-peaks and heroism now; the "
        "golden rule and soul-making once round two accepts them); the (c) goes to the intake, love-from-the-void "
        "first, and the R-V6 self-objection batch (r_v6_adopted_V2b) follows the pilot's judgment.")
    nrs["V2b_closed"] = {"state": "DRAFTED (the two redrafts) and RECORDED (his words on R0298 and R0308; his private "
                                  "statements by md5 only)", "blocks": NEW_KEYS,
                         "canon_writer_next": "gate2 (round two), then seat l"}
    d["keyset_delta_ledger"]["v38_50_V2b"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "V2b (seat l, 2026-10-03): his words on R0298 and R0308 recorded verbatim from the user turns; his private "
        "statements by md5 only; R0288 F5's four candidates adopted into the R-V6 batch; gate2's two AMENDs redrafted "
        "in a new file (the golden rule restates Hare's weighed duty; soul-making carried as (d) at HR-02), validator "
        "PASS 0, for gate2's round two. No pin.")

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-len(NEW_KEYS):] == NEW_KEYS and len(am) == len(am_before) + len(NEW_KEYS)
    assert json.loads(out.decode("utf-8")) == d

    new_text = json.dumps({k: am[k] for k in NEW_KEYS}, ensure_ascii=False) + json.dumps(
        [nrs["session"], nrs["V2b_closed"], d["keyset_delta_ledger"]["v38_50_V2b"], d["session_log_recent"][-1]],
        ensure_ascii=False)
    for rel_ in NEW_FILES:
        new_text += open(os.path.join(REPO, rel_), encoding="utf-8").read()
    leak_check(X, new_text)
    open(OUT, "wb").write(out)
    print("project_canon_v38_50.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
