#!/usr/bin/env python3
"""shapes_redrafts_judgments_gate.py -- the gate on gate2's round-two judgment of V2b's two redrafts (V3b, 2026-10-04).

A second-round judgment is its own record and gate; shapes_pilot_judgments.json and its gate are not touched.
GREEN only if shapes_redrafts_judgments.json is what its header says it is:
  pins       every referent the header pins resolves at its md5 (working tree or git history, via
             adversarial_map_staging/r1/pinned.py, so the append-only records it reads are read at the bytes judged;
             the scholar file through `git show` in the game's repository), and the header pins equal this gate's
  ids        row ids RJ-nnn, unique and in order; 'supersedes' names an earlier row of the same kind and redraft
  vocab      kinds and verdicts from the record's own vocabulary; verdict rows carry one; every row a seat and date
  coverage   each redraft in the redrafts record judged by exactly one standing shape row (its id, shape and the
             round-one row it answers), and each of its pulls by exactly one standing pull row
  routes     class_drafted is the redraft's; AMEND owes something, nothing else does; a kept (d) names a via whose
             map entry is a (d) at that anchor, with the bedrock copied from that entry and the register's facet, and
             its route is the terminus the redrafts record carries
  quotes     every double-quoted span in a row's text is declared in its quotes, every declared quote is used, and
             each is verbatim at its pinned source; a web: quote is at most 15 words and its url is in the row's
             'checked' list (only a fresh fetch can check its words); his words in the header are verbatim at canon
  figures    every figure a row states is recomputed here: word counts, changed fields, termini, and four
             validator runs (the redrafts alone, the pilot with the two replaced, the shapes his word kept, and the
             pilot and redrafts together, which must fail)
  history    append-only: every committed version's rows are a prefix of today's, and its header is today's
             (the state line excepted)

  python3 argument_shapes/shapes_redrafts_judgments_gate.py [--self-test [--write]]
"""
import copy, hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

