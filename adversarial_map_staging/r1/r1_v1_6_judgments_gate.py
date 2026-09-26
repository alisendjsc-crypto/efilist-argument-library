#!/usr/bin/env python3
"""r1_v1_6_judgments_gate.py -- the gate beside R1_v1_6_judgments.json (gate2, 2026-09-26).

R1_v1_6_judgments.json records gate2's third judgment: #46's (d) in v1_6 (R1_redrafts_v1_6.json),
register v0_7's delta, the knock-on measure (l4c_knock_on_v0_1.json), PQ-17 and the pin session's
declaration (canon v38.28, pin_move_queue_v1_6). It is APPEND-ONLY: a row is never edited or removed,
and a correction is a new row whose `supersedes` names the row it replaces. This gate checks, and
exits 1 on any failure:

  1. rows run W-001, W-002, ... in file order, each with exactly its kind's keys, a seat and a date;
  2. every redraft row names a real redraft, the knock-on row it answers and its disposition; every
     register row names one of register v0_7's declared deltas by index and word for word; the
     measure row's claim is the knock-on record's; every queue row names a row the redrafts file adds
     and the pinned canon's queue holds at the same locus; the declaration row names a path the pinned
     canon holds; findings name an owner and real R1 entries;
  3. verdicts are ACCEPT, AMEND or REJECT (redraft, register, queue row) or CONFIRM or CORRECT
     (measure, declaration); an AMEND, REJECT or CORRECT says what is owed;
  4. coverage: every redraft, every register delta and every queue addition has exactly one current
     judgment, and so do the knock-on measure and the declaration;
  5. every double-quoted span in a row's text is declared in that row's quotes, and every declared
     quote is verbatim at its source, each source read at the bytes this header pins: v1_5:, v1_6:,
     redrafts:#n or redrafts:PQ-nn, rulings:R1-nnn, judgments:V-nnn, register_v0_6:HR-nn,
     register_v0_7:HR-nn, knock_on:record and canon:<dotted.path> (the pinned canon); corpus: by
     r1_quote_check's rule, against the corpus map_v1_6 pins (meta.source_corpus_md5); map: (v1_3) as
     r1_quote_check reads it; design: and render: files in adversarial_map_staging/;
  6. the judged artifacts are at the md5s the header names, with two exceptions. An append-only record
     (R1_rulings.json, R1_v1_5_judgments.json) may have grown by appended rows, its pinned bytes
     recoverable from git history, header unchanged and rows a prefix. A canon file may be gone from
     the working tree, since the rename convention removes it at the next bump, if its pinned bytes are
     in git history. Every judged artifact is read at its pinned bytes; the instrument's record is at
     the md5 the header names;
  7. append-only: the committed base (git HEAD's copy, or --base) is intact: header unchanged, every
     committed row still present, unchanged and in order.

  python3 r1_v1_6_judgments_gate.py                             # base = git HEAD's copy
  python3 r1_v1_6_judgments_gate.py --self-test [--emit <path>]   # controls; unmutated first

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/R1_v1_6_judgments.json"
STG = "adversarial_map_staging"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "his_word", "kickoff", "judged", "instrument",
               "rows"]
PINS = ["map_v1_6", "map_v1_5", "redrafts", "register_v0_7", "register_v0_6", "rulings", "judgments_v1_5",
        "knock_on", "canon"]
COMMON = {"id", "kind", "quotes", "seat", "date", "supersedes"}
KEYS = {
    "redraft": COMMON | {"n", "answers", "disposition", "verdict", "reason", "owed", "carries"},
    "register": COMMON | {"delta_index", "delta", "verdict", "reason", "owed", "carries"},
    "measure": COMMON | {"measure", "claim", "verdict", "reason", "owed", "carries"},
    "queue_row": COMMON | {"row_id", "locus", "verdict", "reason", "owed", "carries"},
    "declaration": COMMON | {"at", "verdict", "reason", "owed", "carries"},
    "finding": COMMON | {"title", "finding", "recommendation", "whose", "entries"},
}
VERDICTS = {"redraft": ("ACCEPT", "AMEND", "REJECT"), "register": ("ACCEPT", "AMEND", "REJECT"),
            "queue_row": ("ACCEPT", "AMEND", "REJECT"), "measure": ("CONFIRM", "CORRECT"),
            "declaration": ("CONFIRM", "CORRECT")}
OWES = {"AMEND", "REJECT", "CORRECT"}
TEXT_FIELDS = {k: ("reason", "owed", "carries") for k in VERDICTS}
TEXT_FIELDS["finding"] = ("finding", "recommendation")
SPAN = re.compile(r'"([^"]+)"')
APPEND_ONLY = {"adversarial_map_staging/r1/R1_rulings.json", "adversarial_map_staging/r1/R1_v1_5_judgments.json"}
RENAMED = re.compile(r"project_canon_v38_\d+\.json")

_spec = importlib.util.spec_from_file_location("r1qc", os.path.join(HERE, "r1_quote_check.py"))
Q = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Q)


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


def corpus_text(corpus, rest):
    """r1_quote_check's corpus: rule, read against a pinned corpus."""
    node, _, locus = rest.partition("#")
    if node not in corpus:
        raise KeyError("no corpus node %s" % node)
    o = corpus[node]
    if locus in ("short", "medium", "long"):
        t = o["responses"].get(locus)
    elif locus.startswith("archetypeVariants."):
        t = o["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    else:
        t = o.get(locus)
    if not isinstance(t, str):
        raise KeyError("no corpus text at %s" % rest)
    return [t]


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


class Sources:
    """Every source resolves against the bytes the header pins, except map: (v1_3, never edited)."""

    def __init__(self, repo_dir, doc, history=None):
        self.repo = repo_dir
        self.q = Q.Texts()
        j = doc["judged"]

        def at(key):
            b = pinned_bytes(repo_dir, j[key]["file"], j[key]["md5"], history)
            if b is None:  # rule 6 reports it; read what is there so the other checks still run
                p = os.path.join(repo_dir, j[key]["file"])
                b = open(p, "rb").read() if os.path.exists(p) else b"{}"
            return json.loads(b.decode("utf-8"))

        m16 = at("map_v1_6")
        self.maps = {"v1_5": at("map_v1_5").get("entries", []), "v1_6": m16.get("entries", [])}
        self.redrafts = at("redrafts")
        self.rulings = at("rulings").get("rows", [])
        self.judgments = at("judgments_v1_5").get("rows", [])
        reg = {k: at(k) for k in ("register_v0_6", "register_v0_7")}
        self.regs = {k: {b["bedrock_id"]: b for b in v.get("bedrocks", [])} for k, v in reg.items()}
        self.deltas = reg["register_v0_7"].get("meta", {}).get("changes_from_v0_6", [])
        self.knock = at("knock_on")
        self.canon = at("canon")
        meta = m16.get("meta", {})
        self.corpus_pin = (meta.get("source_corpus", ""), meta.get("source_corpus_md5", ""))
        cb = pinned_bytes(repo_dir, self.corpus_pin[0], self.corpus_pin[1], history) if self.corpus_pin[1] else None
        self.corpus = None if cb is None else {o["id"]: o for o in json.loads(cb.decode("utf-8"))["objections"]}

    def resolve(self, src):
        kind, _, rest = src.partition(":")
        if kind in self.maps:
            node, _, locus = rest.partition("#")
            xs = [x for x in self.maps[kind] if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no %s entry at %s" % (kind, rest))
            return [s for x in xs for s in strings(x)]
        if kind == "redrafts":
            if rest.startswith("PQ-"):
                xs = [x for x in self.redrafts.get("pin_move_queue_additions", []) if x["id"] == rest]
            else:
                xs = [x for x in self.redrafts.get("redrafts", []) if "#%d" % x["n"] == rest]
            if not xs:
                raise KeyError("no redraft %s" % rest)
            return list(strings(xs[0]))
        if kind in ("rulings", "judgments"):
            pool, k = (self.rulings, "row") if kind == "rulings" else (self.judgments, "id")
            xs = [r for r in pool if r[k] == rest]
            if not xs:
                raise KeyError("no %s row %s" % (kind, rest))
            return list(strings(xs[0]))
        if kind in self.regs:
            if rest not in self.regs[kind]:
                raise KeyError("no bedrock %s in %s" % (rest, kind))
            return list(strings(self.regs[kind][rest]))
        if kind == "knock_on":
            return list(strings(self.knock))
        if kind == "canon":
            try:
                return list(strings(walk(self.canon, rest)))
            except (KeyError, TypeError):
                raise KeyError("no path %s in the pinned canon" % rest)
        if kind == "corpus":
            if self.corpus is None:
                raise KeyError("the corpus the judged map pins (%s) is not recoverable" % self.corpus_pin[1][:8])
            return corpus_text(self.corpus, rest)
        if kind in ("design", "render"):
            pat = r"adversarial_map_design_v0_\d+\.md" if kind == "design" else r"render_[a-z0-9_]+\.py"
            if not re.fullmatch(pat, rest):
                raise KeyError("%s source must name %s, got %r" % (kind, pat, rest))
            p = os.path.join(self.repo, STG, rest)
            if not os.path.exists(p):
                raise KeyError("no file %s" % rest)
            return [open(p, encoding="utf-8").read()]
        if kind == "map":
            return self.q.resolve(src)
        raise KeyError("unknown source kind %r" % kind)


def subject(r):
    k = r.get("kind")
    return {"redraft": "redraft #%s" % r.get("n"), "register": "register delta %s" % r.get("delta_index"),
            "measure": "measure %s" % r.get("measure"), "queue_row": "queue row %s" % r.get("row_id"),
            "declaration": "declaration", "finding": "finding %s" % r.get("title")}.get(k, "?")


def texts_of(r):
    out = []
    for f in TEXT_FIELDS.get(r["kind"], ()):
        v = r.get(f)
        out += v if isinstance(v, list) else [v]
    return [t for t in out if isinstance(t, str)]


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

    # 6 -- the referents have not moved; an append-only one may have grown; a renamed canon may be gone
    for name, pin in doc["judged"].items():
        p = os.path.join(repo_dir, pin["file"])
        got = md5(p) if os.path.exists(p) else "MISSING"
        if got == pin["md5"]:
            continue
        base = pinned_bytes(repo_dir, pin["file"], pin["md5"], history)
        if got == "MISSING" and RENAMED.fullmatch(os.path.basename(pin["file"])):
            if base is None:
                fails.append("pin %s: %s is gone and its pinned bytes are not in git history" % (name, pin["file"]))
            else:
                info.append("pin %s: %s is gone from the tree (the rename convention); read from history at %s"
                            % (name, pin["file"], pin["md5"][:8]))
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
    redrafts = {x["n"]: x for x in src.redrafts.get("redrafts", [])}
    additions = {x["id"]: x for x in src.redrafts.get("pin_move_queue_additions", [])}
    try:
        queue = {r["id"]: r for r in walk(src.canon, "adversarial_map.pin_move_queue_v1_6")["rows"]}
    except (KeyError, TypeError):
        queue = {}
    ruled_ns = {r["n"] for r in src.rulings}

    chains, current = {}, {}
    for i, r in enumerate(rows, 1):
        rid = r.get("id", "?")
        kind = r.get("kind")
        if kind not in KEYS:
            fails.append("%s: kind %r" % (rid, kind))
            continue
        if set(r) != KEYS[kind]:
            fails.append("%s: keys differ from the %s schema (%s)" % (rid, kind, sorted(set(r) ^ KEYS[kind])))
            continue
        # 1
        if rid != "W-%03d" % i:
            fails.append("%s: ids must run W-001, W-002, ... in file order (expected W-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2
        if kind == "redraft":
            x = redrafts.get(r["n"])
            if x is None:
                fails.append("%s: n=%s names no redraft" % (rid, r["n"]))
            elif (r["answers"], r["disposition"]) != (x.get("knock_on_row"), x.get("disposition")):
                fails.append("%s: answers/disposition %s/%s != the redraft's %s/%s"
                             % (rid, r["answers"], r["disposition"], x.get("knock_on_row"), x.get("disposition")))
        if kind == "register":
            k = r["delta_index"]
            if not (isinstance(k, int) and 0 <= k < len(src.deltas)) or r["delta"] != src.deltas[k]:
                fails.append("%s: delta %r is not register v0_7's declared delta %r" % (rid, str(r["delta"])[:50], k))
        if kind == "measure":
            want = {"holds_newly_collided": src.knock.get("holds_newly_collided"),
                    "a_entries_left_in_v1_6": src.knock.get("a_entries_left_in_v1_6")}
            if r["measure"] != "knock_on" or r["claim"] != want:
                fails.append("%s: the claim is not the knock-on record's %s" % (rid, json.dumps(want)))
        if kind == "queue_row":
            if r["row_id"] not in additions:
                fails.append("%s: %s is not a row the redrafts file adds to the queue" % (rid, r["row_id"]))
            elif r["row_id"] not in queue or queue[r["row_id"]].get("locus") != r["locus"] \
                    or additions[r["row_id"]].get("locus") != r["locus"]:
                fails.append("%s: %s at %s is not in the pinned canon's queue at that locus" % (rid, r["row_id"], r["locus"]))
        if kind == "declaration":
            try:
                walk(src.canon, r["at"])
            except (KeyError, TypeError):
                fails.append("%s: %s is not a path in the pinned canon" % (rid, r["at"]))
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
        current[subj] = r

    for want, label in ((["redraft #%d" % n for n in sorted(redrafts)], "redrafts"),
                        (["register delta %d" % k for k in range(len(src.deltas))], "register deltas"),
                        (["queue row %s" % x for x in sorted(additions)], "queue additions"),
                        (["measure knock_on"], "the knock-on measure"), (["declaration"], "the declaration")):
        missing = [s for s in want if s not in current]
        if missing:
            fails.append("coverage: %s not judged: %s" % (label, ", ".join(missing)))

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
    for r in current.values():
        if r["kind"] in VERDICTS:
            tally.setdefault(r["kind"], {}).setdefault(r["verdict"], 0)
            tally[r["kind"]][r["verdict"]] += 1
    info.append("rows %d | %s | findings %d | quotes %d" % (
        len(rows), " | ".join("%s: %s" % (k, ", ".join("%s %d" % kv for kv in sorted(v.items())))
                             for k, v in sorted(tally.items())),
        sum(1 for r in current.values() if r["kind"] == "finding"), sum(len(r["quotes"]) for r in rows)))
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
    tmp = tempfile.mkdtemp(prefix="r1v16gate_")
    results = []
    try:
        def stage(mut_doc=None, mut_pin=None, base=None, grow=None, drop=None, corpus_edit=False):
            # every judged artifact is staged at its pinned bytes; `grow` = (file suffix, fn) rewrites an
            # append-only record from its pinned document; `drop` leaves a file out of the staged tree
            d = os.path.join(tmp, "c%d" % len(results))
            for pin in doc0["judged"].values():
                if drop and pin["file"].endswith(drop):
                    continue
                dst = os.path.join(d, pin["file"])
                os.makedirs(os.path.dirname(dst) or d, exist_ok=True)
                b = pinned_bytes(REPO, pin["file"], pin["md5"])
                if grow and pin["file"].endswith(grow[0]):
                    rd = json.loads(b.decode("utf-8")); grow[1](rd)
                    b = json.dumps(rd, ensure_ascii=False).encode("utf-8")
                open(dst, "wb").write(b)
                if mut_pin and pin["file"].endswith(mut_pin):
                    open(dst, "wb").write(b[:-1] + (b"\n" if b[-1:] != b"\n" else b" "))
            for rel in (doc0["instrument"]["file"], doc0["instrument"]["record"]):
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(REPO, rel), os.path.join(d, rel))
            if corpus_edit:
                # a simulated pin move: the working corpus no longer carries the record's first corpus quote
                pm = doc0["judged"]["map_v1_6"]
                m = json.loads(pinned_bytes(REPO, pm["file"], pm["md5"]).decode("utf-8"))["meta"]
                cd = json.loads(pinned_bytes(REPO, m["source_corpus"], m["source_corpus_md5"]).decode("utf-8"))
                src, quote = next((q["src"], q["quote"]) for r in doc0["rows"] for q in r["quotes"]
                                  if q["src"].startswith("corpus:"))
                node, _, locus = src.split(":", 1)[1].partition("#")
                o = next(x for x in cd["objections"] if x["id"] == node)
                if locus in ("short", "medium", "long"):
                    cont, key = o["responses"], locus
                elif locus.startswith("archetypeVariants."):
                    cont, key = o["responses"]["archetypeVariants"], locus.split(".", 1)[1]
                else:
                    cont, key = o, locus
                assert quote in cont[key], "the control's corpus quote is not in the pinned corpus"
                cont[key] = cont[key].replace(quote, "[the declared pin session's repair]")
                open(os.path.join(d, m["source_corpus"]), "w", encoding="utf-8").write(json.dumps(cd, ensure_ascii=False))
            for name in os.listdir(os.path.join(REPO, STG)):
                if re.fullmatch(r"adversarial_map_design_v0_\d+\.md|render_[a-z0-9_]+\.py", name):
                    shutil.copyfile(os.path.join(REPO, STG, name), os.path.join(d, STG, name))
            p = os.path.join(d, REL)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            json.dump(mut_doc if mut_doc is not None else doc0, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            return p, d, json.dumps(base if base is not None else (mut_doc if mut_doc is not None else doc0),
                                    ensure_ascii=False)

        def mut(fn):
            d = copy.deepcopy(doc0); fn(d); return d

        def first(kind, verdict=None):
            return next(i for i, r in enumerate(doc0["rows"]) if r["kind"] == kind
                        and (verdict is None or r.get("verdict") == verdict))

        def renumber(d):
            for k, r in enumerate(d["rows"], 1):
                r["id"] = "W-%03d" % k

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        extra = dict(copy.deepcopy(doc0["rows"][first("redraft")]), id="W-%03d" % (len(doc0["rows"]) + 1))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "the redraft goes unjudged",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("redraft")), renumber(d)))), 1, "redrafts not judged"),
            ("C2", "the queue row reads MAYBE",
             dict(mut_doc=mut(lambda d: d["rows"][first("queue_row")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C3", "an AMEND owes nothing",
             dict(mut_doc=mut(lambda d: d["rows"][first("queue_row")].update(verdict="AMEND", owed=[]))), 1, "without saying what is owed"),
            ("C4", "a register row misquotes its delta",
             dict(mut_doc=mut(lambda d: d["rows"][first("register")].update(delta=d["rows"][first("register")]["delta"] + "x"))), 1, "declared delta"),
            ("C5", "the measure's claim is not the record's",
             dict(mut_doc=mut(lambda d: d["rows"][first("measure")]["claim"].update(a_entries_left_in_v1_6=30))), 1, "knock-on record"),
            ("C6", "a queue row names a row the queue lacks",
             dict(mut_doc=mut(lambda d: d["rows"][first("queue_row")].update(row_id="PQ-99"))), 1, "not a row the redrafts file adds"),
            ("C7", "a quoted span is not declared",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(reason=d["rows"][first("redraft")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C8", "a declared quote is one character off",
             dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C9", "map v1_6 moves by one byte", dict(mut_pin="adversarial_map_v1_6.json"), 1, "pin map_v1_6"),
            ("C10", "a committed row is edited in place",
             dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C11", "a correction row supersedes properly",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("redraft")]["id"]))), base=doc0), 0, None),
            ("C12", "the rulings file grows by one appended row",
             dict(grow=("R1_rulings.json", lambda rd: rd["rows"].append(dict(rd["rows"][-1], row="R1-%03d" % (len(rd["rows"]) + 1))))), 0, None),
            ("C13", "a committed rulings row is edited in place",
             dict(grow=("R1_rulings.json", lambda rd: rd["rows"][0].update(reason=rd["rows"][0]["reason"] + " (edited)"))), 1, "not merely grown by appended rows"),
            ("C14", "the canon is gone (the rename convention)", dict(drop="project_canon_v38_28.json"), 0, None),
            ("C15", "the canon is edited in place", dict(mut_pin="project_canon_v38_28.json"), 1, "pin canon"),
            ("C16", "a simulated pin: a quoted corpus span is gone", dict(corpus_edit=True), 0, None),
            ("C17", "the same, with git history withheld", dict(corpus_edit=True, _history=lambda rel, want: None), 1, "is not recoverable"),
        ]
        # the staged tree has no git; history resolves against this repo's own, as the real run does
        history = lambda rel, want: pinned_bytes(REPO, rel, want)
        ok_all = True
        for cid, what, kw, want_rc, want_msg in controls:
            kw = dict(kw); hist = kw.pop("_history", history)
            p, d, base = stage(**kw)
            fails, _ = check(p, d, base, hist)
            rc = 1 if fails else 0
            matched = (want_msg is None and not fails) or (want_msg is not None and any(want_msg in f for f in fails))
            good = rc == want_rc and matched
            if cid == "C0" and not good:
                for f in fails:
                    print("   ", f)
                print("C0 (unmutated) is not GREEN -- no mutation result below could mean anything")
                return 1
            ok_all &= good
            results.append({"control": cid, "mutation": what, "expected_rc": want_rc, "expected_message": want_msg,
                            "rc": rc, "as_expected": good, "failure_lines": [f.replace(tmp, "<tmp>") for f in fails[:3]]})
            print("%-4s %-44s rc=%d %s" % (cid, what, rc, "as expected" if good else "UNEXPECTED: %s" % fails))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELF-TEST: %d of %d controls as expected" % (sum(r["as_expected"] for r in results), len(results)))
    if emit:
        rec = {"artifact": os.path.basename(emit), "gate": "adversarial_map_staging/r1/r1_v1_6_judgments_gate.py",
               "gate_md5": md5(os.path.abspath(__file__)), "judgments_md5": md5(real),
               "rule": "C0, the unmutated control, runs first and must be GREEN; each mutation must go RED with its "
                       "own failure line; C11 (a proper correction row), C12 (the rulings grown by an appended row), "
                       "C14 (the canon gone by the rename convention) and C16 (a simulated pin move) must stay GREEN.",
               "controls": results}
        open(emit, "w", encoding="utf-8").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    return 0 if ok_all else 1


def main():
    if "--self-test" in sys.argv:
        emit = sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None
        sys.exit(self_test(emit))
    base_text = committed_base()
    if "--base" in sys.argv:
        base_text = open(sys.argv[sys.argv.index("--base") + 1], encoding="utf-8").read()
    fails, info = check(os.path.join(REPO, REL), REPO, base_text)
    for line in info:
        print("  " + line)
    for line in fails:
        print("  FAIL " + line)
    print("R1 v1_6 JUDGMENTS GATE: %s" % ("GREEN" if not fails else "RED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
