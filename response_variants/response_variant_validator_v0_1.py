#!/usr/bin/env python3
"""response_variant_validator_v0_1.py -- the responseVariants validator (V6, seat l, 2026-10-04)

Built from the responseVariants design v0_1, sections 2 and 3 (design/variations/RESPONSE_VARIANTS_design_v0_1.md,
md5 1c4be4d3), as ruled on 2026-10-04: his word at V5's user turn (md5 4dace677) adopts RV-1..RV-8 as leaned
(canon v38.53 adversarial_map.response_variants_rulings_V6). The contract it enforces is
response_variants_schema_v0_1.json beside it; --self-test asserts that the two agree, that the type label equals
canon's label_leaned, and that the two typed floors are the design's words.

THE SAME CODE AS THE MAP AND THE SAFETY PASS. Nothing is re-typed that another instrument owns:
  - wc, non_ascii_chars, DASH_TOKEN_RE, objections_digest, locus_text and PHASES come from the map validator
    v0_6 (adversarial_map_staging/adv_map_validator_v0_6.py), loaded at md5 c002e938 through pinned.py, as V1's
    shape validator loads them;
  - EXIT (gate2's patterns, X-032) and WIDE (L6's thirteen families) come from
    adversarial_map_staging/r1/sp_reading_l6.py, loaded at md5 dc2525ef. Each is applied as its own instrument
    applies it: EXIT case-sensitive (sweep_exit), WIDE case-insensitive (measure).
  - The type table (label, whose account, source root) is read from the schema, never written here.

WHAT IT READS
  A staging file:   {"meta": {...}, "variants": [<variant>, ...]}
  The corpus:       with --embedded, every node's top-level responseVariants list (none today).
  The corpus a staging file is checked against is the one meta.source_corpus_md5 pins; the canon its
  account_sources resolve in is the one meta.source_canon pins ({file, md5}), read from the working tree or git
  history at that md5 (the rename convention removes old canons). --corpus / --canon PATH override, explicitly;
  an override must still match the pinned md5.

CHECKS (RV-6, the design's list; each one is a line in the output)
  container-shape   staging: {meta, variants} and nothing else; embedded: responseVariants is a list, and is
                    never under responses (RV-1: the game embeds responses whole)
  meta-corpus-pin   meta.source_corpus_md5 == the corpus read; source_corpus_objections_md5, if declared
  meta-canon-pin    meta.source_canon {file, md5} resolves to a canon at that md5
  variant-keys      the required keys, and no others
  variant-id        <node-id>/<type>; the node resolves (embedded: it is the host node); the suffix is the type
  type-closed       type is in the closed set (RV-2)
  variant-cap       at most one variant per (node, type) across every file loaded together
  varies-locus      varies is exactly {locus, anchor}, and locus is long
  anchor-rule       non-empty, at most 15 words, verbatim in the node's long, and occurring there exactly once
  text-band         120-300 words
  text-ascii        ASCII, no standalone dash token (v0_6's DASH_TOKEN_RE)
  residual          {where_both_stop, concedes {library, account}, status}; non-empty ASCII strings; status open
  floor-no-win      none of refutes, defeats, proves, settles, decisive, wins (text and residual)
  floor-exit        none of gate2's EXIT patterns (text and residual)
  floor-wide        none of L6's WIDE families (text and residual)
  floor-pro-life    none of: life is worth living, your life matters, things get better, life is precious,
                    life is a gift (text and residual)
  account-sources   non-empty; each {canon, turn_md5}; the path lies under the type's source root, resolves in
                    the pinned canon to his verbatim words, and its turn_md5 equals that entry's
  provenance        {phase, date, seat}; phase "V", disjoint from the map's PHASES and the shapes' S
  variant-coverage  staging only, REQUIRED: meta.variant_coverage "<nodes with a variant in THIS file>/<nodes in
                    the corpus>", gated against this file alone (ccclxx)

A floor is not a census: gate2 still reads every variant against his bar. WIDE contains every EXIT pattern, so
an EXIT phrase turns floor-exit and floor-wide RED together; the self-test expects exactly that pair.
Field checks run only where the key is present; an absent key is variant-keys' failure alone.

Usage:
  python3 response_variant_validator_v0_1.py <fragment.json> [...] [--corpus PATH] [--canon PATH]
  python3 response_variant_validator_v0_1.py --embedded [--corpus PATH] [--canon PATH]   # default: working files
  python3 response_variant_validator_v0_1.py --self-test [--write | --check]
                                             # record: response_variant_validator_control_v0_1.json
"""
import copy, glob, hashlib, json, os, re, shutil, sys, tempfile, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
from pinned import bytes_at, path_at  # noqa: E402

MAPV_REL = "adversarial_map_staging/adv_map_validator_v0_6.py"
MAPV_MD5 = "c002e93877b09d523daf786036af7a57"
SAFETY_REL = "adversarial_map_staging/r1/sp_reading_l6.py"
SAFETY_MD5 = "dc2525ef40fc5353a670484f511bd668"
CORPUS_REL = "efilist_argument_library_v4_0_0.json"
SCHEMA_REL = "response_variants/response_variants_schema_v0_1.json"
RECORD_REL = "response_variants/response_variant_validator_control_v0_1.json"
DESIGN = ("design/variations/RESPONSE_VARIANTS_design_v0_1.md", "1c4be4d36addc95a757b43f57c489b7e")
MEASURE = ("design/variations/measure_response_variants_v0_1.json", "cbae330fe2106d79d572de8e20ac8459")
# The canon the real-data controls read: v38.52, the canon at V6's open (efilist 8e8e153), which carries the
# design's label_leaned and relief_view_for_the_variant.
REAL_CANON = ("project_canon_v38_52.json", "9697f796baacc7c54bd8212057f4e486")
# The corpus the real-data controls read: v4.1.5, the pin at V6's open.
REAL_CORPUS_MD5 = "7b6e65e531018fecb37baf2a4fedd6d1"


