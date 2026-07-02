#!/usr/bin/env python3
"""veganism_validator_v0_1.py -- veganism module validator (checks V1-V7 per the K180 scaffold check-spec).

Flagship-adjacent module validator. Lineage: v3prime_validator_v1_7.py (2cfb638d) check
families (schema / band / ledger-sync / prose-md5); flagship-locked invariants (81 nodes /
5 tiers / 35 mechanisms, map scalars) STRIPPED per spec -- a young module fails them by
construction. Precedent: abortion_validator_v0_1.py.

Usage:
    python3 veganism_validator_v0_1.py [module.json] [ledger.json]
        (defaults: veganism_module_v0_1.json + veganism_grading_ledger.json, co-located)
    python3 veganism_validator_v0_1.py --self-test

Output: JSON verdict on stdout; exit 0 on PASS, 1 on FAIL.
V2 unused-vocabulary entries WARN while node_count < 5 (recorded, non-fatal), FAIL at >= 5.
"""
import hashlib
import json
import os
import sys

BAND_THRESHOLDS = [("A", 0.88), ("B", 0.82), ("C", 0.76), ("D", 0.0)]
DEPTH_MODIFIERS = {"medium": {"c": -0.05, "r": -0.03}, "short": {"c": -0.12, "r": -0.06}}
AXES = ("v", "s", "c", "r", "a")
REQUIRED_HEADER_FIELDS = ("module", "version", "register", "vocabulary", "node_count", "nodes", "changelog_note")
REQUIRED_NODE_FIELDS = ("id", "tier", "category", "mechanism", "trigger", "keywords",
                        "psychMechanism", "diagnosis", "responses", "sources", "rwe_refs")
DEPTHS = ("short", "medium", "long")
FLAGSHIP_LOCKED_SCALARS = (81, 5, 35)  # nodes / tiers / mechanisms -- must NOT be imported as module invariants


def band_of(g):
    for letter, floor in BAND_THRESHOLDS:
        if g >= floor:
            return letter
    return "D"


def geomean(axes):
    p = 1.0
    for k in AXES:
        p *= axes[k]
    return p ** 0.2


def depth_axes(axes, depth):
    out = dict(axes)
    for k, dv in DEPTH_MODIFIERS.get(depth, {}).items():
        out[k] = max(0.0, out[k] + dv)
    return out


