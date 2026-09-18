"""K347 -- derive adv_map_validator_v0_4.py from v0_3 by anchored, single-occurrence
replacement.  v0_3 stays byte-identical on disk: the Phase F defect register's receipt
and canon's validator_pin_v0_3 both name it.

v0_4 adds ONE check -- `stopping-rule`, anti-inflation gate 5 (design v0_3 s10.3),
gated when declared, on the pattern s9.4.3 set for variant_coverage.

Repo-relative: resolves the repo from its own location.  --out <dir> to emit elsewhere.
"""
import os, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K347_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_3.py")
DEST = os.path.join(OUT, "adversarial_map_staging", "adv_map_validator_v0_4.py")

BASE = "eb254a091a94b860a95f0b06b2074563"
src = open(SRC, "rb").read()
got = hashlib.md5(src).hexdigest()
assert got == BASE, "BASE GUARD FAIL: %s != %s" % (got, BASE)
t = src.decode("utf-8")
assert "\r" not in t, "CR present in v0_3"

PATCHES = []
def P(name, old, new):
    PATCHES.append((name, old, new))

# 1 -- docstring: the new check, in the check list
P("doc-checklist",
'''  variant-coverage       IF meta declares variant_coverage "<hit>/<total>", it must equal computed''',
'''  variant-coverage       IF meta declares variant_coverage "<hit>/<total>", it must equal THAT FILE's
                         own variant loci over the corpus total   [K347/ccclxx: was all loaded files]
  stopping-rule          NEW (gate 5) -- IF meta declares locus_closure, the per-locus stopping
                         decision is gated: the declared key set must equal the loci this FILE
                         carries entries for; values in {closed, open}; an `open` claim is
                         discharged by having authored the second continuation, and `closed` by
                         having authored exactly one: open <-> >=2 entries is a biconditional;
                         and two entries at one locus may not sit on the same clause
                         (neither anchor a substring of the other)''')

# 2 -- docstring: provenance line was stale, naming fewer phases than PHASES accepts
P("doc-provenance-stale",
'''  provenance             phase in {A,B1,B2,C,D,E}; date ISO (YYYY-MM-DD...); seat nonempty''',
'''  provenance             phase in PHASES {A,B1,B2,C,D,E,F,R}; date ISO (YYYY-MM-DD...); seat nonempty''')

# 3 -- docstring: version note
P("doc-version",
'''v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".''',
'''v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".
v0_4 (K347): anti-inflation gate 5, the stopping rule, becomes checkable.  Design v0_3
s10.3 made the stop an auditable claim rather than a silence and left the gate owed;
a Phase F fragment declaring a closure the validator did not read would be `cccli`
exactly -- a compliance rule asking a writer to do the right thing at write time.
v0_3 IS RETAINED UNCHANGED beside this file for the same reason v0_2 was: the Phase F
defect register's receipt names it.''')

