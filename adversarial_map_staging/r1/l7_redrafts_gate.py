#!/usr/bin/env python3
"""l7_redrafts_gate.py -- the gate beside L7_successor_redrafts_judgments.json (gate2, 2026-09-26, R0245).

L7_successor_redrafts_judgments.json records gate2's second judgment of L7's successor map: the rows L7 appended to
L7_successor_drafts.json after gate2's first judgment (L7_successor_drafts_judgments.json), map v1_8, register v0_9, the
knock-on control, the controls_v1_7 change, the U-065 route and the (a)s whose collisions changed by class. APPEND-ONLY.
Adapted from l7_judgments_gate.py and sp_redrafts_gate.py. It checks, and exits 1 on any failure:

  1. rows run U2-001, U2-002, ... in file order, each with exactly its kind's keys, a seat and a date;
  2. every redraft row names a current row of the drafts record (read at the bytes this header pins) that the record did
     NOT hold at the bytes the first judgment read; that row supersedes the row the redraft row says it replaces; the first
     judgment's row it answers AMENDs that replaced row; and the target is the replaced row's; an artifact row names map
     v1_8 or register v0_9; the measure row's CONFIRM agrees with the reading record (its count by entry and class equals
     the control's); the tool row names controls_v1_7.py and its CONFIRM agrees with the reading record's pins; the route
     row is U-065's; the knock_on rows are exactly the reading record's class changes at entries already met; findings
     name an owner and R1 entries only;
  3. verdicts: ACCEPT, AMEND or REJECT (redraft); CONFIRM or CORRECT (artifact, measure, tool, route); STANDS or REOPENS
     (knock_on); every AMEND, REJECT, CORRECT and REOPENS says what is owed;
  4. coverage: every such new current row has exactly one current judgment, and so do both artifacts, the measure, the
     tool, the route and every class change;
  5. every double-quoted span in a row's text is declared and verbatim at its source, read at the pinned bytes:
     drafts:<row id>, judgment:U-nnn, corpus:<node#locus>, v1_8:<node#locus>, canon:<dotted.path> and reading:record;
  6. the judged artifacts are at the md5s the header names, except, each read at its pinned bytes from git history: an
     append-only record (the drafts record, the first judgment, R1_rulings.json) may have grown by appended rows; the canon
     may be gone (the rename convention); the corpus may have moved (a pin session moves it);
  7. append-only against git HEAD's copy.

  python3 l7_redrafts_gate.py                             # base = git HEAD's copy
  python3 l7_redrafts_gate.py --self-test [--emit <path>]   # controls; unmutated first

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/L7_successor_redrafts_judgments.json"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "his_word", "kickoff", "judged", "instrument", "rows"]
PINS = ["drafts", "first_judgment", "map_v1_7", "map_v1_8", "register_v0_8", "register_v0_9", "knock_on_record",
        "controls_v1_7_record", "corpus", "rulings", "canon"]
TAIL = ["quotes", "seat", "date", "supersedes"]
KEYS = {
    "redraft": ["id", "kind", "row_id", "replaces", "answers", "target", "verdict", "reason", "owed", "carries"] + TAIL,
    "artifact": ["id", "kind", "artifact", "verdict", "reason", "owed", "carries"] + TAIL,
    "measure": ["id", "kind", "measure", "verdict", "reason", "owed", "carries"] + TAIL,
    "tool": ["id", "kind", "tool", "verdict", "reason", "owed", "carries"] + TAIL,
    "route": ["id", "kind", "route", "verdict", "reason", "owed", "carries"] + TAIL,
    "knock_on": ["id", "kind", "i", "n", "target", "verdict", "reason", "owed", "carries"] + TAIL,
    "finding": ["id", "kind", "title", "finding", "recommendation", "whose", "entries"] + TAIL,
}
VERDICTS = {"redraft": ("ACCEPT", "AMEND", "REJECT"), "artifact": ("CONFIRM", "CORRECT"), "measure": ("CONFIRM", "CORRECT"),
            "tool": ("CONFIRM", "CORRECT"), "route": ("CONFIRM", "CORRECT"), "knock_on": ("STANDS", "REOPENS")}
OWES = {"AMEND", "REJECT", "CORRECT", "REOPENS"}
TEXT_FIELDS = {k: ("reason", "owed", "carries") for k in VERDICTS}
TEXT_FIELDS["finding"] = ("finding", "recommendation")
SPAN = re.compile(r'"([^"]+)"')
APPEND_ONLY = {"adversarial_map_staging/r1/L7_successor_drafts.json",
               "adversarial_map_staging/r1/L7_successor_drafts_judgments.json",
               "adversarial_map_staging/r1/R1_rulings.json"}
MAY_MOVE = {"efilist_argument_library_v4_0_0.json"}
RENAMED = re.compile(r"project_canon_v38_\d+\.json")
ARTIFACTS = ("map_v1_8", "register_v0_9")
TOOL = "adversarial_map_staging/controls_v1_7.py"


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def git_bytes_at(repo_dir, rel, want):
    log = subprocess.run(["git", "-C", repo_dir, "log", "--format=%H", "--", rel], capture_output=True, text=True)
    for sha in log.stdout.split() if log.returncode == 0 else []:
        r = subprocess.run(["git", "-C", repo_dir, "show", "%s:%s" % (sha, rel)], capture_output=True)
        if r.returncode == 0 and hashlib.md5(r.stdout).hexdigest() == want:
            return r.stdout
    return None


def pinned_bytes(repo_dir, rel, want, history=None):
    p = os.path.join(repo_dir, rel)
    if os.path.exists(p):
        b = open(p, "rb").read()
        if hashlib.md5(b).hexdigest() == want:
            return b
    return (history or (lambda r_, w_: git_bytes_at(repo_dir, r_, w_)))(rel, want)


def rows_grown(base_bytes, path):
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
    def __init__(self, repo_dir, doc, history=None):
        j = doc["judged"]

        def at(key, want=None):
            b = pinned_bytes(repo_dir, j[key]["file"], want or j[key]["md5"], history)
            if b is None:
                p = os.path.join(repo_dir, j[key]["file"])
                b = open(p, "rb").read() if os.path.exists(p) else b"{}"
            return json.loads(b.decode("utf-8"))

        self.drafts = at("drafts")
        self.first = at("first_judgment")
        first_drafts_md5 = (self.first.get("judged") or {}).get("drafts", {}).get("md5")
        self.drafts_first = at("drafts", first_drafts_md5) if first_drafts_md5 else {"rows": []}
        self.v18 = at("map_v1_8").get("entries", [])
        self.rulings = at("rulings").get("rows", [])
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
        if kind == "judgment":
            xs = [r for r in self.first.get("rows", []) if r.get("id") == rest]
            if not xs:
                raise KeyError("no first-judgment row %s" % rest)
            return list(strings(xs[0]))
        if kind == "corpus":
            return corpus_text(self.corpus, rest)
        if kind == "v1_8":
            node, _, locus = rest.partition("#")
            xs = [x for x in self.v18 if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no v1_8 entry at %s" % rest)
            return [s for x in xs for s in strings(x)]
        if kind == "canon":
            try:
                return list(strings(walk(self.canon, rest)))
            except (KeyError, TypeError):
                raise KeyError("no path %s in the pinned canon" % rest)
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
    k = r["kind"]
    if k == "redraft":
        return "redraft %s" % r.get("row_id")
    if k == "artifact":
        return "artifact %s" % r.get("artifact")
    if k in ("measure", "tool", "route"):
        return k
    if k == "knock_on":
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

    # 6
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
    first_ids = {r["id"] for r in src.drafts_first.get("rows", [])}
    if not first_ids:
        fails.append("pin drafts: the bytes the first judgment read are not recoverable")
    dall = {r["id"]: r for r in src.drafts.get("rows", [])}
    dcur_new = {r["id"]: r for r in current(src.drafts.get("rows", [])) if r["id"] not in first_ids}
    first_rows = {r["id"]: r for r in src.first.get("rows", [])}
    ruled_ns = {r["n"] for r in src.rulings}
    k = src.reading.get("knock_on", {})
    class_want = {(x["i"], x["target"]) for x in k.get("a_class_change_at_an_entry_already_met", [])}
    art_files = {doc["judged"][a]["file"] for a in ARTIFACTS}

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
        if rid != "U2-%03d" % i:
            fails.append("%s: ids must run U2-001, U2-002, ... in file order (expected U2-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2
        if kind == "redraft":
            x = dcur_new.get(r["row_id"])
            if x is None:
                fails.append("%s: %s is not a current row the drafts record gained after the first judgment" % (rid, r["row_id"]))
            else:
                if x.get("supersedes") != r["replaces"]:
                    fails.append("%s: %s supersedes %s, not %s" % (rid, r["row_id"], x.get("supersedes"), r["replaces"]))
                a = first_rows.get(r["answers"])
                if a is None:
                    fails.append("%s: answers %s, which is not a first-judgment row" % (rid, r["answers"]))
                elif a.get("row_id") != r["replaces"] or a.get("verdict") != "AMEND":
                    fails.append("%s: %s does not AMEND %s" % (rid, r["answers"], r["replaces"]))
                if r["target"] != target_of(dall.get(r["replaces"], {})):
                    fails.append("%s: target %s is not %s's target" % (rid, r["target"], r["replaces"]))
        if kind == "artifact" and r["artifact"] not in art_files:
            fails.append("%s: artifact %s is not one the header pins as judged" % (rid, r["artifact"]))
        if kind == "measure":
            if r["measure"] != "knock_on_control":
                fails.append("%s: measure %r" % (rid, r["measure"]))
            elif r["verdict"] == "CONFIRM" and k.get("by_lineage_and_class") != k.get("the_controls_record_lists"):
                fails.append("%s: CONFIRM, but the reading record's count by entry and class is not the control's" % rid)
        if kind == "tool":
            if r["tool"] != TOOL:
                fails.append("%s: tool %r is not %s" % (rid, r["tool"], TOOL))
            elif r["verdict"] == "CONFIRM" and any((src.reading.get("pins", {}).get("gate2_L7_instrument_names_controls_v1_7") or {"?": True}).values()):
                fails.append("%s: CONFIRM, but the reading record says a gate2 instrument names controls_v1_7" % rid)
        if kind == "route" and not str(r["route"]).startswith("U-065"):
            fails.append("%s: route %r is not U-065's" % (rid, r["route"]))
        if kind == "knock_on" and (r["i"], r["target"]) not in class_want:
            fails.append("%s: entry %s (%s) is not one the reading record lists as a class change" % (rid, r["i"], r["target"]))
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
        # 5
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
        # 4
        subj = subject(r)
        prev = chains.get(subj)
        if prev is None:
            if r["supersedes"] is not None:
                fails.append("%s: supersedes %s, but it is the first row for %s" % (rid, r["supersedes"], subj))
        elif r["supersedes"] != prev:
            fails.append("%s: %s judged twice without superseding %s" % (rid, subj, prev))
        chains[subj] = rid
        cur[subj] = r

    missing = ["redraft %s" % x for x in sorted(dcur_new) if "redraft %s" % x not in cur]
    if missing:
        fails.append("coverage: new rows not judged: %s" % ", ".join(missing))
    for f in sorted(art_files):
        if "artifact %s" % f not in cur:
            fails.append("coverage: artifact %s not judged" % f)
    for s in ("measure", "tool", "route"):
        if s not in cur:
            fails.append("coverage: the %s not judged" % s)
    got = {(r["i"], r["target"]) for s, r in cur.items() if s.startswith("knock_on ")}
    if got != class_want:
        fails.append("coverage: knock-on rows %s do not match the reading record's class changes %s"
                     % (sorted(g[0] for g in got), sorted(w[0] for w in class_want)))

    # 7
    if base_text is None:
        info.append("append-only: SKIPPED -- no committed base yet (first landing); vacuous, not a pass")
    else:
        base = json.loads(base_text)
        if {kk: v for kk, v in base.items() if kk != "rows"} != {kk: v for kk, v in doc.items() if kk != "rows"}:
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
            tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    info.append("rows %d | %s | findings %d | quotes %d" % (
        len(rows), ", ".join("%s %d" % kv for kv in sorted(tally.items())),
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
    tmp = tempfile.mkdtemp(prefix="l7rgate_")
    results = []
    try:
        def stage(mut_doc=None, mut_pin=None, base=None, grow=None, drop=None):
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
                open(dst, "wb").write(b)
                if mut_pin and pin["file"].endswith(mut_pin):
                    open(dst, "wb").write(b[:-1] + (b"\n" if b[-1:] != b"\n" else b" "))
            for rel in (doc0["instrument"]["file"], doc0["instrument"]["record"]):
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(REPO, rel), os.path.join(d, rel))
            p = os.path.join(d, REL)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            json.dump(mut_doc if mut_doc is not None else doc0, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            return p, d, json.dumps(base if base is not None else (mut_doc if mut_doc is not None else doc0), ensure_ascii=False)

        def mut(fn):
            d = copy.deepcopy(doc0); fn(d); return d

        def first(kind):
            return next(i for i, r in enumerate(doc0["rows"]) if r["kind"] == kind)

        def renumber(d):
            for kk, r in enumerate(d["rows"], 1):
                r["id"] = "U2-%03d" % kk

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        extra = dict(copy.deepcopy(doc0["rows"][first("redraft")]), id="U2-%03d" % (len(doc0["rows"]) + 1))
        grow_row = lambda rd: rd["rows"].append(dict(copy.deepcopy(rd["rows"][-1]), id="SM-99", supersedes=rd["rows"][-1]["id"]))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "a new row goes unjudged",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("redraft")), renumber(d)))), 1, "new rows not judged"),
            ("C2", "a redraft's verdict reads MAYBE",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C3", "a redraft names a row the first judgment already read",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(row_id="SM-01"))), 1, "gained after the first judgment"),
            ("C4", "a redraft answers a row that is not the AMEND of what it replaces",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(answers="U-004"))), 1, "does not AMEND"),
            ("C5", "a redraft names the wrong replaced row",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(replaces="SM-04"))), 1, "supersedes"),
            ("C6", "a class-change row is dropped",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("knock_on")), renumber(d)))), 1, "do not match the reading record"),
            ("C7", "the route row is not U-065's",
             dict(mut_doc=mut(lambda d: d["rows"][first("route")].update(route="U-064"))), 1, "is not U-065"),
            ("C8", "a quoted span is not declared",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(reason=d["rows"][first("redraft")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C9", "a declared quote is one character off",
             dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C10", "map v1_8 moves by one byte", dict(mut_pin="adversarial_map_v1_8.json"), 1, "pin map_v1_8"),
            ("C11", "a committed row is edited in place",
             dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C12", "a correction row supersedes properly",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("redraft")]["id"]))), base=doc0), 0, None),
            ("C13", "the first judgment grows by an appended row",
             dict(grow=("L7_successor_drafts_judgments.json", lambda rd: rd["rows"].append(dict(copy.deepcopy(rd["rows"][-1]), id="U-999")))), 0, None),
            ("C14", "a committed first-judgment row is edited in place",
             dict(grow=("L7_successor_drafts_judgments.json", lambda rd: rd["rows"][0].update(reason=rd["rows"][0]["reason"] + " (edited)"))), 1, "not merely grown by appended rows"),
            ("C15", "the canon is gone (the rename convention)", dict(drop=os.path.basename(doc0["judged"]["canon"]["file"])), 0, None),
            ("C16", "a finding names an entry R1 never ruled",
             dict(mut_doc=mut(lambda d: d["rows"][next(i for i, r in enumerate(d["rows"]) if r["kind"] == "finding" and r["entries"])].update(entries=[999]))), 1, "are not R1 entries"),
            ("C17", "an AMEND owes nothing",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(verdict="AMEND", owed=[]))), 1, "without saying what is owed"),
        ]
        history = lambda rel, want: pinned_bytes(REPO, rel, want)
        ok_all = True
        for cid, what, kw, want_rc, want_msg in controls:
            p, d, base = stage(**kw)
            fails, _ = check(p, d, base, history)
            rc = 1 if fails else 0
            ok = rc == want_rc and (want_msg is None or any(want_msg in f for f in fails))
            if cid == "C0" and not ok:
                print("C0 (unmutated) is not GREEN: %s" % fails)
                sys.exit(2)
            ok_all &= ok
            results.append({"control": cid, "what": what, "want_rc": want_rc, "want_message": want_msg, "rc": rc,
                            "as_expected": ok, "first_failure": fails[0] if fails else None})
            print("  %-4s %-66s rc %d  %s" % (cid, what, rc, "as expected" if ok else "NOT AS EXPECTED: %s" % fails[:2]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rec = {"artifact": "l7_redrafts_gate control record", "gate": "adversarial_map_staging/r1/l7_redrafts_gate.py",
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
    print("L7 REDRAFTS GATE: %s" % ("GREEN" if not fails else "RED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
