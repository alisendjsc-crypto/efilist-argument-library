#!/usr/bin/env python3
"""project_canon_v38_39.json -- MINOR canon bump, no release. L6, the X-032 safety pass: SD-02's AMEND answered.

gate2 judged the drafts (canon v38.38, SP_drafts_judgments.json, R0209): nineteen text rows ACCEPT and one, SD-02,
AMEND (Z-002: the slot's unspaced em dash in place of a spaced one). L6 appends SD-10, superseding SD-02, and the
gate's v0_2, whose knock-on check reads the drafts record at the md5 each knock-on names (v0_1 is judged and stays
byte-identical). Adds adversarial_map.safety_pass_redraft_L6 and re-points next_recommended_session to gate2's
one-row judgment and his word.
Everything below is derived from the working tree at run time, never typed:
  - the gate (v0_2) runs GREEN in-process; its control record and the knock-on v0_2 are what it emits now, and the
    judged v0_1 knock-on still reproduces from the record at its md5;
  - v0_1 (judged) also gates the grown record GREEN;
  - the served surfaces are the v4.1.4 release, byte-identical (this bump moves no served byte).
ccclxiv FIRST: v38_38 is round-tripped at the serialization this file emits; it is read at its md5 from the working
tree or git history. Every top-level key other than the ones named in TOUCHED is asserted byte-identical, and inside
adversarial_map only the new key is added.

  python3 tools/build_canon_v38_39.py [--out DIR]
Repo-relative.
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_38.json", "4e27c6e376a69ddeb256a4dd862e0437"
OUT = os.path.join(OUT_DIR, "project_canon_v38_39.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L6", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEY = "safety_pass_redraft_L6"
R1 = "adversarial_map_staging/r1/"
FILES = {"record": R1 + "SP_drafts_L6.json", "gate": R1 + "sp_drafts_gate_l6_v0_2.py",
         "gate_v0_1": R1 + "sp_drafts_gate_l6.py", "control": R1 + "sp_drafts_gate_l6_control_v0_2.json",
         "knock_on": R1 + "SP_knock_on_L6_v0_2.json", "knock_on_v0_1": R1 + "SP_knock_on_L6_v0_1.json",
         "judgment": R1 + "SP_drafts_judgments.json"}
GATE_V0_1_MD5 = "65ea92a4272029cf1b6b02a0aedef4a8"   # judged: SP_drafts_judgments.json pins it
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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_38 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d["adversarial_map"].items()}
    assert NEW_KEY not in d["adversarial_map"]

    # ---------------------------------------------------------------- no served byte moves
    for rel, m in SERVED.items():
        assert hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest() == m, "%s moved: no pin here" % rel

    # ---------------------------------------------------------------- the gates, in-process
    assert f(FILES["gate_v0_1"])["md5"] == GATE_V0_1_MD5, "the judged v0_1 gate moved"
    G = load_mod(FILES["gate"], "sp_gate_v0_2")
    G1 = load_mod(FILES["gate_v0_1"], "sp_gate_v0_1")
    raw = open(os.path.join(REPO, FILES["record"]), "rb").read()
    rec = json.loads(raw.decode("utf-8"))
    fails, notes = G.check(rec, None)
    assert not fails, "the drafts gate v0_2 is RED:\n" + "\n".join(fails)
    fails1, _ = G1.check(rec, None)
    assert not fails1, "the judged v0_1 gate is RED on the grown record:\n" + "\n".join(fails1)
    rec_md5 = hashlib.md5(raw).hexdigest()
    ko = (json.dumps(G.knock_on_record(rec, rec_md5, os.path.basename(FILES["knock_on"])), indent=1,
                     ensure_ascii=False) + "\n").encode("utf-8")
    assert ko == open(os.path.join(REPO, FILES["knock_on"]), "rb").read(), "the knock-on v0_2 is not what the gate emits"
    k1 = open(os.path.join(REPO, FILES["knock_on_v0_1"]), "rb").read()
    named = json.loads(k1.decode("utf-8"))["record"]["md5"]
    at = json.loads(pinned.bytes_at(REPO, FILES["record"], named).decode("utf-8"))
    assert (json.dumps(G.knock_on_record(at, named, os.path.basename(FILES["knock_on_v0_1"])), indent=1,
                       ensure_ascii=False) + "\n").encode("utf-8") == k1, "the judged v0_1 knock-on no longer reproduces"
    assert json.loads(ko.decode("utf-8"))["rows"] == json.loads(k1.decode("utf-8"))["rows"], "the knock-on moved"
    ctl = json.load(open(os.path.join(REPO, FILES["control"]), encoding="utf-8"))
    assert ctl["record_md5"] == rec_md5 and ctl["gate_md5"] == f(FILES["gate"])["md5"], \
        "the control record names another record or gate"
    assert all(c["as_expected"] for c in ctl["controls"]) and ctl["controls"][0]["control"] == "C0"

    # ---------------------------------------------------------------- the row, read from the record
    sup = {r["supersedes"] for r in rec["rows"] if r.get("supersedes")}
    new = [r for r in rec["rows"] if r.get("supersedes")]
    assert [r["id"] for r in new] == ["SD-10"] and new[0]["supersedes"] == "SD-02"
    sd10 = new[0]
    sd02 = next(r for r in rec["rows"] if r["id"] == "SD-02")
    assert sd10["current"] == sd02["current"] and sd10["replacement"] == sd02["replacement"].replace(" — it is not", "—it is not")
    cur = [r for r in rec["rows"] if r["id"] not in sup and r["kind"] in ("draft", "companion", "widening")]
    jd = f(FILES["judgment"])

    block = {
        "what": "SD-02's AMEND answered. gate2 (canon v38.38, R0209) accepted nineteen of the twenty text rows and owed "
                "SD-02 one correction (Z-002): the slot's unspaced em dash in place of the spaced one. SD-10 supersedes "
                "SD-02 with exactly that change; its current text, cuts and keeps are SD-02's. Appended, never edited: "
                "the drafts record is append-only, and gate2's gate reads it at the md5 it judged.",
        "judgment_answered": {"file": jd["file"], "md5": jd["md5"], "row": "Z-002", "relay": "R0209"},
        "record": dict(f(FILES["record"]), rows=len(rec["rows"]), current_patching_rows=len(cur),
                       appended=["SD-10 (supersedes SD-02)"]),
        "row": {"id": sd10["id"], "locus": sd10["locus"], "replacement": sd10["replacement"], "words": sd10["words"]},
        "gate": dict(f(FILES["gate"]), what="v0_2: the knock-on check reproduces a committed knock-on from the drafts "
                                            "record at the md5 that knock-on names, so appended rows cannot turn it "
                                            "RED; --emit writes v0_2. G1..G11 and the self-test are v0_1's.",
                     controls="%d of %d as expected, the unmutated first (%s %s)" % (
                         sum(c["as_expected"] for c in ctl["controls"]), len(ctl["controls"]), FILES["control"],
                         f(FILES["control"])["md5"][:8]), notes=notes),
        "gate_v0_1": dict(f(FILES["gate_v0_1"]), state="judged (SP_drafts_judgments.json pins it); byte-identical; its "
                                                       "main check is GREEN on the grown record; its --knock-on --check "
                                                       "is RED by design once a row is appended (it compares the "
                                                       "knock-on of the CURRENT record); v0_2's check replaces it"),
        "knock_on": dict(f(FILES["knock_on"]), rows=len(json.loads(ko.decode("utf-8"))["rows"]),
                         note="rows identical to the judged v0_1 (%s), which v0_2 still reproduces from the record at "
                              "%s" % (f(FILES["knock_on_v0_1"])["md5"][:8], named[:8])),
        "patch_proof": [n for n in notes if " set: " in n],
        "next": "gate2 judges SD-10 alone; his word on the five asks (adversarial_map.safety_pass_judgment_gate2."
                "for_his_word; R0208 asks for it now, conditional on that one-row judgment); then the v4.1.5 pin.",
        "not_moved": "No served byte. SD-02 stays in the record, superseded.",
    }
    d["adversarial_map"][NEW_KEY] = block
    d["canon_version"] = "38.39"
    d["canon_version_marker"] = "v38.39"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.4. Next, in order: gate2 judges SD-10, L6's answer to SD-02's AMEND "
                      "(adversarial_map.safety_pass_redraft_L6); his word on the five asks (adversarial_map."
                      "safety_pass_judgment_gate2.for_his_word); the v4.1.5 pin (L6), a content cut; then the successor "
                      "map, which also takes X-033's sibling loci, PF-01..03, Z-033's honest-evaluation phrasing and "
                      "SF-05's label. Then adversarial wing v2 and /llms.txt, R2, and the interconnection design.")
    nrs["L6_safety_pass"] = {"state": "JUDGED: 19 of 20 text rows ACCEPT; SD-02 AMEND answered by SD-10, which gate2 "
                                      "judges alone", "record": block["record"]["file"], "md5": block["record"]["md5"],
                             "judgment": jd["file"], "then": "his word (R0208); the v4.1.5 pin"}
    d["keyset_delta_ledger"]["v38_39_L6"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s (SD-10 answers Z-002; the drafts gate's v0_2 and its "
        "knock-on v0_2 and control v0_2); next_recommended_session re-pointed; canon-meta; this note; one "
        "session_log_recent append. No served byte moved." % NEW_KEY)
    d["session_log_recent"].append(
        "L6 (%s): SD-02's AMEND (Z-002, a dash) answered as SD-10; drafts record %s; gate v0_2 (the knock-on check "
        "reads each record at its md5). No pin." % (DATE, block["record"]["md5"][:8]))

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
    print("project_canon_v38_39.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  %s: record %s / %d (%d rows); knock-on v0_2 %s; %s" % (
        NEW_KEY, block["record"]["md5"][:8], block["record"]["bytes"], block["record"]["rows"],
        block["knock_on"]["md5"][:8], block["gate"]["controls"]))


if __name__ == "__main__":
    main()
