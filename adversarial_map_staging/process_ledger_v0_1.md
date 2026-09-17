# Process Ledger v0.1

**The second layer of the library's honesty apparatus.** The honest-residuals register
records where the *arguments* bottom out. This records where the *process* failed, what
caught it, and what changed as a result.

**Library-internal for now.** The recommendation is that it ship: a corpus whose whole claim
is that it earns trust by robustness cannot document where its arguments end while hiding
where its method went wrong. Every failure below is a *caught* failure with a correction
attached, which reads as a working process rather than an unreliable one. But it inherits the
K56 discipline: **no chrome placement**. A failure log belongs behind the door, not on it.

Grounded in the hazard registry in `CLAUDE.md`, not in recollection. The builder verifies
every cited numeral is present there before writing.

---

## Why a taxonomy and not a list

The hazard registry is a log: `cccli`, `ccclv`, `ccclvi`, numbered in the order things went
wrong. A log is the right *record* and the wrong *teacher*, because the next failure never
arrives wearing the last one's costume. What repeats is the **shape**. Seven shapes account
for every process failure this arc, and four of them recur across unrelated surfaces — git,
PowerShell, JSON fragments, prose.

| | class | recurs |
|---|---|---|
| `C1` | The instrument reports on itself | 3 |
| `C2` | The pin measures the envelope, not the text | 1 |
| `C3` | A negative asserted without looking | 2 |
| `C4` | Recall substituted for lookup | 1 |
| `C5` | A rule stated once and breached elsewhere | 2 |
| `C6` | A check that only fails in one direction | 2 |
| `C7` | A fence is a promise | 1 |
| `C8` | The norm that was never written down | 1 |

## `C1` — The instrument reports on itself

*A measurement describes the apparatus rather than the artifact. The reading is real; it is just a reading of the wrong thing.*

- **`ccclvii`** — Under `*.html text eol=lf`, `git status --porcelain` reports ` M combined.html` persistently while the content is byte-identical to HEAD. A gate built on it aborts a correct repo. `git diff --name-only HEAD` returns empty and is the honest instrument.
- **`ccclviii`** — Five readings described the harness: a `--depth 1` clone made the sitemap generator falsify all 55 lastmod dates; `| head -12` turned a BrokenPipeError into a fake exit 1; `open(p,'wb')` truncated a file before its own read; a grep ran against a tree that had already been reset.
- **`ccclix` · THIS SESSION, unrecorded** — `git cat-file blob X > tmp` then md5 the tmp. PowerShell's `>` re-encodes (UTF-16LE under 5.1) and appends a newline, so that md5 describes the redirect. Caught in rehearsal-prep, before shipping. The fix is to never move blob bytes through the shell: a blob SHA *is* the content identity, so compare `git rev-parse HEAD:<path>` git-to-git.

**Counter-discipline.** Before trusting a gate, ask what it would report if the artifact were correct. If the answer is 'the same thing', the gate measures the harness.

## `C2` — The pin measures the envelope, not the text

*A content hash taken over a whole file moves when anything in the file moves, including fields that carry no content.*

- **`K332` · discharged** — Four release relabels walked the corpus `version` field 4.0.0 -> 4.0.4 while every objection stayed byte-identical. One content cut wore five whole-file md5s, and every Adversarial Map fragment pinning `6ee1f6f3` failed `meta-corpus-pin` -- which silently disabled SEVEN downstream checks including `anchor-rule`, the program's core verbatim discipline. The program's central gate had not run for roughly a month and nothing said so.

**Counter-discipline.** Pin the thing the downstream checks actually read. v0_2 adds `source_corpus_objections_md5`, a digest over the objections array alone with `sort_keys=True`, so neither a label nor a key reordering can move it. The K332 failure is now a self-test case: relabel the envelope, and the whole-file pin breaks while the digest holds.

## `C3` — A negative asserted without looking

*Claiming the corpus does not already answer something, without opening the node whose entire subject it is.*

- **`K232-class`** — `suffering-makes-human` was filed as (b) on the claim that the constitutive-goods argument went unengaged. False: `suffering-as-meaning` states and refutes it across four arms.
- **`Phase E` · THIS SESSION, avoided** — Before ruling the first (c) in the program, the absence was measured rather than asserted: 26 of 82 nodes deploy diagnostic vocabulary inside their responses, the licensing rule appears in exactly 2, and T5 holds nothing method-level. The (c) survived the check.

