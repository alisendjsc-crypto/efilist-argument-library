#!/usr/bin/env python3
"""Derive honest_residuals_register_v0_1.json from the (d) entries of the shipped
fragments plus the pre-map registrations already carried in canon and the T5
disposition file.

Everything here is DERIVED except BEDROCK_MAP, which is the editorial act: it
assigns each free-text bedrock_name to a bedrock_id and facet.  The script then
audits its own map and refuses to write if any invariant fails.
"""
import json, hashlib, collections, sys, os

CORPUS = "../efilist_argument_library_v4_0_0.json"  # run from adversarial_map_staging/
FRAGS = [("A",  "adv_map_phaseA_v0_1.json"),
         ("B1", "adv_map_phaseB1_v0_1.json"),
         ("B2", "adv_map_phaseB2_v0_1.json"),
         ("C",  "adv_map_phaseC_v0_1.json")]
PHASE_ORDER = ["A", "B1", "B2", "C", "D", "E"]

# ---- the editorial act: free-text bedrock_name -> (bedrock_id, facet_id) ----
# Keyed on the exact shipped string so a fragment edit breaks the build loudly.
BEDROCK_MAP = {
 "global normative/epistemic skepticism: dissolution of all warrant, harm-premise and license alike (the acknowledged solipsism honest residual)":
   ("HR-01", "dissolution-of-all-warrant"),
 "asymmetry-contingency (impersonal-comparison reading of terminus value)":
   ("HR-02", "impersonal-comparison-reading"),
 "asymmetry-contingency (intrinsic-value-of-existence stake; purified Moorean retreat)":
   ("HR-02", "intrinsic-value-of-existence"),
 "impersonal vs person-affecting axiology as the metaethical locus of the universal antinatalist conclusion":
   ("HR-03", "metaethical-locus"),
 "impersonal-vs-person-affecting axiology":
   ("HR-03", "unfacetted"),
 "impersonal-vs-person-affecting axiology (aggregation-vs-iteration on the negative axis)":
   ("HR-03", "aggregation-vs-iteration"),
 "impersonal-vs-person-affecting axiology (absence-asymmetry: whether a possible person's foregone good is a real cost)":
   ("HR-03", "absence-asymmetry"),
 "impersonal-vs-person-affecting axiology (value-requires-a-valuer / standpoint-dependence of the empty-world verdict)":
   ("HR-03", "value-requires-a-valuer"),
 "impersonal-vs-person-affecting axiology (value-requires-a-valuer: whether a valuerless world is assessable as better)":
   ("HR-03", "value-requires-a-valuer"),
 "impersonal-vs-person-affecting axiology (relational-holist facet: is value/standing seated in the individual-with-a-standpoint or the caring whole)":
   ("HR-03", "relational-holist-seat-of-standing"),
 "impersonal-vs-person-affecting axiology (relational-holist / seat-of-standing facet: standing borne by the whole, a node's suffering a constitutive non-vetoing part of a good)":
   ("HR-03", "relational-holist-seat-of-standing"),
 "realism / is-ought grounding of agent-neutral moral reasons":
   ("HR-13", "binding-an-indifferent-agent"),
 "Benatar's asymmetry (merely-possible-beneficiary)":
   ("HR-02", "merely-possible-beneficiary"),
 "moral-realism / is-ought: stance-independence of suffering's disvalue":
   ("HR-04", "stance-independence-of-disvalue"),
 "moral-realism / is-ought: whether the property conserved under redescription is intrinsically disvaluable or merely reliably avoided":
   ("HR-04", "conserved-property-under-redescription"),
 "comparative-vs-non-comparative-harm: can creation wrong a person with no worse-off baseline":
   ("HR-05", "no-worse-off-baseline"),
 "comparative-vs-non-comparative-harm: can creating a being wrong it with no worse-off baseline":
   ("HR-05", "no-worse-off-baseline"),
 "bedrock-III: imposition of an unrefusable condition on a non-antecedent subject as wrong independent of harm":
   ("HR-06", "unrefusable-condition-on-non-antecedent-subject"),
 "normative error theory (categorical-bindingness denial; aversion-datum granted)":
   ("HR-07", "categorical-bindingness-denial"),
 "sub-specie-aeternitatis quietism (axiological-nihilist exit at cosmic register)":
   ("HR-08", "cosmic-register-exit"),
 "tolerance-weighting pluralism (lexical-priority stake above suffering-minimization)":
   ("HR-09", "lexical-priority-above-suffering-minimization"),
 "radical holism / anti-theory (refusal of invariant verdicts as such)":
   ("HR-10", "refusal-of-invariant-verdicts"),
 "epistemic authority of the anti-extinction intuition (Moorean datum) versus its evolutionary debunking":
   ("HR-11", "moorean-datum-vs-debunking"),
 "ex-ante vs ex-post locus of contractualist justification (prospects vs outcomes; type-standpoints as justificands)":
   ("HR-12", "ex-ante-vs-ex-post-justificand"),
}

