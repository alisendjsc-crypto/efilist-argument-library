#!/usr/bin/env python3
"""measure_response_variants.py -- the measurement behind RESPONSE_VARIANTS_design_v0_1.md (V5, seat l, 2026-10-04).

Every count the design states comes from here, read at pinned bytes and never recalled:
  - the pleasure fork, from the vault's library crossref (its 33 secondary-conflict rows, read at a pinned vault commit
    through `git show`), against the six entries the crossref notes name (note 2, which his word adopted);
  - for each fork node, the long's sentence a relief variant would vary (an anchor of at most 15 words, unique in the
    long), the long's length, and whether the long gives the symmetric-razor reason for its concession;
  - the word lengths of the two answer-side layers that exist (archetype variants; notes) and of the fork's longs;
  - the flagship's two precedents for an alternative text (the archetype pills, which inherit the long's RSI grade; the
    [NOTE] disclosure, shown at long depth), read in site/combined.html at the pin;
  - what the game embeds (argue's KEEP tuple, read through `git show` at a pinned commit);
  - the top-level node keys the corpus carries today.

  python3 design/variations/measure_response_variants.py [--check]
--check recomputes the record and compares bytes, and asserts every figure the design doc states (DOC_FIGURES).
Repo-relative; the vault and the game are read at pinned commits, so their working trees may move.
"""
import hashlib, json, os, re, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402

OUT = "design/variations/measure_response_variants_v0_1.json"
DOC = "design/variations/RESPONSE_VARIANTS_design_v0_1.md"
CORPUS = ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1")
FLAGSHIP = ("site/combined.html", "6fd3617c90cca3c9196ac0143e27020a")
CANON = ("project_canon_v38_51.json", "72efc067aab95b6db04e10db1caf5410")
VAULT = {"repo": "~/Documents/Obsidian Vault", "commit": "e3cb5bbe017a9a5af5914501d9b6d3060a869dd5",
         "crossref": ("wiki/syntheses/library-crossref.md", "74784b04b3cdfc43ed9739bf24d95308"),
         "notes": ("claude/analyses/library-crossref-notes-2026-10-02.md", "71f31df9ad4e1b41da40922e62f21669")}
GAME = {"repo": "~/D/Argue the Argument", "commit": "76cbbd13ef967617b181697675bd15dbbf0a6a0b",
        "file": "inject_data.py", "md5": "e7d1505d11ccc086839a830f1207a0ef"}

# A named-pattern floor over the 33 rows. Every row was also read by hand; the floor must find exactly the rows read
# as the pleasure fork (pleasure as relief or illusion, against a long that grants positive goods), and no other.
FORK_FLOOR = re.compile(r"pleasure|relief|illusor|illusion|real goods?|positive states|not actually good|push|escape", re.I)
# The long's sentence each variant varies: at most 15 words, verbatim and unique in the node's long.
ANCHORS = {
    "life-gift": "the positives are therefore illusory, is one this corpus refuses on pain of incoherence",
    "joy-outweighs-harms": "it does not require the false claim that all pleasure is relief",
    "love-beauty-art": "Beauty is a real good, not demoted by having a neural substrate",
    "masochist-counterexample": "has a genuine appetitive, arousal-driven component; it is not reducible to escape",
    "bradley-no-subject": "positive states are real and genuinely valued by those who have them",
    "hedonic-contrast": "but it would still experience positive states",
    "neuroscience-positive-states": "positive states are real, and they are genuinely valued by the subject who has them",
}
# Where a long already runs his relief mechanism locally (R0290's note), the sentence that does it.
RUNS_HIS_MECHANISM = {
    "masochist-counterexample": "The 'pleasure' is the relief from that state, not a hedonic contribution from the food.",
    "neuroscience-positive-states": "Structurally, the goods of a life are deficit-occasioned, and our estimate of them is "
                                    "inflated upward by design.",
}
FLAGSHIP_MARKS = {
    "archetype_pills_inherit_rsi": "D6: variant inherits parent (base/long) RSI; no per-variant grade",
    "archetype_pills_replace_body": "const _bodyText = (_aSlot && _av && _av[_aSlot]) ? _av[_aSlot] : obj.responses[responseLevel];",
    "note_toggle_at_long": "if (obj.note && responseLevel === 'long') {",
}


def md5b(b):
    return hashlib.md5(b).hexdigest()


