#!/usr/bin/env python3
"""Build v4_1_0_regen_spec_v0_1.md -- the ratification input for the v4.1.0 subtractive regens.

PROPOSED, NEVER APPLIED. This builder writes a SPEC. It does not touch the corpus, it does
not touch combined.html, and it moves no served byte. The repo's own disposition requires
that a /combined graft be ratified by Josiah AND the library seat and then executed in a
deliberate isolated pin-move session; this artifact is the input that ratification needs.

Every BEFORE span is verified verbatim and unique against the corpus before anything is
written, and every AFTER span is verified absent. The builder refuses to write otherwise.

Binary read + explicit decode throughout: open() in text mode takes the LOCALE encoding,
utf-8 on Linux and cp1252 on Windows (ccclx).
"""
import json, sys, hashlib, re

CORPUS = "../efilist_argument_library_v4_0_0.json"
MAP    = "adversarial_map_v1_0.json"
OUT    = "v4_1_0_regen_spec_v0_1.md"
EM     = "—"

R = [
 dict(id="R1", anchor='roughly half of your capacity for happiness was determined at conception', node="happiness-is-choice", locus="long", sev="headline", axis="s",
      why="A heritability coefficient is a population statistic: it partitions the variance "
          "BETWEEN people, and says nothing about what fraction of any one person's trait was "
          "fixed at conception. The corpus states the misreading outright and then builds a "
          "pie-chart carve-up on top of it. It is the standard undergraduate correction, which "
          "makes it the most exposed sentence in the corpus: a competent objector does not need "
          "to be right about anything else to be right about this.",
      keep="The differences in how people fare are substantially driven by unchosen factors, and "
           "the non-genetic remainder is not a reservoir of choice either. That is the whole of "
           "what the paragraph needed, and the corrected version says it without the false step.",
      note="SUBTRACTIVE IN CLAIM, +34 IN WORDS, and the mismatch is named rather than smoothed "
           "over. The conception-fraction inference and the slice-of-the-pie framing both go; what "
           "replaces them is two sentences saying what the statistic does and does not license. "
           "Naming why a number fails to license an inference costs more words than making the "
           "inference did, which is why no version of this repair is word-neutral. A bare deletion "
           "IS available and is carried below as R1-alt; the recommendation is the interpreted "
           "version, because this paragraph's job in the node is to say why the empirical finding "
           "bears on a claim about choice, and a bare number left standing does not do that job.",
      alt=("A bare deletion, which is what `repair_shape: subtractive` literally implies. It is "
           "shorter and honest and it gives up the paragraph\'s argumentative work.",
           "First, the empirical failure: behavioral genetics research consistently finds that "
           "40-50% of the variance between people in subjective wellbeing tracks genetic variance, "
           "and the environmental share of the remainder is itself largely unchosen" + EM + "your "
           "birthplace, your family, your socioeconomic position, your era."),
      before="First, the empirical failure: behavioral genetics research consistently demonstrates "
             "that approximately 40-50% of the variance in subjective wellbeing is heritable. This "
             "means that roughly half of your capacity for happiness was determined at conception"
             + EM + "before any 'choice' was possible. The remaining variance is split between "
             "environmental factors (which are largely unchosen" + EM + "your birthplace, your "
             "family, your socioeconomic position, your era) and a modest contribution from "
             "intentional activity. The portion of wellbeing that is genuinely under voluntary "
             "control is the smallest slice of the pie.",
      after="First, the empirical failure: behavioral genetics research consistently finds that "
            "40-50% of the variance between people in subjective wellbeing tracks genetic variance. "
            "That is a population statistic, not a personal budget" + EM + "it does not say that "
            "half of any given person's happiness was fixed at conception, and the correction is "
            "owed before anything is built on the number. What it does establish is enough: the "
            "differences in how well people fare are driven substantially by factors nobody "
            "selected. Nor is the remainder a reservoir of choice" + EM + "the environmental share "
            "is itself largely unchosen (your birthplace, your family, your socioeconomic position, "
            "your era), and the voluntarist needs whatever is left over to be volitional, which no "
            "such study delivers."),
 dict(id="R2", anchor='has never been substantively refuted', node="just-edgy", locus="long", sev="minor", axis="s",
      why="An argument from silence offered as a credential. Absence of published refutation is "
          "not evidential support, and no charitable reading turns it into any. The surrounding "
          "lineage material is legitimate and survives on the best reading, because the objection "
          "makes an empirical claim about who holds the view and the lineage answers it directly; "
          "the unrefutedness clause is separable and is not rescuable.",
      keep="The lineage, and the observation that the dismissal categorizes rather than engages "
           "-- which is the node's actual charge and is something a reader can check.",
      note="Reception is now described (more often categorized than answered) rather than "
           "adjudicated (never refuted). The first is observable; the second was a claim about the "
           "entire literature that nobody had surveyed.",
      before="Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire "
             "pessimist tradition into a work that has never been substantively refuted" + EM +
             "only dismissed with the exact social categorization you are deploying now.",
      after="Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire "
            "pessimist tradition into a single sustained work" + EM + "one far more often "
            "categorized than answered, in exactly the register you are using now."),
 dict(id="R3", anchor='Roughly one deployment in a hundred is a person actually worried about you', node="just-depressed", locus="long", sev="minor", axis="s",
      why="An unsourced quantitative premise doing architectural work -- the one-in-a-hundred / "
          "ninety-nine split organises the node's opening and its close -- inside the corpus's most "
          "epistemically self-aware rebuttal, which elsewhere refuses exactly this move. Minor "
          "rather than headline only because the logical core is fully separable and survives "
          "deletion intact.",
      keep="The distribution, stated qualitatively, and the rare honest interlocutor named and met "
           "in good faith. Nothing in the argument depended on the ratio being 1:99 rather than "
           "1:20; it depended on genuine concern being the exception, which the corrected text says.",
      note="Three spans, because the figure recurs. A repair that fixed the opening and left the "
           "close still counting to ninety-nine would have produced a node that contradicts itself "
           "-- the recurrence is why this one is listed as three edits rather than one.",
      spans=[
        ("Roughly one deployment in a hundred is a person actually worried about you. The rebuttal "
         "is built for the ninety-nine, and it names the one honestly rather than pretending it away.",
         "Genuine concern is the rare exception here, not the ordinary case. The rebuttal is built "
         "for the ordinary case, and it names the exception honestly rather than pretending it away."),
        ("The one-in-a-hundred who genuinely worries is making the argument-level case",
         "The one who genuinely worries is making the argument-level case"),
        ("The ninety-nine are doing neither; they have changed the subject.",
         "The rest are doing neither; they have changed the subject."),
      ]),
]

