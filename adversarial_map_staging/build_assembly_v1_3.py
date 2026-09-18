#!/usr/bin/env python3
"""Build adversarial_map_v1_3.json -- the assembly that carries the HR-15 fold (K351).

WHAT THIS BUILDER CHANGES FROM build_assembly_v1_2.py, which stays BYTE-IDENTICAL:
  i.   OUT is adversarial_map_v1_3.json, and v1_2 joins the predecessor guards.
  ii.  NOTHING ELSE IN THE PIPELINE MOVES. PHASES, SUPERSEDED, the validator, the caps,
       the partition unit and all three coverage claims are byte-identical to v1_2. The
       fold is entirely upstream: adv_map_phaseG_v0_1.json was amended in place by
       tools/amend_phaseG_K351.py, so care-ethics#note arrives here as a (d) on HR-15.
  iii. The fold is a FRAGMENT AMENDMENT, not an assembly supersession, and the two are
       kept apart on purpose. `supersedes` records entries this assembly DROPS because a
       later phase re-adjudicated their locus -- Phase R's three, unchanged. An amendment
       changes a fragment's own bytes, so it arrives through `fragments[G].amended`, which
       v1_2's builder already reported, plus the explicit `fragment_amendments` block.
  iv.  THE (b) REMAINDER HAS NO HOME IN THIS ARTIFACT, and the builder is where that is
       proven rather than argued. The deepest locus for the three in-node repairs is
       care-ethics#long, which Phase B2 holds; the PARTITION invariant below refuses any
       locus claimed by two phases, and K349's controls_assembly_v1_2.py proves it on this
       exact pair. See fragment_amendments.b_remainder_disposition.

--- the v1_2 header follows, unchanged ------------------------------------------------
Build adversarial_map_v1_2.json -- the successor assembly with the `note` layer (K349).

WHAT THIS BUILDER CHANGES FROM build_assembly_v1_1.py, which stays BYTE-IDENTICAL:
  i.   PHASES gains ("G", "adv_map_phaseG_v0_1.json").
  ii.  The validator moves to v0_6, which reaches the top-level `note` key.
  iii. PRIMARY COVERAGE NO LONGER ABSORBS A NEW LOCUS KIND SILENTLY. v1_1 computed it as
       "every entry whose locus is not a variant", and `variant_slot("note")` is None, so
       a note entry would have counted as primary coverage of its node. That is ccclxxi
       exactly -- an invariant stated over the old locus set, which a new locus kind walks
       into by construction -- and it was found by READING the builder rather than
       assuming the K348 migration had covered it. Primary coverage is now stated
       positively: the four primary loci, and nothing else.
  iv.  note_coverage is asserted and declared. Coverage is THREE claims now, not two.
  v.   v1_1 is not edited, not re-pinned, not re-run. It is this file's predecessor guard.

--- the v1_1 header follows, unchanged ------------------------------------------------
Build adversarial_map_v1_1.json -- the TERMINAL SUCCESSOR ASSEMBLY (K348).

WHY v1_1 AND NOT v2_0.  79 of the 82 nodes inherit their adjudication byte-for-byte; three
re-adjudicate because the v4.1.0 cut destroyed their anchors; the schema is identical; no
inherited entry is re-classed.  That is a REVISION of the same map over a re-cut corpus,
not a re-mapping.  The surface widens -- 39 archetypeVariants loci the v1_0 claim was
structurally unable to cover -- but adding covered surface is an addition, not a break.  A
v2_0 would mean the adjudications themselves were re-done.  Canon's update_protocol names
the MINOR/MAJOR rule for CANON, not for this artifact; this line is the artifact's own.

WHAT THIS BUILDER CHANGES FROM build_assembly.py, which stays BYTE-IDENTICAL on disk so
that adversarial_map_v1_0.json remains reproducible from its own builder:

  1. PHASES gains ("R", ...) and ("F", ...).  Order is explicit, not lexical.
  2. The three entries Phase R supersedes are EXCLUDED from the A-E fragments by
     (target_id, target_locus).  They are the three whose anchors the v4.1.0 cut
     destroyed, which is exactly why the frozen v1_0 fails five checks against the
     post-cut corpus.  The surviving 90 anchors are ASSERTED to hold post-cut, not assumed.
  3. OUT is adversarial_map_v1_1.json.  v1_0 is not edited, not re-pinned, not re-run.
  4. The corpus pin is the POST-cut corpus, and source_corpus_objections_md5 is taken from
     the VALIDATOR's objections_digest rather than reimplemented here (the K344 hazard,
     which fired again on K347's first Phase F build).
  5. THE PARTITION INVARIANT MOVES FROM THE NODE TO THE (NODE, LOCUS).  v1_0's builder
     refused to write if any node was claimed by two phases.  Phase F authors variant loci
     on nodes A-E already cover, so that invariant fails SIXTEEN ways by construction here
     -- and the thing it was actually protecting, that no two phases adjudicate the same
     text, is intact: zero (target_id, target_locus) pairs are claimed by two phases.  This
     is the same unit migration K345 made for the entry cap, one layer over, and it was
     invisible until a fragment set finally crossed it.
  6. The entry caps are the K345 per-locus cap and the K348 node bound, both computed with
     the validator's own node_variant_slots rather than a local rule.

Repo-relative: resolves the repo from its own location.  --out <dir> to emit elsewhere.
"""
import os, sys, json, hashlib, collections

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_3.json")

