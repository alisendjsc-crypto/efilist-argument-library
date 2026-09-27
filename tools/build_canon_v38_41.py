#!/usr/bin/env python3
"""project_canon_v38_41.json -- MINOR canon bump for a PATCH release. L6, THE PIN MOVE: v4.1.4 -> v4.1.5, the content cut
of the X-032 safety pass, ratified by Josiah's word and applied to the three surfaces at once.

Everything written here is derived from the working tree at run time, never typed:
  - the ratification row (his words, the relay whose asks they answer, the exact rows) is read from the drafts record,
    and the drafts gate v0_2 (G11 included) must be GREEN over it;
  - the three working surfaces must be BYTE-IDENTICAL to what tools/pin_patch_l6.py builds from the ratified rows with
    the corpus's content-cut version moved to the release label;
  - tools/xsurface_v4_1_0.py runs on the working tree (GREEN, one canonical md5 across the three surfaces),
    tools/build_map_sidecars.py --check leaves both sidecars unchanged, and build_objections_index.py --check finds the
    projection wuld.ink vendors unchanged;
  - tools/pin_labels_l6.py --check finds every label at the new pin;
  - the reading, gate2's two judgment gates and their readings stay GREEN on the moved corpus (they read every
    artifact at its pinned md5);
  - the knock-on of the ratified record is the knock-on gate2 confirmed (the ratification moves no drafted row).
ccclxiv FIRST: v38_40 is round-tripped at the serialization this file emits; it is read at its md5 from the working
tree or git history. The invariants, schemas and hazard_map subtrees are asserted byte-identical: a PATCH.

  python3 tools/build_canon_v38_41.py --version v4.1.5 [--out DIR]
Repo-relative.
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
VERSION = sys.argv[sys.argv.index("--version") + 1]
SRC_REL, SRC_MD5 = "project_canon_v38_40.json", "0e89f9cddd0aad4488ab41d93408eb85"
OUT = os.path.join(OUT_DIR, "project_canon_v38_41.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L6", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map", "flagship_sidecars"}
NEW_KEY = "safety_pass_LANDED_L6"

R1 = "adversarial_map_staging/r1/"
sys.path.insert(0, os.path.join(REPO, R1))
import pinned  # noqa: E402

CORPUS, JSX, HTML = "efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx", "site/combined.html"
OLD = {CORPUS: ("f3d88311ea98f8333aebbecb67766351", 1337252), JSX: ("518c62f4ce3fe40ea3408475f608b1ff", 1276711),
       HTML: ("ed040cad2f60caaf0cba696af77f860e", 2999806)}
OLD_LABEL, OLD_CANONICAL, OLD_VERSION_FIELD = "v4.1.4", "8b76672fa3ca3cc33ca99e5b35fc25bd", "4.1.3"
RECORD, GATE = R1 + "SP_drafts_L6.json", R1 + "sp_drafts_gate_l6_v0_2.py"
KNOCK = R1 + "SP_knock_on_L6_v0_2.json"   # gate2 confirmed it (Z2-002); the ratification moves no drafted row
PATCH, LABELS, RATIFY = "tools/pin_patch_l6.py", "tools/pin_labels_l6.py", "tools/pin_ratify_l6.py"
XS, SIDECARS, OINDEX = "tools/xsurface_v4_1_0.py", "tools/build_map_sidecars.py", "build_objections_index.py"
VALIDATOR = "adversarial_map_staging/adv_map_validator_v0_6.py"
MUST_STAY_GREEN = [[R1 + "sp_reading_l6.py", "--check"], [R1 + "sp_judgments_gate.py"],
                   [R1 + "sp_judgment_reading.py", "--check"], [R1 + "sp_redrafts_gate.py"],
                   [R1 + "sp_redraft_reading.py", "--check"], [OINDEX, "--check"]]
R0193 = {"relay": "R0193", "md5": "ead76c9af94cb5cedea3c00d1499529c"}


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
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_40 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert NEW_KEY not in am

    # ---------------------------------------------------------------- the drafts gate and the knock-on
    DG = mod(GATE, "spg2")
    rawrec = open(os.path.join(REPO, RECORD), "rb").read()
    rec = json.loads(rawrec.decode("utf-8"))
    dfails, dnotes = DG.check(rec, None)
    assert not dfails, "DRAFTS GATE v0_2 RED: %s" % dfails
    ko = DG.knock_on_record(rec, hashlib.md5(rawrec).hexdigest(), os.path.basename(KNOCK))
    ko2 = json.load(open(os.path.join(REPO, KNOCK), encoding="utf-8"))
    assert ko["rows"] == ko2["rows"], "the ratification moved the knock-on: it must not, since it changes no drafted row"
    for args in MUST_STAY_GREEN:
        rc, out = run(args)
        assert rc == 0, "%s RED on the moved corpus:\n%s" % (" ".join(args), out[-2000:])

    # ---------------------------------------------------------------- the ratification and the patch
    P = mod(PATCH, "pp6")
    cur = P.current_rows(rec)
    rat = [r for r in cur if r["kind"] == "ratification"][-1]
    rows = P.select(rec, "ratified")
    judgment = am["safety_pass_redraft_judgment_gate2"]
    lst = judgment["the_text_his_word_ratifies"]
    assert rat["rows"] == lst["drafts"] + lst["companions_and_widening"], "SR-01 is not gate2's list"
    assert rat["his_words_verbatim"] == judgment["his_word"]["verbatim"]
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
    assert len(canon_md5) == 1 and canon_md5[0] != OLD_CANONICAL, canon_md5
    rc, out = run([SIDECARS, "--check"])
    assert rc == 0, "the sidecars would change"
    rc, out = run([LABELS, "--check", "--version", VERSION, "--canon", "38.41"])
    assert rc == 0, "a label is not at the new pin:\n" + out
    V = mod(VALIDATOR, "v6")
    digest_old = V.objections_digest(json.loads(pinned.bytes_at(REPO, CORPUS, OLD[CORPUS][0]).decode("utf-8")))
    corpus_new = json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8"))
    digest_new = V.objections_digest(corpus_new)
    assert digest_old != digest_new and corpus_new["version"] == VERSION.lstrip("v")
    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    ko_kinds = {}
    for x in ko["rows"]:
        ko_kinds[x["kind"]] = ko_kinds.get(x["kind"], 0) + 1
    loci = sorted({r["locus"] for r in rows})
    nodes = sorted({l.split("#")[0] for l in loci})
    words = sum(r["words"]["delta"] for r in rows)

    # ---------------------------------------------------------------- the block
    am[NEW_KEY] = {
        "what_landed": "The X-032 safety pass, as judged and ratified: %d rewrites (%d drafts over X-032's six passages, "
                       "%d companions at revealed-preference's other slots, %d widening rows at survivor-testimony) at %d "
                       "loci across %d objections, on the corpus JSON, the JSX and site/combined.html in one edit; %+d "
                       "words. Release %s, a PATCH by the invariants convention and a content cut."
                       % (len(rows), kinds.get("draft", 0), kinds.get("companion", 0), kinds.get("widening", 0),
                          len(loci), len(nodes), words, VERSION),
        "his_word": {"his_words_verbatim": rat["his_words_verbatim"], "said": rat["said"], "relay": rat["relay"],
                     "ratification_row": rat["id"], "rows": rat["rows"],
                     "covers": judgment["his_word"]["what_it_covers"]},
        "the_bar": d["adversarial_map"]["safety_pass_drafts_L6"]["his_words"]["bar"],
        "judged_by": rat["judgment"],
        "declared": "R0193 (%s), LD3's kickoff on his word to LD3; the pass itself on his word to L5 answering R0181"
                    % R0193["md5"][:8],
        "pin": {"old": "%s / %d (%s)" % (OLD[HTML][0], OLD[HTML][1], OLD_LABEL),
                "new": "%s / %d (%s)" % (new[HTML][0], new[HTML][1], VERSION)},
        "corpus": {"old": "%s / %d" % OLD[CORPUS], "new": "%s / %d" % new[CORPUS],
                   "version_field": "%s -> %s (it names the CONTENT CUT, K335)" % (OLD_VERSION_FIELD,
                                                                                  VERSION.lstrip("v"))},
        "jsx": {"old": "%s / %d" % OLD[JSX], "new": "%s / %d" % new[JSX]},
        "cross_surface_canonical": {"old": OLD_CANONICAL, "new": canon_md5[0]},
        "objections_digest": {"old": digest_old, "new": digest_new},
        "loci": loci,
        "proof": "The three working surfaces are byte-identical to what %s builds from the ratified rows (whole-locus "
                 "replacement, each locus unique on every surface; every old text gone and every replacement once, on "
                 "each surface); %s GREEN at one canonical md5; %s --check unchanged; %s --check unchanged (the "
                 "projection wuld.ink vendors); %s --check GREEN; the reading and gate2's judgment gates and readings "
                 "GREEN on the moved corpus." % (PATCH, XS, SIDECARS, OINDEX, LABELS),
        "tools": {"patch": dict(f(PATCH), file=PATCH), "labels": dict(f(LABELS), file=LABELS),
                  "ratify": dict(f(RATIFY), file=RATIFY), "drafts_gate": dict(f(GATE), file=GATE)},
        "not_moved": "survivor-testimony's psychMechanism label (SF-05: mirrored in MAP_GRAPH_DATA and pinned by a "
                     "sidecar), the bridge's name where the objection states itself (his word on ask 4, gate2's lean), "
                     "every map, fragment, register and record (pinned to their corpora; never re-pin a map).",
        "for_the_successor_map": dict(f(KNOCK), file=KNOCK, counts=ko_kinds,
                                      does="re-anchor #47 (its anchor was in SD-08's replaced phrase); re-read #44 (its "
                                           "anchor survives inside SD-07's sentence), #3 and #56 (HOLDS; their answers "
                                           "route to repaired loci and stand); rewrite #3's grounds, which quote the "
                                           "removed text; re-judge the (b) at revealed-preference#long, whose repair "
                                           "SC-01..03 made",
                                      also="Z-033 (boonin-critique's 'prevents honest evaluation', with #45's and "
                                           "#47's charge); SF-05's label; X-033's sibling loci; PF-01..03; the two "
                                           "dependency edges SF-07 names"),
        "served_labels": "README (pin table, libraries row, stable-at, canon file, BibTeX), CITATION.cff, the /libraries "
                         "badge and a CHANGELOG release entry, by %s (the K362 law)." % LABELS,
        "next_in_this_session": "wuld-ink's half (the release manifest, tools/library-pin.py once the deploy reads back, "
                                "the releases entry, the feed and the search index) and argue's re-vendor notice: "
                                "wuld.ink/argue/ embeds the corpus, and every landed row is text it shows.",
    }
    fs = d["flagship_sidecars"]
    prev = fs["extracted_from"]
    fs["extracted_from"] = {"file": HTML, "pin": VERSION, "md5": new[HTML][0], "bytes": new[HTML][1],
                            "re_extracted": "%s --check: both sidecars byte-identical from %s (the repairs touch no "
                                            "mapped literal)" % (SIDECARS, VERSION),
                            "previous": prev}
    d["canon_version"] = "38.41"
    d["canon_version_marker"] = "v38.41"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is %s. Next, in order: the successor map, which re-anchors (adversarial_map."
                      "corpus_repairs_LANDED_L5.for_the_successor_map and %s.for_the_successor_map), re-judges the six "
                      "waiting (a)s and files PF-01..03, X-033's siblings, X-034 and Z-033 as (b)s for a later queue; "
                      "V0 (variations of objections and rebuttals, R0194/R0197) in its own lane; then adversarial wing "
                      "v2 and /llms.txt (adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design."
                      % (VERSION, NEW_KEY))
    nrs["L6_safety_pass"] = {"state": "LANDED", "pin": "%s -> %s" % (OLD_LABEL, VERSION), "block": NEW_KEY}
    d["keyset_delta_ledger"]["v38_41_L6"] = (
        "MINOR. keyset UNCHANGED at 42. PIN MOVE %s -> %s (%s -> %s). One adversarial_map subkey addition (%s); "
        "flagship_sidecars.extracted_from moved forward (sidecars byte-identical); next_recommended_session re-pointed; "
        "canon-meta; this note; one session_log_recent append. invariants, schemas and hazard_map asserted "
        "byte-identical: a PATCH." % (OLD_LABEL, VERSION, OLD[HTML][0][:8], new[HTML][0][:8], NEW_KEY))
    d["session_log_recent"].append(
        "L6 (%s): THE PIN MOVE, %s -> %s (%s / %d). The X-032 safety pass: %d rewrites at %d loci across %d objections, "
        "ratified on his word (\"%s\"), applied to the three surfaces in one edit; xsurface %s -> %s; sidecars and the "
        "objections index unchanged; labels moved with the pin." % (
            DATE, OLD_LABEL, VERSION, new[HTML][0][:8], new[HTML][1], len(rows), len(loci), len(nodes),
            rat["his_words_verbatim"], OLD_CANONICAL[:8], canon_md5[0][:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved: not a PATCH" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-1] == NEW_KEY and len(am) == len(am_before) + 1
    fs_before = json.loads(before["flagship_sidecars"])
    fs_after = dict(d["flagship_sidecars"]); fs_after.pop("extracted_from"); fs_before.pop("extracted_from")
    assert fs_after == fs_before, "flagship_sidecars moved beyond extracted_from"
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_41.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  pin %s -> %s  %s / %d; canonical %s -> %s; %d rows at %d loci, %+d words" % (
        OLD_LABEL, VERSION, new[HTML][0], new[HTML][1], OLD_CANONICAL[:8], canon_md5[0][:8], len(rows), len(loci), words))


if __name__ == "__main__":
    main()
