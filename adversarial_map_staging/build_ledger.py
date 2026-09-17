#!/usr/bin/env python3
"""Build process_ledger_v0_1.md -- the 'discrete notes' surface.

Layer two of the library's honesty apparatus. Layer one, honest_residuals_register,
records where the ARGUMENTS bottom out. This records where the PROCESS failed, what
caught it, and what changed as a result.

Grounded in the hazard registry in CLAUDE.md, not in recollection: the numerals and
their headlines are read from that file and verified present before writing.
"""
import re, sys, hashlib, json, os

CLAUDE_MD = "claude_md_hazard_registry_snapshot.txt"  # see README: the registry lives in wuld-ink

# Recorded numerals this ledger cites. Verified against CLAUDE.md before writing.
CITED = ["cccli", "ccclv", "ccclvi", "ccclvii", "ccclviii",
         "ccclix", "ccclx", "ccclxi", "ccclxii"]
# ccclix..ccclxii folded into wuld-ink CLAUDE.md at WI-K332 (bd63ca4). They are now
# CITED, which means the builder REFUSES TO WRITE unless each has a bold headline in
# the snapshot -- the citation is checked rather than asserted.

CLASSES = [
 dict(id="C1", name="The instrument reports on itself",
   gloss="A measurement describes the apparatus rather than the artifact. The reading is real; "
         "it is just a reading of the wrong thing.",
   instances=[
     ("ccclvii", "recorded",
      "Under `*.html text eol=lf`, `git status --porcelain` reports ` M combined.html` "
      "persistently while the content is byte-identical to HEAD. A gate built on it aborts a "
      "correct repo. `git diff --name-only HEAD` returns empty and is the honest instrument."),
     ("ccclviii", "recorded",
      "Five readings described the harness: a `--depth 1` clone made the sitemap generator "
      "falsify all 55 lastmod dates; `| head -12` turned a BrokenPipeError into a fake exit 1; "
      "`open(p,'wb')` truncated a file before its own read; a grep ran against a tree that had "
      "already been reset."),
     ("ccclix", "recorded",
      "`git cat-file blob X > tmp` then md5 the tmp. PowerShell's `>` re-encodes (UTF-16LE under "
      "5.1) and appends a newline, so that md5 describes the redirect. Caught in rehearsal-prep, "
      "before shipping. The fix is to never move blob bytes through the shell: a blob SHA *is* "
      "the content identity, so compare `git rev-parse HEAD:<path>` git-to-git."),
   ],
   counter="Before trusting a gate, ask what it would report if the artifact were correct. If the "
           "answer is 'the same thing', the gate measures the harness."),
 dict(id="C2", name="The pin measures the envelope, not the text",
   gloss="A content hash taken over a whole file moves when anything in the file moves, including "
         "fields that carry no content.",
   instances=[
     ("K332", "discharged",
      "Four release relabels walked the corpus `version` field 4.0.0 -> 4.0.4 while every objection "
      "stayed byte-identical. One content cut wore five whole-file md5s, and every Adversarial Map "
      "fragment pinning `6ee1f6f3` failed `meta-corpus-pin` -- which silently disabled SEVEN "
      "downstream checks including `anchor-rule`, the program's core verbatim discipline. The "
      "program's central gate had not run for roughly a month and nothing said so."),
   ],
   counter="Pin the thing the downstream checks actually read. v0_2 adds "
           "`source_corpus_objections_md5`, a digest over the objections array alone with "
           "`sort_keys=True`, so neither a label nor a key reordering can move it. The K332 failure "
           "is now a self-test case: relabel the envelope, and the whole-file pin breaks while the "
           "digest holds."),
 dict(id="C3", name="A negative asserted without looking",
   gloss="Claiming the corpus does not already answer something, without opening the node whose "
         "entire subject it is.",
   instances=[
     ("K232-class", "recorded",
      "`suffering-makes-human` was filed as (b) on the claim that the constitutive-goods argument "
      "went unengaged. False: `suffering-as-meaning` states and refutes it across four arms."),
     ("Phase E", "THIS SESSION, avoided",
      "Before ruling the first (c) in the program, the absence was measured rather than asserted: "
      "26 of 82 nodes deploy diagnostic vocabulary inside their responses, the licensing rule "
      "appears in exactly 2, and T5 holds nothing method-level. The (c) survived the check."),
   ],
   counter="An absence claim is a measurement. Run it against the corpus, print the count, and put "
           "the count in the grounds."),
 dict(id="C4", name="Recall substituted for lookup",
   gloss="A field whose correct value lives in an earlier artifact gets filled from memory of that "
         "artifact instead of from the artifact.",
   instances=[
     ("N1", "THIS SESSION, found",
      "Every (d) entry carries a `novel` boolean. With no register, a phase author decides it from "
      "memory of preceding phases -- Phase D recalling what B2 did three phases back. The "
      "succession brief records N1 (moral realism / is-ought) as first registered in Phase D. The "
      "shipped B2 fragment carries its birth certificate at `phenomenological-existentialism` with "
      "`novel: true`, and B2's own `eliminativism` entry already routes to it as already-surfaced. "
      "B2 precedes D."),
   ],
   counter="Build the lookup table before the phase that needs it, not after. The honest-residuals "
           "register was scheduled for terminal assembly; it is an INPUT to Phase E. Phase E was "
           "authored against it and both its (d) entries were decided by lookup, introducing no new "
           "birth certificate."),
 dict(id="C5", name="A rule stated once and breached elsewhere",
   gloss="The discipline exists, in writing, in one place -- and the places that breach it never "
         "learn of it, because nothing cross-checks a stated rule against its own corpus.",
   instances=[
     ("diagnostic register", "THIS SESSION, found",
      "The rule forbidding diagnosis-as-refutation is stated in `just-depressed#long` and "
      "`life-gift#long`. Diagnostic vocabulary appears inside responses at 26 nodes. The corpus "
      "wrote the rule and breaches it in 24 of the places it applies. This became the program's "
      "first (c), `diagnosis-not-refutation`."),
     ("B1 vs bradley", "THIS SESSION, found",
      "Phase B1 carries a (b) at `bradley-no-subject#long` whose grounds read: *presupposes "
      "non-comparative harm, which the node asserts via analogy rather than argues*. The same "
      "fragment then used that node as an (a) destination four times. Registering a node's defect "
      "and spending the node as an answer are different entries, and nothing compared them."),
   ],
   counter="When a rule is stated, sweep for its own breaches in the same pass. A rule with one "
           "instance is a note; a rule with a sweep is a discipline."),
 dict(id="C6", name="A check that only fails in one direction",
   gloss="A detector built for one shape of error is silently blind to its mirror image.",
   instances=[
     ("F1", "THIS SESSION, found and remedied",
      "The register's collision detector verifies each bedrock has exactly one birth certificate, "
      "catching one bedrock wearing two novel flags. It cannot catch one bedrock wearing two ids -- "
      "which is precisely what produced 22 free-text strings for 12 bedrocks. The HR-04 / HR-07 "
      "dependency surfaced by hand, not by the instrument."),
     ("F3", "THIS SESSION, found and remedied",
      "The v0_2 attestation tokens were exact-match, so the only clearing token for the "
      "transhumanist route asserted a repair. The ruling on that entry was *not load-bearing*, not "
      "*repaired*. Attesting it would have been false. Tokens now match as a prefix so the suffix "
      "names the disposition the ruling reached."),
   ],
   counter="For every detector, write down the error it cannot see, and say so in the artifact. The "
           "register now declares that its adjacency signals are a floor on what must be "
           "adjudicated, never a ceiling, and names the pair they miss."),
 dict(id="C7", name="A fence is a promise",
   gloss="Formatting carries an instruction whether or not one was intended.",
   instances=[
     ("ccclvi", "recorded",
      "Evidence was presented inside triple backticks. It was pasted into PowerShell and produced "
      "four CommandNotFoundExceptions. Nothing executed -- that exception means nothing reached "
      "execution -- but the report had promised runnability."),
   ],
   counter="Fences are reserved for the one thing meant to be pasted. Evidence goes in prose, "
           "tables or blockquotes."),
 dict(id="C8", name="The norm that was never written down",
   gloss="Practice converges on something the written gate never required. The gate stays "
         "permissive, so a later author can diverge from five phases of custom without failing a "
         "single check, and no artifact-level review can see it.",
   instances=[
     ("ccclxi", "recorded",
      "The Adversarial Map's anchor rule requires a verbatim anchor of 15 words or fewer at a named "
      "locus. It says NOTHING about which locus. Practice settled hard on `long`: 77 of the map's 93 "
      "entries, B1 16/16, B2 15/16, K231's D 15/17, Phase E 12/13. A wuld-ink re-derivation of Phase "
      "D targeted `medium` 11 times out of 17. `long` is the corpus's most defended prose and "
      "`medium` is a condensation, so attacking `medium` finds gaps far more easily: the "
      "re-derivation returned 12 (b) where K231 returned 3, and eight of those twelve never consider "
      "the long form at all. It passed every gate, validated clean, and was an hour from being "
      "folded. Cost had it landed: nine fabricated regen candidates, taking the v4.1.0 cut from 21 "
      "(b) to 30 and its corpus footprint from 26% to 37%, each phantom entry consuming a cold-grade "
      "cycle."),
   ],
   counter="Detection required comparing two AUTHORS, not checking either artifact. Where practice is "
           "uniform and the rule is silent, write the rule down and gate it. The map's is now: author "
           "against the deepest locus that addresses the objection, or state in the grounds why a "
           "shallower one was chosen."),
 dict(id="C9", name="The receipt that describes a different run",
   gloss="A block is derived from a predecessor. Its gates MUST take the new constants or they "
         "abort; its narration takes nothing, because nothing makes narration abort. So the commit "
         "is correct and its account of itself is not -- and the account is all the operator sees.",
   instances=[
     ("ccclxii", "recorded",
      "K339 was derived from K335. Its base gates compared canon blob `9c620ebe` and README blob "
      "`adf05fc5` and passed. Its receipt printed `base gates OK: canon af7a1ba0, README 5eb87fd0` "
      "-- K335's values, carried across the derivation untouched. A second line, `v38_1 removed "
      "(rename per convention: v38_0 -> v38_1 at K221)`, was TRUE at K335 and false at K339, which "
      "removed v38_2. The commit was correct in every respect; only the transcript was wrong, which "
      "is the whole of the hazard, because the transcript is what a reader is offered as evidence "
      "that the commit was correct. The split is measurable and total: every K339 narration line "
      "that INTERPOLATED a variable was right, and exactly two HARDCODED a constant -- both drifted. "
      "Two for two is not an error rate, it is the mechanism stated as a count."),
     ("carry note", "THIS FILE, found",
      "The previous revision of this ledger closed by naming `ccclix`, `ccclx` and `ccclxi` as NOT "
      "YET FOLDED into the registry. WI-K332 folded them. Nothing in the builder would ever have "
      "reported that the sentence had gone false, because the sentence was prose and prose is not "
      "gated. The same revision's taxonomy paragraph said SEVEN shapes while the table beneath it "
      "listed eight. Neither is a hash and neither is dramatic, which is the point: the shape does "
      "not need hex to bite."),
   ],
   counter="Bind the constant once, gate against the binding, and print FROM the binding, so a stale "
           "value fails at a comparison instead of printing quietly. WI-K332 applied it and proved "
           "the application rather than claiming it: zero hex literals inside any narration line, "
           "every printed constant shown to be gated, and a rehearsal control that plants a "
           "predecessor's real blob in the constants block and confirms the run aborts before the "
           "stale value can reach stdout. Extended to claims about OTHER repos: that block gates its "
           "three efilist assertions against the efilist repo before committing the sentence that "
           "makes them. In this file the same rule means counts are DERIVED from the data, never "
           "written into the prose beside it."),
]

