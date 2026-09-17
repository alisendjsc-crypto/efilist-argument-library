#!/usr/bin/env python3
"""Build adversarial_map_regen_queue_v0_1.json -- the (b)/(c) extraction the design doc
names as a terminal deliverable: 'extraction of the (b)/(c) queue as a v-cut scoping input'.

Derived from the fragments. The only editorial acts are REPAIR_SHAPE (how a defect is
fixed) and the version-class ruling; both are audited against the data before writing.
"""
import json, hashlib, collections, re, sys

S = ""  # run from adversarial_map_staging/
FR = [("A", "adv_map_phaseA_v0_1.json"), ("B1", "adv_map_phaseB1_v0_1.json"),
      ("B2", "adv_map_phaseB2_v0_1.json"), ("C", "adv_map_phaseC_v0_1.json"),
      ("D", "adv_map_phaseD_v0_1.json"),
      ("E", "adv_map_phaseE_v0_1.json")]
OUT = "adversarial_map_regen_queue_v0_1.json"

SUBTRACTIVE = re.compile(r"\b(subtractive|delete|drop the|remove the|without it|deleti\w+)\b", re.I)
ADDITIVE = re.compile(r"\b(supply|add a|state the|carry the|name the|unstated|left unstated)\b", re.I)
DIAG = re.compile(r"\bdiagnos|pathologi|genetic fallacy|terror management\b", re.I)

# Editorial: entries whose repair depends on the (c) node existing, so they are HELD
# out of the enrichment cut and carried into the intake cut.
HELD_FOR_INTAKE = {
    "gods-plan": "The defect is a Terror Management paragraph doing argument-work. With "
                 "diagnosis-not-refutation shipped, the repair is a route to the licensing node "
                 "rather than a local disclaimer written into this node.",
    "western-philosophy": "Same shape: a genetic-fallacy overclaim that the licensing node would "
                          "absorb. Repairing it locally now means rewriting it after intake.",
}

# The regen lane from brief s2.5, logged downstream and never authored into the map.
LANE = [
 dict(id="L1", title="Additivity / strong-deflation non-univocity",
   detail=("neuroscience-positive-states#long holds valence realism, adjudicated the defensible "
           "pole. It conflicts with bradley#medium, virtue-ethics-flourishing#long move 4, "
           "flow-states and marxist-materialist#long. The corpus does not affirm 'absence of "
           "pleasure is not bad' univocally, which B2's boonin-critique entry relies on."),
   cut="v4.1.0"),
 dict(id="L2", title="Act/omission-default-under-total-skepticism overclaim",
   detail=("Found in eliminativism and solipsism; total skepticism voids the default "
           "symmetrically. K230's watch on nihilism-label is CLOSED, not pending: the K231 state "
           "was recovered at K336 from its own chat's download cards, ships beside this queue as "
           "session_K231_state.json, and records CF4_nihilism_label_watch as PASS -- the node "
           "asserts the correct pole (antinatalism dissolves under nihilism) and exhibits no "
           "act/omission-default overclaim. So the item is SCOPED rather than re-open, and its "
           "extent is exactly the two T-nodes named. K231's own open_questions leaves one design "
           "question live and this queue does not decide it: a coordinated regen note across both "
           "nodes, or a per-node minor fix. Prior text held this item open on a document that had "
           "already been found -- ccclxii / ledger C9."),
   cut="v4.1.0"),
]


def shape(g):
    if SUBTRACTIVE.search(g): return "subtractive"
    if ADDITIVE.search(g): return "additive"
    return "structural"