def _load(rel, md5, name):
    src = bytes_at(REPO, rel, md5)
    mod = types.ModuleType(name)
    mod.__file__ = os.path.join(REPO, rel)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


MAPV = _load(MAPV_REL, MAPV_MD5, "adv_map_validator_v0_6")
SAFETY = _load(SAFETY_REL, SAFETY_MD5, "sp_reading_l6")
locus_text = MAPV.locus_text
wc = MAPV.wc
non_ascii_chars = MAPV.non_ascii_chars
DASH_TOKEN_RE = MAPV.DASH_TOKEN_RE
objections_digest = MAPV.objections_digest
EXIT = list(SAFETY.EXIT)
WIDE = list(SAFETY.WIDE)

SCHEMA = json.loads(open(os.path.join(REPO, SCHEMA_REL), "rb").read().decode("utf-8"))
TYPES = SCHEMA["x-types"]

REQUIRED_KEYS = ("variant_id", "type", "varies", "text", "residual", "account_sources", "provenance")
VARIES_KEYS = ("locus", "anchor")
LOCI = ("long",)
RESIDUAL_KEYS = ("where_both_stop", "concedes", "status")
CONCEDES_KEYS = ("library", "account")
RESIDUAL_STATUS = ("open",)
SOURCE_KEYS = ("canon", "turn_md5")
PROVENANCE_KEYS = ("phase", "date", "seat")
VARIANT_PHASES = ("V",)
TEXT_WORDS = (120, 300)
ANCHOR_MAX_WORDS = 15
VARIANTS_PER_NODE_AND_TYPE = 1
NO_WIN = ("refutes", "defeats", "proves", "settles", "decisive", "wins")
PRO_LIFE = ("life is worth living", "your life matters", "things get better", "life is precious", "life is a gift")
NO_WIN_RE = re.compile(r"\b(?:%s)\b" % "|".join(NO_WIN), re.I)
VARIANT_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MD5_RE = re.compile(r"^[0-9a-f]{32}$")
PATH_TOKEN_RE = re.compile(r"^([A-Za-z0-9_\-]+)((?:\[\d+\])*)$")
CHECKS = ("container-shape", "meta-corpus-pin", "meta-canon-pin", "variant-keys", "variant-id", "type-closed",
          "variant-cap", "varies-locus", "anchor-rule", "text-band", "text-ascii", "residual", "floor-no-win",
          "floor-exit", "floor-wide", "floor-pro-life", "account-sources", "provenance", "variant-coverage")
assert not set(VARIANT_PHASES) & (set(MAPV.PHASES) | {"S"}), "a variant phase letter collides with another phase"


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def resolve(doc, path):
    """A dotted path with [i] indices ("a.b.c[3]") inside a JSON document; None if any step is missing."""
    cur = doc
    for tok in path.split("."):
        m = PATH_TOKEN_RE.match(tok)
        if not m:
            return None
        if not isinstance(cur, dict) or m.group(1) not in cur:
            return None
        cur = cur[m.group(1)]
        for ix in re.findall(r"\[(\d+)\]", m.group(2)):
            if not isinstance(cur, list) or int(ix) >= len(cur):
                return None
            cur = cur[int(ix)]
    return cur


def floor_hits(s):
    """Every floor's hits in one string: {check: [match, ...]}."""
    low = s.lower()
    return {
        "floor-no-win": [m.group(0) for m in NO_WIN_RE.finditer(s)],
        "floor-exit": [m.group(0) for p in EXIT for m in re.finditer(p, s)],
        "floor-wide": ["%s:%s" % (n, m.group(0)) for n, p in WIDE for m in re.finditer(p, s, flags=re.I)],
        "floor-pro-life": [p for p in PRO_LIFE if p in low],
    }


def _ascii_ok(s):
    return isinstance(s, str) and s.strip() != "" and not non_ascii_chars(s)


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


