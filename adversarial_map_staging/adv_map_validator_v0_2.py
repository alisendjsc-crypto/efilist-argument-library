#!/usr/bin/env python3
"""adv_map_validator_v0_2.py -- adversarial-map fragment / assembly validator (v0.2.0)

Supersedes adv_map_validator_v0_1.py, which stays on disk unmutated: canon pins its
blob and the K228-K231 receipts cite its output. v0_2 is additive -- every v0_1 check
is carried forward verbatim, so any fragment that passed v0_1 passes v0_2 unless it
trips one of the four NEW checks below.

Container contract (unchanged; the schema sibling pins the ENTRY):
  { "meta": { ... source-corpus pin ... }, "entries": [ <entry per schema>, ... ] }

Usage:
  python3 adv_map_validator_v0_2.py <fragment.json> [...] --corpus <corpus.json> [--terminal] [--assembly]
  python3 adv_map_validator_v0_2.py --corpus <corpus.json> --print-digest
  python3 adv_map_validator_v0_2.py --self-test

WHAT IS NEW IN v0.2.0
---------------------
1. PHASES gains "E".  Phase E (T1, n=13) is the terminal authoring phase.  v0_1
   rejected it, so an E fragment could not have been validated at all.

2. objections-digest (NEW CHECK, hard when declared).
   K332 root cause: four release relabels walked the corpus "version" field from
   4.0.0 to 4.0.4 while every objection stayed byte-identical.  One content cut wore
   five whole-file md5s, and every fragment pinning 6ee1f6f3 failed meta-corpus-pin
   -- which silently disabled SEVEN downstream checks including anchor-rule, the
   program's core verbatim discipline.  A whole-file md5 is the wrong instrument: it
   measures the envelope, not the text the anchors are cut from.
   Remedy: meta may declare "source_corpus_objections_md5", a digest over the
   objections ARRAY ALONE, canonically serialized:
       md5(json.dumps(corpus["objections"], indent=2, ensure_ascii=False,
                      sort_keys=True).encode("utf-8") + b"\\n")
   sort_keys makes it immune to key reordering as well as to label churn.  Compute
   it with --print-digest.  The key is OPTIONAL: absent, the check is skipped and
   v0_1-era fragments validate unchanged; present, it is hard.  New fragments should
   carry BOTH pins -- the whole-file md5 says which file, the digest says which text.

3. b1-bradley-bar and b1-hedonic-crossref (NEW, advisory by default / hard under --assembly).
   Brief section 2.5 item 5: Phase B1 predates both carry-forward constraints.
     - K224 BARS routing an (a) into bradley-no-subject#long for a comparative-harm
       move, because bradley answers such moves by asserting non-comparative wronging,
       which is itself unsettled bedrock (HR-05). K229 scopes that bar to
       comparative-harm moves. non-identity-problem is the likeliest breach, since it
       IS the no-worse-off-baseline problem.
     - K230 calls the cross-ref the hedonic-contrast route leans on broken, so an
       (a)-route through transhumanist-objection#long is unsettled until repaired.
   Neither predicate is machine-decidable -- "is this a comparative-harm move" is an
   editorial judgment.  What IS mechanical is whether the author adjudicated it, so
   an entry clears by naming the constraint in its grounds with a literal token:
       [K229-...]          bradley-no-subject#long (a)-routes
       [K230-crossref-...] transhumanist-objection#long (a)-routes
   The token is matched as a PREFIX so the suffix can name the disposition the ruling
   actually reached ([K229-comparative] / [K229-not-comparative];
   [K230-crossref-repaired] / [K230-crossref-not-load-bearing]).
   The token asserts the ruling was made, not that it came out clean; the grounds
   prose carries the reasoning.  These fire on exactly the five B1 entries the brief
   names, which is the point: the debt is standing and stays visible until paid.

4. move-ascii (NEW, advisory by default / hard under --assembly).
   The move gate has always read "40-150 words, ASCII, no standalone dash tokens".
   v0_1 mechanized the word band and neither of the other two.  Mechanizing ASCII
   now registers a live breach rather than inventing one: eight Phase A moves carry
   U+2014, and zero moves in B1, B2, C or D do.  Phase A predates the discipline.
   Advisory keeps that fact reported on every run without failing four ratified
   fragments retroactively; --assembly makes it binding at the one moment it must be.

SEVERITY MODEL
--------------
  PASS/FAIL   hard checks.  Any FAIL sets exit 1.
  WARN        advisory checks.  Reported always, never sets exit 1 on its own.
  --assembly  promotes every advisory to hard and implies --terminal.  The assembly
              step into adversarial_map_v1_0.json must run with it.

Checks (one PASS/FAIL/WARN line each):
  container-shape        top-level {meta, entries}; entries is a list of dicts
  serialization          each file round-trips json.dumps(indent=2, ensure_ascii=False)+'\\n'
  meta-corpus-pin        meta names the source corpus + an md5 (>=8-char prefix) matching --corpus
  objections-digest      NEW -- if declared, digest over the objections array must match
  entry-keys             exactly the 9 schema keys per entry
  target-id              target_id in the corpus id set
  target-locus           target_locus in {short, medium, long, diagnosis}
  anchor-rule            target_anchor nonempty, <=15 words, verbatim substring at target_locus
  move-band              adversarial_move 40-150 words; class (a) additionally <=60
  move-ascii             NEW (advisory) -- move is pure ASCII, no standalone dash token
  class-enum             class in {a, b, c, d}
  grounds                grounds nonempty string
  routing-shape          routing carries exactly the one class-shaped key, fields typed + enum-true
  b1-bradley-bar         NEW (advisory) -- (a)->bradley-no-subject#long attests [K229-...]
  b1-hedonic-crossref    NEW (advisory) -- (a)->transhumanist-objection#long attests [K230-crossref-...]
  status-enum            status == "mapped" (downstream states live in canon, never the artifact)
  provenance             phase in {A,B1,B2,C,D,E}; date ISO (YYYY-MM-DD...); seat nonempty
  id-x-anchor-unique     (target_id, target_anchor) unique across all loaded files
  entry-cap              <=3 entries per target_id across all loaded files (Q1, ratified)
  coverage               union arithmetic reported per phase; with --terminal: every corpus id >=1 entry (82/82)
  meta-summaries         IF meta declares class_counts / coverage_distinct_ids, they must equal computed

Exit: 0 all hard checks pass, 1 any violation, 2 usage error.  Pure ASCII source.
"""
import json, sys, os, hashlib, re, tempfile

