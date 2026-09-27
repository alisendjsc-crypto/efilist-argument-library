#!/usr/bin/env python3
"""shape_validator_v0_1.py -- the argumentShapes validator (V1, seat l, 2026-09-26)

Built from the variations design v0_1, sections 3 and 4 (design/variations/VARIATIONS_design_v0_1.md,
md5 fcf6f6fe), as ruled on 2026-09-26 (R-V1..R-V6; canon v38.42 adversarial_map.variations_rulings_V0).
The contract it enforces is argument_shapes_schema_v0_1.json beside it; --self-test asserts that the two
agree.

THE SAME CODE AS THE MAP. The locus and text functions come from the map validator v0_6
(adversarial_map_staging/adv_map_validator_v0_6.py), loaded at its pinned md5 c002e938 through pinned.py,
never re-typed here: locus_valid (a locus exists on a node, with archetypeVariants.<slot> and note
existence-gated), locus_text, wc, non_ascii_chars, DASH_TOKEN_RE, objections_digest and PHASES. v0_6
computes its anchor rule inline, not in a function, so anchor_ok() below restates that one expression
over v0_6's own locus_text and wc: non-empty, at most 15 words, a verbatim substring of the locus text.
The map validator is NOT bumped here: its argumentShapes locus rides the successor map's bump (R0194).

WHAT IT READS
  A staging file:   {"meta": {...}, "shapes": [<shape>, ...]}
  The corpus:       with --embedded, every node's top-level argumentShapes list.
  The corpus a staging file is checked against is the one its meta.source_corpus_md5 pins, read at that
  md5 (the working copy if it matches, else the committed blob). --corpus PATH overrides, explicitly.

CHECKS (each one is a line in the output; a staging run and an --embedded run share them)
  container-shape   staging: {meta, shapes} and nothing else; embedded: argumentShapes is a list, and is
                    never under responses (the game embeds responses whole)
  meta-corpus-pin   meta.source_corpus_md5 == the corpus read; source_corpus_objections_md5, if declared
  meta-bound-for    meta.bound_for is "corpus" or "staging"
  shape-keys        the required keys, and no others (class is also required in a staging file)
  shape-id          <node-id>/<slug>; the node resolves (embedded: it is the host node); unique across
                    every file loaded together
  label-band        3-6 words, ASCII
  statement-band    30-70 words
  statement-ascii   ASCII, no standalone dash token (v0_6's DASH_TOKEN_RE)
  differs-by        a non-empty ASCII string
  class-enum        class, where present, is a, b, c or d
  class-corpus-a    anything bound for the corpus is class a (R-V2); absent class there means a
  attested-by       non-empty; each item is a realWorldExamples instance_id ATTACHED TO THIS NODE, or
                    {"citation": "<non-empty>"}
  answered-by       a list of {locus, anchor}; non-empty for classes a and b
  answered-locus    "<node-id>#<locus>": the node resolves and v0_6's locus_valid accepts the locus
  anchor-rule       non-empty, <=15 words, verbatim at that locus (checked only where the locus exists)
  provenance        {phase, date, seat}; phase in SHAPE_PHASES ("S", disjoint from the map's PHASES)
  shape-cap-node    at most 3 shapes per node across every file loaded together (the pilot's cap)
  shape-coverage    staging only, REQUIRED: meta.shape_coverage "<nodes with a shape in THIS file>/<nodes
                    in the corpus>", gated against this file alone (ccclxx)

Field checks run only where the key is present; an absent key is shape-keys' failure alone, so every
mutation in the self-test turns exactly one check RED.

Usage:
  python3 shape_validator_v0_1.py <fragment.json> [...] [--corpus PATH]
  python3 shape_validator_v0_1.py --embedded [--corpus PATH]      # default: the working corpus
  python3 shape_validator_v0_1.py --self-test [--write | --check]  # record: shape_validator_control_v0_1.json
"""
import copy, hashlib, json, os, re, shutil, sys, tempfile, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
from pinned import bytes_at, path_at  # noqa: E402

MAPV_REL = "adversarial_map_staging/adv_map_validator_v0_6.py"
MAPV_MD5 = "c002e93877b09d523daf786036af7a57"
CORPUS_REL = "efilist_argument_library_v4_0_0.json"
SCHEMA_REL = "argument_shapes/argument_shapes_schema_v0_1.json"
RECORD_REL = "argument_shapes/shape_validator_control_v0_1.json"
# The corpus the real-corpus controls read: v4.1.5, the pin at V1's open (efilist 22b6229).
REAL_CORPUS_MD5 = "7b6e65e531018fecb37baf2a4fedd6d1"


def _load_map_validator():
    src = bytes_at(REPO, MAPV_REL, MAPV_MD5)
    mod = types.ModuleType("adv_map_validator_v0_6")
    mod.__file__ = os.path.join(REPO, MAPV_REL)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