def _check_variant(run, v, tag, nodes, canon, host=None, per_key=None):
    """One variant. `canon` is the parsed canon, or None if it did not load (meta-canon-pin is RED then)."""
    if not isinstance(v, dict):
        run.note("variant-keys", False, "%s: not an object" % tag)
        return
    missing, extra = sorted(set(REQUIRED_KEYS) - set(v)), sorted(set(v) - set(REQUIRED_KEYS))
    run.note("variant-keys", not missing and not extra, "%s: missing %s, unknown %s" % (tag, missing, extra))

    vtype = v.get("type")
    known_type = vtype in TYPES
    if "type" in v:
        run.note("type-closed", known_type, "%s: type %r not in the closed set %s" % (tag, vtype, sorted(TYPES)))

    node_id = None
    if "variant_id" in v:
        vid = v["variant_id"]
        ok = isinstance(vid, str) and bool(VARIANT_ID_RE.match(vid))
        why = "not <node-id>/<type>"
        if ok:
            nid, suffix = vid.split("/", 1)
            if nid not in nodes:
                ok, why = False, "node %r not in the corpus" % nid
            elif host is not None and nid != host:
                ok, why = False, "sits on %r but names %r" % (host, nid)
            elif "type" in v and suffix != vtype:
                ok, why = False, "suffix %r is not the type %r" % (suffix, vtype)
            else:
                node_id = nid
        run.note("variant-id", ok, "%s: %s" % (tag, why))
        if node_id is not None and per_key is not None:
            per_key.setdefault((node_id, vtype if isinstance(vtype, str) else "?"), []).append(tag)

    if "varies" in v:
        va = v["varies"]
        ok = isinstance(va, dict) and set(va) == set(VARIES_KEYS) and va.get("locus") in LOCI \
            and isinstance(va.get("anchor"), str)
        run.note("varies-locus", ok, "%s: varies must be exactly {locus: %s, anchor: str}" % (tag, LOCI))
        if ok and node_id is not None:
            a, long_t = va["anchor"], locus_text(nodes[node_id], va["locus"])
            n = long_t.count(a) if a.strip() else 0
            run.note("anchor-rule", a.strip() != "" and wc(a) <= ANCHOR_MAX_WORDS and n == 1,
                     "%s: anchor empty, over %d words, or found %d times in %s#long (must be exactly 1)"
                     % (tag, ANCHOR_MAX_WORDS, n, node_id))

    floor_strings = []
    if "text" in v:
        t = v["text"]
        n = wc(t) if isinstance(t, str) else -1
        run.note("text-band", TEXT_WORDS[0] <= n <= TEXT_WORDS[1],
                 "%s: text has %d words (band %d-%d)" % ((tag, n) + TEXT_WORDS))
        why = []
        if not isinstance(t, str):
            why.append("not a string")
        else:
            floor_strings.append(("text", t))
            if non_ascii_chars(t):
                why.append("non-ASCII %r" % non_ascii_chars(t))
            if DASH_TOKEN_RE.search(t):
                why.append("standalone dash token")
        run.note("text-ascii", not why, "%s: %s" % (tag, "; ".join(why)))

    if "residual" in v:
        r = v["residual"]
        why = []
        if not isinstance(r, dict) or set(r) != set(RESIDUAL_KEYS):
            why.append("must be exactly %s" % (RESIDUAL_KEYS,))
        if isinstance(r, dict):
            if "where_both_stop" in r:
                if _ascii_ok(r["where_both_stop"]):
                    floor_strings.append(("residual.where_both_stop", r["where_both_stop"]))
                else:
                    why.append("where_both_stop must be a non-empty ASCII sentence")
            if "concedes" in r:
                c = r["concedes"]
                if not isinstance(c, dict) or set(c) != set(CONCEDES_KEYS):
                    why.append("concedes must be exactly %s" % (CONCEDES_KEYS,))
                else:
                    for k in CONCEDES_KEYS:
                        if _ascii_ok(c[k]):
                            floor_strings.append(("residual.concedes.%s" % k, c[k]))
                        else:
                            why.append("concedes.%s must be a non-empty ASCII sentence" % k)
            if "status" in r and r["status"] not in RESIDUAL_STATUS:
                why.append("status %r: no variant may call the residual anything but open" % r["status"])
        run.note("residual", not why, "%s: %s" % (tag, "; ".join(why)))

    hits = {c: [] for c in ("floor-no-win", "floor-exit", "floor-wide", "floor-pro-life")}
    for where, s in floor_strings:
        for c, hs in floor_hits(s).items():
            hits[c] += ["%s %r" % (where, h) for h in hs]
    if floor_strings:
        for c in ("floor-no-win", "floor-exit", "floor-wide", "floor-pro-life"):
            run.note(c, not hits[c], "%s: %s" % (tag, "; ".join(hits[c])))

    if "account_sources" in v:
        src = v["account_sources"]
        why = []
        if not isinstance(src, list) or not src:
            why.append("must be a non-empty list")
        else:
            root = TYPES[vtype]["source_root"] if known_type else None
            for i, s in enumerate(src):
                if not (isinstance(s, dict) and set(s) == set(SOURCE_KEYS) and isinstance(s.get("canon"), str)
                        and isinstance(s.get("turn_md5"), str) and MD5_RE.match(s["turn_md5"])):
                    why.append("[%d] must be exactly {canon: <path>, turn_md5: <md5>}" % i)
                    continue
                if root is not None and not s["canon"].startswith(root + "["):
                    why.append("[%d] %r is not under the type's source root %s" % (i, s["canon"], root))
                    continue
                if canon is None:
                    continue
                e = resolve(canon, s["canon"])
                if not (isinstance(e, dict) and isinstance(e.get("verbatim"), str) and e["verbatim"].strip()
                        and isinstance(e.get("turn_md5"), str)):
                    why.append("[%d] %r does not resolve to his verbatim words in the pinned canon" % (i, s["canon"]))
                elif e["turn_md5"] != s["turn_md5"]:
                    why.append("[%d] turn_md5 %s is not the entry's %s" % (i, s["turn_md5"], e["turn_md5"]))
        run.note("account-sources", not why, "%s: %s" % (tag, "; ".join(why)))

    if "provenance" in v:
        p = v["provenance"]
        ok = (isinstance(p, dict) and set(p) == set(PROVENANCE_KEYS) and p.get("phase") in VARIANT_PHASES
              and isinstance(p.get("date"), str) and bool(DATE_RE.match(p["date"]))
              and isinstance(p.get("seat"), str) and p["seat"].strip() != "")
        run.note("provenance", ok, "%s: provenance must be {phase in %s, date YYYY-MM-DD, seat}"
                 % (tag, VARIANT_PHASES))


def _cap(run, per_key):
    for (nid, vt), tags in sorted(per_key.items()):
        run.note("variant-cap", len(tags) <= VARIANTS_PER_NODE_AND_TYPE,
                 "(%s, %s) has %d variants (cap %d): %s" % (nid, vt, len(tags), VARIANTS_PER_NODE_AND_TYPE, tags))


