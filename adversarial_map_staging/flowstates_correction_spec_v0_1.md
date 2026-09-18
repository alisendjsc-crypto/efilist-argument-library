# flow-states-csikszentmihalyi#note — correction spec v0.1

**STATUS: PROPOSED. NOT APPLIED. NO BYTE MOVES.** The repair is a corpus change, therefore a
PIN MOVE, therefore a declared isolated session after Josiah ratifies. This document is the
locus map and the argument, nothing else.

Authored K349a, wuld.ink Cowork, 2026-09-17. Derived from the `care-ethics`/`flow-states`
adjudication landed as `adv_map_phaseG_v0_1.json` (entry class **(b)**, severity **headline**,
axes **s/r**).

---

## 1. The defect

The node's `note` says of the node's own Dismantle response:

> *The Dismantle response presents the EFIList counter-interpretation but acknowledges this is an open question*

**It does not.** The response argues its counter-interpretation is CORRECT — *"Autotelic activity
is therefore not evidence of value generated independently of deficit; it is the most damning
confirmation of the deficit grammar"* — and then, **separately and redundantly**, grants intrinsic
value arguendo to show the answer would not matter: *"This is why the flow defense need not be
defeated as value to fail. Grant it as fully genuine intrinsic value: it still does not close the
ledger."*

Two textual markers settle it. *"need not be defeated as value to fail"* presupposes the defeat is
already accomplished — you can only say *need not* about work you take yourself to have done. And
*"it **still** does not close the ledger"* marks the grant as belt-and-braces rather than as a
revision of the verdict. What the response concedes without qualification is the **phenomenology**
and the objection's **force**; neither touches the interpretive verdict.

**Independently confirmed.** This reading was checked against a reader given the full response and
the question, with no sight of the note, the map entry or these grounds. It returned the same
verdict unprompted and supplied both markers above.

**Why it matters more than a loose sentence.** An objector can quote the corpus conceding that the
interpretation is open, when the corpus's actual position is that it is settled AND moot. The note
gives away ground the argument never surrendered.

## 2. The locus map — 4 loci, asserted not assumed

| # | Surface | Locus | Line | Kind |
|---|---|---|---|---|
| 1 | `efilist_argument_library_v4_0_0.json` | objections[flow-states].note | 2423 | corpus |
| 2 | `efilist_argument_library_v4_0_0.jsx` | objections[flow-states].note | 2411 | corpus |
| 3 | `combined.html` | objections[flow-states].note | 5262 | corpus |
| 4 | `combined.html` | RSI CALIBRATION NOTES (apparatus prose) | 1799 | flagship-only |

The corpus note is carried on all 3 surfaces and must move on all
3 together; the cross-surface gate `tools/xsurface_v4_1_0.py` is what proves it
did. **Locus 4 is FLAGSHIP-ONLY** — the string occurs once in `combined.html` and **zero
times** in the corpus JSON and the JSX, so no corpus-derived sweep will ever find it. That is the
whole reason this spec exists as a document rather than as a one-line diff.

Each span occurs **exactly once per surface**, asserted programmatically before this file was
written.

## 3. Repair A — the note (all 3 corpus surfaces)

Replace the span in §1 with:

> *The Dismantle response argues for the EFIList counter-interpretation and, independently, grants intrinsic positive value arguendo to show the asymmetry settles the question either way*

Word count 42 -> 52 (+10). Classified a **correction**, not a subtraction: it replaces a
false description with a true one, and the true one is longer because the response's architecture
has two legs and the false one named a single concession. The v4.1.0 precedent stands — the
classification describes the CLAIM, not the word count.

The note's first sentence is **kept untouched**. *"Flow research is well-established empirically but
the philosophical interpretation ... remains genuinely contested"* is a claim about the FIELD, and
it is true. Only the sentence describing the RESPONSE is false.

**This repair strengthens the node.** The corrected note advertises a two-leg architecture where
the old one advertised a concession.

