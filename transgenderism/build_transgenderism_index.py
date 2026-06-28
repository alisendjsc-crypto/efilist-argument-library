#!/usr/bin/env python3
"""build_transgenderism_index.py — Transgenderism objections-index export generator.

Refusal Suite pilot sibling of build_objections_index.py (flagship). A
projection of the corpus OBJECTIONS array into a small, flat, deterministic
interface consumed downstream by wuld.ink site-search. The consumer reads this
contract and NEVER parses the corpus.

GENERATED-ONLY — never hand-edited (same rule as the flagship export). A
hand-edited derived artifact is just a new drift source.

CONTRACT (sibling of flagship Exchange 47/48; bump schema_version on any
breaking shape change so the consumer can detect it):
  shape        : {"schema_version": <int>, "library": "transgenderism",
                  "surface_route": "<route base>",
                  "objections": [ {id, title, gloss, keywords}, ... ]}
  surface_route: deep-link base; the consumer builds <surface_route>#obj-<id>
                 (i.e. "transgenderism/combined#obj-<id>"). Self-describing so the
                 wuld.ink consumer need not hard-code each sibling's route.
  id           : corpus objections[].id  — the anchor target  obj-<id>
  title        : corpus objections[].objection — the displayed objection statement;
                 combined.html renders the objection as the card heading, so a search
                 result title matches its destination.
  gloss        : corpus objections[].diagnosis (or rebuttal.short when absent), collapsed+truncated
                 to a GLOSS_MAX-char snippet at a word boundary. Corpus-sourced
                 one-liner, NEVER hand-authored. Omitted for an entry whose
                 diagnosis is empty (consumer treats it as {id,title}).
  keywords     : corpus objections[].keywords (or move_tags when absent), whitespace-collapsed, empties
                 dropped, corpus order preserved. Additive-optional at
                 schema_version 1 (consumer ignores when absent); omitted when
                 an objection has no keywords. Folded into the consumer's
                 searchable text for keyword recall (K129).
  bytes        : sorted keys, ensure_ascii=True, compact separators, trailing
                 newline, NO timestamps. Same corpus -> same bytes. md5-gateable.

VALIDATOR (gates the build; exits non-zero on any failure):
  - objection count == corpus["totalEntries"]  (no brittle magic number; the
    library grows, so the guard tracks the corpus's own declared count)
  - export id set == corpus OBJECTIONS id set (exact)
  - objections sorted by id, ids unique, no empty trigger
  - deterministic across two serializations

Usage:
  python3 build_transgenderism_index.py [REPO_ROOT=.] [--out transgenderism-objections-index.json]
  python3 build_transgenderism_index.py --check   # validate only, write nothing
"""
import sys, os, json, glob, argparse

SCHEMA_VERSION = 1
LIBRARY = "transgenderism"
SURFACE_ROUTE = "transgenderism/combined"
GLOSS_MAX = 200
OUT_NAME = "transgenderism-objections-index.json"


def fail(msg):
    sys.stderr.write("TRANS-INDEX FAIL: " + msg + "\n")
    sys.exit(1)


def find_corpus(root):
    pats = ["transgenderism_corpus_v*.json", "transgenderism_corpus*.json"]
    for pat in pats:
        for path in sorted(glob.glob(os.path.join(root, pat))):
            b = os.path.basename(path)
            if any(x in b for x in ("backup", "pre_render")):
                continue
            return path
    return None


def snippet(s, n=GLOSS_MAX):
    s = " ".join(str(s or "").split())
    if len(s) <= n:
        return s
    cut = s[:n]
    sp = cut.rfind(" ")
    if sp > int(n * 0.6):
        cut = cut[:sp]
    return cut.rstrip(" ,;:") + "…"


def project_keywords(o):
    """corpus objections[].keywords -> list of whitespace-collapsed, non-empty
    strings, corpus order preserved (authored salience). Faithful projection:
    no sort, no dedupe; the corpus is authoritative. Absent/!list -> []."""
    kws = o.get("keywords")
    if not isinstance(kws, list):
        kws = o.get("move_tags")
    if not isinstance(kws, list):
        return []
    out = []
    for k in kws:
        k = " ".join(str(k).split())
        if k:
            out.append(k)
    return out


def build(corpus):
    objs = corpus.get("objections")
    if not isinstance(objs, list):
        fail("corpus has no objections[] array")
    out = []
    for o in objs:
        oid = str(o.get("id", "")).strip()
        title = " ".join(str(o.get("objection", o.get("trigger", ""))).split())
        if not oid:
            fail("objection with empty id")
        if not title:
            fail("objection %r has empty objection text (title source)" % oid)
        rec = {"id": oid, "title": title}
        gsrc = o.get("diagnosis") or ((o.get("rebuttal") or {}).get("short", ""))
        gsrc = " ".join(str(gsrc).split())
        if gsrc:
            rec["gloss"] = snippet(gsrc)
        kw = project_keywords(o)
        if kw:
            rec["keywords"] = kw
        out.append(rec)
    out.sort(key=lambda r: r["id"])
    return {"schema_version": SCHEMA_VERSION, "library": LIBRARY,
            "surface_route": SURFACE_ROUTE, "objections": out}


def validate(payload, corpus):
    objs = payload["objections"]
    declared = corpus.get("totalEntries")
    if declared is not None and len(objs) != declared:
        fail("count %d != corpus totalEntries %s" % (len(objs), declared))
    ids = [r["id"] for r in objs]
    if len(set(ids)) != len(ids):
        fail("duplicate ids in export")
    if ids != sorted(ids):
        fail("export not sorted by id")
    corpus_ids = sorted(str(o.get("id", "")).strip() for o in corpus["objections"])
    if sorted(ids) != corpus_ids:
        miss = set(corpus_ids) - set(ids)
        extra = set(ids) - set(corpus_ids)
        fail("id set != corpus OBJECTIONS (missing=%s extra=%s)" % (sorted(miss), sorted(extra)))
    b1 = serialize(payload)
    b2 = serialize(build(corpus))
    if b1 != b2:
        fail("non-deterministic serialization")


def serialize(payload):
    return json.dumps(payload, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    corpus_p = find_corpus(a.root)
    if not corpus_p:
        fail("corpus json not found under " + repr(a.root))
    corpus = json.load(open(corpus_p, encoding="utf-8"))
    payload = build(corpus)
    validate(payload, corpus)
    blob = serialize(payload)
    if a.check:
        sys.stderr.write("OK check: %d objections, %d bytes, deterministic\n"
                         % (len(payload["objections"]), len(blob.encode())))
        return
    out = a.out or os.path.join(a.root, OUT_NAME)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(blob)
    sys.stderr.write("wrote %s  objections=%d  bytes=%d  schema_version=%d\n"
                     % (out, len(payload["objections"]), len(blob.encode()), SCHEMA_VERSION))


if __name__ == "__main__":
    main()
