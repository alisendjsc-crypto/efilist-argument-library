#!/usr/bin/env python3
"""pin_patch_l6.py -- the three-surface corpus patch for the X-032 safety pass (L6, 2026-09-26, R0193).

L5's tools/pin_patch_l5.py and pin_patch_l5_v0_2.py stay byte-identical (gate2's judgments pin them). This is the
same whole-locus patch for L6's record, with the record as a parameter and a third row kind, 'widening'.

The patch replaces WHOLE LOCI, not sentences: every affected locus's full text, JSON-encoded as all three surfaces
encode it, occurs exactly once on each surface, while a short span need not. For each locus the rows' replacements are
applied inside the locus text (each current text exactly once there, no two rows overlapping), and the old locus string
is swapped for the new one on the corpus JSON, the JSX and site/combined.html alike.

Which rows: the record's CURRENT rows (none supersedes them) of kind draft, companion or widening, selected by --set:
  declared   drafts only (status 'declared')                                    -- the default
  all        drafts and every proposed companion and widening
  ratified   exactly the rows the newest current ratification row names         -- the pin, once his word is recorded

--corpus-version X also moves the corpus JSON's top-level "version" (it names the CONTENT CUT, K335; the JSX and the
flagship carry none). It must occur exactly once, and nothing else in the file moves with it.

  python3 tools/pin_patch_l6.py --out DIR [--set declared|all|ratified] [--record REL]   # the patched three under DIR
  python3 tools/pin_patch_l6.py --apply --set ratified --corpus-version 4.1.5            # the pin: over the working three

--apply refuses unless the working surfaces are byte-identical to the release the record pins.
"""
import argparse, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/SP_drafts_L6.json"
CORPUS = "efilist_argument_library_v4_0_0.json"
KINDS = ("draft", "companion", "widening")


def enc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def locus_text(corpus, locus):
    oid, loc = locus.split("#")
    o = next(x for x in corpus["objections"] if x["id"] == oid)
    r = o["responses"]
    if loc.startswith("archetypeVariants."):
        return r["archetypeVariants"][loc.split(".", 1)[1]]
    return r[loc] if loc in r else o[loc]


def current_rows(record):
    sup = {r["supersedes"] for r in record["rows"] if r.get("supersedes")}
    return [r for r in record["rows"] if r["id"] not in sup]


def select(record, which):
    rows = [r for r in current_rows(record) if r["kind"] in KINDS]
    if which == "declared":
        return [r for r in rows if r["status"] == "declared"]
    if which == "all":
        return [r for r in rows if r["status"] == "declared" or r["status"].startswith("proposed")]
    if which == "ratified":
        rat = [r for r in current_rows(record) if r["kind"] == "ratification"]
        if not rat:
            return []
        by = {r["id"]: r for r in rows}
        missing = [x for x in rat[-1]["rows"] if x not in by]
        if missing:
            raise ValueError("the ratification names rows that are not current rows of a patching kind: %s" % missing)
        return [by[x] for x in rat[-1]["rows"]]
    raise ValueError(which)


def build(record, rows, repo=REPO, corpus_version=None):
    """Return ({surface: new_text}, {locus: (old_locus_text, new_locus_text)}). Raises on any ambiguity."""
    surf_pins = record["pinned"]["surfaces"]
    corpus = json.loads(pinned.bytes_at(repo, CORPUS, surf_pins[CORPUS]).decode("utf-8"))
    loci = {}
    for r in rows:
        loci.setdefault(r["locus"], []).append(r)
    change = {}
    for locus, rs in loci.items():
        old = locus_text(corpus, locus)
        spans = []
        for r in rs:
            if old.count(r["current"]) != 1:
                raise ValueError("%s: current text occurs %d times in %s" % (r["id"], old.count(r["current"]), locus))
            i = old.index(r["current"])
            spans.append((i, i + len(r["current"]), r))
        spans.sort(key=lambda x: x[0])
        for (a0, a1, ra), (b0, b1, rb) in zip(spans, spans[1:]):
            if b0 < a1:
                raise ValueError("%s and %s overlap in %s" % (ra["id"], rb["id"], locus))
        new = old
        for s0, s1, r in reversed(spans):
            new = new[:s0] + r["replacement"] + new[s1:]
        change[locus] = (old, new)
    out = {}
    for f, m in surf_pins.items():
        t = pinned.bytes_at(repo, f, m).decode("utf-8")
        for locus, (old, new) in change.items():
            o, n = '"%s"' % enc(old), '"%s"' % enc(new)
            if t.count(o) != 1:
                raise ValueError("%s: locus %s occurs %d times" % (f, locus, t.count(o)))
            t = t.replace(o, n)
        for r in rows:
            if t.count(enc(r["current"])) != 0 and r["current"] not in r["replacement"]:
                raise ValueError("%s: %s's current text survives the patch" % (f, r["id"]))
            if t.count(enc(r["replacement"])) != 1:
                raise ValueError("%s: %s's replacement occurs %d times after the patch" % (
                    f, r["id"], t.count(enc(r["replacement"]))))
        if corpus_version and f == CORPUS:
            old_v = json.loads(t)["version"]
            key_old, key_new = '"version": "%s"' % old_v, '"version": "%s"' % corpus_version
            if t.count(key_old) != 1:
                raise ValueError("%s: the version key occurs %d times" % (f, t.count(key_old)))
            t = t.replace(key_old, key_new)
            if json.loads(t)["version"] != corpus_version:
                raise ValueError("%s: the version did not move" % f)
        out[f] = t
    return out, change


def write(out, dest):
    for f, t in out.items():
        p = os.path.join(dest, f)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        io.open(p, "w", encoding="utf-8", newline="").write(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--set", default="declared", choices=["declared", "all", "ratified"])
    ap.add_argument("--record", default=RECORD)
    ap.add_argument("--corpus-version")
    a = ap.parse_args()
    record = json.load(open(os.path.join(REPO, a.record), encoding="utf-8"))
    rows = select(record, a.set)
    if not rows:
        sys.exit("REFUSED: no current rows in set %r" % a.set)
    out, change = build(record, rows, corpus_version=a.corpus_version)
    if a.apply:
        if a.set != "ratified":
            sys.exit("REFUSED: --apply writes only ratified text (--set ratified)")
        for f, m in record["pinned"]["surfaces"].items():
            if pinned.md5(open(os.path.join(REPO, f), "rb").read()) != m:
                sys.exit("REFUSED: %s is not at the md5 %s the record pins" % (f, m))
        write(out, REPO)
        dest = "the working tree"
    elif a.out:
        write(out, a.out)
        dest = a.out
    else:
        sys.exit("--out DIR or --apply")
    for f, t in out.items():
        print("  %-40s %s / %d" % (f, pinned.md5(t.encode("utf-8")), len(t.encode("utf-8"))))
    print("PATCH: set %s, %d rows over %d loci -> %s" % (a.set, len(rows), len(change), dest))


if __name__ == "__main__":
    main()
