#!/usr/bin/env python3
"""layman_index_validator_v0_3 — K199 (wing-parametric).

Usage:
  python3 layman_index_validator_v0_3.py <layman-index.json> <objections-index.json> <tier-source-corpus.json>
                                         [--dissolve-tiers 4] [--warn-tiers 5]
  python3 layman_index_validator_v0_3.py --self-test

What changed vs v0_2 (a7083044):
  * field_bands are read from the layman index's own `field_bands` block (fallback to the built-in
    defaults if absent). No wing hardcode.
  * tier is read from a REQUIRED third argument, the wing corpus/module (objections[] or nodes[]),
    NOT the tierless objections-index. v0_2's dissolve-defang gate was INERT — the objections-index
    carries only {gloss,id,keywords,title}, so `n.get("tier")` was always None and the gate never
    fired. It now fires against real node ids.
  * DISSOLVE_TIERS  (hard-fail set, default {4} = Genuine-Philosophical — charter-defined
    dissolves-but-does-not-defeat / remains-standing register) and
    DISSOLVE_WARN_TIERS (soft-warn set, default {5} = Meta-Objection — surfaced for per-node review,
    not hard-blocked, because the meta tier is not charter-guaranteed dissolve-defang).
    Both CLI-overridable; a tier in both sets is treated as hard-fail (dissolve wins).
  * tier-source COVERAGE gate: every index id must resolve to a tier in the source. A stale or
    wrong --tier-source can no longer silently disable the dissolve gate.

Exit 0 = PASS (warnings allowed), 1 = FAIL."""
import json, re, sys, hashlib, argparse

DEFAULT_BANDS = {"layman_handle": (1, 40), "layman_trigger": (200, 400),
                 "layman_gloss": (100, 200), "layman_win_line": (1, 90),
                 "layman_diagnosis": (250, 650)}
FIELDS = list(DEFAULT_BANDS)
FORBID = [re.compile(r"\bdestroy\w*\b", re.I), re.compile(r"\bpersuad\w*\b", re.I),
          re.compile(r"won the argument for", re.I)]
DEFEAT = re.compile(r"\bdefeat\w*\b", re.I)
NEGATOR = re.compile(r"\b(not|never|no|isn'?t|wasn'?t|aren'?t|without|un)\W{0,3}$", re.I)
DISSOLVE_GATE = re.compile(r"\b(defeat\w*|routed?|remov\w*|destroy\w*)\b", re.I)
STOP = set("a an the is are was were be been it its of to for on in and or that this "
           "with as not no runs run answer answers on: —".split())
DEFAULT_DISSOLVE_TIERS = {4}
DEFAULT_WARN_TIERS = {5}


def toks(s):
    return set(w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP)


def bare_defeat(text):
    """True iff a defeat* token appears with no licensing negator immediately before it."""
    for m in DEFEAT.finditer(text):
        if not NEGATOR.search(text[max(0, m.start() - 24):m.start()]):
            return True
    return False


def node_list(d):
    """The list of nodes in a wing corpus/module — objections[] (wings) or nodes[] (module)."""
    for k in ("objections", "nodes"):
        if isinstance(d.get(k), list):
            return d[k]
    for v in d.values():
        if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
            return v
    return []


def parse_bands(export):
    """field_bands from the index; coerce [lo,hi] / (lo,hi) / {min,max}|{lo,hi}. Fallback to defaults."""
    fb = export.get("field_bands")
    out = dict(DEFAULT_BANDS)
    if not isinstance(fb, dict):
        return out
    for f, spec in fb.items():
        if isinstance(spec, (list, tuple)) and len(spec) == 2:
            out[f] = (int(spec[0]), int(spec[1]))
        elif isinstance(spec, dict):
            lo = spec.get("min", spec.get("lo"))
            hi = spec.get("max", spec.get("hi"))
            if lo is not None and hi is not None:
                out[f] = (int(lo), int(hi))
    return out


def tier_map_from_source(src_corpus):
    """{id: int(tier)} from the wing corpus/module (tier coerced to int; None kept as None)."""
    m = {}
    for n in node_list(src_corpus):
        nid = n.get("id")
        if nid is None:
            continue
        t = n.get("tier")
        m[nid] = int(t) if t is not None else None
    return m


