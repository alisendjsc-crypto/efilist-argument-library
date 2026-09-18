#!/usr/bin/env python3
"""Amend adv_map_phaseG_v0_1.json IN PLACE for the HR-15 ratification (K351).

THE ROUTE, AND WHY IT IS THE K338 ONE.  Josiah ratified at K350 that care-ethics#note is
(d) rather than (b), routed to a NEW bedrock root, HR-15.  A new phase letter would need
PHASES extended in the validator -- v0_7 -- for one reclassification, so the fragment is
amended in place and the amendment is recorded in its own `meta.amended` block, exactly as
Phase A and Phase B1 were amended at K338.

WHY THE BASE COMES FROM A GIT BLOB AND NOT FROM DISK.  This builder REPLACES the file it
reads, so a disk-based base guard is true exactly once and false forever after -- the
second run would gate the amended bytes against the original md5 and abort.  Reading the
base from `git show <ref>:<path>` makes the build reproducible at any future HEAD, which is
the same instrument tools/verify_v4_1_0.py uses and for the same reason.

WIDTH OF THE RULING (K338's rule, and it is a rule).  The ruling changed the CLASS and the
ROUTING.  It did not change the move.  `adversarial_move` and `target_anchor` are asserted
BYTE-IDENTICAL to the base, the other four entries are asserted byte-identical, and the
only meta fields that move are `class_counts` (which the validator gates against the
entries, so it MUST move) and the new `amended` block.

THE (b) REMAINDER IS NOT A MAP ENTRY, AND THAT IS MEASURED RATHER THAN CHOSEN.  See the
`b_remainder_disposition` key written into the amended block, and canon.

Repo-relative: resolves the repo from its own location.  --out <dir> to emit elsewhere.
"""
import os, sys, json, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
REL = "adversarial_map_staging/adv_map_phaseG_v0_1.json"
OUT = os.path.join(OUT_DIR, REL)

sys.path.insert(0, STAGE)
import adv_map_validator_v0_6 as V   # IMPORT THE INSTRUMENT, NEVER REIMPLEMENT IT

BASE_REF = "649fdbc288611fa6ea420e95055d810264301a06"   # the K350 commit
BASE_MD5 = "d7cd18eb0467f38d8ecd4694776dd885"
BASE_BYTES = 12295
TARGET = ("care-ethics", "note")

# The shipped bedrock_name.  BEDROCK_MAP in build_register_v0_4.py keys on this EXACT
# string, so a later edit here breaks that build loudly rather than silently remapping.
# It carries the id, which the pre-map bedrock names do not: those were named by fragment
# authors who did not know the id, and this one was named by the ruling that assigned it.
BEDROCK_NAME = "HR-15 -- currency of obligation: consent versus constitutive relation"
TERMINUS = ("new root, ratified by Josiah at K350. HR-06 depends_on HR-15; HR-15 sibling_of "
            "HR-03. Birth certificate is this entry.")

GROUNDS = (
 "Reclassified (b) -> (d) by Josiah's ruling at K350; the move and the anchor are unchanged. "
 "The terminus is not a defect in this node but a question the corpus nowhere derives: whether "
 "obligation is denominated in AUTHORIZATION by the obligated party, or CONSTITUTED by the "
 "relation the parties stand in. The consent architecture presupposes the first and a developed "
 "relational ethics denies it, and no node argues for either. Registered as HR-15, novel, birth "
 "certificate here. "
 "THE ALTERNATIVE ROUTING IS A REDUCTIO, WHICH IS WHY THIS IS A ROOT AND NOT A TRIBUTARY. HR-06 "
 "asks whether unauthorized imposition wrongs absent harm, which PRESUPPOSES that authorization "
 "is the currency; routing this into HR-06 would give HR-06 a tributary that dissolves HR-06's "
 "own question. HR-15 is a sibling of HR-03 rather than a facet of it -- HR-03 is the seat of "
 "STANDING, what bears value; HR-15 is the currency of OBLIGATION, what makes a demand binding -- "
 "and they come apart both ways: a relational holist can hold consent is the currency for "
 "impositions on individuals, and a natural-duties theorist denies consent-as-currency with no "
 "relational axiology at all. The registered (d) at care-ethics#long is on HR-03 and does not "
 "cover this. "
 "THE (b) REMAINDER, AND WHAT IT DOES NOT DO. Three in-node defects survive the reclassification "
 "and are repairable without touching the bedrock, specified verbatim in canon's "
 "care_ethics_supersession_RATIFIED_K350: the doctor/infection analogy at #long, which needs an "
 "existing person made worse off and so smuggles the comparative baseline creation lacks; the "
 "phrase 'the deepest possible unchosen moral obligation' at #long and its shorter form at "
 "#medium, an EQUIVOCATION at the node's pivotal move -- the obligation is the PARENT's and "
 "unchosen by the parent, the grievance is the CHILD's and unchosen by the child -- on the exact "
 "term of art this note concedes the node has not engaged; and move one, which should be rebuilt "
 "as the ABSTENTION finding, care ethics having no pre-relational evaluative standpoint and so "
 "rendering no verdict on instantiation at all. They are repair work, not a second adjudication "
 "of this locus, and they have no home in this artifact: see b_remainder_disposition in the "
 "amended block. "
 "NONE OF THEM REMOVES THE (d). The care ethicist's reply is available and must not be "
 "over-claimed away: the absence of a verdict at your chosen moment is not silence, it is the "
 "denial that your moment is the evaluative one. That RELOCATES the bedrock; it does not "
 "dissolve it.")