def md5_utf8(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def validate(module, ledger):
    violations = []
    warnings = []
    checks = {}

    # ---- V1 schema ----
    v = []
    for f in REQUIRED_HEADER_FIELDS:
        if f not in module:
            v.append("header missing field '%s'" % f)
    vocab = module.get("vocabulary") or {}
    if not isinstance(vocab.get("tiers"), dict) or not isinstance(vocab.get("mechanisms"), dict):
        v.append("vocabulary must carry dicts 'tiers' and 'mechanisms'")
    nodes = module.get("nodes") or []
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        v.append("node ids not unique")
    for n in nodes:
        nid = n.get("id", "<missing>")
        for f in REQUIRED_NODE_FIELDS:
            if f not in n:
                v.append("node '%s' missing field '%s'" % (nid, f))
        if not (isinstance(nid, str) and nid and all(c.islower() or c.isdigit() or c == "-" for c in nid)):
            v.append("node id '%s' is not a lowercase slug" % nid)
        if not isinstance(n.get("tier"), int):
            v.append("node '%s' tier must be int" % nid)
        resp = n.get("responses") or {}
        for d in DEPTHS:
            if not (isinstance(resp.get(d), str) and resp.get(d).strip()):
                v.append("node '%s' responses.%s empty or missing" % (nid, d))
        if not isinstance(n.get("rwe_refs"), list):
            v.append("node '%s' rwe_refs must be a list" % nid)
    checks["V1_schema"] = {"pass": not v, "violations": v}
    violations += v

    # ---- V2 vocabulary closure ----
    v = []
    tiers = vocab.get("tiers") or {}
    mechs = vocab.get("mechanisms") or {}
    used_tiers, used_mechs = set(), set()
    for n in nodes:
        nid = n.get("id", "<missing>")
        tk = str(n.get("tier"))
        if tk not in tiers:
            v.append("node '%s' tier %s not in vocabulary.tiers" % (nid, tk))
        used_tiers.add(tk)
        mk = n.get("mechanism")
        if mk not in mechs:
            v.append("node '%s' mechanism '%s' not in vocabulary.mechanisms" % (nid, mk))
        used_mechs.add(mk)
    unused = sorted(set(tiers) - used_tiers) + sorted(set(mechs) - used_mechs)
    if unused:
        msg = "unused vocabulary entries: %s" % ", ".join(unused)
        if len(nodes) >= 5:
            v.append(msg + " (FAIL at node_count >= 5)")
        else:
            warnings.append("V2: " + msg + " (WARN while node_count < 5)")
    checks["V2_vocab_closure"] = {"pass": not v, "violations": v}
    violations += v

    # ---- V3 ledger sync ----
    v = []
    grades = ledger.get("grades") or {}
    graded_ids = {k for k, r in grades.items() if isinstance(r, dict) and r.get("graded")}
    ungraded = ledger.get("ungraded")
    if not isinstance(ungraded, list):
        v.append("ledger.ungraded must be a list")
        ungraded = []
    node_ids = set(ids)
    if set(grades) != node_ids:
        v.append("ledger grades keyset != module node id set (grades: %s / nodes: %s)"
                 % (sorted(grades), sorted(node_ids)))
    overlap = graded_ids & set(ungraded)
    if overlap:
        v.append("ids both graded and in ungraded[]: %s" % sorted(overlap))
    not_covered = node_ids - graded_ids - set(ungraded)
    if not_covered:
        v.append("node ids neither graded nor in ungraded[]: %s" % sorted(not_covered))
    checks["V3_ledger_sync"] = {"pass": not v, "violations": v}
    violations += v

    # ---- V4 prose_md5 ----
    v = []
    for n in nodes:
        nid = n.get("id")
        row = grades.get(nid)
        if not (isinstance(row, dict) and isinstance(row.get("prose_md5"), dict)):
            v.append("node '%s' ledger row missing prose_md5 triple" % nid)
            continue
        for d in DEPTHS:
            want = row["prose_md5"].get(d)
            got = md5_utf8((n.get("responses") or {}).get(d, ""))
            if got != want:
                v.append("node '%s' prose_md5.%s drift: ledger %s != recomputed %s" % (nid, d, want, got))
    checks["V4_prose_md5"] = {"pass": not v, "violations": v}
    violations += v

    # ---- V5 band law ----
    v = []
    bt = ledger.get("band_thresholds")
    if isinstance(bt, dict):
        law = {L: f for L, f in BAND_THRESHOLDS}
        if any(abs(bt.get(L, -1) - law[L]) > 1e-12 for L in law):
            v.append("ledger.band_thresholds diverge from the band law %s" % law)
    for nid, row in grades.items():
        if not (isinstance(row, dict) and row.get("graded")):
            continue
        axes = row.get("axes")
        if not (isinstance(axes, dict) and all(k in axes for k in AXES)):
            v.append("row '%s' missing/short axes tuple" % nid)
            continue
        g_long = geomean(axes)
        for d in DEPTHS:
            g = geomean(depth_axes(axes, d))
            cell = row.get(d) or {}
            want_band = band_of(g)
            want_pct = round(g * 100, 1)
            if cell.get("grade") != want_band:
                v.append("row '%s' %s grade %s != band-of-unrounded %s (g=%.6f)"
                         % (nid, d, cell.get("grade"), want_band, g))
            if cell.get("rsi_pct") != want_pct:
                v.append("row '%s' %s rsi_pct %s != round(g*100,1) %s" % (nid, d, cell.get("rsi_pct"), want_pct))
        if row.get("headline_grade_long") != band_of(g_long):
            v.append("row '%s' headline_grade_long %s != long band %s"
                     % (nid, row.get("headline_grade_long"), band_of(g_long)))
    checks["V5_band_law"] = {"pass": not v, "violations": v}
    violations += v

    # ---- V6 counts + flagship-scalar absence ----
    v = []
    if module.get("node_count") != len(nodes):
        v.append("header node_count %s != len(nodes) %s" % (module.get("node_count"), len(nodes)))
    if len(grades) != len(nodes):
        v.append("ledger row count %s != len(nodes) %s" % (len(grades), len(nodes)))
    inv = module.get("invariants")
    if inv is not None:
        blob = json.dumps(inv)
        hits = [s for s in FLAGSHIP_LOCKED_SCALARS if str(s) in blob]
        if hits:
            v.append("flagship-locked scalars present in module invariant block: %s (81/5/35 must not be imported)" % hits)
    checks["V6_counts"] = {"pass": not v, "violations": v}
    violations += v

    return {
        "artifact": "veganism_validator_v0_1",
        "checks": checks,
        "warnings": warnings,
        "violation_count": len(violations),
        "verdict": "PASS" if not violations else "FAIL",
    }


# ---- V7 self-test fixtures ----

def _fixture_good():
    axes = {"v": 0.94, "s": 0.90, "c": 0.90, "r": 0.88, "a": 0.94}
    responses = {"short": "fixture short prose.", "medium": "fixture medium prose.", "long": "fixture long prose."}
    row = {"graded": True, "axes": axes}
    for d in DEPTHS:
        g = geomean(depth_axes(axes, d))
        row[d] = {"rsi_pct": round(g * 100, 1), "grade": band_of(g)}
    row["headline_grade_long"] = band_of(geomean(axes))
    row["note"] = "self-test fixture"
    row["prose_md5"] = {d: md5_utf8(responses[d]) for d in DEPTHS}
    module = {
        "module": "veganism", "version": "0.0.0-selftest",
        "register": "fixture",
        "vocabulary": {"tiers": {"1": {"name": "standing", "gloss": "fixture"}},
                       "mechanisms": {"property-criterion-status-denial": "fixture"}},
        "node_count": 1,
        "nodes": [{"id": "fixture-node", "tier": 1, "category": "standing",
                   "mechanism": "property-criterion-status-denial", "trigger": "fixture trigger",
                   "keywords": ["fixture"], "psychMechanism": "fixture", "diagnosis": "fixture",
                   "responses": responses, "sources": ["fixture"], "rwe_refs": []}],
        "changelog_note": "fixture",
    }
    ledger = {"artifact": "veganism_grading_ledger", "ungraded": [],
              "band_thresholds": {"A": 0.88, "B": 0.82, "C": 0.76, "D": 0.0},
              "grades": {"fixture-node": row}}
    return module, ledger


def self_test():
    module, ledger = _fixture_good()
    good = validate(module, ledger)

    bad_module, bad_ledger = _fixture_good()
    bad_row = bad_ledger["grades"]["fixture-node"]
    bad_row["long"]["grade"] = "B" if bad_row["long"]["grade"] == "A" else "A"  # deliberate mis-band
    bad_row["headline_grade_long"] = bad_row["long"]["grade"]
    bad = validate(bad_module, bad_ledger)
    misband_caught = bad["verdict"] == "FAIL" and any("V5" in x or "band" in x for x in
                                                      [m for m in bad["checks"]["V5_band_law"]["violations"]] or ["x"]) \
        and bad["checks"]["V5_band_law"]["violations"]

    out = {
        "good_fixture_verdict": good["verdict"],
        "good_fixture_violations": good["violation_count"],
        "misband_fixture_verdict": bad["verdict"],
        "misband_caught_by_V5": bool(misband_caught),
        "_overall_pass": good["verdict"] == "PASS" and bool(misband_caught),
    }
    return out


def main(argv):
    if "--self-test" in argv:
        out = self_test()
        print(json.dumps(out, indent=2))
        return 0 if out["_overall_pass"] else 1
    args = [a for a in argv if not a.startswith("--")]
    mod_path = args[0] if len(args) > 0 else "veganism_module_v0_1.json"
    led_path = args[1] if len(args) > 1 else "veganism_grading_ledger.json"
    if not (os.path.exists(mod_path) and os.path.exists(led_path)):
        print("ERROR: module/ledger not found (%s / %s); pass paths or run co-located, or --self-test."
              % (mod_path, led_path), file=sys.stderr)
        return 1
    with open(mod_path, encoding="utf-8") as fh:
        module = json.load(fh)
    with open(led_path, encoding="utf-8") as fh:
        ledger = json.load(fh)
    out = validate(module, ledger)
    print(json.dumps(out, indent=2))
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
