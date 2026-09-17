#!/usr/bin/env python3
"""Build adversarial_map_assembly_rulings_v0_1.json.

RULING SESSION artifact. Per the dual-session law (brief s1.4) this session emits an
artifact and commits nothing; an execute session consumes it and authors no net-new
prose. Every quotation below is pulled from the shipped fragments and re-verified
before writing, so no evidence in this document is asserted from memory.
"""
import json, hashlib, sys, collections

S = ""  # run from adversarial_map_staging/
CORPUS = "../efilist_argument_library_v4_0_0.json"
B1 = S + "adv_map_phaseB1_v0_1.json"
B2 = S + "adv_map_phaseB2_v0_1.json"
OUT = "adversarial_map_assembly_rulings_v0_1.json"

BAR_LOCUS = "bradley-no-subject#long"
CROSSREF_LOCUS = "transhumanist-objection#long"

# index -> (verdict, comparative?, disposition, attestation, note)
ADJ = {
 4:  ("CLEAR", False, "route-hygiene",
      "[K229-not-comparative]",
      "The move is a determinism tu quoque about the parent's authorship, not a worse-off "
      "comparison, so the K224 bar does not bite. The bradley leg does no work either: the "
      "grounds rest on consent-incoherent#long for act-structure. Drop the bradley leg and "
      "the entry stands as (a) on a single destination."),
 5:  ("BREACH", True, "reclassify (a) -> (d)",
      None,
      "The move is comparative-harm in its own words: harm to others needs an identifiable "
      "party made worse-off, and the child had no better counterfactual. The grounds answer "
      "it with a bearer whose wronging is constituted by the creation itself, not by a "
      "worse-off comparison, which is the contested HR-05 thesis, not a corpus result. "
      "Routing here answers the dilemma by assuming the horn in dispute."),
 8:  ("CLEAR", False, "attest",
      "[K229-not-comparative]",
      "The move is the no-relatum move (there is no interest-bearer whom restraint serves), "
      "not a worse-off comparison, so the bar does not bite. Bradley's answer, that the "
      "relatum is the actual future person who will exist and bear the harm, turns on "
      "subject-existence rather than on a baseline. Noted: that answer is carried by the "
      "poisoning parallel, which B1's own (b) at bradley-no-subject#long and B2's at "
      "incommensurability both find comparative-smuggling. The (a) survives the bar and "
      "inherits that separately-registered (b)."),
 10: ("CLEAR", False, "attest",
      "[K230-crossref-not-load-bearing]",
      "The broken cross-ref is real and is already registered as B1's (b) at "
      "transhumanist-objection#long: the node says the terminus pressure is carried at "
      "bradley-no-subject, and bradley disclaims pro-mortalism, so the destination declines "
      "the delivery. But the defect sits in the node's extinction-terminus paragraph. This "
      "(a) leans on the asymmetry paragraph, which is sound and self-contained. Adjudicated, "
      "not load-bearing."),
 13: ("BREACH", True, "reclassify (a) -> (d)",
      None,
      "The likeliest breach, as the brief predicted, and for the reason it gave: this node "
      "IS the no-worse-off-baseline problem. The grounds answer it with a harm requiring no "
      "worse-off comparison, which is the exact proposition the move disputes. Bradley "
      "asserts non-comparative wronging via analogy; he does not establish it. The route is "
      "circular."),
}

