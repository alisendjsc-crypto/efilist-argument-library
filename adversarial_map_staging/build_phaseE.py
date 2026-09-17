#!/usr/bin/env python3
"""Build adv_map_phaseE_v0_1.json -- Phase E, T1, n=13.

Self-checking: verifies every anchor verbatim at its named locus, every word band,
the entry cap, id x anchor uniqueness, ASCII purity and the absence of standalone
dash tokens BEFORE writing.  Refuses to write on any failure.
"""
import json, hashlib, re, sys, collections

CORPUS = "../efilist_argument_library_v4_0_0.json"  # run from adversarial_map_staging/
OUT = "adv_map_phaseE_v0_1.json"
SEAT = "wuld-ink Cowork (K334)"
DATE = "2026-09-16"
DASH = re.compile(r"(?:^|\s)[-‐-―]+(?:\s|$)")

E = []
def add(node, locus, anchor, move, klass, grounds, routing):
    E.append({"target_id": node, "target_locus": locus, "target_anchor": anchor,
              "adversarial_move": " ".join(move.split()), "class": klass,
              "grounds": " ".join(grounds.split()), "routing": routing,
              "status": "mapped",
              "provenance": {"phase": "E", "date": DATE, "seat": SEAT}})

# ---------------------------------------------------------------- (a) entries
add("animals-reproduce", "long",
 "Animals reproduce because they are driven by instinct",
 """Then the agency premise proves too much. If animals lack moral standing as agents,
 the predation you call a slaughterhouse carries no verdict, only weather. You want
 animals inside the frame as victims and outside it as authorities. Name the asymmetry
 that licenses both, or drop the green-slaughterhouse indictment.""",
 "a",
 """Met at wild-animal-suffering-consistency#medium, which affirms the extension rather
 than dodging it and holds animals as moral patients whose suffering the deterrence
 criterion identifies as paradigmatic, while never treating their behaviour as
 norm-giving. Patient-standing and agent-standing are the licensed asymmetry, and the
 T4 node carries it explicitly.""",
 {"answered_by": ["wild-animal-suffering-consistency#medium"]})

add("bitter-childhood", "long",
 "even if my childhood WAS the catalyst for this philosophy",
 """You spent four paragraphs holding that biography cannot invalidate a philosophy, then
 offered your biography as evidence for one. If etiology is inert, it is inert in both
 directions. Either withdraw the closing move or concede that biographical facts bear on
 the question after all, and let mine bear too.""",
 "a",
 """Met on the best reading. The closing move is evidential, not genetic: the childhood is
 offered as an instance of what the proxy gamble imposes, a datum about procreation's
 consequences, not as a warrant for the philosophy's truth. The medium already frames it
 that way and addresses it to the objector's own premise rather than asserting it as the
 corpus's inference.""",
 {"answered_by": ["bitter-childhood#medium"]})

add("next-person-cure-cancer", "long",
 "if the speculative possibility of extraordinary positive outcomes justifies creation",
 """Your own asymmetry forbids that symmetry. Absent goods are not bad; present harms are.
 The genocide case therefore outweighs the cure case rather than balancing it, and invoking
 parity concedes a commensurability the corpus denies elsewhere. You have borrowed the
 objector's scales to beat him.""",
 "a",
 """Met. The medium states the move as a property of the objection rather than of the
 corpus's axiology: the objection works in both directions. Arguing from the opponent's
 own premise is the point of the move, not a lapse into commensurability, and the node's
 third and fifth points carry the asymmetric case independently.""",
 {"answered_by": ["next-person-cure-cancer#medium"]})

add("privileged-first-world", "long",
 "applies MORE forcefully in conditions of extreme deprivation",
 """Said of a population rather than of an act, that sentence selects whose children should
 not exist, and the objection was built to make you write it. You answered the genetic
 fallacy and walked into the charge beneath it: a wrongness that scales with deprivation
 ranks the deprived.""",
 "a",
 """Met at slippery-slope-eugenics#medium, which holds the prohibition universal across
 every human regardless of race or genetics and identifies selective application as the
 structural feature of eugenics that antinatalism lacks. Under a universal prohibition,
 degree of wrongness ranks acts, not populations; no differential licence over any group
 is generated.""",
 {"answered_by": ["slippery-slope-eugenics#medium"]})

