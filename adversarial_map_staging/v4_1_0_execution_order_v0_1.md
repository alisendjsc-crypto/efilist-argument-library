# COWORK EXECUTION ORDER v4.1.0 — the three subtractive repairs

**Status: RATIFIED IN CONTENT, BLOCKED ON MACHINERY.** This order is the handoff for the
deliberate isolated pin-move session the shipping-fork disposition requires. It is written by
the library seat after auditing the map seat's `v4_1_0_regen_spec_v0_1.md`, and it exists
because that spec is correct about the repairs and silent about two things that will stop the
cut dead.

Read this before `v4_1_0_regen_spec_v0_1.md`, not after. The spec says *what* to change. This
says what changing it costs.

---

## 0. The ratification

The library seat ratifies **the content of all three repairs**, and prefers the interpreted
form of `R1` over `R1-alt`: the paragraph's job in that node is to say why an empirical finding
bears on a claim about choice, and a bare corrected number does not do that job. `R1-alt` stays
on the record as the literal reading of `repair_shape: subtractive`, for Josiah to take instead
if he wants the smaller edit.

**A second signature from the same author is not a second signature.** The map seat authored
these repairs; the library seat re-reading its own prose adds nothing (`C1`). What follows is
the part a second seat can actually contribute: what the repairs do to everything downstream of
the sentences.

---

## 1. BLOCKER — the terminal artifact becomes unvalidatable

`adv_map_validator_v0_2.py` holds two checks that cannot both survive a landed regen:

- `anchor-rule` — `target_anchor` must be a verbatim substring at `target_locus`.
- `status-enum` — `status == "mapped"`, hard, with a self-test case (`bad-status`) proving
  that `queued` is a violation. Downstream lifecycle states live in canon, never the artifact.

Each of the three nodes carries a Phase E entry classed `(b)` whose anchor is cut from the
exact sentence being repaired. So after the cut, three entries hold anchors that no longer
match, and **no status value exists that says so**. `adversarial_map_v1_0.json` fails
`anchor-rule` permanently, `--assembly` never passes again, and the terminal gate the program
spent from K220 to K338 reaching is gone on the first regen.

The spec framed anchor destruction as the *receipt* for a successful repair. That is right, and
it is not enough: the machinery has no way to express a receipt.

**Three options, with a recommendation.**

| | option | cost |
|---|---|---|
| A | Add a `landed` status; `anchor-rule` skips landed entries | validator v0_3 + schema change = MAJOR canon bump; a new code path with no landed data to test against |
| B | Re-anchor the three entries to the repaired text | incoherent — the entry asserts a defect while quoting text that no longer has it |
| **C** | **Remove landed entries from the artifact; canon records them as landed** | **no validator change, no schema change; follows the rule already written** |

**Take C.** Canon already says the lifecycle `mapped → queued → ratified → landed | rejected`
lives in canon and *never in the artifact*, and that the artifact is the MAPPED-COMPLETE,
PRE-TRIAGE state. An entry that has landed is no longer mapped-pending; it has left the map.
The artifact goes 93 → 90 entries over 82 → 82 nodes, `class_counts` drops 3 from (b), and
canon's `terminal_artifact_pin` gains a `landed` list naming the three with their pre-cut
anchors — which is where the receipt belongs, dated, beside the commit that landed it.

**Option C does not work as written, and here is the exact reason.** The validator carries
`coverage`, which under `--terminal` requires *every corpus id to hold at least one entry*
(82/82) — and `--assembly` **implies** `--terminal`. All three nodes carry exactly one entry
each, so removing them drops three ids to zero and `coverage` hard-fails. Not "may fire":
will. `meta-summaries` also binds, so `class_counts` and `coverage_distinct_ids` must be
recomputed to match, which `build_assembly.py` already does.

So C requires one further decision, and it is the cut's first: **does `coverage` mean every
node was adjudicated, or every node is currently pending?** If the former, the check must
read canon's landed list as well as the artifact, and that is a validator change after all —
smaller than A's new status vocabulary, but not free. If the latter, the three entries stay
in the artifact and A is the only path.

*That decision is deliberately not made here.* It is a question about what the map is FOR,
and the seat that authored the entries should not also decide what their removal means.

---

## 2. BLOCKER — the cut is a three-surface synchronized edit

`README.md` says it twice: **no build step.** `combined.html` is not generated from the corpus;
it is a hand-assembled superset that carries `REBUTTAL_STRENGTH`, which the JSX does not. So
the same five sentences live in three shipped files, and nothing regenerates any of them from
any other.

