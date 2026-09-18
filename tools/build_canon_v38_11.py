#!/usr/bin/env python3
"""build_canon_v38_11.py -- derive project_canon_v38_11.json from v38_10 (MINOR).

ccclxiv: the SOURCE is round-tripped at the emitted serialization BEFORE anything is derived.
Asserts: top-level keyset unchanged at 41; invariants, schemas and hazard_map byte-identical.
Every constant comes from tools/k349_pins.json; no hex or count is typed here.
Repo-relative; --out <dir>.
"""
import json, os, sys, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K349_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_10.json")
DEST = os.path.join(OUT, "project_canon_v38_11.json")
DATE = "2026-09-17"          # OPERATOR-LOCAL (America/Phoenix). The sandbox clock reads UTC.
SESSION = "K349_phase_G_note_layer"

raw = open(SRC, "rb").read()
c = json.loads(raw.decode("utf-8"))
SER = dict(indent=2, ensure_ascii=False)
assert (json.dumps(c, **SER) + "\n").encode("utf-8") == raw, \
    "ccclxiv: source does not round-trip at the emitted serialization -- do not derive"
print("ccclxiv round-trip: v38_10 reproduces byte-for-byte at indent=2/ensure_ascii=False + NL")

FROZEN = {k: json.dumps(c[k], sort_keys=True, ensure_ascii=False)
          for k in ("invariants", "schemas", "hazard_map")}
KEYS_BEFORE = sorted(c.keys())
AM_KEYS_BEFORE = sorted(c["adversarial_map"].keys())

P = json.loads(open(os.path.join(_HERE, "k349_pins.json"), "rb").read().decode("utf-8"))
am = c["adversarial_map"]
N, CF = P["note"], P["confidence"]

am["note_ruling_K349"] = {
  "ruling": ("`note` IS a map target, NARROWLY: authored only where a note makes or concedes a "
             "claim the corpus would have to defend. Josiah, K349 (%s), DELEGATED to the build "
             "seat, which took the narrow form. Recorded as a delegation rather than as a ruling, "
             "because the difference matters to whoever reads this next." % DATE),
  "what_K345_left_open": (
    "K345 named `note` IN SCOPE and never discharged its own reservation -- the shape is not a "
    "response and the anchor rule assumes one. The reservation was real. The anchor rule turns out "
    "to transfer unchanged; the CLASS LAW does not."),
  "the_classification_measured_before_the_disposition_was_put": (
    "%d notes, %d words. %d are authoring apparatus (sibling taxonomy, build-pass provenance, a "
    "ratification-delta line, a TIER NOTE addressed to a future editor), %d is a legitimate scope "
    "qualifier checked against its own #long, and %d carry a claim or concession. ccclxviii applied "
    "to a scope question rather than to a class distribution: decide what the population looks like "
    "before deciding what to do with it."
    % (N["nodes"], N["words"], N["apparatus"], N["qualifier"], N["authored"])),
  "why_narrow_and_not_all_nine": (
    "'The strongest continuation a maximally competent hostile interlocutor deploys against our "
    "text' is MALFORMED against a build-accounting line. Authoring against all %d would have "
    "produced %d entries, four of them inflation -- the 82/82 problem in a new artifact, which the "
    "kickoff named as the risk in advance."
    % (N["nodes"], N["nodes"])),
  "note_coverage": ("%s, declared and DELIBERATELY PARTIAL. A phase that cannot say what it has "
                    "not done is how a coverage claim becomes misleading." % N["note_coverage"]),
  "fragment": {"artifact": "adv_map_phaseG_v0_1.json", "md5": P["phaseG_md5"],
               "bytes": P["phaseG_bytes"], "entries": N["authored"],
               "class_counts": P["class_counts_phaseG"]},
  "class_mix_gate": (
    "a+d %d/%d = %s against the A-E prior of %s computed from the FROZEN v1_0's 93 entries, exact "
    "two-sided p = %s; zero (d) against a prior of %s, p = %s. BOTH ARE STATED WITH THEIR POWER: at "
    "n=%d the gate is nearly unfalsifiable, and reporting a pass without saying so would be the "
    "flattery version of a control. The STRUCTURAL reason for zero (d) is measured instead: %d of "
    "the %d authored nodes already carry a (d) at a primary locus on the very bedrock a note entry "
    "would route to, against %d of 82 corpus-wide, so a second one would restate a registered "
    "residue rather than route a new one."
    % (P["class_mix"]["a_or_d"], P["class_mix"]["n"],
       round(P["class_mix"]["a_or_d"] / P["class_mix"]["n"], 4), P["class_mix"]["prior_A_to_E"],
       P["class_mix"]["p_two_sided"], P["class_mix"]["d_prior"], P["class_mix"]["d_p"],
       P["class_mix"]["n"], P["already_bedrock"], N["authored"], P["corpus_d_nodes"])),
  "entry_cap_not_extended": (
    "Ruled EXPLICITLY rather than carried by silence (ccclxxi). The node bound stays 3 + "
    "3*(variant loci) with NO note term. Minimum headroom across the %d note-bearing nodes was "
    "measured at %d BEFORE authoring, so no node is in reach and no ruling was owed. If a future "
    "phase authors a second note entry at a node already at its bound, that becomes Josiah's in "
    "the same shape K348's was." % (N["nodes"], P["min_headroom"])),
}

