#!/usr/bin/env python3
"""build_design_v0_4.py -- emits adversarial_map_design_v0_4.md from v0_3 plus section 11.

v0_3 stays on disk byte-identical: canon pins it at design_pin_v0_3 and the Phase F receipt
cites it. Nothing is rewritten. Section 11 amends sections 9 and 10, and a pointer is inserted
into each so a reader cannot author against the superseded text by accident.

ccclxii discipline, taken one step further than v0_3 took it: every numeric constant in section
11 is BOUND ONCE below and gated against measure_k348_v0_1.json, AND the emitter then extracts
every numeric token from the finished section and refuses to write if one of them is not a bound
constant or an explicitly allowed literal. v0_3's docstring claimed that second half; its code
asserted only that no placeholder survived. This file makes the claim true.

Repo-relative. --out <dir> to emit elsewhere.
"""
import os, sys, json, re, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MEAS_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_design_v0_4.md")

BASE = os.path.join(_HERE, "adversarial_map_design_v0_3.md")
raw = open(BASE, "rb").read()
assert hashlib.md5(raw).hexdigest() == "eed4b2af42b1ad2235cf6a6a22974ea9", "design v0_3 base guard FAILED"
src = raw.decode("utf-8")

M = json.load(open(os.path.join(MEAS_DIR, "measure_k348_v0_1.json"), encoding="utf-8"))


def at(path):
    cur = M
    for k in path.split("/"):
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    return cur


def n_at(path):
    return len(at(path)) if isinstance(at(path), list) else at(path)


# name -> (rendered, json path or literal value). Bound once; gated; printed from the binding.
C = {
 "F_A":        ("26",     "inheritance/phaseF_class_counts/a"),
 "F_B":        ("6",      "inheritance/phaseF_b_total"),
 "CURE_N":     ("20",     "inheritance/cured_count"),
 "AGG_N":      ("2",      "inheritance/aggravated_count"),
 "MULTI_LOCI": ("7",      "gate5/assembly_multi_entry_loci"),
 "SAME_CLAUSE": ("0",     "gate5/assembly_same_clause_pairs"),
 "ST_V05":     ("62",     "gate5/validator_v0_5_self_test"),
 "ST_V04":     ("60",     "gate5/validator_v0_4_self_test"),
 "PARITY_RUNS": ("72",    "gate5/parity_runs"),
 "PARITY_DIFF": ("0",     "gate5/parity_divergences"),
 "CAP":        ("3",      "entry_cap/per_locus_cap"),
 "RBR_E":      ("6",      "entry_cap/red_button_repugnant/entries"),
 "RBR_V":      ("2",      "entry_cap/red_button_repugnant/variant_loci"),
 "BOUND_OLD":  ("5",      "entry_cap/red_button_repugnant/bound_k345"),
 "BOUND_NEW":  ("9",      "entry_cap/red_button_repugnant/bound_k348"),
 "VIOL_OLD":   ("1",      "@len:entry_cap/violations_under_k345_bound"),
 "VIOL_NEW":   ("0",      "@len:entry_cap/violations_under_k348_bound"),
 "NODES":      ("82",     "entry_cap/nodes_total"),
 "MAX_NODE":   ("6",      "entry_cap/max_entries_at_any_node"),
 "MAX_LOCUS":  ("3",      "entry_cap/max_entries_at_any_locus"),
 "ENTRIES":    ("133",    "assembly/entries"),
 "VAR_HIT":    ("39",     "assembly/variant_loci_hit"),
 "VAR_TOT":    ("39",     "assembly/variant_loci_total"),
 "INHERITED":  ("90",     "assembly/inherited_from_v1_0"),
 "SUPERSEDED": ("3",      "assembly/superseded"),
 "CL_A":       ("66",     "assembly/class_counts/a"),
 "CL_B":       ("27",     "assembly/class_counts/b"),
 "CL_C":       ("1",      "assembly/class_counts/c"),
 "CL_D":       ("39",     "assembly/class_counts/d"),
 "BASE_RATE":  ("0.7634", "assembly/base_rate"),
 "UNION_SH":   ("0.7895", "assembly/union_share"),
 "UNION_P":    ("0.5408", "assembly/union_two_sided_p"),
 "NEW_SH":     ("0.7907", "assembly/new_share"),
 "NEW_P":      ("0.8575", "assembly/new_two_sided_p"),
 "NODE_CLASH": ("16",     "partition/node_level_clashes"),
 "LOCUS_CLASH": ("0",     "partition/locus_level_clashes"),
}
for name, (rendered, path) in C.items():
    got = n_at(path[5:]) if path.startswith("@len:") else at(path)
    assert abs(float(rendered) - float(got)) < 1e-9, \
        "CONSTANT %s: doc says %s, measurement says %s" % (name, rendered, got)
print("constants gated: %d of %d against %s" % (len(C), len(C), os.path.basename(
    os.path.join(MEAS_DIR, "measure_k348_v0_1.json"))))

