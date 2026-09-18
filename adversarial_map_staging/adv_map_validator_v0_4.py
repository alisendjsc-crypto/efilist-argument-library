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
  provenance             phase in PHASES {A,B1,B2,C,D,E,F,R}; date ISO (YYYY-MM-DD...); seat nonempty
  id-x-anchor-unique     (target_id, target_anchor) unique across all loaded files
  entry-cap              <=3 entries per target_id across all loaded files (Q1, ratified)
  coverage               union arithmetic reported per phase; with --terminal: every corpus id >=1 entry (82/82)
  meta-summaries         IF meta declares class_counts / coverage_distinct_ids, they must equal computed
  variant-coverage       IF meta declares variant_coverage "<hit>/<total>", it must equal THAT FILE's
                         own variant loci over the corpus total   [K347/ccclxx: was all loaded files]
  stopping-rule          NEW (gate 5) -- IF meta declares locus_closure, the per-locus stopping
                         decision is gated: the declared key set must equal the loci this FILE
                         carries entries for; values in {closed, open}; an `open` claim is
                         discharged by having authored the second continuation, and `closed` by
                         having authored exactly one: open <-> >=2 entries is a biconditional;
                         and two entries at one locus may not sit on the same clause
                         (neither anchor a substring of the other)
  entry-cap              <=3 entries per (target_id, target_locus)          [K345: unit was the node]
  entry-cap-node         <=3 + (variant loci on that node) entries per node [K345: was a flat 3]

v0_3 (K345): target_locus reaches archetypeVariants via "archetypeVariants.<slot>".
v0_4 (K347): anti-inflation gate 5, the stopping rule, becomes checkable.  Design v0_3
s10.3 made the stop an auditable claim rather than a silence and left the gate owed;
a Phase F fragment declaring a closure the validator did not read would be `cccli`
exactly -- a compliance rule asking a writer to do the right thing at write time.
v0_3 IS RETAINED UNCHANGED beside this file for the same reason v0_2 was: the Phase F
defect register's receipt names it.
v0_2 IS RETAINED UNCHANGED beside this file: adversarial_map_v1_0.json's receipt names
it, and that receipt has to stay reproducible.

