#!/usr/bin/env python3
"""project_canon_v38_55.json -- MINOR canon bump, no release. V8 (gate2, 2026-10-04): V7's relief variant pilot
and V5's RD-03 judged; judged, not ruled; R0320 (with R0317 folded in).

Adds to adversarial_map:
  relief_variants_judgment_gate2       the seven verdicts (six ACCEPT, one AMEND and its owed lines), the builder's
                                       checks (CORRECT) and controls, the source check, F1-F3, the five pulls, the
                                       Berridge check, the two quotations read at their turns, the safety read, the
                                       new finding F4, and the asks with leans; every value read from gate2's record
                                       at its md5
  shapes_redrafts_v0_2_judgment_gate2  RD-03 ACCEPT as (d) at HR-02 via joy-outweighs-harms#long, its five pulls and
                                       sources, read from gate2's third-round record at its md5
  record_notes_V8                      statements measured and corrected forward
and re-points next_recommended_session (his word on the judgment -> seat l's one owed line -> gate2 on it -> the next
declared pin).

Measured at run time, never typed: every md5, byte count and check result. ccclxiv FIRST: v38_54 round-trips at this
file's serialization, read at its md5 from the working tree or git history. Every top-level key outside TOUCHED is
asserted byte-identical; inside adversarial_map only the new keys are added. The served surfaces, the drafts judged and
their checkers, and gate2's earlier records are asserted at their md5s. The gates it records run in their own process
groups with TMPDIR in scratch.

Order (r1_collision_list_l7_v0_1.json names the one canon file present): git mv v38_54 to v38_55, regenerate that record
with its own --write, then run this builder, which reads v38_54 from git history and overwrites v38_55.

  python3 tools/build_canon_v38_55.py [--out DIR]
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_54.json", "e0f3e2f695a43f18d0c90d6ce3e08748"
OUT = os.path.join(OUT_DIR, "project_canon_v38_55.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "V8"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["relief_variants_judgment_gate2", "shapes_redrafts_v0_2_judgment_gate2", "record_notes_V8"]
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
KEPT = {"response_variants/relief_variants_pilot_v0_1.json": "1d5e8f1c65a387da495dba91edbee9e8",
        "response_variants/relief_variants_record_v0_1.json": "1d8556443af14f95bff9e906f2a67037",
        "response_variants/build_relief_variants.py": "c5f02c47f1daf965f2dbd29bfa9aec9a",
        "response_variants/response_variants_schema_v0_1.json": "169c15b30f3fcc578689daa257d5b41f",
        "response_variants/response_variant_validator_v0_1.py": "30cb7f3bc4f9e81b0ff5c85ecfaacdf3",
        "response_variants/response_variant_validator_control_v0_1.json": "44a77cc75a062fb6e4bac7b47aaec421",
        "response_variants/README.md": "a26ee64f0c422bc7de3a9eb2bde1db0c",
        "design/variations/measure_response_variants_v0_1.json": "cbae330fe2106d79d572de8e20ac8459",
        "argument_shapes/shapes_redrafts_v0_2.json": "159c546ef224f87037578f7dee1464e2",
        "argument_shapes/shapes_redrafts_record_v0_2.json": "c7bdef1e18f4a2763118a305be25ef4c",
        "argument_shapes/build_shapes_redrafts_v0_2.py": "cf505158a26b35de977d11c3d14a732b",
        "argument_shapes/shapes_redrafts_v0_1.json": "fc28cd12265e2712a9d610bbb2c1b69f",
        "argument_shapes/shapes_pilot_v0_1.json": "1f9c5da6166b538a90efa6dc7598124e",
        "argument_shapes/shapes_pilot_judgments.json": "73503bccdd3ddf8b3a82f280181251d4",
        "argument_shapes/shapes_redrafts_judgments.json": "6f4974966c23920234f495cb20813d4c",
        "argument_shapes/shapes_redrafts_judgments_gate.py": "950c715c4b7ba35b6db8715600df8832",
        "argument_shapes/shapes_redrafts_judgments_gate_control_v0_1.json": "a66790d45a73a1698584d230877ac0ed"}
JUDGED = {
    "variants": {"record": "response_variants/relief_variants_judgments.json",
                 "gate": "response_variants/relief_variants_judgments_gate.py",
                 "control": "response_variants/relief_variants_judgments_gate_control_v0_1.json"},
    "rd03": {"record": "argument_shapes/shapes_redrafts_v0_2_judgments.json",
             "gate": "argument_shapes/shapes_redrafts_v0_2_judgments_gate.py",
             "control": "argument_shapes/shapes_redrafts_v0_2_judgments_gate_control_v0_1.json"}}
KICKOFF = {"relay": "R0320", "md5": "e0ed9ab632807f71a9194be9d683e9aa"}
FOLDED = {"relay": "R0317", "md5": "6c61dd850d1fdcbda7db2d64664ec047"}
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
CL_REL = "adversarial_map_staging/r1/r1_collision_list_l7_v0_1.json"
NEW_FILES = [p for j in JUDGED.values() for p in j.values()] + ["tools/build_canon_v38_55.py", "README.md",
                                                                  "CHANGELOG.md"]
ASKS = [
    {"ask": ("Adopt gate2's judgment of the relief variant: six ACCEPT (life-gift, joy-outweighs-harms, "
             "love-beauty-art, masochist-counterexample, hedonic-contrast, neuroscience-positive-states) and one AMEND "
             "(bradley-no-subject: the frame over account [2])."),
     "lean": ("adopt; seat l meets the one owed line in a new file, gate2 judges that line, and the seven then wait "
              "for the render in a declared pin (RV-4)")},
    {"ask": "Adopt RD-03, the golden rule's third pass: ACCEPT as (d) at HR-02 via joy-outweighs-harms#long.",
     "lean": "adopt; the golden rule joins the (d)s at the successor map's next validator bump"},
    {"ask": ("F4: joy-outweighs-harms#long calls the relief thesis 'the false claim', beside a variant that ends on "
             "canon's open residual. Queue it with F1 for the next declared pin's served-text pass?"),
     "lean": ("queue it; the pin session drafts any change, gate2 judges it, and his word decides whether the long's "
              "word stands as the library's verdict")},
    {"ask": ("Account [0]: in 'though, it does not completely defeat them' (vault_V2 line 805), 'them' has no single "
             "antecedent; the variants carry the sentence whole and leave it open. Name the referent only if one "
             "reading is wrong for you."),
     "lean": "no change; the sentence plays the same role in the variants as at its turn"}]

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
    return out.strip().splitlines()[-1]


def index_md5s():
    got = {}
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) > 8 and f[1] == "SENT" and f[2] in (KICKOFF["relay"], FOLDED["relay"]):
                got[f[2]] = f[8]
        assert got.get(KICKOFF["relay"]) == KICKOFF["md5"] and got.get(FOLDED["relay"]) == FOLDED["md5"], got
        return True
    return False


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_54 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in list(SERVED.items()) + list(KEPT.items()):
        assert md5f(rel) == m, "%s moved" % rel
    for blk in ("response_variants_design_V5", "shapes_redrafts_V5", "response_variants_build_V6",
                "relief_variants_pilot_V7"):
        for k, p in am[blk]["files"].items():
            assert md5f(p["file"]) == p["md5"], "%s's %s moved" % (blk, k)
    indexed = index_md5s()

    raws = {k: open(os.path.join(REPO, v["record"]), "rb").read() for k, v in JUDGED.items()}
    vj = json.loads(raws["variants"].decode("utf-8"))
    tj = json.loads(raws["rd03"].decode("utf-8"))
    assert vj["kickoff"] == KICKOFF and tj["kickoff"] == KICKOFF and tj["relay"] == FOLDED
    assert vj["judged"]["canon"] == {"file": SRC_REL, "md5": SRC_MD5} == tj["judged"]["canon"]

    scratch = tempfile.mkdtemp(prefix="canon_v38_55_")
    try:
        runs = {}
        for k, v in JUDGED.items():
            for args in ([v["gate"]], [v["gate"], "--self-test"]):
                tail = run(args, scratch)
                assert ("GREEN" in tail) if len(args) == 1 else ("control record matches" in tail), tail
                runs[" ".join(args)] = tail
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    def rows(rec, kind):
        return [r for r in rec["rows"] if r.get("kind") == kind]
    var = rows(vj, "variant")
    one = lambda rec, kind: rows(rec, kind)[0]  # noqa: E731
    am["relief_variants_judgment_gate2"] = {
        "state": vj["state"],
        "kickoff": dict(KICKOFF, read_at_the_index=indexed),
        "files": {k: pin(v) for k, v in JUDGED["variants"].items()},
        "judged": vj["judged"],
        "verdicts": {r["variant_id"]: r["verdict"] for r in var},
        "count": {v: sum(1 for r in var if r["verdict"] == v) for v in ("ACCEPT", "AMEND", "REJECT")},
        "owed": {r["variant_id"]: r["owed"] for r in var if r.get("owed")},
        "amend_reason": {r["variant_id"]: r["reads"]["his_words"] for r in var if r["verdict"] == "AMEND"},
        "builder_checks": {"verdict": one(vj, "checks")["verdict"], "finding": one(vj, "checks")["finding"],
                           "carries": one(vj, "checks")["carries"]},
        "controls": {"verdict": one(vj, "controls")["verdict"], "finding": one(vj, "controls")["finding"]},
        "source_check": {"verdict": one(vj, "source")["verdict"], "finding": one(vj, "source")["finding"]},
        "findings": {r["finding_id"]: r["verdict"] for r in rows(vj, "finding")},
        "pulls": [r["verdict"] for r in sorted(rows(vj, "pull"), key=lambda r: r["pull"])],
        "berridge": {"verdict": one(vj, "berridge")["verdict"], "reads": one(vj, "berridge")["reads"]},
        "quotations_read_at_their_turns": {"account_%d" % r["account"]: {"verdict": r["verdict"], "reads": r["reads"]}
                                           for r in rows(vj, "note")},
        "safety": {"verdict": one(vj, "safety")["verdict"], "reads": one(vj, "safety")["reads"]},
        "found": {r["found_id"]: r["found"] for r in rows(vj, "found")},
        "asks_for_his_word": ASKS,
        "run_at_this_build": {k: v for k, v in runs.items() if k.startswith("response_variants/")},
        "copied_from": "%s at %s" % (JUDGED["variants"]["record"], md5b(raws["variants"]))}

    shp = one(tj, "shape")
    am["shapes_redrafts_v0_2_judgment_gate2"] = {
        "state": tj["state"],
        "kickoff": dict(KICKOFF, read_at_the_index=indexed),
        "relay_folded": FOLDED,
        "files": {k: pin(v) for k, v in JUDGED["rd03"].items()},
        "judged": tj["judged"],
        "verdict": {"redraft": shp["redraft"], "shape_id": shp["shape_id"], "answers": shp["answers"],
                    "verdict": shp["verdict"], "class_judged": shp["class_judged"], "route": shp["route"],
                    "reason": shp["reason"]},
        "pulls": [{"pull": r["pull"], "verdict": r["verdict"], "reads": r["reads"]}
                  for r in sorted(rows(tj, "pull"), key=lambda r: r["pull"])],
        "sources": {"verdict": one(tj, "sources")["verdict"], "finding": one(tj, "sources")["finding"]},
        "safety": {"verdict": one(tj, "safety")["verdict"], "finding": one(tj, "safety")["finding"]},
        "run_at_this_build": {k: v for k, v in runs.items() if k.startswith("argument_shapes/")},
        "copied_from": "%s at %s" % (JUDGED["rd03"]["record"], md5b(raws["rd03"]))}

    cl_was = am["record_notes_V7"][-1]["record"]["md5"]
    cl_old_lines = pinned.bytes_at(REPO, CL_REL, cl_was).decode("utf-8").splitlines()
    cl_new_lines = open(os.path.join(REPO, CL_REL), encoding="utf-8").read().splitlines()
    cl_diff = [(x, y) for x, y in zip(cl_old_lines, cl_new_lines) if x != y]
    assert len(cl_old_lines) == len(cl_new_lines) and cl_diff == [('  "canon": "project_canon_v38_54.json"',
                                                                   '  "canon": "project_canon_v38_55.json"')], cl_diff
    am["record_notes_V8"] = [
        {"statement": ("V7 (efilist primer and R0320): the builder's ten checks, each proven to fire by a mutation "
                       "(C1-C5, C0 first)"),
         "measured": one(vj, "checks")["finding"]},
        {"statement": "R0320: battery at V7's close 70/70 GREEN + 3 RED by design",
         "measured": ("reproduced at V8's open with gate2's own runner (gate2 V3b's list plus the post-V2..post-V7 "
                      "additions read from the primer's verify_before chain): 70 of 70 GREEN, 3 of 3 RED by design")},
        {"statement": "relief_view_for_the_variant: his ten accounts, verbatim, each with its turn md5 (F3)",
         "measured": one(vj, "source")["finding"]},
        {"statement": "record_notes_V7 pins r1_collision_list_l7_v0_1.json at %s" % cl_was,
         "measured": ("the record names the canon file present, so this bump moved it by exactly one line, its "
                      "'canon' field (v38_54 to v38_55); regenerated by the tool's own --write"),
         "record": dict(pin(CL_REL), was=cl_was)}]

    d["canon_version"] = "38.55"
    d["canon_version_marker"] = "v38.55"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    kept_tail = nrs["session"][nrs["session"].index("V4 takes the one (a)"):]
    assert kept_tail.startswith("V4 takes the one (a) after the successor map's pin; the (d)s enter the map")
    c = am["relief_variants_judgment_gate2"]["count"]
    nrs["session"] = (
        "The pin is v4.1.5. gate2 (V8) judged V7's relief variant (%d ACCEPT, %d AMEND: bradley-no-subject, the frame "
        "over account [2]) and RD-03 (ACCEPT as (d) at HR-02); judged, not ruled "
        "(adversarial_map.relief_variants_judgment_gate2, shapes_redrafts_v0_2_judgment_gate2). Next, in order: (1) his "
        "word on gate2's four asks; (2) seat l meets the one owed line in a new file, with five mutations for the "
        "builder's unproven checks; (3) gate2 judges that line; (4) the next declared pin session (safety_queue_L7, "
        "pin_queue_additions_R0292, the served-text repairs carried since L1 and LD3, F1's dopamine sentence and F4's "
        "'false claim' if his word queues it; the responseVariants render, RV-4, drawn by the design lane). "
        % (c["ACCEPT"], c["AMEND"]) + kept_tail)
    nrs["V8_closed"] = {"state": "JUDGED, NOT RULED (the relief variant pilot and RD-03)",
                        "blocks": NEW_KEYS, "canon_writer_next": "seat l"}
    d["keyset_delta_ledger"]["v38_55_V8"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: nothing; no pin." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "V8 (gate2, 2026-10-04): V7's relief variant judged (%d ACCEPT, %d AMEND, %d REJECT; the builder's checks "
        "CORRECT, five of ten unproven by a mutation; F1-F3 and the five pulls CONFIRM; F4 found) and RD-03 judged "
        "(ACCEPT as (d) at HR-02); gate2's own gates and controls; judged, not ruled. No pin."
        % (c["ACCEPT"], c["AMEND"], c["REJECT"]))

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
    print("project_canon_v38_55.json  %s / %d" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()
