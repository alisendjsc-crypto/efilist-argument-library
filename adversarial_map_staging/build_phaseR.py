import json,os,hashlib,importlib.util,sys
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
E=REPO
spec=importlib.util.spec_from_file_location("v", os.path.join(REPO,"adversarial_map_staging","adv_map_validator_v0_3.py"))
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
CORPUS=os.path.join(REPO,"efilist_argument_library_v4_0_0.json")
craw=open(CORPUS,"rb").read(); corpus=json.loads(craw.decode("utf-8"))
CMD5=hashlib.md5(craw).hexdigest(); ODIG=v.objections_digest(corpus)
assert CMD5=="04bf6482aa0374ee92a81c1d55ec41f8", CMD5
assert ODIG.startswith("2c5a083a"), ODIG
N={n["id"]:n for n in corpus["objections"]}
DATE="2026-09-17"; SEAT="wuld.ink Cowork, K345"

E1_MOVE=("The correction to the genetic term installs an error in the environmental one. "
"Wellbeing's non-genetic variance is dominated by the non-shared component, and the four examples "
"offered here (birthplace, family, socioeconomic position, era) are shared-environment factors, the "
"component twin designs find contributes least to adult wellbeing. The illustration is drawn from the "
"smallest term while the claim is made about the largest, which is where a voluntarist locates choice "
"in the first place. And no such study delivers overstates what these designs can show: the non-shared "
"term is a residual that absorbs measurement error and everything unmodelled, so it neither grants "
"volition nor denies it.")
E1_GROUNDS=("Best reading: largely unchosen is a hedge and the parenthetical is illustrative rather than "
"exhaustive. That reading does not rescue the clause, because the hedge is spent in the same sentence, "
"which denies the voluntarist any volitional remainder at all and offers the illustrative list as its "
"only support. Worth stating plainly: the repaired paragraph makes a STRONGER claim than the text it "
"replaced, which had conceded a modest contribution from intentional activity. A repair recorded as pure "
"subtraction removed a concession and added a denial. Headline because this is the node's designated "
"empirical paragraph, the non-shared-variance correction is the standard next one a competent objector "
"makes, and the fix again costs no ground: say what the finding shows about between-person differences "
"and stop there.")

E2_MOVE=("In a node shelved beside just-depressed and why-not-suicide, remained alive is not idle. It "
"concedes in passing the correlation between antinatalist conviction and mortality that the adjacent "
"nodes spend their length denying the objector any use of. Either the word is load-bearing, and you have "
"granted the premise of the objection next door, or it is decorative, and the sentence reduces to the "
"claim that the vocal are vocal, leaving the survivorship inference with no selection mechanism at all. "
"Your own corpus shows the clean form: change-your-mind runs the identical argument from visibility "
"without reaching for mortality.")
E2_GROUNDS=("Best reading takes alive as idiomatic, part of a fixed phrase rather than a claim. That reading "
"is available and it empties the sentence: a survivorship inference needs a selection mechanism, and with "
"mortality removed the only one left is visibility, which change-your-mind already states more precisely. "
"So the charitable reading costs the argument and the literal reading costs the corpus its consistency. "
"Minor rather than headline: one word in one clause, the genetic-fallacy core is untouched, and the repair "
"has a sibling template already shipped. Noted for the record, this is not the clause the v4.1.0 cut "
"touched. A re-adjudication asks what the strongest continuation against the current text is, not whether "
"the repair worked, and the strongest move here survived the repair untouched.")

E3_MOVE=("Exasperation is a single motive and it produces both utterances. Someone who opens with get help "
"and, twenty minutes into being argued with, reaches for the second sentence has not shown the first was "
"insincere. They have shown that concern curdled. Motives are not fixed across an exchange and nothing "
"here establishes that they are. This tell is the only evidence offered for the motive attribution; the "
"attribution is what licenses the frequency claim; the frequency claim is what the node says its design "
"is built for. One ordinary alternative explanation and all three go.")
E3_GROUNDS=("Best reading: the two utterances are incompatible under a motive of care held STEADILY, which is "
"true and which the text does not say. It says a single motive of care, and a motive that changes mid-thread "
"is still single in the only sense that sentence needs to exclude. The node's own charge is that inferring "
"from etiology is the objector's fallacy; it then infers hostility from a sequence of utterances, which is "
"that inference in the same direction. Headline, and the repair is NOT subtractive: the v4.1.0 cut removed "
"the unsourced ratio and left the architecture the ratio was resting on. The node has to either produce "
"evidence the motive was hostile from the start or drop the motive claim and rest on the argument-level "
"case, which it can afford to do.")

E4_MOVE=("The slot's headline play is a motive verdict, which is the move this node condemns, fired in the "
"other direction. Met rather than merely addressable: the long response holds that naming a bad-faith ad "
"hominem is not itself one and does not become one when deployed in self-defence, and that is exactly the "
"charge.")
E4_GROUNDS=("Class law run in order stops at (a). The strongest continuation against the defender slot is that "
"its recommended reply diagnoses the opponent's motive, the objection's own vice; the slot polices the "
"smaller version of this in its boomerang and leaves the larger one undisclaimed. The long response meets it "
"directly and on the best reading, since bad faith just is a motive attribution. Recorded as coverage, not as "
"a defect. This is the first archetypeVariants locus the map has ever been able to reach, and what it found "
"is that the primary ladder already answers the slot's central exposure. That is a datum about expected "
"Phase F yield, not a licence to skip it.")