def _report(run, out, extra):
    for c in CHECKS:
        ok_n, bad_n = run.counts[c]
        out("%s . %s (%d ok / %d fail)" % ("PASS" if bad_n == 0 else "FAIL", c, ok_n, bad_n))
    verdict = "PASS" if not run.violations else "FAIL"
    summary = dict(extra)
    summary.update({"violation_count": len(run.violations), "violations": run.violations[:25], "verdict": verdict})
    out(json.dumps(summary, indent=1, sort_keys=True))
    return verdict == "PASS"


def _load_corpus(corpus_path):
    raw = open(corpus_path, "rb").read()
    corpus = json.loads(raw.decode("utf-8"))
    return raw, corpus, {n["id"]: n for n in corpus["objections"]}


def _load_canon(source_canon, override):
    """(canon or None, why). The canon at meta.source_canon's md5; an explicit override must match it too."""
    if not (isinstance(source_canon, dict) and set(source_canon) == {"file", "md5"}
            and isinstance(source_canon.get("file"), str) and isinstance(source_canon.get("md5"), str)):
        return None, "meta.source_canon must be exactly {file, md5}"
    try:
        b = open(override, "rb").read() if override else bytes_at(REPO, source_canon["file"], source_canon["md5"])
    except (LookupError, OSError) as e:
        return None, str(e)
    if md5_bytes(b) != source_canon["md5"]:
        return None, "the canon read is %s, not the pinned %s" % (md5_bytes(b), source_canon["md5"])
    try:
        return json.loads(b.decode("utf-8")), None
    except ValueError as e:
        return None, "the canon does not parse: %s" % e


def validate(paths, corpus_path, canon_override=None, out=print):
    """Staging files against one corpus. Returns (ok, failed_checks, violations)."""
    raw, corpus, nodes = _load_corpus(corpus_path)
    run = _Run()
    per_key, n_var = {}, 0
    for p in paths:
        base = os.path.basename(p)
        doc = json.loads(open(p, "rb").read().decode("utf-8"))
        ok = isinstance(doc, dict) and set(doc) == {"meta", "variants"} and isinstance(doc.get("meta"), dict) \
            and isinstance(doc.get("variants"), list)
        run.note("container-shape", ok, "%s: must be exactly {meta: {...}, variants: [...]}" % base)
        if not ok:
            continue
        meta, variants = doc["meta"], doc["variants"]
        pin_ok = meta.get("source_corpus_md5") == md5_bytes(raw)
        if pin_ok and "source_corpus_objections_md5" in meta:
            pin_ok = meta["source_corpus_objections_md5"] == objections_digest(corpus)
        run.note("meta-corpus-pin", pin_ok, "%s: the corpus pin does not match the corpus read" % base)
        canon, why = _load_canon(meta.get("source_canon"), canon_override)
        run.note("meta-canon-pin", canon is not None, "%s: %s" % (base, why))
        own = set()
        for i, v in enumerate(variants):
            n_var += 1
            tag = "%s[%d] %s" % (base, i, v.get("variant_id") if isinstance(v, dict) else "?")
            before = {k: len(x) for k, x in per_key.items()}
            _check_variant(run, v, tag, nodes, canon, per_key=per_key)
            own.update(k[0] for k, x in per_key.items() if len(x) > before.get(k, 0))
        own_cov = "%d/%d" % (len(own), len(nodes))
        run.note("variant-coverage", meta.get("variant_coverage") == own_cov,
                 "%s: declared %r vs this file's %r" % (base, meta.get("variant_coverage"), own_cov))
    _cap(run, per_key)
    ok = _report(run, out, {"mode": "staging", "files": len(paths), "variants": n_var,
                            "nodes_with_variants": len({k[0] for k in per_key}), "corpus_md5": md5_bytes(raw)})
    return ok, run.failed(), run.violations


def _root_canon():
    found = sorted(glob.glob(os.path.join(REPO, "project_canon_v38_*.json")))
    if len(found) != 1:
        raise SystemExit("expected exactly one project_canon_v38_*.json at the root, found %d" % len(found))
    return found[0]


def validate_embedded(corpus_path, canon_path, out=print):
    """The corpus's own responseVariants, against the canon given (default: the one at the root)."""
    raw, corpus, nodes = _load_corpus(corpus_path)
    run = _Run()
    cb = open(canon_path, "rb").read()
    canon, why = _load_canon({"file": os.path.basename(canon_path), "md5": md5_bytes(cb)}, canon_path)
    run.note("meta-canon-pin", canon is not None, "%s: %s" % (os.path.basename(canon_path), why))
    per_key, n_var = {}, 0
    for n in corpus["objections"]:
        if "responseVariants" in (n.get("responses") or {}):
            run.note("container-shape", False, "%s: responseVariants under responses (RV-1: a top-level key)" % n["id"])
        if "responseVariants" not in n:
            continue
        vs = n["responseVariants"]
        run.note("container-shape", isinstance(vs, list), "%s: responseVariants is not a list" % n["id"])
        if not isinstance(vs, list):
            continue
        for i, v in enumerate(vs):
            n_var += 1
            _check_variant(run, v, "%s.responseVariants[%d]" % (n["id"], i), nodes, canon, host=n["id"],
                           per_key=per_key)
    _cap(run, per_key)
    nn = len({k[0] for k in per_key})
    ok = _report(run, out, {"mode": "embedded", "variants": n_var, "nodes_with_variants": nn,
                            "variant_coverage": "%d/%d" % (nn, len(nodes)), "corpus_md5": md5_bytes(raw),
                            "canon_md5": md5_bytes(cb)})
    return ok, run.failed(), run.violations