add("why-not-suicide", "long",
 "agent stands on the side of the non-existent",
 """The demand is crude and its target is not. You say no positive action against existing
 beings follows, then hold a button that ends every existing being. The suicide question,
 cleaned up, is simply: what does your second layer license, and why does the first layer's
 silence bind it? Routing that to another node answers where, not what.""",
 "a",
 """Met by routing. The node names its own destination, inviting the objector to name the
 NU layer if that is the target, and red-button-repugnant#long takes the licence question
 as its subject. Routing to a node that answers is a corpus operation, not an evasion, and
 the two-layer separation the node draws is what makes the routing legible.""",
 {"answered_by": ["red-button-repugnant#long", "why-not-suicide#long"]})

# ---------------------------------------------------------------- (c) entry
add("change-your-mind", "long",
 "This is not wisdom; it is motivated reasoning.",
 """Count what your answer does. Survivorship bias, confirmation bias, sunk cost, hormonal
 override: four explanations of why I hold my view, and no demonstration that it is false.
 That is the genetic fallacy you convict me of, run in your favour, and it is not confined
 here. Twenty-six of your nodes diagnose the objector inside the rebuttal itself. Two of
 them state the rule that forbids it. I am not asking you to abandon diagnosis; I am asking
 where the corpus licenses it, because at present the licence appears only where it happens
 to be obeyed.""",
 "c",
 """Not (a): no shipped node has the corpus's own diagnostic method as its subject. T5 holds
 self-defeat, value-imposition, red-button, pluralism, futility, particularism and
 universalization, all objections to the position rather than to the manner of rebuttal.
 Not (b): the register is architectural, carried by the psychMechanism and diagnosis fields
 on all 82 nodes and deployed inside responses at 26 of them, so no rewrite of this node
 answers it. The licensing condition is stated in exactly two places, life-gift#long and
 just-depressed#long, both of which forbid diagnosing the opponent as a substitute for
 refutation; the remaining 24 breach a rule the corpus has already written down. An
 objection whose scope is the corpus and whose answer must be a statement of when diagnosis
 is legitimate is a node, not a patch. FIRST (c) IN THE PROGRAM: the previous zero across 69
 nodes is an artefact of adjudicating node-against-node, which gives a corpus-level
 objection nowhere to land.""",
 {"intake_candidate": {"proposed_id": "diagnosis-not-refutation", "tier_guess": 5,
   "mechanism_guess": "Method-level tu quoque: the rebuttal's psychological diagnosis of the objector, deployed where an argument-level refutation is owed",
   "individuation_grounds": "presupposition-inversion"}})

# ---------------------------------------------------------------- (b) entries
add("antinatalism-misanthropic", "long",
 "structural criticism of a species is not the same as hatred of individuals",
 """The charge was never about your motive. Grant the hyper-empathy in full; it changes
 nothing. Misanthropy is an accusation about what a framework recommends, and yours
 recommends that the species cease. That output is extensionally indistinguishable from
 what contempt would recommend, and your building analogy concedes it: stop building more
 of these. A motivational defence answers a psychological charge nobody competent is
 making. The competent version asks why a verdict coinciding exactly with hatred's verdict
 should be read off its author's warmth rather than its content.""",
 "b",
 """The node answers the weak form. Its entire architecture is motivational, hyper-empathy
 against contempt, and the strong form concedes motive at the outset and presses on
 extensional equivalence of the action-guiding output. Nothing in short, medium or long
 engages that. The repair is available inside the node: the antinatalist verdict is
 conditional on suffering-imposition and would lapse if suffering lapsed, which no
 contempt-driven verdict would, and that is a content-level discriminator the node
 currently leaves unstated.""",
 {"regen_candidate": {"axis_hit": ["c", "r"], "severity": "headline"}})

