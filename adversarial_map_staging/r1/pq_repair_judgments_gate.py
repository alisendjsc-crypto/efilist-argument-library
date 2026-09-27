#!/usr/bin/env python3
"""pq_repair_judgments_gate.py -- the gate beside PQ_repair_drafts_judgments.json (gate2, 2026-09-26, R0175).

PQ_repair_drafts_judgments.json records gate2's fourth judgment: the declared pin session's drafted repairs for
pin_move_queue_L5 (PQ_repair_drafts_L5.json: 18 drafts, 5 proposed companions, 7 findings) and its knock-on
record. It is APPEND-ONLY: a row is never edited or removed, and a correction is a new row whose `supersedes`
names the row it replaces. This gate checks, and exits 1 on any failure:

  1. rows run X-001, X-002, ... in file order, each with exactly its kind's keys, a seat and a date;
  2. every draft, companion and finding_review row names a current row of that kind in the drafts record, read
     at the bytes this header pins, and a draft or companion row names that row's locus; the knock_on row's
     claim is the knock-on record's own figures and the reading record's independent ones, which must match the
     record's sets; every finding names an owner and real R1 entries;
  3. verdicts are ACCEPT, AMEND or REJECT (draft, companion) or CONFIRM or CORRECT (finding_review, knock_on);
     an AMEND, REJECT or CORRECT says what is owed; a companion's lean is 'admit' or 'do not admit';
  4. coverage: every current draft, companion and finding of the pinned drafts record has exactly one current
     judgment, and so does the knock-on;
  5. every double-quoted span in a row's text is declared in that row's quotes, and every declared quote is
     verbatim at its source, each source read at the bytes this header pins: drafts:<row id>, corpus:<node#locus>
     (the corpus the drafts record pins, by r1_quote_check's locus rule), v1_6:<node#locus>, rulings:R1-nnn,
     canon:<dotted.path>, knock_on:record and reading:record;
  6. the judged artifacts are at the md5s the header names, with two exceptions. An append-only record (the drafts
     record, R1_rulings.json) may have grown by appended rows, its pinned bytes recoverable from git history,
     header unchanged and rows a prefix. The canon may be gone from the working tree (the rename convention
     removes it at the next bump) if its pinned bytes are in git history. Every artifact is read at its pinned
     bytes, the corpus included, so the pin move cannot turn a true row RED; the instrument's record is at the
     md5 the header names;
  7. append-only: the committed base (git HEAD's copy) is intact: header unchanged, every committed row still
     present, unchanged and in order.

  python3 pq_repair_judgments_gate.py                             # base = git HEAD's copy
  python3 pq_repair_judgments_gate.py --self-test [--emit <path>]   # controls; unmutated first

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/PQ_repair_drafts_judgments.json"
CORPUS = "efilist_argument_library_v4_0_0.json"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "his_word", "kickoff", "judged", "instrument",
               "rows"]
PINS = ["drafts", "drafts_gate", "drafts_gate_control", "knock_on", "patch_tool", "map_v1_6", "rulings", "canon"]
COMMON = ["id", "kind", "quotes", "seat", "date", "supersedes"]
KEYS = {
    "draft": ["id", "kind", "row_id", "locus", "verdict", "reason", "owed", "carries", "quotes", "seat", "date",
              "supersedes"],
    "companion": ["id", "kind", "row_id", "locus", "verdict", "lean", "reason", "owed", "carries", "quotes", "seat",
                  "date", "supersedes"],
    "finding_review": ["id", "kind", "row_id", "verdict", "reason", "owed", "carries", "quotes", "seat", "date",
                       "supersedes"],
    "knock_on": ["id", "kind", "claim", "verdict", "reason", "owed", "carries", "quotes", "seat", "date", "supersedes"],
    "finding": ["id", "kind", "title", "finding", "recommendation", "whose", "entries", "quotes", "seat", "date",
                "supersedes"],
}
DRAFT_KIND = {"draft": "draft", "companion": "companion", "finding_review": "finding"}
VERDICTS = {"draft": ("ACCEPT", "AMEND", "REJECT"), "companion": ("ACCEPT", "AMEND", "REJECT"),
            "finding_review": ("CONFIRM", "CORRECT"), "knock_on": ("CONFIRM", "CORRECT")}
LEANS = ("admit", "do not admit")
OWES = {"AMEND", "REJECT", "CORRECT"}
TEXT_FIELDS = {k: ("reason", "owed", "carries") for k in VERDICTS}
TEXT_FIELDS["finding"] = ("finding", "recommendation")
SPAN = re.compile(r'"([^"]+)"')
APPEND_ONLY = {"adversarial_map_staging/r1/PQ_repair_drafts_L5.json", "adversarial_map_staging/r1/R1_rulings.json"}
RENAMED = re.compile(r"project_canon_v38_\d+\.json")


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
    """r1_quote_check's corpus: rule, read against the pinned corpus."""
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


