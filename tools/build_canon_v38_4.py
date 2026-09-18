#!/usr/bin/env python3
"""build_canon_v38_4.py -- canon v38.3 -> v38.4, MINOR, for the K344 v4.1.0 pin move.

MINOR by the update_protocol: value-only edits plus additions inside an existing top-level
block. The keyset does not move (41 keys before and after) and `invariants`, `schemas` and
`hazard_map` are asserted byte-identical -- which is what would have made it MAJOR, so the
builder VERIFIES it rather than asserting it in prose.

Writes to k344_drop/project_canon_v38_4.json. Never mutates the tracked canon.
"""
import hashlib, io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "project_canon_v38_3.json")
DROP = os.path.join(ROOT, "k344_drop")
OUT  = os.path.join(DROP, "project_canon_v38_4.json")

BASE_MD5, BASE_BYTES = "05eabe951f751ff9e356dfef09994505", 288514
PRECUT_HEAD = "3e71546316285ef4fe3bd6d2da4ef1b5e4d6b50f"

PIN_OLD, PIN_OLD_B = "cee25a00b68ba036138d064c383d9a8b", 2982658
PIN_NEW, PIN_NEW_B = "72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770
CORPUS_OLD, CORPUS_OLD_B = "6ee1f6f31e0f012db0d58cae4f912fcb", 1333912
CORPUS_NEW, CORPUS_NEW_B = "04bf6482aa0374ee92a81c1d55ec41f8", 1334024
JSX_OLD, JSX_NEW = "b7dadfc39d988d643c408b3329ffcb54", "b196548b6eb39065842d62292acca89f"
DIG_OLD, DIG_NEW = "0218f73b7bfac7c9bcf7d352a5eab5cc", "2c5a083a31448dec0f1ce41e08ba5b04"
XSURF_OLD, XSURF_NEW = "a597fb18cac0b12434d63c4cfd23cfff", "6cd132ee5b8c7ca78ad0e095806f1c93"

raw = io.open(SRC, encoding="utf-8", newline="").read()
b = raw.encode("utf-8")
assert hashlib.md5(b).hexdigest() == BASE_MD5, "canon base md5 moved"
assert len(b) == BASE_BYTES, "canon base byte count moved"
c = json.loads(raw)
before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in c.items()}
KEYSET = sorted(c)

# ============================ the adversarial_map additions ============================
am = c["adversarial_map"]