| span | `..._v4_0_0.json` | `..._v4_0_0.jsx` | `combined.html` |
|---|---|---|---|
| R1 `happiness-is-choice` | line 1756 | line 1744 | line 4595 |
| R2 `just-edgy` | line 581 | line 569 | line 3420 |
| R3a/b/c `just-depressed` | line 91 | line 79 | line 2930 |

Every span occurs **exactly once** in each file, and R3's three spans share one line per file
(the long response is a single JSON string). That is 9 line-loci and 15 span-replacements.

Base pins at the time of writing:

- `efilist_argument_library_v4_0_0.json` — `6ee1f6f31e0f012db0d58cae4f912fcb` / 1,333,912 B / 12,342 lines
- `efilist_argument_library_v4_0_0.jsx` — `b7dadfc39d988d643c408b3329ffcb54` / 1,273,371 B / 8,584 lines
- `combined.html` — `cee25a00b68ba036138d064c383d9a8b` / 2,982,658 B / 12,447 lines (**the pin**)

**No gate anywhere cross-checks corpus text against the flagship.** A missed surface ships a
corpus and a served page that disagree, and nothing says so. Build that gate as part of this
cut, not after it: for each of the five spans, assert the new text present and the old text
absent in all three files, and assert the three files agree on the repaired passage.

---

## 3. The method is already in the repo

`tools/sweep_v4_0_1.py`, `tools/restamp_v4_0_1.py` and `tools/verify_v4_0_1.py` are the v4.0.1
pin-move session's toolkit and they are the template. Reuse the shape, not the content:

- **Line-indexed, per-line anchor assertion, abort before any write.** `sweep_v4_0_1.py` says
  it outright: *"not sed -i, not a global regex."* Each edit names its line and the anchor that
  must be on it.
- **Frozen lines.** That sweep carried a `FROZEN` map of line → byte-length for lines that must
  not change. Do the same for the three long responses' neighbours.
- **Verify by diff against HEAD, not by grep.** `verify_v4_0_1.py` exists, in its author's own
  words, *"because the video seat ran the check I had not: the greps prove the named strings
  moved, they do NOT prove that nothing ELSE moved."* It diffs the working file against
  `git show HEAD:combined.html` line by line and asserts the changed set is **exactly** the
  named loci. Do this for all three files. It is the same lesson as `C6` and `C9` and the repo
  learned it here first.
- **`GONE` and `HELD` lists.** That verify carried strings that must have disappeared and
  strings that must have survived. For a subtractive regen this is the natural shape: the false
  claim GONE from all three surfaces, the surrounding argument HELD.
- **Re-stamp is phase 2.** Every surface carrying the pin md5 needs the NEW md5, which does not
  exist until the flagship is written. Do not try to do it in one pass.

---

## 4. Phase order

1. **Decide §1.** The landed-entry question. Nothing else can be sequenced until it is answered.
2. **Corpus, JSX, flagship** — one line-indexed sweep per file, each with its own anchor
   assertions and its own verify-against-HEAD. Three commits or one, but three verifies.
3. **Cross-surface gate** — the check that does not exist yet: five spans × three files, new
   present, old absent, passages agree.
4. **Re-pin the map in the SAME session.** K332's finding is decisive here: a failing
   `meta-corpus-pin` **silently skips seven downstream checks**, `anchor-rule` among them. A
   map left stale across sessions is not a stale artifact, it is a disabled instrument, and
   that is precisely how a month of unvalidated fragments happened once already.
5. **Canon** — MINOR for the corpus content change (v3.9 opened the enrichment line; enrichment
   of existing nodes is MINOR), plus the landed list from §1. MAJOR only if §1 lands option A.
6. **Re-stamp**, then **wuld search-index regen and objection re-vendor**, same session, per
   the disposition.
7. **The pin moves.** Read it before and after and print both.

---

## 5. Abort conditions

- Any line-anchor assertion fails → abort before writing, no partial file.
- The verify-against-HEAD changed set is not exactly the named loci → abort, even if every
  named string moved correctly.
- The three surfaces disagree on any repaired passage → abort.
- `--assembly` cannot be made to pass after §4 → **stop and do not push.** The terminal gate is
  the program's only proof that the map means anything; shipping a corpus change that
  permanently breaks it trades the whole instrument for three sentences.

---

## 6. What this order does not decide

The other sixteen v4.1.0 items — five structural, ten additive, with `selfish-lazy#long`
travelling with the v5.0.0 intake cut instead. Whether the three repairs ship as one commit or
three. The `R1` / `R1-alt` choice, which is Josiah's. And §1, which is the cut's first real
decision and is deliberately left open, because a handoff that pre-decides the hard question is
a handoff that has not identified it.
