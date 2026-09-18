import json,os,hashlib,copy
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
E=REPO
SRC=os.path.join(REPO,"project_canon_v38_4.json")
raw=open(SRC,"rb").read()
assert hashlib.md5(raw).hexdigest()=="2ca9553200f6f5d3d0394493778cb0db","BASE GUARD FAIL"
c=json.loads(raw.decode("utf-8"))
FROZEN={k:json.dumps(c[k],sort_keys=True,ensure_ascii=False) for k in ("invariants","schemas","hazard_map")}
KEYS_BEFORE=list(c.keys())
def md5f(p): return hashlib.md5(open(p,"rb").read()).hexdigest()
def szf(p): return os.path.getsize(p)
D=os.path.join(REPO,"adversarial_map_staging")
PINS={n:(md5f(os.path.join(D,n)),szf(os.path.join(D,n))) for n in
      ("adv_map_validator_v0_3.py","adv_map_phaseR_v0_1.json","adversarial_map_design_v0_2.md","loci_coverage_measurement_v0_1.json")}
am=c["adversarial_map"]

am["loci_enum_ruling_K345"]={
 "ruling":"EXTEND. Josiah, K345 (2026-09-17). target_locus reaches responses.archetypeVariants via the dotted form 'archetypeVariants.<slot>', slot in {sophisticate, defender, drifter, blended}, valid only where that slot exists on that node. answered_by refs take the same grammar.",
 "why_the_alternative_died":"The defensible version of leaving the enum at four was that variants are register re-castings of an already-adjudicated response. MEASURED WITH CONTROLS and FALSIFIED: content-token novelty of each variant against its own node's four primary loci has median 0.591, against 0.293 for a KNOWN register-compression (short vs medium+long+diagnosis) and 0.498 (medium vs long+diagnosis), with an unrelated-node ceiling of 0.855. Variants are adjacent new argument on the same target. 27 of 39 name another slot explicitly and hand work to it -- the slots partition the dialectical labour rather than restating one another. Out-of-scope remained available on BUDGET grounds; it was not taken.",
 "entry_cap_amended":"The cap's unit moves from the node to the locus: <=3 per (target_id, target_locus), because the locus is the unit the anchor engages. A second node-level bound holds at 3 + (variant loci on that node), so a node carrying NO variants keeps the Q1-ratified bound of 3 EXACTLY and the gate extends in proportion to the text rather than being loosened flat. Measured need: 29 free entry slots across the 16 variant nodes against 39 variant loci, with red-button-repugnant already at cap. Josiah delegated the form of the amendment, K345.",
 "coverage_is_now_two_claims":"coverage 82/82 continues to mean the PRIMARY ladder. variant_coverage <hit>/<total> is reported on every run and gated whenever a fragment declares it. Completion is deliberately NOT forced by the gate: Phase F is owed and a successor map must be able to exist before it lands. A map that cannot state what it has not done is how 82/82 became misleading in the first place.",
 "note_IN_SCOPE_unadjudicated":"responses-adjacent `note`: 9 nodes, 544 words, RENDERED behind a toggle at responseLevel==='long'. Editorial apparatus rather than rebuttal prose, and at least one instance (care-ethics) is a published concession that the node's own response is underpowered -- an attack surface of an unusual kind. NOT added to the enum here, because its shape is not a response and the anchor rule assumes one. Named as owed, with grounds, rather than left silent.",
 "objectionSubforms_OUT_OF_SCOPE":"1 node (violence-as-reductio), 4 units, 646 words, and NOT RENDERED: grep finds exactly one occurrence in combined.html and one in the JSX, and in both the only occurrence is the data key. The map's contract is the strongest continuation against text shipped TO A READER. Decided on measurement, recorded so that if it is ever surfaced the scope decision is visible rather than overlooked.",
 "phase_F_opened":"39 variant loci across 16 nodes (sophisticate 13, defender 12, drifter 7, blended 7; by tier T1 7, T2 2, T3 4, T4 2, T5 1). Tier-descending within the phase per design section 3. Library-seat authoring, Max-class; Cowork folds.",
 "evidence":{"file":"adversarial_map_staging/loci_coverage_measurement_v0_1.json","md5":PINS["loci_coverage_measurement_v0_1.json"][0],"bytes":PINS["loci_coverage_measurement_v0_1.json"][1],
   "gate":"every constant in design v0_2 section 9 was extracted programmatically and asserted equal to a value in this file: 20 of 20 matched. The doc transcribes; the file measures."}}