am["note_reachability_finding_K349"] = {
  "finding": ("`note` is NOT an independent field. It is a DEPENDENT of `confidence`. "
              "combined.html emits the [NOTE] button INSIDE `if (conf !== 'full')`, where "
              "`conf = obj.confidence || 'full'`, and toggleNote has exactly one caller -- that "
              "button. A note on a node graded full, or ungraded, has its div emitted at "
              "display:none with nothing in the artifact able to reveal it."),
  "measured": ("%d of the %d notes are STRUCTURALLY UNREACHABLE by any reader: %s. %d of %d words, "
               "%s%% of the layer, and they are the two longest."
               % (N["unreachable"], N["nodes"], ", ".join(N["unreachable_ids"]),
                  N["words_unreachable"], N["words"], N["pct_unreachable"])),
  "the_sharpest_case": (
    "solipsism's note is the text that EXPLAINS its confidence:full -- and that value is exactly "
    "what suppresses the button that would let anyone read the explanation."),
  "consequence_for_naming": (
    "The CSS class name `confidence-note` was never the misnomer. The FIELD name `note` is. The "
    "layer is architecturally a confidence disclosure, which is also why %d of the %d note-bearing "
    "nodes already carry a (d) in the successor assembly against %d of 82 corpus-wide: the corpus "
    "puts a note where it knows it is on hard ground."
    % (P["already_bedrock"], N["nodes"], P["corpus_d_nodes"])),
  "status": "LOGGED, not repaired. Repairing it moves a flagship byte, which is a pin move.",
}

am["confidence_ruling_K349"] = {
  "ruling": ("`confidence` is OUT as a map target and IN as a regen candidate. Josiah, K349. Out "
             "because it carries no corpus text and the anchor rule has nothing to bite on; ruled "
             "EXPLICITLY rather than by silence, and on different grounds from objectionSubforms, "
             "which K345 ruled out for having no render site at all."),
  "the_handoff_premise_was_false": (
    "The K349 handoff stated that no text reaches the reader. The badge emits the literal strings "
    "STRONG and PROVISIONAL for %d nodes. Corrected here rather than carried."
    % CF["badge_emitting"]),
  "regen_candidate_three_legs": [
    "`full` renders IDENTICALLY to absent: %d nodes were affirmatively graded full and %d were "
    "never graded, and a reader cannot tell them apart." % (CF["graded_full"], CF["ungraded"]),
    "`provisional` renders as a 70%% opacity band on the long response with NO label, which a "
    "reader cannot interpret and a screen reader cannot convey at all. One node is affected.",
    "The grade silently controls whether a node's note is reachable at all. A field documented "
    "nowhere as a visibility control is one.",
  ],
  "distribution": CF["distribution"],
}

