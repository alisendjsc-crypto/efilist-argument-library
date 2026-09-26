#!/usr/bin/env python3
"""project_canon_v38_25.json -- MINOR. L4b: Josiah's word on gate2's judgment, and the six fixes it owed.

ccclxiv FIRST: v38_24 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas, hazard_map and flagship_sidecars byte-identical; every
top-level key this build does not name byte-identical; inside adversarial_map nine subkeys are ADDED and
none moves (pin_move_queue_L4 and relation_vocabulary_K349 are superseded by new keys, not edited). The
map and register are rebuilt by their own builders into scratch and must equal the committed bytes; the
control record must be all-as-expected and name them; the knock-on is re-measured on v1_5 with L4's
committed instrument. His words are carried verbatim.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import collections, hashlib, importlib.util, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_24.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_25.json")
SRC_MD5 = "9b2fbb32fa914d1e7e92c715e19f1e13"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L4b"
DATE = "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map", "last_updated"}
ADDED = {"R1_drafts_judgment_ruled_L4b", "terminal_assembly_v1_5_L4b", "honest_residuals_register_pin_v0_6",
         "pin_move_queue_v1_5", "relation_direction_corrected_J052", "new_prose_reading_ruled_J049",
         "aggravation_repair_rule_J051", "knock_on_collisions_v1_5", "judgments_gate_referent_pinned_L4b"}

MAP = "adversarial_map_staging/adversarial_map_v1_5.json"
MAP_BUILDER = "adversarial_map_staging/build_assembly_v1_5.py"
REDRAFTS = "adversarial_map_staging/r1/R1_redrafts_v1_5.json"
REG = "adversarial_map_staging/honest_residuals_register_v0_6.json"
REG_MD = "adversarial_map_staging/honest_residuals_register_v0_6.md"
REG_BUILDER = "adversarial_map_staging/build_register_v0_6.py"
REG_RENDER = "adversarial_map_staging/render_register_v0_6.py"
CONTROLS = "adversarial_map_staging/controls_v1_5.py"
CONTROL_REC = "adversarial_map_staging/controls_v1_5_v0_1.json"
DRAFTS_L4 = "adversarial_map_staging/r1/R1_drafts_L4.json"
KNOCK = os.path.join(STG, "r1", "l4_knock_on.py")
JGATE = "adversarial_map_staging/r1/r1_judgments_gate.py"
JGATE_MD5_BEFORE = "a2a20f22d55b8474dd92bbb5b7e81182"
JCTL = "adversarial_map_staging/r1/r1_judgments_gate_control_v0_2.json"
CORPUS = "efilist_argument_library_v4_0_0.json"

HIS_WORD = "Go with the recommendations on all of the above and for Gate 2's seat. Continue with my word."
L4_LEANS = [
    "the pin-move queue: open it as one declared pin session after gate2 rules, not before",
    "#62's completed move: accept; the words are the ruled record's, not new argument",
    "#45 departs from R1-017: HR-02, with #47",
    "the drafted map keeps the name v1_4",
    "accept gate2's judgment as ruled",
]


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def run(tool, outdir):
    p = subprocess.run([sys.executable, os.path.join(REPO, tool), "--out", outdir],
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
    assert p.returncode == 0, "%s refused:\n%s" % (tool, p.stdout + p.stderr)


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
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_24.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_24 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- measured, not typed
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "adversarial_map_staging"))
        run(MAP_BUILDER, t)
        fresh = open(os.path.join(t, MAP), "rb").read()
        assert fresh == open(os.path.join(REPO, MAP), "rb").read(), "the committed v1_5 is not what its builder emits"
        run(REG_BUILDER, t)
        run(REG_RENDER, t)
        for rel in (REG, REG_MD):
            assert open(os.path.join(t, rel), "rb").read() == open(os.path.join(REPO, rel), "rb").read(), \
                "%s is not what its builder emits" % rel
    ctl = json.load(open(os.path.join(REPO, CONTROL_REC), encoding="utf-8"))
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["map"]["md5"] == f(MAP)["md5"] \
        and ctl["register"]["md5"] == f(REG)["md5"], "the control record does not name the committed artifacts"
    spec = importlib.util.spec_from_file_location("l4_knock_on", KNOCK)
    K = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(K)
    K.V1_4 = os.path.join(REPO, MAP)
    knock = K.measure()
    knock_v01 = json.load(open(os.path.join(STG, "r1", "l4_knock_on_v0_1.json"), encoding="utf-8"))

    p = subprocess.run([sys.executable, os.path.join(REPO, JGATE)], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    assert p.returncode == 0, "the judgments gate is RED:\n" + p.stdout + p.stderr
    jctl = json.load(open(os.path.join(REPO, JCTL), encoding="utf-8"))
    assert jctl["gate_md5"] == f(JGATE)["md5"] and all(c["as_expected"] for c in jctl["controls"]) \
        and jctl["controls"][0]["control"] == "C0", "the judgments gate's control record does not match the gate"

    m = json.loads(fresh.decode("utf-8"))
    mm = m["meta"]
    rr = mm["r1_redrafts"]
    rd = json.load(open(os.path.join(REPO, REDRAFTS), encoding="utf-8"))
    reg = json.load(open(os.path.join(REPO, REG), encoding="utf-8"))
    corpus = {o["id"]: o for o in json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8"))["objections"]}
    g = am["R1_drafts_judgment_gate2"]

    queue = [dict(r) for r in am["pin_move_queue_L4"]["rows"]]
    for pq in rd["pin_move_queue_additions"]:
        node, _, locus = pq["locus"].partition("#")
        row = {"id": pq["id"], "serves": ["#%d" % n for n in pq["serves"]], "section": pq["section"],
               "locus": pq["locus"], "sentence": sentence_with(locus_text(corpus[node], locus), pq["anchor"]),
               "answers": ("the (b) at %s, anchored on %r" % (pq["b_at"], pq["b_anchor"]))
               if pq["section"] == "new_b_drafted_here" else "a defect the map concedes and never filed as a (b)",
               "repair": pq["repair"]}
        if pq.get("note"):
            row["note"] = pq["note"]
        queue.append(row)
    sections = dict(collections.Counter(q["section"] for q in queue))

    # ---------------------------------------------------------------- adversarial_map: eight additions
    am["R1_drafts_judgment_ruled_L4b"] = {
        "his_words_verbatim": HIS_WORD,
        "said": "%s, in chat, to the L4 session" % DATE,
        "what_it_answered": ("gate2's six asks (adversarial_map.R1_drafts_judgment_gate2.for_his_word, relayed as R0129) "
                             "and the leans in L4's close (R0123), which the L4 session had put to him in chat"),
        "adopted_from_gate2": [{"ask": a["ask"], "lean": a["recommendation"]} for a in g["for_his_word"]],
        "adopted_from_L4": L4_LEANS,
        "so": ("The judgment stands as ruled: 43 drafts accepted, #14 amended, #58 rejected, the three relations "
               "accepted. The fixes it owed are built as adversarial_map_v1_5.json on this word ('Continue with my "
               "word'), and a seat that did not draft them judges them."),
        "outside_this_word": ("The design lane's merge (R0126) was not put to him in this chat, so this word does not "
                              "reach it. The P4c gate (argue's record) was: the L4 session counted 'all of the above' "
                              "as including its P4c lean and passed his words to the argue seat for the author's §8 "
                              "line, saying so; he may correct that forward."),
    }
    am["terminal_assembly_v1_5_L4b"] = {
        "artifact": "adversarial_map_v1_5.json", **f(MAP), "entries": len(m["entries"]),
        "class_counts": mm["class_counts"],
        "redrafted": rr["rows"],
        "redrafts": dict(f(REDRAFTS), file=REDRAFTS),
        "validation": "validator v0_6 under --assembly, in-process at build: 23 checks, 0 violations, 0 advisories",
        "builder": dict(f(MAP_BUILDER), file=MAP_BUILDER,
                        reproducible="byte-identical under two forced PYTHONHASHSEED values, and rebuilt into scratch "
                                     "by this canon builder"),
        "controls": dict(f(CONTROL_REC), file=CONTROL_REC, instrument=CONTROLS, result=ctl["result"]),
        "successor_to": "adversarial_map_v1_4.json cb61db5cdade98234d69d222b372f515, byte-identical on disk; the "
                        "judgment record pins it",
        "status": "DRAFTED, NOT JUDGED: the six redrafts go to a seat that did not draft them (K258).",
        "not_served": "Nothing reaches /adversarial/, which still renders from v1_3 and register v0_4.",
    }
    am["honest_residuals_register_pin_v0_6"] = {
        "artifact": "honest_residuals_register_v0_6.json", **f(REG), "bedrocks": len(reg["bedrocks"]),
        "residue_entries": reg["meta"]["residue_entries"],
        "changes_from_v0_5": reg["meta"]["changes_from_v0_5"],
        "method": "derived from v0_5 by the declared deltas, then cross-checked against v1_5 (every (d) a tributary "
                  "with the map's terminus_routing and novel flag) and re-run through both adjacency signals",
        "render": dict(f(REG_MD), file=REG_MD),
        "builder": dict(f(REG_BUILDER), file=REG_BUILDER), "renderer": dict(f(REG_RENDER), file=REG_RENDER),
        "predecessor": "honest_residuals_register_v0_5.json 0c29e3bd286ef9f5e6ddead7019f7ed3, byte-identical on disk",
    }
    am["pin_move_queue_v1_5"] = {
        "whose": "Josiah's to open, as one declared pin session after the judgment (his word, adopting L4's lean). "
                 "Every row is corpus text served in /combined.",
        "supersedes": "adversarial_map.pin_move_queue_L4 (13 rows), which stays as recorded. This is those 13 plus "
                      "gate2's two (J-053) and #58's redraft.",
        "counts": sections, "rows": queue,
        "sequence": "after gate2 judges v1_5 and the 11 knock-on HOLDS are read, because both can move what the "
                    "repairs must say",
    }
    am["relation_direction_corrected_J052"] = {
        "was": "HR-14 conditions HR-11 (relation_vocabulary_K349.first_instance; the register through v0_5)",
        "is": "HR-11 conditions HR-14",
        "why": "The ratified definition runs from the bedrock whose resolution changes the other's force, and the "
               "pair's own note says that is HR-11. Found by gate2 (J-052).",
        "his_words_verbatim": HIS_WORD,
        "substance": "unchanged; the note is carried verbatim with one forward sentence (register v0_6)",
        "canon": "relation_vocabulary_K349 is not edited; this block supersedes its first_instance name",
    }
    j49 = [r for r in json.load(open(os.path.join(STG, "r1", "R1_drafts_judgments.json"), encoding="utf-8"))["rows"]
           if r["id"] == "J-049"][0]
    am["new_prose_reading_ruled_J049"] = {
        "reading": j49["finding"], "adopted": HIS_WORD,
        "reaches": "#1, #7, #62 and #14 (v1_5's completion), and any later move completed the same way",
    }
    j51 = [r for r in json.load(open(os.path.join(STG, "r1", "R1_drafts_judgments.json"), encoding="utf-8"))["rows"]
           if r["id"] == "J-051"][0]
    am["aggravation_repair_rule_J051"] = {
        "reading": j51["finding"],
        "corrects_forward": "adversarial_map_design_v0_5.md section 11.1 ('at the NODE rather than at the locus'), "
                            "which stays byte-identical",
        "rule": "Repair the text that is false: the node's other loci when they are the defect, the locus when the "
                "node is accurate and the locus overclaims.",
    }
    am["judgments_gate_referent_pinned_L4b"] = {
        "what": ("r1_judgments_gate.py resolved register: quotes through r1_quote_check, which reads the register the "
                 "CURRENT canon pins. Register v0_6 made the changes the judgment itself asked for (J-046's note, "
                 "J-052's re-declaration), so two of the judgment's verbatim quotes (J-046, J-052) stopped resolving "
                 "and the gate went RED on true rows."),
        "fix": ("register: quotes now resolve against the register the record judged (its header's "
                "judged.register_v0_5, md5-pinned). Four lines; no check was removed or relaxed."),
        "gate": dict(f(JGATE), file=JGATE, md5_before=JGATE_MD5_BEFORE),
        "controls": dict(f(JCTL), file=JCTL, result="%d of %d as expected, the unmutated control first" % (
            sum(c["as_expected"] for c in jctl["controls"]), len(jctl["controls"])),
            v0_1="r1_judgments_gate_control_v0_1.json kept as committed; it names the gate before the fix"),
        "whose": ("The judge's instrument, changed by the drafting seat to keep every gate green, and disclosed: "
                  "gate2 confirms or corrects it when it judges v1_5."),
        "same_shape_elsewhere": ("r1_quote_check.py resolves R1_rulings.json's register quotes the same floating way. "
                                 "They quote glosses no register version has moved, so it is not failing; it will "
                                 "the first time a quoted gloss moves."),
    }
    am["knock_on_collisions_v1_5"] = {
        "measured": "with r1/l4_knock_on.py pointed at v1_5 (its own agreement check on v1_3 held first)",
        "a_entries_left": knock["a_entries_left_in_v1_4"],
        "holds_newly_collided": knock["holds_newly_collided"],
        "same_as_v1_4": knock["holds_newly_collided"] == knock_v01["holds_newly_collided"],
        "read_after": "gate2's judgment of v1_5",
    }

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.25"
    d["canon_version_marker"] = "v38.25"
    d["last_updated_by_session"] = SESSION
    d["last_updated"] = DATE
    nrs = d["next_recommended_session"]
    nrs["session"] = ("gate2: judge v1_5's six redrafts (adversarial_map.terminal_assembly_v1_5_L4b; %s, %s) as a seat "
                      "that did not draft them (K258). Then a non-drafting seat reads the %d knock-on HOLDS (%s) against "
                      "what survives. Then the pin-move session Josiah declares (adversarial_map.pin_move_queue_v1_5, "
                      "%d rows). Then R2, then the interconnection design."
                      % (MAP, f(MAP)["md5"][:8], len(knock["holds_newly_collided"]),
                         " ".join("#%d" % n for n in knock["holds_newly_collided"]), len(queue)))
    nrs["ruled_L4b"] = {"his_words_verbatim": HIS_WORD, "record": "adversarial_map.R1_drafts_judgment_ruled_L4b"}
    d["keyset_delta_ledger"]["v38_25_L4b"] = (
        "MINOR. keyset UNCHANGED at 42. Eight adversarial_map subkey additions (R1_drafts_judgment_ruled_L4b, "
        "terminal_assembly_v1_5_L4b, honest_residuals_register_pin_v0_6, pin_move_queue_v1_5, "
        "relation_direction_corrected_J052, new_prose_reading_ruled_J049, aggravation_repair_rule_J051, "
        "knock_on_collisions_v1_5); next_recommended_session re-pointed (session rewritten; ruled_L4b added); "
        "canon-meta; this note; one session_log_recent append. NO PIN.")
    d["session_log_recent"].append(
        "L4b (%s; NO PIN): his word on gate2's judgment, verbatim '%s'. The six fixes it owed are built as "
        "adversarial_map_v1_5.json %s: #14's move completed from R1-049, #58 redrafted as a (b) at "
        "social-contract#long, #25/#59/#62's terminus_routing names the path, #16's grounds name "
        "why-not-suicide#long. Class counts a%d b%d c%d d%d. Register v0_6 %s re-declares the K349 pair as HR-11 "
        "conditions HR-14 (J-052). Pin-move queue %d rows. Drafted, not judged: gate2 next."
        % (DATE, HIS_WORD, f(MAP)["md5"][:8], mm["class_counts"]["a"], mm["class_counts"]["b"],
           mm["class_counts"]["c"], mm["class_counts"]["d"], f(REG)["md5"][:8], len(queue)))

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
    print("project_canon_v38_25.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  v1_5 %s %s | register v0_6 %s | queue %d %s | knock-on HOLDS %d (same as v1_4: %s)"
          % (f(MAP)["md5"][:8], json.dumps(mm["class_counts"], sort_keys=True), f(REG)["md5"][:8], len(queue),
             json.dumps(sections), len(knock["holds_newly_collided"]),
             knock["holds_newly_collided"] == knock_v01["holds_newly_collided"]))


if __name__ == "__main__":
    main()