**Counter-discipline.** An absence claim is a measurement. Run it against the corpus, print the count, and put the count in the grounds.

## `C4` — Recall substituted for lookup

*A field whose correct value lives in an earlier artifact gets filled from memory of that artifact instead of from the artifact.*

- **`N1` · THIS SESSION, found** — Every (d) entry carries a `novel` boolean. With no register, a phase author decides it from memory of preceding phases -- Phase D recalling what B2 did three phases back. The succession brief records N1 (moral realism / is-ought) as first registered in Phase D. The shipped B2 fragment carries its birth certificate at `phenomenological-existentialism` with `novel: true`, and B2's own `eliminativism` entry already routes to it as already-surfaced. B2 precedes D.

**Counter-discipline.** Build the lookup table before the phase that needs it, not after. The honest-residuals register was scheduled for terminal assembly; it is an INPUT to Phase E. Phase E was authored against it and both its (d) entries were decided by lookup, introducing no new birth certificate.

## `C5` — A rule stated once and breached elsewhere

*The discipline exists, in writing, in one place -- and the places that breach it never learn of it, because nothing cross-checks a stated rule against its own corpus.*

- **`diagnostic register` · THIS SESSION, found** — The rule forbidding diagnosis-as-refutation is stated in `just-depressed#long` and `life-gift#long`. Diagnostic vocabulary appears inside responses at 26 nodes. The corpus wrote the rule and breaches it in 24 of the places it applies. This became the program's first (c), `diagnosis-not-refutation`.
- **`B1 vs bradley` · THIS SESSION, found** — Phase B1 carries a (b) at `bradley-no-subject#long` whose grounds read: *presupposes non-comparative harm, which the node asserts via analogy rather than argues*. The same fragment then used that node as an (a) destination four times. Registering a node's defect and spending the node as an answer are different entries, and nothing compared them.

**Counter-discipline.** When a rule is stated, sweep for its own breaches in the same pass. A rule with one instance is a note; a rule with a sweep is a discipline.

## `C6` — A check that only fails in one direction

*A detector built for one shape of error is silently blind to its mirror image.*

- **`F1` · THIS SESSION, found and remedied** — The register's collision detector verifies each bedrock has exactly one birth certificate, catching one bedrock wearing two novel flags. It cannot catch one bedrock wearing two ids -- which is precisely what produced 22 free-text strings for 12 bedrocks. The HR-04 / HR-07 dependency surfaced by hand, not by the instrument.
- **`F3` · THIS SESSION, found and remedied** — The v0_2 attestation tokens were exact-match, so the only clearing token for the transhumanist route asserted a repair. The ruling on that entry was *not load-bearing*, not *repaired*. Attesting it would have been false. Tokens now match as a prefix so the suffix names the disposition the ruling reached.

**Counter-discipline.** For every detector, write down the error it cannot see, and say so in the artifact. The register now declares that its adjacency signals are a floor on what must be adjudicated, never a ceiling, and names the pair they miss.

## `C7` — A fence is a promise

*Formatting carries an instruction whether or not one was intended.*

- **`ccclvi`** — Evidence was presented inside triple backticks. It was pasted into PowerShell and produced four CommandNotFoundExceptions. Nothing executed -- that exception means nothing reached execution -- but the report had promised runnability.

**Counter-discipline.** Fences are reserved for the one thing meant to be pasted. Evidence goes in prose, tables or blockquotes.

## `C8` — The norm that was never written down

*Practice converges on something the written gate never required. The gate stays permissive, so a later author can diverge from five phases of custom without failing a single check, and no artifact-level review can see it.*

- **`ccclxi` · THIS SESSION, found** — The Adversarial Map's anchor rule requires a verbatim anchor of 15 words or fewer at a named locus. It says NOTHING about which locus. Practice settled hard on `long`: 77 of the map's 93 entries, B1 16/16, B2 15/16, K231's D 15/17, Phase E 12/13. A wuld-ink re-derivation of Phase D targeted `medium` 11 times out of 17. `long` is the corpus's most defended prose and `medium` is a condensation, so attacking `medium` finds gaps far more easily: the re-derivation returned 12 (b) where K231 returned 3, and eight of those twelve never consider the long form at all. It passed every gate, validated clean, and was an hour from being folded. Cost had it landed: nine fabricated regen candidates, taking the v4.1.0 cut from 21 (b) to 30 and its corpus footprint from 26% to 37%, each phantom entry consuming a cold-grade cycle.

