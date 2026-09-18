#!/usr/bin/env python3
"""project_canon_v38_15.json -- MINOR. Direction two LANDED: the map's own reader-facing surface.

ccclxiv FIRST: v38_14 is round-tripped at the serialization this file emits BEFORE anything is
derived.

MINOR is asserted, not claimed: the top-level keyset is held at 41 and `invariants`, `schemas`
and `hazard_map` are required byte-identical, which is what would force MAJOR.

`last_updated` is NOT required to move -- K352 ran on the same operator-local day.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K353_REPO") or os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_14.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_15.json")
SRC_MD5 = "0eb13633ab88087d5f882f94bb6edfc9"
DUMP = dict(indent=2, ensure_ascii=False)


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_14.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_14 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False)
              for k in ("invariants", "schemas", "hazard_map")}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_keys_before = set(am)

    am["wing_LANDED_K353"] = {
        "the_fork_taken": (
            "THE AUX WING, not the /combined graft. shipping_fork_disposition_verbatim makes an "
            "own-surface render 'an ordinary no-pin aux-wing fold runnable any session'; only a "
            "graft is a stance-layer change needing R4, which is still open. The graft buys "
            "nothing the wing does not have, because K352 built the inbound grammar precisely so "
            "an off-flagship surface could land a reader at the locus -- and that grammar had NO "
            "CONSUMER until this fold. Put to Josiah with that recommendation before anything "
            "was built, and built on it."),
        "surface": "adversarial/index.html -> library.wuld.ink/adversarial/ . NO PIN.",
        "what_ships": (
            "The 21 pure-(d) nodes, 22 entries: 20 at #long, 1 at #diagnosis "
            "(natural-reproduce), 1 at #note (care-ethics). Grouped BY REGISTERED BEDROCK rather "
            "than by node, because the concentration is the argument and grouping by node hides "
            "it. Zero new philosophical text: the objection wording, the sentence each "
            "continuation attacks, the continuation, the adjudication and the terminus routing "
            "are all verbatim from the corpus, the assembly or the register. The only authored "
            "reader-facing prose is the frame, the labels and the colophon."),
        "generator": (
            "adversarial_map_staging/render_wing_v0_1.py -- repo-relative, reproduces byte-for-"
            "byte from its committed location and under two forced PYTHONHASHSEED values. Gates "
            "all four inputs on md5 AND byte count plus the objections digest before rendering, "
            "and RE-RUNS THE ANCHOR RULE AT SHIP TIME against the live corpus: 22/22 verbatim."),
        "controls": (
            "adversarial_map_staging/controls_wing_v0_1.py -> wing_control_v0_1.json, 54 checks, "
            "0 failed, every gate carrying a failing control. The link-grammar gate does not "
            "retype the regex: it EXTRACTS it from combined.html at run time, so a future pin "
            "that narrows the grammar breaks this battery rather than silently shipping links "
            "the flagship no longer accepts."),
        "functional_gate": (
            "tools/k353_wing_functional_gate.py -> 16 checks, 0 failed, in real Chromium over a "
            "local server mirroring the Pages routing. All 22 emitted links load the flagship "
            "with the target card open; the 21 @long links land at responseLevel 'long'; the "
            "suffix-stripped forms run as the NULL and stay at 'medium', so the suffix is what "
            "does the work, measured rather than asserted. Every probe carries a boot witness "
            "and a failing control proves the witness can fire (ccclxxvii). It runs in the "
            "Cowork container, which has Chromium; the operator VM does not, so like "
            "k352_functional_gate.py it does not reproduce from its committed location."),
        "front_door": (
            "libraries/index.html, +239 bytes / -4 lines, by tools/frontdoor_K353.py -- line-"
            "indexed with per-line anchor assertion, base read from the GIT BLOB so it stays "
            "reproducible after it lands (the amend_phaseG defect K351 registered, repaired the "
            "same way)."),
        "NOT_done_and_deliberately": (
            "The five wing surfaces' own wing-switcher navs were NOT swept. The new surface links "
            "back to all of them; adding it to five combined.html files multiplies risk for a "
            "navigation convenience. Carried."),
    }

    am["front_door_strength_language_removed_K353"] = {
        "finding": (
            "libraries/index.html's 'Being built' blurb described the map as 'the strongest "
            "continuation a maximally competent opponent would deploy'. That was written when "
            "NOTHING shipped. The moment the front door links a reader-facing (d)-only surface, "
            "that sentence becomes the label on it -- and class_asymmetry_ruling_K350 says in "
            "terms that the licence survives only under a TERMINUS label, because under a "
            "strength label a (d) makes exactly the overreaching claim an (a) makes and R1 bites "
            "it just as hard."),
        "why_it_was_invisible": (
            "It sat in a place nobody would look for a label: a coming-soon blurb that predated "
            "the ruling by a session. A label lives wherever a reader meets the claim, which is "
            "not only on the surface that makes it."),
        "disposition": (
            "The blurb is REMOVED rather than relinked, and its replacement card claims "
            "disposition rather than force: 'one disposition of four'. A gate on the rendered "
            "front door refuses any surviving `strongest ... continuation|objection`."),
    }

    am["terminus_label_pin_K353"] = {
        "ruling": (
            "The label is part of class_asymmetry_ruling_K350, not presentation, so it is pinned "
            "here rather than left in a template. Proposed by this seat and built on; Josiah's "
            "to redline, and a redline is one sweep per string because each is bound once in "
            "render_wing_v0_1.py."),
        "strings": {
            "page_title": "Where the lines terminate",
            "section_label": "WHERE THIS LINE TERMINATES",
            "the_mapped_move": "THE CONTINUATION",
            "the_residue": "TERMINUS",
            "the_grounds": "WHY NO REWRITE CLOSES IT",
            "the_anchor": "AGAINST",
        },
        "and_the_frame_states_the_disclaimer_positively": (
            "The page says why only this disposition is on it: whether a continuation was "
            "authored at full force or at the most repairable reading of our text is R1, still "
            "open, so a card saying WE ANSWER THIS would claim more than the map has "
            "established, while a card saying THIS LINE TERMINATES HERE would not. Stating R1 as "
            "the reason is what makes the restraint legible instead of merely observed."),
    }

    am["bedrock_normalizer_correction_K353"] = {
        "corrected": (
            "The K353 handoff and interconnection_design_v0_2 both counted '15 distinct "
            "bedrocks' over the ship set. That is a count of the free-text "
            "routing.residue.bedrock_name STRINGS -- the exact normalizer error the same "
            "design's own section 5 had flagged one section earlier about terminus_routing."),
        "measured": (
            "Under the register's HR-id namespace, which is the namespace, the 22 entries land "
            "on 9 of the 15 REGISTERED bedrocks: HR-03 x8, HR-05 x5, HR-02 x2, HR-04 x2, and "
            "HR-01 / HR-11 / HR-12 / HR-13 / HR-15 x1 each. The coincidence of two fifteens is "
            "what made it survive: 15 distinct strings, and 15 bedrocks in the register."),
        "consequence_for_the_claim": (
            "'A third of the ship set lands on two bedrocks' does not hold under either "
            "normalizer. Under the register it is HR-03 + HR-05 = 13 of 22 entries, 59 percent, "
            "which is a stronger claim than the one being corrected. The surface groups by the "
            "registered bedrock and a control asserts the two normalizers disagree, so the "
            "choice is proved non-vacuous rather than assumed."),
        "and_the_ship_set_count_is_re_confirmed": (
            "21 nodes / 22 entries, re-derived here against adversarial_map_v1_3.json rather "
            "than carried. class_asymmetry_ruling_K350's '20 pure-(d) nodes, 20 entries' and "
            "interconnection_design_v0_2 section 3's identical figure were both true when "
            "written and are left alone (ccclv); K351's fold made care-ethics pure-(d)."),
    }

    am["note_locus_link_form_instance_of_ccclxxii_K353"] = {
        "the_bug": (
            "The first cut of render_wing_v0_1.link_for handed the `note` locus the BARE anchor, "
            "because `note` is not in the grammar and the obvious fallthrough is the bare form. "
            "The bare form is exactly what fails there: the note DIV is emitted on "
            "`obj.note && responseLevel === 'long'` (combined.html L10584), so a bare link "
            "leaving a reader at the boot default renders no note element and no [NOTE] control "
            "-- the card would open with NOTHING of what the entry attacks anywhere on it."),
        "family": (
            "ccclxxii, and a clean instance of it: whether shipped text reaches a reader is a "
            "fact about a render site's CONDITIONS, not about the locus's name. The fix is "
            "@long, the deepest form the grammar offers and the one the note depends on, and "
            "the surface states the remaining click rather than papering over it."),
        "found_by": "controls_wing_v0_1.py, not by reading. The gate that caught it was written "
                    "before the link forms were reviewed.",
        "the_caveat_is_TRUE_and_was_measured": (
            "care-ethics is confidence:strong with a note, so its [NOTE] control IS emitted at "
            "long -- asserted in a real browser, scoped by the toggle's own onclick binding. "
            "And the surface it links into carries K349's finding as live data: 9 confidence "
            "notes render at `long`, 7 carry a reachable control, and solipsism -- itself in "
            "this ship set -- is one of the two whose note no reader can open."),
    }

    am["ccclxxix_hazard_K353"] = {
        "hazard": (
            "A CHECK THAT LOCATES ITS SUBJECT BY POSITION OR BY NAME-SHAPE, RATHER THAN BY A "
            "BINDING THE ARTIFACT ITSELF DECLARES, IS A CLAIM ABOUT LAYOUT AND NOT ABOUT THE "
            "SUBJECT -- and it fails plausibly, in whichever direction the layout happens to "
            "give."),
        "three_instances_in_one_session_in_three_substrates": [
            "JSON: a gate read a TOP-LEVEL `archetypeVariants` key, which no objection has -- "
            "they live at responses.archetypeVariants. It returned a reassuring zero for the "
            "wrong reason, and only its own non-vacuity control convicted it. The validator "
            "PUBLISHES node_variant_slots; reimplementing the path is what broke it.",
            "HTML source: a scan for `prefers-color-scheme` matched the source COMMENT that "
            "explains why the branch is absent. The marker, not the defect -- the third firing "
            "of that family in this arc.",
            "DOM: `.note-toggle` scoped by containment (`#obj-care-ethics .note-toggle`) is "
            "EMPTY for every node, because the expanded body lives in a sibling subtree "
            "(#results > .detail-panel) rather than inside the card element; and the same query "
            "UNSCOPED answers 'does any card anywhere have a note control', which at `long` is "
            "seven. Two cuts, wrong in opposite directions, both reported as facts about one "
            "node.",
        ],
        "counter_discipline": (
            "Locate by a binding the artifact declares: the module's published accessor, the "
            "CSS rule rather than the token naming it, the element's own onclick naming its "
            "node. And carry a control proving the locator is NOT VACUOUS -- in both directions, "
            "because a locator that can never match and one that always matches are both silent."),
        "neighbours": (
            "WI-K343's standing lesson is about REDUNDANCY -- a check restating what a stronger "
            "check proves is where false alarms accumulate. This is about the LOCATOR, and it "
            "bites a check that is not redundant at all. ccclviii is its parent: the apparatus "
            "is the likeliest explanation of an alarming reading, and equally of a reassuring "
            "one."),
        "and_the_arithmetic": (
            "Four gates failed in this session. ONE was the artifact -- the note link form, a "
            "real bug a gate caught before it shipped. THREE were gates wrong about their own "
            "subject, and all three are this numeral. The strong gates -- the input pin, the "
            "ship-time anchor rule, the byte reproduction -- were green from their first run."),
    }

    am["next"] = {
        "first": (
            "R1 with the library seat. It is now the binding constraint on everything the map "
            "can show: it releases the (a) surface, which is 69 of 138 entries against the 22 "
            "that just shipped. Then R2 for the (b) surface. R4, the /combined graft, is Josiah "
            "plus the library seat and nothing downstream waits on it -- the wing is live "
            "without it."),
        "second": (
            "UPSTREAM AUTHORING, and it is still the honest move. The map has produced 29 (b) "
            "items and the programme has repaired three sentences. Cowork cannot close that "
            "gap: a repair is a pin move and stance-bearing content is Josiah's with the "
            "library seat. The queue: the sixteen v4.1.0 enrichment items, "
            "happiness-is-choice#medium, the just-depressed depressive-realism contradiction "
            "(an AGGRAVATION per design 11.1 -- repair at the NODE), care-ethics#note's "
            "unrouted remainder (ccclxxvi), and flow-states, whole or not at all."),
        "also_open": (
            "The [NOTE] confidence coupling and the `confidence` regen item, both flagship-side "
            "and therefore pin-move work, and they should ride together -- and the wing has now "
            "made one of them visible to readers, since solipsism is IN the ship set and its "
            "own note is one of the two no reader can open. The regen queue still derives from "
            "the A-E fragments only: 10 adjudicated (b) entries from R, F and G are unqueued. "
            "The five wings' navs do not yet route to /adversarial/."),
        "explicitly_NOT_recommended": (
            "Flipping responseLevel's default to `long`. Held at K352 and held here; the wing "
            "needs no such flip, because every link it emits carries its own depth."),
    }

    assert set(am) - am_keys_before == {
        "wing_LANDED_K353", "front_door_strength_language_removed_K353",
        "terminus_label_pin_K353", "bedrock_normalizer_correction_K353",
        "note_locus_link_form_instance_of_ccclxxii_K353", "ccclxxix_hazard_K353"}, \
        "adversarial_map gained keys other than the six named"
    assert am_keys_before - set(am) == set(), "adversarial_map lost a key"

    d["canon_version"] = "38.15"
    d["canon_version_marker"] = "v38.15"
    d["last_updated_by_session"] = "K353_direction_two"
    d["keyset_delta_ledger"]["v38_15_K353"] = (
        "MINOR. Six adversarial_map subkey additions (wing_LANDED_K353, "
        "front_door_strength_language_removed_K353, terminus_label_pin_K353, "
        "bedrock_normalizer_correction_K353, note_locus_link_form_instance_of_ccclxxii_K353, "
        "ccclxxix_hazard_K353) and a replacement of adversarial_map.next. One "
        "keyset_delta_ledger addition; a replacement of next_recommended_session; one "
        "session_log_recent append. NO PIN: combined.html "
        "f095c0ce0e5a1d796d57fa5a5dd62f7d / 2,985,989 (v4.1.1) HELD, corpus and jsx HELD, no "
        "map or register artifact touched. Two site surfaces move and both are NO-PIN "
        "auto-deploying: adversarial/index.html (new) and libraries/index.html. invariants, "
        "schemas and hazard_map asserted byte-identical.")
    d["next_recommended_session"] = {
        "session": "R1 with the library seat, then R2.",
        "why": ("R1 is now the binding constraint on everything the map can show to a reader. "
                "It releases the (a) surface -- 69 of 138 entries against the 22 that just "
                "shipped -- and until it is ruled no (a) card can claim `we answer this` without "
                "claiming more than the map has established. R2 then releases (b)."),
        "scope": ("A ruling, not a build. If a build session is wanted instead, the honest one "
                  "is upstream authoring: 29 (b) items produced against three sentences "
                  "repaired, and Cowork cannot close that gap because a repair is a pin move."),
        "do_not": ("Ship (a) or (b) cards before their ruling. Use a strength label anywhere a "
                   "reader meets a (d) claim -- including on a front door or an index. Assume a "
                   "count taken over free text; the register is the namespace."),
    }
    d["session_log_recent"].append(
        "K353_direction_two (2026-09-18): DIRECTION TWO LANDED -- the Adversarial Map's own "
        "reader-facing surface at library.wuld.ink/adversarial/ , the first reader-facing map "
        "content in the programme's history. NO PIN: combined.html "
        "f095c0ce0e5a1d796d57fa5a5dd62f7d HELD, corpus, jsx and every map and register artifact "
        "untouched. THE FORK: the aux wing, per shipping_fork_disposition_verbatim -- runnable "
        "any session, no R4 -- and it is the first CONSUMER of the inbound anchor grammar K352 "
        "built. 21 pure-(d) nodes / 22 entries, grouped by REGISTERED bedrock rather than by "
        "node, under a TERMINUS label pinned in canon. Zero new philosophical text: objection "
        "wording, attacked sentence, continuation, adjudication and routing all verbatim. Gates: "
        "54 static controls, 16 functional checks in real Chromium with the suffix-stripped "
        "links run as the NULL and a boot witness on every probe, and byte reproduction under "
        "two forced PYTHONHASHSEED values from the generator's committed location. FOUR GATES "
        "FAILED AND ONLY ONE WAS THE ARTIFACT: the `note` locus was linked bare, which renders "
        "no note at all (ccclxxii); the other three were gates locating their subject by layout "
        "rather than by a declared binding, registered as ccclxxix. Corrected by measurement: "
        "the ship set lands on 9 REGISTERED bedrocks, not the 15 free-text strings the handoff "
        "counted, and HR-03 + HR-05 take 13 of 22. Also removed: the front door's own "
        "pre-ruling STRENGTH description of the map, which would have become the label on the "
        "surface the moment it was linked.")
    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before, "top-level keyset moved -- that would force MAJOR"
    assert len(keys_before) == 41, "keyset is %d, expected 41" % len(keys_before)
    for k in ("invariants", "schemas", "hazard_map"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], \
            "%s moved -- that would force MAJOR" % k
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_15.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset %d held; invariants/schemas/hazard_map byte-identical" % len(keys_before))
    print("  adversarial_map %d -> %d keys" % (len(am_keys_before), len(am)))


if __name__ == "__main__":
    main()