MAPV = _load_map_validator()
locus_valid = MAPV.locus_valid
locus_text = MAPV.locus_text
wc = MAPV.wc
non_ascii_chars = MAPV.non_ascii_chars
DASH_TOKEN_RE = MAPV.DASH_TOKEN_RE
objections_digest = MAPV.objections_digest

REQUIRED_KEYS = ("shape_id", "label", "statement", "differs_by", "attested_by", "answered_by", "provenance")
OPTIONAL_KEYS = ("class",)
CLASSES = ("a", "b", "c", "d")
ANSWERED_CLASSES = ("a", "b")
BOUND_FOR = ("corpus", "staging")
SHAPE_PHASES = ("S",)
LABEL_WORDS = (3, 6)
STATEMENT_WORDS = (30, 70)
ANCHOR_MAX_WORDS = 15
SHAPES_PER_NODE = 3
PROVENANCE_KEYS = ("phase", "date", "seat")
SHAPE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CHECKS = ("container-shape", "meta-corpus-pin", "meta-bound-for", "shape-keys", "shape-id", "label-band",
          "statement-band", "statement-ascii", "differs-by", "class-enum", "class-corpus-a", "attested-by",
          "answered-by", "answered-locus", "anchor-rule", "provenance", "shape-cap-node", "shape-coverage")
assert not set(SHAPE_PHASES) & set(MAPV.PHASES), "a shape phase letter collides with the map's PHASES"


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def anchor_ok(node, locus, anchor):
    """v0_6's anchor-rule expression, over v0_6's own locus_text and wc."""
    return (isinstance(anchor, str) and anchor.strip() != "" and wc(anchor) <= ANCHOR_MAX_WORDS
            and anchor in locus_text(node, locus))


def _ascii_ok(s):
    return isinstance(s, str) and not non_ascii_chars(s)


class _Run:
    def __init__(self):
        self.counts = {c: [0, 0] for c in CHECKS}
        self.violations = []

    def note(self, check, ok, msg):
        self.counts[check][0 if ok else 1] += 1
        if not ok:
            self.violations.append("%s: %s" % (check, msg))

    def failed(self):
        return sorted(c for c, (_ok, bad) in self.counts.items() if bad)


