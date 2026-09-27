#!/usr/bin/env python3
"""sp_redrafts_gate.py -- the gate beside SP_redrafts_judgments.json (gate2, 2026-09-26, R0210).

SP_redrafts_judgments.json records gate2's second judgment of L6's X-032 safety pass: the correction rows L6 appended to
SP_drafts_L6.json after gate2's first judgment (SP_drafts_judgments.json), the knock-on after them, and the patch.
APPEND-ONLY. Adapted from pq_repair_redrafts_gate.py (the same seven rules). It checks, and exits 1 on any failure:

  1. rows run Z2-001, Z2-002, ... in file order, each with exactly its kind's keys, a seat and a date;
  2. every redraft row names a current row of the drafts record (read at the bytes this header pins) that the record did
     NOT hold at the bytes the first judgment read; it replaces what the judgment says, at the same locus; the first
     judgment judged the replaced row, and the row it answers is that judgment's AMEND of it or one of its findings; the
     knock_on and patch rows' claims are the reading record's; findings name an owner and real R1 entries;
  3. verdicts: ACCEPT, AMEND or REJECT (redraft) or CONFIRM or CORRECT (knock_on, patch); AMEND, REJECT or CORRECT owe;
  4. coverage: every such new current row has exactly one current judgment, and so do the knock-on and the patch;
  5. every double-quoted span in a row's text is declared and verbatim at its source, read at the pinned bytes:
     drafts:<row id>, judgment:Z-nnn (the first judgment), corpus:<node#locus>, v1_6:<node#locus>, rulings:R1-nnn,
     canon:<dotted.path> and reading:record;
  6. the judged artifacts are at the md5s the header names; an append-only record (the drafts record, the first
     judgment, R1_rulings.json) may have grown by appended rows; the canon may be gone (the rename convention);
  7. append-only against git HEAD's copy.

  python3 sp_redrafts_gate.py                             # base = git HEAD's copy
  python3 sp_redrafts_gate.py --self-test [--emit <path>]   # controls; unmutated first
Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/SP_redrafts_judgments.json"
CORPUS = "efilist_argument_library_v4_0_0.json"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "his_word", "kickoff", "judged", "instrument",
               "rows"]
PINS = ["drafts", "first_judgment", "knock_on", "patch_tool", "drafts_gate_v0_2", "map_v1_6", "rulings", "canon"]
KEYS = {
    "redraft": ["id", "kind", "row_id", "replaces", "answers", "locus", "verdict", "reason", "owed", "carries",
                "quotes", "seat", "date", "supersedes"],
    "companion_redraft": ["id", "kind", "row_id", "replaces", "answers", "locus", "verdict", "lean", "reason", "owed",
                          "carries", "quotes", "seat", "date", "supersedes"],
    "knock_on": ["id", "kind", "claim", "verdict", "reason", "owed", "carries", "quotes", "seat", "date", "supersedes"],
    "patch": ["id", "kind", "claim", "verdict", "reason", "owed", "carries", "quotes", "seat", "date", "supersedes"],
    "finding": ["id", "kind", "title", "finding", "recommendation", "whose", "entries", "quotes", "seat", "date",
                "supersedes"],
}
ROW_KIND = {"redraft": "draft", "companion_redraft": "companion"}
VERDICTS = {"redraft": ("ACCEPT", "AMEND", "REJECT"), "companion_redraft": ("ACCEPT", "AMEND", "REJECT"),
            "knock_on": ("CONFIRM", "CORRECT"), "patch": ("CONFIRM", "CORRECT")}
LEANS = ("admit", "do not admit")
OWES = {"AMEND", "REJECT", "CORRECT"}
TEXT_FIELDS = {k: ("reason", "owed", "carries") for k in VERDICTS}
TEXT_FIELDS["finding"] = ("finding", "recommendation")
SPAN = re.compile(r'"([^"]+)"')
APPEND_ONLY = {"adversarial_map_staging/r1/SP_drafts_L6.json",
               "adversarial_map_staging/r1/SP_drafts_judgments.json",
               "adversarial_map_staging/r1/R1_rulings.json"}
RENAMED = re.compile(r"project_canon_v38_\d+\.json")


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
        t = o["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    else:
        t = o.get(locus)
    if not isinstance(t, str):
        raise KeyError("no corpus text at %s" % rest)
    return [t]


def current(rows):
    sup = {r.get("supersedes") for r in rows if r.get("supersedes")}
    return [r for r in rows if r["id"] not in sup]


class Sources:
    def __init__(self, repo_dir, doc, history=None):
        j = doc["judged"]

        def raw(key, rel=None, want=None):
            rel, want = rel or j[key]["file"], want or j[key]["md5"]
            b = pinned_bytes(repo_dir, rel, want, history)
            if b is None:
                p = os.path.join(repo_dir, rel)
                b = open(p, "rb").read() if os.path.exists(p) else b"{}"
            return json.loads(b.decode("utf-8"))

        self.drafts = raw("drafts")
        self.first = raw("first_judgment")
        fp = self.first.get("judged", {}).get("drafts", {})
        self.first_drafts_ids = {r["id"] for r in raw(None, fp.get("file", j["drafts"]["file"]), fp.get("md5", "-")).get("rows", [])} \
            if fp else set()
        self.map = raw("map_v1_6").get("entries", [])
        self.rulings = raw("rulings").get("rows", [])
        self.canon = raw("canon")
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
        if kind == "judgment":
            xs = [r for r in self.first.get("rows", []) if r.get("id") == rest]
            if not xs:
                raise KeyError("no first-judgment row %s" % rest)
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
    if r["kind"] in ROW_KIND:
        return "%s %s" % (r["kind"], r.get("row_id"))
    if r["kind"] in ("knock_on", "patch"):
        return r["kind"]
    return "finding %s" % r.get("title")


def reading_claims(reading):
    k, p = reading.get("knock_on", {}), reading.get("patch", {})
    knock = {"v0_2_rows_equal_v0_1": k.get("v0_2_rows_equal_v0_1")}
    patch = {"x032_hits_after_every_row": p.get("x032_hits_after_every_row"),
             "rows_mixing_dash_styles": p.get("rows_mixing_dash_styles")}
    knock_ok = knock["v0_2_rows_equal_v0_1"] is True
    patch_ok = patch["x032_hits_after_every_row"] == 0 and patch["rows_mixing_dash_styles"] == []
    return knock, knock_ok, patch, patch_ok


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
    if not src.first_drafts_ids:
        fails.append("pin first_judgment: the drafts bytes the first judgment read are not recoverable")
    dcur = {r["id"]: r for r in current(src.drafts.get("rows", []))}
    new_current = {i: r for i, r in dcur.items() if i not in src.first_drafts_ids and r.get("kind") in ROW_KIND.values()}
    first_rows = {r["id"]: r for r in src.first.get("rows", [])}
    ruled_ns = {r["n"] for r in src.rulings}
    knock, knock_ok, patch, patch_ok = reading_claims(src.reading)

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
        if rid != "Z2-%03d" % i:
            fails.append("%s: ids must run Z2-001, Z2-002, ... in file order (expected Z2-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2
        if kind in ROW_KIND:
            x = new_current.get(r["row_id"])
            if x is None or x.get("kind") != ROW_KIND[kind]:
                fails.append("%s: %s is not a current %s row added since the first judgment" % (rid, r["row_id"], ROW_KIND[kind]))
            else:
                if x.get("supersedes") != r["replaces"] or x.get("locus") != r["locus"]:
                    fails.append("%s: %s replaces %s at %s, not %s at %s" % (rid, r["row_id"], x.get("supersedes"),
                                                                          x.get("locus"), r["replaces"], r["locus"]))
                judged = [y for y in first_rows.values() if y.get("row_id") == r["replaces"]]
                if not judged:
                    fails.append("%s: the first judgment never judged %s" % (rid, r["replaces"]))
                a = first_rows.get(r["answers"])
                if a is None:
                    fails.append("%s: answers %s, which is not a first-judgment row" % (rid, r["answers"]))
                elif not ((a.get("kind") in ("draft", "companion") and a.get("row_id") == r["replaces"]
                           and a.get("verdict") in ("AMEND", "REJECT")) or a.get("kind") == "finding"):
                    fails.append("%s: %s does not AMEND %s and is not a finding" % (rid, r["answers"], r["replaces"]))
        if kind == "knock_on" and (r["claim"] != knock or not knock_ok):
            fails.append("%s: the claim is not the reading record's %s, or its flags fail" % (rid, json.dumps(knock)))
        if kind == "patch" and (r["claim"] != patch or not patch_ok):
            fails.append("%s: the claim is not the reading record's %s, or its flags fail" % (rid, json.dumps(patch)))
        if kind == "companion_redraft" and r["lean"] not in LEANS:
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

    missing = ["%s %s" % ({"draft": "redraft", "companion": "companion_redraft"}[x["kind"]], i)
               for i, x in new_current.items()
               if "%s %s" % ({"draft": "redraft", "companion": "companion_redraft"}[x["kind"]], i) not in cur]
    if missing:
        fails.append("coverage: rows added since the first judgment not judged: %s" % ", ".join(missing))
    for k in ("knock_on", "patch"):
        if k not in cur:
            fails.append("coverage: the %s not judged" % k)

    # 7
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
    tmp = tempfile.mkdtemp(prefix="sprjgate_")
    results = []
    try:
        dp = doc0["judged"]["drafts"]
        corpus_md5 = json.loads(pinned_bytes(REPO, dp["file"], dp["md5"]).decode("utf-8"))["pinned"]["surfaces"][CORPUS]

        def stage(mut_doc=None, mut_pin=None, base=None, grow=None, drop=None, corpus_edit=False):
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

        def first(kind):
            return next(i for i, r in enumerate(doc0["rows"]) if r["kind"] == kind)

        def renumber(d):
            for k, r in enumerate(d["rows"], 1):
                r["id"] = "Z2-%03d" % k

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        extra = dict(copy.deepcopy(doc0["rows"][first("redraft")]), id="Z2-%03d" % (len(doc0["rows"]) + 1))
        ratify = lambda rd: rd["rows"].append({"id": "RT-01", "kind": "ratification", "rows": ["PD-01"],
                                               "seat": "a control", "date": "2026-09-26", "supersedes": None})
        grow_first = lambda rd: rd["rows"].append(dict(copy.deepcopy(rd["rows"][-1]), id="Z-%03d" % (len(rd["rows"]) + 1)))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "a correction goes unjudged",
             dict(mut_doc=mut(lambda d: (d["rows"].pop(first("redraft")), renumber(d)))), 1, "not judged"),
            ("C2", "a verdict reads MAYBE",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C3", "an AMEND owes nothing",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(verdict="AMEND", owed=[]))), 1, "without saying what is owed"),
            ("C5", "a row names a row the record lacks",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(row_id="SD-99"))), 1, "added since the first judgment"),
            ("C6", "a row names one the first judgment already read",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(row_id="SD-04"))), 1, "added since the first judgment"),
            ("C7", "a row answers a judgment that did not AMEND it",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(answers="Z-001"))), 1, "does not AMEND"),
            ("C8", "the knock-on claim is not the reading's",
             dict(mut_doc=mut(lambda d: d["rows"][first("knock_on")]["claim"].update(anchor_inside=14))), 1, "reading record's"),
            ("C9", "the patch claim is not the reading's",
             dict(mut_doc=mut(lambda d: d["rows"][first("patch")]["claim"].update(sets=["all"]))), 1, "reading record's"),
            ("C10", "a quoted span is not declared",
             dict(mut_doc=mut(lambda d: d["rows"][first("redraft")].update(reason=d["rows"][first("redraft")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C11", "a declared quote is one character off",
             dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C12", "map v1_6 moves by one byte", dict(mut_pin="adversarial_map_v1_6.json"), 1, "pin map_v1_6"),
            ("C13", "a committed row is edited in place",
             dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C14", "a correction row supersedes properly",
             dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("redraft")]["id"]))), base=doc0), 0, None),
            ("C15", "the drafts record grows by a ratification row", dict(grow=("SP_drafts_L6.json", ratify)), 0, None),
            ("C16", "the first judgment grows by an appended row", dict(grow=("SP_drafts_judgments.json", grow_first)), 0, None),
            ("C17", "the canon is gone (the rename convention)", dict(drop=os.path.basename(doc0["judged"]["canon"]["file"])), 0, None),
            ("C18", "a simulated pin: a quoted corpus span is gone", dict(corpus_edit=True), 0, None),
            ("C19", "the same, with git history withheld", dict(corpus_edit=True, _history=lambda rel, want: None), 1, "not recoverable"),
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
    rec = {"artifact": "sp_redrafts_gate control record",
           "gate": "adversarial_map_staging/r1/sp_redrafts_gate.py",
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
    print("SP REDRAFTS GATE: %s" % ("GREEN" if not fails else "RED (%d)" % len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