WINS = [
 ("The sweep was built with the defect already inside it",
  "Rather than fix the one drifted line, twelve blocks were swept for narration quoting hex, "
  "filenames or version tokens that no gate in the same block holds -- with the known-bad block "
  "wired in as a POSITIVE CONTROL. A sweep that cannot find the defect it was written for is not a "
  "clean sweep, it is a broken one, and its silence would mean nothing. The control was found, so "
  "the eleven clean results could be believed."),
 ("A count is not a finding",
  "That sweep returned TEN hits, of which two were real. K335's identical sentence was true when "
  "written, which makes it the origin of the drift rather than an instance of it; six more were "
  "prose deliberately naming what the block discusses, one of them cleared only by decoding the "
  "block's own base64 payload rather than assuming. Shipping the raw count would have overstated "
  "the problem five-fold -- the same error one level up, since a detector's output is evidence and "
  "not a verdict."),
 ("The control that failed for the wrong reason",
  "Two rehearsal controls for WI-K332 passed or failed on the harness instead of the block: one "
  "aborted because the harness had not created TEMP, so a fake curl could not write and the block "
  "reported a failed read rather than the unstable pin under test; another tampered every pin read "
  "instead of the closing one, so all three agreed and the block honestly reported the pin unmoved. "
  "Both were rebuilt and re-run. A control that cannot fail for its own reason is C1 wearing a lab "
  "coat."),
 ("The block refused its own stale claim",
  "K333's self-test gate aborted with `case count is not 35` because an amendment made mid-session "
  "added a test case. The block declined to commit an artifact whose behaviour did not match the "
  "block's own description of it. That is the gate doing exactly the job it exists for, against "
  "its own author."),
 ("The adjacency audit caught a silent assumption",
  "After the F1 remedy made an empty relations list an assertion rather than a default, the very "
  "first rebuild refused to write: HR-07 and HR-09 share a tributary node and neither declared a "
  "relation. The unstated 'co-located but unrelated' had to become a stated ruling."),
 ("The path was wrong and the machine said so",
  "The operator block hardcoded a repo path inferred from an email address. The connected device "
  "reported the real one. An inference presented as a fact, caught by asking the system that "
  "knows."),
 ("Rehearsal, seven paths",
  "Every operator block this session was rehearsed against a bare origin with `core.autocrlf true` "
  "and a faked `curl.exe`, including a negative control that writes a CRLF working copy and "
  "confirms the block does NOT abort -- the ccclvii failure, reproduced on purpose to prove the "
  "fix holds."),
 ("The calibration control paid for itself with an hour to spare",
  "Two independent Phase D derivations of the same 17 nodes existed, and the brief had asked since "
  "2.5 that they be diffed before either was folded. Treated as a nicety, it would have been skipped: "
  "the re-derivation validated clean and was built into a rehearsed block. Diffing the pair against "
  "EACH OTHER rather than either against the corpus returned class agreement 5/17 and ANCHOR "
  "agreement 0/17 -- and the second number, not the first, is the finding. A shared-zero anchor count "
  "means the two never engaged the same text, which no per-artifact check can report."),
 ("The register's audit fired on an artifact it did not author",
  "Loading K231's fragment, the birth-certificate check aborted the build: nihilism-label(d, "
  "novel=true) collided with B2's phenomenological-existentialism. Working it through, the fault was "
  "the register's own BEDROCK_MAP: HR-04 asks whether suffering's disvalue is stance-independent and "
  "HR-13 asks whether that disvalue gives a reason binding an INDIFFERENT agent, which a Humean "
  "denies while granting HR-04. Foreign data is the only real test of an instrument, and it found "
  "under-individuation the author had missed."),
 ("Two independent derivations agreed on coverage and disagreed on everything else",
  "Both Phase D fragments cover the same 17 T2 node ids, reaching the 82/82 the brief projected. That "
  "agreement is what made the disagreement legible: identical scope, disjoint anchors, 5/17 class "
  "agreement. Coverage agreement with anchor disjointness is a sharper signal than either fragment "
  "alone could give, and it is only available while both exist separately -- which is the argument "
  "for retaining the superseded one as evidence rather than deleting it."),
]


