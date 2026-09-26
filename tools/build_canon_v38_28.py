#!/usr/bin/env python3
"""project_canon_v38_28.json -- MINOR. L4c: #46 drafted as a (d) under R1-070; the reader's-aid backlog; the pin
session declared.

ccclxiv FIRST: v38_27 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; every top-level key this build does not name byte-identical; inside adversarial_map six
subkeys are ADDED and none moves (pin_move_queue_v1_5 is superseded by pin_move_queue_v1_6, not edited). The map
and register are rebuilt by their own builders into scratch and must equal the committed bytes; the control record
must be all-as-expected and name them; the knock-on is re-measured by its committed instrument, must equal its
record, and its self-test must pass. His words are carried verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, hashlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_27.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_28.json")
SRC_MD5 = "9e97e845840307b5482cabbe02674d20"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L4c"
DATE = "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map", "last_updated"}
ADDED = {"terminal_assembly_v1_6_L4c", "honest_residuals_register_pin_v0_7", "pin_move_queue_v1_6",
         "knock_on_collisions_v1_6", "reader_aid_backlog_L4c", "instruments_append_proofed_L4c"}

MAP = "adversarial_map_staging/adversarial_map_v1_6.json"
MAP_BUILDER = "adversarial_map_staging/build_assembly_v1_6.py"
REDRAFTS = "adversarial_map_staging/r1/R1_redrafts_v1_6.json"
REG = "adversarial_map_staging/honest_residuals_register_v0_7.json"
REG_MD = "adversarial_map_staging/honest_residuals_register_v0_7.md"
REG_BUILDER = "adversarial_map_staging/build_register_v0_7.py"
REG_RENDER = "adversarial_map_staging/render_register_v0_7.py"
CONTROLS = "adversarial_map_staging/controls_v1_6.py"
CONTROL_REC = "adversarial_map_staging/controls_v1_6_v0_1.json"
KNOCK = "adversarial_map_staging/r1/l4c_knock_on.py"
KNOCK_REC = "adversarial_map_staging/r1/l4c_knock_on_v0_1.json"
PINNED = "adversarial_map_staging/r1/pinned.py"
PROOFED = ["adversarial_map_staging/controls_assembly_v1_4.py", "adversarial_map_staging/controls_v1_5.py",
           "adversarial_map_staging/r1/l4_knock_on.py"]
CORPUS = "efilist_argument_library_v4_0_0.json"

WORD_RERULE = "Proceed with all of your recommendations."
WORD_TODO = ("Proceed with all of your recommendations. Note the highlighted text in the screenshots. Note for later "
             "so it doesn't get lost. Prioritize based on your recommendations.")
WORD_AGENT = ("Go with your recommendations on all of the above.\n\nOn the \"for your agent\" handout--no prompt "
              "injection--I just want it to be easily findable by any LLM scanning the site\na user would probably be "
              "likely to hand the site to an LLM in an attempt to summarize what it is, so the handout's purpose is to "
              "be discoverable and make that easier")
WORD_OPEN = "open it when the window is clear"
WORD_PIN_GATE2 = "Go with your recommendation on the pin session."
GATE2_PIN_REC = ("declare it once L4 has added the why-not-suicide sentence to the queue, so one session makes all 17 "
                 "corpus fixes instead of two sessions.")
KICKOFF = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2", "from": "gate2", "to": "l"}
TODO_LINES = [
    "Adversarial part of library has no unique favicon icon (fix)",
    "Adversarial library feels very technical and has no [plain] explanation toggle mode like other wings | "
    "furthermore, some of the terms like \"terminate here\" or \"continuations\" or \"floors named\" or \"floors in the "
    "register\" feel obtuse upon first reading; though, I like technical language--it deserves a brief explanation "
    "(brainstorm how to do so discretely without sacrificing robustness)",
    "Adversarial corpus has no unique \"tutorial\" that activates when entering its wing",
    "Adversarial corpus has no \"methedology\" panel -- though is it warranted or not? (open question)",
    "\"For your agent\" section library--optimal for LLM's assimilation | give a specialized handout for each model "
    "you think deserves one that helps them understand what they are seeing and draws the attention of any model "
    "reading the site | discrete for normal viewers so it doesn't clutter the view",
]


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def run(args, outdir=None):
    cmd = [sys.executable, os.path.join(REPO, args[0])] + args[1:] + (["--out", outdir] if outdir else [])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if outdir:
        env["K348_MAP_DIR"] = os.path.join(outdir, "adversarial_map_staging")
    p = subprocess.run(cmd, env=env, capture_output=True, text=True)
    assert p.returncode == 0, "%s refused:\n%s" % (" ".join(args), p.stdout + p.stderr)
    return p.stdout


def sentence_with(text, anchor):
    for s in re.split(r"(?<=[.!?])\s+", text):
        if anchor in s:
            return s
    raise AssertionError("anchor %r not inside one sentence" % anchor)


def locus_text(o, locus):
    if locus in ("short", "medium", "long"):
        return o["responses"].get(locus)
    if locus.startswith("archetypeVariants."):
        return o["responses"]["archetypeVariants"][locus.split(".", 1)[1]]
    return o[locus]


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_27.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_27 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "adversarial_map_staging"))
        run([MAP_BUILDER], t)
        fresh = open(os.path.join(t, MAP), "rb").read()
        assert fresh == open(os.path.join(REPO, MAP), "rb").read(), "the committed v1_6 is not what its builder emits"
        run([REG_BUILDER], t)
        run([REG_RENDER], t)
        for rel in (REG, REG_MD):
            assert open(os.path.join(t, rel), "rb").read() == open(os.path.join(REPO, rel), "rb").read(), \
                "%s is not what its builder emits" % rel
    ctl = json.load(open(os.path.join(REPO, CONTROL_REC), encoding="utf-8"))
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["map"]["md5"] == f(MAP)["md5"] \
        and ctl["register"]["md5"] == f(REG)["md5"], "the control record does not name the committed artifacts"
    run([KNOCK, "--check"])
    self_test = run([KNOCK, "--self-test"]).strip()
    knock = json.load(open(os.path.join(REPO, KNOCK_REC), encoding="utf-8"))
    assert knock["maps"]["after"]["md5"] == f(MAP)["md5"], "the knock-on record does not name the committed v1_6"

    m = json.loads(fresh.decode("utf-8"))
    mm = m["meta"]
    rr = mm["r1_rerulings"]
    rd = json.load(open(os.path.join(REPO, REDRAFTS), encoding="utf-8"))
    x46 = rd["redrafts"][0]
    reg = json.load(open(os.path.join(REPO, REG), encoding="utf-8"))
    corpus = {o["id"]: o for o in json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8"))["objections"]}
    amended = [e for e in m["entries"] if e["provenance"].get("amended", {}).get("at") == "L4c"]
    assert len(amended) == 1 and amended[0]["provenance"]["amended"]["r1_row"] == "R1-070"

    queue = [dict(r) for r in am["pin_move_queue_v1_5"]["rows"]]
    for pq in rd["pin_move_queue_additions"]:
        node, _, locus = pq["locus"].partition("#")
        queue.append({"id": pq["id"], "serves": ["#%d" % n for n in pq["serves"]], "section": pq["section"],
                      "locus": pq["locus"], "sentence": sentence_with(locus_text(corpus[node], locus), pq["anchor"]),
                      "answers": "a misfit %s conceded and the map never filed as a (b); gate2's finding %s"
                                 % (pq["conceded_by"], pq["finding"]),
                      "repair": pq["repair"], "note": pq["note"]})
    sections = dict(collections.Counter(q["section"] for q in queue))
    assert len(queue) == 17 and len({q["id"] for q in queue}) == 17

    # ---------------------------------------------------------------- adversarial_map: six additions
    am["terminal_assembly_v1_6_L4c"] = {
        "artifact": "adversarial_map_v1_6.json", **f(MAP), "entries": len(m["entries"]),
        "class_counts": mm["class_counts"],
        "reclassified": rr["rows"],
        "his_words_verbatim": WORD_RERULE,
        "under": "adversarial_map.R1_070_rerule_gate2 (R1-070 supersedes R1-011: #46 FAILS) and R1_standard_ruling_L2",
        "disposition": {
            "class": "d", "bedrock": "%s, %s facet" % (x46["hr"], x46["facet"]),
            "bedrock_from": "%s, anchored on %r" % (x46["bedrock_from"], x46["bedrock_from_anchor"]),
            "lean_it_follows": "gate2's (V-017 of R1_v1_5_judgments.json, carried in R1-070's note_not_ruled)",
            "why_not_HR_02": x46["why_not_HR_02"],
            "class_law": x46["class_law"],
        },
        "shape": ("%s, read from canon's newest R1_progress_L* block by r1_collision_list.shapes_from_canon, as gate2 "
                  "advised at R1-070" % amended[0]["provenance"]["amended"]["shape"]),
        "redrafts": dict(f(REDRAFTS), file=REDRAFTS),
        "validation": "validator v0_6 under --assembly, in-process at build: 23 checks, 0 violations, 0 advisories",
        "builder": dict(f(MAP_BUILDER), file=MAP_BUILDER,
                        reproducible="byte-identical under two forced PYTHONHASHSEED values, and rebuilt into scratch "
                                     "by this canon builder"),
        "controls": dict(f(CONTROL_REC), file=CONTROL_REC, instrument=CONTROLS, result=ctl["result"]),
        "successor_to": "adversarial_map_v1_5.json 0df413ed655a5373468c218832854bbe, byte-identical on disk; gate2's "
                        "v1_5 judgment pins it",
        "status": "DRAFTED, NOT JUDGED: gate2 judges it (K258).",
        "not_served": "Nothing reaches /adversarial/, which still renders from v1_3 and register v0_4.",
    }
    am["honest_residuals_register_pin_v0_7"] = {
        "artifact": "honest_residuals_register_v0_7.json", **f(REG), "bedrocks": len(reg["bedrocks"]),
        "residue_entries": reg["meta"]["residue_entries"],
        "changes_from_v0_6": reg["meta"]["changes_from_v0_6"],
        "method": "derived from v0_6 by one declared delta, then cross-checked against v1_6 (every (d) a tributary "
                  "with the map's terminus_routing and novel flag; HR-14 the only bedrock that moves) and re-run "
                  "through both adjacency signals; no relation added",
        "render": dict(f(REG_MD), file=REG_MD),
        "builder": dict(f(REG_BUILDER), file=REG_BUILDER), "renderer": dict(f(REG_RENDER), file=REG_RENDER),
        "predecessor": "honest_residuals_register_v0_6.json 0689f46f18a4dbe8d40c9982a2ad06f9, byte-identical on disk",
    }
    am["knock_on_collisions_v1_6"] = {
        "measured": "r1/l4c_knock_on.py: v1_6 against v1_5 with l4_knock_on.collisions imported, after "
                    "l4_knock_on.measure() reproduced its committed record",
        "record": dict(f(KNOCK_REC), file=KNOCK_REC), "instrument": dict(f(KNOCK), file=KNOCK),
        "a_entries_left": knock["a_entries_left_in_v1_6"],
        "holds_newly_collided": knock["holds_newly_collided"],
        "rows": len(knock["rows"]),
        "why_none": "No (a) left in v1_6 sits on red-button-repugnant or routes to it: every entry on that node is "
                    "now a (d).",
        "self_test": self_test,
    }
    am["pin_move_queue_v1_6"] = {
        "whose": "Josiah's. Every row is corpus text served in /combined.",
        "declared": {
            "words": [
                {"his_words_verbatim": WORD_OPEN, "said": "%s, in chat, to the L4 session" % DATE,
                 "answered": ("the L4 session's recommendation to open the repair session as soon as #46 is judged, "
                              "since nothing else blocks it")},
                {"his_words_verbatim": WORD_PIN_GATE2, "said": "%s, to gate2, as its kickoff R0150 records" % DATE,
                 "answered": "gate2's recommendation, as R0150 quotes it: '%s'" % GATE2_PIN_REC},
            ],
            "so": ("One session makes all 17 fixes, opened once gate2's judgment of v1_6 lands, when efilist canon has "
                   "one writer again. gate2 launches it zero-click; the L4 session does not launch a second."),
            "kickoff": KICKOFF,
        },
        "supersedes": "adversarial_map.pin_move_queue_v1_5 (16 rows), which stays as recorded. This is those 16 plus "
                      "PQ-17, queued as gate2's lean (R0142 item 3, finding V-023).",
        "counts": sections, "rows": queue,
        "flow": [
            "the pin session drafts the replacement text for each row",
            "a seat that did not draft it judges it (K258)",
            "Josiah ratifies the text",
            "the pin moves: combined.html, the corpus and the jsx together under tools/xsurface_v4_1_0.py; README, "
            "CHANGELOG and the front-door badge with it; the sidecars regenerated if a mapped literal moves; "
            "wuld-ink's pin surfaces and search index; the game's re-vendor notice",
        ],
    }
    am["reader_aid_backlog_L4c"] = {
        "his_words_verbatim": [WORD_TODO, WORD_AGENT],
        "said": ("%s, in chat, to the L4 session; the first with two screenshots of his notes-app list "
                 "'TO DO (library)'" % DATE),
        "his_lines": {"transcribed": "from his screenshots by the L4 session, the highlighted lines, typos kept",
                      "lines": TODO_LINES,
                      "not_recorded_here": "the list's other lines, which belong to other lanes"},
        "priority_adopted": [
            {"rank": 1, "item": "a favicon for /adversarial/",
             "how": "the design lane draws the mark under its no-shared-silhouette gate in icons/gen_icons.py; the "
                    "library seat wires it into the renderer, because the page is rendered"},
            {"rank": 2, "item": "a plain layer for /adversarial/",
             "how": "a [plain] toggle like the wings', and first-use glosses of the page's terms (terminus, 'terminate "
                    "here', continuation, floor, register, bedrock) that open on tap or hover; the pinned label strings "
                    "(terminus_label_pin_K353) stay, and the glosses explain them"},
            {"rank": 3, "item": "a methodology panel",
             "how": "warranted, collapsed by default: how entries are made (the class law), how they are judged (R1; "
                    "the drafter is never the judge, K258), and what a terminus card claims and does not claim"},
            {"rank": 4, "item": "'For your agent'",
             "how": "one /llms.txt at the library's site root, linked from each page head by <link rel=\"alternate\" "
                    "type=\"text/markdown\"> and from one quiet footer line: what the site is, its libraries, how the "
                    "adversarial page works, the license (CC BY 4.0) and how to cite it; one text for every model"},
            {"rank": 5, "item": "a tutorial on entering the wing",
             "how": "after 2 and 3, reusing their text through the house layer's first-visit tour"},
        ],
        "for_your_agent_ruled": {
            "his_words_verbatim": WORD_AGENT,
            "so": ("Built to be discoverable and to make a summary accurate. No per-model handouts and no copy written "
                   "to steer a model: the L4 session's reason, which his words adopt, is that such copy works like "
                   "prompt injection and would spend the trust the adversarial page is built to earn."),
        },
        "sessions": ("Items 1-3 and 5 change the rendered /adversarial/ page: one 'adversarial wing v2' session, which "
                     "also ships the ruled (d) cards once render_wing_v0_1.py is keyed on the anchor (gate2's J-055). "
                     "/adversarial/ deploys on push, so a preview and his word come first. Item 4 is its own small "
                     "session."),
        "order": ["gate2 judges v1_6 (#46)", "the pin session (pin_move_queue_v1_6)", "adversarial wing v2",
                  "'For your agent' (/llms.txt)", "R2", "the interconnection design"],
    }
    am["instruments_append_proofed_L4c"] = {
        "commit": "46b6f65",
        "what": ("L4's instruments pinned R1_rulings.json at 3f1dfad5 and read the working file, so an appended row "
                 "(R1-070) would turn them RED on true bytes. They now read the pinned bytes, which r1/pinned.py "
                 "recovers from git history when the file has grown."),
        "helper": dict(f(PINNED), file=PINNED),
        "instruments": [dict(f(p), file=p) for p in PROOFED],
        "also_uses_it": [CONTROLS, KNOCK],
        "judge_side": ("gate2 wrote its own inline lookup in its two judgment gates rather than import pinned.py, so a "
                       "drafting seat's helper cannot move the judge's gates (adversarial_map.R1_070_rerule_gate2)."),
        "law": "An instrument that pins an append-only record reads it at the pinned bytes, never at the working file.",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.28"
    d["canon_version_marker"] = "v38.28"
    d["last_updated_by_session"] = SESSION
    d["last_updated"] = DATE
    nrs = d["next_recommended_session"]
    nrs["session"] = ("gate2: judge v1_6 (adversarial_map.terminal_assembly_v1_6_L4c; %s, %s), #46's (d) at HR-14, as "
                      "a seat that did not draft it (K258); the knock-on found %d HOLDS newly collided. Then the pin "
                      "session Josiah declared (adversarial_map.pin_move_queue_v1_6, %d rows; kickoff R0150), which gate2 "
                      "launches once that judgment lands. Then adversarial wing v2 and the /llms.txt session "
                      "(adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design."
                      % (MAP, f(MAP)["md5"][:8], len(knock["holds_newly_collided"]), len(queue)))
    nrs["ruled_L4c"] = {"his_words_verbatim": [WORD_RERULE, WORD_AGENT, WORD_OPEN],
                        "records": ["adversarial_map.R1_070_rerule_gate2", "adversarial_map.terminal_assembly_v1_6_L4c",
                                    "adversarial_map.reader_aid_backlog_L4c", "adversarial_map.pin_move_queue_v1_6"]}
    d["keyset_delta_ledger"]["v38_28_L4c"] = (
        "MINOR. keyset UNCHANGED at 42. Six adversarial_map subkey additions (terminal_assembly_v1_6_L4c, "
        "honest_residuals_register_pin_v0_7, knock_on_collisions_v1_6, pin_move_queue_v1_6, reader_aid_backlog_L4c, "
        "instruments_append_proofed_L4c); next_recommended_session re-pointed (session rewritten; ruled_L4c added); "
        "canon-meta; this note; one session_log_recent append. NO PIN.")
    d["session_log_recent"].append(
        "L4c (%s; NO PIN): #46, re-ruled FAILS at R1-070 on '%s', drafted as a (d) at %s %s in "
        "adversarial_map_v1_6.json %s (a%d b%d c%d d%d); register v0_7 %s adds its tributary to HR-14. Knock-on: %d "
        "HOLDS newly collided. Pin-move queue %d rows (PQ-17 queued as gate2's lean), declared by him to the L4 session ('%s') and to gate2 "
        "('%s'). His TO "
        "DO lines on /adversarial/ and 'For your agent' recorded with the adopted priority. Drafted, not judged: "
        "gate2 next."
        % (DATE, WORD_RERULE, x46["hr"], x46["facet"], f(MAP)["md5"][:8], mm["class_counts"]["a"],
           mm["class_counts"]["b"], mm["class_counts"]["c"], mm["class_counts"]["d"], f(REG)["md5"][:8],
           len(knock["holds_newly_collided"]), len(queue), WORD_OPEN, WORD_PIN_GATE2))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == ADDED
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"
    open(OUT, "wb").write(out)
    print("project_canon_v38_28.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  v1_6 %s %s | register v0_7 %s | queue %d %s | knock-on HOLDS %d | %s"
          % (f(MAP)["md5"][:8], json.dumps(mm["class_counts"], sort_keys=True), f(REG)["md5"][:8], len(queue),
             json.dumps(sections), len(knock["holds_newly_collided"]), self_test))


if __name__ == "__main__":
    main()