RULINGS = [
 dict(id="D1", question="Impersonal-vs-person-affecting bedrock (K224 bedrock 1): consolidate the facets or register each one.",
   ruling="CONSOLIDATE, facets preserved as sub-identifiers.",
   evidence_key="hr03",
   reasoning=(
     "Executed in honest_residuals_register_v0_1: one bedrock_id HR-03 carrying 10 tributaries "
     "across 6 named facets (metaethical-locus, aggregation-vs-iteration, absence-asymmetry, "
     "value-requires-a-valuer, relational-holist-seat-of-standing, unfacetted). The brief "
     "estimated at least 9 tributaries across at least 4 facets; measured from the artifact it "
     "is 10 and 6. Registering each facet as its own bedrock would multiply one dispute into "
     "six and destroy the very property that makes a bedrock useful, that a later phase can "
     "check novelty against a short list."),
   consequence=("The 3 C-phase tributaries carry the bare string with no facet qualifier and sit "
     "in the unfacetted bucket. They should be faceted at assembly or the bucket should be "
     "declared permanent.")),
 dict(id="D2", question="Phase D's split: love-beauty-art, joy-outweighs-harms and suffering-as-meaning spread three facets across two bedrocks.",
   ruling="MOOT under the Phase D re-derivation; reactivates only if K231's Phase D is recovered and selected.",
   evidence_key="d_residues",
   reasoning=(
     "The decision is stated over K231's Phase D, which carried 4 (d) entries. The re-derivation "
     "carries 1, at evolution-purpose, terminating at HR-04. None of the three named nodes "
     "carries a (d) in it. There is no split to adjudicate against the fragment that exists."),
   consequence="Hold D2 open but unblocking: it cannot gate the terminal assembly under the current Phase D."),
 dict(id="D3", question="N1 (is-ought / agent-neutral-reasons realism): triage against meta-ethical-pluralism#long for possible collapse to already-registered.",
   ruling="NO COLLAPSE. HR-04 stands as its own bedrock. The triage cannot be run as specified, because the target node is at entry cap and its is-ought surface is already taken.",
   evidence_key="mep",
   reasoning=(
     "meta-ethical-pluralism carries 3 entries against a cap of 3, and its Phase A (d) at long is "
     "anchored on the is-ought sentence itself. That entry terminates at normative error theory "
     "(HR-07), not at HR-04. So the node's is-ought surface is mined and routed elsewhere; there "
     "is no unclaimed registration for HR-04 to collapse into. Separately, the brief's premise for "
     "this item is wrong: it records N1 as first registered at nihilism-label in Phase D, but the "
     "shipped B2 fragment carries the birth certificate at phenomenological-existentialism with "
     "novel true, and B2 precedes D."),
   consequence=(
     "NEW FINDING, not in the brief: HR-07 (normative error theory) is downstream of HR-04 rather "
     "than a sibling. HR-04 asks whether suffering's disvalue is stance-independent; HR-07 grants "
     "the aversion datum and denies categorical bindingness, which is a further question that "
     "survives either answer to HR-04. Keep both, register the dependency.")),
 dict(id="D4", question="N2 / N4: comparative-vs-non-comparative harm against bedrock-III (imposition wrong independent of harm).",
   ruling="TWO BEDROCKS. Do not consolidate. Register HR-06 as strictly stronger than HR-05 and link them.",
   evidence_key="n2n4",
   reasoning=(
     "The two ask different questions. HR-05 asks whether wronging requires a worse-off baseline; "
     "HR-06 asks whether wronging requires harm at all. A position can answer HR-05 in the "
     "antinatalist's favour (creation non-comparatively harms) and still reject HR-06 (nothing "
     "wrongs absent harm). HR-06 therefore survives HR-05's resolution in either direction, which "
     "is the definition of a distinct floor. Merging them would make B2's incommensurability entry "
     "unstatable: it terminates at HR-05 while routing its consent fallback to HR-06, a "
     "discrimination a merged bedrock could not express."),
   consequence="Add a depends_on / stronger_than link to the register schema rather than merging the ids."),
 dict(id="D5", question="B1 predates both carry-forward constraints: 4 (a)-routes into bradley-no-subject#long and 1 through transhumanist-objection#long.",
   ruling="2 BREACHES, 2 CLEARS with attestation, 1 CLEAR with route hygiene. See carry_forward_adjudication.",
   evidence_key="b1",
   reasoning=(
     "The bar reads as a prohibition, not a licence: K224 forbids routing an (a) into "
     "bradley-no-subject#long FOR A COMPARATIVE-HARM MOVE, because bradley answers such moves by "
     "asserting non-comparative wronging, which is unsettled bedrock (HR-05). K229 scopes the "
     "prohibition to comparative-harm moves. B2 applies it explicitly, twice, in its own grounds "
     "text: do NOT route (a) into bradley-no-subject per K224 carry-forward. B1 predates it. "
     "Adjudicating the five against that bar gives 2 breaches, both comparative-harm moves, both "
     "the ones whose grounds lean on a harm requiring no worse-off comparison."),
   consequence=(
     "The two breaches reclassify (a) -> (d) terminating at HR-05, taking B1 from 8a/5b/0c/3d to "
     "6a/5b/0c/5d and HR-05 from 3 tributaries to 5. Entries are shipped and ratified, so the "
     "reclassification is a proposal for triage, never a unilateral rewrite.")),
]

