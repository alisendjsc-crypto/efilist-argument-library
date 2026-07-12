#!/usr/bin/env python3
"""adv_map_validator_v0_1.py -- adversarial-map fragment / assembly validator (v0.1.0)

Implements the machine checks of adversarial_map_design_v0_1.md section 6 against
adversarial_map_schema_v0_1.json (both staged in adversarial_map_staging/).

Container contract (defined here + staging README; the schema sibling pins the ENTRY):
  { "meta": { ... source-corpus pin ... }, "entries": [ <entry per schema>, ... ] }

Usage:
  python3 adv_map_validator_v0_1.py <fragment.json> [<fragment2.json> ...] --corpus <corpus.json> [--terminal]
  python3 adv_map_validator_v0_1.py --self-test

Checks (names printed one PASS/FAIL line each):
  container-shape        top-level {meta, entries}; entries is a list of dicts
  serialization          each file round-trips json.dumps(indent=2, ensure_ascii=False)+'\\n'
  meta-corpus-pin        meta names the source corpus + an md5 (>=8-char prefix) matching --corpus
  entry-keys             exactly the 9 schema keys per entry
  target-id              target_id in the corpus id set
  target-locus           target_locus in {short, medium, long, diagnosis}
  anchor-rule            target_anchor nonempty, <=15 words, verbatim substring at target_locus
  move-band              adversarial_move 40-150 words; class (a) additionally <=60
  class-enum             class in {a, b, c, d}
  grounds                grounds nonempty string
  routing-shape          routing carries exactly the one class-shaped key, fields typed + enum-true
  status-enum            status == "mapped" (downstream states live in canon, never the artifact)
  provenance             phase in {A,B1,B2,C,D}; date ISO (YYYY-MM-DD...); seat nonempty
  id-x-anchor-unique     (target_id, target_anchor) unique across all loaded files
  entry-cap              <=3 entries per target_id across all loaded files (Q1, ratified)
  coverage               union arithmetic reported per phase; with --terminal: every corpus id >=1 entry (82/82)
  meta-summaries         IF meta declares class_counts / coverage_distinct_ids, they must equal computed

Exit: 0 all checks pass, 1 any violation, 2 usage error.  Pure ASCII source.
"""
import json, sys, os, hashlib, re, tempfile

LOCI = ("short", "medium", "long", "diagnosis")
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D")
ENTRY_KEYS = ["target_id", "target_locus", "target_anchor", "adversarial_move",
              "class", "grounds", "routing", "status", "provenance"]
AXES = ("v", "s", "c", "r", "a")
IND_GROUNDS = ("presupposition-inversion", "reader-test", "grading-object-integrity")
SEVERITIES = ("minor", "headline")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    return node.get("responses", {}).get(locus, "")


def wc(s):
    return len(s.split())


