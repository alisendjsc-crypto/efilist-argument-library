#!/usr/bin/env python3
"""right_to_die_validator_v0_1.py — Right-to-Die corpus/ledger/export validator.

Refusal Suite pilot sibling of v3prime_validator_v1_7.py (flagship), reusing its
harness idiom: pure check functions returning structured violations, synthetic
fixtures proving each check fires/passes, and a live leg over the real seed
artifacts. Near-trivial at launch (a 2-stub corpus, an empty ledger) — expected;
it grows with authored content.

CHECKS:
  1. schema validity      — corpus shape + required node fields + count/response
                            self-consistency + access_basis allowed-values (when present).
  2. anchor uniqueness    — objection ids unique AND anchor-safe (^[a-z0-9][a-z0-9-]*$);
                            ids are the append-only deep-link targets (obj-<id>).
  3. ledger<->corpus sync — every graded/ungraded id exists in the corpus and is
                            not a stub; every NON-stub corpus id is graded-or-ungraded;
                            ledger band_thresholds == canonical thresholds.
  4. band<->geomean       — RSI integrity: geomean == (v*s*c*r*a)^(1/5); each
                            per-depth grade bands its UNROUNDED rsi fraction
                            (rsi_pct is 1dp display-only); headline == long grade.
  5. export determinism   — build the index twice via build_right_to_die_index;
                            byte-identical; id-set == corpus.
  6. rwe referential integ— RWE instance_ids unique; every attached_objections[].
                            objection_id resolves to a corpus objection id; every
                            objection.rwe_refs[] resolves to an RWE instance_id.
                            VACUOUS while realWorldExamples == [] (engages on data).
  7. keyword projection   — every objection's corpus keywords[] project into the
                            export non-empty + corpus-order-preserved (the
                            project_keywords contract); guards the K129 cadence-
                            lock: a stale generator dropping keywords fails LOUD
                            here, not silently in search recall.


Change-order (library-Claude, 2026-06-22): node field `mechanisms[]` -> `strands[]`;
optional `access_basis` in {universal,gated,both} (compensation fork 3); RWE schema
vendored at right_to_die_rwe_schema_v0_1.json.
Strand-vocabulary covenant (library-Claude, 2026-06-24): node field `strands[]` -> `move_tags[]`
(per-node field holds granular move-tags, not the 4 charter strands; top-level `strands` reserved).

Usage:
  python3 right_to_die_validator_v0_1.py --self-test     # synthetic + live, JSON, 0/1
  python3 right_to_die_validator_v0_1.py <corpus.json>   # validate one corpus file
"""
import sys, os, json, re, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
CANON_THRESHOLDS = {"A": 0.88, "B": 0.82, "C": 0.76, "D": 0.0}
ACCESS_BASIS_VALUES = {"universal", "gated", "both"}
RWE_POLARITY_VALUES = {"response-supporting", "objector-weaponized", "neutral-illustration", "contested"}
RWE_SUBJECT_TYPES = {"real-person", "structural", "category"}
RWE_ATTESTATION_VALUES = {"public-record", "published-case", "subject-public-testimony", "family-attested-public", "unverified"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REQUIRED_NODE_FIELDS = ["id", "tier", "category", "trigger", "keywords",
                        "move_tags", "diagnosis", "responses", "rwe_refs"]
DEPTHS = ("short", "medium", "long")
ROUND_TOL = 0.0005   # half of a 0.1% display step — the rsi_pct rounding band


def _v(check, msg, oid=None):
    return {"check": check, "id": oid, "msg": msg}


# ----------------------------------------------------------------------------- checks
def check_schema(corpus):
    out = []
    if not isinstance(corpus, dict):
        return [_v("schema", "corpus is not an object")]
    objs = corpus.get("objections")
    if not isinstance(objs, list):
        return [_v("schema", "corpus has no objections[] array")]
    declared = corpus.get("totalEntries")
    if declared is not None and declared != len(objs):
        out.append(_v("schema", "totalEntries %r != len(objections) %d" % (declared, len(objs))))
    resp_count = 0
    for o in objs:
        oid = (o.get("id") if isinstance(o, dict) else None)
        if not isinstance(o, dict):
            out.append(_v("schema", "objection is not an object", oid))
            continue
        for f in REQUIRED_NODE_FIELDS:
            if f not in o:
                out.append(_v("schema", "missing field %r" % f, oid))
        if not str(o.get("id", "")).strip():
            out.append(_v("schema", "empty id", oid))
        if not str(o.get("trigger", "")).strip():
            out.append(_v("schema", "empty trigger", oid))
        if not isinstance(o.get("tier"), int):
            out.append(_v("schema", "tier not an int", oid))
        for f in ("keywords", "move_tags", "rwe_refs"):
            if f in o and not isinstance(o[f], list):
                out.append(_v("schema", "%s not a list" % f, oid))
        ab = o.get("access_basis")
        if ab is not None and ab not in ACCESS_BASIS_VALUES:
            out.append(_v("schema", "access_basis %r not in {universal,gated,both}" % ab, oid))
        r = o.get("responses")
        if not isinstance(r, dict) or any(k not in r for k in DEPTHS):
            out.append(_v("schema", "responses missing short/medium/long", oid))
        else:
            resp_count += sum(1 for k in DEPTHS if str(r.get(k, "")).strip())
    tr = corpus.get("totalResponses")
    if tr is not None and tr != resp_count:
        out.append(_v("schema", "totalResponses %r != non-empty response count %d" % (tr, resp_count)))
    return out


def check_anchor_uniqueness(corpus):
    out = []
    objs = corpus.get("objections", []) if isinstance(corpus, dict) else []
    seen = {}
    for o in objs:
        oid = str((o or {}).get("id", "")).strip()
        if not oid:
            continue
        if oid in seen:
            out.append(_v("anchor", "duplicate id (anchor collision)", oid))
        seen[oid] = True
        if not ID_RE.match(oid):
            out.append(_v("anchor", "id not anchor-safe (^[a-z0-9][a-z0-9-]*$)", oid))
    return out


def _is_stub(o):
    return bool((o or {}).get("_stub"))


def check_ledger_corpus_sync(corpus, ledger):
    out = []
    objs = corpus.get("objections", []) if isinstance(corpus, dict) else []
    corpus_ids = {str(o.get("id", "")).strip() for o in objs}
    stub_ids = {str(o.get("id", "")).strip() for o in objs if _is_stub(o)}
    gradeable = corpus_ids - stub_ids
    grades = (ledger or {}).get("grades", {}) or {}
    ungraded = set((ledger or {}).get("ungraded", []) or [])
    for gid in grades:
        if gid not in corpus_ids:
            out.append(_v("sync", "graded id not in corpus", gid))
        elif gid in stub_ids:
            out.append(_v("sync", "stub id must not be graded", gid))
    for uid in ungraded:
        if uid not in corpus_ids:
            out.append(_v("sync", "ungraded id not in corpus", uid))
    covered = set(grades) | ungraded
    for cid in gradeable - covered:
        out.append(_v("sync", "gradeable objection neither graded nor in ungraded[]", cid))
    thr = (ledger or {}).get("band_thresholds")
    if thr is not None and thr != CANON_THRESHOLDS:
        out.append(_v("sync", "ledger band_thresholds != canonical %r" % CANON_THRESHOLDS))
    return out


def geomean5(axes):
    try:
        vals = [float(axes[k]) for k in ("v", "s", "c", "r", "a")]
    except (KeyError, TypeError, ValueError):
        return None
    if any(x < 0 for x in vals):
        return None
    p = 1.0
    for x in vals:
        p *= x
    return p ** 0.2


def band(frac, thr=CANON_THRESHOLDS):
    if frac >= thr["A"]:
        return "A"
    if frac >= thr["B"]:
        return "B"
    if frac >= thr["C"]:
        return "C"
    return "D"


def _band_ambiguous(frac, thr=CANON_THRESHOLDS):
    # True if a band threshold falls inside the display-rounding interval, so a
    # grade disagreeing with band(frac) is explained by rsi_pct rounding, not error.
    return any(abs(frac - t) <= ROUND_TOL for t in thr.values() if t > 0)


def check_band_geomean(corpus, ledger):
    out = []
    grades = (ledger or {}).get("grades", {}) or {}
    thr = (ledger or {}).get("band_thresholds") or CANON_THRESHOLDS
    for gid, g in grades.items():
        if not isinstance(g, dict):
            out.append(_v("band", "grade entry not an object", gid))
            continue
        axes = g.get("axes")
        gm = geomean5(axes) if axes is not None else None
        if "geomean" in g and gm is not None and abs(float(g["geomean"]) - gm) > 1e-6:
            out.append(_v("band", "geomean %r != (v*s*c*r*a)^(1/5)=%.6f" % (g["geomean"], gm), gid))
        for depth in DEPTHS:
            dd = g.get(depth)
            if not isinstance(dd, dict):
                out.append(_v("band", "missing depth block %r" % depth, gid))
                continue
            grade = dd.get("grade")
            if grade not in ("A", "B", "C", "D"):
                out.append(_v("band", "%s grade %r not in A/B/C/D" % (depth, grade), gid))
                continue
            pct = dd.get("rsi_pct")
            if isinstance(pct, (int, float)):
                frac = float(pct) / 100.0
                if band(frac, thr) != grade and not _band_ambiguous(frac, thr):
                    out.append(_v("band", "%s grade %s disagrees with band(%.4f)=%s"
                                  % (depth, grade, frac, band(frac, thr)), gid))
        long_block = g.get("long") if isinstance(g.get("long"), dict) else {}
        if "headline_grade_long" in g and g["headline_grade_long"] != long_block.get("grade"):
            out.append(_v("band", "headline_grade_long != long.grade", gid))
    return out


def check_export_determinism(corpus):
    out = []
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        mod = importlib.import_module("build_right_to_die_index")
    except Exception as e:  # pragma: no cover
        return [_v("export", "cannot import build_right_to_die_index: %r" % e)]
    try:
        b1 = mod.serialize(mod.build(corpus))
        b2 = mod.serialize(mod.build(corpus))
    except SystemExit as e:
        return [_v("export", "build/serialize raised SystemExit(%s)" % e.code)]
    if b1 != b2:
        out.append(_v("export", "non-deterministic serialization"))
    payload = mod.build(corpus)
    ex_ids = sorted(r["id"] for r in payload["objections"])
    co_ids = sorted(str(o.get("id", "")).strip() for o in corpus.get("objections", []))
    if ex_ids != co_ids:
        out.append(_v("export", "export id-set != corpus id-set"))
    return out


def _keyword_projection_violations(corpus, payload):
    """Pure: every corpus objection carrying non-empty keywords[] must appear in
    the export with those keywords projected non-empty and corpus-order-preserved
    (the generator's project_keywords contract: whitespace-collapsed, empties
    dropped, no sort, no dedupe). Guards the K129 cadence-lock — a stale generator
    that drops keywords fails LOUD here instead of silently reverting search
    recall. Pure over (corpus, built-payload) so the synthetic leg can fire it
    with a hand-crafted stale-export payload (like export determinism, the live
    generator build is exercised by the live leg)."""
    out = []
    by_id = {str(r.get("id", "")).strip(): r for r in payload.get("objections", [])}
    for o in corpus.get("objections", []):
        oid = str(o.get("id", "")).strip()
        kws = o.get("keywords")
        if not isinstance(kws, list):
            continue
        expect = [k for k in (" ".join(str(x).split()) for x in kws) if k]
        if not expect:
            continue
        rec = by_id.get(oid)
        if rec is None:
            out.append(_v("keywords", "objection with keywords[] missing from export", oid)); continue
        got = rec.get("keywords")
        if not got:
            out.append(_v("keywords", "corpus keywords[] not projected into export (stale generator?)", oid))
        elif got != expect:
            out.append(_v("keywords", "export keywords differ from corpus projection (order/content drift)", oid))
    return out


def check_keyword_projection(corpus):
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        mod = importlib.import_module("build_right_to_die_index")
    except Exception as e:  # pragma: no cover
        return [_v("keywords", "cannot import build_right_to_die_index: %r" % e)]
    try:
        payload = mod.build(corpus)
    except SystemExit as e:
        return [_v("keywords", "build raised SystemExit(%s)" % e.code)]
    return _keyword_projection_violations(corpus, payload)


def check_rwe(corpus):
    """Referential integrity for vendored RWE plumbing. VACUOUS while
    realWorldExamples == [] and all rwe_refs empty (the launch state); engages
    automatically when RWE data lands. (Mirrors the parent v1/v4 rules.)"""
    out = []
    if not isinstance(corpus, dict):
        return out
    objs = corpus.get("objections", []) or []
    rwe = corpus.get("realWorldExamples", [])
    if not isinstance(rwe, list):
        return [_v("rwe", "realWorldExamples is not a list")]
    obj_ids = {str(o.get("id", "")).strip() for o in objs}
    inst_ids, seen = [], set()
    for rec in rwe:
        if not isinstance(rec, dict):
            out.append(_v("rwe", "realWorldExamples record is not an object")); continue
        iid = str(rec.get("instance_id", "")).strip()
        if not iid:
            out.append(_v("rwe", "RWE record with empty instance_id"))
        else:
            if iid in seen:
                out.append(_v("rwe", "duplicate instance_id (anchor collision): %s" % iid))
            seen.add(iid); inst_ids.append(iid)
        ao = rec.get("attached_objections", [])
        if not isinstance(ao, list) or len(ao) < 1:
            out.append(_v("rwe", "attached_objections must have >=1 item", iid or None)); ao = ao if isinstance(ao, list) else []
        for link in ao:
            lid = str((link or {}).get("objection_id", "")).strip()
            if lid and lid not in obj_ids:
                out.append(_v("rwe", "attached objection_id does not resolve: %s" % lid, iid or None))
        pol = rec.get("instance_polarity")
        if pol is not None and pol not in RWE_POLARITY_VALUES:
            out.append(_v("rwe", "instance_polarity %r not in allowed set" % pol, iid or None))
        st = rec.get("subject_type")
        if st is not None and st not in RWE_SUBJECT_TYPES:
            out.append(_v("rwe", "subject_type %r not in allowed set" % st, iid or None))
        att = rec.get("attestation_status")
        if att is not None and att not in RWE_ATTESTATION_VALUES:
            out.append(_v("rwe", "attestation_status %r not in allowed set" % att, iid or None))
        if "subject_type" not in rec:
            out.append(_v("rwe", "RWE record missing required subject_type (real-person attestation guard)", iid or None))
        if "instance_polarity" not in rec:
            out.append(_v("rwe", "RWE record missing required instance_polarity", iid or None))
        if st == "real-person":
            if att is None:
                out.append(_v("rwe", "real-person record requires attestation_status", iid or None))
            elif att == "unverified":
                out.append(_v("rwe", "real-person record attestation_status is 'unverified' (blocks the record)", iid or None))
    inst_set = set(inst_ids)
    for o in objs:
        for ref in (o.get("rwe_refs") or []):
            r = str(ref).strip()
            if r and r not in inst_set:
                out.append(_v("rwe", "rwe_refs id does not resolve to an RWE instance_id: %s" % r, o.get("id")))
    return out


def validate_all(corpus, ledger):
    issues = []
    issues += check_schema(corpus)
    issues += check_anchor_uniqueness(corpus)
    issues += check_ledger_corpus_sync(corpus, ledger)
    issues += check_band_geomean(corpus, ledger)
    issues += check_export_determinism(corpus)
    issues += check_keyword_projection(corpus)
    issues += check_rwe(corpus)
    return issues


# ----------------------------------------------------------------------------- synthetic
def _good_corpus():
    return {
        "totalEntries": 1, "totalResponses": 0,
        "objections": [{
            "id": "alpha", "tier": 1, "category": "Emotional/Reflexive",
            "trigger": "t", "keywords": [], "move_tags": [], "diagnosis": "d",
            "responses": {"short": "", "medium": "", "long": ""}, "rwe_refs": [],
        }],
        "realWorldExamples": [],
    }


def run_synthetic_tests():
    cases = {}

    # schema
    c = _good_corpus(); c["totalEntries"] = 9
    cases["schema_count_mismatch_fires"] = (len(check_schema(c)) > 0, True)
    c = _good_corpus(); c["objections"][0]["responses"] = {"short": ""}
    cases["schema_missing_depth_fires"] = (len(check_schema(c)) > 0, True)
    cases["schema_clean_passes"] = (len(check_schema(_good_corpus())) == 0, True)
    # move_tags rename: a node carrying the OLD field name lacks `move_tags` -> fires
    c = _good_corpus(); del c["objections"][0]["move_tags"]; c["objections"][0]["strands"] = []
    cases["schema_missing_move_tags_fires"] = (len(check_schema(c)) > 0, True)
    # access_basis allowed-values
    c = _good_corpus(); c["objections"][0]["access_basis"] = "gated"
    cases["access_basis_valid_passes"] = (len(check_schema(c)) == 0, True)
    c = _good_corpus(); c["objections"][0]["access_basis"] = "both"
    cases["access_basis_both_passes"] = (len(check_schema(c)) == 0, True)
    c = _good_corpus(); c["objections"][0]["access_basis"] = "sometimes"
    cases["access_basis_bad_fires"] = (len(check_schema(c)) > 0, True)
    cases["access_basis_absent_passes"] = (len(check_schema(_good_corpus())) == 0, True)

    # anchor
    c = _good_corpus(); c["objections"].append(dict(c["objections"][0])); c["totalEntries"] = 2
    cases["anchor_dup_fires"] = (len(check_anchor_uniqueness(c)) > 0, True)
    c = _good_corpus(); c["objections"][0]["id"] = "Bad_ID"
    cases["anchor_badchar_fires"] = (len(check_anchor_uniqueness(c)) > 0, True)
    cases["anchor_clean_passes"] = (len(check_anchor_uniqueness(_good_corpus())) == 0, True)

    # sync
    led = {"grades": {"ghost": {}}, "ungraded": [], "band_thresholds": CANON_THRESHOLDS}
    cases["sync_ghost_grade_fires"] = (len(check_ledger_corpus_sync(_good_corpus(), led)) > 0, True)
    c = _good_corpus(); c["objections"][0]["_stub"] = True
    led = {"grades": {"alpha": {}}, "ungraded": [], "band_thresholds": CANON_THRESHOLDS}
    cases["sync_stub_graded_fires"] = (len(check_ledger_corpus_sync(c, led)) > 0, True)
    led = {"grades": {}, "ungraded": [], "band_thresholds": CANON_THRESHOLDS}
    cases["sync_uncovered_gradeable_fires"] = (len(check_ledger_corpus_sync(_good_corpus(), led)) > 0, True)
    led = {"grades": {}, "ungraded": ["alpha"], "band_thresholds": {"A": 0.9, "B": 0.8, "C": 0.7, "D": 0.0}}
    cases["sync_bad_thresholds_fire"] = (len(check_ledger_corpus_sync(_good_corpus(), led)) > 0, True)
    c = _good_corpus(); c["objections"][0]["_stub"] = True
    led = {"grades": {}, "ungraded": [], "band_thresholds": CANON_THRESHOLDS}
    cases["sync_launch_state_passes"] = (len(check_ledger_corpus_sync(c, led)) == 0, True)

    # band
    led = {"grades": {"alpha": {"axes": {"v": .8, "s": .8, "c": .8, "r": .8, "a": .8}, "geomean": 0.5,
                                "short": {"rsi_pct": 80.0, "grade": "C"}, "medium": {"rsi_pct": 80.0, "grade": "C"},
                                "long": {"rsi_pct": 80.0, "grade": "C"}, "headline_grade_long": "C"}}}
    cases["band_bad_geomean_fires"] = (len(check_band_geomean(_good_corpus(), led)) > 0, True)
    led = {"grades": {"alpha": {"axes": {"v": .7, "s": .7, "c": .7, "r": .7, "a": .7}, "geomean": 0.7,
                                "short": {"rsi_pct": 70.0, "grade": "A"}, "medium": {"rsi_pct": 70.0, "grade": "D"},
                                "long": {"rsi_pct": 70.0, "grade": "D"}, "headline_grade_long": "D"}}}
    cases["band_two_off_fires"] = (len(check_band_geomean(_good_corpus(), led)) > 0, True)
    gm = geomean5({"v": .83, "s": .83, "c": .83, "r": .83, "a": .83})
    led = {"grades": {"alpha": {"axes": {"v": .83, "s": .83, "c": .83, "r": .83, "a": .83}, "geomean": gm,
                                "short": {"rsi_pct": 79.0, "grade": "C"}, "medium": {"rsi_pct": 81.0, "grade": "C"},
                                "long": {"rsi_pct": 83.0, "grade": "B"}, "headline_grade_long": "B"}}}
    cases["band_consistent_passes"] = (len(check_band_geomean(_good_corpus(), led)) == 0, True)
    led = {"grades": {"alpha": {"axes": {"v": .83, "s": .83, "c": .83, "r": .83, "a": .83}, "geomean": gm,
                                "short": {"rsi_pct": 83.0, "grade": "B"}, "medium": {"rsi_pct": 83.0, "grade": "B"},
                                "long": {"rsi_pct": 83.0, "grade": "B"}, "headline_grade_long": "A"}}}
    cases["band_headline_mismatch_fires"] = (len(check_band_geomean(_good_corpus(), led)) > 0, True)

    # rwe referential integrity + v0.2 enforcement (presence + enum + real-person attestation)
    def _rwe(**kw):
        r = {"instance_id": "rwe-x", "subject_type": "category", "instance_polarity": "neutral-illustration",
             "attached_objections": [{"objection_id": "alpha"}]}
        r.update(kw)
        return r
    def _corp(recs, refs):
        c = _good_corpus(); c["realWorldExamples"] = recs; c["objections"][0]["rwe_refs"] = refs
        return c
    cases["rwe_launch_empty_passes"] = (len(check_rwe(_good_corpus())) == 0, True)
    cases["rwe_clean_record_passes"] = (len(check_rwe(_corp([_rwe()], ["rwe-x"]))) == 0, True)
    cases["rwe_bad_attach_fires"] = (len(check_rwe(_corp([_rwe(attached_objections=[{"objection_id": "ghost"}])], ["rwe-x"]))) > 0, True)
    cases["rwe_dangling_ref_fires"] = (len(check_rwe(_corp([], ["rwe-nope"]))) > 0, True)
    cases["rwe_dup_instance_fires"] = (len(check_rwe(_corp([_rwe(), _rwe()], ["rwe-x"]))) > 0, True)
    cases["rwe_missing_subject_type_fires"] = (len(check_rwe(_corp([{"instance_id": "rwe-x", "instance_polarity": "neutral-illustration", "attached_objections": [{"objection_id": "alpha"}]}], ["rwe-x"]))) > 0, True)
    cases["rwe_missing_polarity_fires"] = (len(check_rwe(_corp([{"instance_id": "rwe-x", "subject_type": "category", "attached_objections": [{"objection_id": "alpha"}]}], ["rwe-x"]))) > 0, True)
    cases["rwe_realperson_omits_subject_type_fires"] = (len(check_rwe(_corp([{"instance_id": "rwe-x", "instance_polarity": "neutral-illustration", "attestation_status": "public-record", "attached_objections": [{"objection_id": "alpha"}]}], ["rwe-x"]))) > 0, True)
    cases["rwe_realperson_no_attestation_fires"] = (len(check_rwe(_corp([_rwe(subject_type="real-person")], ["rwe-x"]))) > 0, True)
    cases["rwe_realperson_unverified_fires"] = (len(check_rwe(_corp([_rwe(subject_type="real-person", attestation_status="unverified")], ["rwe-x"]))) > 0, True)
    cases["rwe_realperson_attested_passes"] = (len(check_rwe(_corp([_rwe(subject_type="real-person", attestation_status="public-record")], ["rwe-x"]))) == 0, True)
    cases["rwe_structural_passes"] = (len(check_rwe(_corp([_rwe(subject_type="structural")], ["rwe-x"]))) == 0, True)
    cases["rwe_bad_polarity_fires"] = (len(check_rwe(_corp([_rwe(instance_polarity="bogus")], ["rwe-x"]))) > 0, True)
    cases["rwe_contested_polarity_passes"] = (len(check_rwe(_corp([_rwe(instance_polarity="contested")], ["rwe-x"]))) == 0, True)

    # keyword projection (Rider 2): pure over (corpus, built-payload); like export
    # determinism the live generator build runs in the live leg, so here the pure
    # projection-comparison is fired with hand-crafted stale-export payloads.
    _kw = _good_corpus(); _kw["objections"][0]["keywords"] = ["aa", "bb"]
    cases["kw_projected_passes"] = (len(_keyword_projection_violations(_kw, {"objections": [{"id": "alpha", "keywords": ["aa", "bb"]}]})) == 0, True)
    cases["kw_dropped_fires"] = (len(_keyword_projection_violations(_kw, {"objections": [{"id": "alpha", "title": "t"}]})) > 0, True)
    cases["kw_reordered_fires"] = (len(_keyword_projection_violations(_kw, {"objections": [{"id": "alpha", "keywords": ["bb", "aa"]}]})) > 0, True)
    cases["kw_missing_entry_fires"] = (len(_keyword_projection_violations(_kw, {"objections": []})) > 0, True)
    cases["kw_no_keywords_passes"] = (len(_keyword_projection_violations(_good_corpus(), {"objections": [{"id": "alpha"}]})) == 0, True)

    results, all_pass = {}, True
    for name, (observed, expected) in cases.items():
        passed = observed == expected
        all_pass = all_pass and passed
        results[name] = {"observed": observed, "expected": expected, "pass": passed}
    results["_overall_pass"] = all_pass
    return results


def run_live_test():
    out = {"_overall_pass": True}
    try:
        corpus = json.load(open(os.path.join(HERE, "right_to_die_corpus_v0_1.json"), encoding="utf-8"))
    except Exception as e:
        return {"_overall_pass": False, "error": "cannot load seed corpus: %r" % e}
    ledger = {}
    lp = os.path.join(HERE, "right_to_die_grading_ledger.json")
    if os.path.exists(lp):
        try:
            ledger = json.load(open(lp, encoding="utf-8"))
        except Exception as e:
            return {"_overall_pass": False, "error": "cannot load ledger: %r" % e}
    issues = validate_all(corpus, ledger)
    out["seed_violation_count"] = len(issues)
    out["seed_violations"] = issues
    out["_overall_pass"] = len(issues) == 0
    return out


def _main(argv):
    if "--self-test" in argv:
        syn = run_synthetic_tests()
        live = run_live_test()
        combined = {
            "synthetic_self_test": syn,
            "live_seed_test": live,
            "_overall_pass": syn["_overall_pass"] and live["_overall_pass"],
        }
        print(json.dumps(combined, indent=2, ensure_ascii=False))
        return 0 if combined["_overall_pass"] else 1

    if len(argv) < 2:
        print(__doc__)
        print("\nERROR: pass a corpus JSON path or --self-test.", file=sys.stderr)
        return 2

    corpus = json.load(open(argv[1], encoding="utf-8"))
    ledger = {}
    lp = os.path.join(os.path.dirname(os.path.abspath(argv[1])), "right_to_die_grading_ledger.json")
    if os.path.exists(lp):
        ledger = json.load(open(lp, encoding="utf-8"))
    issues = validate_all(corpus, ledger)
    report = {"input_path": argv[1], "violation_count": len(issues),
              "violations": issues, "verdict": "PASS" if not issues else "FAIL"}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
