#!/usr/bin/env python3
"""project_canon_v38_42.json -- MINOR canon bump, no release. L6's close: the v4.1.5 pin's tail, and his word on V0's six
rulings (relayed to the canon writer as R0216, the R0164 precedent).

Adds to adversarial_map:
  safety_pass_LANDED_L6_tail      wuld.ink's half of the v4.1.5 pin (wuld-ink b217171), the live read-backs, and the
                                  game's re-vendor notice (R0222)
  variations_rulings_V0           his word on V0's six rulings (R-V1..R-V6), read at source in the V0 session
  audience_forward_note_V0_R_V5   R-V5 recorded FORWARD beside audience_and_purpose_ruling_L1a, whose text is untouched
and re-points next_recommended_session.
Measured at run time, never typed: the relay md5s (from the relay index), wuld-ink's pin commit and its release
manifest (from that repo's git objects), V0's design and record (from this repo's git objects at 08a3402), the served
surfaces (the v4.1.5 release, byte-identical: this bump moves no served byte). The live read-backs are what L6 measured
at 21:07-21:15 America/Phoenix; they are recorded as observations, dated, not re-measured here.
ccclxiv FIRST: v38_41 is round-tripped at the serialization this file emits; it is read at its md5 from the working
tree or git history. Every top-level key outside TOUCHED is asserted byte-identical, and inside adversarial_map only the
three new keys are added.

  python3 tools/build_canon_v38_42.py [--out DIR]
Repo-relative.
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_41.json", "d2d95e612b9c1018fbc9312d8d819f54"
OUT = os.path.join(OUT_DIR, "project_canon_v38_42.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION, DATE = "L6", "2026-09-26"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["safety_pass_LANDED_L6_tail", "variations_rulings_V0", "audience_forward_note_V0_R_V5"]
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
WULD = os.path.expanduser("~/Projects/wuld-ink")
WULD_PIN = "b21717192c86dfaf2ad543e4cbb6620c9f0162c8"
V0_COMMIT = "08a3402809dba39b4e24462e6707f9186fbf2359"
V0_FILES = {"design": ("design/variations/VARIATIONS_design_v0_1.md", "fcf6f6fe0813072a3c66edd723a1ec80"),
            "record": ("design/variations/measure_variations_v0_1.json", "67aa82418682b03560945c4d77f0c504")}
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
V0_WORDS = "Go with your leans on all of the rulings."

sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402


def relay_row(rid):
    for line in open(INDEX, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) > 8 and p[1] == "SENT" and p[2] == rid:
            return p
    raise LookupError(rid)


def relay_md5(rid):
    return relay_row(rid)[8]


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, check=True).stdout


def main():
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_41 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in SERVED.items():
        assert hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest() == m, "%s moved: no pin here" % rel

    manifest = git(WULD, "show", "%s:release_v4_1_5.json" % WULD_PIN)
    assert json.loads(manifest)["pin"]["new"] == SERVED["site/combined.html"]
    wuld_files = [x for x in git(WULD, "show", "--name-only", "--format=", WULD_PIN).decode().split("\n") if x]
    v0 = {k: hashlib.md5(git(REPO, "show", "%s:%s" % (V0_COMMIT, rel))).hexdigest() for k, (rel, _) in V0_FILES.items()}
    assert all(v0[k] == m for k, (_, m) in V0_FILES.items()), v0
    row = relay_row("R0216")
    r0216 = row[8]
    r0216_body = open(os.path.join(os.path.dirname(INDEX), row[7]), "rb").read()
    assert hashlib.md5(r0216_body).hexdigest() == r0216, "R0216 drifted"
    assert V0_WORDS.encode("utf-8") in r0216_body, "R0216 does not carry the words recorded here"

    am["safety_pass_LANDED_L6_tail"] = {
        "wuld_ink": {"commit": WULD_PIN, "manifest": {"file": "release_v4_1_5.json",
                                                     "md5": hashlib.md5(manifest).hexdigest(), "bytes": len(manifest)},
                     "files": len(wuld_files),
                     "did": "tools/library-pin.py --apply --date 2026-09-26 after its live gate read 6fd3617c three "
                            "times: 12 src surfaces (md5 x2, version x24, bytes x1), 0 residual over 108 files; "
                            "tools/apply_release_summary.py (the release's own prose; feed 100 items); "
                            "src/search-index.json 1,014 -> 1,014 entries, two version labels changed. Branched from "
                            "origin/main 1ff18d2 in its own worktree and pushed fast-forward."},
        "read_back_live": [
            "library.wuld.ink/combined: 6fd3617c on 3 consecutive reads, 18 s after the efilist push (21:07 MST)",
            "library.wuld.ink/libraries/: byte-identical to the committed page (078d89de), badge 'pinned v4.1.5'",
            "rendered in the browser: 82 objection cards; five sampled replacements present and five sampled removed "
            "passages absent; no console error; every request 200",
            "wuld.ink: 14 of 15 changed surfaces byte-identical to b217171; /contact/ differs only by Cloudflare's "
            "edge email obfuscation and carries v4.1.5",
        ],
        "argue": {"relay": "R0222", "md5": relay_md5("R0222"),
                  "state": "wuld.ink/argue/ (fc5e3ee8, byte-identical to its source) still embeds 20 of 20 pre-cut "
                           "passages until argue re-vendors corpus 4.1.5 and re-mounts; L6's lean: at its next session"},
    }
    am["variations_rulings_V0"] = {
        "his_words_verbatim": V0_WORDS,
        "said": "2026-09-26, in chat to the V0 session (local_09acbf8f), as R0216 reports it",
        "read_at_source": "L6 found the sentence verbatim in the V0 session's transcript (K392: a relay points to his "
                          "words, it does not replace them)",
        "relay": {"relay": "R0216", "md5": r0216},
        "adopts": "V0's design section 9, each ruling as leaned (recorded in the design's section 11)",
        "rulings": {
            "R-V1": "argumentShapes is a new top-level node key. objectionSubforms stays as ratified (it holds the "
                    "defender's refusal shapes: 4 of 4 definitions open 'Position-holder').",
            "R-V2": "The corpus carries (a) shapes only. (b) goes to the regen queue, (d) to the map, (c) to the intake.",
            "R-V3": "Shapes render on the flagship card in a pin; the game re-vendors them from the corpus.",
            "R-V4": "Pilot: life-gift, joy-outweighs-harms, future-solve, free-will-defense, meta-ethical-pluralism, "
                    "meaning-through-suffering.",
            "R-V5": "The game may play the adversarial map's retreats in ROUTE THE RETREAT, after the successor map "
                    "lands, (a) entries first; the (d) entries fall under the same ruling. Recorded forward beside L1a: "
                    "audience_forward_note_V0_R_V5.",
            "R-V6": "The new-objection intake runs after the pilot is judged, over scholarly and published work "
                    "including 2024-2026 (his K345a scope).",
        },
        "design": {"branch": "design/variations", "commit": V0_COMMIT,
                   "file": V0_FILES["design"][0], "md5": v0["design"],
                   "record": {"file": V0_FILES["record"][0], "md5": v0["record"]},
                   "state": "on its branch, not on main: V1 (R0217) lands it --no-ff from main's side"},
        "recorded_by": "L6, the canon writer at its close (the R0164 precedent: a word relayed to the canon writer is "
                       "recorded in its next bump); V1 therefore writes no canon for these",
    }
    am["audience_forward_note_V0_R_V5"] = {
        "note": "For the game, R-V5 changes L1a's 'public to read, never promoted': the game may play the adversarial "
                "map's retreats in ROUTE THE RETREAT once the successor map lands, (a) entries first, the (d) entries "
                "under the same ruling. Everywhere else L1a stands as ruled.",
        "his_words_verbatim": V0_WORDS,
        "ruling": "variations_rulings_V0.rulings.R-V5",
        "leaves_untouched": "adversarial_map.audience_and_purpose_ruling_L1a (its text is not edited; this note sits "
                            "beside it, forward-only)",
    }
    assert json.dumps(am["audience_and_purpose_ruling_L1a"], sort_keys=True, ensure_ascii=False) == \
        am_before["audience_and_purpose_ruling_L1a"]

    d["canon_version"] = "38.42"
    d["canon_version_marker"] = "v38.42"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = ("The pin is v4.1.5. Next, side by side: V1 (R0217) lands design/variations on main (--no-ff "
                      "from main's side) and builds the argumentShapes schema and shape validator in new files (no "
                      "canon: the six rulings are recorded at adversarial_map.variations_rulings_V0; no pin); and the "
                      "successor map, which holds the canon: it re-anchors (adversarial_map.corpus_repairs_LANDED_L5."
                      "for_the_successor_map and safety_pass_LANDED_L6.for_the_successor_map), re-judges the six "
                      "waiting (a)s, files PF-01..03, X-033's siblings, X-034 and Z-033 as (b)s, and its validator "
                      "bump carries argumentShapes.<shape_id> as an existence-gated locus (R0194's sequence). Then V2 "
                      "drafts the pilot's shapes (R-V4) and gate2 judges; argue re-vendors v4.1.5 (R0222); then "
                      "adversarial wing v2 and /llms.txt, R2, the interconnection design, and the new-objection intake "
                      "(R-V6) once the pilot is judged.")
    nrs["L6_safety_pass"] = {"state": "LANDED and read back (efilist and wuld.ink); argue's re-vendor pending",
                             "pin": "v4.1.4 -> v4.1.5", "blocks": ["safety_pass_LANDED_L6", "safety_pass_LANDED_L6_tail"]}
    d["keyset_delta_ledger"]["v38_42_L6"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. No served byte moved; audience_and_purpose_ruling_L1a asserted "
        "byte-identical (R-V5 is recorded forward beside it)." % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "L6 (%s): the v4.1.5 pin's tail (wuld-ink %s, read back; argue's re-vendor notice R0222) and his word on V0's six "
        "rulings (\"%s\", R0216, read at source), R-V5 recorded forward beside L1a. No pin." % (DATE, WULD_PIN[:8],
                                                                                                V0_WORDS))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-3:] == NEW_KEYS and len(am) == len(am_before) + 3
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_42.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()
