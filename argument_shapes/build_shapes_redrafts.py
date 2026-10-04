#!/usr/bin/env python3
"""The argument-shapes redrafts (V2b, seat l, 2026-10-03): shapes_redrafts_v0_1.json and its record.

gate2 judged V2's pilot in V3 (R0307; shapes_pilot_judgments.json): two AMENDs owed by seat l "in a new row or file,
never the pilot". His word on R0308 adopted the judgment and handed both to this session (R0309). Drafted, not judged:
gate2 judges them in round two (K258).

  SJ-003  life-gift/the-golden-rule-passes-it-on   the statement: Hare's duty restated as weighed, other things equal;
                                                   class (d) and route unchanged
  SJ-008  free-will-defense/a-vale-of-soul-making  the route: (d), no answering locus, terminus via
                                                   suffering-makes-human#long; the statement stands

What this builder does, every value measured at run time:
  - reads the pilot and gate2's judgment record at the md5s it pins; starts each redraft from the pilot's shape of the
    same id, changes only what the row owes, and asserts the changed fields are exactly those;
  - copies each (d)'s terminus from the registered (d) its line reaches (map v1_8, by node, locus and anchor) and from
    register v0_9, never typed (L4's law), and asserts it equals the route the judgment row states;
  - asserts every terminus anchor and every quote in the record verbatim at its source, read at pinned bytes;
  - writes the staging file (bound_for staging, phase S, the pilot's corpus pin). Its shape ids repeat the pilot's on
    purpose: each redraft SUPERSEDES the pilot shape of the same id, so the file validates alone, and the record
    resolves the current set;
  - runs shape_validator_v0_1.py over the staging file alone, and over two resolved views written to scratch: the
    pilot with the two shapes replaced (10 shapes), and the set his word kept (the 5 ACCEPTs and the 2 redrafts).
    Each run is in its own process group, with TMPDIR in scratch.

  python3 argument_shapes/build_shapes_redrafts.py [--check]
Repo-relative. --check rebuilds both files, validator runs included, and compares bytes.
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402
import shape_validator_v0_1 as SV  # noqa: E402

PILOT = ("argument_shapes/shapes_pilot_v0_1.json", "1f9c5da6166b538a90efa6dc7598124e")
MEASURE = ("argument_shapes/shapes_pilot_measure_v0_1.json", "576be8f2c469f84b4bc9ca628d9b41c1")
JUDGMENTS = ("argument_shapes/shapes_pilot_judgments.json", "73503bccdd3ddf8b3a82f280181251d4")
JGATE = ("argument_shapes/shapes_judgments_gate.py", "f56df1e7fdaa82bf3c0f1a11e9622837")
CORPUS = ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1")
MAP = ("adversarial_map_staging/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827")
REGISTER = ("adversarial_map_staging/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351")
VALIDATOR = ("argument_shapes/shape_validator_v0_1.py", "64553b25b6db0ff67edeb87b89178297")
WORDS = ("tools/v38_50_his_words.json", "6f2d0c5e060de228cabe9b6bcc357890")
OUT = "argument_shapes/shapes_redrafts_v0_1.json"
RECORD = "argument_shapes/shapes_redrafts_record_v0_1.json"
PROV = {"phase": "S", "date": "2026-10-03", "seat": "l (V2b, Code)"}

# The redrafts: what each row owes, and what changes. Every other field is the pilot's, asserted unchanged.
REDRAFTS = [
    {"id": "RD-01", "answers": "SJ-003", "shape_id": "life-gift/the-golden-rule-passes-it-on",
     "changes": {"statement": ("You are glad you were brought into existence, and so are nearly all of us. The golden "
                               "rule says do to others what you are glad was done to you. A person who would be glad "
                               "to exist is harmed if we choose never to create them, so their interests are weighed "
                               "with everyone's: other things equal, we ought to create them whenever that adds to the "
                               "total good.")},
     "via": ("joy-outweighs-harms", "long", "a merely possible person can be a genuine beneficiary of being brought into"),
     "reading": ("(d), unchanged. The duty is now bounded twice, by other things equal and by the total good, so the "
                 "reductio at rights-future-generations#long (\"The obligation would be literally infinite\") no longer "
                 "meets it; that answer belongs to the unqualified form gate2 struck. The premise that carries the line "
                 "is untouched: a person who would be glad to exist is harmed by never being created. That is the "
                 "merely-possible-beneficiary premise the (d) at joy-outweighs-harms#long records as its open "
                 "remainder."),
     "quotes": [("corpus", "rights-future-generations", "long", "The obligation would be literally infinite")],
     "pulls": [
         "Wording: 'interests', Hare's own word in the chapter's opening (source 2), where SJ-003's owed line says "
         "'preferences' (the SEP's 'total satisfaction of preference'). In Hare's preference utilitarianism they name "
         "the same thing; gate2 reads whether 'interests' is the better fit.",
         "Omitted for the band: the indexer's abstract (source 3) adds two conditions, the proportionate distribution "
         "held fixed and a floor where the worst-off lives are just worth living. The statement keeps only the total "
         "good, which is the clause that bounds the duty. gate2 reads whether the omission understates Hare.",
         "Attestation is unchanged, because it was not owed. The golden-rule step is attested for Hare's view of "
         "possible people by the SEP (citing his 1975, 1988b and 1988c, not this article) and by Chan 2004; the "
         "article's own opening, through its 1993 reprint, attests the weighing. If gate2 reads the golden-rule step "
         "as better attested by Hare 1975 ('Abortion and the Golden Rule'), adding that citation is a one-line change."],
     "sources_checked": [
         {"what": "the publisher's record of the article (Wiley, through Crossref)",
          "url": "https://api.crossref.org/works/10.1111/j.1467-8519.1988.tb00055.x",
          "supports": "the citation: R. M. Hare, Possible People, Bioethics 2(4), October 1988, pp. 279-293. No abstract.",
          "excerpts": []},
         {"what": "the publisher's record of the article's reprint, chapter 5 of Hare's Essays on Bioethics (Oxford "
                  "University Press, 1993, pp. 67-83, through Crossref); its abstract is the chapter's opening paragraph",
          "url": "https://api.crossref.org/works/10.1093/oso/9780198239833.003.0005",
          "supports": "the weighing, in Hare's own words: when we choose whether to create someone, that possible "
                      "person's interests count",
          "excerpts": ["the interests of that possible person have to be con sidered"],
          "note": "'con sidered' is the record's own line-break artifact, kept verbatim"},
         {"what": "the MEDLINE record of the article, with the Kennedy Institute of Ethics' abstract (PMID 11651921)",
          "url": "https://pubmed.ncbi.nlm.nih.gov/11651921/",
          "supports": "the weighing again, and the bound: Hare's population policy adds people only while the total grows",
          "excerpts": ["the interests of the possible person must be considered",
                       "increasing the population of a society while increasing the total utility"]},
         {"what": "the Stanford Encyclopedia of Philosophy, 'Richard Mervyn Hare', section 6 (Possible People); it "
                  "cites Hare 1975, 1988b and 1988c, not this article",
          "url": "https://plato.stanford.edu/entries/hare/",
          "supports": "the golden-rule step from one's own gladness, other things equal, and the total",
          "excerpts": ["I must prescribe, ceteris paribus, the bringing into existence of others relevantly like me",
                       "so long as this will increase the total satisfaction of preference"]},
         {"what": "the publisher's record of Essays on Bioethics (Oxford University Press, 1993, through Crossref)",
          "url": "https://api.crossref.org/works/10.1093/oso/9780198239833.001.0001",
          "supports": "the harm clause, unchanged from the pilot",
          "excerpts": ["we can harm possible people by preventing them from becoming actual people"]},
         {"what": "K. M. Chan, The Golden Rule and the Potentiality Principle, Journal of Applied Philosophy 21(1), "
                  "2004, pp. 33-42, its abstract (PMID 15148950)",
          "url": "https://pubmed.ncbi.nlm.nih.gov/15148950/",
          "supports": "Hare derived duties to potential people from the golden rule",
          "excerpts": ["R.M. Hare purportedly derived counterintuitive duties to potential people"]}],
     "not_read": ("The full text of the article and of its reprint. The publisher's article page and PhilPapers "
                  "returned 403 to this seat, as the university repository did to gate2; OUP's book page returned "
                  "nothing. The statement claims only what the six records above support. Checked 2026-10-03 (V2b); "
                  "the builder does not re-fetch them.")},
    {"id": "RD-02", "answers": "SJ-008", "shape_id": "free-will-defense/a-vale-of-soul-making",
     "changes": {"class": "d", "answered_by": []},
     "via": ("suffering-makes-human", "long", "evaluate the component (suffering) on its own terms"),
     "reading": ("(d) at HR-02, as SJ-008 states the route; the statement stands. Its conclusion is about the created "
                 "person's own good, and the (d) at suffering-makes-human#long already records the intrapersonal "
                 "instrumental move (\"instrumental necessity: suffering is the causal precondition of goods\") ending "
                 "there."),
     "quotes": [("map", 71, "adversarial_move", "instrumental necessity: suffering is the causal precondition of goods")],
     "pulls": [],
     "sources_checked": [],
     "not_read": None},
]


def md5b(b):
    return hashlib.md5(b).hexdigest()


def at(rel, m):
    return pinned.bytes_at(REPO, rel, m)


def dump(o):
    return (json.dumps(o, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def run_validator(path, scratch):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
    p = subprocess.Popen([sys.executable, VALIDATOR[0], path], cwd=REPO, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, env=env, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        raise
    tail = json.loads(out[out.rfind("\n{") + 1:])
    return {"rc": p.returncode, "verdict": tail["verdict"], "violation_count": tail["violation_count"],
            "shapes": tail["shapes"], "nodes_with_shapes": tail["nodes_with_shapes"]}


def build():
    pilot = json.loads(at(*PILOT).decode("utf-8"))
    meas = json.loads(at(*MEASURE).decode("utf-8"))
    jrec = json.loads(at(*JUDGMENTS).decode("utf-8"))
    corpus = json.loads(at(*CORPUS).decode("utf-8"))
    cmap = json.loads(at(*MAP).decode("utf-8"))
    reg = json.loads(at(*REGISTER).decode("utf-8"))
    words = json.loads(at(*WORDS).decode("utf-8"))
    for rel, m in (VALIDATOR, JGATE):
        assert md5b(open(os.path.join(REPO, rel), "rb").read()) == m, "%s moved" % rel
    assert jrec["judged"]["pilot"]["md5"] == PILOT[1] and jrec["judged"]["measure"]["md5"] == MEASURE[1]
    O = {o["id"]: o for o in corpus["objections"]}
    E = cmap["entries"]
    rows_j = {r["id"]: r for r in jrec["rows"]}
    by_id = {s["shape_id"]: s for s in pilot["shapes"]}
    word = words["excerpts"]["R0308_word"]

    def entry(node, locus, anchor):
        hit = [i for i, e in enumerate(E) if (e["target_id"], e["target_locus"], e["target_anchor"]) == (node, locus, anchor)]
        assert len(hit) == 1 and E[hit[0]]["class"] == "d", "%s#%s %r: want one (d)" % (node, locus, anchor)
        return hit[0], E[hit[0]]

    def register_of(node, locus, anchor):
        found = [(b["bedrock_id"], b["name"], f["facet_id"]) for b in reg["bedrocks"] for f in b["facets"]
                 for t in f["tributaries"] if (t.get("node"), t.get("locus"), t.get("anchor")) == (node, locus, anchor)]
        assert len(found) == 1, "%s#%s: %d register tributaries" % (node, locus, len(found))
        return found[0]

    shapes, rows = [], []
    for rd in REDRAFTS:
        j = rows_j[rd["answers"]]
        assert j["kind"] == "shape" and j["shape_id"] == rd["shape_id"] and j["verdict"] == "AMEND", rd["id"]
        assert j["class_judged"] == "d", rd["id"]
        base = by_id[rd["shape_id"]]
        new = dict(base)
        new.update(rd["changes"])
        new["provenance"] = dict(PROV)
        new = {k: new[k] for k in base}  # the pilot's key order
        changed = sorted(k for k in base if base[k] != new[k])
        assert changed == sorted(set(rd["changes"]) | {"provenance"}), (rd["id"], changed)
        if rd["answers"] == "SJ-003":
            assert changed == ["provenance", "statement"]  # owed: the statement only
        else:
            assert changed == ["answered_by", "class", "provenance"]  # owed: the route only; the statement stands
        n, loc, anc = rd["via"]
        assert anc in SV.locus_text(O[n], loc), "%s: the terminus anchor is not at %s#%s" % (rd["id"], n, loc)
        idx, e = entry(n, loc, anc)
        hr, name, facet = register_of(n, loc, anc)
        terminus = {"via": "%s#%s" % (n, loc), "via_anchor": anc,
                    "bedrock": {"bedrock_name": e["routing"]["residue"]["bedrock_name"],
                                "terminus_routing": e["routing"]["residue"]["terminus_routing"],
                                "register": {"bedrock_id": hr, "name": name, "facet": facet}},
                    "copied_from": {"map_entry": idx, "register": "%s / %s" % (hr, facet)}}
        assert j["route"] == {"via": terminus["via"], "via_anchor": anc, "bedrock": terminus["bedrock"]}, rd["id"]
        quotes = []
        for q in rd["quotes"]:
            if q[0] == "corpus":
                assert q[3] in SV.locus_text(O[q[1]], q[2]), q
                quotes.append({"src": "corpus:%s#%s" % (q[1], q[2]), "quote": q[3]})
            else:
                assert q[3] in E[q[1]][q[2]], q
                quotes.append({"src": "map:#%d.%s" % (q[1], q[2]), "quote": q[3]})
        for q in quotes:
            assert '"%s"' % q["quote"] in rd["reading"], q
        shapes.append(new)
        row = {"id": rd["id"], "shape_id": rd["shape_id"],
               "answers": {"row": j["id"], "verdict": j["verdict"], "owed": j["owed"]},
               "supersedes": {"file": PILOT[0], "md5": PILOT[1], "shape_id": rd["shape_id"]},
               "changed": changed, "class": new["class"],
               "words": {"pilot": SV.wc(base["statement"]), "redraft": SV.wc(new["statement"])},
               "terminus": terminus, "route_equals_the_judged_route": True,
               "reading": rd["reading"], "quotes": quotes}
        if rd["pulls"]:
            row["pulls"] = rd["pulls"]
        if rd["sources_checked"]:
            for s in rd["sources_checked"]:
                assert all(SV.wc(x) < 15 for x in s["excerpts"])
            row["sources_checked"] = rd["sources_checked"]
            row["not_read"] = rd["not_read"]
        rows.append(row)

    per_node = sorted({s["shape_id"].split("/")[0] for s in shapes})
    doc = {"meta": {"source_corpus_md5": CORPUS[1], "source_corpus_objections_md5": SV.objections_digest(corpus),
                    "bound_for": "staging", "shape_coverage": "%d/%d" % (len(per_node), len(O))},
           "shapes": shapes}
    assert doc["meta"]["source_corpus_objections_md5"] == pilot["meta"]["source_corpus_objections_md5"]
    out = dump(doc)

    # the resolved views: the pilot with the superseded shapes replaced; and the set his word kept
    repl = {s["shape_id"]: s for s in shapes}
    superseded = [repl.get(s["shape_id"], s) for s in pilot["shapes"]]
    kept_ids = [r["shape_id"] for r in jrec["rows"] if r["kind"] == "shape" and r["verdict"] in ("ACCEPT", "AMEND")]
    ruled = [s for s in superseded if s["shape_id"] in kept_ids]

    def view(ss):
        nodes = {s["shape_id"].split("/")[0] for s in ss}
        return {"meta": dict(doc["meta"], shape_coverage="%d/%d" % (len(nodes), len(O))), "shapes": ss}

    scratch = tempfile.mkdtemp(prefix="shapes_redrafts_")
    try:
        runs = {}
        for name, payload in (("redrafts_alone", out), ("superseded_view", dump(view(superseded))),
                              ("ruled_view", dump(view(ruled)))):
            if name == "redrafts_alone":
                path = os.path.join(scratch, "redrafts.json")
            else:
                path = os.path.join(scratch, name + ".json")
            open(path, "wb").write(payload)
            runs[name] = run_validator(path, scratch)
            assert runs[name]["rc"] == 0 and runs[name]["verdict"] == "PASS" and runs[name]["violation_count"] == 0, \
                (name, runs[name])
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    runs["redrafts_alone"]["file"] = OUT
    runs["superseded_view"]["what"] = "the pilot's ten shapes in its order, the two superseded ones replaced by these"
    runs["ruled_view"]["what"] = ("the shapes his word on R0308 kept: gate2's five ACCEPTs and these two redrafts; "
                                  "the three REJECTs left out")
    runs["ruled_view"]["shape_ids"] = [s["shape_id"] for s in ruled]
    cls = {}
    for s in ruled:
        cls[s["class"]] = cls.get(s["class"], 0) + 1

    record = {
        "what": ("the two redrafts gate2's V3 judgment owed seat l (SJ-003, SJ-008), V2b, seat l, 2026-10-03; drafted, "
                 "not judged"),
        "state": "DRAFTED, NOT JUDGED. gate2 judges these two redrafts in round two (K258); his word decides.",
        "authority": {"his_word": word["text"], "turn_md5": word["turn"]["turn_md5"], "utc": word["turn"]["utc"],
                      "answers": "R0308", "from": "%s at %s" % (WORDS[0], WORDS[1]),
                      "adopted": ("gate2's judgment (5 ACCEPT, 2 AMEND, 3 REJECT) and V2's hand-off: a fresh seat-l "
                                  "session drafts the two AMENDs")},
        "supersession": ("Each row supersedes the pilot shape of the same shape_id. The pilot stays byte-identical "
                         "(gate2's gate pins it), so the staging file repeats the pilot's ids and validates alone. "
                         "The current set is the pilot with each superseded shape replaced by its redraft: "
                         "'superseded_view' below. Loading the pilot and this file together fails shape-id, as it "
                         "should."),
        "pins": {"redrafts": {"file": OUT, "md5": md5b(out), "bytes": len(out)},
                 "pilot": dict(zip(("file", "md5"), PILOT)), "measure": dict(zip(("file", "md5"), MEASURE)),
                 "judgments": dict(zip(("file", "md5"), JUDGMENTS)), "judgments_gate": dict(zip(("file", "md5"), JGATE)),
                 "corpus": dict(zip(("file", "md5"), CORPUS)), "map": dict(zip(("file", "md5"), MAP)),
                 "register": dict(zip(("file", "md5"), REGISTER)), "validator": dict(zip(("file", "md5"), VALIDATOR)),
                 "his_words": dict(zip(("file", "md5"), WORDS))},
        "rows": rows,
        "validator_runs": runs,
        "after_round_two": {"ruled_set_classes": dict(sorted(cls.items())),
                            "routes": ("(d)s to the map at the successor map's next validator bump (many-peaks and "
                                       "heroism now; these two once judged); the (a) to the corpus in V4 after the "
                                       "successor map's pin; the (b) to the regen queue; the (c) to the intake")},
        "not_moved": ("the pilot, its measurement, its builder, the validator, its control, the schema and gate2's "
                      "records; no corpus or served byte")}
    return out, dump(record)


def main():
    out, rec = build()
    if "--check" in sys.argv:
        ok = (open(os.path.join(REPO, OUT), "rb").read() == out and open(os.path.join(REPO, RECORD), "rb").read() == rec)
        print("SHAPES REDRAFTS: %s" % ("matches the committed redrafts and record" if ok else "DIFFERS"))
        sys.exit(0 if ok else 1)
    open(os.path.join(REPO, OUT), "wb").write(out)
    open(os.path.join(REPO, RECORD), "wb").write(rec)
    print("%s  %s / %d" % (OUT, md5b(out), len(out)))
    print("%s  %s / %d" % (RECORD, md5b(rec), len(rec)))


if __name__ == "__main__":
    main()