LOCI = ("short", "medium", "long", "diagnosis")
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E")
ENTRY_KEYS = ["target_id", "target_locus", "target_anchor", "adversarial_move",
              "class", "grounds", "routing", "status", "provenance"]
AXES = ("v", "s", "c", "r", "a")
IND_GROUNDS = ("presupposition-inversion", "reader-test", "grading-object-integrity")
SEVERITIES = ("minor", "headline")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

# --- carry-forward register (brief s2.5 item 5) -------------------------------
# locus that triggers the constraint -> (check name, attestation token, ruling)
# The token is a PREFIX, so the author names the disposition in the suffix rather than
# being forced into one the ruling did not reach. Canonical suffixes:
#   [K229-comparative]              the move is a comparative-harm move; bar bites
#   [K229-not-comparative]          adjudicated, the move is not comparative-harm; bar clears
#   [K230-crossref-repaired]        the cross-ref has been repaired
#   [K230-crossref-not-load-bearing] adjudicated, the broken cross-ref does not carry this (a)
# An attestation asserts the ruling was MADE, never that it came out clean.
CARRY_FORWARD = {
    "bradley-no-subject#long": (
        "b1-bradley-bar", "[K229-",
        "K224 bars routing (a) into bradley for comparative-harm moves; K229 scopes the bar"),
    "transhumanist-objection#long": (
        "b1-hedonic-crossref", "[K230-crossref",
        "K230 calls the cross-ref this route leans on broken"),
}

