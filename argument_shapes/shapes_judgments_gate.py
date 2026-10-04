#!/usr/bin/env python3
"""shapes_judgments_gate.py -- the gate on gate2's judgment of the argument-shapes pilot (V3, 2026-10-03).

GREEN only if shapes_pilot_judgments.json is what its header says it is:
  pins       every referent the header pins resolves at its md5 (working tree or git history, via
             adversarial_map_staging/r1/pinned.py; the scholar file through `git show` in the game's repository), and
             the header pins equal this gate's
  ids        row ids SJ-nnn, unique and in order; 'supersedes' names an earlier row of the same kind and shape
  vocab      kinds and verdicts from the record's own vocabulary; verdict rows carry one
  coverage   every pilot shape judged by exactly one standing shape row, and no other shape
  routes     class_drafted is the pilot's; REJECT has no class, no route and a belongs_to that is another node;
             (a)/(b) name answering loci whose anchors are verbatim and at most 15 words; (d) names a via whose map
             entry is a (d) at that anchor, with the bedrock copied from that entry and the register's facet; (c)
             names the intake; AMEND owes something, nothing else does
  quotes     every double-quoted span in a row's text is declared in its quotes, every declared quote is used, and
             each is verbatim at its source; his words in the header are verbatim at their canon path
  figures    every figure a row states is the reading record's, at the md5 this gate pins
  history    append-only: every committed version's rows are a prefix of today's, and its header is today's
             (the state line excepted)

  python3 argument_shapes/shapes_judgments_gate.py [--self-test [--write]]
"""
import copy, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402

