# v4.1.0 regen spec v0.1 — the three subtractive repairs

**PROPOSED, NEVER APPLIED.** This file is an input to a ratification, not a change. No
corpus byte moves here, `combined.html` is untouched, and the pin does not move. The repo's
own disposition is explicit that a `/combined` graft is ratified by Josiah **and** the
library seat and then executed in a *deliberate isolated pin-move session*, which forces a
same-session wuld search-index regen and objection re-vendor. Opening that cut inside a
session doing other work would be `C8` with the rule not even silent.

These three are the **pure-subtraction** entries of the nineteen-item v4.1.0 enrichment
queue: each removes a claim that is false or unsupported, and none adds a new argument.
They are first because they are the only ones whose correctness can be judged without
re-litigating any philosophy — the question is whether the sentence is true, not
whether the move is good. Note that *subtractive* classifies the CLAIM, not the word count:
`R1` is +34 words, because saying why a statistic fails to license an inference takes more
room than the inference took. That is flagged in its own scope note and a shorter
bare-deletion variant is carried beside it.

| | node | locus | sev | spans | words | delta | anchor destroyed |
|---|---|---|---|---|---|---|---|
| `R1` | `happiness-is-choice` | long | headline | 1 | 555 → 589 | +34 | yes |
| `R2` | `just-edgy` | long | minor | 1 | 220 → 220 | +0 | yes |
| `R3` | `just-depressed` | long | minor | 3 | 979 → 978 | -1 | yes |

## Why anchor destruction is the success criterion, not a side effect

Each of these nodes carries a Phase E map entry classed `(b)`, and each entry's verbatim
anchor is cut from the exact sentence being repaired. So a successful repair **must** break
its own entry's `anchor-rule` check. An anchor that still matches after a subtractive regen
is proof the defect is still in the text. This builder asserts destruction for all three and
refuses to write if any anchor survives — which makes the post-cut map failure the
*receipt* for the repair rather than bookkeeping left over from it.

Consequence for sequencing: after the cut, `adversarial_map_v1_0.json` fails `meta-corpus-pin`
(both the whole-file md5 and the objections digest move) and three entries fail `anchor-rule`.
K332's finding applies directly — a failing corpus pin **silently skips seven downstream
checks**, `anchor-rule` among them — so the map must be re-pinned in the same session as
the cut, not the next one. Leaving it stale would reproduce the exact month-long blind spot
that v0_2 was built to close.

---

## `R1` — `happiness-is-choice#long` (headline, axis `s`)

**Map anchor (Phase E, class b):** `roughly half of your capacity for happiness was determined at conception`

**The defect.** A heritability coefficient is a population statistic: it partitions the variance BETWEEN people, and says nothing about what fraction of any one person's trait was fixed at conception. The corpus states the misreading outright and then builds a pie-chart carve-up on top of it. It is the standard undergraduate correction, which makes it the most exposed sentence in the corpus: a competent objector does not need to be right about anything else to be right about this.

**What survives.** The differences in how people fare are substantially driven by unchosen factors, and the non-genetic remainder is not a reservoir of choice either. That is the whole of what the paragraph needed, and the corrected version says it without the false step.

**Scope note.** SUBTRACTIVE IN CLAIM, +34 IN WORDS, and the mismatch is named rather than smoothed over. The conception-fraction inference and the slice-of-the-pie framing both go; what replaces them is two sentences saying what the statistic does and does not license. Naming why a number fails to license an inference costs more words than making the inference did, which is why no version of this repair is word-neutral. A bare deletion IS available and is carried below as R1-alt; the recommendation is the interpreted version, because this paragraph's job in the node is to say why the empirical finding bears on a claim about choice, and a bare number left standing does not do that job.

**Span — now:**

> First, the empirical failure: behavioral genetics research consistently demonstrates that approximately 40-50% of the variance in subjective wellbeing is heritable. This means that roughly half of your capacity for happiness was determined at conception—before any 'choice' was possible. The remaining variance is split between environmental factors (which are largely unchosen—your birthplace, your family, your socioeconomic position, your era) and a modest contribution from intentional activity. The portion of wellbeing that is genuinely under voluntary control is the smallest slice of the pie.

**Span — proposed:**

