#!/usr/bin/env python3
"""pin_labels_l5.py -- move the release labels with the pin (L5, 2026-09-26, R0150 phase 5; the K362 law).

K362 found two pin moves that had touched combined.html and the canon only, leaving README, CHANGELOG and the front
door's badge two days stale. This moves every label the pin owns, in one run, each edit anchored exactly once:

  README.md               the pin table (version, md5, size), the libraries row, the 'Stable at' paragraph's opening,
                          the BibTeX version
  CITATION.cff            version, date-released
  site/libraries/index.html   the flagship card's 'pinned vX' badge (the one served label)
  CHANGELOG.md            a release entry at the top, with the md5 table; his words are read from the ratification
                          row of the repair record, never typed here

The new md5 and bytes are read from the working site/combined.html; the old ones must be what the files say now.

  python3 tools/pin_labels_l5.py --version v4.1.3 --date 2026-09-26 [--canonical OLD NEW]   # write
  python3 tools/pin_labels_l5.py --check --version v4.1.3                                  # every label agrees
"""
import argparse, hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RECORD = "adversarial_map_staging/r1/PQ_repair_drafts_L5.json"
OLD = {"version": "v4.1.2", "md5": "006aa9833f7a8b103ad27a289ab22fa9", "bytes": 2987411, "date": "2026-09-18"}
HISTORY = [("v4.1.0", "72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770), ("v4.1.1", "f095c0ce0e5a1d796d57fa5a5dd62f7d", 2985989),
           ("v4.1.2", "006aa9833f7a8b103ad27a289ab22fa9", 2987411)]


def rd(rel):
    return io.open(os.path.join(REPO, rel), encoding="utf-8", newline="").read()


def wr(rel, t):
    io.open(os.path.join(REPO, rel), "w", encoding="utf-8", newline="").write(t)


def once(t, old, new, where):
    n = t.count(old)
    if n != 1:
        raise SystemExit("ABORT: %s: %r occurs %d times, expected 1" % (where, old[:70], n))
    return t.replace(old, new)


def flagship():
    b = open(os.path.join(REPO, "site/combined.html"), "rb").read()
    return hashlib.md5(b).hexdigest(), len(b)


def ratification():
    rec = json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
    sup = {r["supersedes"] for r in rec["rows"] if r.get("supersedes")}
    rats = [r for r in rec["rows"] if r["kind"] == "ratification" and r["id"] not in sup]
    if not rats:
        raise SystemExit("ABORT: no ratification row in %s -- the labels move only after his word" % RECORD)
    rat = rats[-1]
    by = {r["id"]: r for r in rec["rows"]}
    rows = [by[x] for x in rat["rows"]]
    return rat, rows


def num(n):
    return "{:,}".format(n)


def entry(ver, date, md5, size, canonical, rat, rows):
    drafts = [r for r in rows if r["kind"] == "draft"]
    comps = [r for r in rows if r["kind"] == "companion"]
    objs = sorted({r["locus"].split("#")[0] for r in drafts})
    words = sum(r["words"]["delta"] for r in rows)
    table = "\n".join(["| | md5 | bytes |", "|---|---|---|"] +
                      ["| superseded — %s | `%s` | %s |" % (v, m, num(b)) for v, m, b in HISTORY] +
                      ["| **current — %s** | **`%s`** | **%s** |" % (ver, md5, num(size))])
    return (
        "## [%s] — %s\n\n"
        "**PATCH** by the invariants convention (the canon's `invariants` subtree is byte-identical), and **a content "
        "cut**: %d sentences repaired across %d objections, with %d companion sentences beside them, on all three "
        "surfaces at once — the corpus JSON (whose `version` field now reads `%s`, naming the cut), the JSX, and "
        "`site/combined.html`. The cross-surface gate (`tools/xsurface_v4_1_0.py`) moves from `%s` to `%s`, the three "
        "surfaces agreeing at both; both map sidecars regenerate byte for byte from the new flagship. The adversarial "
        "maps stay pinned to the pre-cut corpus (`04bf6482`), as the frozen-map law requires; a successor map "
        "re-anchors the entries whose anchors lay inside a repaired sentence.\n\n"
        "Each repair answers a defect the adversarial map found in the library's own text — a motive read off a thread, "
        "a premise asserted and never argued, a claim wider than its argument, a principle stretched past what it "
        "covers — and follows the repair the map asked for. The text grows by %d words. A session that wrote none of it "
        "judged every sentence; three came back once and were judged again. Josiah ratified it on %s: \"%s\" The "
        "record is `%s`.\n\n%s\n\n---\n\n"
        % (ver, date, len(drafts), len(objs), len(comps), ver.lstrip("v"), canonical[0], canonical[1], words, date,
           rat["his_words_verbatim"], RECORD, table))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--date")
    ap.add_argument("--canonical", nargs=2, metavar=("OLD", "NEW"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    md5, size = flagship()
    ver, bare = a.version, a.version.lstrip("v")
    if a.check:
        bad = []
        R, C, L = rd("README.md"), rd("CITATION.cff"), rd("site/libraries/index.html")
        for what, ok in (("README pin version", "| Version (pin) | `%s` |" % ver in R),
                         ("README pin md5", "| md5 | `%s` |" % md5 in R),
                         ("README pin size", "| Size | `%s` bytes |" % num(size) in R),
                         ("README libraries row", "flagship · pinned %s |" % ver in R),
                         ("README stable-at", "**Stable at %s**" % ver in R),
                         ("README BibTeX", "version = {%s}," % bare in R),
                         ("CITATION version", 'version: "%s"' % bare in C),
                         ("badge", "<span>pinned %s</span>" % ver in L),
                         ("CHANGELOG entry", ("## [%s]" % ver) in rd("CHANGELOG.md") and
                          ("**`%s`**" % md5) in rd("CHANGELOG.md"))):
            print("  %-22s %s" % (what, "ok" if ok else "FAIL"))
            bad += [] if ok else [what]
        print("PIN LABELS: %s" % ("GREEN" if not bad else "RED"))
        sys.exit(1 if bad else 0)
    if not a.date or not a.canonical:
        sys.exit("--date and --canonical OLD NEW are required to write")
    if md5 == OLD["md5"]:
        raise SystemExit("ABORT: site/combined.html is still the old pin; apply the patch first")
    rat, rows = ratification()
    R = rd("README.md")
    R = once(R, "| Version (pin) | `%s` |" % OLD["version"], "| Version (pin) | `%s` |" % ver, "README")
    R = once(R, "| md5 | `%s` |" % OLD["md5"], "| md5 | `%s` |" % md5, "README")
    R = once(R, "| Size | `%s` bytes |" % num(OLD["bytes"]), "| Size | `%s` bytes |" % num(size), "README")
    R = once(R, "flagship · pinned %s |" % OLD["version"], "flagship · pinned %s |" % ver, "README")
    R = once(R, "**Stable at %s** (" % OLD["version"], "**Stable at %s** (" % ver, "README")
    nd = sum(r["kind"] == "draft" for r in rows)
    nc = sum(r["kind"] == "companion" for r in rows)
    R = once(R, "). v4.1.1 and v4.1.2 (both 2026-09-18) moved the pin",
             "). %s (%s) is a content cut: %d sentences repaired where the adversarial map found the library's own text "
             "claiming more than its argument, with %d companion sentences beside them (see [`CHANGELOG.md`](CHANGELOG.md))."
             " v4.1.1 and v4.1.2 (both 2026-09-18) moved the pin" % (ver, a.date, nd, nc), "README")
    R = once(R, "version = {%s}," % OLD["version"].lstrip("v"), "version = {%s}," % bare, "README")
    C = rd("CITATION.cff")
    C = once(C, 'version: "%s"' % OLD["version"].lstrip("v"), 'version: "%s"' % bare, "CITATION.cff")
    C = once(C, 'date-released: "%s"' % OLD["date"], 'date-released: "%s"' % a.date, "CITATION.cff")
    L = rd("site/libraries/index.html")
    L = once(L, "<span>pinned %s</span>" % OLD["version"], "<span>pinned %s</span>" % ver, "site/libraries/index.html")
    G = rd("CHANGELOG.md")
    i = G.index("---\n\n## ") + len("---\n\n")
    G = G[:i] + entry(ver, a.date, md5, size, a.canonical, rat, rows) + G[i:]
    wr("README.md", R); wr("CITATION.cff", C); wr("site/libraries/index.html", L); wr("CHANGELOG.md", G)
    print("PIN LABELS: %s -> %s  (%s / %s)" % (OLD["version"], ver, md5, num(size)))


if __name__ == "__main__":
    main()
