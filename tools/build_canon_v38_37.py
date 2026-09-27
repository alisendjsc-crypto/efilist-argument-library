#!/usr/bin/env python3
"""project_canon_v38_37.json -- MINOR canon bump, no release. L6, the X-032 safety pass: the drafts (R0193 order 2).

Adds adversarial_map.safety_pass_drafts_L6 and re-points next_recommended_session to gate2's judgment of them.
Everything below is derived from the working tree at run time, never typed, except his words:
  - the drafts record's gate runs GREEN in-process, and its control record and knock-on record are what the gate
    emits now;
  - the reading record is what sp_reading_l6.py computes now;
  - the counts (rows by kind, loci, words) are read from the record;
  - the served surfaces are the v4.1.4 release, byte-identical (this bump moves no served byte).
ccclxiv FIRST: v38_36 is round-tripped at the serialization this file emits; it is read at its md5 from the working
tree or git history. Every top-level key other than the ones named in TOUCHED is asserted byte-identical, and inside
adversarial_map only the new key is added.

  python3 tools/build_canon_v38_37.py [--out DIR]
Repo-relative.
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_36.json", "6d84dfc8ab465e409bc712154f74a30a"
OUT = os.path.join(OUT_DIR, "project_canon_v38_37.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L6", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEY = "safety_pass_drafts_L6"
R1 = "adversarial_map_staging/r1/"
FILES = {"record": R1 + "SP_drafts_L6.json", "builder": R1 + "build_SP_drafts_L6.py",
         "gate": R1 + "sp_drafts_gate_l6.py", "control": R1 + "sp_drafts_gate_l6_control_v0_1.json",
         "knock_on": R1 + "SP_knock_on_L6_v0_1.json", "dossiers": R1 + "sp_dossiers_l6.py",
         "reading_instrument": R1 + "sp_reading_l6.py", "reading": R1 + "sp_reading_l6_v0_1.json",
         "patch_tool": "tools/pin_patch_l6.py"}
SERVED = {"site/combined.html": "ed040cad2f60caaf0cba696af77f860e",
          "efilist_argument_library_v4_0_0.json": "f3d88311ea98f8333aebbecb67766351",
          "efilist_argument_library_v4_0_0.jsx": "518c62f4ce3fe40ea3408475f608b1ff"}

sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"file": rel, "md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def load_mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_36 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d["adversarial_map"].items()}
    assert NEW_KEY not in d["adversarial_map"]

    # ---------------------------------------------------------------- no served byte moves
    for rel, m in SERVED.items():
        assert hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest() == m, "%s moved: no pin here" % rel

    # ---------------------------------------------------------------- the gate, in-process
    G = load_mod(FILES["gate"], "sp_gate")
    rec = json.load(open(os.path.join(REPO, FILES["record"]), encoding="utf-8"))
    # base None: the build precedes the commit, so the notes are the build-time notes and a rebuild from the commit
    # reproduces them (the append-only check, G10, is the gate's own, run in the battery against HEAD)
    fails, notes = G.check(rec, None)
    assert not fails, "the drafts gate is RED:\n" + "\n".join(fails)
    ko = (json.dumps(G.knock_on_record(rec), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    assert ko == open(os.path.join(REPO, FILES["knock_on"]), "rb").read(), "the knock-on record is not what the gate emits"
    ctl = json.load(open(os.path.join(REPO, FILES["control"]), encoding="utf-8"))
    assert ctl["record_md5"] == f(FILES["record"])["md5"] and ctl["gate_md5"] == f(FILES["gate"])["md5"], \
        "the control record names another record or gate"
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["controls"][0]["control"] == "C0"
    Rd = load_mod(FILES["reading_instrument"], "sp_reading")
    fresh = (json.dumps(Rd.measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    assert fresh == open(os.path.join(REPO, FILES["reading"]), "rb").read(), "the reading record is not fresh"
    reading = json.loads(fresh.decode("utf-8"))
    assert rec["queue"]["reading"]["md5"] == hashlib.md5(fresh).hexdigest()

    # ---------------------------------------------------------------- counts, read from the record
    cur = [r for r in rec["rows"]]
    by = {}
    for r in cur:
        by.setdefault(r["kind"], []).append(r)
    counts = {k: {"rows": len(v), "loci": sorted({r["locus"] for r in v}) if k != "finding" else None,
                  "words_delta": sum(r["words"]["delta"] for r in v) if k != "finding" else None}
              for k, v in by.items()}
    counts = {k: {kk: vv for kk, vv in v.items() if vv is not None} for k, v in counts.items()}
    kor = json.loads(ko.decode("utf-8"))["rows"]
    canon_lines = [n for n in notes if " set: " in n]

    block = {
        "what": "L6, the X-032 safety pass, drafted: the six passages gate2 found framing the survival drive, or the "
                "taboo against suicide, as a barrier on an exit (PQ_repair_drafts_judgments.json X-032), re-measured "
                "on the v4.1.4 text and repaired in draft, with the same framing found and drafted at revealed-"
                "preference's other slots (proposed companions) and at survivor-testimony (a proposed widening). "
                "DRAFTED, NOT JUDGED: gate2 judges (K258), then his word, then the pin (v4.1.5, a content cut).",
        "his_words": rec["queue"]["his_word"],
        "bar_reading": rec["queue"]["bar_reading"],
        "queue": {"finding": "X-032", "judgment": rec["queue"]["judgment"], "loci": rec["queue"]["loci"]},
        "reading": {"instrument": f(FILES["reading_instrument"]), "record": f(FILES["reading"]),
                    "gate2_patterns": "%d hits at %d loci on %d nodes of corpus %s; equal to X-032's six: %s" % (
                        len(reading["exit_framing_gate2"]["hits"]), len(reading["exit_framing_gate2"]["loci"]),
                        len(reading["exit_framing_gate2"]["nodes"]), reading["reads"]["corpus"]["md5"][:8],
                        reading["exit_framing_gate2"]["equals_x032"]),
                    "every_corpus_string": "%d strings, %d hits outside the six" % (
                        reading["exit_framing_all"]["strings_swept"], len(reading["exit_framing_all"]["outside_the_six"])),
                    "wide_set_classes": {k: len(v) for k, v in reading["classes"].items()},
                    "wings": "no X-032 framing in any of the five; Right to Die's 'exit' is its word for assisted death "
                             "under its own firewall (class rtd_term)"},
        "drafts": dict(f(FILES["record"]), counts=counts,
                       statuses={"draft": "declared (the queue)",
                                 "companion": "proposed: needs his word to enter the queue",
                                 "widening": "proposed: widens the queue beyond X-032; needs his word"}),
        "gate": dict(f(FILES["gate"]), controls="%d of %d as expected, the unmutated first (%s %s)" % (
            sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]), FILES["control"],
            f(FILES["control"])["md5"][:8]), notes=notes),
        "patch_tool": f(FILES["patch_tool"]),
        "patch_proof": canon_lines + ["on both sets xsurface's sidecar checks are GREEN too: both sidecars regenerate byte "
                                      "for byte from the patched flagship, so no mapped literal moves (survivor-"
                                      "testimony's psychMechanism, mirrored in MAP_GRAPH_DATA, is left for that "
                                      "reason; SF-05)"],
        "knock_on": dict(f(FILES["knock_on"]), rows=len(kor),
                         summary=["%s %s #%s%s" % (r["kind"], r.get("locus", r.get("row")), r.get("n"),
                                                  (" (%s)" % r.get("verdict")) if r.get("verdict") else "")
                                  for r in kor]),
        "dossiers": dict(f(FILES["dossiers"]), how="python3 %s --out <scratch dir>" % FILES["dossiers"]),
        "builder": f(FILES["builder"]),
        "asks": [
            "Judge (gate2, K258): SD-01..09 over the six; SC-01..04, the siblings at revealed-preference; SW-01..07, "
            "the widening to survivor-testimony; the ten findings.",
            "His word, after the judgment: ratify the drafts; admit the companions (lean yes: a slot fixed while its "
            "sibling keeps the framing leaves the node saying both); widen to survivor-testimony (lean yes: the "
            "strongest form of the framing in the corpus); take SW-07 (lean yes: one figure, nothing the argument uses).",
            "Then the pin, v4.1.5, a content cut: tools/pin_patch_l6.py --apply --set ratified --corpus-version 4.1.5.",
        ],
        "not_moved": "No served byte. The frozen maps and every record stay pinned to their corpora; nothing here "
                     "re-pins a map.",
    }
    d["adversarial_map"][NEW_KEY] = block
    d["canon_version"] = "38.37"
    d["canon_version_marker"] = "v38.37"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.4. Next, in order: gate2 judges L6's safety-pass drafts (adversarial_map."
                      "safety_pass_drafts_L6; a session that drafted none of them, K258); Josiah's word on the drafts, "
                      "the companions and the widening; the v4.1.5 pin (L6); then the successor map that re-anchors "
                      "(adversarial_map.corpus_repairs_LANDED_L5.for_the_successor_map, and L6's knock-on), re-judges "
                      "the six waiting (a)s and files PF-01..03, X-033's siblings and X-034 as (b)s for a later queue; "
                      "then adversarial wing v2 and /llms.txt (adversarial_map.reader_aid_backlog_L4c), R2, and the "
                      "interconnection design. R0160 (the house layer's depth, wuld-ink) runs in its own lane.")
    nrs["L6_safety_pass"] = {"state": "DRAFTED, NOT JUDGED", "record": block["drafts"]["file"],
                             "md5": block["drafts"]["md5"], "judge": "gate2 (K258)",
                             "then": "his word; the v4.1.5 pin"}
    d["keyset_delta_ledger"]["v38_37_L6"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s (the X-032 safety pass's drafts, not judged); "
        "next_recommended_session re-pointed with an L6_safety_pass record; canon-meta; this note; one "
        "session_log_recent append. No served byte moved; invariants, schemas, hazard_map and flagship_sidecars "
        "asserted byte-identical." % NEW_KEY)
    d["session_log_recent"].append(
        "L6 (%s): the X-032 safety pass DRAFTED, not judged. gate2's patterns re-find exactly the six on v4.1.4; a "
        "wider sweep finds the same framing at revealed-preference's long and short and at survivor-testimony. %d "
        "drafts over the six, %d proposed companions, %d proposed widening rows, %d findings (%s %s). No pin." % (
            DATE, counts["draft"]["rows"], counts["companion"]["rows"], counts["widening"]["rows"],
            counts["finding"]["rows"], block["drafts"]["file"].split("/")[-1], block["drafts"]["md5"][:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(d["adversarial_map"][k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(d["adversarial_map"])[-1] == NEW_KEY and len(d["adversarial_map"]) == len(am_before) + 1
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_37.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  %s: drafts %s / %d; knock-on %d rows; %s" % (NEW_KEY, block["drafts"]["md5"][:8], block["drafts"]["bytes"],
                                                          len(kor), block["gate"]["controls"]))


if __name__ == "__main__":
    main()