add("happiness-is-choice", "long",
 "roughly half of your capacity for happiness was determined at conception",
 """Heritability does not say that. A heritability estimate partitions variance across a
 population under its observed range of environments; it licenses no claim about what
 fraction of one person's trait was fixed at conception. Heritability of height is high and
 height still rose several inches in a century. You state the misreading twice and build
 the empirical paragraph on it, inside a rebuttal whose charge is that your opponent
 reasons from a premise he has not earned. The voluntarist claim falls without it: the
 neurochemical and circumstantial arguments in the same passage do the work unaided.""",
 "b",
 """Straightforward misstatement of what a heritability coefficient measures, load-bearing
 and stated twice, in the node's designated empirical paragraph. It is also the node most
 exposed to a competent objector, since the h-squared misreading is the standard
 undergraduate correction. Repair is subtractive and costs no ground: drop the
 conception-fraction inference, keep the finding that wellbeing has substantial
 unchosen determinants.""",
 {"regen_candidate": {"axis_hit": ["s"], "severity": "headline"}})

add("just-depressed", "long",
 "Roughly one deployment in a hundred is a person actually worried about you",
 """Where does that number come from? The rebuttal's own indictment is that the objector
 infers from something he has not established. Here a ratio arrives with no source and
 immediately becomes architecture: the response is built for the ninety-nine and names the
 one. At one in three the same design insults a large minority acting in good faith, and
 the passage offers no way to tell which world we are in. The structural argument needs no
 ratio. Delete the figure and the etiology-is-not-truth core, the boomerang dilemma and the
 directional-bias point all stand unchanged.""",
 "b",
 """An unsourced quantitative premise doing architectural work in the corpus's most
 epistemically self-aware node, which elsewhere refuses exactly this move. Minor rather
 than headline because the logical core is fully separable and survives deletion intact.
 Repair is subtractive: state the distribution qualitatively, keep the one-in-a-hundred
 reader named and met.""",
 {"regen_candidate": {"axis_hit": ["s"], "severity": "minor"}})

add("just-edgy", "long",
 "has never been substantively refuted",
 """An argument from silence, offered as a credential, inside a rebuttal against arguments
 from authority. It is also false as stated: the book has academic critics, and had it
 none, absence of published refutation would be evidence of attention, not of
 irrefutability. The lineage paragraph does not need it. Schopenhauer, Zapffe and Benatar
 already defeat the sociological premise the objection actually asserts, that this is what
 adolescents say before maturing. Appending a claim of unrefutedness converts a sound
 demographic correction into the very move the node opens by naming.""",
 "b",
 """The lineage material is legitimate and survives on the best reading, since the objection
 makes an empirical claim about who holds the view and the lineage refutes it directly. The
 unrefutedness clause is separable and not so rescuable: no charitable reading turns
 absence of published refutation into evidential support. Repair is subtractive and the
 node's force is unaffected.""",
 {"regen_candidate": {"axis_hit": ["s"], "severity": "minor"}})

add("selfish-lazy", "long",
 "the most radical form of altruism available to a biological organism",
 """Costly is not the same as altruistic. Altruism requires a beneficiary, and the node
 names the difficulty in its own sentence: an entity who will never exist to thank them. On
 the corpus's asymmetry the uncreated are not better off, merely absent, so no one is made
 better off by the restraint. The ledger establishes only that the antinatalist forgoes
 more, which is a claim about cost. Say ethical restraint and the argument is untouched;
 say altruism and you have imported a beneficiary your own asymmetry refuses to supply.""",
 "b",
 """A one-word overclaim at the node's closing position, and the only point at which the
 node contradicts the asymmetry it depends on. The diagnosis field already has the correct
 formulation, restraint of self-interest rather than its expression, so the repair is to
 carry the diagnosis's wording into the long response. Minor: subtractive, local, and the
 projection-inversion argument is untouched.""",
 {"regen_candidate": {"axis_hit": ["s", "a"], "severity": "minor"}})

