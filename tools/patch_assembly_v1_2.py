#!/usr/bin/env python3
"""K349: derive build_assembly_v1_2.py from build_assembly_v1_1.py by ANCHORED patches.

build_assembly_v1_1.py stays byte-identical on disk so adversarial_map_v1_1.json remains
reproducible from its own builder -- the same reason build_assembly.py was kept at K348.
Every anchor is asserted to occur EXACTLY once. Binary read, explicit UTF-8 (ccclx).
"""
import os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "adversarial_map_staging", "build_assembly_v1_1.py")
BASE_MD5 = "4da2a5e0f9b1ef0e2f4a3c8b7d6e5f00"  # bound at run time; see main()

PATCHES = []
def P(tag, old, new):
    PATCHES.append((tag, old, new))

P("header",
'''"""Build adversarial_map_v1_1.json -- the TERMINAL SUCCESSOR ASSEMBLY (K348).''',
'''"""Build adversarial_map_v1_2.json -- the successor assembly with the `note` layer (K349).

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
Build adversarial_map_v1_1.json -- the TERMINAL SUCCESSOR ASSEMBLY (K348).''')

P("out-path",
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_1.json")''',
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_2.json")''')

P("validator-import",
'''import adv_map_validator_v0_5 as V   # noqa: E402  -- IMPORT THE INSTRUMENT, NEVER REIMPLEMENT IT''',
'''import adv_map_validator_v0_6 as V   # noqa: E402  -- IMPORT THE INSTRUMENT, NEVER REIMPLEMENT IT''')

P("base-guards-const",
'''BASE_BUILDER_MD5 = "5267ecdbd4e14d7fc1830d7f0a979eca"   # build_assembly.py
BASE_V1_0_MD5 = "c4989e98b042e2f787a82df3f11ecdad"      # adversarial_map_v1_0.json''',
'''BASE_BUILDER_MD5 = "5267ecdbd4e14d7fc1830d7f0a979eca"   # build_assembly.py
BASE_V1_0_MD5 = "c4989e98b042e2f787a82df3f11ecdad"      # adversarial_map_v1_0.json
BASE_V1_1_MD5 = "e9e5abf820e3f7a687e2b84443883ade"      # adversarial_map_v1_1.json
BASE_V1_1_BUILDER_MD5 = "__V1_1_BUILDER_MD5__"          # build_assembly_v1_1.py''')

P("phases",
'''          ("R", "adv_map_phaseR_v0_1.json"), ("F", "adv_map_phaseF_v0_1.json")]''',
'''          ("R", "adv_map_phaseR_v0_1.json"), ("F", "adv_map_phaseF_v0_1.json"),
          ("G", "adv_map_phaseG_v0_1.json")]''')

P("base-guards-assert",
'''    got = md5f(os.path.join(STAGE, "adversarial_map_v1_0.json"))
    assert got == BASE_V1_0_MD5, "BASE GUARD: adversarial_map_v1_0.json moved (%s)" % got''',
'''    got = md5f(os.path.join(STAGE, "adversarial_map_v1_0.json"))
    assert got == BASE_V1_0_MD5, "BASE GUARD: adversarial_map_v1_0.json moved (%s)" % got
    got = md5f(os.path.join(STAGE, "build_assembly_v1_1.py"))
    assert got == BASE_V1_1_BUILDER_MD5, "BASE GUARD: build_assembly_v1_1.py moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adversarial_map_v1_1.json"))
    assert got == BASE_V1_1_MD5, "BASE GUARD: adversarial_map_v1_1.json moved (%s)" % got''')

P("primary-coverage",
'''    # Coverage is TWO claims and both are asserted, not reported.
    primary_cov = {e["target_id"] for e in entries if V.variant_slot(e["target_locus"]) is None}''',
'''    # Coverage is THREE claims now and all three are asserted, not reported.
    # STATED POSITIVELY (ccclxxi): v1_1 said "not a variant locus", which a new locus kind
    # walks into. `note` is apparatus attached to a node, not the node's argument, so it
    # cannot make a node covered -- the same ruling the v0_6 validator enforces.
    primary_cov = {e["target_id"] for e in entries if e["target_locus"] in V.LOCI}''')

P("note-coverage-assert",
'''    var_hit = sorted({(e["target_id"], e["target_locus"]) for e in entries
                      if V.variant_slot(e["target_locus"]) is not None})
    if len(var_hit) != len(var_total):
        fail.append("variant coverage %d/%d -- the assembly declares completion"
                    % (len(var_hit), len(var_total)))''',
'''    var_hit = sorted({(e["target_id"], e["target_locus"]) for e in entries
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
        fail.append("note coverage %d/%d exceeds the corpus" % (len(note_hit), len(note_total)))''')

P("locus-distribution",
'''    prim_loci = {k: v for k, v in loci.items() if V.variant_slot(k) is None}
    var_loci = {k: v for k, v in loci.items() if V.variant_slot(k) is not None}''',
'''    prim_loci = {k: v for k, v in loci.items() if k in V.LOCI}
    var_loci = {k: v for k, v in loci.items() if V.variant_slot(k) is not None}
    note_loci = {k: v for k, v in loci.items() if k == V.NOTE_LOCUS}''')

P("meta-artifact",
'''      "artifact": "adversarial_map_v1_1.json",''',
'''      "artifact": "adversarial_map_v1_2.json",''')

P("meta-assembled",
'''      "assembled": "2026-09-17, wuld.ink Cowork, K348",
      "successor_to": {
        "artifact": "adversarial_map_v1_0.json", "md5": BASE_V1_0_MD5, "bytes": 186406,''',
'''      "assembled": "2026-09-17, wuld.ink Cowork, K349",
      "successor_to": {
        "artifact": "adversarial_map_v1_1.json", "md5": BASE_V1_1_MD5, "bytes": 252665,
        "and_before_it": "adversarial_map_v1_0.json (FROZEN, %s)" % BASE_V1_0_MD5,
        "why_v1_2_and_not_v2_0": ("Every one of v1_1's 133 entries is inherited byte-for-byte; "
          "nothing is superseded, re-classed or re-pinned; the schema is unchanged. Phase G adds "
          "five entries at a locus kind the enum could not previously name. Adding covered surface "
          "is an addition, not a break -- the same line v1_1 took over v1_0, and it is the "
          "artifact's own line rather than canon's update_protocol, which governs CANON."),
        "frozen_predecessor": {
          "artifact": "adversarial_map_v1_0.json", "md5": BASE_V1_0_MD5, "bytes": 186406,''')

P("meta-coverage-claims",
'''      "variant_coverage": "%d/%d" % (len(var_hit), len(var_total)),
      "coverage_is_two_claims": ("coverage %d/%d is the PRIMARY ladder, the claim v1_0 made. ''',
'''      "variant_coverage": "%d/%d" % (len(var_hit), len(var_total)),
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
      "coverage_is_three_claims": ("coverage %d/%d is the PRIMARY ladder, the claim v1_0 made. ''')

P("meta-locus-distribution",
'''      "locus_distribution": {"primary": prim_loci, "variant_entries": sum(var_loci.values()),
                             "variant_loci_carrying_entries": len(var_hit)},''',
'''      "locus_distribution": {"primary": prim_loci, "variant_entries": sum(var_loci.values()),
                             "variant_loci_carrying_entries": len(var_hit),
                             "note_entries": sum(note_loci.values()),
                             "note_loci_carrying_entries": len(note_hit)},''')

P("meta-validation",
'''      "validation": ("validator v0_5 under --assembly against the post-cut corpus: 0 violations ''',
'''      "validation": ("validator v0_6 under --assembly against the post-cut corpus: 0 violations ''')

P("meta-siblings",
'''      "siblings": {"predecessor": "adversarial_map_v1_0.json",''',
'''      "siblings": {"predecessor": "adversarial_map_v1_1.json",''')

P("print-tail",
'''    print("  %d/%d nodes (primary), variant %d/%d, %d entries, classes %s"
          % (len(primary_cov), len(ids), len(var_hit), len(var_total), len(entries),
             doc["meta"]["class_counts"]))''',
'''    print("  %d/%d nodes (primary), variant %d/%d, note %d/%d, %d entries, classes %s"
          % (len(primary_cov), len(ids), len(var_hit), len(var_total),
             len(note_hit), len(note_total), len(entries), doc["meta"]["class_counts"]))''')


P("successor-to-close",
'''          "adjudications were re-done.")},
      "source_corpus": "efilist_argument_library_v4_0_0.json",''',
'''          "adjudications were re-done.")}},
      "source_corpus": "efilist_argument_library_v4_0_0.json",''')

P("three-claims-text",
'''        "variant_coverage %d/%d is the archetypeVariants surface, which v1_0's validator could "
        "not name. Both are declared here rather than reported, and per ccclxx a declared "
        "summary is gated against the scope of the file that declares it -- for a single-file "
        "assembly that scope is the whole set, so both declarations are honest in a way they "
        "could not be in a fragment's meta."
        % (len(primary_cov), len(ids), len(var_hit), len(var_total))),''',
'''        "variant_coverage %d/%d is the archetypeVariants surface, which v1_0's validator could "
        "not name. note_coverage %d/%d is the third, and it is deliberately partial rather than "
        "complete -- see note_coverage_is_deliberately_partial. All three are declared here "
        "rather than reported, and per ccclxx a declared summary is gated against the scope of "
        "the file that declares it; for a single-file assembly that scope is the whole set, so "
        "the declarations are honest in a way they could not be in a fragment's meta. The three "
        "are NOT commensurable and are never summed: the first is the claim that every node's "
        "argument was adjudicated, and a note locus does not contribute to it."
        % (len(primary_cov), len(ids), len(var_hit), len(var_total),
           len(note_hit), len(note_total))),''')


def main():
    raw = open(SRC, "rb").read()
    src_md5 = hashlib.md5(raw).hexdigest()
    print("  base build_assembly_v1_1.py md5 %s" % src_md5)
    txt = raw.decode("utf-8")
    for tag, old, new in PATCHES:
        new = new.replace("__V1_1_BUILDER_MD5__", src_md5)
        n = txt.count(old)
        assert n == 1, "anchor %r occurs %d times, expected exactly 1" % (tag, n)
        txt = txt.replace(old, new, 1)
        print("  patched %s" % tag)
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "adversarial_map_staging", "build_assembly_v1_2.py")
    out = txt.encode("utf-8")
    open(dest, "wb").write(out)
    print("wrote %s  %s  %d B" % (dest, hashlib.md5(out).hexdigest(), len(out)))
    assert hashlib.md5(open(SRC, "rb").read()).hexdigest() == src_md5, "v1_1 builder mutated"
    print("  build_assembly_v1_1.py byte-identical: OK")


if __name__ == "__main__":
    main()