def _check_shape(run, s, tag, nodes, rwe, bound, host=None, seen_ids=None, per_node=None):
    """One shape. `bound` is "corpus" or "staging"; `host` is the node id in --embedded mode."""
    if not isinstance(s, dict):
        run.note("shape-keys", False, "%s: not an object" % tag)
        return
    keys = set(s)
    required = set(REQUIRED_KEYS) | ({"class"} if bound == "staging" else set())
    allowed = set(REQUIRED_KEYS) | set(OPTIONAL_KEYS)
    missing, extra = sorted(required - keys), sorted(keys - allowed)
    run.note("shape-keys", not missing and not extra, "%s: missing %s, unknown %s" % (tag, missing, extra))

    node_id = None
    if "shape_id" in s:
        sid = s["shape_id"]
        ok = isinstance(sid, str) and bool(SHAPE_ID_RE.match(sid))
        why = "not <node-id>/<slug>"
        if ok:
            node_id = sid.split("/", 1)[0]
            if node_id not in nodes:
                ok, why = False, "node %r not in the corpus" % node_id
            elif host is not None and node_id != host:
                ok, why = False, "sits on %r but names %r" % (host, node_id)
            elif seen_ids is not None and sid in seen_ids:
                ok, why = False, "duplicate id (also %s)" % seen_ids[sid]
        run.note("shape-id", ok, "%s: %s" % (tag, why))
        if ok:
            if seen_ids is not None:
                seen_ids[sid] = tag
            if per_node is not None:
                per_node.setdefault(node_id, []).append(tag)
        else:
            node_id = None

    if "label" in s:
        lb = s["label"]
        ok = isinstance(lb, str) and LABEL_WORDS[0] <= wc(lb) <= LABEL_WORDS[1] and _ascii_ok(lb)
        run.note("label-band", ok, "%s: label must be %d-%d ASCII words" % ((tag,) + LABEL_WORDS))
    if "statement" in s:
        st = s["statement"]
        n = wc(st) if isinstance(st, str) else -1
        run.note("statement-band", STATEMENT_WORDS[0] <= n <= STATEMENT_WORDS[1],
                 "%s: statement has %d words (band %d-%d)" % ((tag, n) + STATEMENT_WORDS))
        why = []
        if not isinstance(st, str):
            why.append("not a string")
        else:
            if non_ascii_chars(st):
                why.append("non-ASCII %r" % non_ascii_chars(st))
            if DASH_TOKEN_RE.search(st):
                why.append("standalone dash token")
        run.note("statement-ascii", not why, "%s: %s" % (tag, "; ".join(why)))
    if "differs_by" in s:
        d = s["differs_by"]
        run.note("differs-by", isinstance(d, str) and d.strip() != "" and _ascii_ok(d),
                 "%s: differs_by must be a non-empty ASCII sentence" % tag)

    cls = s.get("class")
    if "class" in s:
        run.note("class-enum", cls in CLASSES, "%s: class %r not in %s" % (tag, cls, CLASSES))
    eff_cls = cls if "class" in s else ("a" if bound == "corpus" else None)
    if bound == "corpus":
        run.note("class-corpus-a", eff_cls == "a",
                 "%s: bound for the corpus but class %r (R-V2: the corpus carries (a) only)" % (tag, cls))

    if "attested_by" in s:
        att = s["attested_by"]
        why = []
        if not isinstance(att, list) or not att:
            why.append("must be a non-empty list")
        else:
            for i, a in enumerate(att):
                if isinstance(a, str):
                    r = rwe.get(a)
                    if r is None:
                        why.append("[%d] instance %r not in realWorldExamples" % (i, a))
                    elif node_id is not None and node_id not in {x.get("objection_id") for x in
                                                                 r.get("attached_objections") or []}:
                        why.append("[%d] instance %r is not attached to %r" % (i, a, node_id))
                elif isinstance(a, dict):
                    if set(a) != {"citation"} or not isinstance(a["citation"], str) or not a["citation"].strip():
                        why.append("[%d] a citation is exactly {\"citation\": <non-empty>}" % i)
                else:
                    why.append("[%d] neither an instance_id nor a citation" % i)
        run.note("attested-by", not why, "%s: %s" % (tag, "; ".join(why)))

    if "answered_by" in s:
        ab = s["answered_by"]
        why = []
        items = []
        if not isinstance(ab, list):
            why.append("not a list")
        else:
            if eff_cls in ANSWERED_CLASSES and not ab:
                why.append("class %r needs at least one answering locus" % eff_cls)
            for i, it in enumerate(ab):
                if isinstance(it, dict) and set(it) == {"locus", "anchor"} and isinstance(it["locus"], str):
                    items.append((i, it))
                else:
                    why.append("[%d] must be exactly {locus: str, anchor: str}" % i)
        run.note("answered-by", not why, "%s: %s" % (tag, "; ".join(why)))
        for i, it in items:
            loc = it["locus"]
            lwhy = None
            if "#" not in loc:
                lwhy = "%r is not <node-id>#<locus>" % loc
            else:
                nid, lc = loc.split("#", 1)
                if nid not in nodes:
                    lwhy = "node %r not in the corpus" % nid
                elif not locus_valid(nodes[nid], lc):
                    lwhy = "%r does not exist on %r" % (lc, nid)
            run.note("answered-locus", lwhy is None, "%s answered_by[%d]: %s" % (tag, i, lwhy))
            if lwhy is None:
                run.note("anchor-rule", anchor_ok(nodes[nid], lc, it["anchor"]),
                         "%s answered_by[%d]: anchor empty, over %d words, or not verbatim at %s"
                         % (tag, i, ANCHOR_MAX_WORDS, loc))

    if "provenance" in s:
        p = s["provenance"]
        ok = (isinstance(p, dict) and set(p) == set(PROVENANCE_KEYS) and p.get("phase") in SHAPE_PHASES
              and isinstance(p.get("date"), str) and bool(DATE_RE.match(p["date"]))
              and isinstance(p.get("seat"), str) and p["seat"].strip() != "")
        run.note("provenance", ok, "%s: provenance must be {phase in %s, date YYYY-MM-DD, seat}"
                 % (tag, SHAPE_PHASES))


def _report(run, out, extra):
    for c in CHECKS:
        ok_n, bad_n = run.counts[c]
        out("%s . %s (%d ok / %d fail)" % ("PASS" if bad_n == 0 else "FAIL", c, ok_n, bad_n))
    verdict = "PASS" if not run.violations else "FAIL"
    summary = dict(extra)
    summary.update({"violation_count": len(run.violations), "violations": run.violations[:25],
                    "verdict": verdict})
    out(json.dumps(summary, indent=1, sort_keys=True))
    return verdict == "PASS"


def _load_corpus(corpus_path):
    raw = open(corpus_path, "rb").read()
    corpus = json.loads(raw.decode("utf-8"))
    nodes = {n["id"]: n for n in corpus["objections"]}
    rwe = {r["instance_id"]: r for r in corpus.get("realWorldExamples") or [] if "instance_id" in r}
    return raw, corpus, nodes, rwe