def validate(map_paths, corpus_path, terminal=False, out=print):
    violations = []
    checks = {}

    def note(check, ok, detail=""):
        checks.setdefault(check, [0, 0])
        checks[check][0 if ok else 1] += 1
        if not ok:
            violations.append("%s: %s" % (check, detail))

    craw = open(corpus_path, "rb").read()
    corpus = json.loads(craw.decode("utf-8"))
    cmd5 = md5_bytes(craw)
    nodes = {o["id"]: o for o in corpus["objections"]}
    ids = set(nodes)

    all_entries = []
    for p in map_paths:
        raw = open(p, "rb").read()
        try:
            doc = json.loads(raw.decode("utf-8"))
        except Exception as e:
            note("container-shape", False, "%s: unparseable JSON (%s)" % (p, e))
            continue
        ok_shape = isinstance(doc, dict) and isinstance(doc.get("meta"), dict) \
            and isinstance(doc.get("entries"), list) \
            and all(isinstance(e, dict) for e in doc.get("entries", []))
        note("container-shape", ok_shape, p)
        canon = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        note("serialization", canon == raw, "%s: not canonical json.dumps(indent=2, ensure_ascii=False)+NL" % p)
        if not ok_shape:
            continue
        meta = doc["meta"]
        pin = ""
        for k in ("source_corpus_md5", "corpus_md5", "source_corpus_md5_prefix_observed"):
            v = meta.get(k)
            if isinstance(v, str) and v:
                pin = v
                break
        note("meta-corpus-pin",
             isinstance(meta.get("source_corpus"), str) and len(pin) >= 8 and cmd5.startswith(pin),
             "%s: meta pin %r vs corpus %s" % (p, pin[:12], cmd5[:12]))
        if isinstance(meta.get("class_counts"), dict):
            comp = {}
            for e in doc["entries"]:
                c = e.get("class")
                comp[c] = comp.get(c, 0) + 1
            note("meta-summaries", {k: v for k, v in meta["class_counts"].items()} == comp,
                 "%s: declared class_counts != computed %s" % (p, comp))
        if "coverage_distinct_ids" in meta:
            comp_n = len(set(e.get("target_id") for e in doc["entries"]))
            note("meta-summaries", meta["coverage_distinct_ids"] == comp_n,
                 "%s: declared coverage_distinct_ids != computed %d" % (p, comp_n))
        for i, e in enumerate(doc["entries"]):
            tag = "%s[%d]" % (os.path.basename(p), i)
            all_entries.append((tag, e))

    for tag, e in all_entries:
        note("entry-keys", sorted(e.keys()) == sorted(ENTRY_KEYS),
             "%s: keys %s" % (tag, sorted(e.keys())))
        if sorted(e.keys()) != sorted(ENTRY_KEYS):
            continue
        tid, locus = e["target_id"], e["target_locus"]
        in_ids = tid in ids
        note("target-id", in_ids, "%s: %r not in corpus" % (tag, tid))
        note("target-locus", locus in LOCI, "%s: %r" % (tag, locus))
        anchor = e["target_anchor"]
        a_ok = isinstance(anchor, str) and anchor.strip() != "" and wc(anchor) <= 15
        if a_ok and in_ids and locus in LOCI:
            a_ok = anchor in locus_text(nodes[tid], locus)
            note("anchor-rule", a_ok, "%s: anchor not a verbatim substring of %s#%s" % (tag, tid, locus))
        else:
            note("anchor-rule", a_ok, "%s: anchor empty or >15 words" % tag)
        klass = e["class"]
        note("class-enum", klass in CLASSES, "%s: %r" % (tag, klass))
        w = wc(e["adversarial_move"]) if isinstance(e["adversarial_move"], str) else -1
        band_ok = 40 <= w <= 150 and (klass != "a" or w <= 60)
        note("move-band", band_ok, "%s: %d words (class %s)" % (tag, w, klass))
        note("grounds", isinstance(e["grounds"], str) and e["grounds"].strip() != "", "%s: empty grounds" % tag)
        r = e["routing"]
        r_ok = isinstance(r, dict)
        if r_ok and klass == "a":
            ab = r.get("answered_by")
            r_ok = set(r) == {"answered_by"} and isinstance(ab, list) and len(ab) > 0
            if r_ok:
                for ref in ab:
                    parts = ref.split("#") if isinstance(ref, str) else []
                    if len(parts) != 2 or parts[0] not in ids or parts[1] not in LOCI:
                        r_ok = False
        elif r_ok and klass == "b":
            rc = r.get("regen_candidate")
            r_ok = set(r) == {"regen_candidate"} and isinstance(rc, dict) \
                and set(rc) == {"axis_hit", "severity"} \
                and isinstance(rc.get("axis_hit"), list) and len(rc["axis_hit"]) > 0 \
                and all(a in AXES for a in rc["axis_hit"]) \
                and rc.get("severity") in SEVERITIES
        elif r_ok and klass == "c":
            ic = r.get("intake_candidate")
            r_ok = set(r) == {"intake_candidate"} and isinstance(ic, dict) \
                and set(ic) == {"proposed_id", "tier_guess", "mechanism_guess", "individuation_grounds"} \
                and isinstance(ic.get("proposed_id"), str) and ic["proposed_id"].strip() != "" \
                and isinstance(ic.get("tier_guess"), int) and 1 <= ic["tier_guess"] <= 5 \
                and isinstance(ic.get("mechanism_guess"), str) and ic["mechanism_guess"].strip() != "" \
                and ic.get("individuation_grounds") in IND_GROUNDS
        elif r_ok and klass == "d":
            rs = r.get("residue")
            r_ok = set(r) == {"residue"} and isinstance(rs, dict) \
                and set(rs) == {"bedrock_name", "terminus_routing", "novel"} \
                and isinstance(rs.get("bedrock_name"), str) and rs["bedrock_name"].strip() != "" \
                and isinstance(rs.get("terminus_routing"), str) and rs["terminus_routing"].strip() != "" \
                and isinstance(rs.get("novel"), bool)
        elif klass not in CLASSES:
            r_ok = False
        note("routing-shape", r_ok, "%s: routing not class-shaped for %r" % (tag, klass))
        note("status-enum", e["status"] == "mapped", "%s: %r" % (tag, e["status"]))
        pv = e["provenance"]
        pv_ok = isinstance(pv, dict) and pv.get("phase") in PHASES \
            and isinstance(pv.get("date"), str) and DATE_RE.match(pv.get("date", "")) \
            and isinstance(pv.get("seat"), str) and pv.get("seat", "").strip() != ""
        note("provenance", pv_ok, "%s: %r" % (tag, pv))

    pairs = {}
    per_id = {}
    per_phase = {}
    for tag, e in all_entries:
        key = (e.get("target_id"), e.get("target_anchor"))
        pairs.setdefault(key, []).append(tag)
        per_id.setdefault(e.get("target_id"), []).append(tag)
        ph = (e.get("provenance") or {}).get("phase")
        per_phase.setdefault(ph, set()).add(e.get("target_id"))
    for key, tags in pairs.items():
        note("id-x-anchor-unique", len(tags) == 1, "%r claimed by %s" % (key[0], tags))
    for tid, tags in per_id.items():
        note("entry-cap", len(tags) <= 3, "%r has %d entries (cap 3)" % (tid, len(tags)))
    covered = set(per_id) & ids
    missing = sorted(ids - covered)
    out("coverage: %d/%d corpus ids covered; per-phase %s" %
        (len(covered), len(ids), {k: len(v) for k, v in sorted(per_phase.items(), key=lambda x: str(x[0]))}))
    if terminal:
        note("coverage", not missing, "terminal map missing %d ids: %s" % (len(missing), missing[:5]))

    for name in sorted(checks):
        ok_n, bad_n = checks[name]
        out("%s . %s (%d ok / %d fail)" % ("PASS" if bad_n == 0 else "FAIL", name, ok_n, bad_n))
    verdict = "PASS" if not violations else "FAIL"
    out(json.dumps({"files": len(map_paths), "entries": len(all_entries),
                    "coverage_distinct_ids": len(covered), "terminal": terminal,
                    "violation_count": len(violations),
                    "violations": violations[:25], "verdict": verdict}, indent=1))
    return verdict == "PASS", violations


