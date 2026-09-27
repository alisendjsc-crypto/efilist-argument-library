#!/usr/bin/env python3
"""measure_variations.py -- V0 (seat l, 2026-09-26): every count in VARIATIONS_design_v0_1.md, re-derived.

R0194's law: "Every count in the design is re-derived by a script committed beside it." This is that script.
It reads, never writes, everything outside design/variations/, and every input is pinned by md5:

  efilist (this repo), through adversarial_map_staging/r1/pinned.py, so the record still reproduces after a
  later pin moves the corpus (L5's law: an instrument reads the corpus at the md5 its record pins):
    the corpus, the JSX, site/combined.html, the flagship layman index, the Map 1 sidecar, the adversarial
    map v1_6, the map validator v0_6, R1_rulings.json, the PQ judgments and drafts records, the RWE schema
    v1.7, the four wing corpora and the veganism module, and the flagship and wing grading ledgers.
  the game (Argue the Argument), READ-ONLY through `git show` at a pinned commit, never its working tree
  (a live argue session may hold uncommitted edits there): inject_data.py, index.html and the vendored
  scholar-objections_v1_1.json.

  python3 design/variations/measure_variations.py           # writes measure_variations_v0_1.json beside it
  python3 design/variations/measure_variations.py --check   # recomputes; exit 1 if the record differs

The output is deterministic (sorted keys, sorted lists, no set iteration order, no clock), so it must come
out byte-identical under any PYTHONHASHSEED.  Pure ASCII source.
"""
import ast, collections, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
from pinned import bytes_at  # noqa: E402

OUT = os.path.join(HERE, "measure_variations_v0_1.json")

PINS = {
    "corpus": ("efilist_argument_library_v4_0_0.json", "f3d88311ea98f8333aebbecb67766351"),
    "jsx": ("efilist_argument_library_v4_0_0.jsx", "518c62f4ce3fe40ea3408475f608b1ff"),
    "combined": ("site/combined.html", "ed040cad2f60caaf0cba696af77f860e"),
    "layman": ("site/flagship-layman-index.json", "7a1f0881a6a9e964a4155d7897c312f8"),
    "map1": ("sidecars/map1_transitions.json", "1b059c498321cc2bbb960a3f8dac3c52"),
    "advmap": ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "validator": ("adversarial_map_staging/adv_map_validator_v0_6.py", "c002e93877b09d523daf786036af7a57"),
    "rulings": ("adversarial_map_staging/r1/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74"),
    "pq_judgments": ("adversarial_map_staging/r1/PQ_repair_drafts_judgments.json", "2ed68a7cf7f83b8d61a977f0aad0b08e"),
    "pq_drafts": ("adversarial_map_staging/r1/PQ_repair_drafts_L5.json", "8c57223e8f9170cb8303bcc4b9d982c4"),
    "rwe_schema": ("real_world_examples_schema_v1_7.json", "13ca1171725b8652dffc04b864692d40"),
    "ledger": ("rebuttal_grading_ledger.json", "96c492cf4a9e15aefabdcb362838a515"),
}
LEDGERS = {  # the wings' grading ledgers: where a retreat lattice (grades.routes_to) lives, if anywhere
    "abortion": ("site/abortion/abortion_grading_ledger.json", "35fdee8ac2ae8af94258da8e86442717"),
    "anthropocentrism": ("site/anthropocentrism/anthropocentrism_grading_ledger.json", "4be54416d2a089da8263b1dfd5a44fa9"),
    "right-to-die": ("site/right-to-die/right_to_die_grading_ledger.json", "846379a5bba3c516bb70ddcdd80a509c"),
    "transgenderism": ("site/transgenderism/transgenderism_grading_ledger.json", "e4e852a0394532facedd2ed950e12538"),
    "veganism": ("site/veganism/veganism_grading_ledger.json", "a6a4dc136cf497a0a84634a9a6c18b40"),
}
WINGS = {
    "right-to-die": ("site/right-to-die/right_to_die_corpus_v0_1.json", "e7d6243a249e761ec96397e65aa0e174", "objections"),
    "anthropocentrism": ("site/anthropocentrism/anthropocentrism_corpus_v0_1.json", "d9304ac25b18b2300b605dbd8b829004", "objections"),
    "transgenderism": ("site/transgenderism/transgenderism_corpus_v0_1.json", "faa26bc5084da0027341b570fb6c375e", "objections"),
    "abortion": ("site/abortion/abortion_corpus_v0_1.json", "827b74be5f62194efb8a230f8df20c72", "objections"),
    "veganism": ("site/veganism/veganism_module_v0_1.json", "5667a092a930be455defe8934a94cd39", "nodes"),
}
ARGUE_REPO = os.path.expanduser("~/D/Argue the Argument")
ARGUE_SHA = "a801c556882f98adac248aa5ea841e823f327af1"  # game main at V0 open (S47 kickoff)
ARGUE_PINS = {
    "inject_data": ("inject_data.py", "a740d36388d51d7dec95b3e613e18015"),
    "index": ("index.html", "c3dc6fc44ab0190242be8335675faf09"),
    "scholar": ("data/flagship/scholar-objections_v1_1.json", "20999eb9b1b384d0f871a9deec464b2a"),
}

