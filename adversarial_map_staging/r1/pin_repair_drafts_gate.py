#!/usr/bin/env python3
"""pin_repair_drafts_gate.py -- the gate for PQ_repair_drafts_L5.json (L5, 2026-09-26, R0150 phase 2).

The record holds the pin session's repair text: one draft per sentence of the queue block it names, proposed
companion sentences, and findings. It is append-only (L2's law: the file lands with its gate).

  G1 schema      header keys; row keys per kind; ids unique; a 'supersedes' names an earlier row
  G2 pins        the canon the record names exists at its md5 (working tree or git); the three surfaces and the
                 map are recoverable at their md5s
  G3 coverage    every sentence of the queue block has exactly one current declared draft, (pq, part) unique
  G4 text        a draft's current text IS the queue's sentence; every current text occurs exactly once in its
                 locus in the pinned corpus; repair_followed and serves are the queue row's own
  G5 words       recorded word counts equal the computed ones
  G6 replacement non-empty, different from the current text, and absent from the pinned corpus
  G7 quotes      every declared quote occurs verbatim in its source, read at the pinned bytes
  G8 patch       tools/pin_patch_l5.py builds the declared set and the set with companions; on each, the three
                 surfaces agree under xsurface's canonical md5, every current text is gone and every
                 replacement occurs exactly once on each surface
  G9 append-only every row committed at HEAD is still there, byte-identical and in order; the header is unchanged

  python3 pin_repair_drafts_gate.py                          # gate the record
  python3 pin_repair_drafts_gate.py --self-test [--emit P]   # controls, the unmutated first
  python3 pin_repair_drafts_gate.py --knock-on [--emit|--check]   # the derived knock-on record

Repo-relative. Writes nothing unless --emit is given.
"""
import copy, glob, importlib.util, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

REL = "adversarial_map_staging/r1/PQ_repair_drafts_L5.json"
KNOCK = "adversarial_map_staging/r1/PQ_knock_on_L5_v0_1.json"
CORPUS = "efilist_argument_library_v4_0_0.json"
HEADER = ["artifact", "state", "law", "kickoff", "queue", "pinned", "rows"]
KEYS = {
    "draft": ["id", "kind", "status", "pq", "part", "locus", "serves", "current", "replacement", "repair_followed",
              "how", "words", "quotes", "seat", "date", "supersedes"],
    "companion": ["id", "kind", "status", "pq", "part", "locus", "serves", "current", "replacement",
                  "repair_followed", "how", "words", "quotes", "seat", "date", "supersedes"],
    "finding": ["id", "kind", "title", "finding", "lean", "seat", "date", "supersedes"],
}


def load_mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


PATCH = load_mod("tools/pin_patch_l5.py", "pin_patch_l5")
XSURFACE = "tools/xsurface_v4_1_0.py"   # run, not imported: it gates at import time


def words(s):
    return len(s.split())


def committed_base():
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + REL], capture_output=True)
    return json.loads(r.stdout.decode("utf-8")) if r.returncode == 0 else None


def canon_queue(rec):
    q = rec["queue"]
    raw = pinned.bytes_at(REPO, q["canon"], q["canon_md5"])
    return json.loads(raw.decode("utf-8"))["adversarial_map"][q["block"]]