am["design_pin_v0_2"]={
 "file":"adversarial_map_staging/adversarial_map_design_v0_2.md","md5":PINS["adversarial_map_design_v0_2.md"][0],"bytes":PINS["adversarial_map_design_v0_2.md"][1],
 "landed":"K345 (2026-09-17); NO PIN",
 "supersedes":"adversarial_map_design_v0_1.md, which stays on disk BYTE-IDENTICAL at 49514ec9d631c3fbdf2cbf227923dd1b because design_pin above pins it and the Phase A-E receipts cite it. Sections 0-8 are v0.1 verbatim; section 9 is the K345 amendment and three inline pointers into it were added at the schema line, the coverage contract and the anchor rule."}

am["validator_pin_v0_3"]={
 "file":"adversarial_map_staging/adv_map_validator_v0_3.py","md5":PINS["adv_map_validator_v0_3.py"][0],"bytes":PINS["adv_map_validator_v0_3.py"][1],
 "landed":"K345 (2026-09-17); NO PIN",
 "supersedes":"adv_map_validator_v0_2.py, which stays on disk BYTE-IDENTICAL at d775fbea1cd726690a49acf0914270c2 because adversarial_map_v1_0.json's receipt names it and that receipt has to stay reproducible.",
 "proof":"--self-test 50/50 = v0_2's 36 inherited cases plus 14 K345 controls written FOR the new behaviour, both directions: a well-formed variant entry validates; an absent slot and a bogus slot each trip target-locus; an anchor absent from the named variant trips anchor-rule; and the ROUTING PROOF runs both ways -- a #long anchor named at a variant locus fails, and a variant anchor named at #long fails, which is what proves locus_text reads the named variant ALONE and never a concatenation. Plus per-locus cap, node bound unchanged at 3 for a variant-less node, node bound scaling to 5 and tripping at 6, declared variant_coverage true and false, and answered_by pointing at a present and an absent variant.",
 "regression":"v0_3 reproduces v0_2's verdict on the FROZEN adversarial_map_v1_0.json in both directions: PASS 21 checks / 0 violations / 0 advisories against the pre-cut corpus it names, and FAIL with exactly the same 5 violations against the post-cut corpus. The instrument changed and the frozen artifact's receipt did not."}

am["successor_map_phase_R"]={
 "file":"adversarial_map_staging/adv_map_phaseR_v0_1.json","md5":PINS["adv_map_phaseR_v0_1.json"][0],"bytes":PINS["adv_map_phaseR_v0_1.json"][1],
 "landed":"K345 (2026-09-17); NO PIN","pinned_to":"the POST-CUT corpus 04bf6482aa0374ee92a81c1d55ec41f8",
 "state":"MAPPED, PRE-TRIAGE. 4 entries, class a1 b3, coverage_distinct_ids 3, variant_coverage 1/39.",
 "changed_locus_set":"DERIVED, not inherited: 367 loci swept pre-cut against post-cut under the v0_3 enum (82x4 primary + 39 variant), 4 changed. The handoff named three. The fourth, just-depressed#archetypeVariants.defender, became nameable only once the ruling extended the enum -- so the ruling changed the size of this session's own authoring set.",
 "entries":{
  "happiness-is-choice#long":"(b) headline. The correction to the GENETIC term installed an error in the ENVIRONMENTAL one: the non-genetic variance is dominated by the non-shared component, while the four examples offered (birthplace, family, socioeconomic position, era) are shared-environment factors. The illustration is drawn from the smallest term and the claim is made about the largest, which is where a voluntarist locates choice. Also recorded: the repaired paragraph makes a STRONGER claim than the text it replaced, which had conceded a modest contribution from intentional activity. A repair logged as pure subtraction removed a concession and added a denial.",
  "just-edgy#long":"(b) minor. 'the ones who remained alive and vocal' concedes in passing the correlation between antinatalist conviction and mortality that the adjacent nodes deny the objector any use of. Dilemma: load-bearing and it grants the neighbouring objection its premise, or decorative and the survivorship inference has no selection mechanism left. change-your-mind already ships the clean form.",
  "just-depressed#long":"(b) headline. Exasperation is a SINGLE motive and it produces both utterances, so the 'reliable tell' does not establish that the first was insincere. That tell is the only evidence for the motive attribution; the attribution licenses the frequency claim; the frequency claim is what the node says its design is built for. The v4.1.0 cut removed the unsourced ratio and left the architecture the ratio rested on.",
  "just-depressed#archetypeVariants.defender":"(a), answered_by just-depressed#long. The slot's headline play is a motive verdict, the objection's own vice; #long holds that naming a bad-faith ad hominem is not itself one and does not become one in self-defence, which meets it on the best reading. THE FIRST VARIANT LOCUS THE MAP HAS EVER REACHED, and what it found is that the primary ladder already answers the slot's central exposure -- a datum about expected Phase F yield, not a licence to skip it."},
 "the_trap_was_named_and_it_did_not_close":"The handoff warned against assuming the three come back (a). They did not: three (b) and one (a), and the (a) is at the locus the handoff could not name. The anchor provenance control is the sharper result -- only ONE of the four anchors sits in text the cut moved. Three sit in text the cut never touched, which means the strongest continuation against those loci was available before the cut and five phases of mapping did not take it.",
 "FINDING_strongest_vs_repairable":"Phase A-E authored 1.13 entries per node against a cap of 3, and the entry taken was consistently the REPAIRABLE-DEFECT move (a clause with a fixable error, routable as a (b) regen candidate) rather than the STRONGEST-ATTACK move the design's section 0 contract actually asks for. Nothing in the written gates distinguishes the two, and the anti-inflation machinery and the (b)/(c) routing shapes pull toward repairable. This is ccclxi's shape a third time: practice settled on one reading, the gate never checked which, nothing failed. Detected the way ccclxi was -- by comparing two AUTHORS, not by checking either artifact. NOT ruled here: it is a design question for Josiah and the library seat, because it changes what an entry is FOR.",
 "logged_not_authored":[
  "just-depressed asserts depressive realism as evidence at #short ('research suggests that pessimists often assess reality with greater objective accuracy') and #medium ('clinical studies ... demonstrate'), and REPUDIATES it at #long ('narrow and contested, and nothing here leans on it') and in its sophisticate variant ('a sophisticate who reached for it would be cherry-picking'). A reader using the depth toggle sees the corpus assert and then disown the same finding. Invisible to a per-locus map by construction; found only by comparing loci.",
  "happiness-is-choice#medium still performs the set-point slide ('heritable set-points that no amount of positive thinking can override') that its own repaired #long now warns against, two loci apart in one node. Queued at K344, still queued: authoring it is enrichment-lane work, not re-adjudication."]}

