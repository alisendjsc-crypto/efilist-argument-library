#!/usr/bin/env python3
"""K351: derive build_assembly_v1_3.py from build_assembly_v1_2.py by ANCHORED patches.

build_assembly_v1_2.py stays byte-identical on disk so adversarial_map_v1_2.json remains
reproducible from its own builder -- the same reason build_assembly.py and
build_assembly_v1_1.py were kept. Every anchor is asserted to occur EXACTLY once.
Binary read, explicit UTF-8 (ccclx).
"""
import os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(HERE)
SRC = os.path.join(REPO, "adversarial_map_staging", "build_assembly_v1_2.py")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "build_assembly_v1_3.py")
BASE_MD5 = "45e711f47aad877741950dae43db929c"

PATCHES = []
def P(tag, old, new):
    PATCHES.append((tag, old, new))

P("header",
'''"""Build adversarial_map_v1_2.json -- the successor assembly with the `note` layer (K349).''',
'''"""Build adversarial_map_v1_3.json -- the assembly that carries the HR-15 fold (K351).

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
Build adversarial_map_v1_2.json -- the successor assembly with the `note` layer (K349).''')

P("out-path",
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_2.json")''',
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_3.json")''')

P("base-guard-consts",
'''BASE_V1_1_BUILDER_MD5 = "915593ab85de872f142f41f66431fe72"          # build_assembly_v1_1.py''',
'''BASE_V1_1_BUILDER_MD5 = "915593ab85de872f142f41f66431fe72"          # build_assembly_v1_1.py
BASE_V1_2_MD5 = "e4bef3cac882aa079951ba7ec1a9d11e"      # adversarial_map_v1_2.json
BASE_V1_2_BUILDER_MD5 = "45e711f47aad877741950dae43db929c"          # build_assembly_v1_2.py
AMENDED_PHASE_G_MD5 = "571cd47305612068651f13ca049557c2"            # adv_map_phaseG_v0_1.json''')

P("base-guard-asserts",
'''    got = md5f(os.path.join(STAGE, "adversarial_map_v1_1.json"))
    assert got == BASE_V1_1_MD5, "BASE GUARD: adversarial_map_v1_1.json moved (%s)" % got''',
'''    got = md5f(os.path.join(STAGE, "adversarial_map_v1_1.json"))
    assert got == BASE_V1_1_MD5, "BASE GUARD: adversarial_map_v1_1.json moved (%s)" % got
    got = md5f(os.path.join(STAGE, "build_assembly_v1_2.py"))
    assert got == BASE_V1_2_BUILDER_MD5, "BASE GUARD: build_assembly_v1_2.py moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adversarial_map_v1_2.json"))
    assert got == BASE_V1_2_MD5, "BASE GUARD: adversarial_map_v1_2.json moved (%s)" % got
    got = md5f(os.path.join(STAGE, "adv_map_phaseG_v0_1.json"))
    assert got == AMENDED_PHASE_G_MD5, ("BASE GUARD: the amended Phase G fragment is %s -- "
                                        "run tools/amend_phaseG_K351.py first" % got)''')

P("artifact-name",
'''      "artifact": "adversarial_map_v1_2.json",''',
'''      "artifact": "adversarial_map_v1_3.json",''')

P("assembled",
'''      "assembled": "2026-09-17, wuld.ink Cowork, K349",
      "successor_to": {
        "artifact": "adversarial_map_v1_1.json", "md5": BASE_V1_1_MD5, "bytes": 252665,
        "and_before_it": "adversarial_map_v1_0.json (FROZEN, %s)" % BASE_V1_0_MD5,
        "why_v1_2_and_not_v2_0": ("Every one of v1_1's 133 entries is inherited byte-for-byte; "
          "nothing is superseded, re-classed or re-pinned; the schema is unchanged. Phase G adds "
          "five entries at a locus kind the enum could not previously name. Adding covered surface "
          "is an addition, not a break -- the same line v1_1 took over v1_0, and it is the "
          "artifact's own line rather than canon's update_protocol, which governs CANON."),''',
'''      "assembled": "2026-09-18, wuld.ink Cowork, K351",
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
          "in `supersedes`."),''')

P("supersedes-note",
'''      "nodes_covered": len(primary_cov), "nodes_total": len(ids), "entries": len(entries),''',
'''      "fragment_amendments": {
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
      "nodes_covered": len(primary_cov), "nodes_total": len(ids), "entries": len(entries),''')

P("siblings-register",
'''      "fences": ("Nothing here authorizes a byte. (b) and (c) yields are intake candidates routing "
        "through staging -> cold-grade -> assembly inside a declared content cut; see "
        "adversarial_map_regen_queue_v0_1.json. (d) termini route to "
        "honest_residuals_register_v0_2.json."),
      "siblings": {"predecessor": "adversarial_map_v1_1.json",
                   "queue": "adversarial_map_regen_queue_v0_1.json",
                   "register": "honest_residuals_register_v0_2.json",''',
'''      "fences": ("Nothing here authorizes a byte. (b) and (c) yields are intake candidates routing "
        "through staging -> cold-grade -> assembly inside a declared content cut; see "
        "adversarial_map_regen_queue_v0_1.json. (d) termini route to "
        "honest_residuals_register_v0_4.json."),
      "siblings": {"predecessor": "adversarial_map_v1_2.json",
                   "queue": "adversarial_map_regen_queue_v0_1.json",
                   "register": "honest_residuals_register_v0_4.json",''')


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == BASE_MD5, "BASE GUARD: build_assembly_v1_2.py is %s" % got
    src = raw.decode("utf-8")
    for tag, old, new in PATCHES:
        n = src.count(old)
        assert n == 1, "anchor %r occurs %d times, expected exactly 1" % (tag, n)
        src = src.replace(old, new, 1)
    for tag, old, new in PATCHES:
        assert src.count(new) == 1, "patched text %r is not unique in the result" % tag
    out = src.encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "wb").write(out)
    compile(src, OUT, "exec")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), hashlib.md5(out).hexdigest()))
    print("  %d anchored patches, each unique before and after; compiles clean" % len(PATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