def validate(paths, corpus_path, out=print):
    """Staging files against one corpus. Returns (ok, failed_checks, violations)."""
    raw, corpus, nodes, rwe = _load_corpus(corpus_path)
    run = _Run()
    seen_ids, per_node, n_shapes = {}, {}, 0
    for p in paths:
        base = os.path.basename(p)
        doc = json.loads(open(p, "rb").read().decode("utf-8"))
        ok = isinstance(doc, dict) and set(doc) == {"meta", "shapes"} and isinstance(doc.get("meta"), dict) \
            and isinstance(doc.get("shapes"), list)
        run.note("container-shape", ok, "%s: must be exactly {meta: {...}, shapes: [...]}" % base)
        if not ok:
            continue
        meta, shapes = doc["meta"], doc["shapes"]
        pin_ok = meta.get("source_corpus_md5") == md5_bytes(raw)
        if pin_ok and "source_corpus_objections_md5" in meta:
            pin_ok = meta["source_corpus_objections_md5"] == objections_digest(corpus)
        run.note("meta-corpus-pin", pin_ok, "%s: the corpus pin does not match the corpus read" % base)
        bound = meta.get("bound_for")
        run.note("meta-bound-for", bound in BOUND_FOR, "%s: bound_for %r not in %s" % (base, bound, BOUND_FOR))
        eff_bound = bound if bound in BOUND_FOR else "staging"
        own = set()
        for i, s in enumerate(shapes):
            n_shapes += 1
            tag = "%s[%d] %s" % (base, i, s.get("shape_id") if isinstance(s, dict) else "?")
            before = {k: len(v) for k, v in per_node.items()}
            _check_shape(run, s, tag, nodes, rwe, eff_bound, seen_ids=seen_ids, per_node=per_node)
            own.update(k for k, v in per_node.items() if len(v) > before.get(k, 0))
        own_cov = "%d/%d" % (len(own), len(nodes))
        run.note("shape-coverage", meta.get("shape_coverage") == own_cov,
                 "%s: declared %r vs this file's %r" % (base, meta.get("shape_coverage"), own_cov))
    for nid, tags in sorted(per_node.items()):
        run.note("shape-cap-node", len(tags) <= SHAPES_PER_NODE,
                 "%r has %d shapes (cap %d)" % (nid, len(tags), SHAPES_PER_NODE))
    ok = _report(run, out, {"mode": "staging", "files": len(paths), "shapes": n_shapes,
                            "nodes_with_shapes": len(per_node), "corpus_md5": md5_bytes(raw)})
    return ok, run.failed(), run.violations


def validate_embedded(corpus_path, out=print):
    """The corpus's own argumentShapes: bound for the corpus by definition."""
    raw, corpus, nodes, rwe = _load_corpus(corpus_path)
    run = _Run()
    seen_ids, per_node, n_shapes = {}, {}, 0
    for n in corpus["objections"]:
        if "argumentShapes" in (n.get("responses") or {}):
            run.note("container-shape", False, "%s: argumentShapes under responses (it is a top-level key)"
                     % n["id"])
        if "argumentShapes" not in n:
            continue
        shapes = n["argumentShapes"]
        run.note("container-shape", isinstance(shapes, list), "%s: argumentShapes is not a list" % n["id"])
        if not isinstance(shapes, list):
            continue
        for i, s in enumerate(shapes):
            n_shapes += 1
            _check_shape(run, s, "%s.argumentShapes[%d]" % (n["id"], i), nodes, rwe, "corpus",
                         host=n["id"], seen_ids=seen_ids, per_node=per_node)
    for nid, tags in sorted(per_node.items()):
        run.note("shape-cap-node", len(tags) <= SHAPES_PER_NODE,
                 "%r has %d shapes (cap %d)" % (nid, len(tags), SHAPES_PER_NODE))
    ok = _report(run, out, {"mode": "embedded", "shapes": n_shapes, "nodes_with_shapes": len(per_node),
                            "shape_coverage": "%d/%d" % (len(per_node), len(nodes)),
                            "corpus_md5": md5_bytes(raw)})
    return ok, run.failed(), run.violations


# ---------------------------------------------------------------- self-test

def _words(n, w="word"):
    return " ".join([w] * n)


def _mini_corpus():
    long_x = ("The quick brown fox jumps over the lazy dog while the library answers the objection in full, "
              "naming its premise and the cost of holding it.")
    return {
        "version": "mini",
        "objections": [
            {"id": "node-x", "tier": 1, "trigger": ["x"], "diagnosis": "diagnosis text for node x",
             "responses": {"short": "short text x", "medium": "medium text x", "long": long_x}},
            {"id": "node-y", "tier": 2, "trigger": ["y"], "diagnosis": "diagnosis text for node y",
             "responses": {"short": "short text y", "medium": "medium text y", "long": "long text y",
                           "archetypeVariants": {"sophisticate": "the sophisticate reply names the bad faith "
                                                                 "in the move and answers it"}}},
            {"id": "node-z", "tier": 3, "trigger": ["z"], "diagnosis": "diagnosis text for node z",
             "note": "a note conceding kappa lambda mu for node z",
             "responses": {"short": "short text z", "medium": "medium text z", "long": "long text z"}},
        ],
        "realWorldExamples": [
            {"instance_id": "inst-x-001", "attached_objections": [{"objection_id": "node-x"}]},
            {"instance_id": "inst-y-001", "attached_objections": [{"objection_id": "node-y"}]},
        ],
    }


