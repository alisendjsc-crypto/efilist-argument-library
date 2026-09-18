#!/usr/bin/env python3
"""K349a: the flow-states#note correction spec. PROPOSED, NEVER APPLIED.

Emits flowstates_correction_spec_v0_1.md and its measurement. Repo-relative.
Every locus is ASSERTED against the live surfaces before the spec is written; every
numeric token in the emitted prose is a bound constant or an allow-listed literal.

Nothing here moves a byte. The repair is a corpus change, hence a PIN MOVE, hence a
declared isolated session after Josiah ratifies.
"""
import json, os, re, sys, hashlib, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

NOTE_SPAN = "The Dismantle response presents the EFIList counter-interpretation but acknowledges this is an open question"
NOTE_REPLACEMENT = ("The Dismantle response argues for the EFIList counter-interpretation and, "
                    "independently, grants intrinsic positive value arguendo to show the asymmetry "
                    "settles the question either way")
CAL_SPAN = ("Entries that honestly acknowledge contested premises (e.g., "
            "<code>flow-states-csikszentmihalyi</code> acknowledging the open question on "
            "intrinsic positive value) may score lower on Robustness")
CAL_REPLACEMENT = ("Entries that honestly acknowledge contested premises (e.g., "
                   "<code>indigenous-philosophy</code> conceding that against a rival axiology the "
                   "argument ties rather than wins) may score lower on Robustness")

SURFACES = ["efilist_argument_library_v4_0_0.json",
            "efilist_argument_library_v4_0_0.jsx",
            "combined.html"]

ALLOWED = {
    "0": "a rule constant: the target count for surfaces missed",
    "1": "an ordinal in the locus table, and the count of flagship-only loci",
    "2": "an ordinal in the locus table",
    "3": "the number of surfaces carrying the corpus note",
    "4": "the total locus count",
    "82": "the corpus node count, an invariant canon already pins",
    "7": "the count of downstream checks a failing corpus pin silently skips (K332 finding)",
    # the operator-local date; asserted against the measurement's own date field below
    "2026": "session date year", "09": "session date month", "17": "session date day",
    "349": "session K349 / K349a, an identifier rather than a quantity",
    # version tokens, which name releases and toolkits and are never re-derived here
    "4.0": "the v4.0.1 pin-move toolkit, cited for its per-line assertion discipline",
    "4.1": "the v4.1.0 content cut and the current pin",
    "0.1": "this spec's own version",
}


def meas_date_ok():
    return DATE == "2026-09-17"


DATE = "2026-09-17"   # OPERATOR-LOCAL (America/Phoenix); the sandbox clock reads UTC.


