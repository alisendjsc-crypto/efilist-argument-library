#!/usr/bin/env python3
"""K349 PHASE G -- the `note` locus, authored NARROWLY.

Josiah's 0a ruling delegated the disposition to this seat, which took the NARROW form:
author only where a note makes or concedes a claim the corpus would have to defend.
Four of the nine notes are authoring apparatus (taxonomy, build-pass provenance, a
ratification-delta line, a tier instruction addressed to a future editor) and one is a
legitimate scope qualifier consistent with its response; none is a claim, and the class
law -- "the strongest continuation against our text" -- is malformed against them.

Every instrument is IMPORTED from the validator. Nothing here recomputes a digest, a
locus lookup or an md5 by hand (the hazard that has fired in four sessions).
"""
import json, os, sys, importlib.util, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SEAT = "wuld.ink Cowork, K349"
DATE = "2026-09-17"


def load_validator():
    p = os.path.join(HERE, "adv_map_validator_v0_6.py")
    spec = importlib.util.spec_from_file_location("advval6", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, p


V, VPATH = load_validator()


def E(tid, anchor, move, grounds, klass, routing):
    return {
        "target_id": tid,
        "target_locus": V.NOTE_LOCUS,
        "target_anchor": anchor,
        "adversarial_move": " ".join(move.split()),
        "class": klass,
        "grounds": " ".join(grounds.split()),
        "routing": routing,
        "status": "mapped",
        "provenance": {"phase": "G", "date": DATE, "seat": SEAT},
    }


ENTRIES = [
    E("care-ethics",
      "would benefit from deeper engagement with Held's distinction between 'chosen' and 'unchosen' caring relationships",
      """Your own apparatus concedes that engaging Held's chosen and unchosen distinction
      has direct implications for the consent framework, and then does not engage it. That
      distinction is the claim that unchosen caring relations generate binding obligation
      without anyone having consented to them. If it holds, consent is not the currency in
      which relational obligation is denominated, and the structural impossibility of
      consent from a non-existent subject stops being decisive and becomes merely true.
      Your response answers when the caring relation is evaluated. It never answers whether
      consent is the right test. You published the gap, named the text that closes it, and
      left it open.""",
      """Read whole-node per design v0_4 section 11.1: the node FAILS TO CURE. Held appears
      once, in the opening roster, and the chosen/unchosen distinction appears nowhere in
      #long. The node's three moves are the temporal inversion, the dependency argument and
      an honest acknowledgment; the temporal inversion answers WHEN the caring relation is
      assessed, not whether consent is the right currency for relational obligation. The
      node does deploy the word at its pivotal move, 'the deepest possible unchosen moral
      obligation', but applies it to the PARENT's obligation, helping itself to one half of
      a distinction the note concedes it has not engaged. The registered (d) at
      care-ethics#long is on a different question, the seat of standing, so it does not
      cover this. Repair is authoring work at #long; deleting the note is the cheap repair
      and the wrong one, because the exposure exists whether or not it is published.""",
      "b", {"regen_candidate": {"axis_hit": ["c", "r"], "severity": "headline"}}),

    E("boonin-critique",
      "broad attack categories rather than engaged with at the level of symbolic reconstruction",
      """You pronounce a verdict on a formal argument while conceding you never examined it
      formally. Boonin reconstructs in notation; you answer in three prose categories and
      admit an academic will notice the absence. A summary cannot refute a proof, so your
      claim that his critique does not touch the architecture is unearned.""",
      """Met on best reading, and the node CURES per section 11.1. The verdict claimed is
      about the architecture's REDUNDANCY, not about Boonin's validity, and redundancy is
      established without formal engagement: #long argues the position 'is not a
      single-load-bearing-wall structure' but 'a convergent architecture where multiple
      independent arguments arrive at the same conclusion', then names four grounds that
      survive the asymmetry falling. Honest limit, stated rather than smoothed: the node's
      OWN dissolution of the quadrant objection, that the absence of pain need only be 'not
      bad', is itself a formal move the note concedes is unverified, so that particular
      reply stands unbacked. It is not load-bearing; the convergence backstop is, and the
      move above reaches the reply rather than the claim.""",
      "a", {"answered_by": ["boonin-critique#long"]}),

    E("indigenous-philosophy",
      "A fully adequate treatment would require engagement with specific traditions by their own practitioners",
      """You concede that an adequate treatment needs practitioners you have not consulted
      and cannot consult from inside a text. So the verdict is provisional by your own
      admission, and the node's own grade says so. An entry that cannot be made adequate by
      any amount of authoring should not be presented as an answer at all.""",
      """Met, and the node CURES by conceding MORE than the note does. The note says
      adequacy would require practitioners; #long goes further and concedes the outcome:
      against the strong reading, where the view advances a rival axiology rather than a
      redescription, 'it ties rather than wins: the concern is portable across
      descriptions, not across every axiology.' A locus whose exposure is already conceded
      at greater strength one locus over is answered. The registered (d) at
      indigenous-philosophy#long already carries the bedrock this would otherwise route to,
      the relational-holist / seat-of-standing facet of impersonal-vs-person-affecting; a
      second (d) here would restate a registered residue rather than route a new one, which
      the force floor and the anti-inflation gates both forbid.""",
      "a", {"answered_by": ["indigenous-philosophy#long"]}),

    E("flow-states-csikszentmihalyi",
      "The Dismantle response presents the EFIList counter-interpretation but acknowledges this is an open question",
      """Your note reports that your Dismantle response acknowledges the interpretation is
      an open question. Read it: it does not. It argues that flow IS deficit management,
      calls autotelic activity the most damning confirmation of the deficit grammar, and
      only then grants intrinsic value arguendo in order to show it would change nothing.
      Granting a premise to defeat it is not conceding the question is open. So your
      apparatus hands me a concession your argument never made. Worse, your RSI calibration
      notes name this very node as the worked example of an entry that honestly
      acknowledges a contested premise. The apparatus that grades intellectual honesty has
      misread the one case it cites.""",
      """The defect is locus-local and the node cannot cure a false description of itself.
      #long's position is that the deficit reading is correct AND that the alternative is
      moot; the note reports the weaker claim that the question is open, conceding ground
      the response refused. Best reading tested and rejected: granting arguendo does signal
      the author does not treat the reading as beyond dispute, but the note's word is
      'acknowledges', which attributes an epistemic stance rather than a concessive move,
      and the difference is exactly what an objector quotes. SECOND INSTANCE MEASURED: the
      flagship's RSI calibration notes cite this node 'acknowledging the open question on
      intrinsic positive value' as the exemplar of honest acknowledgment scoring lower on
      Robustness. That string occurs once in combined.html and in NEITHER the corpus JSON
      nor the JSX, so the repair spans a corpus locus and a flagship-only locus and the
      flagship half is a pin move. Severity headline because the exposure reaches the
      grading apparatus rather than this node. Honest limit: the calibration note is
      illustrative prose, not a scoring input, so no RSI value is shown to be wrong.""",
      "b", {"regen_candidate": {"axis_hit": ["s", "r"], "severity": "headline"}}),

    E("eliminativism",
      "refutation is dialectical (non-selectivity) rather than a knockdown of the metaphysics",
      """You concede that your refutation is dialectical and lands no knockdown on the
      metaphysics. Then the illusionist who holds the view for reasons predating this
      debate is untouched: non-selectivity bites only someone applying eliminativism
      selectively. Your strongest cluster member survives your strongest reply, on your own
      accounting.""",
      """Met, and the node CURES. #long concedes the same limit, that non-selectivity is
      'decisive against the objection's dialectical use even if the metaphysics stays
      contested', and then answers the non-selective case rather than leaving it standing:
      the symmetric eliminativist 'arrives at global nihilism', and 'a barren ledger hands
      the antinatalist everything, for where nothing is good, there is no good reason to
      set a new sufferer running, illusion or not.' The honest illusionist is met on the
      merits, so no knockdown of the metaphysics is needed for the node's conclusion. The
      registered (d) at eliminativism#long is on whether the property conserved under
      redescription is intrinsically disvaluable, a different question.""",
      "a", {"answered_by": ["eliminativism#long"]}),
]

NOT_AUTHORED = {
    "violence-as-reductio": "(i) apparatus. Sibling taxonomy plus build-pass provenance ('first taxonomically committed in session 4h-alt', '6 source-vehicles in build-pass batches 1 and 3'). Also UNREACHABLE: no confidence key, so combined.html emits no [NOTE] button.",
    "solipsism": "(i) apparatus. Cluster taxonomy plus a TIER NOTE addressed to a future editor. Also UNREACHABLE: confidence full suppresses the button that would reveal it, and the note is the text that explains that value.",
    "suffering-as-meaning": "(i) apparatus. Cluster taxonomy plus a ratification-delta line, 'inclusion bumps the ratified delta 78->80 to 78->81', which is build accounting and means nothing to a reader.",
    "neuroscience-positive-states": "(ii) scope qualifier, and a legitimate one. It says the philosophical interpretation of neural reward remains open; #long grants the positive interpretation in full and argues it does not reach across the threshold, so the note concedes nothing the response denies. Checked against #long rather than assumed.",
}


def main():
    corpus_path = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
    raw = open(corpus_path, "rb").read()
    corpus = json.loads(raw.decode("utf-8"))
    nodes = {o["id"]: o for o in corpus["objections"]}

    note_nodes = sorted(i for i, o in nodes.items() if V.node_has_note(o))
    authored = sorted(e["target_id"] for e in ENTRIES)

    # ---- assertions, before anything is written ---------------------------------
    assert len(set(authored)) == len(authored), "a node is authored twice"
    for e in ENTRIES:
        n = nodes[e["target_id"]]
        assert V.node_has_note(n), "%s has no note" % e["target_id"]
        txt = V.locus_text(n, V.NOTE_LOCUS)
        assert e["target_anchor"] in txt, \
            "anchor not verbatim in %s#note: %r" % (e["target_id"], e["target_anchor"])
        aw = len(e["target_anchor"].split())
        assert 0 < aw <= 15, "%s anchor is %d words" % (e["target_id"], aw)
        mw = len(e["adversarial_move"].split())
        lo, hi = 40, (60 if e["class"] == "a" else 150)
        assert lo <= mw <= hi, "%s move is %d words (class %s band %d-%d)" % (
            e["target_id"], mw, e["class"], lo, hi)
        assert not V.DASH_TOKEN_RE.search(e["adversarial_move"]), \
            "%s move carries a standalone dash token" % e["target_id"]
        assert e["adversarial_move"].isascii(), "%s move is not ASCII" % e["target_id"]
        # an (a) must name an answering locus that EXISTS
        if e["class"] == "a":
            for ref in e["routing"]["answered_by"]:
                nid, loc = ref.split("#")
                assert nid in nodes and V.locus_valid(nodes[nid], loc), "bad answered_by %r" % ref
    # every unauthored note node must carry a stated reason
    for i in note_nodes:
        if i not in authored:
            assert i in NOT_AUTHORED, "unauthored note node %s has no stated reason" % i
    assert sorted(list(authored) + list(NOT_AUTHORED)) == note_nodes, \
        "authored + not-authored != the note-bearing node set"

    cls = collections.Counter(e["class"] for e in ENTRIES)
    closure = {"%s#%s" % (e["target_id"], V.NOTE_LOCUS): "closed" for e in ENTRIES}

    doc = {
        "meta": {
            "artifact": "adv_map_phaseG_v0_1.json",
            "phase": "G -- the top-level `note` key, authored NARROWLY",
            "state": "MAPPED, PRE-TRIAGE. Lifecycle lives in project_canon, never here.",
            "authored": "%s, %s" % (DATE, SEAT),
            "source_corpus": "efilist_argument_library_v4_0_0.json",
            "source_corpus_md5": V.md5_bytes(raw),
            "source_corpus_objections_md5": V.objections_digest(corpus),
            "ruling_0a": ("Josiah, K349, delegated to this seat, which took the NARROW form: "
                          "`note` is a map target, authored only where a note makes or concedes a "
                          "claim the corpus would have to defend. The classification was measured "
                          "BEFORE the disposition was put up, per ccclxviii applied to a scope "
                          "question: of nine notes, 3 are apparatus, 1 is a legitimate scope "
                          "qualifier, and 5 carry a claim."),
            "not_authored": NOT_AUTHORED,
            "class_counts": dict(cls),
            "coverage_distinct_ids": len(set(authored)),
            "note_coverage": "%d/%d" % (len(set(authored)), len(note_nodes)),
            "locus_closure": closure,
            "coverage_note": ("This fragment adds NO primary-ladder coverage. Per the K349 "
                              "coverage ruling a note locus does not make a node covered, so "
                              "`coverage` is unchanged at 82/82 from the primary entries."),
            "not_in_scope": ("`confidence` (ruled OUT as a map target by Josiah, K349: no corpus "
                             "text to anchor; filed as a regen candidate instead), "
                             "`objectionSubforms` (ruled OUT at K345, no render site), and the "
                             "four notes listed in not_authored."),
            "validator": "adv_map_validator_v0_6.py",
        },
        "entries": ENTRIES,
    }

    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "adv_map_phaseG_v0_1.json")
    out = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    open(dest, "wb").write(out)
    print("wrote %s  %s  %d B" % (dest, V.md5_bytes(out), len(out)))
    print("  entries %d  classes %s  note_coverage %s"
          % (len(ENTRIES), dict(cls), doc["meta"]["note_coverage"]))


if __name__ == "__main__":
    main()
