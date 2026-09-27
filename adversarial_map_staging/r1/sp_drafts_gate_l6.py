#!/usr/bin/env python3
"""sp_drafts_gate_l6.py -- the gate for SP_drafts_L6.json, the X-032 safety pass's drafts (L6, 2026-09-26, R0193).

The record holds the pass's repair text: nine drafts over X-032's six loci, proposed companions at the five nodes'
other slots, proposed rows widening the pass beyond X-032, findings, and (later) his ratification. It is append-only
(L2's law: the file lands with its gate).

  G1  schema        header keys; row keys per kind; ids unique; a 'supersedes' names an earlier row
  G2  pins          X-032's judgment, the three surfaces, map v1_6, the rulings and the reading record are recoverable
                    at the md5s the record names (working tree or git history)
  G3  coverage      the queue is exactly X-032's six loci, each named in X-032's own text; every one of them has a
                    current declared draft, and a draft sits nowhere else; a proposed row never sits at one of the six
  G4  text          every current text occurs exactly once in its locus in the pinned corpus; spans in one locus do not
                    overlap; parts number a locus's rows in text order
  G5  words         recorded word counts equal the computed ones
  G6  replacement   non-empty, different from the current text, absent from the pinned corpus, and free of every one
                    of gate2's named patterns (X-032's EXIT list)
  G7  quotes        every declared quote occurs verbatim in its source, read at the pinned bytes (corpus:<locus>,
                    map:<locus>, judgment:<row>, wing:<wing>:<locus>)
  G8  framing gone  the declared patch leaves no hit of gate2's patterns at the six loci; on the patch of every
                    current row, the wide set (sp_reading_l6.py) matches inside a replacement only where that row
                    declares the match as residual, with its reason, and every declared residual occurs
  G9  patch         tools/pin_patch_l6.py builds the declared set and the full set; on each, the three surfaces agree
                    under xsurface's canonical md5, every current text is gone and every replacement occurs once
  G10 append-only   every row committed at HEAD is still there, byte-identical and in order; the header is unchanged
  G11 ratification  the newest current ratification (if any) names only current rows of a patching kind, every
                    current declared draft among them, no row twice, and carries his words, the relay and the judgment

  python3 sp_drafts_gate_l6.py                                # gate the record
  python3 sp_drafts_gate_l6.py --self-test [--emit P]         # controls, the unmutated first
  python3 sp_drafts_gate_l6.py --knock-on [--emit|--check]    # the derived knock-on record

Repo-relative. Writes nothing unless --emit is given. Its patch simulation's temp directories are its own and removed.
"""
import copy, importlib.util, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

REL = "adversarial_map_staging/r1/SP_drafts_L6.json"
KNOCK = "adversarial_map_staging/r1/SP_knock_on_L6_v0_1.json"
CORPUS = "efilist_argument_library_v4_0_0.json"
XSURFACE = "tools/xsurface_v4_1_0.py"   # run, not imported: it gates at import time
HEADER = ["artifact", "state", "law", "kickoff", "queue", "pinned", "rows"]
PATCHING = ("draft", "companion", "widening")
KEYS = {k: ["id", "kind", "status", "part", "locus", "answers", "current", "replacement", "cuts", "keeps", "how", "words",
            "residual", "quotes", "seat", "date", "supersedes"] for k in PATCHING}
KEYS["finding"] = ["id", "kind", "title", "finding", "lean", "seat", "date", "supersedes"]
KEYS["ratification"] = ["id", "kind", "rows", "his_words_verbatim", "said", "relay", "judgment", "seat", "date",
                        "supersedes"]
WINGS = {"right-to-die": "site/right-to-die/right_to_die_corpus_v0_1.json"}


def load_mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


PATCH = load_mod("tools/pin_patch_l6.py", "pin_patch_l6")
READING = load_mod("adversarial_map_staging/r1/sp_reading_l6.py", "sp_reading_l6")
DOSSIERS = load_mod("adversarial_map_staging/r1/sp_dossiers_l6.py", "sp_dossiers_l6")


def words(s):
    return len(s.split())


def committed_base():
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + REL], capture_output=True)
    return json.loads(r.stdout.decode("utf-8")) if r.returncode == 0 else None


def jload(rel, md5):
    return json.loads(pinned.bytes_at(REPO, rel, md5).decode("utf-8"))