am["terminal_artifact_pin"]["scope_note_K345"]=("coverage '82/82 nodes, 93 entries' means 82/82 nodes AT THE FOUR PRIMARY LOCI. "
 "At the time it was assembled the validator's LOCI enum could not name responses.archetypeVariants, so 39 variant loci across 16 nodes "
 "-- 10,069 words of rendered corpus text -- were outside what the claim could cover. THE ARTIFACT IS NOT RE-RUN AND NOT RE-PINNED AND ITS "
 "BYTES DO NOT MOVE. This note is the scope the claim always had, written down. K345.")

c["open_questions"]["active"]["CORPUS_IS_REACTIVE_ONLY_K345"]=(
 "RAISED BY JOSIAH, K345, recorded so it does not stay an observation. THE LIBRARY IS AN OBJECTION "
 "CATALOGUE FIRST AND A REBUTTAL CATALOGUE SECOND, AND IT HAS NO THIRD LANE. Every one of the 82 nodes is "
 "indexed by an objection AGAINST antinatalism / NU / efilism, and the corpus's own content is the reaction "
 "to it. The positive arguments FOR those positions -- the asymmetry, consent and foreseeable-imposition, "
 "risk-imposition, and the rest -- are nowhere catalogued in their own right; they appear only as material "
 "cited inside rebuttals. Two distinct gaps follow, and they are not the same gap. (1) NO POSITIVE-ARGUMENT "
 "CATALOGUE: there is no surface that enumerates and individuates the arguments themselves, as objects, the "
 "way objections-index.json does for objections. (2) NO GRADED CORPUS OF REBUTTALS IN THE WILD: nothing "
 "collects or grades how these exchanges actually run on the internet and in real-world contexts; the RSI "
 "ledger grades OUR rebuttals against OUR objection set, which is a different thing. NOT SCOPED AND NOT "
 "BUILT HERE. Josiah's framing: something to note for documentation later and perhaps its own implementation "
 "eventually, beyond just creating variations of rebuttals. It bears on the Adversarial Map because the map "
 "inherits the corpus's reactive shape -- a map of the strongest continuations against our rebuttals cannot "
 "reach an argument the corpus never states in its own voice.")
c["open_questions"]["active_count"]=len(c["open_questions"]["active"])
c["adversarial_map"]=am
c["canon_version"]="38.5"; c["canon_version_marker"]="v38.5"
c["last_updated"]="2026-09-17"; c["last_updated_by_session"]="K345_successor_map_loci_ruling"
c["keyset_delta_ledger"]["v38_5_note"]=("v38.4 -> v38.5 MINOR (K345_successor_map_loci_ruling, 2026-09-17): keyset UNCHANGED at 41 "
 "(no top-level key added or removed; value-only edits to canon-meta, session_log_recent, next_recommended_session and open_questions, and five additions "
 "INSIDE adversarial_map: loci_enum_ruling_K345, design_pin_v0_2, validator_pin_v0_3, successor_map_phase_R, and a scope_note_K345 inside "
 "terminal_artifact_pin). invariants, schemas and hazard_map asserted byte-identical by the builder, which is what would have made this MAJOR. "
 "NO PIN: the flagship, the corpus, the JSX, the ledger and objections-index are untouched, and adversarial_map_v1_0.json is byte-identical.")
