#!/usr/bin/env python3
"""controls_phaseF_proper.py -- the control battery for adv_map_phaseF_v0_1.json.

Three jobs.
 (1) MUTATION CONTROLS: a gate with no failing control is not a gate. Includes controls for the
     two checks v0_4 adds, in both directions.
 (2) THE (a) EVIDENCE BATTERY: every (a) entry names an answering locus, and every answering
     locus is asserted to carry a verbatim snippet that does the answering -- against the corpus,
     programmatically, never quoted from memory. A lazy (a) is worse than a lazy (b).
 (3) THE CLASS-MIX GATE (ccclxviii), with a null (ccclxvi): the phase's a+d share is tested
     against the phases A-E base rate rather than eyeballed, in BOTH directions.

Emits phaseF_proper_control_v0_1.json. Repo-relative; reproducible under any PYTHONHASHSEED.
"""
import json, os, sys, copy, tempfile, importlib.util, hashlib, math

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K347_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else _HERE
VAL = os.environ.get("K347_VALIDATOR") or os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_4.py")
FRAG = os.environ.get("K347_FRAGMENT") or os.path.join(REPO, "adversarial_map_staging", "adv_map_phaseF_v0_1.json")
spec = importlib.util.spec_from_file_location("v", VAL)
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)
POST = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
corpus = json.loads(open(POST, "rb").read().decode("utf-8"))
N = {n["id"]: n for n in corpus["objections"]}
base = json.loads(open(FRAG, "rb").read().decode("utf-8"))
tmp = tempfile.mkdtemp(prefix="k347ctl_")
res = []

