#!/usr/bin/env python3
"""project_canon_v38_16.json -- MINOR. The note-and-confidence repair, landed as the v4.1.2 pin.

ccclxiv FIRST: v38_15 is round-tripped at the serialization this file emits BEFORE anything is
derived.

MINOR is asserted, not claimed: the top-level keyset is held at 41 and `invariants`, `schemas`
and `hazard_map` are required byte-identical, which is what would force MAJOR.

`last_updated` is NOT required to move -- K353 ran on the same operator-local day.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K354_REPO") or os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_15.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_16.json")
SRC_MD5 = "878bca22bbdeb14bfba28163d9d7456c"
DUMP = dict(indent=2, ensure_ascii=False)

PIN_OLD = "f095c0ce0e5a1d796d57fa5a5dd62f7d / 2985989 (v4.1.1)"
PIN_NEW = "006aa9833f7a8b103ad27a289ab22fa9 / 2987411 (v4.1.2)"


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_15.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_15 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False)
              for k in ("invariants", "schemas", "hazard_map")}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_keys_before = set(am)

    # ---------------------------------------------------------------- the repair
    am["note_confidence_repair_LANDED_K354"] = {
        "what_landed": (
            "The [NOTE] control is LIFTED OUT of `if (conf !== 'full')` so its condition equals "
            "its container's. 9 note containers, 9 controls. This is the repair "
            "note_confidence_coupling_QUEUED_K352 specified, executed verbatim: the container "
            "was always right and was not touched."),
        "why_this_session_rather_than_a_carry": (
            "K353 turned an internal defect into a live one. solipsism is IN the wing's 21-node "
            "ship set at library.wuld.ink/adversarial/ , and solipsism was one of the two nodes "
            "whose confidence note no reader could open. The wing points readers at that card."),
        "measured_again_this_session_not_recalled": {
            "notes": "9, 544 words",
            "unreachable_before": ("violence-as-reductio 106w (ungraded) and solipsism 89w "
                                   "(confidence:full) -- 195 words, 35.8% of the layer, and the "
                                   "two longest"),
            "confidence_distribution": {"absent": 64, "full": 11, "strong": 6, "provisional": 1},
        },
        "proved_end_to_end_not_by_presence": (
            "The functional gate CLICKS solipsism's control and requires the note to become "
            "visible. An affordance that exists and does nothing is the defect one level up."),
        "pin": {"old": PIN_OLD, "new": PIN_NEW},
        "the_mechanical_proof_that_no_data_moved": (
            "tools/xsurface_v4_1_0.py reads IDENTICALLY before and after at "
            "6cd132ee5b8c7ca78ad0e095806f1c93, asserted at open and at close. The corpus JSON "
            "04bf6482aa0374ee92a81c1d55ec41f8 and the JSX b196548b6eb39065842d62292acca89f are "
            "asserted UNMOVED git-to-git, and the corpus `version` field stays 4.1.0 because it "
            "names the CONTENT CUT. No map or register artifact was opened for writing."),
        "tools": {
            "cut": "tools/note_confidence_K354.py -- line-indexed, per-line anchor assertion",
            "verify": ("tools/verify_K354.py -- RECONSTRUCTION: base segments from the GIT BLOB "
                       "plus the declared blocks, byte-compared against the candidate, so the "
                       "changed set is proved to be EXACTLY the declared loci rather than "
                       "merely reported"),
            "one_binding": ("tools/k354_cut_pins.json -- the cut declares every constant once "
                            "and the verifier RECOMPUTES against it; no hash is typed twice "
                            "(ccclxii)"),
        },
        "the_control_markup_is_the_base_s_own": (
            "The [NOTE] button's markup is EXTRACTED from the base's own line 10565 and "
            "re-emitted byte-for-byte rather than retyped, and that is asserted. This repairs "
            "the CONDITION, not the control."),
    }

    # ---------------------------------------------------------------- the render ruling
    am["confidence_render_ruling_K354"] = {
        "authority": (
            "The K354 handoff reserved this to Josiah as register-sensitive. He DELEGATED it to "
            "this seat -- 'continue with your recommendations on all of the above' -- before the "
            "recommendations had been listed, so they were stated in full, in the conversation, "
            "with the note that nothing was irreversible until he pasted a block. Recorded as a "
            "delegation with the recommendation on the record, not as his ruling."),
        "full_renders": {
            "ruling": "YES. `full` renders the literal FULL, as strong and provisional do.",
            "the_defect_is_sharper_than_the_handoff_stated": (
                "The code read `const conf = obj.confidence || 'full'`, so the 64 NEVER-GRADED "
                "objections were silently upgraded to the TOP grade, and the 11 affirmatively "
                "graded ones were indistinguishable from them. That default is DELETED. The "
                "badge now reads obj.confidence directly: 18 cards carry a grade, 64 carry "
                "none, and the absence of a badge means UNGRADED, which is true."),
            "it_authors_nothing": ("This displays a corpus field the artifact was suppressing. "
                                   "An unknown value still renders nothing, as before."),
        },
        "provisional_band": {
            "ruling": ("REMOVED, the rule and the class emission both. Pure subtraction; "
                       "nothing dangles as a future locator trap."),
            "grounds": ("A 70% opacity band on one node's long response: unlabelled, conveying "
                        "nothing to a screen reader, costing contrast, and restating the "
                        "PROVISIONAL badge that renders in the section label directly above the "
                        "same box. Measured after: that node's response body is at opacity 1."),
        },
        "note_toggle_border": {
            "ruling": "#332, not the literal expansion #33332200.",
            "grounds": ("#33332200 is a fully transparent border and no repair anyone would "
                        "recognise. The artifact declares the answer: K352's .depth-jump comment "
                        "says it is 'sibling of .note-toggle ... and styled off it', and uses a "
                        "visible dim #442222."),
        },
    }

    # ---------------------------------------------------------------- the hex repair
    am["hex_repair_K354"] = {
        "what": ("ELEVEN 5-digit hex literals over SIX declarations, invalid CSS since they were "
                 "written. A 5-digit value makes the WHOLE declaration invalid and the parser "
                 "drops it, so the confidence badges rendered as bare coloured text with no "
                 "border and no background in all three modes, and .note-toggle rendered as "
                 "browser-default button chrome rather than as [DISMANTLE]'s sibling."),
        "the_count_WI_K343_recorded_was_wrong": (
            "WI-K343 logged this and said EIGHT while listing eleven; the K354 handoff carried "
            "the eight and listed only eight, omitting .confidence-full's pair (#4a733/#4a711, "
            "dead code until `full` renders -- which this cut makes live, so it rides) and "
            ".note-toggle's #33200 (the border of the very control this cut puts on two more "
            "cards). Corrected by counting DECLARATIONS."),
        "and_a_naive_grep_returns_15": (
            "Four of the fifteen are inside K352's own COMMENT documenting the bug -- ccclxxix's "
            "marker trap, which had already produced two false readings in two sessions. The "
            "comment is rewritten so it no longer carries the literals, and the gate requires "
            "the result to contain ZERO 5-digit literals with the base's 15 asserted for "
            "non-vacuity."),
        "form": ("3-digit colour plus 2 alpha digits, expanded to the 8-digit form the author "
                 "intended: #4a733 -> #44aa7733, and so on."),
        "proved_by_computed_style": (
            "Read as getComputedStyle().borderTopWidth and .backgroundColor in real Chromium, "
            "never as a string in the stylesheet: base 0px / rgba(0,0,0,0), candidate 1px solid "
            "/ the declared fill. The defect is the ABSENCE of a computed border, which is "
            "exactly what a text scan cannot see."),
    }

    # ---------------------------------------------------------------- ccclxxx
    am["ccclxxx_hazard_K354"] = {
        "hazard": (
            "REPAIRING AN INVALID DECLARATION IS AN ADDITION TO THE CASCADE, NOT A RESTORATION "
            "OF INTENT. An invalid declaration is DROPPED, so everything downstream was computed "
            "against its ABSENCE. Restoring it introduces a value nothing else was written "
            "against, and the effect can go either way."),
        "how_it_bit": (
            "Repairing the badges' invalid `background` restored dark tints. In DARK mode they "
            "lighten a near-black ground and contrast barely moves. In HIGH CONTRAST they "
            "darken a LIGHT ground under DARK text, and the STRONG badge measured 4.16:1 before "
            "the repair and 3.84:1 after -- LESS LEGIBLE REPAIRED THAN BROKEN. Nothing in the "
            "cut, the reconstruction gate or the stylesheet could see it; only a contrast ratio "
            "computed on the RENDERED COMPOSITE could."),
        "the_fix": (
            "In high contrast the badges take the repaired BORDER and `background: none`. That "
            "keeps the ground exactly as the reader has always seen it, repairs the real defect, "
            "regresses nothing, and changes no authored colour. Gated: STRONG 4.16 -> 4.16 and "
            "PROVISIONAL 5.48 -> 5.48, both required to be >= their base values."),
        "counter_discipline": (
            "When a repair restores a dropped value, enumerate what was computed against its "
            "absence and RE-MEASURE those on the composite -- not on the palette. A ratio taken "
            "against a guessed ground is a claim about the guess."),
        "family": ("ccclxxix's neighbour by instrument -- the measurement was of the palette "
                   "rather than of the render -- and ccclxxi's by shape: a value everything "
                   "else was written against, changed underneath them."),
    }

    # ---------------------------------------------------------------- the inversion
    am["prior_gate_inversion_K354"] = {
        "the_finding": (
            "tools/k353_wing_functional_gate.py contained three checks that ASSERTED THE DEFECT: "
            "that solipsism's [NOTE] control is absent, that 7 cards carry one, and that the "
            "layer stands at 9 notes / 7 reachable. Run UNCHANGED against the repaired flagship "
            "it fails exactly those three and NOTHING ELSE -- all 22 wing links, the NULL, the "
            "care-ethics caveat and the boot-witness control stay green."),
        "why_it_is_the_session_s_best_evidence": (
            "The gate was written a session earlier by a seat with no knowledge of this cut, so "
            "its inversion is an independent verdict rather than a self-report. Captured before "
            "anything was amended, as tools/k354_prior_gate_inversion_v0_1.json, 16 checks / 3 "
            "failed."),
        "symmetry_proved_both_ways": (
            "K353 gate unchanged: 0 failed on the base, 3 on the candidate. Amended gate: 0 "
            "failed on the candidate, the SAME 3 on the base."),
        "why_it_was_amended_in_place": (
            "A gate is not a record. The wuld primer makes every future pin move owe this file a "
            "re-run, so leaving it permanently three-red would hand the next session a landmine "
            "that reads exactly like a regression. Amended on the K338/K351 precedent, with its "
            "pre-amendment bytes recoverable from git; its landed K353 control artifact is NOT "
            "overwritten and the amended gate emits v0_2."),
        "and_a_SECOND_gate_asserts_it_too_found_only_by_grepping": (
            "tools/k352_functional_gate.py asserts `(noteDivs, noteBtns) == (9, 7)` under the "
            "label 'note layer UNCHANGED ... the coupling is queued, not repaired'. Two gates "
            "in two sessions encoded the same defect, and the second was found by GREPPING for "
            "it rather than by running anything -- which is the counter-discipline, applied to "
            "itself."),
        "and_it_is_deliberately_NOT_amended_which_is_the_sharper_rule": (
            "A gate scoped to a HISTORICAL PAIR and a gate on a STANDING RE-RUN PATH are "
            "different objects. k352_functional_gate.py takes --base and --cand and measures "
            "the K352 cut; against K352's own pair (9, 7) is still TRUE, and it breaks only if "
            "someone points it at a flagship it was never about. The wing gate takes --root and "
            "the wuld primer makes every future pin move owe it a re-run against the CURRENT "
            "surfaces, so it must track the artifact or it becomes a landmine. Amend the second "
            "kind; leave the first, which is a record. 'Amend every gate that mentions the "
            "defect' would have falsified a correct historical measurement."),
        "general_form_worth_carrying": (
            "A green control battery is also a MAP OF WHAT THE BUILDERS AND GATES WILL NOT "
            "ACCEPT, and nothing reads it that way -- K351 registered the same thing when a "
            "passing control turned out to have already refuted the next session's plan. A "
            "session that repairs a defect should grep the gates for assertions OF that defect "
            "before it starts, and expect to amend them."),
    }

    # ---------------------------------------------------------------- legibility
    am["high_contrast_legibility_K354"] = {
        "measured_on_the_composite_in_real_chromium": {
            "note_toggle": "2.49 -> 6.80",
            "confidence_full": "new, 4.72",
            "confidence_strong": "4.16 -> 4.16 (unchanged)",
            "confidence_provisional": "5.48 -> 5.48 (unchanged)",
        },
        "two_rules_this_cut_REQUIRED_rather_than_chose": (
            "`.confidence-full` never rendered, so it never needed a high-contrast rule; #4a7 "
            "measures about 2.5:1 on the high-contrast ground and #174 measures 4.72:1. "
            "`.note-toggle` never had one either: #996 measures 2.49:1 there, UNDER even the "
            "3:1 floor for a UI component, while its [DISMANTLE] sibling has had one since "
            "K352. Making a control legible on two more cards while leaving it illegible in the "
            "accessibility mode is not a repair."),
        "LOGGED_not_repaired": (
            "The high-contrast STRONG badge measures 4.16:1, under 4.5 for 8px text. "
            "PRE-EXISTING and UNCHANGED by this cut. #960 is an authored colour and moving it "
            "is a register call rather than a build one -- Josiah's, with the library seat."),
    }

    # ---------------------------------------------------------------- lifecycle updates
    am["note_confidence_coupling_QUEUED_K352"]["lifecycle_status"] = (
        "LANDED at K354 as the v4.1.2 pin move. The repair executed is the one specified here, "
        "verbatim. See note_confidence_repair_LANDED_K354.")
    am["note_reachability_finding_K349"]["lifecycle_status"] = (
        "REPAIRED at K354. The 195 unreachable words are reachable: 9 containers, 9 controls, "
        "and the control is proved to WORK by clicking it, not merely to exist.")
    am["confidence_ruling_K349"]["lifecycle_status"] = (
        "Two of the three regen legs are DISCHARGED at K354 -- `full` now renders, and the "
        "unlabelled provisional opacity band is removed. The third, that the grade silently "
        "controlled note reachability, is dissolved rather than discharged: the grade no longer "
        "controls it. See confidence_render_ruling_K354.")

    am["next"] = {
        "first": (
            "R1 with the library seat, unchanged and still the binding constraint on everything "
            "the map can show a reader: it releases the (a) surface, 69 of 138 entries against "
            "the 22 shipped at K353. Then R2 for (b). R4, the /combined graft, is Josiah plus "
            "the library seat and nothing downstream waits on it."),
        "second": (
            "UPSTREAM AUTHORING, and it is still the honest move. The map has produced 29 (b) "
            "items and the programme has repaired three sentences. Cowork cannot close that "
            "gap: a repair is a pin move and stance-bearing content is Josiah's with the "
            "library seat. The queue: the sixteen v4.1.0 enrichment items, "
            "happiness-is-choice#medium, the just-depressed depressive-realism contradiction "
            "(an AGGRAVATION per design 11.1 -- repair at the NODE), care-ethics#note's "
            "unrouted remainder (ccclxxvi), and flow-states, whole or not at all."),
        "also_open": (
            "The regen queue still derives from the A-E fragments only: 10 adjudicated (b) "
            "entries from R, F and G are unqueued, and it is a build against committed "
            "artifacts that touches no flagship byte. The five wings' navs do not route to "
            "/adversarial/. The high-contrast STRONG badge measures 4.16:1 -- logged, an "
            "authored colour. archive/INDEX.md is a dated record of the WI-K316 filing pass "
            "rather than a live index, so K352-K354 material is findable only by path."),
        "explicitly_NOT_recommended": (
            "Flipping responseLevel's default to `long`. Held at K352, K353 and again here; "
            "asserted byte-identical by the cut and measured in the browser at both roots."),
        "closed_by_this_session": (
            "The [NOTE] confidence coupling and the `confidence` regen item, which canon had "
            "said should ride together. They did."),
    }

    d["keyset_delta_ledger"]["v38_16_K354"] = (
        "MINOR. Six adversarial_map subkey additions (note_confidence_repair_LANDED_K354, "
        "confidence_render_ruling_K354, hex_repair_K354, ccclxxx_hazard_K354, "
        "prior_gate_inversion_K354, high_contrast_legibility_K354), three lifecycle_status "
        "additions inside existing subkeys (note_confidence_coupling_QUEUED_K352, "
        "note_reachability_finding_K349, confidence_ruling_K349) and a replacement of "
        "adversarial_map.next. One keyset_delta_ledger addition; a replacement of "
        "next_recommended_session; one session_log_recent append. PIN MOVE: combined.html "
        + PIN_OLD + " -> " + PIN_NEW + ", and NO CORPUS BYTE on any surface -- "
        "xsurface_v4_1_0.py reads identically at 6cd132ee5b8c7ca78ad0e095806f1c93 before and "
        "after, corpus and jsx asserted unmoved git-to-git, corpus `version` held at 4.1.0. No "
        "map or register artifact touched. invariants, schemas and hazard_map asserted "
        "byte-identical.")

    d["next_recommended_session"] = {
        "session": "R1 with the library seat, then R2.",
        "why": ("Unchanged by this session and now the ONLY thing standing between the map and "
                "its (a) surface. K354 closed the last flagship-side mechanism item canon was "
                "carrying, so nothing mechanical is in front of the rulings any more."),
        "scope": ("A ruling, not a build. If a build session is wanted instead, the two clean "
                  "no-pin candidates are the regen-queue gap (10 adjudicated (b) entries from "
                  "R, F and G that build_queue.py structurally cannot reach) and the five "
                  "wings' navs."),
        "do_not": ("Ship (a) or (b) cards before their ruling. Flip responseLevel's default. "
                   "Assume a count taken over free text. Trust a CSS text scan to tell you what "
                   "a browser renders."),
    }

    d["session_log_recent"].append(
        "K354_note_and_confidence (2026-09-18): THE NOTE AND THE CONFIDENCE LAYER, landed as "
        "the v4.1.2 PIN MOVE -- combined.html " + PIN_OLD + " -> " + PIN_NEW + " -- with NO "
        "CORPUS BYTE on any surface: xsurface_v4_1_0.py reads identically at "
        "6cd132ee5b8c7ca78ad0e095806f1c93 before and after, which is the mechanical proof, and "
        "the corpus `version` stays 4.1.0. THE REPAIR: the [NOTE] control lifted out of `if "
        "(conf !== 'full')` so its condition equals its container's -- 9 containers, 9 controls "
        "-- making 195 words readable that no reader could open, on a card K353 had just "
        "started pointing readers at. THE RENDER RULINGS, delegated by Josiah with the "
        "recommendations on the record: `full` renders FULL and the silent `|| 'full'` upgrade "
        "of 64 never-graded objections is deleted, so absence now means ungraded; the "
        "unlabelled 70% provisional opacity band is removed, rule and class both. THE HEX: "
        "eleven 5-digit literals over six declarations repaired -- not the eight WI-K343 "
        "counted, and the three it missed include the [NOTE] button's own border. THE SESSION'S "
        "BEST EVIDENCE IS NOT ITS OWN: K353's wing gate, run UNCHANGED, fails exactly the three "
        "checks that assert the defect and nothing else, and the amended gate fails the same "
        "three on the base. ccclxxx registered -- repairing an invalid declaration is an "
        "ADDITION to the cascade, and the restored fills made the high-contrast STRONG badge "
        "LESS legible repaired (4.16 -> 3.84) than broken, visible only in a contrast ratio "
        "computed on the rendered composite; fixed with `background: none` in high contrast, "
        "and both ratios gated against regression.")

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before, "top-level keyset moved -- that would force MAJOR"
    assert len(keys_before) == 41, "keyset is %d, expected 41" % len(keys_before)
    for k in ("invariants", "schemas", "hazard_map"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], \
            "%s moved -- that would force MAJOR" % k
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"
    added = set(am) - am_keys_before
    assert added == {"note_confidence_repair_LANDED_K354", "confidence_render_ruling_K354",
                     "hex_repair_K354", "ccclxxx_hazard_K354", "prior_gate_inversion_K354",
                     "high_contrast_legibility_K354"}, "adversarial_map gained %r" % sorted(added)

    open(OUT, "wb").write(out)
    print("project_canon_v38_16.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset %d held; invariants/schemas/hazard_map byte-identical" % len(keys_before))
    print("  adversarial_map %d -> %d keys" % (len(am_keys_before), len(am)))


if __name__ == "__main__":
    main()