def _shape(sid, cls, answered, attested, statement_words=40):
    s = {"shape_id": sid, "label": "a shape label here", "statement": _words(statement_words),
         "differs_by": "It argues from a different premise.", "class": cls,
         "attested_by": attested, "answered_by": answered,
         "provenance": {"phase": "S", "date": "2026-09-26", "seat": "self-test"}}
    return s


def _base_fragment(corpus_md5, digest):
    return {"meta": {"source_corpus_md5": corpus_md5, "source_corpus_objections_md5": digest,
                     "bound_for": "staging", "shape_coverage": "2/3"},
            "shapes": [
                _shape("node-x/first-shape", "a", [{"locus": "node-x#long", "anchor": "the lazy dog"}],
                       ["inst-x-001"]),
                _shape("node-y/variant-routed", "a",
                       [{"locus": "node-y#archetypeVariants.sophisticate", "anchor": "names the bad faith"}],
                       [{"citation": "Author, Title, 2020, p. 1"}]),
                _shape("node-x/cross-node", "b", [{"locus": "node-z#note", "anchor": "conceding kappa lambda mu"}],
                       ["inst-x-001"]),
            ]}


def self_test():
    tmp = tempfile.mkdtemp(prefix="shape_selftest_")
    results = []
    try:
        mini = _mini_corpus()
        cpath = os.path.join(tmp, "mini_corpus.json")
        cbytes = (json.dumps(mini, indent=2, sort_keys=True) + "\n").encode("utf-8")
        open(cpath, "wb").write(cbytes)
        cmd5, cdig = md5_bytes(cbytes), objections_digest(mini)
        counter = [0]

        def write(doc):
            counter[0] += 1
            p = os.path.join(tmp, "frag_%03d.json" % counter[0])
            open(p, "w").write(json.dumps(doc, indent=1))
            return p

        def run_case(name, docs, expect, corpus_path=cpath, embedded=False):
            sink = []
            if embedded:
                ok, failed, _v = validate_embedded(corpus_path, out=sink.append)
            else:
                ok, failed, _v = validate([write(d) for d in docs], corpus_path, out=sink.append)
            want = [] if expect is None else [expect]
            results.append({"case": name, "expect": expect or "PASS", "failed": failed, "ok": failed == want})

        def mut(fn, bound=None):
            d = _base_fragment(cmd5, cdig)
            if bound:
                d["meta"]["bound_for"] = bound
            fn(d)
            return d

        S = lambda d, i: d["shapes"][i]  # noqa: E731

        # 0. the unmutated control, FIRST
        run_case("control-staging", [_base_fragment(cmd5, cdig)], None)

        def all_a(d):
            S(d, 2)["class"] = "a"
        run_case("control-bound-corpus", [mut(all_a, "corpus")], None)

        def two_files():
            a, b = _base_fragment(cmd5, cdig), _base_fragment(cmd5, cdig)
            a["shapes"] = a["shapes"][:1]
            a["meta"]["shape_coverage"] = "1/3"
            b["shapes"] = b["shapes"][1:2]
            b["meta"]["shape_coverage"] = "1/3"
            return [a, b]
        run_case("control-two-files-own-coverage", two_files(), None)

        # container-shape, meta-*
        run_case("container-extra-key", [mut(lambda d: d.__setitem__("extra", 1))], "container-shape")
        run_case("meta-pin-wrong", [mut(lambda d: d["meta"].__setitem__("source_corpus_md5", "0" * 32))],
                 "meta-corpus-pin")
        run_case("meta-digest-wrong",
                 [mut(lambda d: d["meta"].__setitem__("source_corpus_objections_md5", "0" * 32))],
                 "meta-corpus-pin")
        run_case("meta-bound-for-unknown", [mut(lambda d: d["meta"].__setitem__("bound_for", "public"))],
                 "meta-bound-for")
        # shape-keys
        run_case("keys-unknown", [mut(lambda d: S(d, 0).__setitem__("scholar", "x"))], "shape-keys")
        run_case("keys-missing-differs-by", [mut(lambda d: S(d, 0).pop("differs_by"))], "shape-keys")
        run_case("keys-staging-needs-class", [mut(lambda d: S(d, 0).pop("class"))], "shape-keys")
        # shape-id
        run_case("id-bad-format", [mut(lambda d: S(d, 2).__setitem__("shape_id", "node-x_cross"))], "shape-id")
        run_case("id-unknown-node", [mut(lambda d: S(d, 2).__setitem__("shape_id", "node-q/cross-node"))],
                 "shape-id")
        run_case("id-duplicate", [mut(lambda d: S(d, 2).__setitem__("shape_id", "node-x/first-shape"))],
                 "shape-id")

        def dup_across():
            a, b = two_files()
            b["shapes"].append(copy.deepcopy(a["shapes"][0]))  # b keeps its own node-y shape
            b["meta"]["shape_coverage"] = "1/3"
            return [a, b]
        run_case("id-duplicate-across-files", dup_across(), "shape-id")
        # label, statement, differs_by
        run_case("label-two-words", [mut(lambda d: S(d, 0).__setitem__("label", "two words"))], "label-band")
        run_case("label-seven-words", [mut(lambda d: S(d, 0).__setitem__("label", _words(7)))], "label-band")
        run_case("statement-29-words", [mut(lambda d: S(d, 0).__setitem__("statement", _words(29)))],
                 "statement-band")
        run_case("statement-71-words", [mut(lambda d: S(d, 0).__setitem__("statement", _words(71)))],
                 "statement-band")
        run_case("statement-em-dash", [mut(lambda d: S(d, 0).__setitem__(
            "statement", _words(20) + " cost—benefit " + _words(19)))], "statement-ascii")
        run_case("statement-dash-token", [mut(lambda d: S(d, 0).__setitem__(
            "statement", _words(20) + " - " + _words(20)))], "statement-ascii")
        run_case("differs-by-empty", [mut(lambda d: S(d, 0).__setitem__("differs_by", " "))], "differs-by")
        # class
        run_case("class-unknown", [mut(lambda d: S(d, 2).__setitem__("class", "e"))], "class-enum")
        run_case("class-b-bound-for-corpus", [mut(lambda d: None, "corpus")], "class-corpus-a")
        # attested_by
        run_case("attested-empty", [mut(lambda d: S(d, 0).__setitem__("attested_by", []))], "attested-by")
        run_case("attested-unknown-instance", [mut(lambda d: S(d, 0).__setitem__("attested_by", ["inst-q-001"]))],
                 "attested-by")
        run_case("attested-instance-on-another-node",
                 [mut(lambda d: S(d, 0).__setitem__("attested_by", ["inst-y-001"]))], "attested-by")
        run_case("attested-citation-empty",
                 [mut(lambda d: S(d, 1).__setitem__("attested_by", [{"citation": ""}]))], "attested-by")
        run_case("attested-citation-extra-key",
                 [mut(lambda d: S(d, 1).__setitem__("attested_by", [{"citation": "A", "url": "u"}]))],
                 "attested-by")
        # answered_by
        run_case("answered-empty-for-a", [mut(lambda d: S(d, 0).__setitem__("answered_by", []))], "answered-by")
        run_case("answered-empty-for-b", [mut(lambda d: S(d, 2).__setitem__("answered_by", []))], "answered-by")

        def empty_for_d(d):
            S(d, 2)["class"] = "d"
            S(d, 2)["answered_by"] = []
        run_case("control-answered-empty-for-d", [mut(empty_for_d)], None)
        run_case("answered-item-missing-anchor",
                 [mut(lambda d: S(d, 0).__setitem__("answered_by", [{"locus": "node-x#long"}]))], "answered-by")
        # answered-locus (existence-gated, by v0_6's locus_valid)
        for nm, loc in (("locus-unknown", "node-x#longer"), ("locus-no-hash", "node-x.long"),
                        ("locus-unknown-node", "node-q#long"),
                        ("locus-variant-absent", "node-x#archetypeVariants.defender"),
                        ("locus-note-absent", "node-x#note")):
            run_case(nm, [mut(lambda d, loc=loc: S(d, 0).__setitem__(
                "answered_by", [{"locus": loc, "anchor": "the lazy dog"}]))], "answered-locus")
        # anchor-rule
        run_case("anchor-not-verbatim", [mut(lambda d: S(d, 0)["answered_by"][0].__setitem__(
            "anchor", "the lazy cat"))], "anchor-rule")
        run_case("anchor-16-words", [mut(lambda d: S(d, 0)["answered_by"][0].__setitem__(
            "anchor", _words(16)))], "anchor-rule")
        run_case("anchor-empty", [mut(lambda d: S(d, 0)["answered_by"][0].__setitem__("anchor", " "))],
                 "anchor-rule")
        run_case("anchor-from-long-at-variant", [mut(lambda d: S(d, 1).__setitem__("answered_by", [
            {"locus": "node-y#archetypeVariants.sophisticate", "anchor": "long text y"}]))], "anchor-rule")
        # provenance
        run_case("provenance-map-phase", [mut(lambda d: S(d, 0)["provenance"].__setitem__("phase", "A"))],
                 "provenance")
        run_case("provenance-bad-date", [mut(lambda d: S(d, 0)["provenance"].__setitem__("date", "26-09-2026"))],
                 "provenance")
        run_case("provenance-no-seat", [mut(lambda d: S(d, 0)["provenance"].__setitem__("seat", ""))],
                 "provenance")
        # shape-cap-node

        def four_on_y(d):
            for k in range(3):
                s = copy.deepcopy(S(d, 1))
                s["shape_id"] = "node-y/extra-%d" % k
                d["shapes"].append(s)
        run_case("cap-four-on-one-node", [mut(four_on_y)], "shape-cap-node")

        def cap_across():
            a, b = two_files()
            for doc, pre in ((a, "a"), (b, "b")):
                s1, s2 = copy.deepcopy(_base_fragment(cmd5, cdig)["shapes"][1]), None
                s1["shape_id"] = "node-y/from-%s-1" % pre
                s2 = copy.deepcopy(s1)
                s2["shape_id"] = "node-y/from-%s-2" % pre
                doc["shapes"] += [s1, s2]
            a["meta"]["shape_coverage"] = "2/3"
            b["meta"]["shape_coverage"] = "1/3"
            return [a, b]
        run_case("cap-across-files", cap_across(), "shape-cap-node")
        # shape-coverage
        run_case("coverage-overclaimed", [mut(lambda d: d["meta"].__setitem__("shape_coverage", "3/3"))],
                 "shape-coverage")
        run_case("coverage-undeclared", [mut(lambda d: d["meta"].pop("shape_coverage"))], "shape-coverage")

        def two_files_summed():
            a, b = two_files()
            a["meta"]["shape_coverage"] = b["meta"]["shape_coverage"] = "2/3"
            return [a, b]
        run_case("coverage-summed-across-files", two_files_summed(), "shape-coverage")

        # --embedded: the corpus's own argumentShapes
        def embedded_case(name, fn, expect):
            c = _mini_corpus()
            s = _shape("node-x/first-shape", "a", [{"locus": "node-x#long", "anchor": "the lazy dog"}],
                       ["inst-x-001"])
            s.pop("class")
            c["objections"][0]["argumentShapes"] = [s]
            fn(c)
            p = os.path.join(tmp, "embedded_%s.json" % name)
            open(p, "w").write(json.dumps(c, indent=2, sort_keys=True) + "\n")
            run_case(name, None, expect, corpus_path=p, embedded=True)
        embedded_case("control-embedded", lambda c: None, None)
        embedded_case("embedded-under-responses", lambda c: c["objections"][1]["responses"].__setitem__(
            "argumentShapes", []), "container-shape")
        embedded_case("embedded-not-a-list", lambda c: c["objections"][0].__setitem__(
            "argumentShapes", {}), "container-shape")
        embedded_case("embedded-class-b", lambda c: c["objections"][0]["argumentShapes"][0].__setitem__(
            "class", "b"), "class-corpus-a")
        embedded_case("embedded-wrong-host", lambda c: c["objections"][0]["argumentShapes"][0].__setitem__(
            "shape_id", "node-y/first-shape"), "shape-id")

        # the real corpus, read at its pin: existence-gating and RWE attachment on true data
        rpath = path_at(REPO, CORPUS_REL, REAL_CORPUS_MD5)
        rraw, rcorpus, rnodes, _rwe = _load_corpus(rpath)

        def cut(nid, locus, n=8):
            m = re.match(r"\S+(?:\s+\S+){%d}" % (n - 1), locus_text(rnodes[nid], locus).strip())
            return m.group(0)

        def real(shapes, cov):
            return {"meta": {"source_corpus_md5": md5_bytes(rraw),
                             "source_corpus_objections_md5": objections_digest(rcorpus),
                             "bound_for": "corpus", "shape_coverage": cov}, "shapes": shapes}
        fs = _shape("future-solve/control-variant", "a",
                    [{"locus": "future-solve#archetypeVariants.sophisticate",
                      "anchor": cut("future-solve", "archetypeVariants.sophisticate")}],
                    [{"citation": "self-test control, not a shape"}])
        ms = _shape("meaning-through-suffering/control-rwe", "a",
                    [{"locus": "meaning-through-suffering#long", "anchor": cut("meaning-through-suffering", "long")}],
                    ["peterson-better-never-meaning-through-suffering-001"])
        n_real = len(rnodes)
        run_case("real-control", [real([fs, ms], "2/%d" % n_real)], None, corpus_path=rpath)
        lg = _shape("life-gift/control-absent-variant", "a",
                    [{"locus": "life-gift#archetypeVariants.sophisticate", "anchor": cut("life-gift", "long")}],
                    [{"citation": "self-test control, not a shape"}])
        run_case("real-variant-absent-on-life-gift", [real([lg], "1/%d" % n_real)], "answered-locus",
                 corpus_path=rpath)
        lr = _shape("life-gift/control-rwe-elsewhere", "a",
                    [{"locus": "life-gift#long", "anchor": cut("life-gift", "long")}],
                    ["peterson-better-never-meaning-through-suffering-001"])
        run_case("real-rwe-attached-elsewhere", [real([lr], "1/%d" % n_real)], "attested-by", corpus_path=rpath)
        results.append({"case": "real-corpus-has-no-argumentShapes-yet",
                        "expect": "0 nodes", "failed": [],
                        "ok": not any("argumentShapes" in n for n in rcorpus["objections"])})

        # the schema file and the validator agree
        sch = json.loads(open(os.path.join(REPO, SCHEMA_REL), "rb").read().decode("utf-8"))
        sh = sch["$defs"]["shape"]
        pr = sh["properties"]
        agree = {
            "required": sorted(sh["required"]) == sorted(REQUIRED_KEYS),
            "optional": sorted(set(pr) - set(sh["required"])) == sorted(OPTIONAL_KEYS),
            "label": pr["label"]["x-words"] == list(LABEL_WORDS),
            "statement": pr["statement"]["x-words"] == list(STATEMENT_WORDS),
            "anchor": pr["answered_by"]["items"]["properties"]["anchor"]["x-words"] == [1, ANCHOR_MAX_WORDS],
            "classes": pr["class"]["enum"] == list(CLASSES),
            "phases": pr["provenance"]["properties"]["phase"]["enum"] == list(SHAPE_PHASES),
            "provenance": sorted(pr["provenance"]["required"]) == sorted(PROVENANCE_KEYS),
            "bound_for": sch["properties"]["meta"]["properties"]["bound_for"]["enum"] == list(BOUND_FOR),
            "cap": sch["x-caps"]["shapes_per_node"] == SHAPES_PER_NODE,
            "shape_id_re": pr["shape_id"]["pattern"].replace("(-", "(?:-") == SHAPE_ID_RE.pattern,
        }
        results.append({"case": "schema-agrees-with-validator", "expect": "all true",
                        "failed": sorted(k for k, v in agree.items() if not v), "ok": all(agree.values())})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    fired = sorted({r["expect"] for r in results if r["expect"] in CHECKS})
    record = {
        "instrument": "argument_shapes/shape_validator_v0_1.py",
        "map_validator": {"path": MAPV_REL, "md5": MAPV_MD5},
        "real_corpus_md5": REAL_CORPUS_MD5,
        "cases": results,
        "summary": {"cases": len(results), "as_expected": sum(r["ok"] for r in results),
                    "checks": len(CHECKS), "checks_turned_red_by_a_mutation": len(fired),
                    "checks_never_turned_red": sorted(set(CHECKS) - set(fired)),
                    "first_case_is_the_unmutated_control": results[0]["case"] == "control-staging"},
    }
    return record