REL = "argument_shapes/shapes_redrafts_judgments.json"
CONTROL = "argument_shapes/shapes_redrafts_judgments_gate_control_v0_1.json"
KICKOFF = ("R0311", "95ae9542298d5162efb407780e82d2ff")
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
PINS = {
    "redrafts": ("argument_shapes/shapes_redrafts_v0_1.json", "fc28cd12265e2712a9d610bbb2c1b69f"),
    "redrafts_record": ("argument_shapes/shapes_redrafts_record_v0_1.json", "ace5fb88886f7f7ce49a90658b590954"),
    "redrafts_builder": ("argument_shapes/build_shapes_redrafts.py", "ee38e0ad8d83cb95539d40af7931fdc9"),
    "pilot": ("argument_shapes/shapes_pilot_v0_1.json", "1f9c5da6166b538a90efa6dc7598124e"),
    "judgments": ("argument_shapes/shapes_pilot_judgments.json", "73503bccdd3ddf8b3a82f280181251d4"),
    "judgments_gate": ("argument_shapes/shapes_judgments_gate.py", "f56df1e7fdaa82bf3c0f1a11e9622837"),
    "validator": ("argument_shapes/shape_validator_v0_1.py", "64553b25b6db0ff67edeb87b89178297"),
    "schema": ("argument_shapes/argument_shapes_schema_v0_1.json", "bef95b1dc2b9cb109760cd961d2da72b"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1"),
    "map_v1_8": ("adversarial_map_staging/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827"),
    "register_v0_9": ("adversarial_map_staging/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351"),
    "canon": ("project_canon_v38_50.json", "98302afdf29af8ed3149111843d717ab"),
}
SCHOLAR = {"repo": "~/D/Argue the Argument", "commit": "76cbbd13ef967617b181697675bd15dbbf0a6a0b",
           "file": "data/flagship/scholar-objections_v1_1.json", "md5": "20999eb9b1b384d0f871a9deec464b2a"}
KINDS = {"shape", "scheme", "sources", "pull", "note", "finding", "safety", "sequence"}
VERDICT_KINDS = {"shape", "scheme", "sources", "pull", "note", "safety"}
SHAPE_VERDICTS = {"ACCEPT", "AMEND", "REJECT"}
OTHER_VERDICTS = {"CONFIRM", "CORRECT"}
NO_SPAN = {"id", "kind", "redraft", "shape_id", "answers", "class_drafted", "class_judged", "verdict", "belongs_to",
           "route", "seat", "date", "supersedes", "quotes", "figures", "checked", "whose", "pull", "pull_text"}
SLOTS = ("short", "medium", "long")
WEB_MAX_WORDS = 15
RUN_KEYS = ("verdict", "violation_count", "shapes", "nodes_with_shapes")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def walk(obj, path):
    for p in path.split("."):
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    return obj


class Sources:
    def __init__(self):
        raw = {k: pinned.bytes_at(REPO, *v) for k, v in PINS.items()}
        j = lambda k: json.loads(raw[k].decode("utf-8"))  # noqa: E731
        self.redrafts_doc = j("redrafts")
        self.redrafts = {s["shape_id"]: s for s in self.redrafts_doc["shapes"]}
        self.record = j("redrafts_record")
        self.pilot_doc = j("pilot")
        self.pilot = {s["shape_id"]: s for s in self.pilot_doc["shapes"]}
        self.judgments = {r["id"]: r for r in j("judgments")["rows"]}
        c = j("corpus")
        self.corpus = {o["id"]: o for o in c["objections"]}
        self.map = j("map_v1_8")
        self.register = {b["bedrock_id"]: b for b in j("register_v0_9")["bedrocks"]}
        self.canon = j("canon")
        b = subprocess.run(["git", "-C", os.path.expanduser(SCHOLAR["repo"]), "show",
                            "%s:%s" % (SCHOLAR["commit"], SCHOLAR["file"])], capture_output=True).stdout
        if md5b(b) != SCHOLAR["md5"]:
            print("SHAPES REDRAFTS JUDGMENTS GATE: the scholar file is not readable at %s here" % SCHOLAR["md5"][:8])
            sys.exit(2)
        self.scholar = {n["id"]: n["scholar_objection"] for n in json.loads(b.decode("utf-8"))["nodes"]}
        self.figures = compute_figures(self)

    def locus(self, node, slot):
        o = self.corpus[node]
        if slot in ("trigger", "diagnosis"):
            return o[slot]
        if slot in SLOTS:
            return o["responses"][slot]
        if slot.startswith("archetypeVariants."):
            return o["responses"]["archetypeVariants"][slot.split(".", 1)[1]]
        raise KeyError(slot)

    def text(self, src):
        kind, ref = src.split(":", 1)
        if kind == "redraft":
            sid, field = ref.rsplit(".", 1)
            v = self.redrafts[sid][field]
        elif kind == "pilot":
            sid, field = ref.rsplit(".", 1)
            v = self.pilot[sid][field]
        elif kind == "record":
            v = walk(self.record, ref)
        elif kind == "judgments":
            rid, path = ref.split(".", 1)
            v = walk(self.judgments[rid], path)
        elif kind == "corpus":
            node, slot = ref.split("#", 1)
            v = self.locus(node, slot)
        elif kind == "map":
            n, field = ref.lstrip("#").split(".", 1)
            v = self.map["entries"][int(n)][field]
        elif kind == "register":
            hr, path = ref.split(".", 1)
            v = walk(self.register[hr], path)
        elif kind == "canon":
            v = walk(self.canon, ref)
        elif kind == "scholar":
            v = self.scholar[ref]
        else:
            raise KeyError(kind)
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def validator_runs(S):
    """The four runs, with the pinned validator over the pinned corpus; the two views are written to scratch."""
    if md5b(open(os.path.join(REPO, PINS["validator"][0]), "rb").read()) != PINS["validator"][1]:
        raise LookupError("the validator in the working tree is not the one pinned (%s)" % PINS["validator"][1][:8])
    import shape_validator_v0_1 as SV
    corpus = pinned.path_at(REPO, *PINS["corpus"])
    scratch = tempfile.mkdtemp(prefix="v3b_gate_")
    try:
        paths = {}
        for k in ("pilot", "redrafts"):
            paths[k] = pinned.path_at(REPO, *PINS[k])
        sup = {"meta": S.pilot_doc["meta"],
               "shapes": [S.redrafts.get(s["shape_id"], s) for s in S.pilot_doc["shapes"]]}
        kept = [r["shape_id"] for r in S.judgments.values() if r.get("kind") == "shape" and r.get("verdict") == "ACCEPT"]
        kept += list(S.redrafts)
        ruled_shapes = [s for s in sup["shapes"] if s["shape_id"] in kept]
        nodes = {s["shape_id"].split("/")[0] for s in ruled_shapes}
        ruled = {"meta": dict(S.pilot_doc["meta"], shape_coverage="%d/%d" % (len(nodes), len(S.corpus))),
                 "shapes": ruled_shapes}
        for name, doc in (("superseded_view", sup), ("ruled_view", ruled)):
            paths[name] = os.path.join(scratch, name + ".json")
            open(paths[name], "w", encoding="utf-8").write(json.dumps(doc, indent=1, ensure_ascii=False))

        def run(ps, failed=False):
            lines = []
            _ok, f, _v = SV.validate(ps, corpus, out=lines.append)
            s = json.loads(lines[-1])
            out = {k: s[k] for k in RUN_KEYS}
            if failed:
                out["failed"] = sorted(f)
            return out
        runs = {"redrafts_alone": run([paths["redrafts"]]),
                "superseded_view": run([paths["superseded_view"]]),
                "ruled_view": run([paths["ruled_view"]]),
                "pilot_and_redrafts_together": run([paths["pilot"], paths["redrafts"]], failed=True)}
        rv = S.record.get("validator_runs", {})
        runs["record_runs_match"] = (
            all({k: rv.get(n, {}).get(k) for k in RUN_KEYS} == runs[n]
                for n in ("redrafts_alone", "superseded_view", "ruled_view"))
            and rv.get("ruled_view", {}).get("shape_ids") == [s["shape_id"] for s in ruled_shapes])
        return runs
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def compute_figures(S):
    import shape_validator_v0_1 as SV
    F = {}
    for r in S.record["rows"]:
        sid = r["shape_id"]
        a, b = S.pilot[sid], S.redrafts[sid]
        term = {k: v for k, v in r["terminus"].items() if k != "copied_from"}
        judged = S.judgments[r["answers"]["row"]]["route"]
        F[r["id"]] = {"words": {"pilot": SV.wc(a["statement"]), "redraft": SV.wc(b["statement"])},
                      "changed": sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k)),
                      "statement_unchanged": a["statement"] == b["statement"],
                      "terminus_is_the_route": term == judged}
    F["validator"] = validator_runs(S)
    return F