sys.path.insert(0, STAGE)
import adv_map_validator_v0_6 as V   # noqa: E402  -- IMPORT THE INSTRUMENT, NEVER REIMPLEMENT IT

CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")

# Predecessor guards: this builder derives a successor, so the predecessor and ITS builder
# must be exactly what they were when v1_0 was written (ccclv / ccclxiv).
BASE_BUILDER_MD5 = "5267ecdbd4e14d7fc1830d7f0a979eca"   # build_assembly.py
BASE_V1_0_MD5 = "c4989e98b042e2f787a82df3f11ecdad"      # adversarial_map_v1_0.json
BASE_V1_1_MD5 = "e9e5abf820e3f7a687e2b84443883ade"      # adversarial_map_v1_1.json
BASE_V1_1_BUILDER_MD5 = "915593ab85de872f142f41f66431fe72"          # build_assembly_v1_1.py
BASE_V1_2_MD5 = "e4bef3cac882aa079951ba7ec1a9d11e"      # adversarial_map_v1_2.json
BASE_V1_2_BUILDER_MD5 = "45e711f47aad877741950dae43db929c"          # build_assembly_v1_2.py
AMENDED_PHASE_G_MD5 = "571cd47305612068651f13ca049557c2"            # adv_map_phaseG_v0_1.json
PRE_CUT_CORPUS_MD5 = "6ee1f6f31e0f012db0d58cae4f912fcb"
PRE_CUT_GIT_REF = "3e71546316285ef4fe3bd6d2da4ef1b5e4d6b50f:efilist_argument_library_v4_0_0.json"

PHASES = [("A", "adv_map_phaseA_v0_1.json"), ("B1", "adv_map_phaseB1_v0_1.json"),
          ("B2", "adv_map_phaseB2_v0_1.json"), ("C", "adv_map_phaseC_v0_1.json"),
          ("D", "adv_map_phaseD_v0_1.json"), ("E", "adv_map_phaseE_v0_1.json"),
          ("R", "adv_map_phaseR_v0_1.json"), ("F", "adv_map_phaseF_v0_1.json"),
          ("G", "adv_map_phaseG_v0_1.json")]
PHASE_ORDER = {ph: n for n, (ph, _f) in enumerate(PHASES)}
INHERITED = ("A", "B1", "B2", "C", "D", "E")

# The three v1_0 entries Phase R supersedes: the anchors the v4.1.0 cut destroyed.
SUPERSEDED = (("happiness-is-choice", "long"), ("just-edgy", "long"), ("just-depressed", "long"))