am["v4_1_0_cut"] = {
  "landed": "K344 (2026-09-17, efilist commit atop %s). THE PIN MOVED: v4.0.5 -> v4.1.0. "
            "The commit sha resolves in the push output and is folded into the wuld ledger stratum." % PRECUT_HEAD,
  "ratified_by": "Josiah, 2026-09-17, on the library seat's v4_1_0_execution_order_v0_1.md (which audits the "
                 "map seat's v4_1_0_regen_spec_v0_1.md). Content ratified at WI-K334; the four rulings that "
                 "unblocked execution were taken at K344 and are recorded below.",
  "what": "The three PURE-SUBTRACTION entries of the nineteen-item v4.1.0 enrichment queue. Each removes a "
          "claim that is false or unsupported; none adds an argument. They went first because their "
          "correctness is judgeable without re-litigating any philosophy -- the question is whether the "
          "sentence is true, not whether the move is good.",
  "repairs": {
    "R1_happiness_is_choice_long": {
      "severity": "headline", "axis": "s", "spans": 1, "words": "555 -> 589 (+34)",
      "defect": "A heritability coefficient read as the fraction of ONE person's trait fixed at conception. "
                "The coefficient partitions variance BETWEEN people and says nothing of the kind. The corpus "
                "stated the misreading outright and built a slice-of-the-pie carve-up on top of it. The "
                "standard undergraduate correction, which is what made it the most exposed sentence in the "
                "corpus: a competent objector needed to be right about nothing else.",
      "form": "INTERPRETED, not R1-alt. Josiah's ruling, K344. `subtractive` classifies the CLAIM, not the "
              "word count: naming why a number fails to license an inference costs more words than making "
              "the inference did, so no version of this repair is word-neutral. R1-alt, the bare deletion, "
              "stays on the record in the spec as the literal reading of repair_shape.",
      "destroyed_anchor": "roughly half of your capacity for happiness was determined at conception"},
    "R2_just_edgy_long": {
      "severity": "minor", "axis": "s", "spans": 1, "words": "220 -> 220 (+0)",
      "defect": "An argument from silence offered as a credential, inside a rebuttal against arguments from "
                "authority. Reception is now DESCRIBED (more often categorized than answered) rather than "
                "ADJUDICATED (never refuted): the first is observable, the second was a claim about an "
                "entire literature nobody had surveyed. The lineage material survives on the best reading.",
      "destroyed_anchor": "has never been substantively refuted"},
    "R3_just_depressed": {
      "severity": "minor", "axis": "s", "spans": 4, "words": "long 979 -> 978 (-1); archetypeVariants.defender 347 -> 344 (-3)",
      "defect": "An unsourced quantitative premise doing architectural work -- the one-in-a-hundred / "
                "ninety-nine split organises the node's opening and its close -- inside the corpus's most "
                "epistemically self-aware rebuttal, which elsewhere refuses exactly this move. Nothing in "
                "the argument depended on the ratio being 1:99 rather than 1:20; it depended on genuine "
                "concern being the exception, which the corrected text says.",
      "FOURTH_SPAN": "THE SPEC SAID THREE SPANS AND THERE WERE FOUR. The spec's own scope note says a repair "
                     "that fixes the opening and leaves the close counting to ninety-nine produces a node "
                     "that contradicts itself. Its recurrence count was three because the search ran over "
                     "responses.long. The same unsourced ratio also stands at "
                     "responses.archetypeVariants.defender ('roughly one deployment in a hundred is genuine "
                     "worry') -- live shipped text, once per surface. Found at K344 by sweeping the DEFECT "
                     "across every locus of every node rather than the five named strings; ratified by "
                     "Josiah the same session and repaired with the other three, at the width of the "
                     "existing ruling and no wider.",
      "destroyed_anchor": "Roughly one deployment in a hundred is a person actually worried about you"}},

  "section_1_ruling_the_landed_entry_question": {
    "question": "The order's section 1, left deliberately open: does `coverage` mean every node was "
                "ADJUDICATED, or every node is currently PENDING? Each of the three nodes carried exactly "
                "one Phase E entry classed (b) whose verbatim anchor is cut from the sentence being "
                "repaired, and `status-enum` pins status to `mapped` as a hard check, so after the cut no "
                "status value exists that can say an anchor is historical.",
    "ruling": "ADJUDICATED -- and the design document settles it in one line rather than by argument: "
              "'every node gets >=1 entry -- a confident (a) or (d) is itself the routing datum.' 71 of the "
              "93 entries are (a) or (d) and neither is pending anything, so `coverage` could never have "
              "meant pending; the map would already have failed the check it passes. Josiah, K344.",
    "consequence_option_D": "FREEZE, DO NOT RE-PIN. The order inferred that `adjudicated` forces `coverage` "
              "to read canon's landed list, hence a validator change. That follows only if the map is ALSO "
              "re-pinned to the post-cut corpus, and re-pinning is the false move: `coverage: 82/82` is a "
              "claim about a (map, corpus) PAIR, bound by meta-corpus-pin. Advancing the pin under entries "
              "authored against the old text takes a receipt that named its referent and changes the "
              "referent underneath it -- ccclxii, one level out. So the map stays pinned where it is.",
    "options_rejected": {
      "A_landed_status_in_artifact": "Reverses canon's own invariant that downstream lifecycle states live "
              "in canon and NEVER in the artifact. MAJOR, and MAJOR in the direction canon forbids, on a "
              "code path with no landed data to test against.",
      "B_reanchor": "Incoherent: the entry would assert a defect while quoting text that no longer has it.",
      "C_remove_entries": "The order's own recommendation, and it showed why it fails: removing the three "
              "drops three corpus ids to zero entries and `coverage` hard-fails under --terminal, which "
              "--assembly implies. Making it work needs the validator to read canon, which couples the "
              "instrument to canon and lands the three landed anchors in the one place no gate checks."},
    "MEASURED_NOT_ARGUED": {
      "map_vs_the_corpus_it_names": "validator v0_2 --assembly: 21 checks, 0 violations, 0 advisories, PASS",
      "map_vs_the_post_cut_corpus": "FAIL, 5 violations -- anchor-rule 3, meta-corpus-pin 1, "
              "objections-digest 1. coverage PASSES in both, which is the proof that coverage only breaks "
              "if the ENTRIES are removed, exactly as the order predicted.",
      "so": "Freezing is the only path on which --assembly stays green. The order's section 5 abort "
            "condition is satisfied in the sense that matters -- the instrument is intact -- and NOT in the "
            "sense of a green run against the new corpus, which no option delivers. Said plainly rather "
            "than claimed cleanly."},
    "what_is_owed": "A SUCCESSOR MAP pinned to the post-cut corpus. 79 of 82 nodes inherit their "
              "adjudication unchanged; three re-adjudicate, because their text moved. Until it exists the "
              "repo has no map pinned to the LIVE corpus, and that is a real gap, named here so it cannot "
              "become the silent kind."},

  "locus_coverage_gap_FOUND_K344": {
    "finding": "The validator's LOCI enum is ('short','medium','long','diagnosis'). `archetypeVariants` is "
               "not in it, so target_locus cannot name it and anchor-rule cannot reach it. 16 of the 82 "
               "nodes carry archetype variants -- 10,072 words of LIVE SHIPPED corpus text that the "
               "Adversarial Map is structurally incapable of adjudicating. '82/82 nodes, 93 entries' covers "
               "none of it.",
    "shape": "ccclxi one level up: the written gate is silent about a whole CLASS of text, practice never "
             "went there, and nothing ever failed. Detection required sweeping the defect across every "
             "locus rather than checking any artifact -- the same method that turned up R3's fourth span, "
             "and in fact the same search.",
    "not_a_blocker_for_this_cut": "R3's fourth span is repaired; the gap is recorded. The successor map "
             "inherits it as its first problem, and the LOCI enum is the decision it opens: extend it, or "
             "state in the design why archetype variants are out of scope.",
    "also_logged_not_repaired": "happiness-is-choice#medium carries a milder cousin of R1's defect -- "
             "'40-50% of the variance ... attributable to genetic factors, heritable set-points that no "
             "amount of positive thinking can overcome'. That is the set-point slide, not the "
             "conception-fraction misreading; R1's anchor is not there and R1 does not falsify it. Judging "
             "its severity is a fresh adjudication of a locus the map never mapped, which is map-seat work "
             "under locus_discipline, not a build call. Queued as a v4.1.0 item. Josiah's ruling, K344."},

  "cross_surface_gate_BUILT_K344": {
    "why": "The order is right that NO GATE ANYWHERE cross-checked corpus text against the flagship. There "
           "is no build step: combined.html is a hand-assembled superset carrying REBUTTAL_STRENGTH, which "
           "the JSX does not, and nothing regenerates any surface from any other. A missed surface shipped "
           "a corpus and a served page that disagree with nothing to say so.",
    "tool": "tools/xsurface_v4_1_0.py -- string-aware bracket-balance extraction of the `const OBJECTIONS = "
            "[...]` literal from combined.html and the JSX, json.loads, and a canonical-serialization md5 "
            "against the corpus file's objections. One hash, three surfaces. The K330 data-literal "
            "extraction method generalised from 'did the literal move' to 'do the surfaces agree'.",
    "measured": "all three surfaces agree at %s before the cut and at %s after, and the SAME four leaves "
                "moved on every surface." % (XSURF_OLD, XSURF_NEW)},

  "method": "tools/sweep_v4_1_0.py (line-indexed, per-line anchor assertion, aborts before any write and "
            "never mutates the tracked originals -- it emits to a drop, so the operator block's base guard "
            "still has an untouched base to guard), tools/verify_v4_1_0.py (reads the base from GIT BLOBS, "
            "a different instrument from the sweep's own changed-set check, and asserts the changed set is "
            "EXACTLY the named loci), tools/xsurface_v4_1_0.py. Shaped on the v4.0.1 toolkit, which had "
            "said 'not sed -i, not a global regex' and 'the greps prove the named strings moved, they do "
            "NOT prove that nothing ELSE moved' before either had a ledger class.",
  "controls": "13 of 13 behaved: a positive control on each tool, then base-md5, base-CR, line-anchor, "
              "changed-set, HELD-lost, GONE-survives, word-count, collateral-anchor and json-leaf-set "
              "against the sweep, and surface-disagreement against the cross-surface gate. The first "
              "collateral-anchor control aborted at the LINE gate and so proved section 1, not section 7; "
              "it was kept and a second built beside it that applies cleanly and is caught only by the "
              "anchor sweep. A control that cannot fail for its own reason is C1 in a lab coat.",
  "anchor_destruction_is_the_receipt": "90 of the map's 93 anchors hold against the post-cut corpus and "
              "exactly the three intended break. An anchor that still matched after a subtractive regen "
              "would be proof the defect was still in the text.",
  "pins": {"flagship_old": "%s / %d (v4.0.5)" % (PIN_OLD, PIN_OLD_B),
           "flagship_new": "%s / %d (v4.1.0)" % (PIN_NEW, PIN_NEW_B),
           "corpus_old": "%s / %d" % (CORPUS_OLD, CORPUS_OLD_B),
           "corpus_new": "%s / %d" % (CORPUS_NEW, CORPUS_NEW_B),
           "jsx": "%s -> %s" % (JSX_OLD, JSX_NEW),
           "objections_digest": "%s -> %s" % (DIG_OLD, DIG_NEW),
           "all_three_surfaces": "+112 bytes each, and the six span deltas sum to +112",
           "objections_index": "d034af153aafa08c6f57884a9e7426a1 UNCHANGED -- the re-vendor is a no-op BY "
                               "IDENTITY, proven by regenerating from the post-cut corpus, with the "
                               "generator first reproducing the committed artifact as a positive control. "
                               "The index projects id/trigger/diagnosis/keywords; this cut moved only "
                               "responses.",
           "corpus_version_field": "4.0.0 -> 4.1.0, AND IT WAS NOT STALE. The field names the CONTENT "
                               "CUT, not the release. Commit e922e6c had restored it to 4.0.0 after the "
                               "v4.0.1-v4.0.4 relabels walked it to 4.0.4 while the content stayed "
                               "byte-identical, which made one content version wear five hashes and broke "
                               "validation for every artifact pinning 6ee1f6f3. v4.1.0 is the first genuine "
                               "content cut since K219, so it is the first bump that rule licenses -- and "
                               "the only reason to touch the field at all. This session first read it as "
                               "five pin moves of drift; `git log` corrected that before anything shipped. "
                               "The objections digest is independent of the field -- it is computed over "
                               "`objections`, and the validator's own label-churn self-test sets version to "
                               "4.0.4 to prove it -- so the digest moved because the RESPONSES moved. "
                               "`generated` is NOT touched: it dates an authoring run, and no run "
                               "happened."}}