REL = "argument_shapes/shapes_pilot_judgments.json"
CONTROL = "argument_shapes/shapes_judgments_gate_control_v0_1.json"
READING = ("argument_shapes/shapes_judgment_reading_v0_1.json", "0f1c71f9c31f985329cc27b011376c11")
KICKOFF = ("R0297", "2a8a8ca2deea71aa39b1f12f30d7dc53")
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
PINS = {
    "pilot": ("argument_shapes/shapes_pilot_v0_1.json", "1f9c5da6166b538a90efa6dc7598124e"),
    "measure": ("argument_shapes/shapes_pilot_measure_v0_1.json", "576be8f2c469f84b4bc9ca628d9b41c1"),
    "builder": ("argument_shapes/build_shapes_pilot.py", "4623c057a98482b85662b138acfc786e"),
    "validator": ("argument_shapes/shape_validator_v0_1.py", "64553b25b6db0ff67edeb87b89178297"),
    "validator_control": ("argument_shapes/shape_validator_control_v0_1.json", "64222600e415617bcd3ab8f7b8e453ef"),
    "schema": ("argument_shapes/argument_shapes_schema_v0_1.json", "bef95b1dc2b9cb109760cd961d2da72b"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1"),
    "map_v1_8": ("adversarial_map_staging/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827"),
    "register_v0_9": ("adversarial_map_staging/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351"),
    "rulings": ("adversarial_map_staging/r1/R1_rulings.json", "f7d02b16f6837e53033b3c7fb68332a9"),
    "layman": ("site/flagship-layman-index.json", "7a1f0881a6a9e964a4155d7897c312f8"),
    "canon": ("project_canon_v38_48.json", "c971855b153a297f182503c342b3659c"),
    "design": ("design/variations/VARIATIONS_design_v0_1.md", "fcf6f6fe0813072a3c66edd723a1ec80"),
}
SCHOLAR = {"repo": "~/D/Argue the Argument", "commit": "76cbbd13ef967617b181697675bd15dbbf0a6a0b",
           "file": "data/flagship/scholar-objections_v1_1.json", "md5": "20999eb9b1b384d0f871a9deec464b2a"}
KINDS = {"shape", "pull", "measure", "attestation", "safety", "finding", "sequence"}
VERDICT_KINDS = {"shape", "pull", "measure", "attestation", "safety"}
VERDICTS = {"ACCEPT", "AMEND", "REJECT", "CONFIRM", "CORRECT"}
SHAPE_VERDICTS = {"ACCEPT", "AMEND", "REJECT"}
NO_SPAN = {"id", "kind", "shape_id", "class_drafted", "class_judged", "verdict", "belongs_to", "route", "seat", "date",
           "supersedes", "quotes", "figures", "checked", "whose"}
SLOTS = ("short", "medium", "long")


def md5b(b):
    return hashlib.md5(b).hexdigest()


class Sources:
    def __init__(self):
        j = lambda k: json.loads(pinned.bytes_at(REPO, *PINS[k]).decode("utf-8"))  # noqa: E731
        self.pilot = {s["shape_id"]: s for s in j("pilot")["shapes"]}
        self.measure = j("measure")
        self.corpus = {o["id"]: o for o in j("corpus")["objections"]}
        c = j("corpus")
        self.rwe = {r["instance_id"]: r for r in c["realWorldExamples"]}
        self.map = j("map_v1_8")
        self.register = {b["bedrock_id"]: b for b in j("register_v0_9")["bedrocks"]}
        self.layman = {n["id"]: n for n in j("layman")["nodes"]}
        self.canon = j("canon")
        for k in ("builder", "validator", "validator_control", "schema", "rulings", "design"):
            pinned.bytes_at(REPO, *PINS[k])
        b = subprocess.run(["git", "-C", os.path.expanduser(SCHOLAR["repo"]), "show",
                            "%s:%s" % (SCHOLAR["commit"], SCHOLAR["file"])], capture_output=True).stdout
        if md5b(b) != SCHOLAR["md5"]:
            print("SHAPES JUDGMENTS GATE: the scholar file is not readable at %s here" % SCHOLAR["md5"][:8])
            sys.exit(2)
        self.scholar = {n["id"]: n["scholar_objection"] for n in json.loads(b.decode("utf-8"))["nodes"]}
        self.reading = json.loads(pinned.bytes_at(REPO, *READING).decode("utf-8"))

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
        if kind == "pilot":
            sid, field = ref.rsplit(".", 1)
            v = self.pilot[sid][field]
        elif kind == "measure":
            v = walk(self.measure, ref)
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
        elif kind == "layman":
            node, field = ref.split(".", 1)
            v = self.layman[node][field]
        elif kind == "rwe":
            iid, field = ref.rsplit(".", 1)
            v = self.rwe[iid][field]
        else:
            raise KeyError(kind)
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def walk(obj, path):
    for p in path.split("."):
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    return obj


def figure(reading, path):
    """Resolve a dotted path into the reading's figures; shape ids contain no dots."""
    obj = reading["figures"]
    parts = path.split(".")
    while parts:
        for n in range(len(parts), 0, -1):
            k = ".".join(parts[:n])
            if isinstance(obj, dict) and k in obj:
                obj, parts = obj[k], parts[n:]
                break
        else:
            raise KeyError(path)
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
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"SJ-\d{3}", str(i)) for i in ids) or ids != sorted(ids):
        fail("ids", "row ids not unique, well-formed and in order")
    seen = {}
    for r in rows:
        s = r.get("supersedes")
        if s is not None:
            o = seen.get(s)
            if not o or o.get("kind") != r.get("kind") or o.get("shape_id") != r.get("shape_id"):
                fail("ids", "%s supersedes %s, which is not an earlier row of its kind" % (r.get("id"), s))
        seen[r.get("id")] = r
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}

    # vocab
    for r in rows:
        if r.get("kind") not in KINDS:
            fail("vocab", "%s: kind %r" % (r.get("id"), r.get("kind")))
        if r.get("kind") in VERDICT_KINDS and r.get("verdict") not in VERDICTS:
            fail("vocab", "%s: verdict %r" % (r.get("id"), r.get("verdict")))
        if r.get("kind") == "shape" and r.get("verdict") not in SHAPE_VERDICTS:
            fail("vocab", "%s: a shape verdict is ACCEPT, AMEND or REJECT" % r.get("id"))
        if not r.get("seat") or not r.get("date"):
            fail("vocab", "%s: seat and date" % r.get("id"))

    # coverage
    standing = [r for r in rows if r.get("kind") == "shape" and r.get("id") not in superseded]
    got = sorted(r.get("shape_id") for r in standing)
    if got != sorted(S.pilot):
        fail("coverage", "standing shape rows %s != pilot %s" % (len(got), len(S.pilot)))

    # routes
    for r in standing:
        sid, v, cj, rt = r.get("shape_id"), r.get("verdict"), r.get("class_judged"), r.get("route")
        own = str(sid).split("/")[0]
        p = S.pilot.get(sid)
        if not p or r.get("class_drafted") != p["class"]:
            fail("routes", "%s: class_drafted is not the pilot's" % sid)
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
            try:
                if q["quote"] not in S.text(q["src"]):
                    fail("quotes", "%s: not verbatim at %s" % (r.get("id"), q["src"]))
            except (KeyError, IndexError, ValueError, AttributeError):
                fail("quotes", "%s: no source %s" % (r.get("id"), q.get("src")))

    # figures
    for r in rows:
        for path, val in (r.get("figures") or {}).items():
            try:
                if figure(S.reading, path) != val:
                    fail("figures", "%s: %s is not the reading's" % (r.get("id"), path))
            except KeyError:
                fail("figures", "%s: the reading has no %s" % (r.get("id"), path))

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


