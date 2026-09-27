#!/usr/bin/env python3
"""l7_judgment_reading.py -- gate2's reading instrument for its judgment of L7's successor-map drafts
(gate2, 2026-09-26, R0237).

Every figure L7_drafts_judgments.json states as measured, recomputed from the judged artifacts at the md5s they are
pinned to, never from the working tree, and never by importing the drafting seat's builder (a judge that reuses the
drafter's code checks the drafter against itself):

  derivation      v1_7 re-derived from v1_6 and the rows: every entry below 138 is v1_6's byte for byte or v1_6's
                  with exactly its row's fields set (a '@from' bedrock copied from the (d) the row names), provenance
                  v1_6's plus successor_L7; every entry from 138 is a filed row's new entry, in row order
  quotes          every declared quotation verbatim at its source; every double-quoted span in a changed or filed field
                  declared in its row
  anchors         how often each changed or filed entry's anchor occurs in its locus of the v4.1.5 corpus
  bedrocks        for each row that copies a bedrock: the copy equals the named (d)'s name; register v0_7 files that
                  (d) under the facet claimed; register v0_8 files the new entry there with the map's routing
  knock_on        the collision rule v0_2 (l4_knock_on.collisions, imported at its pinned bytes) over every (a) left
                  in v1_7: each (b) or (d) it meets in v1_7 that it did not meet in v1_6, the row that made it, and
                  whether the (a)'s own row (if it has one) names it
  new_a_without_r1  (a) entries of v1_7 that are not one of R1's 69 and so carry no R1 verdict
  move_register   corpus-history wording ("now", "in place of", "since withdrawn", "as repaired", ...) in every move
                  of v1_6 and in every move a row drafts
  safety          gate2's X-032 patterns and L6's wide set (both imported at their pinned bytes) over every field a
                  row drafts
  adjacency       every pair of bedrocks that share a node in v1_7, and whether register v0_8 declares it
  wide_after_pin  L6's wide set over the v4.1.5 text of every locus L6 classed queue, sibling or widen: what the
                  safety pass left standing
  honest_eval_family  every v4.1.5 locus that says a drive, programming or bias prevents evaluation or engagement
  validator       v0_7 --assembly on v1_7 against the v4.1.5 corpus, in-process at its pinned bytes

  python3 l7_judgment_reading.py            # print the record
  python3 l7_judgment_reading.py --emit     # write the record beside this file
  python3 l7_judgment_reading.py --check    # compare with the committed record; exit 1 on any difference

Repo-relative. Writes nothing unless --emit is given. Deterministic.
"""
import collections, copy, json, os, re, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/l7_judgment_reading_v0_1.json"
PIN = {
    "drafts": ("adversarial_map_staging/r1/L7_successor_drafts.json", "fd9267f853a5a09fe5aa3972b16fa2a7"),
    "v1_6": ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "v1_7": ("adversarial_map_staging/adversarial_map_v1_7.json", "db40b45693eff1297b3f3152c6295c15"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1"),
    "register_v0_7": ("adversarial_map_staging/honest_residuals_register_v0_7.json", "bcbff23113f3fb0135d5fd5b3e2630d5"),
    "register_v0_8": ("adversarial_map_staging/honest_residuals_register_v0_8.json", "8f6d38886b95033600752a5be052bd99"),
    "rulings": ("adversarial_map_staging/r1/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74"),
    "measure": ("adversarial_map_staging/r1/l7_measure_v0_1.json", "4d98b4a3b5c3a57ef62543001ba7ff64"),
    "validator_v0_7": ("adversarial_map_staging/adv_map_validator_v0_7.py", "8a74dcc452338f127ec03e078090c2ed"),
    "knock_on_tool": ("adversarial_map_staging/r1/l4_knock_on.py", "66022fa8e9ba7ad3ff26e42aee5b0b1c"),
    "exit_patterns": ("adversarial_map_staging/r1/pq_judgment_reading.py", "d11cfbc7182e8fba0f549467b654b1bd"),
    "wide_patterns": ("adversarial_map_staging/r1/sp_reading_l6.py", "dc2525ef40fc5353a670484f511bd668"),
}
FIELDS = ("target_id", "target_locus", "target_anchor", "adversarial_move", "class", "grounds", "routing", "status")
# corpus-history wording in a move: a reader of the v4.1.5 text cannot see the text a repair replaced
HISTORY = [("now", r"\bnow\b"), ("still", r"\bstill (?:calls|says|reads|keeps)\b"), ("in place of", r"\bin place of\b"),
           ("since", r"\bhas since\b"), ("withdrew/withdrawn", r"\bwithdr(?:ew|awn)\b"), ("the repair", r"\bthe repair\b"),
           ("as repaired", r"\bas repaired\b"), ("the old", r"\bthe old\b(?! without)"), ("the new ground", r"\bthe new ground\b")]
HONEST_FAMILY = (r"(?:prevent|distort)\w*\s+(?:honest|systematically distorting|moral judg|the organism from engaging)"
                 r"|systematically distorting moral judgment|prevents honest evaluation")


def module_at(key, name):
    rel, want = PIN[key]
    m = types.ModuleType(name)
    m.__file__ = os.path.join(REPO, rel)
    exec(compile(pinned.bytes_at(REPO, rel, want).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def load(key):
    rel, want = PIN[key]
    return json.loads(pinned.bytes_at(REPO, rel, want).decode("utf-8"))


def lt(node, locus):
    if node is None:
        return None
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    if locus == "note":
        return node.get("note", "")
    if locus == "trigger":
        return node.get("trigger", "")
    if locus.startswith("archetypeVariants."):
        return (node.get("responses", {}).get("archetypeVariants") or {}).get(locus.split(".", 1)[1])
    return node.get("responses", {}).get(locus)


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def split(t):
    node, _, loc = t.partition("#")
    return node, loc


def ek(x):
    return (x["target_id"], x["target_locus"], x["target_anchor"], x["class"])


def measure():
    D, M6, M7 = load("drafts"), load("v1_6"), load("v1_7")
    C = load("corpus")
    R7, R8 = load("register_v0_7"), load("register_v0_8")
    RUL, MEAS = load("rulings"), load("measure")
    nodes = {o["id"]: o for o in C["objections"]}
    e6, e7 = M6["entries"], M7["entries"]
    rows = D["rows"]
    by_i = {r["entry"]["i"]: r for r in rows if r["kind"] == "amend"}
    filed = [r for r in rows if r["kind"] == "file"]
    stands = {r["entry"]["i"]: r for r in rows if r["kind"] == "stands"}
    fail = []

    # ---- derivation ----
    def resolve(r, routing):
        rs = routing.get("residue") if isinstance(routing, dict) else None
        if not rs or rs.get("bedrock_name") != "@from":
            return routing
        bf = r["bedrock_from"]
        node, loc = split(bf["locus"])
        src = [y for y in e6 if y["target_id"] == node and y["target_locus"] == loc
               and y["target_anchor"] == bf["anchor"] and y["class"] == "d"]
        out = copy.deepcopy(routing)
        out["residue"]["bedrock_name"] = src[0]["routing"]["residue"]["bedrock_name"] if len(src) == 1 else None
        return out

    carried, changed = [], []
    for i, x6 in enumerate(e6):
        x7 = e7[i]
        if i not in by_i:
            if json.dumps(x7, sort_keys=True) != json.dumps(x6, sort_keys=True):
                fail.append("entry %d moved without a row" % i)
            carried.append(i)
            continue
        r = by_i[i]
        exp = {k: copy.deepcopy(x6[k]) for k in FIELDS if k in x6}
        for k, v in r["set"].items():
            exp[k] = resolve(r, v) if k == "routing" else v
        got = {k: x7[k] for k in FIELDS if k in x7}
        if json.dumps(exp, sort_keys=True) != json.dumps(got, sort_keys=True):
            fail.append("entry %d (%s) is not v1_6 plus its row's fields" % (i, r["id"]))
        prov = dict(x7["provenance"])
        sl = prov.pop("successor_L7", None)
        if json.dumps(prov, sort_keys=True) != json.dumps(x6["provenance"], sort_keys=True) or not sl or sl.get("row") != r["id"]:
            fail.append("entry %d provenance is not v1_6's plus successor_L7 for %s" % (i, r["id"]))
        changed.append(i)
    new7 = e7[len(e6):]
    if len(new7) != len(filed):
        fail.append("%d entries past v1_6's %d, %d filing rows" % (len(new7), len(e6), len(filed)))
    for r, x7 in zip(filed, new7):
        ne = dict(r["new_entry"])
        ne["routing"] = resolve(r, ne["routing"])
        for k in ne:
            if json.dumps(ne[k], sort_keys=True) != json.dumps(x7.get(k), sort_keys=True):
                fail.append("filed entry for %s differs in %s" % (r["id"], k))
        if x7["provenance"].get("phase") != "H":
            fail.append("filed entry for %s is not phase H" % r["id"])
    cc = lambda es: dict(sorted(collections.Counter(x["class"] for x in es).items()))
    derivation = {"v1_6_entries": len(e6), "v1_7_entries": len(e7), "carried_byte_for_byte": len(carried),
                  "changed": len(changed), "filed": len(new7), "stands_rows_moving_no_byte": len(stands),
                  "class_counts_v1_6": cc(e6), "class_counts_v1_7": cc(e7), "failures": fail[:]}

    # ---- quotes and undeclared spans ----
    def pool(src):
        kind, _, rest = src.partition(":")
        node, loc = split(rest)
        if kind == "corpus":
            t = lt(nodes.get(node), loc)
            return [] if t is None else [t]
        if kind == "v1_6":
            return [s for y in e6 if y["target_id"] == node and y["target_locus"] == loc for s in strings(y)]
        return []
    nq, bad, undeclared = 0, [], []
    for r in rows:
        declared = []
        for q in r.get("quotes", []):
            nq += 1
            if not any(q["quote"] in t for t in pool(q["src"])):
                bad.append({"row": r["id"], "src": q["src"], "quote": q["quote"]})
            declared.append(q["quote"])
        ch = dict(r.get("set", {}))
        ch.update(r.get("new_entry", {}))
        for fld in ("adversarial_move", "grounds", "routing"):
            for s in strings(ch.get(fld, "")):
                for span in re.findall(r'"([^"]+)"', s):
                    if span not in declared:
                        undeclared.append({"row": r["id"], "field": fld, "span": span})
    quotes = {"declared": nq, "verbatim": nq - len(bad), "not_verbatim": bad, "undeclared_spans": undeclared}

    # ---- anchors ----
    anchors = []
    for i in changed:
        x = e7[i]
        anchors.append({"row": by_i[i]["id"], "target": "%s#%s" % (x["target_id"], x["target_locus"]),
                        "count": (lt(nodes[x["target_id"]], x["target_locus"]) or "").count(x["target_anchor"])})
    for r, x in zip(filed, new7):
        anchors.append({"row": r["id"], "target": "%s#%s" % (x["target_id"], x["target_locus"]),
                        "count": (lt(nodes[x["target_id"]], x["target_locus"]) or "").count(x["target_anchor"])})

    # ---- bedrocks ----
    def tribs(reg):
        out = {}
        for b in reg["bedrocks"]:
            for f in b["facets"]:
                for t in f["tributaries"]:
                    out.setdefault((t["node"], t["locus"], t["anchor"]), []).append((b["bedrock_id"], f["facet_id"], t))
        return out
    t7, t8 = tribs(R7), tribs(R8)
    bedrocks = []
    for r in rows:
        bf = r.get("bedrock_from")
        if not bf:
            continue
        node, loc = split(bf["locus"])
        src = [y for y in e6 if y["target_id"] == node and y["target_locus"] == loc
               and y["target_anchor"] == bf["anchor"] and y["class"] == "d"]
        x = e7[r["entry"]["i"]] if r["kind"] == "amend" else new7[filed.index(r)]
        name_ok = len(src) == 1 and x["routing"]["residue"]["bedrock_name"] == src[0]["routing"]["residue"]["bedrock_name"]
        from_ok = any((h, f) == (bf["hr"], bf["facet"]) for h, f, _ in t7.get((node, loc, bf["anchor"]), []))
        new8 = t8.get((x["target_id"], x["target_locus"], x["target_anchor"]), [])
        new_ok = any((h, f) == (bf["hr"], bf["facet"]) and t["terminus_routing"] == x["routing"]["residue"]["terminus_routing"]
                     and t["novel"] == x["routing"]["residue"]["novel"] for h, f, t in new8)
        bedrocks.append({"row": r["id"], "from": bf["locus"], "hr": bf["hr"], "facet": bf["facet"],
                         "name_copied_equal": name_ok, "v0_7_files_the_source_there": from_ok,
                         "v0_8_files_the_entry_there": new_ok})

    # ---- knock-on (collision rule v0_2, imported) ----
    K = module_at("knock_on_tool", "l4_knock_on_pinned")
    i6_of = {}
    for j, x in enumerate(e6):
        assert ek(x) not in i6_of, ek(x)
        i6_of[ek(x)] = j
    i7_of = {}
    for j, x in enumerate(e7):
        assert ek(x) not in i7_of, ek(x)
        i7_of[ek(x)] = j
    n_of = {x["i"]: x["n"] for x in MEAS["entries"]}
    sup = {r["supersedes"] for r in RUL["rows"] if r.get("supersedes")}
    cur = {r["n"]: r for r in RUL["rows"] if r["row"] not in sup}
    cause = {i: by_i[i]["id"] for i in changed}
    cause.update({len(e6) + k: r["id"] for k, r in enumerate(filed)})
    own_row = {**{i: r for i, r in by_i.items()}, **stands}
    knock, a7 = [], []
    for i, x in enumerate(e7):
        if x["class"] != "a":
            continue
        a7.append(i)
        c7 = K.collisions(e7, [(i, x["target_id"], x["routing"]["answered_by"])])[i]
        before = set()
        if i < len(e6) and e6[i]["class"] == "a":
            c6 = K.collisions(e6, [(i, e6[i]["target_id"], e6[i]["routing"]["answered_by"])])[i]
            before = {i6_of[ek(y)] for y in c6}
        new = sorted({i7_of[ek(y)] for y in c7} - before)
        n = n_of.get(i) if i < len(e6) else None
        r = own_row.get(i)
        prop = (r or {}).get("proposed_r1")
        verdict = ("proposed HOLDS (%s)" % r["id"]) if prop else (cur[n]["verdict"] + " (" + cur[n]["row"] + ")" if n in cur else "no R1 row")
        if not new:
            continue
        text = json.dumps(r, ensure_ascii=False) if r else ""
        rerouted = i >= len(e6) or e6[i]["class"] != "a" or e6[i]["routing"] != x["routing"]
        knock.append({"i": i, "n": n, "target": "%s#%s" % (x["target_id"], x["target_locus"]), "r1": verdict,
                      "own_row": r["id"] if r else None,
                      "new_collisions": [{"at": "%s#%s" % (e7[j]["target_id"], e7[j]["target_locus"]), "class": e7[j]["class"],
                                          "anchor": e7[j]["target_anchor"],
                                          "made_by": cause.get(j, "unchanged entry, met through this (a)'s new class or route"
                                                                  if rerouted else "unchanged entry"),
                                          "made_by_named_in_own_row": bool(r) and j in cause and cause[j] in text}
                                         for j in new]})
    new_a = [{"i": i, "target": "%s#%s" % (e7[i]["target_id"], e7[i]["target_locus"]),
              "made_by": cause.get(i), "v1_6_class": e6[i]["class"] if i < len(e6) else None}
             for i in a7 if (n_of.get(i) if i < len(e6) else None) is None]

    # ---- move register ----
    def hist(s):
        return sorted({name for name, p in HISTORY for _ in re.finditer(p, s)})
    v16_hits = [{"i": j, "hits": hist(x["adversarial_move"])} for j, x in enumerate(e6) if hist(x["adversarial_move"])]
    drafted = []
    for r in rows:
        mv = (r.get("set") or {}).get("adversarial_move") or (r.get("new_entry") or {}).get("adversarial_move")
        if mv and hist(mv):
            drafted.append({"row": r["id"], "hits": hist(mv),
                            "phrases": sorted({mv[max(0, m.start() - 30):m.end() + 30].strip()
                                               for _, p in HISTORY for m in re.finditer(p, mv)})})
    move_register = {"v1_6_moves": len(e6), "v1_6_moves_with_history_wording": len(v16_hits),
                     "drafted_moves": sum(1 for r in rows if (r.get("set") or {}).get("adversarial_move")
                                          or (r.get("new_entry") or {}).get("adversarial_move")),
                     "drafted_moves_with_history_wording": drafted}

    # ---- safety ----
    X = module_at("exit_patterns", "pq_judgment_reading_pinned")
    W = module_at("wide_patterns", "sp_reading_l6_pinned")
    shits = []
    for r in rows:
        ch = dict(r.get("set", {}))
        ch.update(r.get("new_entry", {}))
        for fld in ("adversarial_move", "grounds"):
            s = ch.get(fld)
            if not isinstance(s, str):
                continue
            for p in X.EXIT:
                for m in re.finditer(p, s):
                    shits.append({"row": r["id"], "field": fld, "set": "gate2 X-032", "match": m.group(0)})
            for name, p in W.WIDE:
                for m in re.finditer(p, s, re.I):
                    shits.append({"row": r["id"], "field": fld, "set": "L6 wide:" + name, "match": m.group(0)})
    safety = {"hits_in_drafted_fields": shits}

    # ---- adjacency ----
    at_node = collections.defaultdict(set)
    for b in R8["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                at_node[t["node"]].add(b["bedrock_id"])
    at_node7 = collections.defaultdict(set)
    for b in R7["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                at_node7[t["node"]].add(b["bedrock_id"])

    def declared_pairs(reg):
        out = set()
        for b in reg["bedrocks"]:
            for rel in b.get("relations") or []:
                other = rel.get("to") or rel.get("bedrock") or rel.get("with")
                if other:
                    out.add(tuple(sorted((b["bedrock_id"], other))))
        return out
    dp8 = declared_pairs(R8)
    pairs8 = {tuple(sorted(p)) for ns in at_node.values() for p in __import__("itertools").combinations(sorted(ns), 2)}
    pairs7 = {tuple(sorted(p)) for ns in at_node7.values() for p in __import__("itertools").combinations(sorted(ns), 2)}
    adjacency = {"pairs_sharing_a_node_v0_7": len(pairs7), "pairs_sharing_a_node_v0_8": len(pairs8),
                 "new_pairs": sorted("%s+%s" % p for p in pairs8 - pairs7),
                 "undeclared_in_v0_8": sorted("%s+%s" % p for p in pairs8 if p not in dp8),
                 "tributaries_v0_8_equal_the_map_d": sorted(x["target_id"] + "#" + x["target_locus"] for x in e7 if x["class"] == "d"
                                                           if not any(True for _h, _f, t in t8.get((x["target_id"], x["target_locus"], x["target_anchor"]), [])))}

    # ---- L6's wide set over what the safety pass left ----
    wide_after = []
    for key, cls in sorted(W.CLASS.items()):
        src, _, locus = key.partition(":")
        if src != "flagship" or cls not in ("queue", "sibling", "widen"):
            continue
        node, loc = split(locus)
        t = lt(nodes.get(node), loc)
        if not isinstance(t, str):
            continue
        for name, p in W.WIDE:
            for m in re.finditer(p, t, re.I):
                sent = [s for s in re.split(r"(?<=[.!?])\s+", t) if m.group(0) in s]
                wide_after.append({"locus": locus, "l6_class": cls, "pattern": name, "match": m.group(0),
                                   "sentence": sent[0] if sent else ""})
    honest = []
    for o in C["objections"]:
        for loc in ["short", "medium", "long"] + ["archetypeVariants." + s for s in (o["responses"].get("archetypeVariants") or {})] + ["diagnosis", "note"]:
            t = lt(o, loc)
            if isinstance(t, str):
                for m in re.finditer(HONEST_FAMILY, t):
                    honest.append({"locus": "%s#%s" % (o["id"], loc), "match": m.group(0)})

    # ---- validator ----
    V = module_at("validator_v0_7", "adv_map_validator_v0_7_pinned")
    lines = []
    passed, viol, adv = V.validate([pinned.path_at(REPO, *PIN["v1_7"])], pinned.path_at(REPO, *PIN["corpus"]),
                                   assembly=True, out=lines.append)

    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/l7_judgment_reading.py",
        "reads": {k: v[1] for k, v in sorted(PIN.items())},
        "derivation": derivation,
        "quotes": quotes,
        "anchors": {"all_present": all(a["count"] >= 1 for a in anchors), "per_entry": anchors},
        "bedrocks": {"all_hold": all(b["name_copied_equal"] and b["v0_7_files_the_source_there"] and b["v0_8_files_the_entry_there"]
                                     for b in bedrocks), "per_row": bedrocks},
        "knock_on": {"a_entries_in_v1_7": len(a7), "rule": "collision rule v0_2; l4_knock_on.collisions at its pinned bytes",
                     "newly_collided": knock},
        "new_a_without_r1": new_a,
        "move_register": move_register,
        "safety": safety,
        "adjacency": adjacency,
        "wide_after_the_pin": wide_after,
        "honest_eval_family_v4_1_5": honest,
        "validator": {"v0_7_assembly_on_v1_7": {"passed": bool(passed), "violations": len(viol), "advisories": len(adv)}},
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