am["terminal_artifact_pin"]["corpus_superseded_K344"] = (
  "THE ARTIFACT IS FROZEN, NOT STALE. adversarial_map_v1_0.json stays byte-identical at "
  "c4989e98b042e2f787a82df3f11ecdad / 186,406 and stays pinned to corpus %s, which the v4.1.0 cut "
  "superseded. Against THAT corpus it still validates under --assembly at 21 checks, 0 violations, 0 "
  "advisories -- permanently, reproducibly, and recoverably: the pre-cut corpus is `git show %s:"
  "efilist_argument_library_v4_0_0.json`. A map pinned to a NAMED corpus can only age, and the reader can "
  "see the gap; a map re-pinned under entries authored against the old text cannot ever be falsified. "
  "THREE ENTRIES ARE LANDED: happiness-is-choice#long, just-edgy#long and just-depressed#long, all class "
  "(b), landed at v4.1.0 -- their pre-cut anchors are recorded verbatim in v4_1_0_cut.repairs, which is "
  "where the lifecycle already lives per status_lifecycle. A successor map pinned to the post-cut corpus "
  "is OWED: 79 nodes inherit, three re-adjudicate." % (CORPUS_OLD, PRECUT_HEAD))

am["next"] = ("The SUCCESSOR MAP, pinned to the post-cut corpus %s: 79 of 82 nodes inherit their "
  "adjudication unchanged, three re-adjudicate because their text moved, and the LOCI enum decision from "
  "locus_coverage_gap_FOUND_K344 is taken there or explicitly deferred. Then the remaining sixteen v4.1.0 "
  "enrichment items -- five structural, ten additive, with selfish-lazy#long travelling with the intake "
  "cut instead -- plus happiness-is-choice#medium, queued at K344. Then the v5.0.0 intake cut for the "
  "single (c), diagnosis-not-refutation, still deliberately deferred to a session that begins fresh." % CORPUS_NEW)