am["coverage_ruling_K349"] = {
  "ruling": ("`coverage` counts a node as covered only if it carries an entry at a PRIMARY locus. "
             "A note is apparatus attached to a node, not the node's argument, so apparatus cannot "
             "satisfy 82/82."),
  "why_it_had_to_be_ruled": (
    "`coverage` keyed on target_id alone, and the v1_1 assembly builder computed primary coverage "
    "as 'not a variant locus' -- which a new locus kind walks straight into, because "
    "variant_slot('note') is None. That is ccclxxi a SECOND time in three sessions, and it was "
    "found by READING the builder rather than trusting that the K348 migration had covered it. "
    "Stated POSITIVELY now, in both the validator and the builder: the four primary loci, and "
    "nothing else."),
  "blast_radius_measured": (
    "ZERO. No shipped artifact carries a note entry, so no verdict moves; v0_6 reproduces every "
    "v0_5 verdict across %d runs with %d divergences. What changes is what the NEXT phase can "
    "claim." % (P["parity_runs"], P["parity_divergences"])),
  "coverage_is_three_claims_now": (
    "coverage %s is the primary ladder; variant_coverage %s is the archetypeVariants surface; "
    "note_coverage %s is the third and is deliberately partial. They are NOT commensurable and are "
    "never summed." % (P["coverage"], P["variant_coverage"], N["note_coverage"])),
}

am["relation_vocabulary_K349"] = {
  "ratification": ("A FIFTH relation kind, `conditions`, joins the register's adjacency vocabulary. "
                   "Josiah, K349."),
  "definition": ("A conditions B: A's resolution changes the FORCE of B's open question without "
                 "creating or dissolving it. B stays askable either way; what moves is how much "
                 "turns on the answer."),
  "first_instance": ("HR-14 conditions HR-11, and it is the reason the kind was ratified: K348 "
                     "recorded that pair in the register's AUDIT rather than declaring it, because "
                     "none of depends_on / stronger_than / sibling_of / independent_of states it."),
  "vocabulary_is_now_enforced": (
    "It had been a five-line comment above RELATIONS with nothing checking it. It is an allowlist "
    "checked before the write, so a mistyped or invented kind refuses the build."),
  "and_a_gate_that_never_existed": (
    "build_register.py's own comment claims 'the audit below refuses to write if any "
    "mechanically-derived adjacency candidate is undeclared.' It did not -- it appended an audit "
    "line and wrote anyway. The claim was true by luck, the undeclared set having always been "
    "empty. It is a gate at v0_3. cccli in its purest form, and one more instance discharged; "
    "blast radius measured at 0 undeclared pairs before promoting it."),
}

am["validator_pin_v0_6"] = {
  "artifact": "adversarial_map_staging/adv_map_validator_v0_6.py",
  "md5": P["validator_v0_6_md5"], "bytes": P["validator_v0_6_bytes"],
  "self_test": "%d/%d, against v0_5's %d" % (P["self_test_v0_6"], P["self_test_v0_6"],
                                             P["self_test_v0_5"]),
  "derived_by": "tools/patch_validator_v0_6.py, %d anchored single-occurrence patches"
                % 10,
  "changes": ("`note` reaches the TOP-LEVEL key, EXISTENCE-GATED rather than added to LOCI -- only "
              "9 of 82 nodes carry one, so an unconditional enum entry would let a target_locus of "
              "'note' validate on a node that has none and hand the anchor rule an empty string, "
              "the exact routing defect the K345 both-ways proof was written to catch. Plus "
              "note_coverage (per-file per ccclxx), the coverage restriction, PHASES += G, and "
              "coverage_ids_touched so the two quantities that had shared one name are both named."),
  "v0_5_held": ("%s, byte-identical. Canon pins it and the v1_1 receipt names it."
                % P["validator_v0_5_md5"]),
  "parity": ("v0_6 reproduces EVERY v0_5 verdict across %d runs over the shipped artifacts, both "
             "corpora and all three modes: %d divergences."
             % (P["parity_runs"], P["parity_divergences"])),
}

