#!/usr/bin/env python3
"""r1_v1_5_judgments_gate.py -- the gate beside R1_v1_5_judgments.json (gate2, 2026-09-26).

R1_v1_5_judgments.json records gate2's second judgment: v1_5's redrafts (R1_redrafts_v1_5.json),
register v0_6's deltas, the change L4b made to r1_judgments_gate.py, and the reading of the HOLDS
that L4's drafts knocked on (l4_knock_on_v0_1.json). It is APPEND-ONLY: a row is never edited or
removed, and a correction is a new row whose `supersedes` names the row it replaces. This gate
checks, and exits 1 on any failure:

  1. rows run V-001, V-002, ... in file order, each with exactly its kind's keys, a seat and a date;
  2. every redraft row names a real redraft (n, the judgment row it answers, its kind) with a
     verdict of ACCEPT, AMEND or REJECT; every register row names one of register v0_6's declared
     deltas by index and word for word; every knock-on row names a HOLDS the knock-on record lists,
     with its current R1 row, and a verdict of STANDS or REOPENS; the gate row is CONFIRM or
     CORRECT;
  3. an AMEND, REJECT or CORRECT says what is owed; a REOPENS carries its lean;
  4. coverage: every redraft, every register delta and every knocked-on HOLDS has exactly one
     current judgment, and the gate change has one (a later row supersedes the one before it for
     the same subject, and nothing else);
  5. every double-quoted span in a row's text is declared in that row's quotes, and every declared
     quote is verbatim at its source. Sources: r1_quote_check.py's corpus:, map: (v1_3) and canon:;
     and, each resolved against the file this record's header pins, v1_4:, v1_5:, redrafts:#n,
     rulings:R1-nnn, judgments:J-nnn, register_v0_5:HR-nn and register_v0_6:HR-nn; plus design:
     and render: files in adversarial_map_staging/;
  6. the judged artifacts are still at the md5s the header names, except an append-only record
     (R1_rulings.json, R1_drafts_judgments.json), which may have grown by appended rows since the
     judgment: its pinned bytes must then be recoverable from git history, with their header
     unchanged and their rows a prefix of the current file's. Every judged artifact is read at its
     pinned bytes, never at a later state (gate2, 2026-09-26, when R1-070 was appended);
  7. append-only: the committed base (git HEAD's copy, or --base) is intact: header unchanged,
     every committed row still present, unchanged and in order.

  python3 r1_v1_5_judgments_gate.py                             # base = git HEAD's copy
  python3 r1_v1_5_judgments_gate.py --self-test [--emit <path>]   # controls; unmutated first

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/R1_v1_5_judgments.json"
STG = "adversarial_map_staging"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "his_word", "kickoff", "judged", "instrument",
               "rows"]
PINS = ["map_v1_5", "redrafts", "register_v0_6", "register_v0_5", "map_v1_4", "rulings", "judgments_v1_4",
        "knock_on"]
COMMON = {"id", "kind", "quotes", "seat", "date", "supersedes"}
KEYS = {
    "redraft": COMMON | {"n", "answers", "redraft_kind", "verdict", "reason", "owed", "carries"},
    "register": COMMON | {"delta_index", "delta", "verdict", "reason", "owed", "carries"},
    "gate": COMMON | {"gate", "from_md5", "to_md5", "verdict", "reason", "owed", "carries"},
    "knock_on": COMMON | {"n", "r1_row", "target", "verdict", "reason", "lean", "carries"},
    "finding": COMMON | {"title", "finding", "recommendation", "whose", "entries"},
}
VERDICTS = {"redraft": ("ACCEPT", "AMEND", "REJECT"), "register": ("ACCEPT", "AMEND", "REJECT"),
            "gate": ("CONFIRM", "CORRECT"), "knock_on": ("STANDS", "REOPENS")}
OWES = {"AMEND", "REJECT", "CORRECT"}
TEXT_FIELDS = {"redraft": ("reason", "owed", "carries"), "register": ("reason", "owed", "carries"),
               "gate": ("reason", "owed", "carries"), "knock_on": ("reason", "lean", "carries"),
               "finding": ("finding", "recommendation")}
SPAN = re.compile(r'"([^"]+)"')

_spec = importlib.util.spec_from_file_location("r1qc", os.path.join(HERE, "r1_quote_check.py"))
Q = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Q)


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


APPEND_ONLY = {"adversarial_map_staging/r1/R1_rulings.json", "adversarial_map_staging/r1/R1_drafts_judgments.json"}


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


def jload(repo_dir, rel):
    return json.load(open(os.path.join(repo_dir, rel), encoding="utf-8"))


class Sources:
    """Every source resolves against a file the header pins, at the bytes it pins, except
    r1_quote_check's own three."""

    def __init__(self, repo_dir, doc, history=None):
        self.repo = repo_dir
        self.q = Q.Texts()
        j = doc["judged"]

        def at(key):
            b = pinned_bytes(repo_dir, j[key]["file"], j[key]["md5"], history)
            return json.loads(b.decode("utf-8")) if b is not None else jload(repo_dir, j[key]["file"])

        self.maps = {"v1_4": at("map_v1_4")["entries"], "v1_5": at("map_v1_5")["entries"]}
        self.redrafts = at("redrafts")
        self.rulings = at("rulings")["rows"]
        self.judgments = at("judgments_v1_4")["rows"]
        reg = {k: at(k) for k in ("register_v0_5", "register_v0_6")}
        self.regs = {k: {b["bedrock_id"]: b for b in v["bedrocks"]} for k, v in reg.items()}
        self.deltas = reg["register_v0_6"]["meta"]["changes_from_v0_5"]
        self.knock = at("knock_on")

    def resolve(self, src):
        kind, _, rest = src.partition(":")
        if kind in self.maps:
            node, _, locus = rest.partition("#")
            xs = [x for x in self.maps[kind] if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no %s entry at %s" % (kind, rest))
            return [s for x in xs for s in strings(x)]
        if kind == "redrafts":
            xs = [x for x in self.redrafts["redrafts"] if "#%d" % x["n"] == rest]
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
        if kind in ("design", "render"):
            pat = r"adversarial_map_design_v0_\d+\.md" if kind == "design" else r"render_[a-z0-9_]+\.py"
            if not re.fullmatch(pat, rest):
                raise KeyError("%s source must name %s, got %r" % (kind, pat, rest))
            p = os.path.join(self.repo, STG, rest)
            if not os.path.exists(p):
                raise KeyError("no file %s" % rest)
            return [open(p, encoding="utf-8").read()]
        if kind in ("corpus", "map", "canon"):
            return self.q.resolve(src)
        raise KeyError("unknown source kind %r" % kind)


def subject(r):
    k = r.get("kind")
    if k == "redraft":
        return "redraft #%s" % r.get("n")
    if k == "register":
        return "register delta %s" % r.get("delta_index")
    if k == "gate":
        return "gate %s" % r.get("gate")
    if k == "knock_on":
        return "knock-on #%s" % r.get("n")
    if k == "finding":
        return "finding %s" % r.get("title")
    return "?"


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

    # 6 -- the referents have not moved, or an append-only one has only grown
    for name, pin in doc["judged"].items():
        p = os.path.join(repo_dir, pin["file"])
        got = md5(p) if os.path.exists(p) else "MISSING"
        if got == pin["md5"]:
            continue
        if pin["file"] not in APPEND_ONLY:
            fails.append("pin %s: %s is %s, header names %s" % (name, pin["file"], got, pin["md5"]))
            continue
        base = pinned_bytes(repo_dir, pin["file"], pin["md5"], history)
        grown = rows_grown(base, p) if base is not None and got != "MISSING" else None
        if grown is None:
            fails.append("pin %s: %s is %s, header names %s, and it has not merely grown by appended rows"
                         % (name, pin["file"], got, pin["md5"]))
        else:
            info.append("pin %s: %s has grown by %d appended row(s) since the judgment; read at %s"
                        % (name, pin["file"], grown, pin["md5"][:8]))
    src = Sources(repo_dir, doc, history)
    redrafts = {x["n"]: x for x in src.redrafts["redrafts"]}
    deltas = src.deltas
    holds = list(src.knock["holds_newly_collided"])
    superseded = {r["supersedes"] for r in src.rulings if r.get("supersedes")}
    current_r1 = {r["n"]: r for r in src.rulings if r["row"] not in superseded}

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
        if rid != "V-%03d" % i:
            fails.append("%s: ids must run V-001, V-002, ... in file order (expected V-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2
        if kind == "redraft":
            x = redrafts.get(r["n"])
            if x is None:
                fails.append("%s: n=%s names no redraft" % (rid, r["n"]))
            elif (r["answers"], r["redraft_kind"]) != (x["judgment_row"], x["kind"]):
                fails.append("%s: answers/redraft_kind %s/%s != the redraft's %s/%s"
                             % (rid, r["answers"], r["redraft_kind"], x["judgment_row"], x["kind"]))
        if kind == "register":
            k = r["delta_index"]
            if not (isinstance(k, int) and 0 <= k < len(deltas)) or r["delta"] != deltas[k]:
                fails.append("%s: delta %r is not register v0_6's declared delta %r" % (rid, r["delta"][:50], k))
        if kind == "knock_on":
            cr = current_r1.get(r["n"])
            if r["n"] not in holds:
                fails.append("%s: #%s is not a HOLDS the knock-on record lists" % (rid, r["n"]))
            elif cr is None or cr["verdict"] != "HOLDS" or (r["r1_row"], r["target"]) != (cr["row"], cr["target"]):
                fails.append("%s: r1_row/target %s/%s != the current HOLDS row" % (rid, r["r1_row"], r["target"]))
            if r["verdict"] == "REOPENS" and not str(r["lean"] or "").strip():
                fails.append("%s: REOPENS without its lean" % rid)
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

    for want, label in ((["redraft #%d" % n for n in redrafts], "redrafts"),
                        (["register delta %d" % k for k in range(len(deltas))], "register deltas"),
                        (["knock-on #%d" % n for n in holds], "knocked-on HOLDS")):
        missing = [s for s in want if s not in current]
        if missing:
            fails.append("coverage: %s not judged: %s" % (label, ", ".join(missing)))
    if sum(1 for s in current if s.startswith("gate ")) != 1:
        fails.append("coverage: the gate change needs exactly one current judgment")

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
    tmp = tempfile.mkdtemp(prefix="r1v15gate_")
    results = []
    try:
        def stage(mut_doc=None, mut_pin=None, base=None, grow=None):
            # every judged artifact is staged at its pinned bytes; `grow` = (file suffix, fn) rewrites
            # that append-only record from its pinned document, to test the append-only exception
            d = os.path.join(tmp, "c%d" % len(results))
            for pin in doc0["judged"].values():
                dst = os.path.join(d, pin["file"])
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                b = pinned_bytes(REPO, pin["file"], pin["md5"])
                if grow and pin["file"].endswith(grow[0]):
                    rd = json.loads(b.decode("utf-8")); grow[1](rd)
                    b = json.dumps(rd, ensure_ascii=False).encode("utf-8")
                open(dst, "wb").write(b)
                if mut_pin and pin["file"].endswith(mut_pin):
                    open(dst, "wb").write(b[:-1] + (b"\n" if b[-1:] != b"\n" else b" "))
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
                r["id"] = "V-%03d" % k

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        extra = dict(copy.deepcopy(doc0["rows"][first("redraft")]), id="V-%03d" % (len(doc0["rows"]) + 1))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "a redraft goes unjudged",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("redraft")), renumber(d)))), 1, "redrafts not judged"),
            ("C2", "a knocked-on HOLDS goes unread",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("knock_on")), renumber(d)))), 1, "knocked-on HOLDS not judged"),
            ("C3", "a redraft judged twice, no supersedes",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=None))), base=doc0), 1, "judged twice without superseding"),
            ("C4", "a knock-on verdict reads MAYBE",
             dict(mut_doc=mut(lambda d: d["rows"][first("knock_on")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C5", "a REOPENS carries no lean",
             dict(mut_doc=mut(lambda d: d["rows"][first("knock_on")].update(verdict="REOPENS", lean=""))), 1, "REOPENS without its lean"),
            ("C6", "an AMEND owes nothing",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(verdict="AMEND", owed=[]))), 1, "without saying what is owed"),
            ("C7", "a register row misquotes its delta",
             dict(mut_doc=mut(lambda d: d["rows"][first("register")].update(delta=d["rows"][first("register")]["delta"] + "x"))), 1, "declared delta"),
            ("C8", "a quoted span is not declared",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(reason=d["rows"][first("redraft")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C9", "a declared quote is one character off",
             dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C10", "map v1_5 moves by one byte", dict(mut_pin="adversarial_map_v1_5.json"), 1, "pin map_v1_5"),
            ("C11", "a committed row is edited in place",
             dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C12", "a correction row supersedes properly",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("redraft")]["id"]))), base=doc0), 0, None),
            ("C13", "the rulings file grows by one appended row",
             dict(grow=("R1_rulings.json", lambda rd: rd["rows"].append(dict(rd["rows"][-1], row="R1-%03d" % (len(rd["rows"]) + 1))))), 0, None),
            ("C14", "a committed rulings row is edited in place",
             dict(grow=("R1_rulings.json", lambda rd: rd["rows"][0].update(reason=rd["rows"][0]["reason"] + " (edited)"))), 1, "not merely grown by appended rows"),
            ("C15", "the first judgment record grows by one row",
             dict(grow=("R1_drafts_judgments.json", lambda rd: rd["rows"].append(dict(rd["rows"][-1], id="J-%03d" % (len(rd["rows"]) + 1))))), 0, None),
        ]
        # the staged tree has no git; history resolves against this repo's own, as the real run does
        history = lambda rel, want: pinned_bytes(REPO, rel, want)
        ok_all = True
        for cid, what, kw, want_rc, want_msg in controls:
            p, d, base = stage(**kw)
            fails, _ = check(p, d, base, history)
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
        rec = {"artifact": os.path.basename(emit), "gate": "adversarial_map_staging/r1/r1_v1_5_judgments_gate.py",
               "gate_md5": md5(os.path.abspath(__file__)), "judgments_md5": md5(real),
               "rule": "C0, the unmutated control, runs first and must be GREEN; each mutation must go RED with its "
                       "own failure line; C12, a proper correction row, must stay GREEN; C13 and C15, an append-only "
                       "record grown by an appended row, must stay GREEN, and C14, a committed rulings row edited in "
                       "place, must go RED.",
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
    print("R1 v1_5 JUDGMENTS GATE: %s" % ("GREEN" if not fails else "RED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