def figure(F, path):
    obj = F
    for p in path.split("."):
        obj = obj[p]
    return obj


def spans(row):
    out = []

    def go(v, key=None):
        if key in NO_SPAN:
            return
        if isinstance(v, str):
            out.extend(re.findall(r'"([^"]+)"', v))
        elif isinstance(v, list):
            for x in v:
                go(x)
        elif isinstance(v, dict):
            for k, x in v.items():
                go(x, k)
    for k, v in row.items():
        go(v, k)
    return out


def check(rec, S, history):
    red = {}

    def fail(name, msg):
        red.setdefault(name, []).append(msg)

    # pins
    J = rec.get("judged", {})
    for k, (rel, m) in PINS.items():
        if J.get(k) != {"file": rel, "md5": m}:
            fail("pins", "header pin %s is not the gate's" % k)
    if J.get("scholar") != SCHOLAR:
        fail("pins", "header scholar pin is not the gate's")
    if set(J) != set(PINS) | {"scholar"}:
        fail("pins", "header pins a referent the gate does not")
    if rec.get("kickoff") != {"relay": KICKOFF[0], "md5": KICKOFF[1]}:
        fail("pins", "kickoff relay")
    for w in rec.get("his_word", []):
        try:
            if S.text(w["src"]) != w["verbatim"]:
                fail("his_word", "not verbatim at %s" % w["src"])
        except (KeyError, IndexError, ValueError):
            fail("his_word", "no source %s" % w["src"])

    rows = rec.get("rows", [])
    # ids
    ids = [r.get("id") for r in rows]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"RJ-\d{3}", str(i)) for i in ids) or ids != sorted(ids):
        fail("ids", "row ids not unique, well-formed and in order")
    seen = {}
    for r in rows:
        s = r.get("supersedes")
        if s is not None:
            o = seen.get(s)
            if not o or o.get("kind") != r.get("kind") or o.get("redraft") != r.get("redraft"):
                fail("ids", "%s supersedes %s, which is not an earlier row of its kind" % (r.get("id"), s))
        seen[r.get("id")] = r
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    standing = [r for r in rows if r.get("id") not in superseded]

    # vocab
    for r in rows:
        k = r.get("kind")
        if k not in KINDS:
            fail("vocab", "%s: kind %r" % (r.get("id"), k))
        if k == "shape" and r.get("verdict") not in SHAPE_VERDICTS:
            fail("vocab", "%s: a shape verdict is ACCEPT, AMEND or REJECT" % r.get("id"))
        elif k in VERDICT_KINDS - {"shape"} and r.get("verdict") not in OTHER_VERDICTS:
            fail("vocab", "%s: verdict %r" % (r.get("id"), r.get("verdict")))
        elif k not in VERDICT_KINDS and "verdict" in r:
            fail("vocab", "%s: a %s row carries no verdict" % (r.get("id"), k))
        if not r.get("seat") or not r.get("date"):
            fail("vocab", "%s: seat and date" % r.get("id"))

    # coverage
    want = {x["id"]: x for x in S.record["rows"]}
    shape_rows = [r for r in standing if r.get("kind") == "shape"]
    if sorted(r.get("redraft") for r in shape_rows) != sorted(want):
        fail("coverage", "standing shape rows %s != the record's redrafts %s"
             % (sorted(str(r.get("redraft")) for r in shape_rows), sorted(want)))
    for r in shape_rows:
        x = want.get(r.get("redraft"))
        if x and (r.get("shape_id") != x["shape_id"] or r.get("answers") != x["answers"]["row"]):
            fail("coverage", "%s: shape or answered row is not the record's" % r.get("id"))
    pulls = sorted((r.get("redraft"), r.get("pull")) for r in standing if r.get("kind") == "pull")
    want_pulls = sorted((x["id"], i) for x in S.record["rows"] for i in range(len(x.get("pulls", []))))
    if pulls != want_pulls:
        fail("coverage", "standing pull rows %s != the record's pulls %s" % (pulls, want_pulls))

    # routes
    for r in shape_rows:
        x = want.get(r.get("redraft"))
        if not x:
            continue
        sid, v, cj, rt = x["shape_id"], r.get("verdict"), r.get("class_judged"), r.get("route")
        own = sid.split("/")[0]
        if r.get("class_drafted") != S.redrafts[sid]["class"]:
            fail("routes", "%s: class_drafted is not the redraft's" % sid)
        if (v == "AMEND") != bool(r.get("owed")):
            fail("routes", "%s: AMEND owes something; nothing else does" % sid)
        if v == "REJECT":
            if cj is not None or rt is not None or r.get("belongs_to") not in S.corpus or r.get("belongs_to") == own:
                fail("routes", "%s: a REJECT has no class or route, and belongs to another node" % sid)
            continue
        if r.get("belongs_to") is not None or cj not in ("a", "b", "c", "d") or not isinstance(rt, dict):
            fail("routes", "%s: a kept shape has a class and a route" % sid)
            continue
        if cj in ("a", "b"):
            ab = rt.get("answered_by") or []
            if not ab or set(rt) != {"answered_by"}:
                fail("routes", "%s: (a)/(b) names answering loci only" % sid)
            for a in ab:
                try:
                    node, slot = a["locus"].split("#", 1)
                    ok = a["anchor"] in S.locus(node, slot) and len(a["anchor"].split()) <= 15
                except (KeyError, ValueError):
                    ok = False
                if not ok:
                    fail("routes", "%s: anchor not verbatim at %s" % (sid, a.get("locus")))
        elif cj == "d":
            try:
                node, slot = rt["via"].split("#", 1)
                hits = [e for e in S.map["entries"] if e["target_id"] == node and e["target_locus"] == slot
                        and e["class"] == "d" and e["target_anchor"] == rt["via_anchor"]]
                res = hits[0]["routing"]["residue"] if len(hits) == 1 else {}
                reg = [{"bedrock_id": b["bedrock_id"], "name": b["name"], "facet": f["facet_id"]}
                       for b in S.register.values() for f in b["facets"] for t in f["tributaries"]
                       if t["node"] == node and t["locus"] == slot and t["anchor"] == rt["via_anchor"]]
                bd = rt["bedrock"]
                ok = (len(hits) == 1 and bd["bedrock_name"] == res.get("bedrock_name") and
                      bd["terminus_routing"] == res.get("terminus_routing") and reg == [bd["register"]])
            except (KeyError, ValueError, TypeError):
                ok = False
            if not ok:
                fail("routes", "%s: the (d)'s via and bedrock are not the map's and register's" % sid)
            term = {k: v for k, v in x["terminus"].items() if k != "copied_from"}
            if rt != term:
                fail("routes", "%s: the route is not the terminus the redrafts record carries" % sid)
        elif cj == "c" and set(rt) != {"intake"}:
            fail("routes", "%s: a (c) names the intake only" % sid)

    # quotes
    for r in rows:
        declared = [q.get("quote") for q in r.get("quotes", [])]
        used = spans(r)
        for sp in used:
            if sp not in declared:
                fail("quotes", "%s: undeclared span %r" % (r.get("id"), sp[:40]))
        for q in r.get("quotes", []):
            if q.get("quote") not in used:
                fail("quotes", "%s: declared quote not used %r" % (r.get("id"), str(q.get("quote"))[:40]))
            src = str(q.get("src"))
            if src.startswith("web:"):
                url = src[4:]
                if (len(str(q.get("quote")).split()) > WEB_MAX_WORDS or
                        not any(c == url or c.startswith(url + " ") for c in r.get("checked", []))):
                    fail("quotes", "%s: web quote over %d words or its url unchecked" % (r.get("id"), WEB_MAX_WORDS))
                continue
            try:
                if q["quote"] not in S.text(src):
                    fail("quotes", "%s: not verbatim at %s" % (r.get("id"), src))
            except (KeyError, IndexError, ValueError, AttributeError):
                fail("quotes", "%s: no source %s" % (r.get("id"), src))

    # figures
    for r in rows:
        for path, val in (r.get("figures") or {}).items():
            try:
                if figure(S.figures, path) != val:
                    fail("figures", "%s: %s is not the recomputed figure" % (r.get("id"), path))
            except (KeyError, TypeError):
                fail("figures", "%s: no figure %s" % (r.get("id"), path))

    # history
    head = {k: v for k, v in rec.items() if k not in ("rows", "state")}
    for old in history:
        if {k: v for k, v in old.items() if k not in ("rows", "state")} != head:
            fail("history", "a committed header differs")
        if rows[:len(old.get("rows", []))] != old.get("rows", []):
            fail("history", "a committed row was edited or removed")
    return red


