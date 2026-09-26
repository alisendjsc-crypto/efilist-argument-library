#!/usr/bin/env python3
"""build_map_sidecars.py -- sidecar JSON for two of the flagship's mega-literals, written FROM
site/combined.html's own bytes and never retyped. L1 (2026-09-25), answering relay R0057 (argue S38)
under standing ruling 1 (2026-09-18): no assembler for combined.html; the mega-literals without a
second copy get sidecar data files as the reference, their md5 pinned in canon, and the cross-surface
gate extended over them.

  MAP_GRAPH_DATA   -> sidecars/map_graph_data.json    the Mechanism Web (Map 2): mechanisms, objections, links
  MAP1_TRANSITIONS -> sidecars/map1_transitions.json  Map 1, the Argument Flow Map: next-objection edges by mode

Each file is a pure function of site/combined.html. `data` is the literal as it stands (json.loads of
the flagship's bytes); every other field is derived from the flagship by this script, the Map 1
caveats included (lifted from its methodology panel, HTML entities decoded, nothing else changed).
So a pin move that leaves both literals and that panel alone leaves both files byte-identical, and one
that touches any of them turns tools/xsurface_v4_1_0.py RED until this is re-run and the canon pin
moves with it.

Nothing is invented. MAP_GRAPH_DATA marks no link primary, so no primary mechanism is emitted; Map 1
has no entry for four objections, so none is authored.

  python3 tools/build_map_sidecars.py            # write sidecars/ from site/combined.html
  python3 tools/build_map_sidecars.py --check    # write nothing; exit 1 if either file would change
  python3 tools/build_map_sidecars.py --root DIR --out DIR2
"""
import argparse, glob, hashlib, html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FLAGSHIP = "site/combined.html"
VERSION = "1.0.0"   # the files' SHAPE; the content's identity is data_md5 and the file md5 canon pins
MGD_OUT = "sidecars/map_graph_data.json"
M1_OUT = "sidecars/map1_transitions.json"


def balance(s, start):
    """The balanced [..] / {..} beginning at `start`, ignoring brackets inside strings (as xsurface)."""
    depth = 0; i = start; instr = False; esc = False
    while i < len(s):
        ch = s[i]
        if instr:
            if esc:            esc = False
            elif ch == "\\":   esc = True
            elif ch == '"':    instr = False
        else:
            if ch == '"':      instr = True
            elif ch in "[{":   depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0:
                    return s[start:i + 1]
        i += 1
    return None


def literal(s, name):
    """json.loads of the flagship's one declaration of `name`, var or const."""
    ms = list(re.finditer(r"\b(?:var|let|const)\s+%s\s*=\s*" % name, s))
    if len(ms) != 1:
        raise SystemExit("ABORT: %d declarations of %s in the flagship, expected 1" % (len(ms), name))
    start = ms[0].end()
    if s[start] not in "[{":
        raise SystemExit("ABORT: %s is not a bracketed literal" % name)
    lit = balance(s, start)
    if lit is None:
        raise SystemExit("ABORT: %s never closes" % name)
    if s[start + len(lit)] != ";":
        raise SystemExit("ABORT: %s is not followed by ';'" % name)
    return json.loads(lit)