def locus_text(o, locus):
    """The map's locus vocabulary is short/medium/long/diagnosis. The first three live under
    responses; `diagnosis` is the node's own field. Getting this wrong silently skips two of
    the map's 93 anchors, so it is a function rather than a subscript."""
    return o["diagnosis"] if locus == "diagnosis" else o["responses"][locus]


def spans_of(r):
    return r["spans"] if "spans" in r else [(r["before"], r["after"])]

def main():
    corpus = json.loads(open(CORPUS, "rb").read().decode("utf-8"))
    cmap   = json.loads(open(MAP, "rb").read().decode("utf-8"))
    O = {o["id"]: o for o in corpus["objections"]}
    anchors = {(e["target_id"], e["target_locus"]): e for e in cmap["entries"]}
    fail = []

    for r in R:
        key = (r["node"], r["locus"])
        if key not in anchors:
            fail.append("%s: no map entry for %s#%s" % (r["id"], r["node"], r["locus"])); continue
        text = locus_text(O[r["node"]], r["locus"])
        new  = text
        for i, (b, a) in enumerate(spans_of(r), 1):
            if text.count(b) != 1:
                fail.append("%s span %d: BEFORE occurs %d times, must be exactly 1" % (r["id"], i, text.count(b)))
            if a in text:
                fail.append("%s span %d: AFTER already present in the corpus" % (r["id"], i))
            new = new.replace(b, a, 1)
        r["_before_words"] = len(text.split())
        r["_after_words"]  = len(new.split())
        r["_new"] = new
        # THE INVARIANT THAT MATTERS: a subtractive repair must DESTROY the map's anchor.
        # An anchor that survives means the defect the entry names is still in the text.
        hits = [i for i, e in enumerate(cmap["entries"])
                if (e["target_id"], e["target_locus"]) == key and e["target_anchor"] == r["anchor"]]
        if len(hits) != 1:
            fail.append("%s: %d map entries match %s#%s with the declared anchor, need exactly 1"
                        % (r["id"], len(hits), r["node"], r["locus"]))
            continue
        r["_idx"] = hits[0]
        anc = r["anchor"]
        r["_anchor"] = anc
        if anc not in text:
            fail.append("%s: map anchor is not in the SHIPPED text -- the map is already stale" % r["id"])
        if anc in new:
            fail.append("%s: map anchor SURVIVES the repair -- the defect is still there" % r["id"])
        r["_delta"] = r["_after_words"] - r["_before_words"]

    patched  = {(r["node"], r["locus"]): r["_new"] for r in R if "_new" in r}
    intended = {r["_idx"] for r in R if "_idx" in r}

    # POST-REPAIR ANCHOR SWEEP. The first draft of this check looped over map entries and
    # skipped any whose key was in `intended` -- but `patched` and `intended` hold the SAME
    # keys, so the body was unreachable and it could only ever report success. That is C6, a
    # check that fails in one direction, written while documenting C6. Replaced with a sweep
    # that can fail: re-check EVERY anchor against the corpus as it would stand after all
    # three repairs, and require exactly the three intended entries to break.
    def patched_text(o, locus):
        k = (o["id"], locus)
        return patched[k] if k in patched else locus_text(o, locus)
    broke = {i for i, e in enumerate(cmap["entries"])
             if e["target_anchor"] not in patched_text(O[e["target_id"]], e["target_locus"])}
    if broke != intended:
        for i in sorted(broke - intended):
            e = cmap["entries"][i]
            fail.append("COLLATERAL: %s#%s (%r) anchor destroyed but not intended"
                        % (e["target_id"], e["target_locus"], e["target_anchor"][:40]))
        for i in sorted(intended - broke):
            e = cmap["entries"][i]
            fail.append("%s#%s anchor SURVIVES the repair -- the defect is still there"
                        % (e["target_id"], e["target_locus"]))
    touched = {(r["node"], r["locus"]) for r in R}
    same_locus = sum(1 for e in cmap["entries"]
                     if (e["target_id"], e["target_locus"]) in touched) - len(R)
    # STALENESS CHECK. Every anchor the map holds must be present in the corpus as shipped, or
    # this spec is being written against a target that has already moved.
    for e in cmap["entries"]:
        if e["target_anchor"] not in locus_text(O[e["target_id"]], e["target_locus"]):
            fail.append("map anchor for %s#%s is not in the shipped corpus"
                        % (e["target_id"], e["target_locus"]))

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f in fail: print("  " + f)
        return 1

    L = []; w = L.append
    w("# v4.1.0 regen spec v0.1 " + EM + " the three subtractive repairs"); w("")
    w("**PROPOSED, NEVER APPLIED.** This file is an input to a ratification, not a change. No")
    w("corpus byte moves here, `combined.html` is untouched, and the pin does not move. The repo's")
    w("own disposition is explicit that a `/combined` graft is ratified by Josiah **and** the")
    w("library seat and then executed in a *deliberate isolated pin-move session*, which forces a")
    w("same-session wuld search-index regen and objection re-vendor. Opening that cut inside a")
    w("session doing other work would be `C8` with the rule not even silent.")
    w("")
    w("These three are the **pure-subtraction** entries of the nineteen-item v4.1.0 enrichment")
    w("queue: each removes a claim that is false or unsupported, and none adds a new argument.")
    w("They are first because they are the only ones whose correctness can be judged without")
    w("re-litigating any philosophy " + EM + " the question is whether the sentence is true, not")
    w("whether the move is good. Note that *subtractive* classifies the CLAIM, not the word count:")
    w("`R1` is +34 words, because saying why a statistic fails to license an inference takes more")
    w("room than the inference took. That is flagged in its own scope note and a shorter")
    w("bare-deletion variant is carried beside it.")
    w("")
    w("| | node | locus | sev | spans | words | delta | anchor destroyed |")
    w("|---|---|---|---|---|---|---|---|")
    for r in R:
        w("| `%s` | `%s` | %s | %s | %d | %d \u2192 %d | %+d | yes |"
          % (r["id"], r["node"], r["locus"], r["sev"], len(spans_of(r)),
             r["_before_words"], r["_after_words"], r["_delta"]))
    w("")
    w("## Why anchor destruction is the success criterion, not a side effect"); w("")
    w("Each of these nodes carries a Phase E map entry classed `(b)`, and each entry's verbatim")
    w("anchor is cut from the exact sentence being repaired. So a successful repair **must** break")
    w("its own entry's `anchor-rule` check. An anchor that still matches after a subtractive regen")
    w("is proof the defect is still in the text. This builder asserts destruction for all three and")
    w("refuses to write if any anchor survives " + EM + " which makes the post-cut map failure the")
    w("*receipt* for the repair rather than bookkeeping left over from it.")
    w("")
    w("Consequence for sequencing: after the cut, `adversarial_map_v1_0.json` fails `meta-corpus-pin`")
    w("(both the whole-file md5 and the objections digest move) and three entries fail `anchor-rule`.")
    w("K332's finding applies directly " + EM + " a failing corpus pin **silently skips seven downstream")
    w("checks**, `anchor-rule` among them " + EM + " so the map must be re-pinned in the same session as")
    w("the cut, not the next one. Leaving it stale would reproduce the exact month-long blind spot")
    w("that v0_2 was built to close.")
    w("")
    for r in R:
        w("---"); w("")
        w("## `%s` " % r["id"] + EM + " `%s#%s` (%s, axis `%s`)" % (r["node"], r["locus"], r["sev"], r["axis"]))
        w("")
        w("**Map anchor (Phase E, class b):** `%s`" % r["_anchor"]); w("")
        w("**The defect.** %s" % r["why"]); w("")
        w("**What survives.** %s" % r["keep"]); w("")
        w("**Scope note.** %s" % r["note"]); w("")
        for i, (b, a) in enumerate(spans_of(r), 1):
            lbl = (" " + str(i)) if len(spans_of(r)) > 1 else ""
            w("**Span%s " % lbl + EM + " now:**"); w("")
            w("> " + b); w("")
            w("**Span%s " % lbl + EM + " proposed:**"); w("")
            w("> " + a); w("")
        w("Response word count %d \u2192 %d (%+d)."
          % (r["_before_words"], r["_after_words"], r["_delta"])); w("")
        if r.get("alt"):
            w("**`%s-alt` " % r["id"] + EM + " the bare-deletion variant, NOT recommended.** %s" % r["alt"][0]); w("")
            w("> " + r["alt"][1]); w("")
    w("---"); w("")
    w("## What this spec does not decide"); w("")
    w("The remaining sixteen v4.1.0 items are untouched: five are `structural`, ten are `additive`,")
    w("and one (`selfish-lazy#long`) is coupled to the diagnosis node and therefore travels with the")
    w("v5.0.0 intake cut rather than this one. `cant-prove-nonexistence-better#long` is marked")
    w("subtractive but carries an `r`-axis component as well, so it is not pure subtraction and is")
    w("not in this three. Nothing here commits the cut to a size; it commits three sentences to a")
    w("verdict.")
    w("")
    out = "\n".join(L) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode()
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), hashlib.md5(b).hexdigest()))
    print("  %d repairs, %d spans; all BEFORE verbatim+unique, all AFTER absent"
          % (len(R), sum(len(spans_of(r)) for r in R)))
    print("  post-repair anchor sweep over all %d map anchors: exactly %d broke, and they are the "
          "%d intended" % (len(cmap["entries"]), len(intended), len(intended)))
    print("  co-located entries the sweep could have caught as collateral: %d %s"
          % (same_locus, "(none exist for these three nodes -- the sweep examined them and found none, "
             "which is not the same as the check being vacuous)" if same_locus == 0 else ""))
    for r in R:
        print("   %s %-22s %4d -> %4d words (%+d)" % (r["id"], r["node"], r["_before_words"], r["_after_words"], r["_delta"]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