MUTATIONS = [
    ("unmutated", lambda r: None, []),
    ("verdict out of vocabulary", lambda r: r["rows"][13].update(verdict="MAYBE"), ["vocab"]),
    ("a shape left unjudged", lambda r: r["rows"].pop(4), ["coverage"]),
    ("a quote off by one character", lambda r: r["rows"][0]["quotes"][0].update(
        quote=r["rows"][0]["quotes"][0]["quote"] + "s"), ["quotes"]),
    ("an undeclared quoted span", lambda r: r["rows"][4].update(reason=r["rows"][4]["reason"] + ' "invented"'), ["quotes"]),
    ("a pin moved", lambda r: r["judged"]["corpus"].update(md5="0" * 32), ["pins"]),
    ("a (d)'s facet retyped", lambda r: r["rows"][8]["route"]["bedrock"]["register"].update(facet="typed"), ["routes"]),
    ("an anchor not verbatim", lambda r: r["rows"][4]["route"]["answered_by"][0].update(anchor="not in the text"), ["routes"]),
    ("a REJECT kept on its own node", lambda r: r["rows"][0].update(belongs_to="life-gift"), ["routes"]),
    ("class_drafted not the pilot's", lambda r: r["rows"][5].update(class_drafted="a"), ["routes"]),
    ("an AMEND owing nothing", lambda r: r["rows"][2].update(owed=[]), ["routes"]),
    ("a figure not the reading's", lambda r: r["rows"][13]["figures"].update({"judged.a_cross_node": "2 of 2"}), ["figures"]),
    ("a duplicate id", lambda r: r["rows"][1].update(id="SJ-001"), ["ids"]),
    ("supersedes names no earlier row", lambda r: r["rows"][9].update(supersedes="SJ-099"), ["ids"]),
    ("his word not verbatim", lambda r: r["his_word"][0].update(verbatim=r["his_word"][0]["verbatim"][:-1]), ["his_word"]),
    ("a committed row edited", "HISTORY", ["history"]),
]


def self_test(S, rec):
    results = []
    for name, mut, expect in MUTATIONS:
        r = copy.deepcopy(rec)
        hist = []
        if mut == "HISTORY":
            old = copy.deepcopy(rec)
            old["rows"][3]["reason"] += " (an earlier wording)"
            hist = [old]
        else:
            mut(r)
        red = sorted(check(r, S, hist))
        results.append({"mutation": name, "expect_red": sorted(expect), "red": red, "as_expected": red == sorted(expect)})
    return {"what": "shapes_judgments_gate.py self-test: the unmutated record first, then one mutation per check",
            "record": REL, "cases": len(results), "as_expected": sum(x["as_expected"] for x in results),
            "results": results}


def main():
    S = Sources()
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
    rows = rec["rows"]
    v = {}
    for r in rows:
        if r.get("kind") == "shape":
            v[r["verdict"]] = v.get(r["verdict"], 0) + 1
    print("SHAPES JUDGMENTS GATE: %s (%d rows; shapes %s)" % (
        "RED" if red else "GREEN", len(rows), " ".join("%s %d" % kv for kv in sorted(v.items()))))
    sys.exit(1 if red else 0)


if __name__ == "__main__":
    main()
