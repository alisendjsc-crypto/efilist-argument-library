#!/usr/bin/env python3
"""build_right_to_die_index.py — Right-to-Die objections-index export generator.

Refusal Suite pilot sibling of build_objections_index.py (flagship). A
projection of the corpus OBJECTIONS array into a small, flat, deterministic
interface consumed downstream by wuld.ink site-search. The consumer reads this
contract and NEVER parses the corpus.

GENERATED-ONLY — never hand-edited (same rule as the flagship export). A
hand-edited derived artifact is just a new drift source.

CONTRACT (sibling of flagship Exchange 47/48; bump schema_version on any
breaking shape change so the consumer can detect it):
  shape        : {"schema_version": <int>, "library": "right-to-die",
                  "surface_route": "<route base>",
                  "objections": [ {id, title, gloss}, ... ]}
  surface_route: deep-link base; the consumer builds <surface_route>#obj-<id>
                 (i.e. "right-to-die/combined#obj-<id>"). Self-describing so the
                 wuld.ink consumer need not hard-code each sibling's route.
  id           : corpus objections[].id  — the anchor target  obj-<id>
  title        : corpus objections[].trigger — the displayed objection statement;
                 combined.html renders trigger as the card heading, so a search
                 result title matches its destination.
  gloss        : corpus objections[].diagnosis, whitespace-collapsed and truncated
                 to a GLOSS_MAX-char snippet at a word boundary. Corpus-sourced
                 one-liner, NEVER hand-authored. Omitted for an entry whose
                 diagnosis is empty (consumer treats it as {id,title}).
  bytes        : sorted keys, ensure_ascii=True, compact separators, trailing
                 newline, NO timestamps. Same corpus -> same bytes. md5-gateable.

VALIDATOR (gates the build; exits non-zero on any failure):
  - objection count == corpus["totalEntries"]  (no brittle magic number; the
    library grows, so the guard tracks the corpus's own declared count)
  - export id set == corpus OBJECTIONS id set (exact)
  - objections sorted by id, ids unique, no empty trigger
  - deterministic across two serializations

Usage:
  python3 build_right_to_die_index.py [REPO_ROOT=.] [--out right-to-die-objections-index.json]
  python3 build_right_to_die_index.py --check   # validate only, write nothing
"""
import sys, os, json, glob, argparse

SCHEMA_VERSION = 1
LIBRARY = "right-to-die"
SURFACE_ROUTE = "right-to-die/combined"
GLOSS_MAX = 200
OUT_NAME = "right-to-die-objections-index.json"


def fail(msg):
    sys.stderr.write("RTD-INDEX FAIL: " + msg + "\n")
    sys.exit(1)


def find_corpus(root):
    pats = ["right_to_die_corpus_v*.json", "right_to_die_corpus*.json"]
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


def build(corpus):
    objs = corpus.get("objections")
    if not isinstance(objs, list):
        fail("corpus has no objections[] array")
    out = []
    for o in objs:
        oid = str(o.get("id", "")).strip()
        title = " ".join(str(o.get("trigger", "")).split())
        if not oid:
            fail("objection with empty id")
        if not title:
            fail("objection %r has empty trigger (title source)" % oid)
        rec = {"id": oid, "title": title}
        diag = " ".join(str(o.get("diagnosis", "")).split())
        if diag:
            rec["gloss"] = snippet(diag)
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