> First, the empirical failure: behavioral genetics research consistently finds that 40-50% of the variance between people in subjective wellbeing tracks genetic variance. That is a population statistic, not a personal budget—it does not say that half of any given person's happiness was fixed at conception, and the correction is owed before anything is built on the number. What it does establish is enough: the differences in how well people fare are driven substantially by factors nobody selected. Nor is the remainder a reservoir of choice—the environmental share is itself largely unchosen (your birthplace, your family, your socioeconomic position, your era), and the voluntarist needs whatever is left over to be volitional, which no such study delivers.

Response word count 555 → 589 (+34).

**`R1-alt` — the bare-deletion variant, NOT recommended.** A bare deletion, which is what `repair_shape: subtractive` literally implies. It is shorter and honest and it gives up the paragraph's argumentative work.

> First, the empirical failure: behavioral genetics research consistently finds that 40-50% of the variance between people in subjective wellbeing tracks genetic variance, and the environmental share of the remainder is itself largely unchosen—your birthplace, your family, your socioeconomic position, your era.

---

## `R2` — `just-edgy#long` (minor, axis `s`)

**Map anchor (Phase E, class b):** `has never been substantively refuted`

**The defect.** An argument from silence offered as a credential. Absence of published refutation is not evidential support, and no charitable reading turns it into any. The surrounding lineage material is legitimate and survives on the best reading, because the objection makes an empirical claim about who holds the view and the lineage answers it directly; the unrefutedness clause is separable and is not rescuable.

**What survives.** The lineage, and the observation that the dismissal categorizes rather than engages -- which is the node's actual charge and is something a reader can check.

**Scope note.** Reception is now described (more often categorized than answered) rather than adjudicated (never refuted). The first is observable; the second was a claim about the entire literature that nobody had surveyed.

**Span — now:**

> Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire pessimist tradition into a work that has never been substantively refuted—only dismissed with the exact social categorization you are deploying now.

**Span — proposed:**

> Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire pessimist tradition into a single sustained work—one far more often categorized than answered, in exactly the register you are using now.

Response word count 220 → 220 (+0).

---

## `R3` — `just-depressed#long` (minor, axis `s`)

**Map anchor (Phase E, class b):** `Roughly one deployment in a hundred is a person actually worried about you`

**The defect.** An unsourced quantitative premise doing architectural work -- the one-in-a-hundred / ninety-nine split organises the node's opening and its close -- inside the corpus's most epistemically self-aware rebuttal, which elsewhere refuses exactly this move. Minor rather than headline only because the logical core is fully separable and survives deletion intact.

**What survives.** The distribution, stated qualitatively, and the rare honest interlocutor named and met in good faith. Nothing in the argument depended on the ratio being 1:99 rather than 1:20; it depended on genuine concern being the exception, which the corrected text says.

**Scope note.** Three spans, because the figure recurs. A repair that fixed the opening and left the close still counting to ninety-nine would have produced a node that contradicts itself -- the recurrence is why this one is listed as three edits rather than one.

**Span 1 — now:**

> Roughly one deployment in a hundred is a person actually worried about you. The rebuttal is built for the ninety-nine, and it names the one honestly rather than pretending it away.

**Span 1 — proposed:**

> Genuine concern is the rare exception here, not the ordinary case. The rebuttal is built for the ordinary case, and it names the exception honestly rather than pretending it away.

**Span 2 — now:**

> The one-in-a-hundred who genuinely worries is making the argument-level case

**Span 2 — proposed:**

> The one who genuinely worries is making the argument-level case

**Span 3 — now:**

> The ninety-nine are doing neither; they have changed the subject.

**Span 3 — proposed:**

> The rest are doing neither; they have changed the subject.

Response word count 979 → 978 (-1).

---

## What this spec does not decide

The remaining sixteen v4.1.0 items are untouched: five are `structural`, ten are `additive`,
and one (`selfish-lazy#long`) is coupled to the diagnosis node and therefore travels with the
v5.0.0 intake cut rather than this one. `cant-prove-nonexistence-better#long` is marked
subtractive but carries an `r`-axis component as well, so it is not pure subtraction and is
not in this three. Nothing here commits the cut to a size; it commits three sentences to a
verdict.

