import json,os,copy,importlib.util,tempfile,hashlib
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
E=REPO
spec=importlib.util.spec_from_file_location("v", os.path.join(REPO,"adversarial_map_staging","adv_map_validator_v0_3.py"))
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
POST=os.path.join(E,"efilist_argument_library_v4_0_0.json")
import subprocess
# the pre-cut corpus is recovered from the git blob and kept in a TEMP dir --
# never written into the repo, whose root is publicly served at library.wuld.ink/*
PRE=os.path.join(tempfile.mkdtemp(prefix="k345_precut_"),"corpus_precut.json")
_blob=subprocess.run(["git","-C",REPO,"show","3e71546316285ef4fe3bd6d2da4ef1b5e4d6b50f:efilist_argument_library_v4_0_0.json"],capture_output=True)
assert _blob.returncode==0 and _blob.stdout, "could not recover the pre-cut corpus blob"
open(PRE,"wb").write(_blob.stdout)
SRC=os.path.join(REPO,"adversarial_map_staging","adv_map_phaseR_v0_1.json")
base=json.load(open(SRC,encoding="utf-8"))
tmp=tempfile.mkdtemp(prefix="k345ctl_")
def run(doc,corpus):
    p=os.path.join(tmp,"m%d.json"%abs(hash(json.dumps(doc,sort_keys=True)))) 
    open(p,"wb").write((json.dumps(doc,indent=2,ensure_ascii=False)+"\n").encode("utf-8"))
    return v.validate([p],corpus,out=lambda s:None)
res=[]
def ctl(name,doc,corpus,expect):
    ok,viol,adv=run(doc,corpus)
    pool=viol+adv
    if expect is None:
        good=ok and not adv; detail="clean" if good else pool[:3]
    else:
        good=(not ok) and any(x.startswith(expect+":") for x in pool)
        detail="tripped %s"%expect if good else pool[:3]
    res.append((name,good)); print("%s . %-34s -> %s"%("PASS" if good else "FAIL",name,detail))

ctl("positive-control-as-shipped",base,POST,None)
d=copy.deepcopy(base); d["entries"][0]["target_anchor"]="the environmental share is itself largely unchosed"
ctl("anchor-one-char-corrupted",d,POST,"anchor-rule")
d=copy.deepcopy(base); d["entries"][3]["target_locus"]="archetypeVariants.drifter"
ctl("variant-slot-absent-on-node",d,POST,"target-locus")
d=copy.deepcopy(base); d["entries"][3]["class"]="b"
ctl("class-flipped-routing-stale",d,POST,"routing-shape")
d=copy.deepcopy(base); d["meta"]["variant_coverage"]="2/39"
ctl("variant-coverage-overstated",d,POST,"variant-coverage")
d=copy.deepcopy(base); d["meta"]["class_counts"]={"b":4}
ctl("class-counts-misdeclared",d,POST,"meta-summaries")
d=copy.deepcopy(base); d["entries"][2]["target_anchor"]=d["entries"][2]["target_anchor"]+" x"
ctl("anchor-extended-past-text",d,POST,"anchor-rule")
d=copy.deepcopy(base); d["entries"][0]["provenance"]["phase"]="Z"
ctl("phase-outside-enum",d,POST,"provenance")
d=copy.deepcopy(base); d["entries"][3]["routing"]={"answered_by":["just-depressed#archetypeVariants.drifter"]}
ctl("answered-by-absent-variant",d,POST,"routing-shape")

print("\n=== ANCHOR PROVENANCE CONTROL: the fragment against the PRE-CUT corpus ===")
ok,viol,adv=run(base,PRE)
for x in viol: print("   "+x[:150])
import re
anch=[x for x in viol if x.startswith("anchor-rule")]
print("   anchors that FAIL pre-cut: %d of 4  (these sit in text the cut MOVED)"%len(anch))
print("   anchors that HOLD pre-cut: %d of 4  (these sit in text the cut did NOT touch)"%(4-len(anch)))
print("\n%d/%d controls behaved"%(sum(1 for _,g in res if g),len(res)))