# ---------------- self-test ----------------

def _mini_corpus():
    def node(i, tier):
        return {"id": "node-%s" % i, "tier": tier, "category": "t", "trigger": "trig %s" % i,
                "keywords": [], "psychMechanism": "pm", "diagnosis": "diagnosis text for node %s alpha beta gamma" % i,
                "responses": {"short": "short text %s one two three" % i,
                              "medium": "medium text %s four five six" % i,
                              "long": "long text %s the quick brown fox jumps over the lazy dog again and again" % i},
                "sources": []}
    return {"objections": [node("x", 5), node("y", 4), node("z", 1)]}


def _entry(**kw):
    move_a = " ".join(["move"] * 45)
    e = {"target_id": "node-x", "target_locus": "long", "target_anchor": "the quick brown fox",
         "adversarial_move": move_a, "class": "a", "grounds": "met on best reading",
         "routing": {"answered_by": ["node-y#long"]}, "status": "mapped",
         "provenance": {"phase": "A", "date": "2026-07-12", "seat": "self-test"}}
    e.update(kw)
    return e


def self_test():
    tmp = tempfile.mkdtemp(prefix="advmap_st_")
    cpath = os.path.join(tmp, "corpus.json")
    open(cpath, "wb").write((json.dumps(_mini_corpus(), indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    cmd5 = md5_bytes(open(cpath, "rb").read())

    def write_map(name, entries, meta_extra=None, canonical=True):
        doc = {"meta": {"source_corpus": "corpus.json", "source_corpus_md5": cmd5}, "entries": entries}
        if meta_extra:
            doc["meta"].update(meta_extra)
        p = os.path.join(tmp, name)
        if canonical:
            open(p, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        else:
            open(p, "wb").write(json.dumps(doc, indent=1).encode("utf-8"))
        return p

    move_b = " ".join(["press"] * 80)
    good_entries = [
        _entry(),
        _entry(target_id="node-y", target_anchor="medium text y", target_locus="medium",
               **{"class": "b", "adversarial_move": move_b,
                  "routing": {"regen_candidate": {"axis_hit": ["c", "r"], "severity": "minor"}}}),
        _entry(target_id="node-z", target_locus="diagnosis", target_anchor="diagnosis text for node z",
               **{"class": "c", "adversarial_move": move_b,
                  "routing": {"intake_candidate": {"proposed_id": "new-node", "tier_guess": 3,
                                                   "mechanism_guess": "mech", "individuation_grounds": "reader-test"}}}),
        _entry(target_anchor="quick brown fox jumps",
               **{"class": "d", "adversarial_move": move_b,
                  "routing": {"residue": {"bedrock_name": "bedrock", "terminus_routing": "solipsism-style dissolve", "novel": False}}}),
    ]
    results = []

    def case(name, entries, expect_check, terminal=False, canonical=True, extra_files=None, meta_extra=None):
        p = write_map("m_%s.json" % re.sub(r"[^a-z0-9]+", "_", name), entries, meta_extra=meta_extra, canonical=canonical)
        paths = [p] + (extra_files or [])
        buf = []
        ok, viol = validate(paths, cpath, terminal=terminal, out=lambda s: buf.append(str(s)))
        tripped = any(v.startswith(expect_check + ":") for v in viol)
        good = (not ok) and tripped
        results.append((name, good, expect_check))
        print("%s . self-test [%s] expects FAIL on %s -> %s" %
              ("PASS" if good else "FAIL", name, expect_check, "tripped" if tripped else viol[:2]))

    gp = write_map("good.json", good_entries, meta_extra={"class_counts": {"a": 2, "b": 1, "c": 1, "d": 0} if False else {"a": 1, "b": 1, "c": 1, "d": 1}, "coverage_distinct_ids": 3})
    buf = []
    ok, viol = validate([gp], cpath, terminal=True, out=lambda s: buf.append(str(s)))
    results.append(("good-fixture-terminal", ok, "-"))
    print("%s . self-test [good-fixture-terminal] expects PASS -> %s" % ("PASS" if ok else "FAIL", viol[:3]))

    case("bad-target-id", [_entry(target_id="nope")], "target-id")
    case("bad-locus", [_entry(target_locus="essay")], "target-locus")
    case("anchor-too-long", [_entry(target_anchor=" ".join(["w"] * 16))], "anchor-rule")
    case("anchor-not-substring", [_entry(target_anchor="never shipped clause")], "anchor-rule")
    case("move-under-40", [_entry(adversarial_move="too short")], "move-band")
    case("move-over-150", [_entry(adversarial_move=" ".join(["w"] * 151))], "move-band")
    case("class-a-over-60", [_entry(adversarial_move=" ".join(["w"] * 75))], "move-band")
    case("bad-class", [_entry(**{"class": "e"})], "class-enum")
    case("routing-wrong-shape", [_entry(routing={"residue": {"bedrock_name": "b", "terminus_routing": "t", "novel": True}})], "routing-shape")
    case("routing-bad-depth-ref", [_entry(routing={"answered_by": ["node-y#essay"]})], "routing-shape")
    case("routing-novel-not-bool", [_entry(**{"class": "d", "adversarial_move": " ".join(["w"] * 80),
         "routing": {"residue": {"bedrock_name": "b", "terminus_routing": "t", "novel": "yes"}}})], "routing-shape")
    case("empty-grounds", [_entry(grounds="  ")], "grounds")
    case("bad-status", [_entry(status="queued")], "status-enum")
    case("bad-phase", [_entry(provenance={"phase": "Z", "date": "2026-07-12", "seat": "s"})], "provenance")
    case("bad-date", [_entry(provenance={"phase": "A", "date": "July 12", "seat": "s"})], "provenance")
    case("dup-id-x-anchor", [_entry(), _entry(**{"class": "d", "adversarial_move": " ".join(["w"] * 80),
         "routing": {"residue": {"bedrock_name": "b", "terminus_routing": "t", "novel": True}}})], "id-x-anchor-unique")
    case("entry-cap-4", [_entry(target_anchor=a) for a in ["the quick brown", "quick brown fox", "brown fox jumps", "fox jumps over"]], "entry-cap")
    case("terminal-coverage-gap", [_entry()], "coverage", terminal=True)
    case("round-trip-violation", [_entry()], "serialization", canonical=False)
    case("missing-key", [{k: v for k, v in _entry().items() if k != "grounds"}], "entry-keys")
    case("extra-key", [dict(_entry(), extra="x")], "entry-keys")
    case("meta-pin-mismatch", [_entry()], "meta-corpus-pin", meta_extra={"source_corpus_md5": "0" * 32})
    case("meta-summary-mismatch", [_entry()], "meta-summaries", meta_extra={"class_counts": {"b": 1}})

    passed = sum(1 for _, g, _c in results if g)
    overall = passed == len(results)
    print(json.dumps({"_overall_pass": overall, "cases": len(results), "passed": passed}, indent=1))
    return overall


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--self-test" in argv:
        sys.exit(0 if self_test() else 1)
    if "--corpus" not in argv:
        print(__doc__)
        sys.exit(2)
    ci = argv.index("--corpus")
    corpus_path = argv[ci + 1]
    terminal = "--terminal" in argv
    files = [a for i, a in enumerate(argv) if a not in ("--terminal",) and i != ci and i != ci + 1 and not a.startswith("--")]
    if not files:
        print(__doc__)
        sys.exit(2)
    ok, _ = validate(files, corpus_path, terminal=terminal)
    sys.exit(0 if ok else 1)
