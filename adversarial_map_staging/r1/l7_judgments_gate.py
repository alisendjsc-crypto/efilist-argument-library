#!/usr/bin/env python3
"""l7_judgments_gate.py -- the gate beside L7_successor_drafts_judgments.json (gate2, 2026-09-26, R0237).

L7_successor_drafts_judgments.json records gate2's judgment of L7's successor-map drafts (L7_successor_drafts.json: 31 amend,
8 file, 9 stands, 2 carry and 1 relation rows over adversarial_map_v1_7.json, validator v0_7 and register v0_8), the two
artifacts and the knock-on the successor owed. It is APPEND-ONLY: a row is never edited or removed, and a correction is a
new row whose `supersedes` names the row it replaces. Adapted from sp_judgments_gate.py. This gate checks, and exits 1:

  1. rows run U-001, U-002, ... in file order, each with exactly its kind's keys, a seat and a date;
  2. every amend, file, stands, carry and relation row names a current row of that kind in the drafts record, read at the
     bytes this header pins, and an amend, file or stands row names that row's target; an amend row states an R1 verdict
     exactly when its drafts row proposes one; an artifact row names the validator or the register the header pins; the
     knock_on rows are exactly the reading record's newly collided (a)s; every finding names an owner and R1 entries only;
  3. verdicts: ACCEPT, AMEND or REJECT (amend, file, relation); CONFIRM or REOPEN (stands); CONFIRM or CORRECT (carry,
     artifact); STANDS or REOPENS (knock_on); every AMEND, REJECT, CORRECT, REOPEN and REOPENS says what is owed;
  4. coverage: every current row of the pinned drafts record has exactly one current judgment, and so do both artifacts
     and every newly collided (a);
  5. every double-quoted span in a row's text is declared in that row's quotes, and every declared quote is verbatim at its
     source, each read at the bytes this header pins: drafts:<row id>, corpus:<node#locus>, v1_6:<node#locus>,
     v1_7:<node#locus>, rulings:R1-nnn, judgment_pq:X-nnn, judgment_sp:Z-nnn, canon:<dotted.path>, reading:record and
     l6_reading:record;
  6. the judged artifacts are at the md5s the header names, with three exceptions, each read at its pinned bytes from git
     history: an append-only record (the drafts record, R1_rulings.json, gate2's two earlier judgments) may have grown by
     appended rows; the canon may be gone from the tree (the rename convention); the corpus may have moved (a pin session
     moves it; every figure here is about the corpus the drafts pin). Nothing the next session changes can turn a true
     row RED;
  7. append-only: the committed base (git HEAD's copy) is intact.

  python3 l7_judgments_gate.py                             # base = git HEAD's copy
  python3 l7_judgments_gate.py --self-test [--emit <path>]   # controls; unmutated first

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/L7_successor_drafts_judgments.json"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "his_word", "kickoff", "judged", "instrument", "rows"]
PINS = ["drafts", "map_v1_6", "map_v1_7", "corpus", "validator_v0_7", "register_v0_7", "register_v0_8", "measure",
        "rulings", "judgment_pq", "judgment_sp", "l6_reading", "canon"]
TAIL = ["quotes", "seat", "date", "supersedes"]
KEYS = {
    "amend": ["id", "kind", "row_id", "target", "verdict", "r1", "reason", "owed", "carries"] + TAIL,
    "file": ["id", "kind", "row_id", "target", "verdict", "reason", "owed", "carries"] + TAIL,
    "stands": ["id", "kind", "row_id", "target", "verdict", "reason", "owed", "carries"] + TAIL,
    "carry": ["id", "kind", "row_id", "verdict", "reason", "owed", "carries"] + TAIL,
    "relation": ["id", "kind", "row_id", "verdict", "reason", "owed", "carries"] + TAIL,
    "artifact": ["id", "kind", "artifact", "verdict", "reason", "owed", "carries"] + TAIL,
    "knock_on": ["id", "kind", "i", "n", "target", "verdict", "reason", "owed", "carries"] + TAIL,
    "finding": ["id", "kind", "title", "finding", "recommendation", "whose", "entries"] + TAIL,
}
DRAFT_KINDS = ("amend", "file", "stands", "carry", "relation")
VERDICTS = {"amend": ("ACCEPT", "AMEND", "REJECT"), "file": ("ACCEPT", "AMEND", "REJECT"),
            "relation": ("ACCEPT", "AMEND", "REJECT"), "stands": ("CONFIRM", "REOPEN"),
            "carry": ("CONFIRM", "CORRECT"), "artifact": ("CONFIRM", "CORRECT"), "knock_on": ("STANDS", "REOPENS")}
R1_VALUES = ("HOLDS accepted", "HOLDS not accepted")
OWES = {"AMEND", "REJECT", "CORRECT", "REOPEN", "REOPENS"}
TEXT_FIELDS = {k: ("reason", "owed", "carries") for k in VERDICTS}
TEXT_FIELDS["finding"] = ("finding", "recommendation")
SPAN = re.compile(r'"([^"]+)"')
APPEND_ONLY = {"adversarial_map_staging/r1/L7_successor_drafts.json", "adversarial_map_staging/r1/R1_rulings.json",
               "adversarial_map_staging/r1/PQ_repair_drafts_judgments.json",
               "adversarial_map_staging/r1/SP_drafts_judgments.json"}
MAY_MOVE = {"efilist_argument_library_v4_0_0.json"}
RENAMED = re.compile(r"project_canon_v38_\d+\.json")
ARTIFACTS = ("validator_v0_7", "register_v0_8")


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def git_bytes_at(repo_dir, rel, want):
    """The newest committed blob of rel whose md5 is want, or None."""
    log = subprocess.run(["git", "-C", repo_dir, "log", "--format=%H", "--", rel], capture_output=True, text=True)
    for sha in log.stdout.split() if log.returncode == 0 else []:
        r = subprocess.run(["git", "-C", repo_dir, "show", "%s:%s" % (sha, rel)], capture_output=True)
        if r.returncode == 0 and hashlib.md5(r.stdout).hexdigest() == want:
            return r.stdout
    return None


def pinned_bytes(repo_dir, rel, want, history=None):
    """The bytes a pin names: the working copy if it still matches, else from history, else None."""
    p = os.path.join(repo_dir, rel)
    if os.path.exists(p):
        b = open(p, "rb").read()
        if hashlib.md5(b).hexdigest() == want:
            return b
    return (history or (lambda r_, w_: git_bytes_at(repo_dir, r_, w_)))(rel, want)


def rows_grown(base_bytes, path):
    """How many rows a record gained by appending since base_bytes, or None if it changed otherwise."""
    try:
        base, cur = json.loads(base_bytes.decode("utf-8")), json.load(open(path, encoding="utf-8"))
    except (ValueError, OSError):
        return None
    if {k: v for k, v in base.items() if k != "rows"} != {k: v for k, v in cur.items() if k != "rows"}:
        return None
    if cur.get("rows", [])[:len(base.get("rows", []))] != base.get("rows", []):
        return None
    return len(cur["rows"]) - len(base["rows"])


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def walk(o, dotted):
    for part in dotted.split("."):
        o = o[part]
    return o


def corpus_text(corpus, rest):
    node, _, locus = rest.partition("#")
    if node not in corpus:
        raise KeyError("no corpus node %s" % node)
    o = corpus[node]
    if locus in ("short", "medium", "long"):
        t = o["responses"].get(locus)
    elif locus.startswith("archetypeVariants."):
        t = (o["responses"].get("archetypeVariants") or {}).get(locus.split(".", 1)[1])
    else:
        t = o.get(locus)
    if not isinstance(t, str):
        raise KeyError("no corpus text at %s" % rest)
    return [t]


def current(rows, key="id"):
    sup = {r.get("supersedes") for r in rows if r.get("supersedes")}
    return [r for r in rows if r[key] not in sup]


def target_of(x):
    if x.get("entry"):
        return x["entry"].get("target")
    ne = x.get("new_entry") or {}
    return "%s#%s" % (ne.get("target_id"), ne.get("target_locus")) if ne else None


class Sources:
    """Every source resolves against the bytes the header pins."""

    def __init__(self, repo_dir, doc, history=None):
        j = doc["judged"]

        def at(key):
            b = pinned_bytes(repo_dir, j[key]["file"], j[key]["md5"], history)
            if b is None:  # rule 6 reports it; read what is there so the other checks still run
                p = os.path.join(repo_dir, j[key]["file"])
                b = open(p, "rb").read() if os.path.exists(p) else b"{}"
            return json.loads(b.decode("utf-8"))

        self.drafts = at("drafts")
        self.v16 = at("map_v1_6").get("entries", [])
        self.v17 = at("map_v1_7").get("entries", [])
        self.rulings = at("rulings").get("rows", [])
        self.pq = at("judgment_pq").get("rows", [])
        self.sp = at("judgment_sp").get("rows", [])
        self.l6 = at("l6_reading")
        self.canon = at("canon")
        c = at("corpus")
        self.corpus = {o["id"]: o for o in c.get("objections", [])}
        ip = os.path.join(repo_dir, doc["instrument"]["record"])
        self.reading = json.load(open(ip, encoding="utf-8")) if os.path.exists(ip) else {}

    def resolve(self, src):
        kind, _, rest = src.partition(":")
        if kind == "drafts":
            xs = [r for r in self.drafts.get("rows", []) if r.get("id") == rest]
            if not xs:
                raise KeyError("no drafts row %s" % rest)
            return list(strings(xs[0]))
        if kind == "corpus":
            return corpus_text(self.corpus, rest)
        if kind in ("v1_6", "v1_7"):
            node, _, locus = rest.partition("#")
            xs = [x for x in (self.v16 if kind == "v1_6" else self.v17) if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no %s entry at %s" % (kind, rest))
            return [s for x in xs for s in strings(x)]
        if kind == "rulings":
            xs = [r for r in self.rulings if r.get("row") == rest]
            if not xs:
                raise KeyError("no rulings row %s" % rest)
            return list(strings(xs[0]))
        if kind in ("judgment_pq", "judgment_sp"):
            xs = [r for r in (self.pq if kind == "judgment_pq" else self.sp) if r.get("id") == rest]
            if not xs:
                raise KeyError("no %s row %s" % (kind, rest))
            return list(strings(xs[0]))
        if kind == "canon":
            try:
                return list(strings(walk(self.canon, rest)))
            except (KeyError, TypeError):
                raise KeyError("no path %s in the pinned canon" % rest)
        if kind == "reading" and rest == "record":
            return list(strings(self.reading))
        if kind == "l6_reading" and rest == "record":
            return list(strings(self.l6))
        raise KeyError("unknown source %r" % src)


def texts_of(r):
    out = []
    for f in TEXT_FIELDS.get(r["kind"], ()):
        v = r.get(f)
        out += v if isinstance(v, list) else [v]
    return [t for t in out if isinstance(t, str)]


def subject(r):
    if r["kind"] in DRAFT_KINDS:
        return "%s %s" % (r["kind"], r.get("row_id"))
    if r["kind"] == "artifact":
        return "artifact %s" % r.get("artifact")
    if r["kind"] == "knock_on":
        return "knock_on %s" % r.get("i")
    return "finding %s" % r.get("title")


def check(path, repo_dir, base_text, history=None):
    fails, info = [], []
    doc = json.load(open(path, encoding="utf-8"))
    if list(doc) != HEADER_KEYS:
        return ["structure: header keys are %s" % list(doc)], info
    if sorted(doc["judged"]) != sorted(PINS):
        return ["structure: judged pins are %s" % sorted(doc["judged"])], info
    rows = doc["rows"]
    if not isinstance(rows, list) or not rows:
        return ["structure: no rows"], info

    # 6 -- the referents have not moved; an append-only one may have grown; a renamed canon may be gone; the corpus may move
    for name, pin in doc["judged"].items():
        p = os.path.join(repo_dir, pin["file"])
        got = md5(p) if os.path.exists(p) else "MISSING"
        if got == pin["md5"]:
            continue
        base = pinned_bytes(repo_dir, pin["file"], pin["md5"], history)
        if (got == "MISSING" and RENAMED.fullmatch(os.path.basename(pin["file"]))) or pin["file"] in MAY_MOVE:
            if base is None:
                fails.append("pin %s: %s is not at %s and its pinned bytes are not in git history" % (name, pin["file"], pin["md5"]))
            else:
                info.append("pin %s: %s is %s; read from history at %s" % (name, pin["file"], "gone (the rename convention)"
                                                                           if got == "MISSING" else "moved", pin["md5"][:8]))
            continue
        if pin["file"] not in APPEND_ONLY:
            fails.append("pin %s: %s is %s, header names %s" % (name, pin["file"], got, pin["md5"]))
            continue
        grown = rows_grown(base, p) if base is not None and got != "MISSING" else None
        if grown is None:
            fails.append("pin %s: %s is %s, header names %s, and it has not merely grown by appended rows"
                         % (name, pin["file"], got, pin["md5"]))
        else:
            info.append("pin %s: %s has grown by %d appended row(s) since the judgment; read at %s"
                        % (name, pin["file"], grown, pin["md5"][:8]))
    ins = doc["instrument"]
    ip = os.path.join(repo_dir, ins["record"])
    if not os.path.exists(os.path.join(repo_dir, ins["file"])):
        fails.append("instrument: %s is missing" % ins["file"])
    if not os.path.exists(ip) or md5(ip) != ins["md5"]:
        fails.append("instrument: %s is not at %s" % (ins["record"], ins["md5"]))

    src = Sources(repo_dir, doc, history)
    if not src.corpus:
        fails.append("pin corpus: the pinned corpus is not recoverable")
    dcur = {r["id"]: r for r in current(src.drafts.get("rows", []))}
    ruled_ns = {r["n"] for r in src.rulings}
    knock_want = {(x["i"], x["n"], x["target"]) for x in src.reading.get("knock_on", {}).get("newly_collided", [])}
    art_files = {doc["judged"][k]["file"] for k in ARTIFACTS}

    chains, cur = {}, {}
    for i, r in enumerate(rows, 1):
        rid = r.get("id", "?")
        kind = r.get("kind")
        if kind not in KEYS:
            fails.append("%s: kind %r" % (rid, kind))
            continue
        if list(r) != KEYS[kind]:
            fails.append("%s: keys differ from the %s schema (%s)" % (rid, kind, sorted(set(r) ^ set(KEYS[kind]))))
            continue
        # 1
        if rid != "U-%03d" % i:
            fails.append("%s: ids must run U-001, U-002, ... in file order (expected U-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2
        if kind in DRAFT_KINDS:
            x = dcur.get(r["row_id"])
            if x is None or x.get("kind") != kind:
                fails.append("%s: %s names no current %s row of the drafts record" % (rid, r["row_id"], kind))
            else:
                if kind in ("amend", "file", "stands") and r["target"] != target_of(x):
                    fails.append("%s: target %s is not %s's target %s" % (rid, r["target"], r["row_id"], target_of(x)))
                if kind == "amend":
                    if bool(x.get("proposed_r1")) != (r["r1"] is not None):
                        fails.append("%s: r1 is %r, but %s %s an R1 verdict" % (rid, r["r1"], r["row_id"],
                                                                             "proposes" if x.get("proposed_r1") else "proposes no"))
                    elif r["r1"] is not None and r["r1"] not in R1_VALUES:
                        fails.append("%s: r1 %r is not one of %s" % (rid, r["r1"], "/".join(R1_VALUES)))
        if kind == "artifact" and r["artifact"] not in art_files:
            fails.append("%s: artifact %s is not one the header pins as judged" % (rid, r["artifact"]))
        if kind == "knock_on" and (r["i"], r["n"], r["target"]) not in knock_want:
            fails.append("%s: knock-on entry %s (%s) is not one the reading record lists as newly collided" % (rid, r["i"], r["target"]))
        if kind in VERDICTS:
            if r["verdict"] not in VERDICTS[kind]:
                fails.append("%s: verdict %r is not one of %s" % (rid, r["verdict"], "/".join(VERDICTS[kind])))
            elif r["verdict"] in OWES and not [o for o in r["owed"] if str(o).strip()]:
                fails.append("%s: %s without saying what is owed" % (rid, r["verdict"]))
            if not str(r["reason"]).strip():
                fails.append("%s: no reason" % rid)
        if kind == "finding":
            if not str(r["whose"]).strip():
                fails.append("%s: a finding with no owner" % rid)
            bad = [n for n in r["entries"] if n not in ruled_ns]
            if bad:
                fails.append("%s: entries %s are not R1 entries" % (rid, bad))
        # 5 -- declared, and verbatim
        declared = [q.get("quote") for q in r["quotes"]]
        for t in texts_of(r):
            for span in SPAN.findall(t):
                if span not in declared:
                    fails.append("%s: undeclared quotation %r" % (rid, span[:60]))
        for j, q in enumerate(r["quotes"], 1):
            try:
                pool = src.resolve(q["src"])
            except KeyError as err:
                fails.append("%s: quote %d source %s -- %s" % (rid, j, q["src"], err))
                continue
            if not any(q["quote"] in t for t in pool):
                fails.append("%s: quote %d NOT VERBATIM at %s: %r" % (rid, j, q["src"], q["quote"][:80]))
        # 4 -- one current judgment per subject
        subj = subject(r)
        prev = chains.get(subj)
        if prev is None:
            if r["supersedes"] is not None:
                fails.append("%s: supersedes %s, but it is the first row for %s" % (rid, r["supersedes"], subj))
        elif r["supersedes"] != prev:
            fails.append("%s: %s judged twice without superseding %s" % (rid, subj, prev))
        chains[subj] = rid
        cur[subj] = r

    for k in DRAFT_KINDS:
        want = ["%s %s" % (k, x["id"]) for x in dcur.values() if x.get("kind") == k]
        missing = [s for s in want if s not in cur]
        if missing:
            fails.append("coverage: %s rows not judged: %s" % (k, ", ".join(missing)))
    for f in sorted(art_files):
        if "artifact %s" % f not in cur:
            fails.append("coverage: artifact %s not judged" % f)
    got_knock = {(r["i"], r["n"], r["target"]) for s, r in cur.items() if s.startswith("knock_on ")}
    if got_knock != knock_want:
        fails.append("coverage: knock-on rows %s do not match the reading record's newly collided %s"
                     % (sorted(k[0] for k in got_knock), sorted(k[0] for k in knock_want)))

    # 7 -- append-only against the committed base
    if base_text is None:
        info.append("append-only: SKIPPED -- no committed base yet (first landing); vacuous, not a pass")
    else:
        base = json.loads(base_text)
        if {k: v for k, v in base.items() if k != "rows"} != {k: v for k, v in doc.items() if k != "rows"}:
            fails.append("append-only: the header differs from the committed base")
        brows = base["rows"]
        if rows[:len(brows)] != brows:
            bad = next((b.get("id") for b, c in zip(brows, rows) if b != c), "a removed row")
            fails.append("append-only: committed row %s was edited or removed" % bad)
        if not any(f.startswith("append-only") for f in fails):
            info.append("append-only: %d committed rows intact, %d appended" % (len(brows), len(rows) - len(brows)))
    tally = {}
    for r in cur.values():
        if r["kind"] in VERDICTS:
            tally.setdefault(r["verdict"], 0)
            tally[r["verdict"]] += 1
    r1 = sum(1 for r in cur.values() if r["kind"] == "amend" and r["r1"] == "HOLDS accepted")
    info.append("rows %d | %s | HOLDS accepted %d | findings %d | quotes %d" % (
        len(rows), ", ".join("%s %d" % kv for kv in sorted(tally.items())), r1,
        sum(1 for r in cur.values() if r["kind"] == "finding"), sum(len(r["quotes"]) for r in rows)))
    return fails, info


def committed_base():
    try:
        return subprocess.run(["git", "-C", REPO, "show", "HEAD:" + REL], capture_output=True,
                              check=True).stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def self_test(emit=None):
    import shutil, tempfile
    real = os.path.join(REPO, REL)
    doc0 = json.load(open(real, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="l7jgate_")
    results = []
    try:
        def stage(mut_doc=None, mut_pin=None, base=None, grow=None, drop=None, corpus_edit=False):
            # every judged artifact at its pinned bytes, and the instrument; `grow` = (file suffix, fn) rewrites an
            # append-only record from its pinned document; `drop` leaves a file out; `corpus_edit` moves the corpus
            d = os.path.join(tmp, "c%d" % len(results))
            for key, pin in doc0["judged"].items():
                if drop and pin["file"].endswith(drop):
                    continue
                dst = os.path.join(d, pin["file"])
                os.makedirs(os.path.dirname(dst) or d, exist_ok=True)
                b = pinned_bytes(REPO, pin["file"], pin["md5"])
                if grow and pin["file"].endswith(grow[0]):
                    rd = json.loads(b.decode("utf-8")); grow[1](rd)
                    b = json.dumps(rd, ensure_ascii=False).encode("utf-8")
                if corpus_edit and key == "corpus":
                    cd = json.loads(b.decode("utf-8"))
                    src, quote = next((q["src"], q["quote"]) for r in doc0["rows"] for q in r["quotes"]
                                      if q["src"].startswith("corpus:"))
                    node, _, locus = src.split(":", 1)[1].partition("#")
                    o = next(x for x in cd["objections"] if x["id"] == node)
                    if locus in ("short", "medium", "long"):
                        cont, k2 = o["responses"], locus
                    elif locus.startswith("archetypeVariants."):
                        cont, k2 = o["responses"]["archetypeVariants"], locus.split(".", 1)[1]
                    else:
                        cont, k2 = o, locus
                    assert quote in cont[k2], "the control's corpus quote is not in the pinned corpus"
                    cont[k2] = cont[k2].replace(quote, "[the next pin session's repair]")
                    b = json.dumps(cd, ensure_ascii=False).encode("utf-8")
                open(dst, "wb").write(b)
                if mut_pin and pin["file"].endswith(mut_pin):
                    open(dst, "wb").write(b[:-1] + (b"\n" if b[-1:] != b"\n" else b" "))
            for rel in (doc0["instrument"]["file"], doc0["instrument"]["record"]):
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(REPO, rel), os.path.join(d, rel))
            p = os.path.join(d, REL)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            json.dump(mut_doc if mut_doc is not None else doc0, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            return p, d, json.dumps(base if base is not None else (mut_doc if mut_doc is not None else doc0),
                                    ensure_ascii=False)

        def mut(fn):
            d = copy.deepcopy(doc0); fn(d); return d

        def first(kind, verdict=None, r1=False):
            return next(i for i, r in enumerate(doc0["rows"]) if r["kind"] == kind
                        and (verdict is None or r.get("verdict") == verdict) and (not r1 or r.get("r1")))

        def renumber(d):
            for k, r in enumerate(d["rows"], 1):
                r["id"] = "U-%03d" % k

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        extra = dict(copy.deepcopy(doc0["rows"][first("amend")]), id="U-%03d" % (len(doc0["rows"]) + 1))
        redraft = lambda rd: rd["rows"].append(dict(copy.deepcopy(next(x for x in rd["rows"] if x["kind"] == "amend")),
                                                    id="SM-99", supersedes=next(x for x in rd["rows"] if x["kind"] == "amend")["id"]))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "an amend row goes unjudged",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("amend")), renumber(d)))), 1, "amend rows not judged"),
            ("C2", "an amend row's verdict reads MAYBE",
             dict(mut_doc=mut(lambda d: d["rows"][first("amend")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C3", "an AMEND owes nothing",
             dict(mut_doc=mut(lambda d: d["rows"][first("amend", "AMEND")].update(owed=[]))), 1, "without saying what is owed"),
            ("C4", "a proposed HOLDS goes unanswered",
             dict(mut_doc=mut(lambda d: d["rows"][first("amend", r1=True)].update(r1=None))), 1, "an R1 verdict"),
            ("C5", "a row names a drafts row the record lacks",
             dict(mut_doc=mut(lambda d: d["rows"][first("file")].update(row_id="SM-98"))), 1, "names no current file row"),
            ("C6", "a stands row names the wrong target",
             dict(mut_doc=mut(lambda d: d["rows"][first("stands")].update(target="why-not-suicide#medium"))), 1, "is not SM-"),
            ("C7", "a knock-on row is dropped",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("knock_on")), renumber(d)))), 1, "do not match the reading record"),
            ("C8", "a quoted span is not declared",
             dict(mut_doc=mut(lambda d: d["rows"][first("amend")].update(reason=d["rows"][first("amend")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C9", "a declared quote is one character off",
             dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C10", "map v1_7 moves by one byte", dict(mut_pin="adversarial_map_v1_7.json"), 1, "pin map_v1_7"),
            ("C11", "a committed row is edited in place",
             dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C12", "a correction row supersedes properly",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("amend")]["id"]))), base=doc0), 0, None),
            ("C13", "the drafts record grows by an appended redraft", dict(grow=("L7_successor_drafts.json", redraft)), 0, None),
            ("C14", "a committed drafts row is edited in place",
             dict(grow=("L7_successor_drafts.json", lambda rd: rd["rows"][0].update(why=rd["rows"][0]["why"] + " (edited)"))), 1, "not merely grown by appended rows"),
            ("C15", "the canon is gone (the rename convention)", dict(drop=os.path.basename(doc0["judged"]["canon"]["file"])), 0, None),
            ("C16", "the corpus moves (a later pin): a quoted span is gone", dict(corpus_edit=True), 0, None),
            ("C17", "the same, with git history withheld", dict(corpus_edit=True, _history=lambda rel, want: None), 1, "not in git history"),
            ("C18", "a finding names an entry R1 never ruled",
             dict(mut_doc=mut(lambda d: d["rows"][first("finding")].update(entries=[999]))), 1, "are not R1 entries"),
            ("C19", "an artifact row names a file the header does not judge",
             dict(mut_doc=mut(lambda d: d["rows"][first("artifact")].update(artifact="adversarial_map_staging/adv_map_validator_v0_6.py"))), 1, "is not one the header pins"),
        ]
        history = lambda rel, want: pinned_bytes(REPO, rel, want)
        ok_all = True
        for cid, what, kw, want_rc, want_msg in controls:
            kw = dict(kw); hist = kw.pop("_history", history)
            p, d, base = stage(**kw)
            fails, _ = check(p, d, base, hist)
            rc = 1 if fails else 0
            ok = rc == want_rc and (want_msg is None or any(want_msg in f for f in fails))
            if cid == "C0" and not ok:
                print("C0 (unmutated) is not GREEN: %s" % fails)
                sys.exit(2)
            ok_all &= ok
            results.append({"control": cid, "what": what, "want_rc": want_rc, "want_message": want_msg, "rc": rc,
                            "as_expected": ok, "first_failure": fails[0] if fails else None})
            print("  %-4s %-58s rc %d  %s" % (cid, what, rc, "as expected" if ok else "NOT AS EXPECTED: %s" % fails[:2]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rec = {"artifact": "l7_judgments_gate control record", "gate": "adversarial_map_staging/r1/l7_judgments_gate.py",
           "gate_md5": md5(os.path.abspath(__file__)), "judgments_md5": md5(real),
           "controls": results, "all_as_expected": ok_all}
    if emit:
        open(emit, "w", encoding="utf-8").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    print("SELF-TEST: %d of %d controls as expected" % (sum(r["as_expected"] for r in results), len(results)))
    return 0 if ok_all else 1


def main():
    a = sys.argv[1:]
    if "--self-test" in a:
        emit = a[a.index("--emit") + 1] if "--emit" in a else None
        return self_test(emit)
    fails, info = check(os.path.join(REPO, REL), REPO, committed_base())
    for line in info:
        print("  " + line)
    for f in fails:
        print("FAIL " + f)
    print("L7 JUDGMENTS GATE: %s" % ("GREEN" if not fails else "RED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