def main():
    bs, cs, fail = [], [], []
    frag_md5 = {}
    for ph, f in FR:
        frag_md5[ph] = hashlib.md5(open(f, "rb").read()).hexdigest()
        for e in json.loads(open(f,"rb").read().decode("utf-8"))["entries"]:
            if e["class"] == "b":
                rc = e["routing"]["regen_candidate"]
                bs.append(dict(phase=ph, node=e["target_id"], locus=e["target_locus"],
                               axis_hit=sorted(rc["axis_hit"]), severity=rc["severity"],
                               repair_shape=shape(e["grounds"]),
                               diagnosis_coupled=bool(DIAG.search(e["grounds"])),
                               anchor=e["target_anchor"], grounds=e["grounds"]))
            elif e["class"] == "c":
                cs.append(dict(phase=ph, host_node=e["target_id"],
                               intake=e["routing"]["intake_candidate"], grounds=e["grounds"]))

    per_node = collections.Counter(b["node"] for b in bs)
    dupes = {k: v for k, v in per_node.items() if v > 1}
    if dupes:
        fail.append("nodes carrying >1 (b): %s -- the queue assumes one regen per node" % dupes)
    for n in HELD_FOR_INTAKE:
        if n not in per_node:
            fail.append("HELD_FOR_INTAKE names %r, which carries no (b)" % n)
    if len(cs) != 1:
        fail.append("expected exactly 1 (c), found %d" % len(cs))

    for b in bs:
        b["cut"] = "v5.0.0" if b["node"] in HELD_FOR_INTAKE else "v4.1.0"
        if b["node"] in HELD_FOR_INTAKE:
            b["hold_reason"] = HELD_FOR_INTAKE[b["node"]]

    enrich = [b for b in bs if b["cut"] == "v4.1.0"]
    intake = [b for b in bs if b["cut"] == "v5.0.0"]

    ruling = dict(
      question=("Canon does not classify a v4.x regen cut. Decide its version class explicitly "
                "rather than letting it default into a patch."),
      ruling="SPLIT THE CUT: v4.1.0 enrichment, then v5.0.0 intake.",
      precedent=[
        "v3.9.0 was opened as the ENRICHMENT line: post_terminal_policy reads 'v3.8 frozen / v3.9 "
        "enrichment / v4.0 intake renumbered-GATED'. Enrichment of existing nodes is MINOR.",
        "v4.0.0 (K219) was MAJOR because it was INTAKE: objection_count 81 -> 82, with the node "
        "and link counts renumbered across map_graph_data and dep_graph_data.",
        "A single response recut took a PATCH (the masochist coda, responses.long -> v3.7.5).",
      ],
      reasoning=(
        "%d (b) entries across %d distinct nodes is %d%% of the corpus carrying a correction. That "
        "is far past a patch, and it is exactly the operation v3.9 was opened to perform, so the "
        "enrichment cut is MINOR: v4.1.0. The single (c) proposes an 82 -> 83 intake, which is the "
        "operation that made v4.0.0 MAJOR, so it is v5.0.0. They are split rather than bundled for "
        "three reasons. The precedent already separates them and gated intake behind enrichment. "
        "Bundling makes %d prose corrections hostage to the single most contestable item in the "
        "queue, an objection to the corpus's own method that Josiah may reject or reshape. And each "
        "regen must cold-grade: %d regens is one grading job, a node intake across four surfaces "
        "plus dependency-graph renumbering is another."
        % (len(bs), len(per_node), round(100*len(per_node)/82), len(enrich), len(enrich))),
      coupling_check=(
        "The ordering was measured, not assumed. If many (b) repairs would be rewritten once the "
        "(c) node exists, the intake should lead. Scanning all %d grounds for diagnosis-for-argument "
        "language returns %d, and on inspection only %d genuinely couple: gods-plan and "
        "western-philosophy, whose repairs become a route to the licensing node rather than a local "
        "disclaimer. Those two are HELD for v5.0.0. The other %d are independent of the intake."
        % (len(bs), sum(1 for b in bs if b["diagnosis_coupled"]), len(HELD_FOR_INTAKE), len(enrich))),
      caveat=("This ruling is proposed, not applied. Version class is Josiah's call and canon "
              "records it; the ruling session emits, the execute session lands."))

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f in fail: print("  " + f)
        return 1

    doc = dict(meta=dict(
        artifact=OUT, kind="v-cut scoping input (design doc s: terminal deliverables)",
        status="BUILT AGAINST THE SELECTED PHASE D. The conditional this field used to carry -- "
               "'if the K231 fragment is recovered and selected instead, re-run this builder "
               "against it' -- was DISCHARGED at K336: the fragment was recovered from its own "
               "chat's download cards, landed verbatim, and this queue is built against it. Check "
               "it rather than trust it: source_fragments.D below is K231's md5, not the "
               "superseded re-derivation's. Scoping input; the cut it scopes is ratified "
               "separately and is not opened by this file.",
        source_fragments=frag_md5,
        b_total=len(bs), c_total=len(cs), distinct_nodes=len(per_node),
        corpus_nodes=82, corpus_fraction_pct=round(100*len(per_node)/82, 1),
        severity=dict(collections.Counter(b["severity"] for b in bs)),
        repair_shape=dict(collections.Counter(b["repair_shape"] for b in bs)),
        per_phase=dict(collections.Counter(b["phase"] for b in bs)),
        axes=dict(collections.Counter("".join(b["axis_hit"]) for b in bs)),
        fences="Yields are intake candidates, never authorizations. No byte moves from this artifact."),
        version_class_ruling=ruling,
        v4_1_0_enrichment=dict(count=len(enrich),
            headline=[b for b in enrich if b["severity"] == "headline"],
            minor=[b for b in enrich if b["severity"] == "minor"]),
        v5_0_0_intake=dict(intake_candidate=cs[0], held_regens=intake),
        regen_lane=LANE)

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out.encode()), hashlib.md5(out.encode()).hexdigest()))
    print("  %d (b) + %d (c) over %d distinct nodes = %.1f%% of the corpus"
          % (len(bs), len(cs), len(per_node), doc["meta"]["corpus_fraction_pct"]))
    print("  v4.1.0 enrichment: %d (%d headline / %d minor)  |  v5.0.0 intake: 1 (c) + %d held"
          % (len(enrich), sum(1 for b in enrich if b["severity"] == "headline"),
             sum(1 for b in enrich if b["severity"] == "minor"), len(intake)))
    print("  repair shapes: %s" % doc["meta"]["repair_shape"])
    print("  rendered adversarial_map_regen_queue_v0_1.md  %d B" % render(doc))
    return 0