# The pilot's exclusion is DERIVED, not typed: a node is in flux when a pending finding of the pin queue
# names it -- gate2's X-032 (L6's safety pass, running now), X-033 and X-034 (the next pin's queue), and
# L5's PF-01..PF-07 (the successor map's re-judgments). Shapes answered inside text that is about to move
# would be judged against the wrong words.
FLUX_JUDGMENT_ROWS = ("X-032", "X-033", "X-034")
FLUX_DRAFT_PREFIX = "PF-"
# Control on that derivation: R0193 names X-032's five nodes; if the parse misses any, the derivation is wrong.
X032_NODES = ("heat-death-futility", "red-button-repugnant", "revealed-preference", "social-contract", "why-not-suicide")

NONEXACT_FITS = ("loose", "parallel-structure-different-anchor", "partial")
CHARACTER_MODELS = ("defender", "drifter", "sophisticate")  # Map 1 models a Next Move opponent can be
# Planning constants for the cost estimate (the design's, not measurements; stated so the arithmetic is checkable).
# 35 per session is R1's pace (L2 ruled 40 rows, L3 29); drafting is assumed to run at the same pace.
PLAN = {"shapes_per_node": 3, "words_per_shape": 90, "pilot_nodes": 6, "shapes_per_judging_session": 35}


def md5(b):
    return hashlib.md5(b).hexdigest()


def load(key):
    rel, want = PINS[key]
    return bytes_at(REPO, rel, want)