S11 = """

---

## 11. Inheritance cuts three ways, the stopping rule as a biconditional, and the entry-cap ruling (K348, 2026-09-17) — amends §9 and §10

`adversarial_map_design_v0_3.md` stays on disk byte-identical; canon pins it at `design_pin_v0_3`
and the Phase F receipt cites it. This section is the amendment, on the same terms §§9 and 10 were.

### 11.1 Inheritance cuts BOTH ways — and the honest count is three

§10.4 states one direction: the whole-node reading CURES a locus-local defect, because the strongest
continuation against a variant is usually the one its primary ladder already answers. Phase F bears
that out at scale — **{CURE_N} of its {F_A} (a) entries are answered by a locus of the variant's OWN
node**, which is inheritance curing, measured rather than asserted. `next-person-cure-cancer#archetypeVariants.sophisticate`
is the clean worked example: the variant aims a deprivation argument past its target, the node's
`#long` frames the same refusal on consent, and the move is met.

**It also AGGRAVATES, and §10.4 does not say so.** Two of Phase F's {F_B} (b) entries exist only
because of what the locus inherits:

- `just-depressed#archetypeVariants.sophisticate` disavows depressive realism while the node's
  `#short` and `#medium` assert it as evidence. The sophisticate text is **correct standing alone**
  and is made false-in-context by its own node.
- `violence-as-reductio#archetypeVariants.drifter` asserts an incompatibility between caring about
  suffering and causing harm that the node's own `#long` surrenders when it concedes the bridge is
  held by founders.

**And the third way is the one neither direction names: inheritance can simply FAIL to cure.** The
remaining (b) entries are locus-local defects that survive the whole-node reading — the node has no
answer to supply, or supplies one the locus contradicts. `bitter-childhood#archetypeVariants.defender`
is the shape: no locus in the corpus meets the move, because the corpus's own rule condemns it.

**The rule.** Read the whole node before classing a variant, and record WHICH of the three the node
did — cured, aggravated, or failed to cure. A grounds field that says only "not locus-local" has not
said which, and the difference decides the class: cured is (a), aggravated is (b) and the repair is
at the NODE rather than at the locus, failed-to-cure is (b) and the repair is at the locus. Counted
across Phase F: **{CURE_N} cured, {AGG_N} aggravated**, the rest failed to cure.

### 11.2 Anti-inflation gate 5 is a BICONDITIONAL, and §10.3 reads one-directional

§10.3 states the stopping rule as a question to answer and record: *is there a second continuation at
this locus that engages a different clause and would not be met by the same reply?* The prose reads
as though only an `open` declaration carries an obligation. It does not.

**`open` ⇔ ≥2 entries.** The declaration records the ANSWER to that question, so a locus
carrying two entries has answered *yes* and cannot also declare itself closed, exactly as a locus
carrying one and declaring `open` has not discharged the claim it made. The first cut of the gate at
validator v0_4 asserted only the forward direction, and a mutation declaring the open locus `closed`
did not trip it — **a failing control convicted the gate's author**, which is the whole reason the
control exists.

The minimal mechanisation of *engages a different clause*: two entries at one locus may not have one
anchor a substring of the other. Measured across the successor assembly, **{SAME_CLAUSE} same-clause
pairs over {MULTI_LOCI} multi-entry loci**, so the sub-check is confirmatory rather than a repair,
and it is scoped inside the declaration so no frozen receipt can be disturbed by it.

### 11.3 The node entry cap scales by the per-locus cap, not by one slot per locus (Josiah, K348)

§9.4 item 2 set a second, node-level bound at `{CAP} + (variant loci on that node)`. That was written
when **no variant entry existed anywhere**, and it reserved a single slot per variant locus while the
per-locus cap allows {CAP}. So the node bound and gate 5 disagree BY CONSTRUCTION wherever a variant
locus legitimately opens: §11.2 says author the second continuation, and the node bound refuses to
hold it.

`red-button-repugnant` is where the disagreement surfaced. It carries {RBR_E} entries in the
successor assembly — three inherited from the frozen v1_0 and three from Phase F, {RBR_V} of them at
one variant locus gate 5 declared open — against a §9.4 bound of {BOUND_OLD}. Every one is legal
per-locus and the node is illegal per-node.

**THE RULING (Josiah, K348).** The node bound becomes `{CAP} + {CAP}×(variant loci on that node)`:
the per-locus cap applied to variants exactly as it already applies to primaries. **A node carrying
no variants still keeps the Q1-ratified bound of {CAP} exactly**, which is the property the §9.4
amendment was written to preserve and this one preserves untouched.

The alternative on the table was dropping one of the {RBR_E} on the merits, in the assembly only. It
was declined: the bound and gate 5 are in structural disagreement, and dropping a sound entry to
satisfy an arithmetic fixed before the thing it now constrains existed repairs the symptom.

Blast radius, measured across the assembly's {ENTRIES} entries over {NODES} nodes: **{VIOL_OLD} node
violates the old bound and {VIOL_NEW} violate the new one**. The heaviest node in the corpus carries
{MAX_NODE} entries and the heaviest locus carries {MAX_LOCUS}, so the amendment buys headroom where
gate 5 needs it and nowhere else. Implemented at validator v0_5, whose self-test runs {ST_V05} cases
against v0_4's {ST_V04}, and which reproduces every v0_4 verdict across {PARITY_RUNS} runs over every
shipped artifact and both corpora with {PARITY_DIFF} divergences.

### 11.4 The partition invariant belongs to the LOCUS too, and that was invisible until a fragment set crossed it

v1_0's builder refused to write unless the fragments PARTITIONED the corpus: no node claimed by two
phases. That invariant is sound for phases A–E, which carve the {NODES} nodes between them. Phase F
authors variant loci on nodes A–E already cover, so at the successor assembly's fragment set the
node-level form fails **{NODE_CLASH} ways by construction** — while the property it was actually
protecting, that no two phases adjudicate the same text, is perfectly intact: **{LOCUS_CLASH} loci
are claimed by two phases**.

This is the same unit migration §9.4 made for the entry cap, one layer over, and it has the same
cause: an invariant written when the locus did not exist as a unit states itself over the node
because the node was the only unit there was. The general form is worth carrying: **when a ruling
moves a gate's unit, every OTHER invariant stated over the old unit is a candidate for the same move,
and nothing fails until a fragment set finally crosses it.** The successor assembly states the
migrated invariant in its own meta, with the {NODE_CLASH} nodes listed, so the next reader meets the
fact rather than rediscovering it.

### 11.5 What the successor assembly is

`adversarial_map_v1_1.json`: {ENTRIES} entries covering all {NODES} nodes at the primary ladder and
all {VAR_HIT} of {VAR_TOT} archetypeVariants loci, classes {CL_A}a / {CL_B}b / {CL_C}c / {CL_D}d,
pinned to the post-cut corpus. {INHERITED} entries are inherited from v1_0 unchanged and {SUPERSEDED} are superseded by
Phase R because the v4.1.0 cut destroyed their anchors. It is a **revision**, not a re-mapping, which
is why it is v1_1: the schema is unchanged and no inherited entry is re-classed.

Class mix against the A–E base rate of {BASE_RATE}, per §10.4's detection rule: the union runs
{UNION_SH} (two-sided p = {UNION_P}) and the disjoint R+F set runs {NEW_SH} (p = {NEW_P}). Both sit
inside the prior. **The union figure is reported and does not carry weight**: the union CONTAINS the
base, so testing it against a rate computed from its own subset is not an independent test. Saying
which of two figures is the real one is part of the gate.
"""
for k, (rendered, _p) in C.items():
    S11 = S11.replace("{" + k + "}", rendered)