c["session_log_recent"].append(
 "K345_successor_map_loci_ruling (2026-09-17, wuld.ink Cowork; NO PIN) [MINOR v38.4->v38.5]: THE LOCI ENUM RULING AND THE SUCCESSOR MAP'S "
 "FIRST FRAGMENT. Josiah ruled EXTEND after the alternative was measured rather than argued: the 'archetype variants are just register' "
 "rationale was falsified at median content-token novelty 0.591 against a known register-compression floor of 0.293 and an unrelated ceiling "
 "of 0.855, with 27 of 39 variants naming another slot and handing work to it. Validator v0_3 reaches archetypeVariants via a dotted locus, "
 "moves the entry cap from the node to the LOCUS while leaving a variant-less node's bound at exactly the ratified 3, and reports "
 "variant_coverage as a claim separate from coverage; --self-test 50/50 with 14 controls written for the new behaviour, including a "
 "both-directions routing proof, and it reproduces v0_2's verdict on the FROZEN v1_0 in both directions. Design v0_2 writes the ruling down "
 "(ccclxi's remedy), scoping `note` IN and unrendered `objectionSubforms` OUT on measured grounds, and every one of its 20 constants was "
 "extracted programmatically and asserted against the measurement file. Phase R re-adjudicated FOUR loci, not three -- the ruling made "
 "just-depressed#archetypeVariants.defender nameable -- returning a1 b3, and the anchor provenance control showed only ONE of the four anchors "
 "sits in text the cut moved. Two findings LOGGED not authored, and one raised for ruling: the program has been authoring the repairable-defect "
 "move where the contract asks for the strongest-attack move, and no gate distinguishes them.")
c["next_recommended_session"]={
 "action":"PHASE F -- the 39 archetypeVariants loci across 16 nodes, now that the K345 ruling makes them nameable. Library-seat authoring, Max-class, tier-descending within the phase per design v0_2 section 3; Cowork folds. adv_map_phaseR_v0_1.json is the sibling fragment already pinned to the post-cut corpus; adversarial_map_v1_0.json is FROZEN and is not the input to edit.",
 "first_decision":"Whether an entry names the STRONGEST continuation or the most REPAIRABLE one. Phase A-E consistently authored the second while design section 0 asks for the first, and no written gate distinguishes them (successor_map_phase_R.FINDING_strongest_vs_repairable). It decides what Phase F is for and it is Josiah's plus the library seat's, not a build call.",
 "then":"The terminal successor assembly, once Phase F lands: Phase R + the 78 inherited entries + Phase F, pinned to 04bf6482, declaring BOTH coverage and variant_coverage. Then the sixteen v4.1.0 enrichment items, plus happiness-is-choice#medium and the just-depressed depressive-realism cross-locus contradiction, both logged at K345.",
 "not_this_session":"diagnosis-not-refutation, the single (c), and the v5.0.0 intake cut. Unchanged from v38.3 and v38.4: it belongs to a session that begins fresh, not one that ends tired. gods-plan and western-philosophy stay HELD for it.",
 "gates":["the successor map is NOT assembled until Phase F lands; a partial assembly would restate the 82/82 problem in a new artifact",
          "adversarial_map_v1_0.json stays byte-identical at c4989e98b042e2f787a82df3f11ecdad; its scope note lives in canon, not in the file",
          "`note` (9 nodes, 544 words, rendered) is IN SCOPE and unadjudicated -- it is named as owed and must not drift back into silence"]}

assert list(c.keys())==KEYS_BEFORE, "KEYSET MOVED"
for k,before in FROZEN.items():
    assert json.dumps(c[k],sort_keys=True,ensure_ascii=False)==before, "MAJOR-CLASS EDIT to %s"%k
out=os.path.join(OUT,"project_canon_v38_5.json")
b=(json.dumps(c,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
open(out,"wb").write(b)
print("WROTE %s"%out)
print("  bytes %d  md5 %s"%(len(b),hashlib.md5(b).hexdigest()))
print("  keyset %d (unchanged)  invariants/schemas/hazard_map byte-identical: asserted"%len(c))
print("  source UNTOUCHED md5 %s"%hashlib.md5(open(SRC,'rb').read()).hexdigest())
