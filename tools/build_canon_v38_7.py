"""K345b: canon v38.6 -> v38.7 MINOR. Records the RWE layer's stated PURPOSE (Josiah) and the
MAP1 calibration, which found no defensible signal and says so.
Run: python tools/build_canon_v38_7.py [--out <dir>]"""
import sys, os, json, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_6.json")
raw = open(SRC, "rb").read()
assert hashlib.md5(raw).hexdigest() == "4ed80249e07b6a3d292948a0b01a06f2", "BASE GUARD FAIL"
c = json.loads(raw.decode("utf-8"))
FROZEN = {k: json.dumps(c[k], sort_keys=True, ensure_ascii=False) for k in ("invariants", "schemas", "hazard_map")}
KEYS = list(c.keys())
CAL = json.load(open(os.path.join(REPO, "adversarial_map_staging", "rwe_map1_calibration_v0_1.json"), encoding="utf-8"))
calmd5 = hashlib.md5(open(os.path.join(REPO, "adversarial_map_staging", "rwe_map1_calibration_v0_1.json"), "rb").read()).hexdigest()
T = CAL["tests"]
assert CAL["map1"]["edges"] == c["invariants"]["map1_edge_count_total"], "calibration parse disagrees with canon invariants"
assert CAL["map1"]["sources"] == c["invariants"]["map1_node_count"], "calibration parse disagrees with canon invariants"

c["adversarial_map"]["rwe_layer_purpose_and_map1_calibration_K345b"] = {
 "why_the_RWE_panel_EXISTS": (
  "JOSIAH, K345b, recorded because a layer whose purpose is not written down gets optimised into "
  "something else. The realWorldExamples panel exists FIRST so that no one can claim the library is a "
  "straw man -- every objection the corpus rebuts can be shown deployed by a real person in a real "
  "setting, with an archive URL behind it. SECOND, it exists simply to catalogue the scope and depth of "
  "the subject itself. Those two purposes are served by instance COUNT and BREADTH and are already being "
  "served at 136 instances over 78 of 82 nodes. Prediction is a THIRD and later aim, and it is served by "
  "a different property of the same panel -- see the collection note below, because the two can diverge."),
 "the_long_aim_in_his_framing": (
  "Eventually the RWE panel should aid real-world reaction research and outcome prediction. There is a "
  "foothold already; it will not be robust until many more iterations and findings; it is still worth "
  "aiming for. Start small, aim big. This block is the small start: an instrument and a target, not a "
  "finding."),
 "calibration_artifact": {"file": "adversarial_map_staging/rwe_map1_calibration_v0_1.json", "md5": calmd5,
   "generator": "adversarial_map_staging/rwe_map1_calibration_v0_1.py"},
 "THE_CONTROL_K345_OWED_AND_DID_NOT_RUN": (
  "K345a published '23 of 53 observed transitions are edges MAP1 contains' with no chance baseline. "
  "MAP1 is DENSE: pooled out-degree averages %.1f of 78 possible targets, so %.1f%% of all ordered "
  "(source,target) pairs are edges and a randomly drawn pair hits often. Against a shuffled-target "
  "baseline the observed rate is %.1f%% versus a chance mean of %.1f%%. The raw count was never evidence "
  "of predictive skill and should not have been published without this." % (
   CAL["map1"]["pooled_outdegree_mean"], 100 * CAL["map1"]["pooled_edge_density"],
   100 * T["crossed_pooled"]["rate"], 100 * T["crossed_pooled"]["chance_mean"])),
 "THE_CONFOUND_THAT_DECIDES_IT": (
  "attached_objections is many-to-many, so crossing consecutive instances inflates n with units that are "
  "NOT independent: two nodes attached to one instance are frequently premise-siblings, and MAP1 is BUILT "
  "from premise overlap, so the cross-product manufactures hits for a reason that has nothing to do with "
  "conversational dynamics. Crossed mode reaches p=%.4f pooled and p=%.4f archetype-conditioned. STRICT "
  "mode -- only instances carrying exactly ONE attached objection, which is the clean test -- collapses to "
  "n=%d and lands at p=%.4f and p=%.4f. THE APPARENT SIGNAL LIVES ENTIRELY IN THE CROSS-PRODUCT. There is "
  "NO DEFENSIBLE SIGNAL YET, and this is stated rather than softened." % (
   T["crossed_pooled"]["p_permutation"], T["crossed_archetype_conditioned"]["p_permutation"],
   T["STRICT_pooled"]["n"], T["STRICT_pooled"]["p_permutation"], T["STRICT_archetype_conditioned"]["p_permutation"])),
 "WHAT_IT_WOULD_TAKE_a_target_rather_than_an_aspiration": (
  "Power against a 10-point effect over the measured baseline: %.0f%% at n=53, %.0f%% at n=100, %.0f%% at "
  "n=200, %.0f%% at n=400. So roughly n=200 clean units. TODAY'S CLEAN COUNT IS %d, out of 136 instances. "
  "THE BINDING CONSTRAINT IS NOT THE NUMBER OF INSTANCES. It is how many are THREADED, SEQUENTIALLY "
  "NUMBERED and SINGLE-ATTACHMENT. Collecting more one-off instances serves the panel's first two purposes "
  "and moves this test almost not at all -- which is exactly why the purposes had to be written down first." % (
   100 * CAL["power_to_detect_a_10pt_effect"]["53"], 100 * CAL["power_to_detect_a_10pt_effect"]["100"],
   100 * CAL["power_to_detect_a_10pt_effect"]["200"], 100 * CAL["power_to_detect_a_10pt_effect"]["400"],
   T["STRICT_pooled"]["n"])),
 "instrument_controls": (
  "The calibration's parse of MAP1 was cross-checked against canon's own stored invariants and agrees "
  "exactly: %d source nodes and %d edges, asserted by the builder rather than eyeballed. And a determinism "
  "control caught a real defect before the artifact shipped: the permutation test drew candidates from a "
  "SET comprehension, whose iteration order for strings varies between processes with PYTHONHASHSEED, so a "
  "seeded test was not reproducible. Candidates are now sorted once per source; the artifact reproduces "
  "byte-identically across repeated runs and under two forced hash seeds." % (
   CAL["map1"]["sources"], CAL["map1"]["edges"])),
 "not_ruled_here": (
  "Whether MAP1's analytic weights are right. The instrument cannot say at this n and says so in its own "
  "output. Nothing here licenses re-weighting an edge, and no corpus, flagship or map byte was touched.")}