# ============================ canon-meta ==============================================
c["canon_version"] = "38.4"
c["last_updated_by_session"] = "K344_v4_1_0_pin_move_cut"
# canon_version_marker had drifted to v38.1 across two bumps -- corrected here, and the
# correction is named rather than performed quietly.
assert c["canon_version_marker"] == "v38.1", "marker not at the drifted value this build expects"
c["canon_version_marker"] = "v38.4"

# The bump record goes in keyset_delta_ledger, following the v28_2_ledger_sync_note pattern
# for a keyset-unchanged MINOR. NOT canon_version_history_tail.preserved_entries: its last
# entry is v37.40 -> v38.0 and v38.1, v38.2 and v38.3 were never appended there, so adding a
# lone v38.4 would imply a continuity the list does not have. The gap is named, not filled --
# writing three retrospective entries would be inventing records for sessions I was not in.
assert c["last_updated"] == "2026-09-17", "last_updated is not today; re-derive the operator-local date"
c["keyset_delta_ledger"]["v38_4_note"] = (
  "v38.3 -> v38.4 MINOR (K344_v4_1_0_pin_move_cut, 2026-09-17): keyset UNCHANGED at %d (no top-level key "
  "added or removed; value-only edits to canon-meta, session_log_recent, next_recommended_session and "
  "additions INSIDE adversarial_map). invariants, schemas and hazard_map asserted byte-identical by the "
  "builder, which is what would have made this MAJOR. The v4.1.0 three-repair cut; pin v4.0.5 -> v4.1.0, "
  "%s / %d. The adversarial map is FROZEN at its own corpus pin rather than advanced. canon_version_marker "
  "corrected from a drifted v38.1 -- it had not moved since v38.1 while canon_version reached 38.3. NOTE: "
  "canon_version_history_tail.preserved_entries ends at v37.40 -> v38.0; the v38.1, v38.2 and v38.3 bumps "
  "were never recorded there and are not reconstructed here."
  % (len(KEYSET), PIN_NEW, PIN_NEW_B))