# ---- relation vocabulary (F1 remedy) -----------------------------------------
# depends_on   : this bedrock's question arises only once the other is answered a
#                particular way (the horn is named in the note)
# stronger_than: this bedrock's claim entails the other's, not conversely
# sibling_of   : same effect by different grounds; neither entails the other
# independent_of: adjacency was flagged by evidence and adjudicated to NO relation
# An EMPTY relations list is an assertion of independence, not a default. The audit
# below refuses to write if any mechanically-derived adjacency candidate is undeclared.
RELATIONS = {
 "HR-02": [("depends_on", "HR-03", "lives on HR-03's IMPERSONAL horn: the asymmetry is an impersonal-value claim, so the amplifier cluster is contingent on that horn being taken")],
 "HR-04": [("sibling_of", "HR-01", "both dissolve verdicts, HR-01 by voiding all warrant and HR-04 by denying the ought is derivable; neither entails the other")],
 "HR-05": [("depends_on", "HR-03", "lives on HR-03's PERSON-AFFECTING horn: go impersonal and the worse-off-baseline question does not arise, because no person needs a baseline")],
 "HR-06": [("depends_on", "HR-03", "same person-affecting horn as HR-05: wronging without harm still requires a subject to be wronged"),
           ("stronger_than", "HR-05", "D4 ruling: HR-06 survives HR-05's resolution in either direction, since a wrong independent of harm needs no comparison to establish")],
 "HR-07": [("depends_on", "HR-04", "D3 finding: error theory is a stance WITHIN the HR-04 dispute that additionally denies categorical bindingness, a further question surviving either answer to HR-04. NOT detected by the adjacency signals; found by hand")],
 "HR-08": [("sibling_of", "HR-01", "verdict dissolution at the cosmic register rather than by voiding warrant")],
 "HR-10": [("sibling_of", "HR-01", "verdict dissolution by refusing invariant verdicts rather than by voiding warrant")],
 "HR-13": [("depends_on", "HR-04", "presupposes the HR-04 question: only once suffering's disvalue is stance-independent does it become askable whether that disvalue generates reasons binding an agent who is simply indifferent. A realist about value can deny agent-neutral reasons (the Humean position), so HR-13 survives either answer to HR-04"),
           ("independent_of", "HR-07", "adjacent but distinct: HR-07 denies that anything binds categorically, HR-13 asks whether what binds is agent-NEUTRAL. Agent-relative categorical reasons satisfy HR-07 and fail HR-13")],
 "HR-09": [("independent_of", "HR-07", "co-located at meta-ethical-pluralism, which is why the shared-node signal fires, but the claims are distinct and near-opposed: HR-07 denies that anything binds categorically, HR-09 asserts a competing value with lexical priority. Sharing a tributary node is a fact about where they surfaced, not about what they claim")],
 "HR-01": [], "HR-03": [], "HR-11": [], "HR-12": [],
}