def quote_source(src, rec, corpus):
    kind, _, ref = src.partition(":")
    if kind == "corpus":
        return PATCH.locus_text(corpus, ref)
    if kind == "map":
        m = jload(rec["pinned"]["map"]["file"], rec["pinned"]["map"]["md5"])
        node, loc = ref.split("#")
        return "\n".join(e["target_anchor"] + "\n" + e["adversarial_move"] + "\n" + e["grounds"]
                         for e in m["entries"] if (e["target_id"], e["target_locus"]) == (node, loc))
    if kind == "judgment":
        j = jload(rec["queue"]["judgment"]["file"], rec["queue"]["judgment"]["md5"])
        row = next(r for r in j["rows"] if r["id"] == ref)
        return "\n".join(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False) for v in row.values()) + "\n" + \
            "\n".join(q["quote"] for q in row.get("quotes", []))
    if kind == "wing":
        wing, _, locus = ref.partition(":")
        d = json.load(open(os.path.join(REPO, WINGS[wing]), encoding="utf-8"))
        oid, loc = locus.split("#")
        o = next(x for x in d["objections"] if x["id"] == oid)
        return o["responses"][loc] if loc in o.get("responses", {}) else o[loc]
    raise KeyError(src)


def xsurface_canon(rec, rows):
    """Build the patch for rows in a temp dir and run the cross-surface gate on it. Return (rc, {surface: canon md5})."""
    out, _ = PATCH.build(rec, rows)
    with tempfile.TemporaryDirectory(prefix="sp_patch_") as d:
        PATCH.write(out, d)
        r = subprocess.run([sys.executable, os.path.join(REPO, XSURFACE), "--dir", d], cwd=REPO, capture_output=True,
                           text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=d))
    got = {}
    for line in r.stdout.splitlines():
        p = line.split()
        if len(p) >= 5 and p[2] == "objections" and p[3] == "canon":
            got[p[0]] = p[4]
    return r.returncode, got


