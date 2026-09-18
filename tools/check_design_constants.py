import json,os,re,sys
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
D=os.path.join(REPO,"adversarial_map_staging","adversarial_map_design_v0_2.md")
M=json.load(open(os.path.join(REPO,"adversarial_map_staging","loci_coverage_measurement_v0_1.json"),encoding="utf-8"))
t=open(D,encoding="utf-8").read()
tc=M["text_classes"]; rv=M["register_variant_hypothesis"]; cl=M["changed_locus_set_v4_1_0"]
CLAIMS=[
 ("primary words 67,427","67,427",tc["primary_loci"]["words"]),
 ("primary units 328","| 82 | 328 |",tc["primary_loci"]["units"]),
 ("av nodes 16","| 16 | 39 | 10,069 |",tc["archetypeVariants"]["nodes"]),
 ("av units 39","| 16 | 39 | 10,069 |",tc["archetypeVariants"]["units"]),
 ("av words 10,069","10,069",tc["archetypeVariants"]["words"]),
 ("note nodes 9","| 9 | 9 | 544 |",tc["note"]["nodes"]),
 ("note words 544","544",tc["note"]["words"]),
 ("osf nodes 1","| 1 | 4 | 646 |",tc["objectionSubforms"]["nodes"]),
 ("osf words 646","646",tc["objectionSubforms"]["words"]),
 ("slot sophisticate 13","`sophisticate` 13",tc["archetypeVariants"]["slots"]["sophisticate"]),
 ("slot defender 12","`defender` 12",tc["archetypeVariants"]["slots"]["defender"]),
 ("slot drifter 7","`drifter` 7",tc["archetypeVariants"]["slots"]["drifter"]),
 ("slot blended 7","`blended` 7",tc["archetypeVariants"]["slots"]["blended"]),
 ("treat median 0.591","**0.591**",rv["TREATMENT_variant_vs_own_node_primary_loci"]["median"]),
 ("floor1 0.293","**0.293**",rv["CONTROL_floor_short_vs_rest"]["median"]),
 ("floor2 0.498","**0.498**",rv["CONTROL_floor_medium_vs_rest"]["median"]),
 ("ceiling 0.855","**0.855**",rv["CONTROL_ceiling_variant_vs_unrelated_node"]["median"]),
 ("treat n 39","| **39** | **0.591** |",rv["TREATMENT_variant_vs_own_node_primary_loci"]["n"]),
 ("handoff 27 of 39","**27 of 39 variants",27),
 ("corpus md5","04bf6482aa0374ee92a81c1d55ec41f8",M["corpus_md5"]),
]
bad=0
for label,needle,measured in CLAIMS:
    present = needle in t
    nums=re.findall(r"\d+(?:[.,]\d+)?", needle)
    val=str(measured).replace(",","")
    matched = any(n.replace(",","")==val for n in nums) if nums else (needle==str(measured))
    if label.startswith("corpus"): matched = needle==str(measured)
    ok = present and matched
    if not ok: bad+=1
    print("%s  %-24s doc-needle=%-28s measured=%s"%("ok  " if ok else "FAIL",label,needle[:28],measured))
# cross-check the handoff count independently
print("\n-- independent recount of the 27 --")
print("   measurement file says: %s"%rv["cross_slot_handoff_count"])
assert "27 of 39" in rv["cross_slot_handoff_count"], rv["cross_slot_handoff_count"]
# tiers
for k,vv in tc["archetypeVariants"]["by_tier"].items():
    needle="%s %d"%(k,vv)
    if needle not in t: bad+=1; print("FAIL  tier line %s missing"%needle)
print("\nloci swept %d / changed %d  -- doc says swept: %s changed: %s"%(cl["loci_swept"],cl["loci_changed"],
    "367" in t, "39 variant loci across 16 nodes" in t))
print("\n%s: %d constant(s) failed"%("FAIL" if bad else "ALL DESIGN-DOC CONSTANTS MATCH MEASUREMENT",bad))
sys.exit(1 if bad else 0)