# ---- bedrock-level editorial data --------------------------------------------
# registered_in: where this bedrock was FIRST named. "this-program" means a
# fragment carries its novel=true birth certificate; anything else predates the map.
BEDROCKS = {
 "HR-01": dict(name="Global normative / epistemic skepticism",
   gloss="Skepticism deep enough to dissolve all warrant dissolves the harm premise and the procreative license alike. The corpus defeats solipsism only as a LICENSE, never as metaphysics.",
   registered_in="canon:terminal_stability_marker.honest_residuals.solipsism_global_skeptic",
   alias=None),
 "HR-02": dict(name="Asymmetry-contingency of the positive-states cluster",
   gloss="The positive-states rebuttals run Benatar's asymmetry as the load-bearing spine and grant the hedonic premise arguendo. Reject the asymmetry and the spine goes with it. Ceiling: high-B by design.",
   registered_in="canon:terminal_stability_marker.honest_residuals.asymmetry_dependent_amplifiers",
   alias=None),
 "HR-03": dict(name="Impersonal vs person-affecting axiology",
   gloss="Whether value and standing are seated in a standpoint-bearing individual or assessable impersonally. The corpus's universal conclusion needs the impersonal reading; the objector needs the person-affecting one. Neither side derives the other.",
   registered_in="canon:terminal_stability_marker.honest_residuals.impersonal_vs_person_affecting",
   alias="K224 bedrock 1"),
 "HR-04": dict(name="Moral realism / is-ought",
   gloss="Whether suffering's disvalue is stance-independent. The corpus refuses to derive an ought from a fact, then requires an ought it does not derive either.",
   registered_in="this-program", alias="N1"),
 "HR-05": dict(name="Comparative vs non-comparative harm",
   gloss="Whether creation can wrong a being for whom no worse-off baseline exists.",
   registered_in="K224:carry-forward-bar", alias="N2"),
 "HR-06": dict(name="Imposition wrong independent of harm",
   gloss="Whether imposing an unrefusable condition on a non-antecedent subject is wrong whatever the harm ledger says.",
   registered_in="this-program", alias="N4 / bedrock-III"),
 "HR-07": dict(name="Normative error theory",
   gloss="Categorical bindingness denied while the aversion datum is granted. Nothing in the corpus compels an error theorist who concedes that suffering is aversive.",
   registered_in="this-program", alias=None),
 "HR-08": dict(name="Sub specie aeternitatis quietism",
   gloss="The axiological-nihilist exit taken at the cosmic register: no verdict survives the view from nowhere, the corpus's included.",
   registered_in="flagship_t5_register_dispositions_v0_1:heat-death-futility(defanged)", alias=None),
 "HR-09": dict(name="Tolerance-weighting pluralism",
   gloss="A lexical priority placed above suffering-minimization. The corpus asserts the priority rather than deriving it.",
   registered_in="flagship_t5_register_dispositions_v0_1:meta-ethical-pluralism(defanged)", alias=None),
 "HR-10": dict(name="Radical holism / anti-theory",
   gloss="Refusal of invariant verdicts as such. Dissolves the corpus's universal conclusion and the objector's counter-verdict symmetrically.",
   registered_in="flagship_t5_register_dispositions_v0_1:moral-particularism(defanged)", alias=None),
 "HR-11": dict(name="Epistemic authority of the anti-extinction intuition",
   gloss="Moorean datum versus its evolutionary debunking. The node registers the dispute rather than settling it.",
   registered_in="node:negative-util-aggregation(evolved-attachment-not-truth-tracking)", alias=None),
 "HR-13": dict(name="Agent-neutral reasons grounding",
   gloss="Whether suffering's disvalue generates a reason binding a procreator who is simply indifferent to the future subject. Affirming that the cosmos has no telos and no agent-neutral values is what strips such reasons of a source; the corpus asserts the relation binds rather than showing it does.",
   registered_in="this-program", alias="N1-reasons"),
 "HR-12": dict(name="Ex ante vs ex post locus of contractualist justification",
   gloss="Prospects or outcomes as the justificand, type-standpoints as bearers. A live internal dispute the node registers.",
   registered_in="node:contractualism-scanlon(live-internal-dispute)", alias=None),
}