def validate(export, src_index, tier_map, dissolve_tiers, warn_tiers, bands, pin_ok=None):
    fails, warns = [], []
    src_ids = [n["id"] for n in src_index["objections"]]
    nodes = export.get("nodes", [])
    ids = [n.get("id") for n in nodes]
    if set(ids) != set(src_ids):
        fails.append(f"id closure: export {sorted(set(ids))} != source {sorted(set(src_ids))}")
    if ids != src_ids:
        warns.append("node order differs from source index order")
    if pin_ok is False:
        fails.append("source_index_pin does not match md5 of supplied objections-index")

    # tier-source coverage: every id must resolve, else the dissolve gate silently no-ops
    for nid in ids:
        if nid not in tier_map:
            fails.append(f"tier-source: id '{nid}' absent from --tier-source (dissolve gate would no-op)")
        elif tier_map[nid] is None:
            fails.append(f"tier-source: id '{nid}' has no tier in --tier-source")

    for n in nodes:
        nid = n.get("id", "?")
        for f, (lo, hi) in bands.items():
            v = n.get(f)
            if not isinstance(v, str):
                fails.append(f"{nid}.{f}: missing/non-string"); continue
            if not (lo <= len(v) <= hi):
                fails.append(f"{nid}.{f}: len {len(v)} outside [{lo},{hi}]")
        for f in FIELDS:
            v = n.get(f, "")
            if not isinstance(v, str):
                continue
            for rx in FORBID:
                if rx.search(v):
                    fails.append(f"{nid}.{f}: forbidden vocab '{rx.pattern}'")
            if bare_defeat(v):
                fails.append(f"{nid}.{f}: bare 'defeat*' (negated forms only are licensed)")
        t = tier_map.get(nid)
        if t in dissolve_tiers or t in warn_tiers:
            for tf in ("layman_win_line", "layman_diagnosis"):
                v = n.get(tf)
                if isinstance(v, str):
                    m = DISSOLVE_GATE.search(v)
                    if m:
                        msg = (f"{nid}.{tf}: dissolve gate (T{t}) — '{m.group(0)}' "
                               f"not allowed for a dissolve/meta node")
                        (fails if t in dissolve_tiers else warns).append(msg)

    for field in ("layman_gloss", "layman_diagnosis"):
        rows = [(n.get("id"), n.get(field, "")) for n in nodes if isinstance(n.get(field), str)]
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                (a, ga), (b, gb) = rows[i], rows[j]
                if ga.strip() == gb.strip():
                    fails.append(f"G1[{field}]: identical {a} == {b}"); continue
                ta, tb = toks(ga), toks(gb)
                jac = len(ta & tb) / max(1, len(ta | tb))
                if jac >= 0.5:
                    warns.append(f"G1[{field}]: high overlap {a}~{b} (jaccard {jac:.2f})")
    return fails, warns


def run(export_path, src_path, tier_path, dissolve_tiers, warn_tiers):
    raw = open(src_path, "rb").read()
    export = json.load(open(export_path))
    src = json.loads(raw)
    tier_corpus = json.load(open(tier_path))
    tier_map = tier_map_from_source(tier_corpus)
    bands = parse_bands(export)
    pin_ok = export.get("source_index_pin") == hashlib.md5(raw).hexdigest()
    fails, warns = validate(export, src, tier_map, dissolve_tiers, warn_tiers, bands, pin_ok)
    for w in warns:
        print("WARN", w)
    for f in fails:
        print("FAIL", f)
    ids = [n.get("id") for n in export.get("nodes", [])]
    ndiss = sum(1 for i in ids if tier_map.get(i) in dissolve_tiers)
    nwarn = [i for i in ids if tier_map.get(i) in warn_tiers]
    print(f"[bands from index: {'yes' if export.get('field_bands') else 'defaults'} | "
          f"dissolve_tiers={sorted(dissolve_tiers)} warn_tiers={sorted(warn_tiers)} | "
          f"hard-gated nodes={ndiss}]")
    if nwarn:
        print(f"[warn-tier nodes (soft-gated, review): {nwarn}]")
    print("VERDICT:", "FAIL" if fails else "PASS", f"({len(fails)} fail / {len(warns)} warn)")
    return 1 if fails else 0


