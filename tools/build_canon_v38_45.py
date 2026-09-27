#!/usr/bin/env python3
"""project_canon_v38_45.json -- MINOR canon bump, no release. L7, second round (R0243): gate2's 18 AMENDs redrafted.

Adds to adversarial_map:
  successor_redrafts_L7                 the 18 superseding rows (SM-52..SM-69), each answering its AMEND
  terminal_assembly_v1_8_L7             v1_7 plus the redrafts; v1_7 stays byte-identical (gate2's judgment pins it)
  honest_residuals_register_pin_v0_9    v0_8 plus the one delta the redrafts make (SM-69: HR-05 -> HR-02)
  knock_on_successor_L7                 the knock-on as a build control (gate2's U-064, adopted)
  successor_carries_L7_round2           U-065's answer (how the instruments admit the new (a)), the carries gate2
                                        names, and his two notes of 2026-09-26 on the /adversarial/ tab icon and the
                                        count icons, verbatim, with the seat's lean
and re-points next_recommended_session.
Measured at run time, never typed: every md5 and byte count; v1_8, register v0_9 and its render are rebuilt into scratch
and must equal the working files byte for byte; the knock-on record is recomputed; every moved-by-L7 move is checked
against gate2's own corpus-history patterns. ccclxiv FIRST: v38_44 is round-tripped at the serialization this file emits,
read at its md5 from the working tree or git history. Every top-level key outside TOUCHED is asserted byte-identical,
and inside adversarial_map only the new keys are added. A block of a kind a tool reads "newest of" carries the kind's
whole schema (the register pin leads with artifact, md5, bytes).

  python3 tools/build_canon_v38_45.py [--out DIR]
Repo-relative. It owns its scratch (TMPDIR inside it) and its children's process groups.
"""
import collections, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_44.json", "d6e0bad613c7a7ddfe99d384bca80ad3"
OUT = os.path.join(OUT_DIR, "project_canon_v38_45.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L7", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["successor_redrafts_L7", "terminal_assembly_v1_8_L7", "honest_residuals_register_pin_v0_9",
            "knock_on_successor_L7", "successor_carries_L7_round2"]
S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
FILES = {
    "drafts": R + "/L7_successor_drafts.json", "judgment": R + "/L7_successor_drafts_judgments.json",
    "map": S + "/adversarial_map_v1_8.json", "map_v1_7": S + "/adversarial_map_v1_7.json",
    "builder": S + "/build_assembly_v1_8.py", "controls": S + "/controls_v1_8.py",
    "controls_record": S + "/controls_v1_8_v0_1.json",
    "register": S + "/honest_residuals_register_v0_9.json", "register_md": S + "/honest_residuals_register_v0_9.md",
    "register_builder": S + "/build_register_v0_9.py", "register_render": S + "/render_register_v0_9.py",
    "register_v0_8": S + "/honest_residuals_register_v0_8.json",
    "knock": R + "/l7_knock_on_v0_1.json", "knock_tool": R + "/l7_knock_on.py",
    "knock_control": R + "/l7_knock_on_control_v0_1.json",
}
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
RELAY_BACK = ("R0243", "beecfc4003dfc0936dfa8a377782eef8")
HISTORY = [("now", r"\bnow\b"), ("still", r"\bstill (?:calls|says|reads|keeps)\b"), ("in place of", r"\bin place of\b"),
           ("since", r"\bhas since\b"), ("withdrew/withdrawn", r"\bwithdr(?:ew|awn)\b"), ("the repair", r"\bthe repair\b"),
           ("as repaired", r"\bas repaired\b"), ("the old", r"\bthe old\b(?! without)"), ("the new ground", r"\bthe new ground\b")]
HIS_NOTES = ["small wrinkle on the favicon icon for the adv library--not updated yet",
             "on other 2 screenshots: I think it would look more intriguing if the counts had icons for each of them, but "
             "only if you believe you could come up with another set of symbols that wouldn't feel meaningless",
             "note for later if you wish"]

sys.path.insert(0, os.path.join(REPO, R))
import pinned  # noqa: E402


def md5f(rel):
    return hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest()


def size(rel):
    return os.path.getsize(os.path.join(REPO, rel))


def pin(rel):
    return {"file": rel, "md5": md5f(rel), "bytes": size(rel)}


def run(args, env_extra=None, scratch=None):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if scratch:
        env["TMPDIR"] = scratch
    env.update(env_extra or {})
    p = subprocess.Popen([sys.executable] + args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, env=env, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        raise
    assert p.returncode == 0, "%s failed:\n%s" % (" ".join(args), out[-2000:])
    return out


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_44 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in SERVED.items():
        assert md5f(rel) == m, "%s moved: no pin here" % rel
    judged = am["successor_drafts_judgment_gate2"]
    assert md5f(FILES["judgment"]) == "bd3b4e89f25e7f874f5aa553b998fe0d", "gate2's record moved"
    assert md5f(FILES["map_v1_7"]) == "db40b45693eff1297b3f3152c6295c15", "v1_7 moved"
    assert md5f(FILES["register_v0_8"]) == "8f6d38886b95033600752a5be052bd99", "register v0_8 moved"

    scratch = tempfile.mkdtemp(prefix="canon_v38_45_")
    try:
        run([FILES["knock_tool"], "--check"], scratch=scratch)
        run([S + "/build_assembly_v1_8.py", "--out", scratch], scratch=scratch)
        mapdir = os.path.join(scratch, S)
        run([S + "/build_register_v0_9.py", "--out", scratch], {"K348_MAP_DIR": mapdir}, scratch=scratch)
        run([S + "/render_register_v0_9.py", "--out", scratch], {"K348_MAP_DIR": mapdir}, scratch=scratch)
        for key in ("map", "register", "register_md"):
            rel = FILES[key]
            assert open(os.path.join(scratch, rel), "rb").read() == open(os.path.join(REPO, rel), "rb").read(), \
                "%s does not reproduce from its builder" % rel
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    drafts = json.load(open(os.path.join(REPO, FILES["drafts"]), encoding="utf-8"))
    amap = json.load(open(os.path.join(REPO, FILES["map"]), encoding="utf-8"))
    reg = json.load(open(os.path.join(REPO, FILES["register"]), encoding="utf-8"))
    knock = json.load(open(os.path.join(REPO, FILES["knock"]), encoding="utf-8"))
    kctl = json.load(open(os.path.join(REPO, FILES["knock_control"]), encoding="utf-8"))
    ctl = json.load(open(os.path.join(REPO, FILES["controls_record"]), encoding="utf-8"))
    assert ctl["map"]["md5"] == md5f(FILES["map"]) and ctl["register"]["md5"] == md5f(FILES["register"])
    redrafts = [r for r in drafts["rows"] if r.get("supersedes")]
    touched = [e for e in amap["entries"]
               if any(k in e["provenance"] for k in ("successor_L7", "filed", "redrafted_L7"))]
    hist = sorted({name for e in touched for name, p in HISTORY if re.search(p, e["adversarial_move"])})
    assert not hist, "corpus-history wording left in a move: %s" % hist
    rd = amap["meta"]["l7_redrafts"]

    am["successor_redrafts_L7"] = {
        "state": "DRAFTED, NOT JUDGED: the second round, for a seat that drafted none of it (K258).",
        "answers": {"relay": RELAY_BACK[0], "md5": RELAY_BACK[1], "judgment": "successor_drafts_judgment_gate2"},
        "record": pin(FILES["drafts"]),
        "rows": [{"row": r["id"], "supersedes": r["supersedes"], "answers": r["answers"]} for r in redrafts],
        "what": ("16 rows restate a move against the v4.1.5 text as a reader meets it and change nothing else (U-063); "
                 "SM-55 (for SM-08) states the hub's condition as it stands, the floor clearing a threshold of serious harm "
                 "imposed without consent only if the anti-imposition weight survives, with the net-balance question left "
                 "open; SM-69 (for SM-45) presses the information paragraph's own diagnosis and runs to HR-02, gate2's lean, "
                 "by parity with SM-48, so the register follows."),
        "move_register_check": ("0 moves touched by L7 carry corpus-history wording, by gate2's own patterns "
                                "(l7_judgment_reading.py HISTORY), asserted at this canon's build."),
        "confinement": ("build_assembly_v1_8.py refuses a redraft that changes more than its AMEND names, answers a row "
                        "that is not an AMEND, or leaves an AMEND unanswered (controls B1-B3)."),
        "first_round_rows_untouched": "rows SM-01..SM-51 byte-identical: the record is append-only",
        "corrected_forward": ("controls_v1_7.py now stages the drafts record at the md5 build_assembly_v1_7.py pins "
                              "(fd9267f8), so the record's growth cannot turn its unmutated control RED (the L4c law for "
                              "R1_rulings.json). Its record, controls_v1_7_v0_1.json, is byte-identical.")}
    am["terminal_assembly_v1_8_L7"] = {
        "artifact": os.path.basename(FILES["map"]), "md5": md5f(FILES["map"]), "bytes": size(FILES["map"]),
        "builder": pin(FILES["builder"]),
        "state": "DRAFTED, NOT JUDGED (the 18 redrafted entries); everything else as gate2 judged it in v1_7.",
        "entries": amap["meta"]["entries"], "class_counts": amap["meta"]["class_counts"],
        "redrafted": len(rd["rows"]), "move_only": sum(1 for x in rd["rows"] if x["fields_changed"] == ["adversarial_move"]),
        "validation": amap["meta"]["validation"],
        "controls": dict(pin(FILES["controls_record"]), result=ctl["result"]),
        "reproducible": "byte-identical under PYTHONHASHSEED 0 and 1, and from its builder at this canon's build",
        "predecessor": {"file": FILES["map_v1_7"], "md5": "db40b45693eff1297b3f3152c6295c15",
                        "note": "stays byte-identical: gate2's judgment of the successor drafts pins it"}}
    am["honest_residuals_register_pin_v0_9"] = {
        "artifact": os.path.basename(FILES["register"]), "md5": md5f(FILES["register"]), "bytes": size(FILES["register"]),
        "bedrocks": len(reg["bedrocks"]), "residue_entries": reg["meta"]["residue_entries"],
        "rendered": pin(FILES["register_md"]), "builder": pin(FILES["register_builder"]),
        "renderer": pin(FILES["register_render"]),
        "changes_from_v0_8": reg["meta"]["changes_from_v0_8"], "parity": reg["meta"]["parity_with_v0_8"],
        "predecessor": {"file": FILES["register_v0_8"], "md5": "8f6d38886b95033600752a5be052bd99"}}
    am["knock_on_successor_L7"] = {
        "adopts": "gate2's U-064: a successor's controls run the knock-on after the drafts apply",
        "instrument": pin(FILES["knock_tool"]), "record": pin(FILES["knock"]),
        "control": dict(pin(FILES["knock_control"]), result=kctl["result"]),
        "a_entries_in_successor": knock["a_entries_in_successor"], "newly_collided": knock["newly_collided"],
        "read_by_gate2": knock["read_by_gate2"],
        "note": ("Keyed by entry identity (node, locus, anchor), so a flag re-anchored or re-classed at an answering locus "
                 "counts as new: 12 newly collided (a)s against gate2's 9 (U-054..U-062, keyed by map slot). The three more "
                 "(#32, #49, #53) are read by L7's own rows (SM-05, SM-09, SM-11), which gate2 accepted or confirmed. Every "
                 "one is read, or the build control fails.")}
    am["successor_carries_L7_round2"] = {
        "U_065_the_new_a": ("The (a) new at self-defeating#long has no R1 row: R1's evidence lists only v1_3's 69. L7's call, "
                            "said before any row is written: admit it through an evidence addendum (n=70, "
                            "r1/R1_evidence_L7_addendum.json) that new versions of the rulings gate and the collision list "
                            "read beside the evidence file; its R1 row is written with the other four after his word."),
        "U_001": "just-depressed's frequency claim at three places: the long's anchor sentence, its last paragraph, and the defender slot; the next queue takes them together with PF-01.",
        "U_066_safety_residuals": judged.get("safety_residuals_for_the_next_queue"),
        "U_066_ai_fear": "ai-fear's defender slot keeps \"The accelerationist grabbed the recommendation\"; the repair of SM-62's (b) takes it with the analogy.",
        "U_067": "X-033's analogy filing is weaker at why-not-suicide#long than at the defender slot (SM-58, minor).",
        "his_notes_2026_09_26": {
            "verbatim": HIS_NOTES,
            "said": "in chat to the L7 session, about 22:25 America/Phoenix, with screenshots of the /adversarial/ stat strip, its browser tab and the /libraries rail",
            "seat_lean": ("Tab icon: the mark is drawn, approved and served (/icon-adversarial.svg, afa3a69f); only the "
                          "page's <link rel=\"icon\"> in render_wing_v0_1.py is owed (R0167). Lean: wire it at L7's close as "
                          "a one-line change, no pin, read back live. Count icons: yes on the /adversarial/ strip, where "
                          "the counts are dispositions and LD2's outcome glyphs (R0159) already encode two of them, placed "
                          "with the plain-layer glosses; on the /libraries rail, only 'libraries' (the six library marks, as "
                          "'tiers' carries the tier marks); objections, mechanisms and attested deployments stay bare unless "
                          "the design lane draws each from its own data. Every mark a datum (his game-visuals rule).")}}

    d["canon_version"] = "38.45"
    d["canon_version_marker"] = "v38.45"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.5. Next: a seat that drafted none of it judges L7's 18 redrafts "
                      "(adversarial_map.successor_redrafts_L7; v1_8, register v0_9), a narrow second round: each "
                      "superseding move equals the drafted one but for the named wording, plus SM-55's and SM-69's content. "
                      "Then his word on R0244's four asks, conditional on that acceptance; then L7 closes: the R1 rows he "
                      "rules (#11, #22, #32, #50, and the new (a) at self-defeating#long through the evidence addendum), "
                      "canon records his word, and the /adversarial/ tab icon is wired if he does not object. Beside it: V2 "
                      "drafts the pilot's shapes (R-V4); argue re-vendors v4.1.5 (R0222). After: the next queue "
                      "(successor_carries_L7_round2 and carries_L7), adversarial wing v2 and /llms.txt, R2, the "
                      "interconnection design, and the new-objection intake (R-V6) once the pilot is judged.")
    nrs["L7_successor_redrafts"] = {"state": "DRAFTED, NOT JUDGED", "blocks": NEW_KEYS}
    d["keyset_delta_ledger"]["v38_45_L7"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. No served byte moved." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "L7 (%s), second round: gate2's 18 AMENDs redrafted as superseding rows (SM-52..SM-69); adversarial_map_v1_8.json "
        "(v1_7 plus the redrafts), register v0_9 (SM-69 moves to HR-02), the knock-on as a build control (U-064). "
        "No pin." % DATE)

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-len(NEW_KEYS):] == NEW_KEYS and len(am) == len(am_before) + len(NEW_KEYS)
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_45.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()