def current(rows, key="id"):
    sup = {r.get("supersedes") for r in rows if r.get("supersedes")}
    return [r for r in rows if r[key] not in sup]


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
        self.map = at("map_v1_6").get("entries", [])
        self.rulings = at("rulings").get("rows", [])
        self.knock = at("knock_on")
        self.canon = at("canon")
        ip = os.path.join(repo_dir, doc["instrument"]["record"])
        self.reading = json.load(open(ip, encoding="utf-8")) if os.path.exists(ip) else {}
        cpin = self.drafts.get("pinned", {}).get("surfaces", {}).get(CORPUS)
        cb = pinned_bytes(repo_dir, CORPUS, cpin, history) if cpin else None
        self.corpus_pin = cpin or ""
        self.corpus = None if cb is None else {o["id"]: o for o in json.loads(cb.decode("utf-8"))["objections"]}

    def resolve(self, src):
        kind, _, rest = src.partition(":")
        if kind == "drafts":
            xs = [r for r in self.drafts.get("rows", []) if r.get("id") == rest]
            if not xs:
                raise KeyError("no drafts row %s" % rest)
            return list(strings(xs[0]))
        if kind == "corpus":
            if self.corpus is None:
                raise KeyError("the corpus the drafts record pins (%s) is not recoverable" % self.corpus_pin[:8])
            return corpus_text(self.corpus, rest)
        if kind == "v1_6":
            node, _, locus = rest.partition("#")
            xs = [x for x in self.map if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no v1_6 entry at %s" % rest)
            return [s for x in xs for s in strings(x)]
        if kind == "rulings":
            xs = [r for r in self.rulings if r.get("row") == rest]
            if not xs:
                raise KeyError("no rulings row %s" % rest)
            return list(strings(xs[0]))
        if kind == "canon":
            try:
                return list(strings(walk(self.canon, rest)))
            except (KeyError, TypeError):
                raise KeyError("no path %s in the pinned canon" % rest)
        if kind == "knock_on" and rest == "record":
            return list(strings(self.knock))
        if kind == "reading" and rest == "record":
            return list(strings(self.reading))
        raise KeyError("unknown source %r" % src)


def texts_of(r):
    out = []
    for f in TEXT_FIELDS.get(r["kind"], ()):
        v = r.get(f)
        out += v if isinstance(v, list) else [v]
    return [t for t in out if isinstance(t, str)]


def subject(r):
    if r["kind"] in DRAFT_KIND:
        return "%s %s" % (r["kind"], r.get("row_id"))
    if r["kind"] == "knock_on":
        return "knock_on"
    return "finding %s" % r.get("title")


def knock_figures(knock):
    rows = knock.get("rows", [])
    routes = [r for r in rows if r.get("kind") == "answer_routes_here"]
    return {"anchor_inside": sum(1 for r in rows if r.get("kind") == "anchor_inside"),
            "answer_routes_here": len(routes),
            "holds": sorted({r["n"] for r in routes if r.get("verdict") == "HOLDS"}),
            "waiting_fails": sorted({r["n"] for r in routes if r.get("verdict") == "FAILS"})}


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
    if src.corpus is None:
        fails.append("pin corpus: the corpus the drafts record pins (%s) is not recoverable" % src.corpus_pin[:8])
    dcur = {r["id"]: r for r in current(src.drafts.get("rows", []))}
    ruled_ns = {r["n"] for r in src.rulings}
    kf = knock_figures(src.knock)
    ko = src.reading.get("knock_on_independent", {})

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
        if rid != "X-%03d" % i:
            fails.append("%s: ids must run X-001, X-002, ... in file order (expected X-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2
        if kind in DRAFT_KIND:
            x = dcur.get(r["row_id"])
            if x is None or x.get("kind") != DRAFT_KIND[kind]:
                fails.append("%s: %s names no current %s row of the drafts record" % (rid, r["row_id"], DRAFT_KIND[kind]))
            elif kind != "finding_review" and r["locus"] != x.get("locus"):
                fails.append("%s: locus %s is not %s's locus %s" % (rid, r["locus"], r["row_id"], x.get("locus")))
        if kind == "knock_on":
            if r["claim"] != kf:
                fails.append("%s: the claim is not the knock-on record's figures %s" % (rid, json.dumps(kf)))
            indep = {"anchor_inside": ko.get("anchor_inside"), "answer_routes_here": ko.get("answer_routes_here"),
                     "holds": ko.get("holds"), "waiting_fails": ko.get("fails")}
            if r["claim"] != indep or not (ko.get("anchor_inside_matches_record") and ko.get("answer_routes_here_matches_record")):
                fails.append("%s: the reading record does not reproduce the claim or the record's sets" % rid)
        if kind == "companion" and r["lean"] not in LEANS:
            fails.append("%s: lean %r is not one of %s" % (rid, r["lean"], "/".join(LEANS)))
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

    for dk, jk in (("draft", "draft"), ("companion", "companion"), ("finding", "finding_review")):
        want = ["%s %s" % (jk, x["id"]) for x in dcur.values() if x.get("kind") == dk]
        missing = [s for s in want if s not in cur]
        if missing:
            fails.append("coverage: %s not judged: %s" % (dk, ", ".join(missing)))
    if "knock_on" not in cur:
        fails.append("coverage: the knock-on not judged")

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
            tally.setdefault(r["kind"], {}).setdefault(r["verdict"], 0)
            tally[r["kind"]][r["verdict"]] += 1
    info.append("rows %d | %s | findings %d | quotes %d" % (
        len(rows), " | ".join("%s: %s" % (k, ", ".join("%s %d" % kv for kv in sorted(v.items())))
                             for k, v in sorted(tally.items())),
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
    tmp = tempfile.mkdtemp(prefix="pqjgate_")
    results = []
    try:
        drafts_pin = doc0["judged"]["drafts"]
        corpus_md5 = json.loads(pinned_bytes(REPO, drafts_pin["file"], drafts_pin["md5"]).decode("utf-8"))["pinned"]["surfaces"][CORPUS]

        def stage(mut_doc=None, mut_pin=None, base=None, grow=None, drop=None, corpus_edit=False):
            # every judged artifact at its pinned bytes, the pinned corpus, and the instrument; `grow` = (file
            # suffix, fn) rewrites an append-only record from its pinned document; `drop` leaves a file out
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
            cb = pinned_bytes(REPO, CORPUS, corpus_md5)
            if corpus_edit:
                # a simulated pin move: the working corpus no longer carries the record's first corpus quote
                cd = json.loads(cb.decode("utf-8"))
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
                cb = json.dumps(cd, ensure_ascii=False).encode("utf-8")
            open(os.path.join(d, CORPUS), "wb").write(cb)
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

        def first(kind, verdict=None):
            return next(i for i, r in enumerate(doc0["rows"]) if r["kind"] == kind
                        and (verdict is None or r.get("verdict") == verdict))

        def renumber(d):
            for k, r in enumerate(d["rows"], 1):
                r["id"] = "X-%03d" % k

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        extra = dict(copy.deepcopy(doc0["rows"][first("draft")]), id="X-%03d" % (len(doc0["rows"]) + 1))
        ratified = lambda rd: rd["rows"].append(dict(copy.deepcopy(next(x for x in rd["rows"] if x["kind"] == "draft")),
                                                     id="PR-01", status="ratified (a control's row)",
                                                     supersedes=next(x for x in rd["rows"] if x["kind"] == "draft")["id"]))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "a draft goes unjudged",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("draft")), renumber(d)))), 1, "draft not judged"),
            ("C2", "a draft's verdict reads MAYBE",
             dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C3", "an AMEND owes nothing",
             dict(mut_doc=mut(lambda d: d["rows"][first("draft", "AMEND")].update(owed=[]))), 1, "without saying what is owed"),
            ("C4", "a companion's lean is not a lean",
             dict(mut_doc=mut(lambda d: d["rows"][first("companion")].update(lean="maybe"))), 1, "lean"),
            ("C5", "a row names a draft the record lacks",
             dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(row_id="PD-99"))), 1, "names no current draft row"),
            ("C6", "a draft row names the wrong locus",
             dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(locus="just-depressed#medium"))), 1, "is not PD-"),
            ("C7", "the knock-on claim is not the record's",
             dict(mut_doc=mut(lambda d: d["rows"][first("knock_on")]["claim"].update(anchor_inside=14))), 1, "knock-on record's figures"),
            ("C8", "a quoted span is not declared",
             dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(reason=d["rows"][first("draft")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C9", "a declared quote is one character off",
             dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C10", "map v1_6 moves by one byte", dict(mut_pin="adversarial_map_v1_6.json"), 1, "pin map_v1_6"),
            ("C11", "a committed row is edited in place",
             dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C12", "a correction row supersedes properly",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("draft")]["id"]))), base=doc0), 0, None),
            ("C13", "the drafts record grows by an appended ratified row", dict(grow=("PQ_repair_drafts_L5.json", ratified)), 0, None),
            ("C14", "a committed drafts row is edited in place",
             dict(grow=("PQ_repair_drafts_L5.json", lambda rd: rd["rows"][0].update(how=rd["rows"][0]["how"] + " (edited)"))), 1, "not merely grown by appended rows"),
            ("C15", "the canon is gone (the rename convention)", dict(drop="project_canon_v38_31.json"), 0, None),
            ("C16", "a simulated pin: a quoted corpus span is gone", dict(corpus_edit=True), 0, None),
            ("C17", "the same, with git history withheld", dict(corpus_edit=True, _history=lambda rel, want: None), 1, "not recoverable"),
            ("C18", "a finding names an entry R1 never ruled",
             dict(mut_doc=mut(lambda d: d["rows"][first("finding")].update(entries=[999]))), 1, "are not R1 entries"),
        ]
        # the staged tree has no git; history resolves against this repo's own, as the real run does
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
    rec = {"artifact": "pq_repair_judgments_gate control record", "gate": REL.replace("PQ_repair_drafts_judgments.json", "pq_repair_judgments_gate.py"),
           "gate_md5": md5(os.path.abspath(__file__)), "judgments_md5": md5(real),
           "controls": results, "all_as_expected": ok_all}
    if emit:
        open(emit, "w", encoding="utf-8").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    print("SELF-TEST: %d of %d controls as expected" % (sum(r["as_expected"] for r in results), len(results)))
    return 0 if ok_all else 1


def main():
    if "--self-test" in sys.argv:
        emit = sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None
        sys.exit(self_test(emit))
    fails, info = check(os.path.join(REPO, REL), REPO, committed_base())
    for line in info:
        print("  " + line)
    for f in fails:
        print("  FAIL " + f)
    print("PQ REPAIR JUDGMENTS GATE: %s" % ("GREEN" if not fails else "RED (%d)" % len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