def render(doc):
    m=doc['meta']; r=doc['version_class_ruling']
    L=[];w=L.append
    w("# Adversarial Map \u2014 Regen Queue v0.1"); w("")
    w("The (b)/(c) extraction the design doc names as a terminal deliverable. Derived from the six")
    w("fragments; the only editorial acts are the repair-shape classification and the version-class ruling.")
    w(""); w("---"); w("")
    w("## Scale"); w(""); w("| | |"); w("|---|---|")
    w("| (b) regen candidates | **%d** |" % m['b_total'])
    w("| (c) intake candidates | %d |" % m['c_total'])
    w("| Distinct nodes touched | %d of 82 (**%s%%** of the corpus) |" % (m['distinct_nodes'], m['corpus_fraction_pct']))
    w("| Headline / minor | %d / %d |" % (m['severity'].get('headline',0), m['severity'].get('minor',0)))
    w("| Repair shape | %s |" % ", ".join("%s %d"%(k,v) for k,v in sorted(m['repair_shape'].items())))
    w("| Per phase | %s |" % ", ".join("%s %d"%(k,v) for k,v in m['per_phase'].items()))
    w("")
    w("## Version class \u2014 %s" % r['ruling']); w("")
    w("*%s*" % r['question']); w(""); w("**Precedent.**"); w("")
    for p_ in r['precedent']: w("- %s" % p_)
    w(""); w(r['reasoning']); w("")
    w("**Ordering was measured, not assumed.** %s" % r['coupling_check']); w("")
    w("> %s" % r['caveat']); w(""); w("---"); w("")
    e=doc['v4_1_0_enrichment']
    w("## v4.1.0 \u2014 enrichment cut (%d regens)" % e['count']); w("")
    w("### Headline (%d)" % len(e['headline'])); w("")
    w("| node | locus | axes | repair | defect |"); w("|---|---|---|---|---|")
    for b in e['headline']:
        w("| `%s` | %s | %s | %s | %s |" % (b['node'],b['locus'],"".join(b['axis_hit']),b['repair_shape'],b['grounds'].split('. ')[0][:110]))
    w(""); w("### Minor (%d)" % len(e['minor'])); w("")
    w("| node | locus | axes | repair |"); w("|---|---|---|---|")
    for b in e['minor']:
        w("| `%s` | %s | %s | %s |" % (b['node'],b['locus'],"".join(b['axis_hit']),b['repair_shape']))
    w("")
    i=doc['v5_0_0_intake']; ic=i['intake_candidate']
    w("## v5.0.0 \u2014 intake cut"); w(""); w("### The node"); w("")
    w("**`%s`** \u2014 tier %d, individuated on %s. Host: `%s` (phase %s)."
      % (ic['intake']['proposed_id'], ic['intake']['tier_guess'], ic['intake']['individuation_grounds'], ic['host_node'], ic['phase']))
    w(""); w("*%s*" % ic['intake']['mechanism_guess']); w("")
    w("This is the first (c) in the program across all 82 nodes.")
    w(""); w("### Regens held for this cut (%d)" % len(i['held_regens'])); w("")
    for b in i['held_regens']:
        w("**`%s#%s`** (%s) \u2014 %s" % (b['node'],b['locus'],b['severity'],b['hold_reason'])); w("")
    w("## Regen lane"); w(""); w("Logged downstream, never authored into the map."); w("")
    for l in doc['regen_lane']:
        w("**%s \u00b7 %s** \u2014 `%s`" % (l['id'],l['title'],l['cut'])); w(""); w(l['detail']); w("")
    out="\n".join(L)+"\n"
    open("adversarial_map_regen_queue_v0_1.md","w",encoding="utf-8",newline="\n").write(out)
    return len(out.encode("utf-8"))


if __name__ == "__main__":
    sys.exit(main())