def patch_canon(rec, rows):
    """Build the patch for rows in a temp dir and run the cross-surface gate on it (sidecars included, against
    the repo's). Return (rc, {surface: canonical md5})."""
    out, _ = PATCH.build(rec, rows)
    d = tempfile.mkdtemp(prefix="pq_patch_")
    PATCH.write(out, d)
    r = subprocess.run([sys.executable, os.path.join(REPO, XSURFACE), "--dir", d], cwd=REPO, capture_output=True,
                       text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    got = {}
    for line in r.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[2] == "objections" and parts[3] == "canon":
            got[parts[0]] = parts[4]
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
    try:
        queue = canon_queue(rec)
        for f, m in rec["pinned"]["surfaces"].items():
            pinned.bytes_at(REPO, f, m)
        pinned.bytes_at(REPO, rec["pinned"]["map"]["file"], rec["pinned"]["map"]["md5"])
    except (LookupError, KeyError) as e:
        F("G2", str(e))
        return fails, notes
    corpus_md5 = rec["pinned"]["surfaces"][CORPUS]
    corpus = json.loads(pinned.bytes_at(REPO, CORPUS, corpus_md5).decode("utf-8"))
    corpus_all = pinned.bytes_at(REPO, CORPUS, corpus_md5).decode("utf-8")
    cur = PATCH.current_rows(rec)
    drafts = [r for r in cur if r["kind"] == "draft" and r["status"] == "declared"]
    # G3 ---------------------------------------------------------------
    qrows = {q["id"]: q for q in queue["rows"]}
    want = [(q["id"], i + 1) for q in queue["rows"] for i in range(len(q["sentences"]))]
    have = [(r["pq"], r["part"]) for r in drafts]
    for w in want:
        if have.count(w) != 1:
            F("G3", "%s part %d has %d current declared drafts" % (w[0], w[1], have.count(w)))
    for h in have:
        if h not in want:
            F("G3", "%s part %s is not a sentence of %s" % (h[0], h[1], rec["queue"]["block"]))
    # G4, G5, G6, G7 ---------------------------------------------------
    Q = load_mod("adversarial_map_staging/r1/r1_quote_check.py", "r1qc_pq")
    texts = Q.Texts(corpus_md5=corpus_md5)
    for r in [x for x in cur if x["kind"] in ("draft", "companion")]:
        q = qrows.get(r["pq"])
        if q is None:
            F("G4", "%s: pq %s is not in the queue" % (r["id"], r["pq"])); continue
        if r["kind"] == "draft":
            if r["part"] and 1 <= r["part"] <= len(q["sentences"]) and r["current"] != q["sentences"][r["part"] - 1]:
                F("G4", "%s: current text is not %s's sentence %d" % (r["id"], r["pq"], r["part"]))
            if r["serves"] != q["serves"] or r["locus"] != q["locus"]:
                F("G4", "%s: serves or locus differs from %s" % (r["id"], r["pq"]))
        if r["repair_followed"] != q["repair"]:
            F("G4", "%s: repair_followed is not %s's repair" % (r["id"], r["pq"]))
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
        ok, qf = Q.check([dict(x, tag="%s quote" % r["id"]) for x in r["quotes"]], texts)
        for x in qf:
            F("G7", x)
    if fails:
        return fails, notes
    # G8 ---------------------------------------------------------------
    for which in ("declared", "all"):
        rows = PATCH.select(rec, which)
        try:
            rc, got = patch_canon(rec, rows)
        except ValueError as e:
            F("G8", "%s set: %s" % (which, e)); continue
        if rc != 0 or len(got) != 3 or len(set(got.values())) != 1:
            F("G8", "%s set: xsurface rc %d on the patched surfaces %s" % (which, rc, got))
        else:
            notes.append("%s set: %d rows, the three agree at canonical %s" % (which, len(rows), list(got.values())[0]))
    # G9 ---------------------------------------------------------------
    if base is not None:
        if {k: base[k] for k in HEADER[:-1]} != {k: rec[k] for k in HEADER[:-1]}:
            F("G9", "the committed header moved")
        n = len(base["rows"])
        if rec["rows"][:n] != base["rows"]:
            F("G9", "a committed row moved (the first %d rows must be HEAD's)" % n)
        notes.append("%d committed rows intact, %d appended" % (n, len(rec["rows"]) - n))
    else:
        notes.append("no committed record yet: every row is new")
    return fails, notes


def knock_on_record(rec):
    D = load_mod("adversarial_map_staging/r1/pq_dossiers.py", "pqd")
    w = D.World()
    cur = [r for r in PATCH.current_rows(rec) if r["kind"] in ("draft", "companion")
           and (r["status"] == "declared" or r["status"].startswith("proposed"))]
    shaped, pairs = [], {}
    for r in cur:
        key = r["pq"] if r["kind"] == "draft" else r["id"]
        s = next((x for x in shaped if x["id"] == key), None)
        if s is None:
            s = {"id": key, "locus": r["locus"], "sentences": []}
            shaped.append(s)
        s["sentences"].append(r["current"])
        pairs.setdefault(key, []).append({"row": r["id"], "status": r["status"], "old": r["current"],
                                          "new": r["replacement"]})
    ko = D.knock_on(w, shaped)
    for x in ko["rows"]:
        x["repair"] = pairs[x["pq"]]
    ko["record"] = {"file": REL, "md5": pinned.md5(open(os.path.join(REPO, REL), "rb").read())}
    ko["artifact"] = os.path.basename(KNOCK)
    return {k: ko[k] for k in ("artifact", "record", "queue_block", "map", "corpus_md5", "rows")}


def self_test(emit=None):
    rec0 = json.load(open(os.path.join(REPO, REL), encoding="utf-8"))
    first = lambda rec, kind="draft": next(r for r in rec["rows"] if r["kind"] == kind)

    def m_current(rec):
        first(rec)["current"] = first(rec)["current"].replace("reliable", "reliabel")

    def m_repair(rec):
        first(rec)["repair_followed"] += " (edited)"

    def m_missing(rec):
        rec["rows"] = [r for r in rec["rows"] if r["id"] != "PD-18"]

    def m_duplicate(rec):
        d = copy.deepcopy(first(rec)); d["id"] = "PD-99"; rec["rows"].append(d)

    def m_words(rec):
        first(rec)["words"]["delta"] += 1

    def m_replacement_in_corpus(rec):
        r = first(rec); r["replacement"] = "Genuine concern is the rare exception here, not the ordinary case."
        n = len(r["replacement"].split()); r["words"] = {"current": r["words"]["current"], "replacement": n,
                                                          "delta": n - r["words"]["current"]}

    def m_misquote(rec):
        r = next(x for x in rec["rows"] if x.get("quotes")); r["quotes"][0]["quote"] += " (sic)"

    def m_supersedes(rec):
        first(rec)["supersedes"] = "PD-17"

    def m_canon_pin(rec):
        rec["queue"]["canon_md5"] = "0" * 32

    def m_overlap(rec):
        a = next(r for r in rec["rows"] if r["id"] == "PD-17")
        d = copy.deepcopy(a); d["id"] = "PC-99"; d["kind"] = "companion"; d["part"] = None
        d["status"] = "proposed: needs his word to enter the queue"
        d["current"] = a["current"].split(" — ")[0]
        d["replacement"] = "An overlapping companion."
        n = len(d["current"].split()); m = len(d["replacement"].split())
        d["words"] = {"current": n, "replacement": m, "delta": m - n}
        rec["rows"].append(d)

    def m_committed_row(rec):
        return "base"   # the base is the unmutated record; the mutation edits a committed row

    controls = [
        ("C0", "unmutated record", None, None),
        ("C1", "a draft's current text is not the queue's sentence", m_current, "G4"),
        ("C2", "repair_followed edited", m_repair, "G4"),
        ("C3", "a queue sentence left without a draft", m_missing, "G3"),
        ("C4", "two current drafts for one sentence", m_duplicate, "G3"),
        ("C5", "a word count tampered", m_words, "G5"),
        ("C6", "a replacement that already occurs in the corpus", m_replacement_in_corpus, "G6"),
        ("C7", "a declared quote not verbatim", m_misquote, "G7"),
        ("C8", "supersedes names a later row", m_supersedes, "G1"),
        ("C9", "the canon pin is wrong", m_canon_pin, "G2"),
        ("C10", "a companion overlapping a draft's span", m_overlap, "G8"),
        ("C11", "a committed row edited", m_committed_row, "G9"),
    ]
    out, ok_all = [], True
    for cid, what, fn, expect in controls:
        rec = copy.deepcopy(rec0)
        base = None
        if fn is m_committed_row:
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
            print("SELF-TEST: the unmutated control failed first; nothing after it means anything")
            return 1
    if emit:
        rec = {"artifact": os.path.basename(emit), "gate": "adversarial_map_staging/r1/pin_repair_drafts_gate.py",
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
    print("PQ REPAIR DRAFTS GATE: %s" % ("GREEN" if not fails else "RED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