c["session_log_recent"].append(
  "K344_v4_1_0_pin_move_cut (2026-09-17, wuld.ink Cowork; the deliberate isolated pin-move session the "
  "shipping-fork disposition requires) [MINOR v38.3->v38.4]: THE v4.1.0 CUT LANDED AND THE PIN MOVED, "
  "%s/%d -> %s/%d. Three surfaces edited in lockstep with no build step between them -- corpus, JSX and "
  "the flagship -- 6 spans, 18 span-replacements, 12 text loci and one version locus, every locus "
  "line-indexed with a per-line anchor assertion and every surface verified against its GIT BLOB for a "
  "changed set of EXACTLY the named lines. THE ORDER'S SECTION 1 WAS RULED `ADJUDICATED`, and the map "
  "FREEZES rather than re-pins: coverage: 82/82 is a claim about a (map, corpus) pair, so advancing the "
  "pin under entries authored against the old text would change a receipt's referent while keeping its "
  "claim. Measured both ways -- the map is PASS/0/0 under --assembly against the corpus it names and FAIL "
  "with 5 violations against the post-cut one, while `coverage` passes in BOTH, which is the proof that it "
  "only breaks if the entries are removed. THE SPEC SAID THREE SPANS AND THERE WERE FOUR: the same "
  "unsourced one-in-a-hundred ratio also stood at just-depressed#archetypeVariants.defender, found by "
  "sweeping the DEFECT across every locus instead of the five named strings, and ratified and repaired the "
  "same session. The same sweep found that `archetypeVariants` is not in the validator's LOCI enum at all "
  "-- 16 of 82 nodes, 10,072 words of live shipped text the map is structurally unable to adjudicate. "
  "Built the corpus-vs-flagship gate the order says exists nowhere (tools/xsurface_v4_1_0.py): all three "
  "surfaces agree at %s before and %s after, same four leaves moved on each. 13 of 13 controls behaved, "
  "one of them replacing an earlier control that aborted at the wrong gate and so proved the wrong "
  "section. Also corrected, and named as corrections rather than passed off as restamp: README, the "
  "libraries front door and the CHANGELOG had all said v4.0.4 for four days while /combined served "
  "v4.0.5; the corpus `version` field had read 4.0.0 through five pin moves; canon_version_marker had "
  "drifted to v38.1. The objection re-vendor is a no-op BY IDENTITY, proven by regeneration with the "
  "generator reproducing the committed artifact first as a positive control."
  % (PIN_OLD, PIN_OLD_B, PIN_NEW, PIN_NEW_B, XSURF_OLD, XSURF_NEW))

