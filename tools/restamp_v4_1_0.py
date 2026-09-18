#!/usr/bin/env python3
"""restamp_v4_1_0.py -- phase 2 of the v4.1.0 cut: the surfaces that carry the pin.

Phase 2 because every target needs the NEW md5, which does not exist until the flagship is
written. Reads the tracked files, writes to k344_drop/. Never mutates the originals.

THREE OF THESE ARE CORRECTIONS, NOT RESTAMPS, and they are named as such rather than folded
into a routine-looking diff: README's pin table, its status prose and the front-door badge
all still said v4.0.4 four days after /combined began serving v4.0.5, and the CHANGELOG has
no v4.0.5 entry at all. The v4.0.5 pin move landed the pin and the wuld side and never came
back for the efilist-side release surfaces.
"""
import hashlib, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, "k344_drop")
EMD, ELL = "—", "…"

PIN_NEW, PIN_NEW_B = "72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770
PIN_405, PIN_405_B = "cee25a00b68ba036138d064c383d9a8b", 2982658
PIN_404, PIN_404_B = "c60dcb56498debc84d2fb2860cd55167", 2982518
CORPUS_NEW, CORPUS_NEW_B = "04bf6482aa0374ee92a81c1d55ec41f8", 1334024
JSX_NEW, JSX_NEW_B = "b196548b6eb39065842d62292acca89f", 1273483
DIG_OLD, DIG_NEW = "0218f73b7bfac7c9bcf7d352a5eab5cc", "2c5a083a31448dec0f1ce41e08ba5b04"
XS_OLD, XS_NEW = "a597fb18cac0b12434d63c4cfd23cfff", "6cd132ee5b8c7ca78ad0e095806f1c93"
NB = "{:,}".format(PIN_NEW_B)

fail = []
def edit(path, subs):
    s = io.open(os.path.join(ROOT, path), encoding="utf-8", newline="").read()
    for old, new in subs:
        n = s.count(old)
        if n != 1:
            fail.append("%s: anchor %r occurs %d times, expected 1" % (path, old[:70], n))
            continue
        s = s.replace(old, new, 1)
    out = os.path.join(DROP, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="").write(s)
    b = s.encode("utf-8")
    print("  %-22s %d edits  md5 %s  %d B" % (path, len(subs), hashlib.md5(b).hexdigest(), len(b)))
    return s

print("RESTAMP v4.1.0 " + EMD + " pin %s / %s bytes\n" % (PIN_NEW, NB))

# ---- README ---------------------------------------------------------------------------
STATUS_OLD = "**Stable at v4.0.4** (canon v38.1 line)."
STATUS_NEW = "**Stable at v4.1.0** (canon v38.4 line)."
TAIL_OLD = ("v4.0.4 made the breadcrumb bar's first segment a link to the umbrella front door, which the "
            "flagship had named without linking. None of the four touched the corpus. See")
TAIL_NEW = ("v4.0.4 made the breadcrumb bar's first segment a link to the umbrella front door, which the "
            "flagship had named without linking. v4.0.5 regenerated the load-bearing hierarchy table from "
            "the dependency graph's own links and stripped a third era of inert baked counters. **None of "
            "the five touched the corpus** " + EMD + " and v4.0.5 never reached this README, the front-door "
            "badge or the changelog either, all three of which said `v4.0.4` for four days while "
            "`/combined` served v4.0.5; corrected here. **v4.1.0 is the first release since v4.0.0 to change "
            "the corpus.** Three subtractive repairs, six spans, all three shipped surfaces: a heritability "
            "coefficient read as the fraction of one person's happiness fixed at conception, an argument "
            "from silence offered as a credential, and an unsourced one-in-a-hundred ratio doing "
            "architectural work. Each removes a claim that is false or unsupported; none adds an argument. "
            "See")
edit("README.md", [
    ("| Version (pin) | `v4.0.4` |", "| Version (pin) | `v4.1.0` |"),
    ("| md5 | `%s` |" % PIN_404, "| md5 | `%s` |" % PIN_NEW),
    ("| Size | `{:,}` bytes |".format(PIN_404_B), "| Size | `%s` bytes |" % NB),
    ("flagship " + "·" + " pinned v4.0.4", "flagship " + "·" + " pinned v4.1.0"),
    (STATUS_OLD, STATUS_NEW),
    (TAIL_OLD, TAIL_NEW),
    ("**`project_canon_v38_3.json`** " + EMD + " the current canon record.",
     "**`project_canon_v38_4.json`** " + EMD + " the current canon record."),
])

# ---- the front door -------------------------------------------------------------------
edit(os.path.join("libraries", "index.html"),
     [("<span>pinned v4.0.4</span>", "<span>pinned v4.1.0</span>")])

