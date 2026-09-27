#!/usr/bin/env python3
"""l7_redraft_reading.py -- gate2's reading instrument for its second judgment of L7's successor map: the 18 rows L7
appended after gate2's first judgment (gate2, 2026-09-26, R0245).

Every figure L7_successor_redrafts_judgments.json states as measured, recomputed from the judged artifacts at the md5s they
are pinned to, never from the working tree and never by importing the drafting seat's builder:

  new_rows        the rows the drafts record holds at 370e7d02 that it did not hold at fd9267f8 (the bytes the first
                  judgment read), each with the row it supersedes, the first-judgment row it answers, and the fields its
                  set differs in from the superseded row's
  derivation      v1_8 re-derived from v1_7 and the new rows: every entry v1_7's byte for byte or v1_7's with exactly its
                  superseding row's fields set ('@from' copied from the (d) the row names), provenance v1_7's plus
                  redrafted_L7; the filed entries from 138 are the superseding rows' new entries
  move_register   the first judgment's history patterns (imported from l7_judgment_reading.py at its pinned bytes) over
                  every move a new row drafts
  quotes          every declared quotation verbatim at its source; every double-quoted span in a changed field declared
  bedrock         SM-69's copied bedrock, the source (d) in register v0_8 under the facet claimed, the entry in v0_9 there
  register        v0_9 against v0_8: every tributary that moved, the counts per bedrock, and adjacency
  knock_on        v1_8 against v1_6 under collision rule v0_2 (l4_knock_on.collisions at its pinned bytes), counted three
                  ways: by entry lineage (the first judgment's count), by lineage and class, and by (node, locus, anchor,
                  class) (the drafting seat's control); and the control's own record, read at its md5
  safety          gate2's X-032 patterns and L6's wide set over every field a new row drafts
  pins            whether gate2's committed L7 gate or reading names controls_v1_7 at all; the control record's bytes
  validator       v0_7 --assembly on v1_8 against the v4.1.5 corpus, in-process at its pinned bytes

  python3 l7_redraft_reading.py            # print the record
  python3 l7_redraft_reading.py --emit     # write the record beside this file
  python3 l7_redraft_reading.py --check    # compare with the committed record; exit 1 on any difference

Repo-relative. Writes nothing unless --emit is given. Deterministic.
"""
import collections, copy, itertools, json, os, re, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/l7_redraft_reading_v0_1.json"
PIN = {
    "drafts": ("adversarial_map_staging/r1/L7_successor_drafts.json", "370e7d02457314e10d6211f95d5ae8c0"),
    "drafts_first": ("adversarial_map_staging/r1/L7_successor_drafts.json", "fd9267f853a5a09fe5aa3972b16fa2a7"),
    "first_judgment": ("adversarial_map_staging/r1/L7_successor_drafts_judgments.json", "bd3b4e89f25e7f874f5aa553b998fe0d"),
    "v1_6": ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "v1_7": ("adversarial_map_staging/adversarial_map_v1_7.json", "db40b45693eff1297b3f3152c6295c15"),
    "v1_8": ("adversarial_map_staging/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1"),
    "register_v0_8": ("adversarial_map_staging/honest_residuals_register_v0_8.json", "8f6d38886b95033600752a5be052bd99"),
    "register_v0_9": ("adversarial_map_staging/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351"),
    "knock_on_record": ("adversarial_map_staging/r1/l7_knock_on_v0_1.json", "6635d5ec3aaa4018c146260bb6b58ab0"),
    "controls_v1_7_record": ("adversarial_map_staging/controls_v1_7_v0_1.json", "a0fc503133221975b4dcb1393a41bc99"),
    "validator_v0_7": ("adversarial_map_staging/adv_map_validator_v0_7.py", "8a74dcc452338f127ec03e078090c2ed"),
    "knock_on_tool": ("adversarial_map_staging/r1/l4_knock_on.py", "66022fa8e9ba7ad3ff26e42aee5b0b1c"),
    "first_reading": ("adversarial_map_staging/r1/l7_judgment_reading.py", "122a34339bc4afbbaff58a7643ef8878"),
    "first_gate": ("adversarial_map_staging/r1/l7_judgments_gate.py", "419d4e06e668e47b5ac4b605e66ecc02"),
    "exit_patterns": ("adversarial_map_staging/r1/pq_judgment_reading.py", "d11cfbc7182e8fba0f549467b654b1bd"),
    "wide_patterns": ("adversarial_map_staging/r1/sp_reading_l6.py", "dc2525ef40fc5353a670484f511bd668"),
}
FIELDS = ("target_id", "target_locus", "target_anchor", "adversarial_move", "class", "grounds", "routing", "status")
OWN_GATES = ["first_gate", "first_reading"]   # gate2's committed L7 instruments, read at their pinned bytes