def main():
    fail = []
    md5f = lambda p: V.md5_bytes(open(p, "rb").read())
    got = md5f(os.path.join(STAGE, "build_assembly.py"))
    assert got == BASE_BUILDER_MD5, "BASE GUARD: build_assembly.py moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adversarial_map_v1_0.json"))
    assert got == BASE_V1_0_MD5, "BASE GUARD: adversarial_map_v1_0.json moved (%s)" % got
    got = md5f(os.path.join(STAGE, "build_assembly_v1_1.py"))
    assert got == BASE_V1_1_BUILDER_MD5, "BASE GUARD: build_assembly_v1_1.py moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adversarial_map_v1_1.json"))
    assert got == BASE_V1_1_MD5, "BASE GUARD: adversarial_map_v1_1.json moved (%s)" % got
    got = md5f(os.path.join(STAGE, "build_assembly_v1_2.py"))
    assert got == BASE_V1_2_BUILDER_MD5, "BASE GUARD: build_assembly_v1_2.py moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adversarial_map_v1_2.json"))
    assert got == BASE_V1_2_MD5, "BASE GUARD: adversarial_map_v1_2.json moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adv_map_phaseG_v0_1.json"))
    assert got == AMENDED_PHASE_G_MD5, ("BASE GUARD: the amended Phase G fragment is %s -- "
                                        "run tools/amend_phaseG_K351.py first" % got)

    craw = open(CORPUS, "rb").read()
    corpus = json.loads(craw.decode("utf-8"))
    cmd5 = V.md5_bytes(craw)
    odig = V.objections_digest(corpus)
    assert cmd5 != PRE_CUT_CORPUS_MD5, "this is the PRE-cut corpus; v1_1 pins the post-cut one"
    nodes = {o["id"]: o for o in corpus["objections"]}
    ids = [o["id"] for o in corpus["objections"]]
    idset = set(ids)
    order = {i: n for n, i in enumerate(ids)}

    sup = set(SUPERSEDED)
    entries, frag, dropped = [], {}, []
    for ph, f in PHASES:
        raw = open(os.path.join(STAGE, f), "rb").read()
        doc = json.loads(raw.decode("utf-8"))
        kept = 0
        for e in doc["entries"]:
            pv = e.get("provenance", {})
            if pv.get("phase") != ph:
                fail.append("%s carries an entry stamped phase %r" % (f, pv.get("phase")))
            if ph in INHERITED and (e["target_id"], e["target_locus"]) in sup:
                dropped.append({"target_id": e["target_id"], "target_locus": e["target_locus"],
                                "phase": ph, "class": e["class"],
                                "destroyed_anchor": e["target_anchor"]})
                continue
            entries.append(e)
            kept += 1
        frag[ph] = {"file": f, "md5": V.md5_bytes(raw), "entries_in_file": len(doc["entries"]),
                    "entries_taken": kept, "amended": bool(doc["meta"].get("amended"))}

    # Each superseded locus must be dropped exactly once and re-adjudicated by Phase R.
    if len(dropped) != len(SUPERSEDED):
        fail.append("expected %d superseded entries, dropped %d" % (len(SUPERSEDED), len(dropped)))
    r_loci = {(e["target_id"], e["target_locus"]) for e in entries
              if e["provenance"]["phase"] == "R"}
    for k in SUPERSEDED:
        if k not in r_loci:
            fail.append("%s#%s was dropped but Phase R does not re-adjudicate it" % k)

    # --- PARTITION, at the (node, locus). See change 5 in the docstring.
    by_locus = collections.defaultdict(set)
    by_node = collections.defaultdict(set)
    for e in entries:
        by_locus[(e["target_id"], e["target_locus"])].add(e["provenance"]["phase"])
        by_node[e["target_id"]].add(e["provenance"]["phase"])
    for k, phs in sorted(by_locus.items()):
        if len(phs) > 1:
            fail.append("%s#%s claimed by %s - fragments must PARTITION THE LOCUS" % (k[0], k[1], sorted(phs)))
    node_overlaps = sorted(k for k, phs in by_node.items() if len(phs) > 1)

    pairs = collections.Counter((e["target_id"], e["target_anchor"]) for e in entries)
    for k, n in pairs.items():
        if n > 1:
            fail.append("duplicate id x anchor: %r" % (k,))

    per_locus = collections.Counter((e["target_id"], e["target_locus"]) for e in entries)
    for (tid, loc), n in per_locus.items():
        if n > 3:
            fail.append("%s#%s has %d entries (K345 per-locus cap 3)" % (tid, loc, n))
    per_id = collections.Counter(e["target_id"] for e in entries)
    caps = {}
    for tid, n in per_id.items():
        nvar = len(V.node_variant_slots(nodes[tid])) if tid in nodes else 0
        bound = 3 + 3 * nvar
        caps[tid] = (n, nvar, bound)
        if n > bound:
            fail.append("%s has %d entries (K348 node bound %d = 3 + 3*%d variant loci)"
                        % (tid, n, bound, nvar))

    # Coverage is THREE claims now and all three are asserted, not reported.
    # STATED POSITIVELY (ccclxxi): v1_1 said "not a variant locus", which a new locus kind
    # walks into. `note` is apparatus attached to a node, not the node's argument, so it
    # cannot make a node covered -- the same ruling the v0_6 validator enforces.
    primary_cov = {e["target_id"] for e in entries if e["target_locus"] in V.LOCI}
    missing_primary = sorted(idset - primary_cov)
    if missing_primary:
        fail.append("NOT mapped-complete at the primary ladder: %d uncovered: %s"
                    % (len(missing_primary), missing_primary[:6]))
    extra = sorted(set(per_id) - idset)
    if extra:
        fail.append("entries target %d ids not in the corpus: %s" % (len(extra), extra[:6]))
    var_total = sorted((n["id"], V.VARIANT_PREFIX + s)
                       for n in corpus["objections"] for s in V.node_variant_slots(n))
    var_hit = sorted({(e["target_id"], e["target_locus"]) for e in entries
                      if V.variant_slot(e["target_locus"]) is not None})
    if len(var_hit) != len(var_total):
        fail.append("variant coverage %d/%d -- the assembly declares completion"
                    % (len(var_hit), len(var_total)))
    # note coverage is REPORTED and declared, never forced: the K349 ruling is NARROW, so
    # partial note coverage is the correct state and completion would be the defect.
    note_total = sorted((n["id"], V.NOTE_LOCUS) for n in corpus["objections"]
                        if V.node_has_note(n))
    note_hit = sorted({(e["target_id"], e["target_locus"]) for e in entries
                       if e["target_locus"] == V.NOTE_LOCUS})
    for tid, _l in note_hit:
        if not V.node_has_note(nodes.get(tid, {})):
            fail.append("%s carries a note entry but has no note" % tid)
    if len(note_hit) > len(note_total):
        fail.append("note coverage %d/%d exceeds the corpus" % (len(note_hit), len(note_total)))

    # Every anchor verbatim in ITS locus against the POST-cut corpus. ASSERTED, not assumed:
    # this is the check the frozen v1_0 fails three ways against these bytes.
    anchor_bad = []
    for e in entries:
        txt = V.locus_text(nodes[e["target_id"]], e["target_locus"]) if e["target_id"] in nodes else ""
        if e["target_anchor"] not in txt:
            anchor_bad.append("%s#%s [%s]" % (e["target_id"], e["target_locus"], e["provenance"]["phase"]))
    if anchor_bad:
        fail.append("%d anchors do not hold against the post-cut corpus: %s"
                    % (len(anchor_bad), anchor_bad[:6]))

    if any(e.get("status") != "mapped" for e in entries):
        fail.append("an entry carries a status other than 'mapped'; the lifecycle lives in canon")

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1

    entries.sort(key=lambda e: (order[e["target_id"]], PHASE_ORDER[e["provenance"]["phase"]],
                                e["target_locus"], e["target_anchor"]))

    cc = collections.Counter(e["class"] for e in entries)
    per_phase = {ph: dict(collections.Counter(
        e["class"] for e in entries if e["provenance"]["phase"] == ph)) for ph, _ in PHASES}
    tiers = {o["id"]: o["tier"] for o in corpus["objections"]}
    per_tier = {}
    for t in sorted(set(tiers.values())):
        n = [e for e in entries if tiers[e["target_id"]] == t]
        per_tier["T%d" % t] = {"nodes": len(set(e["target_id"] for e in n)), "entries": len(n),
                               **dict(collections.Counter(e["class"] for e in n))}
    loci = dict(collections.Counter(e["target_locus"] for e in entries))
    prim_loci = {k: v for k, v in loci.items() if k in V.LOCI}
    var_loci = {k: v for k, v in loci.items() if V.variant_slot(k) is not None}
    note_loci = {k: v for k, v in loci.items() if k == V.NOTE_LOCUS}

    doc = {"meta": {
      "artifact": "adversarial_map_v1_3.json",
      "state": ("MAPPED-COMPLETE, PRE-TRIAGE (ratification Q3). Every entry carries status "
        "'mapped'. The lifecycle mapped -> queued -> ratified -> landed | rejected lives in "
        "project_canon, never in this artifact."),
      "assembled": "2026-09-18, wuld.ink Cowork, K351",
      "successor_to": {
        "artifact": "adversarial_map_v1_2.json", "md5": BASE_V1_2_MD5, "bytes": 265046,
        "and_before_it": ("adversarial_map_v1_1.json (%s) and adversarial_map_v1_0.json "
                          "(FROZEN, %s)" % (BASE_V1_1_MD5, BASE_V1_0_MD5)),
        "why_v1_3_and_not_v2_0": ("Every one of v1_2's 138 entries is here; none is added, removed "
          "or re-anchored; the schema is unchanged. ONE entry is re-classed, care-ethics#note from "
          "(b) to (d), by Josiah's ratification at K350, and its routing changes with its class "
          "because the schema binds the two. A single ratified reclassification is a revision of "
          "the same map, not a re-mapping -- and it is the first entry in the programme to change "
          "class without its anchor being destroyed, which is why it is recorded here rather than "
          "in `supersedes`."),
        "frozen_predecessor": {
          "artifact": "adversarial_map_v1_0.json", "md5": BASE_V1_0_MD5, "bytes": 186406,
        "its_corpus_md5": PRE_CUT_CORPUS_MD5, "its_corpus_recoverable_at": PRE_CUT_GIT_REF,
        "disposition": ("FROZEN, NOT STALE, and NOT EDITED. v1_0 stays byte-identical and stays "
          "pinned to the pre-cut corpus, against which it still validates under --assembly at "
          "21 checks / 0 violations / 0 advisories. This file supersedes it; it does not replace "
          "it on disk. A map re-pinned under entries authored against the old text could never be "
          "falsified, which is the whole reason the predecessor is kept rather than refreshed."),
        "why_v1_1_and_not_v2_0": ("79 of 82 nodes inherit their adjudication byte-for-byte, three "
          "re-adjudicate because the v4.1.0 cut destroyed their anchors, the schema is unchanged, "
          "and no inherited entry is re-classed. That is a revision of the same map over a re-cut "
          "corpus. The surface widens to 39 archetypeVariants loci the v1_0 claim was structurally "
          "unable to cover, but covered surface is an addition, not a break. A v2_0 would mean the "
          "adjudications were re-done.")}},
      "source_corpus": "efilist_argument_library_v4_0_0.json",
      "source_corpus_md5": cmd5,
      "source_corpus_objections_md5": odig,
      "corpus_note": ("v4.1.0, the POST-cut corpus. The digest is taken from the validator's own "
        "objections_digest rather than recomputed here: a builder that reimplements its gate's "
        "instrument can disagree with it, which is the K344 hazard and it fired again on K347's "
        "first Phase F build."),
      "supersedes": {
        "count": len(dropped), "entries": dropped,
        "by": "adv_map_phaseR_v0_1.json",
        "grounds": ("These three anchors were destroyed by the v4.1.0 cut -- they are the "
          "repairs R1/R2/R3 recorded verbatim in canon's v4_1_0_cut.repairs. Phase R "
          "re-adjudicates each locus against the post-cut text. The v1_0 entries are excluded "
          "here rather than edited anywhere: the assembly SUPERSEDES, it does not amend a "
          "ratified fragment.")},
      "fragment_amendments": {
        "count": sum(1 for v in frag.values() if v["amended"]),
        "fragments": sorted(ph for ph, v in frag.items() if v["amended"]),
        "this_session": {
          "fragment": "adv_map_phaseG_v0_1.json", "locus": "care-ethics#note",
          "what": "(b) -> (d), routed to HR-15, novel true. Josiah, K350; applied K351.",
          "builder": "tools/amend_phaseG_K351.py, base read from the git blob at 649fdbc2",
          "precedent": ("K338, which amended Phase A and Phase B1 in place rather than minting a "
            "phase letter. A new letter would need PHASES extended in the validator -- v0_7 -- for "
            "one reclassification.")},
        "amendment_vs_supersession": ("An AMENDMENT changes a fragment's own bytes and arrives "
          "here through the fragment; a SUPERSESSION drops an entry from an inherited fragment "
          "because a later phase re-adjudicated its locus, and arrives through `supersedes`. "
          "Phase R's three are supersessions because the v4.1.0 cut destroyed their anchors. "
          "care-ethics#note is an amendment because its anchor is intact and only the ruling "
          "moved."),
        "b_remainder_disposition": ("The three in-node repairs the reclassification leaves behind "
          "are NOT authored as a map entry, and the ground is mechanical rather than editorial. "
          "Their deepest locus is care-ethics#long, which Phase B2 holds since K229: the PARTITION "
          "invariant in this builder refuses any locus claimed by two phases, and K349's own "
          "controls_assembly_v1_2.py proves it by mutating this very entry to #long and requiring "
          "the refusal. They cannot ride on the amended entry either -- routing-shape admits "
          "exactly one class-shaped key, and all 138 entries of v1_2 carry exactly one -- so a (d) "
          "cannot carry a regen_candidate. Authoring them at #medium instead would be "
          "locus-shopping against locus_discipline. They are recorded verbatim in canon's "
          "care_ethics_supersession_RATIFIED_K350, and the queue's reach over non-A-E phases is "
          "the standing carry it already was."),
        "structural_finding": ("A (b) -> (d) reclassification DISCARDS the routing of the class it "
          "left, by construction: routing shape is bound to class and admits exactly one key. The "
          "repairable content the entry identified survives only in prose -- in `grounds` and in "
          "whatever canon block records the ratification -- and no gate can miss it, because no "
          "gate knows it was ever there.")},
      "nodes_covered": len(primary_cov), "nodes_total": len(ids), "entries": len(entries),
      "coverage_distinct_ids": len(set(per_id)),
      "variant_coverage": "%d/%d" % (len(var_hit), len(var_total)),
      "note_coverage": "%d/%d" % (len(note_hit), len(note_total)),
      "note_coverage_is_deliberately_partial": ("The K349 ruling is NARROW: a note is a map "
        "target only where it makes or concedes a claim the corpus would have to defend. Of the "
        "nine notes, three are authoring apparatus (sibling taxonomy, build-pass provenance, a "
        "ratification-delta line, a tier instruction addressed to a future editor) and one is a "
        "legitimate scope qualifier consistent with its response. Against those the class law -- "
        "the strongest continuation against our text -- is malformed, so 9/9 would be inflation "
        "rather than completion. Two of the nine are also structurally unreachable by any reader: "
        "combined.html emits the [NOTE] button inside `if (conf !== 'full')`, and toggleNote has "
        "exactly one caller, so a note on a node graded full or ungraded sits in the DOM at "
        "display:none with nothing able to reveal it."),
      "coverage_is_three_claims": ("coverage %d/%d is the PRIMARY ladder, the claim v1_0 made. "
        "variant_coverage %d/%d is the archetypeVariants surface, which v1_0's validator could "
        "not name. note_coverage %d/%d is the third, and it is deliberately partial rather than "
        "complete -- see note_coverage_is_deliberately_partial. All three are declared here "
        "rather than reported, and per ccclxx a declared summary is gated against the scope of "
        "the file that declares it; for a single-file assembly that scope is the whole set, so "
        "the declarations are honest in a way they could not be in a fragment's meta. The three "
        "are NOT commensurable and are never summed: the first is the claim that every node's "
        "argument was adjudicated, and a note locus does not contribute to it."
        % (len(primary_cov), len(ids), len(var_hit), len(var_total),
           len(note_hit), len(note_total))),
      "class_counts": {k: cc[k] for k in ("a", "b", "c", "d")},
      "per_phase": per_phase, "per_tier": per_tier,
      "locus_distribution": {"primary": prim_loci, "variant_entries": sum(var_loci.values()),
                             "variant_loci_carrying_entries": len(var_hit),
                             "note_entries": sum(note_loci.values()),
                             "note_loci_carrying_entries": len(note_hit)},
      "fragments": frag,
      "entry_caps": {
        "per_locus": "<=3 entries per (target_id, target_locus). K345, Josiah.",
        "per_node": ("<=3 + 3*(variant loci on that node). K348, Josiah. The K345 form reserved "
          "ONE slot per variant locus while the per-locus cap allows three, so the node bound and "
          "anti-inflation gate 5 disagreed by construction wherever a variant locus legitimately "
          "opened: gate 5 asks for the second continuation and the node bound refused to hold it. "
          "red-button-repugnant is where the disagreement surfaced -- 3 inherited + 3 from Phase F "
          "against a K345 bound of 5. A node carrying no variants still keeps the Q1-ratified "
          "bound of 3 exactly. Measured blast radius across these 133 entries: one node changes "
          "verdict and no other, and no node is within reach of the amended bound."),
        "at_or_near_bound": {tid: {"entries": v[0], "variant_loci": v[1], "bound": v[2]}
                             for tid, v in sorted(caps.items()) if v[0] >= v[2] - 1}},
      "partition_invariant": {
        "unit": "(target_id, target_locus)",
        "holds": "0 loci claimed by two phases",
        "migrated_from": ("v1_0's builder refused to write if any NODE was claimed by two phases. "
          "Phase F authors variant loci on nodes A-E already cover, so at this fragment set the "
          "node-level form fails %d ways BY CONSTRUCTION while the property it was protecting -- "
          "that no two phases adjudicate the same text -- is perfectly intact. Same unit migration "
          "K345 made for the entry cap, one layer over; invisible until a fragment set crossed it."
          % len(node_overlaps)),
        "nodes_carrying_more_than_one_phase": node_overlaps},
      "locus_closure_not_declared": ("Deliberate. The stopping rule (gate 5, design v0_3 s10.3) "
        "records a per-locus authoring decision, and the validator gates a declaration against the "
        "loci THAT FILE authored, both ways. Phases A-E predate gate 5 and recorded no stop, so an "
        "assembly-level declaration would either be a guess about what six earlier phases decided "
        "or would fail its own key-set check. Phase F's own locus_closure stands in its fragment, "
        "where the file that made the decisions is the file that declares them."),
      "validation": ("validator v0_6 under --assembly against the post-cut corpus: 0 violations "
        "AND 0 advisories. --assembly promotes every advisory to hard, so the thirteen advisories "
        "v1_0 had to discharge are re-checked here against different bytes rather than assumed to "
        "have stayed discharged."),
      "locus_discipline": ("Author against the deepest locus that addresses the objection, or "
        "state in the grounds why a shallower one was chosen (hazard ccclxi / ledger class C8). "
        "The anchor rule permits any locus and is silent on depth."),
      "fences": ("Nothing here authorizes a byte. (b) and (c) yields are intake candidates routing "
        "through staging -> cold-grade -> assembly inside a declared content cut; see "
        "adversarial_map_regen_queue_v0_1.json. (d) termini route to "
        "honest_residuals_register_v0_4.json."),
      "siblings": {"predecessor": "adversarial_map_v1_2.json",
                   "queue": "adversarial_map_regen_queue_v0_1.json",
                   "register": "honest_residuals_register_v0_4.json",
                   "rulings": "adversarial_map_assembly_rulings_v0_1.json",
                   "ledger": "process_ledger_v0_1.md"}},
      "entries": entries}

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), V.md5_bytes(b)))
    print("  %d/%d nodes (primary), variant %d/%d, note %d/%d, %d entries, classes %s"
          % (len(primary_cov), len(ids), len(var_hit), len(var_total),
             len(note_hit), len(note_total), len(entries), doc["meta"]["class_counts"]))
    print("  dropped %d superseded; node-level partition would report %d overlaps, locus-level 0"
          % (len(dropped), len(node_overlaps)))
    print("  per tier: %s" % json.dumps(per_tier))
    return 0


if __name__ == "__main__":
    sys.exit(main())