def committed_versions():
    out = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", REL], capture_output=True, text=True).stdout
    vs = []
    for h in out.split():
        b = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (h, REL)], capture_output=True).stdout
        if b:
            vs.append(json.loads(b.decode("utf-8")))
    return vs


def kickoff_index():
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) > 8 and f[1] == "SENT" and f[2] == KICKOFF[0]:
                return f[8] == KICKOFF[1]
    return True


def _row(r, rid):
    return next(x for x in r["rows"] if x["id"] == rid)


MUTATIONS = [
    ("unmutated", lambda r: None, []),
    ("verdict out of vocabulary", lambda r: _row(r, "RJ-003").update(verdict="MAYBE"), ["vocab"]),
    ("a redraft left unjudged", lambda r: r["rows"].remove(_row(r, "RJ-002")), ["coverage"]),
    ("a pull left unjudged", lambda r: r["rows"].remove(_row(r, "RJ-006")), ["coverage"]),
    ("a quote off by one character", lambda r: _row(r, "RJ-001")["quotes"][0].update(
        quote=_row(r, "RJ-001")["quotes"][0]["quote"] + "s"), ["quotes"]),
    ("an undeclared quoted span", lambda r: _row(r, "RJ-002").update(reason=_row(r, "RJ-002")["reason"] + ' "invented"'),
     ["quotes"]),
    ("a web quote from an unchecked url", lambda r: next(
        q for q in _row(r, "RJ-001")["quotes"] if q["src"].startswith("web:")).update(src="web:https://example.org/"),
     ["quotes"]),
    ("a pin moved", lambda r: r["judged"]["corpus"].update(md5="0" * 32), ["pins"]),
    ("a (d)'s facet retyped", lambda r: _row(r, "RJ-002")["route"]["bedrock"]["register"].update(facet="typed"),
     ["routes"]),
    ("class_drafted not the redraft's", lambda r: _row(r, "RJ-001").update(class_drafted="a"), ["routes"]),
    ("an AMEND owing nothing", lambda r: _row(r, "RJ-001").update(owed=[]), ["routes"]),
    ("an ACCEPT owing something", lambda r: _row(r, "RJ-002").update(owed=["something"]), ["routes"]),
    ("a figure not recomputed", lambda r: _row(r, "RJ-003")["figures"]["validator.ruled_view"].update(shapes=8),
     ["figures"]),
    ("a duplicate id", lambda r: _row(r, "RJ-002").update(id="RJ-001"), ["ids"]),
    ("supersedes names no earlier row", lambda r: _row(r, "RJ-010").update(supersedes="RJ-099"), ["ids"]),
    ("his word not verbatim", lambda r: r["his_word"][0].update(verbatim=r["his_word"][0]["verbatim"][:-1]),
     ["his_word"]),
    ("a committed row edited", "HISTORY", ["history"]),
]