def module_at(key, name):
    rel, want = PIN[key]
    m = types.ModuleType(name)
    m.__file__ = os.path.join(REPO, rel)
    exec(compile(pinned.bytes_at(REPO, rel, want).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def load(key):
    rel, want = PIN[key]
    return json.loads(pinned.bytes_at(REPO, rel, want).decode("utf-8"))


def split(t):
    node, _, loc = t.partition("#")
    return node, loc


def ek(x):
    return (x["target_id"], x["target_locus"], x["target_anchor"], x["class"])


def measure():
    R1 = module_at("first_reading", "l7_judgment_reading_pinned")
    D, D0 = load("drafts"), load("drafts_first")
    J1 = load("first_judgment")
    M6, M7, M8 = load("v1_6")["entries"], load("v1_7")["entries"], load("v1_8")["entries"]
    C = load("corpus")
    nodes = {o["id"]: o for o in C["objections"]}
    R8, R9 = load("register_v0_8"), load("register_v0_9")
    old_ids = {r["id"] for r in D0["rows"]}
    rows = {r["id"]: r for r in D["rows"]}
    new = [r for r in D["rows"] if r["id"] not in old_ids]
    j1 = {r["row_id"]: r for r in J1["rows"] if r.get("row_id")}
    j1_by_id = {r["id"]: r for r in J1["rows"]}
    fail = []

    # ---- the new rows ----
    new_rows = []
    for r in new:
        old = rows.get(r.get("supersedes"))
        oset = (old or {}).get("set") or (old or {}).get("new_entry") or {}
        nset = r.get("set") or r.get("new_entry") or {}
        diff = sorted(k for k in set(oset) | set(nset) if json.dumps(oset.get(k), sort_keys=True) != json.dumps(nset.get(k), sort_keys=True))
        top = sorted(k for k in set(old or {}) | set(r) if k not in ("id", "set", "new_entry", "why", "supersedes", "answers")
                     and json.dumps((old or {}).get(k), sort_keys=True) != json.dumps(r.get(k), sort_keys=True))
        ans = j1_by_id.get(r.get("answers"), {})
        new_rows.append({"row": r["id"], "supersedes": r.get("supersedes"), "answers": r.get("answers"),
                         "answers_the_amend_of_it": bool(ans) and ans.get("row_id") == r.get("supersedes") and ans.get("verdict") == "AMEND",
                         "set_fields_changed": diff, "other_fields_changed": top})
    amended = sorted(r["row_id"] for r in J1["rows"] if r.get("verdict") == "AMEND")
    answered = sorted(x["supersedes"] for x in new_rows)

    # ---- derivation of v1_8 from v1_7 ----
    def resolve(r, routing, base):
        rs = routing.get("residue") if isinstance(routing, dict) else None
        if not rs or rs.get("bedrock_name") != "@from":
            return routing
        bf = r["bedrock_from"]
        node, loc = split(bf["locus"])
        src = [y for y in base if y["target_id"] == node and y["target_locus"] == loc and y["target_anchor"] == bf["anchor"] and y["class"] == "d"]
        out = copy.deepcopy(routing)
        out["residue"]["bedrock_name"] = src[0]["routing"]["residue"]["bedrock_name"] if len(src) == 1 else None
        return out
    by_i = {}
    filed = [r for r in D0["rows"] if r["kind"] == "file"]
    for r in new:
        if r["kind"] == "amend":
            by_i[r["entry"]["i"]] = r
        else:
            k = [f["id"] for f in filed].index(r["supersedes"])
            by_i[len(M7) - len(filed) + k] = r
    changed, carried = [], 0
    for i, x7 in enumerate(M7):
        x8 = M8[i]
        if i not in by_i:
            if json.dumps(x8, sort_keys=True) != json.dumps(x7, sort_keys=True):
                fail.append("entry %d moved without a row" % i)
            carried += 1
            continue
        r = by_i[i]
        src = r.get("set") or r.get("new_entry")
        exp = {k: copy.deepcopy(x7[k]) for k in FIELDS if k in x7}
        for k, v in src.items():
            if k in FIELDS:
                exp[k] = resolve(r, v, M7) if k == "routing" else v
        got = {k: x8[k] for k in FIELDS if k in x8}
        if json.dumps(exp, sort_keys=True) != json.dumps(got, sort_keys=True):
            fail.append("entry %d (%s) is not v1_7 plus its row's fields" % (i, r["id"]))
        prov = dict(x8["provenance"])
        rd = prov.pop("redrafted_L7", None)
        if json.dumps(prov, sort_keys=True) != json.dumps(x7["provenance"], sort_keys=True) or not rd:
            fail.append("entry %d provenance is not v1_7's plus redrafted_L7" % i)
        changed.append(i)
    cc = lambda es: dict(sorted(collections.Counter(x["class"] for x in es).items()))
    derivation = {"v1_7_entries": len(M7), "v1_8_entries": len(M8), "carried_byte_for_byte": carried, "changed": len(changed),
                  "class_counts_v1_7": cc(M7), "class_counts_v1_8": cc(M8), "failures": fail}

    # ---- move register (the first judgment's patterns) ----
    hist = []
    for r in new:
        mv = (r.get("set") or r.get("new_entry") or {}).get("adversarial_move", "")
        hits = sorted({n for n, p in R1.HISTORY for _ in re.finditer(p, mv)})
        if hits:
            hist.append({"row": r["id"], "hits": hits})

    # ---- quotes ----
    def pool(src):
        kind, _, rest = src.partition(":")
        node, loc = split(rest)
        if kind == "corpus":
            t = R1.lt(nodes.get(node), loc)
            return [] if t is None else [t]
        if kind == "v1_6":
            return [s for y in M6 if y["target_id"] == node and y["target_locus"] == loc for s in R1.strings(y)]
        return []
    nq, bad, undeclared = 0, [], []
    for r in new:
        declared = []
        for q in r.get("quotes", []):
            nq += 1
            if not any(q["quote"] in t for t in pool(q["src"])):
                bad.append({"row": r["id"], "src": q["src"], "quote": q["quote"]})
            declared.append(q["quote"])
        ch = dict(r.get("set") or r.get("new_entry") or {})
        for fld in ("adversarial_move", "grounds", "routing"):
            for s in R1.strings(ch.get(fld, "")):
                for span in re.findall(r'"([^"]+)"', s):
                    if span not in declared:
                        undeclared.append({"row": r["id"], "field": fld, "span": span})

    # ---- SM-69's bedrock ----
    def tribs(reg):
        out = {}
        for b in reg["bedrocks"]:
            for f in b["facets"]:
                for t in f["tributaries"]:
                    out.setdefault((t["node"], t["locus"], t["anchor"]), []).append((b["bedrock_id"], f["facet_id"], t))
        return out
    t8, t9 = tribs(R8), tribs(R9)
    bedrock = []
    for r in new:
        bf = r.get("bedrock_from")
        if not bf or "routing" not in (r.get("set") or {}):
            continue
        node, loc = split(bf["locus"])
        src = [y for y in M7 if y["target_id"] == node and y["target_locus"] == loc and y["target_anchor"] == bf["anchor"] and y["class"] == "d"]
        x = M8[r["entry"]["i"]]
        bedrock.append({"row": r["id"], "from": bf["locus"], "hr": bf["hr"], "facet": bf["facet"],
                        "name_copied_equal": len(src) == 1 and x["routing"]["residue"]["bedrock_name"] == src[0]["routing"]["residue"]["bedrock_name"],
                        "v0_8_files_the_source_there": any((h, f) == (bf["hr"], bf["facet"]) for h, f, _ in t8.get((node, loc, bf["anchor"]), [])),
                        "v0_9_files_the_entry_there": any((h, f) == (bf["hr"], bf["facet"]) and t["terminus_routing"] == x["routing"]["residue"]["terminus_routing"]
                                                          and t["novel"] == x["routing"]["residue"]["novel"]
                                                          for h, f, t in t9.get((x["target_id"], x["target_locus"], x["target_anchor"]), []))})

    # ---- register v0_9 against v0_8 ----
    def flat(reg):
        return {(b["bedrock_id"], f["facet_id"], t["node"], t["locus"], t["anchor"]) for b in reg["bedrocks"] for f in b["facets"] for t in f["tributaries"]}
    f8, f9 = flat(R8), flat(R9)
    counts = lambda reg: {b["bedrock_id"]: b["tributary_count"] for b in reg["bedrocks"]}
    c8, c9 = counts(R8), counts(R9)

    def at_node(reg):
        d = collections.defaultdict(set)
        for b in reg["bedrocks"]:
            for f in b["facets"]:
                for t in f["tributaries"]:
                    d[t["node"]].add(b["bedrock_id"])
        return d

    def declared(reg):
        return {tuple(sorted((b["bedrock_id"], rel["to"]))) for b in reg["bedrocks"] for rel in (b.get("relations") or []) if rel.get("to")}
    n8, n9 = at_node(R8), at_node(R9)
    p8 = {tuple(sorted(p)) for ns in n8.values() for p in itertools.combinations(sorted(ns), 2)}
    p9 = {tuple(sorted(p)) for ns in n9.values() for p in itertools.combinations(sorted(ns), 2)}
    register = {"removed": sorted("%s/%s %s#%s" % (a, b, c, d) for a, b, c, d, _ in f8 - f9),
                "added": sorted("%s/%s %s#%s" % (a, b, c, d) for a, b, c, d, _ in f9 - f8),
                "counts_changed": {k: [c8.get(k), c9.get(k)] for k in sorted(set(c8) | set(c9)) if c8.get(k) != c9.get(k)},
                "new_pairs": sorted("%s+%s" % p for p in p9 - p8),
                "undeclared_in_v0_9": sorted("%s+%s" % p for p in p9 if p not in declared(R9))}

    # ---- knock-on, three counts ----
    K = module_at("knock_on_tool", "l4_knock_on_pinned")
    lin6 = {}
    for j, x in enumerate(M6):
        lin6[ek(x)] = j
    lin8 = {}
    for j, x in enumerate(M8):
        lin8[ek(x)] = j
    by_lineage, by_lineage_class, by_key, class_only = [], [], [], []
    for i, x in enumerate(M8):
        if x["class"] != "a":
            continue
        c8_ = K.collisions(M8, [(i, x["target_id"], x["routing"]["answered_by"])])[i]
        c6_ = []
        if i < len(M6) and M6[i]["class"] == "a":
            c6_ = K.collisions(M6, [(i, M6[i]["target_id"], M6[i]["routing"]["answered_by"])])[i]
        li6 = {lin6[ek(y)] for y in c6_}
        li8 = {lin8[ek(y)] for y in c8_}
        if li8 - li6:
            by_lineage.append(i)
        lc6 = {(lin6[ek(y)], y["class"]) for y in c6_}
        lc8 = {(lin8[ek(y)], y["class"]) for y in c8_}
        if lc8 - lc6:
            by_lineage_class.append(i)
        k6 = {ek(y) for y in c6_}
        k8 = {ek(y) for y in c8_}
        if k8 - k6:
            by_key.append(i)
        extra = sorted(lc8 - lc6)
        if extra and not (li8 - li6) or any(j in li6 for j, _ in extra):
            class_only.append({"i": i, "target": "%s#%s" % (x["target_id"], x["target_locus"]),
                               "reclassed_at_a_known_entry": ["%s#%s (%s, i=%d)" % (M8[j]["target_id"], M8[j]["target_locus"], c, j)
                                                              for j, c in extra if j in li6]})
    KR = load("knock_on_record")
    ctl = [int(x["i"]) for x in KR.get("items", [])]
    knock = {"collision_rule": "v0_2, l4_knock_on.collisions at its pinned bytes",
             "newly_collided_by_lineage": by_lineage, "by_lineage_and_class": by_lineage_class,
             "by_node_locus_anchor_class": by_key,
             "a_class_change_at_an_entry_already_met": class_only,
             "the_controls_record_lists": sorted(ctl)}

    # ---- safety ----
    X = module_at("exit_patterns", "pq_judgment_reading_pinned")
    W = module_at("wide_patterns", "sp_reading_l6_pinned")
    shits = []
    for r in new:
        ch = r.get("set") or r.get("new_entry") or {}
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

    # ---- pins ----
    named = {PIN[k][0]: "controls_v1_7" in pinned.bytes_at(REPO, *PIN[k]).decode("utf-8") for k in OWN_GATES}
    pins = {"gate2_L7_instrument_names_controls_v1_7": named,
            "controls_v1_7_record_read_at": PIN["controls_v1_7_record"][1]}

    # ---- validator ----
    V = module_at("validator_v0_7", "adv_map_validator_v0_7_pinned")
    lines = []
    passed, viol, adv = V.validate([pinned.path_at(REPO, *PIN["v1_8"])], pinned.path_at(REPO, *PIN["corpus"]), assembly=True, out=lines.append)

    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/l7_redraft_reading.py",
        "reads": {k: v[1] for k, v in sorted(PIN.items())},
        "new_rows": new_rows,
        "coverage": {"amended_in_the_first_judgment": amended, "superseded_by_a_new_row": answered,
                     "equal": amended == answered},
        "derivation": derivation,
        "move_register": {"patterns": [n for n, _ in R1.HISTORY], "new_moves_with_history_wording": hist},
        "quotes": {"declared": nq, "verbatim": nq - len(bad), "not_verbatim": bad, "undeclared_spans": undeclared},
        "bedrock": bedrock,
        "register": register,
        "knock_on": knock,
        "safety": {"hits_in_new_fields": shits},
        "pins": pins,
        "validator": {"v0_7_assembly_on_v1_8": {"passed": bool(passed), "violations": len(viol), "advisories": len(adv)}},
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
