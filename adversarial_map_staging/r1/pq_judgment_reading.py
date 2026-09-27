#!/usr/bin/env python3
"""pq_judgment_reading.py -- gate2's reading instrument for its judgment of the pin session's drafts
(gate2, 2026-09-26, R0175).

Every figure the judgment record (PQ_repair_drafts_judgments.json) states as measured, recomputed from the
judged artifacts at the md5s they are pinned to, never from the working tree, so it still reproduces after the
pin moves the corpus and after the drafts record grows by appended rows:

  knock_on_independent  the entries of map v1_6 anchored inside a repaired sentence (and, of those, the ones whose
                        anchor also occurs outside it, so the repair does not move them), and the (a) entries whose
                        answer routes to a repaired locus, with each one's current R1 verdict; compared, as sets,
                        with the drafts' knock-on record (PQ_knock_on_L5_v0_1.json)
  confinement           the post-pin corpus the pin session's own patch tool builds (tools/pin_patch_l5.py at its
                        pinned bytes, every draft and companion) differs from the pre-pin corpus at exactly the
                        repaired loci, and at each one only by the rows' replacements
  holds                 the five HOLDS whose answers route to a repaired locus: the loci and sentences the
                        judgment reads each one as resting on, and whether each stands in the post-pin text
  sibling_loci          named patterns for the defects this pin repairs, swept over the post-pin corpus
  exit_framing          named patterns that frame the survival drive as a barrier to exit, swept over the pre-pin
                        and the post-pin corpus; the two sweeps must agree (the pin neither adds nor removes one)

  python3 pq_judgment_reading.py            # print the record
  python3 pq_judgment_reading.py --emit     # write the record beside this file
  python3 pq_judgment_reading.py --check    # compare with the committed record; exit 1 on any difference

Repo-relative. Writes nothing unless --emit is given. Deterministic: every listing is in file or corpus order.
"""
import copy, json, os, re, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/pq_judgment_reading_v0_1.json"
DRAFTS = ("adversarial_map_staging/r1/PQ_repair_drafts_L5.json", "0819125d28c58561bcda42570181e105")
KNOCK = ("adversarial_map_staging/r1/PQ_knock_on_L5_v0_1.json", "b20fdef1ba8d600a49a4cc8a18163ac3")
MAP = ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed")
RULINGS = ("adversarial_map_staging/r1/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74")
EVID = ("adversarial_map_staging/r1/R1_evidence_2026-09-19.json", "719b5ddb27680f32181a8a953c84b6c2")
PATCH = ("tools/pin_patch_l5.py", "092b9adc7cfbac33ed0f99d2b6170bb5")
CORPUS = "efilist_argument_library_v4_0_0.json"

# The judgment's reading of what each HOLDS rests on (X-030): a locus, and a sentence where the ruling names one.
HOLDS = [
    (24, "just-depressed#long", "The claim is symmetric and modest"),
    (49, "joy-outweighs-harms#long", None),
    (52, "economy-population#long", None),
    (53, "hedonic-contrast#long", None),
    (53, "transhumanist-objection#long", None),
    (18, "violence-as-reductio#archetypeVariants.sophisticate", "Concede the one residue this does not reach"),
]
SIBLING = [
    ("consent-asymmetry read as a general ban on imposition",
     r"maximally non-consensual|maximal such imposition|exact same principle of consent|framework-self-undermining"
     r"|swapped the (?:premise|engine)"),
    ("the lone-actor analogy", r"one violent actor|single violent actor|Unabomber"),
    ("grabbed, not produced", r"grabbed[-, ]+not[-, ]+produced"),
    ("the calculation as the safeguard", r"structural safeguard is not a rule|cascade-math-safeguard then shows"),
    ("clearer sight", r"seeing without the anaesthetic|he is the more reliable one"),
    ("motive frequency", r"Genuine concern is the rare exception"),
]
EXIT = [r"barriers? to exit", r"exit barriers", r"trap(?:s|ped)? (?:conscious beings|by (?:their|its) own survival|by them)",
        r"body vetoes the mind", r"only 'exit' from existence is death", r"graceful exit", r"failure rate of suicide attempts",
        r"It is a trap\.", r"recruited into the same firmware and then trapped"]


