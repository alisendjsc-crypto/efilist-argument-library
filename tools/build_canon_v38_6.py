"""K345a: canon v38.5 -> v38.6 MINOR. Sole mutation: correct the K345 open question
about the corpus being reactive-only. Josiah corrected its scope in the same session;
the entry as committed asserted an absence that a sweep of the corpus falsifies.
Run: python tools/build_canon_v38_6.py [--out <dir>]"""
import sys, os, json, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_5.json")
raw = open(SRC, "rb").read()
assert hashlib.md5(raw).hexdigest() == "459dc784df35d5c1c9d4a45ad731952c", "BASE GUARD FAIL"
c = json.loads(raw.decode("utf-8"))
FROZEN = {k: json.dumps(c[k], sort_keys=True, ensure_ascii=False) for k in ("invariants", "schemas", "hazard_map")}
KEYS = list(c.keys())
OLDKEY = "CORPUS_IS_REACTIVE_ONLY_K345"
assert OLDKEY in c["open_questions"]["active"], "the K345 entry being corrected is not present"

c["open_questions"]["active"][OLDKEY] = (
 "RAISED BY JOSIAH K345, AND ITS SCOPE CORRECTED BY HIM THE SAME SESSION. This entry replaces the K345 "
 "text, which was wrong in one half and is named here as a correction rather than quietly restamped. "
 "WHAT STANDS: the library is objection-first. Each of the 82 nodes is indexed by an objection AGAINST "
 "antinatalism / NU / efilism and the corpus's content is the reaction to it, so 'reactive' is accurate "
 "to a degree and is a structural fact, not a defect -- objection then rebuttal, rather than argument "
 "then objection. GAP 1, UNCHANGED AND STILL OPEN: there is no catalogue of the positive arguments FOR "
 "those positions as objects in their own right. The asymmetry, the consent / foreseeable-imposition "
 "argument, the risk-imposition argument and the rest appear only as material cited inside rebuttals; "
 "nothing individuates them the way objections-index.json individuates objections. Josiah's framing: this "
 "would be a SCHOLARLY endeavour, and it is noted for documentation and possibly its own implementation "
 "later, not scoped now. "
 "GAP 2 AS WRITTEN AT K345 WAS FALSE AND IS WITHDRAWN. It claimed nothing collects how these exchanges "
 "run in the wild. The corpus's own realWorldExamples layer does exactly that and the claim was made "
 "without sweeping for it -- 136 instances attached across 78 of the 82 nodes, on a scholarly schema "
 "(source_url, archive_url, byline, publication, attestation status, corpus_decay_risk, <=15-word quote, "
 "rhetorical_move_observed, archetype_signal_observed, thread_id), drawn from podcasts, lectures, "
 "long-form dialogues, essays, forum threads and private exchanges. Josiah's stated position is that "
 "sweeping every Twitter thread, Reddit post, YouTube comment and Facebook post is NOT wanted; what might "
 "be worth doing later is statistics and data mining as an input to the argument flow's PREDICTION system. "
 "GAP 2 RESTATED, NARROWER AND MEASURED: MAP1_TRANSITIONS carries 2,886 edges over 78 source nodes and 4 "
 "archetype branches, and every edge is scored analytically -- raw_score, weight, shared_strong, "
 "shared_any, pivot_premises, all derived from premise overlap and tier distance. A regex sweep of every "
 "edge field for an observed / empirical / frequency term returns NONE, and source_meta's "
 "disengagement_probability (LOW 10, MEDIUM 61, HIGH 7) is likewise categorical with no stated basis. "
 "THE PREDICTOR HAS NEVER BEEN JOINED TO THE OBSERVATIONS, and that join is what Josiah means. "
 "FEASIBILITY, MEASURED NOT GUESSED: the observations needed already exist. 15 threads, 11 with more than "
 "one instance, 51 instances inside them, and all 11 carry numbered instance_ids so their order is "
 "recoverable without assuming array order. That yields 57 ordered node-to-node pairs, 53 distinct, of "
 "which 23 are edges MAP1 already contains under the MOST GENEROUS test (archetype-pooled). "
 "DO NOT READ THE OTHER 30 AS MAP GAPS. attached_objections is many-to-many, so consecutive instances are "
 "crossed rather than paired, and the RWE layer records notable instances rather than every turn, so an "
 "observed A->B may be A->unrecorded->B. Distinguishing real gaps from those two artifacts IS the "
 "calibration work; 23 of 53 is the statement that a first join is tractable today, not a verdict on the "
 "map. "
 "A SIGNAL ALREADY SITTING UNUSED, AND IT BEARS ON PHASE F: observed archetype_signal_observed runs "
 "sophisticate 72, defender 15, drifter 6, blended 5 over the 98 applicable instances (38 not-applicable), "
 "so roughly three deployments in four read as sophisticate. The AUTHORED variant distribution is close to "
 "even -- sophisticate 13, defender 12, drifter 7, blended 7. Phase F plans 39 variant loci across four "
 "slots; if effort should track observed deployment rather than existing authorship, that is a design "
 "input available now and it has never been consulted. "
 "AND ONE COINCIDENCE WORTH ONE QUERY BEFORE EITHER LAYER IS EXTENDED: the four nodes with no real-world "
 "instance and the four nodes absent from MAP1_TRANSITIONS are the SAME four -- eliminativism, solipsism, "
 "suffering-as-meaning and self-effacing-under-universalization. Exactly the same set is more likely a "
 "shared generation boundary than two independent gaps. Stated as a hypothesis, not a finding.")

