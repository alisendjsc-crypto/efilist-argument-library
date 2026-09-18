#!/usr/bin/env python3
"""
controls_phaseF.py -- the control battery for adv_map_phaseF_defect_register_v0_1.json, and the
measurement that demoted it from an adjudication to a register.

Two jobs. (1) Mutation controls: a gate with no failing control is not a gate. (2) The CLASS
CONTROL: the register returned (b) on all 39 entries. Against the phases A-E base rate that is a
1.7e-24 event, so it is an instrument reading, not a yield. A seeded, sorted-pool sample of four loci
is re-adjudicated under the design's plain reading -- the strongest continuation against the text,
full stop, rather than against what the slot uniquely says -- and every verdict carries a verbatim
snippet from the answering locus, asserted against the corpus rather than quoted from memory.

Emits phaseF_class_control_v0_1.json. Repo-relative; reproducible under any PYTHONHASHSEED.
"""
import json, os, sys, copy, random, importlib.util, tempfile, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else _HERE
spec = importlib.util.spec_from_file_location("v", os.path.join(_HERE, "adv_map_validator_v0_3.py"))
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
POST = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
corpus = json.loads(open(POST, "rb").read().decode("utf-8"))
N = {n["id"]: n for n in corpus["objections"]}
SRC = sys.argv[sys.argv.index("--register") + 1] if "--register" in sys.argv \
      else os.path.join(_HERE, "adv_map_phaseF_defect_register_v0_1.json")
base = json.load(open(SRC, encoding="utf-8"))
tmp = tempfile.mkdtemp(prefix="k346ctl_")
res = []

