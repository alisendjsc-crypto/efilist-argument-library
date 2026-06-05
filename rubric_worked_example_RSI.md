# How an RSI Grade Is Made

*The rubric, walked end-to-end on one node — `privileged-first-world`.*

A grade you cannot reconstruct reads as self-congratulation. A grade you can reconstruct reads as rigor. This page hands you the whole machine: the five axes in plain language, the one formula, the band rule, and one real node carried from its five scores to its final letter — including the deliberate point where the displayed number and the grade disagree.

---

## The rule, in one line

**RSI = (v · s · c · r · a)^(1/5) · 100**

Five axes, each a judgment in **[0, 1]**. The score is their **geometric mean**, read as a percentage. Bands:

| Band | Cutoff (on the *unrounded* mean) |
|---|---|
| **A** | ≥ 0.88 |
| **B** | ≥ 0.82 |
| **C** | ≥ 0.76 |
| **D** | < 0.76 |

Two conventions that matter and are easy to miss:

- **Banding uses the unrounded mean.** The grade is decided on the exact geometric mean, *before* any rounding.
- **Display rounds to one decimal.** The percentage you see is `round(mean × 100, 1)` — for reading only. It is never an input to the grade.

The consequence is built in on purpose: a node can *display* 88.0 and still be graded **B**, because the exact mean was a hair under 0.88. The rubric does not round its way to a higher letter. (Worked below, on PFW.)

---

## Why a geometric mean, not an average

The five axes are **conjunctive**: a rebuttal is only as strong as its weakest dimension. A flawless logical spine cannot buy back a robustness hole — if the strongest counter-move is left standing, the rebuttal is not "mostly fine."

The geometric mean enforces that; an arithmetic mean would launder it. Take a rebuttal that is logically sharp but leaves the hardest reply unanswered:

- scores `v=.95, s=.90, c=.90, r=.50, a=.90`
- **arithmetic** mean = 0.830 → would read **B**
- **geometric** mean = 0.809 → reads **C**

The single weak axis (`r = .50`) costs a full band under the geometric mean and is averaged away under the arithmetic one. That gap *is* the rigor. A rebuttal cannot be strong on balance; it has to be strong on its weakest leg.

---

## The five axes

> **Provenance:** these definitions are reconstructed from the corpus's own grading rationales and pending ratification as the canonical legend. `r` and `a` are fixed by the grading record; `v` is strongly indicated; `s` and `c` are the working readings.

- **v — Validity.** Granting its premises, does the rebuttal's central inference actually follow? The logical spine: no equivocation, no fallacy, the conclusion genuinely carried by the move.
- **s — Soundness.** Are the premises it stands on true and well-grounded — and is its load *not* staked on a single contestable empirical claim? (A rebuttal that wins only if one disputed fact holds is fragile here.)
- **c — Cogency.** Is the reasoning expressed clearly and followably — would a careful reader track the move without supplying the missing steps themselves?
- **r — Robustness.** Does it preempt the live counter-moves and route the surviving residue to a *named* terminus — or does it leave the strongest reply dangling?
- **a — Charity.** Does it engage the objection at its strongest form (the steelman), rather than scoring against a weak version? Over-claiming — for the rebuttal, or against the objection — drags this axis.

The project's own diagnostic shorthand maps straight onto two of these: an **"A-drag"** node has a low `a` (a charity / over-claim fault); an **"R-drag"** node has a low `r` (an unpreempted counter-move). They are not separate metrics — they name *which axis* is holding a grade down.

---

## Worked node: `privileged-first-world`

**The objection.** You only think life isn't worth starting because you're a comfortable first-worlder. The global poor keep choosing to have children and report finding life worth living — so your verdict is a class artifact, not a truth about existence.

**The rebuttal's shape.** It is a standpoint / genetic-fallacy challenge, so the rebuttal answers in kind: the *origin* of a belief does not settle its *truth* (the charge is a genetic fallacy), and the same move cuts the other way — comfort could just as easily distort *toward* pro-natal optimism as pessimism, so the standpoint argument is symmetric and proves nothing about who is right. It grants the narrow legitimate point (situated judgment deserves scrutiny) while showing that scrutiny does not reach the *validity* of the asymmetry or consent arguments, which are evaluated standpoint-independently.

**The five scores (canonical, from the ledger):**

| axis | score | reading |
|---|---|---|
| v | 0.90 | the genetic-fallacy diagnosis is logically clean |
| s | 0.85 | rests partly on a contestable symmetry claim (comfort-distortion cuts both ways) — slightly off the top |
| c | 0.90 | the move is stated plainly |
| r | 0.85 | preempts the main replies but grants a narrow standpoint point, leaving a small residue |
| a | 0.90 | engages the strong version, not the lazy "you're privileged" jab |

The two `0.85`s (`s`, `r`) are the profile's weaker legs — exactly what a standpoint-rebuttal that *grants a narrow point* should look like. The numbers are the grader's judgment on each axis; the rest of this page is arithmetic anyone can repeat.

### Long form — the headline grade

```
axes      v=.90  s=.85  c=.90  r=.85  a=.90
product   .90 · .85 · .90 · .85 · .90  = 0.5267025
mean      0.5267025 ^ (1/5)            = 0.879656
× 100                                  = 87.9656
display   round(87.9656, 1)            = 88.0
band      0.879656 < 0.88              → B
```

**This is the whole point of the two conventions.** PFW's long form **displays 88.0** but is **graded B**, because banding uses the exact mean (0.879656) and that sits just under the A line. It is not an error and not a near-miss to be nudged — it is the rubric declining to promote a sub-threshold rebuttal on a rounding artifact. **12 of 243 cells sit on such an edge.** PFW is the cleanest one, which is why it is the worked example.

### All three registers — the depth modifier

A shorter rebuttal is graded on a modified profile, because brevity costs exactly two things: room to be fully clear (`c`) and room to preempt counter-moves and route residue (`r`). Validity, soundness, and charity do not degrade with length the way those two do — so the modifier touches only `c` and `r`:

| register | modifier | axes (v, s, c, r, a) | mean | display | band |
|---|---|---|---|---|---|
| **long** | base axes | .90, .85, .90, .85, .90 | 0.879656 | 88.0 | **B** |
| **medium** | c −0.05, r −0.03 | .90, .85, .85, .82, .90 | 0.863449 | 86.3 | **B** |
| **short** | c −0.12, r −0.06 | .90, .85, .78, .79, .90 | 0.842428 | 84.2 | **B** |

PFW grades **B / B / B**. Every number in this table is reproducible from the five base scores plus the modifier above — that is what "reconstructable" means.

> **One wrinkle the rubric is honest about.** Where a shorter register's *prose* has been independently rewritten and re-graded (as `benatar-asymmetry-attack`'s short and medium forms were), that register carries its own freshly-judged axis scores rather than the modifier-derived ones. The modifier is the default, not a law — a strengthened short form earns its own grade.

---

## What this guarantees

Hand a skeptic the five axis scores and this page. They will compute the same percentage, apply the same band, and land on the same letter — including landing on **B** for a cell that displays 88.0. The grade is no longer a number out of a black box. It is the geometric mean of five named judgments, banded on the exact value, displayed rounded. The only thing left to argue about is the five judgments themselves — which is the *right* thing to argue about.
