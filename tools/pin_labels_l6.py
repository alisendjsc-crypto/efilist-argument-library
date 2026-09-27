#!/usr/bin/env python3
"""pin_labels_l6.py -- move the release labels with the L6 pin (the X-032 safety pass, a content cut; the K362 law).
pin_labels_l5.py and pin_labels_ld3.py stay as they are: each one's entry text describes its own release.

This moves every label the pin owns, each edit anchored exactly once, from v4.1.4 to the new pin:
  README.md               the pin table (version, md5, size), the libraries row, the 'Stable at' paragraph's opening
                          and its canon file, the canon file named in the integrity and layout paragraphs, the BibTeX
  CITATION.cff            version, date-released
  site/libraries/index.html   the flagship card's 'pinned vX' badge (the one served label)
  CHANGELOG.md            a release entry at the top, with the md5 table and his word verbatim

The new md5 and bytes are read from the working site/combined.html; the old ones must be what the files say now.
The old canon is read from README's 'Stable at' line and must match --old-canon.

  python3 tools/pin_labels_l6.py --version v4.1.5 --date 2026-09-26 --canon 38.39 --old-canon 38.38 --entry E.md
  python3 tools/pin_labels_l6.py --check --version v4.1.5 --canon 38.39
--entry names a file holding the release entry's prose (the paragraphs between the heading and the md5 table), so the
prose is written once, beside the pin that states it, and never cloned from a previous release.
"""
import argparse, hashlib, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OLD = {"version": "v4.1.4", "md5": "ed040cad2f60caaf0cba696af77f860e", "bytes": 2999806, "date": "2026-09-26"}
HISTORY = [("v4.1.0", "72187f6cf0fccdf8e9f4ec6ca5ce009c", 2982770), ("v4.1.1", "f095c0ce0e5a1d796d57fa5a5dd62f7d", 2985989),
           ("v4.1.2", "006aa9833f7a8b103ad27a289ab22fa9", 2987411), ("v4.1.3", "f72e6762173dada604e0fe250e76f810", 2990639),
           ("v4.1.4", "ed040cad2f60caaf0cba696af77f860e", 2999806)]


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


def num(n):
    return "{:,}".format(n)


def cf(v):
    return "project_canon_v%s.json" % v.replace(".", "_")


def entry(ver, date, md5, size, prose):
    table = "\n".join(["| | md5 | bytes |", "|---|---|---|"] +
                      ["| superseded — %s | `%s` | %s |" % (v, m, num(b)) for v, m, b in HISTORY] +
                      ["| **current — %s** | **`%s`** | **%s** |" % (ver, md5, num(size))])
    return "## [%s] — %s\n\n%s\n\n%s\n\n---\n\n" % (ver, date, prose.strip(), table)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--canon", required=True)
    ap.add_argument("--old-canon")
    ap.add_argument("--date")
    ap.add_argument("--entry")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    md5, size = flagship()
    ver, bare = a.version, a.version.lstrip("v")
    if a.check:
        bad = []
        R, C, L, G = rd("README.md"), rd("CITATION.cff"), rd("site/libraries/index.html"), rd("CHANGELOG.md")
        for what, ok in (("README pin version", "| Version (pin) | `%s` |" % ver in R),
                         ("README pin md5", "| md5 | `%s` |" % md5 in R),
                         ("README pin size", "| Size | `%s` bytes |" % num(size) in R),
                         ("README libraries row", "flagship · pinned %s |" % ver in R),
                         ("README stable-at", "**Stable at %s** (canon v%s, file `%s`)" % (ver, a.canon, cf(a.canon)) in R),
                         ("README canon file x3", R.count(cf(a.canon)) == 3),
                         ("README BibTeX", "version = {%s}," % bare in R),
                         ("CITATION version", 'version: "%s"' % bare in C),
                         ("badge", "<span>pinned %s</span>" % ver in L),
                         ("CHANGELOG entry", ("## [%s]" % ver) in G and ("**`%s`**" % md5) in G)):
            print("  %-22s %s" % (what, "ok" if ok else "FAIL"))
            bad += [] if ok else [what]
        print("PIN LABELS: %s" % ("GREEN" if not bad else "RED"))
        sys.exit(1 if bad else 0)
    if not (a.date and a.entry and a.old_canon):
        sys.exit("--date, --entry and --old-canon are required to write")
    if md5 == OLD["md5"]:
        raise SystemExit("ABORT: site/combined.html is still the old pin")
    prose = io.open(a.entry, encoding="utf-8").read()
    if len(prose.strip()) < 200:
        raise SystemExit("ABORT: the release entry's prose is missing or too short")
    R = rd("README.md")
    R = once(R, "| Version (pin) | `%s` |" % OLD["version"], "| Version (pin) | `%s` |" % ver, "README")
    R = once(R, "| md5 | `%s` |" % OLD["md5"], "| md5 | `%s` |" % md5, "README")
    R = once(R, "| Size | `%s` bytes |" % num(OLD["bytes"]), "| Size | `%s` bytes |" % num(size), "README")
    R = once(R, "flagship · pinned %s |" % OLD["version"], "flagship · pinned %s |" % ver, "README")
    R = once(R, "**Stable at %s** (canon v%s, file `%s`). " % (OLD["version"], a.old_canon, cf(a.old_canon)),
             "**Stable at %s** (canon v%s, file `%s`). %s (%s) is a content cut: the safety pass over the passages "
             "that framed the survival drive as a barrier to an exit (see [`CHANGELOG.md`](CHANGELOG.md)). "
             % (ver, a.canon, cf(a.canon), ver, a.date), "README")
    n = R.count(cf(a.old_canon))
    if n != 2:
        raise SystemExit("ABORT: README names %s %d more times, expected 2" % (cf(a.old_canon), n))
    R = R.replace(cf(a.old_canon), cf(a.canon))
    R = once(R, "version = {%s}," % OLD["version"].lstrip("v"), "version = {%s}," % bare, "README")
    C = rd("CITATION.cff")
    C = once(C, 'version: "%s"' % OLD["version"].lstrip("v"), 'version: "%s"' % bare, "CITATION.cff")
    if a.date != OLD["date"]:
        C = once(C, 'date-released: "%s"' % OLD["date"], 'date-released: "%s"' % a.date, "CITATION.cff")
    L = rd("site/libraries/index.html")
    L = once(L, "<span>pinned %s</span>" % OLD["version"], "<span>pinned %s</span>" % ver, "site/libraries/index.html")
    G = rd("CHANGELOG.md")
    k = G.index("---\n\n## ") + len("---\n\n")
    G = G[:k] + entry(ver, a.date, md5, size, prose) + G[k:]
    wr("README.md", R); wr("CITATION.cff", C); wr("site/libraries/index.html", L); wr("CHANGELOG.md", G)
    print("PIN LABELS: %s -> %s  (%s / %s)" % (OLD["version"], ver, md5, num(size)))


if __name__ == "__main__":
    main()