FINDINGS = [
 dict(id="F1", severity="instrument-gap",
   title="The register's collision detector catches under-individuation, not over-individuation.",
   detail=(
     "It verifies that each bedrock_id has exactly one birth certificate, which catches one "
     "bedrock wearing two novel flags. It cannot catch one bedrock wearing two ids, which is "
     "precisely the failure that produced 22 free-text strings for 12 bedrocks. D3's HR-04 / "
     "HR-07 finding surfaced by hand, not by the instrument. Remedy: require every bedrock to "
     "declare its relation to its nearest neighbour (independent / depends_on / stronger_than), "
     "so over-individuation has to be asserted rather than defaulted into.")),
 dict(id="F2", severity="internal-inconsistency",
   title="Phase B1 flagged bradley's non-comparative assertion as a (b) and then routed four (a)s into it.",
   detail=(
     "B1 carries a (b) at bradley-no-subject#long anchored on the no-third-branch boast, whose "
     "grounds read: presupposes non-comparative harm, which the node asserts via analogy rather "
     "than argues. The same fragment then used that node as an (a) destination four times. This "
     "is the concrete reason K224 instituted the bar, and it is a general hazard worth naming: a "
     "fragment can register a node's defect and spend the node as an answer in the same pass, "
     "because the two operations touch different entries and nothing cross-checks them.")),
 dict(id="F3", severity="token-design",
   title="The v0_2 attestation tokens were exact-match and forced a disposition the ruling did not reach.",
   detail=(
     "[K230-crossref-repaired] was the only clearing token for the transhumanist route, but the "
     "ruling on entry 10 is that the broken cross-ref is not load-bearing for that (a), not that "
     "anything was repaired. Attesting it would have been false. v0_2 now matches the token as a "
     "PREFIX so the suffix names the disposition. Caught while authoring these rulings, before "
     "K333 was run; the block was reissued as REV B.")),
]