# ---------------------------------------------------------------- self-test

def _words(n, w="word"):
    return " ".join([w] * n)


ROOT = TYPES["relief-account"]["source_root"]


def _mini_corpus():
    long_x = ("The quick brown fox jumps over the lazy dog while the library answers the objection in full, "
              "naming its premise and the cost of holding it. The fox is quick.")
    return {
        "version": "mini",
        "objections": [
            {"id": "node-x", "tier": 1, "trigger": ["x"], "diagnosis": "diagnosis text for node x",
             "responses": {"short": "short text x", "medium": "medium text x", "long": long_x}},
            {"id": "node-y", "tier": 2, "trigger": ["y"], "diagnosis": "diagnosis text for node y",
             "responses": {"short": "short text y", "medium": "medium text y",
                           "long": "long text y, where positive states are real and valued"}},
            {"id": "node-z", "tier": 3, "trigger": ["z"], "diagnosis": "diagnosis text for node z",
             "responses": {"short": "short text z", "medium": "medium text z", "long": "long text z"}},
        ],
    }


def _mini_canon():
    """The canon's shape at the two paths the controls touch: the type's source root and a his_words block."""
    accounts = [{"verbatim": "an account in his words, number %d" % i, "turn_md5": "%032x" % (i + 1)}
                for i in range(3)]
    canon = {"adversarial_map": {"relief_view_for_the_variant": {"his_accounts_verbatim": accounts},
                                 "his_words_X": {"R0001": {"his_word": {"verbatim": "a ruling",
                                                                        "turn_md5": "f" * 32}}}}}
    assert resolve(canon, ROOT + "[0]") is accounts[0]
    return canon


def _residual():
    return {"where_both_stop": "Both stop at whether the deficit is always present.",
            "concedes": {"library": "The library concedes the account is coherent.",
                         "account": "The account concedes reliability is not proof."},
            "status": "open"}


def _variant(nid, anchor, src_index=0, text_words=150):
    return {"variant_id": "%s/relief-account" % nid, "type": "relief-account",
            "varies": {"locus": "long", "anchor": anchor}, "text": _words(text_words),
            "residual": _residual(),
            "account_sources": [{"canon": "%s[%d]" % (ROOT, src_index), "turn_md5": "%032x" % (src_index + 1)}],
            "provenance": {"phase": "V", "date": "2026-10-04", "seat": "self-test"}}


