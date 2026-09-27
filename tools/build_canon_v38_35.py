#!/usr/bin/env python3
"""project_canon_v38_35.json -- MINOR canon bump for a PATCH release. L5's phase 5, THE PIN MOVE: v4.1.2 -> v4.1.3, the
content cut of the queued corpus repairs, ratified by Josiah's word and applied to the three surfaces at once.

Everything written here is derived from the working tree at run time, never typed:
  - the ratification row (his words, the relay that carried them, the exact rows) is read from the repair record, and
    the drafts gate v0_2 (G10 included) must be GREEN over it;
  - the three working surfaces must be BYTE-IDENTICAL to what tools/pin_patch_l5_v0_2.py builds from the ratified rows
    with the corpus's content-cut version moved to the release label;
  - tools/xsurface_v4_1_0.py runs on the working tree (GREEN, one canonical md5 across the three surfaces), and
    tools/build_map_sidecars.py --check leaves both sidecars unchanged;
  - tools/pin_labels_l5.py --check finds every label at the new pin;
  - the rulings gate, the quote check and gate2's five judgment gates are GREEN in-process.
ccclxiv FIRST: v38_34 is round-tripped at the serialization this file emits; it is read at its md5 from the working
tree or git history. The invariants subtree is asserted byte-identical: that is what makes the release a PATCH.

  python3 tools/build_canon_v38_35.py --version v4.1.3 [--out DIR]
Repo-relative.
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
VERSION = sys.argv[sys.argv.index("--version") + 1]
SRC_REL, SRC_MD5 = "project_canon_v38_34.json", "f9de897c7b28a699f34be101ce98648d"
OUT = os.path.join(OUT_DIR, "project_canon_v38_35.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L5", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map", "flagship_sidecars"}
ADDED = ["corpus_repairs_LANDED_L5"]

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

CORPUS, JSX, HTML = "efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx", "site/combined.html"
OLD = {CORPUS: ("04bf6482aa0374ee92a81c1d55ec41f8", 1334024), JSX: ("b196548b6eb39065842d62292acca89f", 1273483),
       HTML: ("006aa9833f7a8b103ad27a289ab22fa9", 2987411)}
OLD_LABEL, OLD_CANONICAL = "v4.1.2", "6cd132ee5b8c7ca78ad0e095806f1c93"
RECORD, GATE2_DRAFTS = R1 + "PQ_repair_drafts_L5.json", R1 + "pin_repair_drafts_gate_v0_2.py"
KNOCK = R1 + "PQ_knock_on_L5_v0_2.json"   # gate2 pins it; the ratification changes no row it covers
PATCH, LABELS, XS, SIDECARS = ("tools/pin_patch_l5_v0_2.py", "tools/pin_labels_l5.py", "tools/xsurface_v4_1_0.py",
                               "tools/build_map_sidecars.py")
VALIDATOR = "adversarial_map_staging/adv_map_validator_v0_6.py"
JUDGE_GATES = [(R1 + "r1_judgments_gate.py", R1 + "R1_drafts_judgments.json"),
               (R1 + "r1_v1_5_judgments_gate.py", R1 + "R1_v1_5_judgments.json"),
               (R1 + "r1_v1_6_judgments_gate.py", R1 + "R1_v1_6_judgments.json"),
               (R1 + "pq_repair_judgments_gate.py", R1 + "PQ_repair_drafts_judgments.json"),
               (R1 + "pq_repair_redrafts_gate.py", R1 + "PQ_repair_redrafts_judgments.json")]
R0150 = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2"}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=REPO, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.returncode, r.stdout


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_34 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}

    # ---------------------------------------------------------------- gates, in-process
    G = mod(R1 + "r1_rulings_gate.py", "r1rg")
    fails, _ = G.check(os.path.join(REPO, R1 + "R1_rulings.json"), REPO, G.committed_base())
    assert not fails, "RULINGS GATE RED: %s" % fails
    Q = mod(R1 + "r1_quote_check.py", "r1qc")
    q_rows = Q.rulings_quotes()
    q_ok, q_fail = Q.check(q_rows, Q.Texts())
    assert not q_fail and q_ok == len(q_rows), "QUOTE CHECK RED: %s" % q_fail
    for i, (gate, rec_rel) in enumerate(JUDGE_GATES):
        M = mod(gate, "jg%d" % i)
        fl, _ = M.check(os.path.join(REPO, rec_rel), REPO, M.committed_base())
        assert not fl, "%s RED: %s" % (gate, fl)
    DG = mod(GATE2_DRAFTS, "pqg2")
    rec = json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
    dfails, dnotes = DG.check(rec, DG.committed_base())
    assert not dfails, "DRAFTS GATE v0_2 RED: %s" % dfails
    ko = DG.knock_on_record(rec)
    ko2 = json.load(open(os.path.join(REPO, KNOCK), encoding="utf-8"))
    assert {k: v for k, v in ko.items() if k != "record"} == {k: v for k, v in ko2.items() if k != "record"}, \
        "the ratification moved the knock-on: it must not, since it changes no draft or companion"

    # ---------------------------------------------------------------- the ratification and the patch
    P = mod(PATCH, "pp2")
    cur = P.current_rows(rec)
    rat = [r for r in cur if r["kind"] == "ratification"][-1]
    rows = P.select(rec, "ratified")
    built, change = P.build(rec, rows, corpus_version=VERSION.lstrip("v"))
    for surf, text in built.items():
        assert text.encode("utf-8") == open(os.path.join(REPO, surf), "rb").read(), \
            "%s is not what the ratified rows build" % surf
    new = {s: (f(s)["md5"], f(s)["bytes"]) for s in (CORPUS, JSX, HTML)}
    for s in new:
        assert new[s][0] != OLD[s][0], "%s did not move" % s
    rc, out = run([XS])
    assert rc == 0, "xsurface RED on the working tree"
    canon_md5 = sorted({l.split()[4] for l in out.splitlines()
                        if len(l.split()) >= 5 and l.split()[2] == "objections" and l.split()[3] == "canon"})
    assert len(canon_md5) == 1, canon_md5
    rc, out = run([SIDECARS, "--check"])
    assert rc == 0, "the sidecars would change"
    rc, out = run([LABELS, "--check", "--version", VERSION])
    assert rc == 0, "a label is not at the new pin:\n" + out
    V = mod(VALIDATOR, "v6")
    digest_old = V.objections_digest(json.loads(pinned.bytes_at(REPO, CORPUS, OLD[CORPUS][0]).decode("utf-8")))
    digest_new = V.objections_digest(json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8")))
    assert digest_old != digest_new
    corpus_new = json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8"))
    assert corpus_new["version"] == VERSION.lstrip("v")
    drafts = [r for r in rows if r["kind"] == "draft"]
    comps = [r for r in rows if r["kind"] == "companion"]
    kinds = {}
    for x in ko["rows"]:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1

    # ---------------------------------------------------------------- the block
    am["corpus_repairs_LANDED_L5"] = {
        "what_landed": "The queued corpus repairs, as judged and ratified: %d sentences across %d objections and %d "
                       "companion sentences, on the corpus JSON, the JSX and site/combined.html in one edit. Release %s, a "
                       "PATCH by the invariants convention (the invariants subtree byte-identical) and a content cut."
                       % (len(drafts), len({r["locus"].split("#")[0] for r in drafts}), len(comps), VERSION),
        "his_word": {"his_words_verbatim": rat["his_words_verbatim"], "said": rat["said"], "relay": rat["relay"],
                     "ratification_row": rat["id"], "rows": rat["rows"]},
        "judged_by": rat["judgment"],
        "declared": "R0150 (%s), on his words 'Go with your recommendation on the pin session.' and 'open it when the "
                    "window is clear'; see adversarial_map.pin_move_queue_L5.declared" % R0150["md5"][:8],
        "pin": {"old": "%s / %d (%s)" % (OLD[HTML][0], OLD[HTML][1], OLD_LABEL),
                "new": "%s / %d (%s)" % (new[HTML][0], new[HTML][1], VERSION)},
        "corpus": {"old": "%s / %d" % OLD[CORPUS], "new": "%s / %d" % new[CORPUS],
                   "version_field": "4.1.0 -> %s (it names the CONTENT CUT, K335)" % VERSION.lstrip("v")},
        "jsx": {"old": "%s / %d" % OLD[JSX], "new": "%s / %d" % new[JSX]},
        "cross_surface_canonical": {"old": OLD_CANONICAL, "new": canon_md5[0]},
        "objections_digest": {"old": digest_old, "new": digest_new},
        "proof": "The three working surfaces are byte-identical to what %s builds from the ratified rows (whole-locus "
                 "replacement, each locus unique on every surface; every old sentence gone and every replacement once, on "
                 "each surface); %s GREEN at one canonical md5; %s --check unchanged; %s --check GREEN."
                 % (PATCH, XS, SIDECARS, LABELS),
        "tools": {"patch": dict(f(PATCH), file=PATCH), "labels": dict(f(LABELS), file=LABELS),
                  "drafts_gate": dict(f(GATE2_DRAFTS), file=GATE2_DRAFTS)},
        "maps_frozen": "Every map (v1_1..v1_6), fragment, register and measurement stays pinned to corpus %s, and every "
                       "instrument reads it there (adversarial_map.instruments_read_pinned_corpus_L5). Never re-pin a "
                       "map." % OLD[CORPUS][0][:8],
        "for_the_successor_map": dict(f(KNOCK), file=KNOCK, counts=kinds,
                                      stands="every row recomputes identically after the ratification row (only the "
                                             "record md5 in its header names the pre-ratification record)",
                                      does="re-anchor the entries whose anchors lay inside a repaired sentence, re-read "
                                           "the map text that quoted one, and re-judge the six waiting (a)s against the "
                                           "repaired text"),
        "served_labels": "README (pin table, libraries row, stable-at, BibTeX), CITATION.cff, the /libraries badge and a "
                         "CHANGELOG release entry, by %s (the K362 law)." % LABELS,
        "next_in_this_session": "wuld-ink's half (the release manifest, tools/library-pin.py once the deploy reads back, "
                                "the releases entry, the feed and the search index) and the game's re-vendor notice.",
    }
    fs = d["flagship_sidecars"]
    prev = fs["extracted_from"]
    fs["extracted_from"] = {"file": HTML, "pin": VERSION, "md5": new[HTML][0], "bytes": new[HTML][1],
                            "re_extracted": "%s --check: both sidecars byte-identical from %s (the repairs touch no "
                                            "mapped literal)" % (SIDECARS, VERSION),
                            "previous": prev}

    d["canon_version"] = "38.35"
    d["canon_version_marker"] = "v38.35"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is %s. Next, in order: the design lane's flagship package, LD3 (R0170), rebased onto the "
                      "repaired flagship; a short safety pass over the six survival-as-barrier passages gate2 found "
                      "(X-032); a successor map that re-anchors (adversarial_map.corpus_repairs_LANDED_L5."
                      "for_the_successor_map), re-judges the six waiting (a)s and files PF-01..03, X-033's siblings and "
                      "X-034 as (b)s for a later queue; then adversarial wing v2 and /llms.txt "
                      "(adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design." % VERSION)
    nrs["L5_pin"] = "%s -> %s, adversarial_map.corpus_repairs_LANDED_L5." % (OLD_LABEL, VERSION)
    d["keyset_delta_ledger"]["v38_35_L5"] = (
        "MINOR. keyset UNCHANGED at 42. PIN MOVE %s -> %s (%s -> %s). One adversarial_map subkey addition "
        "(corpus_repairs_LANDED_L5); flagship_sidecars.extracted_from moved forward (sidecars byte-identical); "
        "next_recommended_session re-pointed; canon-meta; this note; one session_log_recent append. invariants, schemas "
        "and hazard_map asserted byte-identical: a PATCH." % (OLD_LABEL, VERSION, OLD[HTML][0][:8], new[HTML][0][:8]))
    d["session_log_recent"].append(
        "L5 (%s): THE PIN MOVE, %s -> %s (%s / %d). %d sentences and %d companions, ratified on his word (%s), applied to "
        "the three surfaces in one edit; xsurface %s -> %s; sidecars unchanged; labels moved with the pin." % (
            DATE, OLD_LABEL, VERSION, new[HTML][0][:8], new[HTML][1], len(drafts), len(comps),
            rat["relay"].get("relay"), OLD_CANONICAL[:8], canon_md5[0][:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved: not a PATCH" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-1:] == ADDED and set(am) - set(am_before) == set(ADDED)
    fs_before = json.loads(before["flagship_sidecars"])
    fs_after = dict(d["flagship_sidecars"]); fs_after.pop("extracted_from"); fs_before.pop("extracted_from")
    assert fs_after == fs_before, "flagship_sidecars moved beyond extracted_from"
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_35.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  pin %s -> %s  %s / %d; canonical %s" % (OLD_LABEL, VERSION, new[HTML][0], new[HTML][1], canon_md5[0]))


if __name__ == "__main__":
    main()