def check(rec, base):
    fails, notes = [], []
    F = lambda tag, msg: fails.append("%s %s" % (tag, msg))
    # G1 ---------------------------------------------------------------
    if list(rec) != HEADER:
        F("G1", "header keys %s" % list(rec))
        return fails, notes
    ids = []
    for i, r in enumerate(rec["rows"]):
        k = r.get("kind")
        if k not in KEYS:
            F("G1", "row %d: kind %r" % (i, k)); continue
        if list(r) != KEYS[k]:
            F("G1", "%s: keys %s" % (r.get("id"), list(r)))
        if r["id"] in ids:
            F("G1", "%s: duplicate id" % r["id"])
        if r.get("supersedes") and r["supersedes"] not in ids:
            F("G1", "%s: supersedes %s, which is not an earlier row" % (r["id"], r["supersedes"]))
        ids.append(r["id"])
    if fails:
        return fails, notes
    # G2 ---------------------------------------------------------------
    q, p = rec["queue"], rec["pinned"]
    try:
        judgment = jload(q["judgment"]["file"], q["judgment"]["md5"])
        for f, m in p["surfaces"].items():
            pinned.bytes_at(REPO, f, m)
        for k in ("map", "rulings"):
            pinned.bytes_at(REPO, p[k]["file"], p[k]["md5"])
        pinned.bytes_at(REPO, q["reading"]["file"], q["reading"]["md5"])
    except (LookupError, KeyError) as e:
        F("G2", str(e))
        return fails, notes
    corpus_raw = pinned.bytes_at(REPO, CORPUS, p["surfaces"][CORPUS])
    corpus = json.loads(corpus_raw.decode("utf-8"))
    corpus_all = corpus_raw.decode("utf-8")
    cur = PATCH.current_rows(rec)
    patching = [r for r in cur if r["kind"] in PATCHING]
    drafts = [r for r in patching if r["status"] == "declared"]
    # G3 ---------------------------------------------------------------
    x032 = next((r for r in judgment["rows"] if r["id"] == "X-032"), None)
    if x032 is None:
        F("G3", "no X-032 row in the pinned judgment")
        return fails, notes
    if sorted(q["loci"]) != sorted(READING.X032):
        F("G3", "the queue's loci are not X-032's six")
    for locus in q["loci"]:
        said = locus if locus in x032["finding"] else None
        if said is None and locus.endswith("#archetypeVariants.sophisticate"):
            said = locus.split("#")[0] + "#long" if "its sophisticate slot" in x032["finding"] else None
        if said is None:
            F("G3", "%s is not named in X-032's text" % locus)
        if not any(r["locus"] == locus for r in drafts):
            F("G3", "%s has no current declared draft" % locus)
    for r in patching:
        if r["kind"] == "draft" and r["locus"] not in q["loci"]:
            F("G3", "%s: a draft outside the queue (%s)" % (r["id"], r["locus"]))
        if r["kind"] != "draft" and r["locus"] in q["loci"]:
            F("G3", "%s: a proposed row at one of the six (%s)" % (r["id"], r["locus"]))
        if r["kind"] == "draft" and r["status"] != "declared":
            F("G3", "%s: a draft whose status is %r" % (r["id"], r["status"]))
        if r["kind"] != "draft" and not r["status"].startswith("proposed"):
            F("G3", "%s: a %s whose status is %r" % (r["id"], r["kind"], r["status"]))
    # G4, G5, G6, G7 ---------------------------------------------------
    by_locus = {}
    for r in patching:
        by_locus.setdefault(r["locus"], []).append(r)
        try:
            t = PATCH.locus_text(corpus, r["locus"])
        except (KeyError, StopIteration):
            F("G4", "%s: no locus %s" % (r["id"], r["locus"])); continue
        if t.count(r["current"]) != 1:
            F("G4", "%s: current text occurs %d times in %s" % (r["id"], t.count(r["current"]), r["locus"]))
        w = {"current": words(r["current"]), "replacement": words(r["replacement"]),
             "delta": words(r["replacement"]) - words(r["current"])}
        if r["words"] != w:
            F("G5", "%s: words %s, computed %s" % (r["id"], r["words"], w))
        rep = r["replacement"]
        if not rep.strip() or rep == r["current"]:
            F("G6", "%s: replacement empty or unchanged" % r["id"])
        elif PATCH.enc(rep) in corpus_all:
            F("G6", "%s: replacement already occurs in the pinned corpus" % r["id"])
        for pat in READING.EXIT:
            if re.search(pat, rep):
                F("G6", "%s: replacement matches gate2's pattern %r" % (r["id"], pat))
        for qq in r["quotes"]:
            try:
                src = quote_source(qq["src"], rec, corpus)
            except (KeyError, StopIteration, ValueError) as e:
                F("G7", "%s: no source %s (%s)" % (r["id"], qq["src"], e)); continue
            if qq["quote"] not in src:
                F("G7", "%s: NOT VERBATIM in %s: %r" % (r["id"], qq["src"], qq["quote"][:70]))
    for locus, rs in by_locus.items():
        t = PATCH.locus_text(corpus, locus)
        if any(t.count(r["current"]) != 1 for r in rs):
            continue
        order = sorted(rs, key=lambda r: t.index(r["current"]))
        for a, b in zip(order, order[1:]):
            if t.index(b["current"]) < t.index(a["current"]) + len(a["current"]):
                F("G4", "%s and %s overlap in %s" % (a["id"], b["id"], locus))
        if [r["part"] for r in order] != list(range(1, len(order) + 1)):
            F("G4", "%s: parts %s are not 1..n in text order" % (locus, [r["id"] for r in order]))
    if fails:
        return fails, notes
    # G8 ---------------------------------------------------------------
    for locus in q["loci"]:
        rs = [r for r in drafts if r["locus"] == locus]
        t = PATCH.locus_text(corpus, locus)
        for r in sorted(rs, key=lambda r: -t.index(r["current"])):
            i = t.index(r["current"])
            t = t[:i] + r["replacement"] + t[i + len(r["current"]):]
        left = [m.group(0) for pat in READING.EXIT for m in re.finditer(pat, t)]
        if left:
            F("G8", "%s: gate2's patterns still match after the declared patch: %s" % (locus, left))
    for r in patching:
        got = sorted({n for n, pat in READING.WIDE if re.search(pat, r["replacement"], flags=re.I)})
        declared = sorted({x["pattern"] for x in r["residual"]})
        if got != declared:
            F("G8", "%s: the wide set matches %s inside the replacement; declared residual %s" % (r["id"], got, declared))
        if any(not x.get("why", "").strip() for x in r["residual"]):
            F("G8", "%s: a residual without its reason" % r["id"])
    # G9 ---------------------------------------------------------------
    for which in ("declared", "all"):
        rows = PATCH.select(rec, which)
        try:
            rc, got = xsurface_canon(rec, rows)
        except ValueError as e:
            F("G9", "%s set: %s" % (which, e)); continue
        if rc != 0 or len(got) != 3 or len(set(got.values())) != 1:
            F("G9", "%s set: xsurface rc %d on the patched surfaces %s" % (which, rc, got))
        else:
            notes.append("%s set: %d rows over %d loci, the three agree at canonical %s" % (
                which, len(rows), len({r["locus"] for r in rows}), list(got.values())[0]))
    # G11 --------------------------------------------------------------
    rats = [r for r in cur if r["kind"] == "ratification"]
    if rats:
        rat = rats[-1]
        by = {r["id"]: r for r in patching}
        bad = [x for x in rat["rows"] if x not in by]
        if bad:
            F("G11", "%s names rows that are not current rows of a patching kind: %s" % (rat["id"], bad))
        missing = [r["id"] for r in drafts if r["id"] not in rat["rows"]]
        if missing:
            F("G11", "%s leaves out current declared drafts %s" % (rat["id"], missing))
        if len(set(rat["rows"])) != len(rat["rows"]):
            F("G11", "%s names a row twice" % rat["id"])
        if not rat["his_words_verbatim"].strip() or not rat["relay"].get("md5") or not rat["judgment"].get("md5"):
            F("G11", "%s lacks his words, the relay or the judgment it answers" % rat["id"])
        else:
            named = [by[x] for x in rat["rows"] if x in by]
            notes.append("%s ratifies %d rows (%s)" % (rat["id"], len(named), ", ".join(
                "%d %s" % (sum(r["kind"] == k for r in named), k) for k in PATCHING)))
    # G10 --------------------------------------------------------------
    if base is not None:
        if {k: base[k] for k in HEADER[:-1]} != {k: rec[k] for k in HEADER[:-1]}:
            F("G10", "the committed header moved")
        n = len(base["rows"])
        if rec["rows"][:n] != base["rows"]:
            F("G10", "a committed row moved (the first %d rows must be HEAD's)" % n)
        notes.append("%d committed rows intact, %d appended" % (n, len(rec["rows"]) - n))
    else:
        notes.append("no committed record yet: every row is new")
    return fails, notes