def self_test():
    tmp = tempfile.mkdtemp(prefix="rv_selftest_")
    results = []
    try:
        mini = _mini_corpus()
        cpath = os.path.join(tmp, "mini_corpus.json")
        cbytes = (json.dumps(mini, indent=2, sort_keys=True) + "\n").encode("utf-8")
        open(cpath, "wb").write(cbytes)
        cmd5, cdig = md5_bytes(cbytes), objections_digest(mini)
        kpath = os.path.join(tmp, "mini_canon.json")
        kbytes = (json.dumps(_mini_canon(), indent=2, sort_keys=True) + "\n").encode("utf-8")
        open(kpath, "wb").write(kbytes)
        kmd5 = md5_bytes(kbytes)
        counter = [0]

        def write(doc):
            counter[0] += 1
            p = os.path.join(tmp, "frag_%03d.json" % counter[0])
            open(p, "w").write(json.dumps(doc, indent=1))
            return p

        def run_case(name, docs, expect, corpus_path=cpath, canon_path=kpath, embedded=False):
            sink = []
            if embedded:
                ok, failed, _v = validate_embedded(corpus_path, canon_path, out=sink.append)
            else:
                ok, failed, _v = validate([write(d) for d in docs], corpus_path, canon_override=canon_path,
                                          out=sink.append)
            want = [] if expect is None else sorted([expect] if isinstance(expect, str) else expect)
            results.append({"case": name, "expect": want or ["PASS"], "failed": failed, "ok": failed == want})

        def base():
            return {"meta": {"source_corpus_md5": cmd5, "source_corpus_objections_md5": cdig,
                             "source_canon": {"file": "mini_canon.json", "md5": kmd5}, "variant_coverage": "2/3"},
                    "variants": [_variant("node-x", "the lazy dog", 0),
                                 _variant("node-y", "positive states are real", 2)]}

        def mut(fn):
            d = base()
            fn(d)
            return d

        V = lambda d, i: d["variants"][i]  # noqa: E731

        # 0. the unmutated control, FIRST
        run_case("control-staging", [base()], None)

        def two_files():
            a, b = base(), base()
            a["variants"], b["variants"] = a["variants"][:1], b["variants"][1:]
            a["meta"]["variant_coverage"] = b["meta"]["variant_coverage"] = "1/3"
            return [a, b]
        run_case("control-two-files-own-coverage", two_files(), None)
        run_case("control-text-at-120", [mut(lambda d: V(d, 0).__setitem__("text", _words(120)))], None)
        run_case("control-text-at-300", [mut(lambda d: V(d, 0).__setitem__("text", _words(300)))], None)
        run_case("control-anchor-at-15-words", [mut(lambda d: V(d, 0)["varies"].__setitem__(
            "anchor", "The quick brown fox jumps over the lazy dog while the library answers the objection"))],
            None)
        run_case("control-floor-words-inside-other-words", [mut(lambda d: V(d, 0).__setitem__(
            "text", _words(140) + " the account proved nothing and won nothing, a prove and a defeat"))], None)

        # container-shape, meta-*
        run_case("container-extra-key", [mut(lambda d: d.__setitem__("extra", 1))], "container-shape")
        run_case("container-shapes-not-variants", [mut(lambda d: d.__setitem__("shapes", d.pop("variants")))],
                 "container-shape")
        run_case("meta-corpus-pin-wrong", [mut(lambda d: d["meta"].__setitem__("source_corpus_md5", "0" * 32))],
                 "meta-corpus-pin")
        run_case("meta-digest-wrong", [mut(lambda d: d["meta"].__setitem__("source_corpus_objections_md5",
                                                                          "0" * 32))], "meta-corpus-pin")
        run_case("meta-canon-md5-wrong", [mut(lambda d: d["meta"]["source_canon"].__setitem__("md5", "0" * 32))],
                 "meta-canon-pin")
        run_case("meta-canon-missing", [mut(lambda d: d["meta"].pop("source_canon"))], "meta-canon-pin")
        # variant-keys
        run_case("keys-unknown", [mut(lambda d: V(d, 0).__setitem__("label", "my own label"))], "variant-keys")
        run_case("keys-missing-residual", [mut(lambda d: V(d, 0).pop("residual"))], "variant-keys")
        # variant-id
        # a variant whose id fails names no node, so this file's own coverage is 1/3 and declared so
        def bad_id(vid):
            def fn(d):
                V(d, 0)["variant_id"] = vid
                d["meta"]["variant_coverage"] = "1/3"
            return fn
        run_case("id-bad-format", [mut(bad_id("node-x_relief"))], "variant-id")
        run_case("id-unknown-node", [mut(bad_id("node-q/relief-account"))], "variant-id")
        run_case("id-suffix-not-type", [mut(bad_id("node-x/relief"))], "variant-id")
        # type-closed
        run_case("type-open", [mut(lambda d: (V(d, 0).__setitem__("type", "steelman"),
                                              V(d, 0).__setitem__("variant_id", "node-x/steelman")))],
                 "type-closed")
        # variant-cap
        run_case("cap-two-on-one-node", [mut(lambda d: d["variants"].append(copy.deepcopy(V(d, 0))))], "variant-cap")

        def cap_across():
            a, b = two_files()
            b["variants"].append(copy.deepcopy(a["variants"][0]))
            b["meta"]["variant_coverage"] = "2/3"
            return [a, b]
        run_case("cap-across-files", cap_across(), "variant-cap")
        # varies-locus
        run_case("locus-short", [mut(lambda d: V(d, 0)["varies"].__setitem__("locus", "short"))], "varies-locus")
        run_case("locus-extra-key", [mut(lambda d: V(d, 0)["varies"].__setitem__("sentence", 3))], "varies-locus")
        # anchor-rule
        run_case("anchor-not-verbatim", [mut(lambda d: V(d, 0)["varies"].__setitem__("anchor", "the lazy cat"))],
                 "anchor-rule")
        run_case("anchor-16-words", [mut(lambda d: V(d, 0)["varies"].__setitem__(
            "anchor", "The quick brown fox jumps over the lazy dog while the library answers the objection in"))],
            "anchor-rule")
        run_case("anchor-not-unique", [mut(lambda d: V(d, 0)["varies"].__setitem__("anchor", "fox"))],
                 "anchor-rule")
        run_case("anchor-empty", [mut(lambda d: V(d, 0)["varies"].__setitem__("anchor", " "))], "anchor-rule")
        run_case("anchor-from-another-node", [mut(lambda d: V(d, 0)["varies"].__setitem__(
            "anchor", "positive states are real"))], "anchor-rule")
        # text-band, text-ascii
        run_case("text-119-words", [mut(lambda d: V(d, 0).__setitem__("text", _words(119)))], "text-band")
        run_case("text-301-words", [mut(lambda d: V(d, 0).__setitem__("text", _words(301)))], "text-band")
        run_case("text-curly-quote", [mut(lambda d: V(d, 0).__setitem__(
            "text", _words(140) + " “quoted”"))], "text-ascii")
        run_case("text-dash-token", [mut(lambda d: V(d, 0).__setitem__("text", _words(70) + " - " + _words(70)))],
                 "text-ascii")
        # residual
        run_case("residual-closed", [mut(lambda d: V(d, 0)["residual"].__setitem__("status", "closed"))], "residual")
        run_case("residual-no-account-concession", [mut(lambda d: V(d, 0)["residual"]["concedes"].pop("account"))],
                 "residual")
        run_case("residual-empty-stop", [mut(lambda d: V(d, 0)["residual"].__setitem__("where_both_stop", " "))],
                 "residual")
        run_case("residual-extra-key", [mut(lambda d: V(d, 0)["residual"].__setitem__("bedrock", "HR-02"))],
                 "residual")
        # the floors, over the text and over the residual
        for w in NO_WIN:
            run_case("no-win-text-%s" % w, [mut(lambda d, w=w: V(d, 0).__setitem__(
                "text", _words(140) + " so the account %s it" % w))], "floor-no-win")
        run_case("no-win-in-residual", [mut(lambda d: V(d, 0)["residual"]["concedes"].__setitem__(
            "account", "Nothing; the account wins."))], "floor-no-win")
        for i, w in enumerate(PRO_LIFE):
            run_case("pro-life-%d" % i, [mut(lambda d, w=w: V(d, 0).__setitem__(
                "text", _words(140) + " and " + w.capitalize()))], "floor-pro-life")
        run_case("pro-life-in-residual", [mut(lambda d: V(d, 0)["residual"].__setitem__(
            "where_both_stop", "Both stop where things get better."))], "floor-pro-life")
        run_case("wide-only-taboo", [mut(lambda d: V(d, 0).__setitem__(
            "text", _words(140) + " the taboo"))], "floor-wide")
        run_case("wide-in-residual", [mut(lambda d: V(d, 0)["residual"]["concedes"].__setitem__(
            "library", "The library concedes the neurochemical story."))], "floor-wide")
        run_case("exit-pattern-and-wide-together", [mut(lambda d: V(d, 0).__setitem__(
            "text", _words(140) + " the body vetoes the mind"))], ["floor-exit", "floor-wide"])
        # account-sources
        run_case("sources-empty", [mut(lambda d: V(d, 0).__setitem__("account_sources", []))], "account-sources")
        run_case("sources-outside-root", [mut(lambda d: V(d, 0).__setitem__("account_sources", [
            {"canon": "adversarial_map.his_words_X.R0001.his_word", "turn_md5": "f" * 32}]))], "account-sources")
        run_case("sources-unresolved-index", [mut(lambda d: V(d, 0).__setitem__("account_sources", [
            {"canon": ROOT + "[7]", "turn_md5": "%032x" % 8}]))], "account-sources")
        run_case("sources-turn-md5-wrong", [mut(lambda d: V(d, 0)["account_sources"][0].__setitem__(
            "turn_md5", "%032x" % 2))], "account-sources")
        run_case("sources-extra-key", [mut(lambda d: V(d, 0)["account_sources"][0].__setitem__("quote", "x"))],
                 "account-sources")
        # provenance
        run_case("provenance-shape-phase", [mut(lambda d: V(d, 0)["provenance"].__setitem__("phase", "S"))],
                 "provenance")
        run_case("provenance-bad-date", [mut(lambda d: V(d, 0)["provenance"].__setitem__("date", "04-10-2026"))],
                 "provenance")
        run_case("provenance-no-seat", [mut(lambda d: V(d, 0)["provenance"].__setitem__("seat", ""))], "provenance")
        # variant-coverage
        run_case("coverage-overclaimed", [mut(lambda d: d["meta"].__setitem__("variant_coverage", "3/3"))],
                 "variant-coverage")
        run_case("coverage-undeclared", [mut(lambda d: d["meta"].pop("variant_coverage"))], "variant-coverage")

        def summed():
            a, b = two_files()
            a["meta"]["variant_coverage"] = b["meta"]["variant_coverage"] = "2/3"
            return [a, b]
        run_case("coverage-summed-across-files", summed(), "variant-coverage")

        # --embedded: the corpus's own responseVariants
        def embedded_case(name, fn, expect):
            c = _mini_corpus()
            c["objections"][0]["responseVariants"] = [_variant("node-x", "the lazy dog", 0)]
            fn(c)
            p = os.path.join(tmp, "embedded_%s.json" % name)
            open(p, "w").write(json.dumps(c, indent=2, sort_keys=True) + "\n")
            run_case(name, None, expect, corpus_path=p, embedded=True)
        embedded_case("control-embedded", lambda c: None, None)
        embedded_case("embedded-under-responses", lambda c: c["objections"][1]["responses"].__setitem__(
            "responseVariants", []), "container-shape")
        embedded_case("embedded-not-a-list", lambda c: c["objections"][0].__setitem__("responseVariants", {}),
                      "container-shape")
        embedded_case("embedded-wrong-host", lambda c: c["objections"][0]["responseVariants"][0].__setitem__(
            "variant_id", "node-y/relief-account"), "variant-id")

        # the real corpus and the real canon, each read at its pin: the measured anchors, his accounts
        rpath = path_at(REPO, CORPUS_REL, REAL_CORPUS_MD5)
        rraw, rcorpus, rnodes = _load_corpus(rpath)
        rcanon = json.loads(bytes_at(REPO, *REAL_CANON).decode("utf-8"))
        measure = json.loads(bytes_at(REPO, *MEASURE).decode("utf-8"))
        anchors = {nid: rec["anchor"] for nid, rec in sorted(measure["nodes"].items())}
        accounts = resolve(rcanon, ROOT)
        last = len(accounts) - 1

        def real_variant(nid, src_index=last):
            v = _variant(nid, anchors[nid])
            v["account_sources"] = [{"canon": "%s[%d]" % (ROOT, src_index),
                                     "turn_md5": accounts[src_index]["turn_md5"]}]
            return v

        def real(variants):
            return {"meta": {"source_corpus_md5": md5_bytes(rraw),
                             "source_corpus_objections_md5": objections_digest(rcorpus),
                             "source_canon": {"file": REAL_CANON[0], "md5": REAL_CANON[1]},
                             "variant_coverage": "%d/%d" % (len(variants), len(rnodes))}, "variants": variants}
        real_all = [real_variant(nid) for nid in anchors]
        run_case("real-control-seven-measured-anchors", [real(real_all)], None, corpus_path=rpath, canon_path=None)

        def rmut(fn):
            vs = copy.deepcopy(real_all)
            fn(vs)
            return [real(vs)]
        nps = "neuroscience-positive-states"
        ix = sorted(anchors).index(nps)
        run_case("real-anchor-not-unique", rmut(lambda vs: vs[ix]["varies"].__setitem__("anchor", "positive states")),
                 "anchor-rule", corpus_path=rpath, canon_path=None)
        run_case("real-turn-md5-of-another-account", rmut(lambda vs: vs[ix]["account_sources"][0].__setitem__(
            "turn_md5", accounts[0]["turn_md5"])), "account-sources", corpus_path=rpath, canon_path=None)
        run_case("real-his-ruling-not-an-account", rmut(lambda vs: vs[ix].__setitem__("account_sources", [
            {"canon": "adversarial_map.his_words_V5.R0314.his_word",
             "turn_md5": rcanon["adversarial_map"]["his_words_V5"]["R0314"]["his_word"]["turn_md5"]}])),
            "account-sources", corpus_path=rpath, canon_path=None)
        results.append({"case": "real-corpus-has-no-responseVariants-yet", "expect": ["0 nodes"], "failed": [],
                        "ok": not any("responseVariants" in n or "responseVariants" in (n.get("responses") or {})
                                      for n in rcorpus["objections"])})

        # the schema, the validator, canon and the design agree
        sch, pr = SCHEMA, SCHEMA["$defs"]["variant"]["properties"]
        design = re.sub(r"\s+", " ", bytes_at(REPO, *DESIGN).decode("utf-8"))
        design_v5 = rcanon["adversarial_map"]["response_variants_design_V5"]
        agree = {
            "required": sorted(SCHEMA["$defs"]["variant"]["required"]) == sorted(REQUIRED_KEYS),
            "types": pr["type"]["enum"] == sorted(TYPES),
            "label_is_canon_label_leaned": TYPES["relief-account"]["label"] == design_v5["label_leaned"],
            "label_in_design": TYPES["relief-account"]["label"] in design,
            "whose_account_in_design": TYPES["relief-account"]["whose_account"] in design,
            "source_root_resolves": isinstance(accounts, list) and len(accounts) == measure["his_accounts_in_canon"],
            "loci": pr["varies"]["properties"]["locus"]["enum"] == list(LOCI),
            "anchor": pr["varies"]["properties"]["anchor"]["x-words"] == [1, ANCHOR_MAX_WORDS],
            "text": pr["text"]["x-words"] == list(TEXT_WORDS),
            "residual": sorted(pr["residual"]["required"]) == sorted(RESIDUAL_KEYS)
            and pr["residual"]["properties"]["status"]["enum"] == list(RESIDUAL_STATUS),
            "phases": pr["provenance"]["properties"]["phase"]["enum"] == list(VARIANT_PHASES),
            "cap": sch["x-caps"]["variants_per_node_and_type"] == VARIANTS_PER_NODE_AND_TYPE,
            "variant_id_re": pr["variant_id"]["pattern"].replace("(-", "(?:-") == VARIANT_ID_RE.pattern,
            "no_win_schema": sch["x-floors"]["no_win"] == list(NO_WIN),
            "no_win_is_the_design_list": ", ".join(NO_WIN) in design,
            "pro_life_schema": sch["x-floors"]["pro_life"] == list(PRO_LIFE),
            "pro_life_is_the_design_list": ", ".join(PRO_LIFE) in design,
            "exit_is_gate2s": len(EXIT) == 9,
            "wide_is_l6s": len(WIDE) == 13,
        }
        results.append({"case": "schema-validator-canon-design-agree", "expect": ["all true"],
                        "failed": sorted(k for k, v in agree.items() if not v), "ok": all(agree.values())})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # information for the drafter, not a check: his ten accounts against the floors and the ASCII rule
    info = []
    for i, a in enumerate(accounts):
        h = floor_hits(a["verbatim"])
        info.append({"canon": "%s[%d]" % (ROOT, i), "words": wc(a["verbatim"]),
                     "non_ascii": sorted(set(non_ascii_chars(a["verbatim"]))),
                     "floor_hits": sorted(x for c in sorted(h) for x in h[c])})
    fired = sorted({c for r in results for c in r["expect"] if c in CHECKS})
    record = {
        "instrument": "response_variants/response_variant_validator_v0_1.py",
        "imports": {"map_validator": {"path": MAPV_REL, "md5": MAPV_MD5},
                    "safety_floors": {"path": SAFETY_REL, "md5": SAFETY_MD5, "exit": len(EXIT), "wide": len(WIDE)}},
        "real_data": {"corpus_md5": REAL_CORPUS_MD5, "canon": {"file": REAL_CANON[0], "md5": REAL_CANON[1]},
                      "measure": {"file": MEASURE[0], "md5": MEASURE[1]}, "design": {"file": DESIGN[0],
                                                                                    "md5": DESIGN[1]}},
        "his_accounts_for_the_drafter": info,
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
            print("%s  %-44s expect %-28s failed %s" % ("ok " if r["ok"] else "BAD", r["case"],
                                                         ",".join(r["expect"]), r["failed"]))
        print("SELF-TEST %s: %d of %d as expected; %d of %d checks turned RED by a mutation"
              % ("GREEN" if ok else "RED", rec["summary"]["as_expected"], rec["summary"]["cases"],
                 rec["summary"]["checks_turned_red_by_a_mutation"], rec["summary"]["checks"]))
        return 0 if ok else 1
    opt = lambda k: argv[argv.index(k) + 1] if k in argv else None  # noqa: E731
    corpus, canon = opt("--corpus"), opt("--canon")
    if "--embedded" in argv:
        ok, _f, _v = validate_embedded(corpus or os.path.join(REPO, CORPUS_REL), canon or _root_canon())
        return 0 if ok else 1
    files = [a for i, a in enumerate(argv) if not a.startswith("--") and not (i > 0 and argv[i - 1] in
                                                                                ("--corpus", "--canon"))]
    if not files:
        print(__doc__)
        return 2
    if corpus is None:
        pin = json.loads(open(files[0], "rb").read().decode("utf-8")).get("meta", {}).get("source_corpus_md5")
        corpus = path_at(REPO, CORPUS_REL, pin)
        print("corpus: %s at %s (pinned by %s)" % (CORPUS_REL, pin, os.path.basename(files[0])))
    ok, _f, _v = validate(files, corpus, canon_override=canon)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
