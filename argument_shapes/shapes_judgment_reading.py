#!/usr/bin/env python3
"""shapes_judgment_reading.py -- gate2's reading instrument for the argument-shapes pilot (V3, 2026-10-03).

Recomputes, with its own code, every figure the judgment record states as measured. It reads each artifact at the
md5 the record pins (working tree or git history, via adversarial_map_staging/r1/pinned.py) and never imports the
drafter's builder (build_shapes_pilot.py) or the shape validator. The judged classes and routes come from the record's
shape rows; everything else comes from the judged artifacts.

What it computes:
  drafted        the pilot's counts, and V2's four measures recomputed (cross-node shares, not shipping as (a), words)
  judged         the same measures over the shapes gate2 kept, with gate2's classes and routes
  collisions     the v0_2 collision rule run fresh on map v1_8: every (b) or (d) at an answering locus, at any other
                 slot of an answering node, or on the shape's own node
  bedrock        each (d)'s bedrock, drafted and judged, set against the map entry at its via and the register's facet
  anchors        every answering anchor: verbatim at its corpus locus, and its word count
  lexical_floor  TF-IDF neighbours of each shape over every node's trigger, layman line and scholar line. A floor, not a
                 census: it names candidates to read, and it can miss the node a shape belongs to.
  reserved       love-from-the-void's modal move (R0296) in any statement
  safety         self-harm, suicide and homicide words in any statement

The scholar lines live in the game's repository; they are read through `git show` at the commit the record pins, so
this instrument needs that repository on the machine (exit 2 without it).

  python3 argument_shapes/shapes_judgment_reading.py [--check | --write]
"""
import hashlib, json, math, os, re, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402

RECORD = "argument_shapes/shapes_pilot_judgments.json"
OUT = "argument_shapes/shapes_judgment_reading_v0_1.json"
DUMP = dict(indent=1, ensure_ascii=False)
SLOTS = ("short", "medium", "long")
TERMS = ("golden rule", "skeptical theism", "soul-making", "universalis", "heroi", "Morioka")
RESERVED = re.compile(r"not (?:be )?impossible|not illogical|isn't impossible|isn't illogical", re.I)
SAFETY = re.compile(r"\b(?:suicid\w*|kill\w*|self-harm\w*|murder\w*|homicid\w*|die|dies|dying|death)\b", re.I)
STOP = set(("a an the of to and or in on is are be it its that this for as by with not no but if so than then what who "
            "whom which their there they them we you your our us i me my he his him she her was were has have had do "
            "does did can could would should will may might must one any all every each more most less into from at "
            "about such only also just own same other another").split())


def md5b(b):
    return hashlib.md5(b).hexdigest()


def load(pin):
    return json.loads(pinned.bytes_at(REPO, pin["file"], pin["md5"]).decode("utf-8"))


