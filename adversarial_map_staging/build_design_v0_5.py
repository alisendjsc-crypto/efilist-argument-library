#!/usr/bin/env python3
"""adversarial_map_design_v0_5.md = v0_4 + section 12 (K349).

v0_4 stays byte-identical; canon pins it and the v1_2 receipt cites it.

EVERY numeric token in the emitted section must be either a bound constant traceable to a
measurement file, or an explicitly allowed literal with the reason beside it. The K348 gate
caught a constant that was bound, gated and printed from its binding and still asserted
nothing, because its SOURCE was unrelated to its claim -- so the allow-list carries reasons,
not just values.
"""
import json, os, re, sys, hashlib, collections, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
V = None


def load_v():
    global V
    p = os.path.join(HERE, "adv_map_validator_v0_6.py")
    spec = importlib.util.spec_from_file_location("v6d", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    V = m


def rj(p):
    return json.loads(open(p, "rb").read().decode("utf-8"))


# numbers that are RULES or ENUM SIZES, with no measurement behind them, and why.
ALLOWED_LITERALS = {
    "0": "the target count for violations and advisories; a rule, not a measurement",
    "3": "the Q1-ratified per-locus entry cap, and '1 and 3' inside a verbatim note quotation",
    "15": "the anchor rule's word ceiling",
    "82": "the corpus node count, an invariant canon already pins",
    # structural: this document's own numbering and its cross-references
    "9": "cross-reference to design section 9", "10": "cross-reference to section 10",
    "11": "cross-reference to section 11, and the HR-11 bedrock id",
    "12": "this section's own number",
    "12.1": "subsection", "12.2": "subsection", "12.3": "subsection", "12.4": "subsection",
    "12.5": "subsection", "12.6": "subsection", "12.7": "subsection",
    "14": "the HR-14 bedrock id",
    # the operator-local date, asserted below against the measurement file's own date field
    "2026": "session date year", "09": "session date month", "17": "session date day",
    # session identifiers, not quantities
    "345": "session K345", "348": "session K348", "349": "this session, K349",
    # verbatim quotations FROM the corpus, which must not be re-derived or they stop being quotes
    "4": "inside the verbatim quotation 'session 4h-alt'",
    "6": "inside the verbatim quotation '6 source-vehicles'",
    "78": "inside the verbatim quotation 'the ratified delta 78->80 to 78->81'",
    "80": "same quotation", "81": "same quotation",
}


def main():
    load_v()
    M = rj(os.path.join(HERE, "measure_k349_v0_1.json"))
    CG = rj(os.path.join(HERE, "phaseG_control_v0_1.json"))
    CA = rj(os.path.join(HERE, "assembly_control_v0_2.json"))
    CR = rj(os.path.join(HERE, "register_control_v0_1.json"))
    G = rj(os.path.join(HERE, "adv_map_phaseG_v0_1.json"))
    A12 = rj(os.path.join(HERE, "adversarial_map_v1_2.json"))
    A11 = rj(os.path.join(HERE, "adversarial_map_v1_1.json"))

    nl = M["note_layer"]
    cl = M["confidence_layer"]
    be = M["bedrock_enrichment"]
    cm = CG["class_mix"]

    # ---- CONSTANTS: bound once, from the measurement that MEANS them ---------------
    C = {}
    C["note_nodes"] = nl["nodes"]
    C["note_words"] = nl["words_total"]
    C["reach_n"] = nl["reachable_n"]
    C["unreach_n"] = nl["unreachable_n"]
    C["unreach_words"] = nl["words_unreachable"]
    C["unreach_pct"] = nl["pct_words_unreachable"]
    C["conf_nodes"] = M["out_of_enum_fields"]["confidence"]
    C["badge_n"] = cl["badge_emitting_n"]
    C["graded_full"] = cl["graded_full_n"]
    C["ungraded"] = cl["ungraded_n"]
    C["authored"] = len(G["entries"])
    C["note_cov"] = G["meta"]["note_coverage"]
    C["cls_a"] = cm["counts"].get("a", 0)
    C["cls_b"] = cm["counts"].get("b", 0)
    C["prior"] = cm["prior_A_to_E"]
    C["pval"] = cm["p_two_sided"]
    C["d_prior"] = cm["d_prior"]
    C["d_p"] = cm["d_p"]
    C["already_bedrock"] = be["note_nodes_with_d_n"]
    C["min_headroom"] = M["entry_cap_headroom"]["min_headroom"]
    C["entries_v1_2"] = len(A12["entries"])
    C["entries_v1_1"] = len(A11["entries"])
    C["ctl_g"] = CG["summary"]["controls"]
    C["ctl_a"] = CA["summary"]["controls"]
    C["ctl_r"] = CR["summary"]["controls"]
    C["ctl_total"] = C["ctl_g"] + C["ctl_a"] + C["ctl_r"]
    C["parity_runs"] = CG["parity_runs"]
    C["selftest"] = 78
    C["selftest_prev"] = 62
    # distinct (node, locus) PAIRS, not distinct slot names -- there are only four of those
    C["variant_loci"] = len(set((e["target_id"], e["target_locus"]) for e in A12["entries"]
                                if V.variant_slot(e["target_locus"]) is not None))
    C["apparatus"] = len([k for k, v in G["meta"]["not_authored"].items() if v.startswith("(i)")])
    C["qualifier"] = len([k for k, v in G["meta"]["not_authored"].items() if v.startswith("(ii)")])

    # gate: every constant must equal what its measurement says
    assert C["reach_n"] + C["unreach_n"] == C["note_nodes"]
    assert C["authored"] + C["apparatus"] + C["qualifier"] == C["note_nodes"]
    assert C["cls_a"] + C["cls_b"] == C["authored"]
    assert C["entries_v1_2"] - C["entries_v1_1"] == C["authored"]
    assert C["badge_n"] + C["graded_full"] == C["conf_nodes"]
    assert C["ctl_total"] == C["ctl_g"] + C["ctl_a"] + C["ctl_r"]
    # the date literals above are allowed ONLY because they equal the measurement's own date
    assert M["date_operator_local"] == "2026-09-17", "date literals in the allow-list are stale"

    S = """
## 12. The `note` layer, the reachability finding, and the fifth relation kind (K349, 2026-09-17) — amends §9, §10 and §11

`adversarial_map_design_v0_4.md` stays on disk byte-identical; canon pins it at `design_pin_v0_4`
and the v1_2 receipt cites it. This section is the amendment, on the terms §§10 and 11 were.

### 12.1 `note` is a map target, NARROWLY (Josiah, K349 — delegated to the build seat)

K345 named `note` IN SCOPE and never discharged its own reservation: the shape is not a
response and the anchor rule assumes one. The reservation was real and the disposition was put
to Josiah with the classification already measured, because a scope question deserves the
`ccclxviii` discipline as much as a class distribution does — decide what the population looks
like before deciding what to do with it.

Of the {note_nodes} notes, **{apparatus} are authoring apparatus** — sibling taxonomy, build-pass
provenance (*"first taxonomically committed in session 4h-alt … across 6 source-vehicles in
build-pass batches 1 and 3"*), a ratification-delta line (*"inclusion bumps the ratified delta
78->80 to 78->81"*), and a TIER NOTE addressed to a future editor. **{qualifier} is a legitimate
scope qualifier**, checked against its own `#long` rather than assumed. The remaining
**{authored} carry a claim or a concession the corpus would have to defend**, and those are
Phase G.

**The ruling is NARROW because the class law does not survive the other {apparatus_plus}.**
"The strongest continuation a maximally competent hostile interlocutor deploys against our text"
is malformed against a build-accounting line. Authoring against all {note_nodes} would have
produced {note_nodes} entries and four of them would have been inflation, which is the `82/82`
problem in a new artifact — and the kickoff named that risk in advance. `note_coverage` is
therefore **{note_cov}**, declared and deliberately partial: a phase that cannot say what it has
not done is how a coverage claim becomes misleading.

Josiah delegated 0a to this seat rather than ruling it. That is recorded as a delegation, not as
a ruling, because the difference matters to whoever reads this next.

### 12.2 THE FINDING: `note` is not an independent field. It is a dependent of `confidence`.

`combined.html` emits the `[NOTE]` button INSIDE `if (conf !== 'full')`, where
`conf = obj.confidence || 'full'`, and `toggleNote` has exactly one caller — that button. So a
note on a node graded `full`, or ungraded, has its `<div>` emitted at `display:none` with
nothing in the artifact able to reveal it.

**{unreach_n} of the {note_nodes} notes are structurally unreachable by any reader: {unreach_words}
of {note_words} words, {unreach_pct}% of the layer.** They are the two longest. One of them is
`solipsism`, whose note is the text that *explains* its `confidence:full` — and that value is
exactly what suppresses the button that would let anyone read the explanation.

So the CSS class name `confidence-note` was never the misnomer; the FIELD name `note` is. The
layer is architecturally a confidence disclosure, which is also why {already_bedrock} of the
{note_nodes} note-bearing nodes already carry a (d) in the successor assembly against
{corpus_d_rate} corpus-wide — the corpus puts a note where it knows it is on hard ground.

### 12.3 `confidence` is OUT as a map target and IN as a regen candidate (Josiah, K349)

It carries no corpus text, so the anchor rule has nothing to bite on and it cannot be a map
entry. It is ruled explicitly rather than by silence, and on different grounds from
`objectionSubforms`, which K345 ruled out for having **no render site at all**. `confidence` has
one, and the handoff's premise that "no text reaches the reader" is false: the badge emits the
literal strings STRONG and PROVISIONAL for {badge_n} nodes.

What is filed instead is a regen candidate with three legs, each measured:

1. `full` renders **identically to absent**. {graded_full} nodes were affirmatively graded `full`
   and {ungraded} were never graded, and a reader cannot tell them apart.
2. `provisional` renders as a {opacity} opacity band on the long response with **no label**,
   which a reader cannot interpret and a screen reader cannot convey at all.
3. The grade silently controls whether a node's note is reachable — §12.2. A field documented
   nowhere as a visibility control is one.

### 12.4 Apparatus cannot satisfy coverage (K349 ruling, made explicitly)

`coverage` keyed on `target_id` alone, so a node whose only entry sat at `#note` would have
counted as covered. `coverage` is the claim that every node's ARGUMENT was adjudicated, and a
note is apparatus attached to a node, not the node's argument. It is now restricted to argued
loci in the validator, and stated POSITIVELY in the assembly builder — v1_1 computed primary
coverage as "not a variant locus", which a new locus kind walks straight into.

That is `ccclxxi` a second time in three sessions, and it was found by READING the builder rather
than trusting that the K348 migration had covered it. **Measured blast radius: zero.** No shipped
artifact carries a note entry, so no verdict moves; what changes is what the NEXT phase can claim.

### 12.5 The fifth relation kind: `conditions` (Josiah, K349)

> **A conditions B**: A's resolution changes the FORCE of B's open question without creating or
> dissolving it. B stays askable either way; what moves is how much turns on the answer.

HR-14+HR-11 is its first instance and the reason it was ratified: K348 recorded that pair in the
register's AUDIT rather than declaring it, because none of `depends_on / stronger_than /
sibling_of / independent_of` states it. The register is rebuilt at v0_3 with the relation
declared — and with the vocabulary made an **enforced allowlist** rather than the five-line
comment it had been.

The same pass found that `build_register.py`'s own comment claims *"the audit below refuses to
write if any mechanically-derived adjacency candidate is undeclared."* It did not. It appended an
audit line and wrote anyway. The claim was true by luck — the undeclared set has always been
empty — and it is a gate now. That is `cccli` in its purest form, and one more instance of it
discharged.

### 12.6 `ccclxxii` — A RENDER SITE IS NOT REACHABILITY, AND THE DIFFERENCE IS DATA-DEPENDENT

Two scope audits have now asked *does this field have a render site?* and treated the answer as
settling whether readers meet the text. K345 ruled `objectionSubforms` OUT because it has none.
This session came within one ruling of treating `note` as uniformly rendered because it has one.

**A render site can be nested inside a condition on a DIFFERENT field, so whether text reaches a
reader is a fact about the DATA, not about the code.** The predicate was being evaluated
statically when it is data-dependent, and the error is silent in both directions: it over-counts
a field whose gate is usually closed and under-counts one whose gate is usually open.

The rule: to establish that shipped text reaches a reader, find the render site, **enumerate every
condition gating it, and evaluate those conditions over the actual corpus** — then report the
count, not the existence. `ccclviii`'s family (measure the state you think you measured), narrowed
to the specific case where the instrument is a static read of a dynamic predicate.

### 12.7 What was run

Validator v0_6, self-test **{selftest}/{selftest}** against v0_5's {selftest_prev}, and v0_6
reproduces **every** v0_5 verdict across **{parity_runs} runs** over the shipped artifacts, both
corpora and all three modes, with **{zero} divergences**. `adversarial_map_v1_2.json` carries
{entries_v1_2} entries against v1_1's {entries_v1_1}, 82/82 primary, 39/39 variant, {note_cov}
note, and passes `--assembly` at {zero} violations and {zero} advisories. Phase G's class mix is
{cls_a}(a)/{cls_b}(b) — a+d {a_or_d}/{authored} = {ad_rate} against the A–E prior of {prior},
exact two-sided p = {pval}; zero (d) against a prior of {d_prior}, p = {d_p}.

**Both p-values are stated with their power, because at n={authored} the gate is nearly
unfalsifiable and saying it passed without saying that would be the flattery version of a
control.** The structural reason for zero (d) is measured rather than argued: {already_bedrock} of
the {authored} authored nodes already carry a (d) at a primary locus on the very bedrock a note
entry would route to, so a second one would restate a registered residue rather than route a new
one. Entry-cap headroom on every note-bearing node was checked before authoring — minimum
{min_headroom} — so the node bound was NOT extended and no ruling was owed.

**{ctl_total} controls across three batteries, all passing**: {ctl_g} on Phase G and the patch,
{ctl_a} on the assembly, {ctl_r} on the register. Two of them had to be repaired before they
earned the name — one displayed a violation it had not matched on, and one refused for the
harness's reason rather than the guard's.
"""
    subs = dict(C)
    subs["apparatus_plus"] = C["apparatus"] + C["qualifier"]
    subs["corpus_d_rate"] = "%d of 82" % be["corpus_nodes_with_d_n"]
    subs["a_or_d"] = cm["a_or_d"]
    subs["ad_rate"] = round(cm["a_or_d"] / cm["n"], 4)
    subs["zero"] = 0
    subs["opacity"] = "70%"
    body = S.format(**subs)

    # ---- THE CONSTANT GATE ------------------------------------------------------
    bound = set()
    for v in subs.values():
        for tok in re.findall(r"\d+(?:\.\d+)?", str(v)):
            bound.add(tok)
    unaccounted = []
    for tok in re.findall(r"\d+(?:\.\d+)?", body):
        if tok in bound or tok in ALLOWED_LITERALS:
            continue
        unaccounted.append(tok)
    if unaccounted:
        print("REFUSING TO WRITE -- %d numeric token(s) neither bound nor allowed: %s"
              % (len(unaccounted), sorted(set(unaccounted))))
        return 1
    print("  constant gate: %d distinct numeric tokens, all bound or allowed"
          % len(set(re.findall(r"\d+(?:\.\d+)?", body))))

    base = open(os.path.join(HERE, "adversarial_map_design_v0_4.md"), "rb").read()
    assert hashlib.md5(base).hexdigest() == "4315ff24d3c40e0234586fce87fb8cfd", "v0_4 moved"
    out = base.decode("utf-8").rstrip("\n") + "\n" + body.rstrip() + "\n"
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "adversarial_map_design_v0_5.md")
    b = out.encode("utf-8")
    open(dest, "wb").write(b)
    print("wrote %s  %s  %d B" % (dest, hashlib.md5(b).hexdigest(), len(b)))
    assert hashlib.md5(open(os.path.join(HERE, "adversarial_map_design_v0_4.md"), "rb").read()
                       ).hexdigest() == "4315ff24d3c40e0234586fce87fb8cfd"
    print("  v0_4 byte-identical: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