# ---------------------------------------------------------------- (d) entries
add("life-gift", "long",
 "legitimate unsolicited benefit requires an antecedent recipient with a stake",
 """Apply that evenhandedly and it takes your side down with the natalist's. If no antecedent
 subject exists to hold a stake in the good, none exists to hold a stake in being spared the
 harm. You have denied the gift a beneficiary by a principle that equally denies the
 imposition a victim. The wrong you allege must be borne by someone who exists only because
 the act occurred, which is exactly the standing your condition refuses the benefit. Either
 a subject can be wronged without an antecedent stake, in which case a subject can be
 benefited without one, or neither can, and the transaction has no moral party at all.""",
 "d",
 """Not (b): the antecedent-need condition is the node's load-bearing defeater and the
 objection attacks it at full strength rather than at a repairable margin. No rewrite
 internal to life-gift closes it, because closing it requires an argument that
 non-comparative wronging is possible where non-comparative benefiting is not, which is a
 bedrock commitment and not prose. Already registered: honest-residuals HR-05, birth
 certificate at harman-benign-creation in Phase B2 (N2). Registered by lookup, not recall.""",
 {"residue": {"bedrock_name": "comparative-vs-non-comparative-harm: can creation wrong a person with no worse-off baseline",
   "terminus_routing": "harman-benign-creation (Phase B2 registration, N2); honest-residuals register HR-05, facet no-worse-off-baseline; first T1 surface on this floor",
   "novel": False}})

add("natural-reproduce", "diagnosis",
 "'Natural' has zero moral content.",
 """Then neither does suffering. Your indictment runs on natural facts carrying moral
 weight: that pain is bad, that sentience generates claims, that predation is a catastrophe
 rather than a process. Strip value out of the natural order and the green slaughterhouse
 becomes weather, vividly described. The naturalistic fallacy cuts the appeal to nature and
 the appeal to suffering with one stroke, and the corpus needs the second to survive. What
 you require is not that nature has zero moral content but that it has exactly one kind,
 disvalue, and the argument for that restriction is the one you have not given.""",
 "d",
 """Not (b): the overreach is in the diagnosis field's slogan, but contracting it to
 something defensible requires stating why disvalue survives a razor that dissolves value,
 which is the is-ought floor itself and not a wording fix. Already registered:
 honest-residuals HR-04, birth certificate at phenomenological-existentialism in Phase B2
 (N1), with a second surface at evolution-purpose. Registered by lookup. The brief records
 N1 as first registered in Phase D; the B2 fragment carries the novel flag and B2
 precedes D.""",
 {"residue": {"bedrock_name": "moral-realism / is-ought: stance-independence of suffering's disvalue",
   "terminus_routing": "phenomenological-existentialism (Phase B2 registration, N1); honest-residuals register HR-04, facet stance-independence-of-disvalue; third surface on the same floor",
   "novel": False}})


# ==================================== verify ====================================
def wc(s): return len(s.split())