oq = c["open_questions"]["active"]["CORPUS_IS_REACTIVE_ONLY_K345"]
c["open_questions"]["active"]["CORPUS_IS_REACTIVE_ONLY_K345"] = oq + (
 " READ WITH adversarial_map.rwe_layer_purpose_and_map1_calibration_K345b (K345b): the '23 of 53' figure "
 "above was published WITHOUT a chance baseline, and against one it is not distinguishable from chance on "
 "the clean test. The feasibility claim stands -- the join is computable today -- but nothing about "
 "predictive skill does.")

c["canon_version"] = "38.7"; c["canon_version_marker"] = "v38.7"
c["last_updated"] = "2026-09-17"; c["last_updated_by_session"] = "K345b_rwe_map1_calibration"
c["keyset_delta_ledger"]["v38_7_note"] = (
 "v38.6 -> v38.7 MINOR (K345b_rwe_map1_calibration, 2026-09-17): keyset UNCHANGED at 41; one addition "
 "INSIDE adversarial_map (rwe_layer_purpose_and_map1_calibration_K345b) and one appended pointer sentence "
 "on open_questions.active.CORPUS_IS_REACTIVE_ONLY_K345. invariants, schemas and hazard_map asserted "
 "byte-identical, and the calibration's independent parse of MAP1 was asserted equal to invariants' stored "
 "map1_node_count and map1_edge_count_total. NO PIN; no corpus, JSX, flagship or map byte touched.")
c["session_log_recent"].append(
 "K345b_rwe_map1_calibration (2026-09-17, wuld.ink Cowork; NO PIN) [MINOR v38.6->v38.7]: THE CONTROL K345a "
 "OWED, AND IT TOOK THE CLAIM BACK. '23 of 53 observed transitions are MAP1 edges' was published without a "
 "chance baseline; MAP1 is dense at 21.6% pooled edge density, so against a shuffled-target null the "
 "observed 45.5% sits on a chance mean of 33.7%. Worse for the claim, the apparent significance lives "
 "entirely in the many-to-many cross-product, whose units are not independent because co-attached nodes are "
 "often premise-siblings and MAP1 is built from premise overlap: the clean single-attachment test is n=17 "
 "at p=0.37. NO DEFENSIBLE SIGNAL, stated plainly. What shipped instead is an instrument and a target -- "
 "power says ~n=200 clean units, today's clean count is 17, and the binding constraint is not instance "
 "COUNT but how many instances are threaded, sequentially numbered and single-attachment. Josiah's stated "
 "purposes for the RWE panel are recorded alongside it precisely because those purposes and the prediction "
 "aim pull on different properties of the same panel. A determinism control caught the permutation test "
 "drawing from a set comprehension under PYTHONHASHSEED, making a seeded test irreproducible; fixed and "
 "verified under two forced seeds.")
c["next_recommended_session"]["also_read_first"] = c["next_recommended_session"]["also_read_first"] + (
 " AND adversarial_map.rwe_layer_purpose_and_map1_calibration_K345b, which supplies the RWE growth spec: "
 "threaded, sequentially numbered, single-attachment instances are what the prediction aim needs, and "
 "one-off instances are not. That is a collection instruction, not a finding.")

assert list(c.keys()) == KEYS, "KEYSET MOVED"
for k, before in FROZEN.items():
    assert json.dumps(c[k], sort_keys=True, ensure_ascii=False) == before, "MAJOR-CLASS EDIT to %s" % k
dest = os.path.join(OUT, "project_canon_v38_7.json")
b = (json.dumps(c, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
open(dest, "wb").write(b)
print("WROTE %s\n  bytes %d  md5 %s" % (dest, len(b), hashlib.md5(b).hexdigest()))
print("  keyset %d unchanged; invariants/schemas/hazard_map byte-identical; MAP1 parse == canon invariants" % len(c))
