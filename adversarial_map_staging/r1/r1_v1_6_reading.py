#!/usr/bin/env python3
"""r1_v1_6_reading.py -- the measurements gate2's judgment of v1_6 rests on (gate2, 2026-09-26).

R1_v1_6_judgments.json judges #46's (d), register v0_7, the knock-on measure, PQ-17 and the
pin session's declaration. Every figure its rows lean on is recomputed here from the artifacts it
judged, each read at the md5 it pins (from git history once the working copy moves), and written to
r1_v1_6_reading_v0_1.json:

  - map: which entries of v1_6 differ from v1_5, and in which fields;
  - register: whether v0_7 is v0_6 plus exactly the tributaries it adds;
  - knock-on, measured independently of l4c_knock_on.py: the (a) entries of v1_6 on, or routed to,
    red-button-repugnant, and the current R1 verdicts of all (a) entries;
  - #46's bedrock: whether its bedrock name is the one the sophisticate (d) it copies carries;
  - PQ-17: how often its named sentence, and the lone-actor sentence after it, occur on each of the
    three surfaces; whether R1-024 names the analogy; #4's map anchor and whether it lies in that
    sentence; where 'grabbed, not produced' occurs in the corpus.

  python3 r1_v1_6_reading.py            # print, write nothing
  python3 r1_v1_6_reading.py --emit     # write r1_v1_6_reading_v0_1.json beside this file
  python3 r1_v1_6_reading.py --check    # exit 1 unless the committed record equals a fresh run

Repo-relative. Deterministic: no set iteration reaches the output.
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, "r1_v1_6_reading_v0_1.json")
STG = "adversarial_map_staging/"
PINS = {
    "map_v1_5": (STG + "adversarial_map_v1_5.json", "0df413ed655a5373468c218832854bbe"),
    "map_v1_6": (STG + "adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "register_v0_6": (STG + "honest_residuals_register_v0_6.json", "0689f46f18a4dbe8d40c9982a2ad06f9"),
    "register_v0_7": (STG + "honest_residuals_register_v0_7.json", "bcbff23113f3fb0135d5fd5b3e2630d5"),
    "rulings": (STG + "r1/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74"),
    "canon": ("project_canon_v38_28.json", "d9d0c23a9e47bd1cc38f69a378c2198f"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "04bf6482aa0374ee92a81c1d55ec41f8"),
    "jsx": ("efilist_argument_library_v4_0_0.jsx", "b196548b6eb39065842d62292acca89f"),
    "combined": ("site/combined.html", "006aa9833f7a8b103ad27a289ab22fa9"),
}
NODE = "red-button-repugnant"
LONE_ACTOR = ("Just as one violent actor does not represent environmentalism, an eliminationist adherent does not "
              "convert the consent-and-asymmetry argument into a suicide license.")
PHRASE = "grabbed, not produced"


def pinned(key):
    rel, want = PINS[key]
    p = os.path.join(REPO, rel)
    if os.path.exists(p):
        b = open(p, "rb").read()
        if hashlib.md5(b).hexdigest() == want:
            return b
    log = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", rel], capture_output=True, text=True)
    for sha in log.stdout.split():
        r = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (sha, rel)], capture_output=True)
        if r.returncode == 0 and hashlib.md5(r.stdout).hexdigest() == want:
            return r.stdout
    sys.exit("REFUSED: %s at %s is not in the working tree or git history" % (rel, want))


def js(key):
    return json.loads(pinned(key).decode("utf-8"))


def paths_with(o, needle, path=""):
    if isinstance(o, dict):
        for k in o:
            yield from paths_with(o[k], needle, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from paths_with(v, needle, path + "[%d]" % i)
    elif isinstance(o, str) and needle in o:
        yield path


def measure():
    m5, m6 = js("map_v1_5"), js("map_v1_6")
    e5, e6 = m5["entries"], m6["entries"]
    assert len(e5) == len(e6)
    changed = []
    for i, (a, b) in enumerate(zip(e5, e6)):
        if a != b:
            changed.append({"index": i, "target": "%s#%s" % (a["target_id"], a["target_locus"]),
                            "fields_changed": sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k)),
                            "fields_unchanged": sorted(k for k in a if k in b and a[k] == b[k])})

    r6, r7 = js("register_v0_6"), js("register_v0_7")
    b6 = {b["bedrock_id"]: b for b in r6["bedrocks"]}
    b7 = {b["bedrock_id"]: json.loads(json.dumps(b)) for b in r7["bedrocks"]}
    added = []
    for bid in sorted(b7):
        f6 = {f["facet_id"]: f["tributaries"] for f in b6.get(bid, {}).get("facets", [])}
        for f in b7[bid]["facets"]:
            new = [t for t in f["tributaries"] if t not in f6.get(f["facet_id"], [])]
            for t in new:
                added.append({"bedrock": bid, "facet": f["facet_id"], "node": t["node"], "locus": t["locus"]})
            f["tributaries"] = [t for t in f["tributaries"] if t not in new]
        b7[bid]["tributary_count"] -= sum(1 for x in added if x["bedrock"] == bid)
    register = {"tributaries_added": added,
                "v0_7_minus_added_equals_v0_6": sorted(b7) == sorted(b6) and all(b7[k] == b6[k] for k in b6),
                "audit_unchanged": r6["audit"] == r7["audit"],
                "hr14_relations": [[x["kind"], x["to"]] for x in b7["HR-14"]["relations"]]}

    rows = js("rulings")["rows"]
    sup = {r["supersedes"] for r in rows if r.get("supersedes")}
    cur = {r["n"]: r for r in rows if r["row"] not in sup}
    a6 = [e for e in e6 if e["class"] == "a"]
    target_of = {r["target"]: r for r in cur.values()}
    on_or_to = []
    for e in a6:
        answered = e.get("routing", {}).get("answered_by") or []
        if e["target_id"] == NODE or any(x.split("#")[0] == NODE for x in answered):
            on_or_to.append("%s#%s" % (e["target_id"], e["target_locus"]))
    verdicts = {}
    for e in a6:
        r = target_of.get("%s#%s" % (e["target_id"], e["target_locus"]))
        v = r["verdict"] if r else "UNRULED"
        verdicts[v] = verdicts.get(v, 0) + 1
    knock = {"a_entries": len(a6), "a_on_or_routed_to_node": on_or_to,
             "current_r1_verdicts_of_a_entries": dict(sorted(verdicts.items()))}

    by_anchor = {(e["target_locus"], e["target_anchor"]): e for e in e6 if e["target_id"] == NODE}
    d46 = next(e for e in e6 if e["target_id"] == NODE and e["target_locus"] == "archetypeVariants.defender")
    soph = by_anchor[("archetypeVariants.sophisticate", "this node's terminus to hold open rather than pretend closed")]
    bedrock = {"n46_class": d46["class"], "n46_bedrock_name": d46["routing"]["residue"]["bedrock_name"],
               "equals_sophisticate_d": d46["routing"]["residue"]["bedrock_name"] ==
               soph["routing"]["residue"]["bedrock_name"],
               "node_entries": [{"locus": e["target_locus"], "class": e["class"],
                                 "bedrock_name": (e.get("routing", {}).get("residue") or {}).get("bedrock_name")}
                                for e in e6 if e["target_id"] == NODE]}

    q = js("canon")["adversarial_map"]["pin_move_queue_v1_6"]
    pq17 = next(r for r in q["rows"] if r["id"] == "PQ-17")
    surf = {k: pinned(k).decode("utf-8") for k in ("corpus", "jsx", "combined")}
    corpus = js("corpus")
    wns = next(o for o in corpus["objections"] if o["id"] == "why-not-suicide")
    slot = wns["responses"]["archetypeVariants"]["defender"]
    anchor4 = next(e["target_anchor"] for e in e6 if e["target_id"] == "why-not-suicide"
                   and e["target_locus"] == "archetypeVariants.defender")
    pq = {"rows_in_queue": len(q["rows"]),
          "pq17_locus": pq17["locus"], "pq17_serves": pq17["serves"],
          "named_sentence_per_surface": {k: t.count(pq17["sentence"]) for k, t in surf.items()},
          "lone_actor_sentence_per_surface": {k: t.count(LONE_ACTOR) for k, t in surf.items()},
          "both_in_the_defender_slot": pq17["sentence"] in slot and LONE_ACTOR in slot,
          "lone_actor_follows_named": slot.find(LONE_ACTOR) > slot.find(pq17["sentence"]) >= 0,
          "r1_024_names_the_analogy": "lone-actor analogy" in next(r for r in rows if r["row"] == "R1-024")["reason"],
          "n4_anchor": anchor4, "n4_anchor_in_lone_actor_sentence": anchor4 in LONE_ACTOR,
          "phrase_paths_in_corpus": list(paths_with(corpus, PHRASE))}
    return {"artifact": os.path.basename(OUT), "instrument": "adversarial_map_staging/r1/r1_v1_6_reading.py",
            "pins": {k: v[1] for k, v in PINS.items()}, "map": {"changed_entries": changed,
            "meta_keys_changed": sorted(k for k in set(m5["meta"]) | set(m6["meta"])
                                        if m5["meta"].get(k) != m6["meta"].get(k))},
            "register": register, "knock_on_independent": knock, "n46_bedrock": bedrock, "pq17": pq}


def main():
    rec = measure()
    out = (json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    if "--check" in sys.argv:
        same = os.path.exists(OUT) and open(OUT, "rb").read() == out
        print("READING RECORD: %s" % ("matches the committed record" if same else "DIFFERS from a fresh run"))
        sys.exit(0 if same else 1)
    if "--emit" in sys.argv:
        open(OUT, "wb").write(out)
        print("wrote %s  %s / %d" % (os.path.basename(OUT), hashlib.md5(out).hexdigest(), len(out)))
    else:
        sys.stdout.write(out.decode("utf-8"))


if __name__ == "__main__":
    main()