def canon_md5(x):
    """xsurface_v4_1_0.py's canonical serialization, byte for byte, so the two hashes are comparable."""
    return hashlib.md5(json.dumps(x, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def map1_caveats(s):
    """Map 1's own caveats: the START HERE list and the KNOWN LIMITATIONS section of its methodology panel."""
    panel = '<div id="map1-methodology-panel"'
    if s.count(panel) != 1:
        raise SystemExit("ABORT: %d Map 1 methodology panels, expected 1" % s.count(panel))
    p = s.index(panel)
    a = s.index('<div class="precis-start">', p)
    start_here = re.findall(r"<li>(.*?)</li>", s[a:s.index("</ul>", a)], flags=re.S)
    kl = "<h4>KNOWN LIMITATIONS</h4>"
    if s.count(kl) != 1:
        raise SystemExit("ABORT: %d KNOWN LIMITATIONS headings, expected 1" % s.count(kl))
    k = s.index(kl)
    if not p < a < k:
        raise SystemExit("ABORT: Map 1's START HERE and KNOWN LIMITATIONS are not in its panel's order")
    limits = [x.strip() for x in s[k + len(kl):s.index("<h4>", k + len(kl))].split("<br>")]
    items = start_here + limits
    if not start_here or not all(limits) or any("<" in x or ">" in x or "\n" in x.strip() for x in items):
        raise SystemExit("ABORT: a Map 1 caveat item is empty, carries markup or spans lines")
    return [html.unescape(x.strip()) for x in start_here], [html.unescape(x) for x in limits]


def build(s):
    """{relative path: file bytes} for both sidecars, from the flagship's text alone."""
    ids = [o["id"] for o in literal(s, "OBJECTIONS")]
    g = literal(s, "MAP_GRAPH_DATA")
    t = literal(s, "MAP1_TRANSITIONS")

    # ---------------------------------------------------------------- the Mechanism Web
    mech = {n["id"]: n for n in g["nodes"] if n["type"] == "mechanism"}
    objs = [n for n in g["nodes"] if n["type"] == "objection"]
    if sorted(n["entryId"] for n in objs) != sorted(ids):
        raise SystemExit("ABORT: MAP_GRAPH_DATA's objection nodes are not the flagship's objections")
    if len(g["nodes"]) != len(mech) + len(objs):
        raise SystemExit("ABORT: MAP_GRAPH_DATA carries a node that is neither mechanism nor objection")
    node_of = {n["id"]: n for n in objs}
    linked = {n["id"]: [] for n in objs}
    for l in g["links"]:
        if l["source"] not in mech or l["target"] not in node_of:
            raise SystemExit("ABORT: link %r is not mechanism -> objection" % (l,))
        linked[l["target"]].append(l["source"])
    several = sum(1 for v in linked.values() if len(v) > 1)
    by_objection = {}
    for n in objs:
        by_objection[n["entryId"]] = {
            "tier": n["tier"],
            "mechanisms": [{"id": m, "label": mech[m]["label"], "mechType": mech[m]["mechType"]}
                           for m in linked[n["id"]]],
        }
    mgd = {
        "sidecar": "map_graph_data",
        "version": VERSION,
        "about": ("The Mechanism Web (Map 2) of the efilist argument library's flagship, as data: which "
                  "psychological, rhetorical or structural mechanisms drive each objection. `data` is the "
                  "flagship's MAP_GRAPH_DATA literal as it stands; `by_objection` is the same links keyed "
                  "by corpus objection id. Generated, never hand-edited."),
        "source": {"file": FLAGSHIP, "literal": "MAP_GRAPH_DATA"},
        "generated_by": "tools/build_map_sidecars.py",
        "data_md5": canon_md5(g),
        "data_md5_method": "md5 of json.dumps(data, sort_keys=True, separators=(',', ':')), as tools/xsurface_v4_1_0.py",
        "id_convention": ("Graph node ids are obj_<corpus id> and mech_<name>; each objection node carries "
                          "entryId, the corpus id. by_objection is keyed by entryId."),
        "summary": {"objections": len(objs), "mechanisms": len(mech), "links": len(g["links"]),
                    "objections_with_one_mechanism": sum(1 for v in linked.values() if len(v) == 1),
                    "objections_with_several_mechanisms": several},
        "primary_mechanism": {
            "status": "UNDEFINED",
            "measured": ("No link in MAP_GRAPH_DATA marks a primary mechanism, and %d of the %d objections "
                         "link to more than one." % (several, len(objs))),
            "order": "Each objection's mechanisms are listed in the literal's link order. That order is not a rank.",
            "rule": ("Ruled by Josiah 2026-09-25: no primary mechanism is defined. Pair or group objections "
                     "by the mechanisms they share, and do not read the first-listed mechanism as primary."),
        },
        "by_objection": by_objection,
        "data": g,
    }

    # ---------------------------------------------------------------- Map 1
    modes = [k for k in next(iter(t.values())) if k != "source_meta"]
    for src, v in t.items():
        if src not in ids:
            raise SystemExit("ABORT: Map 1 source %r is not a flagship objection" % src)
        if [k for k in v if k != "source_meta"] != modes:
            raise SystemExit("ABORT: Map 1 source %r does not carry the modes %r" % (src, modes))
    targets = {e["target"] for v in t.values() for m in modes for e in v[m]}
    if not targets <= set(ids):
        raise SystemExit("ABORT: a Map 1 edge targets %r" % sorted(targets - set(ids)))
    counts = {m: sum(len(v[m]) for v in t.values()) for m in modes}
    counts["total"] = sum(counts[m] for m in modes)
    start_here, limits = map1_caveats(s)
    m1 = {
        "sidecar": "map1_transitions",
        "version": VERSION,
        "about": ("Map 1, the Argument Flow Map, of the efilist argument library's flagship, as data: for "
                  "each objection, the objections an interlocutor is likely to raise next, under each "
                  "interlocutor model. `data` is the flagship's MAP1_TRANSITIONS literal as it stands. "
                  "Generated, never hand-edited. Read `caveats` before using a weight."),
        "source": {"file": FLAGSHIP, "literal": "MAP1_TRANSITIONS"},
        "generated_by": "tools/build_map_sidecars.py",
        "data_md5": canon_md5(t),
        "data_md5_method": "md5 of json.dumps(data, sort_keys=True, separators=(',', ':')), as tools/xsurface_v4_1_0.py",
        "id_convention": ("Keys and every edge target are bare corpus objection ids (canon "
                          "invariants.map1_top_level_key_naming_convention). Edge fields: canon "
                          "schemas.map1_transitions_edge_by_archetype."),
        "modes": modes,
        "edge_counts": counts,
        "coverage": {
            "objections": len(ids),
            "sources": len(t),
            "absent_as_source": [i for i in ids if i not in t],
            "never_a_target": [i for i in ids if i not in targets],
        },
        "caveats": {
            "method": ("Lifted by the generator from the flagship's Map 1 methodology panel: its START HERE "
                       "list and its KNOWN LIMITATIONS section, HTML entities decoded, nothing else changed."),
            "start_here": start_here,
            "known_limitations": limits,
        },
        "data": t,
    }

    dump = lambda x: (json.dumps(x, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return {MGD_OUT: dump(mgd), M1_OUT: dump(m1)}


def read_flagship(root):
    return io.open(os.path.join(root, FLAGSHIP), encoding="utf-8", newline="").read()


def invariants_check(root, out):
    """Cross-check against the canon's own recorded invariants. A mismatch means the literal moved and the
    invariants must be revised first -- MAJOR by the canon's update_protocol -- so this refuses to write."""
    found = glob.glob(os.path.join(root, "project_canon_v*.json"))
    if len(found) != 1:
        raise SystemExit("ABORT: %d canon files at %s, expected 1" % (len(found), root))
    inv = json.load(io.open(found[0], encoding="utf-8"))["invariants"]
    g = json.loads(out[MGD_OUT])
    t = json.loads(out[M1_OUT])
    blended = {}
    for v in t["data"].values():
        for e in v["blended"]:
            blended[str(len(e["modes"]))] = blended.get(str(len(e["modes"])), 0) + 1
    disclosed = {m: sum(1 for v in t["data"].values() for e in v[m] if e.get("two_mechanism_disclosure") is True)
                 for m in ("defender", "drifter", "blended")}
    pairs = [
        ("map_graph_data_node_count", len(g["data"]["nodes"])),
        ("map_graph_data_mechanism_node_count", g["summary"]["mechanisms"]),
        ("map_graph_data_objection_node_count", g["summary"]["objections"]),
        ("map_graph_data_link_count", g["summary"]["links"]),
        ("mechanism_count", g["summary"]["mechanisms"]),
        ("map1_node_count", t["coverage"]["sources"]),
        ("map1_edge_count_total", t["edge_counts"]["total"]),
        ("map1_blended_mode_count_distribution", blended),
        ("map1_two_mechanism_disclosure_true_counts", disclosed),
    ]
    bad = [(k, inv.get(k), v) for k, v in pairs if inv.get(k) != v]
    for k, want, got in bad:
        print("  MISMATCH  invariants.%s = %r, the flagship gives %r" % (k, want, got))
    if bad:
        raise SystemExit("ABORT: the flagship disagrees with %s's invariants; nothing written"
                         % os.path.basename(found[0]))
    print("  invariants agree: %d of %d checked against %s" % (len(pairs), len(pairs), os.path.basename(found[0])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=REPO, help="tree holding site/combined.html (default: this repo)")
    ap.add_argument("--out", default=None, help="tree to write sidecars/ into (default: --root)")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if a file would change")
    a = ap.parse_args()
    out_root = a.out or a.root
    out = build(read_flagship(a.root))
    invariants_check(a.root, out)
    changed = 0
    for rel, b in out.items():
        p = os.path.join(out_root, rel)
        old = open(p, "rb").read() if os.path.isfile(p) else None
        same = old == b
        changed += not same
        print("  %-34s %s / %d  %s" % (rel, hashlib.md5(b).hexdigest(), len(b),
                                       "unchanged" if same else ("WOULD CHANGE" if a.check else "written")))
        if not a.check and not same:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(b)
    if a.check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
