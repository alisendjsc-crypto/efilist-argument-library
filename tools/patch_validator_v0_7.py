#!/usr/bin/env python3
"""L7 (R0223 order 3): derive adv_map_validator_v0_7.py from v0_6 by ANCHORED single-occurrence patches.

v0_6 is left byte-identical: canon pins it, v1_2..v1_6 were built against it, and gate2's judgment records name it.
Every anchor is asserted to occur EXACTLY once before substitution; a zero or a duplicate aborts. Reads binary,
decodes UTF-8 explicitly, consults no locale (ccclx).

What v0_7 adds, and why (design/variations/VARIATIONS_design_v0_1.md section 4, fcf6f6fe; R-V1, his word at V0:
"Go with your leans on all of the rulings."):
  1. `argumentShapes.<shape_id>` becomes a map locus, EXISTENCE-GATED exactly as archetype variants became one at
     K345 and `note` at K349: valid only where the node's top-level `argumentShapes` list carries a shape with that
     shape_id and a non-empty statement. locus_text reads the shape's `statement` alone. An (a) may route to a shape
     locus by the same test. No shape exists in the corpus yet (V1's README), so on today's corpus v0_7 behaves as
     v0_6 does, which the builder's regression control proves.
  2. The node bound extends by the per-locus cap for each shape locus, 3 + 3*(variant loci) + 3*(shape loci): the
     K348 principle, one locus kind over.
  3. `coverage` excludes shape loci as it excludes `note` (K349): a shape entry tests the library's statement of an
     objection, which is apparatus beside the node's argument, so apparatus cannot satisfy 82/82.
  4. `shape_coverage`, when a file declares it, is gated against THAT FILE's own shape loci (ccclxx), as
     note_coverage is. Shape loci never fold into variant_coverage or note_coverage.
  5. PHASES gains "H": the successor-map filings of L7 (entries filed against the v4.1.3 and v4.1.5 cuts). The
     shape staging letter "S" is NOT added: V1 keeps it disjoint from the map's PHASES, and an entry against a shape
     locus takes the next free letter when that phase exists.
  6. The self-test gains an L7 battery that runs each routing control BOTH ways (the K345 proof).

  python3 tools/patch_validator_v0_7.py [dest]      # default: adversarial_map_staging/adv_map_validator_v0_7.py
  python3 tools/patch_validator_v0_7.py --check     # derive in memory; compare with the committed v0_7
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_6.py")
DEST = os.path.join(REPO, "adversarial_map_staging", "adv_map_validator_v0_7.py")
V0_6_MD5 = "c002e93877b09d523daf786036af7a57"

PATCHES = []


def P(tag, old, new):
    PATCHES.append((tag, old, new))


P("header-version",
  '''v0_6 (K349): target_locus reaches the top-level `note` key, EXISTENCE-GATED, for the''',
  '''v0_7 (L7):   target_locus reaches `argumentShapes.<shape_id>`, EXISTENCE-GATED on the node's
             top-level `argumentShapes` list (R-V1); the node bound extends by 3 per shape locus;
             `coverage` excludes shape loci as it excludes `note`; shape_coverage added, per-file
             per ccclxx; PHASES += H (the L7 successor filings). "S" stays the shapes' own letter.
v0_6 (K349): target_locus reaches the top-level `note` key, EXISTENCE-GATED, for the''')

P("docstring-checks",
  '''  stopping-rule          NEW (gate 5) -- IF meta declares locus_closure, the per-locus stopping''',
  '''  shape-coverage         NEW (L7) -- IF meta declares shape_coverage "<hit>/<total>", it must equal
                         THAT FILE's own argumentShapes loci over the corpus total (ccclxx)
  stopping-rule          NEW (gate 5) -- IF meta declares locus_closure, the per-locus stopping''')

P("constants",
  '''NOTE_LOCUS = "note"
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E", "F", "R", "G")''',
  '''NOTE_LOCUS = "note"
# L7 (R-V1, his word at V0): a shape is a map target, EXISTENCE-GATED like a variant slot and the note. It is a
# TOP-LEVEL node key, `argumentShapes`, a list beside `objectionSubforms` and never under `responses` (the game
# embeds `responses` whole). The locus names the shape by its id: "argumentShapes.<shape_id>".
SHAPES_KEY = "argumentShapes"
SHAPE_PREFIX = "argumentShapes."
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E", "F", "R", "G", "H")''')

P("shape-helpers",
  '''def locus_valid(node, locus):''',
  '''def shape_id(locus):
    """Shape id for a shape locus, else None. Pure string work -- no corpus needed."""
    if isinstance(locus, str) and locus.startswith(SHAPE_PREFIX):
        return locus[len(SHAPE_PREFIX):]
    return None


def shape_statement(node, sid):
    """The statement of the node's shape `sid`, or None: a shape counts only with a non-empty statement."""
    for s in (node.get(SHAPES_KEY) or []):
        if isinstance(s, dict) and s.get("shape_id") == sid \\
                and isinstance(s.get("statement"), str) and s["statement"].strip() != "":
            return s["statement"]
    return None