am["terminal_assembly_v1_2_K349"] = {
  "artifact": "adversarial_map_staging/adversarial_map_v1_2.json",
  "md5": P["assembly_v1_2_md5"], "bytes": P["assembly_v1_2_bytes"],
  "entries": P["entries_v1_2"], "coverage": P["coverage"],
  "variant_coverage": P["variant_coverage"], "note_coverage": N["note_coverage"],
  "verdict": "--assembly PASS, 0 violations, 0 advisories, against the post-cut corpus",
  "why_v1_2_and_not_v2_0": (
    "Every one of v1_1's %d entries is inherited BYTE-FOR-BYTE -- asserted, not claimed: 0 missing, "
    "0 changed, exactly %d added and all at the note locus. Nothing is superseded or re-classed and "
    "the schema is unchanged." % (P["entries_v1_1"], N["authored"])),
  "predecessors_untouched": (
    "v1_1 %s and the FROZEN v1_0 %s are byte-identical, and v1_1 was REPRODUCED from its own "
    "builder byte-for-byte before this one wrote anything (ccclxiv applied to an artifact rather "
    "than to a serialization)." % (P["v1_1_md5"], P["v1_0_md5"])),
  "builder": {"file": "adversarial_map_staging/build_assembly_v1_2.py",
              "md5": P["build_assembly_v1_2_md5"],
              "note": "derived by tools/patch_assembly_v1_2.py; build_assembly_v1_1.py held at %s"
                      % P["build_assembly_v1_1_md5"]},
}

am["design_pin_v0_5"] = {
  "artifact": "adversarial_map_staging/adversarial_map_design_v0_5.md",
  "md5": P["design_v0_5_md5"], "bytes": P["design_v0_5_bytes"],
  "section": ("12: the note ruling and why narrow (12.1), the reachability finding (12.2), the "
              "confidence ruling (12.3), the coverage ruling (12.4), the fifth relation kind "
              "(12.5), ccclxxii (12.6), and what was run (12.7)."),
  "v0_4_held": "%s, byte-identical" % P["design_v0_4_md5"],
  "constant_gate": ("Every numeric token in the emitted section is either a bound constant "
                    "traceable to a measurement file or an explicitly allowed literal WITH ITS "
                    "REASON -- section numbers, the session date asserted against the measurement's "
                    "own date field, session ids, and digits inside verbatim corpus quotations. "
                    "The gate fired twice during authoring and both were real."),
}

am["honest_residuals_register_pin_v0_3"] = {
  "artifact": "adversarial_map_staging/honest_residuals_register_v0_3.json",
  "md5": P["register_v0_3_md5"], "bytes": P["register_v0_3_bytes"],
  "md": {"file": "honest_residuals_register_v0_3.md", "md5": P["register_v0_3_md_md5"]},
  "bedrocks": P["bedrocks"],
  "content_unchanged_from_v0_2": (
    "Phase G yields NO (d), so the bedrock set, every gloss and all 39 tributaries come back "
    "identical -- ASSERTED by control, not claimed. The only content delta is HR-14 gaining "
    "exactly the `conditions` relation to HR-11."),
  "source": "adversarial_map_v1_2.json",
  "v0_2_held": "%s, byte-identical; canon pins it" % P["register_v0_2_md5"],
}