def knock_on_record(rec):
    w = DOSSIERS.World(rec)
    ko = DOSSIERS.knock_on(w)
    return {"artifact": os.path.basename(KNOCK),
            "record": {"file": REL, "md5": pinned.md5(open(os.path.join(REPO, REL), "rb").read())},
            "map": ko["map"], "rulings": ko["rulings"], "corpus_md5": ko["corpus_md5"], "rows": ko["rows"]}


def self_test(emit=None):
    rec0 = json.load(open(os.path.join(REPO, REL), encoding="utf-8"))
    first = lambda rec, kind="draft": next(r for r in rec["rows"] if r["kind"] == kind)

    def reword(r, rep):
        r["replacement"] = rep
        n, m = len(r["current"].split()), len(rep.split())
        r["words"] = {"current": n, "replacement": m, "delta": m - n}

    def ratify(rec, ids):
        rec["rows"].append({"id": "SR-99", "kind": "ratification", "rows": ids, "his_words_verbatim": "(control)",
                            "said": "(control)", "relay": {"relay": "R0000", "md5": "0" * 32},
                            "judgment": {"file": "(control)", "md5": "0" * 32}, "seat": "control", "date": "control",
                            "supersedes": None})

    def draft_ids(rec):
        return [r["id"] for r in PATCH.current_rows(rec) if r["kind"] == "draft"]

    def m_current(rec):
        first(rec)["current"] = first(rec)["current"].replace("terrifying", "terrifyng")

    def m_uncovered(rec):
        rec["rows"] = [r for r in rec["rows"] if r.get("locus") != "social-contract#long"]

    def m_draft_outside(rec):
        r = next(x for x in rec["rows"] if x["id"] == "SC-04"); r["kind"] = "draft"; r["status"] = "declared"

    def m_words(rec):
        first(rec)["words"]["delta"] += 1

    def m_in_corpus(rec):
        reword(first(rec), "The body vetoes the mind.")

    def m_gate2_pattern(rec):
        reword(first(rec), first(rec)["replacement"] + " It is a trap.")

    def m_undeclared_residual(rec):
        reword(first(rec), first(rec)["replacement"] + " Some who want to die are stopped by nothing but fear.")

    def m_misquote(rec):
        r = next(x for x in rec["rows"] if x.get("quotes")); r["quotes"][0]["quote"] += " (sic)"

    def m_supersedes(rec):
        first(rec)["supersedes"] = "SF-10"

    def m_judgment_pin(rec):
        rec["queue"]["judgment"]["md5"] = "0" * 32

    def m_overlap(rec):
        a = next(r for r in rec["rows"] if r["id"] == "SD-07")
        d = copy.deepcopy(a); d["id"] = "SD-99"; d["part"] = 4
        d["current"] = "The button asks: at what point"
        reword(d, "The button wonders: at which point")
        rec["rows"].insert(rec["rows"].index(a) + 1, d)

    def m_parts(rec):
        next(r for r in rec["rows"] if r["id"] == "SD-06")["part"] = 3

    controls = [
        ("C0", "unmutated record", None, None),
        ("C1", "a current text edited", m_current, "G4"),
        ("C2", "one of the six left without a draft", m_uncovered, "G3"),
        ("C3", "a draft at a locus outside the six", m_draft_outside, "G3"),
        ("C4", "a word count tampered", m_words, "G5"),
        ("C5", "a replacement that already occurs in the corpus", m_in_corpus, "G6"),
        ("C6", "a replacement carrying one of gate2's patterns", m_gate2_pattern, "G6"),
        ("C7", "a replacement matching the wide set, undeclared", m_undeclared_residual, "G8"),
        ("C8", "a declared quote not verbatim", m_misquote, "G7"),
        ("C9", "supersedes names a later row", m_supersedes, "G1"),
        ("C10", "X-032's judgment pinned wrong", m_judgment_pin, "G2"),
        ("C11", "two rows overlapping in one locus", m_overlap, "G4"),
        ("C12", "parts out of text order", m_parts, "G4"),
        ("C13", "a committed row edited", "base", "G10"),
        ("C14", "a ratification leaving a declared draft out", lambda rec: ratify(rec, draft_ids(rec)[:-1]), "G11"),
        ("C15", "a ratification naming a row that is not current", lambda rec: ratify(rec, draft_ids(rec) + ["SD-404"]),
         "G11"),
    ]
    out, ok_all = [], True
    for cid, what, fn, expect in controls:
        rec = copy.deepcopy(rec0)
        base = None
        if fn == "base":
            base = copy.deepcopy(rec0)
            first(rec)["how"] += " (edited after commit)"
        elif fn:
            fn(rec)
        fails, _ = check(rec, base)
        tags = sorted({f.split(" ", 1)[0] for f in fails})
        good = (not fails) if expect is None else (expect in tags)
        ok_all &= good
        out.append({"control": cid, "what": what, "expect": expect or "GREEN", "got": tags or ["GREEN"],
                    "as_expected": good})
        print("  %-4s %-52s expect %-5s got %-12s %s" % (cid, what, expect or "GREEN", ",".join(tags) or "GREEN",
                                                         "ok" if good else "UNEXPECTED"))
        if cid == "C0" and not good:
            for f in fails:
                print("     " + f)
            print("SELF-TEST: the unmutated control failed first; nothing after it means anything")
            return 1
    if emit:
        rec = {"artifact": os.path.basename(emit), "gate": "adversarial_map_staging/r1/sp_drafts_gate_l6.py",
               "gate_md5": pinned.md5(open(os.path.abspath(__file__), "rb").read()),
               "record_md5": pinned.md5(open(os.path.join(REPO, REL), "rb").read()), "controls": out}
        open(emit, "w", encoding="utf-8").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    print("SELF-TEST: %d of %d controls as expected" % (sum(x["as_expected"] for x in out), len(out)))
    return 0 if ok_all else 1


def main():
    if "--self-test" in sys.argv:
        emit = sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None
        sys.exit(self_test(emit))
    rec = json.load(open(os.path.join(REPO, REL), encoding="utf-8"))
    if "--knock-on" in sys.argv:
        ko = knock_on_record(rec)
        out = (json.dumps(ko, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        p = os.path.join(REPO, KNOCK)
        if "--emit" in sys.argv:
            open(p, "wb").write(out)
            print("wrote %s  %s  (%d rows)" % (KNOCK, pinned.md5(out), len(ko["rows"])))
        elif "--check" in sys.argv:
            same = os.path.exists(p) and open(p, "rb").read() == out
            print("KNOCK-ON RECORD: %s" % ("matches the committed record" if same else "DIFFERS"))
            sys.exit(0 if same else 1)
        else:
            sys.stdout.write(out.decode("utf-8"))
        return
    fails, notes = check(rec, committed_base())
    for n in notes:
        print("  " + n)
    for f in fails:
        print("  FAIL " + f)
    print("SP DRAFTS GATE: %s" % ("GREEN" if not fails else "RED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