**Counter-discipline.** Detection required comparing two AUTHORS, not checking either artifact. Where practice is uniform and the rule is silent, write the rule down and gate it. The map's is now: author against the deepest locus that addresses the objection, or state in the grounds why a shallower one was chosen.

## What the discipline caught

A failure log that records only failures is a confession, not a ledger. These are cases where
a gate stopped something before it shipped — several of them stopping its own author.

**The block refused its own stale claim.** K333's self-test gate aborted with `case count is not 35` because an amendment made mid-session added a test case. The block declined to commit an artifact whose behaviour did not match the block's own description of it. That is the gate doing exactly the job it exists for, against its own author.

**The adjacency audit caught a silent assumption.** After the F1 remedy made an empty relations list an assertion rather than a default, the very first rebuild refused to write: HR-07 and HR-09 share a tributary node and neither declared a relation. The unstated 'co-located but unrelated' had to become a stated ruling.

**The path was wrong and the machine said so.** The operator block hardcoded a repo path inferred from an email address. The connected device reported the real one. An inference presented as a fact, caught by asking the system that knows.

**Rehearsal, seven paths.** Every operator block this session was rehearsed against a bare origin with `core.autocrlf true` and a faked `curl.exe`, including a negative control that writes a CRLF working copy and confirms the block does NOT abort -- the ccclvii failure, reproduced on purpose to prove the fix holds.

**The calibration control paid for itself with an hour to spare.** Two independent Phase D derivations of the same 17 nodes existed, and the brief had asked since 2.5 that they be diffed before either was folded. Treated as a nicety, it would have been skipped: the re-derivation validated clean and was built into a rehearsed block. Diffing the pair against EACH OTHER rather than either against the corpus returned class agreement 5/17 and ANCHOR agreement 0/17 -- and the second number, not the first, is the finding. A shared-zero anchor count means the two never engaged the same text, which no per-artifact check can report.

**The register's audit fired on an artifact it did not author.** Loading K231's fragment, the birth-certificate check aborted the build: nihilism-label(d, novel=true) collided with B2's phenomenological-existentialism. Working it through, the fault was the register's own BEDROCK_MAP: HR-04 asks whether suffering's disvalue is stance-independent and HR-13 asks whether that disvalue gives a reason binding an INDIFFERENT agent, which a Humean denies while granting HR-04. Foreign data is the only real test of an instrument, and it found under-individuation the author had missed.

**Two independent derivations agreed on coverage and disagreed on everything else.** Both Phase D fragments cover the same 17 T2 node ids, reaching the 82/82 the brief projected. That agreement is what made the disagreement legible: identical scope, disjoint anchors, 5/17 class agreement. Coverage agreement with anchor disjointness is a sharper signal than either fragment alone could give, and it is only available while both exist separately -- which is the argument for retaining the superseded one as evidence rather than deleting it.

## Registry pointer

The numerals themselves stay in `CLAUDE.md`, which is the record of authority. This ledger
cites them and never restates them. Verified present at build time:

- `cccli` — cccli IS ONE CLASS TOO WEAK AS LANDED, and the library seat named why.
- `ccclv` — A SWEEP FOR A SUPERSEDED FIGURE, IN A DOCUMENT THAT KEEPS DATED RECORDS, RETURNS MOSTLY CORRECT SENTENCES; AND THE FIGURE IT IS LOOKING FOR MAY NOT BE A STRING AT ALL.
- `ccclvi` — A FENCE IN A REPORT IS A PROMISE THAT THE CONTENTS ARE RUNNABLE.
- `ccclvii` — UNDER AN EOL POLICY IT IS NOT ONLY THE WORKING-COPY md5 THAT LIES; `git status` LIES TOO.
- `ccclviii` — MEASURE THE STATE YOU THINK YOU MEASURED.

`ccclix`, `ccclx` and `ccclxi` are this session's additions and are **not yet folded** into
the registry: the C1 redirect instance, the C6 mutate-what-you-verify instance, and the C8 locus
finding. The registry lives in wuld-ink's `CLAUDE.md`, a different repo from efilist canon, so
the efilist canon bump could not carry them. They fold in a wuld-ink block.