def self_test(S, rec):
    results = []
    for name, mut, expect in MUTATIONS:
        r = copy.deepcopy(rec)
        hist = []
        if mut == "HISTORY":
            old = copy.deepcopy(rec)
            _row(old, "RJ-004")["finding"] += " (an earlier wording)"
            hist = [old]
        else:
            mut(r)
        red = sorted(check(r, S, hist))
        results.append({"mutation": name, "expect_red": sorted(expect), "red": red, "as_expected": red == sorted(expect)})
    return {"what": "shapes_redrafts_judgments_gate.py self-test: the unmutated record first, then one mutation per check",
            "record": REL, "cases": len(results), "as_expected": sum(x["as_expected"] for x in results),
            "results": results}


def main():
    try:
        S = Sources()
    except LookupError as e:
        print("RED pins      %s" % e)
        print("SHAPES REDRAFTS JUDGMENTS GATE: RED (a pinned referent is unreadable)")
        sys.exit(1)
    rec = json.loads(open(os.path.join(REPO, REL), encoding="utf-8").read())
    if "--self-test" in sys.argv:
        out = (json.dumps(self_test(S, rec), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        path = os.path.join(REPO, CONTROL)
        if "--write" in sys.argv:
            open(path, "wb").write(out)
            print("SELF-TEST: wrote %s %s" % (CONTROL, md5b(out)))
            return
        ok = os.path.exists(path) and open(path, "rb").read() == out
        st = json.loads(out.decode("utf-8"))
        print("SELF-TEST: %d of %d as expected; control record %s" % (
            st["as_expected"], st["cases"], "matches" if ok else "DIFFERS"))
        sys.exit(0 if ok and st["as_expected"] == st["cases"] else 1)
    red = check(rec, S, committed_versions())
    if not kickoff_index():
        red.setdefault("pins", []).append("the relay index disagrees with the kickoff md5")
    for k in sorted(red):
        for m in red[k][:6]:
            print("RED %-9s %s" % (k, m))
    v = {}
    for r in rec["rows"]:
        if r.get("kind") == "shape":
            v[r["verdict"]] = v.get(r["verdict"], 0) + 1
    print("SHAPES REDRAFTS JUDGMENTS GATE: %s (%d rows; redrafts %s)" % (
        "RED" if red else "GREEN", len(rec["rows"]), " ".join("%s %d" % kv for kv in sorted(v.items()))))
    sys.exit(1 if red else 0)


if __name__ == "__main__":
    main()