assert not re.search(r"\{[A-Z0-9_]+\}", S11), re.findall(r"\{[A-Z0-9_]+\}", S11)

# A number that is not a bound constant cannot appear in the section.
ALLOWED = {c[0] for c in C.values()} | {
 "0", "1", "2", "3",           # section/item numbers, small prose enumerations, and the
                               # gate-5 threshold, which is a RULE constant with no measurement
                               # behind it -- binding it to a measured 2 would print the right
                               # digit and assert nothing
 "9.4", "10.3", "10.4", "11.1", "11.2", "11.3", "11.4", "11.5",
 "0.3", "0.4", "1.1",          # never emitted alone, but tokenisation of the above is greedy-safe
 "2026", "09", "17", "348", "0_3", "0_4", "0_5", "1_0", "1_1", "4.1.0", "5",
 "10", "11",                   # section numbers: "sections 9 and 10", "## 11."
}
tokens = set(re.findall(r"\d+(?:[.,_]\d+)*", S11))
unbound = sorted(t for t in tokens if t not in ALLOWED)
assert not unbound, "UNBOUND NUMERIC LITERAL(S) in section 11: %s" % unbound
print("numeric tokens in section 11: %d, all bound or allowed" % len(tokens))

P9 = """
> **Amended K348 (§11.3):** the node-level entry bound in item 2 below is superseded. It is now
> `3 + 3×(variant loci on that node)` — the per-locus cap applied to variants as it already is to
> primaries — because the one-slot-per-locus form contradicts anti-inflation gate 5 wherever a
> variant locus legitimately opens. A node with no variants is unchanged at 3. **Read §11.3 before
> using the bound in item 2.**
"""
a9 = "### 9.4 The ruling"
assert src.count(a9) == 1
src2 = src.replace(a9, P9.strip() + "\n\n" + a9)

P10 = """
> **Amended K348 (§11):** `open` ⇔ ≥2 entries is a **biconditional** — a locus carrying two entries
> cannot declare itself closed (§11.2) — and §10.4's inheritance principle runs in three directions,
> not one (§11.1). **Read §11 before authoring against this section.**
"""
a10 = "**Anti-inflation gate 5 — the stopping rule.**"
assert src2.count(a10) == 1
src3 = src2.replace(a10, P10.strip() + "\n\n" + a10)

out = src3 + S11
b = out.encode("utf-8")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "wb").write(b)
print("%s  %s  %d bytes  (v0_3 was %d, untouched)"
      % (os.path.basename(OUT), hashlib.md5(b).hexdigest(), len(b), len(raw)))