DASH_TOKEN_RE = re.compile(r"(?:^|\s)[-\u2010-\u2015]+(?:\s|$)")


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def objections_digest(corpus):
    """Digest over the objections array alone -- immune to version-label churn."""
    ser = json.dumps(corpus["objections"], indent=2, ensure_ascii=False, sort_keys=True)
    return md5_bytes(ser.encode("utf-8") + b"\n")


def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    return node.get("responses", {}).get(locus, "")


def wc(s):
    return len(s.split())


def non_ascii_chars(s):
    return sorted(set(ch for ch in s if ord(ch) > 127))


def validate(map_paths, corpus_path, terminal=False, assembly=False, out=print):
    if assembly:
        terminal = True
    violations = []
    advisories = []
    checks = {}
    ADVISORY = set()

    def note(check, ok, detail="", advisory=False):
        checks.setdefault(check, [0, 0])
        checks[check][0 if ok else 1] += 1
        if advisory:
            ADVISORY.add(check)
        if not ok:
            msg = "%s: %s" % (check, detail)
            if advisory and not assembly:
                advisories.append(msg)
            else:
                violations.append(msg)

    craw = open(corpus_path, "rb").read()
    corpus = json.loads(craw.decode("utf-8"))
    cmd5 = md5_bytes(craw)
    odig = objections_digest(corpus)
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
        dec = meta.get("source_corpus_objections_md5")
        if isinstance(dec, str) and dec:
            note("objections-digest", len(dec) >= 8 and odig.startswith(dec),
                 "%s: declared objections digest %r vs computed %s" % (p, dec[:12], odig[:12]))
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
        mv = e["adversarial_move"]
        w = wc(mv) if isinstance(mv, str) else -1
        band_ok = 40 <= w <= 150 and (klass != "a" or w <= 60)
        note("move-band", band_ok, "%s: %d words (class %s)" % (tag, w, klass))
        if isinstance(mv, str):
            bad = non_ascii_chars(mv)
            dash = DASH_TOKEN_RE.search(mv)
            if bad:
                why = "non-ascii %r" % bad
            elif dash:
                why = "standalone dash token %r" % dash.group().strip()
            else:
                why = ""
            note("move-ascii", not why, "%s: %s" % (tag, why), advisory=True)
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

        # carry-forward register: only (a)-routes into the two constrained loci
        if klass == "a" and isinstance(r, dict) and isinstance(r.get("answered_by"), list):
            g = e["grounds"] if isinstance(e["grounds"], str) else ""
            for ref in r["answered_by"]:
                if ref in CARRY_FORWARD:
                    cname, token, ruling = CARRY_FORWARD[ref]
                    note(cname, token in g,
                         "%s: (a)->%s with no %s...] attestation in grounds (%s)"
                         % (tag, ref, token, ruling),
                         advisory=True)

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
    out("corpus: whole-file %s  objections-digest %s" % (cmd5[:12], odig[:12]))
    out("coverage: %d/%d corpus ids covered; per-phase %s" %
        (len(covered), len(ids), {k: len(v) for k, v in sorted(per_phase.items(), key=lambda x: str(x[0]))}))
    if terminal:
        note("coverage", not missing, "terminal map missing %d ids: %s" % (len(missing), missing[:5]))

    for name in sorted(checks):
        ok_n, bad_n = checks[name]
        if bad_n == 0:
            label = "PASS"
        elif name in ADVISORY and not assembly:
            label = "WARN"
        else:
            label = "FAIL"
        out("%s . %s (%d ok / %d fail)" % (label, name, ok_n, bad_n))
    verdict = "PASS" if not violations else "FAIL"
    out(json.dumps({"files": len(map_paths), "entries": len(all_entries),
                    "coverage_distinct_ids": len(covered), "terminal": terminal,
                    "assembly": assembly,
                    "violation_count": len(violations),
                    "violations": violations[:25],
                    "advisory_count": len(advisories),
                    "advisories": advisories[:25],
                    "verdict": verdict}, indent=1))
    return verdict == "PASS", violations, advisories


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
    tmp = tempfile.mkdtemp(prefix="advmap_st2_")
    cpath = os.path.join(tmp, "corpus.json")
    mc = _mini_corpus()
    open(cpath, "wb").write((json.dumps(mc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    cmd5 = md5_bytes(open(cpath, "rb").read())
    odig = objections_digest(mc)

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

    def case(name, entries, expect_check, terminal=False, canonical=True, meta_extra=None,
             advisory=False, assembly=False):
        p = write_map("m_%s.json" % re.sub(r"[^a-z0-9]+", "_", name), entries, meta_extra=meta_extra, canonical=canonical)
        buf = []
        ok, viol, adv = validate([p], cpath, terminal=terminal, assembly=assembly, out=lambda s: buf.append(str(s)))
        pool = adv if (advisory and not assembly) else viol
        tripped = any(v.startswith(expect_check + ":") for v in pool)
        # an advisory must NOT fail the run when --assembly is off
        good = tripped and (ok if (advisory and not assembly) else (not ok))
        results.append((name, good, expect_check))
        print("%s . self-test [%s] expects %s on %s -> %s" %
              ("PASS" if good else "FAIL", name, "WARN" if (advisory and not assembly) else "FAIL",
               expect_check, "tripped" if tripped else (pool[:2] or viol[:2])))

    gp = write_map("good.json", good_entries,
                   meta_extra={"class_counts": {"a": 1, "b": 1, "c": 1, "d": 1},
                               "coverage_distinct_ids": 3,
                               "source_corpus_objections_md5": odig})
    buf = []
    ok, viol, adv = validate([gp], cpath, terminal=True, out=lambda s: buf.append(str(s)))
    results.append(("good-fixture-terminal", ok and not adv, "-"))
    print("%s . self-test [good-fixture-terminal] expects PASS -> %s" % ("PASS" if (ok and not adv) else "FAIL", (viol + adv)[:3]))

    # v0_1 carry-forward cases (unchanged behaviour)
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

    # --- v0_2 additions ---
    # phase E must now be accepted: a lone E entry trips only terminal coverage, never provenance
    pE = write_map("phase_e.json", [_entry(provenance={"phase": "E", "date": "2026-09-16", "seat": "self-test"})])
    ok_e, viol_e, adv_e = validate([pE], cpath, out=lambda s: None)
    good_e = ok_e and not any(v.startswith("provenance:") for v in viol_e)
    results.append(("phase-E-accepted", good_e, "provenance"))
    print("%s . self-test [phase-E-accepted] expects PASS -> %s" % ("PASS" if good_e else "FAIL", viol_e[:2]))

    # objections digest: absent -> skipped; wrong -> hard fail; label churn -> survives
    pAbs = write_map("digest_absent.json", [_entry()])
    ok_abs, v_abs, _a = validate([pAbs], cpath, out=lambda s: None)
    good_abs = ok_abs and not any(v.startswith("objections-digest:") for v in v_abs)
    results.append(("digest-absent-is-skipped", good_abs, "objections-digest"))
    print("%s . self-test [digest-absent-is-skipped] expects PASS -> %s" % ("PASS" if good_abs else "FAIL", v_abs[:2]))

    case("digest-mismatch", [_entry()], "objections-digest",
         meta_extra={"source_corpus_objections_md5": "f" * 32})

    # THE K332 REGRESSION: relabel the corpus envelope, objections byte-identical.
    churn = dict(mc)
    churn["version"] = "4.0.4"
    cpath2 = os.path.join(tmp, "corpus_relabelled.json")
    open(cpath2, "wb").write((json.dumps(churn, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    cmd5_2 = md5_bytes(open(cpath2, "rb").read())
    pChurn = write_map("digest_churn.json", [_entry()],
                       meta_extra={"source_corpus_objections_md5": odig})
    ok_ch, v_ch, _a2 = validate([pChurn], cpath2, out=lambda s: None)
    # whole-file pin must break (that is v0_1's failure mode) while the digest holds
    wf_broke = any(v.startswith("meta-corpus-pin:") for v in v_ch)
    dig_held = not any(v.startswith("objections-digest:") for v in v_ch)
    good_ch = wf_broke and dig_held and cmd5_2 != cmd5
    results.append(("digest-survives-label-churn", good_ch, "objections-digest"))
    print("%s . self-test [digest-survives-label-churn] expects whole-file pin FAIL + digest HOLD -> %s"
          % ("PASS" if good_ch else "FAIL", v_ch[:2]))

    # carry-forward: unattested (a)-route into a constrained locus
    brad = _entry(target_id="node-z", target_anchor="long text z the quick",
                  routing={"answered_by": ["node-x#long"]})
    # rewrite the constrained loci into the mini corpus namespace for the test
    global CARRY_FORWARD
    saved = CARRY_FORWARD
    CARRY_FORWARD = {"node-x#long": ("b1-bradley-bar", "[K229-", "test ruling"),
                     "node-y#long": ("b1-hedonic-crossref", "[K230-crossref", "test ruling")}
    try:
        case("bradley-unattested", [brad], "b1-bradley-bar", advisory=True)
        case("bradley-unattested-assembly", [brad], "b1-bradley-bar", advisory=True, assembly=True, terminal=True)
        attested = dict(brad, grounds="met on best reading [K229-comparative] comparative-harm move")
        pAtt = write_map("bradley_attested.json", [attested])
        ok_at, v_at, a_at = validate([pAtt], cpath, out=lambda s: None)
        good_at = ok_at and not any(v.startswith("b1-bradley-bar:") for v in a_at + v_at)
        results.append(("bradley-attested-clears", good_at, "b1-bradley-bar"))
        print("%s . self-test [bradley-attested-clears] expects PASS -> %s" % ("PASS" if good_at else "FAIL", (v_at + a_at)[:2]))
        case("hedonic-unattested", [_entry(routing={"answered_by": ["node-y#long"]})],
             "b1-hedonic-crossref", advisory=True)
        alt = dict(brad, grounds="adjudicated [K229-not-comparative] the move is agency-based")
        pAlt = write_map("bradley_alt_suffix.json", [alt])
        ok_al, v_al, a_al = validate([pAlt], cpath, out=lambda s: None)
        good_al = ok_al and not any(v.startswith("b1-bradley-bar:") for v in a_al + v_al)
        results.append(("bradley-alt-suffix-clears", good_al, "b1-bradley-bar"))
        print("%s . self-test [bradley-alt-suffix-clears] expects PASS -> %s" % ("PASS" if good_al else "FAIL", (v_al + a_al)[:2]))
    finally:
        CARRY_FORWARD = saved

    # move-ascii: advisory by default, hard under --assembly
    emdash = _entry(adversarial_move=" ".join(["move"] * 44) + " \u2014 end")
    case("move-em-dash", [emdash], "move-ascii", advisory=True)
    case("move-em-dash-assembly", [emdash], "move-ascii", advisory=True, assembly=True, terminal=True)
    case("move-standalone-dash", [_entry(adversarial_move=" ".join(["move"] * 44) + " - end")],
         "move-ascii", advisory=True)

    passed = sum(1 for _n, g, _c in results if g)
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
    if "--print-digest" in argv:
        craw = open(corpus_path, "rb").read()
        c = json.loads(craw.decode("utf-8"))
        print(json.dumps({"corpus": os.path.basename(corpus_path),
                          "whole_file_md5": md5_bytes(craw),
                          "source_corpus_objections_md5": objections_digest(c),
                          "objections": len(c["objections"])}, indent=1))
        sys.exit(0)
    terminal = "--terminal" in argv
    assembly = "--assembly" in argv
    files = [a for i, a in enumerate(argv) if i != ci and i != ci + 1 and not a.startswith("--")]
    if not files:
        print(__doc__)
        sys.exit(2)
    ok, _v, _a = validate(files, corpus_path, terminal=terminal, assembly=assembly)
    sys.exit(0 if ok else 1)
