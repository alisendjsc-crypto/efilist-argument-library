#!/usr/bin/env python3
"""project_canon_v38_36.json -- MINOR canon bump for a PATCH release. LD3, the design lane's pin move: v4.1.3 -> v4.1.4,
the flagship's tier marks and ladder (LD2's package), a page-design change that moves no objection.

Everything written here is derived from the working tree at run time, never typed, except his words:
  - the corpus JSON, the JSX and objections-index.json are BYTE-IDENTICAL to v4.1.3's (read from the v4.1.3 commit),
    and the objections digest is unchanged;
  - tools/xsurface_v4_1_0.py runs GREEN at the v4.1.3 canonical md5, and tools/build_map_sidecars.py --check leaves
    both sidecars unchanged;
  - tools/icons_regen_check.py is GREEN (every mark region is what icons/gen_icons.py draws);
  - tools/pin_labels_ld3.py --check finds every label at the new pin.
ccclxiv FIRST: v38_35 is round-tripped at the serialization this file emits; it is read at its md5 from the working
tree or git history. The invariants subtree is asserted byte-identical: that is what makes the release a PATCH.

  python3 tools/build_canon_v38_36.py --version v4.1.4 [--out DIR]
Repo-relative.
"""
import hashlib, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
VERSION = sys.argv[sys.argv.index("--version") + 1]
SRC_REL, SRC_MD5 = "project_canon_v38_35.json", "972a3856e625f6eb8795a1a63b088d9f"
OUT = os.path.join(OUT_DIR, "project_canon_v38_36.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "LD3", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "flagship_sidecars"}
HIS_WORD = {"his_words_verbatim": "Approved as is.", "said": "2026-09-26, in chat to the LD3 session, on its preview",
            "declared_by": "'Go with your recommendations on both.' (to LD2, on its close; kickoff R0170)"}

sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging/r1/"))
import pinned  # noqa: E402

CORPUS, JSX, HTML, INDEX = ("efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx",
                            "site/combined.html", "objections-index.json")
BASE_COMMIT = "5c4181e0e73c7e9af85998dece9de197d1b6fc22"   # v4.1.3
OLD_HTML, OLD_LABEL, CANONICAL = ("f72e6762173dada604e0fe250e76f810", 2990639), "v4.1.3", "8b76672fa3ca3cc33ca99e5b35fc25bd"
XS, SIDECARS, ICONS, LABELS = ("tools/xsurface_v4_1_0.py", "tools/build_map_sidecars.py", "tools/icons_regen_check.py",
                               "tools/pin_labels_ld3.py")
VALIDATOR = "adversarial_map_staging/adv_map_validator_v0_6.py"
PACKAGE = {"branch": "design/marks-flagship", "built": "LD2 7bf5b35", "merged_v4_1_3": "LD3 8074e80",
           "feedback_link_fix": "LD3 ce7ffc4"}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def at_base(rel):
    return subprocess.run(["git", "show", "%s:%s" % (BASE_COMMIT, rel)], cwd=REPO, capture_output=True, check=True).stdout


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=REPO, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.returncode, r.stdout


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_35 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}

    # ---------------------------------------------------------------- no objection moves
    for rel in (CORPUS, JSX, INDEX):
        assert open(os.path.join(REPO, rel), "rb").read() == at_base(rel), "%s moved: this pin moves no objection" % rel
    spec = importlib.util.spec_from_file_location("v6", os.path.join(REPO, VALIDATOR))
    V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)
    digest = V.objections_digest(json.load(open(os.path.join(REPO, CORPUS), encoding="utf-8")))
    assert digest == d["adversarial_map"]["corpus_repairs_LANDED_L5"]["objections_digest"]["new"], digest
    rc, out = run([XS])
    assert rc == 0, "xsurface RED on the working tree"
    canon_md5 = sorted({l.split()[4] for l in out.splitlines()
                        if len(l.split()) >= 5 and l.split()[2] == "objections" and l.split()[3] == "canon"})
    assert canon_md5 == [CANONICAL], canon_md5
    rc, out = run([SIDECARS, "--check"])
    assert rc == 0, "the sidecars would change"
    rc, out = run([ICONS])
    assert rc == 0, "icons_regen_check RED:\n" + out
    marks_line = [l for l in out.splitlines() if l.startswith("MARKS:")][0]
    rc, out = run([LABELS, "--check", "--version", VERSION, "--canon", "38.36"])
    assert rc == 0, "a label is not at the new pin:\n" + out
    new = f(HTML)
    assert new["md5"] != OLD_HTML[0]

    # ---------------------------------------------------------------- the pin record
    fs = d["flagship_sidecars"]
    prev = fs["extracted_from"]
    fs["extracted_from"] = {"file": HTML, "pin": VERSION, "md5": new["md5"], "bytes": new["bytes"],
                            "re_extracted": "%s --check: both sidecars byte-identical from %s (the marks touch no mapped "
                                            "literal)" % (SIDECARS, VERSION),
                            "previous": prev}
    d["canon_version"] = "38.36"
    d["canon_version_marker"] = "v38.36"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is %s. Next, in order: R0160, the house layer's depth (seat code, wuld-ink; launched by "
                      "LD3 at its close); a short safety pass over the six survival-as-barrier passages gate2 found "
                      "(X-032); a successor map that re-anchors (adversarial_map.corpus_repairs_LANDED_L5."
                      "for_the_successor_map), re-judges the six waiting (a)s and files PF-01..03, X-033's siblings and "
                      "X-034 as (b)s for a later queue; then adversarial wing v2 and /llms.txt "
                      "(adversarial_map.reader_aid_backlog_L4c), R2, and the interconnection design." % VERSION)
    nrs["LD3_pin"] = {
        "what": "%s -> %s: the flagship's tier marks in their tiers' own colours, its ladder beside its title, a shared "
                "link's badge mark playing once, and the badge row kept clear of the house layer's feedback link on "
                "phones. Page design only: the corpus, the JSX and objections-index.json are byte-identical to %s, the "
                "objections digest holds at %s, xsurface holds at %s." % (OLD_LABEL, VERSION, OLD_LABEL, digest[:8],
                                                                           CANONICAL[:8]),
        "his_word": HIS_WORD,
        "pin": {"old": "%s / %d (%s)" % (OLD_HTML[0], OLD_HTML[1], OLD_LABEL),
                "new": "%s / %d (%s)" % (new["md5"], new["bytes"], VERSION)},
        "package": PACKAGE,
        "marks": marks_line,
        "records": "design/glyph_architecture/: ARCHITECTURE_library_v0_2.md s7 (the owes), controls_marks_v0_3.json "
                   "(22 controls; v0_2 is LD2's record, frozen at the pre-pin page), measure_flagship_v0_2.json and its "
                   "control on the v4.1.3 page, ld3/preview_ld3.mjs",
        "tools": {"labels": dict(f(LABELS), file=LABELS)},
    }
    d["keyset_delta_ledger"]["v38_36_LD3"] = (
        "MINOR. keyset UNCHANGED at 42. PIN MOVE %s -> %s (%s -> %s), page design only. next_recommended_session "
        "re-pointed with an LD3_pin record; flagship_sidecars.extracted_from moved forward (sidecars byte-identical); "
        "canon-meta; this note; one session_log_recent append. invariants, schemas, hazard_map and adversarial_map "
        "asserted byte-identical: a PATCH." % (OLD_LABEL, VERSION, OLD_HTML[0][:8], new["md5"][:8]))
    d["session_log_recent"].append(
        "LD3 (%s): THE PIN MOVE, %s -> %s (%s / %d). The design lane's flagship marks, approved on the preview (\"%s\"); "
        "no objection moved (corpus, JSX, index byte-identical; xsurface %s); labels moved with the pin." % (
            DATE, OLD_LABEL, VERSION, new["md5"][:8], new["bytes"], HIS_WORD["his_words_verbatim"], CANONICAL[:8]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map", "adversarial_map"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved: not a PATCH" % k
    fs_before = json.loads(before["flagship_sidecars"])
    fs_after = dict(d["flagship_sidecars"]); fs_after.pop("extracted_from"); fs_before.pop("extracted_from")
    assert fs_after == fs_before, "flagship_sidecars moved beyond extracted_from"
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_36.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  pin %s -> %s  %s / %d; canonical %s (unchanged)" % (OLD_LABEL, VERSION, new["md5"], new["bytes"], CANONICAL))


if __name__ == "__main__":
    main()
