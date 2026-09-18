import sys
import json, collections, random
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else _HERE
S=REPO
c=json.load(open(S+"/efilist_argument_library_v4_0_0.json",encoding="utf-8"))
rwe=c["realWorldExamples"]
R={"n_instances":len(rwe)}
sig=collections.Counter(e.get("archetype_signal_observed") for e in rwe)
R["raw_signal_counter"]={str(k):v for k,v in sig.most_common()}
SLOTS=("sophisticate","defender","drifter","blended")
app=[e for e in rwe if e.get("archetype_signal_observed") in SLOTS]
R["n_applicable"]=len(app)
R["applicable_mix"]=dict(collections.Counter(e["archetype_signal_observed"] for e in app))
R["canon_claim"]={"sophisticate":72,"defender":15,"drifter":6,"blended":5,"n":98}
R["reproduces_canon"]= (R["applicable_mix"]==R["canon_claim"] or
    (R["n_applicable"]==98 and all(R["applicable_mix"].get(k)==v for k,v in R["canon_claim"].items() if k!="n")))
# venue / register cross-tabs
# engagement_context is free text with cardinality ~= n; cross-tabbing it produces noise, not a table
for field in ("source_register","speaker_type","public_reach","instance_polarity"):
    tab=collections.defaultdict(collections.Counter)
    for e in app: tab[str(e.get(field))][e["archetype_signal_observed"]]+=1
    R["xtab_"+field]={k:{"n":sum(v.values()),"soph_share":round(v["sophisticate"]/sum(v.values()),3),**dict(v)}
                      for k,v in sorted(tab.items(), key=lambda kv:-sum(kv[1].values()))}
# how concentrated is the frame? distinct publications, top ones
pub=collections.Counter(str(e.get("source_publication")) for e in app)
R["n_distinct_publications"]=len(pub)
R["top_publications"]=dict(pub.most_common(10))
# per-publication soph share, then: how much of the 72 comes from the top venues
byp=collections.defaultdict(collections.Counter)
for e in app: byp[str(e.get("source_publication"))][e["archetype_signal_observed"]]+=1
top=[p for p,_ in pub.most_common(5)]
R["soph_in_top5_pubs"]=sum(byp[p]["sophisticate"] for p in top)
R["n_in_top5_pubs"]=sum(sum(byp[p].values()) for p in top)
R["soph_outside_top5"]=sum(v["sophisticate"] for p,v in byp.items() if p not in top)
R["n_outside_top5"]=sum(sum(v.values()) for p,v in byp.items() if p not in top)
# permutation null: is sophisticate share heterogeneous across register? (sorted pools; ccclxvii)
regs=sorted({str(e.get("source_register")) for e in app})
obs_tab=[(r,sum(1 for e in app if str(e.get("source_register"))==r),
            sum(1 for e in app if str(e.get("source_register"))==r and e["archetype_signal_observed"]=="sophisticate"))
         for r in regs]
def chi(tab,p):
    s=0.0
    for _,n,k in tab:
        if n==0: continue
        exp=n*p
        if exp>0: s+=(k-exp)**2/exp
        if n-exp>0: s+=((n-k)-(n-exp))**2/(n-exp)
    return s
p0=sum(1 for e in app if e["archetype_signal_observed"]=="sophisticate")/len(app)
obs_chi=chi(obs_tab,p0)
labels=sorted(1 if e["archetype_signal_observed"]=="sophisticate" else 0 for e in app)
memb=[str(e.get("source_register")) for e in sorted(app,key=lambda e:(str(e.get("source_register")),str(e.get("instance_id"))))]
rng=random.Random(20260917); N=20000; hits=0
for _ in range(N):
    L=labels[:]; rng.shuffle(L)
    t=collections.defaultdict(lambda:[0,0])
    for m,l in zip(memb,L):
        t[m][0]+=1; t[m][1]+=l
    if chi([(k,v[0],v[1]) for k,v in t.items()],p0)>=obs_chi: hits+=1
R["register_heterogeneity_obs_chi"]=round(obs_chi,4)
R["register_heterogeneity_perm_p"]=round(hits/N,4)
R["overall_soph_share"]=round(p0,4)
json.dump(R,open(os.path.join(OUT,"measure_archetype_v0_1.json"),"w"),indent=1)
for k,v in R.items():
    if k.startswith("xtab_"): print(f"--- {k} ---"); [print("   ",kk,vv) for kk,vv in v.items()]
    else: print(f"{k} = {v}")
