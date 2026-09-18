#!/usr/bin/env python3
"""project_canon_v38_13.json -- MINOR. The HR-15 fold LANDED (K351).

ccclxiv FIRST: v38_12 is round-tripped at the serialization this file emits BEFORE
anything is derived. A builder that assumes its predecessor's indent produces a diff that
is 99% reformatting and 1% content, in which no reviewer can see the content.

MINOR is asserted, not claimed: the top-level keyset is held at 41 and `invariants`,
`schemas` and `hazard_map` are required byte-identical, which is what would force MAJOR.

`last_updated` is NOT required to move. K350 ran on the same operator-local day, and
demanding that field change would fail a correct canon for a calendar reason -- the gate
K349 wrote wrong before it wrote it right.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_12.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_13.json")
SRC_MD5 = "cf88360ac654d47296b675c94188d986"
DUMP = dict(indent=2, ensure_ascii=False)

PINS = {
    "assembly": ("adversarial_map_v1_3.json", "681827419df72a16a7c6fe70df8fe77f", 269352),
    "register": ("honest_residuals_register_v0_4.json", "d067729fafb51926bc9e845209417886", 44915),
    "fragment": ("adv_map_phaseG_v0_1.json", "571cd47305612068651f13ca049557c2", 16310),
    "predecessor_assembly": ("adversarial_map_v1_2.json", "e4bef3cac882aa079951ba7ec1a9d11e", 265046),
    "predecessor_register": ("honest_residuals_register_v0_3.json", "56a86d36e0354f00051a84ca02993fab", 41576),
    "fragment_base_blob": ("adv_map_phaseG_v0_1.json @ 649fdbc2", "d7cd18eb0467f38d8ecd4694776dd885", 12295),
}


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_12.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_12 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False)
              for k in ("invariants", "schemas", "hazard_map")}
    keys_before = list(d)

    am = d["adversarial_map"]

    # --- pointers brought CURRENT. Not ccclv: these two fields are current-state
    #     pointers, and the K345a precedent is a value correction in place. The dated
    #     records around them are untouched.
    am["HR_15_ratification_K350"]["lifecycle_status"] = (
        "LANDED at K351 in adversarial_map_v1_3.json and honest_residuals_register_v0_4.json. "
        "The artifact still records `mapped` only, per status_lifecycle; `landed(v1_3)` lives "
        "here. Was: RATIFIED, NOT YET LANDED.")
    am["care_ethics_supersession_RATIFIED_K350"]["status"] = (
        "LANDED(v1_3) at K351, per status_lifecycle. Was: RATIFIED by Josiah at K350; QUEUED for "
        "the build session.")

    am["phaseG_amendment_K351"] = {
        "what": ("adv_map_phaseG_v0_1.json amended IN PLACE: care-ethics#note (b) -> (d), "
                 "routing.regen_candidate dropped, routing.residue added on HR-15 with novel: "
                 "true, grounds rewritten to justify a terminus rather than a repair, "
                 "class_counts b 2 -> 1 and d 0 -> 1."),
        "route_and_why": ("The K338 precedent -- amend the ratified fragment and record it in its "
                          "own meta.amended block -- rather than minting a phase letter, which "
                          "would need PHASES extended in the validator (v0_7) for one "
                          "reclassification. Validator stays v0_6, self-test 78/78."),
        "builder": ("tools/amend_phaseG_K351.py. It reads the BASE FROM THE GIT BLOB at "
                    "649fdbc2 rather than from disk, because it replaces the file it reads: a "
                    "disk base guard would be true exactly once and false forever after. Same "
                    "instrument tools/verify_v4_1_0.py uses, same reason."),
        "width_of_the_ruling": ("asserted, not observed. `adversarial_move` and `target_anchor` "
                                "byte-identical to the base; the other four entries byte-identical "
                                "as a set; the only meta fields that move are `class_counts`, "
                                "which the validator gates against the entries and so MUST move, "
                                "and the new `amended` block. The ruling changed the class and the "
                                "routing; it did not change the move."),
        "pins": {"base": "d7cd18eb0467f38d8ecd4694776dd885 / 12,295 B",
                 "amended": "571cd47305612068651f13ca049557c2 / 16,310 B"},
    }

    am["b_remainder_disposition_K351"] = {
        "ruling": ("THE THREE IN-NODE REPAIRS ARE NOT AUTHORED AS A MAP ENTRY. The ground is "
                   "MECHANICAL rather than editorial, and it is measured rather than argued."),
        "the_kickoff_premise_that_was_false": (
            "The K351 kickoff planned one (b)-remainder entry at care-ethics#long and warned that "
            "it would put the node AT its bound of 3. The bound was never the binding constraint. "
            "care-ethics#long is held by PHASE B2 since K229, and the assembly builder's PARTITION "
            "invariant refuses any (target_id, target_locus) claimed by two phases. Measured by "
            "running it: `care-ethics#long claimed by ['B2', 'G'] - fragments must PARTITION THE "
            "LOCUS`. With no entry added the node sits at 2 of 3, not 3 of 3."),
        "and_it_was_already_proven_last_session": (
            "K349's own control battery contains the proof. controls_assembly_v1_2.py's control "
            "`builder-refuses-a-locus-claimed-by-two-phases` mutates THIS VERY ENTRY from #note to "
            "#long and requires the refusal. The plan that could not run had a passing control "
            "against it in the repo before it was written."),
        "the_second_wall": (
            "It cannot ride on the amended entry either. The validator's routing-shape check binds "
            "routing to class and requires EXACTLY one class-shaped key -- `set(r) == {\"residue\"}` "
            "for a (d) -- so a (d) cannot carry a regen_candidate. All 138 entries of v1_2 and "
            "v1_3 carry exactly one routing key, measured."),
        "the_routes_declined": (
            "Authoring at care-ethics#medium instead would be locus-shopping against "
            "locus_discipline: the deepest locus that addresses these defects is #long. Amending "
            "the B2 fragment to add the entry would exceed the width of the ruling and would stamp "
            "this seat's K351 authorship with the library seat's K229 provenance. Superseding the "
            "B2 (d) Phase-R-style would destroy a correct adjudication on a different question."),
        "where_they_live": (
            "care_ethics_supersession_RATIFIED_K350.b_remainder_three_in_node_defects, verbatim, "
            "and in the amended entry's own grounds. They are repair work for a declared content "
            "cut, not a second adjudication of this locus."),
        "queue_arithmetic_corrected": (
            "The kickoff said the fold `may make it 12`. Measured, it goes the other way: (b) "
            "entries from phases outside A-E, which the regen queue's builder cannot reach, were "
            "11 (R 3, F 6, G 2) and are 10 after the fold (G drops to 1). The fold does not move a "
            "(b) into the queue's reach -- it removes one from the map's (b) surface and leaves "
            "its repairable content with no routed home at all. That is ccclxxvi."),
        "what_the_repairs_do_NOT_do": (
            "Unchanged and restated because it is the thing most easily lost: the care ethicist's "
            "reply is available -- the absence of a verdict at your chosen moment is not silence, "
            "it is the denial that your moment is the evaluative one. The (d) survives all three "
            "repairs; they RELOCATE the bedrock rather than dissolving it."),
    }

    am["ccclxxvi_hazard_K351"] = {
        "numeral": "ccclxxvi",
        "headline": ("A CLASS RECLASSIFICATION DISCARDS THE ROUTING OF THE CLASS IT LEFT, AND "
                     "NOTHING CAN NOTICE THE LOSS."),
        "mechanism": (
            "The routing schema binds shape to class and admits exactly one class-shaped key. So "
            "re-classing an entry does not merge or migrate its routing -- it DELETES it by "
            "construction. Whatever that routing pointed at survives only as prose, in `grounds` "
            "and in whichever block records the ratification. No gate can miss it, because no gate "
            "knows it was ever there: the artifact after the change is internally consistent and "
            "validates clean."),
        "instance": ("care-ethics#note carried a regen_candidate naming three repairable in-node "
                     "defects. (b) -> (d) drops it, and the three have no routed home anywhere -- "
                     "not at their own locus, which another phase holds, and not on the entry, "
                     "which may carry only a residue. They are preserved here because K350 wrote "
                     "them down, which is a writer complying at write time: cccli's family."),
        "counter_discipline": (
            "When a ruling re-classes an entry, enumerate what the OLD routing pointed at and rule "
            "each item's destination explicitly BEFORE the build. Silence deletes it. The general "
            "form: any schema that binds a payload's shape to a discriminator turns a change of "
            "discriminator into a silent delete of the payload."),
        "relation_to_neighbours": (
            "ccclxxi is an invariant whose UNIT went stale; this is a payload the schema drops when "
            "its TYPE changes. ccclxii is a claim nothing checks; this is a claim nothing can even "
            "be written against."),
    }

    am["terminal_assembly_v1_3_K351"] = {
        "artifact": PINS["assembly"][0], "md5": PINS["assembly"][1], "bytes": PINS["assembly"][2],
        "entries": 138, "class_counts": {"a": 69, "b": 28, "c": 1, "d": 40},
        "coverage": "82/82 primary, 39/39 variant, 5/9 note (deliberately partial)",
        "validation": ("validator v0_6 under --assembly: 23 checks, 0 violations, 0 ADVISORIES. "
                       "--assembly promotes every advisory to hard."),
        "successor_to": "%s %s" % (PINS["predecessor_assembly"][0], PINS["predecessor_assembly"][1]),
        "why_v1_3_and_not_v2_0": ("All 138 of v1_2's entries are here; none added, removed or "
                                  "re-anchored; the schema is unchanged. ONE entry is re-classed by "
                                  "ratification. A single ratified reclassification is a revision "
                                  "of the same map, not a re-mapping."),
        "measured_delta": ("0 missing, 0 added, exactly 1 changed, and that entry's move, anchor, "
                           "status and provenance are byte-identical. Asserted by control."),
        "predecessors_untouched": ("adversarial_map_v1_0.json c4989e98b042e2f787a82df3f11ecdad "
                                   "(FROZEN, pre-cut corpus), v1_1 e9e5abf820e3f7a687e2b84443883ade, "
                                   "v1_2 e4bef3cac882aa079951ba7ec1a9d11e -- and v1_2 was "
                                   "REPRODUCED byte-for-byte from its own builder on its own inputs "
                                   "before v1_3 was written (ccclxiv)."),
    }

    am["honest_residuals_register_pin_v0_4"] = {
        "artifact": PINS["register"][0], "md5": PINS["register"][1], "bytes": PINS["register"][2],
        "bedrocks": 15, "residue_entries": 40,
        "source": "%s %s" % (PINS["assembly"][0], PINS["assembly"][1]),
        "new": ("HR-15 -- currency of obligation: consent versus constitutive relation. Name, "
                "gloss, alias `rival-occupant` and facet "
                "`unchosen-relations-bind-without-authorization` taken from "
                "HR_15_ratification_K350 verbatim. HR-06 gains depends_on HR-15; HR-15 declares "
                "sibling_of HR-03. Both kinds were already in the ratified vocabulary, so the "
                "v0_3 allowlist passed without extension."),
        "parity": ("TWO gates now. The inherited v0_1 gate is restricted to the phases v0_1 read "
                   "and is structurally blind to a change confined to R/F/G, so v0_4 adds a "
                   "field-for-field gate against v0_3 with exactly two declared exceptions. "
                   "Measured: 13 of 15 bedrocks byte-identical, HR-06 changed only in its "
                   "relations list, no bedrock changed tributary count, 0 undeclared adjacencies."),
        "predecessor": "%s %s, byte-identical on disk and reproduced from its own builder" % (
            PINS["predecessor_register"][0], PINS["predecessor_register"][1]),
        "render": "honest_residuals_register_v0_4.md",
    }

    am["next"] = {
        "first": ("THE LEVEL-INDEPENDENT AFFORDANCE, its own declared isolated PIN-MOVE session. "
                  "It gates every reader-facing thing downstream and it is not a stance-layer "
                  "change. Forces a same-session search-index regen and objection re-vendor."),
        "second": ("Ship direction two and the 20 pure-(d) cards on that affordance, under a "
                   "TERMINUS label, not a strength label."),
        "third": ("Answer R1 with the library seat -- it releases the (a) surface; scope corrected "
                  "at K350, it blocks (a) only. Then R2 for the (b) surface."),
        "also_open": ("The K350 relay Part A had not returned as of K351, so Part B stays sealed. "
                      "The regen queue still derives from the A-E fragments only: 10 adjudicated "
                      "(b) entries from R, F and G are unqueued, and the care-ethics (b)-remainder "
                      "is unrouted entirely (ccclxxvi)."),
        "explicitly_NOT_recommended": ("Flipping responseLevel's default to `long`. The depth "
                                       "ladder is a deliberate reading register and the change "
                                       "hits every visitor's first impression; the affordance "
                                       "forces the level only for the reader who asked."),
    }

    hr = d["terminal_stability_marker"]["honest_residuals"]
    hr["currency_of_obligation"] = {
        "register_id": "HR-15", "alias": "rival-occupant",
        "claim": ("Whether obligation is denominated in authorization by the obligated party, or "
                  "constituted by the relation the parties stand in. The corpus's consent "
                  "architecture presupposes the first; a developed relational ethics denies it, "
                  "and nothing in-corpus derives either."),
        "ratified": "Josiah, K350 (2026-09-18); landed in the artifacts at K351.",
        "birth_certificate": "care-ethics#note, Phase G",
        "why_a_root_and_not_a_tributary": ("Routing it into HR-06 would give HR-06 a tributary "
                                           "that DISSOLVES HR-06's own question -- HR-06 asks "
                                           "whether unauthorized imposition wrongs absent harm, "
                                           "which presupposes that authorization is the currency. "
                                           "A reductio, not a preference. Josiah's ground."),
        "relations": "HR-06 depends_on HR-15; HR-15 sibling_of HR-03.",
    }

    d["canon_version"] = "38.13"
    d["canon_version_marker"] = "v38.13"
    d["last_updated_by_session"] = "K351_build_the_fold"
    d["keyset_delta_ledger"]["v38_13_note"] = (
        "v38.12 -> v38.13 MINOR (K351_build_the_fold, 2026-09-18): keyset UNCHANGED at 41. Five "
        "additions INSIDE adversarial_map (phaseG_amendment_K351, b_remainder_disposition_K351, "
        "ccclxxvi_hazard_K351, terminal_assembly_v1_3_K351, honest_residuals_register_pin_v0_4), a "
        "replacement of adversarial_map.next, and two in-place pointer corrections "
        "(HR_15_ratification_K350.lifecycle_status and "
        "care_ethics_supersession_RATIFIED_K350.status, both RATIFIED -> LANDED per "
        "status_lifecycle). One addition inside terminal_stability_marker.honest_residuals "
        "(currency_of_obligation / HR-15). One keyset_delta_ledger addition; a replacement of "
        "next_recommended_session; one session_log_recent append. NO PIN. invariants, schemas and "
        "hazard_map asserted byte-identical.")
    d["next_recommended_session"] = {
        "session": ("THE LEVEL-INDEPENDENT AFFORDANCE. A declared, isolated PIN-MOVE session on "
                    "combined.html."),
        "why": ("82% of the map's answer targets sit at #long and `#obj-<id>` lands a reader on "
                "`medium`, because combined.html initialises `let responseLevel = \"medium\"`. A "
                "badge that renders at any level and forces `long` on activation fixes both "
                "directions and gates every reader-facing thing downstream. It renders no map "
                "content, so it is not a stance-layer change and does not wait on R4."),
        "scope": ("combined.html only, plus the same-session search-index regen and objection "
                  "re-vendor a pin move forces. NOT this session's shape: the fold is landed and "
                  "the map programme needs no further artifact."),
        "do_not": ("Flip responseLevel's default. Author past the care-ethics node bound. Re-open "
                   "HR-15. Start the sixteen v4.1.0 enrichment items on a session that is also "
                   "moving the pin."),
    }
    d["session_log_recent"].append(
        "K351_build_the_fold (2026-09-18): THE HR-15 FOLD LANDED, AND THE (b) REMAINDER TURNED OUT "
        "TO HAVE NOWHERE TO GO. NO PIN; combined.html 72187f6cf0fccdf8e9f4ec6ca5ce009c, corpus "
        "04bf6482aa0374ee92a81c1d55ec41f8 and jsx b196548b6eb39065842d62292acca89f untouched, "
        "cross-surface gate 6cd132ee5b8c7ca78ad0e095806f1c93 GREEN at open and close. Phase G "
        "amended in place on the K338 precedent (care-ethics#note b -> d, HR-15, novel true; move "
        "and anchor byte-identical, asserted); assembly v1_3 " + PINS["assembly"][1] + " -- 138 "
        "entries, a69/b28/c1/d40, --assembly 0 violations 0 advisories; register v0_4 "
        + PINS["register"][1] + " -- 15 bedrocks, 40 residue entries, 0 undeclared adjacencies, "
        "parity held against BOTH v0_1 and v0_3. THE KICKOFF'S CAP WARNING WAS THE WRONG "
        "CONSTRAINT: care-ethics#long is held by Phase B2, so the PARTITION invariant refuses a "
        "(b)-remainder entry there, and K349's own control battery already proved it on this exact "
        "pair. The node sits at 2 of a bound of 3. ccclxxvi registered: a class reclassification "
        "discards the routing of the class it left, and nothing can notice the loss. 45 controls, "
        "45 green, two of them repaired first because they aborted at an earlier gate than the one "
        "they named.")

    assert list(d) == keys_before, "the top-level keyset moved -- that would be MAJOR"
    assert len(d) == 41, "keyset is %d, expected 41" % len(d)
    for k, v in before.items():
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == v, \
            "%s moved -- that would be MAJOR" % k

    out = json.dumps(d, **DUMP) + "\n"
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), hashlib.md5(b).hexdigest()))
    print("  v38.12 -> v38.13 MINOR; keyset %d held; invariants/schemas/hazard_map byte-identical"
          % len(d))
    print("  adversarial_map subkeys %d; honest_residuals %d"
          % (len(d["adversarial_map"]), len(d["terminal_stability_marker"]["honest_residuals"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