# 4 -- the check itself, inside the per-file loop (the declaration is a claim about
#      THIS fragment's own authoring, so it is gated against this file's entries)
P("stopping-rule-check",
'''        metas.append((p, meta))
        for i, e in enumerate(doc["entries"]):''',
'''        # K346 gate 5 (design v0_3 s10.3), gated when declared, on the s9.4.3 pattern.
        # `locus_closure` records the stopping decision per locus, so the stop is an
        # auditable claim rather than a silence:
        #   "<target_id>#<locus>": "closed"  no second continuation at this locus that
        #                                    engages a different clause and would not be
        #                                    met by the same reply
        #   "<target_id>#<locus>": "open"    one does exist -- and the claim is discharged
        #                                    by AUTHORING it, to the cap, not by saying so
        # Gated against THIS FILE's entries: a fragment declares its own authoring.
        lc = meta.get("locus_closure")
        if isinstance(lc, dict):
            here = {}
            for e in doc["entries"]:
                if isinstance(e, dict) and isinstance(e.get("target_id"), str) \\
                        and isinstance(e.get("target_locus"), str):
                    here.setdefault("%s#%s" % (e["target_id"], e["target_locus"]), []).append(e)
            note("stopping-rule", set(lc) == set(here),
                 "%s: declared-not-authored %r / authored-not-declared %r"
                 % (p, sorted(set(lc) - set(here))[:3], sorted(set(here) - set(lc))[:3]))
            for k in sorted(lc):
                v = lc[k]
                ents = here.get(k, [])
                note("stopping-rule", v in ("closed", "open"),
                     "%s: %s declares %r, not closed|open" % (p, k, v))
                if v == "open":
                    note("stopping-rule", len(ents) >= 2,
                         "%s: %s declares open with %d entries -- an open stop is discharged "
                         "by authoring the second continuation" % (p, k, len(ents)))
                elif v == "closed":
                    # open <-> >=2 entries is a BICONDITIONAL: the declaration records the answer
                    # to "is there a second continuation here", so a locus carrying two entries
                    # answered yes and cannot also declare closed.
                    note("stopping-rule", len(ents) == 1,
                         "%s: %s declares closed with %d entries -- a second continuation was "
                         "authored here, so the recorded answer was yes" % (p, k, len(ents)))
                anchors = [e.get("target_anchor") for e in ents
                           if isinstance(e.get("target_anchor"), str)]
                for ai, a1 in enumerate(anchors):
                    for a2 in anchors[ai + 1:]:
                        note("stopping-rule", a1 not in a2 and a2 not in a1,
                             "%s: %s carries two entries on the SAME clause (%r / %r)"
                             % (p, k, a1[:28], a2[:28]))
        metas.append((p, meta))
        for i, e in enumerate(doc["entries"]):''')

# 5 -- report every run, gate only when declared
P("stopping-rule-report",
'''    out("variant-coverage: %s archetypeVariants loci carry >=1 entry" % vc)''',
'''    out("variant-coverage: %s archetypeVariants loci carry >=1 entry" % vc)
    decl_n = sum(len(m["locus_closure"]) for _p, m in metas
                 if isinstance(m.get("locus_closure"), dict))
    out("stopping-rule: %d/%d loci carrying entries declare a closure decision"
        % (decl_n, len(per_id_locus)))''')

# 6 -- self-test: gate 5 cases.  A gate with no failing control is not a gate.
P("self-test-cases",
'''    passed = sum(1 for _n, g, _c in results if g)''',
'''    # --- v0_4 additions: gate 5, the stopping rule ---
    soph = vent("sophisticate", "carrying its own distinct commitment")
    defe = vent("defender", "naming the bad faith")
    soph_key = "node-y#archetypeVariants.sophisticate"
    defe_key = "node-y#archetypeVariants.defender"
    # 10. a correct declaration passes, and an undeclared fragment is untouched by the gate
    clean("k347-closure-declared-true", [soph, defe],
          meta_extra={"locus_closure": {soph_key: "closed", defe_key: "closed"}})
    clean("k347-closure-undeclared-is-not-gated", [soph, defe])
    # 11. the key set must equal the loci this file actually authored, both ways
    case("k347-closure-misses-an-authored-locus", [soph, defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "closed"}})
    case("k347-closure-declares-an-unauthored-locus", [soph], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "closed", defe_key: "closed"}})
    # 12. an `open` stop is discharged by authoring, not by declaring
    case("k347-open-with-one-entry", [soph], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "open"}})
    clean("k347-open-with-two-distinct-clauses",
          [soph, vent("sophisticate", "sophisticate variant for node y"),
           defe],
          meta_extra={"locus_closure": {soph_key: "open", defe_key: "closed"}})
    # 12b. the biconditional's other direction: two entries cannot declare closed
    case("k347-closed-with-two-entries",
         [soph, vent("sophisticate", "sophisticate variant for node y"), defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "closed", defe_key: "closed"}})
    # 13. two entries at one locus may not sit on the same clause
    case("k347-two-entries-same-clause",
         [soph, vent("sophisticate", "its own distinct commitment"), defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "open", defe_key: "closed"}})
    # 15. ccclxx: a declaration is gated against ITS OWN file, so the verdict cannot move
    #     with how many sibling files the run happens to load. This control FAILS on v0_3.
    pA = write_map("k347_two_file_a.json", [soph], meta_extra={"variant_coverage": "1/2"})
    pB = write_map("k347_two_file_b.json", [defe], meta_extra={"variant_coverage": "1/2"})
    okA, vA, _adA = validate([pA], cpath, out=lambda s: None)
    okJ, vJ, _adJ = validate([pA, pB], cpath, out=lambda s: None)
    good_ind = okA and okJ
    results.append(("k347-declaration-invocation-independent", good_ind, "variant-coverage"))
    print("%s . self-test [k347-declaration-invocation-independent] expects PASS solo AND joint -> %s"
          % ("PASS" if good_ind else "FAIL", (vA + vJ)[:2]))

    # 14. the value enum
    case("k347-closure-bad-value", [soph, defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "sealed", defe_key: "closed"}})

    passed = sum(1 for _n, g, _c in results if g)''')