# ---- CHANGELOG ------------------------------------------------------------------------
ENTRY = """## [v4.1.0] ~~ 2026-09-17

**PATCH by the invariants convention at the top of this file; MINOR by the canon version-class ruling that set the number.** The two conventions are keyed on different things and this is the first release where they disagree, because it is the first release to advance corpus **content** without moving a single count. The invariants subtree is byte-identical, so the rule at the top of this file reads PATCH. Canon's `post_terminal_policy` keys the number on enrichment-versus-intake, and enrichment of existing nodes is MINOR, which is why the queue's `version_class_ruling` set `v4.1.0` rather than `v4.0.6`. Recorded here rather than resolved: both rules are doing their own job correctly.

**The first corpus change since the v4.0.0 content cut of 2026-07-11.** Three pure-subtraction repairs from the nineteen-item v4.1.0 enrichment queue, each removing a claim that is false or unsupported, none adding an argument. They went first because their correctness is judgeable without re-litigating any philosophy: the question is whether the sentence is true, not whether the move is good.

| | node | locus | what went | words |
|---|---|---|---|---|
| **R1** | `happiness-is-choice` | `long` | a heritability coefficient read as the fraction of **one person's** happiness fixed at conception ~~ the coefficient partitions variance *between* people. The slice-of-the-pie carve-up built on it goes with it. | 555 {A} 589 (+34) |
| **R2** | `just-edgy` | `long` | *"has never been substantively refuted"* ~~ an argument from silence offered as a credential, inside a rebuttal against arguments from authority. Reception is now **described** (more often categorized than answered) rather than **adjudicated**. | 220 {A} 220 |
| **R3** | `just-depressed` | `long` + `archetypeVariants.defender` | an unsourced one-in-a-hundred ratio organising the node's opening and its close, inside the corpus's most epistemically self-aware rebuttal. Stated qualitatively instead; nothing depended on 1:99 rather than 1:20. | 979 {A} 978, 347 {A} 344 |

`subtractive` classifies the **claim**, not the word count. R1 is +34 words because saying why a statistic fails to license an inference takes more room than making the inference took. The bare-deletion variant shipped beside it in the spec as `R1-alt` and was **not** taken.

### R3 had four spans, not three

The spec named three, all in `responses.long`, and its own scope note says a repair that fixes the opening and leaves the close still counting to ninety-nine produces a node that contradicts itself. The same unsourced ratio also stood at `responses.archetypeVariants.defender` ~~ live shipped text, once per surface. It was found by sweeping the **defect** across every locus of every node rather than the five named strings, ratified the same session, and repaired with the other three.

That sweep turned up something larger, which is **not** fixed here and is recorded in canon: `archetypeVariants` is not in the map validator's `LOCI` enum at all, so `target_locus` cannot name it and `anchor-rule` cannot reach it. **16 of 82 nodes carry archetype variants ~~ 10,072 words of live shipped corpus text the Adversarial Map is structurally unable to adjudicate.**

### Three surfaces, no build step

`combined.html` is a hand-assembled superset carrying `REBUTTAL_STRENGTH`, which the JSX does not, and nothing regenerates any surface from any other. The same six spans live in all three, byte-identically, so one replacement pair served all three ~~ 18 span-replacements across 12 line-loci, each line-indexed with a per-line anchor assertion, each surface verified against its **git blob** for a changed set of exactly the named lines.

**A corpus-vs-flagship gate did not exist and now does** (`tools/xsurface_v4_1_0.py`): string-aware bracket-balance extraction of the `const OBJECTIONS` literal from the flagship and the JSX, compared against the corpus file by canonical-serialization md5. All three agree at `{XSOLD}` before and `{XSNEW}` after, and the same four leaves moved on every surface.

### The Adversarial Map is frozen, not advanced

Each repaired node carried one Phase E entry classed `(b)` whose verbatim anchor is cut from the sentence being repaired, and `status-enum` pins `status` to `mapped` as a hard check ~~ so after the cut no status value can say an anchor is historical. `coverage: 82/82` is a claim about a **(map, corpus) pair**, bound by `meta-corpus-pin`; advancing the pin under entries authored against the old text would change a receipt's referent while keeping its claim. So `adversarial_map_v1_0.json` stays byte-identical at `c4989e98{E}` and stays pinned to corpus `6ee1f6f3{E}`, against which it still validates under `--assembly` at **21 checks, 0 violations, 0 advisories**. Measured both ways: against the post-cut corpus it is FAIL with 5 violations, while `coverage` passes in **both**, which is the proof it only breaks if the entries are *removed*. A successor map is owed: 79 nodes inherit, three re-adjudicate.

| | md5 | bytes |
|---|---|---|
| superseded ~~ v4.0.0 | `e654eabd32fa95e5969d49e6eb15aa87` | 2,963,752 |
| superseded ~~ v4.0.1 | `9d13359e305c6caa3ae64759f3dcc0e6` | 2,963,789 |
| superseded ~~ v4.0.2 | `62d1e8d86056465ebcb5daced38e0a83` | 2,974,039 |
| superseded ~~ v4.0.3 | `62c733ac8263e6413816cfb6d28e3b8a` | 2,982,420 |
| superseded ~~ v4.0.4 | `{P404}` | {P404B} |
| superseded ~~ v4.0.5 | `{P405}` | {P405B} |
| **current ~~ v4.1.0** | **`{PNEW}`** | **{PNEWB}** |

**v4.0.5 has no entry of its own in this file.** It shipped on 2026-09-13 ~~ the load-bearing hierarchy table regenerated from `DEP_GRAPH_DATA.links` and a third era of inert baked node counters stripped ~~ and the release surfaces were never revisited. Its prose is in `release_v4_0_5.json` in the wuld.ink repo. Its hash is added to the ladder above rather than reconstructed as a retrospective entry, which would be inventing a record for a session that is over.

### Changed

- **`combined.html`** (+112 B) ~~ four lines, six span-replacements. **The pin.**
- **`efilist_argument_library_v4_0_0.json`** (+112 B, `{CNEW}`) ~~ the same four lines' worth of text, plus the `version` field `4.0.0` {A} `4.1.0`. **The field names the content cut, not the release**: commit `e922e6c` restored it to `4.0.0` after the v4.0.1-v4.0.4 relabels walked it to `4.0.4` while the content stayed byte-identical, which made one content version wear five hashes and broke validation for every artifact pinning `6ee1f6f3`. v4.1.0 is the first genuine content cut since K219, so it is the first bump that rule licenses. **Filename stays frozen**, per convention. `generated` is untouched: it dates an authoring run, and no run happened.
- **`efilist_argument_library_v4_0_0.jsx`** (+112 B, `{JNEW}`) ~~ the same six spans.
- **`project_canon_v38_4.json`** ~~ MINOR; keyset held at 41; `invariants`, `schemas` and `hazard_map` asserted byte-identical by the builder, which is what would have made it MAJOR. v38_3 archived. `canon_version_marker` corrected from a drifted `v38.1`.
- **`adversarial_map_staging/`** ~~ the regen queue records the three as landed; the map artifact itself is **untouched**.
- **`README.md`, `libraries/index.html`** ~~ pin table, front-door badge, status prose, canon filename. Three of these were correcting v4.0.5, not stamping v4.1.0.
- **`tools/`** ~~ `sweep_v4_1_0.py`, `verify_v4_1_0.py`, `xsurface_v4_1_0.py`, `build_canon_v38_4.py`, `restamp_v4_1_0.py`.

### Controls

- **13 of 13 behaved.** A positive control on each tool, then base-md5, base-CR, line-anchor, changed-set, HELD-lost, GONE-survives, word-count, collateral-anchor and json-leaf-set against the sweep, and surface-disagreement against the cross-surface gate. The first collateral-anchor control aborted at the *line* gate and so proved section 1 rather than section 7; it was kept and a second built beside it that applies cleanly and is caught only by the anchor sweep. A control that cannot fail for its own reason proves nothing.
- **Anchor destruction is the receipt.** 90 of the map's 93 anchors hold against the post-cut corpus and exactly the three intended break. An anchor still matching after a subtractive regen would be proof the defect was still in the text.
- **Word counts stated in advance** and asserted on both sides: hashes cannot see a change in meaning that is internally consistent.
- **`objections-index.json` unchanged** ~~ `d034af153aafa08c6f57884a9e7426a1` / 41,800 B. The index projects `id`/`trigger`/`diagnosis`/`keywords` and this cut moved only `responses`, so the wuld.ink objection re-vendor is a no-op **by identity** ~~ proven by regenerating from the post-cut corpus, with the generator first reproducing the committed artifact as a positive control.
- **The objections digest moved** `{DOLD}` {A} `{DNEW}`. It is computed over `objections` and is independent of the `version` field ~~ the validator's own label-churn self-test sets `version` to `4.0.4` to prove that ~~ so the digest moved because the responses moved.
- **Line counts frozen.** All three surfaces keep their line count; every changed set is exactly the named loci, checked against `git show HEAD:<file>` and not against a copy on disk.

---

"""

for _k, _v in (("~~", EMD), ("{A}", "→"), ("{E}", ELL), ("{P404}", PIN_404),
               ("{P405}", PIN_405), ("{PNEW}", PIN_NEW), ("{P404B}", "{:,}".format(PIN_404_B)),
               ("{P405B}", "{:,}".format(PIN_405_B)), ("{PNEWB}", "{:,}".format(PIN_NEW_B)),
               ("{CNEW}", CORPUS_NEW), ("{JNEW}", JSX_NEW), ("{XSOLD}", XS_OLD),
               ("{XSNEW}", XS_NEW), ("{DOLD}", DIG_OLD), ("{DNEW}", DIG_NEW)):
    ENTRY = ENTRY.replace(_k, _v)
assert "~~" not in ENTRY and "{" not in ENTRY.replace("{:", ""), "placeholder survived the pass"

edit("CHANGELOG.md", [("## [v4.0.4] " + EMD + " 2026-09-12", ENTRY + "## [v4.0.4] " + EMD + " 2026-09-12")])

if fail:
    print()
    for f in fail: print("  ABORT " + f)
    sys.exit("\nRESTAMP FAILED (%d) -- drop may be incomplete\n" % len(fail))
print("\nRESTAMP GREEN.")