def git_show(repo, commit, rel, want):
    raw = subprocess.run(["git", "-C", os.path.expanduser(repo), "show", "%s:%s" % (commit, rel)],
                         capture_output=True, check=True).stdout
    assert md5b(raw) == want, "%s at %s is not the pinned bytes" % (rel, commit[:8])
    return raw.decode("utf-8")


def wstats(xs):
    xs = sorted(xs)
    q = statistics.quantiles(xs, n=10, method="inclusive") if len(xs) > 1 else [xs[0]] * 9
    return {"n": len(xs), "min": xs[0], "p10": round(q[0]), "median": round(statistics.median(xs)), "p90": round(q[8]),
            "max": xs[-1], "total": sum(xs)}


def build():
    corpus = json.loads(pinned.bytes_at(REPO, *CORPUS).decode("utf-8"))
    O = {o["id"]: o for o in corpus["objections"]}
    flag = pinned.bytes_at(REPO, *FLAGSHIP).decode("utf-8")
    canon = json.loads(pinned.bytes_at(REPO, *CANON).decode("utf-8"))
    xref = git_show(VAULT["repo"], VAULT["commit"], *VAULT["crossref"])
    notes = git_show(VAULT["repo"], VAULT["commit"], *VAULT["notes"])
    inj = git_show(GAME["repo"], GAME["commit"], GAME["file"], GAME["md5"])

    # 1. the crossref's secondary conflicts: the '- *also*' rows of its Conflicts section
    lines = xref.split("\n")
    a = next(i for i, ln in enumerate(lines) if ln.startswith("## Conflicts:"))
    b = next(i for i, ln in enumerate(lines) if i > a and ln.startswith("## ") and not ln.startswith("## Conflicts:"))
    rows = []
    for ln in lines[a:b]:
        m = re.match(r"- \*also\* \[\[(?:obj-|ref-)([^|\]]+)\|[^\]]*\]\] \(([^,)]+)[^)]*\): (.*)$", ln)
        if m:
            rows.append({"entry": m.group(1), "library": m.group(2), "text": m.group(3)})
    floor = [r["entry"] for r in rows if FORK_FLOOR.search(r["text"].split(" Sources:")[0])]
    fork = [r["entry"] for r in rows if r["entry"] in ANCHORS]
    assert floor == fork, (floor, fork)  # the floor and the reading agree
    m = re.search(r"Six entries carry the seam: ([^.]+)\.", notes)
    note_six = [x.strip() for x in re.split(r",| and ", m.group(1)) if x.strip()]
    assert len(note_six) == 6 and set(note_six) <= set(fork)
    not_in_note = [e for e in fork if e not in note_six]

    # 2. per node: the anchor, the long, the razor, his mechanism already run
    nodes = {}
    for n in fork:
        L = O[n]["responses"]["long"]
        anc = ANCHORS[n]
        assert L.count(anc) == 1 and len(anc.split()) <= 15, n
        sents = re.split(r"(?<=[.!?])\s+", L)
        hit = [i for i, s in enumerate(sents) if anc in s]
        assert len(hit) == 1, n
        row = next(r for r in rows if r["entry"] == n)
        nodes[n] = {"tier": O[n]["tier"], "crossref_row_md5": md5b(row["text"].encode("utf-8")),
                    "in_note_2": n in note_six, "long_words": len(L.split()), "long_sentences": len(sents),
                    "anchor": anc, "anchor_sentence_index": hit[0],
                    "anchor_sentence_words": len(sents[hit[0]].split()),
                    "gives_the_symmetric_razor": "razor" in L,
                    "top_level_keys_beyond_the_base": sorted(k for k in O[n] if k not in (
                        "id", "tier", "category", "trigger", "keywords", "psychMechanism", "diagnosis", "responses",
                        "sources"))}
        if n in RUNS_HIS_MECHANISM:
            assert L.count(RUNS_HIS_MECHANISM[n]) == 1, n
            nodes[n]["already_runs_his_mechanism"] = RUNS_HIS_MECHANISM[n]

    # 3. the answer-side layers that exist, by words
    av = [len(t.split()) for o in corpus["objections"] for t in ((o["responses"].get("archetypeVariants") or {}).values())]
    nt = [len(o["note"].split()) for o in corpus["objections"] if o.get("note")]
    lw = [nodes[n]["long_words"] for n in fork]

    # 4. the flagship's precedents and the game's embed
    marks = {k: flag.count(v) for k, v in FLAGSHIP_MARKS.items()}
    assert all(v == 1 for v in marks.values()), marks
    km = re.search(r"KEEP = \(([^)]*)\)", inj)
    keep = [x.strip().strip('"') for x in km.group(1).split(",") if x.strip()]
    top = {}
    for o in corpus["objections"]:
        for k in o:
            top[k] = top.get(k, 0) + 1

    # 5. the residual as canon carries it
    rv = canon["adversarial_map"]["relief_view_for_the_variant"]
    resid = rv["the_open_residual"]
    rec = {
        "what": "the measurement behind the responseVariants design v0_1 (V5, seat l, 2026-10-04)",
        "pins": {"corpus": dict(zip(("file", "md5"), CORPUS)), "flagship": dict(zip(("file", "md5"), FLAGSHIP)),
                 "canon": dict(zip(("file", "md5"), CANON)),
                 "vault": {"repo": VAULT["repo"], "commit": VAULT["commit"],
                           "crossref": dict(zip(("file", "md5"), VAULT["crossref"])),
                           "notes": dict(zip(("file", "md5"), VAULT["notes"]))},
                 "game": GAME},
        "pleasure_fork": {
            "secondary_conflict_rows": len(rows),
            "fork_rows": fork,
            "fork_count": len(fork),
            "floor": FORK_FLOOR.pattern,
            "floor_equals_the_reading": True,
            "note_2_names": note_six,
            "measured_not_in_note_2": not_in_note,
        },
        "nodes": nodes,
        "words": {"archetype_variants": wstats(av), "notes": wstats(nt), "fork_longs": wstats(lw),
                  "shapes_band": [30, 70]},
        "razor_nodes": [n for n in fork if nodes[n]["gives_the_symmetric_razor"]],
        "flagship_precedents": {k: {"marker": FLAGSHIP_MARKS[k], "occurrences": v} for k, v in marks.items()},
        "game_embed": {"keep": keep, "responses_kept_whole": "responses" in keep,
                       "top_level_keys_not_kept": sorted(k for k in top if k not in keep)},
        "corpus_top_level_keys": dict(sorted(top.items())),
        "archetype_variant_nodes": sum(1 for o in corpus["objections"] if o["responses"].get("archetypeVariants")),
        "the_open_residual": {"from": "adversarial_map.relief_view_for_the_variant.the_open_residual",
                              "md5": md5b(resid.encode("utf-8")), "words": len(resid.split())},
        "his_accounts_in_canon": len(rv["his_accounts_verbatim"]),
    }
    return rec, (json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def doc_figures(rec):
    """Each figure the design doc states, as the exact text it must contain."""
    pf, w = rec["pleasure_fork"], rec["words"]
    return [
        "%d secondary-conflict rows" % pf["secondary_conflict_rows"],
        "%d of them" % pf["fork_count"],
        "archetype variants run %d to %d words (median %d" % (w["archetype_variants"]["min"], w["archetype_variants"]["max"],
                                                            w["archetype_variants"]["median"]),
        "%d notes run %d to %d words" % (w["notes"]["n"], w["notes"]["min"], w["notes"]["max"]),
        "%d nodes" % rec["archetype_variant_nodes"],
        "fork's longs run %d to %d words" % (w["fork_longs"]["min"], w["fork_longs"]["max"]),
        "%d of the %d longs" % (len(rec["razor_nodes"]), pf["fork_count"]),
        "KEEP = (%s)" % ", ".join(rec["game_embed"]["keep"]),
    ]


def main():
    rec, out = build()
    if "--check" in sys.argv:
        same = open(os.path.join(REPO, OUT), "rb").read() == out
        doc = open(os.path.join(REPO, DOC), encoding="utf-8").read() if os.path.exists(os.path.join(REPO, DOC)) else ""
        doc = " ".join(doc.split())  # the text wraps; a figure is checked with whitespace collapsed
        missing = [f for f in doc_figures(rec) if f not in doc]
        for f in missing:
            print("DOC FIGURE MISSING: %s" % f)
        print("RESPONSE VARIANTS MEASURE: %s; doc figures %d of %d" % (
            "matches the committed record" if same else "DIFFERS", len(doc_figures(rec)) - len(missing),
            len(doc_figures(rec))))
        sys.exit(0 if same and not missing else 1)
    open(os.path.join(REPO, OUT), "wb").write(out)
    print("%s  %s / %d" % (OUT, md5b(out), len(out)))
    for f in doc_figures(rec):
        print("  doc figure: %s" % f)


if __name__ == "__main__":
    main()