## 4. Repair B — the RSI calibration note (flagship only)

The apparatus at locus 4 reads:

> *Entries that honestly acknowledge contested premises (e.g., <code>flow-states-csikszentmihalyi</code> acknowledging the open question on intrinsic positive value) may score lower on Robustness* while scoring higher on intellectual honesty ...

**The scoring claim is TRUE and the exemplar is FALSE**, and the distinction took a corpus-wide
measurement to establish. flow-states' Robustness is **0.82** against a corpus median of
**0.85** over 82 nodes: 20 nodes score strictly below it, 9 tie it, giving a
percentile rank of **29.9**. So it does sit in the lower third, exactly as the calibration note
implies. **What is false is the reason given** — the note attributes that score to an
acknowledgment the response does not make.

> **Recorded as an instance of `ccclxvi`.** This spec's author first compared flow-states against
> three neighbouring nodes, found it scored HIGHER than all three, and formed the hypothesis that
> the calibration claim failed in both directions. The full distribution falsified that. A
> four-node sample was about to become a published claim; the corpus-wide measurement is what
> stopped it.

**Recommended:** swap the exemplar rather than delete it, because the claim it illustrates is
sound and deserves an illustration that holds. Replace with:

> *Entries that honestly acknowledge contested premises (e.g., <code>indigenous-philosophy</code> conceding that against a rival axiology the argument ties rather than wins) may score lower on Robustness*

`indigenous-philosophy` satisfies **both** halves, asserted: its `#long` concedes *"it ties rather
than wins: the concern is portable across descriptions, not across every axiology"*, it is the
corpus's sole `confidence: provisional` node, and its Robustness is **0.81**, below the median.

**Alternative, if the swap is declined:** delete the parenthetical and keep the general claim. Purely
subtractive, loses the illustration, and leaves the calibration note unfalsifiable rather than
merely unillustrated — which is why it is the second choice.

## 5. What a repair session must gate

1. `tools/xsurface_v4_1_0.py` GREEN **before and after**. The corpus note moves on three surfaces;
   the gate is the only thing that proves they still agree.
2. Locus assertion **per line**, not a global regex — the v4.0.1 toolkit's discipline.
3. **Anchor destruction is the receipt.** The landed map entry `flow-states-csikszentmihalyi#note`
   anchors on the exact span Repair A removes, so after the repair that anchor MUST break, and no
   other anchor may. Sweep all entries; require exactly one break.
4. Because the map's corpus pin fails the moment the corpus moves — and a failing pin **silently
   skips seven downstream checks, `anchor-rule` among them** — the successor map is re-pinned in
   the SAME session as the cut, never the next one.
5. Repair B touches the flagship and NOT the corpus, so the cross-surface gate cannot see it. It
   needs its own before/after assertion on `combined.html` alone.
6. Locus 4 has no generator and no test. It is apparatus prose. **Whoever edits it should
   record that a corpus-derived sweep will never find it again.**

## 6. What this spec does NOT cover

`care-ethics#note`, the other headline (b) from the same phase. It is **not** a repair problem: an
independent read found the objection is that care ethics is a rival account of what GROUNDS
obligation, and that the corpus assumes consent's authority without arguing it. That is a stance
question for Josiah and the library seat, and it may be bedrock rather than a (b). It went out as
`RELAY_K349_care_ethics_to_library_seat.md` instead, and no repair should be drafted for it until
that comes back.

---

### Pins at authoring

| | |
|---|---|
| corpus | `04bf6482aa0374ee92a81c1d55ec41f8` |
| jsx | `b196548b6eb39065842d62292acca89f` |
| flagship (the pin, v4.1.0) | `72187f6cf0fccdf8e9f4ec6ca5ce009c` |

Re-derive every one of these before acting. They were measured 2026-09-17 and a spec's figures go
stale the moment a surface moves.