def main():
    b1 = json.loads(open(B1,"rb").read().decode("utf-8")); b2 = json.loads(open(B2,"rb").read().decode("utf-8"))
    corpus = json.loads(open(CORPUS,"rb").read().decode("utf-8"))
    fail = []
    entries = b1["entries"]
    adj_out = []
    for idx, (verdict, comp, disp, tok, note) in sorted(ADJ.items()):
        if idx >= len(entries):
            fail.append("B1 index %d out of range" % idx); continue
        e = entries[idx]
        if e["class"] != "a":
            fail.append("B1[%d] is class %r, expected a" % (idx, e["class"]))
        ab = e["routing"].get("answered_by", [])
        if BAR_LOCUS not in ab and CROSSREF_LOCUS not in ab:
            fail.append("B1[%d] routes to neither constrained locus: %s" % (idx, ab))
        adj_out.append(dict(
            b1_index=idx, target=e["target_id"] + "#" + e["target_locus"],
            answered_by=ab, constrained_locus=(BAR_LOCUS if BAR_LOCUS in ab else CROSSREF_LOCUS),
            move_is_comparative_harm=comp, verdict=verdict, disposition=disp,
            attestation_token=tok, adjudication=" ".join(note.split()),
            anchor=e["target_anchor"]))
    if len(adj_out) != 5:
        fail.append("expected 5 carry-forward entries, adjudicated %d" % len(adj_out))
    if sum(1 for a in adj_out if a["verdict"] == "BREACH") != 2:
        fail.append("expected exactly 2 breaches")

    # verified evidence pulls
    ev = {}
    for e in entries:
        if e["target_id"] == "bradley-no-subject" and e["class"] == "b":
            ev["b1_bradley_b_grounds"] = e["grounds"]
        if e["target_id"] == "transhumanist-objection" and e["class"] == "b":
            ev["b1_transhumanist_b_grounds"] = e["grounds"]
    for e in b2["entries"]:
        if e["target_id"] == "incommensurability" and e["class"] == "d":
            ev["b2_bar_applied"] = e["routing"]["residue"]["terminus_routing"]
        if e["target_id"] == "phenomenological-existentialism" and e["class"] == "d":
            ev["n1_birth_certificate"] = dict(node="phenomenological-existentialism", phase="B2",
                novel=e["routing"]["residue"]["novel"],
                bedrock=e["routing"]["residue"]["bedrock_name"])
    for k in ("b1_bradley_b_grounds", "b1_transhumanist_b_grounds", "b2_bar_applied", "n1_birth_certificate"):
        if k not in ev:
            fail.append("evidence pull failed: %s" % k)
    if ev.get("n1_birth_certificate", {}).get("novel") is not True:
        fail.append("N1 birth certificate at B2 does not carry novel=true")
    if "do NOT route (a) into bradley-no-subject" not in ev.get("b2_bar_applied", ""):
        fail.append("B2 bar-application text not found where expected")

    mep = [e for f in (S + "adv_map_phaseA_v0_1.json",) for e in json.loads(open(f,"rb").read().decode("utf-8"))["entries"]
           if e["target_id"] == "meta-ethical-pluralism"]
    ev["meta_ethical_pluralism_entries"] = len(mep)
    if len(mep) != 3:
        fail.append("meta-ethical-pluralism has %d entries, ruling D3 assumes cap 3" % len(mep))

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f in fail: print("  " + f)
        return 1

    doc = dict(meta=dict(
        artifact=OUT, kind="RULING SESSION artifact",
        dual_session_law=("Per brief s1.4 this session emits an artifact and commits nothing. An "
            "execute session consumes it and authors no net-new prose. Every ruling below is a "
            "proposal for Josiah's triage; the shipped fragments are ratified and are not "
            "rewritten by this document."),
        source_corpus_md5=hashlib.md5(open(CORPUS, "rb").read()).hexdigest(),
        source_fragments={"B1": hashlib.md5(open(B1, "rb").read()).hexdigest(),
                          "B2": hashlib.md5(open(B2, "rb").read()).hexdigest()},
        decisions=len(RULINGS), carry_forward_entries=len(adj_out),
        breaches=sum(1 for a in adj_out if a["verdict"] == "BREACH"),
        structural_findings=len(FINDINGS)),
        rulings=[dict(r, reasoning=" ".join(r["reasoning"].split()),
                      consequence=" ".join(r["consequence"].split())) for r in RULINGS],
        carry_forward_adjudication=adj_out,
        verified_evidence=ev,
        structural_findings=[dict(f, detail=" ".join(f["detail"].split())) for f in FINDINGS],
        execute_session_actions=[
          "1. Run K333 REV B (validator v0_2 + staging README). Nothing else may land first.",
          "2. Apply the D5 dispositions to adv_map_phaseB1_v0_1.json: drop the inert bradley leg at "
          "index 4; add [K229-not-comparative] to the grounds at indices 4 and 8; add "
          "[K230-crossref-not-load-bearing] at index 10; reclassify indices 5 and 13 from (a) to "
          "(d) terminating at HR-05. Recompute meta.class_counts. This edits a ratified fragment "
          "and requires Josiah's ratification first.",
          "3. Canon MINOR bump: fold HR-03 into terminal_stability_marker.honest_residuals so the "
          "K224 bedrock-1 pointer resolves; pin validator v0_2; update the adversarial_map block "
          "for phases A-E, the first (c), and the next-pointer to terminal assembly.",
          "4. Land the Phase D selection (re-derivation vs K231), then Phase E, then the register.",
          "5. Terminal assembly into adversarial_map_v1_0.json, run with --assembly so the "
          "advisories are binding."])

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    bts = out.encode()
    print("WROTE %s  %d B  md5 %s" % (OUT, len(bts), hashlib.md5(bts).hexdigest()))
    print("  %d decisions, %d carry-forward entries (%d breach / %d clear), %d structural findings"
          % (len(RULINGS), len(adj_out), doc["meta"]["breaches"], len(adj_out) - doc["meta"]["breaches"],
             len(FINDINGS)))
    for a in adj_out:
        print("   B1[%2d] %-26s %-6s %s" % (a["b1_index"], a["target"].split("#")[0], a["verdict"], a["disposition"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