def load(pin):
    return json.loads(pinned.bytes_at(REPO, pin[0], pin[1]).decode("utf-8"))


def patch_module():
    """tools/pin_patch_l5.py at its pinned bytes, run as a module (never the working copy)."""
    m = types.ModuleType("pin_patch_l5_pinned")
    m.__file__ = os.path.join(REPO, PATCH[0])
    exec(compile(pinned.bytes_at(REPO, PATCH[0], PATCH[1]).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def loci(o):
    """Every text locus of an objection, in file order: responses (short, medium, long, variants), then note."""
    r = o["responses"]
    for k, v in r.items():
        if k == "archetypeVariants":
            for s, t in (v or {}).items():
                if isinstance(t, str):
                    yield "archetypeVariants." + s, t
        elif isinstance(v, str):
            yield k, v
    for k in ("note", "diagnosis"):
        if isinstance(o.get(k), str):
            yield k, o[k]


def text_map(corpus):
    return {"%s#%s" % (o["id"], loc): t for o in corpus["objections"] for loc, t in loci(o)}


def sweep(tm, patterns):
    out = []
    for key, t in tm.items():
        for p in patterns:
            for m in re.finditer(p, t):
                out.append({"locus": key, "match": m.group(0)})
    return out


def measure():
    rec = load(DRAFTS)
    P = patch_module()
    rows = P.select(rec, "all")
    pre_corpus = json.loads(pinned.bytes_at(REPO, CORPUS, rec["pinned"]["surfaces"][CORPUS]).decode("utf-8"))
    out, change = P.build(rec, rows, repo=REPO)
    post_corpus = json.loads(out[CORPUS])
    pre, post = text_map(pre_corpus), text_map(post_corpus)
    by_locus = {}
    for r in rows:
        by_locus.setdefault(r["locus"], []).append(r)

    # confinement
    changed = [k for k in pre if pre[k] != post.get(k)]
    conf = []
    for locus, rs in by_locus.items():
        want = pre[locus]
        for r in rs:
            want = want.replace(r["current"], r["replacement"], 1)
        conf.append({"locus": locus, "rows": [r["id"] for r in rs],
                     "each_current_once_before": all(pre[locus].count(r["current"]) == 1 for r in rs),
                     "post_is_pre_with_the_replacements": post[locus] == want})
    confinement = {"repaired_loci": len(by_locus), "rows": len(rows), "changed_loci": len(changed),
                   "changed_loci_are_the_repaired_loci": sorted(changed) == sorted(by_locus),
                   "loci_added_or_removed": sorted(set(pre) ^ set(post)), "per_locus": conf}

    # knock-on, independently
    m = load(MAP)
    ev = {(e["target_id"], e["target_locus"], e["target_anchor"]): e["n"] for e in load(EVID)["entries"]}
    rr = load(RULINGS)["rows"]
    sup = {r["supersedes"] for r in rr if r.get("supersedes")}
    verdict = {r["n"]: (r["row"], r["verdict"]) for r in rr if r["row"] not in sup}
    inside, routes = [], []
    for e in m["entries"]:
        key = "%s#%s" % (e["target_id"], e["target_locus"])
        rs = by_locus.get(key, [])
        hit = [r["id"] for r in rs if e["target_anchor"] in r["current"]]
        if hit:
            n_locus = pre[key].count(e["target_anchor"])
            n_in = sum(r["current"].count(e["target_anchor"]) for r in rs)
            inside.append({"locus": key, "class": e["class"], "anchor": e["target_anchor"], "rows": hit,
                           "occurrences_in_locus": n_locus, "moves_with_the_repair": n_locus == n_in})
        if e["class"] == "a":
            for loc in e.get("routing", {}).get("answered_by", []):
                if loc in by_locus:
                    n = ev.get((e["target_id"], e["target_locus"], e["target_anchor"]))
                    row, v = verdict.get(n, (None, None))
                    routes.append({"routed_to": loc, "target": key, "anchor": e["target_anchor"], "n": n,
                                   "ruling_row": row, "verdict": v})
    k = load(KNOCK)
    rec_inside = sorted((r["locus"], r["anchor"]) for r in k["rows"] if r["kind"] == "anchor_inside")
    rec_routes = sorted((r["locus"], r["target"], r["anchor"]) for r in k["rows"] if r["kind"] == "answer_routes_here")
    moved = [x for x in inside if x["moves_with_the_repair"]]
    knock = {
        "anchor_inside_a_repaired_sentence": len(inside), "anchor_inside": len(moved),
        "anchor_inside_but_also_outside": [x for x in inside if not x["moves_with_the_repair"]],
        "answer_routes_here": len(routes),
        "holds": sorted({x["n"] for x in routes if x["verdict"] == "HOLDS"}),
        "fails": sorted({x["n"] for x in routes if x["verdict"] == "FAILS"}),
        "anchor_inside_matches_record": sorted((x["locus"], x["anchor"]) for x in moved) == rec_inside,
        "answer_routes_here_matches_record": sorted((x["routed_to"], x["target"], x["anchor"]) for x in routes) == rec_routes,
        "quoted_in_map": "not reproduced here (L5's shingle match); pin_repair_drafts_gate.py recomputes it",
        "inside": inside, "routes": routes,
    }

    # the five HOLDS
    holds = []
    for n, locus, sentence in HOLDS:
        x = {"n": n, "verdict": verdict.get(n, (None, None))[1], "rests_on": locus, "locus_repaired": locus in by_locus}
        if sentence is not None:
            spans = [r["replacement"] for r in by_locus.get(locus, [])] + [r["current"] for r in by_locus.get(locus, [])]
            x.update(sentence=sentence, stands_after_the_pin=post[locus].count(sentence) == 1,
                     outside_every_repaired_span=not any(sentence in s for s in spans))
        holds.append(x)

    sib = []
    for name, p in SIBLING:
        hits = sweep(post, [p])
        sib.append({"defect": name, "pattern": p, "loci": sorted({h["locus"] for h in hits}, key=list(post).index),
                    "hits": hits})
    ex_pre, ex_post = sweep(pre, EXIT), sweep(post, EXIT)
    exit_framing = {"patterns": EXIT, "pre_equals_post": ex_pre == ex_post, "hits": ex_post,
                    "loci": sorted({h["locus"] for h in ex_post}, key=list(post).index)}
    exit_framing["nodes"] = sorted({l.split("#")[0] for l in exit_framing["loci"]})

    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/pq_judgment_reading.py",
        "reads": {"drafts": DRAFTS[1], "knock_on": KNOCK[1], "map_v1_6": MAP[1], "rulings": RULINGS[1],
                  "evidence": EVID[1], "patch_tool": PATCH[1], "corpus": rec["pinned"]["surfaces"][CORPUS],
                  "set": "all: %d rows (%s)" % (len(rows), ", ".join(r["id"] for r in rows))},
        "knock_on_independent": knock,
        "confinement": confinement,
        "holds": holds,
        "sibling_loci": sib,
        "exit_framing": exit_framing,
    }


def main():
    fresh = (json.dumps(measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    path = os.path.join(REPO, RECORD)
    if "--emit" in sys.argv:
        open(path, "wb").write(fresh)
        print("wrote %s  %s / %d" % (RECORD, pinned.md5(fresh), len(fresh)))
    elif "--check" in sys.argv:
        same = os.path.exists(path) and open(path, "rb").read() == fresh
        print("READING RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        sys.exit(0 if same else 1)
    else:
        sys.stdout.write(fresh.decode("utf-8"))


if __name__ == "__main__":
    main()
