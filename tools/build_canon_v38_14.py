#!/usr/bin/env python3
"""project_canon_v38_14.json -- MINOR. The level-independent affordance LANDED (K352). PIN MOVE.

ccclxiv FIRST: v38_13 is round-tripped at the serialization this file emits BEFORE anything is
derived.

MINOR is asserted, not claimed: the top-level keyset is held at 41 and `invariants`, `schemas`
and `hazard_map` are required byte-identical, which is what would force MAJOR.

`last_updated` is NOT required to move -- K351 ran on the same operator-local day.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K352_REPO") or os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_13.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_14.json")
SRC_MD5 = "e516008afa35ed401d303ee5faada543"
DUMP = dict(indent=2, ensure_ascii=False)

PINS = {
    "pin_old":   ("combined.html v4.1.0", "72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770),
    "pin_new":   ("combined.html v4.1.1", "f095c0ce0e5a1d796d57fa5a5dd62f7d", 2985989),
    "corpus":    ("efilist_argument_library_v4_0_0.json", "04bf6482aa0374ee92a81c1d55ec41f8", 1334024),
    "jsx":       ("efilist_argument_library_v4_0_0.jsx", "b196548b6eb39065842d62292acca89f", 1273483),
    "xsurface":  ("canonical-serialization md5, all three surfaces", "6cd132ee5b8c7ca78ad0e095806f1c93", 0),
    "sweep":     ("tools/affordance_K352.py", None, 0),
    "verify":    ("tools/verify_K352.py", None, 0),
    "control":   ("tools/k352_functional_control_v0_1.json", "78c2aff851d99bdb3c8d466ddb90ead6", 0),
}


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_13.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_13 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False)
              for k in ("invariants", "schemas", "hazard_map")}
    keys_before = list(d)
    am = d["adversarial_map"]
    am_keys_before = len(am)

    # --- pointer brought current (K345a precedent: a value correction in place, not ccclv) ---
    am["level_independent_affordance_K350"]["lifecycle_status"] = (
        "LANDED at K352 as the v4.1.1 pin move. See level_independent_affordance_LANDED_K352 for "
        "what actually shipped, which is a superset of what was specified: the badge, plus the "
        "anchor grammar that gives it an inbound half. Was: ruled, not built.")

    am["level_independent_affordance_LANDED_K352"] = {
        "what_shipped": (
            "combined.html ONLY, twelve line-indexed edits, +3,219 bytes. (1) A per-card "
            "[DISMANTLE] control in the RESPONSE section label, rendered at EVERY responseLevel -- "
            "a control gated by the depth it exists to change cannot be found by the reader who "
            "needs it -- which calls the single card-anchor router and reaches setDepth(), so the "
            "global depth control syncs and there is no parallel render path. (2) THE ANCHOR "
            "GRAMMAR GAINS AN OPTIONAL DEPTH: `#obj-<id>@<short|medium|long>`. (3) COPY LINK emits "
            "that suffix whenever the reader is not at the boot default, so the grammar ships with "
            "a PRODUCER rather than as a vocabulary nothing writes."),
        "the_inbound_half_was_not_in_the_K350_spec_and_is_the_load_bearing_one": (
            "K350 specified the badge. A badge is the OUTBOUND half and it serves a reader already "
            "on the card. The broken link is INBOUND: a map surface linking `#obj-<id>` lands the "
            "reader on `medium` whatever the badge does. Shipping the badge alone would have left "
            "the stated problem unsolved, so the grammar is not scope creep -- it is the half the "
            "spec's own diagnosis required."),
        "append_only_proven_not_asserted": (
            "`@` is outside the id vocabulary [A-Za-z0-9_-], so the suffix cannot collide with any "
            "objection id. Proven in a real browser: bare `#obj-<id>` still lands at medium and "
            "still focuses, exactly as K108; `#rwe-<id>` still promotes to `#/rwe/instance:<id>`; "
            "`#rwe-<id>@long` is deliberately NOT claimed and still falls through to the legacy "
            "promote; an unknown depth token does not match the carve-out; an unknown id with a "
            "valid depth degrades silently and changes no depth. Canon v37.39's append-only anchor "
            "covenant holds."),
        "what_was_REFUSED": (
            "The default is NOT flipped to `long` (next.explicitly_NOT_recommended; the depth "
            "ladder is a reading register and the default is every visitor's first impression). "
            "archetypeSel is NOT touched (D5/D7). The [NOTE] confidence coupling is NOT repaired "
            "-- see note_confidence_coupling_QUEUED_K352. No map content ships: that is the NEXT "
            "step and it is gated on this one."),
        "the_mechanical_proof_that_no_data_moved": (
            "tools/xsurface_v4_1_0.py reads IDENTICALLY before and after at " + PINS["xsurface"][1] +
            ". The corpus JSON and the JSX blobs are asserted UNMOVED git-to-git. The corpus "
            "`version` field stays 4.1.0 because e922e6c established that it names the CONTENT "
            "CUT, and a UI change is not a content cut; the RELEASE label moves to v4.1.1. This is "
            "the fifth time a release label has moved over unmoved corpus content -- v4.0.1 "
            "through v4.0.4 were the first four."),
        "instruments": {
            "sweep": ("tools/affordance_K352.py -- line-indexed with a per-line anchor assertion on "
                      "the sweep_v4_1_0.py pattern; never mutates the tracked original, emits to "
                      "k352_drop/."),
            "verify": ("tools/verify_K352.py -- reads the base from GIT BLOBS and RECONSTRUCTS: it "
                       "re-applies the sweep's own declared edit list to the git base and asserts "
                       "byte equality with the candidate. Stronger than verify_v4_1_0.py's "
                       "changed-line comparison, which only works when the line count is unchanged "
                       "and this cut INSERTS. It proves the candidate IS the base plus exactly "
                       "these twelve operations, not merely that they are among the changes. It "
                       "IMPORTS the edit list rather than re-typing it (ccclxii)."),
            "functional": ("tools/k352_functional_gate.py -- real Chromium over file:// with all "
                           "http(s) aborted, 28 checks, control artifact " + PINS["control"][1] +
                           ". It runs the PINNED BASE as a NULL for every deep-link claim, because "
                           "'the affordance fixes the broken link' is a claim about a before-state "
                           "and a before-state is measured (ccclxvi). It is the one tool in this "
                           "cut that does NOT reproduce from its committed location: it needs a "
                           "browser the operator's VM does not carry. Said out loud rather than "
                           "left for a later session to find."),
        },
        "pins": {"old": "%s / %d" % (PINS["pin_old"][1], PINS["pin_old"][2]),
                 "new": "%s / %d" % (PINS["pin_new"][1], PINS["pin_new"][2]),
                 "delta_bytes": PINS["pin_new"][2] - PINS["pin_old"][2]},
    }

    am["surface_parity_ruling_K352"] = {
        "ruling": ("THE JSX IS A DATA-PARITY SURFACE ONLY. Its UI is out of scope for flagship UI "
                   "work, and the cross-surface gate's scope -- the OBJECTIONS literal and nothing "
                   "else -- is the correct scope. Ruled at K352 because the K352 handoff asked for "
                   "it explicitly, and because the affordance would otherwise have had to be "
                   "invented twice."),
        "grounds": ("The JSX executes nowhere: nothing loads it, it has no hash router, no "
                    "__arglibRouteObj and no setDepth (it is a React useState). An affordance "
                    "there would be a different mechanism with a different failure surface, gated "
                    "by nothing, on a surface with no reader."),
        "and_the_surfaces_have_ALREADY_diverged_in_three_places": [
            "[NOTE]: the flagship emits the button inside `if (conf !== 'full')`; the JSX gates it "
            "on `obj.note && responseLevel === 'long'` with NO confidence condition. 7 notes "
            "reachable on the flagship against 9 on the JSX.",
            "REBUTTAL_STRENGTH: 2 occurrences in combined.html, 0 in the corpus JSON and 0 in the "
            "JSX. Already documented in xsurface_v4_1_0.py's own docstring, which calls the "
            "flagship a hand-assembled SUPERSET.",
            "The whole outer hash router, the card-anchor router and the anchor self-test: "
            "flagship-only, and now the affordance too.",
        ],
        "consequence": ("UI parity is not a property these surfaces have ever had. Asserting it "
                        "now would invent a claim rather than preserve one. What the gate "
                        "guarantees is DATA parity, and that guarantee is unweakened."),
    }

    am["note_confidence_coupling_QUEUED_K352"] = {
        "ruling": ("On the K352 handoff's second half: THE FLAGSHIP IS WRONG AND THE JSX IS RIGHT, "
                   "and the decisive evidence is inside the flagship rather than across the two."),
        "the_argument": ("combined.html's note <div> is emitted on `obj.note && responseLevel === "
                         "'long'` with NO confidence condition. Only the REVEALER carries one. A "
                         "container emitted for 9 nodes with a button emitted for 7 is an internal "
                         "inconsistency, not a design -- the flagship's own DOM already says the "
                         "note belongs to any node with a note at `long`. solipsism is the "
                         "reductio: its note is the text that EXPLAINS its confidence:full, and "
                         "that value is exactly what suppresses the button."),
        "the_repair": ("one structural move -- lift the [NOTE] button out of the `if (conf !== "
                       "'full')` block so its condition equals the div's. It makes 195 previously "
                       "unreadable words readable, which is why it is NOT a mechanism and did not "
                       "ride with the affordance: this session's whole value is that it shipped a "
                       "mechanism with no stance in it."),
        "status": ("QUEUED. Flagship-side, therefore a pin move, and it should ride with the "
                   "`confidence` regen item (confidence_ruling_K349) rather than alone."),
        "measured_at_K352": ("in the shipped candidate, in a real browser: 9 .confidence-note divs, "
                             "7 .note-toggle buttons. Unchanged by this cut, asserted."),
    }

    am["ccclxxvii_hazard_K352"] = {
        "numeral": "ccclxxvii",
        "headline": ("A NAVIGATION THAT CHANGES ONLY THE FRAGMENT DOES NOT RE-BOOT, SO A TEST THAT "
                     "VARIES ONLY THE HASH READS THE PREVIOUS CASE'S STATE AS THIS CASE'S "
                     "VERDICT."),
        "detail": ("The K352 functional gate probed a series of deep links with "
                   "page.goto(url + '#...'). Same URL, different fragment, is a SAME-DOCUMENT "
                   "navigation: no reload, no re-init, module state survives. Two checks failed "
                   "and both were the harness. Worse, they failed PLAUSIBLY -- the value returned "
                   "was a real responseLevel, just the one the previous case had set -- and had "
                   "the cases been ordered differently they would have PASSED for the wrong "
                   "reason, which is the outcome nothing would have caught."),
        "family": ("ccclxxiv's direct companion. ccclxxiv says a UI-state gate has an INITIALISER "
                   "rather than a distribution, so read the initialiser. ccclxxvii says: then "
                   "PROVE THE INITIALISER RAN. A navigation API that silently degrades to a "
                   "same-document update is, at the assertion, indistinguishable from one that "
                   "re-booted. Also ccclviii: the apparatus is the likeliest explanation of a "
                   "surprising reading."),
        "counter_discipline": ("Reset to a different document between cases, and -- because a rule "
                               "honoured at write time is cccli -- carry a BOOT WITNESS that "
                               "mechanises it: stamp a sentinel on the OUTGOING document and "
                               "assert it is absent after the navigation. The K352 gate ships that "
                               "witness with a FAILING CONTROL proving it can fail: without the "
                               "reset the sentinel survives."),
        "and_the_same_session_found_three_instances_of_ccclxxiii": (
            "Three checks in this cut's own gates failed against a correct artifact: an occurrence "
            "count that forgot the two nested CSS rules also contain the substring; a hex scan "
            "that read the comment naming the invalid literals as if it were a declaration; a "
            "literal count that counted the same comment. Every one was the CHECK'S MODEL OF ITS "
            "OWN SUBJECT, never the bytes -- and every one sat downstream of the reconstruction "
            "check, which proves the candidate is the base plus exactly the declared edits and was "
            "green throughout. ccclxxiii said a gate over a byte-pinned file can only subtract; "
            "the refinement is that a gate which RESTATES what a stronger gate already proves is "
            "exactly where the false alarms accumulate, because nothing forces it to be precise. "
            "Registered as instances, not numerals."),
    }

    am["next"] = {
        "first": ("SHIP DIRECTION TWO AND THE 21 PURE-(d) CARDS on the affordance, under a "
                  "TERMINUS label and not a strength label. The mechanism now exists and the "
                  "inbound grammar gives the map's own surface a link form that lands a reader at "
                  "the locus. THE COUNT IS 21, NOT 20: K351's fold made care-ethics pure-(d) and "
                  "nothing re-counted. Re-derived at K352 against adversarial_map_v1_3.json."),
        "second": ("Answer R1 with the library seat -- it releases the (a) surface; scope corrected "
                   "at K350, it blocks (a) only. Then R2 for the (b) surface. R4, the /combined "
                   "graft, is Josiah plus the library seat."),
        "also_open": ("The [NOTE] confidence coupling and the `confidence` regen item, both "
                      "flagship-side and therefore pin-move work, and they should ride together. "
                      "flowstates_correction_spec_v0_1.md remains PROPOSED and DID NOT ride with "
                      "K352: its own section 5.4 requires the successor map re-pinned in the SAME "
                      "session as the corpus cut, which would have dragged a successor assembly "
                      "into a mechanism session; and landing its flagship-only Repair B alone "
                      "would have corrected the CITATION of a defect while leaving the defect. A "
                      "spec lands whole. The regen queue still derives from the A-E fragments "
                      "only: 10 adjudicated (b) entries from R, F and G are unqueued, and the "
                      "care-ethics (b)-remainder is unrouted entirely (ccclxxvi)."),
        "explicitly_NOT_recommended": ("Flipping responseLevel's default to `long`. Held at K352 "
                                       "and implemented as held: the candidate's initialiser is "
                                       "asserted byte-identical."),
    }

    d["canon_version"] = "38.14"
    d["canon_version_marker"] = "v38.14"
    d["last_updated_by_session"] = "K352_the_affordance"
    d["keyset_delta_ledger"]["v38_14_K352"] = (
        "MINOR. Four adversarial_map subkey additions "
        "(level_independent_affordance_LANDED_K352, surface_parity_ruling_K352, "
        "note_confidence_coupling_QUEUED_K352, ccclxxvii_hazard_K352), a replacement of "
        "adversarial_map.next, and one in-place pointer correction "
        "(level_independent_affordance_K350.lifecycle_status, ruled -> LANDED). One "
        "keyset_delta_ledger addition; a replacement of next_recommended_session; one "
        "session_log_recent append. THIS IS A PIN MOVE: combined.html "
        + PINS["pin_old"][1] + " -> " + PINS["pin_new"][1] + ", v4.1.0 -> v4.1.1. The corpus and "
        "the JSX do NOT move and the corpus `version` field stays 4.1.0. invariants, schemas and "
        "hazard_map asserted byte-identical.")
    d["next_recommended_session"] = {
        "session": ("SHIP DIRECTION TWO: the 21 pure-(d) cards on the level-independent "
                    "affordance, under a TERMINUS label."),
        "why": ("The mechanism the whole interconnection programme was gated on now exists and is "
                "live. A (d) claims its line terminates at bedrock the register names; a stronger "
                "unmapped move reaches the same or deeper bedrock and does not falsify it, which "
                "is why (d) ships while (a) waits on R1. Zero new reader-facing text is owed: the "
                "register's glosses already read."),
        "scope": ("An aux-wing surface plus, if the cards render on /combined itself, R4 first and "
                  "then a separate declared pin-move session. The label is load-bearing and is "
                  "part of the class_asymmetry ruling, not presentation."),
        "do_not": ("Ship (a) or (b) cards. Use a strength label. Re-open HR-15 or the K351 "
                   "(b)-remainder disposition. Assume the pure-(d) count is 20."),
    }
    d["session_log_recent"].append(
        "K352_the_affordance (2026-09-18): THE LEVEL-INDEPENDENT AFFORDANCE LANDED. PIN MOVE, "
        "combined.html " + PINS["pin_old"][1] + " / 2,982,770 -> " + PINS["pin_new"][1] + " / "
        "2,985,989 (+3,219), v4.1.0 -> v4.1.1. Corpus " + PINS["corpus"][1] + " and jsx "
        + PINS["jsx"][1] + " UNMOVED git-to-git; the cross-surface gate reads IDENTICALLY before "
        "and after at " + PINS["xsurface"][1] + ", which is the mechanical proof the cut touched "
        "no data; the corpus `version` field stays 4.1.0 because it names the content cut. Twelve "
        "line-indexed edits: a per-card [DISMANTLE] control rendered at EVERY responseLevel, the "
        "anchor grammar extended to `#obj-<id>@<depth>` (append-only; `@` is outside the id "
        "vocabulary), and COPY LINK emitting that suffix so the grammar ships with a producer. THE "
        "INBOUND HALF WAS NOT IN THE K350 SPEC AND IS THE LOAD-BEARING ONE -- a badge serves a "
        "reader already on the card, and the broken link is inbound. Gates: reconstruction against "
        "the GIT BASE (base + exactly the 12 declared edits == candidate, byte for byte), the "
        "cross-surface identity, and 28 functional checks in real Chromium including the PINNED "
        "BASE run as a null. ccclxxvii registered against this session's own test harness: a "
        "fragment-only navigation does not re-boot, so a hash-varying test reads the previous "
        "case's state -- now mechanised as a boot witness with a failing control. Also ruled: the "
        "JSX is a DATA-parity surface only, the surfaces having already diverged in three UI "
        "places; and the flagship's [NOTE] confidence coupling is the wrong one of the two, QUEUED "
        "not repaired. Corrected by measurement: the pure-(d) set is 21, not 20, and #long is 80 "
        "of 98 answer targets = 81.6%.")

    assert list(d) == keys_before, "the top-level keyset moved -- that would be MAJOR"
    assert len(d) == 41, "keyset is %d, expected 41" % len(d)
    for k, v in before.items():
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == v, \
            "%s moved -- that would be MAJOR" % k
    assert len(am) == am_keys_before + 4, "adversarial_map gained %d subkeys, expected 4" % (len(am) - am_keys_before)

    out = json.dumps(d, **DUMP) + "\n"
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), hashlib.md5(b).hexdigest()))
    print("  v38.13 -> v38.14 MINOR; keyset %d held; invariants/schemas/hazard_map byte-identical" % len(d))
    print("  adversarial_map subkeys %d -> %d" % (am_keys_before, len(am)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