def argue(key):
    rel, want = ARGUE_PINS[key]
    r = subprocess.run(["git", "-C", ARGUE_REPO, "show", "%s:%s" % (ARGUE_SHA, rel)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ABORT: cannot read the game at %s:%s (%s)" % (ARGUE_SHA[:8], rel, r.stderr.decode()[:200]))
    if md5(r.stdout) != want:
        raise SystemExit("ABORT: game file %s is not at its pinned md5" % rel)
    return r.stdout


def wc(s):
    return len(s.split())


def stats(xs):
    xs = sorted(xs)
    if not xs:
        return {"n": 0}
    n = len(xs)
    med = xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
    return {"n": n, "min": xs[0], "median": med, "max": xs[-1], "mean": round(sum(xs) / n, 2), "total": sum(xs)}


def id_in(text, i):
    return re.search(r"(?<![a-z0-9-])" + re.escape(i) + r"(?![a-z0-9-])", text) is not None


def validator_constants(src):
    """Read the validator's enums WITHOUT executing it (ast), so a record never depends on its side effects."""
    want = {"LOCI", "VARIANT_PREFIX", "VARIANT_SLOTS", "NOTE_LOCUS", "CLASSES", "PHASES", "ENTRY_KEYS", "IND_GROUNDS"}
    got = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in want:
                v = ast.literal_eval(node.value)
                got[name] = list(v) if isinstance(v, (tuple, list)) else v
    assert set(got) == want, "validator constants missing: %s" % sorted(want - set(got))
    got["anchor_rule"] = re.search(r"anchor-rule\s+(.+)", src).group(1).strip()
    got["move_band"] = re.search(r"move-band\s+(.+)", src).group(1).strip()
    got["entry_cap_node"] = re.search(r"entry-cap-node\s+(.+)", src).group(1).strip()
    got["entry_cap_locus"] = re.findall(r"entry-cap\s+(<=3 entries per \(target_id, target_locus\))", src)[0]
    return got


def measure():
    corpus = json.loads(load("corpus"))
    obs = corpus["objections"]
    ids = [o["id"] for o in obs]
    node = {o["id"]: o for o in obs}
    R = {"pins": {k: v[1] for k, v in sorted(PINS.items())},
         "pins_argue": dict({k: v[1] for k, v in sorted(ARGUE_PINS.items())}, commit=ARGUE_SHA),
         "pins_wings": {k: v[1] for k, v in sorted(WINGS.items())},
         "pins_ledgers": {k: v[1] for k, v in sorted(LEDGERS.items())},
         "plan_constants": PLAN}

    # ---- 1. the flagship corpus -------------------------------------------------------------------
    tiers = collections.Counter(o["tier"] for o in obs)
    phr = {o["id"]: [p.strip() for p in o["trigger"].split(" / ")] for o in obs}
    pdm = corpus["premiseDependencyMatrix"]
    strong = {i: sum(1 for x in pdm[i]["dependencies"] if x["strength"] == "strong") for i in ids}
    R["corpus"] = {
        "version_field": corpus["version"],
        "objections": len(obs),
        "tiers": {str(k): tiers[k] for k in sorted(tiers)},
        "depths_on_every_node": all(all(k in o["responses"] for k in ("short", "medium", "long")) for o in obs),
        "trigger_phrasings": stats([len(v) for v in phr.values()]),
        "trigger_phrasings_total": sum(len(v) for v in phr.values()),
        "trigger_phrasing_words": stats([wc(p) for v in phr.values() for p in v]),
        "keywords_per_node": stats([len(o["keywords"]) for o in obs]),
        "strong_premise_deps_per_node": stats(list(strong.values())),
        "strong_premise_max_nodes": sorted(i for i in ids if strong[i] == max(strong.values())),
        "top_level_keys_by_count": dict(sorted(collections.Counter(k for o in obs for k in o).items())),
        "registered_moves": len(corpus["registered_moves"]),
    }

    # ---- 2. the variation layers that already exist ----------------------------------------------
    av = {i: node[i]["responses"]["archetypeVariants"] for i in ids if "archetypeVariants" in node[i]["responses"]}
    slots = collections.Counter(s for v in av.values() for s in v)
    av_words = [wc(t) for v in av.values() for t in v.values()]
    R["archetypeVariants"] = {
        "nodes": len(av), "slots": sum(slots.values()), "by_slot": dict(sorted(slots.items())),
        "by_tier": dict(sorted(collections.Counter(str(node[i]["tier"]) for i in av).items())),
        "words_per_slot": stats(av_words), "node_ids": sorted(av)}

    sub = {i: node[i]["objectionSubforms"] for i in ids if "objectionSubforms" in node[i]}
    units = [u for v in sub.values() for u in v]
    rwe = corpus["realWorldExamples"]
    rwe_by_id = {r["instance_id"]: r for r in rwe}
    anchors = sorted(a for u in units for a in u.get("corpus_anchors", []))
    fk_docs = []

    def walk(x):
        if isinstance(x, dict):
            if "objectionSubforms" in str(x.get("foreign_key", "")):
                fk_docs.append(x.get("_doc", ""))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(json.loads(load("rwe_schema")))
    assert len(fk_docs) == 1, "expected exactly one RWE field keyed on objectionSubforms"
    combined = load("combined").decode("utf-8")
    jsx = load("jsx").decode("utf-8")
    R["objectionSubforms"] = {
        "nodes": sorted(sub), "units": len(units),
        "words": sum(wc(" ".join(str(x) for x in u.values())) for u in units),
        "definitions_opening_Position-holder": sum(1 for u in units
                                                    if u["discriminating_definition"].startswith("Position-holder")),
        "deployment_registers": sorted(u["deployment_register"] for u in units),
        "corpus_anchor_polarity": dict(sorted(collections.Counter(
            rwe_by_id[a]["instance_polarity"] for a in anchors).items())),
        "rwe_instances_coding_refutation_variant_id": sum(1 for r in rwe if r.get("refutation_variant_id")),
        "rwe_schema_calls_it_a_refutational_variant": "canonical refutational variant" in fk_docs[0],
        "occurrences_in_combined_html": combined.count("objectionSubforms"),
        "occurrences_in_jsx": jsx.count("objectionSubforms"),
    }
    R["note_and_confidence"] = {"note_nodes": sum(1 for o in obs if isinstance(o.get("note"), str) and o["note"].strip()),
                                "confidence_nodes": sum(1 for o in obs if "confidence" in o)}

    # ---- 3. real-world instances: the attested shapes ------------------------------------------------
    att = [(r, a) for r in rwe for a in r["attached_objections"]]
    fit = collections.Counter(a.get("fit_to_trigger_phrases") for _, a in att)
    against = [(r, a) for r, a in att if r["instance_polarity"] == "deploys-against"]
    nonexact = collections.defaultdict(set)
    exact = collections.defaultdict(set)
    for r, a in against:
        (nonexact if a.get("fit_to_trigger_phrases") in NONEXACT_FITS else exact)[a["objection_id"]].add(r["instance_id"])
    quoted = [r for r in rwe if r.get("short_quote_under_15_words")]
    quoted_against = [r for r in quoted if r["instance_polarity"] == "deploys-against"]
    R["realWorldExamples"] = {
        "instances": len(rwe),
        "nodes_attached": len({a["objection_id"] for _, a in att}),
        "attachments": len(att),
        "fit_to_trigger_phrases": {str(k): v for k, v in sorted(fit.items(), key=lambda kv: str(kv[0]))},
        "polarity": dict(sorted(collections.Counter(r["instance_polarity"] for r in rwe).items())),
        "deploys_against_nonexact_attachments": sum(len(v) for v in nonexact.values()),
        "deploys_against_nonexact_nodes": len(nonexact),
        "deploys_against_nonexact_by_node": {k: len(v) for k, v in sorted(nonexact.items())},
        "short_quotes_nonempty": len(quoted),
        "short_quotes_on_deploys_against": len(quoted_against),
        "short_quote_node_pairs_deploys_against_exact_fit": len({(r["instance_id"], a["objection_id"])
                                                                  for r in quoted_against for a in r["attached_objections"]
                                                                  if a.get("fit_to_trigger_phrases") == "exact"}),
        "short_quote_node_pairs_deploys_against_exact_fit_nodes": len({a["objection_id"] for r in quoted_against
                                                                        for a in r["attached_objections"]
                                                                        if a.get("fit_to_trigger_phrases") == "exact"}),
        "short_quote_attestation_status": {str(k): v for k, v in sorted(collections.Counter(
            r.get("short_quote_attestation_status") for r in rwe).items(), key=lambda kv: str(kv[0]))},
        "archetype_signal_observed": dict(sorted(collections.Counter(r["archetype_signal_observed"] for r in rwe).items())),
        "dated_2024_or_later": sum(1 for r in rwe if r["source_date"][:4].isdigit() and r["source_date"][:4] >= "2024"),
    }

    # ---- 4. Map 1: where the game deals ----------------------------------------------------------------
    m1 = json.loads(load("map1"))
    indeg = collections.Counter()
    for s, v in m1["data"].items():
        for model in CHARACTER_MODELS:
            for e in v[model]:
                indeg[e["target"]] += 1
    R["map1"] = {"edge_counts": m1["edge_counts"], "sources": len(m1["data"]),
                 "absent_as_source": sorted(set(ids) - set(m1["data"])),
                 "in_degree_three_character_models": stats([indeg[i] for i in ids]),
                 "top10_in_degree": [[i, indeg[i]] for i in sorted(ids, key=lambda i: (-indeg[i], i))[:10]]}

    # ---- 5. what a variation must carry to be judged: the map, its validator, R1 ----------------------
    vsrc = load("validator").decode("utf-8")
    R["validator_v0_6"] = validator_constants(vsrc)
    amap = json.loads(load("advmap"))
    ents = amap["entries"]
    kinds = collections.Counter("variant" if e["target_locus"].startswith("archetypeVariants.") else
                                "note" if e["target_locus"] == "note" else "primary" for e in ents)
    a_rout = [t for e in ents if e["class"] == "a" for t in e["routing"]["answered_by"]]
    locus_only = re.compile(r"^[a-z0-9-]+#(short|medium|long|diagnosis|note|archetypeVariants\.[a-z]+)$")
    move_words = collections.defaultdict(list)
    for e in ents:
        move_words[e["class"]].append(wc(e["adversarial_move"]))
    R["adversarial_map_v1_6"] = {
        "entries": len(ents), "class_counts": dict(sorted(collections.Counter(e["class"] for e in ents).items())),
        "locus_kinds": dict(sorted(kinds.items())),
        "a_routing_targets": len(a_rout),
        "a_routing_targets_locus_only_no_anchor": sum(1 for t in a_rout if locus_only.match(t)),
        "c_entries": [[e["target_id"], e["routing"]["intake_candidate"]["proposed_id"],
                       e["routing"]["intake_candidate"]["individuation_grounds"]] for e in ents if e["class"] == "c"],
        "move_words_by_class": {k: stats(v) for k, v in sorted(move_words.items())},
        "source_corpus_md5": amap["meta"]["source_corpus_md5"]}
    a_ents = [e for e in ents if e["class"] == "a"]
    R["adversarial_map_v1_6"]["a_entries_routing_to_another_node"] = sum(
        1 for e in a_ents if any(t.split("#")[0] != e["target_id"] for t in e["routing"]["answered_by"]))
    R["adversarial_map_v1_6"]["a_routing_targets_on_another_node"] = sum(
        1 for e in a_ents for t in e["routing"]["answered_by"] if t.split("#")[0] != e["target_id"])
    lattice = {}
    for w, (rel, want) in sorted(dict(LEDGERS, flagship=PINS["ledger"]).items()):
        g = json.loads(bytes_at(REPO, rel, want)).get("grades", {})
        kinds = collections.Counter()
        for v in g.values():
            for e in (v.get("routes_to") or []) if isinstance(v, dict) else []:
                kinds["to_node" if e.get("to") else "terminus:%s" % e.get("terminus_kind")] += 1
        lattice[w] = {"nodes_graded": len(g), "retreat_edges": sum(kinds.values()), "by_kind": dict(sorted(kinds.items()))}
    R["retreat_lattice"] = lattice
    rul = json.loads(load("rulings"))["rows"]
    superseded = {r["supersedes"] for r in rul if r.get("supersedes")}
    live = [r for r in rul if r["row"] not in superseded]
    R["r1"] = {"rows": len(rul), "entries_ruled": len({r["n"] for r in live}),
               "verdicts": dict(sorted(collections.Counter(r["verdict"] for r in live).items()))}

    # ---- 6. the game: what it embeds, what it reads, what it shows ------------------------------------
    inj = argue("inject_data").decode("utf-8")
    keep = ast.literal_eval(re.search(r"KEEP = (\([^)]*\))", inj).group(1))
    html = argue("index").decode("utf-8")
    blocks = re.findall(r"<!--DATA:(\w+)-->", html)
    code = re.sub(r"<!--DATA:(\w+)-->.*?<!--/DATA:\1-->", "", html, flags=re.S)
    reads = {f: code.count(f) for f in ("archetypeVariants", "objectionSubforms", "realWorldExamples",
                                         "layman_trigger", "scholar_objection", "responses.short")}
    sch = json.loads(argue("scholar"))
    R["game"] = {
        "lean_embed_keep_fields": list(keep),
        "embeds_objectionSubforms": "objectionSubforms" in keep,
        "embeds_responses_whole": "responses" in keep,
        "data_blocks": blocks,
        "code_reads": reads,
        "code_splits_trigger_phrasings": bool(re.search(r"trigger\s*\.\s*split|split\(\s*[\"']\s*/", code)),
        "default_register": re.search(r'let MODE = "(\w+)"', code).group(1),
        "one_fixed_line_per_node_per_register": True,
        "scholar_layer": {"nodes": len(sch["nodes"]),
                          "words": stats([wc(n["scholar_objection"]) for n in sch["nodes"]])},
    }
    # the claim just recorded, asserted rather than assumed: the default line is a single field per node
    assert "l.layman_trigger" in code and "s.scholar_objection" in code and not R["game"]["code_splits_trigger_phrasings"]

    # ---- 7. surfaces held vs shown ---------------------------------------------------------------------
    lay = json.loads(load("layman"))
    R["surfaces"] = {
        "shown_per_register": len(lay["nodes"]),
        "layman_trigger_words": stats([wc(n["layman_trigger"]) for n in lay["nodes"]]),
        "held_not_shown": {"trigger_phrasings": R["corpus"]["trigger_phrasings_total"],
                           "attributed_short_quotes_deploys_against": len(quoted_against)},
    }

    # ---- 8. the wings: advanced sets that already exist -------------------------------------------------
    wings = {}
    for w, (rel, want, key) in sorted(WINGS.items()):
        wings[w] = len(json.loads(bytes_at(REPO, rel, want))[key])
    R["wings"] = {"objections_by_wing": wings, "total": sum(wings.values())}

    # ---- 9. the pilot: derived exclusion, stated rule ---------------------------------------------------
    jrows = json.loads(load("pq_judgments"))["rows"]
    drows = json.loads(load("pq_drafts"))["rows"]
    src = [r for r in jrows if r.get("id") in FLUX_JUDGMENT_ROWS] + \
          [r for r in drows if str(r.get("id", "")).startswith(FLUX_DRAFT_PREFIX)]
    assert sorted(r["id"] for r in src if r["id"] in FLUX_JUDGMENT_ROWS) == sorted(FLUX_JUDGMENT_ROWS)
    txt = json.dumps(src, ensure_ascii=False)
    flux = sorted(i for i in ids if id_in(txt, i))
    missing = [i for i in X032_NODES if i not in flux]
    assert not missing, "flux derivation missed X-032 nodes: %s" % missing
    elig = [i for i in ids if i not in flux]
    pick = []
    for t in (1, 2, 3, 4, 5):
        cand = sorted((i for i in elig if node[i]["tier"] == t), key=lambda i: (-indeg[i], i))
        if cand:
            pick.append((cand[0], "highest Map 1 in-degree in T%d" % t))
    att_best = sorted(elig, key=lambda i: (-len(nonexact[i]), -indeg[i], i))[0]
    if att_best not in [p for p, _ in pick]:
        pick.append((att_best, "most attested non-exact deployments among stable nodes (%d)" % len(nonexact[att_best])))
    R["pilot"] = {
        "rule": ("exclude nodes named by a pending pin-queue finding (X-032, X-033, X-034, PF-*); then, for each "
                 "tier, the stable node the three Next Move characters reach most often (Map 1 in-degree); then the "
                 "stable node with the most attested non-exact deployments, if not already chosen"),
        "in_flux": flux,
        "eligible": len(elig),
        "eligible_with_2plus_attested_nonexact": sorted(i for i in elig if len(nonexact[i]) >= 2),
        "nodes": [{"id": i, "why": why, "tier": node[i]["tier"], "map1_in_degree": indeg[i],
                   "attested_nonexact": sorted(nonexact[i]), "attested_exact": len(exact[i]),
                   "trigger_phrasings": len(phr[i]), "keywords": len(node[i]["keywords"]),
                   "strong_premises": strong[i], "has_archetypeVariants": i in av,
                   "variant_slots": sorted(av.get(i, {})),
                   "has_note": bool(node[i].get("note"))} for i, why in pick],
        "rwe_concentration": {
            "nonexact_attachments_total": sum(len(v) for v in nonexact.values()),
            "nonexact_attachments_on_in_flux_nodes": sum(len(nonexact[i]) for i in flux)},
    }

    # ---- 10. cost anchors (measured) and the estimate (planning constants x measured anchors) ------------
    R["cost"] = {
        "anchors_words_per_unit": {
            "archetype_variant_slot_mean": R["archetypeVariants"]["words_per_slot"]["mean"],
            "scholar_objection_mean": R["game"]["scholar_layer"]["words"]["mean"],
            "layman_trigger_mean": R["surfaces"]["layman_trigger_words"]["mean"],
            "map_move_mean_class_a": R["adversarial_map_v1_6"]["move_words_by_class"]["a"]["mean"],
            "trigger_phrasing_mean": R["corpus"]["trigger_phrasing_words"]["mean"]},
        "existing_layer_totals_words": {
            "archetypeVariants": R["archetypeVariants"]["words_per_slot"]["total"],
            "scholar_layer": R["game"]["scholar_layer"]["words"]["total"]},
        "estimate": {
            "pilot_shapes": PLAN["pilot_nodes"] * PLAN["shapes_per_node"],
            "pilot_words": PLAN["pilot_nodes"] * PLAN["shapes_per_node"] * PLAN["words_per_shape"],
            "full_shapes": len(obs) * PLAN["shapes_per_node"],
            "full_words": len(obs) * PLAN["shapes_per_node"] * PLAN["words_per_shape"],
            "full_judging_sessions": -(-len(obs) * PLAN["shapes_per_node"] // PLAN["shapes_per_judging_session"]),
            "full_drafting_sessions": -(-len(obs) * PLAN["shapes_per_node"] // PLAN["shapes_per_judging_session"])},
    }
    return R


def render(R):
    return json.dumps(R, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def main(argv):
    text = render(measure())
    if "--check" in argv:
        have = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if have != text:
            print("RED: measure_variations_v0_1.json differs from a fresh measurement")
            return 1
        print("GREEN: measure_variations_v0_1.json reproduces (md5 %s)" % md5(text.encode()))
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote %s (md5 %s, %d bytes)" % (os.path.relpath(OUT, REPO), md5(text.encode()), len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