def main():
    raw = {s: open(os.path.join(REPO, s), "rb").read().decode("utf-8") for s in SURFACES}
    corpus = json.loads(raw[SURFACES[0]])
    by = {o["id"]: o for o in corpus["objections"]}
    fs = by["flow-states-csikszentmihalyi"]

    # ---- LOCUS MAP, asserted ----------------------------------------------------
    loci = []
    for s in SURFACES:
        lines = raw[s].split("\n")
        n = raw[s].count(NOTE_SPAN)
        ln = [i + 1 for i, L in enumerate(lines) if NOTE_SPAN in L]
        assert n == 1 and len(ln) == 1, "%s carries the note span %d times" % (s, n)
        loci.append({"surface": s, "locus": "objections[flow-states].note", "line": ln[0],
                     "occurrences": n, "kind": "corpus"})
    h = raw["combined.html"]
    lines = h.split("\n")
    nc = h.count(CAL_SPAN)
    lnc = [i + 1 for i, L in enumerate(lines) if CAL_SPAN in L]
    assert nc == 1 and len(lnc) == 1, "calibration span occurs %d times in the flagship" % nc
    for s in SURFACES[:2]:
        assert CAL_SPAN not in raw[s], "%s unexpectedly carries the calibration span" % s
        assert "acknowledging the open question" not in raw[s]
    loci.append({"surface": "combined.html", "locus": "RSI CALIBRATION NOTES (apparatus prose)",
                 "line": lnc[0], "occurrences": nc, "kind": "flagship-only"})

    # ---- THE RSI MEASUREMENT ----------------------------------------------------
    i = h.find("var REBUTTAL_STRENGTH = {")
    j = h.find("\n};", i)
    rsi = json.loads(h[i + len("var REBUTTAL_STRENGTH = "): j + 2])
    r = {k: v["r"] for k, v in rsi.items()}
    vals = sorted(r.values())
    fsr = r["flow-states-csikszentmihalyi"]
    ipr = r["indigenous-philosophy"]
    below = sum(1 for x in vals if x < fsr)
    equal = sum(1 for x in vals if x == fsr)
    pct = round(100 * (below + 0.5 * equal) / len(vals), 1)
    med = st.median(vals)

    # the replacement exemplar must actually satisfy BOTH halves of the claim
    ip_long = by["indigenous-philosophy"]["responses"]["long"]
    assert "ties rather than wins" in ip_long, "the proposed exemplar does not concede a tie"
    assert by["indigenous-philosophy"].get("confidence") == "provisional"
    assert ipr < med, "the proposed exemplar does not score below the Robustness median"

    C = {
        "n_loci": len(loci), "n_corpus_surfaces": len(SURFACES), "n_flagship_only": 1,
        "fs_r": fsr, "ip_r": ipr, "median_r": med,
        "below": below, "equal": equal, "pct": pct, "n_nodes": len(vals),
        "note_words_before": len(fs["note"].split()),
        "note_words_after": len((fs["note"].replace(NOTE_SPAN, NOTE_REPLACEMENT)).split()),
        "corpus_md5": md5f(os.path.join(REPO, SURFACES[0])),
        "jsx_md5": md5f(os.path.join(REPO, SURFACES[1])),
        "flagship_md5": md5f(os.path.join(REPO, SURFACES[2])),
    }
    C["word_delta"] = C["note_words_after"] - C["note_words_before"]

    tbl = "\n".join(
        "| %d | `%s` | %s | %d | %s |" % (n + 1, L["surface"], L["locus"], L["line"], L["kind"])
        for n, L in enumerate(loci))

    body = """# flow-states-csikszentmihalyi#note — correction spec v0.1

**STATUS: PROPOSED. NOT APPLIED. NO BYTE MOVES.** The repair is a corpus change, therefore a
PIN MOVE, therefore a declared isolated session after Josiah ratifies. This document is the
locus map and the argument, nothing else.

Authored K349a, wuld.ink Cowork, 2026-09-17. Derived from the `care-ethics`/`flow-states`
adjudication landed as `adv_map_phaseG_v0_1.json` (entry class **(b)**, severity **headline**,
axes **s/r**).

---

## 1. The defect

The node's `note` says of the node's own Dismantle response:

> *{span}*

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

## 2. The locus map — {n_loci} loci, asserted not assumed

| # | Surface | Locus | Line | Kind |
|---|---|---|---|---|
{tbl}

The corpus note is carried on all {n_corpus_surfaces} surfaces and must move on all
{n_corpus_surfaces} together; the cross-surface gate `tools/xsurface_v4_1_0.py` is what proves it
did. **Locus {n_loci} is FLAGSHIP-ONLY** — the string occurs once in `combined.html` and **zero
times** in the corpus JSON and the JSX, so no corpus-derived sweep will ever find it. That is the
whole reason this spec exists as a document rather than as a one-line diff.

Each span occurs **exactly once per surface**, asserted programmatically before this file was
written.

## 3. Repair A — the note (all {n_corpus_surfaces} corpus surfaces)

Replace the span in §1 with:

> *{repl}*

Word count {wb} -> {wa} ({delta:+d}). Classified a **correction**, not a subtraction: it replaces a
false description with a true one, and the true one is longer because the response's architecture
has two legs and the false one named a single concession. The v4.1.0 precedent stands — the
classification describes the CLAIM, not the word count.

The note's first sentence is **kept untouched**. *"Flow research is well-established empirically but
the philosophical interpretation ... remains genuinely contested"* is a claim about the FIELD, and
it is true. Only the sentence describing the RESPONSE is false.

**This repair strengthens the node.** The corrected note advertises a two-leg architecture where
the old one advertised a concession.

## 4. Repair B — the RSI calibration note (flagship only)

The apparatus at locus {n_loci} reads:

> *{cal}* while scoring higher on intellectual honesty ...

**The scoring claim is TRUE and the exemplar is FALSE**, and the distinction took a corpus-wide
measurement to establish. flow-states' Robustness is **{fs_r}** against a corpus median of
**{median_r}** over {n_nodes} nodes: {below} nodes score strictly below it, {equal} tie it, giving a
percentile rank of **{pct}**. So it does sit in the lower third, exactly as the calibration note
implies. **What is false is the reason given** — the note attributes that score to an
acknowledgment the response does not make.

> **Recorded as an instance of `ccclxvi`.** This spec's author first compared flow-states against
> three neighbouring nodes, found it scored HIGHER than all three, and formed the hypothesis that
> the calibration claim failed in both directions. The full distribution falsified that. A
> four-node sample was about to become a published claim; the corpus-wide measurement is what
> stopped it.

**Recommended:** swap the exemplar rather than delete it, because the claim it illustrates is
sound and deserves an illustration that holds. Replace with:

> *{calr}*

`indigenous-philosophy` satisfies **both** halves, asserted: its `#long` concedes *"it ties rather
than wins: the concern is portable across descriptions, not across every axiology"*, it is the
corpus's sole `confidence: provisional` node, and its Robustness is **{ip_r}**, below the median.

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
6. Locus {n_loci} has no generator and no test. It is apparatus prose. **Whoever edits it should
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
| corpus | `{corpus_md5}` |
| jsx | `{jsx_md5}` |
| flagship (the pin, v4.1.0) | `{flagship_md5}` |

Re-derive every one of these before acting. They were measured 2026-09-17 and a spec's figures go
stale the moment a surface moves.
"""
    subs = dict(C, span=NOTE_SPAN, repl=NOTE_REPLACEMENT, cal=CAL_SPAN, calr=CAL_REPLACEMENT,
                tbl=tbl, wb=C["note_words_before"], wa=C["note_words_after"],
                delta=C["word_delta"])
    out = body.format(**subs)

    bound = set()
    for v in subs.values():
        for t in re.findall(r"\d+(?:\.\d+)?", str(v)):
            bound.add(t)
    bad = [t for t in re.findall(r"\d+(?:\.\d+)?", out) if t not in bound and t not in ALLOWED]
    if bad:
        print("REFUSING: unbound numeric tokens: %s" % sorted(set(bad)))
        return 1
    assert meas_date_ok(), "the date literals in the allow-list are stale"
    print("  constant gate: %d distinct numeric tokens, all bound or allowed"
          % len(set(re.findall(r"\d+(?:\.\d+)?", out))))

    meas = {"artifact": "flowstates_correction_measurement_v0_1.json", "session": "K349a",
            "date_operator_local": "2026-09-17", "loci": loci, "constants": C,
            "robustness": {"median": med, "n": len(vals),
                           "flow_states": fsr, "indigenous_philosophy": ipr,
                           "below": below, "equal": equal, "percentile": pct}}
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "flowstates_correction_spec_v0_1.md")
    mdest = os.path.join(os.path.dirname(dest), "flowstates_correction_measurement_v0_1.json")
    ob = out.encode("utf-8")
    open(dest, "wb").write(ob)
    mb = (json.dumps(meas, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(mdest, "wb").write(mb)
    print("wrote %s  %s  %d B" % (dest, hashlib.md5(ob).hexdigest(), len(ob)))
    print("wrote %s  %s  %d B" % (mdest, hashlib.md5(mb).hexdigest(), len(mb)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