c["canon_version"] = "38.6"; c["canon_version_marker"] = "v38.6"
c["last_updated"] = "2026-09-17"; c["last_updated_by_session"] = "K345a_open_question_correction"
c["keyset_delta_ledger"]["v38_6_note"] = (
 "v38.5 -> v38.6 MINOR (K345a_open_question_correction, 2026-09-17): keyset UNCHANGED at 41, and the "
 "open_questions.active key set is unchanged too -- this is a value correction in place, not an addition. "
 "Sole mutation: open_questions.active.CORPUS_IS_REACTIVE_ONLY_K345 rewritten after Josiah corrected its "
 "scope and a corpus sweep falsified half of it. invariants, schemas and hazard_map asserted byte-identical "
 "by the builder. NO PIN; no corpus, JSX, flagship, ledger or objections-index byte touched, and "
 "adversarial_map_v1_0.json remains byte-identical.")
c["session_log_recent"].append(
 "K345a_open_question_correction (2026-09-17, wuld.ink Cowork; NO PIN) [MINOR v38.5->v38.6]: A CORRECTION "
 "TO K345'S OWN OPEN QUESTION, LANDED BEFORE ANYTHING COULD BE BUILT ON IT. K345 recorded Josiah's "
 "observation that the library is objection-first and split it into two gaps. He corrected the scope the "
 "same session -- the cataloguing of positive arguments is a scholarly endeavour, and mining every Twitter, "
 "Reddit, YouTube and Facebook instance is explicitly not wanted -- and a sweep of the corpus then "
 "falsified K345's second gap outright: realWorldExamples already holds 136 scholarly-schema instances "
 "across 78 of 82 nodes. THE CLAIM HAD BEEN MADE WITHOUT GREPPING FOR THE THING IT DENIED, with "
 "realWorldExamples sitting in the corpus's top-level key list the whole time. The gap restated and "
 "measured instead: MAP1_TRANSITIONS scores all 2,886 of its edges from premise overlap and tier distance, "
 "carries no observed field anywhere, and has never been joined to the 136 observations -- while 11 "
 "numbered threads already yield 53 distinct ordered node-to-node pairs, 23 of them edges the map contains "
 "under the most generous test. Also surfaced: observed archetype deployment runs ~73% sophisticate against "
 "a near-even authored variant distribution, which is a live input to Phase F's effort allocation, and the "
 "four nodes missing from the real-world layer are exactly the four missing from MAP1.")
nrs = c["next_recommended_session"]
nrs["also_read_first"] = (
 "open_questions.active.CORPUS_IS_REACTIVE_ONLY_K345, corrected at K345a. It carries a Phase F design input "
 "that did not exist when Phase F was scoped: observed archetype deployment is ~73% sophisticate (72 of 98 "
 "applicable real-world instances) while the authored variants are near-even across the four slots. Decide "
 "deliberately whether Phase F's 39 loci are authored evenly or weighted to observed deployment. Either "
 "answer is defensible; taking the even split by default, without looking, is the one that is not.")
c["next_recommended_session"] = nrs

assert list(c.keys()) == KEYS, "KEYSET MOVED"
for k, before in FROZEN.items():
    assert json.dumps(c[k], sort_keys=True, ensure_ascii=False) == before, "MAJOR-CLASS EDIT to %s" % k
assert set(c["open_questions"]["active"]) == {OLDKEY}, "open_questions.active key set moved"
dest = os.path.join(OUT, "project_canon_v38_6.json")
b = (json.dumps(c, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
open(dest, "wb").write(b)
print("WROTE %s" % dest)
print("  bytes %d  md5 %s" % (len(b), hashlib.md5(b).hexdigest()))
print("  keyset %d unchanged; invariants/schemas/hazard_map byte-identical: asserted" % len(c))