# 7 -- ccclxx: a per-file declaration gated against a globally-computed value
P("file-entries-accumulator",
"""    all_entries = []
    metas = []""",
"""    all_entries = []
    metas = []
    file_entries = {}""")

P("variant-coverage-per-file",
"""    vc = "%d/%d" % (len(set(var_loci_hit)), len(var_loci_total))
    for p, meta in metas:
        if "variant_coverage" in meta:
            note("variant-coverage", meta["variant_coverage"] == vc,
                 "%s: declared %r vs computed %r" % (p, meta["variant_coverage"], vc))""",
"""    vc = "%d/%d" % (len(set(var_loci_hit)), len(var_loci_total))
    # K347 (ccclxx): variant_coverage is declared BY A FILE, so it is gated against THAT
    # FILE's own entries -- as class_counts and coverage_distinct_ids already are. Gating a
    # per-file declaration against a figure summed over every loaded file makes the verdict
    # depend on how many files the run happened to load: a fragment whose declaration is
    # true alone fails beside its sibling, and the same bytes pass or fail by invocation.
    # The all-loaded-files figure is still REPORTED, on the line below.
    for p, meta in metas:
        if "variant_coverage" in meta:
            own = set()
            for e in file_entries.get(p, []):
                if isinstance(e, dict) and isinstance(e.get("target_locus"), str) \\
                        and variant_slot(e["target_locus"]) is not None:
                    own.add((e.get("target_id"), e["target_locus"]))
            own_vc = "%d/%d" % (len(own), len(var_loci_total))
            note("variant-coverage", meta["variant_coverage"] == own_vc,
                 "%s: declared %r vs this file's %r (all loaded files: %s)"
                 % (p, meta["variant_coverage"], own_vc, vc))""")

P("file-entries-record",
"""        metas.append((p, meta))
        for i, e in enumerate(doc[\"entries\"]):""",
"""        metas.append((p, meta))
        file_entries[p] = doc[\"entries\"]
        for i, e in enumerate(doc[\"entries\"]):""")

for name, old, new in PATCHES:
    n = t.count(old)
    assert n == 1, "ANCHOR %s occurs %d times, expected 1" % (name, n)
    t = t.replace(old, new)

out_b = t.encode("utf-8")
assert b"\r" not in out_b, "CR in output"
assert all(c < 128 for c in out_b), "non-ASCII byte in output"
os.makedirs(os.path.dirname(DEST), exist_ok=True)
open(DEST, "wb").write(out_b)
print("wrote %s  md5 %s  bytes %d  patches %d"
      % (DEST, hashlib.md5(out_b).hexdigest(), len(out_b), len(PATCHES)))
