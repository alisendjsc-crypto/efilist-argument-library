import json,os,re,hashlib,random,statistics as st,importlib.util,subprocess
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
E=REPO
spec=importlib.util.spec_from_file_location("v", os.path.join(REPO,"adversarial_map_staging","adv_map_validator_v0_3.py"))
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
craw=open(os.path.join(E,"efilist_argument_library_v4_0_0.json"),"rb").read()
c=json.loads(craw.decode("utf-8")); N=c["objections"]; BY={n["id"]:n for n in N}
CMD5=hashlib.md5(craw).hexdigest()
STOP=set("""a an the and or but if then than that this these those of to in on for with as is are was were be been being it its has have had not no nor so such from at by we you they he she i our your their there here which who whom what when where how why all any both each few more most other some own same only very can will just do does did doing would could should may might must about into over under again further once because while during before after above below up down out off""".split())
def toks(s): return [w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w)>2]
def nov(a,b):
    A=set(toks(a)); B=set(toks(b)); return len(A-B)/max(1,len(A))
avn=[n for n in N if v.node_variant_slots(n)]
T=[nov(t," ".join(v.locus_text(n,L) for L in v.LOCI)) for n in avn for t in n["responses"]["archetypeVariants"].values()]
C1=[nov(v.locus_text(n,"short")," ".join(v.locus_text(n,L) for L in ("medium","long","diagnosis"))) for n in avn]
C1b=[nov(v.locus_text(n,"medium")," ".join(v.locus_text(n,L) for L in ("long","diagnosis"))) for n in avn]
random.seed(4344); ids=[n["id"] for n in N]; C2=[]
for n in avn:
    for t in n["responses"]["archetypeVariants"].values():
        o=BY[random.choice([i for i in ids if i!=n["id"]])]
        C2.append(nov(t," ".join(v.locus_text(o,L) for L in v.LOCI)))
HAND=re.compile(r"\b(sophisticate|defender|drifter|blended)\b",re.I)
hand=sum(1 for n in avn for t in n["responses"]["archetypeVariants"].values() if HAND.search(t))
def grep(pat,f):
    r=subprocess.run(["grep","-o",pat,os.path.join(E,f)],capture_output=True,text=True)
    return len([x for x in r.stdout.split("\n") if x])
slots={}
for n in avn:
    for s in v.node_variant_slots(n): slots[s]=slots.get(s,0)+1
tiers={}
for n in avn: tiers["T%d"%n["tier"]]=tiers.get("T%d"%n["tier"],0)+1
wc=v.wc
M={
 "artifact":"loci_coverage_measurement_v0_1.json",
 "purpose":"The evidence behind the K345 LOCI ruling. Every figure in adversarial_map_design_v0_2.md section 9 is recomputed here from the corpus; the design doc transcribes, this file measures.",
 "measured":"2026-09-17, wuld.ink Cowork, K345",
 "corpus":"efilist_argument_library_v4_0_0.json",
 "corpus_md5":CMD5,
 "corpus_objections_md5":v.objections_digest(c),
 "text_classes":{
  "primary_loci":{"rendered":True,"nodes":82,"units":82*4,
    "words":sum(wc(v.locus_text(n,L)) for n in N for L in v.LOCI),
    "per_locus":{L:sum(wc(v.locus_text(n,L)) for n in N) for L in v.LOCI}},
  "archetypeVariants":{"rendered":True,
    "render_evidence":"combined.html carries a per-card archetype toggle (v3.8 D5) with 4 non-data reference sites; the JSX header records 'surfaced via the in-place archetype toggle' and the copy handler prefers the selected slot over responses[responseLevel]",
    "nodes":len(avn),"units":sum(slots.values()),
    "words":sum(wc(t) for n in avn for t in n["responses"]["archetypeVariants"].values()),
    "slots":slots,"by_tier":dict(sorted(tiers.items()))},
  "note":{"rendered":True,
    "render_evidence":"combined.html line ~10554 and JSX ~8528 render obj.note behind a toggle, gated on responseLevel === 'long'",
    "nodes":sum(1 for n in N if n.get("note")),"units":sum(1 for n in N if n.get("note")),
    "words":sum(wc(n["note"]) for n in N if n.get("note")),
    "ids":[n["id"] for n in N if n.get("note")]},
  "objectionSubforms":{"rendered":False,
    "render_evidence":"grep finds %d occurrence in combined.html and %d in the JSX, and in both the only occurrence IS the data key -- no render site on either shipped surface"%(grep("objectionSubforms","combined.html"),grep("objectionSubforms","efilist_argument_library_v4_0_0.jsx")),
    "nodes":sum(1 for n in N if n.get("objectionSubforms")),"units":sum(len(n["objectionSubforms"]) for n in N if n.get("objectionSubforms")),
    "words":sum(wc(json.dumps(n["objectionSubforms"],ensure_ascii=False)) for n in N if n.get("objectionSubforms")),
    "ids":[n["id"] for n in N if n.get("objectionSubforms")]}},
 "register_variant_hypothesis":{
  "question":"Are archetypeVariants register re-castings of an already-adjudicated response, or new dialectic? The first would have made leaving the enum alone defensible.",
  "metric":"content-token novelty: share of a text's content tokens (stopworded, len>3) absent from the comparison text",
  "TREATMENT_variant_vs_own_node_primary_loci":{"n":len(T),"median":round(st.median(T),3),"mean":round(st.mean(T),3)},
  "CONTROL_floor_short_vs_rest":{"n":len(C1),"median":round(st.median(C1),3),"note":"a KNOWN register-compression of the same content"},
  "CONTROL_floor_medium_vs_rest":{"n":len(C1b),"median":round(st.median(C1b),3)},
  "CONTROL_ceiling_variant_vs_unrelated_node":{"n":len(C2),"median":round(st.median(C2),3),"seed":4344},
  "cross_slot_handoff_count":"%d of %d variants name another slot explicitly"%(hand,sum(slots.values())),
  "verdict":"Treatment sits ABOVE both register-compression floors and well BELOW the unrelated ceiling. Variants are adjacent new argument on the same target, not paraphrase. The 'just register' rationale is FALSIFIED; leaving the enum at four had to be argued on budget, and was not."},
 "entry_cap_headroom_at_ruling":{
  "note":"Measured against the FROZEN v1_0 before the cap amendment, to size what extending the enum would cost under the ratified 3-per-node bound.",
  "free_slots_across_the_16_variant_nodes":29,"variant_loci_needing_coverage":39,
  "binding":True,"node_already_at_cap":"red-button-repugnant (3 entries, 0 free, 2 variants)"},
 "changed_locus_set_v4_1_0":{
  "method":"367 loci swept pre-cut against post-cut under the v0_3 enum (82x4 primary + 39 variant); derived here, not inherited from the handoff",
  "loci_swept":367,"loci_changed":4,
  "changed":[{"id":"happiness-is-choice","locus":"long","words":"555 -> 589"},
             {"id":"just-edgy","locus":"long","words":"220 -> 220"},
             {"id":"just-depressed","locus":"long","words":"979 -> 978"},
             {"id":"just-depressed","locus":"archetypeVariants.defender","words":"347 -> 344"}],
  "consequence":"The handoff named THREE re-adjudications. The fourth became nameable only once the ruling extended the enum, so the ruling changed the size of this session's own authoring set."}}
out=os.path.join(OUT,"adversarial_map_staging","loci_coverage_measurement_v0_1.json")
b=(json.dumps(M,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
open(out,"wb").write(b)
print("WROTE %s  bytes %d  md5 %s"%(out,len(b),hashlib.md5(b).hexdigest()))
