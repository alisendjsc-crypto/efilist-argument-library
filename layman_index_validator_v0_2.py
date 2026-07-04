#!/usr/bin/env python3
"""layman_index_validator_v0_2 — K183 (layman_diagnosis field added).
Usage:  python3 layman_index_validator_v0_1.py <layman-index.json> <source-objections-index.json>
        python3 layman_index_validator_v0_1.py --self-test
Checks: (1) id closure vs source index  (2) char bands on decoded strings
        (3) forbidden vocab (destroy*/persuad*/"won the argument for"; bare defeat* blocked,
            negated forms licensed)  (4) T4 gate: T4 win_lines carry no defeat*/routed/remov*/destroy*
        (5) G1 heuristic: identical glosses FAIL, token-overlap >= 0.5 WARN
        (+) source_index_pin must equal md5 of the supplied source index file.
Exit 0 = PASS (warnings allowed), 1 = FAIL."""
import json, re, sys, hashlib

BANDS = {"layman_handle": (1, 40), "layman_trigger": (200, 400),
         "layman_gloss": (100, 200), "layman_win_line": (1, 90),
         "layman_diagnosis": (250, 650)}
FIELDS = list(BANDS)
FORBID = [re.compile(r"\bdestroy\w*\b", re.I), re.compile(r"\bpersuad\w*\b", re.I),
          re.compile(r"won the argument for", re.I)]
DEFEAT = re.compile(r"\bdefeat\w*\b", re.I)
NEGATOR = re.compile(r"\b(not|never|no|isn'?t|wasn'?t|aren'?t|without|un)\W{0,3}$", re.I)
T4GATE = re.compile(r"\b(defeat\w*|routed?|remov\w*|destroy\w*)\b", re.I)
STOP = set("a an the is are was were be been it its of to for on in and or that this "
           "with as not no runs run answer answers on: —".split())

def toks(s):
    return set(w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP)

def bare_defeat(text):
    """True iff a defeat* token appears without a licensing negator immediately before it."""
    for m in DEFEAT.finditer(text):
        if not NEGATOR.search(text[max(0, m.start() - 24):m.start()]):
            return True
    return False

def validate(export, src, pin_ok=None):
    fails, warns = [], []
    tier = {n["id"]: n.get("tier") for n in src["objections"]}
    src_ids = [n["id"] for n in src["objections"]]
    nodes = export.get("nodes", [])
    ids = [n.get("id") for n in nodes]
    if set(ids) != set(src_ids):
        fails.append(f"id closure: export {sorted(set(ids))} != source {sorted(set(src_ids))}")
    if ids != src_ids:
        warns.append("node order differs from source index order")
    if pin_ok is False:
        fails.append("source_index_pin does not match md5 of supplied source index")
    for n in nodes:
        nid = n.get("id", "?")
        for f, (lo, hi) in BANDS.items():
            v = n.get(f)
            if not isinstance(v, str):
                fails.append(f"{nid}.{f}: missing/non-string"); continue
            if not (lo <= len(v) <= hi):
                fails.append(f"{nid}.{f}: len {len(v)} outside [{lo},{hi}]")
        for f in FIELDS:
            v = n.get(f, "")
            if not isinstance(v, str): continue
            for rx in FORBID:
                if rx.search(v):
                    fails.append(f"{nid}.{f}: forbidden vocab '{rx.pattern}'")
            if bare_defeat(v):
                fails.append(f"{nid}.{f}: bare 'defeat*' (negated forms only are licensed)")
        if tier.get(nid) == 4:
            for tf in ("layman_win_line", "layman_diagnosis"):
                v = n.get(tf)
                if isinstance(v, str):
                    m = T4GATE.search(v)
                    if m:
                        fails.append(f"{nid}.{tf}: T4 gate — '{m.group(0)}' not allowed at tier 4")
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

def run(export_path, src_path):
    raw = open(src_path, "rb").read()
    export = json.load(open(export_path)); src = json.loads(raw)
    pin_ok = export.get("source_index_pin") == hashlib.md5(raw).hexdigest()
    fails, warns = validate(export, src, pin_ok)
    for w in warns: print("WARN", w)
    for f in fails: print("FAIL", f)
    print("VERDICT:", "FAIL" if fails else "PASS", f"({len(fails)} fail / {len(warns)} warn)")
    return 1 if fails else 0

def self_test():
    src = {"objections": [{"id": "f1", "tier": 2}, {"id": "f2", "tier": 3}, {"id": "f3", "tier": 4}]}
    def row(i, **kw):
        base = dict(id=f"f{i}", layman_handle=f"handle {i}", layman_trigger="t" * 250,
                    layman_gloss=f"gloss body {i} " + "distinct wording number %d " % i + "x" * 70,
                    layman_win_line=f"win line {i}",
                    layman_diagnosis=f"anatomy {i}: " + chr(97 + i) * 320)
        base.update(kw); return base
    def expect(name, export, want_fail, needle=""):
        fails, _ = validate(export, src, pin_ok=None)
        got = bool(fails)
        hit = (not needle) or any(needle in f for f in fails)
        ok = (got == want_fail) and hit
        print(("ok  " if ok else "BAD "), name, "->", fails if fails else "clean")
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
    r.append(expect("t4-gate",
                    {"nodes": [row(1), row(2), row(3, layman_win_line="the claim is removed")]}, True, "T4 gate"))
    r.append(expect("g1-identical",
                    {"nodes": [row(1, layman_gloss="same gloss " + "y" * 90),
                               row(2, layman_gloss="same gloss " + "y" * 90), row(3)]}, True, "identical"))
    r.append(expect("diagnosis-band",
                    {"nodes": [row(1, layman_diagnosis="too short"), row(2), row(3)]}, True, "outside"))
    r.append(expect("t4-diagnosis-gate",
                    {"nodes": [row(1), row(2),
                               row(3, layman_diagnosis="anatomy 3: the premise is removed " + "d" * 300)]},
                    True, "T4 gate"))
    print("SELF-TEST:", "PASS" if all(r) else "FAIL")
    return 0 if all(r) else 1

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        sys.exit(self_test())
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(run(sys.argv[1], sys.argv[2]))
