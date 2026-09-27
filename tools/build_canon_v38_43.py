#!/usr/bin/env python3
"""project_canon_v38_43.json -- MINOR canon bump, no release. L7 (R0223): the successor map, drafted and not judged.

Adds to adversarial_map:
  successor_measure_L7                  where every entry of v1_6 stands in the v4.1.5 text (order 1)
  successor_drafts_L7                   the drafts record: 51 rows, what each kind did, the departures named, the R1
                                        verdicts proposed and not written
  validator_pin_v0_7                    the map validator's next version: argumentShapes.<shape_id> existence-gated
  terminal_assembly_v1_7_L7             the successor map, pinned to 7b6e65e5; v1_6 frozen beside it
  honest_residuals_register_pin_v0_8    the register carried to v1_7, and the one relation the adjacency gate owed
  carries_L7                            what is not the map's, or not yet
and re-points next_recommended_session.
Measured at run time, never typed: every md5 and byte count; the map, the register and its render are rebuilt into
scratch and must equal the working files byte for byte; the validator's derivation from v0_6 is re-run in memory; the
measure record is recomputed. ccclxiv FIRST: v38_42 is round-tripped at the serialization this file emits, read at its
md5 from the working tree or git history. Every top-level key outside TOUCHED is asserted byte-identical, and inside
adversarial_map only the six new keys are added.

  python3 tools/build_canon_v38_43.py [--out DIR]
Repo-relative. It owns its scratch (TMPDIR inside it) and its children's process groups.
"""
import collections, hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_42.json", "684a38034af0d4113cd4530a397e42e4"
OUT = os.path.join(OUT_DIR, "project_canon_v38_43.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L7", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["successor_measure_L7", "successor_drafts_L7", "validator_pin_v0_7", "terminal_assembly_v1_7_L7",
            "honest_residuals_register_pin_v0_8", "carries_L7"]
S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
FILES = {
    "measure": R + "/l7_measure_v0_1.json", "measure_control": R + "/l7_measure_control_v0_1.json",
    "measure_tool": R + "/l7_measure.py", "dossiers_tool": R + "/l7_dossiers.py",
    "drafts": R + "/L7_successor_drafts.json",
    "validator": S + "/adv_map_validator_v0_7.py", "validator_v0_6": S + "/adv_map_validator_v0_6.py",
    "validator_patch": "tools/patch_validator_v0_7.py",
    "map": S + "/adversarial_map_v1_7.json", "map_v1_6": S + "/adversarial_map_v1_6.json",
    "builder": S + "/build_assembly_v1_7.py", "controls": S + "/controls_v1_7.py",
    "controls_record": S + "/controls_v1_7_v0_1.json",
    "register": S + "/honest_residuals_register_v0_8.json", "register_md": S + "/honest_residuals_register_v0_8.md",
    "register_builder": S + "/build_register_v0_8.py", "register_render": S + "/render_register_v0_8.py",
    "register_v0_7": S + "/honest_residuals_register_v0_7.json",
}
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
KICKOFF = ("R0223", "78a6b9853ba6c83ae855f09d7127a8e6")
ORDER_WORDS = "Go with your recommendations on all of the above."

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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_42 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in SERVED.items():
        assert md5f(rel) == m, "%s moved: no pin here" % rel

    # ---- rebuild everything the blocks describe, in scratch, and require byte equality ----
    scratch = tempfile.mkdtemp(prefix="canon_v38_43_")
    try:
        run([R + "/l7_measure.py", "--check"], scratch=scratch)
        run(["tools/patch_validator_v0_7.py", "--check"], scratch=scratch)
        st = run([S + "/adv_map_validator_v0_7.py", "--self-test"], scratch=scratch)
        self_test = json.loads(st[st.rindex("{"):])
        assert self_test["_overall_pass"] and self_test["passed"] == self_test["cases"]
        run([S + "/build_assembly_v1_7.py", "--out", scratch], scratch=scratch)
        mapdir = os.path.join(scratch, S)
        run([S + "/build_register_v0_8.py", "--out", scratch], {"K348_MAP_DIR": mapdir}, scratch=scratch)
        run([S + "/render_register_v0_8.py", "--out", scratch], {"K348_MAP_DIR": mapdir}, scratch=scratch)
        for key in ("map", "register", "register_md"):
            rel = FILES[key]
            assert open(os.path.join(scratch, rel), "rb").read() == open(os.path.join(REPO, rel), "rb").read(), \
                "%s does not reproduce from its builder" % rel
        # regression: v0_6 and v0_7 give the same verdict on v1_6 against the corpus v1_6 pins
        pre = pinned.path_at(REPO, "efilist_argument_library_v4_0_0.json", "04bf6482aa0374ee92a81c1d55ec41f8")
        v6 = run([FILES["validator_v0_6"], FILES["map_v1_6"], "--corpus", pre, "--assembly"], scratch=scratch)
        v7 = run([FILES["validator"], FILES["map_v1_6"], "--corpus", pre, "--assembly"], scratch=scratch)
        extra = [l for l in v7.splitlines() if l not in v6.splitlines()]
        assert extra == ["shape-coverage: 0/0 argumentShapes loci carry >=1 entry"], extra
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    assert md5f(FILES["validator_v0_6"]) == "c002e93877b09d523daf786036af7a57", "v0_6 moved"
    assert md5f(FILES["map_v1_6"]) == "7a69bc9fd197047c3cf7cecdb37a44ed", "v1_6 moved"
    assert md5f(FILES["register_v0_7"]) == "bcbff23113f3fb0135d5fd5b3e2630d5", "register v0_7 moved"

    measure = json.load(open(os.path.join(REPO, FILES["measure"]), encoding="utf-8"))
    drafts = json.load(open(os.path.join(REPO, FILES["drafts"]), encoding="utf-8"))
    amap = json.load(open(os.path.join(REPO, FILES["map"]), encoding="utf-8"))
    reg = json.load(open(os.path.join(REPO, FILES["register"]), encoding="utf-8"))
    ctl = json.load(open(os.path.join(REPO, FILES["controls_record"]), encoding="utf-8"))
    mctl = json.load(open(os.path.join(REPO, FILES["measure_control"]), encoding="utf-8"))
    assert ctl["map"]["md5"] == md5f(FILES["map"]) and ctl["register"]["md5"] == md5f(FILES["register"])
    assert drafts["kickoff"]["md5"] == KICKOFF[1] and drafts["his_word"]["verbatim"] == ORDER_WORDS
    rows = drafts["rows"]
    kinds = collections.Counter((r["kind"], r["disposition"]) for r in rows)
    l7 = amap["meta"]["l7_successor"]
    by_disp = collections.defaultdict(list)
    for r in rows:
        if r.get("entry"):
            by_disp[r["disposition"]].append("%s%s %s" % (r["id"], (" #%d" % r["entry"]["n"]) if r["entry"]["n"] else "",
                                                          r["entry"]["target"]))
        elif r.get("new_entry"):
            by_disp[r["disposition"]].append("%s %s#%s" % (r["id"], r["new_entry"]["target_id"],
                                                           r["new_entry"]["target_locus"]))
    base_cc = dict(collections.Counter(e["class"] for e in json.load(
        open(os.path.join(REPO, FILES["map_v1_6"]), encoding="utf-8"))["entries"]))
    b_now = collections.defaultdict(list)
    for e in amap["entries"]:
        sl = e["provenance"].get("successor_L7")
        if sl and sl["from"].get("class", e["class"]) == "b" or (sl and "class" not in sl["from"] and e["class"] == "b"):
            b_now["(b) -> (%s)" % e["class"]].append("%s#%s" % (e["target_id"], e["target_locus"]))
    b_now = dict(sorted(b_now.items()))
    queue_b = ["%s#%s" % (e["target_id"], e["target_locus"]) for e in amap["entries"]
               if e["class"] == "b" and (e["provenance"].get("successor_L7") or e["provenance"].get("filed"))]

    am["successor_measure_L7"] = {
        "what": ("R0223 order 1: where every entry of the ruled map v1_6 stands in the v4.1.5 text, measured before a "
                 "word of the successor was drafted. The two knock-on records are inputs, read at their md5s; every row "
                 "of each is reproduced, or the instrument refuses."),
        "instrument": pin(FILES["measure_tool"]), "record": pin(FILES["measure"]),
        "control": dict(pin(FILES["measure_control"]), result=mctl["result"]),
        "chain": measure["chain"],
        "status_counts": measure["status_counts"],
        "survives_outside_a_repaired_sentence": len(measure["survives_outside_a_repaired_sentence"]),
        "routed_answers": len(measure["routes"]), "quoting_passages": len(measure["quotes"]),
        "agreement": measure["agreement"],
        "beyond_the_knock_on_records": {k: len(v) for k, v in measure["beyond_the_knock_on_records"].items()},
        "reading_instrument": dict(pin(FILES["dossiers_tool"]),
                                   note="one dossier per node the successor had to read; writes only under --out"),
        "commit": "390d2ca (order 1, pushed before any draft)"}
    am["successor_drafts_L7"] = {
        "state": "DRAFTED, NOT JUDGED. A seat that drafted none of it judges it (K258, the gate2 role); then his word.",
        "record": pin(FILES["drafts"]),
        "his_word": drafts["his_word"],
        "kickoff": {"relay": KICKOFF[0], "md5": KICKOFF[1]},
        "rows": len(rows),
        "by_kind": {"%s/%s" % k: v for k, v in sorted(kinds.items())},
        "by_disposition": {k: v for k, v in sorted(by_disp.items())},
        "proposed_r1_rows": l7["proposed_r1_rows"],
        "proposed_r1_note": ("No R1 row is written. Four re-judgments propose HOLDS on the repaired text (#11 on a "
                             "re-route, #22, #32, #50); each R1 row is appended only after gate2's judgment and his word, "
                             "as R1-070 was."),
        "departures_named": [
            "#48 (PF-02): not re-routed to the repaired slots; re-judged a (b) at its own slot (design s11.1, "
            "aggravation), which also carries X-033's defender-slot filing. The re-route would ship an (a) whose own "
            "target still says what its node withdrew.",
            "#11 (PF-05, X-028): PF-05 expected it to fail again. It is re-routed to "
            "self-effacing-under-universalization#long, whose Parfit sentence answers the Parfitian charge in the "
            "routed text, and HOLDS is proposed.",
            "Z-033: the kickoff's summary lists it among the (b)s; Z-033's own words ('file it where #45's and #47's "
            "charge already sits') and the class law make it a (d) at HR-02, with the wording carry in carries_L7.",
            "X-034: the source check was made. Bradley's own summary of his 2010 objection (in 'Asymmetries in "
            "Benefiting, Harming and Creating', The Journal of Ethics 17, 2013; penultimate version on his site) frames "
            "it in the logic of betterness, and that paper defends making someone better or worse off by creating her. "
            "The 2010 note itself was not read (its download link returned 404). Filed as a headline (b)."],
        "safety": ("His 2026-09-25 bar, read on every row that touches suicide or killing (why-not-suicide's long, "
                   "drifter, defender and blended slots; violence-as-reductio's sophisticate slot and long): no move "
                   "argues for anyone's death or anyone's continued life, and none speaks to the reader's own life."),
        "adjudication_rule": ("An entry whose (b) landed is adjudicated afresh under K346 (the strongest continuation "
                              "against the repaired text), the Phase R precedent; it is never assumed discharged into an "
                              "(a)."),
        "former_b_now": b_now}
    am["validator_pin_v0_7"] = {
        "artifact": FILES["validator"], "md5": md5f(FILES["validator"]), "bytes": size(FILES["validator"]),
        "derived_by": dict(pin(FILES["validator_patch"]),
                           note="11 anchored single-occurrence patches over v0_6, which stays byte-identical; --check re-derives it"),
        "base": {"file": FILES["validator_v0_6"], "md5": "c002e93877b09d523daf786036af7a57"},
        "self_test": "%d of %d (the 78 carried from v0_6, and 22 new: the shape locus both ways, the node bound, "
                     "shape_coverage, coverage, phase H in and S out)" % (self_test["passed"], self_test["cases"]),
        "adds": ["argumentShapes.<shape_id> as a map locus, existence-gated on the node's top-level argumentShapes list "
                 "(a shape counts only with a non-empty statement); locus_text reads the statement alone",
                 "the node bound: 3 + 3*(variant loci) + 3*(shape loci)",
                 "coverage excludes shape loci, as it excludes note (apparatus cannot satisfy 82/82)",
                 "shape_coverage, when declared, gated per file (ccclxx)",
                 "PHASES += H, the L7 successor filings; S stays the shapes' own letter (V1)"],
        "regression": ("v0_6 and v0_7 give identical verdicts on v1_6 against 04bf6482; v0_7 prints one more line, "
                       "shape-coverage 0/0. The corpus carries no shapes yet, so nothing moves until V4 puts them in."),
        "why": "R0223 order 3; design/variations section 4 (fcf6f6fe); R-V1, his word at V0 (variations_rulings_V0)."}
    am["terminal_assembly_v1_7_L7"] = {
        "artifact": os.path.basename(FILES["map"]), "md5": md5f(FILES["map"]), "bytes": size(FILES["map"]),
        "builder": pin(FILES["builder"]),
        "state": "DRAFTED, NOT JUDGED (the successor's changed and filed entries); everything else carried from v1_6.",
        "pinned_to": {"corpus": "7b6e65e5 (v4.1.5)", "objections_digest": amap["meta"]["source_corpus_objections_md5"]},
        "entries": amap["meta"]["entries"], "class_counts": amap["meta"]["class_counts"], "class_counts_v1_6": base_cc,
        "changed": l7["entries_changed"], "filed": l7["entries_filed"], "carried_byte_for_byte":
            l7["entries_carried_byte_for_byte"],
        "coverage": {"primary": "%d/82" % amap["meta"]["nodes_covered"], "variant": amap["meta"]["variant_coverage"],
                     "note": amap["meta"]["note_coverage"]},
        "validation": amap["meta"]["validation"],
        "controls": dict(pin(FILES["controls_record"]), result=ctl["result"]),
        "reproducible": "byte-identical under PYTHONHASHSEED 0 and 1, and from its builder at this canon's build",
        "predecessor": {"file": FILES["map_v1_6"], "md5": "7a69bc9fd197047c3cf7cecdb37a44ed",
                        "note": "FROZEN: never edited, never re-pinned; it stays pinned to 04bf6482"}}
    am["honest_residuals_register_pin_v0_8"] = {
        # the precedent's keys first: r1_quote_check.py and r1_dossiers.py read the NEWEST register pin by its artifact
        "artifact": os.path.basename(FILES["register"]), "md5": md5f(FILES["register"]), "bytes": size(FILES["register"]),
        "bedrocks": len(reg["bedrocks"]), "residue_entries": reg["meta"]["residue_entries"],
        "rendered": pin(FILES["register_md"]),
        "builder": pin(FILES["register_builder"]), "renderer": pin(FILES["register_render"]),
        "changes_from_v0_7": reg["meta"]["changes_from_v0_7"],
        "relations_drafted": reg["meta"]["adjacency"]["added_at_L7"],
        "parity": reg["meta"]["parity_with_v0_7"],
        "predecessor": {"file": FILES["register_v0_7"], "md5": "bcbff23113f3fb0135d5fd5b3e2630d5"}}
    am["carries_L7"] = {
        "the_b_for_the_next_queue": queue_b,
        "queue_gap": ("build_queue.py derives the regen queue from the A-E fragments only (K349's measured gap), so "
                      "these (b)s, phase H and the re-adjudicated ones alike, are adjudicated and unqueued until the "
                      "queue is built from the assembly."),
        "SF-05": ("survivor-testimony's psychMechanism, mirrored as mechanism_raw in MAP_GRAPH_DATA and "
                  "sidecars/map_graph_data.json: to the next pin that regenerates the Mechanism Web sidecar, with L1's "
                  "two served-text repairs."),
        "SF-07": ("two dependency edges graded strong at v3.5 partly on passages SW-04 and SC-01 removed "
                  "(DEP_REVIEW_NOTES['_premise_contextus-claudit']): to the next dependency review; the note stays."),
        "Z-033_wording": ("boonin-critique#long is the only locus that still says programming \"prevents honest "
                          "evaluation\"; the adjudication is the (d) filed there, and the phrase can be brought into the "
                          "safety pass's register in a later queue."),
        "boonin_lead": "L2's unverified Boonin lead (the 2012 article versus 'book-length treatment') stands, not checked here."}
    am_after = dict(am)

    d["canon_version"] = "38.43"
    d["canon_version_marker"] = "v38.43"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.5. Next: gate2 judges L7's successor drafts (adversarial_map_v1_7.json, "
                      "r1/L7_successor_drafts.json, register v0_8, validator v0_7) under K258, with the checkout held "
                      "idle; L7 redrafts on any AMEND; then his word, and L7 closes (the R1 rows it proposes are "
                      "appended only then). Beside it: V2 drafts the pilot's shapes (R-V4), which validator v0_7 can now "
                      "adjudicate as map loci once V4 puts them in the corpus; argue re-vendors v4.1.5 (R0222). After: "
                      "the next queue from carries_L7, adversarial wing v2 and /llms.txt, R2, the interconnection design, "
                      "and the new-objection intake (R-V6) once the pilot is judged.")
    nrs["L7_successor_map"] = {"state": "DRAFTED, NOT JUDGED", "blocks": NEW_KEYS}
    d["keyset_delta_ledger"]["v38_43_L7"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. No served byte moved." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "L7 (%s): the successor map over the v4.1.3 and v4.1.5 cuts, drafted and not judged: measure (every v1_6 entry, "
        "38 of 38 knock-on rows reproduced), 51 drafted rows, adversarial_map_v1_7.json (%d entries), register v0_8, "
        "validator v0_7 with the argumentShapes locus. No pin." % (DATE, amap["meta"]["entries"]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am_after[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-len(NEW_KEYS):] == NEW_KEYS and len(am) == len(am_before) + len(NEW_KEYS)
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_43.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()
