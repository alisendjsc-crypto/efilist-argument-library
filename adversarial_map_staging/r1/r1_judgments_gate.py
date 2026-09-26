#!/usr/bin/env python3
"""r1_judgments_gate.py -- the gate beside R1_drafts_judgments.json (gate2, 2026-09-25).

R1_drafts_judgments.json records gate2's judgment of L4's drafts (R1_drafts_L4.json). It is
APPEND-ONLY: a row is never edited or removed, and a correction is a new row whose `supersedes`
names the row it replaces. This gate checks, and exits 1 on any failure:

  1. rows run J-001, J-002, ... in file order, each with exactly its kind's keys;
  2. every draft row names a real draft: its n, R1 row, target and drafted disposition are the
     drafts file's; its verdict is ACCEPT, AMEND or REJECT; an AMEND or REJECT says what is owed;
  3. coverage: each of the drafts file's drafts, and each relation register v0_5 records as
     "L4, drafted", has exactly one current judgment (a later row supersedes the one before it
     for the same subject, and nothing else);
  4. every relation row names a relation the register stores; every finding names its owner
     and only real draft numbers;
  5. every double-quoted span in a row's text is declared in that row's quotes, and every
     declared quote is verbatim at its source (r1_quote_check.py's sources, plus v1_4:, drafts:,
     rulings:, design: and render:);
  6. the judged artifacts are still at the md5s the header names;
  7. append-only: the committed base (git HEAD's copy, or --base) is intact: header unchanged,
     every committed row still present, unchanged and in order.

  python3 r1_judgments_gate.py                       # base = git HEAD's copy
  python3 r1_judgments_gate.py --self-test [--emit <path>]   # controls; unmutated first

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, hashlib, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "adversarial_map_staging/r1/R1_drafts_judgments.json"
STG = "adversarial_map_staging"

HEADER_KEYS = ["artifact", "state", "law", "what_a_verdict_means", "standard", "kickoff", "judged",
               "canon_at_judgment", "instrument", "rows"]
COMMON = {"id", "kind", "quotes", "seat", "date", "supersedes"}
KEYS = {
    "draft": COMMON | {"n", "r1_row", "target", "drafted", "verdict", "reason", "owed", "carries"},
    "relation": COMMON | {"relation", "verdict", "reason", "owed", "carries"},
    "finding": COMMON | {"title", "finding", "recommendation", "whose", "entries"},
}
TEXT_FIELDS = {"draft": ("reason", "owed", "carries"), "relation": ("reason", "owed", "carries"),
               "finding": ("finding", "recommendation")}
VERDICTS = ("ACCEPT", "AMEND", "REJECT")
SPAN = re.compile(r'"([^"]+)"')

_spec = importlib.util.spec_from_file_location("r1qc", os.path.join(HERE, "r1_quote_check.py"))
Q = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Q)


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


class Sources:
    """r1_quote_check's sources, plus the ones a judgment of drafts needs."""

    def __init__(self, repo_dir, doc):
        self.repo = repo_dir
        self.q = Q.Texts()
        j = doc["judged"]
        self.v14 = json.load(open(os.path.join(repo_dir, j["map_v1_4"]["file"]), encoding="utf-8"))["entries"]
        self.drafts = json.load(open(os.path.join(repo_dir, j["drafts"]["file"]), encoding="utf-8"))
        self.rulings = json.load(open(os.path.join(repo_dir, j["rulings"]["file"]), encoding="utf-8"))["rows"]

    def resolve(self, src):
        kind, _, rest = src.partition(":")
        if kind == "v1_4":
            node, _, locus = rest.partition("#")
            xs = [x for x in self.v14 if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no v1_4 entry at %s" % rest)
            return [s for x in xs for s in strings(x)]
        if kind == "drafts":
            xs = [x for x in self.drafts["drafts"] if "#%d" % x["n"] == rest]
            if not xs:
                raise KeyError("no draft %s" % rest)
            return list(strings(xs[0]))
        if kind == "rulings":
            xs = [r for r in self.rulings if r["row"] == rest]
            if not xs:
                raise KeyError("no rulings row %s" % rest)
            return list(strings(xs[0]))
        if kind in ("design", "render"):
            pat = r"adversarial_map_design_v0_\d+\.md" if kind == "design" else r"render_[a-z0-9_]+\.py"
            if not re.fullmatch(pat, rest):
                raise KeyError("%s source must name %s, got %r" % (kind, pat, rest))
            p = os.path.join(self.repo, STG, rest)
            if not os.path.exists(p):
                raise KeyError("no file %s" % rest)
            return [open(p, encoding="utf-8").read()]
        return self.q.resolve(src)


def subject(r):
    return {"draft": lambda: "draft #%s" % r.get("n"), "relation": lambda: "relation %s" % r.get("relation"),
            "finding": lambda: "finding %s" % r.get("title")}.get(r.get("kind"), lambda: "?")()


def texts_of(r):
    out = []
    for f in TEXT_FIELDS.get(r["kind"], ()):
        v = r.get(f)
        out += v if isinstance(v, list) else [v]
    return [t for t in out if isinstance(t, str)]


def check(path, repo_dir, base_text):
    fails, info = [], []
    doc = json.load(open(path, encoding="utf-8"))
    if list(doc) != HEADER_KEYS:
        return ["structure: header keys are %s" % list(doc)], info
    rows = doc["rows"]
    if not isinstance(rows, list) or not rows:
        return ["structure: no rows"], info

    # 6 -- the referents have not moved
    for name, pin in doc["judged"].items():
        p = os.path.join(repo_dir, pin["file"])
        got = md5(p) if os.path.exists(p) else "MISSING"
        if got != pin["md5"]:
            fails.append("pin %s: %s is %s, header names %s" % (name, pin["file"], got, pin["md5"]))
    src = Sources(repo_dir, doc)
    drafts = {x["n"]: x for x in src.drafts["drafts"]}
    targets = {}
    for r in src.rulings:
        targets[r["n"]] = r["target"]
    reg = json.load(open(os.path.join(repo_dir, doc["judged"]["register_v0_5"]["file"]), encoding="utf-8"))
    stored = {"%s %s %s" % (b["bedrock_id"], rel["kind"], rel["to"]): rel
              for b in reg["bedrocks"] for rel in b["relations"]}
    drafted_rels = {k for k, rel in stored.items() if str(rel.get("note", "")).startswith("L4, drafted")}

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
        if rid != "J-%03d" % i:
            fails.append("%s: ids must run J-001, J-002, ... in file order (expected J-%03d)" % (rid, i))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
            fails.append("%s: date %r is not YYYY-MM-DD" % (rid, r["date"]))
        if not str(r["seat"]).strip():
            fails.append("%s: no seat" % rid)
        # 2 and 4
        if kind == "draft":
            x = drafts.get(r["n"])
            if x is None:
                fails.append("%s: n=%s names no draft" % (rid, r["n"]))
            else:
                if r["r1_row"] != x["row"]:
                    fails.append("%s: r1_row %s != the draft's %s" % (rid, r["r1_row"], x["row"]))
                if r["drafted"] != x["disposition"]:
                    fails.append("%s: drafted %s != the draft's %s" % (rid, r["drafted"], x["disposition"]))
                if r["target"] != targets.get(r["n"]):
                    fails.append("%s: target %s != R1's %s" % (rid, r["target"], targets.get(r["n"])))
        if kind in ("draft", "relation"):
            if r["verdict"] not in VERDICTS:
                fails.append("%s: verdict %r is not one of %s" % (rid, r["verdict"], "/".join(VERDICTS)))
            elif r["verdict"] in ("AMEND", "REJECT") and not [o for o in r["owed"] if str(o).strip()]:
                fails.append("%s: %s without saying what is owed" % (rid, r["verdict"]))
            if not str(r["reason"]).strip():
                fails.append("%s: no reason" % rid)
        if kind == "relation" and r["relation"] not in stored:
            fails.append("%s: relation %r is not stored in register v0_5" % (rid, r["relation"]))
        if kind == "finding":
            if not str(r["whose"]).strip():
                fails.append("%s: a finding with no owner" % rid)
            bad = [n for n in r["entries"] if n not in drafts]
            if bad:
                fails.append("%s: entries %s name no draft" % (rid, bad))
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
        # 3 -- one current judgment per subject
        subj = subject(r)
        prev = chains.get(subj)
        if prev is None:
            if r["supersedes"] is not None:
                fails.append("%s: supersedes %s, but it is the first row for %s" % (rid, r["supersedes"], subj))
        elif r["supersedes"] != prev:
            fails.append("%s: %s judged twice without superseding %s" % (rid, subj, prev))
        chains[subj] = rid
        current[subj] = r

    judged_n = {int(s.split("#")[1]) for s in current if s.startswith("draft #") and s.split("#")[1].isdigit()}
    missing = sorted(set(drafts) - judged_n)
    if missing:
        fails.append("coverage: drafts not judged: %s" % ", ".join("#%d" % n for n in missing))
    judged_rels = {s[len("relation "):] for s in current if s.startswith("relation ")}
    if judged_rels != drafted_rels:
        fails.append("coverage: relations judged %s, register v0_5's drafted relations %s"
                     % (sorted(judged_rels), sorted(drafted_rels)))

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
    cur = [r for r in current.values() if r["kind"] in ("draft", "relation")]
    tally = {v: sum(1 for r in cur if r["kind"] == "draft" and r["verdict"] == v) for v in VERDICTS}
    info.append("rows %d | drafts judged %d of %d (%s) | relations %d of %d | findings %d | quotes %d"
                % (len(rows), len(judged_n & set(drafts)), len(drafts),
                   ", ".join("%s %d" % kv for kv in tally.items()), len(judged_rels & drafted_rels),
                   len(drafted_rels), sum(1 for r in current.values() if r["kind"] == "finding"),
                   sum(len(r["quotes"]) for r in rows)))
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
    tmp = tempfile.mkdtemp(prefix="r1jgate_")
    results = []
    try:
        def stage(mut_doc=None, mut_pin=None, base=None):
            d = os.path.join(tmp, "c%d" % len(results))
            for pin in doc0["judged"].values():
                dst = os.path.join(d, pin["file"])
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(REPO, pin["file"]), dst)
                if mut_pin and pin["file"].endswith(mut_pin):
                    b = open(dst, "rb").read()
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

        iq = next(i for i, r in enumerate(doc0["rows"]) if r["quotes"])
        ia = first("draft", "AMEND") if any(r.get("verdict") == "AMEND" for r in doc0["rows"]) else first("draft")
        extra = dict(copy.deepcopy(doc0["rows"][first("draft")]), id="J-%03d" % (len(doc0["rows"]) + 1))
        controls = [
            ("C0", "unmutated", {}, 0, None),
            ("C1", "a draft goes unjudged", dict(mut_doc=mut(lambda d: d["rows"].pop(first("draft")) and
                                                             [r.update(id="J-%03d" % k) for k, r in enumerate(d["rows"], 1)])), 1, "drafts not judged"),
            ("C2", "a draft judged twice, no supersedes", dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=None))), base=doc0), 1, "judged twice without superseding"),
            ("C3", "a verdict reads MAYBE", dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(verdict="MAYBE"))), 1, "is not one of"),
            ("C4", "an AMEND owes nothing", dict(mut_doc=mut(lambda d: d["rows"][ia].update(verdict="AMEND", owed=[]))), 1, "without saying what is owed"),
            ("C5", "a draft row names the wrong R1 row", dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(r1_row="R1-999"))), 1, "r1_row"),
            ("C6", "a quoted span is not declared", dict(mut_doc=mut(lambda d: d["rows"][first("draft")].update(reason=d["rows"][first("draft")]["reason"] + ' "an undeclared span"'))), 1, "undeclared quotation"),
            ("C7", "a declared quote is one character off", dict(mut_doc=mut(lambda d: d["rows"][iq]["quotes"][0].update(quote=d["rows"][iq]["quotes"][0]["quote"][:-1] + "#"))), 1, "NOT VERBATIM"),
            ("C8", "the drafts file moves by one byte", dict(mut_pin="R1_drafts_L4.json"), 1, "pin drafts"),
            ("C9", "a relation names one the register lacks", dict(mut_doc=mut(lambda d: d["rows"][first("relation")].update(relation="HR-01 conditions HR-02"))), 1, "not stored in register"),
            ("C10", "a committed row is edited in place", dict(mut_doc=mut(lambda d: d["rows"][0].update(reason=d["rows"][0]["reason"] + " (edited)")), base=doc0), 1, "was edited or removed"),
            ("C11", "a correction row supersedes properly", dict(mut_doc=mut(lambda d: d["rows"].append(dict(extra, supersedes=d["rows"][first("draft")]["id"]))), base=doc0), 0, None),
        ]
        ok_all = True
        for cid, what, kw, want_rc, want_msg in controls:
            p, d, base = stage(**kw)
            fails, _ = check(p, d, base)
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
        rec = {"artifact": os.path.basename(emit), "gate": "adversarial_map_staging/r1/r1_judgments_gate.py",
               "gate_md5": md5(os.path.abspath(__file__)), "judgments_md5": md5(real),
               "rule": "C0, the unmutated control, runs first and must be GREEN; each mutation must go RED with its "
                       "own failure line; C11, a proper correction row, must stay GREEN.",
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
    print("R1 JUDGMENTS GATE: %s" % ("GREEN" if not fails else "RED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