c["next_recommended_session"] = {
  "action": "THE SUCCESSOR ADVERSARIAL MAP, pinned to the post-cut corpus %s / %d. 79 of 82 nodes inherit "
            "their adjudication unchanged; happiness-is-choice, just-edgy and just-depressed re-adjudicate "
            "because their text moved. adversarial_map_v1_0.json is FROZEN and is not the input to edit -- "
            "it is the terminal adjudication of corpus %s and keeps validating against it." % (CORPUS_NEW, CORPUS_NEW_B, CORPUS_OLD),
  "first_decision": "The LOCI enum. `archetypeVariants` is unreachable by target_locus, so 10,072 words "
            "across 16 nodes have never been adjudicated. Extend the enum, or state in the design why "
            "archetype variants are out of scope. Do not let it stay silent a third arc.",
  "then": "The remaining sixteen v4.1.0 enrichment items (five structural, ten additive), plus "
            "happiness-is-choice#medium queued at K344.",
  "not_this_session": "diagnosis-not-refutation, the single (c), and the v5.0.0 intake cut. Unchanged from "
            "v38.3: it is an objection to the corpus's own method and the most contestable item the "
            "program produced; it belongs to a session that begins fresh, not one that ends tired. "
            "gods-plan and western-philosophy stay HELD for it.",
  "gates": ["the v4.1.0 line is now OPEN, not proposed -- three of nineteen items have landed",
            "a successor map must not be authored against the frozen v1_0's corpus pin"]}

# ============================ change isolation ========================================
after = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in c.items()}
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session",
           "keyset_delta_ledger", "session_log_recent", "next_recommended_session",
           "adversarial_map"}
assert sorted(c) == KEYSET, "KEYSET MOVED: %r" % (set(c) ^ set(KEYSET))
moved = {k for k in KEYSET if before[k] != after[k]}
assert moved == TOUCHED, "ISOLATION BROKEN: moved %r, named %r" % (sorted(moved), sorted(TOUCHED))
for k in ("invariants", "schemas", "hazard_map"):
    assert before[k] == after[k], "%s MOVED -- this would be a MAJOR, not a MINOR" % k

os.makedirs(DROP, exist_ok=True)
blob = json.dumps(c, indent=2, ensure_ascii=False) + "\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(blob)
ob = blob.encode("utf-8")
print("canon v38.3 -> v38.4  MINOR")
print("  keyset          %d -> %d (held)" % (len(KEYSET), len(c)))
print("  moved keys      %s" % ", ".join(sorted(moved)))
print("  invariants/schemas/hazard_map  byte-identical -- MINOR, verified not asserted")
print("  out             %s" % os.path.relpath(OUT, ROOT))
print("  new_md5         %s" % hashlib.md5(ob).hexdigest())
print("  new_bytes       %d" % len(ob))