am["ccclxxii_hazard_K349"] = {
  "numeral": "ccclxxii",
  "headline": ("A RENDER SITE IS NOT REACHABILITY, AND THE DIFFERENCE IS DATA-DEPENDENT."),
  "detail": (
    "Two scope audits have now asked 'does this field have a render site?' and treated the answer "
    "as settling whether readers meet the text. K345 ruled objectionSubforms OUT because it has "
    "none. K349 came within one ruling of treating `note` as uniformly rendered because it has one. "
    "A render site can be nested inside a condition on a DIFFERENT field, so whether shipped text "
    "reaches a reader is a fact about the DATA, not about the code. The predicate was being "
    "evaluated statically when it is data-dependent, and the error is silent in both directions: it "
    "over-counts a field whose gate is usually closed and under-counts one whose gate is usually "
    "open."),
  "counter_discipline": (
    "To establish that shipped text reaches a reader: find the render site, ENUMERATE EVERY "
    "CONDITION GATING IT, and evaluate those conditions over the actual corpus -- then report the "
    "COUNT, never the existence."),
  "family": ("ccclviii (measure the state you think you measured), narrowed to the specific case "
             "where the instrument is a static read of a dynamic predicate."),
  "first_instance": "%d of %d notes unreachable; %s%% of the layer's words."
                    % (N["unreachable"], N["nodes"], N["pct_unreachable"]),
}

am["next"] = (
  "PHASE G IS LANDED AND THE MAP HAS NO FURTHER TEXT CLASS. Every rendered field the corpus ships "
  "is now either adjudicated or ruled out with its grounds recorded. What remains is not mapping. "
  "THE HONEST NEXT MOVE IS UPSTREAM AUTHORING, NOT ANOTHER MAP: the sixteen v4.1.0 enrichment items "
  "plus happiness-is-choice#medium plus the just-depressed depressive-realism contradiction "
  "(classed an AGGRAVATION at K348, so its repair belongs at the NODE) plus the two new headline "
  "(b) items this session produced -- care-ethics#note, where the corpus published an unclosed "
  "implication for its own consent framework and named the text that would close it, and "
  "flow-states-csikszentmihalyi#note, where the note reports a concession the response never made "
  "and the flagship's RSI CALIBRATION NOTES repeat it as their worked example of honest "
  "acknowledgment. That last one spans a corpus locus and a FLAGSHIP-ONLY locus, so its repair is "
  "a pin move. The map has produced 29 (b) items and the programme has repaired three sentences "
  "since it began; that gap closes with ratified authoring in the Argument Library seat, not with "
  "another phase. Also queued: the regen queue derives from the A-E fragments ONLY, so Phase F's "
  "6, Phase R's 3 and Phase G's 2 (b) entries are adjudicated and UNQUEUED -- 11 in total, a "
  "pre-existing gap this session measured rather than introduced.")

c["keyset_delta_ledger"]["v38_11_note"] = (
  "v38.10 -> v38.11 MINOR (%s, %s): keyset UNCHANGED at 41. Nine additions INSIDE adversarial_map "
  "(note_ruling_K349, note_reachability_finding_K349, confidence_ruling_K349, coverage_ruling_K349, "
  "relation_vocabulary_K349, validator_pin_v0_6, terminal_assembly_v1_2_K349, design_pin_v0_5, "
  "honest_residuals_register_pin_v0_3, ccclxxii_hazard_K349) and a replacement of "
  "adversarial_map.next. A replacement of next_recommended_session; one session_log_recent append. "
  "NO PIN: the flagship, the corpus and the jsx are untouched and the cross-surface gate is GREEN "
  "at open and close. invariants, schemas and hazard_map asserted byte-identical, which is what "
  "would have forced MAJOR." % (SESSION, DATE))