def main():
    # Binary read + explicit decode: open() in text mode takes the LOCALE encoding,
    # which is UTF-8 on Linux and cp1252 on Windows. The objections digest is computed
    # from the PARSED corpus, so a locale-dependent parse makes the artifact
    # irreproducible across platforms (0218f73b vs 8ebb07ab). Never let locale decide.
    corpus = json.loads(open(CORPUS, "rb").read().decode("utf-8"))
    nodes = {o["id"]: o for o in corpus["objections"]}
    T1 = sorted(i for i, o in nodes.items() if o["tier"] == 1)
    fail = []

    def ltext(nid, locus):
        n = nodes[nid]
        return n.get("diagnosis", "") if locus == "diagnosis" else n["responses"].get(locus, "")

    for i, e in enumerate(E):
        tag = "[%d] %s#%s" % (i, e["target_id"], e["target_locus"])
        if e["target_id"] not in nodes:
            fail.append("%s: node not in corpus" % tag); continue
        if nodes[e["target_id"]]["tier"] != 1:
            fail.append("%s: tier %d, Phase E is T1" % (tag, nodes[e["target_id"]]["tier"]))
        a = e["target_anchor"]
        if wc(a) > 15:
            fail.append("%s: anchor %d words (cap 15)" % (tag, wc(a)))
        if a not in ltext(e["target_id"], e["target_locus"]):
            fail.append("%s: ANCHOR NOT VERBATIM: %r" % (tag, a))
        w = wc(e["adversarial_move"])
        if not (40 <= w <= 150):
            fail.append("%s: move %d words (band 40-150)" % (tag, w))
        if e["class"] == "a" and w > 60:
            fail.append("%s: class (a) move %d words (cap 60)" % (tag, w))
        for fld in ("adversarial_move", "grounds", "target_anchor"):
            v = e[fld]
            bad = sorted(set(ch for ch in v if ord(ch) > 127))
            if bad:
                fail.append("%s: non-ascii in %s: %r" % (tag, fld, bad))
            if fld == "adversarial_move" and DASH.search(v):
                fail.append("%s: standalone dash token in move: %r" % (tag, DASH.search(v).group().strip()))
        for ref in e["routing"].get("answered_by", []):
            nid, _, loc = ref.partition("#")
            if nid not in nodes or loc not in ("short", "medium", "long", "diagnosis"):
                fail.append("%s: bad answered_by ref %r" % (tag, ref))
            elif not ltext(nid, loc).strip():
                fail.append("%s: answered_by %r points at empty text" % (tag, ref))

    per = collections.Counter(e["target_id"] for e in E)
    for nid, n in per.items():
        if n > 3:
            fail.append("%s has %d entries (cap 3)" % (nid, n))
    missing = [i for i in T1 if i not in per]
    if missing:
        fail.append("T1 nodes with no entry (%d): %s" % (len(missing), missing))
    pairs = collections.Counter((e["target_id"], e["target_anchor"]) for e in E)
    for k, n in pairs.items():
        if n > 1:
            fail.append("duplicate id x anchor: %r" % (k,))

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f in fail: print("  " + f)
        return 1

    craw = open(CORPUS, "rb").read()
    odig = hashlib.md5(json.dumps(corpus["objections"], indent=2, ensure_ascii=False,
                                  sort_keys=True).encode("utf-8") + b"\n").hexdigest()
    cc = collections.Counter(e["class"] for e in E)
    doc = {"meta": {
        "phase": "E", "tier": 1, "seat": SEAT, "date": DATE,
        "source_corpus": "efilist_argument_library_v4_0_0.json",
        "source_corpus_md5": hashlib.md5(craw).hexdigest(),
        "source_corpus_objections_md5": odig,
        "class_counts": {k: cc.get(k, 0) for k in ("a", "b", "c", "d")},
        "coverage_distinct_ids": len(per),
        "note": ("Phase E closes the tier-descending sweep: T1, n=13, every node carries an "
                 "entry. Authored against honest_residuals_register_v0_1, so every (d) novel "
                 "flag is a lookup rather than a recall. Carries the v0_2 objections digest "
                 "alongside the whole-file md5.")},
        "entries": E}
    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), hashlib.md5(b).hexdigest()))
    print("  entries %d over %d/%d T1 nodes   classes %s"
          % (len(E), len(per), len(T1), dict(sorted(cc.items()))))
    print("  corpus %s  objections-digest %s" % (doc["meta"]["source_corpus_md5"][:12], odig[:12]))
    for e in E:
        print("   %s  %-26s %-9s %3dw" % (e["class"], e["target_id"], e["target_locus"],
                                          wc(e["adversarial_move"])))
    return 0

if __name__ == "__main__":
    sys.exit(main())