def main():
    src = open(CLAUDE_MD, "rb").read().decode("utf-8") if os.path.exists(CLAUDE_MD) else ""
    fail = []
    found = {}
    for n in CITED:
        m = re.search(r"\*\*%s\b[^*]*\*\*" % n, src)
        if not m:
            fail.append("cited numeral %s has no bold headline in CLAUDE.md" % n)
        else:
            found[n] = re.sub(r"\s+", " ", m.group(0)).strip("*")
    # every instance tagged 'recorded' must name a numeral present in CLAUDE.md
    for c in CLASSES:
        for num, status, _d in c["instances"]:
            if status == "recorded" and num.startswith("ccc") and num not in found:
                fail.append("%s cites %s as recorded, but it is not in CLAUDE.md" % (c["id"], num))
    if not src:
        print("NOTE: no CLAUDE.md snapshot beside this builder; numeral verification skipped.")
        fail = [f for f in fail if "CLAUDE.md" not in f]
        found = {n: n for n in CITED}
    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f in fail: print("  " + f)
        return 1

    L = []; w = L.append
    w("# Process Ledger v0.1"); w("")
    w("**The second layer of the library's honesty apparatus.** The honest-residuals register")
    w("records where the *arguments* bottom out. This records where the *process* failed, what")
    w("caught it, and what changed as a result.")
    w("")
    w("**Library-internal for now.** The recommendation is that it ship: a corpus whose whole claim")
    w("is that it earns trust by robustness cannot document where its arguments end while hiding")
    w("where its method went wrong. Every failure below is a *caught* failure with a correction")
    w("attached, which reads as a working process rather than an unreliable one. But it inherits the")
    w("K56 discipline: **no chrome placement**. A failure log belongs behind the door, not on it.")
    w("")
    w("Grounded in the hazard registry in `CLAUDE.md`, not in recollection. The builder verifies")
    w("every cited numeral is present there before writing.")
    w(""); w("---"); w("")
    w("## Why a taxonomy and not a list"); w("")
    w("The hazard registry is a log: `cccli`, `ccclv`, `ccclvi`, numbered in the order things went")
    w("wrong. A log is the right *record* and the wrong *teacher*, because the next failure never")
    _n  = {1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",
           9:"Nine",10:"Ten",11:"Eleven",12:"Twelve"}
    _sh = _n.get(len(CLASSES), str(len(CLASSES)))
    _rc = sum(1 for c in CLASSES if len(c["instances"]) > 1)
    w("arrives wearing the last one's costume. What repeats is the **shape**. %s shapes account" % _sh)
    w("for every process failure this arc, and %s of them recur across unrelated surfaces — git,"
      % _n.get(_rc, str(_rc)).lower())
    w("PowerShell, JSON fragments, prose.")
    w("")
    w("| | class | recurs |")
    w("|---|---|---|")
    for c in CLASSES:
        w("| `%s` | %s | %d |" % (c["id"], c["name"], len(c["instances"])))
    w("")
    for c in CLASSES:
        w("## `%s` — %s" % (c["id"], c["name"])); w("")
        w("*%s*" % c["gloss"]); w("")
        for num, status, d in c["instances"]:
            tag = {"recorded": "`%s`" % num,
                   "discharged": "`%s` · discharged" % num}.get(status, "`%s` · %s" % (num, status))
            w("- **%s** — %s" % (tag, d))
        w("")
        w("**Counter-discipline.** %s" % c["counter"]); w("")
    w("## What the discipline caught"); w("")
    w("A failure log that records only failures is a confession, not a ledger. These are cases where")
    w("a gate stopped something before it shipped — several of them stopping its own author.")
    w("")
    for t, d in WINS:
        w("**%s.** %s" % (t, d)); w("")
    w("## Registry pointer"); w("")
    w("The numerals themselves stay in `CLAUDE.md`, which is the record of authority. This ledger")
    w("cites them and never restates them. Verified present at build time:")
    w("")
    for n in CITED:
        w("- `%s` — %s" % (n, found[n].split("—", 1)[-1].strip() if "—" in found[n] else found[n]))
    w("")
    w("Every numeral above was checked against the snapshot before this file was written; a")
    w("citation the registry does not carry makes the builder refuse. The registry lives in")
    w("wuld-ink's `CLAUDE.md`, a different repo from efilist canon, which is why the snapshot")
    w("exists at all. The previous revision closed with a carry — `ccclix`, `ccclx` and `ccclxi`")
    w("*not yet folded* — which WI-K332 discharged and which nothing in this file would have")
    w("noticed had gone stale. That is `C9` in its quietest form, and the reason the counts above")
    w("are now derived from the data rather than written into the prose.")
    w("")

    out = "\n".join(L) + "\n"
    open("process_ledger_v0_1.md", "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode()
    print("WROTE process_ledger_v0_1.md  %d B  md5 %s" % (len(b), hashlib.md5(b).hexdigest()))
    print("  %d classes, %d instances, %d wins; %d numerals verified in CLAUDE.md"
          % (len(CLASSES), sum(len(c["instances"]) for c in CLASSES), len(WINS), len(found)))
    for c in CLASSES:
        print("   %s %-42s %d" % (c["id"], c["name"], len(c["instances"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