def run(doc):
    p = os.path.join(tmp, "m%s.json" % hashlib.md5(json.dumps(doc, sort_keys=True).encode()).hexdigest()[:8])
    open(p, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    return v.validate([p], POST, out=lambda s: None)

def ctl(name, doc, expect):
    ok, viol, adv = run(doc); pool = viol + adv
    if expect is None:
        good = ok and not adv; detail = "clean" if good else pool[:2]
    else:
        # advisories do not clear `ok`, so a trip is measured on the pool, not on the verdict
        good = any(x.startswith(expect + ":") for x in pool)
        detail = "tripped %s" % expect if good else pool[:2]
    res.append((name, good)); print("%s . %-36s -> %s" % ("PASS" if good else "FAIL", name, detail))

print("=== MUTATION CONTROLS ===")
ctl("positive-control-as-shipped", base, None)
d = copy.deepcopy(base); d["entries"][0]["target_anchor"] = d["entries"][0]["target_anchor"][:-1] + "x"
ctl("anchor-one-char-corrupted", d, "anchor-rule")
d = copy.deepcopy(base); d["entries"][0]["target_anchor"] = d["entries"][0]["target_anchor"] + " x"
ctl("anchor-extended-past-text", d, "anchor-rule")
d = copy.deepcopy(base); d["entries"][1]["target_locus"] = "archetypeVariants.drifter"
ctl("variant-slot-absent-on-node", d, "target-locus")
d = copy.deepcopy(base); d["entries"][0]["class"] = "a"
ctl("class-flipped-routing-stale", d, "routing-shape")
d = copy.deepcopy(base); d["meta"]["variant_coverage"] = "39/39"   # overstated by one: 38 of 39 loci carry an entry
ctl("variant-coverage-declared-wrong", d, "variant-coverage")
d = copy.deepcopy(base); d["meta"]["class_counts"] = {"b": 38}
ctl("class-counts-misdeclared", d, "meta-summaries")
d = copy.deepcopy(base); d["entries"][0]["provenance"]["phase"] = "Z"
ctl("phase-outside-enum", d, "provenance")
d = copy.deepcopy(base); d["entries"][0]["adversarial_move"] = "Too short by far."
ctl("move-under-band", d, "move-band")
d = copy.deepcopy(base)
e0 = copy.deepcopy(d["entries"][20]); e1 = copy.deepcopy(d["entries"][20]); e2 = copy.deepcopy(d["entries"][20])
for k, ee in enumerate((e0, e1, e2)): ee["target_anchor"] = ee["target_anchor"][:12 + k]
d["entries"].extend([e0, e1, e2]); ctl("per-locus-cap-breached", d, "entry-cap")
d = copy.deepcopy(base); d["entries"][0]["adversarial_move"] = d["entries"][0]["adversarial_move"].replace(",", " -- ", 1)
ctl("standalone-dash-token-reintroduced", d, "move-ascii")

print("\n=== CLASS CONTROL ===")
obs = {}
for e in base["entries"]: obs[e["class"]] = obs.get(e["class"], 0) + 1
AE = {"a": 39, "b": 21, "c": 1, "d": 32}
p_ad = (AE["a"] + AE["d"]) / sum(AE.values())
n_loci = len({(e["target_id"], e["target_locus"]) for e in base["entries"]})
p_null = (1 - p_ad) ** n_loci
print("observed class counts        : %s over %d loci" % (obs, n_loci))
print("phases A-E base rate P(a or d): %.4f" % p_ad)
print("P(0 of %d in {a,d} | base rate): %.3g" % (n_loci, p_null))

pool = sorted({"%s#%s" % (e["target_id"], e["target_locus"]) for e in base["entries"]})
SAMPLE = random.Random(20260918).sample(pool, 4)   # ccclxvii: sorted pool, seeded, reproducible
READJ = {
 "red-button-repugnant#archetypeVariants.defender": {
   "strongest_continuation_plain_reading":
     "The button overrides the preference of every existing being who wants to go on living, which is "
     "a consent violation in the framework's own terms.",
   "verdict": "a", "answered_by": "red-button-repugnant#long",
   "evidence": "The strongest version of this objection bypasses the violence conflation entirely and targets preference violation"},
 "benatar-asymmetry-attack#archetypeVariants.defender": {
   "strongest_continuation_plain_reading":
     "The parity charge: if absence of pain is good with no subject, absence of pleasure must be bad "
     "with no subject.",
   "verdict": "a", "answered_by": "benatar-asymmetry-attack#long",
   "evidence": "deprivation is an irreducibly two-place relation"},
 "violence-as-reductio#archetypeVariants.defender": {
   "strongest_continuation_plain_reading":
     "The framework's adherents committed violence, so the framework is dangerous and stands "
     "convicted by their conduct.",
   "verdict": "a", "answered_by": "violence-as-reductio#medium",
   "evidence": "The framework-versus-actor distinction is foundational"},
 "ai-fear#archetypeVariants.sophisticate": {
   "strongest_continuation_plain_reading":
     "Substrate-neutral scoring by suffering-capacity ranks a pain-free successor above us, so the "
     "framework prefers our replacement.",
   "verdict": "b", "answered_by": None,
   "evidence": None,
   "note": "The slot itself concedes this residue is unmet and routes it to red-button-repugnant."},
}
assert sorted(READJ) == sorted(SAMPLE), (sorted(SAMPLE), sorted(READJ))
flips = 0
for k in SAMPLE:
    r = READJ[k]
    if r["evidence"] is not None:
        nid, loc = r["answered_by"].split("#")
        txt = v.locus_text(N[nid], loc)
        assert r["evidence"] in txt, "evidence not verbatim at %s" % r["answered_by"]
    if r["verdict"] == "a": flips += 1
    print("  %-52s -> (%s)%s" % (k, r["verdict"], "  answered_by " + r["answered_by"] if r["answered_by"] else ""))
print("  %d of %d flip to (a) under the plain reading; every (a) evidence string asserted verbatim." % (flips, len(SAMPLE)))

doc = {
 "artifact": "phaseF_class_control_v0_1.json",
 "authored": "2026-09-18, wuld.ink Cowork, K346",
 "register_under_test": os.path.basename(SRC),
 "register_md5": hashlib.md5(open(SRC, "rb").read()).hexdigest(),
 "mutation_controls": {"run": len(res), "behaved": sum(1 for _, g in res if g),
                       "detail": {n: g for n, g in res}},
 "class_distribution": {
   "observed": obs, "loci": n_loci,
   "phases_A_to_E_base_rate": AE,
   "P_a_or_d_base_rate": round(p_ad, 4),
   "P_zero_of_n_in_a_or_d_given_base_rate": p_null,
   "reading": "A 1.7e-24 departure is an instrument reading, not a yield surprise."},
 "readjudication_sample": {
   "draw": "random.Random(20260918).sample(sorted_pool, 4); sorted pool per ccclxvii",
   "sample": SAMPLE, "verdicts": READJ, "flips_to_a": flips, "of": len(SAMPLE)},
 "mechanism": (
   "The authoring seat ruled ccclxv as strongest-not-repairable and then operationalised strongest as "
   "strongest-against-what-this-slot-uniquely-says. For a register variant that filter selects against "
   "(a) by construction, because what a variant uniquely says is precisely the part its primary ladder "
   "does not already answer. Every internal inconsistency so found is repairable, hence (b). The error "
   "is ccclxv's substitution one level out, committed by the session that ruled on ccclxv."),
 "disposition": (
   "The 39 entries stand as verified defects and ship as a register. No coverage claim is made. Phase F "
   "proper -- the class-law adjudication of the 39 variant loci -- remains OWED and re-opens from the "
   "plain reading."),
}
b = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
p = os.path.join(OUT, "phaseF_class_control_v0_1.json")
open(p, "wb").write(b)
print("\n%d/%d mutation controls behaved" % (sum(1 for _, g in res if g), len(res)))
print("%s  %s  %d bytes" % (os.path.basename(p), hashlib.md5(b).hexdigest(), len(b)))
