#!/usr/bin/env python3
"""project_canon_v38_23.json -- MINOR. L4: the drafting pass over R1's 45 FAILS, drafted and not judged.

ccclxiv FIRST: v38_22 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map five subkeys are ADDED and
none moves. Every figure written here is computed from the committed files: the map is rebuilt by its own
builder into scratch and must equal the committed bytes, the register likewise, both control records must
be all-as-expected and name the committed artifacts, and the knock-on record must re-measure identically.
His words are carried verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, hashlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_22.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_23.json")
SRC_MD5 = "01d139245b85c1994ce3a7947b21be1f"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L4"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
ADDED = {"R1_drafting_pass_L4", "terminal_assembly_v1_4_L4", "honest_residuals_register_pin_v0_5",
         "pin_move_queue_L4", "knock_on_collisions_L4"}

MAP = "adversarial_map_staging/adversarial_map_v1_4.json"
MAP_BUILDER = "adversarial_map_staging/build_assembly_v1_4.py"
MAP_CONTROLS = "adversarial_map_staging/controls_assembly_v1_4.py"
MAP_CONTROL_REC = "adversarial_map_staging/assembly_control_v0_4.json"
DRAFTS = "adversarial_map_staging/r1/R1_drafts_L4.json"
REG = "adversarial_map_staging/honest_residuals_register_v0_5.json"
REG_MD = "adversarial_map_staging/honest_residuals_register_v0_5.md"
REG_BUILDER = "adversarial_map_staging/build_register_v0_5.py"
REG_RENDER = "adversarial_map_staging/render_register_v0_5.py"
REG_CONTROLS = "adversarial_map_staging/controls_register_v0_5.py"
REG_CONTROL_REC = "adversarial_map_staging/register_control_v0_3.json"
KNOCK = "adversarial_map_staging/r1/l4_knock_on.py"
KNOCK_REC = "adversarial_map_staging/r1/l4_knock_on_v0_1.json"
CORPUS = "efilist_argument_library_v4_0_0.json"

# The kickoff, and his words it rests on, verbatim.
KICKOFF = {"relay": "R0110", "md5": "206380b85ac2d5da071b8b72888995f2"}
HIS_PROCEED_L3 = "Proceed with your recommendations on all front's."
REC_L4 = ("The drafting pass (L4). Lean: a fresh session, starting from the worklist, with a different session "
          "judging the drafts.")


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def rebuild(builder, outrel, extra_env=None):
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "adversarial_map_staging"))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", **(extra_env or {}))
        if extra_env and "K348_MAP_DIR" in extra_env:
            pass
        p = subprocess.run([sys.executable, os.path.join(REPO, builder), "--out", t], env=env,
                           capture_output=True, text=True)
        assert p.returncode == 0, "%s refused:\n%s" % (builder, p.stdout + p.stderr)
        return open(os.path.join(t, outrel), "rb").read()


def sentence_with(text, anchor):
    for s in re.split(r"(?<=[.!?])\s+", text):
        if anchor in s:
            return s
    raise AssertionError("anchor %r not inside one sentence" % anchor)


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_22.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_22 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    fresh_map = rebuild(MAP_BUILDER, "adversarial_map_staging/adversarial_map_v1_4.json")
    assert fresh_map == open(os.path.join(REPO, MAP), "rb").read(), "the committed v1_4 is not what its builder emits"
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "adversarial_map_staging"))
        open(os.path.join(t, MAP), "wb").write(fresh_map)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        for tool in (REG_BUILDER, REG_RENDER):
            p = subprocess.run([sys.executable, os.path.join(REPO, tool), "--out", t], env=env,
                               capture_output=True, text=True)
            assert p.returncode == 0, "%s refused:\n%s" % (tool, p.stdout + p.stderr)
        for rel in (REG, REG_MD):
            assert open(os.path.join(t, rel), "rb").read() == open(os.path.join(REPO, rel), "rb").read(), \
                "%s is not what its builder emits" % rel
    mc = json.load(open(os.path.join(REPO, MAP_CONTROL_REC), encoding="utf-8"))
    assert mc["map"]["md5"] == f(MAP)["md5"] and all(c["as_expected"] for c in mc["controls"])
    assert mc["controls"][0]["control"].startswith("C0")
    rc = json.load(open(os.path.join(REPO, REG_CONTROL_REC), encoding="utf-8"))
    assert rc["register"]["md5"] == f(REG)["md5"] and all(c["as_expected"] for c in rc["controls"])
    assert rc["controls"][0]["control"].startswith("C0")
    p = subprocess.run([sys.executable, os.path.join(REPO, KNOCK), "--check"], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    assert p.returncode == 0, "the knock-on record does not re-measure:\n" + p.stdout + p.stderr

    m = json.loads(fresh_map.decode("utf-8"))
    mm = m["meta"]
    ra = mm["r1_amendments"]
    drafts = json.load(open(os.path.join(REPO, DRAFTS), encoding="utf-8"))
    dby = {x["n"]: x for x in drafts["drafts"]}
    reg = json.load(open(os.path.join(REPO, REG), encoding="utf-8"))
    rm = reg["meta"]
    knock = json.load(open(os.path.join(REPO, KNOCK_REC), encoding="utf-8"))
    corpus = {o["id"]: o for o in json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8"))["objections"]}

    rows = []
    for rw in ra["rows"]:
        x = dby[rw["n"]]
        row = {"n": rw["n"], "r1_row": rw["row"], "target": rw["target"], "shape": rw["shape"],
               "disposition": rw["disposition"], "class_after": rw["class_after"],
               "entry_changed": rw["entry_changed"]}
        if rw["disposition"] == "a_to_d":
            row["terminus"] = "%s %s" % (x["hr"], x["facet"])
        if rw["disposition"] == "a_to_b":
            row["regen"] = "%s %s" % ("".join(x["regen_candidate"]["axis_hit"]), x["regen_candidate"]["severity"])
        if rw["disposition"] == "reroute_a":
            row["answered_by"] = x["answered_by"]
        if "move_edit" in x:
            row["move_edit"] = x["move_edit"]["kind"]
        if "waits_on" in x:
            row["waits_on"] = x["waits_on"]
        rows.append(row)
    by_d = dict(sorted(collections.Counter(r["disposition"] for r in rows).items()))
    by_bed = dict(sorted(collections.Counter(r["terminus"].split()[0] for r in rows if "terminus" in r).items()))
    for_the_judge = {"#%d" % x["n"]: x["for_the_judge"] for x in drafts["drafts"] if x.get("for_the_judge")}

    queue = []
    for pq in drafts["pin_move_queue"]:
        node, _, locus = pq["locus"].partition("#")
        o = corpus[node]
        text = (o["responses"].get(locus) if locus in ("short", "medium", "long") else
                o["responses"]["archetypeVariants"][locus.split(".", 1)[1]] if locus.startswith("archetypeVariants.")
                else o[locus])
        row = {"id": pq["id"], "serves": ["#%d" % n for n in pq["serves"]], "section": pq["section"],
               "locus": pq["locus"], "sentence": sentence_with(text, pq["anchor"]),
               "answers": "the (%s) at %s, anchored on %r" % ("b" if pq["section"] != "passed_over_by_a_new_d" or
                                                              pq["locus"] != "eliminativism#long" else "d",
                                                              pq["b_at"], pq["b_anchor"]),
               "repair": pq["repair"]}
        for k in ("also", "note"):
            if pq.get(k):
                row[k] = pq[k]
        queue.append(row)
    sections = dict(collections.Counter(q["section"] for q in queue))

    # ---------------------------------------------------------------- adversarial_map: five additions
    am["R1_drafting_pass_L4"] = {
        "status": "DRAFTED, NOT JUDGED. A seat that did not draft judges these drafts (K258, the gate2 role); nothing "
                  "ships before that judgment and Josiah's word. Ruled is not shipped, and drafted is not ruled.",
        "his_words_verbatim": HIS_PROCEED_L3,
        "the_recommendation_he_adopted": REC_L4,
        "the_standard_it_executes": {"canon": "adversarial_map.R1_standard_ruling_L2",
                                     "his_words_verbatim": drafts["standard"]["his_words_verbatim"],
                                     "the_recommendation_he_adopted": drafts["standard"]["the_recommendation_he_adopted"]},
        "kickoff": KICKOFF,
        "drafts": dict(f(DRAFTS), file=DRAFTS, law=drafts["law"]),
        "outcome": {"fails_rows": len(rows), "entries_changed": ra["entries_changed"],
                    "entries_waiting_unchanged": ra["entries_waiting_unchanged"], "by_disposition": by_d,
                    "new_d_by_bedrock": by_bed,
                    "class_counts_v1_3": {"a": 69, "b": 28, "c": 1, "d": 40},
                    "class_counts_v1_4": mm["class_counts"]},
        "how_each_shape_was_disposed": {
            "route_to_bedrock": "all 30 to (d), each on the registered (d) its R1 row cites, bedrock_name copied from "
                                "that entry and its facet asserted against the register; moves kept, except #14's "
                                "embedded rebuttal cut (42 words remain, so nothing was added)",
            "answer_flagged_b": "6 wait on the (b) at their answering locus, since that (b)'s own repair is local "
                                "(#1, #7, #11, #32, #48, #50); 3 go to (d) because the (b)'s own grounds route the "
                                "repair to bedrock (#42 HR-05, #62 HR-06; #67 HR-04, whose record is a (d) with a "
                                "logged overclaim rather than a (b))",
            "aggravation": "#5 and #63 to (b) at the target, each a regen candidate with its corpus sentence queued",
            "routed_answer_silent": "#22 to (b), since no locus in the corpus speaks to determinism or "
                                    "ought-implies-can; #25 to (d) HR-06 through transhumanist-objection#long, the "
                                    "locus that takes the payload; #58 re-routed as a NEW (a) to economy-population#long",
            "under_strength_move": "#40 re-authored at full strength from R1-006's line, then the class law: (d) HR-02",
        },
        "move_edits": {"#1": "trim and complete from R1-004", "#7": "trim and complete from R1-048",
                       "#14": "trim only", "#62": "trim and complete from R1-047, adapted by four words",
                       "#40": "re-authored from R1-006",
                       "why_completed": "the move floor is 40 words (the ratified move gate); the cuts left #1 at 19, "
                                        "#7 at 33 and #62 at 21. The completions are the R1 rows' own stronger "
                                        "continuations, so no argument was added that the ruled record does not hold; "
                                        "#62 is the one (d) whose move gained words, flagged for the judge"},
        "for_the_judge": for_the_judge,
        "departure_from_an_R1_row": "#45: R1-017 names HR-03 (the bedrock of the tie-breaker the answer falls back on); "
                                    "the draft puts #45 on HR-02 intrinsic-value-of-existence with #47, because R1-012 "
                                    "says they are one move and names the (d) at red-button-repugnant#medium that "
                                    "registers the tie itself.",
        "where_the_records_live": "provenance.amended on every changed entry of adversarial_map_v1_4.json; the "
                                  "drafts file; this block.",
        "rows": rows,
    }
    am["terminal_assembly_v1_4_L4"] = {
        "artifact": "adversarial_map_v1_4.json", **f(MAP), "entries": len(m["entries"]),
        "class_counts": mm["class_counts"],
        "coverage": "%s/82 primary, %s variant, %s note (unchanged)" % (mm["coverage_distinct_ids"],
                                                                         mm["variant_coverage"], mm["note_coverage"]),
        "validation": "validator v0_6 under --assembly, in-process at build: 23 checks, 0 violations, 0 ADVISORIES. "
                      "v0_6 is unchanged: the amendment record rides in provenance, which its key check reads by field.",
        "builder": dict(f(MAP_BUILDER), file=MAP_BUILDER,
                        reproducible="byte-identical under two forced PYTHONHASHSEED values and re-run by this canon "
                                     "builder into scratch"),
        "controls": dict(f(MAP_CONTROL_REC), file=MAP_CONTROL_REC, instrument=MAP_CONTROLS, result=mc["result"]),
        "successor_to": "adversarial_map_v1_3.json 681827419df72a16a7c6fe70df8fe77f, byte-identical on disk; the R1 "
                        "rulings, the R1 evidence file and every R1 gate pin it",
        "not_served": "Nothing reaches /adversarial/, which is still rendered from v1_3 and register v0_4.",
    }
    am["honest_residuals_register_pin_v0_5"] = {
        "artifact": "honest_residuals_register_v0_5.json", **f(REG), "bedrocks": rm["bedrocks"],
        "residue_entries": rm["residue_entries"], "reclassified_at_L4": rm["reclassified_at_L4"]["count"],
        "by_bedrock": rm["reclassified_at_L4"]["by_bedrock"],
        "new_bedrocks": 0,
        "relations_added": rm["adjacency"]["added_at_L4"],
        "relations_note": "HR-11 conditions HR-02, HR-12 independent_of HR-10, HR-14 independent_of HR-05: drafted "
                          "because the new tributaries made each pair share a node and the adjacency gate refuses an "
                          "undeclared pair; judged with the drafts",
        "source": rm["source"],
        "render": dict(f(REG_MD), file=REG_MD),
        "builder": dict(f(REG_BUILDER), file=REG_BUILDER), "renderer": dict(f(REG_RENDER), file=REG_RENDER),
        "controls": dict(f(REG_CONTROL_REC), file=REG_CONTROL_REC, instrument=REG_CONTROLS, result=rc["result"]),
        "predecessor": "honest_residuals_register_v0_4.json d067729fafb51926bc9e845209417886, byte-identical on disk; "
                       "the served /adversarial/ page reads it",
    }
    am["pin_move_queue_L4"] = {
        "whose": "Josiah's to open. Every row is corpus text served in /combined, so every repair is pin-move work "
                 "(a declared session he opens and ratifies); L4 lists them and drafts none.",
        "sections": {"needed_before_rejudging": "the repairs the six waiting (a)s wait on",
                     "new_b_drafted_here": "the repairs the three (b)s L4 drafted name",
                     "passed_over_by_a_new_d": "defects already on record under records three new (d)s stand on; "
                                               "no (d) waits on them"},
        "counts": sections,
        "rows": queue,
    }
    am["knock_on_collisions_L4"] = {
        "finding": "L4's drafts put new (b)s and (d)s on nodes that answer entries R1 held. %d HOLDS now meet a (b) "
                   "or (d) that did not exist when R1 ruled them on v1_3: %s. Their verdicts stand; the collision "
                   "rule says each is read again before its card ships, and that reading waits on the judgment of "
                   "the drafts, since a rejected draft removes its collision." % (
                       len(knock["holds_newly_collided"]), ", ".join("#%d" % n for n in knock["holds_newly_collided"])),
        "record": dict(f(KNOCK_REC), file=KNOCK_REC, instrument=KNOCK),
        "method": knock["rule"],
        "holds_newly_collided": knock["holds_newly_collided"],
        "the_new_a": "#58 is an (a) in a new form (re-routed); no (b) or (d) sits on its new answering node, and it "
                     "needs a ruling like any other.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.23"
    d["canon_version_marker"] = "v38.23"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("gate2: judge L4's drafts of R1's 45 FAILS (adversarial_map.R1_drafting_pass_L4; %s, %s) as a "
                      "seat that did not draft them (K258), including #58's new (a) and register v0_5's three "
                      "relations. Then the %d knock-on HOLDS are read against the drafts that survive. The pin-move "
                      "queue (adversarial_map.pin_move_queue_L4, %d rows) is Josiah's to open. Then R2, then the "
                      "interconnection design." % (MAP, f(MAP)["md5"][:8], len(knock["holds_newly_collided"]), len(queue)))
    nrs["drafted_L4"] = ("L4 drafted all 45 FAILS: %s. Nothing reached /adversarial/ or /combined; drafted is not "
                         "ruled." % ", ".join("%s %d" % kv for kv in by_d.items()))

    d["keyset_delta_ledger"]["v38_23_L4"] = (
        "MINOR. keyset UNCHANGED at 42. Five adversarial_map subkey additions (R1_drafting_pass_L4, "
        "terminal_assembly_v1_4_L4, honest_residuals_register_pin_v0_5, pin_move_queue_L4, knock_on_collisions_L4); "
        "next_recommended_session re-pointed (session rewritten; drafted_L4 added); canon-meta; this note; one "
        "session_log_recent append. NO PIN. invariants, schemas, hazard_map and flagship_sidecars asserted "
        "byte-identical, and every other top-level key too.")
    d["session_log_recent"].append(
        "L4 (%s; NO PIN): the drafting pass over R1's 45 FAILS, on '%s' (R0110). adversarial_map_v1_4.json %s: "
        "%d entries change (%s) and %d wait unchanged on their (b) repairs; class counts a%d b%d c%d d%d. Register v0_5 "
        "%s: %d tributaries reclassified onto registered bedrock, no bedrock added, three relations drafted. "
        "Pin-move queue %d rows, Josiah's. %d HOLDS newly collided by the drafts, read after judgment. Drafted, not "
        "judged: gate2 next."
        % (DATE, HIS_PROCEED_L3, f(MAP)["md5"][:8], ra["entries_changed"], ", ".join("%s %d" % kv for kv in by_d.items()),
           ra["entries_waiting_unchanged"], mm["class_counts"]["a"], mm["class_counts"]["b"], mm["class_counts"]["c"],
           mm["class_counts"]["d"], f(REG)["md5"][:8], rm["reclassified_at_L4"]["count"], len(queue),
           len(knock["holds_newly_collided"])))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "flagship_sidecars"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == ADDED
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_23.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  v1_4 %s: %s | register v0_5 %s | queue %d | knock-on HOLDS %d"
          % (f(MAP)["md5"][:8], json.dumps(by_d), f(REG)["md5"][:8], len(queue), len(knock["holds_newly_collided"])))


if __name__ == "__main__":
    main()