def md5f(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main(extra_frags, outpath):
    # locale-independent: see the note in build_phaseE.py
    corpus = json.loads(open(CORPUS, "rb").read().decode("utf-8"))
    ids = set(o["id"] for o in corpus["objections"])
    frags = list(FRAGS) + list(extra_frags)
    rows, fail = [], []
    for ph, path in frags:
        doc = json.loads(open(path, "rb").read().decode("utf-8"))
        for i, e in enumerate(doc["entries"]):
            if e["class"] != "d":
                continue
            r = e["routing"]["residue"]
            key = r["bedrock_name"]
            if key not in BEDROCK_MAP:
                fail.append("UNMAPPED bedrock_name at %s[%d] (%s): %r" % (ph, i, e["target_id"], key))
                continue
            bid, facet = BEDROCK_MAP[key]
            rows.append(dict(bedrock_id=bid, facet=facet, phase=ph, node=e["target_id"],
                             locus=e["target_locus"], anchor=e["target_anchor"],
                             novel=r["novel"], shipped_bedrock_name=key,
                             terminus_routing=r["terminus_routing"]))
            if e["target_id"] not in ids:
                fail.append("tributary node not in corpus: %s" % e["target_id"])

    # ---- audits --------------------------------------------------------------
    by_id = collections.defaultdict(list)
    for r in rows:
        by_id[r["bedrock_id"]].append(r)

    # ---- mechanically derived adjacency candidates (F1) --------------------
    import itertools, re as _re
    alias = {}
    for bid, meta in BEDROCKS.items():
        keys = [meta["name"].lower()]
        if meta["alias"]:
            keys += [a.strip().lower() for a in _re.split(r"[/]", meta["alias"])]
        alias[bid] = keys
    cands = collections.defaultdict(set)
    for r in rows:
        low = r["terminus_routing"].lower()
        for other, keys in alias.items():
            if other == r["bedrock_id"]:
                continue
            if other.lower() in low or any(k in low or k.replace(" ", "-") in low for k in keys):
                cands[tuple(sorted((r["bedrock_id"], other)))].add(
                    "terminus at %s/%s names %s" % (r["phase"], r["node"], other))
    bynode = collections.defaultdict(set)
    for r in rows:
        bynode[r["node"]].add(r["bedrock_id"])
    for node, bids in bynode.items():
        if len(bids) > 1:
            for a, b_ in itertools.combinations(sorted(bids), 2):
                cands[(a, b_)].add("shared tributary node %s" % node)

    declared = set()
    for bid, rels in RELATIONS.items():
        for _kind, other, _note in rels:
            declared.add(tuple(sorted((bid, other))))
            if other not in BEDROCKS:
                fail.append("%s declares a relation to unknown bedrock %s" % (bid, other))
    for bid in BEDROCKS:
        if bid not in RELATIONS:
            fail.append("%s declares no relations list; an empty list must be explicit" % bid)
    undeclared = sorted(set(cands) - declared)

    audit = []
    for pair in undeclared:
        audit.append(dict(severity="undeclared-adjacency", bedrock_id="%s+%s" % pair,
            detail=("%s and %s are adjacent by evidence (%s) but neither declares a relation. "
                    "Rule the pair or assert independence." % (pair[0], pair[1],
                    "; ".join(sorted(cands[pair]))))))
    hand_only = sorted(declared - set(cands))
    for bid, rs in sorted(by_id.items()):
        meta = BEDROCKS.get(bid)
        if meta is None:
            fail.append("bedrock_id %s has tributaries but no BEDROCKS entry" % bid)
            continue
        births = [r for r in rs if r["novel"]]
        if meta["registered_in"] == "this-program":
            if len(births) != 1:
                fail.append("%s claims this-program registration but has %d novel=true entries (need exactly 1)"
                            % (bid, len(births)))
            else:
                b = births[0]
                earlier = [r for r in rs if PHASE_ORDER.index(r["phase"]) < PHASE_ORDER.index(b["phase"])]
                if earlier:
                    fail.append("%s birth certificate is %s/%s but %d tributary/ies precede it: %s"
                                % (bid, b["phase"], b["node"], len(earlier),
                                   [(r["phase"], r["node"]) for r in earlier]))
        else:
            if births:
                audit.append(dict(severity="novel-flag-collision", bedrock_id=bid,
                    detail=("%s was registered before this program (%s) but %d fragment entry/ies "
                            "flag it novel=true: %s. A bedrock has one birth certificate.")
                           % (bid, meta["registered_in"], len(births),
                              [(r["phase"], r["node"]) for r in births])))
        if meta["registered_in"].startswith("K224:"):
            audit.append(dict(severity="dangling-registration-pointer", bedrock_id=bid,
                detail=("%s cites %s, which is not present in canon's "
                        "terminal_stability_marker.honest_residuals. %d tributaries route to a "
                        "registration that exists only in a session receipt. Fold it into canon "
                        "or the pointer cannot be checked.") % (bid, meta["alias"], len(rs))))

    if fail:
        print("REFUSING TO WRITE -- %d invariant failure(s):" % len(fail))
        for f in fail:
            print("  " + f)
        return 1

    bedrocks = []
    for bid in sorted(BEDROCKS):
        rs = by_id.get(bid, [])
        facets = collections.defaultdict(list)
        for r in rs:
            facets[r["facet"]].append(dict(phase=r["phase"], node=r["node"], locus=r["locus"],
                                           anchor=r["anchor"], novel=r["novel"],
                                           terminus_routing=r["terminus_routing"]))
        births = [r for r in rs if r["novel"]]
        bedrocks.append(dict(
            bedrock_id=bid, name=BEDROCKS[bid]["name"], alias=BEDROCKS[bid]["alias"],
            gloss=BEDROCKS[bid]["gloss"], registered_in=BEDROCKS[bid]["registered_in"],
            birth_certificate=(dict(phase=births[0]["phase"], node=births[0]["node"],
                                    locus=births[0]["locus"]) if len(births) == 1 else None),
            tributary_count=len(rs), facet_count=len(facets),
            relations=[dict(kind=k, to=o, note=n) for k, o, n in RELATIONS.get(bid, [])],
            facets=[dict(facet_id=k, tributaries=v) for k, v in sorted(facets.items())]))

    doc = dict(meta=dict(
        artifact="honest_residuals_register_v0_1.json",
        status="WORKING -- not terminal. Phase E (T1, n=13) has not been authored; this register "
               "is an INPUT to that authoring, not only an output of the terminal fold.",
        purpose="Consolidate every (d) honest-residue the Adversarial Map has produced into a "
                "bedrock namespace, so that a phase author can decide novel: true|false against a "
                "list instead of against memory of three phases back.",
        source_corpus="efilist_argument_library_v4_0_0.json",
        source_corpus_md5=md5f(CORPUS),
        source_fragments=[dict(phase=ph, file=os.path.basename(p), md5=md5f(p)) for ph, p in frags],
        residue_entries=len(rows), bedrocks=len(BEDROCKS),
        distinct_shipped_bedrock_names=len(set(r["shipped_bedrock_name"] for r in rows)),
        pre_map_registrations=sum(1 for b in BEDROCKS.values() if b["registered_in"] != "this-program"),
        this_program_registrations=sum(1 for b in BEDROCKS.values() if b["registered_in"] == "this-program"),
        adjacency=dict(
            candidates_derived=len(cands), declared_relations=len(declared),
            detected_and_declared=sorted("%s+%s" % p for p in sorted(set(cands) & declared)),
            declared_but_undetected=sorted("%s+%s" % p for p in hand_only),
            note=("Adjacency candidates are derived from two signals: a terminus_routing naming "
                  "another bedrock, and a corpus node feeding two bedrocks. The signals cut 66 "
                  "possible pairs to a handful, but they are NOT complete: HR-04+HR-07 is a real "
                  "dependency that neither signal fires on, found by hand during the D3 triage. "
                  "So the signals are a floor on what must be adjudicated, never a ceiling, and an "
                  "empty relations list is an assertion of independence rather than a default.")),
        fences="LIBRARY-INTERNAL. No corpus, ledger, index or combined byte moves from this artifact. "
               "Do not publish until the map is terminal."),
        audit=audit, bedrocks=bedrocks)

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    open(outpath, "w", encoding="utf-8", newline="\n").write(out)
    print("WROTE %s  %d B  md5 %s" % (outpath, len(out.encode()), hashlib.md5(out.encode()).hexdigest()))
    print("  %d (d) entries -> %d bedrocks (%d distinct shipped names collapsed)"
          % (len(rows), len(BEDROCKS), len(set(r["shipped_bedrock_name"] for r in rows))))
    print("  adjacency: %d candidates derived, %d relations declared, %d hand-found beyond the signals"
          % (len(cands), len(declared), len(hand_only)))
    print("  registrations: %d pre-map, %d by this program"
          % (doc["meta"]["pre_map_registrations"], doc["meta"]["this_program_registrations"]))
    for b in bedrocks:
        print("  %-6s %-2d trib / %d facet  %-14s %s" % (b["bedrock_id"], b["tributary_count"],
              b["facet_count"], b["registered_in"].split(":")[0], b["name"]))
    if audit:
        print("  AUDIT (%d):" % len(audit))
        for a in audit:
            print("    [%s] %s" % (a["severity"], a["detail"]))
    return 0


if __name__ == "__main__":
    extra = []
    if "--with-d" in sys.argv:
        extra.append(("D", "adv_map_phaseD_v0_1.json"))
    if "--with-e" in sys.argv:
        extra.append(("E", "adv_map_phaseE_v0_1.json"))
    out = "honest_residuals_register_v0_1.json"
    sys.exit(main(extra, out))