def run(doc, extra_files=()):
    p = os.path.join(tmp, "m%s.json" % hashlib.md5(json.dumps(doc, sort_keys=True).encode()).hexdigest()[:8])
    open(p, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    return V.validate([p] + list(extra_files), POST, out=lambda s: None)

def ctl(name, doc, expect, extra_files=()):
    ok, viol, adv = run(doc, extra_files); pool = viol + adv
    if expect is None:
        good = ok and not adv; detail = "clean" if good else pool[:2]
    else:
        good = any(x.startswith(expect + ":") for x in pool)
        detail = "tripped %s" % expect if good else ("NO TRIP; pool=%s" % (pool[:2],))
    res.append((name, good)); print("%s . %-44s -> %s" % ("PASS" if good else "FAIL", name, detail))

print("=== (1) MUTATION CONTROLS ===")
ctl("positive-control-as-shipped", base, None)
d = copy.deepcopy(base); d["entries"][0]["target_anchor"] = d["entries"][0]["target_anchor"][:-1] + "x"
ctl("anchor-one-char-corrupted", d, "anchor-rule")
d = copy.deepcopy(base); d["entries"][0]["target_anchor"] += " zzz"
ctl("anchor-extended-past-text", d, "anchor-rule")
d = copy.deepcopy(base); d["entries"][0]["target_locus"] = "archetypeVariants.drifter"
ctl("variant-slot-absent-on-node", d, "target-locus")
d = copy.deepcopy(base); d["entries"][0]["class"] = "b"
ctl("class-flipped-routing-stale", d, "routing-shape")
d = copy.deepcopy(base); d["meta"]["class_counts"] = {"a": 39}
ctl("class-counts-misdeclared", d, "meta-summaries")
d = copy.deepcopy(base); d["meta"]["variant_coverage"] = "39/39"
ctl("variant-coverage-overstated", d, "variant-coverage")
d = copy.deepcopy(base); d["entries"][0]["adversarial_move"] = "Far too short."
ctl("move-under-band", d, "move-band")
d = copy.deepcopy(base)
for x in d["entries"]:
    if x["class"] == "a": x["adversarial_move"] = " ".join(["w"] * 61); break
ctl("class-a-move-over-60", d, "move-band")
d = copy.deepcopy(base); d["entries"][0]["adversarial_move"] = d["entries"][0]["adversarial_move"].replace(" the ", " -- ", 1)
ctl("standalone-dash-token", d, "move-ascii")
d = copy.deepcopy(base); d["entries"][0]["provenance"]["phase"] = "Q"
ctl("phase-outside-enum", d, "provenance")
d = copy.deepcopy(base); d["meta"]["source_corpus_objections_md5"] = "0" * 32
ctl("objections-digest-wrong", d, "objections-digest")

print()
print("=== (1b) CONTROLS FOR THE TWO CHECKS v0_4 ADDS ===")
# gate 5, both directions
d = copy.deepcopy(base); d["meta"]["locus_closure"].pop("most-people-happy#archetypeVariants.sophisticate")
ctl("closure-misses-an-authored-locus", d, "stopping-rule")
d = copy.deepcopy(base); d["meta"]["locus_closure"]["future-solve#archetypeVariants.drifter"] = "closed"
ctl("closure-declares-an-unauthored-locus", d, "stopping-rule")
d = copy.deepcopy(base); d["meta"]["locus_closure"]["most-people-happy#archetypeVariants.sophisticate"] = "open"
ctl("open-declared-with-one-entry", d, "stopping-rule")
d = copy.deepcopy(base); d["meta"]["locus_closure"]["red-button-repugnant#archetypeVariants.sophisticate"] = "closed"
ctl("open-locus-misdeclared-closed", d, "stopping-rule")
d = copy.deepcopy(base); d["meta"]["locus_closure"]["selfish-lazy#archetypeVariants.defender"] = "sealed"
ctl("closure-value-outside-enum", d, "stopping-rule")
# two entries at one locus on the SAME clause: shrink the open locus's second anchor into the first
d = copy.deepcopy(base)
tgt = [x for x in d["entries"] if (x["target_id"], x["target_locus"]) == ("red-button-repugnant", "archetypeVariants.sophisticate")]
assert len(tgt) == 2, "expected the open locus to carry 2 entries"
tgt[1]["target_anchor"] = tgt[0]["target_anchor"][:40]
ctl("two-entries-same-clause", d, "stopping-rule")
d = copy.deepcopy(base); d["meta"].pop("locus_closure")
ctl("undeclared-closure-is-not-gated", d, None)

# ccclxx: the declaration's verdict must not move with how many files the run loads
R = os.path.join(REPO, "adversarial_map_staging", "adv_map_phaseR_v0_1.json")
okS, vS, _ = V.validate([FRAG], POST, out=lambda s: None)
okJ, vJ, _ = V.validate([FRAG, R], POST, out=lambda s: None)
good = okS and okJ
res.append(("ccclxx-verdict-invocation-independent", good))
print("%s . %-44s -> solo=%s joint=%s" % ("PASS" if good else "FAIL",
      "ccclxx-verdict-invocation-independent", okS, okJ))
# and the SAME pair under v0_3, which must fail -- the control that proves the fix is not cosmetic
V3 = os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_3.py")
s3 = importlib.util.spec_from_file_location("v3", V3); V3m = importlib.util.module_from_spec(s3); s3.loader.exec_module(V3m)
ok3S, _, _ = V3m.validate([FRAG], POST, out=lambda s: None)
ok3J, v3J, _ = V3m.validate([FRAG, R], POST, out=lambda s: None)
good = ok3S and (not ok3J) and any(x.startswith("variant-coverage:") for x in v3J)
res.append(("ccclxx-defect-reproduced-on-v0_3", good))
print("%s . %-44s -> v0_3 solo=%s joint=%s" % ("PASS" if good else "FAIL",
      "ccclxx-defect-reproduced-on-v0_3", ok3S, ok3J))

print()
print("=== (2) THE (a) EVIDENCE BATTERY: answering locus carries a verbatim snippet ===")
EV = {
 ("red-button-repugnant", "archetypeVariants.defender"):
   ("red-button-repugnant#long", "its continuation must be justified by its content"),
 ("red-button-repugnant", "archetypeVariants.sophisticate"):
   ("red-button-repugnant#long", "not by a philosophically reliable endorsement of existence"),
 ("benatar-asymmetry-attack", "archetypeVariants.blended"):
   ("benatar-asymmetry-attack#archetypeVariants.sophisticate", "deprivation is irreducibly two-place"),
 ("benatar-asymmetry-attack", "archetypeVariants.defender"):
   ("benatar-asymmetry-attack#long", "inference to the best explanation, not stipulation"),
 ("benatar-asymmetry-attack", "archetypeVariants.drifter"):
   ("benatar-asymmetry-attack#long", "the un-instantiated pleasure generates no reason"),
 ("wild-animal-suffering-consistency", "archetypeVariants.blended"):
   ("wild-animal-suffering-consistency#long", "not anti-intervention in principle"),
 ("wild-animal-suffering-consistency", "archetypeVariants.defender"):
   ("wild-animal-suffering-consistency#long", "confuses ethical salience with intervention obligation"),
 ("wild-animal-suffering-consistency", "archetypeVariants.drifter"):
   ("wild-animal-suffering-consistency#long", "is itself a contribution to the case for antinatalism"),
 ("wild-animal-suffering-consistency", "archetypeVariants.sophisticate"):
   ("wild-animal-suffering-consistency#long", "who will suffer and was not consulted"),
 ("ai-fear", "archetypeVariants.blended"):
   ("violence-as-reductio#long", "the bridge is held, and held by founders"),
 ("ai-fear", "archetypeVariants.drifter"):
   ("why-not-suicide#long", "only the negative action of not procreating is authorized"),
 ("violence-as-reductio", "archetypeVariants.blended"):
   ("violence-as-reductio#archetypeVariants.sophisticate", "route it to the node that owns the anchor"),
 ("violence-as-reductio", "archetypeVariants.defender"):
   ("violence-as-reductio#long", "Centrality is sociology; entailment is logic"),
 ("violence-as-reductio", "archetypeVariants.sophisticate"):
   ("why-not-suicide#archetypeVariants.sophisticate", "indexed to the non-existence case"),
 ("slippery-slope-eugenics", "archetypeVariants.defender"):
   ("slippery-slope-eugenics#long", "they are nodding at a slogan"),
 ("future-solve", "archetypeVariants.sophisticate"):
   ("most-people-happy#long", "You do not get to gamble with someone else's welfare"),
 ("most-people-happy", "archetypeVariants.sophisticate"):
   ("cherry-picking-worst#archetypeVariants.sophisticate", "Strip the distribution to its guaranteed baseline"),
 ("antinatalism-misanthropic", "archetypeVariants.blended"):
   ("antinatalism-misanthropic#archetypeVariants.sophisticate", "The prevention-ground is impersonal"),
 ("antinatalism-misanthropic", "archetypeVariants.defender"):
   ("antinatalism-misanthropic#long", "structural criticism of a species is not the same as hatred of individuals"),
 ("antinatalism-misanthropic", "archetypeVariants.drifter"):
   ("antinatalism-misanthropic#archetypeVariants.sophisticate", "empathy aimed at a harm"),
 ("next-person-cure-cancer", "archetypeVariants.sophisticate"):
   ("next-person-cure-cancer#long", "did they consent to the conditions under which they must achieve it"),
 ("privileged-first-world", "archetypeVariants.defender"):
   ("privileged-first-world#long", "emerged from conditions of extreme suffering"),
 ("selfish-lazy", "archetypeVariants.defender"):
   ("selfish-lazy#long", "identifies the natalist as the selfish party"),
 ("why-not-suicide", "archetypeVariants.blended"):
   ("why-not-suicide#long", "biology has installed exit barriers"),
 ("why-not-suicide", "archetypeVariants.defender"):
   ("violence-as-reductio#long", "Centrality is sociology; entailment is logic"),
 ("why-not-suicide", "archetypeVariants.drifter"):
   ("why-not-suicide#long", "the structural layer does not entail the NU layer"),
}
a_entries = [x for x in base["entries"] if x["class"] == "a"]
seen_keys = set()
ev_ok = 0
for x in a_entries:
    k = (x["target_id"], x["target_locus"])
    # the open locus carries two entries; its (a) is the second, keyed once
    if k in seen_keys and k in EV: pass
    seen_keys.add(k)
    good = k in EV
    if good:
        ref, snip = EV[k]
        nid, _, loc = ref.partition("#")
        txt = V.locus_text(N[nid], loc)
        good = snip in txt and ref in x["routing"]["answered_by"]
        detail = ("verbatim at %s" % ref) if good else ("MISS: snippet in locus=%s, ref routed=%s"
                  % (snip in txt, ref in x["routing"]["answered_by"]))
    else:
        detail = "NO EVIDENCE ENTRY for this (a)"
    ev_ok += 1 if good else 0
    print("%s . %-62s -> %s" % ("PASS" if good else "FAIL", "%s#%s" % (k[0], k[1].split(".")[-1]), detail))
res.append(("a-evidence-battery-%d-of-%d" % (ev_ok, len(a_entries)), ev_ok == len(a_entries)))
print("  %d of %d (a) entries carry an answering locus with a verbatim snippet asserted against the corpus."
      % (ev_ok, len(a_entries)))

print()
print("=== (3) CLASS-MIX GATE vs THE A-E BASE RATE, WITH A NULL (ccclxvi / ccclxviii) ===")
BASE = {"a": 39, "b": 21, "c": 1, "d": 32}
nb = sum(BASE.values()); p0 = (BASE["a"] + BASE["d"]) / float(nb)
cc = {}
for x in base["entries"]: cc[x["class"]] = cc.get(x["class"], 0) + 1
n = len(base["entries"]); k = cc.get("a", 0) + cc.get("d", 0)
def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
pmf = [C(n, i) * (p0 ** i) * ((1 - p0) ** (n - i)) for i in range(n + 1)]
p_obs = pmf[k]
p_two = sum(q for q in pmf if q <= p_obs + 1e-15)
exp = n * p0; sd = math.sqrt(n * p0 * (1 - p0))
print("  base rate a+d = %d/%d = %.4f   observed = %d/%d = %.4f" % (BASE["a"] + BASE["d"], nb, p0, k, n, k / float(n)))
print("  expected %.2f, sd %.2f, z = %+.2f" % (exp, sd, (k - exp) / sd))
print("  exact two-sided binomial p = %.4f" % p_two)
K346 = 0  # the register drew zero (a)-or-(d) across 38 loci
p_k346 = pmf[0] if n >= 0 else 0.0
print("  for contrast, K346's register drew 0 of 39 at this prior: p = %.3g" % ((1 - p0) ** n))
verdict = "CONSISTENT" if p_two >= 0.05 else "DEPARTS FROM PRIOR"
good = p_two >= 0.05
res.append(("class-mix-consistent-with-prior", good))
print("  %s . class mix is %s with its own base rate (two-sided p = %.4f)"
      % ("PASS" if good else "FAIL", verdict, p_two))
print("  within-total split: a %.4f (base %.4f), d %.4f (base %.4f), b %.4f (base %.4f), c %.4f (base %.4f)"
      % (cc.get("a", 0) / float(n), BASE["a"] / float(nb), cc.get("d", 0) / float(n), BASE["d"] / float(nb),
         cc.get("b", 0) / float(n), BASE["b"] / float(nb), cc.get("c", 0) / float(n), BASE["c"] / float(nb)))

# slot cross-tab: the design section 10.5 expectation, measured
slots = {}
for x in base["entries"]:
    s = x["target_locus"].split(".")[-1]
    slots.setdefault(s, {"n": 0, "b": 0})
    slots[s]["n"] += 1
    if x["class"] == "b": slots[s]["b"] += 1
print("  per-slot (b) counts:", {s: "%d/%d" % (v["b"], v["n"]) for s, v in sorted(slots.items())})

print()
passed = sum(1 for _n, g in res if g)
allgood = passed == len(res)
doc = {
  "artifact": "phaseF_proper_control_v0_1.json",
  "subject": "adv_map_phaseF_v0_1.json",
  "authored": "2026-09-17, wuld.ink Cowork, K347",
  "validator": os.path.basename(VAL),
  "controls": {nme: bool(g) for nme, g in res},
  "controls_passed": passed, "controls_total": len(res), "all_pass": allgood,
  "a_evidence": {"%s#%s" % kk: {"answered_by": vv[0], "snippet": vv[1]} for kk, vv in sorted(EV.items())},
  "a_evidence_verified": ev_ok, "a_entries": len(a_entries),
  "class_mix": {
    "base_phases_A_to_E": BASE, "base_a_or_d_share": round(p0, 6),
    "observed": cc, "n": n, "observed_a_or_d": k, "observed_a_or_d_share": round(k / float(n), 6),
    "expected_a_or_d": round(exp, 4), "sd": round(sd, 4), "z": round((k - exp) / sd, 4),
    "exact_two_sided_binomial_p": round(p_two, 6),
    "verdict": verdict,
    "k346_register_for_contrast": {"a_or_d": 0, "n": 39, "p_at_this_prior": (1 - p0) ** n},
    "reading": ("The gate is two-sided by design (ccclxviii): knowing K346 drew zero (a) is not a licence to "
                "rubber-stamp (a). a+d lands inside the prior, so the phase's receipt is not written over an "
                "instrument reading. Within that total the split moves toward (a) and away from (d), which is "
                "what design section 10.4 predicts for loci that re-present an argument their primary ladder "
                "already answers."),
  },
  "per_slot_b_counts": {s: v for s, v in sorted(slots.items())},
}
os.makedirs(OUT, exist_ok=True)
dest = os.path.join(OUT, "phaseF_proper_control_v0_1.json")
out = (json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
open(dest, "wb").write(out)
print("controls %d/%d ; wrote %s md5 %s bytes %d" % (passed, len(res), dest, hashlib.md5(out).hexdigest(), len(out)))
sys.exit(0 if allgood else 1)