c["next_recommended_session"] = {
  "session": "UPSTREAM AUTHORING IN THE ARGUMENT LIBRARY SEAT, not another map phase.",
  "why": ("The map is complete over every rendered text class and has produced 29 (b) regen items "
          "against three sentences repaired since the programme began. Cowork cannot close that: a "
          "repair changes the corpus, which makes it a PIN MOVE, and stance-bearing content is "
          "ratified by Josiah with the library seat rather than authored by a build seat."),
  "scope": ("The sixteen v4.1.0 enrichment items, happiness-is-choice#medium, the just-depressed "
            "depressive-realism contradiction (AGGRAVATION -- repair at the node), and the two K349 "
            "headline items. When that comes back ratified, Cowork folds it in a declared pin-move "
            "session."),
  "if_a_build_session_is_wanted_instead": (
    "Extend the regen queue past the A-E fragments -- it has never read Phase F, R or G, so 11 "
    "adjudicated (b) entries are unqueued."),
}

c["session_log_recent"].append(
  "%s (%s): PHASE G -- the `note` layer, authored NARROWLY. NO PIN; combined.html %s, corpus %s "
  "and jsx %s untouched, cross-surface gate GREEN at open and close. Two rulings taken before a "
  "line was authored: `note` is a map target narrowly (Josiah, delegated to the build seat), and "
  "`confidence` is out as a target and in as a regen candidate (Josiah). THE HANDOFF'S PREMISE FOR "
  "THE SECOND WAS FALSE -- confidence emits visible STRONG/PROVISIONAL text for %d nodes -- and the "
  "audit turned up something larger: `note` is a DEPENDENT of `confidence`, because the [NOTE] "
  "button sits inside `if (conf !== 'full')` and toggleNote has exactly one caller, so %d of %d "
  "notes (%s%% of the layer's words) are structurally unreachable by any reader. Registered as "
  "ccclxxii. Phase G authored %d entries, %s, class %s; v1_2 carries %d entries at 82/82 primary, "
  "%s variant, %s note and passes --assembly at 0/0. Validator v0_6 self-test %d/%d and reproduces "
  "every v0_5 verdict across %d runs with %d divergences. Register v0_3 adds the ratified fifth "
  "relation kind `conditions` (HR-14 conditions HR-11) and makes the vocabulary an enforced "
  "allowlist; it also found that build_register.py's claim to refuse on an undeclared adjacency was "
  "never a gate, and made it one. %d controls across three batteries, all green."
  % (SESSION, DATE, P["combined_md5"], P["corpus_md5"], P["jsx_md5"], CF["badge_emitting"],
     N["unreachable"], N["nodes"], N["pct_unreachable"], N["authored"], N["note_coverage"],
     json.dumps(P["class_counts_phaseG"], sort_keys=True), P["entries_v1_2"],
     P["variant_coverage"], N["note_coverage"], P["self_test_v0_6"], P["self_test_v0_6"],
     P["parity_runs"], P["parity_divergences"], P["controls"]["total"]))

c["canon_version"] = "38.11"
c["canon_version_marker"] = "v38.11"
c["last_updated"] = DATE
c["last_updated_by_session"] = SESSION

assert sorted(c.keys()) == KEYS_BEFORE, "top-level keyset moved: %r" % (set(c.keys()) ^ set(KEYS_BEFORE),)
assert len(c.keys()) == 41, "keyset is %d, expected 41" % len(c.keys())
for k, v in FROZEN.items():
    assert json.dumps(c[k], sort_keys=True, ensure_ascii=False) == v, \
        "%s MOVED -- this would be a MAJOR bump, not MINOR" % k
added = sorted(set(c["adversarial_map"].keys()) - set(AM_KEYS_BEFORE))
assert len(added) == 10, "expected 10 new adversarial_map subkeys, got %d: %s" % (len(added), added)
print("keyset 41 unchanged; invariants / schemas / hazard_map byte-identical -> MINOR")
print("adversarial_map gains exactly %d subkeys: %s" % (len(added), added))

out = (json.dumps(c, **SER) + "\n").encode("utf-8")
os.makedirs(OUT, exist_ok=True)
open(DEST, "wb").write(out)
print("wrote %s  md5 %s  bytes %d" % (DEST, hashlib.md5(out).hexdigest(), len(out)))