def scholar(pin):
    try:
        b = subprocess.run(["git", "-C", os.path.expanduser(pin["repo"]), "show", "%s:%s" % (pin["commit"], pin["file"])],
                           capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        print("READING: the scholar file is not readable here (%s at %s)" % (pin["file"], pin["commit"][:8]))
        sys.exit(2)
    assert md5b(b) == pin["md5"], "scholar file at %s is not %s" % (pin["commit"][:8], pin["md5"])
    return json.loads(b.decode("utf-8"))


def locus_text(node, locus):
    r = node["responses"]
    if locus in SLOTS:
        return r[locus]
    if locus.startswith("archetypeVariants."):
        return r["archetypeVariants"][locus.split(".", 1)[1]]
    raise KeyError(locus)


def wc(s):
    return len(s.split())


def answer_nodes(route):
    if not route:
        return []
    if "via" in route:
        return [route["via"].split("#")[0]]
    return [a["locus"].split("#")[0] for a in route.get("answered_by", [])]


def share(rows, own):
    routed = [(sid, nodes) for sid, nodes in rows if nodes]
    cross = [sid for sid, nodes in routed if any(n != own[sid] for n in nodes)]
    return "%d of %d" % (len(cross), len(routed))


def words(stmts):
    w = [wc(s) for s in stmts]
    return {"min": min(w), "max": max(w), "mean": round(sum(w) / len(w), 1), "n": len(w)}


def collisions(M, sid, own, nodes, loci):
    """The v0_2 rule: (b)/(d) entries at answering loci, at other slots of answering nodes, and on the own node."""
    out = []
    for i, e in enumerate(M["entries"]):
        if e["class"] not in ("b", "d"):
            continue
        where = "%s#%s" % (e["target_id"], e["target_locus"])
        why = ("at the answering locus" if where in loci else "another slot of an answering node"
               if e["target_id"] in nodes else "the shape's own node" if e["target_id"] == own else None)
        if why:
            out.append({"entry": i, "node": e["target_id"], "locus": e["target_locus"], "class": e["class"],
                        "anchor": e["target_anchor"], "why": why})
    return out


def bedrock_check(M, Rg, via, via_anchor, claimed):
    node, locus = via.split("#")
    hits = [(i, e) for i, e in enumerate(M["entries"]) if e["target_id"] == node and e["target_locus"] == locus
            and e["class"] == "d" and e["target_anchor"] == via_anchor]
    if len(hits) != 1:
        return {"via": via, "map_entry": None, "ok": False}
    i, e = hits[0]
    res = e["routing"]["residue"]
    reg = None
    for b in Rg["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                if t["node"] == node and t["locus"] == locus and t["anchor"] == via_anchor:
                    reg = {"bedrock_id": b["bedrock_id"], "name": b["name"], "facet": f["facet_id"]}
    out = {"via": via, "map_entry": i, "bedrock_name": res["bedrock_name"], "terminus_routing": res["terminus_routing"],
           "register": reg}
    out["ok"] = bool(reg) and claimed.get("bedrock_name") == res["bedrock_name"] and \
        claimed.get("terminus_routing") == res["terminus_routing"] and claimed.get("register") == reg
    return out


def tfidf_floor(C, L, S, shapes):
    def toks(s):
        return [w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2]
    docs = {o["id"]: toks(o["trigger"] + " " + L[o["id"]]["layman_trigger"] + " " + S[o["id"]]["scholar_objection"])
            for o in C["objections"]}
    df = Counter()
    for d in docs.values():
        df.update(set(d))
    n = len(docs)
    idf = {w: math.log((n + 1) / (df[w] + 1)) + 1 for w in df}

    def vec(t):
        tf = Counter(t)
        return {w: tf[w] * idf.get(w, math.log(n + 1) + 1) for w in tf}

    def cos(a, b):
        num = sum(a[w] * b.get(w, 0) for w in a)
        return num / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) or 1)
    dv = {i: vec(d) for i, d in docs.items()}
    out, orders = {}, {}
    for s in shapes:
        v = vec(toks(s["statement"] + " " + s["differs_by"]))
        ranked = sorted(((round(cos(v, dv[i]), 4), i) for i in dv), key=lambda x: (-x[0], x[1]))
        orders[s["shape_id"]] = [i for _, i in ranked]
        own = s["shape_id"].split("/")[0]
        out[s["shape_id"]] = {"top5": [[i, x] for x, i in ranked[:5]],
                              "rank_of": {own: orders[s["shape_id"]].index(own) + 1}}
    return out, orders