Exit: 0 all hard checks pass, 1 any violation, 2 usage error.  Pure ASCII source.
"""
import json, sys, os, hashlib, re, tempfile

LOCI = ("short", "medium", "long", "diagnosis")
# K345 LOCI RULING (Josiah): the enum is EXTENDED to reach archetypeVariants.
# A target_locus is either a PRIMARY locus (the four above, unchanged) or a VARIANT
# locus spelled "archetypeVariants.<slot>". The dotted form is required so the entry
# names WHICH slot it engages -- 16 nodes carry 39 variants and they do not paraphrase
# one another. A variant locus is valid only where that slot exists on that node.
VARIANT_PREFIX = "archetypeVariants."
VARIANT_SLOTS = ("sophisticate", "defender", "drifter", "blended")
CLASSES = ("a", "b", "c", "d")
PHASES = ("A", "B1", "B2", "C", "D", "E", "F", "R")
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


def variant_slot(locus):
    """Slot name for a variant locus, else None. Pure string work -- no corpus needed."""
    if isinstance(locus, str) and locus.startswith(VARIANT_PREFIX):
        return locus[len(VARIANT_PREFIX):]
    return None


def locus_valid(node, locus):
    """A locus is valid if it is one of the four primaries, or a variant slot that
    EXISTS on this node. Primary loci are accepted unconditionally, exactly as v0_2
    accepted them: all 82 nodes carry all four, so tightening there would change
    passing behaviour for no measured gain."""
    if locus in LOCI:
        return True
    s = variant_slot(locus)
    if s is None or s not in VARIANT_SLOTS:
        return False
    return s in (node.get("responses", {}).get("archetypeVariants") or {})


def node_variant_slots(node):
    return [s for s in VARIANT_SLOTS
            if s in (node.get("responses", {}).get("archetypeVariants") or {})]


def locus_text(node, locus):
    if locus == "diagnosis":
        return node.get("diagnosis", "")
    s = variant_slot(locus)
    if s is not None:
        return (node.get("responses", {}).get("archetypeVariants") or {}).get(s, "")
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
    metas = []
    file_entries = {}
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
        # K346 gate 5 (design v0_3 s10.3), gated when declared, on the s9.4.3 pattern.
        # `locus_closure` records the stopping decision per locus, so the stop is an
        # auditable claim rather than a silence:
        #   "<target_id>#<locus>": "closed"  no second continuation at this locus that
        #                                    engages a different clause and would not be
        #                                    met by the same reply
        #   "<target_id>#<locus>": "open"    one does exist -- and the claim is discharged
        #                                    by AUTHORING it, to the cap, not by saying so
        # Gated against THIS FILE's entries: a fragment declares its own authoring.
        lc = meta.get("locus_closure")
        if isinstance(lc, dict):
            here = {}
            for e in doc["entries"]:
                if isinstance(e, dict) and isinstance(e.get("target_id"), str) \
                        and isinstance(e.get("target_locus"), str):
                    here.setdefault("%s#%s" % (e["target_id"], e["target_locus"]), []).append(e)
            note("stopping-rule", set(lc) == set(here),
                 "%s: declared-not-authored %r / authored-not-declared %r"
                 % (p, sorted(set(lc) - set(here))[:3], sorted(set(here) - set(lc))[:3]))
            for k in sorted(lc):
                v = lc[k]
                ents = here.get(k, [])
                note("stopping-rule", v in ("closed", "open"),
                     "%s: %s declares %r, not closed|open" % (p, k, v))
                if v == "open":
                    note("stopping-rule", len(ents) >= 2,
                         "%s: %s declares open with %d entries -- an open stop is discharged "
                         "by authoring the second continuation" % (p, k, len(ents)))
                elif v == "closed":
                    # open <-> >=2 entries is a BICONDITIONAL: the declaration records the answer
                    # to "is there a second continuation here", so a locus carrying two entries
                    # answered yes and cannot also declare closed.
                    note("stopping-rule", len(ents) == 1,
                         "%s: %s declares closed with %d entries -- a second continuation was "
                         "authored here, so the recorded answer was yes" % (p, k, len(ents)))
                anchors = [e.get("target_anchor") for e in ents
                           if isinstance(e.get("target_anchor"), str)]
                for ai, a1 in enumerate(anchors):
                    for a2 in anchors[ai + 1:]:
                        note("stopping-rule", a1 not in a2 and a2 not in a1,
                             "%s: %s carries two entries on the SAME clause (%r / %r)"
                             % (p, k, a1[:28], a2[:28]))
        metas.append((p, meta))
        file_entries[p] = doc["entries"]
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
        l_ok = in_ids and locus_valid(nodes[tid], locus)
        note("target-locus", l_ok, "%s: %r" % (tag, locus))
        anchor = e["target_anchor"]
        a_ok = isinstance(anchor, str) and anchor.strip() != "" and wc(anchor) <= 15
        if a_ok and in_ids and l_ok:
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
                    # K345: an (a) may route to a variant locus too. Same ruling, one step
                    # over: leaving this at LOCI would let the enum extend while the routing
                    # target stayed silently narrower than the thing it points at.
                    if len(parts) != 2 or parts[0] not in ids \
                            or not locus_valid(nodes[parts[0]], parts[1]):
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
    per_id_locus = {}
    per_phase = {}
    for tag, e in all_entries:
        key = (e.get("target_id"), e.get("target_anchor"))
        pairs.setdefault(key, []).append(tag)
        per_id.setdefault(e.get("target_id"), []).append(tag)
        per_id_locus.setdefault((e.get("target_id"), e.get("target_locus")), []).append(tag)
        ph = (e.get("provenance") or {}).get("phase")
        per_phase.setdefault(ph, set()).add(e.get("target_id"))
    for key, tags in pairs.items():
        note("id-x-anchor-unique", len(tags) == 1, "%r claimed by %s" % (key[0], tags))
    # K345: the cap's unit moves from the NODE to the LOCUS, because the locus is the
    # unit the anchor engages. A node with no archetypeVariants keeps the ratified
    # bound of 3 EXACTLY; a node with variants gets one more slot per variant locus,
    # so the gate extends in proportion to the text rather than being loosened flat.
    for (tid, locus), tags in per_id_locus.items():
        note("entry-cap", len(tags) <= 3,
             "%r#%s has %d entries (cap 3 per locus)" % (tid, locus, len(tags)))
    for tid, tags in per_id.items():
        bound = 3 + (len(node_variant_slots(nodes[tid])) if tid in nodes else 0)
        note("entry-cap-node", len(tags) <= bound,
             "%r has %d entries (node bound %d = 3 + %d variant loci)"
             % (tid, len(tags), bound, bound - 3))
    covered = set(per_id) & ids
    missing = sorted(ids - covered)
    # Variant coverage is REPORTED, never forced: Phase F is owed and a successor map
    # must be able to exist before it lands. When meta DECLARES the figure it is gated,
    # so the claim is checked even though completion is not compelled.
    var_loci_total = sorted((n["id"], VARIANT_PREFIX + s)
                            for n in corpus["objections"] for s in node_variant_slots(n))
    var_loci_hit = sorted(k for k in per_id_locus if variant_slot(k[1]) is not None)
    vc = "%d/%d" % (len(set(var_loci_hit)), len(var_loci_total))
    # K347 (ccclxx): variant_coverage is declared BY A FILE, so it is gated against THAT
    # FILE's own entries -- as class_counts and coverage_distinct_ids already are. Gating a
    # per-file declaration against a figure summed over every loaded file makes the verdict
    # depend on how many files the run happened to load: a fragment whose declaration is
    # true alone fails beside its sibling, and the same bytes pass or fail by invocation.
    # The all-loaded-files figure is still REPORTED, on the line below.
    for p, meta in metas:
        if "variant_coverage" in meta:
            own = set()
            for e in file_entries.get(p, []):
                if isinstance(e, dict) and isinstance(e.get("target_locus"), str) \
                        and variant_slot(e["target_locus"]) is not None:
                    own.add((e.get("target_id"), e["target_locus"]))
            own_vc = "%d/%d" % (len(own), len(var_loci_total))
            note("variant-coverage", meta["variant_coverage"] == own_vc,
                 "%s: declared %r vs this file's %r (all loaded files: %s)"
                 % (p, meta["variant_coverage"], own_vc, vc))
    out("corpus: whole-file %s  objections-digest %s" % (cmd5[:12], odig[:12]))
    out("variant-coverage: %s archetypeVariants loci carry >=1 entry" % vc)
    decl_n = sum(len(m["locus_closure"]) for _p, m in metas
                 if isinstance(m.get("locus_closure"), dict))
    out("stopping-rule: %d/%d loci carrying entries declare a closure decision"
        % (decl_n, len(per_id_locus)))
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

    # ---------------- K345 control battery: the NEW behaviour, both directions ----
    # A suite written before a change proves nothing about the change. Each control
    # below fails loudly if v0_3's locus grammar or cap arithmetic is wrong.
    SOPH = "sophisticate variant for node y carrying its own distinct commitment epsilon zeta"
    DEFE = "defender variant for node y naming the bad faith eta theta iota"
    for _n in mc["objections"]:
        if _n["id"] == "node-y":
            _n["responses"]["archetypeVariants"] = {"sophisticate": SOPH, "defender": DEFE}
    open(cpath, "wb").write((json.dumps(mc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    cmd5 = md5_bytes(open(cpath, "rb").read())
    odig = objections_digest(mc)

    def vent(slot, anchor, **kw):
        d = dict(target_id="node-y", target_locus=VARIANT_PREFIX + slot, target_anchor=anchor)
        d.update(kw)
        return _entry(**d)

    def clean(name, entries, meta_extra=None, terminal=False, assembly=False):
        pth = write_map("k345_%s.json" % re.sub(r"[^a-z0-9]+", "_", name), entries, meta_extra=meta_extra)
        ok, viol, adv = validate([pth], cpath, terminal=terminal, assembly=assembly, out=lambda s: None)
        good = ok and not adv
        results.append((name, good, "-"))
        print("%s . self-test [%s] expects PASS -> %s" % ("PASS" if good else "FAIL", name, (viol + adv)[:3]))

    # 1. a well-formed variant entry validates
    clean("k345-variant-locus-valid", [vent("sophisticate", "carrying its own distinct commitment")])
    # 2. slot that does not exist on THIS node
    case("k345-variant-slot-absent", [vent("drifter", "carrying its own distinct commitment")], "target-locus")
    # 3. slot outside the declared set
    case("k345-variant-slot-bogus", [vent("apologist", "carrying its own distinct commitment")], "target-locus")
    # 4. anchor absent from the named variant
    case("k345-variant-anchor-absent", [vent("defender", "carrying its own distinct commitment")], "anchor-rule")
    # 5. ROUTING PROOF, both directions: locus_text must read the named variant ALONE,
    #    never a concatenation with the node's primary loci, and vice versa.
    case("k345-long-anchor-not-in-variant", [vent("defender", "quick brown fox jumps")], "anchor-rule")
    case("k345-variant-anchor-not-in-long",
         [_entry(target_id="node-y", target_locus="long", target_anchor="naming the bad faith")], "anchor-rule")
    # 6. per-locus cap: 4 distinct anchors at one locus
    four = [_entry(target_id="node-y", target_anchor=a) for a in
            ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over", "fox jumps over the")]
    case("k345-entry-cap-per-locus", four, "entry-cap")
    # 7. the node bound on a node with NO variants stays exactly 3, the ratified value
    nov = [_entry(target_id="node-z", target_locus=L, target_anchor=a) for L, a in
           (("long", "the quick brown fox"), ("long", "quick brown fox jumps"),
            ("long", "brown fox jumps over"), ("medium", "medium text z"))]
    case("k345-entry-cap-node-unchanged-at-3", nov, "entry-cap-node")
    # 8. the node bound SCALES: node-y carries 2 variant slots, so 5 is clean and 6 trips
    five = [_entry(target_id="node-y", target_anchor=a) for a in
            ("the quick brown fox", "quick brown fox jumps", "brown fox jumps over")] + [
           vent("sophisticate", "carrying its own distinct commitment"),
           vent("defender", "naming the bad faith")]
    clean("k345-entry-cap-node-scales-to-5", five)
    case("k345-entry-cap-node-trips-at-6",
         five + [_entry(target_id="node-y", target_locus="medium", target_anchor="medium text y")],
         "entry-cap-node")
    # 8b. an (a) may route TO a variant locus, and a bogus one still trips
    clean("k345-answered-by-variant-ok",
          [_entry(target_id="node-z", target_anchor="the quick brown fox",
                  routing={"answered_by": ["node-y#archetypeVariants.defender"]})])
    case("k345-answered-by-variant-absent",
         [_entry(target_id="node-z", target_anchor="the quick brown fox",
                 routing={"answered_by": ["node-y#archetypeVariants.drifter"]})], "routing-shape")

    # 9. a DECLARED variant_coverage is gated; an undeclared one is only reported
    clean("k345-variant-coverage-declared-true",
          [vent("sophisticate", "carrying its own distinct commitment")],
          meta_extra={"variant_coverage": "1/2"})
    case("k345-variant-coverage-declared-false",
         [vent("sophisticate", "carrying its own distinct commitment")], "variant-coverage",
         meta_extra={"variant_coverage": "2/2"})

    # --- v0_4 additions: gate 5, the stopping rule ---
    soph = vent("sophisticate", "carrying its own distinct commitment")
    defe = vent("defender", "naming the bad faith")
    soph_key = "node-y#archetypeVariants.sophisticate"
    defe_key = "node-y#archetypeVariants.defender"
    # 10. a correct declaration passes, and an undeclared fragment is untouched by the gate
    clean("k347-closure-declared-true", [soph, defe],
          meta_extra={"locus_closure": {soph_key: "closed", defe_key: "closed"}})
    clean("k347-closure-undeclared-is-not-gated", [soph, defe])
    # 11. the key set must equal the loci this file actually authored, both ways
    case("k347-closure-misses-an-authored-locus", [soph, defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "closed"}})
    case("k347-closure-declares-an-unauthored-locus", [soph], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "closed", defe_key: "closed"}})
    # 12. an `open` stop is discharged by authoring, not by declaring
    case("k347-open-with-one-entry", [soph], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "open"}})
    clean("k347-open-with-two-distinct-clauses",
          [soph, vent("sophisticate", "sophisticate variant for node y"),
           defe],
          meta_extra={"locus_closure": {soph_key: "open", defe_key: "closed"}})
    # 12b. the biconditional's other direction: two entries cannot declare closed
    case("k347-closed-with-two-entries",
         [soph, vent("sophisticate", "sophisticate variant for node y"), defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "closed", defe_key: "closed"}})
    # 13. two entries at one locus may not sit on the same clause
    case("k347-two-entries-same-clause",
         [soph, vent("sophisticate", "its own distinct commitment"), defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "open", defe_key: "closed"}})
    # 15. ccclxx: a declaration is gated against ITS OWN file, so the verdict cannot move
    #     with how many sibling files the run happens to load. This control FAILS on v0_3.
    pA = write_map("k347_two_file_a.json", [soph], meta_extra={"variant_coverage": "1/2"})
    pB = write_map("k347_two_file_b.json", [defe], meta_extra={"variant_coverage": "1/2"})
    okA, vA, _adA = validate([pA], cpath, out=lambda s: None)
    okJ, vJ, _adJ = validate([pA, pB], cpath, out=lambda s: None)
    good_ind = okA and okJ
    results.append(("k347-declaration-invocation-independent", good_ind, "variant-coverage"))
    print("%s . self-test [k347-declaration-invocation-independent] expects PASS solo AND joint -> %s"
          % ("PASS" if good_ind else "FAIL", (vA + vJ)[:2]))

    # 14. the value enum
    case("k347-closure-bad-value", [soph, defe], "stopping-rule",
         meta_extra={"locus_closure": {soph_key: "sealed", defe_key: "closed"}})

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