def node_shape_ids(node):
    return [s["shape_id"] for s in (node.get(SHAPES_KEY) or [])
            if isinstance(s, dict) and isinstance(s.get("shape_id"), str)
            and shape_statement(node, s["shape_id"]) is not None]


def locus_valid(node, locus):''')

P("locus-valid",
  '''    if locus == NOTE_LOCUS:
        return isinstance(node.get(NOTE_LOCUS), str) and node[NOTE_LOCUS].strip() != ""
    s = variant_slot(locus)
    if s is None or s not in VARIANT_SLOTS:''',
  '''    if locus == NOTE_LOCUS:
        return isinstance(node.get(NOTE_LOCUS), str) and node[NOTE_LOCUS].strip() != ""
    sid = shape_id(locus)
    if sid is not None:
        return shape_statement(node, sid) is not None
    s = variant_slot(locus)
    if s is None or s not in VARIANT_SLOTS:''')

P("locus-text",
  '''        return node.get(NOTE_LOCUS, "")
    s = variant_slot(locus)
    if s is not None:''',
  '''        return node.get(NOTE_LOCUS, "")
    sid = shape_id(locus)
    if sid is not None:
        # The shape's statement ALONE: never a concatenation with the node's ladder (the K345 proof, again).
        return shape_statement(node, sid) or ""
    s = variant_slot(locus)
    if s is not None:''')

P("node-bound",
  '''        nvar = len(node_variant_slots(nodes[tid])) if tid in nodes else 0
        bound = 3 + 3 * nvar
        note("entry-cap-node", len(tags) <= bound,
             "%r has %d entries (node bound %d = 3 + 3*%d variant loci)"
             % (tid, len(tags), bound, nvar))''',
  '''        nvar = len(node_variant_slots(nodes[tid])) if tid in nodes else 0
        nshape = len(node_shape_ids(nodes[tid])) if tid in nodes else 0
        # L7: the per-locus cap applies to each shape locus exactly as K348 applied it to each variant locus.
        bound = 3 + 3 * nvar + 3 * nshape
        note("entry-cap-node", len(tags) <= bound,
             "%r has %d entries (node bound %d = 3 + 3*%d variant loci + 3*%d shape loci)"
             % (tid, len(tags), bound, nvar, nshape))''')

P("coverage-argued",
  '''    argued = set(tid for (tid, locus) in per_id_locus if locus != NOTE_LOCUS)''',
  '''    # L7: a shape entry tests the library's statement of an objection, apparatus beside the node's argument, so a
    # shape locus no more covers a node than its note does.
    argued = set(tid for (tid, locus) in per_id_locus if locus != NOTE_LOCUS and shape_id(locus) is None)''')

P("shape-coverage",
  '''    out("corpus: whole-file %s  objections-digest %s" % (cmd5[:12], odig[:12]))''',
  '''    # L7: shape_coverage is declared BY A FILE and gated against THAT FILE (ccclxx), as note_coverage is. Shape
    # loci are counted here and nowhere else.
    shape_loci_total = sorted((n["id"], SHAPE_PREFIX + s) for n in corpus["objections"] for s in node_shape_ids(n))
    shape_loci_hit = sorted(k for k in per_id_locus if shape_id(k[1]) is not None)
    sc = "%d/%d" % (len(set(shape_loci_hit)), len(shape_loci_total))
    for p, meta in metas:
        if "shape_coverage" in meta:
            own = set()
            for e in file_entries.get(p, []):
                if isinstance(e, dict) and shape_id(e.get("target_locus")) is not None:
                    own.add((e.get("target_id"), e["target_locus"]))
            own_sc = "%d/%d" % (len(own), len(shape_loci_total))
            note("shape-coverage", meta["shape_coverage"] == own_sc,
                 "%s: declared %r vs this file's %r (all loaded files: %s)"
                 % (p, meta["shape_coverage"], own_sc, sc))
    out("corpus: whole-file %s  objections-digest %s" % (cmd5[:12], odig[:12]))''')

P("shape-coverage-out",
  '''    out("note-coverage: %s note loci carry >=1 entry" % nc)''',
  '''    out("note-coverage: %s note loci carry >=1 entry" % nc)
    out("shape-coverage: %s argumentShapes loci carry >=1 entry" % sc)''')

P("l7-battery",
  '''    passed = sum(1 for _n, g, _c in results if g)
    overall = passed == len(results)''',
  '''    # ---------------- L7 control battery: the `argumentShapes` locus, both directions ----
    # A suite written before a change proves nothing about the change; the routing controls run BOTH ways. The
    # shape sits on node-z, which carries no variants and no note, so the node-bound control isolates the change.
    SHAPE_Z = "shape statement for node z sigma tau upsilon phi chi psi omega and beyond"
    SID = "node-z/sharper"
    for _n in mc["objections"]:
        if _n["id"] == "node-z":
            _n[SHAPES_KEY] = [{"shape_id": SID, "label": "the sharper form", "statement": SHAPE_Z}]
    open(cpath, "wb").write((json.dumps(mc, indent=2, ensure_ascii=False) + "\\n").encode("utf-8"))
    cmd5 = md5_bytes(open(cpath, "rb").read())
    odig = objections_digest(mc)
    SLOC = SHAPE_PREFIX + SID

    def sent(anchor, tid="node-z", sid=SID, **kw):
        d = dict(target_id=tid, target_locus=SHAPE_PREFIX + sid, target_anchor=anchor)
        d.update(kw)
        return _entry(**d)

    skey = "node-z#" + SLOC
    # 27. a well-formed shape entry validates, and so does the new phase letter
    clean("l7-shape-entry-validates", [sent("sigma tau upsilon phi")])
    clean("l7-phase-H-validates", [_entry(provenance={"phase": "H", "date": "2026-09-26", "seat": "self-test"})])
    # 28. "S" is the shapes' own letter, kept disjoint from the map's PHASES
    case("l7-phase-S-is-not-a-map-phase",
         [_entry(provenance={"phase": "S", "date": "2026-09-26", "seat": "self-test"})], "provenance")
    # 29. EXISTENCE GATE, twice: node-x carries no shapes; node-z carries none by this id
    case("l7-shape-on-node-without-shapes", [sent("sigma tau upsilon phi", tid="node-x")], "target-locus")
    case("l7-shape-id-absent-on-node", [sent("sigma tau upsilon phi", sid="node-z/absent")], "target-locus")
    # 30+31. THE ROUTING PROOF, BOTH WAYS: locus_text reads the statement ALONE
    case("l7-long-anchor-does-not-validate-against-shape", [sent("the quick brown fox")], "anchor-rule")
    case("l7-shape-anchor-does-not-validate-against-long",
         [_entry(target_id="node-z", target_locus="long", target_anchor="sigma tau upsilon phi")], "anchor-rule")
    # 32. an (a) may route TO a shape locus; a bogus one still trips
    clean("l7-answered-by-shape-ok",
          [_entry(target_id="node-x", target_anchor="the quick brown fox", routing={"answered_by": ["node-z#" + SLOC]})])
    case("l7-answered-by-shape-absent",
         [_entry(target_id="node-x", target_anchor="the quick brown fox",
                 routing={"answered_by": ["node-y#" + SHAPE_PREFIX + "node-y/none"]})], "routing-shape")
    # 33. a DECLARED shape_coverage is gated, both ways
    clean("l7-shape-coverage-declared-true", [sent("sigma tau upsilon phi")], meta_extra={"shape_coverage": "1/1"})
    case("l7-shape-coverage-declared-false", [sent("sigma tau upsilon phi")], "shape-coverage",
         meta_extra={"shape_coverage": "0/1"})
    # 34. shape loci NEVER fold into variant_coverage or note_coverage
    clean("l7-shape-is-not-a-variant", [sent("sigma tau upsilon phi")], meta_extra={"variant_coverage": "0/2"})
    case("l7-shape-counted-as-a-variant-trips", [sent("sigma tau upsilon phi")], "variant-coverage",
         meta_extra={"variant_coverage": "1/2"})
    case("l7-shape-counted-as-a-note-trips", [sent("sigma tau upsilon phi")], "note-coverage",
         meta_extra={"note_coverage": "1/1"})
    # 35. apparatus cannot satisfy coverage: a node reached only at a shape locus is NOT covered
    _covx = _entry(target_id="node-x", target_anchor="the quick brown fox")
    _covy = _entry(target_id="node-y", target_anchor="the quick brown fox")
    case("l7-shape-only-node-is-not-covered", [_covx, _covy, sent("sigma tau upsilon phi")], "coverage", terminal=True)
    clean("l7-primary-plus-shape-is-covered",
          [_covx, _covy, _entry(target_id="node-z", target_anchor="the quick brown fox"), sent("sigma tau upsilon phi")],
          terminal=True)
    # 36. the per-locus cap binds at a shape locus
    case("l7-shape-per-locus-cap",
         [sent(a) for a in ("sigma tau upsilon phi", "tau upsilon phi chi", "upsilon phi chi psi", "phi chi psi omega")],
         "entry-cap")
    # 37. THE NODE BOUND EXTENDS BY 3 PER SHAPE LOCUS: node-z has no variants and one shape, so its bound is 6.
    #     Six entries at node-z pass (v0_6's bound of 3 would refuse them); seven trip it.
    _six = [_entry(target_id="node-z", target_anchor=a) for a in
            ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over")] + \\
           [sent(a) for a in ("sigma tau upsilon phi", "tau upsilon phi chi", "upsilon phi chi psi")]
    clean("l7-node-bound-six-with-one-shape", _six)
    case("l7-node-bound-seven-trips", _six + [_entry(target_id="node-z", target_locus="medium",
                                                     target_anchor="medium text z four")], "entry-cap-node")
    # 38. gate 5 reaches a shape locus like any other
    case("l7-shape-open-with-one-entry", [sent("sigma tau upsilon phi")], "stopping-rule",
         meta_extra={"locus_closure": {skey: "open"}})
    clean("l7-shape-closed-with-one-entry", [sent("sigma tau upsilon phi")],
          meta_extra={"locus_closure": {skey: "closed"}})
    # 39. a shape with an empty statement is not a shape: the gate reads the statement, not only the id
    for _n in mc["objections"]:
        if _n["id"] == "node-z":
            _n[SHAPES_KEY] = [{"shape_id": SID, "label": "the sharper form", "statement": "   "}]
    open(cpath, "wb").write((json.dumps(mc, indent=2, ensure_ascii=False) + "\\n").encode("utf-8"))
    cmd5 = md5_bytes(open(cpath, "rb").read())
    case("l7-empty-statement-is-not-a-shape", [sent("sigma tau upsilon phi")], "target-locus")

    passed = sum(1 for _n, g, _c in results if g)
    overall = passed == len(results)''')


def derive():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == V0_6_MD5, "BASE GUARD: v0_6 md5 %s != %s" % (got, V0_6_MD5)
    txt = raw.decode("utf-8")
    for tag, old, new in PATCHES:
        n = txt.count(old)
        assert n == 1, "anchor %r occurs %d times, expected exactly 1" % (tag, n)
        txt = txt.replace(old, new, 1)
    return txt.encode("utf-8")


def main():
    out = derive()
    if "--check" in sys.argv:
        same = os.path.exists(DEST) and open(DEST, "rb").read() == out
        print("VALIDATOR v0_7: %s" % ("matches its derivation from v0_6" if same else "DIFFERS from its derivation"))
        return 0 if same else 1
    dest = next((a for a in sys.argv[1:] if not a.startswith("--")), DEST)
    open(dest, "wb").write(out)
    print("wrote %s  %s  %d B (%d patches)" % (dest, hashlib.md5(out).hexdigest(), len(out), len(PATCHES)))
    assert hashlib.md5(open(SRC, "rb").read()).hexdigest() == V0_6_MD5, "v0_6 was mutated"
    print("  v0_6 byte-identical: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