def main():
    rec = json.loads(open(os.path.join(REPO, RECORD), encoding="utf-8").read())
    J = rec["judged"]
    P, Ms, C, M, Rg, L = (load(J[k]) for k in ("pilot", "measure", "corpus", "map_v1_8", "register_v0_9", "layman"))
    S = {n["id"]: n for n in scholar(J["scholar"])["nodes"]}
    L = {n["id"]: n for n in L["nodes"]}
    O = {o["id"]: o for o in C["objections"]}
    shapes = P["shapes"]
    own = {s["shape_id"]: s["shape_id"].split("/")[0] for s in shapes}
    meas = {m["shape_id"]: m for m in Ms["shapes"]}

    # drafted: V2's measures, recomputed
    def drafted_nodes(s):
        m = meas[s["shape_id"]]
        if s["answered_by"]:
            return [a["locus"].split("#")[0] for a in s["answered_by"]]
        return [m["terminus"]["via"].split("#")[0]] if "terminus" in m else []
    dn = [(s["shape_id"], drafted_nodes(s)) for s in shapes]
    drafted = {"shapes": len(shapes), "nodes": len(set(own.values())),
               "classes": dict(sorted(Counter(s["class"] for s in shapes).items())),
               "a_cross_node": share([x for x in dn if next(s for s in shapes if s["shape_id"] == x[0])["class"] == "a"], own),
               "routed_cross_node": share(dn, own),
               "not_shipping_as_a": "%d of %d" % (sum(s["class"] != "a" for s in shapes), len(shapes)),
               "words": words([s["statement"] for s in shapes])}

    # judged: gate2's classes and routes, from the record's shape rows (latest row per shape)
    rows = {}
    for r in rec["rows"]:
        if r["kind"] == "shape":
            rows[r["shape_id"]] = r
    kept = [s for s in shapes if rows[s["shape_id"]]["verdict"] != "REJECT"]
    jn = [(s["shape_id"], answer_nodes(rows[s["shape_id"]]["route"])) for s in kept]
    judged = {"kept": len(kept), "rejected": sorted(s["shape_id"] for s in shapes if s not in kept),
              "classes": dict(sorted(Counter(rows[s["shape_id"]]["class_judged"] for s in kept).items())),
              "per_node": dict(sorted(Counter(own[s["shape_id"]] for s in kept).items())),
              "a_cross_node": share([x for x in jn if rows[x[0]]["class_judged"] == "a"], own),
              "routed_cross_node": share(jn, own),
              "not_shipping_as_a_of_drafted": "%d of %d" % (sum(rows[s["shape_id"]]["class_judged"] != "a"
                                                              for s in shapes), len(shapes)),
              "not_shipping_as_a_of_kept": "%d of %d" % (sum(rows[s["shape_id"]]["class_judged"] != "a"
                                                           for s in kept), len(kept)),
              "words_kept": words([s["statement"] for s in kept])}

    # collisions, fresh, for every shape the drafter routed through answering loci
    coll, match = {}, {}
    for s in shapes:
        if not s["answered_by"]:
            continue
        loci = {a["locus"] for a in s["answered_by"]}
        nodes = {x.split("#")[0] for x in loci}
        c = collisions(M, s["shape_id"], own[s["shape_id"]], nodes, loci)
        coll[s["shape_id"]] = c
        theirs = sorted((x["node"], x["locus"], x["class"], x["anchor"]) for x in meas[s["shape_id"]].get("machine_collisions", []))
        match[s["shape_id"]] = theirs == sorted((x["node"], x["locus"], x["class"], x["anchor"]) for x in c)

    # bedrock: the drafter's (d)s and gate2's (d)s
    bed = {"drafted": {}, "judged": {}}
    for s in shapes:
        t = meas[s["shape_id"]].get("terminus")
        if t:
            bed["drafted"][s["shape_id"]] = bedrock_check(M, Rg, t["via"], t["via_anchor"], {
                "bedrock_name": t["bedrock_name"], "terminus_routing": t["terminus_routing"],
                "register": t["register"] and {"bedrock_id": t["register"]["bedrock_id"], "name": t["register"]["name"],
                                               "facet": t["register"]["facet"]}})
        r = rows[s["shape_id"]]
        if r["verdict"] != "REJECT" and r["class_judged"] == "d":
            bed["judged"][s["shape_id"]] = bedrock_check(M, Rg, r["route"]["via"], r["route"]["via_anchor"], r["route"]["bedrock"])

    # anchors: drafted answered_by and judged answered_by / via anchors
    anchors = {}
    for s in shapes:
        al = [(a["locus"], a["anchor"]) for a in s["answered_by"]]
        r = rows[s["shape_id"]]
        if r["route"] and "answered_by" in r["route"]:
            al += [(a["locus"], a["anchor"]) for a in r["route"]["answered_by"]]
        if r["route"] and "via" in r["route"]:
            al.append((r["route"]["via"], r["route"]["via_anchor"]))
        seen, out = set(), []
        for loc, anc in al:
            if (loc, anc) in seen:
                continue
            seen.add((loc, anc))
            node, locus = loc.split("#")
            out.append({"locus": loc, "anchor": anc, "verbatim": anc in locus_text(O[node], locus), "words": wc(anc)})
        anchors[s["shape_id"]] = out

    floor, orders = tfidf_floor(C, L, S, shapes)
    for sid, r in rows.items():
        if r.get("belongs_to"):
            floor[sid]["rank_of"][r["belongs_to"]] = orders[sid].index(r["belongs_to"]) + 1

    out = {"what": "gate2's reading of the argument-shapes pilot (V3, 2026-10-03): every figure the judgment record "
                   "states as measured, recomputed from the judged artifacts at their pinned md5s",
           "reads": {k: J[k]["md5"] for k in ("pilot", "measure", "corpus", "map_v1_8", "register_v0_9", "layman", "scholar")},
           "figures": {"drafted": drafted, "judged": judged,
                       "collisions_v0_2": coll, "collisions_match_the_measure": match,
                       "bedrock": bed, "anchors": anchors, "lexical_floor": floor,
                       "corpus_term_hits": {t: sum(len(re.findall(re.escape(t), x, re.I)) for o in C["objections"]
                                                   for x in [o["trigger"], o["diagnosis"] or ""] + [
                                                       v if isinstance(v, str) else json.dumps(v)
                                                       for v in o["responses"].values()]) for t in TERMS},
                       "reserved_move_hits": sorted(s["shape_id"] for s in shapes if RESERVED.search(s["statement"])),
                       "safety_word_hits": {s["shape_id"]: SAFETY.findall(s["statement"]) for s in shapes
                                            if SAFETY.search(s["statement"])}}}
    b = (json.dumps(out, **DUMP) + "\n").encode("utf-8")
    path = os.path.join(REPO, OUT)
    if "--write" in sys.argv:
        open(path, "wb").write(b)
        print("READING: wrote %s %s / %d" % (OUT, md5b(b), len(b)))
    elif "--check" in sys.argv:
        ok = os.path.exists(path) and open(path, "rb").read() == b
        print("READING RECORD: %s" % ("matches the committed record" if ok else "DIFFERS from the committed record"))
        sys.exit(0 if ok else 1)
    else:
        sys.stdout.write(b.decode("utf-8"))


if __name__ == "__main__":
    main()