AMENDED = {
 "at": "K351 (2026-09-18)",
 "ratified_by": "Josiah, K350",
 "what": ("care-ethics#note reclassified (b) -> (d). `routing.regen_candidate` dropped, "
          "`routing.residue` added on HR-15 with novel: true. `grounds` rewritten to justify a "
          "terminus rather than a repair. `meta.class_counts` b 2 -> 1, d 0 -> 1."),
 "how": ("Built by tools/amend_phaseG_K351.py, which reads the base from the git blob at "
         "%s rather than from disk -- this file is the file the builder replaces, so a "
         "disk-based base guard would be true exactly once. The class change forces the routing "
         "change: the validator's routing-shape check binds routing to class and requires EXACTLY "
         "one class-shaped key, so a (d) carries `residue` and can carry nothing else." % BASE_REF[:12]),
 "not_touched": ("`adversarial_move` and `target_anchor`, asserted byte-identical to the base, and "
                 "the other four entries, asserted byte-identical as a set. The ruling changed the "
                 "CLASS and the ROUTING; it did not change the move. A ratified artifact is amended "
                 "to the width of the ruling and no wider -- the K338 rule, applied here. "
                 "`locus_closure`, `coverage_distinct_ids`, `note_coverage` and `ruling_0a` are "
                 "unchanged: one entry changed class, none was added or removed."),
 "b_remainder_disposition": (
   "THE THREE IN-NODE DEFECTS ARE NOT AUTHORED AS A MAP ENTRY, AND THE GROUND IS MECHANICAL "
   "RATHER THAN EDITORIAL. The deepest locus that addresses them is care-ethics#long, which "
   "Phase B2 already holds; the assembly builder's PARTITION invariant refuses any locus claimed "
   "by two phases, and K349's own control battery proves it on this exact pair -- "
   "controls_assembly_v1_2.py, `builder-refuses-a-locus-claimed-by-two-phases`, mutates this very "
   "entry to #long and requires the refusal. They cannot ride on this entry either: routing-shape "
   "admits exactly one class-shaped key, so a (d) cannot carry a regen_candidate, and all 138 "
   "entries of v1_2 carry exactly one routing key. Authoring at #medium instead would be "
   "locus-shopping against locus_discipline (ccclxi). They live in canon, verbatim, and the "
   "queue's reach is the standing carry it already was: adversarial_map_regen_queue_v0_1.json "
   "derives from the A-E fragments only."),
}


def main():
    git = ["git", "-C", REPO, "show", "%s:%s" % (BASE_REF, REL)]
    raw = subprocess.run(git, capture_output=True, check=True).stdout
    assert V.md5_bytes(raw) == BASE_MD5, "BASE GUARD: blob md5 %s" % V.md5_bytes(raw)
    assert len(raw) == BASE_BYTES, "BASE GUARD: blob is %d B" % len(raw)
    base = json.loads(raw.decode("utf-8"))

    doc = json.loads(raw.decode("utf-8"))
    hits = [e for e in doc["entries"]
            if (e["target_id"], e["target_locus"]) == TARGET]
    assert len(hits) == 1, "expected exactly one entry at %s#%s, found %d" % (TARGET + (len(hits),))
    e = hits[0]
    assert e["class"] == "b", "base entry is class %r, not 'b'" % e["class"]
    assert set(e["routing"]) == {"regen_candidate"}, "base routing is %s" % sorted(e["routing"])

    e["class"] = "d"
    e["grounds"] = GROUNDS
    e["routing"] = {"residue": {"bedrock_name": BEDROCK_NAME,
                                "terminus_routing": TERMINUS, "novel": True}}

    cc = {}
    for x in doc["entries"]:
        cc[x["class"]] = cc.get(x["class"], 0) + 1
    doc["meta"]["class_counts"] = {k: cc[k] for k in ("a", "b", "c", "d") if k in cc}
    doc["meta"]["amended"] = AMENDED

    # --- WIDTH OF THE RULING, ASSERTED ------------------------------------------------
    b_e = [x for x in base["entries"] if (x["target_id"], x["target_locus"]) == TARGET][0]
    assert e["adversarial_move"] == b_e["adversarial_move"], "the adversarial_move MOVED"
    assert e["target_anchor"] == b_e["target_anchor"], "the target_anchor MOVED"
    assert e["status"] == b_e["status"] and e["provenance"] == b_e["provenance"], \
        "status or provenance moved"
    j = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)
    others_base = sorted(j(x) for x in base["entries"]
                         if (x["target_id"], x["target_locus"]) != TARGET)
    others_new = sorted(j(x) for x in doc["entries"]
                        if (x["target_id"], x["target_locus"]) != TARGET)
    assert others_base == others_new, "an entry other than %s#%s moved" % TARGET
    assert len(doc["entries"]) == len(base["entries"]) == 5, "the entry count moved"
    moved = sorted(k for k in set(base["meta"]) | set(doc["meta"])
                   if base["meta"].get(k) != doc["meta"].get(k))
    assert moved == ["amended", "class_counts"], "meta fields moved beyond the ruling: %s" % moved
    assert doc["meta"]["class_counts"] == {"a": 3, "b": 1, "d": 1}, doc["meta"]["class_counts"]

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), V.md5_bytes(b)))
    print("  base %s / %d B  ->  class_counts %s"
          % (BASE_MD5[:12], BASE_BYTES, doc["meta"]["class_counts"]))
    print("  move and anchor byte-identical; 4 other entries byte-identical; meta moved: %s" % moved)
    return 0


if __name__ == "__main__":
    sys.exit(main())