def main(argv):
    if "--self-test" in argv:
        rec = self_test()
        text = json.dumps(rec, indent=1, sort_keys=True) + "\n"
        ok = rec["summary"]["as_expected"] == rec["summary"]["cases"] \
            and not rec["summary"]["checks_never_turned_red"] and rec["summary"]["first_case_is_the_unmutated_control"]
        rp = os.path.join(REPO, RECORD_REL)
        if "--write" in argv:
            open(rp, "w").write(text)
            print("wrote %s  md5 %s" % (RECORD_REL, md5_bytes(text.encode())))
        elif "--check" in argv:
            same = os.path.exists(rp) and open(rp, "rb").read() == text.encode()
            print("%s: %s" % (RECORD_REL, "reproduced byte for byte" if same else "DIFFERS from a fresh run"))
            ok = ok and same
        for r in rec["cases"]:
            print("%s  %-44s expect %-16s failed %s" % ("ok " if r["ok"] else "BAD", r["case"], r["expect"],
                                                         r["failed"]))
        print("SELF-TEST %s: %d of %d as expected; %d of %d checks turned RED by a mutation"
              % ("GREEN" if ok else "RED", rec["summary"]["as_expected"], rec["summary"]["cases"],
                 rec["summary"]["checks_turned_red_by_a_mutation"], rec["summary"]["checks"]))
        return 0 if ok else 1
    corpus = None
    if "--corpus" in argv:
        corpus = argv[argv.index("--corpus") + 1]
    if "--embedded" in argv:
        ok, _f, _v = validate_embedded(corpus or os.path.join(REPO, CORPUS_REL))
        return 0 if ok else 1
    files = [a for i, a in enumerate(argv) if not a.startswith("--") and not (i > 0 and argv[i - 1] == "--corpus")]
    if not files:
        print(__doc__)
        return 2
    if corpus is None:
        pin = json.loads(open(files[0], "rb").read().decode("utf-8")).get("meta", {}).get("source_corpus_md5")
        corpus = path_at(REPO, CORPUS_REL, pin)
        print("corpus: %s at %s (pinned by %s)" % (CORPUS_REL, pin, os.path.basename(files[0])))
    ok, _f, _v = validate(files, corpus)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
