import sys
import json, collections, random, importlib.util, hashlib, difflib, sys, subprocess, tempfile
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else _HERE
S=REPO
spec=importlib.util.spec_from_file_location("v3", os.path.join(_HERE,"adv_map_validator_v0_3.py"))
v3=importlib.util.module_from_spec(spec); spec.loader.exec_module(v3)

post=json.load(open(S+"/efilist_argument_library_v4_0_0.json",encoding="utf-8"))
_pd=tempfile.mkdtemp(prefix="k346_precut_")
PRE=os.path.join(_pd,"corpus_precut.json")
_b=subprocess.run(["git","-C",REPO,"show","3e71546316285ef4fe3bd6d2da4ef1b5e4d6b50f:efilist_argument_library_v4_0_0.json"],capture_output=True)
assert _b.returncode==0 and _b.stdout, "could not recover the pre-cut corpus blob"
open(PRE,"wb").write(_b.stdout)
pre =json.load(open(PRE,encoding="utf-8"))
MAP =json.load(open(S+"/adversarial_map_staging/adversarial_map_v1_0.json",encoding="utf-8"))
PR  =json.load(open(S+"/adversarial_map_staging/adv_map_phaseR_v0_1.json",encoding="utf-8"))
prenodes={o["id"]:o for o in pre["objections"]}
postnodes={o["id"]:o for o in post["objections"]}
E=MAP["entries"]
R={}

# ---------- A1 per-phase class mix ----------
byphase=collections.defaultdict(collections.Counter)
for e in E: byphase[e["provenance"]["phase"]][e["class"]]+=1
for e in PR["entries"]: byphase["R"][e["class"]]+=1
R["A1_per_phase_class"]={p:dict(cnt) for p,cnt in sorted(byphase.items())}
tot=collections.Counter(e["class"] for e in E)
R["A1_v1_0_class_total"]=dict(tot)
R["A1_v1_0_b_share"]=round(tot["b"]/len(E),4)
R["A1_R_b_share"]=round(sum(1 for e in PR["entries"] if e["class"]=="b")/len(PR["entries"]),4)

# ---------- A2 entries per node, class mix by node multiplicity ----------
pernode=collections.Counter(e["target_id"] for e in E)
R["A2_entries_per_node_dist"]=dict(sorted(collections.Counter(pernode.values()).items()))
R["A2_entries_per_node_mean"]=round(len(E)/len(pernode),4)
single={i for i,n in pernode.items() if n==1}
multi ={i for i,n in pernode.items() if n>1}
cs=collections.Counter(e["class"] for e in E if e["target_id"] in single)
cm=collections.Counter(e["class"] for e in E if e["target_id"] in multi)
R["A2_class_in_single_entry_nodes"]=dict(cs); R["A2_class_in_multi_entry_nodes"]=dict(cm)
R["A2_b_share_single"]=round(cs["b"]/max(1,sum(cs.values())),4)
R["A2_b_share_multi"] =round(cm["b"]/max(1,sum(cm.values())),4)
# permutation null: shuffle class labels across entries, recompute b-share gap. SORTED pool (ccclxvii).
obs=R["A2_b_share_multi"]-R["A2_b_share_single"]
labels=sorted(e["class"] for e in E)
ids=sorted(e["target_id"] for e in E)
memb=[1 if i in multi else 0 for i in ids]
rng=random.Random(20260917); hits=0; N=20000
nm=sum(memb); ns=len(memb)-nm
for _ in range(N):
    L=labels[:]; rng.shuffle(L)
    bm=sum(1 for l,m in zip(L,memb) if m and l=="b")
    bs=sum(1 for l,m in zip(L,memb) if not m and l=="b")
    if (bm/nm - bs/ns) >= obs: hits+=1
R["A2_perm_null_p_b_enriched_in_multi"]=round(hits/N,4)
R["A2_perm_N"]=N

# ---------- A3 move word counts by class ----------
wcb=collections.defaultdict(list)
for e in E: wcb[e["class"]].append(len(e["adversarial_move"].split()))
R["A3_move_words_median_by_class"]={k:sorted(v)[len(v)//2] for k,v in sorted(wcb.items())}
R["A3_move_words_n_by_class"]={k:len(v) for k,v in sorted(wcb.items())}

# ---------- A4 anchor locus distribution ----------
R["A4_locus_dist"]=dict(collections.Counter(e["target_locus"] for e in E))

# ---------- A5 THE NULL FOR THE PHASE R ANCHOR CLAIM ----------
# which loci changed pre->post, and how many words changed within each
changed={}
for nid,pn in prenodes.items():
    qn=postnodes.get(nid)
    if not qn: continue
    for loc in v3.LOCI+tuple(v3.VARIANT_PREFIX+s for s in v3.VARIANT_SLOTS):
        if not (v3.locus_valid(pn,loc) or v3.locus_valid(qn,loc)): continue
        a=v3.locus_text(pn,loc); b=v3.locus_text(qn,loc)
        if a!=b:
            aw=a.split(); bw=b.split()
            sm=difflib.SequenceMatcher(None,aw,bw,autojunk=False)
            same=sum(bl.size for bl in sm.get_matching_blocks())
            changed[f"{nid}#{loc}"]=dict(pre_words=len(aw),post_words=len(bw),
                                         unchanged_words=same,changed_words_post=len(bw)-same)
R["A5_changed_loci"]=changed
R["A5_changed_loci_count"]=len(changed)

rows=[]
for e in PR["entries"]:
    key=f'{e["target_id"]}#{e["target_locus"]}'
    node=postnodes[e["target_id"]]
    txt=v3.locus_text(node,e["target_locus"])
    tw=len(txt.split())
    ch=changed.get(key)
    chw=ch["changed_words_post"] if ch else 0
    anchor=e["target_anchor"]
    inch=False
    if ch:
        # is the anchor inside a region the cut altered? compare against the PRE text
        pretxt=v3.locus_text(prenodes[e["target_id"]],e["target_locus"]) if v3.locus_valid(prenodes[e["target_id"]],e["target_locus"]) else ""
        inch = (anchor in txt) and (anchor not in pretxt)
    rows.append(dict(locus=key,locus_words=tw,changed_words=chw,
                     changed_fraction=round(chw/tw,4) if tw else None,
                     anchor_in_changed_text=inch))
R["A5_phaseR_entries"]=rows
exp=sum(r["changed_fraction"] or 0 for r in rows)
R["A5_expected_anchors_in_changed_text_under_uniform"]=round(exp,4)
R["A5_observed_anchors_in_changed_text"]=sum(1 for r in rows if r["anchor_in_changed_text"])
R["A5_n_phaseR_entries"]=len(rows)
json.dump(R,open(os.path.join(OUT,"measure_ccclxv_v0_1.json"),"w"),indent=1)
for k,v in R.items():
    if k in ("A5_changed_loci","A5_phaseR_entries"): continue
    print(f"{k} = {v}")
print("\nA5_changed_loci:"); [print("  ",k,v) for k,v in changed.items()]
print("\nA5_phaseR_entries:"); [print("  ",r) for r in rows]