ENTRIES=[
 dict(target_id="happiness-is-choice", target_locus="long",
      target_anchor="the environmental share is itself largely unchosen",
      adversarial_move=E1_MOVE, **{"class":"b"}, grounds=E1_GROUNDS,
      routing={"regen_candidate":{"axis_hit":["s","v"],"severity":"headline"}},
      status="mapped", provenance={"phase":"R","date":DATE,"seat":SEAT}),
 dict(target_id="just-edgy", target_locus="long",
      target_anchor="the ones who remained alive and vocal",
      adversarial_move=E2_MOVE, **{"class":"b"}, grounds=E2_GROUNDS,
      routing={"regen_candidate":{"axis_hit":["s"],"severity":"minor"}},
      status="mapped", provenance={"phase":"R","date":DATE,"seat":SEAT}),
 dict(target_id="just-depressed", target_locus="long",
      target_anchor="two utterances incompatible with a single motive of care",
      adversarial_move=E3_MOVE, **{"class":"b"}, grounds=E3_GROUNDS,
      routing={"regen_candidate":{"axis_hit":["s","r"],"severity":"headline"}},
      status="mapped", provenance={"phase":"R","date":DATE,"seat":SEAT}),
 dict(target_id="just-depressed", target_locus="archetypeVariants.defender",
      target_anchor="pointing at the second sentence and asking which one was sincere",
      adversarial_move=E4_MOVE, **{"class":"a"}, grounds=E4_GROUNDS,
      routing={"answered_by":["just-depressed#long"]},
      status="mapped", provenance={"phase":"R","date":DATE,"seat":SEAT}),
]

print("=== PRE-WRITE ASSERTIONS ===")
for i,e in enumerate(ENTRIES):
    n=N[e["target_id"]]; L=e["target_locus"]; t=v.locus_text(n,L)
    a=e["target_anchor"]; w=v.wc(e["adversarial_move"])
    assert v.locus_valid(n,L), "locus invalid %s#%s"%(e["target_id"],L)
    assert a in t, "ANCHOR NOT VERBATIM: %r not in %s#%s"%(a,e["target_id"],L)
    assert v.wc(a)<=15, "anchor %d words"%v.wc(a)
    lo,hi=(40,60) if e["class"]=="a" else (40,150)
    assert lo<=w<=hi, "move %d words, band %d-%d (class %s)"%(w,lo,hi,e["class"])
    assert all(ord(ch)<128 for ch in e["adversarial_move"]), "non-ascii in move %d"%i
    assert not v.DASH_TOKEN_RE.search(e["adversarial_move"]), "standalone dash in move %d"%i
    assert sorted(e.keys())==sorted(v.ENTRY_KEYS), sorted(e.keys())
    print("  ok  %-22s %-28s anchor %2dw  move %3dw  class %s"%(e["target_id"],L,v.wc(a),w,e["class"]))

vt=sorted((n["id"],v.VARIANT_PREFIX+s) for n in corpus["objections"] for s in v.node_variant_slots(n))
hit=set((e["target_id"],e["target_locus"]) for e in ENTRIES if v.variant_slot(e["target_locus"]))
cc={}
for e in ENTRIES: cc[e["class"]]=cc.get(e["class"],0)+1
doc={"meta":{
  "artifact":"adv_map_phaseR_v0_1.json",
  "phase":"R -- RE-ADJUDICATION of the loci whose text moved in the v4.1.0 cut",
  "state":"MAPPED, PRE-TRIAGE. Lifecycle lives in project_canon, never here.",
  "authored":"2026-09-17, wuld.ink Cowork, K345",
  "source_corpus":"efilist_argument_library_v4_0_0.json",
  "source_corpus_md5":CMD5,
  "source_corpus_objections_md5":ODIG,
  "supersedes":("The three v1_0 entries whose anchors the cut destroyed: happiness-is-choice#long, "
    "just-edgy#long, just-depressed#long. adversarial_map_v1_0.json is NOT edited and NOT re-pinned; "
    "it remains the terminal adjudication of corpus 6ee1f6f31e0f012db0d58cae4f912fcb."),
  "changed_locus_set":("Derived here rather than inherited: 367 loci swept pre-cut against post-cut under "
    "the v0_3 enum, 4 changed. The handoff named three. The fourth, just-depressed#archetypeVariants.defender, "
    "became nameable only once the K345 LOCI ruling extended the enum, so the re-adjudication set is four."),
  "class_counts":cc,
  "coverage_distinct_ids":len(set(e["target_id"] for e in ENTRIES)),
  "variant_coverage":"%d/%d"%(len(hit),len(vt)),
  "not_in_scope":("Phase F (the remaining 38 variant loci) and the sixteen v4.1.0 enrichment items. Two "
    "findings surfaced here are LOGGED, not authored: just-depressed asserts depressive realism at #short "
    "and #medium and repudiates it at #long, and happiness-is-choice#medium still performs the set-point "
    "slide its own repaired #long now warns against."),
  "validator":"adv_map_validator_v0_3.py"},
 "entries":ENTRIES}
out=os.path.join(OUT,"adversarial_map_staging","adv_map_phaseR_v0_1.json")
b=(json.dumps(doc,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
open(out,"wb").write(b)
print("\nWROTE %s\n  bytes %d  md5 %s"%(out,len(b),hashlib.md5(b).hexdigest()))
print("  class_counts %s   variant_coverage %s"%(cc,doc["meta"]["variant_coverage"]))