def self_test():
    # objections-index is TIERLESS (real shape); tier comes from a separate map — the fork's point.
    src = {"objections": [{"id": "f1"}, {"id": "f2"}, {"id": "f3"}]}
    tmap = {"f1": 2, "f2": 3, "f3": 4}          # f3 = a T4 dissolve node
    tmap5 = {"f1": 2, "f2": 3, "f3": 5}         # f3 promoted to T5 (meta) for the warn leg
    bands = dict(DEFAULT_BANDS)

    def row(i, **kw):
        base = dict(id=f"f{i}", layman_handle=f"handle {i}", layman_trigger="t" * 250,
                    layman_gloss=f"gloss body {i} " + "distinct wording number %d " % i + "x" * 70,
                    layman_win_line=f"win line {i}",
                    layman_diagnosis=f"anatomy {i}: " + chr(97 + i) * 320)
        base.update(kw)
        return base

    def expect(name, export, want_fail, needle="", tm=None, dt=None, wt=None, want_warn=None):
        tm = tmap if tm is None else tm
        dt = DEFAULT_DISSOLVE_TIERS if dt is None else dt
        wt = DEFAULT_WARN_TIERS if wt is None else wt
        fails, warns = validate(export, src, tm, dt, wt, bands, pin_ok=None)
        got = bool(fails)
        pool = fails if want_warn is None else fails + warns
        hit = (not needle) or any(needle in f for f in pool)
        okw = (want_warn is None) or (bool(warns) == want_warn)
        ok = (got == want_fail) and hit and okw
        print(("ok  " if ok else "BAD "), name, "-> F:", fails or "clean", "| W:", warns or "-")
        return ok

    r = []
    r.append(expect("clean", {"nodes": [row(1), row(2), row(3)]}, False))
    r.append(expect("licensed-negated-defeat",
                    {"nodes": [row(1), row(2, layman_win_line="dissolved, not defeated"), row(3)]}, False))
    r.append(expect("id-closure", {"nodes": [row(1), row(2)]}, True, "id closure"))
    r.append(expect("char-band", {"nodes": [row(1, layman_handle="h" * 41), row(2), row(3)]}, True, "outside"))
    r.append(expect("forbidden-destroy",
                    {"nodes": [row(1, layman_trigger=("z" * 240) + " destroyed "), row(2), row(3)]}, True, "forbidden"))
    r.append(expect("bare-defeat",
                    {"nodes": [row(1), row(2, layman_win_line="the objection is defeated"), row(3)]}, True, "bare"))
    # THE fork's headline leg: the T4 dissolve gate fires from the TIER MAP (not the tierless src).
    r.append(expect("tier-source-t4-fires",
                    {"nodes": [row(1), row(2), row(3, layman_win_line="the claim is routed")]}, True, "dissolve gate"))
    r.append(expect("t4-diagnosis-gate",
                    {"nodes": [row(1), row(2),
                               row(3, layman_diagnosis="anatomy 3: the premise is removed " + "d" * 300)]},
                    True, "dissolve gate"))
    # T5 meta node with gate-vocab under default {warn:5} -> WARN, not FAIL.
    r.append(expect("t5-meta-warns",
                    {"nodes": [row(1), row(2), row(3, layman_win_line="the meta-worry is routed")]},
                    False, "dissolve gate (T5)", tm=tmap5, want_warn=True))
    # tier-source coverage: an id absent from the source -> FAIL (gate can't silently no-op).
    r.append(expect("tier-source-missing-id",
                    {"nodes": [row(1), row(2), row(3)]}, True, "absent from --tier-source",
                    tm={"f1": 2, "f2": 3}))
    r.append(expect("g1-identical",
                    {"nodes": [row(1, layman_gloss="same gloss " + "y" * 90),
                               row(2, layman_gloss="same gloss " + "y" * 90), row(3)]}, True, "identical"))
    r.append(expect("diagnosis-band",
                    {"nodes": [row(1, layman_diagnosis="too short"), row(2), row(3)]}, True, "outside"))
    print("SELF-TEST:", "PASS" if all(r) else "FAIL")
    return 0 if all(r) else 1


def main():
    ap = argparse.ArgumentParser(description="layman index validator v0_3 (wing-parametric)")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("layman", nargs="?")
    ap.add_argument("objections", nargs="?")
    ap.add_argument("tier_source", nargs="?")
    ap.add_argument("--dissolve-tiers", default="4")
    ap.add_argument("--warn-tiers", default="5")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not (a.layman and a.objections and a.tier_source):
        ap.error("need: <layman-index> <objections-index> <tier-source-corpus>  (or --self-test)")
    dt = set(int(x) for x in a.dissolve_tiers.split(",") if x.strip())
    wt = set(int(x) for x in a.warn_tiers.split(",") if x.strip()) - dt   # dissolve wins over warn
    return run(a.layman, a.objections, a.tier_source, dt, wt)


if __name__ == "__main__":
    sys.exit(main())
