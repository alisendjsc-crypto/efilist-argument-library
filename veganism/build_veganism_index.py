#!/usr/bin/env python3
"""build_veganism_index.py — Veganism module objections-index export generator.

Flagship-adjacent MODULE sibling of build_right_to_die_index.py. Projects the
module NODES array into the same small, flat, deterministic interface the
wuld.ink site-search consumer already reads for the suite wings (Exchange 47/48
contract). The consumer reads this contract and NEVER parses the module.

GENERATED-ONLY — never hand-edited (a hand-edited derived artifact is drift).

CONTRACT (identical shape to the wing exports; schema_version 1):
  shape        : {"schema_version": <int>, "library": "veganism",
                  "surface_route": "veganism/combined",
                  "objections": [ {id, title, gloss, keywords}, ... ]}
  source       : module["nodes"]  (the module has no objections[]; it is a
                 flagship-adjacent module, node-shaped, not a suite wing)
  id           : node id — the anchor target  obj-<id>
  title        : node.trigger — the displayed objection statement; combined.html
                 renders trigger as the card heading, so a result title matches
                 its destination.
  gloss        : node.responses.short, whitespace-collapsed + word-boundary
                 truncated to GLOSS_MAX. NOTE the module's `diagnosis` is the
                 objection-PSYCHOLOGY (flagship node shape), NOT the rebuttal, so
                 the gloss is sourced from responses.short (the answer), the
                 analog of the wings' rebuttal-flavored diagnosis. Omitted when
                 empty.
  keywords     : node.keywords, whitespace-collapsed, empties dropped, order
                 preserved. Folded into the consumer's searchable text (K129).
  bytes        : sorted keys, ensure_ascii=True, compact separators, trailing
                 newline, NO timestamps. Same module -> same bytes. md5-gateable.

VALIDATOR (gates the build; exits non-zero on failure):
  - node count == module["node_count"]  (tracks the module's own declared count)
  - export id set == module NODES id set (exact)
  - sorted by id, ids unique, no empty trigger
  - deterministic across two serializations

Usage:
  python3 build_veganism_index.py [REPO_ROOT=.] [--out veganism-objections-index.json]
  python3 build_veganism_index.py --check   # validate only, write nothing
"""
import sys, os, json, glob, argparse

SCHEMA_VERSION = 1
LIBRARY = "veganism"
SURFACE_ROUTE = "veganism/combined"
GLOSS_MAX = 200
OUT_NAME = "veganism-objections-index.json"


def fail(msg):
    sys.stderr.write("VEG-INDEX FAIL: " + msg + "\n")
    sys.exit(1)


def find_module(root):
    for path in sorted(glob.glob(os.path.join(root, "veganism_module_v*.json"))):
        b = os.path.basename(path)
        if any(x in b for x in ("backup", "pre_render")):
            continue
        # skip session sidecars (veganism_module_v0_1.k184.json etc.)
        stem = b[:-len(".json")] if b.endswith(".json") else b
        if "." in stem:  # canonical stem has no dot; sidecars do (".k184")
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
    kws = o.get("keywords")
    if not isinstance(kws, list):
        return []
    out = []
    for k in kws:
        k = " ".join(str(k).split())
        if k:
            out.append(k)
    return out


def build(module):
    nodes = module.get("nodes")
    if not isinstance(nodes, list):
        fail("module has no nodes[] array")
    out = []
    for o in nodes:
        oid = str(o.get("id", "")).strip()
        title = " ".join(str(o.get("trigger", "")).split())
        if not oid:
            fail("node with empty id")
        if not title:
            fail("node %r has empty trigger (title source)" % oid)
        rec = {"id": oid, "title": title}
        resp = o.get("responses") or {}
        short = " ".join(str(resp.get("short", "")).split())
        if short:
            rec["gloss"] = snippet(short)
        kw = project_keywords(o)
        if kw:
            rec["keywords"] = kw
        out.append(rec)
    out.sort(key=lambda r: r["id"])
    return {"schema_version": SCHEMA_VERSION, "library": LIBRARY,
            "surface_route": SURFACE_ROUTE, "objections": out}


def serialize(payload):
    return json.dumps(payload, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def validate(payload, module):
    objs = payload["objections"]
    declared = module.get("node_count")
    if declared is not None and len(objs) != declared:
        fail("count %d != module node_count %s" % (len(objs), declared))
    ids = [r["id"] for r in objs]
    if len(set(ids)) != len(ids):
        fail("duplicate ids in export")
    if ids != sorted(ids):
        fail("export not sorted by id")
    module_ids = sorted(str(o.get("id", "")).strip() for o in module["nodes"])
    if sorted(ids) != module_ids:
        miss = set(module_ids) - set(ids)
        extra = set(ids) - set(module_ids)
        fail("id set != module NODES (missing=%s extra=%s)" % (sorted(miss), sorted(extra)))
    if serialize(payload) != serialize(build(module)):
        fail("non-deterministic serialization")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    mp = find_module(a.root)
    if not mp:
        fail("veganism module json not found under " + repr(a.root))
    module = json.load(open(mp, encoding="utf-8"))
    payload = build(module)
    validate(payload, module)
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
